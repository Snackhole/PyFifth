import json
import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import QGridLayout, QLabel, QSpinBox

from Core.PlayerCharacter import PlayerCharacter
from Core.DiceRoller import DiceRoller
from Interface.Widgets.CenteredLineEdit import CenteredLineEdit
from Interface.Windows.Window import Window
from SaveAndLoad.SaveAndOpenMixin import SaveAndOpenMixin


class CharacterSheetWindow(Window, SaveAndOpenMixin):
    # Initialization Methods
    def __init__(self, ScriptName, AbsoluteDirectoryPath, AppInst):
        # Store Parameters
        self.ScriptName = ScriptName
        self.AbsoluteDirectoryPath = AbsoluteDirectoryPath
        self.AppInst = AppInst

        # Initialize Window
        super().__init__(ScriptName, AbsoluteDirectoryPath, AppInst)

        # Set Up Save and Open
        self.SetUpSaveAndOpen(".pyfifthcharacter", "PyFifth Character Sheet", (PlayerCharacter, DiceRoller))

        # Create Player Character
        self.PlayerCharacter = PlayerCharacter()

        # Derived Stats
        self.DerivedStats = self.PlayerCharacter.GetDerivedStats()

        # Load Configs
        self.LoadConfigs()

        # Update Display
        self.UpdateDisplay()

    def CreateInterface(self):
        super().LoadTheme()

        # Header
        self.NameLabel = QLabel("Name:")
        self.NameLineEdit = CenteredLineEdit()
        self.NameLineEdit.textChanged.connect(lambda: self.UpdateStat("Character Name", self.NameLineEdit.text()))

        self.ClassLabel = QLabel("Class:")
        self.ClassLineEdit = CenteredLineEdit()
        self.ClassLineEdit.textChanged.connect(lambda: self.UpdateStat("Character Class", self.ClassLineEdit.text()))

        self.LevelLabel = QLabel("Level:")
        self.LevelSpinBox = QSpinBox()
        self.LevelSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.LevelSpinBox.setButtonSymbols(self.LevelSpinBox.NoButtons)
        self.LevelSpinBox.setRange(1, 20)
        self.LevelSpinBox.valueChanged.connect(lambda: self.UpdateStat("Character Level", self.LevelSpinBox.value()))

        self.ProficiencyBonusLabel = QLabel("Proficiency Bonus:")
        self.ProficiencyBonusLineEdit = CenteredLineEdit()
        self.ProficiencyBonusLineEdit.setReadOnly(True)

        self.ExperienceLabel = QLabel("Exp.:")
        self.ExperienceSpinBox = QSpinBox()
        self.ExperienceSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ExperienceSpinBox.setButtonSymbols(self.ExperienceSpinBox.NoButtons)
        self.ExperienceSpinBox.setRange(0, 1000000000)
        self.ExperienceSpinBox.valueChanged.connect(lambda: self.UpdateStat("Character Experience Earned", self.ExperienceSpinBox.value()))

        self.NeededExperienceLabel = QLabel("Needed Exp.:")
        self.NeededExperienceLineEdit = CenteredLineEdit()
        self.NeededExperienceLineEdit.setReadOnly(True)

        # Create and Set Layout
        self.Layout = QGridLayout()

        self.HeaderLayout = QGridLayout()
        self.HeaderLayout.addWidget(self.NameLabel, 0, 0)
        self.HeaderLayout.addWidget(self.NameLineEdit, 0, 1)
        self.HeaderLayout.addWidget(self.ClassLabel, 1, 0)
        self.HeaderLayout.addWidget(self.ClassLineEdit, 1, 1)
        self.HeaderLayout.addWidget(self.LevelLabel, 0, 2)
        self.HeaderLayout.addWidget(self.LevelSpinBox, 0, 3)
        self.HeaderLayout.addWidget(self.ProficiencyBonusLabel, 1, 2)
        self.HeaderLayout.addWidget(self.ProficiencyBonusLineEdit, 1, 3)
        self.HeaderLayout.addWidget(self.ExperienceLabel, 0, 4)
        self.HeaderLayout.addWidget(self.ExperienceSpinBox, 0, 5)
        self.HeaderLayout.addWidget(self.NeededExperienceLabel, 1, 4)
        self.HeaderLayout.addWidget(self.NeededExperienceLineEdit, 1, 5)
        self.HeaderLayout.setColumnStretch(1, 1)

        self.Layout.addLayout(self.HeaderLayout, 0, 0)
        self.Frame.setLayout(self.Layout)

    def CreateActions(self):
        pass

    def CreateMenuBar(self):
        pass

    def CreateKeybindings(self):
        pass

    def LoadConfigs(self):
        pass

    def SaveConfigs(self):
        # TODO Keybindings
        # with open(self.GetResourcePath("Configs/Keybindings.cfg"), "w") as ConfigFile:
        #     ConfigFile.write(json.dumps(self.Keybindings, indent=2))

        # Last Opened Directory
        self.SaveLastOpenedDirectory()

        # Gzip Mode
        self.SaveGzipMode()

    # Player Character Methods
    def UpdateStat(self, Stat, NewValue):
        self.PlayerCharacter.UpdateStat(Stat, NewValue)
        self.UpdateUnsavedChangesFlag(True)

    # Save and Open Methods
    def UpdateUnsavedChangesFlag(self, UnsavedChanges):
        self.UnsavedChanges = UnsavedChanges
        self.UpdateDisplay()

    # Display Update Methods
    def UpdateDisplay(self):
        self.UpdateWindowTitle()

        # Update Derived Stats
        self.DerivedStats = self.PlayerCharacter.GetDerivedStats()

        # Proficiency Bonus
        ProficiencyBonusText = "+" + str(self.DerivedStats["Proficiency Bonus"])
        self.ProficiencyBonusLineEdit.setText(ProficiencyBonusText)

        # Needed Experience
        ExperienceNeeded = str(self.DerivedStats["Experience Needed"])
        self.NeededExperienceLineEdit.setText(ExperienceNeeded)

    def UpdateWindowTitle(self):
        CurrentFileTitleSection = " [" + os.path.basename(self.CurrentOpenFileName) + "]" if self.CurrentOpenFileName != "" else ""
        UnsavedChangesIndicator = " *" if self.UnsavedChanges else ""
        self.setWindowTitle(self.ScriptName + " Character Sheet" + CurrentFileTitleSection + UnsavedChangesIndicator)
