import copy

from PyQt6 import QtCore
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QMessageBox, QPushButton, QGridLayout

from Interface.Widgets.IndentingTextEdit import IndentingTextEdit
from Interface.Widgets.ToggleButtons import PreparedButton


class EditSpellDialog(QDialog):
    def __init__(self, CharacterWindow, SpellList, SpellIndex, AddMode=False):
        super().__init__(parent=CharacterWindow)

        # Store Parameters
        self.CharacterWindow = CharacterWindow
        self.SpellList = SpellList
        self.SpellIndex = SpellIndex

        # Variables
        self.Spell = self.SpellList[self.SpellIndex]
        self.SpellOriginalState = copy.deepcopy(self.Spell)
        self.SmallTextEditMaxHeight = 70
        self.UpdatingFromSpell = False
        self.UnsavedChanges = False
        self.Cancelled = False

        # Prompt Label
        self.PromptLabel = QLabel("Add this spell:" if AddMode else "Edit this spell:")
        self.PromptLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Spell Name
        self.NameLabel = QLabel("Name:")
        self.NameLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.NameLineEdit = QLineEdit()
        self.NameLineEdit.setText(self.Spell["Spell Name"])
        self.NameLineEdit.textChanged.connect(self.UpdateSpell)

        # Spell Level
        self.LevelLabel = QLabel("Level:")
        self.LevelLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.LevelLineEdit = QLineEdit()
        self.LevelLineEdit.setText(self.Spell["Spell Level"])
        self.LevelLineEdit.textChanged.connect(self.UpdateSpell)

        # Spell School
        self.SchoolLabel = QLabel("School:")
        self.SchoolLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SchoolLineEdit = QLineEdit()
        self.SchoolLineEdit.setText(self.Spell["Spell School"])
        self.SchoolLineEdit.textChanged.connect(self.UpdateSpell)

        # Spell Casting Time
        self.CastingTimeLabel = QLabel("Casting Time:")
        self.CastingTimeLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CastingTimeTextEdit = IndentingTextEdit(TextChangedSlot=self.UpdateSpell, InitialContent=self.Spell["Spell Casting Time"])
        self.CastingTimeTextEdit.setMaximumHeight(self.SmallTextEditMaxHeight)
        self.CastingTimeTextEdit.setTabChangesFocus(True)

        # Spell Range
        self.RangeLabel = QLabel("Range:")
        self.RangeLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.RangeTextEdit = IndentingTextEdit(TextChangedSlot=self.UpdateSpell, InitialContent=self.Spell["Spell Range"])
        self.RangeTextEdit.setMaximumHeight(self.SmallTextEditMaxHeight)
        self.RangeTextEdit.setTabChangesFocus(True)

        # Spell Components
        self.ComponentsLabel = QLabel("Components:")
        self.ComponentsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ComponentsTextEdit = IndentingTextEdit(TextChangedSlot=self.UpdateSpell, InitialContent=self.Spell["Spell Components"])
        self.ComponentsTextEdit.setMaximumHeight(self.SmallTextEditMaxHeight)
        self.ComponentsTextEdit.setTabChangesFocus(True)

        # Spell Duration
        self.DurationLabel = QLabel("Duration:")
        self.DurationLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.DurationTextEdit = IndentingTextEdit(TextChangedSlot=self.UpdateSpell, InitialContent=self.Spell["Spell Duration"])
        self.DurationTextEdit.setMaximumHeight(self.SmallTextEditMaxHeight)
        self.DurationTextEdit.setTabChangesFocus(True)

        # Spell Description
        self.DescriptionLabel = QLabel("Description:")
        self.DescriptionLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.DescriptionTextEdit = IndentingTextEdit(TextChangedSlot=self.UpdateSpell, InitialContent=self.Spell["Spell Text"])
        self.DescriptionTextEdit.setTabChangesFocus(True)

        # Prepared
        self.PreparedButton = PreparedButton(self.UpdateSpell)
        self.UpdatingFromSpell = True
        self.PreparedButton.setChecked(self.Spell["Spell Prepared"])
        self.UpdatingFromSpell = False

        # Buttons
        self.DoneButton = QPushButton("Done")
        self.DoneButton.clicked.connect(self.Done)
        self.DoneButton.setDefault(True)
        self.DoneButton.setAutoDefault(True)
        self.CancelButton = QPushButton("Cancel")
        self.CancelButton.clicked.connect(self.Cancel)

        # Layout
        self.Layout = QGridLayout()

        self.Layout.addWidget(self.PromptLabel, 0, 0)

        self.SpellInputsLayout = QGridLayout()
        self.SpellInputsLayout.addWidget(self.NameLabel, 0, 0)
        self.SpellInputsLayout.addWidget(self.NameLineEdit, 0, 1)
        self.SpellInputsLayout.addWidget(self.LevelLabel, 1, 0)
        self.SpellInputsLayout.addWidget(self.LevelLineEdit, 1, 1)
        self.SpellInputsLayout.addWidget(self.SchoolLabel, 2, 0)
        self.SpellInputsLayout.addWidget(self.SchoolLineEdit, 2, 1)
        self.SpellInputsTextEditsLayout = QGridLayout()
        self.SpellInputsTextEditsLayout.addWidget(self.CastingTimeLabel, 0, 0)
        self.SpellInputsTextEditsLayout.addWidget(self.CastingTimeTextEdit, 1, 0)
        self.SpellInputsTextEditsLayout.addWidget(self.RangeLabel, 0, 1)
        self.SpellInputsTextEditsLayout.addWidget(self.RangeTextEdit, 1, 1)
        self.SpellInputsTextEditsLayout.addWidget(self.ComponentsLabel, 2, 0)
        self.SpellInputsTextEditsLayout.addWidget(self.ComponentsTextEdit, 3, 0)
        self.SpellInputsTextEditsLayout.addWidget(self.DurationLabel, 2, 1)
        self.SpellInputsTextEditsLayout.addWidget(self.DurationTextEdit, 3, 1)
        self.SpellInputsTextEditsLayout.addWidget(self.DescriptionLabel, 4, 0, 1, 2)
        self.SpellInputsTextEditsLayout.addWidget(self.DescriptionTextEdit, 5, 0, 1, 2)
        self.SpellInputsTextEditsLayout.setRowStretch(5, 1)
        self.SpellInputsLayout.addLayout(self.SpellInputsTextEditsLayout, 3, 0, 1, 2)
        self.SpellInputsLayout.addWidget(self.PreparedButton, 4, 0, 1, 2)
        self.Layout.addLayout(self.SpellInputsLayout, 1, 0)

        self.ButtonsLayout = QGridLayout()
        self.ButtonsLayout.addWidget(self.DoneButton, 0, 0)
        self.ButtonsLayout.addWidget(self.CancelButton, 0, 1)
        self.Layout.addLayout(self.ButtonsLayout, 2, 0)

        self.Layout.setRowStretch(1, 1)

        self.setLayout(self.Layout)

        # Set Window Title and Icon
        self.setWindowTitle(self.CharacterWindow.ScriptName)
        self.setWindowIcon(self.CharacterWindow.WindowIcon)

        # Select Text in Name Line Edit
        self.NameLineEdit.selectAll()

        # Execute Dialog
        self.exec()

    def UpdateSpell(self):
        if not self.ValidInput():
            return
        if self.UpdatingFromSpell:
            return
        self.Spell["Spell Name"] = self.NameLineEdit.text()
        self.Spell["Spell Level"] = self.LevelLineEdit.text()
        self.Spell["Spell School"] = self.SchoolLineEdit.text()
        self.Spell["Spell Casting Time"] = self.CastingTimeTextEdit.toPlainText()
        self.Spell["Spell Range"] = self.RangeTextEdit.toPlainText()
        self.Spell["Spell Components"] = self.ComponentsTextEdit.toPlainText()
        self.Spell["Spell Duration"] = self.DurationTextEdit.toPlainText()
        self.Spell["Spell Text"] = self.DescriptionTextEdit.toPlainText()
        self.Spell["Spell Prepared"] = self.PreparedButton.isChecked()
        self.UnsavedChanges = True

    def Done(self):
        if self.ValidInput(Alert=True):
            self.close()

    def Cancel(self):
        self.Spell.update(self.SpellOriginalState)
        self.UnsavedChanges = False
        self.Cancelled = True
        self.close()

    def ValidInput(self, Alert=False):
        if self.NameLineEdit.text() == "":
            if Alert:
                self.CharacterWindow.DisplayMessageBox("Spells must have a name.", Icon=QMessageBox.Icon.Warning, Parent=self)
            return False
        return True
