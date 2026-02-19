from PyQt6.QtWidgets import QPushButton


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


class PreparedButton(QPushButton):
    def __init__(self, Slot):
        # Initialize
        super().__init__("Prepared")

        # Store Parameters
        self.Slot = Slot

        # Configure
        self.setCheckable(True)
        self.setStyleSheet("QPushButton {font-size: 16pt;}\nQPushButton:checked {background-color: darkgreen;}")
        self.clicked.connect(self.Slot)


class AliveButton(QPushButton):
    def __init__(self, Slot):
        # Initialize
        super().__init__("Alive")

        # Store Parameters
        self.Slot = Slot

        # Configure
        self.setCheckable(True)
        self.setStyleSheet("QPushButton {font-size: 10pt;}\nQPushButton:checked {background-color: darkgreen;}")
        self.clicked.connect(self.Slot)


class TurnTakenButton(QPushButton):
    def __init__(self, Slot):
        # Initialize
        super().__init__("Turn Taken")

        # Store Parameters
        self.Slot = Slot

        # Configure
        self.setCheckable(True)
        self.setStyleSheet("QPushButton {font-size: 10pt;}\nQPushButton:checked {background-color: darkgreen;}")
        self.clicked.connect(self.Slot)
