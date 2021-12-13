import copy
import json
import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import QAction, QMessageBox, QGridLayout

from Core.DiceRoller import DiceRoller
from Core.NonPlayerCharacter import NonPlayerCharacter
from Interface.Windows.Window import Window
from SaveAndLoad.SaveAndOpenMixin import SaveAndOpenMixin


class NPCSheetWindow(Window, SaveAndOpenMixin):
    # Initialization Methods
    def __init__(self, ScriptName, AbsoluteDirectoryPath, AppInst):
        # Store Parameters
        self.ScriptName = ScriptName
        self.AbsoluteDirectoryPath = AbsoluteDirectoryPath
        self.AppInst = AppInst

        # Variables
        self.UpdatingFieldsFromNonPlayerCharacter = False

        # Initialize Window
        super().__init__(ScriptName, AbsoluteDirectoryPath, AppInst)

        # Set Up Save and Open
        self.SetUpSaveAndOpen(".pyfifthnpc", "PyFifth NPC Sheet", (NonPlayerCharacter, DiceRoller))

        # Create Non-Player Character
        self.NonPlayerCharacter = NonPlayerCharacter()

        # Derived Stats
        self.DerivedStats = self.NonPlayerCharacter.GetDerivedStats()

        # Load Configs
        self.LoadConfigs()

        # Update Display
        self.UpdateDisplay()

    def CreateInterface(self):
        super().LoadTheme()

        # Create and Set Layout
        self.Layout = QGridLayout()

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

        # TODO
        # self.CoinCalculatorAction = QAction("Coin Calculator")
        # self.CoinCalculatorAction.triggered.connect(self.ShowCoinCalculator)

        # TODO
        # self.PortraitEnabledAction = QAction("Portrait Enabled")
        # self.PortraitEnabledAction.setCheckable(True)
        # self.PortraitEnabledAction.setChecked(True)
        # self.PortraitEnabledAction.triggered.connect(self.TogglePortraitEnabled)

        # TODO
        # self.SetCritMinimumAction = QAction("Set Crit Minimum")
        # self.SetCritMinimumAction.triggered.connect(self.SetCritMinimumActionTriggered)

        # TODO
        # self.RollAction = QAction("Roll")
        # self.RollAction.triggered.connect(self.RollActionTriggered)

        # TODO
        # self.RollPresetRollAction = QAction("Roll Preset Roll")
        # self.RollPresetRollAction.triggered.connect(self.RollPresetRollActionTriggered)

        # TODO
        # self.AverageRollAction = QAction("Average Roll")
        # self.AverageRollAction.triggered.connect(self.AverageRollActionTriggered)

        # TODO
        # self.AddLogEntryAction = QAction("Add Log Entry")
        # self.AddLogEntryAction.triggered.connect(self.AddLogEntryActionTriggered)

        # TODO
        # self.RemoveLastLogEntryAction = QAction("Remove Last Log Entry")
        # self.RemoveLastLogEntryAction.triggered.connect(self.RemoveLastLogEntryActionTriggered)

        # TODO
        # self.ClearLogAction = QAction("Clear Log")
        # self.ClearLogAction.triggered.connect(self.ClearLogActionTriggered)

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

        # TODO
        # self.ViewMenu = self.MenuBar.addMenu("View")
        # self.ViewMenu.addAction(self.CoinCalculatorAction)

        # TODO
        # self.NPCSettingsMenu = self.MenuBar.addMenu("NPC Settings")
        # self.NPCSettingsMenu.addAction(self.PortraitEnabledAction)
        # self.NPCSettingsMenu.addSeparator()
        # self.NPCSettingsMenu.addAction(self.SetCritMinimumAction)

        # TODO
        # self.RollerMenu = self.MenuBar.addMenu("Roller")
        # self.RollerMenu.addAction(self.RollAction)
        # self.RollerMenu.addAction(self.RollPresetRollAction)
        # self.RollerMenu.addAction(self.AverageRollAction)
        # self.RollerMenu.addSeparator()
        # self.RollerMenu.addAction(self.AddLogEntryAction)
        # self.RollerMenu.addAction(self.RemoveLastLogEntryAction)
        # self.RollerMenu.addAction(self.ClearLogAction)

    def CreateKeybindings(self):
        self.DefaultKeybindings = {}
        self.DefaultKeybindings["NewAction"] = "Ctrl+N"
        self.DefaultKeybindings["OpenAction"] = "Ctrl+O"
        self.DefaultKeybindings["SaveAction"] = "Ctrl+S"
        self.DefaultKeybindings["SaveAsAction"] = "Ctrl+Shift+S"
        self.DefaultKeybindings["QuitAction"] = "Ctrl+Q"

        # TODO
        # self.DefaultKeybindings["RollAction"] = "Ctrl+R"
        # self.DefaultKeybindings["RollPresetRollAction"] = "Ctrl+Shift+R"
        # self.DefaultKeybindings["AverageRollAction"] = "Ctrl+Alt+R"

    def LoadConfigs(self):
        # Keybindings
        KeybindingsFile = self.GetResourcePath("Configs/NPCKeybindings.cfg")
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
        with open(self.GetResourcePath("Configs/NPCKeybindings.cfg"), "w") as ConfigFile:
            ConfigFile.write(json.dumps(self.Keybindings, indent=2))

        # Last Opened Directory
        self.SaveLastOpenedDirectory()

        # Gzip Mode
        self.SaveGzipMode()

    # Save and Open Methods
    def NewActionTriggered(self):
        if self.New(self.NonPlayerCharacter):
            self.NonPlayerCharacter = NonPlayerCharacter()
        self.UpdatingFieldsFromNonPlayerCharacter = True
        self.UpdateDisplay()
        self.UpdatingFieldsFromNonPlayerCharacter = False

    def OpenActionTriggered(self):
        OpenData = self.Open(self.NonPlayerCharacter)
        if OpenData is not None:
            self.NonPlayerCharacter = OpenData
        self.UpdatingFieldsFromNonPlayerCharacter = True
        self.UpdateDisplay()
        self.UpdatingFieldsFromNonPlayerCharacter = False

    def SaveActionTriggered(self):
        self.Save(self.NonPlayerCharacter)
        self.UpdateDisplay()

    def SaveAsActionTriggered(self):
        self.Save(self.NonPlayerCharacter, SaveAs=True)
        self.UpdateDisplay()

    def ToggleGzipMode(self):
        self.GzipMode = not self.GzipMode

    def closeEvent(self, event):
        Close = True
        if self.UnsavedChanges:
            SavePrompt = self.DisplayMessageBox("Save unsaved changes before closing?", Icon=QMessageBox.Warning, Buttons=(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel))
            if SavePrompt == QMessageBox.Yes:
                if not self.Save(self.NonPlayerCharacter):
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
        self.DerivedStats = self.NonPlayerCharacter.GetDerivedStats()

        # TODO
        # # Proficiency Bonus
        # ProficiencyBonusText = "+" + str(self.DerivedStats["Proficiency Bonus"])
        # self.ProficiencyBonusLineEdit.setText(ProficiencyBonusText)

        # TODO
        # # Portrait Enabled
        # self.StatsTabWidget.setTabVisible(6, self.PlayerCharacter.Stats["Portrait Enabled"])
        # self.ViewPortraitTabAction.setEnabled(self.PlayerCharacter.Stats["Portrait Enabled"])

        # TODO
        # # Set Negative Current HP Indicator
        # Style = self.PlayerCharacterCombatAndFeaturesWidgetInst.HPSpinBoxStyle if self.PlayerCharacter.Stats["Current Health"] >= 0 else self.PlayerCharacterCombatAndFeaturesWidgetInst.NegativeCurrentHealthSpinBoxStyle
        # self.PlayerCharacterCombatAndFeaturesWidgetInst.CurrentHPSpinBox.setStyleSheet(Style)

        # TODO
        # # Portrait
        # self.PlayerCharacterPortraitWidgetInst.UpdateDisplay()

        # TODO
        # # Results Log
        # ResultsLogString = self.PlayerCharacter.Stats["Dice Roller"].CreateLogText()
        # self.DiceRollerWidget.ResultsLogTextEdit.setPlainText(ResultsLogString)

        # TODO
        # # Preset Rolls
        # CurrentSelection = self.DiceRollerWidget.PresetRollsTreeWidget.selectedItems()
        # if len(CurrentSelection) > 0:
        #     CurrentSelectionIndex = CurrentSelection[0].Index
        #     self.DiceRollerWidget.PresetRollsTreeWidget.FillFromPresetRolls()
        #     self.DiceRollerWidget.PresetRollsTreeWidget.SelectIndex(CurrentSelectionIndex)
        # else:
        #     self.DiceRollerWidget.PresetRollsTreeWidget.FillFromPresetRolls()

        # TODO
        # Updating Fields from Non-Player Character
        if self.UpdatingFieldsFromNonPlayerCharacter:
            pass

    def UpdateWindowTitle(self):
        CurrentFileTitleSection = " [" + os.path.basename(self.CurrentOpenFileName) + "]" if self.CurrentOpenFileName != "" else ""
        UnsavedChangesIndicator = " *" if self.UnsavedChanges else ""
        self.setWindowTitle(self.ScriptName + " NPC Sheet" + CurrentFileTitleSection + UnsavedChangesIndicator)
