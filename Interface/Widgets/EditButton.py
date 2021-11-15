from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QPushButton


class EditButton(QPushButton):
    def __init__(self, Slot):
        super().__init__()

        self.CreateIcon()

        self.clicked.connect(Slot)

    def CreateIcon(self):
        IconPixmap = QPixmap()
        IconPixmap.loadFromData(QtCore.QByteArray.fromBase64(b"iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAuElEQVQ4jZ2SsQ6DMAxEz1VF1XZB4n+694vZ+R8kFkCwXIcQyy7QJD3JkqPknR0nQhKZsgclJpcSWETcOtdA4blbdiYpAwcD2Jn8MlB46CvcXzfdcCYkj4IM0+XQVxoAOHcLAxYkB6/gKgNA3awuN4x8X6EIBvwQi2Fr8BfsOhARTGOLulkBIAuOBm6K1iQFA4CQZKxu9Xi+kzCA8KBbF5zGVnMj/R+G0dAO7Kbt8LTypusBlAVGfQDRP71h3nr/pAAAAABJRU5ErkJggg=="))
        self.setIcon(QIcon(IconPixmap))
