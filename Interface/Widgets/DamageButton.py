from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton


class DamageButton(QPushButton):
    def __init__(self, Slot, Tooltip="Damage"):
        super().__init__()

        self.CreateIcon()

        self.setToolTip(Tooltip)

        self.clicked.connect(Slot)

    def CreateIcon(self):
        IconPixmap = QPixmap()
        IconPixmap.loadFromData(QtCore.QByteArray.fromBase64(b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAtElEQVQ4jZ2S4Q2FIAyEr4RNXKNzOIwDOIxzdA1n4f14FE8oPvMuIVSgXy5npZRSMEqCs1AZAESu95Xn0J+g7IWZgWEEeoRk/lDVG+gVpFQBKGbWdq9JiFbq6WYGVW015ROFjURObo1vIQ6QfyGJ6hACfMPd1iWEMCCEeDOAECLxINZLkdbM2o/Tf/HgYHCyH+dwyU5mgEcIOwiHo1tt0LZ1GYZrlkGvlgm9F2Ae4hTCzQDwAWgNwjiDIS4PAAAAAElFTkSuQmCC"))
        self.setIcon(QIcon(IconPixmap))
