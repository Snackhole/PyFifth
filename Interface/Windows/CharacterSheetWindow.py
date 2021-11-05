from PyQt5.QtWidgets import QGridLayout

from Core.PlayerCharacter import PlayerCharacter
from Core.DiceRoller import DiceRoller
from Interface.Windows.Window import Window
from SaveAndLoad.SaveAndOpenMixin import SaveAndOpenMixin


class CharacterSheetWindow(Window, SaveAndOpenMixin):
    def __init__(self, ScriptName, AbsoluteDirectoryPath):
        # Store Parameters
        self.ScriptName = ScriptName
        self.AbsoluteDirectoryPath = AbsoluteDirectoryPath

        # Initialize Window
        super().__init__(ScriptName, AbsoluteDirectoryPath)

        # Create Player Character
        self.PlayerCharacter = PlayerCharacter()

        # Set Up Save and Open
        self.SetUpSaveAndOpen(".pyfifthcharacter", "PyFifth Character Sheet", (PlayerCharacter, DiceRoller))

    def CreateInterface(self):
        # Create and Set Layout
        self.Layout = QGridLayout()
        self.Frame.setLayout(self.Layout)

    def UpdateWindowTitle(self):
        self.setWindowTitle(self.ScriptName + " Character Sheet")
