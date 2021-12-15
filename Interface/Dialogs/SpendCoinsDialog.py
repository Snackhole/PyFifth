from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QGridLayout, QSizePolicy, QPushButton, QSpinBox, QLabel, QMessageBox

from Interface.Widgets.CenteredLineEdit import CenteredLineEdit


class SpendCoinsDialog(QDialog):
    def __init__(self, ParentWindow):
        super().__init__(parent=ParentWindow)

        # Store Parameters
        self.ParentWindow = ParentWindow

        # Variables
        self.CPValues = {}
        self.CPValues["CP"] = 1
        self.CPValues["SP"] = 10
        self.CPValues["EP"] = 50
        self.CPValues["GP"] = 100
        self.CPValues["PP"] = 1000
        self.SpentCoins = {}
        self.SpentCoins["CP"] = 0
        self.SpentCoins["SP"] = 0
        self.SpentCoins["EP"] = 0
        self.SpentCoins["GP"] = 0
        self.SpentCoins["PP"] = 0
        self.RemainingCoins = self.ParentWindow.GetCurrentCoinCounts()
        self.OriginalRemainingCoinsCPValue = self.GetCPValueOfCoins(self.RemainingCoins)
        self.Submitted = False

        # Styles
        self.CoinValuesStyle = "QLabel {font-size: 6pt;}"
        self.MatchValuesEqualSpinBoxStyle = "QSpinBox {background-color: darkgreen;}"
        self.MatchValuesUnequalSpinBoxStyle = "QSpinBox {background-color: darkred;}"
        self.MatchValuesEqualLineEditStyle = "QLineEdit {background-color: darkgreen;}"
        self.MatchValuesUnequalLineEditStyle = "QLineEdit {background-color: darkred;}"

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Prompt Label
        self.PromptLabel = QLabel("Spend coins by adjusting the number of spent coins and the number of remaining coins until the value of your coins after spending and the value of your coins remaining are equal.")
        self.PromptLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.PromptLabel.setWordWrap(False)

        # Spend Label
        self.SpendLabel = QLabel("Spent Coins")
        self.SpendLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SpendLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.SpendLabel.setMargin(5)

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
        self.SpentCPSpinBox.setValue(self.SpentCoins["CP"])
        self.SpentCPSpinBox.valueChanged.connect(self.Update)
        self.SpentSPSpinBox = QSpinBox()
        self.SpentSPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.SpentSPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpentSPSpinBox.setButtonSymbols(self.SpentSPSpinBox.NoButtons)
        self.SpentSPSpinBox.setRange(0, 1000000000)
        self.SpentSPSpinBox.setValue(self.SpentCoins["SP"])
        self.SpentSPSpinBox.valueChanged.connect(self.Update)
        self.SpentEPSpinBox = QSpinBox()
        self.SpentEPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.SpentEPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpentEPSpinBox.setButtonSymbols(self.SpentEPSpinBox.NoButtons)
        self.SpentEPSpinBox.setRange(0, 1000000000)
        self.SpentEPSpinBox.setValue(self.SpentCoins["EP"])
        self.SpentEPSpinBox.valueChanged.connect(self.Update)
        self.SpentGPSpinBox = QSpinBox()
        self.SpentGPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.SpentGPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpentGPSpinBox.setButtonSymbols(self.SpentGPSpinBox.NoButtons)
        self.SpentGPSpinBox.setRange(0, 1000000000)
        self.SpentGPSpinBox.setValue(self.SpentCoins["GP"])
        self.SpentGPSpinBox.valueChanged.connect(self.Update)
        self.SpentPPSpinBox = QSpinBox()
        self.SpentPPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.SpentPPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpentPPSpinBox.setButtonSymbols(self.SpentPPSpinBox.NoButtons)
        self.SpentPPSpinBox.setRange(0, 1000000000)
        self.SpentPPSpinBox.setValue(self.SpentCoins["PP"])
        self.SpentPPSpinBox.valueChanged.connect(self.Update)

        self.SpentCoinsSpinBoxes = {}
        self.SpentCoinsSpinBoxes["CP"] = self.SpentCPSpinBox
        self.SpentCoinsSpinBoxes["SP"] = self.SpentSPSpinBox
        self.SpentCoinsSpinBoxes["EP"] = self.SpentEPSpinBox
        self.SpentCoinsSpinBoxes["GP"] = self.SpentGPSpinBox
        self.SpentCoinsSpinBoxes["PP"] = self.SpentPPSpinBox

        # Match Values Label
        self.MatchValuesLabel = QLabel("Match Values")
        self.MatchValuesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MatchValuesLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.MatchValuesLabel.setMargin(5)

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
        self.ValueAfterSpendingSpinBox.setFocusPolicy(QtCore.Qt.NoFocus)

        # Equality Line Edit
        self.EqualityLineEdit = CenteredLineEdit()
        self.EqualityLineEdit.setSizePolicy(self.InputsSizePolicy)
        self.EqualityLineEdit.setReadOnly(True)
        self.EqualityLineEdit.setFocusPolicy(QtCore.Qt.NoFocus)

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
        self.RemainingCoinsValueSpinBox.setFocusPolicy(QtCore.Qt.NoFocus)

        # Remaining Label
        self.RemainingLabel = QLabel("Remaining Coins")
        self.RemainingLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.RemainingLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.RemainingLabel.setMargin(5)

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
        self.RemainingCPSpinBox.setValue(self.RemainingCoins["CP"])
        self.RemainingCPSpinBox.valueChanged.connect(self.Update)
        self.RemainingSPSpinBox = QSpinBox()
        self.RemainingSPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.RemainingSPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.RemainingSPSpinBox.setButtonSymbols(self.RemainingSPSpinBox.NoButtons)
        self.RemainingSPSpinBox.setRange(0, 1000000000)
        self.RemainingSPSpinBox.setValue(self.RemainingCoins["SP"])
        self.RemainingSPSpinBox.valueChanged.connect(self.Update)
        self.RemainingEPSpinBox = QSpinBox()
        self.RemainingEPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.RemainingEPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.RemainingEPSpinBox.setButtonSymbols(self.RemainingEPSpinBox.NoButtons)
        self.RemainingEPSpinBox.setRange(0, 1000000000)
        self.RemainingEPSpinBox.setValue(self.RemainingCoins["EP"])
        self.RemainingEPSpinBox.valueChanged.connect(self.Update)
        self.RemainingGPSpinBox = QSpinBox()
        self.RemainingGPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.RemainingGPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.RemainingGPSpinBox.setButtonSymbols(self.RemainingGPSpinBox.NoButtons)
        self.RemainingGPSpinBox.setRange(0, 1000000000)
        self.RemainingGPSpinBox.setValue(self.RemainingCoins["GP"])
        self.RemainingGPSpinBox.valueChanged.connect(self.Update)
        self.RemainingPPSpinBox = QSpinBox()
        self.RemainingPPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.RemainingPPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.RemainingPPSpinBox.setButtonSymbols(self.RemainingPPSpinBox.NoButtons)
        self.RemainingPPSpinBox.setRange(0, 1000000000)
        self.RemainingPPSpinBox.setValue(self.RemainingCoins["PP"])
        self.RemainingPPSpinBox.valueChanged.connect(self.Update)

        self.RemainingCoinsSpinBoxes = {}
        self.RemainingCoinsSpinBoxes["CP"] = self.RemainingCPSpinBox
        self.RemainingCoinsSpinBoxes["SP"] = self.RemainingSPSpinBox
        self.RemainingCoinsSpinBoxes["EP"] = self.RemainingEPSpinBox
        self.RemainingCoinsSpinBoxes["GP"] = self.RemainingGPSpinBox
        self.RemainingCoinsSpinBoxes["PP"] = self.RemainingPPSpinBox

        # Coin Values Labels
        self.CPValueLabel = QLabel("1 CP")
        self.CPValueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.CPValueLabel.setStyleSheet(self.CoinValuesStyle)
        self.SPValueLabel = QLabel("10 CP")
        self.SPValueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SPValueLabel.setStyleSheet(self.CoinValuesStyle)
        self.EPValueLabel = QLabel("50 CP")
        self.EPValueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.EPValueLabel.setStyleSheet(self.CoinValuesStyle)
        self.GPValueLabel = QLabel("100 CP")
        self.GPValueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.GPValueLabel.setStyleSheet(self.CoinValuesStyle)
        self.PPValueLabel = QLabel("1000 CP")
        self.PPValueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.PPValueLabel.setStyleSheet(self.CoinValuesStyle)

        # Buttons
        self.SubmitButton = QPushButton("Submit")
        self.SubmitButton.clicked.connect(self.Submit)
        self.CancelButton = QPushButton("Cancel")
        self.CancelButton.clicked.connect(self.Cancel)

        # Layout
        self.Layout = QGridLayout()

        self.Layout.addWidget(self.PromptLabel, 0, 0, 1, 3)

        self.SpentCoinsLayout = QGridLayout()
        self.SpentCoinsLayout.addWidget(self.SpendLabel, 0, 0, 1, 5)
        self.SpentCoinsLayout.addWidget(self.SpentCPLabel, 1, 0)
        self.SpentCoinsLayout.addWidget(self.SpentSPLabel, 1, 1)
        self.SpentCoinsLayout.addWidget(self.SpentEPLabel, 1, 2)
        self.SpentCoinsLayout.addWidget(self.SpentGPLabel, 1, 3)
        self.SpentCoinsLayout.addWidget(self.SpentPPLabel, 1, 4)
        self.SpentCoinsLayout.addWidget(self.SpentCPSpinBox, 2, 0)
        self.SpentCoinsLayout.addWidget(self.SpentSPSpinBox, 2, 1)
        self.SpentCoinsLayout.addWidget(self.SpentEPSpinBox, 2, 2)
        self.SpentCoinsLayout.addWidget(self.SpentGPSpinBox, 2, 3)
        self.SpentCoinsLayout.addWidget(self.SpentPPSpinBox, 2, 4)
        self.SpentCoinsLayout.setRowStretch(2, 1)
        self.Layout.addLayout(self.SpentCoinsLayout, 1, 0)

        self.MatchValuesLayout = QGridLayout()
        self.MatchValuesLayout.addWidget(self.MatchValuesLabel, 0, 0, 1, 3)
        self.MatchValuesLayout.addWidget(self.ValueAfterSpendingLabel, 1, 0)
        self.MatchValuesLayout.addWidget(self.RemainingCoinsValueLabel, 1, 2)
        self.MatchValuesLayout.addWidget(self.ValueAfterSpendingSpinBox, 2, 0)
        self.MatchValuesLayout.addWidget(self.EqualityLineEdit, 2, 1)
        self.MatchValuesLayout.addWidget(self.RemainingCoinsValueSpinBox, 2, 2)
        self.MatchValuesLayout.setRowStretch(2, 1)
        self.Layout.addLayout(self.MatchValuesLayout, 1, 1)

        self.RemainingCoinsLayout = QGridLayout()
        self.RemainingCoinsLayout.addWidget(self.RemainingLabel, 0, 0, 1, 5)
        self.RemainingCoinsLayout.addWidget(self.RemainingCPLabel, 1, 0)
        self.RemainingCoinsLayout.addWidget(self.RemainingSPLabel, 1, 1)
        self.RemainingCoinsLayout.addWidget(self.RemainingEPLabel, 1, 2)
        self.RemainingCoinsLayout.addWidget(self.RemainingGPLabel, 1, 3)
        self.RemainingCoinsLayout.addWidget(self.RemainingPPLabel, 1, 4)
        self.RemainingCoinsLayout.addWidget(self.RemainingCPSpinBox, 2, 0)
        self.RemainingCoinsLayout.addWidget(self.RemainingSPSpinBox, 2, 1)
        self.RemainingCoinsLayout.addWidget(self.RemainingEPSpinBox, 2, 2)
        self.RemainingCoinsLayout.addWidget(self.RemainingGPSpinBox, 2, 3)
        self.RemainingCoinsLayout.addWidget(self.RemainingPPSpinBox, 2, 4)
        self.RemainingCoinsLayout.addWidget(self.CPValueLabel, 3, 0)
        self.RemainingCoinsLayout.addWidget(self.SPValueLabel, 3, 1)
        self.RemainingCoinsLayout.addWidget(self.EPValueLabel, 3, 2)
        self.RemainingCoinsLayout.addWidget(self.GPValueLabel, 3, 3)
        self.RemainingCoinsLayout.addWidget(self.PPValueLabel, 3, 4)
        self.RemainingCoinsLayout.setRowStretch(2, 1)
        self.Layout.addLayout(self.RemainingCoinsLayout, 1, 2)

        self.ButtonsLayout = QGridLayout()
        self.ButtonsLayout.addWidget(self.SubmitButton, 0, 0)
        self.ButtonsLayout.addWidget(self.CancelButton, 0, 1)
        self.Layout.addLayout(self.ButtonsLayout, 2, 0, 1, 3)

        for Column in [0, 2]:
            self.Layout.setColumnStretch(Column, 1)

        self.setLayout(self.Layout)

        # Set Window Title and Icon
        self.setWindowTitle(self.ParentWindow.ScriptName)
        self.setWindowIcon(self.ParentWindow.WindowIcon)

        # Update Display
        self.Update()

        # Select Spent CP Spin Box
        self.SpentCPSpinBox.selectAll()

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

    def ValidEntry(self, Alert=False):
        SpentCoinsCPValue = self.GetCPValueOfCoins(self.SpentCoins)
        RemainingCoinsCPValue = self.GetCPValueOfCoins(self.RemainingCoins)
        CPValueAfterSpending = self.OriginalRemainingCoinsCPValue - SpentCoinsCPValue
        if CPValueAfterSpending != RemainingCoinsCPValue:
            if Alert:
                self.ParentWindow.DisplayMessageBox("The value of your coins after spending must be equal to the value of your remaining coins.", Icon=QMessageBox.Warning, Parent=self)
            return False
        return True

    def GetCPValueOfCoins(self, Coins):
        CPValueOfCoins = 0
        for CoinDenomination in Coins.keys():
            CPValueOfCoins += Coins[CoinDenomination] * self.CPValues[CoinDenomination]
        return CPValueOfCoins

    def Update(self):
        # Update Coin Counts from Spin Boxes
        for CoinDenomination in self.SpentCoins.keys():
            self.SpentCoins[CoinDenomination] = self.SpentCoinsSpinBoxes[CoinDenomination].value()
            self.RemainingCoins[CoinDenomination] = self.RemainingCoinsSpinBoxes[CoinDenomination].value()

        # Get CP Values of Spent and Remaining Coins
        SpentCoinsCPValue = self.GetCPValueOfCoins(self.SpentCoins)
        RemainingCoinsCPValue = self.GetCPValueOfCoins(self.RemainingCoins)

        # Value After Spending
        CPValueAfterSpending = self.OriginalRemainingCoinsCPValue - SpentCoinsCPValue

        # Set Match Values and Styles
        self.ValueAfterSpendingSpinBox.setValue(CPValueAfterSpending)
        self.RemainingCoinsValueSpinBox.setValue(RemainingCoinsCPValue)
        if CPValueAfterSpending == RemainingCoinsCPValue:
            self.ValueAfterSpendingSpinBox.setStyleSheet(self.MatchValuesEqualSpinBoxStyle)
            self.RemainingCoinsValueSpinBox.setStyleSheet(self.MatchValuesEqualSpinBoxStyle)
            self.EqualityLineEdit.setStyleSheet(self.MatchValuesEqualLineEditStyle)
            self.EqualityLineEdit.setText("=")
        else:
            self.ValueAfterSpendingSpinBox.setStyleSheet(self.MatchValuesUnequalSpinBoxStyle)
            self.RemainingCoinsValueSpinBox.setStyleSheet(self.MatchValuesUnequalSpinBoxStyle)
            self.EqualityLineEdit.setStyleSheet(self.MatchValuesUnequalLineEditStyle)
            if CPValueAfterSpending > RemainingCoinsCPValue:
                self.EqualityLineEdit.setText(">")
            else:
                self.EqualityLineEdit.setText("<")
