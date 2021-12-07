import copy
import json
import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import QFrame, QGridLayout, QInputDialog, QLabel, QSpinBox, QMessageBox, QAction, QTabWidget

from Core.PlayerCharacter import PlayerCharacter
from Core.DiceRoller import DiceRoller
from Interface.Dialogs.EditModifierDialog import EditModifierDialog
from Interface.Dialogs.EditPresetRollDialog import EditPresetRollDialog
from Interface.Widgets.CenteredLineEdit import CenteredLineEdit
from Interface.Widgets.DiceRollerWidget import DiceRollerWidget
from Interface.Widgets.PlayerCharacterAbilitiesAndSkillsWidget import PlayerCharacterAbilitiesAndSkillsWidget
from Interface.Widgets.PlayerCharacterCombatAndFeaturesWidget import PlayerCharacterCombatAndFeaturesWidget
from Interface.Widgets.PlayerCharacterInventoryWidget import PlayerCharacterInventoryWidget
from Interface.Widgets.PlayerCharacterSpellcastingWidget import PlayerCharacterSpellcastingWidget
from Interface.Widgets.ToggleButtons import InspirationButton
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
        self.UpdatingFieldsFromPlayerCharacter = False
        self.SavingThrowModifierLineEditStyleSheet = "QLineEdit {font-size: 16pt;}"
        self.SavingThrowProficiencyLineEditStyleSheet = "QLineEdit {font-size: 16pt; background-color: darkgreen;}"
        self.SavingThrowExpertiseLineEditStyleSheet = "QLineEdit {font-size: 16pt; background-color: darkgoldenrod;}"
        self.SkillModifierLineEditStyleSheet = "QLineEdit {}"
        self.SkillProficiencyLineEditStyleSheet = "QLineEdit {background-color: darkgreen;}"
        self.SkillExpertiseLineEditStyleSheet = "QLineEdit {background-color: darkgoldenrod;}"

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

        # Stats Tab Widget
        self.StatsTabWidget = QTabWidget()
        self.StatsTabWidget.setUsesScrollButtons(False)
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst = PlayerCharacterAbilitiesAndSkillsWidget(self)
        self.StatsTabWidget.addTab(self.PlayerCharacterAbilitiesAndSkillsWidgetInst, "Abilities and Skills")
        self.PlayerCharacterCombatAndFeaturesWidgetInst = PlayerCharacterCombatAndFeaturesWidget(self)
        self.StatsTabWidget.addTab(self.PlayerCharacterCombatAndFeaturesWidgetInst, "Combat and Features")
        self.PlayerCharacterSpellcastingWidgetInst = PlayerCharacterSpellcastingWidget(self)
        self.StatsTabWidget.addTab(self.PlayerCharacterSpellcastingWidgetInst, "Spellcasting")
        self.PlayerCharacterInventoryWidgetInst = PlayerCharacterInventoryWidget(self)
        self.StatsTabWidget.addTab(self.PlayerCharacterInventoryWidgetInst, "Inventory")
        # TODO:  Replace QFrames with widgets
        self.PlayerCharacterNotesWidgetInst = QFrame()
        self.StatsTabWidget.addTab(self.PlayerCharacterNotesWidgetInst, "Notes")
        self.PlayerCharacterPersonalityAndBackstoryWidgetInst = QFrame()
        self.StatsTabWidget.addTab(self.PlayerCharacterPersonalityAndBackstoryWidgetInst, "Personality and Backstory")
        self.PlayerCharacterPortraitWidgetInst = QFrame()
        self.StatsTabWidget.addTab(self.PlayerCharacterPortraitWidgetInst, "Portrait")

        # Dice Roller
        self.DiceRollerWidget = DiceRollerWidget(self)
        self.InspirationButton = InspirationButton(self)

        # Create and Set Layout
        self.Layout = QGridLayout()

        self.HeaderFrame = QFrame()
        self.HeaderFrame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.HeaderLayout = QGridLayout()
        self.HeaderLayout.addWidget(self.NameLabel, 0, 0)
        self.HeaderLayout.addWidget(self.NameLineEdit, 0, 1)
        self.HeaderLayout.addWidget(self.ClassLabel, 0, 2)
        self.HeaderLayout.addWidget(self.ClassLineEdit, 0, 3)
        self.HeaderLayout.addWidget(self.LevelLabel, 0, 4)
        self.HeaderLayout.addWidget(self.LevelSpinBox, 0, 5)
        self.HeaderLayout.addWidget(self.ProficiencyBonusLabel, 0, 6)
        self.HeaderLayout.addWidget(self.ProficiencyBonusLineEdit, 0, 7)
        self.HeaderLayout.addWidget(self.ExperienceLabel, 0, 8)
        self.HeaderLayout.addWidget(self.ExperienceSpinBox, 0, 9)
        self.HeaderLayout.addWidget(self.NeededExperienceLabel, 0, 10)
        self.HeaderLayout.addWidget(self.NeededExperienceLineEdit, 0, 11)
        for Column in [1, 3]:
            self.HeaderLayout.setColumnStretch(Column, 1)
        self.HeaderFrame.setLayout(self.HeaderLayout)

        self.StatsFrame = QFrame()
        self.StatsFrame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.StatsLayout = QGridLayout()
        self.StatsLayout.addWidget(self.StatsTabWidget, 0, 0)
        self.StatsFrame.setLayout(self.StatsLayout)

        self.DiceRollerFrame = QFrame()
        self.DiceRollerFrame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.DiceRollerLayout = QGridLayout()
        self.DiceRollerLayout.addWidget(self.DiceRollerWidget, 0, 0)
        self.DiceRollerLayout.addWidget(self.InspirationButton, 1, 0)
        self.DiceRollerFrame.setLayout(self.DiceRollerLayout)

        self.Layout.addWidget(self.HeaderFrame, 0, 0, 1, 2)
        self.Layout.addWidget(self.StatsFrame, 1, 0)
        self.Layout.addWidget(self.DiceRollerFrame, 1, 1)
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

        self.ViewPreviousTabAction = QAction("Previous Tab")
        self.ViewPreviousTabAction.triggered.connect(self.ViewPreviousTab)

        self.ViewNextTabAction = QAction("Next Tab")
        self.ViewNextTabAction.triggered.connect(self.ViewNextTab)

        self.ViewAbilitiesAndSkillsTabAction = QAction("Abilities and Skills Tab")
        self.ViewAbilitiesAndSkillsTabAction.triggered.connect(lambda: self.ViewTab(0))

        self.ViewCombatAndFeaturesTabAction = QAction("Combat and Features Tab")
        self.ViewCombatAndFeaturesTabAction.triggered.connect(lambda: self.ViewTab(1))

        self.ViewSpellcastingTabAction = QAction("Spellcasting Tab")
        self.ViewSpellcastingTabAction.triggered.connect(lambda: self.ViewTab(2))

        self.ViewInventoryTabAction = QAction("Inventory Tab")
        self.ViewInventoryTabAction.triggered.connect(lambda: self.ViewTab(3))

        self.ViewNotesTabAction = QAction("Notes Tab")
        self.ViewNotesTabAction.triggered.connect(lambda: self.ViewTab(4))

        self.ViewPersonalityAndBackstoryTabAction = QAction("Personality and Backstory Tab")
        self.ViewPersonalityAndBackstoryTabAction.triggered.connect(lambda: self.ViewTab(5))

        self.ViewPortraitTabAction = QAction("Portrait Tab")
        self.ViewPortraitTabAction.triggered.connect(lambda: self.ViewTab(6))

        self.SpellcastingEnabledAction = QAction("Spellcasting Enabled")
        self.SpellcastingEnabledAction.setCheckable(True)
        self.SpellcastingEnabledAction.setChecked(True)
        self.SpellcastingEnabledAction.triggered.connect(self.ToggleSpellcastingEnabled)

        self.ConcentrationCheckPromptEnabledAction = QAction("Concentration Check Prompt Enabled")
        self.ConcentrationCheckPromptEnabledAction.setCheckable(True)
        self.ConcentrationCheckPromptEnabledAction.setChecked(True)
        self.ConcentrationCheckPromptEnabledAction.triggered.connect(self.ToggleConcentrationCheckPromptEnabled)

        self.SpellPointsEnabledAction = QAction("Spell Points Enabled")
        self.SpellPointsEnabledAction.setCheckable(True)
        self.SpellPointsEnabledAction.setChecked(False)
        self.SpellPointsEnabledAction.triggered.connect(self.ToggleSpellPointsEnabled)

        self.PortraitEnabledAction = QAction("Portrait Enabled")
        self.PortraitEnabledAction.setCheckable(True)
        self.PortraitEnabledAction.setChecked(True)
        self.PortraitEnabledAction.triggered.connect(self.TogglePortraitEnabled)

        self.LuckyHalflingAction = QAction("Lucky Halfling")
        self.LuckyHalflingAction.setCheckable(True)
        self.LuckyHalflingAction.setChecked(False)
        self.LuckyHalflingAction.triggered.connect(self.ToggleLuckyHalfling)

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
        self.ViewMenu.addAction(self.ViewPreviousTabAction)
        self.ViewMenu.addAction(self.ViewNextTabAction)
        self.ViewMenu.addAction(self.ViewAbilitiesAndSkillsTabAction)
        self.ViewMenu.addAction(self.ViewCombatAndFeaturesTabAction)
        self.ViewMenu.addAction(self.ViewSpellcastingTabAction)
        self.ViewMenu.addAction(self.ViewInventoryTabAction)
        self.ViewMenu.addAction(self.ViewNotesTabAction)
        self.ViewMenu.addAction(self.ViewPersonalityAndBackstoryTabAction)
        self.ViewMenu.addAction(self.ViewPortraitTabAction)

        self.CharacterSettingsMenu = self.MenuBar.addMenu("Character Settings")
        self.CharacterSettingsMenu.addAction(self.SpellcastingEnabledAction)
        self.CharacterSettingsMenu.addAction(self.ConcentrationCheckPromptEnabledAction)
        self.CharacterSettingsMenu.addAction(self.SpellPointsEnabledAction)
        self.CharacterSettingsMenu.addAction(self.PortraitEnabledAction)
        self.CharacterSettingsMenu.addAction(self.LuckyHalflingAction)
        self.CharacterSettingsMenu.addSeparator()
        self.CharacterSettingsMenu.addAction(self.SetCritMinimumAction)

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
        self.DefaultKeybindings["ViewPreviousTabAction"] = "Ctrl+Shift+Tab"
        self.DefaultKeybindings["ViewNextTabAction"] = "Ctrl+Tab"
        self.DefaultKeybindings["ViewAbilitiesAndSkillsTabAction"] = "Ctrl+1"
        self.DefaultKeybindings["ViewCombatAndFeaturesTabAction"] = "Ctrl+2"
        self.DefaultKeybindings["ViewSpellcastingTabAction"] = "Ctrl+3"
        self.DefaultKeybindings["ViewInventoryTabAction"] = "Ctrl+4"
        self.DefaultKeybindings["ViewNotesTabAction"] = "Ctrl+5"
        self.DefaultKeybindings["ViewPersonalityAndBackstoryTabAction"] = "Ctrl+6"
        self.DefaultKeybindings["ViewPortraitTabAction"] = "Ctrl+7"
        self.DefaultKeybindings["RollAction"] = "Ctrl+R"
        self.DefaultKeybindings["RollPresetRollAction"] = "Ctrl+Shift+R"
        self.DefaultKeybindings["AverageRollAction"] = "Ctrl+Alt+R"

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
        if not self.UpdatingFieldsFromPlayerCharacter:
            self.PlayerCharacter.UpdateStat(Stat, NewValue)
            self.UpdateUnsavedChangesFlag(True)

    def EditStatModifier(self, ParentWidget, StatModifier, StatModifierDescription):
        EditModifierDialogInst = EditModifierDialog(ParentWidget, self, StatModifier, StatModifierDescription)
        if EditModifierDialogInst.UnsavedChanges:
            self.UpdateUnsavedChangesFlag(True)

    def ToggleSpellcastingEnabled(self):
        self.UpdateStat("Spellcasting Enabled", self.SpellcastingEnabledAction.isChecked())

    def ToggleConcentrationCheckPromptEnabled(self):
        self.UpdateStat("Enable Concentration Check", self.ConcentrationCheckPromptEnabledAction.isChecked())

    def ToggleSpellPointsEnabled(self):
        self.UpdateStat("Spell Points Enabled", self.SpellPointsEnabledAction.isChecked())

    def TogglePortraitEnabled(self):
        self.UpdateStat("Portrait Enabled", self.PortraitEnabledAction.isChecked())

    def ToggleLuckyHalfling(self):
        self.UpdateStat("Lucky Halfling", self.LuckyHalflingAction.isChecked())

    # Roller Methods
    def RollActionTriggered(self):
        DiceNumber = self.DiceRollerWidget.DiceNumberSpinBox.value()
        DieType = self.DiceRollerWidget.DieTypeSpinBox.value()
        Modifier = self.DiceRollerWidget.ModifierSpinBox.value()
        self.PlayerCharacter.Stats["Dice Roller"].RollDice(DiceNumber, DieType, Modifier)
        self.UpdateUnsavedChangesFlag(True)

    def RollPresetRollActionTriggered(self):
        CurrentSelection = self.DiceRollerWidget.PresetRollsTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentPresetRoll = CurrentSelection[0]
            CurrentPresetRollIndex = CurrentPresetRoll.Index
            self.PlayerCharacter.Stats["Dice Roller"].RollPresetRoll(CurrentPresetRollIndex)
            self.UpdateUnsavedChangesFlag(True)
            self.DiceRollerWidget.PresetRollsTreeWidget.SelectIndex(CurrentPresetRollIndex)

    def AverageRollActionTriggered(self):
        DiceNumber = self.DiceRollerWidget.DiceNumberSpinBox.value()
        DieType = self.DiceRollerWidget.DieTypeSpinBox.value()
        Modifier = self.DiceRollerWidget.ModifierSpinBox.value()
        AverageResult = self.PlayerCharacter.Stats["Dice Roller"].AverageRoll(DiceNumber, DieType, Modifier)
        AverageResultText = "The average result of " + str(DiceNumber) + "d" + str(DieType) + ("+" if Modifier >= 0 else "") + str(Modifier) + " is:\n\n" + str(AverageResult)
        self.DisplayMessageBox(AverageResultText)

    def SetCritMinimumActionTriggered(self):
        CritMin, OK = QInputDialog.getInt(self, "Set Crit Minimum", "Set crit minimum to:", self.PlayerCharacter.Stats["Crit Minimum"], 1, 20)
        if OK:
            self.UpdateStat("Crit Minimum", CritMin)

    def AddPresetRoll(self):
        PresetRollIndex = self.PlayerCharacter.Stats["Dice Roller"].AddPresetRoll()
        self.UpdateDisplay()
        EditPresetRollDialogInst = EditPresetRollDialog(self, self.PlayerCharacter.Stats["Dice Roller"], PresetRollIndex, AddMode=True)
        if EditPresetRollDialogInst.Cancelled:
            self.PlayerCharacter.Stats["Dice Roller"].DeleteLastPresetRoll()
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
                self.PlayerCharacter.Stats["Dice Roller"].DeletePresetRoll(CurrentPresetRollIndex)
                self.UpdateUnsavedChangesFlag(True)
                PresetRollsLength = len(self.PlayerCharacter.Stats["Dice Roller"].PresetRolls)
                if PresetRollsLength > 0:
                    self.DiceRollerWidget.PresetRollsTreeWidget.SelectIndex(CurrentPresetRollIndex if CurrentPresetRollIndex < PresetRollsLength else PresetRollsLength - 1)

    def EditPresetRoll(self):
        CurrentSelection = self.DiceRollerWidget.PresetRollsTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentPresetRoll = CurrentSelection[0]
            CurrentPresetRollIndex = CurrentPresetRoll.Index
            EditPresetRollDialogInst = EditPresetRollDialog(self, self.PlayerCharacter.Stats["Dice Roller"], CurrentPresetRollIndex)
            if EditPresetRollDialogInst.UnsavedChanges:
                self.UpdateUnsavedChangesFlag(True)
                self.DiceRollerWidget.PresetRollsTreeWidget.SelectIndex(CurrentPresetRollIndex)

    def CopyPresetRoll(self):
        CurrentSelection = self.DiceRollerWidget.PresetRollsTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentPresetRoll = CurrentSelection[0]
            CurrentPresetRollIndex = CurrentPresetRoll.Index
            NewPresetRollIndex = self.PlayerCharacter.Stats["Dice Roller"].CopyPresetRoll(CurrentPresetRollIndex)
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
            if self.PlayerCharacter.Stats["Dice Roller"].MovePresetRoll(CurrentPresetRollIndex, Delta):
                self.UpdateUnsavedChangesFlag(True)
                self.DiceRollerWidget.PresetRollsTreeWidget.SelectIndex(CurrentPresetRollIndex + Delta)

    def AddLogEntryActionTriggered(self):
        LogText, OK = QInputDialog.getText(self, "Add Log Entry", "Add text to log:")
        if OK:
            if LogText == "":
                self.DisplayMessageBox("Log entries cannot be blank.")
                return
            self.PlayerCharacter.Stats["Dice Roller"].AddLogEntry(LogText)
            self.UpdateUnsavedChangesFlag(True)

    def RemoveLastLogEntryActionTriggered(self):
        if self.DisplayMessageBox("Are you sure you want to remove the last log entry?  This cannot be undone.", Icon=QMessageBox.Warning, Buttons=(QMessageBox.Yes | QMessageBox.No)) == QMessageBox.Yes:
            self.PlayerCharacter.Stats["Dice Roller"].RemoveLastLogEntry()
            self.UpdateUnsavedChangesFlag(True)

    def ClearLogActionTriggered(self):
        if self.DisplayMessageBox("Are you sure you want to clear the log?  This cannot be undone.", Icon=QMessageBox.Warning, Buttons=(QMessageBox.Yes | QMessageBox.No)) == QMessageBox.Yes:
            self.PlayerCharacter.Stats["Dice Roller"].ClearLog()
            self.UpdateUnsavedChangesFlag(True)

    # View Methods
    def ViewTab(self, Index):
        self.StatsTabWidget.setCurrentIndex(Index)

    def ViewPreviousTab(self):
        CurrentIndex = self.StatsTabWidget.currentIndex()
        LastIndex = self.StatsTabWidget.count() - 1
        if CurrentIndex == 0:
            TargetIndex = LastIndex
        else:
            TargetIndex = CurrentIndex - 1
        if TargetIndex == 2 and not self.PlayerCharacter.Stats["Spellcasting Enabled"]:
            TargetIndex = 1
        if TargetIndex == 6 and not self.PlayerCharacter.Stats["Portrait Enabled"]:
            TargetIndex = 5
        self.ViewTab(TargetIndex)

    def ViewNextTab(self):
        CurrentIndex = self.StatsTabWidget.currentIndex()
        LastIndex = self.StatsTabWidget.count() - 1
        if CurrentIndex == LastIndex:
            TargetIndex = 0
        else:
            TargetIndex = CurrentIndex + 1
        if TargetIndex == 2 and not self.PlayerCharacter.Stats["Spellcasting Enabled"]:
            TargetIndex = 3
        if TargetIndex == 6 and not self.PlayerCharacter.Stats["Portrait Enabled"]:
            TargetIndex = 0
        self.ViewTab(TargetIndex)

    # Save and Open Methods
    def NewActionTriggered(self):
        if self.New(self.PlayerCharacter):
            self.PlayerCharacter = PlayerCharacter()
        self.UpdatingFieldsFromPlayerCharacter = True
        self.UpdateDisplay()
        self.UpdatingFieldsFromPlayerCharacter = False

    def OpenActionTriggered(self):
        OpenData = self.Open(self.PlayerCharacter)
        if OpenData is not None:
            self.PlayerCharacter = OpenData
        self.UpdatingFieldsFromPlayerCharacter = True
        self.UpdateDisplay()
        self.UpdatingFieldsFromPlayerCharacter = False

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

        # Spellcasting Enabled
        self.StatsTabWidget.setTabVisible(2, self.PlayerCharacter.Stats["Spellcasting Enabled"])
        self.ViewSpellcastingTabAction.setEnabled(self.PlayerCharacter.Stats["Spellcasting Enabled"])

        # Spell Points Enabled
        self.PlayerCharacterSpellcastingWidgetInst.SetSpellPointsEnabled(self.PlayerCharacter.Stats["Spell Points Enabled"])

        # Portrait Enabled
        self.StatsTabWidget.setTabVisible(6, self.PlayerCharacter.Stats["Portrait Enabled"])
        self.ViewPortraitTabAction.setEnabled(self.PlayerCharacter.Stats["Portrait Enabled"])

        # Abilities and Saving Throws
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.StrengthTotalLineEdit.setText(str(self.DerivedStats["Strength Total Score"]))
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.StrengthModifierLineEdit.setText(("+" if self.DerivedStats["Strength Modifier"] >= 0 else "") + str(self.DerivedStats["Strength Modifier"]))
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.StrengthSavingThrowLineEdit.setText(("+" if self.DerivedStats["Strength Saving Throw Modifier"] >= 0 else "") + str(self.DerivedStats["Strength Saving Throw Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.StrengthSavingThrowLineEdit, self.PlayerCharacter.Stats["Ability Scores"]["Strength Save Stat Modifier"])
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.DexterityTotalLineEdit.setText(str(self.DerivedStats["Dexterity Total Score"]))
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.DexterityModifierLineEdit.setText(("+" if self.DerivedStats["Dexterity Modifier"] >= 0 else "") + str(self.DerivedStats["Dexterity Modifier"]))
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.DexteritySavingThrowLineEdit.setText(("+" if self.DerivedStats["Dexterity Saving Throw Modifier"] >= 0 else "") + str(self.DerivedStats["Dexterity Saving Throw Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.DexteritySavingThrowLineEdit, self.PlayerCharacter.Stats["Ability Scores"]["Dexterity Save Stat Modifier"])
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.ConstitutionTotalLineEdit.setText(str(self.DerivedStats["Constitution Total Score"]))
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.ConstitutionModifierLineEdit.setText(("+" if self.DerivedStats["Constitution Modifier"] >= 0 else "") + str(self.DerivedStats["Constitution Modifier"]))
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.ConstitutionSavingThrowLineEdit.setText(("+" if self.DerivedStats["Constitution Saving Throw Modifier"] >= 0 else "") + str(self.DerivedStats["Constitution Saving Throw Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.ConstitutionSavingThrowLineEdit, self.PlayerCharacter.Stats["Ability Scores"]["Constitution Save Stat Modifier"])
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.IntelligenceTotalLineEdit.setText(str(self.DerivedStats["Intelligence Total Score"]))
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.IntelligenceModifierLineEdit.setText(("+" if self.DerivedStats["Intelligence Modifier"] >= 0 else "") + str(self.DerivedStats["Intelligence Modifier"]))
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.IntelligenceSavingThrowLineEdit.setText(("+" if self.DerivedStats["Intelligence Saving Throw Modifier"] >= 0 else "") + str(self.DerivedStats["Intelligence Saving Throw Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.IntelligenceSavingThrowLineEdit, self.PlayerCharacter.Stats["Ability Scores"]["Intelligence Save Stat Modifier"])
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.WisdomTotalLineEdit.setText(str(self.DerivedStats["Wisdom Total Score"]))
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.WisdomModifierLineEdit.setText(("+" if self.DerivedStats["Wisdom Modifier"] >= 0 else "") + str(self.DerivedStats["Wisdom Modifier"]))
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.WisdomSavingThrowLineEdit.setText(("+" if self.DerivedStats["Wisdom Saving Throw Modifier"] >= 0 else "") + str(self.DerivedStats["Wisdom Saving Throw Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.WisdomSavingThrowLineEdit, self.PlayerCharacter.Stats["Ability Scores"]["Wisdom Save Stat Modifier"])
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.CharismaTotalLineEdit.setText(str(self.DerivedStats["Charisma Total Score"]))
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.CharismaModifierLineEdit.setText(("+" if self.DerivedStats["Charisma Modifier"] >= 0 else "") + str(self.DerivedStats["Charisma Modifier"]))
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.CharismaSavingThrowLineEdit.setText(("+" if self.DerivedStats["Charisma Saving Throw Modifier"] >= 0 else "") + str(self.DerivedStats["Charisma Saving Throw Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.CharismaSavingThrowLineEdit, self.PlayerCharacter.Stats["Ability Scores"]["Charisma Save Stat Modifier"])

        # Skills
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.AcrobaticsModifierLineEdit.setText(("+" if self.DerivedStats["Acrobatics Modifier"] >= 0 else "") + str(self.DerivedStats["Acrobatics Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.AcrobaticsModifierLineEdit, self.PlayerCharacter.Stats["Skills"]["Acrobatics Stat Modifier"])
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.AnimalHandlingModifierLineEdit.setText(("+" if self.DerivedStats["Animal Handling Modifier"] >= 0 else "") + str(self.DerivedStats["Animal Handling Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.AnimalHandlingModifierLineEdit, self.PlayerCharacter.Stats["Skills"]["Animal Handling Stat Modifier"])
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.ArcanaModifierLineEdit.setText(("+" if self.DerivedStats["Arcana Modifier"] >= 0 else "") + str(self.DerivedStats["Arcana Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.ArcanaModifierLineEdit, self.PlayerCharacter.Stats["Skills"]["Arcana Stat Modifier"])
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.AthleticsModifierLineEdit.setText(("+" if self.DerivedStats["Athletics Modifier"] >= 0 else "") + str(self.DerivedStats["Athletics Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.AthleticsModifierLineEdit, self.PlayerCharacter.Stats["Skills"]["Athletics Stat Modifier"])
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.DeceptionModifierLineEdit.setText(("+" if self.DerivedStats["Deception Modifier"] >= 0 else "") + str(self.DerivedStats["Deception Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.DeceptionModifierLineEdit, self.PlayerCharacter.Stats["Skills"]["Deception Stat Modifier"])
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.HistoryModifierLineEdit.setText(("+" if self.DerivedStats["History Modifier"] >= 0 else "") + str(self.DerivedStats["History Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.HistoryModifierLineEdit, self.PlayerCharacter.Stats["Skills"]["History Stat Modifier"])
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.InsightModifierLineEdit.setText(("+" if self.DerivedStats["Insight Modifier"] >= 0 else "") + str(self.DerivedStats["Insight Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.InsightModifierLineEdit, self.PlayerCharacter.Stats["Skills"]["Insight Stat Modifier"])
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.IntimidationModifierLineEdit.setText(("+" if self.DerivedStats["Intimidation Modifier"] >= 0 else "") + str(self.DerivedStats["Intimidation Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.IntimidationModifierLineEdit, self.PlayerCharacter.Stats["Skills"]["Intimidation Stat Modifier"])
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.InvestigationModifierLineEdit.setText(("+" if self.DerivedStats["Investigation Modifier"] >= 0 else "") + str(self.DerivedStats["Investigation Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.InvestigationModifierLineEdit, self.PlayerCharacter.Stats["Skills"]["Investigation Stat Modifier"])
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.MedicineModifierLineEdit.setText(("+" if self.DerivedStats["Medicine Modifier"] >= 0 else "") + str(self.DerivedStats["Medicine Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.MedicineModifierLineEdit, self.PlayerCharacter.Stats["Skills"]["Medicine Stat Modifier"])
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.NatureModifierLineEdit.setText(("+" if self.DerivedStats["Nature Modifier"] >= 0 else "") + str(self.DerivedStats["Nature Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.NatureModifierLineEdit, self.PlayerCharacter.Stats["Skills"]["Nature Stat Modifier"])
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.PerceptionModifierLineEdit.setText(("+" if self.DerivedStats["Perception Modifier"] >= 0 else "") + str(self.DerivedStats["Perception Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.PerceptionModifierLineEdit, self.PlayerCharacter.Stats["Skills"]["Perception Stat Modifier"])
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.PerformanceModifierLineEdit.setText(("+" if self.DerivedStats["Performance Modifier"] >= 0 else "") + str(self.DerivedStats["Performance Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.PerformanceModifierLineEdit, self.PlayerCharacter.Stats["Skills"]["Performance Stat Modifier"])
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.PersuasionModifierLineEdit.setText(("+" if self.DerivedStats["Persuasion Modifier"] >= 0 else "") + str(self.DerivedStats["Persuasion Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.PersuasionModifierLineEdit, self.PlayerCharacter.Stats["Skills"]["Persuasion Stat Modifier"])
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.ReligionModifierLineEdit.setText(("+" if self.DerivedStats["Religion Modifier"] >= 0 else "") + str(self.DerivedStats["Religion Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.ReligionModifierLineEdit, self.PlayerCharacter.Stats["Skills"]["Religion Stat Modifier"])
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.SleightOfHandModifierLineEdit.setText(("+" if self.DerivedStats["Sleight of Hand Modifier"] >= 0 else "") + str(self.DerivedStats["Sleight of Hand Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.SleightOfHandModifierLineEdit, self.PlayerCharacter.Stats["Skills"]["Sleight of Hand Stat Modifier"])
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.StealthModifierLineEdit.setText(("+" if self.DerivedStats["Stealth Modifier"] >= 0 else "") + str(self.DerivedStats["Stealth Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.StealthModifierLineEdit, self.PlayerCharacter.Stats["Skills"]["Stealth Stat Modifier"])
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.SurvivalModifierLineEdit.setText(("+" if self.DerivedStats["Survival Modifier"] >= 0 else "") + str(self.DerivedStats["Survival Modifier"]))
        self.SetProficiencyIndicators(self.PlayerCharacterAbilitiesAndSkillsWidgetInst.SurvivalModifierLineEdit, self.PlayerCharacter.Stats["Skills"]["Survival Stat Modifier"])

        # Passive Scores
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.PassivePerceptionLineEdit.setText(str(self.DerivedStats["Passive Perception"]))
        self.PlayerCharacterAbilitiesAndSkillsWidgetInst.PassiveInvestigationLineEdit.setText(str(self.DerivedStats["Passive Investigation"]))

        # Set Negative Current HP Indicator
        Style = self.PlayerCharacterCombatAndFeaturesWidgetInst.HPSpinBoxStyle if self.PlayerCharacter.Stats["Current Health"] >= 0 else self.PlayerCharacterCombatAndFeaturesWidgetInst.NegativeCurrentHealthSpinBoxStyle
        self.PlayerCharacterCombatAndFeaturesWidgetInst.CurrentHPSpinBox.setStyleSheet(Style)

        # Max HP
        self.PlayerCharacterCombatAndFeaturesWidgetInst.MaxHPSpinBox.setValue(self.DerivedStats["Max Health"])

        # AC
        self.PlayerCharacterCombatAndFeaturesWidgetInst.AC1SpinBox.setValue(self.DerivedStats["AC 1"])
        self.PlayerCharacterCombatAndFeaturesWidgetInst.AC2SpinBox.setValue(self.DerivedStats["AC 2"])
        self.PlayerCharacterCombatAndFeaturesWidgetInst.AC3SpinBox.setValue(self.DerivedStats["AC 3"])

        # Initiative
        self.PlayerCharacterCombatAndFeaturesWidgetInst.InitiativeSpinBox.setValue(self.DerivedStats["Initiative Modifier"])

        # Ability Score Derivatives
        for AbilityScoreDerivativeWidget in [self.PlayerCharacterCombatAndFeaturesWidgetInst.AbilityScoreDerivativeWidgetInst1, self.PlayerCharacterCombatAndFeaturesWidgetInst.AbilityScoreDerivativeWidgetInst2, self.PlayerCharacterCombatAndFeaturesWidgetInst.AbilityScoreDerivativeWidgetInst3, self.PlayerCharacterSpellcastingWidgetInst.SpellcastingAbilityWidgetInst1, self.PlayerCharacterSpellcastingWidgetInst.SpellcastingAbilityWidgetInst2, self.PlayerCharacterSpellcastingWidgetInst.SpellcastingAbilityWidgetInst3]:
            Ability = self.PlayerCharacter.Stats["Ability Score Derivatives"]["Ability Score Derivatives Displayed"][AbilityScoreDerivativeWidget.Index]
            if Ability == "":
                AbilityScoreDerivativeWidget.SaveDCLineEdit.setText("N/A")
                AbilityScoreDerivativeWidget.SaveDCLineEdit.setStyleSheet(self.SkillModifierLineEditStyleSheet)
                AbilityScoreDerivativeWidget.AttackModifierLineEdit.setText("N/A")
                AbilityScoreDerivativeWidget.AttackModifierLineEdit.setStyleSheet(self.SkillModifierLineEditStyleSheet)
            else:
                AbilityScoreDerivativeWidget.SaveDCLineEdit.setText(str(self.DerivedStats[Ability + " Save DC Stat Modifier"]))
                AbilityScoreDerivativeWidget.AttackModifierLineEdit.setText(("+" if self.DerivedStats[Ability + " Attack Modifier Stat Modifier"] >= 0 else "") + str(self.DerivedStats[Ability + " Attack Modifier Stat Modifier"]))
                self.SetProficiencyIndicators(AbilityScoreDerivativeWidget.AttackModifierLineEdit, self.PlayerCharacter.Stats["Ability Score Derivatives"][Ability + " Attack Modifier Stat Modifier"])

        # Features
        CurrentSelection = self.PlayerCharacterCombatAndFeaturesWidgetInst.FeaturesTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentSelectionIndex = CurrentSelection[0].Index
            self.PlayerCharacterCombatAndFeaturesWidgetInst.FeaturesTreeWidget.FillFromFeatures()
            self.PlayerCharacterCombatAndFeaturesWidgetInst.FeaturesTreeWidget.SelectIndex(CurrentSelectionIndex)
        else:
            self.PlayerCharacterCombatAndFeaturesWidgetInst.FeaturesTreeWidget.FillFromFeatures()

        # Spell Points Calculation
        if self.DerivedStats["Max Spell Points"] is not None:
            self.PlayerCharacterSpellcastingWidgetInst.SpellPointsMaxSpinBox.setValue(self.DerivedStats["Max Spell Points"])
            self.PlayerCharacterSpellcastingWidgetInst.SpellPointsMaxSpinBox.setSpecialValueText("")
        else:
            self.PlayerCharacterSpellcastingWidgetInst.SpellPointsMaxSpinBox.setValue(0)
            self.PlayerCharacterSpellcastingWidgetInst.SpellPointsMaxSpinBox.setSpecialValueText("N/A")

        # Spell List
        CurrentSelection = self.PlayerCharacterSpellcastingWidgetInst.SpellListTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentSelectionIndex = CurrentSelection[0].Index
            self.PlayerCharacterSpellcastingWidgetInst.SpellListTreeWidget.FillFromSpellList()
            self.PlayerCharacterSpellcastingWidgetInst.SpellListTreeWidget.SelectIndex(CurrentSelectionIndex)
        else:
            self.PlayerCharacterSpellcastingWidgetInst.SpellListTreeWidget.FillFromSpellList()

        # Carrying Capacity
        self.PlayerCharacterInventoryWidgetInst.CarryingCapacitySpinBox.setValue(self.DerivedStats["Carrying Capacity"])

        # Loads and Values
        self.PlayerCharacterInventoryWidgetInst.TotalLoadSpinBox.setValue(self.DerivedStats["Item Loads"]["Total"])
        self.PlayerCharacterInventoryWidgetInst.GearLoadSpinBox.setValue(self.DerivedStats["Item Loads"]["Gear"])
        self.PlayerCharacterInventoryWidgetInst.TreasureLoadSpinBox.setValue(self.DerivedStats["Item Loads"]["Treasure"])
        self.PlayerCharacterInventoryWidgetInst.MiscLoadSpinBox.setValue(self.DerivedStats["Item Loads"]["Misc."])
        self.PlayerCharacterInventoryWidgetInst.TotalValueSpinBox.setValue(self.DerivedStats["Item Values"]["Total"])
        self.PlayerCharacterInventoryWidgetInst.GearValueSpinBox.setValue(self.DerivedStats["Item Values"]["Gear"])
        self.PlayerCharacterInventoryWidgetInst.TreasureValueSpinBox.setValue(self.DerivedStats["Item Values"]["Treasure"])
        self.PlayerCharacterInventoryWidgetInst.MiscValueSpinBox.setValue(self.DerivedStats["Item Values"]["Misc."])
        if self.DerivedStats["Item Loads"]["Total"] > self.DerivedStats["Carrying Capacity"]:
            self.PlayerCharacterInventoryWidgetInst.TotalLoadSpinBox.setStyleSheet(self.PlayerCharacterInventoryWidgetInst.TotalLoadsEncumberedStyle)
        else:
            self.PlayerCharacterInventoryWidgetInst.TotalLoadSpinBox.setStyleSheet(self.PlayerCharacterInventoryWidgetInst.TotalLoadsStyle)
        self.PlayerCharacterInventoryWidgetInst.CoinValueSpinBox.setValue(self.DerivedStats["Value of Coins"])
        self.PlayerCharacterInventoryWidgetInst.CoinLoadSpinBox.setValue(self.DerivedStats["Load of Coins"])

        # Food and Water
        self.PlayerCharacterInventoryWidgetInst.FoodLoadSpinBox.setValue(self.DerivedStats["Item Loads"]["Food"])
        self.PlayerCharacterInventoryWidgetInst.FoodDaysSpinBox.setValue(self.DerivedStats["Days of Food"])
        self.PlayerCharacterInventoryWidgetInst.WaterLoadSpinBox.setValue(self.DerivedStats["Item Loads"]["Water"])
        self.PlayerCharacterInventoryWidgetInst.WaterDaysSpinBox.setValue(self.DerivedStats["Days of Water"])

        # Results Log
        ResultsLogString = self.PlayerCharacter.Stats["Dice Roller"].CreateLogText()
        self.DiceRollerWidget.ResultsLogTextEdit.setPlainText(ResultsLogString)

        # Preset Rolls
        CurrentSelection = self.DiceRollerWidget.PresetRollsTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentSelectionIndex = CurrentSelection[0].Index
            self.DiceRollerWidget.PresetRollsTreeWidget.FillFromPresetRolls()
            self.DiceRollerWidget.PresetRollsTreeWidget.SelectIndex(CurrentSelectionIndex)
        else:
            self.DiceRollerWidget.PresetRollsTreeWidget.FillFromPresetRolls()

        # Updating Fields from Player Character
        if self.UpdatingFieldsFromPlayerCharacter:
            # Header
            self.NameLineEdit.setText(self.PlayerCharacter.Stats["Character Name"])
            self.ClassLineEdit.setText(self.PlayerCharacter.Stats["Character Class"])
            self.LevelSpinBox.setValue(self.PlayerCharacter.Stats["Character Level"])
            self.ExperienceSpinBox.setValue(self.PlayerCharacter.Stats["Character Experience Earned"])

            # Proficiencies
            self.PlayerCharacterAbilitiesAndSkillsWidgetInst.WeaponsProficiencesTextEdit.setPlainText(self.PlayerCharacter.Stats["Weapons Proficiencies"])
            self.PlayerCharacterAbilitiesAndSkillsWidgetInst.ArmorProficiencesTextEdit.setPlainText(self.PlayerCharacter.Stats["Armor Proficiencies"])
            self.PlayerCharacterAbilitiesAndSkillsWidgetInst.ToolsAndInstrumentsProficiencesTextEdit.setPlainText(self.PlayerCharacter.Stats["Tools and Instruments Proficiencies"])
            self.PlayerCharacterAbilitiesAndSkillsWidgetInst.LanguagesProficiencesTextEdit.setPlainText(self.PlayerCharacter.Stats["Languages Proficiencies"])
            self.PlayerCharacterAbilitiesAndSkillsWidgetInst.OtherProficiencesTextEdit.setPlainText(self.PlayerCharacter.Stats["Other Proficiencies"])

            # Vitality
            self.PlayerCharacterCombatAndFeaturesWidgetInst.TempHPSpinBox.setValue(self.PlayerCharacter.Stats["Temp Health"])
            self.PlayerCharacterCombatAndFeaturesWidgetInst.CurrentHPSpinBox.setValue(self.PlayerCharacter.Stats["Current Health"])
            self.PlayerCharacterCombatAndFeaturesWidgetInst.TotalHitDiceLineEdit.setText(self.PlayerCharacter.Stats["Total Hit Dice"])
            self.PlayerCharacterCombatAndFeaturesWidgetInst.HitDiceRemainingLineEdit.setText(self.PlayerCharacter.Stats["Hit Dice Remaining"])
            self.PlayerCharacterCombatAndFeaturesWidgetInst.DeathSavingThrowsSuccessCheckBoxOne.setChecked(self.PlayerCharacter.Stats["Death Saving Throws"]["Success 1"])
            self.PlayerCharacterCombatAndFeaturesWidgetInst.DeathSavingThrowsSuccessCheckBoxTwo.setChecked(self.PlayerCharacter.Stats["Death Saving Throws"]["Success 2"])
            self.PlayerCharacterCombatAndFeaturesWidgetInst.DeathSavingThrowsSuccessCheckBoxThree.setChecked(self.PlayerCharacter.Stats["Death Saving Throws"]["Success 3"])
            self.PlayerCharacterCombatAndFeaturesWidgetInst.DeathSavingThrowsFailureCheckBoxOne.setChecked(self.PlayerCharacter.Stats["Death Saving Throws"]["Failure 1"])
            self.PlayerCharacterCombatAndFeaturesWidgetInst.DeathSavingThrowsFailureCheckBoxTwo.setChecked(self.PlayerCharacter.Stats["Death Saving Throws"]["Failure 2"])
            self.PlayerCharacterCombatAndFeaturesWidgetInst.DeathSavingThrowsFailureCheckBoxThree.setChecked(self.PlayerCharacter.Stats["Death Saving Throws"]["Failure 3"])

            # Speed
            self.PlayerCharacterCombatAndFeaturesWidgetInst.SpeedSpinBox.setValue(self.PlayerCharacter.Stats["Speed"])

            # Ability Score Derivatives
            for AbilityScoreDerivativeWidget in [self.PlayerCharacterCombatAndFeaturesWidgetInst.AbilityScoreDerivativeWidgetInst1, self.PlayerCharacterCombatAndFeaturesWidgetInst.AbilityScoreDerivativeWidgetInst2, self.PlayerCharacterCombatAndFeaturesWidgetInst.AbilityScoreDerivativeWidgetInst3, self.PlayerCharacterSpellcastingWidgetInst.SpellcastingAbilityWidgetInst1, self.PlayerCharacterSpellcastingWidgetInst.SpellcastingAbilityWidgetInst2, self.PlayerCharacterSpellcastingWidgetInst.SpellcastingAbilityWidgetInst3]:
                AbilityScoreDerivativeWidget.AbilityComboBox.setCurrentText(self.PlayerCharacter.Stats["Ability Score Derivatives"]["Ability Score Derivatives Displayed"][AbilityScoreDerivativeWidget.Index])

            # Combat and Features Notes
            self.PlayerCharacterCombatAndFeaturesWidgetInst.CombatAndFeaturesNotesTextEdit.setPlainText(self.PlayerCharacter.Stats["Combat and Features Notes"])

            # Concentrating
            self.PlayerCharacterSpellcastingWidgetInst.ConcentratingButton.setChecked(self.PlayerCharacter.Stats["Concentrating"])

            # Spell Notes
            self.PlayerCharacterSpellcastingWidgetInst.SpellNotesTextEdit.setPlainText(self.PlayerCharacter.Stats["Spell Notes"])

            # Spell Slots
            self.PlayerCharacterSpellcastingWidgetInst.SpellSlotsTotalSlots1stSpinBox.setValue(self.PlayerCharacter.Stats["Spell Slots"]["1st"]["Total Slots"])
            self.PlayerCharacterSpellcastingWidgetInst.SpellSlotsTotalSlots2ndSpinBox.setValue(self.PlayerCharacter.Stats["Spell Slots"]["2nd"]["Total Slots"])
            self.PlayerCharacterSpellcastingWidgetInst.SpellSlotsTotalSlots3rdSpinBox.setValue(self.PlayerCharacter.Stats["Spell Slots"]["3rd"]["Total Slots"])
            self.PlayerCharacterSpellcastingWidgetInst.SpellSlotsTotalSlots4thSpinBox.setValue(self.PlayerCharacter.Stats["Spell Slots"]["4th"]["Total Slots"])
            self.PlayerCharacterSpellcastingWidgetInst.SpellSlotsTotalSlots5thSpinBox.setValue(self.PlayerCharacter.Stats["Spell Slots"]["5th"]["Total Slots"])
            self.PlayerCharacterSpellcastingWidgetInst.SpellSlotsTotalSlots6thSpinBox.setValue(self.PlayerCharacter.Stats["Spell Slots"]["6th"]["Total Slots"])
            self.PlayerCharacterSpellcastingWidgetInst.SpellSlotsTotalSlots7thSpinBox.setValue(self.PlayerCharacter.Stats["Spell Slots"]["7th"]["Total Slots"])
            self.PlayerCharacterSpellcastingWidgetInst.SpellSlotsTotalSlots8thSpinBox.setValue(self.PlayerCharacter.Stats["Spell Slots"]["8th"]["Total Slots"])
            self.PlayerCharacterSpellcastingWidgetInst.SpellSlotsTotalSlots9thSpinBox.setValue(self.PlayerCharacter.Stats["Spell Slots"]["9th"]["Total Slots"])
            self.PlayerCharacterSpellcastingWidgetInst.SpellSlotsUsedSlots1stSpinBox.setValue(self.PlayerCharacter.Stats["Spell Slots"]["1st"]["Used Slots"])
            self.PlayerCharacterSpellcastingWidgetInst.SpellSlotsUsedSlots2ndSpinBox.setValue(self.PlayerCharacter.Stats["Spell Slots"]["2nd"]["Used Slots"])
            self.PlayerCharacterSpellcastingWidgetInst.SpellSlotsUsedSlots3rdSpinBox.setValue(self.PlayerCharacter.Stats["Spell Slots"]["3rd"]["Used Slots"])
            self.PlayerCharacterSpellcastingWidgetInst.SpellSlotsUsedSlots4thSpinBox.setValue(self.PlayerCharacter.Stats["Spell Slots"]["4th"]["Used Slots"])
            self.PlayerCharacterSpellcastingWidgetInst.SpellSlotsUsedSlots5thSpinBox.setValue(self.PlayerCharacter.Stats["Spell Slots"]["5th"]["Used Slots"])
            self.PlayerCharacterSpellcastingWidgetInst.SpellSlotsUsedSlots6thSpinBox.setValue(self.PlayerCharacter.Stats["Spell Slots"]["6th"]["Used Slots"])
            self.PlayerCharacterSpellcastingWidgetInst.SpellSlotsUsedSlots7thSpinBox.setValue(self.PlayerCharacter.Stats["Spell Slots"]["7th"]["Used Slots"])
            self.PlayerCharacterSpellcastingWidgetInst.SpellSlotsUsedSlots8thSpinBox.setValue(self.PlayerCharacter.Stats["Spell Slots"]["8th"]["Used Slots"])
            self.PlayerCharacterSpellcastingWidgetInst.SpellSlotsUsedSlots9thSpinBox.setValue(self.PlayerCharacter.Stats["Spell Slots"]["9th"]["Used Slots"])

            # Spell Points Remaining
            self.PlayerCharacterSpellcastingWidgetInst.SpellPointsRemainingSpinBox.setValue(self.PlayerCharacter.Stats["Current Spell Points"])

            # Coins
            self.PlayerCharacterInventoryWidgetInst.CPSpinBox.setValue(self.PlayerCharacter.Stats["Coins"]["CP"])
            self.PlayerCharacterInventoryWidgetInst.SPSpinBox.setValue(self.PlayerCharacter.Stats["Coins"]["SP"])
            self.PlayerCharacterInventoryWidgetInst.EPSpinBox.setValue(self.PlayerCharacter.Stats["Coins"]["EP"])
            self.PlayerCharacterInventoryWidgetInst.GPSpinBox.setValue(self.PlayerCharacter.Stats["Coins"]["GP"])
            self.PlayerCharacterInventoryWidgetInst.PPSpinBox.setValue(self.PlayerCharacter.Stats["Coins"]["PP"])

            # Inspiration
            self.InspirationButton.setChecked(self.PlayerCharacter.Stats["Inspiration"])

            # Settings
            self.SpellcastingEnabledAction.setChecked(self.PlayerCharacter.Stats["Spellcasting Enabled"])
            self.ConcentrationCheckPromptEnabledAction.setChecked(self.PlayerCharacter.Stats["Enable Concentration Check"])
            self.SpellPointsEnabledAction.setChecked(self.PlayerCharacter.Stats["Spell Points Enabled"])
            self.PortraitEnabledAction.setChecked(self.PlayerCharacter.Stats["Portrait Enabled"])
            self.LuckyHalflingAction.setChecked(self.PlayerCharacter.Stats["Lucky Halfling"])

    def SetProficiencyIndicators(self, LineEdit, StatModifier):
        if LineEdit in [self.PlayerCharacterAbilitiesAndSkillsWidgetInst.StrengthSavingThrowLineEdit, self.PlayerCharacterAbilitiesAndSkillsWidgetInst.DexteritySavingThrowLineEdit, self.PlayerCharacterAbilitiesAndSkillsWidgetInst.ConstitutionSavingThrowLineEdit, self.PlayerCharacterAbilitiesAndSkillsWidgetInst.IntelligenceSavingThrowLineEdit, self.PlayerCharacterAbilitiesAndSkillsWidgetInst.WisdomSavingThrowLineEdit, self.PlayerCharacterAbilitiesAndSkillsWidgetInst.CharismaSavingThrowLineEdit]:
            if StatModifier["Proficiency Multiplier"] == 1:
                LineEdit.setStyleSheet(self.SavingThrowProficiencyLineEditStyleSheet)
                LineEdit.setToolTip("Proficient")
            elif StatModifier["Proficiency Multiplier"] == 2:
                LineEdit.setStyleSheet(self.SavingThrowExpertiseLineEditStyleSheet)
                LineEdit.setToolTip("Expertise")
            else:
                LineEdit.setStyleSheet(self.SavingThrowModifierLineEditStyleSheet)
                LineEdit.setToolTip("")
        else:
            if StatModifier["Proficiency Multiplier"] == 1:
                LineEdit.setStyleSheet(self.SkillProficiencyLineEditStyleSheet)
                LineEdit.setToolTip("Proficient")
            elif StatModifier["Proficiency Multiplier"] == 2:
                LineEdit.setStyleSheet(self.SkillExpertiseLineEditStyleSheet)
                LineEdit.setToolTip("Expertise")
            else:
                LineEdit.setStyleSheet(self.SkillModifierLineEditStyleSheet)
                LineEdit.setToolTip("")

    def UpdateWindowTitle(self):
        CurrentFileTitleSection = " [" + os.path.basename(self.CurrentOpenFileName) + "]" if self.CurrentOpenFileName != "" else ""
        UnsavedChangesIndicator = " *" if self.UnsavedChanges else ""
        self.setWindowTitle(self.ScriptName + " Character Sheet" + CurrentFileTitleSection + UnsavedChangesIndicator)
