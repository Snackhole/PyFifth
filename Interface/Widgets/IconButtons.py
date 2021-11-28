from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton


class AddButton(QPushButton):
    def __init__(self, Slot, Tooltip="Add"):
        super().__init__()

        self.CreateIcon()

        self.setToolTip(Tooltip)

        self.clicked.connect(Slot)

    def CreateIcon(self):
        IconPixmap = QPixmap()
        IconPixmap.loadFromData(QtCore.QByteArray.fromBase64(b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAe0lEQVQ4jWP8//8/AxrAEEADjMhcFmwqbOrFsOo80vgKQwyrASCgZCuEwr93+B1WdUwEnEsQsBDhZ3SAoh7sBVx+Rgfo6kBhAg8DdD+jA1xhQnEYDLwB8DBAj2di0wHYAPQURmpKREnbpOYF6oUBOsDlZwznUJSdGRgYAHP6JbnRUVuCAAAAAElFTkSuQmCC"))
        self.setIcon(QIcon(IconPixmap))


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


class EditButton(QPushButton):
    def __init__(self, Slot, Tooltip="Edit"):
        super().__init__()

        self.CreateIcon()

        self.setToolTip(Tooltip)

        self.clicked.connect(Slot)

    def CreateIcon(self):
        IconPixmap = QPixmap()
        IconPixmap.loadFromData(QtCore.QByteArray.fromBase64(b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAuElEQVQ4jZ2SsQ6DMAxEz1VF1XZB4n+694vZ+R8kFkCwXIcQyy7QJD3JkqPknR0nQhKZsgclJpcSWETcOtdA4blbdiYpAwcD2Jn8MlB46CvcXzfdcCYkj4IM0+XQVxoAOHcLAxYkB6/gKgNA3awuN4x8X6EIBvwQi2Fr8BfsOhARTGOLulkBIAuOBm6K1iQFA4CQZKxu9Xi+kzCA8KBbF5zGVnMj/R+G0dAO7Kbt8LTypusBlAVGfQDRP71h3nr/pAAAAABJRU5ErkJggg=="))
        self.setIcon(QIcon(IconPixmap))


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
