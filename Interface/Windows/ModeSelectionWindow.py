import json
import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QGridLayout, QComboBox, QLabel, QInputDialog, QSizePolicy

from Interface.Windows.Window import Window


class ModeSelectionWindow(Window):
    def __init__(self, ScriptName, AbsoluteDirectoryPath, AppInst):
        super().__init__(ScriptName, AbsoluteDirectoryPath, AppInst)

        # Create Mode Value
        self.Mode = None

    def CreateInterface(self):
        super().LoadTheme()

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Mode Label
        self.ModeLabel = QLabel("PyFifth Mode:")

        # Mode Combo Box
        self.ModeComboBox = QComboBox()
        self.ModeComboBox.setSizePolicy(self.InputsSizePolicy)
        self.ModeComboBox.addItem("Character Sheet")
        self.ModeComboBox.addItem("NPC Sheet")
        self.ModeComboBox.addItem("Coin Calculator")
        self.ModeComboBox.setEditable(False)

        # Buttons
        self.OpenButton = QPushButton("Open")
        self.OpenButton.clicked.connect(lambda: self.SelectMode(self.ModeComboBox.currentText()))
        self.SetThemeButton = QPushButton("Set Theme")
        self.SetThemeButton.clicked.connect(self.SetTheme)

        # Create and Set Layout
        self.Layout = QGridLayout()
        self.Layout.addWidget(self.ModeLabel, 0, 0)
        self.Layout.addWidget(self.ModeComboBox, 0, 1)
        self.Layout.addWidget(self.OpenButton, 1, 0, 1, 2)
        self.Layout.addWidget(self.SetThemeButton, 2, 0, 1, 2)
        self.Layout.setRowStretch(0, 1)
        self.Layout.setColumnStretch(1, 1)
        self.Frame.setLayout(self.Layout)

    def UpdateWindowTitle(self):
        self.setWindowTitle(self.ScriptName + " Mode Selection")

    def SelectMode(self, Mode):
        self.Mode = Mode
        self.close()

    def keyPressEvent(self, QKeyEvent):
        KeyPressed = QKeyEvent.key()
        if KeyPressed == QtCore.Qt.Key_Return or KeyPressed == QtCore.Qt.Key_Enter:
            self.SelectMode(self.ModeComboBox.currentText())
        else:
            super().keyPressEvent(QKeyEvent)

    def closeEvent(self, event):
        if not os.path.isdir(self.GetResourcePath("Configs")):
            os.mkdir(self.GetResourcePath("Configs"))
        with open(self.GetResourcePath("Configs/Theme.cfg"), "w") as ConfigFile:
            ConfigFile.write(json.dumps(self.Theme))
        event.accept()

    def SetTheme(self):
        Themes = list(self.Themes.keys())
        Themes.sort()
        CurrentThemeIndex = Themes.index(self.Theme)
        Theme, OK = QInputDialog.getItem(self, "Set Theme", "Set theme (requires restart to take effect):", Themes, current=CurrentThemeIndex, editable=False)
        if OK:
            self.Theme = Theme
            self.DisplayMessageBox("The new theme will be active after PyFifth is restarted or a mode is selected.")
