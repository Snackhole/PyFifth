import copy

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QMessageBox, QPushButton, QSpinBox

from Interface.Widgets.CenteredLineEdit import CenteredLineEdit
from Interface.Widgets.ToggleButtons import AliveButton, TurnTakenButton


class EditInitiativeEntryDialog(QDialog):
    def __init__(self, EncounterWindow, InitiativeOrder, EntryIndex, AddMode=False):
        super().__init__(parent=EncounterWindow)

        # Store Parameters
        self.EncounterWindow = EncounterWindow
        self.InitiativeOrder = InitiativeOrder
        self.EntryIndex = EntryIndex

        # Variables
        self.Entry = self.InitiativeOrder[self.EntryIndex]
        self.EntryOriginalState = copy.deepcopy(self.Entry)
        self.UnsavedChanges = False
        self.Cancelled = False

        # Labels
        self.PromptLabel = QLabel("Add this initiative entry:" if AddMode else "Edit this initiative entry:")
        self.PromptLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.CreatureNameLabel = QLabel("Creature Name:")
        self.InitiativeLabel = QLabel("Initiative:")
        self.TiePriorityLabel = QLabel("Tie Priority:")
        self.ConditionsLabel = QLabel("Conditions:")
        self.LocationLabel = QLabel("Location:")
        self.NotesLabel = QLabel("Notes:")

        # Entry Inputs
        self.CreatureNameLineEdit = CenteredLineEdit()
        self.CreatureNameLineEdit.setText(self.Entry["Creature Name"])
        self.CreatureNameLineEdit.textChanged.connect(self.UpdateEntry)

        self.InitiativeSpinBox = QSpinBox()
        self.InitiativeSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.InitiativeSpinBox.setButtonSymbols(self.InitiativeSpinBox.NoButtons)
        self.InitiativeSpinBox.setRange(-1000000000, 1000000000)
        self.InitiativeSpinBox.setValue(self.Entry["Initiative"])
        self.InitiativeSpinBox.valueChanged.connect(self.UpdateEntry)

        self.TiePrioritySpinBox = QSpinBox()
        self.TiePrioritySpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.TiePrioritySpinBox.setButtonSymbols(self.TiePrioritySpinBox.NoButtons)
        self.TiePrioritySpinBox.setRange(1, 1000000000)
        self.TiePrioritySpinBox.setValue(self.Entry["Tie Priority"])
        self.TiePrioritySpinBox.valueChanged.connect(self.UpdateEntry)

        self.ConditionsLineEdit = CenteredLineEdit()
        self.ConditionsLineEdit.setText(self.Entry["Conditions"])
        self.ConditionsLineEdit.textChanged.connect(self.UpdateEntry)

        self.LocationLineEdit = CenteredLineEdit()
        self.LocationLineEdit.setText(self.Entry["Location"])
        self.LocationLineEdit.textChanged.connect(self.UpdateEntry)

        self.NotesLineEdit = CenteredLineEdit()
        self.NotesLineEdit.setText(self.Entry["Notes"])
        self.NotesLineEdit.textChanged.connect(self.UpdateEntry)

        self.TurnTakenButton = TurnTakenButton(self.UpdateEntry)
        self.TurnTakenButton.setChecked(self.Entry["Turn Taken"])

        self.AliveButton = AliveButton(self.UpdateEntry)
        self.AliveButton.setChecked(self.Entry["Alive"])

        # Dialog Buttons
        self.DoneButton = QPushButton("Done")
        self.DoneButton.clicked.connect(self.Done)
        self.DoneButton.setDefault(True)
        self.DoneButton.setAutoDefault(True)
        self.CancelButton = QPushButton("Cancel")
        self.CancelButton.clicked.connect(self.Cancel)

        # Layout
        self.Layout = QGridLayout()
        self.Layout.addWidget(self.PromptLabel, 0, 0, 1, 2)
        self.Layout.addWidget(self.CreatureNameLabel, 1, 0)
        self.Layout.addWidget(self.CreatureNameLineEdit, 1, 1)
        self.Layout.addWidget(self.InitiativeLabel, 2, 0)
        self.Layout.addWidget(self.InitiativeSpinBox, 2, 1)
        self.Layout.addWidget(self.TiePriorityLabel, 3, 0)
        self.Layout.addWidget(self.TiePrioritySpinBox, 3, 1)
        self.Layout.addWidget(self.ConditionsLabel, 4, 0)
        self.Layout.addWidget(self.ConditionsLineEdit, 4, 1)
        self.Layout.addWidget(self.LocationLabel, 5, 0)
        self.Layout.addWidget(self.LocationLineEdit, 5, 1)
        self.Layout.addWidget(self.NotesLabel, 6, 0)
        self.Layout.addWidget(self.NotesLineEdit, 6, 1)
        self.ToggleButtonsLayout = QGridLayout()
        self.ToggleButtonsLayout.addWidget(self.TurnTakenButton, 0, 0)
        self.ToggleButtonsLayout.addWidget(self.AliveButton, 0, 1)
        self.Layout.addLayout(self.ToggleButtonsLayout, 7, 0, 1, 2)
        self.DialogButtonsLayout = QGridLayout()
        self.DialogButtonsLayout.addWidget(self.DoneButton, 0, 0)
        self.DialogButtonsLayout.addWidget(self.CancelButton, 0, 1)
        self.Layout.addLayout(self.DialogButtonsLayout, 8, 0, 1, 2)
        self.setLayout(self.Layout)

        # Set Window Title and Icon
        self.setWindowTitle(self.EncounterWindow.ScriptName)
        self.setWindowIcon(self.EncounterWindow.WindowIcon)

        # Select Text in Name Line Edit
        self.CreatureNameLineEdit.selectAll()

        # Execute Dialog
        self.exec_()

    def UpdateEntry(self):
        if not self.ValidInput():
            return
        self.Entry["Creature Name"] = self.CreatureNameLineEdit.text()
        self.Entry["Initiative"] = self.InitiativeSpinBox.value()
        self.Entry["Tie Priority"] = self.TiePrioritySpinBox.value()
        self.Entry["Conditions"] = self.ConditionsLineEdit.text()
        self.Entry["Location"] = self.LocationLineEdit.text()
        self.Entry["Notes"] = self.NotesLineEdit.text()
        self.Entry["Turn Taken"] = self.TurnTakenButton.isChecked()
        self.Entry["Alive"] = self.AliveButton.isChecked()
        self.UnsavedChanges = True

    def Done(self):
        if self.ValidInput(Alert=True):
            self.close()

    def Cancel(self):
        self.Entry.update(self.EntryOriginalState)
        self.UnsavedChanges = False
        self.Cancelled = True
        self.close()

    def ValidInput(self, Alert=False):
        if self.CreatureNameLineEdit.text() == "":
            if Alert:
                self.EncounterWindow.DisplayMessageBox("Initiative entries must have a creature name.", Icon=QMessageBox.Warning, Parent=self)
            return False
        return True
