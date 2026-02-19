from PyQt6 import QtCore
from PyQt6.QtWidgets import QLineEdit


class CenteredLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
