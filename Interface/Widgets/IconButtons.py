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


class CopyButton(QPushButton):
    def __init__(self, Slot, Tooltip="Copy"):
        super().__init__()

        self.CreateIcon()

        self.setToolTip(Tooltip)

        self.clicked.connect(Slot)

    def CreateIcon(self):
        IconPixmap = QPixmap()
        IconPixmap.loadFromData(QtCore.QByteArray.fromBase64(b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAf0lEQVQ4jWP8////fwbiASO6ShYQYVMvRtCEI42vMNQdbXoNMQAElGyFcGq+d/gdTjkmEpxPGwNYiFADB0caX6EGeCMeA9D9jS2gQQGL1wXEBCz1wgBfVBE0AOQXdEBM4oIZwIiuGCO08YBBnpCICVhQdmZgZETNpURncQYGBgDHRSyJhgjGSwAAAABJRU5ErkJggg=="))
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


class DeleteButton(QPushButton):
    def __init__(self, Slot, Tooltip="Delete"):
        super().__init__()

        self.CreateIcon()

        self.setToolTip(Tooltip)

        self.clicked.connect(Slot)

    def CreateIcon(self):
        IconPixmap = QPixmap()
        IconPixmap.loadFromData(QtCore.QByteArray.fromBase64(b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAQ0lEQVQ4jWMYBQyM/////09JMLCAiHoxMbI0N756BTEABGyFhEjSfPjdOzDNRJbVSGDgDYCHAcxPpAKKo3HEAwYGBgADWhCsPEB/zAAAAABJRU5ErkJggg=="))
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


class MoveDownButton(QPushButton):
    def __init__(self, Slot, Tooltip="Move Down"):
        super().__init__()

        self.CreateIcon()

        self.setToolTip(Tooltip)

        self.clicked.connect(Slot)

    def CreateIcon(self):
        IconPixmap = QPixmap()
        IconPixmap.loadFromData(QtCore.QByteArray.fromBase64(b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAj0lEQVQ4jWP8//8/AxrAEEADjMhcFmwqxBTqsep89aARQwyrASAg5GWLwn+37TBWdUwEnEsQDAMDWIiINnSAoh4cC7iiDR2gqwNFKzwa0aMNHeCKViaYSbjiGRsAqYUlKiZY0iTWEGTNIL2wWCDKEHTNcC8QYwg2zWAGrtyILcTRNeMyAG4IFoCimYGBgQEAtDVEATWWeH0AAAAASUVORK5CYII="))
        self.setIcon(QIcon(IconPixmap))


class MoveUpButton(QPushButton):
    def __init__(self, Slot, Tooltip="Move Up"):
        super().__init__()

        self.CreateIcon()

        self.setToolTip(Tooltip)

        self.clicked.connect(Slot)

    def CreateIcon(self):
        IconPixmap = QPixmap()
        IconPixmap.loadFromData(QtCore.QByteArray.fromBase64(b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAkklEQVQ4jWP8//8/AxaAVZCBgYERXYAFl2YxhXoUwVcPGmFyKIaguwCuWcjLFsWAd9sOwwxBcQkTMZpBACSG5Cq4rUzEaMZnCBOxmnEZwkSKZmyGwGMBFEjoipABujwMgA1ACl0GBixRCAPo6mAuQE8cuBIRDKCoZ8KrlAgwDAzAlpnAAFe0oQNs2Zn4WGBgYAAAciE1ohhWgxkAAAAASUVORK5CYII="))
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


class SortButton(QPushButton):
    def __init__(self, Slot, Tooltip="Sort"):
        super().__init__()

        self.CreateIcon()

        self.setToolTip(Tooltip)

        self.clicked.connect(Slot)

    def CreateIcon(self):
        IconPixmap = QPixmap()
        IconPixmap.loadFromData(QtCore.QByteArray.fromBase64(b"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"))
        self.setIcon(QIcon(IconPixmap))
