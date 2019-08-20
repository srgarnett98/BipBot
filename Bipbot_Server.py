import numpy as np
import ipaddress
import time
import scipy.stats
import socket
import pickle
import sys
import selectors
import asyncio

from Bipbot_Shared import (
BipStatus,
BaseClass
)

import discord

def bipCheck(channel):
    '''
    Contains the logic to get the information about a bip

    params:
    -------

        channel: discord.voice_channel object
            The voice channel which a bip is being checked for

    returns:
    -------

        bip_status: BipStatus object
            A BipStatus struct describing the bip
    '''
    members = [x for x in channel.members
               if (not x.bot and
                   not x.voice.mute and
                   not x.voice.self_mute)]
    if len(members) !=0:

        bippers = len(members)

        games = []
        for member in members:
            try:
                games.append(member.activities[0].name)
            except:
                games.append("Chatting")
        major_game = scipy.stats.mode(games).mode[0]
        if games.count(major_game) < 2 and len(members) > 1:
            major_game = 'Various'

        member_names = [member.name for member in members]
        bip_status = BipStatus(member_names,
                            major_game,
                            channel.name,
                            channel.id,
                            channel.guild.name,
                            channel.guild.id)
                            #some kind of hash for the guild
    else:
        bip_status = BipStatus([],
                             None,
                             channel.name,
                             channel.id,
                             channel.guild.name,
                             channel.guild.id)

    return bip_status


