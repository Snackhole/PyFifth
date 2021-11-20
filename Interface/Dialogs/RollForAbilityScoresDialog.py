from PyQt5 import QtCore
from PyQt5.QtWidgets import QComboBox, QDialog, QGridLayout, QPushButton, QSpinBox, QMessageBox, QSizePolicy


class RollForAbilityScoresDialog(QDialog):
    def __init__(self, Parent, CharacterWindow):
        super().__init__(parent=Parent)

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Variables
        self.RolledAbilityScores = None
        self.AbilitiesList = self.CharacterWindow.PlayerCharacter.Abilities
        self.InputsSuffixes = ["One", "Two", "Three", "Four", "Five", "Six"]

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Roll Button
        self.RollAbilityScoresButton = QPushButton("Roll Ability Scores")
        self.RollAbilityScoresButton.clicked.connect(self.RollAbilityScores)

        # Inputs
        self.Inputs = {}
        for InputsSuffix in self.InputsSuffixes:
            # Combo Box
            self.Inputs["ComboBox " + InputsSuffix] = QComboBox()
            ComboBox = self.Inputs["ComboBox " + InputsSuffix]
            ComboBox.setSizePolicy(self.InputsSizePolicy)
            ComboBox.addItems(self.AbilitiesList)
            ComboBox.setEditable(False)

            # SpinBox
            self.Inputs["SpinBox " + InputsSuffix] = QSpinBox()
            SpinBox = self.Inputs["SpinBox " + InputsSuffix]
            SpinBox.setAlignment(QtCore.Qt.AlignCenter)
            SpinBox.setSizePolicy(self.InputsSizePolicy)
            SpinBox.setButtonSymbols(self.Inputs["SpinBox " + InputsSuffix].NoButtons)
            SpinBox.setRange(0, 18)
            SpinBox.setSpecialValueText("Not Rolled")
            SpinBox.setValue(0)
            SpinBox.setReadOnly(True)
            SpinBox.setMinimumWidth(70)

        # Dialog Buttons
        self.DoneButton = QPushButton("Done")
        self.DoneButton.clicked.connect(self.Done)
        self.CancelButton = QPushButton("Cancel")
        self.CancelButton.clicked.connect(self.Cancel)

        # Layout
        self.Layout = QGridLayout()

        self.Layout.addWidget(self.RollAbilityScoresButton, 0, 0)

        self.InputsLayout = QGridLayout()
        Row = 0
        for InputsSuffix in self.InputsSuffixes:
            self.InputsLayout.addWidget(self.Inputs["ComboBox " + InputsSuffix], Row, 0)
            self.InputsLayout.addWidget(self.Inputs["SpinBox " + InputsSuffix], Row, 1)
            Row += 1
        self.Layout.addLayout(self.InputsLayout, 1, 0)

        self.DialogButtonsLayout = QGridLayout()
        self.DialogButtonsLayout.addWidget(self.DoneButton, 0, 0)
        self.DialogButtonsLayout.addWidget(self.CancelButton, 0, 1)
        self.Layout.addLayout(self.DialogButtonsLayout, 2, 0)

        self.Layout.setRowStretch(2, 1)

        self.setLayout(self.Layout)

        # Set Window Title and Icon
        self.setWindowTitle(self.CharacterWindow.ScriptName)
        self.setWindowIcon(self.CharacterWindow.WindowIcon)

        # Execute Dialog
        self.exec_()

    def RollAbilityScores(self):
        RolledScores = self.CharacterWindow.PlayerCharacter.GetRolledAbilityScores()
        Index = 0
        for RolledScore in RolledScores:
            self.Inputs["SpinBox " + self.InputsSuffixes[Index]].setValue(RolledScore)
            Index += 1

    def Done(self):
        if not self.ValidInput(Alert=True):
            return
        self.RolledAbilityScores = {}
        for InputsSuffix in self.InputsSuffixes:
            Ability = self.Inputs["ComboBox " + InputsSuffix].currentText()
            Score = self.Inputs["SpinBox " + InputsSuffix].value()
            self.RolledAbilityScores[Ability] = Score
        self.close()

    def Cancel(self):
        self.close()

    def ValidInput(self, Alert=False):
        AbilitiesSet = set()
        for InputsSuffix in self.InputsSuffixes:
            if self.Inputs["SpinBox " + InputsSuffix].value() == 0:
                if Alert:
                    self.CharacterWindow.DisplayMessageBox("No scores have been rolled.", Icon=QMessageBox.Warning, Parent=self)
                return False
            AbilitiesSet.add(self.Inputs["ComboBox " + InputsSuffix].currentText())
        if len(AbilitiesSet) != 6:
            if Alert:
                self.CharacterWindow.DisplayMessageBox("Each rolled score must be uniquely assigned to one of the six ability scores.", Icon=QMessageBox.Warning, Parent=self)
            return False
        return True
