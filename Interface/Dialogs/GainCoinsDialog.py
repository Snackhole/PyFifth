from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QGridLayout, QSizePolicy, QPushButton, QSpinBox, QLabel


class GainCoinsDialog(QDialog):
    def __init__(self, CharacterWindow):
        super().__init__(parent=CharacterWindow)

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Variables
        self.GainedCoins = {}
        self.GainedCoins["CP"] = None
        self.GainedCoins["SP"] = None
        self.GainedCoins["EP"] = None
        self.GainedCoins["GP"] = None
        self.GainedCoins["PP"] = None
        self.Submitted = False

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Prompt Label
        self.PromptLabel = QLabel("Gain coins:")
        self.PromptLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Coins Header Labels
        self.CPLabel = QLabel("CP")
        self.CPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.CPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.CPLabel.setMargin(5)
        self.SPLabel = QLabel("SP")
        self.SPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.SPLabel.setMargin(5)
        self.EPLabel = QLabel("EP")
        self.EPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.EPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.EPLabel.setMargin(5)
        self.GPLabel = QLabel("GP")
        self.GPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.GPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.GPLabel.setMargin(5)
        self.PPLabel = QLabel("PP")
        self.PPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.PPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.PPLabel.setMargin(5)

        # Coins Spin Boxes
        self.CPSpinBox = QSpinBox()
        self.CPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.CPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CPSpinBox.setButtonSymbols(self.CPSpinBox.NoButtons)
        self.CPSpinBox.setRange(0, 1000000000)
        self.SPSpinBox = QSpinBox()
        self.SPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.SPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SPSpinBox.setButtonSymbols(self.SPSpinBox.NoButtons)
        self.SPSpinBox.setRange(0, 1000000000)
        self.EPSpinBox = QSpinBox()
        self.EPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.EPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.EPSpinBox.setButtonSymbols(self.EPSpinBox.NoButtons)
        self.EPSpinBox.setRange(0, 1000000000)
        self.GPSpinBox = QSpinBox()
        self.GPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.GPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.GPSpinBox.setButtonSymbols(self.GPSpinBox.NoButtons)
        self.GPSpinBox.setRange(0, 1000000000)
        self.PPSpinBox = QSpinBox()
        self.PPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.PPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.PPSpinBox.setButtonSymbols(self.PPSpinBox.NoButtons)
        self.PPSpinBox.setRange(0, 1000000000)

        # Buttons
        self.SubmitButton = QPushButton("Submit")
        self.SubmitButton.clicked.connect(self.Submit)
        self.CancelButton = QPushButton("Cancel")
        self.CancelButton.clicked.connect(self.Cancel)

        # Layout
        self.Layout = QGridLayout()
        self.Layout.addWidget(self.PromptLabel, 0, 0, 1, 5)
        self.Layout.addWidget(self.CPLabel, 1, 0)
        self.Layout.addWidget(self.SPLabel, 1, 1)
        self.Layout.addWidget(self.EPLabel, 1, 2)
        self.Layout.addWidget(self.GPLabel, 1, 3)
        self.Layout.addWidget(self.PPLabel, 1, 4)
        self.Layout.addWidget(self.CPSpinBox, 2, 0)
        self.Layout.addWidget(self.SPSpinBox, 2, 1)
        self.Layout.addWidget(self.EPSpinBox, 2, 2)
        self.Layout.addWidget(self.GPSpinBox, 2, 3)
        self.Layout.addWidget(self.PPSpinBox, 2, 4)
        self.ButtonsLayout = QGridLayout()
        self.ButtonsLayout.addWidget(self.SubmitButton, 0, 0)
        self.ButtonsLayout.addWidget(self.CancelButton, 0, 1)
        self.Layout.addLayout(self.ButtonsLayout, 3, 0, 1, 5)
        self.Layout.setRowStretch(2, 1)
        for Column in range(5):
            self.Layout.setColumnStretch(Column, 1)
        self.setLayout(self.Layout)

        # Set Window Title and Icon
        self.setWindowTitle(self.CharacterWindow.ScriptName)
        self.setWindowIcon(self.CharacterWindow.WindowIcon)

        # Execute Dialog
        self.exec_()

    def Submit(self):
        self.GainedCoins["CP"] = self.CPSpinBox.value()
        self.GainedCoins["SP"] = self.SPSpinBox.value()
        self.GainedCoins["EP"] = self.EPSpinBox.value()
        self.GainedCoins["GP"] = self.GPSpinBox.value()
        self.GainedCoins["PP"] = self.PPSpinBox.value()
        self.Submitted = True
        self.close()

    def Cancel(self):
        self.close()
