import numpy as np
import time
import ipaddress

def bip_message(bip_status):
    message = ""
    message += str(len(bip_status[members])) + " person bip in channel "
    message += str(bip_status[channels]) + ", playing "
    message += str(bip_status[game])

async def bip_change(bip_status, prefs):
    if (bip_status[channel] in prefs.channels):
        if bip_status[game] in prefs.excludes:
            icon_set("orange")
        elif len(bip_status[members]) == 2 and bip_status[game] != 'Various':
            icon_set("blue")
            if settings.smol_bip and settings.alerts:
                alert(bip_message(bip_status))
        elif len(bip_status[members]) > 2:
            icon_set("green")
            if settings.alerts:
                alert(bip_message(bip_status))
        elif len(bip_status[members]) <2:
            icon_set("red")

class BaseClass(object):
    def _update(change_dict):
        for change_key, change_value in change_dict.items():
            setattr(self, change_key, change_value)

class _Preferences(BaseClass):
    """
    """
    def __init__(self):
        self.excluded_games = []
        self.subbed_channels = []
        self.active_guilds = []
        self.notifications_on = True

class _Settings(BaseClass):
    """
    """
    def __init__(self):
        self.uhhhhh = False

class Client_status(BaseClass):

    """
    dw a
    """
    def __init__(self, HostType = 'client'):
        self.name = ""
        self.prefs = _Preferences()
        self.settings = _Settings()
        self.LFB = False
        if HostType == 'server':
            self.gamestate = ""
            self.IP = None
            self.port = 65034
            self.time_added = None

class Server_status(BaseClass):

    """
    dw a
    """
    def __init__(self, HostType = 'client'):
        self.IP = None
        self.port = 65034

    async def update_connection(self, ping):
        self.IP = ping.sender_IP
        self.port = ping.sender_port


class ping(BaseClass):
    def __init__(self, target_info, sender_info):
        self.sender = Client_status()
        self.sender._update(sender_info.__dict__)

        self.target = Client_status()
        self.target._update(target_info.__dict__)

class Bip_status(BaseClass):
    def
