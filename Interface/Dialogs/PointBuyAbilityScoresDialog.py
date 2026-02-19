from PyQt6 import QtCore
from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QSpinBox, QSizePolicy, QMessageBox


class PointBuyAbilityScoresDialog(QDialog):
    def __init__(self, Parent, CharacterWindow):
        super().__init__(parent=Parent)

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Variables
        self.PointBoughtAbilityScores = None
        self.AbilitiesList = self.CharacterWindow.PlayerCharacter.Abilities

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        # Prompt Label
        self.PromptLabel = QLabel("Buy ability scores with points:")
        self.PromptLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Strength Input
        self.StrengthLabel = QLabel("Strength")
        self.StrengthLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.StrengthSpinBox = QSpinBox()
        self.StrengthSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.StrengthSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.StrengthSpinBox.setButtonSymbols(self.StrengthSpinBox.ButtonSymbols.NoButtons)
        self.StrengthSpinBox.setRange(8, 15)
        self.StrengthSpinBox.setValue(8)
        self.StrengthSpinBox.valueChanged.connect(self.UpdateDisplay)

        # Dexterity Input
        self.DexterityLabel = QLabel("Dexterity")
        self.DexterityLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.DexteritySpinBox = QSpinBox()
        self.DexteritySpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.DexteritySpinBox.setSizePolicy(self.InputsSizePolicy)
        self.DexteritySpinBox.setButtonSymbols(self.DexteritySpinBox.ButtonSymbols.NoButtons)
        self.DexteritySpinBox.setRange(8, 15)
        self.DexteritySpinBox.setValue(8)
        self.DexteritySpinBox.valueChanged.connect(self.UpdateDisplay)

        # Constitution Input
        self.ConstitutionLabel = QLabel("Constitution")
        self.ConstitutionLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.ConstitutionSpinBox = QSpinBox()
        self.ConstitutionSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ConstitutionSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.ConstitutionSpinBox.setButtonSymbols(self.ConstitutionSpinBox.ButtonSymbols.NoButtons)
        self.ConstitutionSpinBox.setRange(8, 15)
        self.ConstitutionSpinBox.setValue(8)
        self.ConstitutionSpinBox.valueChanged.connect(self.UpdateDisplay)

        # Intelligence Input
        self.IntelligenceLabel = QLabel("Intelligence")
        self.IntelligenceLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.IntelligenceSpinBox = QSpinBox()
        self.IntelligenceSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.IntelligenceSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.IntelligenceSpinBox.setButtonSymbols(self.IntelligenceSpinBox.ButtonSymbols.NoButtons)
        self.IntelligenceSpinBox.setRange(8, 15)
        self.IntelligenceSpinBox.setValue(8)
        self.IntelligenceSpinBox.valueChanged.connect(self.UpdateDisplay)

        # Wisdom Input
        self.WisdomLabel = QLabel("Wisdom")
        self.WisdomLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.WisdomSpinBox = QSpinBox()
        self.WisdomSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.WisdomSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.WisdomSpinBox.setButtonSymbols(self.WisdomSpinBox.ButtonSymbols.NoButtons)
        self.WisdomSpinBox.setRange(8, 15)
        self.WisdomSpinBox.setValue(8)
        self.WisdomSpinBox.valueChanged.connect(self.UpdateDisplay)

        # Charisma Input
        self.CharismaLabel = QLabel("Charisma")
        self.CharismaLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.CharismaSpinBox = QSpinBox()
        self.CharismaSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CharismaSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CharismaSpinBox.setButtonSymbols(self.CharismaSpinBox.ButtonSymbols.NoButtons)
        self.CharismaSpinBox.setRange(8, 15)
        self.CharismaSpinBox.setValue(8)
        self.CharismaSpinBox.valueChanged.connect(self.UpdateDisplay)

        # Points Remaining
        self.PointsRemainingLabel = QLabel("Points Remaining")
        self.PointsRemainingLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.PointsRemainingSpinBox = QSpinBox()
        self.PointsRemainingSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.PointsRemainingSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.PointsRemainingSpinBox.setButtonSymbols(self.PointsRemainingSpinBox.ButtonSymbols.NoButtons)
        self.PointsRemainingSpinBox.setRange(-27, 27)
        self.PointsRemainingSpinBox.setValue(27)
        self.PointsRemainingSpinBox.setReadOnly(True)
        self.PointsRemainingSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        # Point Costs Label
        self.PointCostsLabel = QLabel("Min Score:  8\nMax Score:  15\n\nCosts:\n8:  0\n9:  1\n10:  2\n11:  3\n12:  4\n13:  5\n14:  7\n15:  9")

        # Dialog Buttons
        self.DoneButton = QPushButton("Done")
        self.DoneButton.clicked.connect(self.Done)
        self.CancelButton = QPushButton("Cancel")
        self.CancelButton.clicked.connect(self.Cancel)

        # Layout
        self.Layout = QGridLayout()

        self.Layout.addWidget(self.PromptLabel, 0, 0, 1, 2)

        self.InputsLayout = QGridLayout()
        self.InputsLayout.addWidget(self.StrengthLabel, 0, 0)
        self.InputsLayout.addWidget(self.StrengthSpinBox, 0, 1)
        self.InputsLayout.addWidget(self.DexterityLabel, 1, 0)
        self.InputsLayout.addWidget(self.DexteritySpinBox, 1, 1)
        self.InputsLayout.addWidget(self.ConstitutionLabel, 2, 0)
        self.InputsLayout.addWidget(self.ConstitutionSpinBox, 2, 1)
        self.InputsLayout.addWidget(self.IntelligenceLabel, 3, 0)
        self.InputsLayout.addWidget(self.IntelligenceSpinBox, 3, 1)
        self.InputsLayout.addWidget(self.WisdomLabel, 4, 0)
        self.InputsLayout.addWidget(self.WisdomSpinBox, 4, 1)
        self.InputsLayout.addWidget(self.CharismaLabel, 5, 0)
        self.InputsLayout.addWidget(self.CharismaSpinBox, 5, 1)
        self.Layout.addLayout(self.InputsLayout, 1, 0)

        self.PointsRemainingLayout = QGridLayout()
        self.PointsRemainingLayout.addWidget(self.PointsRemainingLabel, 0, 0)
        self.PointsRemainingLayout.addWidget(self.PointsRemainingSpinBox, 1, 0)
        self.PointsRemainingLayout.addWidget(self.PointCostsLabel, 2, 0)
        self.PointsRemainingLayout.setRowStretch(1, 1)
        self.Layout.addLayout(self.PointsRemainingLayout, 1, 1)

        self.DialogButtonsLayout = QGridLayout()
        self.DialogButtonsLayout.addWidget(self.DoneButton, 0, 0)
        self.DialogButtonsLayout.addWidget(self.CancelButton, 0, 1)
        self.Layout.addLayout(self.DialogButtonsLayout, 2, 0, 1, 2)

        self.Layout.setRowStretch(1, 1)

        self.setLayout(self.Layout)

        # Set Window Title and Icon
        self.setWindowTitle(self.CharacterWindow.ScriptName)
        self.setWindowIcon(self.CharacterWindow.WindowIcon)

        self.UpdateDisplay()

        # Execute Dialog
        self.exec()

    def UpdateDisplay(self):
        Scores = []
        Scores.append(self.StrengthSpinBox.value())
        Scores.append(self.DexteritySpinBox.value())
        Scores.append(self.ConstitutionSpinBox.value())
        Scores.append(self.IntelligenceSpinBox.value())
        Scores.append(self.WisdomSpinBox.value())
        Scores.append(self.CharismaSpinBox.value())
        PointsRemaining = self.CharacterWindow.PlayerCharacter.CalculatePointBuyPointsRemaining(Scores)
        self.PointsRemainingSpinBox.setValue(PointsRemaining)
        if PointsRemaining < 0:
            self.PointsRemainingSpinBox.setStyleSheet("QSpinBox {background-color: darkred;}")
        else:
            self.PointsRemainingSpinBox.setStyleSheet("QSpinBox {background-color: darkgreen;}")

    def Done(self):
        if not self.ValidInput(Alert=True):
            return
        self.PointBoughtAbilityScores = {}
        self.PointBoughtAbilityScores["Strength"] = self.StrengthSpinBox.value()
        self.PointBoughtAbilityScores["Dexterity"] = self.DexteritySpinBox.value()
        self.PointBoughtAbilityScores["Constitution"] = self.ConstitutionSpinBox.value()
        self.PointBoughtAbilityScores["Intelligence"] = self.IntelligenceSpinBox.value()
        self.PointBoughtAbilityScores["Wisdom"] = self.WisdomSpinBox.value()
        self.PointBoughtAbilityScores["Charisma"] = self.CharismaSpinBox.value()
        self.close()

    def Cancel(self):
        self.close()

    def ValidInput(self, Alert=False):
        if self.PointsRemainingSpinBox.value() < 0:
            if Alert:
                self.CharacterWindow.DisplayMessageBox("Not enough points remain for these scores.", Icon=QMessageBox.Icon.Warning, Parent=self)
            return False
        return True
