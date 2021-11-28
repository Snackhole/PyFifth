import copy
import functools

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QSizePolicy, QMessageBox

from Interface.Dialogs.EditModifierDialog import EditModifierDialog
from Interface.Widgets.IconButtons import EditButton


class EditSkillsDialog(QDialog):
    def __init__(self, CharacterWindow):
        super().__init__(parent=CharacterWindow)

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Variables
        self.Skills = self.CharacterWindow.PlayerCharacter.Stats["Skills"]
        self.SkillsOriginalState = copy.deepcopy(self.Skills)
        self.UnsavedChanges = False
        self.Cancelled = False

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Prompt Label
        self.PromptLabel = QLabel("Set your skill modifiers:")
        self.PromptLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Skill Inputs
        self.SkillInputs = {}
        self.SkillInputsList = []
        for Skill in self.Skills:
            # Label
            LabelText = Skill[:-len(" Stat Modifier")]
            self.SkillInputs[Skill + " Label"] = QLabel(LabelText)
            Label = self.SkillInputs[Skill + " Label"]
            Label.setAlignment(QtCore.Qt.AlignCenter)

            # Edit Button
            self.SkillInputs[Skill + " Edit Button"] = EditButton(functools.partial(self.EditModifier, Skill), "Edit " + Skill)
            Button = self.SkillInputs[Skill + " Edit Button"]
            Button.setSizePolicy(self.InputsSizePolicy)

            # Append to List
            self.SkillInputsList.append((Label, Button))

        # Dialog Buttons
        self.DoneButton = QPushButton("Done")
        self.DoneButton.clicked.connect(self.Done)
        self.SetToDefaultButton = QPushButton("Set to Default")
        self.SetToDefaultButton.clicked.connect(self.SetToDefault)
        self.CancelButton = QPushButton("Cancel")
        self.CancelButton.clicked.connect(self.Cancel)

        # Layout
        self.Layout = QGridLayout()

        self.Layout.addWidget(self.PromptLabel, 0, 0)

        self.SkillInputsLayout = QGridLayout()
        CurrentWidgetsIndex = 0
        for Column in range(0, 6, 2):
            for Row in range(6):
                self.SkillInputsLayout.addWidget(self.SkillInputsList[CurrentWidgetsIndex][0], Row, Column)
                self.SkillInputsLayout.addWidget(self.SkillInputsList[CurrentWidgetsIndex][1], Row, Column + 1)
                CurrentWidgetsIndex += 1
        self.PassiveSkillInputsLayout = QGridLayout()
        self.PassiveSkillInputsLayout.addWidget(self.SkillInputsList[CurrentWidgetsIndex][0], 0, 0)
        self.PassiveSkillInputsLayout.addWidget(self.SkillInputsList[CurrentWidgetsIndex][1], 0, 1)
        CurrentWidgetsIndex += 1
        self.PassiveSkillInputsLayout.addWidget(self.SkillInputsList[CurrentWidgetsIndex][0], 0, 2)
        self.PassiveSkillInputsLayout.addWidget(self.SkillInputsList[CurrentWidgetsIndex][1], 0, 3)
        self.SkillInputsLayout.addLayout(self.PassiveSkillInputsLayout, 6, 0, 1, 6)
        self.Layout.addLayout(self.SkillInputsLayout, 1, 0)

        self.DialogButtonsLayout = QGridLayout()
        self.DialogButtonsLayout.addWidget(self.DoneButton, 0, 0)
        self.DialogButtonsLayout.addWidget(self.SetToDefaultButton, 0, 1)
        self.DialogButtonsLayout.addWidget(self.CancelButton, 0, 2)
        self.Layout.addLayout(self.DialogButtonsLayout, 3, 0)

        self.Layout.setRowStretch(1, 1)

        self.setLayout(self.Layout)

        # Set Window Title and Icon
        self.setWindowTitle(self.CharacterWindow.ScriptName)
        self.setWindowIcon(self.CharacterWindow.WindowIcon)

        # Execute Dialog
        self.exec_()

    def EditModifier(self, Modifier):
        EditModifierDialogInst = EditModifierDialog(self, self.CharacterWindow, self.Skills[Modifier], Modifier)
        self.UnsavedChanges = EditModifierDialogInst.UnsavedChanges

    def Done(self):
        self.close()

    def SetToDefault(self):
        Confirm = self.CharacterWindow.DisplayMessageBox("Are you sure you want to set skills data to default values?  This cannot be undone.", Icon=QMessageBox.Warning, Buttons=(QMessageBox.Yes | QMessageBox.No), Parent=self)
        if Confirm == QMessageBox.Yes:
            DefaultSkillsData = self.CharacterWindow.PlayerCharacter.CreateSkillsStats()
            self.Skills.update(DefaultSkillsData)
            self.UnsavedChanges = True
            self.close()

    def Cancel(self):
        self.Skills.update(self.SkillsOriginalState)
        self.UnsavedChanges = False
        self.Cancelled = True
        self.close()
