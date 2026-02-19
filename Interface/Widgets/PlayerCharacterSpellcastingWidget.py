from PyQt6 import QtCore
from PyQt6.QtWidgets import QFrame, QLabel, QSizePolicy, QGridLayout, QSpinBox, QMessageBox

from Interface.Dialogs.EditSpellDialog import EditSpellDialog
from Interface.Dialogs.SpendOrRestoreSpellPointsDialog import SpendOrRestoreSpellPointsDialog
from Interface.Widgets.AbilityScoreDerivativeWidget import AbilityScoreDerivativeWidget
from Interface.Widgets.IconButtons import AddButton, DeleteButton, EditButton, MoveDownButton, MoveUpButton
from Interface.Widgets.IndentingTextEdit import IndentingTextEdit
from Interface.Widgets.SpellListTreeWidget import SpellListTreeWidget
from Interface.Widgets.ToggleButtons import ConcentratingButton


class PlayerCharacterSpellcastingWidget(QFrame):
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
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        # Create Spellcasting Abilities
        self.CreateSpellcastingAbilities()

        # Create Concentrating Button
        self.CreateConcentratingButton()

        # Create Spell Notes
        self.CreateSpellNotes()

        # Create Spell Slots
        self.CreateSpellSlots()

        # Create Spell Points
        self.CreateSpellPoints()

        # Create Spell List
        self.CreateSpellList()

        # Create and Set Layout
        self.CreateAndSetLayout()

    def CreateSpellcastingAbilities(self):
        # Spellcasting Abilities Label
        self.SpellcastingAbilitiesLabel = QLabel("Spellcasting Abilities")
        self.SpellcastingAbilitiesLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellcastingAbilitiesLabel.setStyleSheet(self.SectionLabelStyle)
        self.SpellcastingAbilitiesLabel.setMargin(self.HeaderLabelMargin)

        # Ability Score Derivative Widgets
        self.SpellcastingAbilityWidgetInst1 = AbilityScoreDerivativeWidget(self.CharacterWindow, 3)
        self.SpellcastingAbilityWidgetInst2 = AbilityScoreDerivativeWidget(self.CharacterWindow, 4)
        self.SpellcastingAbilityWidgetInst3 = AbilityScoreDerivativeWidget(self.CharacterWindow, 5)

    def CreateConcentratingButton(self):
        self.ConcentratingButton = ConcentratingButton(self.CharacterWindow)

    def CreateSpellNotes(self):
        # Spell Notes Label
        self.SpellNotesLabel = QLabel("Spell Notes")
        self.SpellNotesLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellNotesLabel.setStyleSheet(self.SectionLabelStyle)
        self.SpellNotesLabel.setMargin(self.HeaderLabelMargin)

        # Spell Notes Text Edit
        self.SpellNotesTextEdit = IndentingTextEdit(TextChangedSlot=lambda: self.CharacterWindow.UpdateStat("Spell Notes", self.SpellNotesTextEdit.toPlainText()))
        self.SpellNotesTextEdit.setTabChangesFocus(True)

    def CreateSpellSlots(self):
        # Spell Slots Label
        self.SpellSlotsLabel = QLabel("Spell Slots")
        self.SpellSlotsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlotsLabel.setStyleSheet(self.SectionLabelStyle)
        self.SpellSlotsLabel.setMargin(self.HeaderLabelMargin)

        # Header Labels
        self.SpellSlotsLevelLabel = QLabel("Level")
        self.SpellSlotsLevelLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlotsLevelLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.SpellSlotsLevelLabel.setMargin(5)
        self.SpellSlotsTotalSlotsLabel = QLabel("Slots")
        self.SpellSlotsTotalSlotsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlotsTotalSlotsLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.SpellSlotsTotalSlotsLabel.setMargin(5)
        self.SpellSlotsUsedSlotsLabel = QLabel("Used")
        self.SpellSlotsUsedSlotsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlotsUsedSlotsLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.SpellSlotsUsedSlotsLabel.setMargin(5)

        # Level Labels
        self.SpellSlots1stLabel = QLabel("1st")
        self.SpellSlots1stLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlots2ndLabel = QLabel("2nd")
        self.SpellSlots2ndLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlots3rdLabel = QLabel("3rd")
        self.SpellSlots3rdLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlots4thLabel = QLabel("4th")
        self.SpellSlots4thLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlots5thLabel = QLabel("5th")
        self.SpellSlots5thLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlots6thLabel = QLabel("6th")
        self.SpellSlots6thLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlots7thLabel = QLabel("7th")
        self.SpellSlots7thLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlots8thLabel = QLabel("8th")
        self.SpellSlots8thLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlots9thLabel = QLabel("9th")
        self.SpellSlots9thLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Total Slots Spin Boxes
        self.SpellSlotsTotalSlots1stSpinBox = QSpinBox()
        self.SpellSlotsTotalSlots1stSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlotsTotalSlots1stSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpellSlotsTotalSlots1stSpinBox.setButtonSymbols(self.SpellSlotsTotalSlots1stSpinBox.ButtonSymbols.NoButtons)
        self.SpellSlotsTotalSlots1stSpinBox.setRange(0, 1000000000)
        self.SpellSlotsTotalSlots1stSpinBox.setValue(0)
        self.SpellSlotsTotalSlots1stSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Spell Slots", "1st", "Total Slots"), self.SpellSlotsTotalSlots1stSpinBox.value()))

        self.SpellSlotsTotalSlots2ndSpinBox = QSpinBox()
        self.SpellSlotsTotalSlots2ndSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlotsTotalSlots2ndSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpellSlotsTotalSlots2ndSpinBox.setButtonSymbols(self.SpellSlotsTotalSlots2ndSpinBox.ButtonSymbols.NoButtons)
        self.SpellSlotsTotalSlots2ndSpinBox.setRange(0, 1000000000)
        self.SpellSlotsTotalSlots2ndSpinBox.setValue(0)
        self.SpellSlotsTotalSlots2ndSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Spell Slots", "2nd", "Total Slots"), self.SpellSlotsTotalSlots2ndSpinBox.value()))

        self.SpellSlotsTotalSlots3rdSpinBox = QSpinBox()
        self.SpellSlotsTotalSlots3rdSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlotsTotalSlots3rdSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpellSlotsTotalSlots3rdSpinBox.setButtonSymbols(self.SpellSlotsTotalSlots3rdSpinBox.ButtonSymbols.NoButtons)
        self.SpellSlotsTotalSlots3rdSpinBox.setRange(0, 1000000000)
        self.SpellSlotsTotalSlots3rdSpinBox.setValue(0)
        self.SpellSlotsTotalSlots3rdSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Spell Slots", "3rd", "Total Slots"), self.SpellSlotsTotalSlots3rdSpinBox.value()))

        self.SpellSlotsTotalSlots4thSpinBox = QSpinBox()
        self.SpellSlotsTotalSlots4thSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlotsTotalSlots4thSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpellSlotsTotalSlots4thSpinBox.setButtonSymbols(self.SpellSlotsTotalSlots4thSpinBox.ButtonSymbols.NoButtons)
        self.SpellSlotsTotalSlots4thSpinBox.setRange(0, 1000000000)
        self.SpellSlotsTotalSlots4thSpinBox.setValue(0)
        self.SpellSlotsTotalSlots4thSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Spell Slots", "4th", "Total Slots"), self.SpellSlotsTotalSlots4thSpinBox.value()))

        self.SpellSlotsTotalSlots5thSpinBox = QSpinBox()
        self.SpellSlotsTotalSlots5thSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlotsTotalSlots5thSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpellSlotsTotalSlots5thSpinBox.setButtonSymbols(self.SpellSlotsTotalSlots5thSpinBox.ButtonSymbols.NoButtons)
        self.SpellSlotsTotalSlots5thSpinBox.setRange(0, 1000000000)
        self.SpellSlotsTotalSlots5thSpinBox.setValue(0)
        self.SpellSlotsTotalSlots5thSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Spell Slots", "5th", "Total Slots"), self.SpellSlotsTotalSlots5thSpinBox.value()))

        self.SpellSlotsTotalSlots6thSpinBox = QSpinBox()
        self.SpellSlotsTotalSlots6thSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlotsTotalSlots6thSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpellSlotsTotalSlots6thSpinBox.setButtonSymbols(self.SpellSlotsTotalSlots6thSpinBox.ButtonSymbols.NoButtons)
        self.SpellSlotsTotalSlots6thSpinBox.setRange(0, 1000000000)
        self.SpellSlotsTotalSlots6thSpinBox.setValue(0)
        self.SpellSlotsTotalSlots6thSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Spell Slots", "6th", "Total Slots"), self.SpellSlotsTotalSlots6thSpinBox.value()))

        self.SpellSlotsTotalSlots7thSpinBox = QSpinBox()
        self.SpellSlotsTotalSlots7thSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlotsTotalSlots7thSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpellSlotsTotalSlots7thSpinBox.setButtonSymbols(self.SpellSlotsTotalSlots7thSpinBox.ButtonSymbols.NoButtons)
        self.SpellSlotsTotalSlots7thSpinBox.setRange(0, 1000000000)
        self.SpellSlotsTotalSlots7thSpinBox.setValue(0)
        self.SpellSlotsTotalSlots7thSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Spell Slots", "7th", "Total Slots"), self.SpellSlotsTotalSlots7thSpinBox.value()))

        self.SpellSlotsTotalSlots8thSpinBox = QSpinBox()
        self.SpellSlotsTotalSlots8thSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlotsTotalSlots8thSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpellSlotsTotalSlots8thSpinBox.setButtonSymbols(self.SpellSlotsTotalSlots8thSpinBox.ButtonSymbols.NoButtons)
        self.SpellSlotsTotalSlots8thSpinBox.setRange(0, 1000000000)
        self.SpellSlotsTotalSlots8thSpinBox.setValue(0)
        self.SpellSlotsTotalSlots8thSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Spell Slots", "8th", "Total Slots"), self.SpellSlotsTotalSlots8thSpinBox.value()))

        self.SpellSlotsTotalSlots9thSpinBox = QSpinBox()
        self.SpellSlotsTotalSlots9thSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlotsTotalSlots9thSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpellSlotsTotalSlots9thSpinBox.setButtonSymbols(self.SpellSlotsTotalSlots9thSpinBox.ButtonSymbols.NoButtons)
        self.SpellSlotsTotalSlots9thSpinBox.setRange(0, 1000000000)
        self.SpellSlotsTotalSlots9thSpinBox.setValue(0)
        self.SpellSlotsTotalSlots9thSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Spell Slots", "9th", "Total Slots"), self.SpellSlotsTotalSlots9thSpinBox.value()))

        # Used Slots Spin Boxes
        self.SpellSlotsUsedSlots1stSpinBox = QSpinBox()
        self.SpellSlotsUsedSlots1stSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlotsUsedSlots1stSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpellSlotsUsedSlots1stSpinBox.setButtonSymbols(self.SpellSlotsUsedSlots1stSpinBox.ButtonSymbols.NoButtons)
        self.SpellSlotsUsedSlots1stSpinBox.setRange(0, 1000000000)
        self.SpellSlotsUsedSlots1stSpinBox.setValue(0)
        self.SpellSlotsUsedSlots1stSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Spell Slots", "1st", "Used Slots"), self.SpellSlotsUsedSlots1stSpinBox.value()))

        self.SpellSlotsUsedSlots2ndSpinBox = QSpinBox()
        self.SpellSlotsUsedSlots2ndSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlotsUsedSlots2ndSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpellSlotsUsedSlots2ndSpinBox.setButtonSymbols(self.SpellSlotsUsedSlots2ndSpinBox.ButtonSymbols.NoButtons)
        self.SpellSlotsUsedSlots2ndSpinBox.setRange(0, 1000000000)
        self.SpellSlotsUsedSlots2ndSpinBox.setValue(0)
        self.SpellSlotsUsedSlots2ndSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Spell Slots", "2nd", "Used Slots"), self.SpellSlotsUsedSlots2ndSpinBox.value()))

        self.SpellSlotsUsedSlots3rdSpinBox = QSpinBox()
        self.SpellSlotsUsedSlots3rdSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlotsUsedSlots3rdSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpellSlotsUsedSlots3rdSpinBox.setButtonSymbols(self.SpellSlotsUsedSlots3rdSpinBox.ButtonSymbols.NoButtons)
        self.SpellSlotsUsedSlots3rdSpinBox.setRange(0, 1000000000)
        self.SpellSlotsUsedSlots3rdSpinBox.setValue(0)
        self.SpellSlotsUsedSlots3rdSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Spell Slots", "3rd", "Used Slots"), self.SpellSlotsUsedSlots3rdSpinBox.value()))

        self.SpellSlotsUsedSlots4thSpinBox = QSpinBox()
        self.SpellSlotsUsedSlots4thSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlotsUsedSlots4thSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpellSlotsUsedSlots4thSpinBox.setButtonSymbols(self.SpellSlotsUsedSlots4thSpinBox.ButtonSymbols.NoButtons)
        self.SpellSlotsUsedSlots4thSpinBox.setRange(0, 1000000000)
        self.SpellSlotsUsedSlots4thSpinBox.setValue(0)
        self.SpellSlotsUsedSlots4thSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Spell Slots", "4th", "Used Slots"), self.SpellSlotsUsedSlots4thSpinBox.value()))

        self.SpellSlotsUsedSlots5thSpinBox = QSpinBox()
        self.SpellSlotsUsedSlots5thSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlotsUsedSlots5thSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpellSlotsUsedSlots5thSpinBox.setButtonSymbols(self.SpellSlotsUsedSlots5thSpinBox.ButtonSymbols.NoButtons)
        self.SpellSlotsUsedSlots5thSpinBox.setRange(0, 1000000000)
        self.SpellSlotsUsedSlots5thSpinBox.setValue(0)
        self.SpellSlotsUsedSlots5thSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Spell Slots", "5th", "Used Slots"), self.SpellSlotsUsedSlots5thSpinBox.value()))

        self.SpellSlotsUsedSlots6thSpinBox = QSpinBox()
        self.SpellSlotsUsedSlots6thSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlotsUsedSlots6thSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpellSlotsUsedSlots6thSpinBox.setButtonSymbols(self.SpellSlotsUsedSlots6thSpinBox.ButtonSymbols.NoButtons)
        self.SpellSlotsUsedSlots6thSpinBox.setRange(0, 1000000000)
        self.SpellSlotsUsedSlots6thSpinBox.setValue(0)
        self.SpellSlotsUsedSlots6thSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Spell Slots", "6th", "Used Slots"), self.SpellSlotsUsedSlots6thSpinBox.value()))

        self.SpellSlotsUsedSlots7thSpinBox = QSpinBox()
        self.SpellSlotsUsedSlots7thSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlotsUsedSlots7thSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpellSlotsUsedSlots7thSpinBox.setButtonSymbols(self.SpellSlotsUsedSlots7thSpinBox.ButtonSymbols.NoButtons)
        self.SpellSlotsUsedSlots7thSpinBox.setRange(0, 1000000000)
        self.SpellSlotsUsedSlots7thSpinBox.setValue(0)
        self.SpellSlotsUsedSlots7thSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Spell Slots", "7th", "Used Slots"), self.SpellSlotsUsedSlots7thSpinBox.value()))

        self.SpellSlotsUsedSlots8thSpinBox = QSpinBox()
        self.SpellSlotsUsedSlots8thSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlotsUsedSlots8thSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpellSlotsUsedSlots8thSpinBox.setButtonSymbols(self.SpellSlotsUsedSlots8thSpinBox.ButtonSymbols.NoButtons)
        self.SpellSlotsUsedSlots8thSpinBox.setRange(0, 1000000000)
        self.SpellSlotsUsedSlots8thSpinBox.setValue(0)
        self.SpellSlotsUsedSlots8thSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Spell Slots", "8th", "Used Slots"), self.SpellSlotsUsedSlots8thSpinBox.value()))

        self.SpellSlotsUsedSlots9thSpinBox = QSpinBox()
        self.SpellSlotsUsedSlots9thSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellSlotsUsedSlots9thSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpellSlotsUsedSlots9thSpinBox.setButtonSymbols(self.SpellSlotsUsedSlots9thSpinBox.ButtonSymbols.NoButtons)
        self.SpellSlotsUsedSlots9thSpinBox.setRange(0, 1000000000)
        self.SpellSlotsUsedSlots9thSpinBox.setValue(0)
        self.SpellSlotsUsedSlots9thSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Spell Slots", "9th", "Used Slots"), self.SpellSlotsUsedSlots9thSpinBox.value()))

    def CreateSpellPoints(self):
        # Spell Points Label
        self.SpellPointsLabel = QLabel("Spell Points")
        self.SpellPointsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellPointsLabel.setStyleSheet(self.SectionLabelStyle)
        self.SpellPointsLabel.setMargin(self.HeaderLabelMargin)

        # Spell Points Max
        self.SpellPointsMaxLabel = QLabel("Max")
        self.SpellPointsMaxLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellPointsMaxLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.SpellPointsMaxLabel.setMargin(5)

        self.SpellPointsMaxSpinBox = QSpinBox()
        self.SpellPointsMaxSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellPointsMaxSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpellPointsMaxSpinBox.setButtonSymbols(self.SpellPointsMaxSpinBox.ButtonSymbols.NoButtons)
        self.SpellPointsMaxSpinBox.setRange(0, 1000000000)
        self.SpellPointsMaxSpinBox.setSpecialValueText("N/A")
        self.SpellPointsMaxSpinBox.setReadOnly(True)
        self.SpellPointsMaxSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.SpellPointsMaxEditButton = EditButton(self.EditBonusSpellPointsStatModifier, "Edit Bonus Spell Points Stat Modifier")
        self.SpellPointsMaxEditButton.setSizePolicy(self.InputsSizePolicy)

        # Spell Points Remaining
        self.SpellPointsRemainingLabel = QLabel("Remaining")
        self.SpellPointsRemainingLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellPointsRemainingLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.SpellPointsRemainingLabel.setMargin(5)

        self.SpellPointsRemainingSpinBox = QSpinBox()
        self.SpellPointsRemainingSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellPointsRemainingSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpellPointsRemainingSpinBox.setButtonSymbols(self.SpellPointsRemainingSpinBox.ButtonSymbols.NoButtons)
        self.SpellPointsRemainingSpinBox.setRange(0, 1000000000)
        self.SpellPointsRemainingSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat("Current Spell Points", self.SpellPointsRemainingSpinBox.value()))

        self.SpellPointsSpendButton = DeleteButton(self.SpendSpellPoints, "Spend Spell Points")
        self.SpellPointsSpendButton.setSizePolicy(self.InputsSizePolicy)

        self.SpellPointsRestoreButton = AddButton(self.RestoreSpellPoints, "Restore Spell Points")
        self.SpellPointsRestoreButton.setSizePolicy(self.InputsSizePolicy)

    def CreateSpellList(self):
        # Spell List Label
        self.SpellListLabel = QLabel("Spell List")
        self.SpellListLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SpellListLabel.setStyleSheet(self.SectionLabelStyle)
        self.SpellListLabel.setMargin(self.HeaderLabelMargin)

        # Spell List Tree Widget
        self.SpellListTreeWidget = SpellListTreeWidget(self.CharacterWindow)
        self.SpellListTreeWidget.itemActivated.connect(self.EditSpell)

        # Buttons
        self.AddSpellButton = AddButton(self.AddSpell, "Add Spell")
        self.AddSpellButton.setSizePolicy(self.InputsSizePolicy)
        self.DeleteSpellButton = DeleteButton(self.DeleteSpell, "Delete Spell")
        self.DeleteSpellButton.setSizePolicy(self.InputsSizePolicy)
        self.EditSpellButton = EditButton(self.EditSpell, "Edit Spell")
        self.EditSpellButton.setSizePolicy(self.InputsSizePolicy)
        self.MoveSpellUpButton = MoveUpButton(self.MoveSpellUp, "Move Spell Up")
        self.MoveSpellUpButton.setSizePolicy(self.InputsSizePolicy)
        self.MoveSpellDownButton = MoveDownButton(self.MoveSpellDown, "Move Spell Down")
        self.MoveSpellDownButton.setSizePolicy(self.InputsSizePolicy)

    def CreateAndSetLayout(self):
        # Create Layout
        self.Layout = QGridLayout()

        # Ability Score Derivatives
        self.SpellcastingAbilitiesLayout = QGridLayout()
        self.SpellcastingAbilitiesLayout.addWidget(self.SpellcastingAbilitiesLabel, 0, 0)
        self.SpellcastingAbilitiesLayout.addWidget(self.SpellcastingAbilityWidgetInst1, 1, 0)
        self.SpellcastingAbilitiesLayout.addWidget(self.SpellcastingAbilityWidgetInst2, 2, 0)
        self.SpellcastingAbilitiesLayout.addWidget(self.SpellcastingAbilityWidgetInst3, 3, 0)
        self.Layout.addLayout(self.SpellcastingAbilitiesLayout, 0, 0, 2, 1)

        # Spell Slots
        self.SpellSlotsLayout = QGridLayout()

        self.SpellSlotsLayout.addWidget(self.SpellSlotsLabel, 0, 0, 1, 3)
        self.SpellSlotsLayout.addWidget(self.SpellSlotsLevelLabel, 1, 0)
        self.SpellSlotsLayout.addWidget(self.SpellSlotsTotalSlotsLabel, 1, 1)
        self.SpellSlotsLayout.addWidget(self.SpellSlotsUsedSlotsLabel, 1, 2)

        self.SpellSlotsLayout.addWidget(self.SpellSlots1stLabel, 2, 0)
        self.SpellSlotsLayout.addWidget(self.SpellSlots2ndLabel, 3, 0)
        self.SpellSlotsLayout.addWidget(self.SpellSlots3rdLabel, 4, 0)
        self.SpellSlotsLayout.addWidget(self.SpellSlots4thLabel, 5, 0)
        self.SpellSlotsLayout.addWidget(self.SpellSlots5thLabel, 6, 0)
        self.SpellSlotsLayout.addWidget(self.SpellSlots6thLabel, 7, 0)
        self.SpellSlotsLayout.addWidget(self.SpellSlots7thLabel, 8, 0)
        self.SpellSlotsLayout.addWidget(self.SpellSlots8thLabel, 9, 0)
        self.SpellSlotsLayout.addWidget(self.SpellSlots9thLabel, 10, 0)

        self.SpellSlotsLayout.addWidget(self.SpellSlotsTotalSlots1stSpinBox, 2, 1)
        self.SpellSlotsLayout.addWidget(self.SpellSlotsUsedSlots1stSpinBox, 2, 2)
        self.SpellSlotsLayout.addWidget(self.SpellSlotsTotalSlots2ndSpinBox, 3, 1)
        self.SpellSlotsLayout.addWidget(self.SpellSlotsUsedSlots2ndSpinBox, 3, 2)
        self.SpellSlotsLayout.addWidget(self.SpellSlotsTotalSlots3rdSpinBox, 4, 1)
        self.SpellSlotsLayout.addWidget(self.SpellSlotsUsedSlots3rdSpinBox, 4, 2)
        self.SpellSlotsLayout.addWidget(self.SpellSlotsTotalSlots4thSpinBox, 5, 1)
        self.SpellSlotsLayout.addWidget(self.SpellSlotsUsedSlots4thSpinBox, 5, 2)
        self.SpellSlotsLayout.addWidget(self.SpellSlotsTotalSlots5thSpinBox, 6, 1)
        self.SpellSlotsLayout.addWidget(self.SpellSlotsUsedSlots5thSpinBox, 6, 2)
        self.SpellSlotsLayout.addWidget(self.SpellSlotsTotalSlots6thSpinBox, 7, 1)
        self.SpellSlotsLayout.addWidget(self.SpellSlotsUsedSlots6thSpinBox, 7, 2)
        self.SpellSlotsLayout.addWidget(self.SpellSlotsTotalSlots7thSpinBox, 8, 1)
        self.SpellSlotsLayout.addWidget(self.SpellSlotsUsedSlots7thSpinBox, 8, 2)
        self.SpellSlotsLayout.addWidget(self.SpellSlotsTotalSlots8thSpinBox, 9, 1)
        self.SpellSlotsLayout.addWidget(self.SpellSlotsUsedSlots8thSpinBox, 9, 2)
        self.SpellSlotsLayout.addWidget(self.SpellSlotsTotalSlots9thSpinBox, 10, 1)
        self.SpellSlotsLayout.addWidget(self.SpellSlotsUsedSlots9thSpinBox, 10, 2)

        self.Layout.addLayout(self.SpellSlotsLayout, 0, 1)

        self.SpellPointsLayout = QGridLayout()
        self.SpellPointsLayout.addWidget(self.SpellPointsLabel, 0, 0, 1, 4)
        self.SpellPointsLayout.addWidget(self.SpellPointsMaxLabel, 1, 0)
        self.SpellPointsLayout.addWidget(self.SpellPointsMaxSpinBox, 1, 1, 1, 2)
        self.SpellPointsLayout.addWidget(self.SpellPointsMaxEditButton, 1, 3)
        self.SpellPointsLayout.addWidget(self.SpellPointsRemainingLabel, 2, 0)
        self.SpellPointsLayout.addWidget(self.SpellPointsRemainingSpinBox, 2, 1)
        self.SpellPointsLayout.addWidget(self.SpellPointsSpendButton, 2, 2)
        self.SpellPointsLayout.addWidget(self.SpellPointsRestoreButton, 2, 3)
        self.Layout.addLayout(self.SpellPointsLayout, 1, 1)

        # Concentrating Button
        self.Layout.addWidget(self.ConcentratingButton, 2, 0, 1, 2)

        # Spell Notes
        self.SpellNotesLayout = QGridLayout()
        self.SpellNotesLayout.addWidget(self.SpellNotesLabel, 0, 0)
        self.SpellNotesLayout.addWidget(self.SpellNotesTextEdit, 1, 0)
        self.SpellNotesLayout.setRowStretch(1, 1)
        self.Layout.addLayout(self.SpellNotesLayout, 3, 0, 1, 2)

        # Spell List
        self.SpellListLayout = QGridLayout()
        self.SpellListLayout.addWidget(self.SpellListLabel, 0, 0, 1, 5)
        self.SpellListLayout.addWidget(self.AddSpellButton, 1, 0)
        self.SpellListLayout.addWidget(self.DeleteSpellButton, 1, 1)
        self.SpellListLayout.addWidget(self.EditSpellButton, 1, 2)
        self.SpellListLayout.addWidget(self.MoveSpellUpButton, 1, 3)
        self.SpellListLayout.addWidget(self.MoveSpellDownButton, 1, 4)
        self.SpellListLayout.addWidget(self.SpellListTreeWidget, 2, 0, 1, 5)
        self.SpellListLayout.setRowStretch(2, 1)
        self.Layout.addLayout(self.SpellListLayout, 0, 2, 4, 1)

        # Layout Stretching
        self.Layout.setRowStretch(3, 1)
        self.Layout.setColumnStretch(2, 1)

        # Set Layout
        self.setLayout(self.Layout)

    def SetSpellPointsEnabled(self, Enabled):
        for Widget in [self.SpellPointsLabel, self.SpellPointsMaxLabel, self.SpellPointsMaxSpinBox, self.SpellPointsMaxEditButton, self.SpellPointsRemainingLabel, self.SpellPointsRemainingSpinBox, self.SpellPointsSpendButton, self.SpellPointsRestoreButton]:
            Widget.setEnabled(Enabled)
        if not Enabled:
            self.SpellPointsRemainingSpinBox.setValue(0)

    def EditBonusSpellPointsStatModifier(self):
        self.CharacterWindow.EditStatModifier(self, self.CharacterWindow.PlayerCharacter.Stats["Bonus Spell Points Stat Modifier"], "Bonus Spell Points Stat Modifier")

    def SpendSpellPoints(self):
        SpendSpellPointsDialogInst = SpendOrRestoreSpellPointsDialog(self.CharacterWindow)
        if SpendSpellPointsDialogInst.Submitted:
            self.CharacterWindow.PlayerCharacter.ExpendSpellPoints(SpendSpellPointsDialogInst.SpellSlotLevel, SpendSpellPointsDialogInst.SpellSlotAmount, SpendSpellPointsDialogInst.ManualAmount)
            self.CharacterWindow.UpdatingFieldsFromPlayerCharacter = True
            self.CharacterWindow.UpdateUnsavedChangesFlag(True)
            self.CharacterWindow.UpdatingFieldsFromPlayerCharacter = False

    def RestoreSpellPoints(self):
        RestoreSpellPointsDialogInst = SpendOrRestoreSpellPointsDialog(self.CharacterWindow, RestoreMode=True)
        if RestoreSpellPointsDialogInst.Submitted:
            self.CharacterWindow.PlayerCharacter.RestoreSpellPoints(RestoreSpellPointsDialogInst.SpellSlotLevel, RestoreSpellPointsDialogInst.SpellSlotAmount, RestoreSpellPointsDialogInst.ManualAmount)
            self.CharacterWindow.UpdatingFieldsFromPlayerCharacter = True
            self.CharacterWindow.UpdateUnsavedChangesFlag(True)
            self.CharacterWindow.UpdatingFieldsFromPlayerCharacter = False

    def AddSpell(self):
        SpellIndex = self.CharacterWindow.PlayerCharacter.AddSpell()
        self.CharacterWindow.UpdateDisplay()
        EditSpellDialogInst = EditSpellDialog(self.CharacterWindow, self.CharacterWindow.PlayerCharacter.Stats["Spell List"], SpellIndex, AddMode=True)
        if EditSpellDialogInst.Cancelled:
            self.CharacterWindow.PlayerCharacter.DeleteLastSpell()
            self.CharacterWindow.UpdateDisplay()
        else:
            self.CharacterWindow.UpdateUnsavedChangesFlag(True)
            self.SpellListTreeWidget.SelectIndex(SpellIndex)

    def DeleteSpell(self):
        CurrentSelection = self.SpellListTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            if self.CharacterWindow.DisplayMessageBox("Are you sure you want to delete this spell?  This cannot be undone.", Icon=QMessageBox.Icon.Warning, Buttons=(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)) == QMessageBox.StandardButton.Yes:
                CurrentSpell = CurrentSelection[0]
                CurrentSpellIndex = CurrentSpell.Index
                self.CharacterWindow.PlayerCharacter.DeleteSpell(CurrentSpellIndex)
                self.CharacterWindow.UpdateUnsavedChangesFlag(True)
                SpellListLength = len(self.CharacterWindow.PlayerCharacter.Stats["Spell List"])
                if SpellListLength > 0:
                    self.SpellListTreeWidget.SelectIndex(CurrentSpellIndex if CurrentSpellIndex < SpellListLength else SpellListLength - 1)

    def EditSpell(self):
        CurrentSelection = self.SpellListTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentSpell = CurrentSelection[0]
            CurrentSpellIndex = CurrentSpell.Index
            EditSpellDialogInst = EditSpellDialog(self.CharacterWindow, self.CharacterWindow.PlayerCharacter.Stats["Spell List"], CurrentSpellIndex)
            if EditSpellDialogInst.UnsavedChanges:
                self.CharacterWindow.UpdateUnsavedChangesFlag(True)
                self.SpellListTreeWidget.SelectIndex(CurrentSpellIndex)

    def MoveSpellUp(self):
        self.MoveSpell(-1)

    def MoveSpellDown(self):
        self.MoveSpell(1)

    def MoveSpell(self, Delta):
        CurrentSelection = self.SpellListTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentSpell = CurrentSelection[0]
            CurrentSpellIndex = CurrentSpell.Index
            if self.CharacterWindow.PlayerCharacter.MoveSpell(CurrentSpellIndex, Delta):
                self.CharacterWindow.UpdateUnsavedChangesFlag(True)
                self.SpellListTreeWidget.SelectIndex(CurrentSpellIndex + Delta)
