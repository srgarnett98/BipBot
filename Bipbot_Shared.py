import numpy as np
import time
import copy

class BaseClass(object):
    def _update(self, change_dict):
        for change_key, change_value in change_dict.items():
            setattr(self, change_key, copy.deepcopy(change_value))

class Client(BaseClass):

    """
    dw a
    """
    def __init__(self, HostType = 'client'):
        super().__init__()
        self.name = ""
        self.excluded_games = []
        self.excluded_channels = []
        self.guilds = []
        self.notifications = True
        self.LFB = False
        self.IP = None
        self.port = 65034
        if HostType == 'server':
            self.gamestate = ""
            self.time_added = None

class Server_props(BaseClass):

    """
    dw a
    """
    def __init__(self, HostType = 'client'):
        super().__init__()
        self.IP = None
        self.port = 65034

    async def update_connection(self, ping):
        self.IP = ping.sender_IP
        self.port = ping.sender_port


class ping(BaseClass):
    def __init__(self, target_info, sender_info):
        super().__init__()
        self.sender = Client_status()
        self.sender._update(sender_info.__dict__)

        self.target = Client_status()
        self.target._update(target_info.__dict__)
