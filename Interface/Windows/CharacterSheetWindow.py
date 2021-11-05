import json
import os

from PyQt5.QtWidgets import QGridLayout

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

        # Create and Set Layout
        self.Layout = QGridLayout()
        self.Frame.setLayout(self.Layout)

    def CreateActions(self):
        pass

    def CreateMenuBar(self):
        pass

    def CreateKeybindings(self):
        pass

    def LoadConfigs(self):
        super().LoadConfigs()

    def SaveConfigs(self):
        super().SaveConfigs()

        # TODO Keybindings
        # with open(self.GetResourcePath("Configs/Keybindings.cfg"), "w") as ConfigFile:
        #     ConfigFile.write(json.dumps(self.Keybindings, indent=2))

        # Last Opened Directory
        self.SaveLastOpenedDirectory()

        # Gzip Mode
        self.SaveGzipMode()

    # Display Update Methods
    def UpdateDisplay(self):
        self.UpdateWindowTitle()

    def UpdateWindowTitle(self):
        self.setWindowTitle(self.ScriptName + " Character Sheet")
