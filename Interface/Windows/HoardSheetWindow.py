import copy
import json
import os

from PyQt5.QtWidgets import QAction, QFrame, QGridLayout, QLabel, QMessageBox

from Core.Hoard import Hoard
from Interface.Dialogs.CoinCalculatorDialog import CoinCalculatorDialog
from Interface.Widgets.CenteredLineEdit import CenteredLineEdit
from Interface.Windows.Window import Window
from SaveAndLoad.SaveAndOpenMixin import SaveAndOpenMixin


class HoardSheetWindow(Window, SaveAndOpenMixin):
    # Initialization Methods
    def __init__(self, ScriptName, AbsoluteDirectoryPath, AppInst):
        # Store Parameters
        self.ScriptName = ScriptName
        self.AbsoluteDirectoryPath = AbsoluteDirectoryPath
        self.AppInst = AppInst

        # Variables
        self.UpdatingFieldsFromHoard = False

        # Initialize Window
        super().__init__(ScriptName, AbsoluteDirectoryPath, AppInst)

        # Set Up Save and Open
        self.SetUpSaveAndOpen(".pyfifthhoard", "PyFifth Hoard Sheet", (Hoard,))

        # Create Hoard
        self.Hoard = Hoard()

        # Load Configs
        self.LoadConfigs()

        # Update Display
        self.UpdateDisplay()

    def CreateInterface(self):
        super().LoadTheme()

        # Header
        self.NameOrOwnersLabel = QLabel("Name or Owners:")
        self.NameOrOwnersLineEdit = CenteredLineEdit()
        self.NameOrOwnersLineEdit.textChanged.connect(lambda: self.UpdateData("Name or Owners", self.NameOrOwnersLineEdit.text()))

        self.LocationLabel = QLabel("Location:")
        self.LocationLineEdit = CenteredLineEdit()
        self.LocationLineEdit.textChanged.connect(lambda: self.UpdateData("Location", self.LocationLineEdit.text()))

        self.StorageCostsLabel = QLabel("Storage Costs:")
        self.StorageCostsLineEdit = CenteredLineEdit()
        self.StorageCostsLineEdit.textChanged.connect(lambda: self.UpdateData("Storage Costs", self.StorageCostsLineEdit.text()))

        # Create and Set Layout
        self.Layout = QGridLayout()

        self.HeaderFrame = QFrame()
        self.HeaderFrame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.HeaderLayout = QGridLayout()
        self.HeaderLayout.addWidget(self.NameOrOwnersLabel, 0, 0)
        self.HeaderLayout.addWidget(self.NameOrOwnersLineEdit, 0, 1)
        self.HeaderLayout.addWidget(self.LocationLabel, 0, 2)
        self.HeaderLayout.addWidget(self.LocationLineEdit, 0, 3)
        self.HeaderLayout.addWidget(self.StorageCostsLabel, 0, 4)
        self.HeaderLayout.addWidget(self.StorageCostsLineEdit, 0, 5)
        for Column in [1, 3, 5]:
            self.HeaderLayout.setColumnStretch(Column, 1)
        self.HeaderFrame.setLayout(self.HeaderLayout)
        self.Layout.addWidget(self.HeaderFrame, 0, 0)

        self.HoardFrame = QFrame()
        self.HoardFrame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.HoardLayout = QGridLayout()
        self.HoardFrame.setLayout(self.HoardLayout)
        self.Layout.addWidget(self.HoardFrame, 1, 0)

        self.Layout.setRowStretch(1, 1)

        self.Frame.setLayout(self.Layout)

        # Create Actions
        self.CreateActions()

        # Create Menu Bar
        self.CreateMenuBar()

        # Create Status Bar
        self.StatusBar = self.statusBar()

        # Create Keybindings
        self.CreateKeybindings()

    def CreateActions(self):
        self.NewAction = QAction("New")
        self.NewAction.triggered.connect(self.NewActionTriggered)

        self.OpenAction = QAction("Open")
        self.OpenAction.triggered.connect(self.OpenActionTriggered)

        self.SaveAction = QAction("Save")
        self.SaveAction.triggered.connect(self.SaveActionTriggered)

        self.SaveAsAction = QAction("Save As")
        self.SaveAsAction.triggered.connect(self.SaveAsActionTriggered)

        self.GzipModeAction = QAction("Gzip Mode (Smaller Files)")
        self.GzipModeAction.setCheckable(True)
        self.GzipModeAction.setChecked(self.GzipMode)
        self.GzipModeAction.triggered.connect(self.ToggleGzipMode)

        self.QuitAction = QAction("Quit")
        self.QuitAction.triggered.connect(self.close)

        self.CoinCalculatorAction = QAction("Coin Calculator")
        self.CoinCalculatorAction.triggered.connect(self.ShowCoinCalculator)

    def CreateMenuBar(self):
        self.MenuBar = self.menuBar()

        self.FileMenu = self.MenuBar.addMenu("File")
        self.FileMenu.addAction(self.NewAction)
        self.FileMenu.addAction(self.OpenAction)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.SaveAction)
        self.FileMenu.addAction(self.SaveAsAction)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.GzipModeAction)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.QuitAction)

        self.MenuBar.addAction(self.CoinCalculatorAction)

    def CreateKeybindings(self):
        self.DefaultKeybindings = {}
        self.DefaultKeybindings["NewAction"] = "Ctrl+N"
        self.DefaultKeybindings["OpenAction"] = "Ctrl+O"
        self.DefaultKeybindings["SaveAction"] = "Ctrl+S"
        self.DefaultKeybindings["SaveAsAction"] = "Ctrl+Shift+S"
        self.DefaultKeybindings["QuitAction"] = "Ctrl+Q"

    def LoadConfigs(self):
        # Keybindings
        KeybindingsFile = self.GetResourcePath("Configs/HoardKeybindings.cfg")
        if os.path.isfile(KeybindingsFile):
            with open(KeybindingsFile, "r") as ConfigFile:
                self.Keybindings = json.loads(ConfigFile.read())
        else:
            self.Keybindings = copy.deepcopy(self.DefaultKeybindings)
        for Action, Keybinding in self.DefaultKeybindings.items():
            if Action not in self.Keybindings:
                self.Keybindings[Action] = Keybinding
        InvalidBindings = []
        for Action in self.Keybindings.keys():
            if Action not in self.DefaultKeybindings:
                InvalidBindings.append(Action)
        for InvalidBinding in InvalidBindings:
            del self.Keybindings[InvalidBinding]
        for Action, Keybinding in self.Keybindings.items():
            getattr(self, Action).setShortcut(Keybinding)

    def SaveConfigs(self):
        if not os.path.isdir(self.GetResourcePath("Configs")):
            os.mkdir(self.GetResourcePath("Configs"))

        # Keybindings
        with open(self.GetResourcePath("Configs/NPCKeybindings.cfg"), "w") as ConfigFile:
            ConfigFile.write(json.dumps(self.Keybindings, indent=2))

        # Last Opened Directory
        self.SaveLastOpenedDirectory()

        # Gzip Mode
        self.SaveGzipMode()

    # Hoard Methods
    def UpdateData(self, Data, NewValue):
        if not self.UpdatingFieldsFromHoard:
            self.Hoard.UpdateData(Data, NewValue)
            self.UpdateUnsavedChangesFlag(True)

    # View Methods
    def ShowCoinCalculator(self):
        CoinCalculatorDialog(self)

    # Save and Open Methods
    def NewActionTriggered(self):
        if self.New(self.Hoard):
            self.Hoard = Hoard()
        self.UpdatingFieldsFromHoard = True
        self.UpdateDisplay()
        self.UpdatingFieldsFromHoard = False

    def OpenActionTriggered(self):
        OpenData = self.Open(self.Hoard)
        if OpenData is not None:
            self.Hoard = OpenData
        self.UpdatingFieldsFromHoard = True
        self.UpdateDisplay()
        self.UpdatingFieldsFromHoard = False

    def SaveActionTriggered(self):
        self.Save(self.Hoard)
        self.UpdateDisplay()

    def SaveAsActionTriggered(self):
        self.Save(self.Hoard, SaveAs=True)
        self.UpdateDisplay()

    def ToggleGzipMode(self):
        self.GzipMode = not self.GzipMode

    def closeEvent(self, event):
        Close = True
        if self.UnsavedChanges:
            SavePrompt = self.DisplayMessageBox("Save unsaved changes before closing?", Icon=QMessageBox.Warning, Buttons=(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel))
            if SavePrompt == QMessageBox.Yes:
                if not self.Save(self.Hoard):
                    Close = False
            elif SavePrompt == QMessageBox.No:
                pass
            elif SavePrompt == QMessageBox.Cancel:
                Close = False
        if not Close:
            event.ignore()
        else:
            self.SaveConfigs()
            event.accept()

    def UpdateUnsavedChangesFlag(self, UnsavedChanges):
        self.UnsavedChanges = UnsavedChanges
        self.UpdateDisplay()

   # Display Update Methods
    def UpdateDisplay(self):
        self.UpdateWindowTitle()

        # Updating Fields from Hoard
        if self.UpdatingFieldsFromHoard:
            self.NameOrOwnersLineEdit.setText(self.Hoard.HoardData["Name or Owners"])
            self.LocationLineEdit.setText(self.Hoard.HoardData["Location"])
            self.StorageCostsLineEdit.setText(self.Hoard.HoardData["Storage Costs"])

    def UpdateWindowTitle(self):
        CurrentFileTitleSection = " [" + os.path.basename(self.CurrentOpenFileName) + "]" if self.CurrentOpenFileName != "" else ""
        UnsavedChangesIndicator = " *" if self.UnsavedChanges else ""
        self.setWindowTitle(self.ScriptName + " Hoard Sheet" + CurrentFileTitleSection + UnsavedChangesIndicator)
