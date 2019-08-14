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

class Client(BaseClass):
    '''
    A struct containing all the relevant details of a client. If the host is a
    server, will also contain what game they are playing, and when they were added.

    Time added is for the future, when the bot contains a list of past users and
    such so i can collect data on all my friends. WHEN I DO THIS I WILL WORK BY
    GDPR LAWS AND ASK FOR CONSENT DW

    params:
    -------

        HostType: 'client' or 'server'
            If hosttype is server, adds gamestate and time_added as attributes

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
    def __init__(self, HostType = 'client'):
        super().__init__()
        self.name = ""
        self.excluded_games = []
        self.channels = []
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
