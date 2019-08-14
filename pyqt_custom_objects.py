import PyQt5
from PyQt5.QtWidgets import(
QAbstractButton
)
from PyQt5.QtGui import(
QPainter
)

class QPicButton(QAbstractButton):
    def __init__(self, pixmap, rect, parent=None):
        super(QPicButton, self).__init__(parent)
        self.pixmap = pixmap
        self.rect = rect

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect, self.pixmap)


    def sizeHint(self):
        return self.pixmap.size()
