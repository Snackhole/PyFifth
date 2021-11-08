import copy
import json
import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import QGridLayout, QLabel, QSpinBox, QMessageBox, QAction

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

        # Variables
        self.Opening = False

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

    def CreateKeybindings(self):
        self.DefaultKeybindings = {}
        self.DefaultKeybindings["NewAction"] = "Ctrl+N"
        self.DefaultKeybindings["OpenAction"] = "Ctrl+O"
        self.DefaultKeybindings["SaveAction"] = "Ctrl+S"
        self.DefaultKeybindings["SaveAsAction"] = "Ctrl+Shift+S"
        self.DefaultKeybindings["QuitAction"] = "Ctrl+Q"

    def LoadConfigs(self):
        # Keybindings
        KeybindingsFile = self.GetResourcePath("Configs/Keybindings.cfg")
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
        # Keybindings
        with open(self.GetResourcePath("Configs/Keybindings.cfg"), "w") as ConfigFile:
            ConfigFile.write(json.dumps(self.Keybindings, indent=2))

        # Last Opened Directory
        self.SaveLastOpenedDirectory()

        # Gzip Mode
        self.SaveGzipMode()

    # Player Character Methods
    def UpdateStat(self, Stat, NewValue):
        if not self.Opening:
            self.PlayerCharacter.UpdateStat(Stat, NewValue)
            self.UpdateUnsavedChangesFlag(True)

    # Save and Open Methods
    def NewActionTriggered(self):
        if self.New(self.PlayerCharacter):
            self.PlayerCharacter = PlayerCharacter()
        self.Opening = True
        self.UpdateDisplay()
        self.Opening = False

    def OpenActionTriggered(self):
        OpenData = self.Open(self.PlayerCharacter)
        if OpenData is not None:
            self.PlayerCharacter = OpenData
        self.Opening = True
        self.UpdateDisplay()
        self.Opening = False

    def SaveActionTriggered(self):
        self.Save(self.PlayerCharacter)
        self.UpdateDisplay()

    def SaveAsActionTriggered(self):
        self.Save(self.PlayerCharacter, SaveAs=True)
        self.UpdateDisplay()

    def ToggleGzipMode(self):
        self.GzipMode = not self.GzipMode

    def closeEvent(self, event):
        Close = True
        if self.UnsavedChanges:
            SavePrompt = self.DisplayMessageBox("Save unsaved changes before closing?", Icon=QMessageBox.Warning, Buttons=(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel))
            if SavePrompt == QMessageBox.Yes:
                if not self.Save(self.PlayerCharacter):
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

        # Update Derived Stats
        self.DerivedStats = self.PlayerCharacter.GetDerivedStats()

        # Proficiency Bonus
        ProficiencyBonusText = "+" + str(self.DerivedStats["Proficiency Bonus"])
        self.ProficiencyBonusLineEdit.setText(ProficiencyBonusText)

        # Needed Experience
        ExperienceNeeded = str(self.DerivedStats["Experience Needed"])
        self.NeededExperienceLineEdit.setText(ExperienceNeeded)

        if self.Opening:
            self.NameLineEdit.setText(self.PlayerCharacter.Stats["Character Name"])
            self.ClassLineEdit.setText(self.PlayerCharacter.Stats["Character Class"])
            self.LevelSpinBox.setValue(self.PlayerCharacter.Stats["Character Level"])
            self.ExperienceSpinBox.setValue(self.PlayerCharacter.Stats["Character Experience Earned"])

    def UpdateWindowTitle(self):
        CurrentFileTitleSection = " [" + os.path.basename(self.CurrentOpenFileName) + "]" if self.CurrentOpenFileName != "" else ""
        UnsavedChangesIndicator = " *" if self.UnsavedChanges else ""
        self.setWindowTitle(self.ScriptName + " Character Sheet" + CurrentFileTitleSection + UnsavedChangesIndicator)
