import PyQt5
from PyQt5.QtGUI import QMainWindow, QApplication, QWidget, QPushButton, QLineEdit, QCheckBox

class BipApp(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

        self._nameArea = QLineEdit()
        self._portArea = QLineEdit()
        self._channelIDArea = QLineEdit()
        self._excludesArea = QLineEdit()

        self._LFBCheckbox = QCheckBox("Looking For Bip", self)
        self._LFBCheckbox.stateChanged.connect(self.LFBAction)
        self.b.move(20,20)
        self.b.resize(320,40)

    def LFBAction(self, state):

        #change LFB state to whatever
        return

    def initUI(self):

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('BipApp')
        self.setWindowIcon(QIcon('taskbar_icon.png'))



        self.show()

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

class Connection(object):
    def __init__(self, server, socket):
        self.server = server
        self.socket = socket

    def send_client_status(self, client_status):
        return

    def recieve_server_update(self, server_update):
        #when a packet comes via this connection
        #async somehow
        return


 if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = BipApp()
    sys.exit(app.exec_())
