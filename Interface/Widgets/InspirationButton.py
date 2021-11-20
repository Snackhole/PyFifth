from PyQt5.QtWidgets import QPushButton


class InspirationButton(QPushButton):
    def __init__(self, CharacterSheetWindow):
        # Initialize
        super().__init__("Inspiration")

        # Store Parameters
        self.CharacterSheetWindow = CharacterSheetWindow

        # Configure
        self.setCheckable(True)
        self.setStyleSheet("QPushButton {font-size: 16pt;}\nQPushButton:checked {background-color: darkgreen}")
        self.clicked.connect(lambda: self.CharacterSheetWindow.UpdateStat("Inspiration", self.isChecked()))
