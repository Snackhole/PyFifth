from PyQt5 import QtCore
from PyQt5.QtWidgets import QCheckBox, QFrame, QInputDialog, QLabel, QMessageBox, QSizePolicy, QGridLayout, QSpinBox, QTabWidget, QTextEdit

from Interface.Dialogs.EditFeatureDialog import EditFeatureDialog
from Interface.Dialogs.EditMaxHPDialog import EditMaxHPDialog
from Interface.Widgets.AbilityScoreDerivativeWidget import AbilityScoreDerivativeWidget
from Interface.Widgets.CenteredLineEdit import CenteredLineEdit
from Interface.Widgets.FeaturesTreeWidget import FeaturesTreeWidget
from Interface.Widgets.IconButtons import AddButton, DamageButton, DeleteButton, EditButton, HealButton, MoveDownButton, MoveUpButton, RollButton


class PlayerCharacterCombatAndFeaturesWidget(QFrame):
    def __init__(self, CharacterWindow):
        # Initialize Frame
        super().__init__()

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Styles
        self.SectionLabelStyle = "QLabel {font-size: 10pt; font-weight: bold;}"
        self.CombatAndFeaturesSpinBoxStyle = "QSpinBox {font-size: 16pt;}"
        self.HPSpinBoxStyle = "QSpinBox {font-size: 16pt;}"
        self.NegativeCurrentHealthSpinBoxStyle = "QSpinBox {font-size: 16pt; background-color: darkred;}"

        # Header Label Margin
        self.HeaderLabelMargin = 5

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Create Vitality Table
        self.CreateVitalityTable()

        # Create AC Tabs
        self.CreateACTabs()

        # Create Initiative
        self.CreateInitiative()

        # Create Speed
        self.CreateSpeed()

        # Create Ability Score Derivatives
        self.CreateAbilityScoreDerivatives()

        # Create Combat and Features Notes
        self.CreateCombatAndFeaturesNotes()

        # Create Features List
        self.CreateFeaturesList()

        # Create and Set Layout
        self.CreateAndSetLayout()

    def CreateVitalityTable(self):
        # Header Label
        self.VitalityLabel = QLabel("Vitality")
        self.VitalityLabel.setStyleSheet(self.SectionLabelStyle)
        self.VitalityLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.VitalityLabel.setMargin(self.HeaderLabelMargin)

        # Temp HP
        self.TempHPLabel = QLabel("Temp HP:")
        self.TempHPLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.TempHPSpinBox = QSpinBox()
        self.TempHPSpinBox.setRange(0, 1000000000)
        self.TempHPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.TempHPSpinBox.setStyleSheet(self.HPSpinBoxStyle)
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
        self.CurrentHPSpinBox.setStyleSheet(self.HPSpinBoxStyle)
        self.CurrentHPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CurrentHPSpinBox.setButtonSymbols(self.CurrentHPSpinBox.NoButtons)
        self.CurrentHPSpinBox.setValue(5)
        self.CurrentHPSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat("Current Health", self.CurrentHPSpinBox.value()))

        # Max HP
        self.MaxHPLabel = QLabel("Max HP:")
        self.MaxHPLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.MaxHPSpinBox = QSpinBox()
        self.MaxHPSpinBox.setRange(0, 1000000000)
        self.MaxHPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPSpinBox.setStyleSheet(self.HPSpinBoxStyle)
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

        self.DeathSavingThrowsSuccessesLabel = QLabel("Success")
        self.DeathSavingThrowsSuccessesLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.DeathSavingThrowsSuccessCheckBoxOne = QCheckBox()
        self.DeathSavingThrowsSuccessCheckBoxOne.setSizePolicy(self.InputsSizePolicy)
        self.DeathSavingThrowsSuccessCheckBoxOne.stateChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Death Saving Throws", "Success 1"), self.DeathSavingThrowsSuccessCheckBoxOne.isChecked()))
        self.DeathSavingThrowsSuccessCheckBoxTwo = QCheckBox()
        self.DeathSavingThrowsSuccessCheckBoxTwo.setSizePolicy(self.InputsSizePolicy)
        self.DeathSavingThrowsSuccessCheckBoxTwo.stateChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Death Saving Throws", "Success 2"), self.DeathSavingThrowsSuccessCheckBoxTwo.isChecked()))
        self.DeathSavingThrowsSuccessCheckBoxThree = QCheckBox()
        self.DeathSavingThrowsSuccessCheckBoxThree.setSizePolicy(self.InputsSizePolicy)
        self.DeathSavingThrowsSuccessCheckBoxThree.stateChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Death Saving Throws", "Success 3"), self.DeathSavingThrowsSuccessCheckBoxThree.isChecked()))

        self.DeathSavingThrowsFailuresLabel = QLabel("Fail")
        self.DeathSavingThrowsFailuresLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.DeathSavingThrowsFailureCheckBoxOne = QCheckBox()
        self.DeathSavingThrowsFailureCheckBoxOne.setSizePolicy(self.InputsSizePolicy)
        self.DeathSavingThrowsFailureCheckBoxOne.stateChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Death Saving Throws", "Failure 1"), self.DeathSavingThrowsFailureCheckBoxOne.isChecked()))
        self.DeathSavingThrowsFailureCheckBoxTwo = QCheckBox()
        self.DeathSavingThrowsFailureCheckBoxTwo.setSizePolicy(self.InputsSizePolicy)
        self.DeathSavingThrowsFailureCheckBoxTwo.stateChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Death Saving Throws", "Failure 2"), self.DeathSavingThrowsFailureCheckBoxTwo.isChecked()))
        self.DeathSavingThrowsFailureCheckBoxThree = QCheckBox()
        self.DeathSavingThrowsFailureCheckBoxThree.setSizePolicy(self.InputsSizePolicy)
        self.DeathSavingThrowsFailureCheckBoxThree.stateChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Death Saving Throws", "Failure 3"), self.DeathSavingThrowsFailureCheckBoxThree.isChecked()))

    def CreateACTabs(self):
        # AC Tab Widget
        self.ACTabWidget = QTabWidget()
        self.ACTabWidget.setUsesScrollButtons(False)

        # AC Tab Frames
        self.AC1TabFrame = QFrame()
        self.ACTabWidget.addTab(self.AC1TabFrame, "AC 1")

        self.AC2TabFrame = QFrame()
        self.ACTabWidget.addTab(self.AC2TabFrame, "AC 2")

        self.AC3TabFrame = QFrame()
        self.ACTabWidget.addTab(self.AC3TabFrame, "AC 3")

        # AC Spin Boxes
        self.AC1SpinBox = QSpinBox()
        self.AC1SpinBox.setRange(0, 1000000000)
        self.AC1SpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.AC1SpinBox.setStyleSheet(self.CombatAndFeaturesSpinBoxStyle)
        self.AC1SpinBox.setSizePolicy(self.InputsSizePolicy)
        self.AC1SpinBox.setButtonSymbols(self.AC1SpinBox.NoButtons)
        self.AC1SpinBox.setValue(0)
        self.AC1SpinBox.setReadOnly(True)

        self.AC2SpinBox = QSpinBox()
        self.AC2SpinBox.setRange(0, 1000000000)
        self.AC2SpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.AC2SpinBox.setStyleSheet(self.CombatAndFeaturesSpinBoxStyle)
        self.AC2SpinBox.setSizePolicy(self.InputsSizePolicy)
        self.AC2SpinBox.setButtonSymbols(self.AC2SpinBox.NoButtons)
        self.AC2SpinBox.setValue(0)
        self.AC2SpinBox.setReadOnly(True)

        self.AC3SpinBox = QSpinBox()
        self.AC3SpinBox.setRange(0, 1000000000)
        self.AC3SpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.AC3SpinBox.setStyleSheet(self.CombatAndFeaturesSpinBoxStyle)
        self.AC3SpinBox.setSizePolicy(self.InputsSizePolicy)
        self.AC3SpinBox.setButtonSymbols(self.AC3SpinBox.NoButtons)
        self.AC3SpinBox.setValue(0)
        self.AC3SpinBox.setReadOnly(True)

        # AC Edit Buttons
        self.AC1EditButton = EditButton(lambda: self.EditAC("1"), "Edit AC Stat Modifier 1")
        self.AC1EditButton.setSizePolicy(self.InputsSizePolicy)
        self.AC2EditButton = EditButton(lambda: self.EditAC("2"), "Edit AC Stat Modifier 2")
        self.AC2EditButton.setSizePolicy(self.InputsSizePolicy)
        self.AC3EditButton = EditButton(lambda: self.EditAC("3"), "Edit AC Stat Modifier 3")
        self.AC3EditButton.setSizePolicy(self.InputsSizePolicy)

    def CreateInitiative(self):
        # Initiative Label
        self.InitiativeLabel = QLabel("Initiative")
        self.InitiativeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.InitiativeLabel.setStyleSheet(self.SectionLabelStyle)
        self.InitiativeLabel.setMargin(self.HeaderLabelMargin)

        # Initiative Spin Box
        self.InitiativeSpinBox = QSpinBox()
        self.InitiativeSpinBox.setRange(-1000000000, 1000000000)
        self.InitiativeSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.InitiativeSpinBox.setStyleSheet(self.CombatAndFeaturesSpinBoxStyle)
        self.InitiativeSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.InitiativeSpinBox.setButtonSymbols(self.InitiativeSpinBox.NoButtons)
        self.InitiativeSpinBox.setValue(0)
        self.InitiativeSpinBox.setReadOnly(True)

        # Initiative Roll Button
        self.InitiativeRollButton = RollButton(self.RollInitiative, "Roll Initiative")
        self.InitiativeRollButton.setSizePolicy(self.InputsSizePolicy)

        # Initiative Edit Button
        self.InitiativeEditButton = EditButton(self.EditInitiative, "Edit Initiative Modifier")
        self.InitiativeEditButton.setSizePolicy(self.InputsSizePolicy)

    def CreateSpeed(self):
        # Speed Label
        self.SpeedLabel = QLabel("Speed")
        self.SpeedLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SpeedLabel.setStyleSheet(self.SectionLabelStyle)
        self.SpeedLabel.setMargin(self.HeaderLabelMargin)

        # Speed Spin Box
        self.SpeedSpinBox = QSpinBox()
        self.SpeedSpinBox.setRange(0, 1000000000)
        self.SpeedSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.SpeedSpinBox.setStyleSheet(self.CombatAndFeaturesSpinBoxStyle)
        self.SpeedSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpeedSpinBox.setButtonSymbols(self.SpeedSpinBox.NoButtons)
        self.SpeedSpinBox.setValue(30)
        self.SpeedSpinBox.setSuffix(" ft.")
        self.SpeedSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat("Speed", self.SpeedSpinBox.value()))

    def CreateAbilityScoreDerivatives(self):
        # Ability Score Derivatives Label
        self.AbilityScoreDerivativesLabel = QLabel("Ability Score Derivatives")
        self.AbilityScoreDerivativesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.AbilityScoreDerivativesLabel.setStyleSheet(self.SectionLabelStyle)
        self.AbilityScoreDerivativesLabel.setMargin(self.HeaderLabelMargin)

        # Ability Score Derivative Widgets
        self.AbilityScoreDerivativeWidgetInst1 = AbilityScoreDerivativeWidget(self, self.CharacterWindow, 0)
        self.AbilityScoreDerivativeWidgetInst2 = AbilityScoreDerivativeWidget(self, self.CharacterWindow, 1)
        self.AbilityScoreDerivativeWidgetInst3 = AbilityScoreDerivativeWidget(self, self.CharacterWindow, 2)

    def CreateCombatAndFeaturesNotes(self):
        # Combat and Features Notes Label
        self.CombatAndFeaturesNotesLabel = QLabel("Combat and Features Notes")
        self.CombatAndFeaturesNotesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.CombatAndFeaturesNotesLabel.setStyleSheet(self.SectionLabelStyle)
        self.CombatAndFeaturesNotesLabel.setMargin(self.HeaderLabelMargin)

        # Combat and Features Notes Text Edit
        self.CombatAndFeaturesNotesTextEdit = QTextEdit()
        self.CombatAndFeaturesNotesTextEdit.setTabChangesFocus(True)
        self.CombatAndFeaturesNotesTextEdit.textChanged.connect(lambda: self.CharacterWindow.UpdateStat("Combat and Features Notes", self.CombatAndFeaturesNotesTextEdit.toPlainText()))

    def CreateFeaturesList(self):
        # Features Label
        self.FeaturesLabel = QLabel("Features")
        self.FeaturesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.FeaturesLabel.setStyleSheet(self.SectionLabelStyle)
        self.FeaturesLabel.setMargin(self.HeaderLabelMargin)

        # Features Tree Widget
        self.FeaturesTreeWidget = FeaturesTreeWidget(self.CharacterWindow)
        self.FeaturesTreeWidget.itemActivated.connect(self.EditFeature)

        # Buttons
        self.AddFeatureButton = AddButton(self.AddFeature, "Add Feature")
        self.AddFeatureButton.setSizePolicy(self.InputsSizePolicy)
        self.DeleteFeatureButton = DeleteButton(self.DeleteFeature, "Delete Feature")
        self.DeleteFeatureButton.setSizePolicy(self.InputsSizePolicy)
        self.EditFeatureButton = EditButton(self.EditFeature, "Edit Feature")
        self.EditFeatureButton.setSizePolicy(self.InputsSizePolicy)
        self.MoveFeatureUpButton = MoveUpButton(self.MoveFeatureUp, "Move Feature Up")
        self.MoveFeatureUpButton.setSizePolicy(self.InputsSizePolicy)
        self.MoveFeatureDownButton = MoveDownButton(self.MoveFeatureDown, "Move Feature Down")
        self.MoveFeatureDownButton.setSizePolicy(self.InputsSizePolicy)

    def CreateAndSetLayout(self):
        # Create Layout
        self.Layout = QGridLayout()

        # Vitality Table
        self.VitalityLayout = QGridLayout()

        self.VitalityLayout.addWidget(self.VitalityLabel, 0, 0, 1, 2)

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
        for Row in [1, 3, 5]:
            self.HPLayout.setRowStretch(Row, 1)
        self.VitalityLayout.addLayout(self.HPLayout, 1, 0, 2, 1)

        self.HitDiceLayout = QGridLayout()
        self.HitDiceLayout.addWidget(self.TotalHitDiceLabel, 0, 0)
        self.HitDiceLayout.addWidget(self.TotalHitDiceLineEdit, 0, 1)
        self.HitDiceLayout.addWidget(self.HitDiceRemainingLabel, 1, 0)
        self.HitDiceLayout.addWidget(self.HitDiceRemainingLineEdit, 1, 1)
        self.HitDiceLayout.setColumnStretch(1, 1)
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
        for Row in [1, 2]:
            self.DeathSavingThrowsLayout.setRowStretch(Row, 1)
        self.VitalityLayout.addLayout(self.DeathSavingThrowsLayout, 2, 1)

        self.VitalityLayout.setRowStretch(2, 1)
        self.VitalityLayout.setColumnStretch(1, 1)

        self.Layout.addLayout(self.VitalityLayout, 0, 0, 3, 1)

        # AC Tab Widget
        self.AC1Layout = QGridLayout()
        self.AC1Layout.addWidget(self.AC1SpinBox, 0, 0)
        self.AC1Layout.addWidget(self.AC1EditButton, 0, 1)
        self.AC1Layout.setColumnStretch(0, 1)
        self.AC1TabFrame.setLayout(self.AC1Layout)
        self.AC2Layout = QGridLayout()
        self.AC2Layout.addWidget(self.AC2SpinBox, 0, 0)
        self.AC2Layout.addWidget(self.AC2EditButton, 0, 1)
        self.AC2Layout.setColumnStretch(0, 1)
        self.AC2TabFrame.setLayout(self.AC2Layout)
        self.AC3Layout = QGridLayout()
        self.AC3Layout.addWidget(self.AC3SpinBox, 0, 0)
        self.AC3Layout.addWidget(self.AC3EditButton, 0, 1)
        self.AC3Layout.setColumnStretch(0, 1)
        self.AC3TabFrame.setLayout(self.AC3Layout)

        self.Layout.addWidget(self.ACTabWidget, 0, 1)

        # Initiative
        self.InitiativeLayout = QGridLayout()
        self.InitiativeLayout.addWidget(self.InitiativeLabel, 0, 0, 1, 3)
        self.InitiativeLayout.addWidget(self.InitiativeSpinBox, 1, 0)
        self.InitiativeLayout.addWidget(self.InitiativeRollButton, 1, 1)
        self.InitiativeLayout.addWidget(self.InitiativeEditButton, 1, 2)
        self.InitiativeLayout.setRowStretch(1, 1)
        self.InitiativeLayout.setColumnStretch(0, 1)
        self.Layout.addLayout(self.InitiativeLayout, 1, 1)

        # Speed
        self.SpeedLayout = QGridLayout()
        self.SpeedLayout.addWidget(self.SpeedLabel, 0, 0)
        self.SpeedLayout.addWidget(self.SpeedSpinBox, 1, 0)
        self.SpeedLayout.setRowStretch(1, 1)
        self.Layout.addLayout(self.SpeedLayout, 2, 1)

        # Combat and Features Notes
        self.CombatAndFeaturesNotesLayout = QGridLayout()
        self.CombatAndFeaturesNotesLayout.addWidget(self.CombatAndFeaturesNotesLabel, 0, 0)
        self.CombatAndFeaturesNotesLayout.addWidget(self.CombatAndFeaturesNotesTextEdit, 1, 0)
        self.CombatAndFeaturesNotesLayout.setRowStretch(1, 1)
        self.Layout.addLayout(self.CombatAndFeaturesNotesLayout, 3, 0)

        # Ability Score Derivatives
        self.AbilityScoreDerivativesLayout = QGridLayout()
        self.AbilityScoreDerivativesLayout.addWidget(self.AbilityScoreDerivativesLabel, 0, 0)
        self.AbilityScoreDerivativesLayout.addWidget(self.AbilityScoreDerivativeWidgetInst1, 1, 0)
        self.AbilityScoreDerivativesLayout.addWidget(self.AbilityScoreDerivativeWidgetInst2, 2, 0)
        self.AbilityScoreDerivativesLayout.addWidget(self.AbilityScoreDerivativeWidgetInst3, 3, 0)
        self.Layout.addLayout(self.AbilityScoreDerivativesLayout, 3, 1)

        # Features List
        self.FeaturesLayout = QGridLayout()
        self.FeaturesLayout.addWidget(self.FeaturesLabel, 0, 0, 1, 5)
        self.FeaturesLayout.addWidget(self.AddFeatureButton, 1, 0)
        self.FeaturesLayout.addWidget(self.DeleteFeatureButton, 1, 1)
        self.FeaturesLayout.addWidget(self.EditFeatureButton, 1, 2)
        self.FeaturesLayout.addWidget(self.MoveFeatureUpButton, 1, 3)
        self.FeaturesLayout.addWidget(self.MoveFeatureDownButton, 1, 4)
        self.FeaturesLayout.addWidget(self.FeaturesTreeWidget, 2, 0, 1, 5)
        self.FeaturesLayout.setRowStretch(2, 1)
        self.Layout.addLayout(self.FeaturesLayout, 0, 2, 5, 1)

        # Layout Stretching
        self.Layout.setRowStretch(3, 1)
        self.Layout.setColumnStretch(2, 1)

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

    def EditAC(self, AC):
        self.CharacterWindow.EditStatModifier(self, self.CharacterWindow.PlayerCharacter.Stats["AC Stat Modifier " + AC], "AC Stat Modifier " + AC)

    def RollInitiative(self):
        self.CharacterWindow.PlayerCharacter.Stats["Dice Roller"].RollDice(1, 20, self.CharacterWindow.PlayerCharacter.Stats["Initiative Stat Modifier"], LogPrefix="Initiative:\n")
        self.CharacterWindow.UpdateUnsavedChangesFlag(True)

    def EditInitiative(self):
        self.CharacterWindow.EditStatModifier(self, self.CharacterWindow.PlayerCharacter.Stats["Initiative Stat Modifier"], "Initiative Stat Modifier")

    def AddFeature(self):
        FeatureIndex = self.CharacterWindow.PlayerCharacter.AddFeature()
        self.CharacterWindow.UpdateDisplay()
        EditFeatureDialogInst = EditFeatureDialog(self.CharacterWindow, self.CharacterWindow.PlayerCharacter.Stats["Features"], FeatureIndex, AddMode=True)
        if EditFeatureDialogInst.Cancelled:
            self.CharacterWindow.PlayerCharacter.DeleteLastFeature()
            self.CharacterWindow.UpdateDisplay()
        else:
            self.CharacterWindow.UpdateUnsavedChangesFlag(True)
            self.FeaturesTreeWidget.SelectIndex(FeatureIndex)

    def DeleteFeature(self):
        CurrentSelection = self.FeaturesTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            if self.CharacterWindow.DisplayMessageBox("Are you sure you want to delete this feature?  This cannot be undone.", Icon=QMessageBox.Warning, Buttons=(QMessageBox.Yes | QMessageBox.No)) == QMessageBox.Yes:
                CurrentFeature = CurrentSelection[0]
                CurrentFeatureIndex = CurrentFeature.Index
                self.CharacterWindow.PlayerCharacter.DeleteFeature(CurrentFeatureIndex)
                self.CharacterWindow.UpdateUnsavedChangesFlag(True)
                FeaturesLength = len(self.CharacterWindow.PlayerCharacter.Stats["Features"])
                if FeaturesLength > 0:
                    self.FeaturesTreeWidget.SelectIndex(CurrentFeatureIndex if CurrentFeatureIndex < FeaturesLength else FeaturesLength - 1)

    def EditFeature(self):
        CurrentSelection = self.FeaturesTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentFeature = CurrentSelection[0]
            CurrentFeatureIndex = CurrentFeature.Index
            EditFeatureDialogInst = EditFeatureDialog(self.CharacterWindow, self.CharacterWindow.PlayerCharacter.Stats["Features"], CurrentFeatureIndex)
            if EditFeatureDialogInst.UnsavedChanges:
                self.CharacterWindow.UpdateUnsavedChangesFlag(True)
                self.FeaturesTreeWidget.SelectIndex(CurrentFeatureIndex)

    def MoveFeatureUp(self):
        self.MoveFeature(-1)

    def MoveFeatureDown(self):
        self.MoveFeature(1)

    def MoveFeature(self, Delta):
        CurrentSelection = self.FeaturesTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentFeature = CurrentSelection[0]
            CurrentFeatureIndex = CurrentFeature.Index
            if self.CharacterWindow.PlayerCharacter.MoveFeature(CurrentFeatureIndex, Delta):
                self.CharacterWindow.UpdateUnsavedChangesFlag(True)
                self.FeaturesTreeWidget.SelectIndex(CurrentFeatureIndex + Delta)
