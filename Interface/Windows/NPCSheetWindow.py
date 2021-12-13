import copy
import json
import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import QAction, QFrame, QInputDialog, QLabel, QMessageBox, QGridLayout, QTabWidget

from Core.DiceRoller import DiceRoller
from Core.NonPlayerCharacter import NonPlayerCharacter
from Interface.Dialogs.CoinCalculatorDialog import CoinCalculatorDialog
from Interface.Dialogs.EditPresetRollDialog import EditPresetRollDialog
from Interface.Widgets.CenteredLineEdit import CenteredLineEdit
from Interface.Widgets.CharacterPortraitWidget import CharacterPortraitWidget
from Interface.Widgets.DiceRollerWidget import DiceRollerWidget
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

        # Header
        self.NameLabel = QLabel("Name:")
        self.NameLineEdit = CenteredLineEdit()
        self.NameLineEdit.textChanged.connect(lambda: self.UpdateStat("NPC Name", self.NameLineEdit.text()))

        self.SizeLabel = QLabel("Size:")
        self.SizeLineEdit = CenteredLineEdit()
        self.SizeLineEdit.textChanged.connect(lambda: self.UpdateStat("Size", self.SizeLineEdit.text()))

        self.TypeAndTagsLabel = QLabel("Type and Tags:")
        self.TypeAndTagsLineEdit = CenteredLineEdit()
        self.TypeAndTagsLineEdit.textChanged.connect(lambda: self.UpdateStat("Type and Tags", self.TypeAndTagsLineEdit.text()))

        self.AlignmentLabel = QLabel("Alignment:")
        self.AlignmentLineEdit = CenteredLineEdit()
        self.AlignmentLineEdit.textChanged.connect(lambda: self.UpdateStat("Alignment", self.AlignmentLineEdit.text()))

        self.ProficiencyBonusLabel = QLabel("Proficiency Bonus:")
        self.ProficiencyBonusLineEdit = CenteredLineEdit()
        self.ProficiencyBonusLineEdit.setReadOnly(True)
        self.ProficiencyBonusLineEdit.setFocusPolicy(QtCore.Qt.NoFocus)

        # Tab Widget
        self.TabWidget = QTabWidget()
        self.TabWidget.setUsesScrollButtons(False)
        self.NonPlayerCharacterStatsWidgetInst = QFrame()
        self.TabWidget.addTab(self.NonPlayerCharacterStatsWidgetInst, "Stats")
        self.NonPlayerCharacterPortraitWidgetInst = CharacterPortraitWidget(self)
        self.TabWidget.addTab(self.NonPlayerCharacterPortraitWidgetInst, "Portrait")

        # Dice Roller
        self.DiceRollerWidget = DiceRollerWidget(self)

        # Create and Set Layout
        self.Layout = QGridLayout()

        self.HeaderFrame = QFrame()
        self.HeaderFrame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.HeaderLayout = QGridLayout()
        self.HeaderLayout.addWidget(self.NameLabel, 0, 0)
        self.HeaderLayout.addWidget(self.NameLineEdit, 0, 1)
        self.HeaderLayout.addWidget(self.SizeLabel, 0, 2)
        self.HeaderLayout.addWidget(self.SizeLineEdit, 0, 3)
        self.HeaderLayout.addWidget(self.TypeAndTagsLabel, 0, 4)
        self.HeaderLayout.addWidget(self.TypeAndTagsLineEdit, 0, 5)
        self.HeaderLayout.addWidget(self.AlignmentLabel, 0, 6)
        self.HeaderLayout.addWidget(self.AlignmentLineEdit, 0, 7)
        self.HeaderLayout.addWidget(self.ProficiencyBonusLabel, 0, 8)
        self.HeaderLayout.addWidget(self.ProficiencyBonusLineEdit, 0, 9)
        self.HeaderLayout.setColumnStretch(1, 2)
        for Column in [3, 5, 7]:
            self.HeaderLayout.setColumnStretch(Column, 1)
        self.HeaderFrame.setLayout(self.HeaderLayout)
        self.Layout.addWidget(self.HeaderFrame, 0, 0, 1, 2)

        self.StatsFrame = QFrame()
        self.StatsFrame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.StatsLayout = QGridLayout()
        self.StatsLayout.addWidget(self.TabWidget, 0, 0)
        self.StatsFrame.setLayout(self.StatsLayout)
        self.Layout.addWidget(self.StatsFrame, 1, 0)

        self.Layout.addWidget(self.DiceRollerWidget, 1, 1)

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

        self.SwitchTabAction = QAction("Switch Tab")
        self.SwitchTabAction.triggered.connect(self.SwitchTab)

        self.PortraitEnabledAction = QAction("Portrait Enabled")
        self.PortraitEnabledAction.setCheckable(True)
        self.PortraitEnabledAction.setChecked(True)
        self.PortraitEnabledAction.triggered.connect(self.TogglePortraitEnabled)

        self.SetCritMinimumAction = QAction("Set Crit Minimum")
        self.SetCritMinimumAction.triggered.connect(self.SetCritMinimumActionTriggered)

        self.RollAction = QAction("Roll")
        self.RollAction.triggered.connect(self.RollActionTriggered)

        self.RollPresetRollAction = QAction("Roll Preset Roll")
        self.RollPresetRollAction.triggered.connect(self.RollPresetRollActionTriggered)

        self.AverageRollAction = QAction("Average Roll")
        self.AverageRollAction.triggered.connect(self.AverageRollActionTriggered)

        self.AddLogEntryAction = QAction("Add Log Entry")
        self.AddLogEntryAction.triggered.connect(self.AddLogEntryActionTriggered)

        self.RemoveLastLogEntryAction = QAction("Remove Last Log Entry")
        self.RemoveLastLogEntryAction.triggered.connect(self.RemoveLastLogEntryActionTriggered)

        self.ClearLogAction = QAction("Clear Log")
        self.ClearLogAction.triggered.connect(self.ClearLogActionTriggered)

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

        self.ViewMenu = self.MenuBar.addMenu("View")
        self.ViewMenu.addAction(self.CoinCalculatorAction)
        self.ViewMenu.addSeparator()
        self.ViewMenu.addAction(self.SwitchTabAction)

        self.NPCSettingsMenu = self.MenuBar.addMenu("NPC Settings")
        self.NPCSettingsMenu.addAction(self.PortraitEnabledAction)
        self.NPCSettingsMenu.addSeparator()
        self.NPCSettingsMenu.addAction(self.SetCritMinimumAction)

        self.RollerMenu = self.MenuBar.addMenu("Roller")
        self.RollerMenu.addAction(self.RollAction)
        self.RollerMenu.addAction(self.RollPresetRollAction)
        self.RollerMenu.addAction(self.AverageRollAction)
        self.RollerMenu.addSeparator()
        self.RollerMenu.addAction(self.AddLogEntryAction)
        self.RollerMenu.addAction(self.RemoveLastLogEntryAction)
        self.RollerMenu.addAction(self.ClearLogAction)

    def CreateKeybindings(self):
        self.DefaultKeybindings = {}
        self.DefaultKeybindings["NewAction"] = "Ctrl+N"
        self.DefaultKeybindings["OpenAction"] = "Ctrl+O"
        self.DefaultKeybindings["SaveAction"] = "Ctrl+S"
        self.DefaultKeybindings["SaveAsAction"] = "Ctrl+Shift+S"
        self.DefaultKeybindings["QuitAction"] = "Ctrl+Q"
        self.DefaultKeybindings["RollAction"] = "Ctrl+R"
        self.DefaultKeybindings["RollPresetRollAction"] = "Ctrl+Shift+R"
        self.DefaultKeybindings["AverageRollAction"] = "Ctrl+Alt+R"

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

    # Non-Player Character Methods
    def GetCharacter(self):
        return self.NonPlayerCharacter

    def UpdateStat(self, Stat, NewValue):
        if not self.UpdatingFieldsFromNonPlayerCharacter:
            self.NonPlayerCharacter.UpdateStat(Stat, NewValue)
            self.UpdateUnsavedChangesFlag(True)

    def TogglePortraitEnabled(self):
        self.UpdateStat("Portrait Enabled", self.PortraitEnabledAction.isChecked())

    # Roller Methods
    def RollActionTriggered(self):
        DiceNumber = self.DiceRollerWidget.DiceNumberSpinBox.value()
        DieType = self.DiceRollerWidget.DieTypeSpinBox.value()
        Modifier = self.DiceRollerWidget.ModifierSpinBox.value()
        self.NonPlayerCharacter.Stats["Dice Roller"].RollDice(DiceNumber, DieType, Modifier)
        self.UpdateUnsavedChangesFlag(True)

    def RollPresetRollActionTriggered(self):
        CurrentSelection = self.DiceRollerWidget.PresetRollsTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentPresetRoll = CurrentSelection[0]
            CurrentPresetRollIndex = CurrentPresetRoll.Index
            self.NonPlayerCharacter.Stats["Dice Roller"].RollPresetRoll(CurrentPresetRollIndex)
            self.UpdateUnsavedChangesFlag(True)
            self.DiceRollerWidget.PresetRollsTreeWidget.SelectIndex(CurrentPresetRollIndex)

    def AverageRollActionTriggered(self):
        DiceNumber = self.DiceRollerWidget.DiceNumberSpinBox.value()
        DieType = self.DiceRollerWidget.DieTypeSpinBox.value()
        Modifier = self.DiceRollerWidget.ModifierSpinBox.value()
        AverageResult = self.NonPlayerCharacter.Stats["Dice Roller"].AverageRoll(DiceNumber, DieType, Modifier)
        AverageResultText = "The average result of " + str(DiceNumber) + "d" + str(DieType) + ("+" if Modifier >= 0 else "") + str(Modifier) + " is:\n\n" + str(AverageResult)
        self.DisplayMessageBox(AverageResultText)

    def SetCritMinimumActionTriggered(self):
        CritMin, OK = QInputDialog.getInt(self, "Set Crit Minimum", "Set crit minimum to:", self.NonPlayerCharacter.Stats["Crit Minimum"], 1, 20)
        if OK:
            self.UpdateStat("Crit Minimum", CritMin)

    def AddPresetRoll(self):
        PresetRollIndex = self.NonPlayerCharacter.Stats["Dice Roller"].AddPresetRoll()
        self.UpdateDisplay()
        EditPresetRollDialogInst = EditPresetRollDialog(self, self.NonPlayerCharacter.Stats["Dice Roller"], PresetRollIndex, AddMode=True)
        if EditPresetRollDialogInst.Cancelled:
            self.NonPlayerCharacter.Stats["Dice Roller"].DeleteLastPresetRoll()
            self.UpdateDisplay()
        else:
            self.UpdateUnsavedChangesFlag(True)
            self.DiceRollerWidget.PresetRollsTreeWidget.SelectIndex(PresetRollIndex)

    def DeletePresetRoll(self):
        CurrentSelection = self.DiceRollerWidget.PresetRollsTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            if self.DisplayMessageBox("Are you sure you want to delete this preset roll?  This cannot be undone.", Icon=QMessageBox.Warning, Buttons=(QMessageBox.Yes | QMessageBox.No)) == QMessageBox.Yes:
                CurrentPresetRoll = CurrentSelection[0]
                CurrentPresetRollIndex = CurrentPresetRoll.Index
                self.NonPlayerCharacter.Stats["Dice Roller"].DeletePresetRoll(CurrentPresetRollIndex)
                self.UpdateUnsavedChangesFlag(True)
                PresetRollsLength = len(self.NonPlayerCharacter.Stats["Dice Roller"].PresetRolls)
                if PresetRollsLength > 0:
                    self.DiceRollerWidget.PresetRollsTreeWidget.SelectIndex(CurrentPresetRollIndex if CurrentPresetRollIndex < PresetRollsLength else PresetRollsLength - 1)

    def EditPresetRoll(self):
        CurrentSelection = self.DiceRollerWidget.PresetRollsTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentPresetRoll = CurrentSelection[0]
            CurrentPresetRollIndex = CurrentPresetRoll.Index
            EditPresetRollDialogInst = EditPresetRollDialog(self, self.NonPlayerCharacter.Stats["Dice Roller"], CurrentPresetRollIndex)
            if EditPresetRollDialogInst.UnsavedChanges:
                self.UpdateUnsavedChangesFlag(True)
                self.DiceRollerWidget.PresetRollsTreeWidget.SelectIndex(CurrentPresetRollIndex)

    def CopyPresetRoll(self):
        CurrentSelection = self.DiceRollerWidget.PresetRollsTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentPresetRoll = CurrentSelection[0]
            CurrentPresetRollIndex = CurrentPresetRoll.Index
            NewPresetRollIndex = self.NonPlayerCharacter.Stats["Dice Roller"].CopyPresetRoll(CurrentPresetRollIndex)
            self.UpdateUnsavedChangesFlag(True)
            self.DiceRollerWidget.PresetRollsTreeWidget.SelectIndex(NewPresetRollIndex)

    def MovePresetRollUp(self):
        self.MovePresetRoll(-1)

    def MovePresetRollDown(self):
        self.MovePresetRoll(1)

    def MovePresetRoll(self, Delta):
        CurrentSelection = self.DiceRollerWidget.PresetRollsTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentPresetRoll = CurrentSelection[0]
            CurrentPresetRollIndex = CurrentPresetRoll.Index
            if self.NonPlayerCharacter.Stats["Dice Roller"].MovePresetRoll(CurrentPresetRollIndex, Delta):
                self.UpdateUnsavedChangesFlag(True)
                self.DiceRollerWidget.PresetRollsTreeWidget.SelectIndex(CurrentPresetRollIndex + Delta)

    def AddLogEntryActionTriggered(self):
        LogText, OK = QInputDialog.getText(self, "Add Log Entry", "Add text to log:")
        if OK:
            if LogText == "":
                self.DisplayMessageBox("Log entries cannot be blank.")
                return
            self.NonPlayerCharacter.Stats["Dice Roller"].AddLogEntry(LogText)
            self.UpdateUnsavedChangesFlag(True)

    def RemoveLastLogEntryActionTriggered(self):
        if self.DisplayMessageBox("Are you sure you want to remove the last log entry?  This cannot be undone.", Icon=QMessageBox.Warning, Buttons=(QMessageBox.Yes | QMessageBox.No)) == QMessageBox.Yes:
            self.NonPlayerCharacter.Stats["Dice Roller"].RemoveLastLogEntry()
            self.UpdateUnsavedChangesFlag(True)

    def ClearLogActionTriggered(self):
        if self.DisplayMessageBox("Are you sure you want to clear the log?  This cannot be undone.", Icon=QMessageBox.Warning, Buttons=(QMessageBox.Yes | QMessageBox.No)) == QMessageBox.Yes:
            self.NonPlayerCharacter.Stats["Dice Roller"].ClearLog()
            self.UpdateUnsavedChangesFlag(True)

    # View Methods
    def ShowCoinCalculator(self):
        CoinCalculatorDialog(self)

    # TODO
    def SwitchTab(self):
        pass

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

        # Proficiency Bonus
        ProficiencyBonusText = "+" + str(self.DerivedStats["Proficiency Bonus"])
        self.ProficiencyBonusLineEdit.setText(ProficiencyBonusText)

        # Portrait Enabled
        self.TabWidget.setTabVisible(1, self.NonPlayerCharacter.Stats["Portrait Enabled"])

        # TODO
        # # Set Negative Current HP Indicator
        # Style = self.NonPlayerCharacterCombatAndFeaturesWidgetInst.HPSpinBoxStyle if self.NonPlayerCharacter.Stats["Current Health"] >= 0 else self.NonPlayerCharacterCombatAndFeaturesWidgetInst.NegativeCurrentHealthSpinBoxStyle
        # self.NonPlayerCharacterCombatAndFeaturesWidgetInst.CurrentHPSpinBox.setStyleSheet(Style)

        # Portrait
        self.NonPlayerCharacterPortraitWidgetInst.UpdateDisplay()

        # Results Log
        ResultsLogString = self.NonPlayerCharacter.Stats["Dice Roller"].CreateLogText()
        self.DiceRollerWidget.ResultsLogTextEdit.setPlainText(ResultsLogString)

        # Preset Rolls
        CurrentSelection = self.DiceRollerWidget.PresetRollsTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentSelectionIndex = CurrentSelection[0].Index
            self.DiceRollerWidget.PresetRollsTreeWidget.FillFromPresetRolls()
            self.DiceRollerWidget.PresetRollsTreeWidget.SelectIndex(CurrentSelectionIndex)
        else:
            self.DiceRollerWidget.PresetRollsTreeWidget.FillFromPresetRolls()

        # TODO
        # Updating Fields from Non-Player Character
        if self.UpdatingFieldsFromNonPlayerCharacter:
            # Header
            self.NameLineEdit.setText(self.NonPlayerCharacter.Stats["NPC Name"])
            self.SizeLineEdit.setText(self.NonPlayerCharacter.Stats["Size"])
            self.TypeAndTagsLineEdit.setText(self.NonPlayerCharacter.Stats["Type and Tags"])
            self.AlignmentLineEdit.setText(self.NonPlayerCharacter.Stats["Alignment"])

    def UpdateWindowTitle(self):
        CurrentFileTitleSection = " [" + os.path.basename(self.CurrentOpenFileName) + "]" if self.CurrentOpenFileName != "" else ""
        UnsavedChangesIndicator = " *" if self.UnsavedChanges else ""
        self.setWindowTitle(self.ScriptName + " NPC Sheet" + CurrentFileTitleSection + UnsavedChangesIndicator)
