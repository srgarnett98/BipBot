import numpy as np
import ipaddress
import time
import scipy.stats
import socket
import json
import sys
import selectors

from Bipbot_Shared import (
Client
)

import discord

def bipDict(members, game, channel, guild):
    bip_status = {}
    bip_status[members] = members
    bip_status[game] = game
    bip_status[channel] = channel
    bip_status[guild] = guild
    return bip_status

def bipCheck(channel):
    """
    Contains the logic to get the information about a bip
    """

    members = [x for x in channel.members
               if (not x.bot and
                   not x.VoiceState.mute and
                   not x.VoiceState.self_mute)]
    if len(members) !=0:
        print(members)

        bippers = len(members)

        games = []
        for member in members:
            try:
                games.append(member.activities[0].name)
            except:
                games.append("Chatting")
        major_game = scipy.stats.mode(games)
        if games.count(major_game) < 2:
            major_game = 'Various'

        member_names = [member.name for member in members]
        bip_status = self.bipDict(member_names,
                            major_game,
                            channel.name,
                            channel.guild.id)
                            #some kind of hash for the guild
    else:
        bip_status = None

    return bip_status


class bipBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.connected = []
        self.channels = []

        self.loop.create_task(self.open_listen())


    def transmit(self, bip_status):
        for user in self.connected:
            if bip_status[guild] in user.prefs.guilds:
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

    async def every_5_mins(self, channel):
        while True:
            await time.sleep(300)
            bip_status = bipCheck(channel)
            transmit(bip_status)
        return

    async def on_ready(self):
        print("ready")

    async def on_message(self, message):
        if message.content.startswith("$test"):
            await message.channel.send("fuck you")
        elif message.content.startswith("$bipcheck"):
            bip_status = bipCheck(message.channel)
            await message.channel.send(str(bip_status.members))

        return True

    async def open_listen(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('', 65043))
        self.socket.listen()
        self.socket.setblocking(False)

        def create_new_connection(conn, addr):
            ping_size = conn.recv(1)
            ping_size = int.from_bytes(ping_size, byteorder = 'little')
            client_ping = json.loads(conn.recv(ping_size).decode('UTF-8'))
            client = ping_to_client(client_ping)
            client.IP, client.port = addr
            client.time_added = time.time()

            return Connection(client, conn)

        while True:
            conn, addr = await self.loop.sock_accept(self.socket)
            self.connected.append(create_new_connection(conn, addr))

class Connection(object):
    def __init__(self, client, socket):
        self.User = client
        self.socket = socket

    def send_bip_status(self, bip_status):
        bip_json = json.dumps(bip_status)
        bip_json_size = bytes(sys.getsizeof(bip_json))
        self.socket.sendall(bip_json_size)
        self.socket.sendall(bip_json)
        return True

    def recieve_user_update(self, ping_size):
        ping_size = conn.recv(1)
        ping_size = int.from_bytes(ping_size, byteorder = 'little')
        client_ping = json.loads(conn.recv(ping_size).decode('UTF-8'))
        self.User._update(client_ping)
        return True

def ping_to_client(ping):
    client = Client(HostType = 'server')
    client._update(ping)

    return client


def main():

    server = bipBot()
    with open('hash.txt', 'r') as file:
        bipbot_hash = file.readline().strip()
    server.run(bipbot_hash)

if __name__ == "__main__":
    main()
