import PyQt5
from PyQt5.QtCore import(
QLine,
QRect
)
from PyQt5.QtWidgets import(
QApplication,
QWidget,
QErrorMessage,
QGridLayout,
QLineEdit,
QCheckBox,
QComboBox,
QLabel,
QPushButton
)
from PyQt5.QtGui import(
QPixmap,
QIntValidator
)
import numpy as np
import ipaddress
import time
import scipy.stats
import socket
import pickle
import sys
import asyncio

from pyqt_custom_objects import(
QPicButton
)

from Bipbot_Shared import (
BaseClass,
Server_props,
BipStatus
)

class SettingsWindow(QWidget):
    def __init__(self, User):
        super().__init__()

        self.User = User

        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        grid.setVerticalSpacing(50)
        grid.setHorizontalSpacing(50)
        self.setLayout(grid)

        self._NotificationsLabel = QLabel()
        self._NotificationsLabel.setText('Notifications')
        grid.addWidget(self._NotificationsLabel, 0, 0, 1, 2)

        self._NotificationsButton = QCheckBox()
        self._NotificationsButton.stateChanged.connect(self.notifications_click)
        grid.addWidget(self._NotificationsButton, 0, 2, 1, 1)


        self.setWindowTitle('Preferences')
        self.setGeometry(300, 100, 300, 300)

    def open(self):
        self.show()

    def update(self):
        self._NotificationsButton.setChecked(self.User.notifications)


    def notifications_click(self):
        self.User.notifications = self._NotificationsButton.isChecked()
        self.User.save_to_file()
        return

