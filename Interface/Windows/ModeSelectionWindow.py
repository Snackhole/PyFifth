import json
import os
import urllib.request

from PyQt6 import QtCore
from PyQt6.QtWidgets import QPushButton, QGridLayout, QComboBox, QLabel, QInputDialog, QSizePolicy, QCheckBox

from Build import BuildVariables
from Interface.Dialogs.UpdateDialog import UpdateDialog
from Interface.Windows.Window import Window


class ModeSelectionWindow(Window):
    def __init__(self, ScriptName, AbsoluteDirectoryPath, AppInst):
        # Variables
        self.Mode = None

        # Initialize Window
        super().__init__(ScriptName, AbsoluteDirectoryPath, AppInst)

        # Load Configs
        self.LoadConfigs()

        # Check for Updates
        if self.CheckForUpdatesOnStartCheckBox.isChecked():
            self.UpdateCheck()

    def CreateInterface(self):
        super().LoadTheme()

        # Styles
        self.ModeLabelStyle = "QLabel {font-size: 16pt;}"
        self.ModeComboBoxStyle = "QComboBox {font-size: 16pt;}"

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        # Mode Label
        self.ModeLabel = QLabel("PyFifth Mode:")
        self.ModeLabel.setStyleSheet(self.ModeLabelStyle)

        # Mode Combo Box
        self.ModeComboBox = QComboBox()
        self.ModeComboBox.setStyleSheet(self.ModeComboBoxStyle)
        self.ModeComboBox.setSizePolicy(self.InputsSizePolicy)
        self.ModeComboBox.addItem("Character Sheet")
        self.ModeComboBox.addItem("NPC Sheet")
        self.ModeComboBox.addItem("Encounter Sheet")
        self.ModeComboBox.addItem("Hoard Sheet")
        self.ModeComboBox.addItem("Coin Calculator")
        self.ModeComboBox.setEditable(False)

        # Buttons
        self.OpenButton = QPushButton("Open")
        self.OpenButton.clicked.connect(lambda: self.SelectMode(self.ModeComboBox.currentText()))
        self.SetThemeButton = QPushButton("Set Theme")
        self.SetThemeButton.clicked.connect(self.SetTheme)
        self.CheckForUpdatesButton = QPushButton("Check for Updates")
        self.CheckForUpdatesButton.clicked.connect(lambda: self.UpdateCheck(ManualCheck=True))

        # Check for Updates on Start Check Box
        self.CheckForUpdatesOnStartCheckBox = QCheckBox("Check for Updates on Start")

        # Create and Set Layout
        self.Layout = QGridLayout()
        self.Layout.addWidget(self.ModeLabel, 0, 0)
        self.Layout.addWidget(self.ModeComboBox, 0, 1)
        self.Layout.addWidget(self.OpenButton, 1, 0, 1, 2)
        self.Layout.addWidget(self.SetThemeButton, 2, 0, 1, 2)
        self.UpdatesLayout = QGridLayout()
        self.UpdatesLayout.addWidget(self.CheckForUpdatesButton, 0, 0)
        self.UpdatesLayout.addWidget(self.CheckForUpdatesOnStartCheckBox, 0, 1)
        self.UpdatesLayout.setColumnStretch(0, 1)
        self.Layout.addLayout(self.UpdatesLayout, 3, 0, 1, 2)
        self.Layout.setRowStretch(0, 1)
        self.Layout.setColumnStretch(1, 1)
        self.Frame.setLayout(self.Layout)

    def UpdateWindowTitle(self):
        self.setWindowTitle(f"{self.ScriptName} Mode Selection")

    def SelectMode(self, Mode):
        self.Mode = Mode
        self.close()

    def keyPressEvent(self, QKeyEvent):
        KeyPressed = QKeyEvent.key()
        if KeyPressed == QtCore.Qt.Key.Key_Return or KeyPressed == QtCore.Qt.Key.Key_Enter:
            self.SelectMode(self.ModeComboBox.currentText())
        else:
            super().keyPressEvent(QKeyEvent)

    def closeEvent(self, event):
        self.SaveConfigs()
        event.accept()

    def SetTheme(self):
        Themes = list(self.Themes.keys())
        Themes.sort()
        CurrentThemeIndex = Themes.index(self.Theme)
        Theme, OK = QInputDialog.getItem(self, "Set Theme", "Set theme (requires restart to take effect):", Themes, current=CurrentThemeIndex, editable=False)
        if OK:
            self.Theme = Theme
            self.DisplayMessageBox(f"The new theme will be active after {self.ScriptName} is restarted or a mode is selected.")

    def LoadConfigs(self):
        # Check for Updates on Start
        CheckForUpdatesOnStartFile = self.GetResourcePath("Configs/CheckForUpdatesOnStart.cfg")
        if os.path.isfile(CheckForUpdatesOnStartFile):
            with open(CheckForUpdatesOnStartFile, "r") as ConfigFile:
                self.CheckForUpdatesOnStartCheckBox.setChecked(json.loads(ConfigFile.read()))
        else:
            self.CheckForUpdatesOnStartCheckBox.setChecked(True)

    def SaveConfigs(self):
        if not os.path.isdir(self.GetResourcePath("Configs")):
            os.mkdir(self.GetResourcePath("Configs"))

        # Theme
        with open(self.GetResourcePath("Configs/Theme.cfg"), "w") as ConfigFile:
            ConfigFile.write(json.dumps(self.Theme))

        # Check for Updates on Start
        with open(self.GetResourcePath("Configs/CheckForUpdatesOnStart.cfg"), "w") as ConfigFile:
            ConfigFile.write(json.dumps(self.CheckForUpdatesOnStartCheckBox.isChecked()))

    # Update Checking Methods
    def UpdateCheck(self, ManualCheck=False):
        try:
            Contents = urllib.request.urlopen(f"https://api.github.com/repos/Snackhole/{BuildVariables["AppName"]}/releases").read()
            Contents = Contents.decode("utf-8")
            Contents = json.loads(Contents)
            LatestVersion = Contents[0]["tag_name"]
            if LatestVersion != BuildVariables["Version"]:
                UpdateDialogInst = UpdateDialog(LatestVersion, self)
            elif ManualCheck and LatestVersion == BuildVariables["Version"]:
                self.DisplayMessageBox("You are using the latest version.")
        except Exception as Error:
            self.DisplayMessageBox(f"Checking for updates caused the following error:\n\n{str(Error)}.")
