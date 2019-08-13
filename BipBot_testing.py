import numpy as np
import ipaddress
import time
import scipy.stats
import socket
import json
import sys

from Bipbot_Shared import (
Client,
Server_props
)

import discord

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

        time.sleep(1)
        ping_size = self.socket.recv(1)
        ping_size = int.from_bytes(ping_size, byteorder = 'little')
        client_ping = json.loads(self.socket.recv(ping_size).decode('UTF-8'))
        print(client_ping)

        return True

    def send_client_status(self, client_status):
        return

    def recieve_server_update(self, server_update):
        #when a packet comes via this connection
        #async somehow
        return

client = Client(HostType = 'client')
client.name = 'test'
client.IP = '127.0.0.1'

connection = Connection()
connection.server.IP = '127.0.0.1'
connection.server.port = 65043
print(connection.server.__dict__)
connection.start_socket()
