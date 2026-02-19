from PyQt6 import QtCore
from PyQt6.QtWidgets import QFrame, QGridLayout, QLabel, QSizePolicy, QMessageBox
from Interface.Dialogs.EditAdditionalNoteDialog import EditAdditionalNoteDialog

from Interface.Widgets.AdditionalNotesTreeWidget import AdditionalNotesTreeWidget
from Interface.Widgets.IconButtons import AddButton, DeleteButton, EditButton, MoveDownButton, MoveUpButton
from Interface.Widgets.IndentingTextEdit import IndentingTextEdit


class PlayerCharacterNotesWidget(QFrame):
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

        # Create Notes
        self.CreateNotes()

        # Create Additional Notes
        self.CreateAdditionalNotes()

        # Create and Set Layout
        self.CreateAndSetLayout()

    def CreateNotes(self):
        self.NotesTextEdit1 = IndentingTextEdit(TextChangedSlot=lambda: self.CharacterWindow.UpdateStat("Notes 1", self.NotesTextEdit1.toPlainText()))
        self.NotesTextEdit1.setTabChangesFocus(True)
        self.NotesTextEdit2 = IndentingTextEdit(TextChangedSlot=lambda: self.CharacterWindow.UpdateStat("Notes 2", self.NotesTextEdit2.toPlainText()))
        self.NotesTextEdit2.setTabChangesFocus(True)

    def CreateAdditionalNotes(self):
        # Additional Notes Label
        self.AdditionalNotesLabel = QLabel("Additional Notes")
        self.AdditionalNotesLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.AdditionalNotesLabel.setStyleSheet(self.SectionLabelStyle)
        self.AdditionalNotesLabel.setMargin(self.HeaderLabelMargin)

        # Additional Notes Tree Widget
        self.AdditionalNotesTreeWidget = AdditionalNotesTreeWidget(self.CharacterWindow)
        self.AdditionalNotesTreeWidget.itemActivated.connect(self.EditAdditionalNote)

        # Buttons
        self.AddAdditionalNoteButton = AddButton(self.AddAdditionalNote, "Add Additional Note")
        self.AddAdditionalNoteButton.setSizePolicy(self.InputsSizePolicy)
        self.DeleteAdditionalNoteButton = DeleteButton(self.DeleteAdditionalNote, "Delete Additional Note")
        self.DeleteAdditionalNoteButton.setSizePolicy(self.InputsSizePolicy)
        self.EditAdditionalNoteButton = EditButton(self.EditAdditionalNote, "Edit Additional Note")
        self.EditAdditionalNoteButton.setSizePolicy(self.InputsSizePolicy)
        self.MoveAdditionalNoteUpButton = MoveUpButton(self.MoveAdditionalNoteUp, "Move Additional Note Up")
        self.MoveAdditionalNoteUpButton.setSizePolicy(self.InputsSizePolicy)
        self.MoveAdditionalNoteDownButton = MoveDownButton(self.MoveAdditionalNoteDown, "Move Additional Note Down")
        self.MoveAdditionalNoteDownButton.setSizePolicy(self.InputsSizePolicy)

    def CreateAndSetLayout(self):
        # Create Layout
        self.Layout = QGridLayout()

        # Notes
        self.Layout.addWidget(self.NotesTextEdit1, 0, 0)
        self.Layout.addWidget(self.NotesTextEdit2, 0, 1)

        # Additional Notes
        self.AdditionalNotesLayout = QGridLayout()
        self.AdditionalNotesLayout.addWidget(self.AdditionalNotesLabel, 0, 0, 1, 5)
        self.AdditionalNotesLayout.addWidget(self.AddAdditionalNoteButton, 1, 0)
        self.AdditionalNotesLayout.addWidget(self.DeleteAdditionalNoteButton, 1, 1)
        self.AdditionalNotesLayout.addWidget(self.EditAdditionalNoteButton, 1, 2)
        self.AdditionalNotesLayout.addWidget(self.MoveAdditionalNoteUpButton, 1, 3)
        self.AdditionalNotesLayout.addWidget(self.MoveAdditionalNoteDownButton, 1, 4)
        self.AdditionalNotesLayout.addWidget(self.AdditionalNotesTreeWidget, 2, 0, 1, 5)
        self.AdditionalNotesLayout.setRowStretch(2, 1)
        self.Layout.addLayout(self.AdditionalNotesLayout, 0, 2)

        # Layout Stretching
        for Column in range(2):
            self.Layout.setColumnStretch(Column, 1)

        # Set Layout
        self.setLayout(self.Layout)

    def AddAdditionalNote(self):
        NoteIndex = self.CharacterWindow.PlayerCharacter.AddAdditionalNote()
        self.CharacterWindow.UpdateDisplay()
        EditAdditionalNoteDialogInst = EditAdditionalNoteDialog(self.CharacterWindow, self.CharacterWindow.PlayerCharacter.Stats["Additional Notes"], NoteIndex, AddMode=True)
        if EditAdditionalNoteDialogInst.Cancelled:
            self.CharacterWindow.PlayerCharacter.DeleteLastAdditionalNote()
            self.CharacterWindow.UpdateDisplay()
        else:
            self.CharacterWindow.UpdateUnsavedChangesFlag(True)
            self.AdditionalNotesTreeWidget.SelectIndex(NoteIndex)

    def DeleteAdditionalNote(self):
        CurrentSelection = self.AdditionalNotesTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            if self.CharacterWindow.DisplayMessageBox("Are you sure you want to delete this note?  This cannot be undone.", Icon=QMessageBox.Icon.Warning, Buttons=(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)) == QMessageBox.StandardButton.Yes:
                CurrentNote = CurrentSelection[0]
                CurrentNoteIndex = CurrentNote.Index
                self.CharacterWindow.PlayerCharacter.DeleteAdditionalNote(CurrentNoteIndex)
                self.CharacterWindow.UpdateUnsavedChangesFlag(True)
                AdditionalNotesLength = len(self.CharacterWindow.PlayerCharacter.Stats["Additional Notes"])
                if AdditionalNotesLength > 0:
                    self.AdditionalNotesTreeWidget.SelectIndex(CurrentNoteIndex if CurrentNoteIndex < AdditionalNotesLength else AdditionalNotesLength - 1)

    def EditAdditionalNote(self):
        CurrentSelection = self.AdditionalNotesTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentNote = CurrentSelection[0]
            CurrentNoteIndex = CurrentNote.Index
            EditAdditionalNoteDialogInst = EditAdditionalNoteDialog(self.CharacterWindow, self.CharacterWindow.PlayerCharacter.Stats["Additional Notes"], CurrentNoteIndex)
            if EditAdditionalNoteDialogInst.UnsavedChanges:
                self.CharacterWindow.UpdateUnsavedChangesFlag(True)
                self.AdditionalNotesTreeWidget.SelectIndex(CurrentNoteIndex)

    def MoveAdditionalNoteUp(self):
        self.MoveAdditionalNote(-1)

    def MoveAdditionalNoteDown(self):
        self.MoveAdditionalNote(1)

    def MoveAdditionalNote(self, Delta):
        CurrentSelection = self.AdditionalNotesTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentNote = CurrentSelection[0]
            CurrentNoteIndex = CurrentNote.Index
            if self.CharacterWindow.PlayerCharacter.MoveAdditionalNote(CurrentNoteIndex, Delta):
                self.CharacterWindow.UpdateUnsavedChangesFlag(True)
                self.AdditionalNotesTreeWidget.SelectIndex(CurrentNoteIndex + Delta)
