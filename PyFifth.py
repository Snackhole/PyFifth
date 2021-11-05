import os
import sys

AbsoluteDirectoryPath = os.path.dirname(os.path.abspath(__file__))
if AbsoluteDirectoryPath.endswith(".pyz") or AbsoluteDirectoryPath.endswith(".pyzw"):
    AbsoluteDirectoryPath = os.path.dirname(AbsoluteDirectoryPath)
if sys.path[0] != AbsoluteDirectoryPath:
    sys.path.insert(0, AbsoluteDirectoryPath)

from PyQt5.QtWidgets import QApplication

from Interface.Windows.ModeSelectionWindow import ModeSelectionWindow
from Interface.Windows.CharacterSheetWindow import CharacterSheetWindow
from Build import BuildVariables


def StartApp():
    AppInst = QApplication(sys.argv)

    # Script Name
    ScriptName = BuildVariables["VersionedAppName"]

    # Mode Selection Window
    ModeSelectionWindowInst = ModeSelectionWindow(ScriptName, AbsoluteDirectoryPath, AppInst)

    # Enter Mode Selection Loop
    AppInst.exec_()

    # Initialize Mode
    Mode = ModeSelectionWindowInst.Mode
    if Mode is not None:
        # Modes Dictionary
        Modes = {}
        Modes["Character Sheet"] = CharacterSheetWindow

        # Create Mode Window
        ModeWindowInst = Modes[Mode](ScriptName, AbsoluteDirectoryPath, AppInst)

        # Enter Mode Loop
        sys.exit(AppInst.exec_())


if __name__ == "__main__":
    StartApp()