class bipBot(discord.Client):
    '''
    BipBot discord client, inherits from discord.Client

    params:
    ---------

        port: int
            the port which the program recieves new connections on

    Attributes:
    ---------

        connected: list of Connection objects
            A list of connected users, represented by their Connection objects.
            Connected user details can be found by connected[i].User

        listen_port: int
            the port which the program recieves new connections on

    Methods:
    ---------
        transmit( bip_status : BipStatus object)
            transmits a bip status change to all necessary parties

        async on_ready:
            Code to run when the bot has first set up

        async on_message( message : discord.message object)
            Code to run on message in a text channel. This is hwere to add text
            commands

        async on_group_join( channel : discord.voice_channel object,
                              user: discord.User object)
            When a user joins, rechecks the bip status, and then transmits that
            out

        async on_group_leave( channel : discord.voice_channel object,
                              user: discord.User object)
            When a user leave, rechecks the bip status, and then transmits that
            out

        async every_5_mins( channel : discord.voice_channel object)
            When a new user joins, rechecks the bip status, and then transmits that
            out

        async open_listen:
            creates a socket which is listening on all IPs for new connections.
            When a connection is formed, it forms a Connection object for that user
            and adds it to the connected list

    '''
    def __init__(self, port):
        super().__init__()
        self.connected = []
        self.listen_port = port
        self.loop.create_task(self.open_listen())


    def transmit(self, bip_status):
        for user in self.connected:
            if bip_status.channel in user.channels:
                user.send_bip_status(bip_status)
        return

    async def on_group_join(self, channel, user):
        bip_status = bipCheck(channel)
        transmit(bip_status)
        return

    async def on_group_leave(self, channel, user):
        bip_status = bipCheck(channel)
        transmit(bip_status)
        return

    async def every_5_mins(self):
        await asyncio.sleep(300)
        for guild in self.guilds:
            for channel in guild.voice_channels:
                bip_status = bipCheck(channel)
                transmit(bip_status)
        return

    async def on_ready(self):
        print("ready")

    async def on_message(self, message):
        if message.content.startswith("$test"):
            await message.channel.send("fuck you")
        elif message.content.startswith("$bipcheck"):
            for voice_channel in message.channel.guild.voice_channels:
                bip_status = bipCheck(voice_channel)
                await message.channel.send(bip_status.__dict__)
        elif message.content.startswith("$connected"):
            for user in self.connected:
                await message.channel.send(user.name)
        return True

    async def open_listen(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', self.listen_port))
        self.socket.listen()
        self.socket.setblocking(False)

        while True:
            conn, addr = await self.loop.sock_accept(self.socket)

            ping_size = await self.loop.sock_recv(conn, 8)
            ping_size = int.from_bytes(ping_size, byteorder = 'big')
            client_ping = await self.loop.sock_recv(conn, ping_size)
            client_ping = pickle.loads(client_ping)
            client = ping_to_client(client_ping)
            client.IP, client.port = addr
            print('New connection')
            print(addr)

            self.connected.append(Connection(client, conn, self.loop, self.guilds))

class Connection(object):
    '''
    Object which holds a users socket connection and their details. Is constantly
    listening for messages on this socket.

    Params / Attributes:
    --------

        User: Client object
            The details of the client, created by ping_to_client in the initial
            message

        socket: socket.socket object
            The socket between the client and the server

        event_loop: asyncio.event_loop object, belonging to BipBot/discord.Client
            The discord clients event loop, such that the open listening can be
            added as an async event

        guilds: list of discord.guild objects
            A list of the guilds which BipBot has permissions on. This is super
            dumb and will be changed when I remember how to pass stuff through
            properly

    Methods:
    ---------

        send_data( data : any form)
            Sends whatever data is passed to it as a pickle to the client. Prefaces
            this with a 64 bit int representation of how many bytes (bits? idk)
            the client should be expecting. 64 bit int is way over the top, but
            its 64 bits, idgaf

        send_guild_channel_ids( guild_id : int)
            Uses the bipbots guilds to find the channel ids of all voice channels
            under that guilds. Then sends these channel ids to the user.

            Plan on the user using bipbot to find the guild ID, then using this
            function to find the channel ids under it

        async recieve_user_message
            Constantly listens for a message from a user, and then acts upon it.
            Is likely to have a massive string of if commands downstream of this
            to determine what the user wants
    '''
    def __init__(self, User, socket, event_loop, guilds):
        self.User = User
        self.socket = socket
        self.socket.setblocking(False)
        self.event_loop = event_loop
        self.guilds = guilds
        self.event_loop.create_task(self.recieve_user_message())
        self.send_data('ready')

    def send_data(self, data):
        data = pickle.dumps(data)
        length = (sys.getsizeof(data)).to_bytes(8, byteorder = 'big')
        self.socket.sendall(length)
        self.socket.sendall(data)
        return True

    def send_guild_channel_ids(self, guild_id):
        voice_ids = {}
        for guild in self.guilds:
            if guild.id == guild_id:
                for voice_channel in guild.voice_channels:
                    voice_ids[voice_channel.name] = voice_channel.id
                voice_ids['guild_name'] = guild.name
        if voice_ids == {}:
            voice_ids = None
        self.send_data(voice_ids)

        return True

    async def recieve_user_message(self):
        try:
            self.socket.setblocking(False)
            ping_size = await self.event_loop.sock_recv(self.socket, 8)
            ping_size = int.from_bytes(ping_size, byteorder = 'big')
            client_ping = await self.event_loop.sock_recv(self.socket,
                                                          ping_size)
            client_ping = pickle.loads(client_ping)
            if 'get_channels_of_guild' in client_ping:
                self.send_guild_channel_ids(client_ping['get_channels_of_guild'])
            else:
                self.User._update(client_ping)
            self.event_loop.create_task(self.recieve_user_message())
        except Exception:
            print('connection closed')
        finally:
            return True

class Client(BaseClass):
    '''
    A struct containing all the relevant details of a client. If the host is a
    server, will also contain what game they are playing, and when they were added.

    Time added is for the future, when the bot contains a list of past users and
    such so i can collect data on all my friends. WHEN I DO THIS I WILL WORK BY
    GDPR LAWS AND ASK FOR CONSENT DW

    Attributes:
    -------

        name: string
            The users name, will be self set and disconnected from discord name

        excluded_games: list of string
            A list of which games the user doesnt want to recieve bips about

        channels: list of tuple (channel name: string, channel_id: int)
            A list of channels which the user is interested in and will recieve
            bips for.

        guilds: list of tuple (guild name: string, guild_id: int)
            A list of the guilds which the user is interested in and will recieve
            bips for

        notifications: bool
            If False, user will not recieve push notifications of bips

        LFB: bool
            Looking For Bip status. if enough people LFB then it will trigger a
            bip alert

        IP: string formatted as IPV4
            The IP to which the client is on. Dont know if I need this

        port: int
            The port to which the client is on. Dont know if i need this

        IF HOSTTYPE = 'SERVER':

        gamestate: string
            The game which the user is playing. WARNING: spotify may fuck this

        time_added: float
            time which the user was added to the server, for database uses.
        '''
    def __init__(self):
        super().__init__()
        self.name = ""
        self.excluded_games = []
        self.channels = []
        self.guilds = []
        self.notifications = True
        self.LFB = False
        self.IP = None
        self.port = 65034
        self.gamestate = ""
        self.time_added = None

class Channel(BaseClass):
    def __init__(self,
                 name,
                 id,
                 guild_id,
                 big_req,
                 smol_req,
                 ignore,
                 bip_status):
        self.name = name
        self.id = id
        self.guild_id = guild_id
        self.big_req = big_req
        self.smol_req = smol_req
        self.ignore = ignore
        self.bip_status = bip_status

def ping_to_client(ping):
    '''
    converts a ping consisting of a dict of the users attributes, into a new
    Client object.

    Placeholder
    '''
    client = Client()
    client._update(ping)

    return client


def main():
    try:
        server = bipBot(port = 65019)
        with open('hash.txt', 'r') as file:
            bipbot_hash = file.readline().strip()
        server.run(bipbot_hash)
    except Exception:
        import traceback as tb
        tb.print_exc(Exception)

    finally:
        server.socket.close()
        for connection in server.connected:
            connection.socket.close()

if __name__ == "__main__":
    main()
