import numpy as np
import time
import copy

class BaseClass(object):
    '''
    Easy way to update objects using a single dict, without worrying about
    mutability and such. This will probably change at some point
    '''
    def _update(self, change_dict):
        for change_key, change_value in change_dict.items():
            setattr(self, change_key, copy.deepcopy(change_value))

class BipStatus(BaseClass):
    '''
    C-like struct containing information about a bip to be sent to a client

    params:
    ---------

        members: list of strings
            Each member is a string name. I have no reason to give them ID's at this
            point

        game: string
            The name of the game the majority of members are playing. Can also be
            chatting or various

        channel: string
            The name of the voice channel which the bip is referring to

        channel_id: int
            The discord id for that voice channel

        guild: string
            The name of the guild which the bip is referring to

        guild_id: int
            The discord id for that guild
    '''
    def __init__(self, members, game,
                       channel, channel_id,
                       guild, guild_id):
        self.members = members
        self.game = game
        self.channel = channel
        self.channel_id = channel_id
        self.guild = guild
        self.guild_id = guild_id


class Server_props(BaseClass):

    """
    Properties of the server from the perspective of the user
    This seems extraneous

    Attributes:
    --------
        IP: string formatted as IPV4
            IP of the server

        port: int
            port of the server

    """
    def __init__(self):
        super().__init__()
        self.IP = None
        self.port = 65034
