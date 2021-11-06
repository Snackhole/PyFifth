import json
import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit

from Core.PlayerCharacter import PlayerCharacter
from Core.DiceRoller import DiceRoller
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

        # Load Configs
        self.LoadConfigs()

        # Update Display
        self.UpdateDisplay()

    def CreateInterface(self):
        super().LoadTheme()

        # Header
        self.NameLabel = QLabel("Name:")
        self.NameLineEdit = QLineEdit()
        self.NameLineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.NameLineEdit.textChanged.connect(lambda: self.UpdateStat("Character Name", self.NameLineEdit.text()))

        # Create and Set Layout
        self.Layout = QGridLayout()
        self.HeaderLayout = QGridLayout()
        self.HeaderLayout.addWidget(self.NameLabel, 0, 0)
        self.HeaderLayout.addWidget(self.NameLineEdit, 0, 1)
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

    def UpdateWindowTitle(self):
        CurrentFileTitleSection = " [" + os.path.basename(self.CurrentOpenFileName) + "]" if self.CurrentOpenFileName != "" else ""
        UnsavedChangesIndicator = " *" if self.UnsavedChanges else ""
        self.setWindowTitle(self.ScriptName + " Character Sheet" + CurrentFileTitleSection + UnsavedChangesIndicator)
