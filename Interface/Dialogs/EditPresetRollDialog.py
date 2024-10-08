import copy

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QGridLayout, QPushButton, QSpinBox, QSizePolicy, QMessageBox

from Interface.Dialogs.EditModifierDialog import EditModifierDialog
from Interface.Dialogs.EditResultMessageDialog import EditResultMessageDialog
from Interface.Widgets.DieTypeSpinBox import DieTypeSpinBox
from Interface.Widgets.IconButtons import AddButton, CopyButton, DeleteButton, EditButton, MoveDownButton, MoveUpButton
from Interface.Widgets.ResultMessagesTreeWidget import ResultMessagesTreeWidget


class EditPresetRollDialog(QDialog):
    def __init__(self, CharacterWindow, DiceRoller, PresetRollIndex, AddMode=False):
        super().__init__(parent=CharacterWindow)

        # Store Parameters
        self.CharacterWindow = CharacterWindow
        self.DiceRoller = DiceRoller
        self.PresetRollIndex = PresetRollIndex

        # Variables
        self.PresetRoll = self.DiceRoller.PresetRolls[self.PresetRollIndex]
        self.PresetRollOriginalState = copy.deepcopy(self.PresetRoll)
        self.UnsavedChanges = False
        self.Cancelled = False

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Labels
        self.PromptLabel = QLabel("Add this preset roll:" if AddMode else "Edit this preset roll:")
        self.PromptLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.NameLabel = QLabel("Name:")
        self.DieTypeLabel = QLabel("d")
        self.ModifierLabel = QLabel("+")
        self.ResultMessagesLabel = QLabel("Result Messages:")
        self.ResultMessagesLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Roll Inputs
        self.NameLineEdit = QLineEdit()
        self.NameLineEdit.setText(self.PresetRoll["Name"])
        self.NameLineEdit.textChanged.connect(self.UpdatePresetRoll)

        self.DiceNumberSpinBox = QSpinBox()
        self.DiceNumberSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.DiceNumberSpinBox.setButtonSymbols(self.DiceNumberSpinBox.NoButtons)
        self.DiceNumberSpinBox.setRange(1, 1000000000)
        self.DiceNumberSpinBox.setValue(self.PresetRoll["Dice Number"])
        self.DiceNumberSpinBox.valueChanged.connect(self.UpdatePresetRoll)

        self.DieTypeSpinBox = DieTypeSpinBox()
        self.DieTypeSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.DieTypeSpinBox.setButtonSymbols(self.DieTypeSpinBox.NoButtons)
        self.DieTypeSpinBox.setRange(1, 1000000000)
        self.DieTypeSpinBox.setValue(self.PresetRoll["Die Type"])
        self.DieTypeSpinBox.valueChanged.connect(self.UpdatePresetRoll)

        self.ModifierButton = QPushButton("Modifier")
        self.ModifierButton.clicked.connect(self.EditModifier)

        # Result Messages Tree Widget
        self.ResultMessagesTreeWidget = ResultMessagesTreeWidget(self)

        # Buttons
        self.AddResultMessageButton = AddButton(self.AddResultMessage, "Add Result Message")
        self.AddResultMessageButton.setSizePolicy(self.InputsSizePolicy)
        self.DeleteResultMessageButton = DeleteButton(self.DeleteResultMessage, "Delete Result Message")
        self.DeleteResultMessageButton.setSizePolicy(self.InputsSizePolicy)
        self.EditResultMessageButton = EditButton(self.EditResultMessage, "Edit Result Message")
        self.EditResultMessageButton.setSizePolicy((self.InputsSizePolicy))
        self.CopyResultMessageButton = CopyButton(self.CopyResultMessage, "Copy Result Message")
        self.CopyResultMessageButton.setSizePolicy((self.InputsSizePolicy))
        self.ResultMessageMoveUpButton = MoveUpButton(self.MoveResultMessageUp, "Move Result Message Up")
        self.ResultMessageMoveUpButton.setSizePolicy(self.InputsSizePolicy)
        self.ResultMessageMoveDownButton = MoveDownButton(self.MoveResultMessageDown, "Move Result Message Down")
        self.ResultMessageMoveDownButton.setSizePolicy(self.InputsSizePolicy)
        self.DoneButton = QPushButton("Done")
        self.DoneButton.clicked.connect(self.Done)
        self.DoneButton.setDefault(True)
        self.DoneButton.setAutoDefault(True)
        self.CancelButton = QPushButton("Cancel")
        self.CancelButton.clicked.connect(self.Cancel)

        # Layout
        self.Layout = QGridLayout()
        self.Layout.addWidget(self.PromptLabel, 0, 0, 1, 2)
        self.NameLayout = QGridLayout()
        self.NameLayout.addWidget(self.NameLabel, 0, 0)
        self.NameLayout.addWidget(self.NameLineEdit, 0, 1)
        self.NameLayout.setColumnStretch(1, 1)
        self.Layout.addLayout(self.NameLayout, 1, 0, 1, 2)
        self.DiceInputsLayout = QGridLayout()
        self.DiceInputsLayout.addWidget(self.DiceNumberSpinBox, 0, 0)
        self.DiceInputsLayout.addWidget(self.DieTypeLabel, 0, 1)
        self.DiceInputsLayout.addWidget(self.DieTypeSpinBox, 0, 2)
        self.DiceInputsLayout.addWidget(self.ModifierLabel, 0, 3)
        self.DiceInputsLayout.addWidget(self.ModifierButton, 0, 4)
        self.DiceInputsLayout.setColumnStretch(0, 1)
        self.DiceInputsLayout.setColumnStretch(2, 1)
        self.DiceInputsLayout.setColumnStretch(4, 1)
        self.Layout.addLayout(self.DiceInputsLayout, 2, 0, 1, 2)
        self.ResultMessagesLayout = QGridLayout()
        self.ResultMessagesLayout.addWidget(self.ResultMessagesLabel, 0, 0, 1, 6)
        self.ResultMessagesLayout.addWidget(self.AddResultMessageButton, 1, 0)
        self.ResultMessagesLayout.addWidget(self.DeleteResultMessageButton, 1, 1)
        self.ResultMessagesLayout.addWidget(self.EditResultMessageButton, 1, 2)
        self.ResultMessagesLayout.addWidget(self.CopyResultMessageButton, 1, 3)
        self.ResultMessagesLayout.addWidget(self.ResultMessageMoveUpButton, 1, 4)
        self.ResultMessagesLayout.addWidget(self.ResultMessageMoveDownButton, 1, 5)
        self.ResultMessagesLayout.addWidget(self.ResultMessagesTreeWidget, 2, 0, 1, 6)
        self.ResultMessagesLayout.setRowStretch(2, 1)
        self.Layout.addLayout(self.ResultMessagesLayout, 3, 0, 1, 2)
        self.Layout.addWidget(self.DoneButton, 4, 0)
        self.Layout.addWidget(self.CancelButton, 4, 1)
        self.setLayout(self.Layout)

        # Set Window Title and Icon
        self.setWindowTitle(self.CharacterWindow.ScriptName)
        self.setWindowIcon(self.CharacterWindow.WindowIcon)

        # Update Display
        self.UpdateDisplay()

        # Select Text in Name Line Edit
        self.NameLineEdit.selectAll()

        # Execute Dialog
        self.exec_()

    def EditModifier(self):
        StatModifierDescription = f"modifier for {self.NameLineEdit.text()}" if self.NameLineEdit.text() != "" else "modifier"
        EditModifierDialogInst = EditModifierDialog(self, self.CharacterWindow, self.PresetRoll["Modifier"], StatModifierDescription)
        self.UnsavedChanges = EditModifierDialogInst.UnsavedChanges

    def AddResultMessage(self):
        ResultMessageIndex = self.DiceRoller.AddResultMessage(self.PresetRollIndex)
        self.UpdateDisplay()
        EditResultMessageDialogInst = EditResultMessageDialog(self, ResultMessageIndex, AddMode=True)
        if EditResultMessageDialogInst.Cancelled:
            self.DiceRoller.DeleteLastResultMessage(self.PresetRollIndex)
            self.UpdateDisplay()
        else:
            self.UnsavedChanges = True
            self.UpdateDisplay()
            self.ResultMessagesTreeWidget.SelectIndex(ResultMessageIndex)

    def DeleteResultMessage(self):
        CurrentSelection = self.ResultMessagesTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            if self.CharacterWindow.DisplayMessageBox("Are you sure you want to delete this result message?  This cannot be undone.", Icon=QMessageBox.Warning, Buttons=(QMessageBox.Yes | QMessageBox.No)) == QMessageBox.Yes:
                CurrentResultMessage = CurrentSelection[0]
                CurrentResultMessageIndex = CurrentResultMessage.Index
                self.DiceRoller.DeleteResultMessage(self.PresetRollIndex, CurrentResultMessageIndex)
                self.UnsavedChanges = True
                self.UpdateDisplay()
                ResultMessagesLength = len(self.PresetRoll["Result Messages"])
                if ResultMessagesLength > 0:
                    self.ResultMessagesTreeWidget.SelectIndex(CurrentResultMessageIndex if CurrentResultMessageIndex < ResultMessagesLength else ResultMessagesLength - 1)

    def EditResultMessage(self):
        CurrentSelection = self.ResultMessagesTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentResultMessage = CurrentSelection[0]
            CurrentResultMessageIndex = CurrentResultMessage.Index
            EditResultMessageDialogInst = EditResultMessageDialog(self, CurrentResultMessageIndex)
            if EditResultMessageDialogInst.UnsavedChanges:
                self.UnsavedChanges = True
                self.UpdateDisplay()
                self.ResultMessagesTreeWidget.SelectIndex(CurrentResultMessageIndex)

    def CopyResultMessage(self):
        CurrentSelection = self.ResultMessagesTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentResultMessage = CurrentSelection[0]
            CurrentResultMessageIndex = CurrentResultMessage.Index
            NewResultMessageIndex = self.DiceRoller.CopyResultMessage(self.PresetRollIndex, CurrentResultMessageIndex)
            self.UnsavedChanges = True
            self.UpdateDisplay()
            self.ResultMessagesTreeWidget.SelectIndex(NewResultMessageIndex)

    def MoveResultMessageUp(self):
        self.MoveResultMessage(-1)

    def MoveResultMessageDown(self):
        self.MoveResultMessage(1)

    def MoveResultMessage(self, Delta):
        CurrentSelection = self.ResultMessagesTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentResultMessage = CurrentSelection[0]
            CurrentResultMessageIndex = CurrentResultMessage.Index
            if self.DiceRoller.MoveResultMessage(self.PresetRollIndex, CurrentResultMessageIndex, Delta):
                self.UnsavedChanges = True
                self.UpdateDisplay()
                self.ResultMessagesTreeWidget.SelectIndex(CurrentResultMessageIndex + Delta)

    def UpdatePresetRoll(self):
        if not self.ValidInput():
            return
        self.PresetRoll["Name"] = self.NameLineEdit.text()
        self.PresetRoll["Dice Number"] = self.DiceNumberSpinBox.value()
        self.PresetRoll["Die Type"] = self.DieTypeSpinBox.value()
        self.UnsavedChanges = True

    def Done(self):
        if self.ValidInput(Alert=True):
            self.close()

    def Cancel(self):
        self.PresetRoll.update(self.PresetRollOriginalState)
        self.UnsavedChanges = False
        self.Cancelled = True
        self.close()

    def ValidInput(self, Alert=False):
        if self.NameLineEdit.text() == "":
            if Alert:
                self.CharacterWindow.DisplayMessageBox("Preset rolls must have a name.", Icon=QMessageBox.Warning, Parent=self)
            return False
        return True

    def UpdateDisplay(self):
        self.ResultMessagesTreeWidget.FillFromResultMessages()
