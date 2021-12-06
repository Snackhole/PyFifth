from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QGridLayout, QSizePolicy, QPushButton, QSpinBox, QLabel

from Interface.Widgets.CenteredLineEdit import CenteredLineEdit


class SpendCoinsDialog(QDialog):
    def __init__(self, CharacterWindow):
        super().__init__(parent=CharacterWindow)

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Variables
        self.CurrentCoinsValue = self.GetCurrentCoinsValue()
        self.RemainingCoins = {}
        self.RemainingCoins["CP"] = None
        self.RemainingCoins["SP"] = None
        self.RemainingCoins["EP"] = None
        self.RemainingCoins["GP"] = None
        self.RemainingCoins["PP"] = None
        self.Submitted = False

        # Styles
        self.CoinValuesStyle = "QLabel {}"

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Prompt Label
        self.PromptLabel = QLabel("Spend coins by adjusting the number of spent coins and the number of remaining coins until the value of your coins after spending and the value of your coins remaining are equal:")
        self.PromptLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.PromptLabel.setWordWrap(False)

        # Spend Label
        self.SpendLabel = QLabel("Spend:")
        self.SpendLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Spent Coins Header Labels
        self.SpentCPLabel = QLabel("CP")
        self.SpentCPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SpentCPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.SpentCPLabel.setMargin(5)
        self.SpentSPLabel = QLabel("SP")
        self.SpentSPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SpentSPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.SpentSPLabel.setMargin(5)
        self.SpentEPLabel = QLabel("EP")
        self.SpentEPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SpentEPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.SpentEPLabel.setMargin(5)
        self.SpentGPLabel = QLabel("GP")
        self.SpentGPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SpentGPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.SpentGPLabel.setMargin(5)
        self.SpentPPLabel = QLabel("PP")
        self.SpentPPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SpentPPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.SpentPPLabel.setMargin(5)

        # Spent Coins Spin Boxes
        self.SpentCPSpinBox = QSpinBox()
        self.SpentCPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.SpentCPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpentCPSpinBox.setButtonSymbols(self.SpentCPSpinBox.NoButtons)
        self.SpentCPSpinBox.setRange(0, 1000000000)
        self.SpentCPSpinBox.valueChanged.connect(self.UpdateDisplay)
        self.SpentSPSpinBox = QSpinBox()
        self.SpentSPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.SpentSPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpentSPSpinBox.setButtonSymbols(self.SpentSPSpinBox.NoButtons)
        self.SpentSPSpinBox.setRange(0, 1000000000)
        self.SpentSPSpinBox.valueChanged.connect(self.UpdateDisplay)
        self.SpentEPSpinBox = QSpinBox()
        self.SpentEPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.SpentEPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpentEPSpinBox.setButtonSymbols(self.SpentEPSpinBox.NoButtons)
        self.SpentEPSpinBox.setRange(0, 1000000000)
        self.SpentEPSpinBox.valueChanged.connect(self.UpdateDisplay)
        self.SpentGPSpinBox = QSpinBox()
        self.SpentGPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.SpentGPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpentGPSpinBox.setButtonSymbols(self.SpentGPSpinBox.NoButtons)
        self.SpentGPSpinBox.setRange(0, 1000000000)
        self.SpentGPSpinBox.valueChanged.connect(self.UpdateDisplay)
        self.SpentPPSpinBox = QSpinBox()
        self.SpentPPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.SpentPPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpentPPSpinBox.setButtonSymbols(self.SpentPPSpinBox.NoButtons)
        self.SpentPPSpinBox.setRange(0, 1000000000)
        self.SpentPPSpinBox.valueChanged.connect(self.UpdateDisplay)

        # Match Values Label
        self.MatchValuesLabel = QLabel("Match Values:")
        self.MatchValuesLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Value After Spending Label
        self.ValueAfterSpendingLabel = QLabel("Value After Spending (CP):")
        self.ValueAfterSpendingLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ValueAfterSpendingLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.ValueAfterSpendingLabel.setMargin(5)

        # Value After Spending Spin Box
        self.ValueAfterSpendingSpinBox = QSpinBox()
        self.ValueAfterSpendingSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ValueAfterSpendingSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.ValueAfterSpendingSpinBox.setButtonSymbols(self.ValueAfterSpendingSpinBox.NoButtons)
        self.ValueAfterSpendingSpinBox.setRange(0, 1000000000)
        self.ValueAfterSpendingSpinBox.setReadOnly(True)

        # Equality Line Edit
        self.EqualityLineEdit = CenteredLineEdit()
        self.EqualityLineEdit.setSizePolicy(self.InputsSizePolicy)
        self.EqualityLineEdit.setReadOnly(True)

        # Remaining Coins Value Label
        self.RemainingCoinsValueLabel = QLabel("Remaining Coins Value (CP):")
        self.RemainingCoinsValueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.RemainingCoinsValueLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.RemainingCoinsValueLabel.setMargin(5)

        # Remaining Coins Value Spin Box
        self.RemainingCoinsValueSpinBox = QSpinBox()
        self.RemainingCoinsValueSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.RemainingCoinsValueSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.RemainingCoinsValueSpinBox.setButtonSymbols(self.RemainingCoinsValueSpinBox.NoButtons)
        self.RemainingCoinsValueSpinBox.setRange(0, 1000000000)
        self.RemainingCoinsValueSpinBox.setReadOnly(True)

        # Remaining Label
        self.RemainingLabel = QLabel("Remaining:")
        self.RemainingLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Remaining Coins Header Labels
        self.RemainingCPLabel = QLabel("CP")
        self.RemainingCPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.RemainingCPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.RemainingCPLabel.setMargin(5)
        self.RemainingSPLabel = QLabel("SP")
        self.RemainingSPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.RemainingSPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.RemainingSPLabel.setMargin(5)
        self.RemainingEPLabel = QLabel("EP")
        self.RemainingEPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.RemainingEPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.RemainingEPLabel.setMargin(5)
        self.RemainingGPLabel = QLabel("GP")
        self.RemainingGPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.RemainingGPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.RemainingGPLabel.setMargin(5)
        self.RemainingPPLabel = QLabel("PP")
        self.RemainingPPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.RemainingPPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.RemainingPPLabel.setMargin(5)

        # Remaining Coins Spin Boxes
        self.RemainingCPSpinBox = QSpinBox()
        self.RemainingCPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.RemainingCPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.RemainingCPSpinBox.setButtonSymbols(self.RemainingCPSpinBox.NoButtons)
        self.RemainingCPSpinBox.setRange(0, 1000000000)
        self.RemainingCPSpinBox.valueChanged.connect(self.UpdateDisplay)
        self.RemainingSPSpinBox = QSpinBox()
        self.RemainingSPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.RemainingSPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.RemainingSPSpinBox.setButtonSymbols(self.RemainingSPSpinBox.NoButtons)
        self.RemainingSPSpinBox.setRange(0, 1000000000)
        self.RemainingSPSpinBox.valueChanged.connect(self.UpdateDisplay)
        self.RemainingEPSpinBox = QSpinBox()
        self.RemainingEPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.RemainingEPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.RemainingEPSpinBox.setButtonSymbols(self.RemainingEPSpinBox.NoButtons)
        self.RemainingEPSpinBox.setRange(0, 1000000000)
        self.RemainingEPSpinBox.valueChanged.connect(self.UpdateDisplay)
        self.RemainingGPSpinBox = QSpinBox()
        self.RemainingGPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.RemainingGPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.RemainingGPSpinBox.setButtonSymbols(self.RemainingGPSpinBox.NoButtons)
        self.RemainingGPSpinBox.setRange(0, 1000000000)
        self.RemainingGPSpinBox.valueChanged.connect(self.UpdateDisplay)
        self.RemainingPPSpinBox = QSpinBox()
        self.RemainingPPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.RemainingPPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.RemainingPPSpinBox.setButtonSymbols(self.RemainingPPSpinBox.NoButtons)
        self.RemainingPPSpinBox.setRange(0, 1000000000)
        self.RemainingPPSpinBox.valueChanged.connect(self.UpdateDisplay)

        # Coin Values Labels
        self.CPValueLabel = QLabel("1 CP")
        self.CPValueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.CPValueLabel.setStyleSheet(self.CoinValuesStyle)
        self.SPValueLabel = QLabel("1 SP")
        self.SPValueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SPValueLabel.setStyleSheet(self.CoinValuesStyle)
        self.EPValueLabel = QLabel("1 EP")
        self.EPValueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.EPValueLabel.setStyleSheet(self.CoinValuesStyle)
        self.GPValueLabel = QLabel("1 GP")
        self.GPValueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.GPValueLabel.setStyleSheet(self.CoinValuesStyle)
        self.PPValueLabel = QLabel("1 PP")
        self.PPValueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.PPValueLabel.setStyleSheet(self.CoinValuesStyle)

        # Buttons
        self.SubmitButton = QPushButton("Submit")
        self.SubmitButton.clicked.connect(self.Submit)
        self.CancelButton = QPushButton("Cancel")
        self.CancelButton.clicked.connect(self.Cancel)

        # Layout
        self.Layout = QGridLayout()

        self.Layout.addWidget(self.PromptLabel, 0, 0, 1, 6)

        self.Layout.addWidget(self.SpentCPLabel, 1, 1)
        self.Layout.addWidget(self.SpentSPLabel, 1, 2)
        self.Layout.addWidget(self.SpentEPLabel, 1, 3)
        self.Layout.addWidget(self.SpentGPLabel, 1, 4)
        self.Layout.addWidget(self.SpentPPLabel, 1, 5)
        self.Layout.addWidget(self.SpendLabel, 2, 0)
        self.Layout.addWidget(self.SpentCPSpinBox, 2, 1)
        self.Layout.addWidget(self.SpentSPSpinBox, 2, 2)
        self.Layout.addWidget(self.SpentEPSpinBox, 2, 3)
        self.Layout.addWidget(self.SpentGPSpinBox, 2, 4)
        self.Layout.addWidget(self.SpentPPSpinBox, 2, 5)

        self.MatchValuesLayout = QGridLayout()
        self.MatchValuesLayout.addWidget(self.ValueAfterSpendingLabel, 0, 1)
        self.MatchValuesLayout.addWidget(self.RemainingCoinsValueLabel, 0, 3)
        self.MatchValuesLayout.addWidget(self.MatchValuesLabel, 1, 0)
        self.MatchValuesLayout.addWidget(self.ValueAfterSpendingSpinBox, 1, 1)
        self.MatchValuesLayout.addWidget(self.EqualityLineEdit, 1, 2)
        self.MatchValuesLayout.addWidget(self.RemainingCoinsValueSpinBox, 1, 3)
        self.Layout.addLayout(self.MatchValuesLayout, 3, 0, 1, 6)

        self.Layout.addWidget(self.RemainingCPLabel, 4, 1)
        self.Layout.addWidget(self.RemainingSPLabel, 4, 2)
        self.Layout.addWidget(self.RemainingEPLabel, 4, 3)
        self.Layout.addWidget(self.RemainingGPLabel, 4, 4)
        self.Layout.addWidget(self.RemainingPPLabel, 4, 5)
        self.Layout.addWidget(self.RemainingLabel, 5, 0)
        self.Layout.addWidget(self.RemainingCPSpinBox, 5, 1)
        self.Layout.addWidget(self.RemainingSPSpinBox, 5, 2)
        self.Layout.addWidget(self.RemainingEPSpinBox, 5, 3)
        self.Layout.addWidget(self.RemainingGPSpinBox, 5, 4)
        self.Layout.addWidget(self.RemainingPPSpinBox, 5, 5)
        self.Layout.addWidget(self.CPValueLabel, 6, 1)
        self.Layout.addWidget(self.SPValueLabel, 6, 2)
        self.Layout.addWidget(self.EPValueLabel, 6, 3)
        self.Layout.addWidget(self.GPValueLabel, 6, 4)
        self.Layout.addWidget(self.PPValueLabel, 6, 5)

        self.ButtonsLayout = QGridLayout()
        self.ButtonsLayout.addWidget(self.SubmitButton, 0, 0)
        self.ButtonsLayout.addWidget(self.CancelButton, 0, 1)
        self.Layout.addLayout(self.ButtonsLayout, 7, 0, 1, 6)

        for Row in [2, 3, 5]:
            self.Layout.setRowStretch(Row, 1)
        for Column in range(1, 6):
            self.Layout.setColumnStretch(Column, 1)

        self.setLayout(self.Layout)

        # Set Window Title and Icon
        self.setWindowTitle(self.CharacterWindow.ScriptName)
        self.setWindowIcon(self.CharacterWindow.WindowIcon)

        # Execute Dialog
        self.exec_()

    def Submit(self):
        if not self.ValidEntry(Alert=True):
            return
        self.RemainingCoins["CP"] = self.RemainingCPSpinBox.value()
        self.RemainingCoins["SP"] = self.RemainingSPSpinBox.value()
        self.RemainingCoins["EP"] = self.RemainingEPSpinBox.value()
        self.RemainingCoins["GP"] = self.RemainingGPSpinBox.value()
        self.RemainingCoins["PP"] = self.RemainingPPSpinBox.value()
        self.Submitted = True
        self.close()

    def Cancel(self):
        self.close()

    # TODO Methods
    def ValidEntry(self, Alert=False):
        return True

    def UpdateDisplay(self):
        pass

    def GetCurrentCoinsValue(self):
        pass
