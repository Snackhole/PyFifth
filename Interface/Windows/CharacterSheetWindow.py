from PyQt5.QtWidgets import QGridLayout

from Interface.Windows.Window import Window


class CharacterSheetWindow(Window):
    def __init__(self, ScriptName, AbsoluteDirectoryPath):
        super().__init__(ScriptName, AbsoluteDirectoryPath)

    def CreateInterface(self):
        # Create and Set Layout
        self.Layout = QGridLayout()
        self.Frame.setLayout(self.Layout)

    def UpdateWindowTitle(self):
        self.setWindowTitle(self.ScriptName + " Character Sheet")
