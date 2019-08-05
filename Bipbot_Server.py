import numpy as np
import ipaddress
import time

from Bipbot_Shared import (
Client
)

import discord
import PyQt5

def bipDict(members, game, channel, guild, status):
    bip_status = {}
    bip_status[members] = members
    bip_status[game] = game
    bip_status[channel] = channel
    bip_status[guild] = guild
    bip_status[status] = status
    return bip_status

def transmit(bip_status, Users):
    for member in Users:

    return True

def bipCheck(channel):
    """
    Contains the logic to check whether a big bip is in progress.
    """
    print("bipCheck start")

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

        if bippers > 2 or (bippers == 2 and major_game != 'Various'):
            bip_status = self.bipDict(members, major_game, channel, guild, True)
        else:
            bip_status = self.bipDict(members, major_game, channel, guild, False)
    else:
        bip_status = None

    return bip_status


class bipBot(discord.Client):
    def __init__(self):
        self.connected = connections()



    async def on_group_join(self, channel, user):
            bip_status = bipCheck(channel)
            transmit(bip_status, self.connected.members)
    async def on_group_leave(self, channel, user):
            bip_status = bipCheck(channel)
            transmit(bip_status, self.connected.members)

    async def on_ready(self):
        #code to run on first time startup
        print("ready")

        #load settings

        #Load gang members

        #Load Chat commands

    async def on_message(self, message):
        #code to run when a message is sent to chat

        if message.content.startswith("$test"):
            await message.channel.send("fuck you")


class connections:
    def __init__(self):
        self.members = []

    async def update_connection(self, ping):
        User = Client(HostType = 'server')
        User.name = ping.name
        User.IP = ping.sender_IP
        User.prefs._update(ping.prefs.__dict__)
        User.settings._update(ping.settings.__dict__)
        user.LFB = ping.LFB
        self.time_added = ping.time

        if User not in self.members:
            for c, member in enumerate(members):
                if member.IP == User.IP and member.port == User.port:
                    members.remove(c)
            self.members.append(User)





bipBot = bipBot()
bipBot.run("NTcyMDA2NjM2NDIwNDY0NjQw.XMWH1Q.sLvRAf_9UktYaH_u_9eQ_Nk-Rwc")
