import PyQt5
from PyQt5.QtCore import(
QLine,
QRect
)
from PyQt5.QtWidgets import(
QApplication,
QWidget,
QGridLayout,
QLineEdit,
QCheckBox,
QComboBox,
QLabel,
QPushButton
)
from PyQt5.QtGui import(
QPixmap
)
import numpy as np
import ipaddress
import time
import scipy.stats
import socket
import json
import sys

from pyqt_custom_objects import(
QPicButton
)

from Bipbot_Shared import (
BaseClass,
Server_props,
BipStatus
)

class BipApp(QWidget):

    def __init__(self):
        super().__init__()

        self.User = Client()
        self.connection = Connection(self.User)

        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        grid.setVerticalSpacing(30)
        grid.setHorizontalSpacing(50)
        self.setLayout(grid)
        #position is a grid of (y, x) coords
        # position = (y, x)

        self._Title = QLabel()
        self._Title.setText('BipBot UI')
        grid.addWidget(self._Title, 0, 0, 1, 2)

        self._nameArea = QLineEdit()
        self._nameArea.setPlaceholderText('Name')
        grid.addWidget(self._nameArea, 1, 0, 1, 2)

        self._LfbTooltip = QLabel()
        self._LfbTooltip.setText('LFB')
        grid.addWidget(self._LfbTooltip, 1, 4, 1, 1)

        self._LfbBox = QCheckBox()
        self._LfbBox.stateChanged.connect(self.LFB_press)
        grid.addWidget(self._LfbBox, 1, 5, 1, 1)

        self._GuildsDrop = QComboBox()
        self._GuildsDrop.currentIndexChanged.connect(self.show_channels_of_guild,
                                                     self._GuildsDrop.currentIndex())
        grid.addWidget(self._GuildsDrop, 2, 0, 1, 2)

        self._GuildsTooltip = QLabel()
        self._GuildsTooltip.setText('Guilds')
        grid.addWidget(self._GuildsTooltip, 2, 2, 1, 2)

        self._ChannelsDrop = QComboBox()
        grid.addWidget(self._ChannelsDrop, 2, 3, 1, 2)

        self._ChannelsTooltip = QLabel()
        self._ChannelsTooltip.setText('Channels')
        grid.addWidget(self._ChannelsTooltip, 2, 5, 1, 1)

        self._NewGuildArea = QLineEdit()
        self._NewGuildArea.setPlaceholderText('Guild ID')
        grid.addWidget(self._NewGuildArea, 3, 0, 1, 2)

        self._NewGuildButton = QPushButton()
        self._NewGuildButton.setText('Add')
        self._NewGuildButton.clicked.connect(self.add_guild)
        grid.addWidget(self._NewGuildButton, 3, 2, 1, 1)

        self._RemoveCurrentGuild = QPushButton()
        self._RemoveCurrentGuild.setText('Remove Selected Guild')
        grid.addWidget(self._RemoveCurrentGuild, 4, 0, 1, 3)

        picture = QPixmap('settings-cog.png')
        settings_height = self.frameGeometry().height()
        settings_width = self.frameGeometry().width()
        self._SettingsButton = QPicButton(picture, QRect(0,
                                                         0,
                                                         settings_height/9,
                                                         settings_width/16))
        grid.addWidget(self._SettingsButton, 5, 5, 1, 1)


        self._channelIDArea = QLineEdit()
        self._excludesArea = QLineEdit()


        #self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('BipApp')

        self.show()

    def LFB_press(self):
        print('Lfb pressed')
        self.User.LFB = self._LfbBox.isChecked()
        return

    def add_guild(self):
        print('add guild')
        self.connection.request_guild_channel_ids(int(self._NewGuildArea.text()))
        print(self._NewGuildArea.text())
        self.update_listed_guilds()
        return

    def update_listed_guilds(self):
        self._GuildsDrop.clear()
        for key, value in self.User.guilds.items():
            self._GuildsDrop.addItem(value, key)
        return

    def show_channels_of_guild(self, index):
        self._ChannelsDrop.clear()
        relevant_channels = []
        print(self._GuildsDrop.itemData(index))
        for channel_id, channel_tuple in self.User.channels.items():
            if channel_tuple[1] == self._GuildsDrop.itemData(index):
                relevant_channels.append(channel_tuple[0])
        self._ChannelsDrop.addItems(relevant_channels)

class Connection(object):
    def __init__(self, User):
        self.server = Server_props()
        self.server.IP = '127.0.0.1'
        self.server.port = 65019
        self.User = User
        self.start_socket()

    def start_socket(self):
        '''
        Sends a ping to the server containing client info, waits until server
        responds
        '''
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server.IP,
                             self.server.port))

        print(self.User.__dict__)
        self.send_client_status()

        ping_size = self.socket.recv(8)
        ping_size = int.from_bytes(ping_size, byteorder = 'big')
        ready = json.loads(self.socket.recv(ping_size).decode('UTF-8'))

        if ready == 'ready':
            print('ready')
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
        data = self.User.__dict__
        self.send_data(data)
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
            return
        self.User.guilds[guild_id] = voice_ids.pop('guild_name')
        for key, value in voice_ids.items():
            if key is not 'guild_name':
                self.User.channels[value] = (key, guild_id)

        self.send_client_status()
        return True

    async def recieve_server_ping(self):
        try:
            ping_size = await self.loop.sock_recv(self.socket, 8)
            ping_size = int.from_bytes(ping_size, byteorder = 'little')
            server_ping = await self.loop.sock_recv(self.socket, ping_size)
            server_ping = json.loads(server_ping.decode('UTF-8'))
            process_ping(self, server_ping)
        except Exception:
            print('Connection closed')
        finally:
            return

        self.show()

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

        channels: dict of tuple (name : string, guild id : int)
            Dict index is the channel id

        guilds: dict of strings
            dict keys are the guild_id, dict strings are the guild names

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
        self.channels = {}
        self.guilds = {}
        self.notifications = True
        self.LFB = False
        self.IP = None
        self.port = 65034

    def __dict_current__(self):
        dict = self.__dict__
        for key, value in dict.items():
            dict[key] = copy.deepcopy(value)
        return dict

def process_ping(connection, ping):
    '''
    code that takes a ping and does whatever that ping was designed to do
    '''
    return

def bip_message(bip_status):
    message = ""
    message += str(len(bip_status[members])) + " person bip in channel "
    message += str(bip_status[channels]) + ", playing "
    message += str(bip_status[game])

def bip_change(bip_status, prefs):
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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = BipApp()

    sys.exit(app.exec_())
