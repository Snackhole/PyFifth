from PyQt5.QtWidgets import QPushButton


class InspirationButton(QPushButton):
    def __init__(self, CharacterWindow):
        # Initialize
        super().__init__("Inspiration")

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Configure
        self.setCheckable(True)
        self.setStyleSheet("QPushButton {font-size: 16pt;}\nQPushButton:checked {background-color: darkgreen;}")
        self.clicked.connect(lambda: self.CharacterWindow.UpdateStat("Inspiration", self.isChecked()))


class ConcentratingButton(QPushButton):
    def __init__(self, CharacterWindow):
        # Initialize
        super().__init__("Concentrating")

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Configure
        self.setCheckable(True)
        self.setStyleSheet("QPushButton {font-size: 16pt;}\nQPushButton:checked {background-color: darkgreen;}")
        self.clicked.connect(lambda: self.CharacterWindow.UpdateStat("Concentrating", self.isChecked()))