class BipApp(QWidget):

    def __init__(self):
        super().__init__()

        self.User = Client()
        self.bip_status = BipStatus(members = [],
                                    game = None,
                                    channel = None,
                                    channel_id = None,
                                    guild = None,
                                    guild_id = None)
        self.loop = asyncio.new_event_loop()

        self.initUI()
        self.set_default_states()

        self.connection = Connection(self.User)

    def initUI(self):

        grid = QGridLayout()
        grid.setVerticalSpacing(30)
        grid.setHorizontalSpacing(50)
        self.setLayout(grid)
        #position is a grid of (y, x) coords
        # position = (y, x)

        self._Settings = SettingsWindow(self.User)

        self._Title = QLabel()
        self._Title.setText('BipBot UI')
        grid.addWidget(self._Title, 0, 0, 1, 4)

        self._NameArea = QLineEdit()
        self._NameArea.setPlaceholderText('Name')
        self._NameArea.textChanged.connect(self.update_name)
        grid.addWidget(self._NameArea, 1, 0, 1, 4)

        self._LfbTooltip = QLabel()
        self._LfbTooltip.setText('LFB')
        grid.addWidget(self._LfbTooltip, 1, 8, 1, 2)

        self._LfbBox = QCheckBox()
        self._LfbBox.stateChanged.connect(self.LFB_press)
        grid.addWidget(self._LfbBox, 1, 10, 1, 2)

        self._GuildsDrop = QComboBox()
        self._GuildsDrop.currentIndexChanged.connect(self.show_channels_of_guild,
                                                     self._GuildsDrop.currentIndex())
        grid.addWidget(self._GuildsDrop, 2, 0, 1, 4)

        self._GuildsTooltip = QLabel()
        self._GuildsTooltip.setText('Guilds')
        grid.addWidget(self._GuildsTooltip, 2, 4, 1, 2)

        self._ChannelsDrop = QComboBox()
        self._ChannelsDrop.currentIndexChanged.connect(self.show_channel_settings,
                                                     self._ChannelsDrop.currentIndex())
        grid.addWidget(self._ChannelsDrop, 2, 6, 1, 4)

        self._ChannelsTooltip = QLabel()
        self._ChannelsTooltip.setText('Channels')
        grid.addWidget(self._ChannelsTooltip, 2, 10, 1, 3)

        self._NewGuildArea = QLineEdit()
        self._NewGuildArea.setPlaceholderText('Guild ID')
        grid.addWidget(self._NewGuildArea, 3, 0, 1, 4)

        self._NewGuildButton = QPushButton()
        self._NewGuildButton.setText('Add')
        self._NewGuildButton.clicked.connect(self.add_guild)
        grid.addWidget(self._NewGuildButton, 3, 4, 1, 2)

        self._ChannelBipNumberLabel = QLabel()
        self._ChannelBipNumberLabel.setText('Required to bip:')
        grid.addWidget(self._ChannelBipNumberLabel, 3, 6, 1, 3)

        self._ChannelBigBipNumber = QLineEdit()
        self._ChannelBigBipNumber.setValidator(QIntValidator())
        self._ChannelBigBipNumber.setPlaceholderText('Big')
        self._ChannelBigBipNumber.textChanged.connect(self.bigbip_change)
        grid.addWidget(self._ChannelBigBipNumber, 3, 9, 1, 2)

        self._ChannelSmolBipNumber = QLineEdit()
        self._ChannelSmolBipNumber.setValidator(QIntValidator())
        self._ChannelSmolBipNumber.setPlaceholderText('Smol')
        self._ChannelSmolBipNumber.textChanged.connect(self.smolbip_change)
        grid.addWidget(self._ChannelSmolBipNumber, 3, 11, 1, 2)

        self._RemoveCurrentGuild = QPushButton()
        self._RemoveCurrentGuild.setText('Remove Selected Guild')
        self._RemoveCurrentGuild.clicked.connect(self.remove_guild,
                                                 self._GuildsDrop.currentIndex())
        grid.addWidget(self._RemoveCurrentGuild, 4, 0, 1, 6)

        self._IgnoreChannelTooltip = QLabel()
        self._IgnoreChannelTooltip.setText('Ignore Selected Channel')
        grid.addWidget(self._IgnoreChannelTooltip, 4, 6, 1, 4)

        self._IgnoreChannelBox = QCheckBox()
        self._IgnoreChannelBox.stateChanged.connect(self.ignore_channel_press)
        grid.addWidget(self._IgnoreChannelBox, 4, 10, 1, 2)

        picture = QPixmap('settings-cog.png')
        settings_height = self.frameGeometry().height()
        settings_width = self.frameGeometry().width()
        self._SettingsButton = QPicButton(picture, QRect(0,
                                                         0,
                                                         settings_height/9,
                                                         settings_width/16))
        self._SettingsButton.clicked.connect(self._Settings.open)
        grid.addWidget(self._SettingsButton, 5, 10, 1, 2)


        self._channelIDArea = QLineEdit()
        self._excludesArea = QLineEdit()


        #self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('BipApp')

        self.show()

    def set_default_states(self):
        self.User.load_from_file()

        self._NameArea.setText(self.User.name)
        self._LfbBox.setChecked(False)
        self.update_listed_guilds()
        self.show_channels_of_guild(self._GuildsDrop.currentIndex())
        self._Settings.update()

    def LFB_press(self):
        self.User.LFB = self._LfbBox.isChecked()
        return

    def update_name(self):
        self.User.name = self._NameArea.text()
        self.User.save_to_file()
        return

    def add_guild(self):
        try:
            int(self._NewGuildArea.text())
        except Exception:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('Guild id must be int. Try $guildID in the required discord text channel')
            error_dialog.exec()
            return
        self.connection.request_guild_channel_ids(int(self._NewGuildArea.text()))
        self.update_listed_guilds()
        self.User.save_to_file()
        return

    def remove_guild(self, index):
        guild_id = self._GuildsDrop.itemData(index)
        self.User.guilds.pop(guild_id)
        self.update_listed_guilds()
        self.User.save_to_file()
        return

    def update_listed_guilds(self):
        self._GuildsDrop.clear()
        for key, value in self.User.guilds.items():
            self._GuildsDrop.addItem(value, int(key))
        return

    def show_channels_of_guild(self, index):
        self._ChannelsDrop.clear()
        relevant_channels = []
        for channel_id, channel in self.User.channels.items():
            if channel.guild_id == self._GuildsDrop.itemData(index):
                self._ChannelsDrop.addItem(channel.name,
                                           (channel_id))

    def show_channel_settings(self, index):
        try:
            channel = self.User.channels[self._ChannelsDrop.itemData(index)]
        except:
            return
        try:
            self._ChannelBigBipNumber.setText(str(channel.big_req))
        except Exception:
            self._ChannelBigBipNumber.setText('')
        try:
            self._ChannelSmolBipNumber.setText(str(channel.smol_req))
        except Exception:
            self._ChannelSmolBipNumber.setText('')
        try:
            self._IgnoreChannelBox.setChecked(channel.ignore)
        except:
            self._IgnoreChannelBox.setChecked(False)

        return

    def bigbip_change(self):
        try:
            index = self._ChannelsDrop.currentIndex()
            channel = self.User.channels[self._ChannelsDrop.itemData(index)]
            big_req = int(self._ChannelBigBipNumber.text())
            self.User.channels[channel.id].big_req = big_req
            self.User.save_to_file()
        except Exception:
            pass

    def smolbip_change(self):
        try:
            index = self._ChannelsDrop.currentIndex()
            channel = self.User.channels[self._ChannelsDrop.itemData(index)]
            smol_req = int(self._ChannelSmolBipNumber.text())
            self.User.channels[channel.id].smol_req = smol_req
            self.User.save_to_file()
        except:
            pass

    def ignore_channel_press(self):
        try:
            index = self._ChannelsDrop.currentIndex()
            channel = self.User.channels[self._ChannelsDrop.itemData(index)]
            ignore = int(self._IgnoreChannelBox.isChecked())
            self.User.channels[channel.id].ignore = ignore
            self.User.save_to_file()
        except:
            pass
        return


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
        ready = pickle.loads(self.socket.recv(ping_size))

        if ready == 'ready':
            print('ready')
            return True
        else:
            return False

    def send_data(self, data):
        data = pickle.dumps(data)
        length = (sys.getsizeof(data)).to_bytes(8, byteorder = 'big')
        self.socket.sendall(length)
        self.socket.sendall(data)
        return True

    def send_client_status(self):
        data = self.User.__dict__
        self.send_data(data)
        return

    def request_guild_channel_ids(self, guild_id):
        data = {'get_channels_of_guild': guild_id}
        self.send_data(data)

        ping_size = self.socket.recv(8)
        ping_size = int.from_bytes(ping_size, byteorder = 'big')
        voice_ids = pickle.loads(self.socket.recv(ping_size))
        if voice_ids is None:
            print('guild id not recognised')
            return
        if guild_id not in self.User.guilds:
            self.User.guilds[guild_id] = voice_ids.pop('guild_name')
            for key, value in voice_ids.items():
                if key is not 'guild_name':
                    self.User.channels[value]=Channel(name = key,
                                                  id = value,
                                                  guild_id = guild_id,
                                                  big_req = 3,
                                                  smol_req = 2,
                                                  ignore = False,
                                                  bip_status = BipStatus(members = [],
                                                                     game = None,
                                                                     channel = None,
                                                                     channel_id = None,
                                                                     guild = None,
                                                                     guild_id = None))

            self.send_client_status()
        return True

    async def recieve_server_ping(self):
        try:
            ping_size = await self.loop.sock_recv(self.socket, 8)
            ping_size = int.from_bytes(ping_size, byteorder = 'little')
            server_ping = await self.loop.sock_recv(self.socket, ping_size)
            server_ping = pickle.loads(server_ping)
            self.process_ping(self, server_ping)
        except Exception:
            print('Connection closed')
        finally:
            return

        self.show()

    def process_ping(self, ping):
        type = ping.pop('type')

        if type == 'bip_status':
            if (ping['channel_id'] in self.User.channels and
                    not self.User.channels[ping['channel_id']][4]):
                self.bip

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

        channels: dict of dict (name : string, guild id : int)
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

    def load_from_file(self):
        try:
            with open('config.pickle', 'rb') as fp:
                data = pickle.load(fp)
            self._update(data.__dict__)
        except:
            pass
        return

    def save_to_file(self):
        with open('config.pickle', 'wb') as fp:
            pickle.dump(self, fp)
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = BipApp()

    sys.exit(app.exec_())
