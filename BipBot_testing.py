import numpy as np
import ipaddress
import time
import scipy.stats
import socket
import json
import sys

from Bipbot_Shared import (
Client,
Server_props,
BipStatus
)

import discord

class BipStatus(object):
    def __init__(self, members, game,
                       channel, channel_id,
                       guild, guild_id):
        self.members = members
        self.game = game
        self.channel = channel
        self.channel_id = channel_id
        self.guild = guild
        self.guild_id = guild_id

class Connection(object):
    def __init__(self):
        self.server = Server_props()

    def start_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server.IP,
                             self.server.port))
        data = client.__dict__
        data = json.dumps(data)
        self.socket.sendall(bytes([sys.getsizeof(data)]))
        self.socket.sendall(bytes(data, 'UTF-8'))

        ping_size = self.socket.recv(8)
        ping_size = int.from_bytes(ping_size, byteorder = 'big')
        ready = json.loads(self.socket.recv(ping_size).decode('UTF-8'))

        if ready == 'ready':
            return True
        else:
            return False

    def send_data(self, data):
        data = json.dumps(data)
        length = (sys.getsizeof(data)).to_bytes(8, byteorder = 'big')
        self.socket.sendall(length)
        self.socket.sendall(bytes(data, 'UTF-8'))
        return True

    def send_client_status(self):
        data = client.__dict__
        print(data)
        self.send_data(data)
        print('sent client data')
        return

    def request_guild_channel_ids(self, guild_id):
        print('requesting guild ids')
        data = {'get_channels_of_guild': guild_id}
        self.send_data(data)
        print('sent guild ids')

        ping_size = self.socket.recv(8)
        ping_size = int.from_bytes(ping_size, byteorder = 'big')
        print(ping_size)
        voice_ids = json.loads(self.socket.recv(ping_size).decode('UTF-8'))
        if voice_ids is None:
            print('guild id not recognised')
        for key, value in voice_ids.items():
            client.channels.append((key, value))

        print(client.channels)

        self.send_client_status()
        return True

    def recieve_server_ping(self):
        ping_size = self.socket.recv(8)
        ping_size = int.from_bytes(ping_size, byteorder = 'little')
        server_ping = json.loads(self.recv(ping_size).decode('UTF-8'))
        try:
            channel_id = server_ping['channel_id']
            bip_statuses[channel_id] = BipStatus(
                server_ping['members'],
                server_ping['game'],
                server_ping['channel'],
                server_ping['channel_id'],
                server_ping['guild'],
                server_ping['guild_id']
            )
        except:
            print('message style not recognised')
        return

client = Client(HostType = 'client')
client.name = 'test'
client.IP = '127.0.0.1'
client.guilds.append(393544638201331712)

connection = Connection()
connection.server.IP = '127.0.0.1'
connection.server.port = 65014
print(connection.server.__dict__)
connection.start_socket()


connection.request_guild_channel_ids(client.guilds[0])

time.sleep(2)
