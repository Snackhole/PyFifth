from PyQt6.QtWidgets import QDialog, QPushButton, QGridLayout

from Interface.Widgets.CoinCalculatorWidget import CoinCalculatorWidget


class CoinCalculatorDialog(QDialog):
    def __init__(self, CharacterWindow):
        super().__init__(parent=CharacterWindow)

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Coin Calculator Widget
        self.CoinCalculatorWidget = CoinCalculatorWidget()

        # Close Button
        self.CloseButton = QPushButton("Close")
        self.CloseButton.clicked.connect(self.close)

        # Layout
        self.Layout = QGridLayout()

        self.Layout.addWidget(self.CoinCalculatorWidget, 0, 0)

        self.Layout.addWidget(self.CloseButton, 1, 0)

        self.setLayout(self.Layout)

        # Set Window Title and Icon
        self.setWindowTitle(self.CharacterWindow.ScriptName)
        self.setWindowIcon(self.CharacterWindow.WindowIcon)

        # Execute Dialog
        self.exec()
