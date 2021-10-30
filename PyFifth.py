import os
import sys

AbsoluteDirectoryPath = os.path.dirname(os.path.abspath(__file__))
if AbsoluteDirectoryPath.endswith(".pyz") or AbsoluteDirectoryPath.endswith(".pyzw"):
    AbsoluteDirectoryPath = os.path.dirname(AbsoluteDirectoryPath)
if sys.path[0] != AbsoluteDirectoryPath:
    sys.path.insert(0, AbsoluteDirectoryPath)

from PyQt5.QtWidgets import QApplication

from Build import BuildVariables


def StartApp():
    pass


if __name__ == "__main__":
    StartApp()
