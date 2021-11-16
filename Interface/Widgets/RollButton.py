from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton


class RollButton(QPushButton):
    def __init__(self, Slot, Tooltip="Roll"):
        super().__init__()

        self.CreateIcon()

        self.setToolTip(Tooltip)

        self.clicked.connect(Slot)

    def CreateIcon(self):
        IconPixmap = QPixmap()
        IconPixmap.loadFromData(QtCore.QByteArray.fromBase64(b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAATElEQVQ4jWP8////fwYKAAsDAwMDIyMjWZr///8PMQDGIQXALGXCJoHNRbjEMQwgFbCgC+DyCi5xil0wGgbDIgzgBpCboVjwmU4MAACMcR88hf4SzwAAAABJRU5ErkJggg=="))
        self.setIcon(QIcon(IconPixmap))
