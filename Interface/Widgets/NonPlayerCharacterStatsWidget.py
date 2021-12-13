from PyQt5.QtWidgets import QFrame


class NonPlayerCharacterStatsWidget(QFrame):
    def __init__(self, CharacterWindow):
        # Initialize Frame
        super().__init__()

        # Store Parameters
        self.CharacterWindow = CharacterWindow
