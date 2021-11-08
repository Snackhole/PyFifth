from PyQt5 import QtCore
from PyQt5.QtWidgets import QLineEdit


class CenteredLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setAlignment(QtCore.Qt.AlignCenter)
