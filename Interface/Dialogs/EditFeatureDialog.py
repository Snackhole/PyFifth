import copy

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QMessageBox, QPushButton, QGridLayout, QTextEdit


class EditFeatureDialog(QDialog):
    def __init__(self, CharacterWindow, Features, FeatureIndex, AddMode=False):
        super().__init__(parent=CharacterWindow)

        # Store Parameters
        self.CharacterWindow = CharacterWindow
        self.Features = Features
        self.FeatureIndex = FeatureIndex

        # Variables
        self.Feature = self.Features[self.FeatureIndex]
        self.FeatureOriginalState = copy.deepcopy(self.Feature)
        self.UnsavedChanges = False
        self.Cancelled = False

        # Labels
        self.PromptLabel = QLabel("Add this feature:" if AddMode else "Edit this feature:")
        self.PromptLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Feature Inputs
        self.NameLineEdit = QLineEdit()
        self.NameLineEdit.setPlaceholderText("Feature Name")
        self.NameLineEdit.setText(self.Feature["Feature Name"])
        self.NameLineEdit.textChanged.connect(self.UpdateFeature)
        self.DescriptionTextEdit = QTextEdit()
        self.DescriptionTextEdit.setPlaceholderText("Feature Text")
        self.DescriptionTextEdit.setTabChangesFocus(True)
        self.DescriptionTextEdit.setPlainText(self.Feature["Feature Text"])
        self.DescriptionTextEdit.textChanged.connect(self.UpdateFeature)

        # Buttons
        self.DoneButton = QPushButton("Done")
        self.DoneButton.clicked.connect(self.Done)
        self.DoneButton.setDefault(True)
        self.DoneButton.setAutoDefault(True)
        self.CancelButton = QPushButton("Cancel")
        self.CancelButton.clicked.connect(self.Cancel)

        # Layout
        self.Layout = QGridLayout()
        self.Layout.addWidget(self.PromptLabel, 0, 0, 1, 2)
        self.Layout.addWidget(self.NameLineEdit, 1, 0, 1, 2)
        self.Layout.addWidget(self.DescriptionTextEdit, 2, 0, 1, 2)
        self.Layout.addWidget(self.DoneButton, 3, 0)
        self.Layout.addWidget(self.CancelButton, 3, 1)
        self.setLayout(self.Layout)

        # Set Window Title and Icon
        self.setWindowTitle(self.CharacterWindow.ScriptName)
        self.setWindowIcon(self.CharacterWindow.WindowIcon)

        # Select Text in Name Line Edit
        self.NameLineEdit.selectAll()

        # Execute Dialog
        self.exec_()

    def UpdateFeature(self):
        if not self.ValidInput():
            return
        self.Feature["Feature Name"] = self.NameLineEdit.text()
        self.Feature["Feature Text"] = self.DescriptionTextEdit.toPlainText()
        self.UnsavedChanges = True

    def Done(self):
        if self.ValidInput(Alert=True):
            self.close()

    def Cancel(self):
        self.Feature.update(self.FeatureOriginalState)
        self.UnsavedChanges = False
        self.Cancelled = True
        self.close()

    def ValidInput(self, Alert=False):
        if self.NameLineEdit.text() == "":
            if Alert:
                self.CharacterWindow.DisplayMessageBox("Features must have a name.", Icon=QMessageBox.Warning, Parent=self)
            return False
        return True
