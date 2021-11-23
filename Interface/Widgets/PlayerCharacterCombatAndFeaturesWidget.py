from PyQt5 import QtCore
from PyQt5.QtWidgets import QCheckBox, QFrame, QInputDialog, QLabel, QSizePolicy, QGridLayout, QSpinBox

from Interface.Dialogs.EditMaxHPDialog import EditMaxHPDialog
from Interface.Widgets.CenteredLineEdit import CenteredLineEdit
from Interface.Widgets.DamageButton import DamageButton
from Interface.Widgets.EditButton import EditButton
from Interface.Widgets.HealButton import HealButton


class PlayerCharacterCombatAndFeaturesWidget(QFrame):
    def __init__(self, CharacterWindow):
        # Initialize Frame
        super().__init__()

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Styles
        self.SectionLabelStyle = "QLabel {font-size: 10pt; font-weight: bold;}"

        # Header Label Margin
        self.HeaderLabelMargin = 5

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Create Vitality Table
        self.CreateVitalityTable()

        # Create and Set Layout
        self.CreateAndSetLayout()

    def CreateVitalityTable(self):
        # Header
        self.VitalityHeader = QLabel("Vitality")
        self.VitalityHeader.setStyleSheet(self.SectionLabelStyle)
        self.VitalityHeader.setAlignment(QtCore.Qt.AlignCenter)
        self.VitalityHeader.setMargin(self.HeaderLabelMargin)

        # Temp HP
        self.TempHPLabel = QLabel("Temp HP:")
        self.TempHPLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.TempHPSpinBox = QSpinBox()
        self.TempHPSpinBox.setRange(0, 1000000000)
        self.TempHPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.TempHPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.TempHPSpinBox.setButtonSymbols(self.TempHPSpinBox.NoButtons)
        self.TempHPSpinBox.setValue(0)
        self.TempHPSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat("Temp Health", self.TempHPSpinBox.value()))

        # Current HP
        self.CurrentHPLabel = QLabel("Current HP:")
        self.CurrentHPLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.CurrentHPSpinBox = QSpinBox()
        self.CurrentHPSpinBox.setRange(-1000000000, 1000000000)
        self.CurrentHPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.CurrentHPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CurrentHPSpinBox.setButtonSymbols(self.CurrentHPSpinBox.NoButtons)
        self.CurrentHPSpinBox.setValue(0)
        self.CurrentHPSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat("Current Health", self.CurrentHPSpinBox.value()))

        # Max HP
        self.MaxHPLabel = QLabel("Max HP:")
        self.MaxHPLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.MaxHPSpinBox = QSpinBox()
        self.MaxHPSpinBox.setRange(0, 1000000000)
        self.MaxHPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MaxHPSpinBox.setButtonSymbols(self.MaxHPSpinBox.NoButtons)
        self.MaxHPSpinBox.setValue(0)
        self.MaxHPSpinBox.setReadOnly(True)

        # HP Buttons
        self.DamageButton = DamageButton(self.Damage)
        self.HealButton = HealButton(self.Heal)
        self.EditMaxHPButton = EditButton(self.EditMaxHP, "Edit Max HP")

        # Total Hit Dice
        self.TotalHitDiceLabel = QLabel("Total Hit Dice:")
        self.TotalHitDiceLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.TotalHitDiceLineEdit = CenteredLineEdit()
        self.TotalHitDiceLineEdit.textChanged.connect(lambda: self.CharacterWindow.UpdateStat("Total Hit Dice", self.TotalHitDiceLineEdit.text()))

        # Hit Dice Remaining
        self.HitDiceRemainingLabel = QLabel("Hit Dice Remaining:")
        self.HitDiceRemainingLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.HitDiceRemainingLineEdit = CenteredLineEdit()
        self.HitDiceRemainingLineEdit.textChanged.connect(lambda: self.CharacterWindow.UpdateStat("Hit Dice Remaining", self.HitDiceRemainingLineEdit.text()))

        # Death Saving Throws
        self.DeathSavingThrowsLabel = QLabel("Death Saving Throws:")
        self.DeathSavingThrowsLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.DeathSavingThrowsSuccessesLabel = QLabel("Succ.")
        self.DeathSavingThrowsSuccessesLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.DeathSavingThrowsSuccessCheckBoxOne = QCheckBox()
        self.DeathSavingThrowsSuccessCheckBoxOne.stateChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Death Saving Throws", "Success 1"), self.DeathSavingThrowsSuccessCheckBoxOne.isChecked()))
        self.DeathSavingThrowsSuccessCheckBoxTwo = QCheckBox()
        self.DeathSavingThrowsSuccessCheckBoxTwo.stateChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Death Saving Throws", "Success 2"), self.DeathSavingThrowsSuccessCheckBoxTwo.isChecked()))
        self.DeathSavingThrowsSuccessCheckBoxThree = QCheckBox()
        self.DeathSavingThrowsSuccessCheckBoxThree.stateChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Death Saving Throws", "Success 3"), self.DeathSavingThrowsSuccessCheckBoxThree.isChecked()))

        self.DeathSavingThrowsFailuresLabel = QLabel("Fail")
        self.DeathSavingThrowsFailuresLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.DeathSavingThrowsFailureCheckBoxOne = QCheckBox()
        self.DeathSavingThrowsFailureCheckBoxOne.stateChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Death Saving Throws", "Failure 1"), self.DeathSavingThrowsFailureCheckBoxOne.isChecked()))
        self.DeathSavingThrowsFailureCheckBoxTwo = QCheckBox()
        self.DeathSavingThrowsFailureCheckBoxTwo.stateChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Death Saving Throws", "Failure 2"), self.DeathSavingThrowsFailureCheckBoxTwo.isChecked()))
        self.DeathSavingThrowsFailureCheckBoxThree = QCheckBox()
        self.DeathSavingThrowsFailureCheckBoxThree.stateChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Death Saving Throws", "Failure 3"), self.DeathSavingThrowsFailureCheckBoxThree.isChecked()))

    def CreateAndSetLayout(self):
        # Create Layout
        self.Layout = QGridLayout()

        # Vitality Table
        self.VitalityLayout = QGridLayout()

        self.VitalityLayout.addWidget(self.VitalityHeader, 0, 0, 1, 2)

        self.HPLayout = QGridLayout()
        self.HPLayout.addWidget(self.TempHPLabel, 0, 0)
        self.HPLayout.addWidget(self.TempHPSpinBox, 1, 0)
        self.HPLayout.addWidget(self.CurrentHPLabel, 2, 0)
        self.HPLayout.addWidget(self.CurrentHPSpinBox, 3, 0)
        self.HPLayout.addWidget(self.MaxHPLabel, 4, 0)
        self.HPLayout.addWidget(self.MaxHPSpinBox, 5, 0)
        self.HPButtonsLayout = QGridLayout()
        self.HPButtonsLayout.addWidget(self.DamageButton, 0, 0)
        self.HPButtonsLayout.addWidget(self.HealButton, 0, 1)
        self.HPButtonsLayout.addWidget(self.EditMaxHPButton, 0, 2)
        self.HPLayout.addLayout(self.HPButtonsLayout, 6, 0)
        self.VitalityLayout.addLayout(self.HPLayout, 1, 0, 2, 1)

        self.HitDiceLayout = QGridLayout()
        self.HitDiceLayout.addWidget(self.TotalHitDiceLabel, 0, 0)
        self.HitDiceLayout.addWidget(self.TotalHitDiceLineEdit, 0, 1)
        self.HitDiceLayout.addWidget(self.HitDiceRemainingLabel, 1, 0)
        self.HitDiceLayout.addWidget(self.HitDiceRemainingLineEdit, 1, 1)
        self.VitalityLayout.addLayout(self.HitDiceLayout, 1, 1)

        self.DeathSavingThrowsLayout = QGridLayout()
        self.DeathSavingThrowsLayout.addWidget(self.DeathSavingThrowsLabel, 0, 0, 1, 4)
        self.DeathSavingThrowsLayout.addWidget(self.DeathSavingThrowsSuccessesLabel, 1, 0)
        self.DeathSavingThrowsLayout.addWidget(self.DeathSavingThrowsSuccessCheckBoxOne, 1, 1)
        self.DeathSavingThrowsLayout.addWidget(self.DeathSavingThrowsSuccessCheckBoxTwo, 1, 2)
        self.DeathSavingThrowsLayout.addWidget(self.DeathSavingThrowsSuccessCheckBoxThree, 1, 3)
        self.DeathSavingThrowsLayout.addWidget(self.DeathSavingThrowsFailuresLabel, 2, 0)
        self.DeathSavingThrowsLayout.addWidget(self.DeathSavingThrowsFailureCheckBoxOne, 2, 1)
        self.DeathSavingThrowsLayout.addWidget(self.DeathSavingThrowsFailureCheckBoxTwo, 2, 2)
        self.DeathSavingThrowsLayout.addWidget(self.DeathSavingThrowsFailureCheckBoxThree, 2, 3)
        self.VitalityLayout.addLayout(self.DeathSavingThrowsLayout, 2, 1)

        self.Layout.addLayout(self.VitalityLayout, 0, 0)

        # Set Layout
        self.setLayout(self.Layout)

    def Damage(self):
        DamageAmount, OK = QInputDialog.getInt(self, "Damage", "How much damage?", 1, 1, 1000000000)
        if OK:
            ConcentrationDC = self.CharacterWindow.PlayerCharacter.Damage(DamageAmount)
            self.CharacterWindow.UpdatingFieldsFromPlayerCharacter = True
            self.TempHPSpinBox.setValue(self.CharacterWindow.PlayerCharacter.Stats["Temp Health"])
            self.CurrentHPSpinBox.setValue(self.CharacterWindow.PlayerCharacter.Stats["Current Health"])
            self.CharacterWindow.UpdatingFieldsFromPlayerCharacter = False
            self.CharacterWindow.UpdateUnsavedChangesFlag(True)
            if ConcentrationDC is not None:
                self.CharacterWindow.DisplayMessageBox("DC " + str(ConcentrationDC) + " Constitution saving throw required to maintain concentration.", Parent=self)

    def Heal(self):
        HealAmount, OK = QInputDialog.getInt(self, "Heal", "Heal how much?", 1, 1, 1000000000)
        if OK:
            self.CharacterWindow.PlayerCharacter.Heal(HealAmount, self.CharacterWindow.PlayerCharacter.CalculateMaxHealth())
            self.CharacterWindow.UpdatingFieldsFromPlayerCharacter = True
            self.CurrentHPSpinBox.setValue(self.CharacterWindow.PlayerCharacter.Stats["Current Health"])
            self.CharacterWindow.UpdatingFieldsFromPlayerCharacter = False
            self.CharacterWindow.UpdateUnsavedChangesFlag(True)

    def EditMaxHP(self):
        EditMaxHPDialogInst = EditMaxHPDialog(self.CharacterWindow)
        if EditMaxHPDialogInst.UnsavedChanges:
            self.CharacterWindow.UpdateUnsavedChangesFlag(True)
