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

    def initUI(self):

        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('BipApp')
        self.setWindowIcon(QIcon('taskbar_icon.png'))



        self.show()

app = QApplication(sys.argv)
ex = BipApp()
sys.exit(app.exec_())
