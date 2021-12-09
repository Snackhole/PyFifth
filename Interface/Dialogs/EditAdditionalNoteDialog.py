import copy

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QLabel, QMessageBox, QPushButton, QGridLayout, QTextEdit

from Interface.Widgets.CenteredLineEdit import CenteredLineEdit


class EditAdditionalNoteDialog(QDialog):
    def __init__(self, CharacterWindow, AdditionalNotes, AdditionalNoteIndex, AddMode=False):
        super().__init__(parent=CharacterWindow)

        # Store Parameters
        self.CharacterWindow = CharacterWindow
        self.AdditionalNotes = AdditionalNotes
        self.AdditionalNoteIndex = AdditionalNoteIndex

        # Variables
        self.AdditionalNote = self.AdditionalNotes[self.AdditionalNoteIndex]
        self.AdditionalNoteOriginalState = copy.deepcopy(self.AdditionalNote)
        self.UnsavedChanges = False
        self.Cancelled = False

        # Labels
        self.PromptLabel = QLabel("Add this note:" if AddMode else "Edit this note:")
        self.PromptLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Note Inputs
        self.NoteNameLineEdit = CenteredLineEdit()
        self.NoteNameLineEdit.setPlaceholderText("Note Name")
        self.NoteNameLineEdit.setText(self.AdditionalNote["Note Name"])
        self.NoteNameLineEdit.textChanged.connect(self.UpdateNote)
        self.NoteTextTextEdit = QTextEdit()
        self.NoteTextTextEdit.setPlaceholderText("Note Text")
        self.NoteTextTextEdit.setTabChangesFocus(True)
        self.NoteTextTextEdit.setPlainText(self.AdditionalNote["Note Text"])
        self.NoteTextTextEdit.textChanged.connect(self.UpdateNote)

        # Buttons
        self.DoneButton = QPushButton("Done")
        self.DoneButton.clicked.connect(self.Done)
        self.CancelButton = QPushButton("Cancel")
        self.CancelButton.clicked.connect(self.Cancel)

        # Layout
        self.Layout = QGridLayout()
        self.Layout.addWidget(self.PromptLabel, 0, 0, 1, 2)
        self.Layout.addWidget(self.NoteNameLineEdit, 1, 0, 1, 2)
        self.Layout.addWidget(self.NoteTextTextEdit, 2, 0, 1, 2)
        self.Layout.addWidget(self.DoneButton, 3, 0)
        self.Layout.addWidget(self.CancelButton, 3, 1)
        self.setLayout(self.Layout)

        # Set Window Title and Icon
        self.setWindowTitle(self.CharacterWindow.ScriptName)
        self.setWindowIcon(self.CharacterWindow.WindowIcon)

        # Select Text in Name Line Edit
        self.NoteNameLineEdit.selectAll()

        # Execute Dialog
        self.exec_()

    def UpdateNote(self):
        if not self.ValidInput():
            return
        self.AdditionalNote["Note Name"] = self.NoteNameLineEdit.text()
        self.AdditionalNote["Note Text"] = self.NoteTextTextEdit.toPlainText()
        self.UnsavedChanges = True

    def Done(self):
        if self.ValidInput(Alert=True):
            self.close()

    def Cancel(self):
        self.AdditionalNote.update(self.AdditionalNoteOriginalState)
        self.UnsavedChanges = False
        self.Cancelled = True
        self.close()

    def ValidInput(self, Alert=False):
        if self.NoteNameLineEdit.text() == "":
            if Alert:
                self.CharacterWindow.DisplayMessageBox("Notes must have a name.", Icon=QMessageBox.Warning, Parent=self)
            return False
        return True
