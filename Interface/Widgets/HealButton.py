from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton


class HealButton(QPushButton):
    def __init__(self, Slot, Tooltip="Heal"):
        super().__init__()

        self.CreateIcon()

        self.setToolTip(Tooltip)

        self.clicked.connect(Slot)

    def CreateIcon(self):
        IconPixmap = QPixmap()
        IconPixmap.loadFromData(QtCore.QByteArray.fromBase64(b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAkElEQVQ4jd2SOw7DMAxDH4NuyWV6/0Okl8nMDo0MxfBvLqeYIB9kR7JN0uMAaOKz1WVJSMpezwfgVZfPfSe+Y7qOb0Dyfcqh0Pu6AJp+gdt2qzxTQLZ5dKx/AdguL76i/Bc27q1aheQyoLjCEqQulysAfI5jCMnlyD4AI0ivDL9NbE1b1juAeewVQIHkbCv0Be5ga3xiirSUAAAAAElFTkSuQmCC"))
        self.setIcon(QIcon(IconPixmap))
