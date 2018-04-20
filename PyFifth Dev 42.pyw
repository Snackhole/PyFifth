# PyFifth is coded in Python 3.6.3 on Windows 10.  Earlier or later versions and other operating systems may or may not work.

import json
import math
import os
import platform
import random
import string
from decimal import *
from time import sleep
from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox
from tkinter import ttk
from zipfile import ZipFile


# Global Functions and Variables
class Global:
    def __init__(self):
        # Variables
        self.ScriptName = os.path.splitext(os.path.basename(__file__))[0]
        self.OS = platform.system()
        self.ButtonColor = "#F1F1D4"
        self.SortTooltipString = "Left-click/right-click to sort in ascending/descending order.  Shift+left-click to search."

    def GetStringVarAsNumber(self, Var, Mode="Int"):
        VarText = Var.get()
        if len(VarText) == 0 or VarText == "+" or VarText == "-":
            VarText = 0
        if Mode == "Int":
            return int(VarText)
        elif Mode == "Decimal":
            return Decimal(VarText)
        elif Mode == "Float":
            return float(VarText)

    def ValidateNumberFromString(self, NewText, NotANumberString, Mode="Int", MinValue=None, LessThanMinString="", MaxValue=None, MoreThanMaxString=""):
        if NewText == "" or NewText == "+" or NewText == "-": return True
        try:
            if Mode == "Int":
                NewTextNumber = int(NewText)
            elif Mode == "Float":
                NewTextNumber = float(NewText)
            else:
                return False
        except:
            messagebox.showerror("Invalid Entry", NotANumberString)
            return False
        if MinValue is not None:
            if NewTextNumber < MinValue:
                messagebox.showerror("Invalid Entry", LessThanMinString)
                return False
        if MaxValue is not None:
            if NewTextNumber > MaxValue:
                messagebox.showerror("Invalid Entry", MoreThanMaxString)
                return False
        return True

    def WindowGeometry(self, Window, IsDialog=False, DialogMaster=None, WidthOffset=0, HeightOffset=0):
        Window.update_idletasks()
        BaseWidth = Window.winfo_width()
        BaseHeight = Window.winfo_height()
        BorderWidth = Window.winfo_rootx() - Window.winfo_x()
        WindowWidth = BaseWidth + (2 * BorderWidth)
        TitleHeight = Window.winfo_rooty() - Window.winfo_y()
        WindowHeight = BaseHeight + TitleHeight + BorderWidth
        if IsDialog:
            XCoordinate = DialogMaster.winfo_x() + ((DialogMaster.winfo_width() // 2) - (WindowWidth // 2))
            YCoordinate = DialogMaster.winfo_y() + ((DialogMaster.winfo_height() // 2) - (WindowHeight // 2))
        else:
            XCoordinate = (Window.winfo_screenwidth() // 2) - (WindowWidth // 2)
            YCoordinate = (Window.winfo_screenheight() // 2) - (WindowHeight // 2)
        Window.geometry("{}x{}+{}+{}".format(BaseWidth + WidthOffset, BaseHeight + HeightOffset, XCoordinate - (WidthOffset // 2), YCoordinate - (HeightOffset // 2)))
        Window.resizable(width=False, height=False)

    def WindowIcon(self, Window):
        try:
            Window.iconbitmap("PyFifthIcon.ico")
        except TclError:
            pass

    def SetupStatModifiers(self):
        self.StatModifierEntries = {}
        if WindowInst.Mode == "CharacterSheet":
            self.StatModifierEntries["Strength"] = Inst["AbilitiesAndSavingThrows"].StrengthEntry.AbilityEntryModifierVar
            self.StatModifierEntries["Dexterity"] = Inst["AbilitiesAndSavingThrows"].DexterityEntry.AbilityEntryModifierVar
            self.StatModifierEntries["Constitution"] = Inst["AbilitiesAndSavingThrows"].ConstitutionEntry.AbilityEntryModifierVar
            self.StatModifierEntries["Intelligence"] = Inst["AbilitiesAndSavingThrows"].IntelligenceEntry.AbilityEntryModifierVar
            self.StatModifierEntries["Wisdom"] = Inst["AbilitiesAndSavingThrows"].WisdomEntry.AbilityEntryModifierVar
            self.StatModifierEntries["Charisma"] = Inst["AbilitiesAndSavingThrows"].CharismaEntry.AbilityEntryModifierVar
            self.StatModifierEntries["Proficiency"] = CharacterSheetInst.ProficiencyBonusEntryVar
            self.StatModifierEntries["Level"] = CharacterSheetInst.CharacterLevelDropdownVar
        elif WindowInst.Mode == "NPCSheet":
            self.StatModifierEntries["Strength"] = CreatureDataInst.AbilitiesStrengthEntryVar
            self.StatModifierEntries["Dexterity"] = CreatureDataInst.AbilitiesDexterityEntryVar
            self.StatModifierEntries["Constitution"] = CreatureDataInst.AbilitiesConstitutionEntryVar
            self.StatModifierEntries["Intelligence"] = CreatureDataInst.AbilitiesIntelligenceEntryVar
            self.StatModifierEntries["Wisdom"] = CreatureDataInst.AbilitiesWisdomEntryVar
            self.StatModifierEntries["Charisma"] = CreatureDataInst.AbilitiesCharismaEntryVar
            self.StatModifierEntries["Proficiency"] = CreatureDataInst.ProficiencyEntryVar

    # Interception of Conflicting Bindings
    def InterceptEvents(self, Widget):
        if isinstance(Widget, ScrolledText.TrackableText):
            Widget.bind("<<Paste>>", lambda event: self.Paste(Widget))
            Widget.bind("<Tab>", lambda event: self.NextFocus(Widget))
            Widget.bind("<Shift-Tab>", lambda event: self.PreviousFocus(Widget))
        if WindowInst.Mode in ["CreatureDataUtility", "DiceRoller", "EncounterManager", "CharacterSheet", "NPCSheet"]:
            Widget.bind("<Control-o>", self.OpenButton)
            if WindowInst.Mode == "CharacterSheet":
                Widget.bind("<Control-d>", self.UpdateStatsAndInventory)
            if WindowInst.Mode == "NPCSheet":
                Widget.bind("<Control-d>", self.UpdateStats)
        if WindowInst.Mode == "EncounterManager":
            Widget.bind("<Control-r>", self.NewRoundEncounterManager)
            Widget.bind("<Control-t>", self.NextTurnEncounterManager)
            Widget.bind("<Control-T>", self.ClearTurnsEncounterManager)
            Widget.bind("<Control-i>", self.SortInitiativeOrderEncounterManager)
        if WindowInst.Mode == "CompactInitiativeOrder":
            Widget.bind("<Control-r>", self.NewRoundCompactInitiativeOrder)
            Widget.bind("<Control-t>", self.NextTurnCompactInitiativeOrder)
            Widget.bind("<Control-T>", self.ClearTurnsCompactInitiativeOrder)
            Widget.bind("<Control-i>", self.SortInitiativeOrderCompactInitiativeOrder)

    def Paste(self, Widget):
        SelectionRange = Widget.tag_ranges("sel")
        if SelectionRange:
            SelectionStart = Widget.index(SEL_FIRST)
            SelectionEnd = Widget.index(SEL_LAST)
            Widget.delete(SelectionStart, SelectionEnd)
            Widget.mark_set(INSERT, SelectionStart)
        Widget.insert(INSERT, Widget.clipboard_get())
        Widget.see(INSERT)
        return "break"

    def OpenButton(self, event):
        SavingAndOpeningInst.OpenButton()
        return "break"

    def UpdateStatsAndInventory(self, event):
        CharacterSheetInst.UpdateStatsAndInventory()
        return "break"

    def UpdateStats(self, event):
        CreatureDataInst.UpdateStats()
        return "break"

    def NewRoundEncounterManager(self, event):
        InitiativeOrderInst.NewRound()
        return "break"

    def NextTurnEncounterManager(self, event):
        InitiativeOrderInst.NextTurn()
        return "break"

    def ClearTurnsEncounterManager(self, event):
        InitiativeOrderInst.ClearTurns()
        return "break"

    def SortInitiativeOrderEncounterManager(self, event):
        InitiativeOrderInst.SortInitiativeOrder()
        return "break"

    def NewRoundCompactInitiativeOrder(self, event):
        CompactInitiativeOrderInst.NewRound()
        return "break"

    def NextTurnCompactInitiativeOrder(self, event):
        CompactInitiativeOrderInst.NextTurn()
        return "break"

    def ClearTurnsCompactInitiativeOrder(self, event):
        CompactInitiativeOrderInst.ClearTurns()
        return "break"

    def SortInitiativeOrderCompactInitiativeOrder(self, event):
        CompactInitiativeOrderInst.SortInitiativeOrder()
        return "break"

    def NextFocus(self, Widget):
        Widget.tk_focusNext().focus_set()
        return "break"

    def PreviousFocus(self, Widget):
        Widget.tk_focusPrev().focus_set()
        return "break"


# Saving
class SavingAndOpening:
    def __init__(self):
        self.CurrentOpenFilePath = StringVar()
        self.Opening = False
        self.OpenErrors = False
        self.OpenErrorsString = ""
        self.SavedData = {}
        self.SavePrompt = False

        # File Types
        self.FileTypes = {}
        self.FileTypes["CreatureDataUtility"] = self.FileType("Creature file", ".crea", "Save Creature File", "Open Creature File", "Creature Data.txt")
        self.FileTypes["DiceRoller"] = self.FileType("Roll file", ".roll", "Save Roll File", "Open Roll File", "Roll Data.txt")
        self.FileTypes["EncounterManager"] = self.FileType("Encounter file", ".enc", "Save Encounter File", "Open Encounter File", "Encounter Data.txt")
        self.FileTypes["CharacterSheet"] = self.FileType("Character file", ".char", "Save Character File", "Open Character File", "Character Data.txt")
        self.FileTypes["NPCSheet"] = self.FileType("NPC file", ".npc", "Save NPC File", "Open NPC File", "NPC Data.txt")
        self.FileTypes["HoardSheet"] = self.FileType("Hoard file", ".hrd", "Save Hoard File", "Open Hoard File", "Hoard Data.txt")

        # Bind Closing Protocol
        WindowInst.wm_protocol("WM_DELETE_WINDOW", self.CloseWindow)

    # Save Methods
    def SaveButton(self, SaveAs=False):
        # Store Window Mode
        WindowMode = WindowInst.Mode

        # Saving...
        StatusBarInst.StatusBarSetText("Saving...", Lock=True)

        # Determine Save Path
        CurrentPath = self.CurrentOpenFilePath.get()
        if CurrentPath == "" or SaveAs:
            SaveFileName = filedialog.asksaveasfilename(filetypes=((self.FileTypes[WindowMode].Descriptor, "*" + self.FileTypes[WindowMode].Extension), ("All files", "*.*")), defaultextension=self.FileTypes[WindowMode].Extension,
                                                        title=self.FileTypes[WindowMode].SavePromptTitle)
        else:
            SaveFileName = CurrentPath

        # Store Text File Name
        TextFileName = self.FileTypes[WindowMode].TextFileName

        # Create File
        if SaveFileName != "":
            # Try to Create File
            try:
                with ZipFile(SaveFileName, mode="w") as SaveFile:
                    with open(TextFileName, mode="w") as TextFile:
                        self.SaveData(TextFile)
                    SaveFile.write(TextFileName)

                    # Character Portrait
                    if WindowMode == "CharacterSheet":
                        if self.SavedData["PortraitSelectedVar"].get():
                            PortraitFileName = "Portrait.gif"
                            Inst["Portrait"].PortraitImage.write(PortraitFileName)
                            SaveFile.write(PortraitFileName)
                            self.DeleteFile(PortraitFileName)

            # Handle Permission Error
            except PermissionError:
                messagebox.showerror("Save File Permission Error",
                                     "Could not save the following file due to a permission error:\n\n" + SaveFileName + "\n\nIt could be open in another program or in a location that you don't have permission to write to.")
                StatusBarInst.FlashStatus("No file saved!")
                return False

            # Delete Text File
            self.DeleteFile(TextFileName)

            # Set Current Open File Path
            self.CurrentOpenFilePath.set(SaveFileName)

            # Small Pause
            sleep(0.5)

            # Unflag Save Prompt
            self.SavePrompt = False

            # Update Window Title
            WindowInst.UpdateWindowTitle()

            # Flash Status
            StatusBarInst.FlashStatus("File saved as:  " + os.path.basename(SaveFileName))

            # Return Successful Save
            return True

        # No File Name
        else:
            # Flash Status
            StatusBarInst.FlashStatus("No file saved!")

            # Return Unsuccessful Save
            return False

    def SaveData(self, File):
        for Tag, Field in SavingAndOpeningInst.SavedData.items():
            File.write(json.dumps({Tag: Field.get()}) + "\n")

    def ExportDiceRoller(self):
        if WindowInst.Mode in ["CharacterSheet", "NPCSheet"]:
            ExportConfirm = messagebox.askyesno("Export Dice Roller Data", "Dice roller data will not include settings for preset roll modifier calculations.  Proceed?")
            if not ExportConfirm:
                return
        StatusBarInst.StatusBarSetText("Exporting rolls file...", Lock=True)
        SaveFileName = filedialog.asksaveasfilename(filetypes=(("Roll file", "*.roll"), ("All files", "*.*")), defaultextension=".roll", title="Export Roll File")
        TextFileName = "Roll Data.txt"
        if SaveFileName != "":
            with ZipFile(SaveFileName, mode="w") as SaveFile:
                with open(TextFileName, mode="w") as TextFile:
                    self.ExportDiceRollerData(TextFile)
                SaveFile.write(TextFileName)
            self.DeleteFile(TextFileName)
            sleep(0.5)
            StatusBarInst.FlashStatus("File saved as:  " + os.path.basename(SaveFileName))
        else:
            StatusBarInst.FlashStatus("No file saved!")

    def ExportDiceRollerData(self, File):
        for Tag, Field in Inst["PresetRolls"].DiceRollerFields.items():
            File.write(json.dumps({Tag: Field.get()}) + "\n")

    # Open Methods
    def OpenButton(self):
        # Store Window Mode
        WindowMode = WindowInst.Mode

        # Save Prompt
        if self.SavePrompt:
            SaveConfirm = messagebox.askyesnocancel("Save", "Save unsaved work before opening?")
            if SaveConfirm == None:
                return
            elif SaveConfirm == True:
                if not self.SaveButton():
                    return

        # Opening...
        StatusBarInst.StatusBarSetText("Opening...", Lock=True)

        # Determine Open Path
        OpenFileName = filedialog.askopenfilename(filetypes=((self.FileTypes[WindowMode].Descriptor, "*" + self.FileTypes[WindowMode].Extension), ("All files", "*.*")), defaultextension=self.FileTypes[WindowMode].Extension,
                                                  title=self.FileTypes[WindowMode].OpenPromptTitle)

        # Store Text File Name
        TextFileName = self.FileTypes[WindowMode].TextFileName

        # Open File
        if OpenFileName != "":
            # Extract Data from File
            with ZipFile(OpenFileName, mode="r") as OpenFile:
                with open(OpenFile.extract(TextFileName), mode="r") as TextFile:
                    self.OpenData(TextFile)

                # Character Portrait
                if WindowMode == "CharacterSheet":
                    if self.SavedData["PortraitSelectedVar"].get():
                        PortraitFileName = "Portrait.gif"
                        OpenFile.extract(PortraitFileName)
                        Inst["Portrait"].SetPortrait(PortraitFileName)
                        self.DeleteFile(PortraitFileName)

            # Delete Text File
            self.DeleteFile(TextFileName)

            # Set Current Open File Path
            self.CurrentOpenFilePath.set(OpenFileName)

            # Character Sheet Stats and Inventory
            if WindowMode == "CharacterSheet":
                CharacterSheetInst.UpdateStatsAndInventory()

            # NPC Sheet Stats
            if WindowMode == "NPCSheet":
                CreatureDataInst.UpdateStats()

            # Hoard Sheet Stats
            if WindowMode == "HoardSheet":
                HoardSheetInst.UpdateHoardStats()

            # Small Pause
            sleep(0.5)

            # Handle Dictionary Key Errors
            if self.OpenErrors:
                OpenErrorsPromptInst = OpenErrorsPrompt(WindowInst, self.OpenErrorsString[:-1])
                WindowInst.wait_window(OpenErrorsPromptInst.Window)
                self.OpenErrors = False
                self.OpenErrorsString = ""

            # Unflag Save Prompt
            self.SavePrompt = False

            # Update Window Title
            WindowInst.UpdateWindowTitle()

            # Flash Status
            StatusBarInst.FlashStatus("Opened file:  " + os.path.basename(OpenFileName))

        # No File Name
        else:
            # Flash Status
            StatusBarInst.FlashStatus("No file opened!")

    def OpenData(self, File):
        self.Opening = True
        for Line in File:
            if Line != "":
                LoadedLine = json.loads(Line)
                for Tag, Field in LoadedLine.items():
                    try:
                        SavingAndOpeningInst.SavedData[Tag].set(Field)
                    except KeyError:
                        self.OpenErrors = True
                        self.OpenErrorsString += Line
        if WindowInst.Mode == "Encounter Manager":
            for Entry in InitiativeOrderInst.InitiativeEntriesList:
                if Entry.InitiativeEntryTurnDoneVar.get():
                    Entry.TurnDoneOn()
                else:
                    Entry.TurnDoneOff()
                if Entry.InitiativeEntryDeadVar.get():
                    Entry.DeadOn()
                else:
                    Entry.DeadOff()
        if WindowInst.Mode == "CharacterSheet":
            CharacterSheetInst.SpellcasterToggle()
            CharacterSheetInst.PortraitToggle()
        self.Opening = False

    def NewButton(self):
        # Check for Save Prompt
        if SavingAndOpeningInst.SavePrompt:
            SaveConfirm = messagebox.askyesnocancel("New", "Save unsaved work before starting a new file?")
            if SaveConfirm == None:
                return
            elif SaveConfirm == True:
                if not SavingAndOpeningInst.SaveButton():
                    return

        # Flag Opening
        self.Opening = True

        # Reset Saved Fields to Default Values
        for Field in SavingAndOpeningInst.SavedData.values():
            if WindowInst.Mode in ["DiceRoller", "EncounterManager", "CharacterSheet", "NPCSheet"]:
                if Field == DiceRollerInst.CritMinimumEntryVar:
                    Field.set("20")
                    continue
            if WindowInst.Mode == "CharacterSheet":
                if Field in [CharacterSheetInst.SpellcasterBoxVar, CharacterSheetInst.ConcentrationCheckPromptBoxVar, CharacterSheetInst.PortraitBoxVar]:
                    Field.set(True)
                    continue
                if Field is CharacterSheetInst.CharacterLevelDropdownVar:
                    Field.set("1")
                    continue
                if Field in [Inst["AbilitiesAndSavingThrows"].StrengthEntry.AbilityBaseVar, Inst["AbilitiesAndSavingThrows"].StrengthEntry.AbilityEntryTotalVar, Inst["AbilitiesAndSavingThrows"].DexterityEntry.AbilityBaseVar,
                             Inst["AbilitiesAndSavingThrows"].DexterityEntry.AbilityEntryTotalVar, Inst["AbilitiesAndSavingThrows"].ConstitutionEntry.AbilityBaseVar,
                             Inst["AbilitiesAndSavingThrows"].ConstitutionEntry.AbilityEntryTotalVar, Inst["AbilitiesAndSavingThrows"].IntelligenceEntry.AbilityBaseVar,
                             Inst["AbilitiesAndSavingThrows"].IntelligenceEntry.AbilityEntryTotalVar, Inst["AbilitiesAndSavingThrows"].WisdomEntry.AbilityBaseVar, Inst["AbilitiesAndSavingThrows"].WisdomEntry.AbilityEntryTotalVar,
                             Inst["AbilitiesAndSavingThrows"].CharismaEntry.AbilityBaseVar, Inst["AbilitiesAndSavingThrows"].CharismaEntry.AbilityEntryTotalVar]:
                    Field.set("8")
                    continue
            if type(Field) in [BooleanVar, SavedBooleanVar]:
                Field.set(False)
            else:
                Field.set("")

        # Dice Roller Defaults
        if WindowInst.Mode in ["DiceRoller", "EncounterManager", "CharacterSheet"]:
            DiceRollerInst.DiceNumberEntryVar.set("1")
            DiceRollerInst.DieTypeEntryVar.set("20")
            DiceRollerInst.ModifierEntryVar.set("0")

        # Encounter Manager Defaults
        if WindowInst.Mode == "EncounterManager":
            for Entry in InitiativeOrderInst.InitiativeEntriesList:
                Entry.TurnDoneOff()
                Entry.DeadOff()

        # Character Sheet Defaults
        if WindowInst.Mode == "CharacterSheet":
            # Clear Portrait
            Inst["Portrait"].Clear()

            # Set All Preset Roll Modifiers to Default Values
            for Entry in Inst["PresetRolls"].PresetRollsList:
                Entry.PresetRollModifierEntryStatModifierInst.DefaultValues()

            # Experience Needed and Proficiency Bonus to Default
            CharacterSheetInst.CharacterExperienceNeededEntryVar.set("")
            CharacterSheetInst.ProficiencyBonusEntryVar.set("")

            # All Ability and Skill Modifiers to Default
            for Entry in Inst["AbilitiesAndSavingThrows"].AbilityEntriesList:
                Entry.AbilityEntryModifierVar.set("")
                Entry.AbilityEntryModifierStatModifierInst.DefaultValues()
                Entry.AbilitySavingThrowModifierVar.set("")
                Entry.AbilitySavingThrowModifierStatModifierInst.DefaultValues()
            for Entry in Inst["Skills"].SkillsEntriesList:
                Entry.TotalModifierVar.set("")
                Entry.ModifierEntryStatModifierInst.DefaultValues()

            # Inventory Values to Default
            Inst["Inventory"].CarryingCapacityVar.set("")
            Inst["Inventory"].CarryingCapacityEntryStatModifierInst.DefaultValues()
            Inst["Inventory"].CoinValueEntryVar.set("")
            Inst["Inventory"].CoinWeightEntryVar.set("")
            Inst["Inventory"].TotalLoadEntryVar.set("")
            Inst["Inventory"].GearLoadEntryVar.set("")
            Inst["Inventory"].TreasureLoadEntryVar.set("")
            Inst["Inventory"].MiscLoadEntryVar.set("")
            Inst["Inventory"].TotalValueEntryVar.set("")
            Inst["Inventory"].GearValueEntryVar.set("")
            Inst["Inventory"].TreasureValueEntryVar.set("")
            Inst["Inventory"].MiscValueEntryVar.set("")
            Inst["Inventory"].TotalLoadEntry.configure(disabledbackground="light gray", disabledforeground="black")
            Inst["Inventory"].FoodDisplay.LoadEntryVar.set("")
            Inst["Inventory"].FoodDisplay.DaysEntryVar.set("")
            Inst["Inventory"].FoodDisplay.ConsumptionRateVar.set("1")
            Inst["Inventory"].WaterDisplay.LoadEntryVar.set("")
            Inst["Inventory"].WaterDisplay.DaysEntryVar.set("")
            Inst["Inventory"].WaterDisplay.ConsumptionRateVar.set("8")
            for Entry in Inst["Inventory"].InventoryEntriesList:
                Entry.TotalWeightEntryVar.set("")
                Entry.TotalValueEntryVar.set("")

            # Max HP, AC, and Initiative to Default
            Inst["CombatAndFeatures"].MaxHPEntryVar.set("")
            Inst["CombatAndFeatures"].ACEntryVar.set("")
            Inst["CombatAndFeatures"].ACEntryStatModifierInst.DefaultValues()
            Inst["CombatAndFeatures"].InitiativeEntryVar.set("")
            Inst["CombatAndFeatures"].InitiativeEntryStatModifierInst.DefaultValues()

            # Ability Score Derivatives to Defaults
            AllAbilityScoreDerivativesList = Inst["CombatAndFeatures"].AbilityScoreDerivativesList + Inst["Spellcasting"].SpellcastingAbilitiesList
            for Ability in AllAbilityScoreDerivativesList:
                Ability.AttackModifierEntryVar.set("")
                Ability.AttackModifierEntryStatModifierInst.DefaultValues()
                Ability.SaveDCEntryVar.set("")
                Ability.SaveDCEntryStatModifierInst.DefaultValues()

            # Passive Perception and Investigation to Default
            Inst["AbilitiesAndSkills"].PassivePerceptionEntryVar.set("")
            Inst["AbilitiesAndSkills"].PassivePerceptionStatModifierInst.DefaultValues()
            Inst["AbilitiesAndSkills"].PassiveInvestigationEntryVar.set("")
            Inst["AbilitiesAndSkills"].PassiveInvestigationStatModifierInst.DefaultValues()

            # Spell Points to Default
            Inst["Spellcasting"].SpellPointsMaxEntryVar.set("")
            Inst["Spellcasting"].SpellPointsMaxEntryStatModifierInst.DefaultValues()

        # NPC Sheet Defaults
        if WindowInst.Mode == "NPCSheet":
            # Set All Preset Roll Modifiers to Default Values
            for Entry in Inst["PresetRolls"].PresetRollsList:
                Entry.PresetRollModifierEntryStatModifierInst.DefaultValues()

        # Unflag Opening
        self.Opening = False

        # No Current File
        self.CurrentOpenFilePath.set("")

        # No Save Prompt
        SavingAndOpeningInst.SavePrompt = False

        # Update Window Title
        WindowInst.UpdateWindowTitle()

        # Calculate Stats
        if WindowInst.Mode == "CharacterSheet":
            CharacterSheetInst.UpdateStatsAndInventory()

        # Flash Status
        StatusBarInst.FlashStatus("New file started.")

    def ImportDiceRoller(self):
        ImportConfirm = messagebox.askyesno("Import Dice Roller Data", "Are you sure you want to overwrite the dice roller data with imported data?  This cannot be undone.")
        if not ImportConfirm:
            return
        StatusBarInst.StatusBarSetText("Importing roll file...", Lock=True)
        OpenFileName = filedialog.askopenfilename(filetypes=(("Roll file", "*.roll"), ("All files", "*.*")), defaultextension=".roll", title="Import Roll File")
        TextFileName = "Roll Data.txt"
        if OpenFileName != "":
            with ZipFile(OpenFileName, mode="r") as OpenFile:
                with open(OpenFile.extract(TextFileName), mode="r") as TextFile:
                    self.ImportDiceRollerData(TextFile)
            self.DeleteFile(TextFileName)
            sleep(0.5)
            if self.OpenErrors:
                OpenErrorsPromptInst = OpenErrorsPrompt(WindowInst, self.OpenErrorsString[:-1])
                WindowInst.wait_window(OpenErrorsPromptInst.Window)
                self.OpenErrors = False
                self.OpenErrorsString = ""
            StatusBarInst.FlashStatus("Imported file:  " + os.path.basename(OpenFileName))
        else:
            StatusBarInst.FlashStatus("No file imported!")

    def ImportDiceRollerData(self, File):
        for Line in File:
            if Line != "":
                LoadedLine = json.loads(Line)
                for Tag, Field in LoadedLine.items():
                    try:
                        Inst["PresetRolls"].DiceRollerFields[Tag].set(Field)
                    except KeyError:
                        self.OpenErrors = True
                        self.OpenErrorsString += Line
        if WindowInst.Mode in ["CharacterSheet", "NPCSheet"]:
            for Entry in Inst["PresetRolls"].PresetRollsList:
                Entry.PresetRollModifierEntryStatModifierInst.DefaultValues()

    # Field Tracking
    def TrackModifiedFields(self):
        for Field in self.SavedData.values():
            FieldType = type(Field)
            if FieldType in [StringVar, SavedStringVar, BooleanVar, SavedBooleanVar]:
                Field.trace_add("write", lambda a, b, c: self.SavedDataModified())
            elif FieldType == ScrolledText:
                Field.Text.bind("<<TextModified>>", lambda event: self.SavedDataModified())

    def SavedDataModified(self):
        if not self.Opening:
            self.SavePrompt = True
            WindowInst.UpdateWindowTitle()

    def CloseWindow(self):
        if self.SavePrompt:
            SaveConfirm = messagebox.askyesnocancel("Save", "Save unsaved work before closing?")
            if SaveConfirm == None:
                return
            elif SaveConfirm == True:
                if not self.SaveButton():
                    return
        WindowInst.destroy()

    # Save and Open Helpers
    def DeleteFile(self, File):
        try:
            os.remove(File)
        except PermissionError:
            messagebox.showerror("Temporary File Permission Error", "Could not delete the following temporary file due to a permission error:\n\n" + File + "\n\nTry again or delete the file manually.")

    class FileType:
        def __init__(self, Descriptor, Extension, SavePromptTitle, OpenPromptTitle, TextFileName):
            self.Descriptor = Descriptor
            self.Extension = Extension
            self.SavePromptTitle = SavePromptTitle
            self.OpenPromptTitle = OpenPromptTitle
            self.TextFileName = TextFileName


class SavedStringVar(StringVar):
    def __init__(self, Tag=None, DefaultValue=""):
        # Store Parameters
        self.Tag = Tag

        # Init
        StringVar.__init__(self, value=DefaultValue)

        # Add to Saved Data Dictionary
        if self.Tag is not None:
            SavingAndOpeningInst.SavedData[self.Tag] = self

    def UpdateTag(self, Tag):
        self.Tag = Tag
        SavingAndOpeningInst.SavedData[self.Tag] = self


class SavedBooleanVar(BooleanVar):
    def __init__(self, Tag=None, DefaultValue=False):
        # Store Parameters
        self.Tag = Tag

        # Init
        BooleanVar.__init__(self, value=DefaultValue)

        # Add to Saved Data Dictionary
        if self.Tag is not None:
            SavingAndOpeningInst.SavedData[self.Tag] = self

    def UpdateTag(self, Tag):
        self.Tag = Tag
        SavingAndOpeningInst.SavedData[self.Tag] = self


# Window Elements
class CharacterSheet:
    def __init__(self, master):
        # Variables
        self.CharacterNameEntryVar = SavedStringVar("CharacterNameEntryVar")
        self.CharacterLevelDropdownVar = SavedStringVar("CharacterLevelEntryVar", DefaultValue="1")
        self.CharacterLevelDropdownVar.trace_add("write", lambda a, b, c: self.UpdateStatsAndInventory())
        self.CharacterClassEntryVar = SavedStringVar("CharacterClassEntryVar")
        self.CharacterExperienceEntryVar = SavedStringVar("CharacterExperienceEntryVar")
        self.CharacterExperienceNeededEntryVar = StringVar()
        self.ProficiencyBonusEntryVar = StringVar()
        self.SpellcasterBoxVar = SavedBooleanVar("SpellcasterBoxVar", DefaultValue=True)
        self.ConcentrationCheckPromptBoxVar = SavedBooleanVar("ConcentrationCheckPromptBoxVar", DefaultValue=True)
        self.PortraitBoxVar = SavedBooleanVar("PortraitBoxVar", DefaultValue=True)
        self.JackOfAllTradesBoxVar = SavedBooleanVar("JackOfAllTradesBoxVar")
        self.RemarkableAthleteBoxVar = SavedBooleanVar("RemarkableAthleteBoxVar")
        self.ObservantBoxVar = SavedBooleanVar("ObservantBoxVar")
        self.LuckyHalflingBoxVar = SavedBooleanVar("LuckyHalflingBoxVar")

        # Settings Menu Vars
        self.SettingsMenuVars = {}
        self.SettingsMenuVars["SpellcasterBoxVar"] = self.SpellcasterBoxVar
        self.SettingsMenuVars["ConcentrationCheckPromptBoxVar"] = self.ConcentrationCheckPromptBoxVar
        self.SettingsMenuVars["PortraitBoxVar"] = self.PortraitBoxVar
        self.SettingsMenuVars["JackOfAllTradesBoxVar"] = self.JackOfAllTradesBoxVar
        self.SettingsMenuVars["RemarkableAthleteBoxVar"] = self.RemarkableAthleteBoxVar
        self.SettingsMenuVars["ObservantBoxVar"] = self.ObservantBoxVar
        self.SettingsMenuVars["LuckyHalflingBoxVar"] = self.LuckyHalflingBoxVar

        # Character Sheet Frame
        self.CharacterSheetFrame = Frame(master)
        self.CharacterSheetFrame.grid(row=0, column=0, sticky=NSEW)

        # Character Sheet Header Frame
        self.CharacterSheetHeaderFrame = LabelFrame(self.CharacterSheetFrame, text="Basic Character Info:")
        self.CharacterSheetHeaderFrame.grid_columnconfigure(2, weight=1)
        self.CharacterSheetHeaderFrame.grid_columnconfigure(5, weight=1)
        self.CharacterSheetHeaderFrame.grid_rowconfigure(1, minsize=25, weight=1)
        self.CharacterSheetHeaderFrame.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Character Name
        self.CharacterNameLabel = Label(self.CharacterSheetHeaderFrame, text="Name:")
        self.CharacterNameLabel.grid(row=0, column=0, sticky=E)
        self.CharacterNameEntry = EntryExtended(self.CharacterSheetHeaderFrame, textvariable=self.CharacterNameEntryVar, justify=CENTER, width=50)
        self.CharacterNameEntry.grid(row=0, column=1, sticky=E, padx=2, pady=2)

        # Class
        self.CharacterClassLabel = Label(self.CharacterSheetHeaderFrame, text="Class:")
        self.CharacterClassLabel.grid(row=1, column=0, sticky=E)
        self.CharacterClassEntry = EntryExtended(self.CharacterSheetHeaderFrame, textvariable=self.CharacterClassEntryVar, justify=CENTER, width=50)
        self.CharacterClassEntry.grid(row=1, column=1, sticky=E, padx=2, pady=2)

        # Character Level
        self.CharacterLevelLabel = Label(self.CharacterSheetHeaderFrame, text="Level:")
        self.CharacterLevelLabel.grid(row=0, column=3, sticky=E)
        self.CharacterLevelDropdownValues = []
        for Index in range(1, 21):
            self.CharacterLevelDropdownValues.append(str(Index))
        self.CharacterLevelDropdown = DropdownExtended(self.CharacterSheetHeaderFrame, textvariable=self.CharacterLevelDropdownVar, width=5, justify=CENTER, state="readonly", values=self.CharacterLevelDropdownValues)
        self.CharacterLevelDropdown.grid(row=0, column=4, sticky=NSEW, padx=2, pady=2)

        # Proficiency Bonus
        self.ProficiencyBonusLabel = Label(self.CharacterSheetHeaderFrame, text="Proficiency Bonus:")
        self.ProficiencyBonusLabel.grid(row=1, column=3, sticky=E)
        self.ProficiencyBonusEntry = EntryExtended(self.CharacterSheetHeaderFrame, textvariable=self.ProficiencyBonusEntryVar, state=DISABLED, justify=CENTER, width=5, disabledbackground="light gray",
                                                   disabledforeground="black",
                                                   cursor="arrow")
        self.ProficiencyBonusEntry.grid(row=1, column=4, sticky=NSEW, padx=2, pady=2)

        # Experience
        self.CharacterExperienceLabel = Label(self.CharacterSheetHeaderFrame, text="Exp.:")
        self.CharacterExperienceLabel.grid(row=0, column=6, sticky=E)
        self.CharacterExperienceEntry = EntryExtended(self.CharacterSheetHeaderFrame, textvariable=self.CharacterExperienceEntryVar, width=10, justify=CENTER)
        self.CharacterExperienceEntry.grid(row=0, column=7, sticky=NSEW, padx=2, pady=2)

        # Needed Experience
        self.CharacterExperienceNeededLabel = Label(self.CharacterSheetHeaderFrame, text="Needed Exp.:")
        self.CharacterExperienceNeededLabel.grid(row=1, column=6, sticky=E)
        self.CharacterExperienceNeededEntry = EntryExtended(self.CharacterSheetHeaderFrame, textvariable=self.CharacterExperienceNeededEntryVar, state=DISABLED, justify=CENTER, width=10, disabledbackground="light gray",
                                                            disabledforeground="black", cursor="arrow")
        self.CharacterExperienceNeededEntry.grid(row=1, column=7, sticky=NSEW, padx=2, pady=2)

        # Character Stats Frame
        self.CharacterStatsFrame = LabelFrame(self.CharacterSheetFrame, text="Character Stats, Inventory, and Notes:")
        self.CharacterStatsFrame.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)

        # Character Stats Notebook
        self.CharacterStatsNotebook = ttk.Notebook(self.CharacterStatsFrame, height=500)
        self.CharacterStatsNotebook.grid(row=0, column=0)
        self.CharacterStatsNotebook.enable_traversal()

        # Abilities and Skills Page
        self.AbilitiesAndSkillsPage = Frame(self.CharacterStatsNotebook)
        self.CharacterStatsNotebook.add(self.AbilitiesAndSkillsPage, text="Abilities and Skills")
        self.AbilitiesAndSkillsInst = self.AbilitiesAndSkills(self.AbilitiesAndSkillsPage)
        Inst["AbilitiesAndSkills"] = self.AbilitiesAndSkillsInst

        # Combat and Features
        self.CombatAndFeaturesPage = Frame(self.CharacterStatsNotebook)
        self.CharacterStatsNotebook.add(self.CombatAndFeaturesPage, text="Combat and Features")
        self.CombatAndFeaturesInst = self.CombatAndFeatures(self.CombatAndFeaturesPage)
        Inst["CombatAndFeatures"] = self.CombatAndFeaturesInst

        # Spellcasting
        self.SpellcastingPage = Frame(self.CharacterStatsNotebook)
        self.CharacterStatsNotebook.add(self.SpellcastingPage, text="Spellcasting")
        self.SpellcastingInst = self.Spellcasting(self.SpellcastingPage)
        Inst["Spellcasting"] = self.SpellcastingInst

        # Inventory
        self.InventoryPage = Frame(self.CharacterStatsNotebook)
        self.CharacterStatsNotebook.add(self.InventoryPage, text="Inventory")
        self.InventoryInst = self.Inventory(self.InventoryPage)
        Inst["Inventory"] = self.InventoryInst

        # Notes
        self.NotesPage = Frame(self.CharacterStatsNotebook)
        self.CharacterStatsNotebook.add(self.NotesPage, text="Notes")
        self.NotesInst = self.Notes(self.NotesPage)
        Inst["Notes"] = self.NotesInst

        # Personality and Backstory
        self.PersonalityAndBackstoryPage = Frame(self.CharacterStatsNotebook)
        self.CharacterStatsNotebook.add(self.PersonalityAndBackstoryPage, text="Personality and Backstory")
        self.PersonalityAndBackstoryInst = self.PersonalityAndBackstory(self.PersonalityAndBackstoryPage)
        Inst["PersonalityAndBackstory"] = self.PersonalityAndBackstoryInst

        # Portrait
        self.PortraitPage = Frame(self.CharacterStatsNotebook)
        self.CharacterStatsNotebook.add(self.PortraitPage, text="Portrait")
        self.PortraitInst = self.Portrait(self.PortraitPage)
        Inst["Portrait"] = self.PortraitInst

    def UpdateStatsAndInventory(self):
        # Check Opening
        if SavingAndOpeningInst.Opening:
            return
        else:
            pass

        # Store Level
        CharacterLevelValue = GlobalInst.GetStringVarAsNumber(self.CharacterLevelDropdownVar)

        # Calculate Experience Needed and Proficiency Modifier
        TotalExperienceNeeded = 0
        ProficiencyModifier = 0
        if CharacterLevelValue >= 1:
            TotalExperienceNeeded += 300
            ProficiencyModifier += 2
        if CharacterLevelValue >= 2:
            TotalExperienceNeeded += 600
        if CharacterLevelValue >= 3:
            TotalExperienceNeeded += 1800
        if CharacterLevelValue >= 4:
            TotalExperienceNeeded += 3800
        if CharacterLevelValue >= 5:
            TotalExperienceNeeded += 7500
            ProficiencyModifier += 1
        if CharacterLevelValue >= 6:
            TotalExperienceNeeded += 9000
        if CharacterLevelValue >= 7:
            TotalExperienceNeeded += 11000
        if CharacterLevelValue >= 8:
            TotalExperienceNeeded += 14000
        if CharacterLevelValue >= 9:
            TotalExperienceNeeded += 16000
            ProficiencyModifier += 1
        if CharacterLevelValue >= 10:
            TotalExperienceNeeded += 21000
        if CharacterLevelValue >= 11:
            TotalExperienceNeeded += 15000
        if CharacterLevelValue >= 12:
            TotalExperienceNeeded += 20000
        if CharacterLevelValue >= 13:
            TotalExperienceNeeded += 20000
            ProficiencyModifier += 1
        if CharacterLevelValue >= 14:
            TotalExperienceNeeded += 25000
        if CharacterLevelValue >= 15:
            TotalExperienceNeeded += 30000
        if CharacterLevelValue >= 16:
            TotalExperienceNeeded += 30000
        if CharacterLevelValue >= 17:
            TotalExperienceNeeded += 40000
            ProficiencyModifier += 1
        if CharacterLevelValue >= 18:
            TotalExperienceNeeded += 40000
        if CharacterLevelValue >= 19:
            TotalExperienceNeeded += 50000
        if CharacterLevelValue >= 20:
            TotalExperienceNeeded = "N/A"
        self.CharacterExperienceNeededEntryVar.set(TotalExperienceNeeded)
        self.ProficiencyBonusEntryVar.set("+" + str(ProficiencyModifier))

        # Calculate Ability and Saving Throw Modifiers
        for Entry in Inst["AbilitiesAndSavingThrows"].AbilityEntriesList:
            Entry.CalculateModifiers(ProficiencyModifier)

        # Store Ability Modifiers
        StrengthModifier = GlobalInst.GetStringVarAsNumber(Inst["AbilitiesAndSavingThrows"].StrengthEntry.AbilityEntryModifierVar)
        DexterityModifier = GlobalInst.GetStringVarAsNumber(Inst["AbilitiesAndSavingThrows"].DexterityEntry.AbilityEntryModifierVar)
        ConstitutionModifier = GlobalInst.GetStringVarAsNumber(Inst["AbilitiesAndSavingThrows"].ConstitutionEntry.AbilityEntryModifierVar)
        IntelligenceModifier = GlobalInst.GetStringVarAsNumber(Inst["AbilitiesAndSavingThrows"].IntelligenceEntry.AbilityEntryModifierVar)
        WisdomModifier = GlobalInst.GetStringVarAsNumber(Inst["AbilitiesAndSavingThrows"].WisdomEntry.AbilityEntryModifierVar)
        CharismaModifier = GlobalInst.GetStringVarAsNumber(Inst["AbilitiesAndSavingThrows"].CharismaEntry.AbilityEntryModifierVar)

        # Calculate Skill Modifiers
        for Entry in Inst["Skills"].SkillsEntriesList:
            if Entry.SkillNameVar.get().endswith("(STR)"):
                AbilityModifier = StrengthModifier
            elif Entry.SkillNameVar.get().endswith("(DEX)"):
                AbilityModifier = DexterityModifier
            elif Entry.SkillNameVar.get().endswith("(INT)"):
                AbilityModifier = IntelligenceModifier
            elif Entry.SkillNameVar.get().endswith("(WIS)"):
                AbilityModifier = WisdomModifier
            elif Entry.SkillNameVar.get().endswith("(CHA)"):
                AbilityModifier = CharismaModifier
            else:
                continue
            Entry.CalculateSkillModifier(AbilityModifier, ProficiencyModifier)

        # Calculate Preset Roll Modifiers
        for Entry in Inst["PresetRolls"].PresetRollsList:
            CalculatedModifierString = Entry.PresetRollModifierEntryStatModifierInst.GetPresetDiceRollModifier()
            CurrentModifierString = Entry.PresetRollModifierEntryVar.get()
            if CalculatedModifierString not in ["", CurrentModifierString]:
                Entry.PresetRollModifierEntryVar.set(CalculatedModifierString)

        # Calculate AC
        self.CombatAndFeaturesInst.ACEntryVar.set(str(self.CombatAndFeaturesInst.ACEntryStatModifierInst.GetModifier()))

        # Calculate Max HP
        self.CombatAndFeaturesInst.CalculateMaxHP(ConstitutionModifier, CharacterLevelValue)

        # Calculate Initiative Bonus
        InitiativeStatModifier = self.CombatAndFeaturesInst.InitiativeEntryStatModifierInst.GetModifier()
        TotalInitiativeBonus = InitiativeStatModifier + DexterityModifier
        InitiativeBonusSign = ""
        if TotalInitiativeBonus > 0:
            InitiativeBonusSign = "+"
        self.CombatAndFeaturesInst.InitiativeEntryVar.set(InitiativeBonusSign + str(TotalInitiativeBonus))

        # Calculate Ability Score Derivatives
        AllAbilityScoreDerivativesList = self.CombatAndFeaturesInst.AbilityScoreDerivativesList + self.SpellcastingInst.SpellcastingAbilitiesList
        for Ability in AllAbilityScoreDerivativesList:
            AbilityScore = Ability.AbilityScoreSelectionDropdownVar.get()
            AbilityModifier = 0
            AttackModifierStatModifier = Ability.AttackModifierEntryStatModifierInst.GetModifier()
            SaveDCStatModifier = Ability.SaveDCEntryStatModifierInst.GetModifier()
            if AbilityScore != "":
                if AbilityScore == "STR":
                    AbilityModifier = StrengthModifier
                elif AbilityScore == "DEX":
                    AbilityModifier = DexterityModifier
                elif AbilityScore == "CON":
                    AbilityModifier = ConstitutionModifier
                elif AbilityScore == "INT":
                    AbilityModifier = IntelligenceModifier
                elif AbilityScore == "WIS":
                    AbilityModifier = WisdomModifier
                elif AbilityScore == "CHA":
                    AbilityModifier = CharismaModifier
                AttackModifier = AbilityModifier + ProficiencyModifier + AttackModifierStatModifier
                AttackModifierSign = ""
                if AttackModifier > 0:
                    AttackModifierSign = "+"
                Ability.AttackModifierEntryVar.set(AttackModifierSign + str(AttackModifier))
                SaveDC = AbilityModifier + ProficiencyModifier + SaveDCStatModifier + 8
                Ability.SaveDCEntryVar.set(str(SaveDC))
            elif AbilityScore == "":
                Ability.AttackModifierEntryVar.set("N/A")
                Ability.SaveDCEntryVar.set("N/A")

        # Calculate Passive Perception and Investigation
        PassivePerceptionStatModifier = self.AbilitiesAndSkillsInst.PassivePerceptionStatModifierInst.GetModifier()
        PassiveInvestigationStatModifier = self.AbilitiesAndSkillsInst.PassiveInvestigationStatModifierInst.GetModifier()
        PerceptionBonus = GlobalInst.GetStringVarAsNumber(Inst["Skills"].SkillsEntryPerceptionInst.TotalModifierVar)
        InvestigationBonus = GlobalInst.GetStringVarAsNumber(Inst["Skills"].SkillsEntryInvestigationInst.TotalModifierVar)
        ObservantBonus = 0
        if self.ObservantBoxVar.get():
            ObservantBonus += 5
        PassivePerceptionTotalBonus = str(10 + PerceptionBonus + PassivePerceptionStatModifier + ObservantBonus)
        PassiveInvestigationTotalBonus = str(10 + InvestigationBonus + PassiveInvestigationStatModifier + ObservantBonus)
        self.AbilitiesAndSkillsInst.PassivePerceptionEntryVar.set(PassivePerceptionTotalBonus)
        self.AbilitiesAndSkillsInst.PassiveInvestigationEntryVar.set(PassiveInvestigationTotalBonus)

        # Calculate Spell Points
        self.SpellcastingInst.CalculateSpellPoints()

        # Calculate Inventory
        self.InventoryInst.Calculate()

        # Update Window Title
        WindowInst.UpdateWindowTitle()

    def Settings(self):
        # Create Config Window and Wait
        SettingsMenuInst = self.SettingsMenu(WindowInst, self.SettingsMenuVars)
        WindowInst.wait_window(SettingsMenuInst.Window)

        # Handle Variables
        if SettingsMenuInst.DataSubmitted.get():
            for Tag, Var in SettingsMenuInst.Vars.items():
                self.SettingsMenuVars[Tag].set(Var.get())
            self.SpellcasterToggle()
            self.PortraitToggle()

        # Update Stats and Inventory
        self.UpdateStatsAndInventory()

    def SpellcasterToggle(self):
        Spellcaster = self.SpellcasterBoxVar.get()
        if Spellcaster:
            self.CharacterStatsNotebook.add(self.SpellcastingPage)
        if not Spellcaster:
            self.CharacterStatsNotebook.hide(2)

    def PortraitToggle(self):
        Portrait = self.PortraitBoxVar.get()
        if Portrait:
            self.CharacterStatsNotebook.add(self.PortraitPage)
        if not Portrait:
            self.CharacterStatsNotebook.hide(6)

    # Abilities and Skills
    class AbilitiesAndSkills:
        def __init__(self, master):
            self.PassivePerceptionEntryVar = StringVar()
            self.PassiveInvestigationEntryVar = StringVar()

            # Center Abilities, Saving Throws, and Skills
            master.grid_rowconfigure(3, weight=1)
            master.grid_columnconfigure(0, weight=1)
            master.grid_columnconfigure(2, weight=1)
            master.grid_columnconfigure(4, weight=1)
            master.grid_columnconfigure(6, weight=1)

            # Abilities and Saving Throws
            self.AbilitiesAndSavingThrowsInst = self.AbilitiesAndSavingThrowsTable(master)
            Inst["AbilitiesAndSavingThrows"] = self.AbilitiesAndSavingThrowsInst

            # Passive Scores
            self.PassiveScoresFrame = LabelFrame(master, text="Passive Scores:")
            self.PassiveScoresFrame.grid_columnconfigure(0, weight=1)
            self.PassiveScoresFrame.grid_columnconfigure(1, weight=1)
            self.PassiveScoresFrame.grid_rowconfigure(1, weight=1)
            self.PassiveScoresFrame.grid(row=3, column=1, padx=2, pady=2, sticky=NSEW)
            self.PassivePerceptionHeader = Label(self.PassiveScoresFrame, text="Perception", bd=2, relief=GROOVE)
            self.PassivePerceptionHeader.grid(row=0, column=0, sticky=NSEW)
            self.PassivePerceptionEntry = EntryExtended(self.PassiveScoresFrame, justify=CENTER, width=20, textvariable=self.PassivePerceptionEntryVar)
            self.PassivePerceptionEntry.grid(row=1, column=0, sticky=NSEW)
            self.PassivePerceptionStatModifierInst = StatModifier(self.PassivePerceptionEntry, "<Button-1>", "Left-click on Passive Perception to set a stat modifier.", "Passive Perception", Prefix="PassivePerception")
            self.PassiveInvestigationHeader = Label(self.PassiveScoresFrame, text="Investigation", bd=2, relief=GROOVE)
            self.PassiveInvestigationHeader.grid(row=0, column=1, sticky=NSEW)
            self.PassiveInvestigationEntry = EntryExtended(self.PassiveScoresFrame, justify=CENTER, width=20, textvariable=self.PassiveInvestigationEntryVar)
            self.PassiveInvestigationEntry.grid(row=1, column=1, sticky=NSEW)
            self.PassiveInvestigationStatModifierInst = StatModifier(self.PassiveInvestigationEntry, "<Button-1>", "Left-click on Passive Investigation to set a stat modifier.", "Passive Investigation",
                                                                     Prefix="PassiveInvestigation")

            # Skills
            self.SkillsInst = self.SkillsTable(master)
            Inst["Skills"] = self.SkillsInst

            # Proficiencies Frame
            self.ProficienciesFrame = LabelFrame(master, text="Proficiencies:")
            self.ProficienciesFrame.grid(row=1, column=5, padx=2, pady=2, rowspan=5, sticky=NSEW)

            # Weapon Proficiencies
            self.ProficienciesWeaponsHeader = Label(self.ProficienciesFrame, text="Weapons", bd=2, relief=GROOVE)
            self.ProficienciesWeaponsHeader.grid(row=0, column=0, sticky=NSEW)
            self.ProficienciesWeaponsFieldFrame = Frame(self.ProficienciesFrame)
            self.ProficienciesWeaponsFieldFrame.grid(row=1, column=0)
            self.ProficienciesWeaponsField = ScrolledText(self.ProficienciesWeaponsFieldFrame, Width=130, Height=73, SavedDataTag="ProficienciesWeaponsField")
            self.ProficienciesWeaponsField.grid(row=0, column=0)

            # Armor Proficiencies
            self.ProficienciesArmorHeader = Label(self.ProficienciesFrame, text="Armor", bd=2, relief=GROOVE)
            self.ProficienciesArmorHeader.grid(row=2, column=0, sticky=NSEW)
            self.ProficienciesArmorFieldFrame = Frame(self.ProficienciesFrame)
            self.ProficienciesArmorFieldFrame.grid(row=3, column=0)
            self.ProficienciesArmorField = ScrolledText(self.ProficienciesArmorFieldFrame, Width=130, Height=73, SavedDataTag="ProficienciesArmorField")
            self.ProficienciesArmorField.grid(row=0, column=0)

            # Tool and Instrument Proficiencies
            self.ProficienciesToolsAndInstrumentsHeader = Label(self.ProficienciesFrame, text="Tools and Instruments", bd=2, relief=GROOVE)
            self.ProficienciesToolsAndInstrumentsHeader.grid(row=4, column=0, sticky=NSEW)
            self.ProficienciesToolsAndInstrumentsFieldFrame = Frame(self.ProficienciesFrame)
            self.ProficienciesToolsAndInstrumentsFieldFrame.grid(row=5, column=0)
            self.ProficienciesToolsAndInstrumentsField = ScrolledText(self.ProficienciesToolsAndInstrumentsFieldFrame, Width=130, Height=73, SavedDataTag="ProficienciesToolsAndInstrumentsField")
            self.ProficienciesToolsAndInstrumentsField.grid(row=0, column=0)

            # Language Proficiencies
            self.ProficienciesLanguagesHeader = Label(self.ProficienciesFrame, text="Languages", bd=2, relief=GROOVE)
            self.ProficienciesLanguagesHeader.grid(row=6, column=0, sticky=NSEW)
            self.ProficienciesLanguagesFieldFrame = Frame(self.ProficienciesFrame)
            self.ProficienciesLanguagesFieldFrame.grid(row=7, column=0)
            self.ProficienciesLanguagesField = ScrolledText(self.ProficienciesLanguagesFieldFrame, Width=130, Height=73, SavedDataTag="ProficienciesLanguagesField")
            self.ProficienciesLanguagesField.grid(row=0, column=0)

            # Other Proficiencies
            self.ProficienciesOtherHeader = Label(self.ProficienciesFrame, text="Other", bd=2, relief=GROOVE)
            self.ProficienciesOtherHeader.grid(row=8, column=0, sticky=NSEW)
            self.ProficienciesOtherFieldFrame = Frame(self.ProficienciesFrame)
            self.ProficienciesOtherFieldFrame.grid(row=9, column=0)
            self.ProficienciesOtherField = ScrolledText(self.ProficienciesOtherFieldFrame, Width=130, Height=73, SavedDataTag="ProficienciesOtherField")
            self.ProficienciesOtherField.grid(row=0, column=0)

        # Abilities and Saving Throws
        class AbilitiesAndSavingThrowsTable:
            def __init__(self, master):
                # Abilities and Saving Throws Frame
                self.AbilitiesAndSavingThrowsFrame = LabelFrame(master, text="Abilities and Saving Throws:")
                self.AbilitiesAndSavingThrowsFrame.grid_columnconfigure(0, weight=1)
                self.AbilitiesAndSavingThrowsFrame.grid(row=1, column=1, padx=2, pady=2)

                # Table Frame
                self.TableFrame = Frame(self.AbilitiesAndSavingThrowsFrame)
                self.TableFrame.grid_columnconfigure(3, weight=1)
                self.TableFrame.grid(row=0, column=0, sticky=NSEW)

                # Labels
                self.AbilitiesHeaderAbility = Label(self.TableFrame, text="Ability", bd=2, relief=GROOVE)
                self.AbilitiesHeaderAbility.grid(row=0, column=0, sticky=NSEW)
                self.AbilitiesHeaderTotal = Label(self.TableFrame, text="Total", bd=2, relief=GROOVE)
                self.AbilitiesHeaderTotal.grid(row=0, column=1, sticky=NSEW)
                self.AbilitiesHeaderModifier = Label(self.TableFrame, text="Modifier", bd=2, relief=GROOVE)
                self.AbilitiesHeaderModifier.grid(row=0, column=2, sticky=NSEW)
                self.AbilitiesHeaderSavingThrowsProf = Label(self.TableFrame, text="Prof.", bd=2, relief=GROOVE)
                self.AbilitiesHeaderSavingThrowsProf.grid(row=0, column=4, sticky=NSEW)
                self.AbilitiesHeaderSavingThrows = Label(self.TableFrame, text="Saving Throws", bd=2, relief=GROOVE)
                self.AbilitiesHeaderSavingThrows.grid(row=0, column=5, sticky=NSEW)

                # Ability Entries List
                self.AbilityEntriesList = []

                # Ability Entries
                self.StrengthEntry = self.AbilitiesAndSavingThrowsEntry(self.TableFrame, "Strength", self.AbilityEntriesList, 1)
                self.DexterityEntry = self.AbilitiesAndSavingThrowsEntry(self.TableFrame, "Dexterity", self.AbilityEntriesList, 2)
                self.ConstitutionEntry = self.AbilitiesAndSavingThrowsEntry(self.TableFrame, "Constitution", self.AbilityEntriesList, 3)
                self.IntelligenceEntry = self.AbilitiesAndSavingThrowsEntry(self.TableFrame, "Intelligence", self.AbilityEntriesList, 4)
                self.WisdomEntry = self.AbilitiesAndSavingThrowsEntry(self.TableFrame, "Wisdom", self.AbilityEntriesList, 5)
                self.CharismaEntry = self.AbilitiesAndSavingThrowsEntry(self.TableFrame, "Charisma", self.AbilityEntriesList, 6)

                # Abilities Data Config
                self.AbilitiesDataConfigButton = Button(self.AbilitiesAndSavingThrowsFrame, text="Abilities Data", command=self.ConfigureAbilitiesData, bg=GlobalInst.ButtonColor)
                self.AbilitiesDataConfigButton.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)

                # Abilities Notes
                self.AbilitiesNotesFrame = LabelFrame(self.AbilitiesAndSavingThrowsFrame, text="Abilities Notes:")
                self.AbilitiesNotesFrame.grid_columnconfigure(0, weight=1)
                self.AbilitiesNotesFrame.grid(row=2, column=0, padx=2, pady=2)
                self.AbilitiesNotes = ScrolledText(self.AbilitiesNotesFrame, Width=275, Height=180, SavedDataTag="AbilitiesNotes")
                self.AbilitiesNotes.grid(row=0, column=0)

            def ConfigureAbilitiesData(self):
                # Create Window and Wait
                AbilitiesDataConfigInst = self.AbilitiesDataConfig(WindowInst)
                WindowInst.wait_window(AbilitiesDataConfigInst.Window)

                # Handle Variables
                if AbilitiesDataConfigInst.DataSubmitted.get():
                    # Store Abilities Data
                    for Entry in AbilitiesDataConfigInst.EntriesList:
                        Entry.AbilityEntry.AbilityEntryTotalVar.set(Entry.AbilityTotalVar.get())
                        Entry.AbilityEntry.AbilityBaseVar.set(Entry.AbilityBaseVar.get())
                        Entry.AbilityEntry.AbilityRacialVar.set(Entry.AbilityRacialVar.get())
                        Entry.AbilityEntry.AbilityASIVar.set(Entry.AbilityASIVar.get())
                        Entry.AbilityEntry.AbilityMiscVar.set(Entry.AbilityMiscVar.get())
                        Entry.AbilityEntry.AbilityOverrideVar.set(Entry.AbilityOverrideVar.get())

                # Update Stats
                CharacterSheetInst.UpdateStatsAndInventory()

            class AbilitiesAndSavingThrowsEntry:
                def __init__(self, master, AbilityName, List, Row):
                    # Store Parameters
                    self.AbilityName = AbilityName
                    self.Row = Row

                    # Variables
                    self.AbilityNameVar = StringVar(value=self.AbilityName)
                    self.AbilityEntryTotalVar = SavedStringVar(self.AbilityName + "AbilityEntryTotalVar", DefaultValue="8")
                    self.AbilityEntryModifierVar = StringVar()
                    self.AbilitySavingThrowProficiencyBoxVar = SavedBooleanVar(self.AbilityName + "AbilitySavingThrowProficiencyBoxVar")
                    self.AbilitySavingThrowProficiencyBoxVar.trace_add("write", lambda a, b, c: CharacterSheetInst.UpdateStatsAndInventory())
                    self.AbilitySavingThrowModifierVar = StringVar()

                    # Config Variables
                    self.AbilityBaseVar = SavedStringVar(self.AbilityName + "AbilityBaseVar", DefaultValue="8")
                    self.AbilityRacialVar = SavedStringVar(self.AbilityName + "AbilityRacialVar")
                    self.AbilityASIVar = SavedStringVar(self.AbilityName + "AbilityASIVar")
                    self.AbilityMiscVar = SavedStringVar(self.AbilityName + "AbilityMiscVar")
                    self.AbilityOverrideVar = SavedStringVar(self.AbilityName + "AbilityOverrideVar")

                    # Add to List
                    List.append(self)

                    # Label
                    self.AbilityLabel = Label(master, textvariable=self.AbilityNameVar)
                    self.AbilityLabel.grid(row=self.Row, column=0, sticky=NSEW)

                    # Total Entry
                    self.AbilityEntryTotal = EntryExtended(master, width=3, justify=CENTER, textvariable=self.AbilityEntryTotalVar, state=DISABLED, disabledbackground="light gray", disabledforeground="black",
                                                           cursor="arrow")
                    self.AbilityEntryTotal.grid(row=self.Row, column=1, sticky=NSEW)

                    # Ability And Saving Throw Tooltip String
                    self.AbilityAndSavingThrowTooltipString = "Left-click on an ability or saving throw modifier to roll 1d20 with it.  Right-click to set a stat modifier."

                    # Modifier Entry
                    self.AbilityEntryModifier = EntryExtended(master, width=3, justify=CENTER, textvariable=self.AbilityEntryModifierVar, cursor="dotbox")
                    self.AbilityEntryModifier.grid(row=self.Row, column=2, sticky=NSEW)
                    self.AbilityEntryModifierStatModifierInst = StatModifier(self.AbilityEntryModifier, "<Button-3>", self.AbilityAndSavingThrowTooltipString, self.AbilityName + " Modifier", Cursor="dotbox",
                                                                             Prefix=self.AbilityName + "AbilityEntryModifier")
                    self.AbilityEntryModifier.bind("<Button-1>", self.RollAbility)

                    # Saving Throw Proficiency Box
                    self.AbilitySavingThrowProficiencyBox = Checkbutton(master, variable=self.AbilitySavingThrowProficiencyBoxVar)
                    self.AbilitySavingThrowProficiencyBox.grid(row=self.Row, column=4, sticky=NSEW)

                    # Saving Throw Modifier Entry
                    self.AbilitySavingThrowModifier = EntryExtended(master, width=3, justify=CENTER, textvariable=self.AbilitySavingThrowModifierVar, cursor="dotbox")
                    self.AbilitySavingThrowModifier.grid(row=self.Row, column=5, sticky=NSEW)
                    self.AbilitySavingThrowModifierStatModifierInst = StatModifier(self.AbilitySavingThrowModifier, "<Button-3>", self.AbilityAndSavingThrowTooltipString, self.AbilityName + " Saving Throw", Cursor="dotbox",
                                                                                   Prefix=self.AbilityName + "AbilitySavingThrowModifier")
                    self.AbilitySavingThrowModifier.bind("<Button-1>", self.RollSavingThrow)

                def CalculateModifiers(self, ProficiencyBonus):
                    BaseAbilityModifier = int(math.floor((int(self.AbilityEntryTotalVar.get()) - 10) / 2))
                    AbilityModifier = BaseAbilityModifier + self.AbilityEntryModifierStatModifierInst.GetModifier()
                    AbilityModifierSign = ""
                    if AbilityModifier >= 1:
                        AbilityModifierSign = "+"
                    AbilityModifierString = AbilityModifierSign + str(AbilityModifier)
                    SavingThrowModifier = BaseAbilityModifier + self.AbilitySavingThrowModifierStatModifierInst.GetModifier()
                    if self.AbilitySavingThrowProficiencyBoxVar.get():
                        SavingThrowModifier += ProficiencyBonus
                    SavingThrowSign = ""
                    if SavingThrowModifier >= 1:
                        SavingThrowSign = "+"
                    SavingThrowModifierString = SavingThrowSign + str(SavingThrowModifier)
                    self.AbilityEntryModifierVar.set(AbilityModifierString)
                    self.AbilitySavingThrowModifierVar.set(SavingThrowModifierString)

                def RollAbility(self, event):
                    BaseModifier = GlobalInst.GetStringVarAsNumber(self.AbilityEntryModifierVar)
                    JackOfAllTradesModifier = BaseModifier
                    RemarkableAthleteModifier = BaseModifier
                    ProficiencyBonus = GlobalInst.GetStringVarAsNumber(CharacterSheetInst.ProficiencyBonusEntryVar)
                    AbilityName = self.AbilityNameVar.get()
                    if CharacterSheetInst.RemarkableAthleteBoxVar.get():
                        if AbilityName == "Strength" or AbilityName == "Dexterity" or AbilityName == "Constitution":
                            RemarkableAthleteModifier += math.ceil(ProficiencyBonus / 2)
                    if CharacterSheetInst.JackOfAllTradesBoxVar.get():
                        JackOfAllTradesModifier += math.floor(ProficiencyBonus / 2)
                    FinalModifier = max(BaseModifier, RemarkableAthleteModifier, JackOfAllTradesModifier)
                    DiceRollerInst.DiceNumberEntryVar.set(1)
                    DiceRollerInst.DieTypeEntryVar.set(20)
                    DiceRollerInst.ModifierEntryVar.set(str(FinalModifier))
                    DiceRollerInst.Roll(self.AbilityNameVar.get() + " Ability Check:\n")

                def RollSavingThrow(self, event):
                    DiceRollerInst.DiceNumberEntryVar.set(1)
                    DiceRollerInst.DieTypeEntryVar.set(20)
                    DiceRollerInst.ModifierEntryVar.set(str(GlobalInst.GetStringVarAsNumber(self.AbilitySavingThrowModifierVar)))
                    DiceRollerInst.Roll(self.AbilityNameVar.get() + " Saving Throw:\n")

            class AbilitiesDataConfig:
                def __init__(self, master):
                    # Variables
                    self.DataSubmitted = BooleanVar()
                    self.RollButtonVar = BooleanVar()
                    self.PointBuyButtonVar = BooleanVar()
                    self.RollForAbilitiesMenuInst = None
                    self.PointBuyMenuInst = None
                    self.RollForAbilitiesWidthOffset = 163
                    self.PointBuyWidthOffset = 138

                    # Create Window
                    self.Window = Toplevel(master)
                    self.Window.wm_attributes("-toolwindow", 1)
                    self.Window.wm_title("Abilities Data")

                    # Labels
                    self.HeaderLabelAbility = Label(self.Window, text="Ability", bd=2, relief=GROOVE)
                    self.HeaderLabelAbility.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
                    self.HeaderLabelBase = Label(self.Window, text="Base", bd=2, relief=GROOVE)
                    self.HeaderLabelBase.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
                    self.HeaderLabelRacial = Label(self.Window, text="Racial", bd=2, relief=GROOVE)
                    self.HeaderLabelRacial.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
                    self.HeaderLabelASI = Label(self.Window, text="ASI", bd=2, relief=GROOVE)
                    self.HeaderLabelASI.grid(row=0, column=3, sticky=NSEW, padx=2, pady=2)
                    self.HeaderLabelMisc = Label(self.Window, text="Misc.", bd=2, relief=GROOVE)
                    self.HeaderLabelMisc.grid(row=0, column=4, sticky=NSEW, padx=2, pady=2)
                    self.HeaderLabelOverride = Label(self.Window, text="Override", bd=2, relief=GROOVE)
                    self.HeaderLabelOverride.grid(row=0, column=5, sticky=NSEW, padx=2, pady=2)
                    self.HeaderLabelTotal = Label(self.Window, text="Total", bd=2, relief=GROOVE)
                    self.HeaderLabelTotal.grid(row=0, column=6, sticky=NSEW, padx=2, pady=2)

                    # Entries List
                    self.EntriesList = []

                    # Entries
                    self.StrengthConfigEntry = self.AbilitiesDataConfigEntry(self.Window, Inst["AbilitiesAndSavingThrows"].StrengthEntry, "STR", self.EntriesList, 1)
                    self.DexterityConfigEntry = self.AbilitiesDataConfigEntry(self.Window, Inst["AbilitiesAndSavingThrows"].DexterityEntry, "DEX", self.EntriesList, 2)
                    self.ConstitutionConfigEntry = self.AbilitiesDataConfigEntry(self.Window, Inst["AbilitiesAndSavingThrows"].ConstitutionEntry, "CON", self.EntriesList, 3)
                    self.IntelligenceConfigEntry = self.AbilitiesDataConfigEntry(self.Window, Inst["AbilitiesAndSavingThrows"].IntelligenceEntry, "INT", self.EntriesList, 4)
                    self.WisdomConfigEntry = self.AbilitiesDataConfigEntry(self.Window, Inst["AbilitiesAndSavingThrows"].WisdomEntry, "WIS", self.EntriesList, 5)
                    self.CharismaConfigEntry = self.AbilitiesDataConfigEntry(self.Window, Inst["AbilitiesAndSavingThrows"].CharismaEntry, "CHA", self.EntriesList, 6)

                    # Entry Validation and Calculation
                    for Entry in self.EntriesList:
                        Entry.AbilityEntryBase.ConfigureValidation(
                            lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Base score must be a whole number.", MinValue=1, LessThanMinString="Base score cannot be less than 1."), "key")
                        Entry.AbilityEntryRacial.ConfigureValidation(lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Racial bonus must be a whole number."), "key")
                        Entry.AbilityEntryASI.ConfigureValidation(lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Ability score increase must be a whole number."), "key")
                        Entry.AbilityEntryMisc.ConfigureValidation(lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Miscellaneous bonus must be a whole number."), "key")
                        Entry.AbilityEntryOverride.ConfigureValidation(
                            lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Override must be a whole number.", MinValue=1, LessThanMinString="Override cannot be less than 1.  Leave blank to remove override."), "key")
                        Entry.AbilityBaseVar.trace_add("write", lambda a, b, c: self.Calculate())
                        Entry.AbilityRacialVar.trace_add("write", lambda a, b, c: self.Calculate())
                        Entry.AbilityASIVar.trace_add("write", lambda a, b, c: self.Calculate())
                        Entry.AbilityMiscVar.trace_add("write", lambda a, b, c: self.Calculate())
                        Entry.AbilityOverrideVar.trace_add("write", lambda a, b, c: self.Calculate())

                    # Side Buttons
                    self.SideButtonsFrame = Frame(self.Window)
                    self.SideButtonsFrame.grid_rowconfigure(0, weight=1)
                    self.SideButtonsFrame.grid_rowconfigure(1, weight=1)
                    self.SideButtonsFrame.grid(row=0, column=7, rowspan=7, sticky=NSEW)
                    self.RollButton = Checkbutton(self.SideButtonsFrame, text="Roll", variable=self.RollButtonVar, command=lambda: self.CreateRollForAbilitiesMenu(True), bg=GlobalInst.ButtonColor, indicatoron=False,
                                                  selectcolor=GlobalInst.ButtonColor)
                    self.RollButton.grid(row=0, column=7, padx=2, pady=2, sticky=NSEW)
                    self.PointBuyButton = Checkbutton(self.SideButtonsFrame, text="Point Buy", variable=self.PointBuyButtonVar, command=lambda: self.CreatePointBuyMenu(True), bg=GlobalInst.ButtonColor, indicatoron=False,
                                                      selectcolor=GlobalInst.ButtonColor)
                    self.PointBuyButton.grid(row=1, column=7, padx=2, pady=2, sticky=NSEW)

                    # Bottom Buttons
                    self.BottomButtonsFrame = Frame(self.Window)
                    self.BottomButtonsFrame.grid_columnconfigure(0, weight=1)
                    self.BottomButtonsFrame.grid_columnconfigure(1, weight=1)
                    self.BottomButtonsFrame.grid(row=7, column=0, columnspan=8, sticky=NSEW)
                    self.SubmitButton = Button(self.BottomButtonsFrame, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
                    self.SubmitButton.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)
                    self.CancelButton = Button(self.BottomButtonsFrame, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
                    self.CancelButton.grid(row=0, column=1, padx=2, pady=2, sticky=NSEW)

                    # Prevent Main Window Input
                    self.Window.grab_set()

                    # Handle Config Window Geometry and Focus
                    GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst)
                    self.Window.focus_force()

                    # Focus on Strength Entry
                    self.StrengthConfigEntry.AbilityEntryBase.focus_set()

                def Calculate(self):
                    EntriesCalculated = True
                    for Entry in self.EntriesList:
                        if Entry.Calculate():
                            pass
                        else:
                            EntriesCalculated = False
                    if not EntriesCalculated:
                        return False
                    return True

                def Submit(self):
                    if self.Calculate():
                        pass
                    else:
                        messagebox.showerror("Invalid Entry", "Not valid ability scores!")
                        return
                    self.DataSubmitted.set(True)
                    self.Window.destroy()

                def Cancel(self):
                    self.DataSubmitted.set(False)
                    self.Window.destroy()

                def CreateRollForAbilitiesMenu(self, Pressed):
                    if self.PointBuyButtonVar.get() and Pressed:
                        self.PointBuyButtonVar.set(False)
                        self.CreatePointBuyMenu(not Pressed)
                    if self.RollButtonVar.get():
                        # Create Menu
                        self.RollForAbilitiesMenuInst = self.RollForAbilitiesMenu(self.Window, self)

                        # Adjust Geometry
                        GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst, WidthOffset=self.RollForAbilitiesWidthOffset)
                    else:
                        # Destroy Menu
                        if self.RollForAbilitiesMenuInst is not None:
                            self.RollForAbilitiesMenuInst.RollForAbilitiesFrame.destroy()

                        # Adjust Geometry
                        GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst, WidthOffset=-self.RollForAbilitiesWidthOffset)

                def CreatePointBuyMenu(self, Pressed):
                    if self.RollButtonVar.get() and Pressed:
                        self.RollButtonVar.set(False)
                        self.CreateRollForAbilitiesMenu(not Pressed)
                    if self.PointBuyButtonVar.get():
                        # Create Menu
                        self.PointBuyMenuInst = self.PointBuyMenu(self.Window, self)

                        # Adjust Geometry
                        GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst, WidthOffset=self.PointBuyWidthOffset)
                    else:
                        # Destroy Menu
                        if self.PointBuyMenuInst is not None:
                            self.PointBuyMenuInst.PointBuyFrame.destroy()

                        # Adjust Geometry
                        GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst, WidthOffset=-self.PointBuyWidthOffset)

                class AbilitiesDataConfigEntry:
                    def __init__(self, master, AbilityEntry, AbilityNameShort, List, Row):
                        self.AbilityEntry = AbilityEntry
                        self.AbilityNameVar = StringVar(value=self.AbilityEntry.AbilityNameVar.get())
                        self.AbilityNameShort = AbilityNameShort
                        self.AbilityBaseVar = StringVar(value=self.AbilityEntry.AbilityBaseVar.get())
                        self.AbilityRacialVar = StringVar(value=self.AbilityEntry.AbilityRacialVar.get())
                        self.AbilityASIVar = StringVar(value=self.AbilityEntry.AbilityASIVar.get())
                        self.AbilityMiscVar = StringVar(value=self.AbilityEntry.AbilityMiscVar.get())
                        self.AbilityOverrideVar = StringVar(value=self.AbilityEntry.AbilityOverrideVar.get())
                        self.AbilityTotalVar = StringVar(value=self.AbilityEntry.AbilityEntryTotalVar.get())

                        # Add to List
                        List.append(self)

                        # Label
                        self.AbilityLabel = Label(master, textvariable=self.AbilityNameVar)
                        self.AbilityLabel.grid(row=Row, column=0, sticky=NSEW, padx=2, pady=2)

                        # Base Entry
                        self.AbilityEntryBase = EntryExtended(master, width=9, justify=CENTER, textvariable=self.AbilityBaseVar)
                        self.AbilityEntryBase.grid(row=Row, column=1, sticky=NSEW, padx=2, pady=2)

                        # Racial Entry
                        self.AbilityEntryRacial = EntryExtended(master, width=9, justify=CENTER, textvariable=self.AbilityRacialVar)
                        self.AbilityEntryRacial.grid(row=Row, column=2, sticky=NSEW, padx=2, pady=2)

                        # ASI Entry
                        self.AbilityEntryASI = EntryExtended(master, width=9, justify=CENTER, textvariable=self.AbilityASIVar)
                        self.AbilityEntryASI.grid(row=Row, column=3, sticky=NSEW, padx=2, pady=2)

                        # Misc. Entry
                        self.AbilityEntryMisc = EntryExtended(master, width=9, justify=CENTER, textvariable=self.AbilityMiscVar)
                        self.AbilityEntryMisc.grid(row=Row, column=4, sticky=NSEW, padx=2, pady=2)

                        # Override Entry
                        self.AbilityEntryOverride = EntryExtended(master, width=9, justify=CENTER, textvariable=self.AbilityOverrideVar)
                        self.AbilityEntryOverride.grid(row=Row, column=5, sticky=NSEW, padx=2, pady=2)

                        # Total Entry
                        self.AbilityEntryTotal = EntryExtended(master, width=9, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow",
                                                               textvariable=self.AbilityTotalVar)
                        self.AbilityEntryTotal.grid(row=Row, column=6, sticky=NSEW, padx=2, pady=2)

                    def Calculate(self):
                        AbilityBaseString = self.AbilityBaseVar.get()
                        if AbilityBaseString == "" or AbilityBaseString == "+" or AbilityBaseString == "-":
                            self.AbilityTotalVar.set("N/A")
                            self.AbilityEntryTotal.configure(disabledforeground="red")
                            return False
                        Base = GlobalInst.GetStringVarAsNumber(self.AbilityBaseVar)
                        Racial = GlobalInst.GetStringVarAsNumber(self.AbilityRacialVar)
                        ASI = GlobalInst.GetStringVarAsNumber(self.AbilityASIVar)
                        Misc = GlobalInst.GetStringVarAsNumber(self.AbilityMiscVar)
                        Override = GlobalInst.GetStringVarAsNumber(self.AbilityOverrideVar)
                        if Override > 0:
                            Total = Override
                        else:
                            Total = Base + Racial + ASI + Misc
                        self.AbilityTotalVar.set(Total)
                        if Total < 1:
                            self.AbilityEntryTotal.configure(disabledforeground="red")
                            return False
                        else:
                            self.AbilityEntryTotal.configure(disabledforeground="black")
                        return True

                class RollForAbilitiesMenu:
                    def __init__(self, master, AbilitiesDataConfigInst):
                        # Store Parameters
                        self.master = master
                        self.AbilitiesDataConfigInst = AbilitiesDataConfigInst

                        # Variables
                        self.DataSubmitted = BooleanVar()
                        self.Rolled = False
                        self.RollForAbilitiesWidthOffset = self.AbilitiesDataConfigInst.RollForAbilitiesWidthOffset

                        # Frame
                        self.RollForAbilitiesFrame = Frame(master)
                        self.RollForAbilitiesFrame.grid_rowconfigure(3, weight=1)
                        self.RollForAbilitiesFrame.grid(row=0, column=8, rowspan=8, sticky=NSEW)

                        # Roll Assign Fields List
                        self.RollAssignFieldsList = []

                        # Roll Assign Fields
                        self.RollAssignField1Inst = self.RollAssignField(self.RollForAbilitiesFrame, self.RollAssignFieldsList, Row=0, Column=0)
                        self.RollAssignField2Inst = self.RollAssignField(self.RollForAbilitiesFrame, self.RollAssignFieldsList, Row=0, Column=1)
                        self.RollAssignField3Inst = self.RollAssignField(self.RollForAbilitiesFrame, self.RollAssignFieldsList, Row=1, Column=0)
                        self.RollAssignField4Inst = self.RollAssignField(self.RollForAbilitiesFrame, self.RollAssignFieldsList, Row=1, Column=1)
                        self.RollAssignField5Inst = self.RollAssignField(self.RollForAbilitiesFrame, self.RollAssignFieldsList, Row=2, Column=0)
                        self.RollAssignField6Inst = self.RollAssignField(self.RollForAbilitiesFrame, self.RollAssignFieldsList, Row=2, Column=1)
                        for Field in self.RollAssignFieldsList:
                            Field.RollDropdown.bind("<Return>", self.ReturnPressed)

                        # Buttons
                        self.RollScoresButton = Button(self.RollForAbilitiesFrame, text="Roll\nScores", command=self.RollScores, bg=GlobalInst.ButtonColor)
                        self.RollScoresButton.grid(row=0, column=2, rowspan=3, padx=2, pady=2, sticky=NSEW)
                        self.AcceptButton = Button(self.RollForAbilitiesFrame, text="Accept", command=self.Accept, bg=GlobalInst.ButtonColor)
                        self.AcceptButton.grid(row=3, column=0, columnspan=3, padx=2, pady=2, sticky=NSEW)

                        # Set Focus
                        self.RollAssignField1Inst.RollDropdown.focus_set()

                    def Accept(self):
                        if self.ValidEntry():
                            pass
                        else:
                            return
                        self.AbilitiesDataConfigInst.RollButtonVar.set(False)
                        for Assignment in self.RollAssignFieldsList:
                            for Entry in self.AbilitiesDataConfigInst.EntriesList:
                                RollLabelString = Assignment.RollLabelVar.get()
                                RollDropdownString = Assignment.RollDropdownVar.get()
                                if Entry.AbilityNameShort == RollDropdownString:
                                    Entry.AbilityBaseVar.set(RollLabelString)
                        self.RollForAbilitiesFrame.destroy()
                        GlobalInst.WindowGeometry(self.master, IsDialog=True, DialogMaster=WindowInst, WidthOffset=-self.RollForAbilitiesWidthOffset)

                    def RollScores(self):
                        for Field in self.RollAssignFieldsList:
                            Rolls = []
                            Total = 0
                            for Roll in range(4):
                                Rolls.append(DiceRollerInst.IntRoll(1, 6, 0))
                            Rolls.remove(min(Rolls))
                            for Roll in Rolls:
                                Total += Roll
                            Field.RollLabelVar.set(str(Total))
                        self.Rolled = True
                        self.RollAssignField1Inst.RollDropdown.focus_set()

                    def ReturnPressed(self, Event):
                        if not self.Rolled:
                            self.RollScores()
                        else:
                            self.Accept()

                    def ValidEntry(self):
                        if self.Rolled:
                            pass
                        else:
                            messagebox.showerror("Invalid Entry", "No scores.")
                            return False
                        FieldAssignmentsList = []
                        for Field in self.RollAssignFieldsList:
                            if Field.RollDropdownVar.get() == "":
                                messagebox.showerror("Invalid Entry", "All scores must be assigned to an ability.")
                                return False
                            FieldAssignmentsList.append(Field.RollDropdownVar.get())
                        if len(FieldAssignmentsList) != len(set(FieldAssignmentsList)):
                            messagebox.showerror("Invalid Entry", "Scores cannot be assigned to the same ability.")
                            return False
                        return True

                    class RollAssignField:
                        def __init__(self, master, List, Row=0, Column=0):
                            # Store Parameters
                            self.Row = Row
                            self.Column = Column

                            # Variables
                            self.RollLabelVar = StringVar(value="-")
                            self.RollDropdownVar = StringVar()

                            # Add to List
                            List.append(self)

                            # Frame
                            self.FieldFrame = Frame(master)
                            self.FieldFrame.grid(row=self.Row, column=self.Column, sticky=NSEW)

                            # Label
                            self.RollLabel = Label(self.FieldFrame, textvariable=self.RollLabelVar, bd=2, relief=GROOVE)
                            self.RollLabel.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)

                            # Dropdown
                            self.RollDropdown = DropdownExtended(self.FieldFrame, textvariable=self.RollDropdownVar, values=["", "STR", "DEX", "CON", "INT", "WIS", "CHA"], width=5, state="readonly", justify=CENTER)
                            self.RollDropdown.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)

                class PointBuyMenu:
                    def __init__(self, master, AbilitiesDataConfigInst):
                        # Store Parameters
                        self.master = master
                        self.AbilitiesDataConfigInst = AbilitiesDataConfigInst

                        # Variables
                        self.DataSubmitted = BooleanVar()
                        self.PointBuyEntryVar = StringVar()
                        self.PointBuyWidthOffset = self.AbilitiesDataConfigInst.PointBuyWidthOffset

                        # Frame
                        self.PointBuyFrame = Frame(master)
                        self.PointBuyFrame.grid_rowconfigure(3, weight=1)
                        self.PointBuyFrame.grid(row=0, column=8, rowspan=8, sticky=NSEW)

                        # Point Buy Fields List
                        self.PointBuyFieldsList = []

                        # Point Buy Fields
                        self.PointBuyField1Inst = self.PointBuyField(self.PointBuyFrame, "STR", self.PointBuyFieldsList, Row=0, Column=0)
                        self.PointBuyField2Inst = self.PointBuyField(self.PointBuyFrame, "DEX", self.PointBuyFieldsList, Row=0, Column=1)
                        self.PointBuyField3Inst = self.PointBuyField(self.PointBuyFrame, "CON", self.PointBuyFieldsList, Row=1, Column=0)
                        self.PointBuyField4Inst = self.PointBuyField(self.PointBuyFrame, "INT", self.PointBuyFieldsList, Row=1, Column=1)
                        self.PointBuyField5Inst = self.PointBuyField(self.PointBuyFrame, "WIS", self.PointBuyFieldsList, Row=2, Column=0)
                        self.PointBuyField6Inst = self.PointBuyField(self.PointBuyFrame, "CHA", self.PointBuyFieldsList, Row=2, Column=1)
                        for Field in self.PointBuyFieldsList:
                            Field.ScoreEntryVar.trace_add("write", lambda a, b, c: self.Calculate())
                            Field.ScoreEntry.bind("<Return>", lambda event: self.Accept())

                        # Point Buy Values and Rules
                        self.PointBuyValuesAndRulesFrame = Frame(self.PointBuyFrame)
                        self.PointBuyValuesAndRulesFrame.grid_rowconfigure(2, weight=1)
                        self.PointBuyValuesAndRulesFrame.grid(row=0, column=2, rowspan=3, sticky=NSEW)
                        self.PointsLabel = Label(self.PointBuyValuesAndRulesFrame, text="Points", bd=2, relief=GROOVE)
                        self.PointsLabel.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)
                        self.PointBuyEntry = EntryExtended(self.PointBuyValuesAndRulesFrame, state=DISABLED, width=9, disabledbackground="light gray", disabledforeground="black", cursor="arrow", textvariable=self.PointBuyEntryVar,
                                                           justify=CENTER)
                        self.PointBuyEntry.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)
                        self.PointBuyRulesFont = font.Font(size=5)
                        self.PointBuyRulesLabel = Label(self.PointBuyValuesAndRulesFrame, text="Min Score:  8\nMax Score:  15\n\nCosts:\n8:  0\n9:  1\n10:  2\n11:  3\n12:  4\n13:  5\n14:  7\n15:  9", justify=LEFT, bd=2,
                                                        relief=GROOVE, wraplength=200, font=self.PointBuyRulesFont)
                        self.PointBuyRulesLabel.grid(row=2, column=0, padx=2, pady=2, sticky=NSEW)

                        # Accept Button
                        self.AcceptButton = Button(self.PointBuyFrame, text="Accept", command=self.Accept, bg=GlobalInst.ButtonColor)
                        self.AcceptButton.grid(row=3, column=0, columnspan=3, padx=2, pady=2, sticky=NSEW)

                        # Calculate
                        self.Calculate()

                        # Focus on Strength Entry
                        self.PointBuyField1Inst.ScoreEntry.focus_set()

                    def Calculate(self):
                        for Field in self.PointBuyFieldsList:
                            ScoreEntryString = Field.ScoreEntryVar.get()
                            if ScoreEntryString == "" or ScoreEntryString == "+" or ScoreEntryString == "-":
                                self.PointBuyEntryVar.set("N/A")
                                return False
                        PointsRemaining = 27
                        ValidScores = True
                        for Field in self.PointBuyFieldsList:
                            FieldValue = GlobalInst.GetStringVarAsNumber(Field.ScoreEntryVar)
                            if FieldValue < 8 or FieldValue > 15:
                                Field.ScoreEntry.configure(fg="red")
                                ValidScores = False
                            else:
                                Field.ScoreEntry.configure(fg="black")
                                PointsRemaining -= Field.PointBuyValue()
                        if ValidScores:
                            self.PointBuyEntryVar.set(str(PointsRemaining))
                            if PointsRemaining < 0:
                                self.PointBuyEntry.configure(disabledforeground="red")
                                return False
                            else:
                                self.PointBuyEntry.configure(disabledforeground="black")
                        else:
                            self.PointBuyEntryVar.set("N/A")
                            self.PointBuyEntry.configure(disabledforeground="black")
                            return False
                        return True

                    def Accept(self):
                        if self.Calculate():
                            pass
                        else:
                            messagebox.showerror("Invalid Entry", "Not a valid point buy array!")
                            return
                        self.AbilitiesDataConfigInst.PointBuyButtonVar.set(False)
                        for Field in self.PointBuyFieldsList:
                            for Entry in self.AbilitiesDataConfigInst.EntriesList:
                                FieldShortName = Field.AbilityNameShort
                                if Entry.AbilityNameShort == FieldShortName:
                                    Entry.AbilityBaseVar.set(Field.ScoreEntryVar.get())
                        self.PointBuyFrame.destroy()
                        GlobalInst.WindowGeometry(self.master, IsDialog=True, DialogMaster=WindowInst, WidthOffset=-self.PointBuyWidthOffset)

                    class PointBuyField:
                        def __init__(self, master, AbilityNameShort, List, Row=0, Column=0):
                            # Store Parameters
                            self.AbilityNameShort = AbilityNameShort
                            self.Row = Row
                            self.Column = Column

                            # Variables
                            self.AbilityLabelVar = StringVar(value=self.AbilityNameShort)
                            self.ScoreEntryVar = StringVar(value="8")

                            # Add to List
                            List.append(self)

                            # Frame
                            self.FieldFrame = Frame(master)
                            self.FieldFrame.grid(row=self.Row, column=self.Column, sticky=NSEW)

                            # Ability Label
                            self.AbilityLabel = Label(self.FieldFrame, textvariable=self.AbilityLabelVar, bd=2, relief=GROOVE)
                            self.AbilityLabel.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)

                            # Score Entry
                            self.ScoreEntry = EntryExtended(self.FieldFrame, textvariable=self.ScoreEntryVar, width=5, justify=CENTER)
                            self.ScoreEntry.ConfigureValidation(
                                lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Point buy score must be a whole number.", MinValue=1, LessThanMinString="Point buy score cannot be less than 1."), "key")
                            self.ScoreEntry.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)

                        def PointBuyValue(self):
                            Base = GlobalInst.GetStringVarAsNumber(self.ScoreEntryVar)
                            Value = Base - 8
                            if Base >= 14:
                                Value += 1
                            if Base >= 15:
                                Value += 1
                            return Value

        # Skills
        class SkillsTable:
            def __init__(self, master):
                # Skills Frame
                self.SkillsFrame = LabelFrame(master, text="Skills:")
                self.SkillsFrame.grid(row=1, column=3, padx=2, pady=2, rowspan=5, sticky=NSEW)

                # Labels
                self.SkillsHeaderProficiency = Label(self.SkillsFrame, text="Prof.", bd=2, relief=GROOVE)
                self.SkillsHeaderProficiency.grid(row=0, column=0, sticky=NSEW)
                self.SkillsHeaderSkills = Label(self.SkillsFrame, text="Skill", bd=2, relief=GROOVE)
                self.SkillsHeaderSkills.grid(row=0, column=1, sticky=NSEW)
                self.SkillsHeaderModifier = Label(self.SkillsFrame, text="Modifier", bd=2, relief=GROOVE)
                self.SkillsHeaderModifier.grid(row=0, column=2, sticky=NSEW)

                # Entries List
                self.SkillsEntriesList = []

                # Entries
                self.SkillsEntryAcrobaticsInst = self.SkillsEntry(self.SkillsFrame, "Acrobatics (DEX)", self.SkillsEntriesList, 1)
                self.SkillsEntryAnimalHandlingInst = self.SkillsEntry(self.SkillsFrame, "Animal Handling (WIS)", self.SkillsEntriesList, 2)
                self.SkillsEntryArcanaInst = self.SkillsEntry(self.SkillsFrame, "Arcana (INT)", self.SkillsEntriesList, 3)
                self.SkillsEntryAthleticsInst = self.SkillsEntry(self.SkillsFrame, "Athletics (STR)", self.SkillsEntriesList, 4)
                self.SkillsEntryDeceptionInst = self.SkillsEntry(self.SkillsFrame, "Deception (CHA)", self.SkillsEntriesList, 5)
                self.SkillsEntryHistoryInst = self.SkillsEntry(self.SkillsFrame, "History (INT)", self.SkillsEntriesList, 6)
                self.SkillsEntryInsightInst = self.SkillsEntry(self.SkillsFrame, "Insight (WIS)", self.SkillsEntriesList, 7)
                self.SkillsEntryIntimidationInst = self.SkillsEntry(self.SkillsFrame, "Intimidation (CHA)", self.SkillsEntriesList, 8)
                self.SkillsEntryInvestigationInst = self.SkillsEntry(self.SkillsFrame, "Investigation (INT)", self.SkillsEntriesList, 9)
                self.SkillsEntryMedicineInst = self.SkillsEntry(self.SkillsFrame, "Medicine (WIS)", self.SkillsEntriesList, 10)
                self.SkillsEntryNatureInst = self.SkillsEntry(self.SkillsFrame, "Nature (INT)", self.SkillsEntriesList, 11)
                self.SkillsEntryPerceptionInst = self.SkillsEntry(self.SkillsFrame, "Perception (WIS)", self.SkillsEntriesList, 12)
                self.SkillsEntryPerformanceInst = self.SkillsEntry(self.SkillsFrame, "Performance (CHA)", self.SkillsEntriesList, 13)
                self.SkillsEntryPersuasionInst = self.SkillsEntry(self.SkillsFrame, "Persuasion (CHA)", self.SkillsEntriesList, 14)
                self.SkillsEntryReligionInst = self.SkillsEntry(self.SkillsFrame, "Religion (INT)", self.SkillsEntriesList, 15)
                self.SkillsEntrySleightOfHandInst = self.SkillsEntry(self.SkillsFrame, "Sleight of Hand (DEX)", self.SkillsEntriesList, 16)
                self.SkillsEntryStealthInst = self.SkillsEntry(self.SkillsFrame, "Stealth (DEX)", self.SkillsEntriesList, 17)
                self.SkillsEntrySurvivalInst = self.SkillsEntry(self.SkillsFrame, "Survival (WIS)", self.SkillsEntriesList, 18)

            class SkillsEntry:
                def __init__(self, master, SkillName, List, Row):
                    # Store Parameters
                    self.SkillName = SkillName

                    # Variables
                    self.SkillNameVar = StringVar(value=self.SkillName)
                    self.ProficiencyBox1Var = SavedBooleanVar(self.SkillName + "SkillProficiency1")
                    self.ProficiencyBox1Var.trace_add("write", lambda a, b, c: CharacterSheetInst.UpdateStatsAndInventory())
                    self.ProficiencyBox2Var = SavedBooleanVar(self.SkillName + "SkillProficiency2")
                    self.ProficiencyBox2Var.trace_add("write", lambda a, b, c: CharacterSheetInst.UpdateStatsAndInventory())
                    self.TotalModifierVar = StringVar()

                    # Add to List
                    List.append(self)

                    # Proficiency Boxes
                    self.ProficiencyBoxesFrame = Frame(master)
                    self.ProficiencyBoxesFrame.grid(row=Row, column=0, sticky=NSEW)
                    self.ProficiencyBox1 = Checkbutton(self.ProficiencyBoxesFrame, variable=self.ProficiencyBox1Var)
                    self.ProficiencyBox2 = Checkbutton(self.ProficiencyBoxesFrame, variable=self.ProficiencyBox2Var)
                    self.ProficiencyBox1.grid(row=0, column=0)
                    self.ProficiencyBox2.grid(row=0, column=1)

                    # Label
                    self.SkillLabel = Label(master, textvariable=self.SkillNameVar)
                    self.SkillLabel.grid(row=Row, column=1, sticky=NSEW)

                    # Modifier
                    self.ModifierEntry = EntryExtended(master, textvariable=self.TotalModifierVar, width=3, justify=CENTER, cursor="dotbox")
                    self.ModifierEntry.grid(row=Row, column=2, sticky=NSEW)
                    self.ModifierEntryStatModifierInst = StatModifier(self.ModifierEntry, "<Button-3>", "Left-click on a skill modifier to roll 1d20 with it.  Right-click to set a bonus.", self.SkillName, Cursor="dotbox",
                                                                      Prefix=self.SkillName + "ModifierEntry")
                    self.ModifierEntry.bind("<Button-1>", self.RollSkill)

                def CalculateSkillModifier(self, Ability, ProficiencyBonus):
                    Modifier = 0
                    if self.ProficiencyBox1Var.get():
                        Modifier += ProficiencyBonus
                    if self.ProficiencyBox2Var.get():
                        Modifier += ProficiencyBonus
                    Modifier += int(Ability) + self.ModifierEntryStatModifierInst.GetModifier()
                    ModifierSign = ""
                    if Modifier >= 1:
                        ModifierSign = "+"
                    self.TotalModifierVar.set(ModifierSign + str(Modifier))

                def RollSkill(self, event):
                    BaseModifier = GlobalInst.GetStringVarAsNumber(self.TotalModifierVar)
                    JackOfAllTradesModifier = BaseModifier
                    RemarkableAthleteModifier = BaseModifier
                    ProficiencyBonus = GlobalInst.GetStringVarAsNumber(CharacterSheetInst.ProficiencyBonusEntryVar)
                    Proficiency1 = self.ProficiencyBox1Var.get()
                    Proficiency2 = self.ProficiencyBox2Var.get()
                    SkillName = self.SkillNameVar.get()
                    if not Proficiency1 and not Proficiency2 and CharacterSheetInst.RemarkableAthleteBoxVar.get():
                        if SkillName.endswith("(STR)") or SkillName.endswith("(DEX)") or SkillName.endswith("(CON)"):
                            RemarkableAthleteModifier += math.ceil(ProficiencyBonus / 2)
                    if not Proficiency1 and not Proficiency2 and CharacterSheetInst.JackOfAllTradesBoxVar.get():
                        JackOfAllTradesModifier += math.floor(ProficiencyBonus / 2)
                    FinalModifier = max(BaseModifier, RemarkableAthleteModifier, JackOfAllTradesModifier)

                    DiceRollerInst.DiceNumberEntryVar.set(1)
                    DiceRollerInst.DieTypeEntryVar.set(20)
                    DiceRollerInst.ModifierEntryVar.set(str(FinalModifier))
                    DiceRollerInst.Roll(self.SkillNameVar.get() + " Check:\n")

    # Combat and Features
    class CombatAndFeatures:
        def __init__(self, master):
            # Variables
            self.TempHPEntryVar = SavedStringVar("TempHPEntryVar")
            self.CurrentHPEntryVar = SavedStringVar("CurrentHPEntryVar")
            self.MaxHPEntryVar = StringVar()
            self.HitDiceEntryVar = SavedStringVar("HitDiceEntryVar")
            self.HitDiceRemainingEntryVar = SavedStringVar("HitDiceRemainingEntryVar")
            self.DeathSavingThrowsBoxSuccess1Var = SavedBooleanVar("DeathSavingThrowsBoxSuccess1Var")
            self.DeathSavingThrowsBoxSuccess2Var = SavedBooleanVar("DeathSavingThrowsBoxSuccess2Var")
            self.DeathSavingThrowsBoxSuccess3Var = SavedBooleanVar("DeathSavingThrowsBoxSuccess3Var")
            self.DeathSavingThrowsBoxFailure1Var = SavedBooleanVar("DeathSavingThrowsBoxFailure1Var")
            self.DeathSavingThrowsBoxFailure2Var = SavedBooleanVar("DeathSavingThrowsBoxFailure2Var")
            self.DeathSavingThrowsBoxFailure3Var = SavedBooleanVar("DeathSavingThrowsBoxFailure3Var")
            self.ACEntryVar = StringVar()
            self.InitiativeEntryVar = StringVar()
            self.SpeedEntryVar = SavedStringVar("SpeedEntryVar")
            self.MaxHPVars = {}
            for Index in range(1, 21):
                self.MaxHPVars[str(Index)] = SavedStringVar("MaxHPData" + str(Index))
            self.MaxHPVars["HPPerLevel"] = SavedStringVar("MaxHPDataHPPerLevel")
            self.MaxHPVars["HPOverride"] = SavedStringVar("MaxHPDataHPOverride")

            # Center Rows and Columns
            master.grid_rowconfigure(0, weight=1)
            master.grid_rowconfigure(2, weight=1)
            master.grid_rowconfigure(4, weight=1)
            master.grid_rowconfigure(6, weight=1)
            master.grid_columnconfigure(0, weight=1)
            master.grid_columnconfigure(2, weight=1)
            master.grid_columnconfigure(4, weight=1)
            master.grid_columnconfigure(6, weight=1)

            # Vitality Frame
            self.VitalityFrame = LabelFrame(master, text="Vitality:")
            self.VitalityFrame.grid(row=1, column=1, sticky=NSEW)

            # Vitality Font Size
            self.VitalityFontSize = font.Font(size=12)

            # HP Frame
            self.HPFrame = Frame(self.VitalityFrame)
            self.HPFrame.grid_rowconfigure(0, weight=1)
            self.HPFrame.grid_rowconfigure(1, weight=1)
            self.HPFrame.grid_rowconfigure(2, weight=1)
            self.HPFrame.grid(row=0, column=0, sticky=NSEW, rowspan=3)

            # Temp HP
            self.TempHPFrame = LabelFrame(self.HPFrame, text="Temp HP:")
            self.TempHPFrame.grid_columnconfigure(0, weight=1)
            self.TempHPFrame.grid_rowconfigure(0, weight=1)
            self.TempHPFrame.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
            self.TempHPEntry = EntryExtended(self.TempHPFrame, width=5, justify=CENTER, textvariable=self.TempHPEntryVar, font=self.VitalityFontSize)
            self.TempHPEntry.grid(row=0, column=0, sticky=NSEW)

            # Current HP
            self.CurrentHPFrame = LabelFrame(self.HPFrame, text="Current HP:")
            self.CurrentHPFrame.grid_columnconfigure(0, weight=1)
            self.CurrentHPFrame.grid_rowconfigure(0, weight=1)
            self.CurrentHPFrame.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
            self.CurrentHPEntry = EntryExtended(self.CurrentHPFrame, width=5, justify=CENTER, textvariable=self.CurrentHPEntryVar, bg=GlobalInst.ButtonColor, font=self.VitalityFontSize)
            self.CurrentHPEntry.grid(row=0, column=0, sticky=NSEW)
            self.CurrentHPEntry.bind("<Button-3>", lambda event: self.Damage())
            self.CurrentHPEntry.bind("<Shift-Button-3>", lambda event: self.Heal())
            self.CurrentHPTooltip = Tooltip(self.CurrentHPEntry, "Right-click to damage.  Shift+right-click to heal.")

            # Max HP
            self.MaxHPFrame = LabelFrame(self.HPFrame, text="Max HP:")
            self.MaxHPFrame.grid_columnconfigure(0, weight=1)
            self.MaxHPFrame.grid_rowconfigure(0, weight=1)
            self.MaxHPFrame.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)
            self.MaxHPEntry = EntryExtended(self.MaxHPFrame, width=5, justify=CENTER, textvariable=self.MaxHPEntryVar, font=self.VitalityFontSize, state=DISABLED, disabledbackground=GlobalInst.ButtonColor,
                                            cursor="arrow",
                                            disabledforeground="black")
            self.MaxHPEntry.grid(row=0, column=0, sticky=NSEW)
            self.MaxHPEntry.bind("<Button-1>", self.SetMaxHPData)
            self.MaxHPTooltip = Tooltip(self.MaxHPEntry, "Left-click to set max HP.")

            # Hit Dice
            self.HitDiceFrame = LabelFrame(self.VitalityFrame, text="Hit Dice:")
            self.HitDiceFrame.grid_columnconfigure(0, weight=1)
            self.HitDiceFrame.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
            self.HitDiceEntry = EntryExtended(self.HitDiceFrame, width=12, justify=CENTER, textvariable=self.HitDiceEntryVar)
            self.HitDiceEntry.grid(row=0, column=0, sticky=NSEW)
            self.HitDiceRemainingFrame = LabelFrame(self.VitalityFrame, text="Hit Dice Remaining:")
            self.HitDiceRemainingFrame.grid_columnconfigure(0, weight=1)
            self.HitDiceRemainingFrame.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
            self.HitDiceRemainingEntry = EntryExtended(self.HitDiceRemainingFrame, width=12, justify=CENTER, textvariable=self.HitDiceRemainingEntryVar)
            self.HitDiceRemainingEntry.grid(row=0, column=0, sticky=NSEW)

            # Death Saves
            self.DeathSavingThrowsFrame = LabelFrame(self.VitalityFrame, text="Death Saving Throws:")
            self.DeathSavingThrowsFrame.grid(row=2, column=1, sticky=NSEW, padx=2, pady=2)
            self.DeathSavingThrowsSuccessLabel = Label(self.DeathSavingThrowsFrame, text="Succ.")
            self.DeathSavingThrowsSuccessLabel.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)
            self.DeathSavingThrowsFailureLabel = Label(self.DeathSavingThrowsFrame, text="Fail")
            self.DeathSavingThrowsFailureLabel.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)
            self.DeathSavingThrowsBoxSuccess1 = Checkbutton(self.DeathSavingThrowsFrame, variable=self.DeathSavingThrowsBoxSuccess1Var)
            self.DeathSavingThrowsBoxSuccess1.grid(row=0, column=1, padx=2, pady=2, sticky=NSEW)
            self.DeathSavingThrowsBoxSuccess2 = Checkbutton(self.DeathSavingThrowsFrame, variable=self.DeathSavingThrowsBoxSuccess2Var)
            self.DeathSavingThrowsBoxSuccess2.grid(row=0, column=2, padx=2, pady=2, sticky=NSEW)
            self.DeathSavingThrowsBoxSuccess3 = Checkbutton(self.DeathSavingThrowsFrame, variable=self.DeathSavingThrowsBoxSuccess3Var)
            self.DeathSavingThrowsBoxSuccess3.grid(row=0, column=3, padx=2, pady=2, sticky=NSEW)
            self.DeathSavingThrowsBoxFailure1 = Checkbutton(self.DeathSavingThrowsFrame, variable=self.DeathSavingThrowsBoxFailure1Var)
            self.DeathSavingThrowsBoxFailure1.grid(row=1, column=1, padx=2, pady=2, sticky=NSEW)
            self.DeathSavingThrowsBoxFailure2 = Checkbutton(self.DeathSavingThrowsFrame, variable=self.DeathSavingThrowsBoxFailure2Var)
            self.DeathSavingThrowsBoxFailure2.grid(row=1, column=2, padx=2, pady=2, sticky=NSEW)
            self.DeathSavingThrowsBoxFailure3 = Checkbutton(self.DeathSavingThrowsFrame, variable=self.DeathSavingThrowsBoxFailure3Var)
            self.DeathSavingThrowsBoxFailure3.grid(row=1, column=3, padx=2, pady=2, sticky=NSEW)

            # AC, Initiative, and Speed Font Size
            self.ACInitiativeSpeedFontSize = font.Font(size=12)

            # AC, Initiative, and Speed Frame
            self.ACInitiativeSpeedFrame = Frame(master)
            self.ACInitiativeSpeedFrame.grid_rowconfigure(0, weight=1)
            self.ACInitiativeSpeedFrame.grid_rowconfigure(1, weight=1)
            self.ACInitiativeSpeedFrame.grid_rowconfigure(2, weight=1)
            self.ACInitiativeSpeedFrame.grid(row=1, column=3, sticky=NS + E)

            # AC
            self.ACFrame = LabelFrame(self.ACInitiativeSpeedFrame, text="AC:")
            self.ACFrame.grid_rowconfigure(0, weight=1)
            self.ACFrame.grid(row=0, column=0, sticky=NSEW)
            self.ACEntry = EntryExtended(self.ACFrame, width=9, justify=CENTER, textvariable=self.ACEntryVar, font=self.ACInitiativeSpeedFontSize)
            self.ACEntry.grid(row=0, column=0, sticky=NSEW)
            self.ACEntryStatModifierInst = StatModifier(self.ACEntry, "<Button-1>", "Left-click to set AC data.", "", ACMode=True, Prefix="ACEntry")
            self.ACTooltip = Tooltip(self.ACEntry, "Left-click on AC to set data.")

            # Initiative
            self.InitiativeFrame = LabelFrame(self.ACInitiativeSpeedFrame, text="Initiative:")
            self.InitiativeFrame.grid_rowconfigure(0, weight=1)
            self.InitiativeFrame.grid(row=1, column=0, sticky=NSEW)
            self.InitiativeEntry = EntryExtended(self.InitiativeFrame, width=9, justify=CENTER, textvariable=self.InitiativeEntryVar, cursor="dotbox", font=self.ACInitiativeSpeedFontSize)
            self.InitiativeEntry.grid(row=0, column=0, sticky=NSEW)
            self.InitiativeEntry.bind("<Button-1>", self.RollInitiative)
            self.InitiativeEntryStatModifierInst = StatModifier(self.InitiativeEntry, "<Button-3>", "Left-click on the initiative modifier to roll 1d20 with it.  Right-click to set a stat modifier.", "Initiative", Cursor="dotbox",
                                                                Prefix="InitiativeEntry")

            # Speed
            self.SpeedFrame = LabelFrame(self.ACInitiativeSpeedFrame, text="Speed:")
            self.SpeedFrame.grid_rowconfigure(0, weight=1)
            self.SpeedFrame.grid(row=2, column=0, sticky=NSEW)
            self.SpeedEntry = EntryExtended(self.SpeedFrame, width=9, justify=CENTER, textvariable=self.SpeedEntryVar, font=self.ACInitiativeSpeedFontSize)
            self.SpeedEntry.grid(row=0, column=0, sticky=NSEW)

            # Ability Score Derivatives Frame
            self.AbilityScoreDerivativesFrame = LabelFrame(master, text="Ability Score Derivatives:")
            self.AbilityScoreDerivativesFrame.grid_columnconfigure(1, weight=1)
            self.AbilityScoreDerivativesFrame.grid_columnconfigure(2, weight=1)
            self.AbilityScoreDerivativesFrame.grid_columnconfigure(3, weight=1)
            self.AbilityScoreDerivativesFrame.grid(row=3, column=1, padx=2, pady=2, columnspan=3, sticky=NSEW)

            # Ability Score Derivatives Labels
            self.AbilityScoreSelectionLabel = Label(self.AbilityScoreDerivativesFrame, text="Ability", bd=2, relief=GROOVE)
            self.AbilityScoreSelectionLabel.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)
            self.SaveDCLabel = Label(self.AbilityScoreDerivativesFrame, text="Save DC", bd=2, relief=GROOVE)
            self.SaveDCLabel.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)
            self.AttackModifierLabel = Label(self.AbilityScoreDerivativesFrame, text="Attack Modifier", bd=2, relief=GROOVE)
            self.AttackModifierLabel.grid(row=2, column=0, padx=2, pady=2, sticky=NSEW)

            # Ability Score Derivatives List
            self.AbilityScoreDerivativesList = []

            # Ability Score Derivatives
            for CurrentIndex in range(1, 4):
                AbilityScoreDerivatives(self.AbilityScoreDerivativesFrame, self.AbilityScoreDerivativesList, "AbilityScoreDerivatives", CurrentIndex)

            # Combat and Features Notes
            self.CombatAndFeaturesNotesFrame = LabelFrame(master, text="Combat and Features Notes:")
            self.CombatAndFeaturesNotesFrame.grid(row=5, column=1, columnspan=3)
            self.CombatAndFeaturesNotes = ScrolledText(self.CombatAndFeaturesNotesFrame, Width=344, Height=180, SavedDataTag="CombatAndFeaturesNotes")
            self.CombatAndFeaturesNotes.grid(row=0, column=0)

            # Features
            self.FeaturesAndCreatureStatsInst = self.FeaturesAndCreatureStats(master)
            Inst["FeaturesAndCreatureStats"] = self.FeaturesAndCreatureStatsInst

        def Damage(self):
            if self.ValidLifeValues():
                pass
            else:
                return
            CurrentTempHP = GlobalInst.GetStringVarAsNumber(self.TempHPEntryVar)
            CurrentHPString = self.CurrentHPEntryVar.get()
            if CurrentHPString == "" or CurrentHPString == "+" or CurrentHPString == "-":
                CurrentHP = GlobalInst.GetStringVarAsNumber(self.MaxHPEntryVar)
            else:
                CurrentHP = GlobalInst.GetStringVarAsNumber(self.CurrentHPEntryVar)
            DamagePrompt = IntegerPrompt(WindowInst, "Damage", "How much damage?", MinValue=0)
            WindowInst.wait_window(DamagePrompt.Window)
            if DamagePrompt.DataSubmitted.get():
                Damage = DamagePrompt.GetData()
                TotalDamage = Damage
            else:
                return
            if CurrentTempHP == 0:
                self.CurrentHPEntryVar.set(str(CurrentHP - Damage))
            elif CurrentTempHP >= 1:
                if CurrentTempHP < Damage:
                    Damage -= CurrentTempHP
                    self.TempHPEntryVar.set(str(0))
                    self.CurrentHPEntryVar.set(str(CurrentHP - Damage))
                elif CurrentTempHP >= Damage:
                    self.TempHPEntryVar.set(str(CurrentTempHP - Damage))
            if Inst["Spellcasting"].ConcentrationBoxVar.get() and CharacterSheetInst.ConcentrationCheckPromptBoxVar.get():
                ConcentrationDC = str(max(10, math.ceil(TotalDamage / 2)))
                messagebox.showinfo("Concentration Check", "DC " + ConcentrationDC + " Constitution saving throw required to maintain concentration.")

        def Heal(self):
            if self.ValidLifeValues():
                pass
            else:
                return
            CurrentHP = GlobalInst.GetStringVarAsNumber(self.CurrentHPEntryVar)
            MaxHP = GlobalInst.GetStringVarAsNumber(self.MaxHPEntryVar)
            HealingPrompt = IntegerPrompt(WindowInst, "Heal", "How much healing?", MinValue=0)
            WindowInst.wait_window(HealingPrompt.Window)
            if HealingPrompt.DataSubmitted.get():
                Healing = HealingPrompt.GetData()
            else:
                return
            HealedValue = Healing + max(CurrentHP, 0)
            if HealedValue > MaxHP:
                self.CurrentHPEntryVar.set(str(MaxHP))
            elif HealedValue <= MaxHP:
                self.CurrentHPEntryVar.set(str(HealedValue))

        def ValidLifeValues(self):
            try:
                TempHP = GlobalInst.GetStringVarAsNumber(self.TempHPEntryVar)
                CurrentHP = GlobalInst.GetStringVarAsNumber(self.CurrentHPEntryVar)
                MaxHP = GlobalInst.GetStringVarAsNumber(self.MaxHPEntryVar)
            except:
                messagebox.showerror("Invalid Entry", "HP values must be whole numbers.")
                return False
            if TempHP < 0 or MaxHP < 1:
                messagebox.showerror("Invalid Entry", "Temp HP cannot be negative and max HP must be positive.")
                return False
            return True

        def RollInitiative(self, event):
            BaseModifier = GlobalInst.GetStringVarAsNumber(self.InitiativeEntryVar)
            JackOfAllTradesModifier = BaseModifier
            RemarkableAthleteModifier = BaseModifier
            ProficiencyBonus = GlobalInst.GetStringVarAsNumber(CharacterSheetInst.ProficiencyBonusEntryVar)
            if CharacterSheetInst.RemarkableAthleteBoxVar.get():
                RemarkableAthleteModifier += math.ceil(ProficiencyBonus / 2)
            if CharacterSheetInst.JackOfAllTradesBoxVar.get():
                JackOfAllTradesModifier += math.floor(ProficiencyBonus / 2)
            FinalModifier = max(BaseModifier, RemarkableAthleteModifier, JackOfAllTradesModifier)
            DiceRollerInst.DiceNumberEntryVar.set(1)
            DiceRollerInst.DieTypeEntryVar.set(20)
            DiceRollerInst.ModifierEntryVar.set(str(FinalModifier))
            DiceRollerInst.Roll("Initiative:\n")

        def SetMaxHPData(self, event):
            # Create Config Window and Wait
            MaxHPMenuInst = self.MaxHPMenu(WindowInst, self.MaxHPVars)
            WindowInst.wait_window(MaxHPMenuInst.Window)

            # Handle Variables
            if MaxHPMenuInst.DataSubmitted.get():
                for Tag, Var in self.MaxHPVars.items():
                    Var.set(MaxHPMenuInst.MaxHPData[Tag].get())

                # Update Stats
                CharacterSheetInst.UpdateStatsAndInventory()

        def CalculateMaxHP(self, ConstitutionModifier, CharacterLevelValue):
            if self.MaxHPVars["HPOverride"].get() != "":
                MaxHP = GlobalInst.GetStringVarAsNumber(self.MaxHPVars["HPOverride"])
            else:
                MaxHP = 0
                for Level in range(1, CharacterLevelValue + 1):
                    MaxHP += GlobalInst.GetStringVarAsNumber(self.MaxHPVars[str(Level)])
                MaxHP += (ConstitutionModifier + GlobalInst.GetStringVarAsNumber(self.MaxHPVars["HPPerLevel"])) * CharacterLevelValue
            self.MaxHPEntryVar.set(str(MaxHP))

        class MaxHPMenu:
            def __init__(self, master, MaxHPData):
                # Variables
                self.DataSubmitted = BooleanVar()
                self.TableWidgetsWidth = 4
                self.MaxHPData = {}
                for Tag, Var in MaxHPData.items():
                    self.MaxHPData[Tag] = StringVar(value=Var.get())

                # Create Window
                self.Window = Toplevel(master)
                self.Window.wm_attributes("-toolwindow", 1)
                self.Window.wm_title("Max HP")

                # Instructions
                self.InstructionsLabel = Label(self.Window,
                                               text="The HP calculation automatically accounts for your\ncharacter level and Constitution modifier.  Max HP\ngained at each level should be based on your hit\ndice only.", bd=2,
                                               relief=GROOVE, justify=LEFT)
                self.InstructionsLabel.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2, columnspan=2)

                # HP at Each Level
                self.HPAtEachLevelFrame = LabelFrame(self.Window, text="Max HP Gained at Each Level:")
                self.HPAtEachLevelFrame.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2, columnspan=2)
                self.HPAtEachLevelFirstLabel = Label(self.HPAtEachLevelFrame, text="1st", bd=2, relief=GROOVE, width=self.TableWidgetsWidth)
                self.HPAtEachLevelFirstLabel.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelFirstEntry = MaxHPDataEntry(self.HPAtEachLevelFrame, justify=CENTER, width=self.TableWidgetsWidth, textvariable=self.MaxHPData["1"])
                self.HPAtEachLevelFirstEntry.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelSecondLabel = Label(self.HPAtEachLevelFrame, text="2nd", bd=2, relief=GROOVE, width=self.TableWidgetsWidth)
                self.HPAtEachLevelSecondLabel.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelSecondEntry = MaxHPDataEntry(self.HPAtEachLevelFrame, justify=CENTER, width=self.TableWidgetsWidth, textvariable=self.MaxHPData["2"])
                self.HPAtEachLevelSecondEntry.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelThirdLabel = Label(self.HPAtEachLevelFrame, text="3rd", bd=2, relief=GROOVE, width=self.TableWidgetsWidth)
                self.HPAtEachLevelThirdLabel.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelThirdEntry = MaxHPDataEntry(self.HPAtEachLevelFrame, justify=CENTER, width=self.TableWidgetsWidth, textvariable=self.MaxHPData["3"])
                self.HPAtEachLevelThirdEntry.grid(row=2, column=1, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelFourthLabel = Label(self.HPAtEachLevelFrame, text="4th", bd=2, relief=GROOVE, width=self.TableWidgetsWidth)
                self.HPAtEachLevelFourthLabel.grid(row=3, column=0, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelFourthEntry = MaxHPDataEntry(self.HPAtEachLevelFrame, justify=CENTER, width=self.TableWidgetsWidth, textvariable=self.MaxHPData["4"])
                self.HPAtEachLevelFourthEntry.grid(row=3, column=1, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelFifthLabel = Label(self.HPAtEachLevelFrame, text="5th", bd=2, relief=GROOVE, width=self.TableWidgetsWidth)
                self.HPAtEachLevelFifthLabel.grid(row=4, column=0, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelFifthEntry = MaxHPDataEntry(self.HPAtEachLevelFrame, justify=CENTER, width=self.TableWidgetsWidth, textvariable=self.MaxHPData["5"])
                self.HPAtEachLevelFifthEntry.grid(row=4, column=1, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelSixthLabel = Label(self.HPAtEachLevelFrame, text="6th", bd=2, relief=GROOVE, width=self.TableWidgetsWidth)
                self.HPAtEachLevelSixthLabel.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelSixthEntry = MaxHPDataEntry(self.HPAtEachLevelFrame, justify=CENTER, width=self.TableWidgetsWidth, textvariable=self.MaxHPData["6"])
                self.HPAtEachLevelSixthEntry.grid(row=0, column=3, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelSeventhLabel = Label(self.HPAtEachLevelFrame, text="7th", bd=2, relief=GROOVE, width=self.TableWidgetsWidth)
                self.HPAtEachLevelSeventhLabel.grid(row=1, column=2, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelSeventhEntry = MaxHPDataEntry(self.HPAtEachLevelFrame, justify=CENTER, width=self.TableWidgetsWidth, textvariable=self.MaxHPData["7"])
                self.HPAtEachLevelSeventhEntry.grid(row=1, column=3, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelEighthLabel = Label(self.HPAtEachLevelFrame, text="8th", bd=2, relief=GROOVE, width=self.TableWidgetsWidth)
                self.HPAtEachLevelEighthLabel.grid(row=2, column=2, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelEighthEntry = MaxHPDataEntry(self.HPAtEachLevelFrame, justify=CENTER, width=self.TableWidgetsWidth, textvariable=self.MaxHPData["8"])
                self.HPAtEachLevelEighthEntry.grid(row=2, column=3, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelNinthLabel = Label(self.HPAtEachLevelFrame, text="9th", bd=2, relief=GROOVE, width=self.TableWidgetsWidth)
                self.HPAtEachLevelNinthLabel.grid(row=3, column=2, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelNinthEntry = MaxHPDataEntry(self.HPAtEachLevelFrame, justify=CENTER, width=self.TableWidgetsWidth, textvariable=self.MaxHPData["9"])
                self.HPAtEachLevelNinthEntry.grid(row=3, column=3, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelTenthLabel = Label(self.HPAtEachLevelFrame, text="10th", bd=2, relief=GROOVE, width=self.TableWidgetsWidth)
                self.HPAtEachLevelTenthLabel.grid(row=4, column=2, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelTenthEntry = MaxHPDataEntry(self.HPAtEachLevelFrame, justify=CENTER, width=self.TableWidgetsWidth, textvariable=self.MaxHPData["10"])
                self.HPAtEachLevelTenthEntry.grid(row=4, column=3, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelEleventhLabel = Label(self.HPAtEachLevelFrame, text="11th", bd=2, relief=GROOVE, width=self.TableWidgetsWidth)
                self.HPAtEachLevelEleventhLabel.grid(row=0, column=4, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelEleventhEntry = MaxHPDataEntry(self.HPAtEachLevelFrame, justify=CENTER, width=self.TableWidgetsWidth, textvariable=self.MaxHPData["11"])
                self.HPAtEachLevelEleventhEntry.grid(row=0, column=5, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelTwelfthLabel = Label(self.HPAtEachLevelFrame, text="12th", bd=2, relief=GROOVE, width=self.TableWidgetsWidth)
                self.HPAtEachLevelTwelfthLabel.grid(row=1, column=4, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelTwelfthEntry = MaxHPDataEntry(self.HPAtEachLevelFrame, justify=CENTER, width=self.TableWidgetsWidth, textvariable=self.MaxHPData["12"])
                self.HPAtEachLevelTwelfthEntry.grid(row=1, column=5, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelThirteenthLabel = Label(self.HPAtEachLevelFrame, text="13th", bd=2, relief=GROOVE, width=self.TableWidgetsWidth)
                self.HPAtEachLevelThirteenthLabel.grid(row=2, column=4, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelThirteenthEntry = MaxHPDataEntry(self.HPAtEachLevelFrame, justify=CENTER, width=self.TableWidgetsWidth, textvariable=self.MaxHPData["13"])
                self.HPAtEachLevelThirteenthEntry.grid(row=2, column=5, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelFourteenthLabel = Label(self.HPAtEachLevelFrame, text="14th", bd=2, relief=GROOVE, width=self.TableWidgetsWidth)
                self.HPAtEachLevelFourteenthLabel.grid(row=3, column=4, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelFourteenthEntry = MaxHPDataEntry(self.HPAtEachLevelFrame, justify=CENTER, width=self.TableWidgetsWidth, textvariable=self.MaxHPData["14"])
                self.HPAtEachLevelFourteenthEntry.grid(row=3, column=5, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelFifteenthLabel = Label(self.HPAtEachLevelFrame, text="15th", bd=2, relief=GROOVE, width=self.TableWidgetsWidth)
                self.HPAtEachLevelFifteenthLabel.grid(row=4, column=4, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelFifteenthEntry = MaxHPDataEntry(self.HPAtEachLevelFrame, justify=CENTER, width=self.TableWidgetsWidth, textvariable=self.MaxHPData["15"])
                self.HPAtEachLevelFifteenthEntry.grid(row=4, column=5, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelSixteenthLabel = Label(self.HPAtEachLevelFrame, text="16th", bd=2, relief=GROOVE, width=self.TableWidgetsWidth)
                self.HPAtEachLevelSixteenthLabel.grid(row=0, column=6, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelSixteenthEntry = MaxHPDataEntry(self.HPAtEachLevelFrame, justify=CENTER, width=self.TableWidgetsWidth, textvariable=self.MaxHPData["16"])
                self.HPAtEachLevelSixteenthEntry.grid(row=0, column=7, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelSeventeenthLabel = Label(self.HPAtEachLevelFrame, text="17th", bd=2, relief=GROOVE, width=self.TableWidgetsWidth)
                self.HPAtEachLevelSeventeenthLabel.grid(row=1, column=6, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelSeventeenthEntry = MaxHPDataEntry(self.HPAtEachLevelFrame, justify=CENTER, width=self.TableWidgetsWidth, textvariable=self.MaxHPData["17"])
                self.HPAtEachLevelSeventeenthEntry.grid(row=1, column=7, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelEighteenthLabel = Label(self.HPAtEachLevelFrame, text="18th", bd=2, relief=GROOVE, width=self.TableWidgetsWidth)
                self.HPAtEachLevelEighteenthLabel.grid(row=2, column=6, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelEighteenthEntry = MaxHPDataEntry(self.HPAtEachLevelFrame, justify=CENTER, width=self.TableWidgetsWidth, textvariable=self.MaxHPData["18"])
                self.HPAtEachLevelEighteenthEntry.grid(row=2, column=7, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelNineteenthLabel = Label(self.HPAtEachLevelFrame, text="19th", bd=2, relief=GROOVE, width=self.TableWidgetsWidth)
                self.HPAtEachLevelNineteenthLabel.grid(row=3, column=6, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelNineteenthEntry = MaxHPDataEntry(self.HPAtEachLevelFrame, justify=CENTER, width=self.TableWidgetsWidth, textvariable=self.MaxHPData["19"])
                self.HPAtEachLevelNineteenthEntry.grid(row=3, column=7, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelTwentiethLabel = Label(self.HPAtEachLevelFrame, text="20th", bd=2, relief=GROOVE, width=self.TableWidgetsWidth)
                self.HPAtEachLevelTwentiethLabel.grid(row=4, column=6, sticky=NSEW, padx=2, pady=2)
                self.HPAtEachLevelTwentiethEntry = MaxHPDataEntry(self.HPAtEachLevelFrame, justify=CENTER, width=self.TableWidgetsWidth, textvariable=self.MaxHPData["20"])
                self.HPAtEachLevelTwentiethEntry.grid(row=4, column=7, sticky=NSEW, padx=2, pady=2)

                # Additional HP Per Level
                self.AdditionalHPPerLevelFrame = LabelFrame(self.Window, text="Additional Max HP Per Level:")
                self.AdditionalHPPerLevelFrame.grid_columnconfigure(0, weight=1)
                self.AdditionalHPPerLevelFrame.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2, columnspan=2)
                self.AdditionalHPPerLevelEntry = MaxHPDataEntry(self.AdditionalHPPerLevelFrame, textvariable=self.MaxHPData["HPPerLevel"], width=5, justify=CENTER)
                self.AdditionalHPPerLevelEntry.grid(row=0, column=0, sticky=NSEW)

                # HP Override
                self.HPOverrideFrame = LabelFrame(self.Window, text="Max HP Override:")
                self.HPOverrideFrame.grid_columnconfigure(0, weight=1)
                self.HPOverrideFrame.grid(row=3, column=0, sticky=NSEW, padx=2, pady=2, columnspan=2)
                self.HPOverrideEntry = MaxHPDataEntry(self.HPOverrideFrame, textvariable=self.MaxHPData["HPOverride"], width=5, justify=CENTER)
                self.HPOverrideEntry.grid(row=0, column=0, sticky=NSEW)

                # Submit Button
                self.SubmitButton = Button(self.Window, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
                self.SubmitButton.grid(row=4, column=0, sticky=NSEW, padx=2, pady=2)

                # Cancel Button
                self.CancelButton = Button(self.Window, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
                self.CancelButton.grid(row=4, column=1, sticky=NSEW, padx=2, pady=2)

                # Prevent Main Window Input
                self.Window.grab_set()

                # Handle Config Window Geometry and Focus
                GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst)
                self.Window.focus_force()

                # Focus on 1st Level Entry
                self.HPAtEachLevelFirstEntry.focus_set()

            def Submit(self):
                self.DataSubmitted.set(True)
                self.Window.destroy()

            def Cancel(self):
                self.DataSubmitted.set(False)
                self.Window.destroy()

        class FeaturesAndCreatureStats:
            def __init__(self, master):
                # Variables
                self.ScrollingDisabledVar = BooleanVar(value=False)

                # Features Frame
                self.FeaturesFrame = LabelFrame(master, text="Features and Creature Stats:")
                self.FeaturesFrame.grid(row=1, column=5, rowspan=5, sticky=NSEW)

                # Features Scrolled Canvas
                self.FeaturesScrolledCanvas = ScrolledCanvas(self.FeaturesFrame, Height=480, Width=327, ScrollingDisabledVar=self.ScrollingDisabledVar)
                self.FeaturesScrolledCanvas.BindEnterAndLeaveToBindMouseWheel()

                # Headers
                self.NameHeader = Label(self.FeaturesScrolledCanvas.WindowFrame, text="Name", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
                self.NameHeader.grid(row=0, column=0, sticky=NSEW)
                self.NameHeader.bind("<Button-1>", lambda event: self.Sort("Name"))
                self.NameHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Name", SearchMode=True))
                self.NameHeader.bind("<Button-3>", lambda event: self.Sort("Name", Reverse=True))
                self.NameTooltip = Tooltip(self.NameHeader, GlobalInst.SortTooltipString)
                self.SortOrderHeader = Label(self.FeaturesScrolledCanvas.WindowFrame, text="Sort\nOrder", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
                self.SortOrderHeader.grid(row=0, column=1, sticky=NSEW)
                self.SortOrderHeader.bind("<Button-1>", lambda event: self.Sort("Sort Order"))
                self.SortOrderHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Sort Order", SearchMode=True))
                self.SortOrderHeader.bind("<Button-3>", lambda event: self.Sort("Sort Order", Reverse=True))
                self.SortOrderTooltip = Tooltip(self.SortOrderHeader, GlobalInst.SortTooltipString)

                # Features Entries List
                self.FeatureOrCreatureStatsEntriesList = []

                # Features Entries Count
                self.FeatureOrCreatureStatsEntryCount = 100

                # Sort Order Values
                self.SortOrderValuesList = [""]
                for CurrentIndex in range(1, self.FeatureOrCreatureStatsEntryCount + 1):
                    self.SortOrderValuesList.append(str(CurrentIndex))

                # Features Entries
                for CurrentIndex in range(1, self.FeatureOrCreatureStatsEntryCount + 1):
                    CurrentEntry = self.FeatureOrCreatureStatsEntry(self.FeaturesScrolledCanvas.WindowFrame, self.FeatureOrCreatureStatsEntriesList, self.ScrollingDisabledVar, self.SortOrderValuesList, CurrentIndex)
                    CurrentEntry.Display(CurrentIndex)

            def Sort(self, Column, Reverse=False, SearchMode=False):
                # List to Sort
                ListToSort = []

                if SearchMode:
                    # Get Search String
                    SearchStringPrompt = StringPrompt(WindowInst, "Search", "What do you want to search for?")
                    WindowInst.wait_window(SearchStringPrompt.Window)
                    if SearchStringPrompt.DataSubmitted.get():
                        SearchString = SearchStringPrompt.StringEntryVar.get()
                    else:
                        return

                    # Add Fields to List
                    for CurrentEntry in self.FeatureOrCreatureStatsEntriesList:
                        ListToSort.append((CurrentEntry, CurrentEntry.SortFields[Column].get().lower()))

                    # Sort the List
                    SortedList = sorted(ListToSort, key=lambda x: (x[1] == "", SearchString not in x[1]))
                else:
                    if Column == "Name":
                        # Add Fields to List
                        for CurrentEntry in self.FeatureOrCreatureStatsEntriesList:
                            ListToSort.append((CurrentEntry, CurrentEntry.SortFields[Column].get()))

                        # Sort the List
                        SortedList = sorted(ListToSort, key=lambda x: ((not Reverse and x[1] == "") or (Reverse and x[1] != ""), x[1].lower()), reverse=Reverse)
                    elif Column == "Sort Order":
                        # Add Fields to List
                        for CurrentEntry in self.FeatureOrCreatureStatsEntriesList:
                            ListToSort.append((CurrentEntry, GlobalInst.GetStringVarAsNumber(CurrentEntry.SortFields[Column])))

                        # Sort the List
                        SortedList = sorted(ListToSort, key=lambda x: ((not Reverse and x[1] == 0) or (Reverse and x[1] != 0), x[1]), reverse=Reverse)
                    else:
                        return

                # Adjust Entries to New Order
                for CurrentIndex in range(len(SortedList)):
                    SortedList[CurrentIndex][0].Display(CurrentIndex + 1)

                # Flag Save Prompt
                SavingAndOpeningInst.SavePrompt = True

                # Update Window Title
                WindowInst.UpdateWindowTitle()

            class FeatureOrCreatureStatsEntry:
                def __init__(self, master, List, ScrollingDisabledVar, SortOrderValuesList, Row):
                    # Store Parameters
                    self.master = master
                    self.ScrollingDisabledVar = ScrollingDisabledVar
                    self.SortOrderValuesList = SortOrderValuesList
                    self.Row = Row

                    # Variables
                    self.NameEntryVar = SavedStringVar()
                    self.SortOrderVar = SavedStringVar()
                    self.FeatureDescriptionVar = SavedStringVar()
                    self.SizeEntryVar = SavedStringVar()
                    self.TypeAndTagsEntryVar = SavedStringVar()
                    self.AlignmentEntryVar = SavedStringVar()
                    self.ProficiencyEntryVar = SavedStringVar()
                    self.TempHPEntryVar = SavedStringVar()
                    self.CurrentHPEntryVar = SavedStringVar()
                    self.MaxHPEntryVar = SavedStringVar()
                    self.ACEntryVar = SavedStringVar()
                    self.SpeedEntryVar = SavedStringVar()
                    self.CRAndExperienceEntryVar = SavedStringVar()
                    self.AbilitiesStrengthEntryVar = SavedStringVar()
                    self.AbilitiesDexterityEntryVar = SavedStringVar()
                    self.AbilitiesConstitutionEntryVar = SavedStringVar()
                    self.AbilitiesIntelligenceEntryVar = SavedStringVar()
                    self.AbilitiesWisdomEntryVar = SavedStringVar()
                    self.AbilitiesCharismaEntryVar = SavedStringVar()
                    self.SkillSensesAndLanguagesFieldVar = SavedStringVar()
                    self.SavingThrowsFieldVar = SavedStringVar()
                    self.VulnerabilitiesResistancesAndImmunitiesFieldVar = SavedStringVar()
                    self.SpecialTraitsFieldVar = SavedStringVar()
                    self.ActionsFieldVar = SavedStringVar()
                    self.ReactionsFieldVar = SavedStringVar()
                    self.InventoryFieldVar = SavedStringVar()
                    self.LegendaryActionsAndLairActionsFieldVar = SavedStringVar()
                    self.NotesFieldVar = SavedStringVar()

                    # Feature Vars Dictionary
                    self.FeatureVars = {}
                    self.FeatureVars["NameEntryVar"] = self.NameEntryVar
                    self.FeatureVars["FeatureDescriptionVar"] = self.FeatureDescriptionVar

                    # Creature Stats Dictionary
                    self.CreatureStats = {}
                    self.CreatureStats["NameEntryVar"] = self.NameEntryVar
                    self.CreatureStats["SizeEntryVar"] = self.SizeEntryVar
                    self.CreatureStats["TypeAndTagsEntryVar"] = self.TypeAndTagsEntryVar
                    self.CreatureStats["AlignmentEntryVar"] = self.AlignmentEntryVar
                    self.CreatureStats["ProficiencyEntryVar"] = self.ProficiencyEntryVar
                    self.CreatureStats["TempHPEntryVar"] = self.TempHPEntryVar
                    self.CreatureStats["CurrentHPEntryVar"] = self.CurrentHPEntryVar
                    self.CreatureStats["MaxHPEntryVar"] = self.MaxHPEntryVar
                    self.CreatureStats["ACEntryVar"] = self.ACEntryVar
                    self.CreatureStats["SpeedEntryVar"] = self.SpeedEntryVar
                    self.CreatureStats["CRAndExperienceEntryVar"] = self.CRAndExperienceEntryVar
                    self.CreatureStats["AbilitiesStrengthEntryVar"] = self.AbilitiesStrengthEntryVar
                    self.CreatureStats["AbilitiesDexterityEntryVar"] = self.AbilitiesDexterityEntryVar
                    self.CreatureStats["AbilitiesConstitutionEntryVar"] = self.AbilitiesConstitutionEntryVar
                    self.CreatureStats["AbilitiesIntelligenceEntryVar"] = self.AbilitiesIntelligenceEntryVar
                    self.CreatureStats["AbilitiesWisdomEntryVar"] = self.AbilitiesWisdomEntryVar
                    self.CreatureStats["AbilitiesCharismaEntryVar"] = self.AbilitiesCharismaEntryVar
                    self.CreatureStats["SkillSensesAndLanguagesFieldVar"] = self.SkillSensesAndLanguagesFieldVar
                    self.CreatureStats["SavingThrowsFieldVar"] = self.SavingThrowsFieldVar
                    self.CreatureStats["VulnerabilitiesResistancesAndImmunitiesFieldVar"] = self.VulnerabilitiesResistancesAndImmunitiesFieldVar
                    self.CreatureStats["SpecialTraitsFieldVar"] = self.SpecialTraitsFieldVar
                    self.CreatureStats["ActionsFieldVar"] = self.ActionsFieldVar
                    self.CreatureStats["ReactionsFieldVar"] = self.ReactionsFieldVar
                    self.CreatureStats["InventoryFieldVar"] = self.InventoryFieldVar
                    self.CreatureStats["LegendaryActionsAndLairActionsFieldVar"] = self.LegendaryActionsAndLairActionsFieldVar
                    self.CreatureStats["NotesFieldVar"] = self.NotesFieldVar

                    # Sort Fields
                    self.SortFields = {}
                    self.SortFields["Name"] = self.NameEntryVar
                    self.SortFields["Sort Order"] = self.SortOrderVar

                    # Add to List
                    List.append(self)

                    # Name Entry
                    self.NameEntry = EntryExtended(master, width=45, justify=CENTER, state=DISABLED, disabledbackground=GlobalInst.ButtonColor, disabledforeground="black", textvariable=self.NameEntryVar, cursor="arrow")
                    self.NameEntry.bind("<Button-1>", self.SetFeature)
                    self.NameEntry.bind("<Button-3>", self.SetCreatureStats)
                    self.NameTooltip = Tooltip(self.NameEntry, "Left-click on a feature or creature stats entry to set a feature.  Right-click to set creature stats.")

                    # Sort Order
                    self.SortOrder = DropdownExtended(master, textvariable=self.SortOrderVar, values=self.SortOrderValuesList, width=5, state="readonly", justify=CENTER)
                    self.SortOrder.bind("<Enter>", self.DisableScrolling)
                    self.SortOrder.bind("<Leave>", self.EnableScrolling)

                def SetFeature(self, event):
                    # Create Config Window and Wait
                    FeatureConfigInst = self.FeatureConfig(WindowInst, self.FeatureVars)
                    WindowInst.wait_window(FeatureConfigInst.Window)

                    # Handle Variables
                    if FeatureConfigInst.DataSubmitted.get():
                        for Tag, Var in FeatureConfigInst.Vars.items():
                            self.FeatureVars[Tag].set(Var.get())

                def SetCreatureStats(self, event):
                    # Create Config Window and Wait
                    CreatureDataInst = CreatureData(WindowInst, DialogMode=True, DialogData=self.CreatureStats)
                    WindowInst.wait_window(CreatureDataInst.Window)

                    # Handle Variables
                    if CreatureDataInst.DataSubmitted.get():
                        for Tag, Var in CreatureDataInst.CreatureStatsFields.items():
                            self.CreatureStats[Tag].set(Var.get())

                def DisableScrolling(self, event):
                    self.ScrollingDisabledVar.set(True)

                def EnableScrolling(self, event):
                    self.ScrollingDisabledVar.set(False)

                def Display(self, Row):
                    self.Row = Row

                    # Set Row Size
                    self.master.grid_rowconfigure(self.Row, minsize=26)

                    # Place in Grid
                    self.NameEntry.grid(row=self.Row, column=0, sticky=NSEW)
                    self.SortOrder.grid(row=self.Row, column=1, sticky=NSEW)

                    # Update Tab Order
                    self.NameEntry.lift()
                    self.SortOrder.lift()

                    # Update Tags
                    self.NameEntryVar.UpdateTag("FeatureOrCreatureStatsNameEntryVar" + str(self.Row))
                    self.SortOrderVar.UpdateTag("FeatureOrCreatureStatsSortOrderVar" + str(self.Row))
                    self.FeatureDescriptionVar.UpdateTag("FeatureOrCreatureStatsFeatureDescriptionVar" + str(self.Row))
                    self.SizeEntryVar.UpdateTag("FeatureOrCreatureStatsSizeEntryVar" + str(self.Row))
                    self.TypeAndTagsEntryVar.UpdateTag("FeatureOrCreatureStatsTypeAndTagsEntryVar" + str(self.Row))
                    self.AlignmentEntryVar.UpdateTag("FeatureOrCreatureStatsAlignmentEntryVar" + str(self.Row))
                    self.ProficiencyEntryVar.UpdateTag("FeatureOrCreatureStatsProficiencyEntryVar" + str(self.Row))
                    self.TempHPEntryVar.UpdateTag("FeatureOrCreatureStatsTempHPEntryVar" + str(self.Row))
                    self.CurrentHPEntryVar.UpdateTag("FeatureOrCreatureStatsCurrentHPEntryVar" + str(self.Row))
                    self.MaxHPEntryVar.UpdateTag("FeatureOrCreatureStatsMaxHPEntryVar" + str(self.Row))
                    self.ACEntryVar.UpdateTag("FeatureOrCreatureStatsACEntryVar" + str(self.Row))
                    self.SpeedEntryVar.UpdateTag("FeatureOrCreatureStatsSpeedEntryVar" + str(self.Row))
                    self.CRAndExperienceEntryVar.UpdateTag("FeatureOrCreatureStatsCRAndExperienceEntryVar" + str(self.Row))
                    self.AbilitiesStrengthEntryVar.UpdateTag("FeatureOrCreatureStatsAbilitiesStrengthEntryVar" + str(self.Row))
                    self.AbilitiesDexterityEntryVar.UpdateTag("FeatureOrCreatureStatsAbilitiesDexterityEntryVar" + str(self.Row))
                    self.AbilitiesConstitutionEntryVar.UpdateTag("FeatureOrCreatureStatsAbilitiesConstitutionEntryVar" + str(self.Row))
                    self.AbilitiesIntelligenceEntryVar.UpdateTag("FeatureOrCreatureStatsAbilitiesIntelligenceEntryVar" + str(self.Row))
                    self.AbilitiesWisdomEntryVar.UpdateTag("FeatureOrCreatureStatsAbilitiesWisdomEntryVar" + str(self.Row))
                    self.AbilitiesCharismaEntryVar.UpdateTag("FeatureOrCreatureStatsAbilitiesCharismaEntryVar" + str(self.Row))
                    self.SkillSensesAndLanguagesFieldVar.UpdateTag("FeatureOrCreatureStatsSkillSensesAndLanguagesFieldVar" + str(self.Row))
                    self.SavingThrowsFieldVar.UpdateTag("FeatureOrCreatureStatsSavingThrowsFieldVar" + str(self.Row))
                    self.VulnerabilitiesResistancesAndImmunitiesFieldVar.UpdateTag("FeatureOrCreatureStatsVulnerabilitiesResistancesAndImmunitiesFieldVar" + str(self.Row))
                    self.SpecialTraitsFieldVar.UpdateTag("FeatureOrCreatureStatsSpecialTraitsFieldVar" + str(self.Row))
                    self.ActionsFieldVar.UpdateTag("FeatureOrCreatureStatsActionsFieldVar" + str(self.Row))
                    self.ReactionsFieldVar.UpdateTag("FeatureOrCreatureStatsReactionsFieldVar" + str(self.Row))
                    self.InventoryFieldVar.UpdateTag("FeatureOrCreatureStatsInventoryFieldVar" + str(self.Row))
                    self.LegendaryActionsAndLairActionsFieldVar.UpdateTag("FeatureOrCreatureStatsLegendaryActionsAndLairActionsFieldVar" + str(self.Row))
                    self.NotesFieldVar.UpdateTag("FeatureOrCreatureStatsNotesFieldVar" + str(self.Row))

                class FeatureConfig:
                    def __init__(self, master, FeatureVars):
                        self.DataSubmitted = BooleanVar()
                        self.Vars = {}
                        self.Vars["NameEntryVar"] = StringVar(value=FeatureVars["NameEntryVar"].get())
                        self.Vars["FeatureDescriptionVar"] = StringVar(value=FeatureVars["FeatureDescriptionVar"].get())

                        # Create Window
                        self.Window = Toplevel(master)
                        self.Window.wm_attributes("-toolwindow", 1)
                        self.Window.wm_title("Feature Description")

                        # Name Entry
                        self.NameFrame = LabelFrame(self.Window, text="Name:")
                        self.NameFrame.grid_columnconfigure(0, weight=1)
                        self.NameFrame.grid(row=0, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                        self.NameEntry = EntryExtended(self.NameFrame, justify=CENTER, width=20, textvariable=self.Vars["NameEntryVar"])
                        self.NameEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                        # Description Field
                        self.DescriptionFrame = LabelFrame(self.Window, text="Description:")
                        self.DescriptionFrame.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                        self.DescriptionField = ScrolledText(self.DescriptionFrame, Width=250, Height=300)
                        self.DescriptionField.grid(row=0, column=0)
                        self.DescriptionField.Text.insert(1.0, self.Vars["FeatureDescriptionVar"].get())

                        # Submit Button
                        self.SubmitButton = Button(self.Window, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
                        self.SubmitButton.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)

                        # Cancel Button
                        self.CancelButton = Button(self.Window, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
                        self.CancelButton.grid(row=2, column=1, sticky=NSEW, padx=2, pady=2)

                        # Prevent Main Window Input
                        self.Window.grab_set()

                        # Handle Config Window Geometry and Focus
                        GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst)
                        self.Window.focus_force()

                        # Focus on Name Entry
                        self.NameEntry.focus_set()

                    def Submit(self):
                        self.DataSubmitted.set(True)
                        self.Vars["FeatureDescriptionVar"].set(self.DescriptionField.get())
                        self.Window.destroy()

                    def Cancel(self):
                        self.DataSubmitted.set(False)
                        self.Window.destroy()

    # Spellcasting
    class Spellcasting:
        def __init__(self, master):
            # Variables
            self.SpellPointsMaxEntryVar = StringVar()
            self.SpellPointsRemainingEntryVar = SavedStringVar("SpellPointsRemainingEntryVar")
            self.SpellUsingSpellPointsBoxVar = SavedBooleanVar("SpellUsingSpellPointsBoxVar")
            self.SpellUsingSpellPointsBoxVar.trace_add("write", lambda a, b, c: CharacterSheetInst.UpdateStatsAndInventory())
            self.ConcentrationBoxVar = SavedBooleanVar("ConcentrationBoxVar")

            # Center Rows and Columns
            master.grid_rowconfigure(0, weight=1)
            master.grid_rowconfigure(2, weight=1)
            master.grid_rowconfigure(4, weight=1)
            master.grid_rowconfigure(6, weight=1)
            master.grid_rowconfigure(8, weight=1)
            master.grid_columnconfigure(0, weight=1)
            master.grid_columnconfigure(2, weight=1)
            master.grid_columnconfigure(4, weight=1)
            master.grid_columnconfigure(6, weight=1)

            # Spellcasting Ability Frame
            self.SpellcastingAbilityFrame = LabelFrame(master, text="Spellcasting Abilities:")
            self.SpellcastingAbilityFrame.grid_columnconfigure(1, weight=1)
            self.SpellcastingAbilityFrame.grid_columnconfigure(2, weight=1)
            self.SpellcastingAbilityFrame.grid_columnconfigure(3, weight=1)
            self.SpellcastingAbilityFrame.grid(row=1, column=1, padx=2, pady=2, columnspan=3, sticky=NSEW)

            # Spellcasting Ability Labels
            self.SpellcastingAbilitySelectionLabel = Label(self.SpellcastingAbilityFrame, text="Ability", bd=2, relief=GROOVE)
            self.SpellcastingAbilitySelectionLabel.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)
            self.SpellSaveDCLabel = Label(self.SpellcastingAbilityFrame, text="Spell Save DC", bd=2, relief=GROOVE)
            self.SpellSaveDCLabel.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)
            self.SpellAttackModifierLabel = Label(self.SpellcastingAbilityFrame, text="Spell Attack Modifier", bd=2, relief=GROOVE)
            self.SpellAttackModifierLabel.grid(row=2, column=0, padx=2, pady=2, sticky=NSEW)

            # Spellcasting Abilities List
            self.SpellcastingAbilitiesList = []

            # Spellcasting Abilities
            for CurrentIndex in range(1, 4):
                AbilityScoreDerivatives(self.SpellcastingAbilityFrame, self.SpellcastingAbilitiesList, "Spellcasting", CurrentIndex, AttackTypeStringSuffix="Spell")

            # Concentration
            self.ConcentrationTrueColor = "#7aff63"
            self.ConcentrationFalseColor = GlobalInst.ButtonColor
            self.ConcentrationBoxFont = font.Font(size=16)
            self.ConcentrationBox = Checkbutton(master, text="Concentration", variable=self.ConcentrationBoxVar, font=self.ConcentrationBoxFont, indicatoron=False, bg=self.ConcentrationFalseColor,
                                                selectcolor=self.ConcentrationTrueColor)
            self.ConcentrationBox.grid(row=3, column=1, padx=2, pady=2, sticky=NSEW)

            # Spell Notes Frame
            self.SpellNotesFrame = LabelFrame(master, text="Spell Notes:")
            self.SpellNotesFrame.grid(row=5, column=1, padx=2, pady=2, rowspan=3)
            self.SpellNotesField = ScrolledText(self.SpellNotesFrame, Width=225, Height=330, SavedDataTag="SpellNotesField")
            self.SpellNotesField.grid(row=0, column=0)

            # Spell Slots Frame
            self.SpellSlotsFrame = LabelFrame(master, text="Spell Slots:")
            self.SpellSlotsFrame.grid(row=3, column=3, padx=2, pady=2, rowspan=3)

            # Spell Slots Headers
            self.SpellSlotsLevelHeader = Label(self.SpellSlotsFrame, text="Level", bd=2, relief=GROOVE)
            self.SpellSlotsLevelHeader.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)
            self.SpellSlotsSlotsHeader = Label(self.SpellSlotsFrame, text="Slots", bd=2, relief=GROOVE)
            self.SpellSlotsSlotsHeader.grid(row=0, column=1, padx=2, pady=2, sticky=NSEW)
            self.SpellSlotsUsedHeader = Label(self.SpellSlotsFrame, text="Used", bd=2, relief=GROOVE)
            self.SpellSlotsUsedHeader.grid(row=0, column=2, padx=2, pady=2, sticky=NSEW)

            # Spell Slots List
            self.SpellSlotsList = []

            # Spell Slots Rows
            self.SpellSlotsFirstLevel = self.SpellSlotsLevel(self.SpellSlotsFrame, self.SpellSlotsList, "1st", 2, 1)
            self.SpellSlotsSecondLevel = self.SpellSlotsLevel(self.SpellSlotsFrame, self.SpellSlotsList, "2nd", 3, 2)
            self.SpellSlotsThirdLevel = self.SpellSlotsLevel(self.SpellSlotsFrame, self.SpellSlotsList, "3rd", 5, 3)
            self.SpellSlotsFourthLevel = self.SpellSlotsLevel(self.SpellSlotsFrame, self.SpellSlotsList, "4th", 6, 4)
            self.SpellSlotsFifthLevel = self.SpellSlotsLevel(self.SpellSlotsFrame, self.SpellSlotsList, "5th", 7, 5)
            self.SpellSlotsSixthLevel = self.SpellSlotsLevel(self.SpellSlotsFrame, self.SpellSlotsList, "6th", 9, 6)
            self.SpellSlotsSeventhLevel = self.SpellSlotsLevel(self.SpellSlotsFrame, self.SpellSlotsList, "7th", 10, 7)
            self.SpellSlotsEighthLevel = self.SpellSlotsLevel(self.SpellSlotsFrame, self.SpellSlotsList, "8th", 11, 8)
            self.SpellSlotsNinthLevel = self.SpellSlotsLevel(self.SpellSlotsFrame, self.SpellSlotsList, "9th", 13, 9)

            # Spell Points Frame
            self.SpellPointsFrame = LabelFrame(master, text="Spell Points:")
            self.SpellPointsFrame.grid(row=7, column=3, padx=2, pady=2, sticky=NSEW)
            self.SpellUsingSpellPointsBox = Checkbutton(self.SpellPointsFrame, variable=self.SpellUsingSpellPointsBoxVar, text="Using\nSpell\nPoints")
            self.SpellUsingSpellPointsBox.grid(row=0, column=0, columnspan=2)
            self.SpellPointsMaxHeader = Label(self.SpellPointsFrame, text="Max", bd=2, relief=GROOVE)
            self.SpellPointsMaxHeader.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)
            self.SpellPointsMaxEntry = EntryExtended(self.SpellPointsFrame, justify=CENTER, width=5, cursor="arrow", textvariable=self.SpellPointsMaxEntryVar)
            self.SpellPointsMaxEntry.grid(row=1, column=1, padx=2, pady=2, sticky=NSEW)
            self.SpellPointsMaxEntryStatModifierInst = StatModifier(self.SpellPointsMaxEntry, "<Button-1>", "Left-click on the spell points max to set a stat modifier.", "Spell Points Max", Prefix="SpellPointsMaxEntry")
            self.SpellPointsRemainingHeader = Label(self.SpellPointsFrame, text="Remaining", bd=2, relief=GROOVE)
            self.SpellPointsRemainingHeader.grid(row=2, column=0, padx=2, pady=2, sticky=NSEW)
            self.SpellPointsRemainingEntry = EntryExtended(self.SpellPointsFrame, justify=CENTER, width=5, textvariable=self.SpellPointsRemainingEntryVar, state=DISABLED, disabledbackground=GlobalInst.ButtonColor,
                                                           disabledforeground="black", cursor="arrow")
            self.SpellPointsRemainingEntry.grid(row=2, column=1, padx=2, pady=2, sticky=NSEW)
            self.SpellPointsRemainingEntry.bind("<Button-1>", self.ExpendSpellPoints)
            self.SpellPointsRemainingEntry.bind("<Button-3>", self.RestoreSpellPoints)
            self.SpellPointsRemainingTooltip = Tooltip(self.SpellPointsRemainingEntry, "Left-click on the spell points remaining to expend points.  Right-click to restore.")

            # Spell Entries Frame
            self.SpellEntriesFrame = LabelFrame(master, text="Spells:")
            self.SpellEntriesFrame.grid(row=1, column=5, padx=2, pady=2, sticky=NSEW, rowspan=7)

            # Spell Entries Notebook
            self.SpellEntriesNotebook = ttk.Notebook(self.SpellEntriesFrame, height=446)
            self.SpellEntriesNotebook.grid(row=0, column=0, padx=2, pady=2)
            self.SpellEntriesNotebook.enable_traversal()

            # Spell Lists List
            self.SpellListsList = []

            # Cantrips Page
            self.CantripsPage = Frame(self.SpellEntriesNotebook)
            self.SpellEntriesNotebook.add(self.CantripsPage, text="Cantrips")
            self.CantripsInst = self.SpellList(self.CantripsPage, self.SpellListsList, "Cantrips")

            # 1st-Level Page
            self.FirstLevelPage = Frame(self.SpellEntriesNotebook)
            self.SpellEntriesNotebook.add(self.FirstLevelPage, text="1st")
            self.FirstLevelInst = self.SpellList(self.FirstLevelPage, self.SpellListsList, "First")

            # 2nd-Level Page
            self.SecondLevelPage = Frame(self.SpellEntriesNotebook)
            self.SpellEntriesNotebook.add(self.SecondLevelPage, text="2nd")
            self.SecondLevelInst = self.SpellList(self.SecondLevelPage, self.SpellListsList, "Second")

            # 3rd-Level Page
            self.ThirdLevelPage = Frame(self.SpellEntriesNotebook)
            self.SpellEntriesNotebook.add(self.ThirdLevelPage, text="3rd")
            self.ThirdLevelInst = self.SpellList(self.ThirdLevelPage, self.SpellListsList, "Third")

            # 4th-Level Page
            self.FourthLevelPage = Frame(self.SpellEntriesNotebook)
            self.SpellEntriesNotebook.add(self.FourthLevelPage, text="4th")
            self.FourthLevelInst = self.SpellList(self.FourthLevelPage, self.SpellListsList, "Fourth")

            # 5th-Level Page
            self.FifthLevelPage = Frame(self.SpellEntriesNotebook)
            self.SpellEntriesNotebook.add(self.FifthLevelPage, text="5th")
            self.FifthLevelInst = self.SpellList(self.FifthLevelPage, self.SpellListsList, "Fifth")

            # 6th-Level Page
            self.SixthLevelPage = Frame(self.SpellEntriesNotebook)
            self.SpellEntriesNotebook.add(self.SixthLevelPage, text="6th")
            self.SixthLevelInst = self.SpellList(self.SixthLevelPage, self.SpellListsList, "Sixth")

            # 7th-Level Page
            self.SeventhLevelPage = Frame(self.SpellEntriesNotebook)
            self.SpellEntriesNotebook.add(self.SeventhLevelPage, text="7th")
            self.SeventhLevelInst = self.SpellList(self.SeventhLevelPage, self.SpellListsList, "Seventh")

            # 8th-Level Page
            self.EighthLevelPage = Frame(self.SpellEntriesNotebook)
            self.SpellEntriesNotebook.add(self.EighthLevelPage, text="8th")
            self.EighthLevelInst = self.SpellList(self.EighthLevelPage, self.SpellListsList, "Eighth")

            # 9th-Level Page
            self.NinthLevelPage = Frame(self.SpellEntriesNotebook)
            self.SpellEntriesNotebook.add(self.NinthLevelPage, text="9th")
            self.NinthLevelInst = self.SpellList(self.NinthLevelPage, self.SpellListsList, "Ninth")

        def CalculateSpellPoints(self):
            # Using Spell Points
            if self.SpellUsingSpellPointsBoxVar.get():
                # Get Total Points
                TotalPoints = 0
                for Level in self.SpellSlotsList:
                    TotalPoints += (Level.PointValue * GlobalInst.GetStringVarAsNumber(Level.SlotsEntryVar))
                TotalPoints += self.SpellPointsMaxEntryStatModifierInst.GetModifier()

                # Set Var
                self.SpellPointsMaxEntryVar.set(str(TotalPoints))

            # Not Using Spell Points
            else:
                self.SpellPointsMaxEntryVar.set("N/A")

        def ExpendSpellPoints(self, event):
            # Check Whether Using Spell Points
            if self.SpellUsingSpellPointsBoxVar.get():
                pass
            else:
                messagebox.showerror("Invalid Entry", "Not using spell points.")
                return

            # Create Window and Wait
            ExpendSpellPointsMenuInst = self.ExpendOrRestoreSpellPointsMenu(WindowInst, "Expend")
            WindowInst.wait_window(ExpendSpellPointsMenuInst.Window)

            # Handle Variables
            if ExpendSpellPointsMenuInst.DataSubmitted.get():
                CurrentRemainingPoints = GlobalInst.GetStringVarAsNumber(self.SpellPointsRemainingEntryVar)
                SpellSlotString = ExpendSpellPointsMenuInst.SpellSlotDropdownVar.get()
                SpellSlotAmount = 0
                if SpellSlotString != "":
                    for Level in self.SpellSlotsList:
                        if SpellSlotString == Level.SlotLevel:
                            SpellSlotAmount = Level.PointValue
                            break
                ManualAmount = GlobalInst.GetStringVarAsNumber(ExpendSpellPointsMenuInst.ManualAmountEntryVar)
                NewRemainingPoints = max(0, (CurrentRemainingPoints - SpellSlotAmount - ManualAmount))
                self.SpellPointsRemainingEntryVar.set(str(NewRemainingPoints))

        def RestoreSpellPoints(self, event):
            # Check Whether Using Spell Points
            if self.SpellUsingSpellPointsBoxVar.get():
                pass
            else:
                messagebox.showerror("Invalid Entry", "Not using spell points.")
                return

            # Create Window and Wait
            ExpendSpellPointsMenuInst = self.ExpendOrRestoreSpellPointsMenu(WindowInst, "Restore")
            WindowInst.wait_window(ExpendSpellPointsMenuInst.Window)

            # Handle Variables
            if ExpendSpellPointsMenuInst.DataSubmitted.get():
                CurrentRemainingPoints = GlobalInst.GetStringVarAsNumber(self.SpellPointsRemainingEntryVar)
                MaxPoints = GlobalInst.GetStringVarAsNumber(self.SpellPointsMaxEntryVar)
                SpellSlotString = ExpendSpellPointsMenuInst.SpellSlotDropdownVar.get()
                SpellSlotAmount = 0
                if SpellSlotString != "":
                    for Level in self.SpellSlotsList:
                        if SpellSlotString == Level.SlotLevel:
                            SpellSlotAmount = Level.PointValue
                            break
                ManualAmount = GlobalInst.GetStringVarAsNumber(ExpendSpellPointsMenuInst.ManualAmountEntryVar)
                NewRemainingPoints = min(MaxPoints, (CurrentRemainingPoints + SpellSlotAmount + ManualAmount))
                self.SpellPointsRemainingEntryVar.set(str(NewRemainingPoints))

        class SpellList:
            def __init__(self, master, List, LevelName):
                # Store Parameters
                self.LevelName = LevelName

                # Variables
                self.ScrollingDisabledVar = BooleanVar(value=False)

                # Add to List
                List.append(self)

                # Spell List Frame
                self.SpellListFrame = Frame(master)
                self.SpellListFrame.grid(row=0, column=0)

                # Spell List Scrolled Canvas
                self.SpellListScrolledCanvas = ScrolledCanvas(self.SpellListFrame, Width=342, Height=447, ScrollingDisabledVar=self.ScrollingDisabledVar)
                self.SpellListScrolledCanvas.BindEnterAndLeaveToBindMouseWheel()

                # Headers
                self.PreparedHeader = Label(self.SpellListScrolledCanvas.WindowFrame, text="Prep.", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
                self.PreparedHeader.grid(row=0, column=0, sticky=NSEW)
                self.PreparedHeader.bind("<Button-1>", lambda event: self.Sort("Prepared"))
                self.PreparedHeader.bind("<Button-3>", lambda event: self.Sort("Prepared", Reverse=True))
                self.PreparedTooltip = Tooltip(self.PreparedHeader, GlobalInst.SortTooltipString[:-29])
                self.NameHeader = Label(self.SpellListScrolledCanvas.WindowFrame, text="Name", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
                self.NameHeader.grid(row=0, column=1, sticky=NSEW)
                self.NameHeader.bind("<Button-1>", lambda event: self.Sort("Name"))
                self.NameHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Name", SearchMode=True))
                self.NameHeader.bind("<Button-3>", lambda event: self.Sort("Name", Reverse=True))
                self.NameTooltip = Tooltip(self.NameHeader, GlobalInst.SortTooltipString)
                self.SortOrderHeader = Label(self.SpellListScrolledCanvas.WindowFrame, text="Sort\nOrder", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
                self.SortOrderHeader.grid(row=0, column=2, sticky=NSEW)
                self.SortOrderHeader.bind("<Button-1>", lambda event: self.Sort("Sort Order"))
                self.SortOrderHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Sort Order", SearchMode=True))
                self.SortOrderHeader.bind("<Button-3>", lambda event: self.Sort("Sort Order", Reverse=True))
                self.SortOrderTooltip = Tooltip(self.SortOrderHeader, GlobalInst.SortTooltipString)

                # Spell List Entries List
                self.SpellListEntriesList = []

                # Spell List Entries Count
                self.SpellListEntriesCount = 100

                # Sort Order Values
                self.SortOrderValuesList = [""]
                for CurrentIndex in range(1, self.SpellListEntriesCount + 1):
                    self.SortOrderValuesList.append(str(CurrentIndex))

                # Spell List Entries
                for CurrentIndex in range(1, self.SpellListEntriesCount + 1):
                    CurrentEntry = self.SpellListEntry(self.SpellListScrolledCanvas, self.SpellListEntriesList, self.LevelName, self.SortOrderValuesList, self.ScrollingDisabledVar, CurrentIndex)
                    CurrentEntry.Display(CurrentIndex)

            def Sort(self, Column, Reverse=False, SearchMode=False):
                # List to Sort
                ListToSort = []

                if SearchMode:
                    # Get Search String
                    SearchStringPrompt = StringPrompt(WindowInst, "Search", "What do you want to search for?")
                    WindowInst.wait_window(SearchStringPrompt.Window)
                    if SearchStringPrompt.DataSubmitted.get():
                        SearchString = SearchStringPrompt.StringEntryVar.get()
                    else:
                        return

                    # Add Fields to List
                    for CurrentEntry in self.SpellListEntriesList:
                        ListToSort.append((CurrentEntry, CurrentEntry.SortFields[Column].get().lower()))

                    # Sort the List
                    SortedList = sorted(ListToSort, key=lambda x: (x[1] == "", SearchString not in x[1]))
                else:
                    if Column == "Prepared":
                        # Add Fields to List
                        for CurrentEntry in self.SpellListEntriesList:
                            ListToSort.append((CurrentEntry, CurrentEntry.SortFields["Name"].get(), CurrentEntry.SortFields[Column].get()))

                        # Sort the List
                        SortedList = sorted(ListToSort, key=lambda x: ((not Reverse and x[1] == "") or (Reverse and x[1] != ""), not x[2]), reverse=Reverse)
                    elif Column == "Name":
                        # Add Fields to List
                        for CurrentEntry in self.SpellListEntriesList:
                            ListToSort.append((CurrentEntry, CurrentEntry.SortFields[Column].get()))

                        # Sort the List
                        SortedList = sorted(ListToSort, key=lambda x: ((not Reverse and x[1] == "") or (Reverse and x[1] != ""), x[1].lower()), reverse=Reverse)
                    elif Column == "Sort Order":
                        # Add Fields to List
                        for CurrentEntry in self.SpellListEntriesList:
                            ListToSort.append((CurrentEntry, GlobalInst.GetStringVarAsNumber(CurrentEntry.SortFields[Column])))

                        # Sort the List
                        SortedList = sorted(ListToSort, key=lambda x: ((not Reverse and x[1] == 0) or (Reverse and x[1] != 0), x[1]), reverse=Reverse)
                    else:
                        return

                # Adjust Entries to New Order
                for CurrentIndex in range(len(SortedList)):
                    SortedList[CurrentIndex][0].Display(CurrentIndex + 1)

                # Flag Save Prompt
                SavingAndOpeningInst.SavePrompt = True

                # Update Window Title
                WindowInst.UpdateWindowTitle()

            class SpellListEntry:
                def __init__(self, master, List, LevelName, SortOrderValuesList, ScrollingDisabledVar, Row):
                    # Store Parameters
                    self.master = master
                    self.LevelName = LevelName
                    self.SortOrderValuesList = SortOrderValuesList
                    self.ScrollingDisabledVar = ScrollingDisabledVar
                    self.Row = Row

                    # Variables
                    self.PreparedBoxVar = SavedBooleanVar()
                    self.NameEntryVar = SavedStringVar()
                    self.SortOrderVar = SavedStringVar()
                    self.SchoolEntryVar = SavedStringVar()
                    self.CastingTimeVar = SavedStringVar()
                    self.RangeVar = SavedStringVar()
                    self.ComponentsVar = SavedStringVar()
                    self.DurationVar = SavedStringVar()
                    self.DescriptionVar = SavedStringVar()

                    # Spell Vars
                    self.SpellVars = {}
                    self.SpellVars["NameEntryVar"] = self.NameEntryVar
                    self.SpellVars["SchoolEntryVar"] = self.SchoolEntryVar
                    self.SpellVars["CastingTimeVar"] = self.CastingTimeVar
                    self.SpellVars["RangeVar"] = self.RangeVar
                    self.SpellVars["ComponentsVar"] = self.ComponentsVar
                    self.SpellVars["DurationVar"] = self.DurationVar
                    self.SpellVars["DescriptionVar"] = self.DescriptionVar

                    # Sort Fields
                    self.SortFields = {}
                    self.SortFields["Prepared"] = self.PreparedBoxVar
                    self.SortFields["Name"] = self.NameEntryVar
                    self.SortFields["Sort Order"] = self.SortOrderVar

                    # Add to List
                    List.append(self)

                    # Prepared Box
                    self.PreparedBox = Checkbutton(master.WindowFrame, variable=self.PreparedBoxVar)

                    # Name Entry
                    self.NameEntry = EntryExtended(master.WindowFrame, width=42, justify=CENTER, state=DISABLED, disabledbackground=GlobalInst.ButtonColor, disabledforeground="black", textvariable=self.NameEntryVar,
                                                   cursor="arrow")
                    self.NameEntry.bind("<Button-1>", self.Set)
                    self.NameTooltip = Tooltip(self.NameEntry, "Left-click on a spell list entry to set a name and description.")

                    # Sort Order
                    self.SortOrder = DropdownExtended(master.WindowFrame, textvariable=self.SortOrderVar, values=self.SortOrderValuesList, width=5, state="readonly", justify=CENTER)
                    self.SortOrder.bind("<Enter>", self.DisableScrolling)
                    self.SortOrder.bind("<Leave>", self.EnableScrolling)

                def Set(self, event):
                    # Create Config Window and Wait
                    SpellConfigInst = self.SpellConfig(WindowInst, self.SpellVars)
                    WindowInst.wait_window(SpellConfigInst.Window)

                    # Handle Variables
                    if SpellConfigInst.DataSubmitted.get():
                        for Tag, Var in SpellConfigInst.Vars.items():
                            self.SpellVars[Tag].set(Var.get())

                def Display(self, Row):
                    self.Row = Row

                    # Set Row Size
                    self.master.WindowFrame.grid_rowconfigure(self.Row, minsize=26)

                    # Place in Grid
                    self.PreparedBox.grid(row=self.Row, column=0, sticky=NSEW)
                    self.NameEntry.grid(row=self.Row, column=1, sticky=NSEW)
                    self.SortOrder.grid(row=self.Row, column=2, sticky=NSEW)

                    # Update Tab Order
                    self.PreparedBox.lift()
                    self.NameEntry.lift()
                    self.SortOrder.lift()

                    # Update Tags
                    self.PreparedBoxVar.UpdateTag("SpellEntryPrepared" + self.LevelName + str(self.Row))
                    self.NameEntryVar.UpdateTag("SpellEntryName" + self.LevelName + str(self.Row))
                    self.SortOrderVar.UpdateTag("SpellEntrySortOrder" + self.LevelName + str(self.Row))
                    self.SchoolEntryVar.UpdateTag("SchoolEntryName" + self.LevelName + str(self.Row))
                    self.CastingTimeVar.UpdateTag("SpellEntryCastingTime" + self.LevelName + str(self.Row))
                    self.RangeVar.UpdateTag("SpellEntryRange" + self.LevelName + str(self.Row))
                    self.ComponentsVar.UpdateTag("SpellEntryComponents" + self.LevelName + str(self.Row))
                    self.DurationVar.UpdateTag("SpellEntryDuration" + self.LevelName + str(self.Row))
                    self.DescriptionVar.UpdateTag("SpellEntryDescription" + self.LevelName + str(self.Row))

                def DisableScrolling(self, event):
                    self.ScrollingDisabledVar.set(True)

                def EnableScrolling(self, event):
                    self.ScrollingDisabledVar.set(False)

                class SpellConfig:
                    def __init__(self, master, SpellVars):
                        self.DataSubmitted = BooleanVar()
                        self.Vars = {}
                        self.Vars["NameEntryVar"] = StringVar(value=SpellVars["NameEntryVar"].get())
                        self.Vars["SchoolEntryVar"] = StringVar(value=SpellVars["SchoolEntryVar"].get())
                        self.Vars["CastingTimeVar"] = StringVar(value=SpellVars["CastingTimeVar"].get())
                        self.Vars["RangeVar"] = StringVar(value=SpellVars["RangeVar"].get())
                        self.Vars["ComponentsVar"] = StringVar(value=SpellVars["ComponentsVar"].get())
                        self.Vars["DurationVar"] = StringVar(value=SpellVars["DurationVar"].get())
                        self.Vars["DescriptionVar"] = StringVar(value=SpellVars["DescriptionVar"].get())

                        # Create Window
                        self.Window = Toplevel(master)
                        self.Window.wm_attributes("-toolwindow", 1)
                        self.Window.wm_title("Spell Description")

                        # Name Entry
                        self.NameFrame = LabelFrame(self.Window, text="Name:")
                        self.NameFrame.grid_columnconfigure(0, weight=1)
                        self.NameFrame.grid(row=0, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                        self.NameEntry = EntryExtended(self.NameFrame, justify=CENTER, width=20, textvariable=self.Vars["NameEntryVar"])
                        self.NameEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                        # School Entry
                        self.SchoolFrame = LabelFrame(self.Window, text="School:")
                        self.SchoolFrame.grid_columnconfigure(0, weight=1)
                        self.SchoolFrame.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                        self.SchoolEntry = EntryExtended(self.SchoolFrame, justify=CENTER, width=10, textvariable=self.Vars["SchoolEntryVar"])
                        self.SchoolEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                        # Casting Time
                        self.CastingTimeFrame = LabelFrame(self.Window, text="Casting Time:")
                        self.CastingTimeFrame.grid(row=2, column=0, padx=2, pady=2, sticky=NSEW)
                        self.CastingTimeField = ScrolledText(self.CastingTimeFrame, Width=121, Height=34)
                        self.CastingTimeField.grid(row=0, column=0)
                        self.CastingTimeField.Text.insert(1.0, self.Vars["CastingTimeVar"].get())

                        # Range
                        self.RangeFrame = LabelFrame(self.Window, text="Range:")
                        self.RangeFrame.grid(row=2, column=1, padx=2, pady=2, sticky=NSEW)
                        self.RangeField = ScrolledText(self.RangeFrame, Width=121, Height=34)
                        self.RangeField.grid(row=0, column=0)
                        self.RangeField.Text.insert(1.0, self.Vars["RangeVar"].get())

                        # Components
                        self.ComponentsFrame = LabelFrame(self.Window, text="Components:")
                        self.ComponentsFrame.grid(row=3, column=0, padx=2, pady=2, sticky=NSEW)
                        self.ComponentsField = ScrolledText(self.ComponentsFrame, Width=121, Height=34)
                        self.ComponentsField.grid(row=0, column=0)
                        self.ComponentsField.Text.insert(1.0, self.Vars["ComponentsVar"].get())

                        # Duration
                        self.DurationFrame = LabelFrame(self.Window, text="Duration:")
                        self.DurationFrame.grid(row=3, column=1, padx=2, pady=2, sticky=NSEW)
                        self.DurationField = ScrolledText(self.DurationFrame, Width=121, Height=34)
                        self.DurationField.grid(row=0, column=0)
                        self.DurationField.Text.insert(1.0, self.Vars["DurationVar"].get())

                        # Description Field
                        self.DescriptionFrame = LabelFrame(self.Window, text="Description:")
                        self.DescriptionFrame.grid(row=4, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                        self.DescriptionField = ScrolledText(self.DescriptionFrame, Width=250, Height=300)
                        self.DescriptionField.grid(row=0, column=0)
                        self.DescriptionField.Text.insert(1.0, self.Vars["DescriptionVar"].get())

                        # Buttons
                        self.SubmitButton = Button(self.Window, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
                        self.SubmitButton.grid(row=5, column=0, sticky=NSEW, padx=2, pady=2)
                        self.CancelButton = Button(self.Window, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
                        self.CancelButton.grid(row=5, column=1, sticky=NSEW, padx=2, pady=2)

                        # Prevent Main Window Input
                        self.Window.grab_set()

                        # Handle Config Window Geometry and Focus
                        GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst)
                        self.Window.focus_force()

                        # Focus on Name Entry
                        self.NameEntry.focus_set()

                    def Submit(self):
                        self.DataSubmitted.set(True)
                        self.Vars["CastingTimeVar"].set(self.CastingTimeField.Text.get("1.0", "end-1c"))
                        self.Vars["RangeVar"].set(self.RangeField.Text.get("1.0", "end-1c"))
                        self.Vars["ComponentsVar"].set(self.ComponentsField.Text.get("1.0", "end-1c"))
                        self.Vars["DurationVar"].set(self.DurationField.Text.get("1.0", "end-1c"))
                        self.Vars["DescriptionVar"].set(self.DescriptionField.Text.get("1.0", "end-1c"))
                        self.Window.destroy()

                    def Cancel(self):
                        self.DataSubmitted.set(False)
                        self.Window.destroy()

        class SpellSlotsLevel:
            def __init__(self, master, List, SlotLevel, PointValue, Row):
                self.Row = Row
                self.SlotLevel = SlotLevel
                self.SlotsEntryVar = SavedStringVar(self.SlotLevel + "SlotsEntryVar")
                self.SlotsEntryVar.trace_add("write", lambda a, b, c: CharacterSheetInst.UpdateStatsAndInventory())
                self.UsedEntryVar = SavedStringVar(self.SlotLevel + "UsedEntryVar")
                self.PointValue = PointValue

                # Add to List
                List.append(self)

                # Label
                self.SlotLabel = Label(master, text=self.SlotLevel, bd=2, relief=GROOVE)
                self.SlotLabel.grid(row=self.Row, column=0, padx=2, pady=2, sticky=NSEW)

                # Slots
                self.SlotsEntry = EntryExtended(master, width=1, justify=CENTER, textvariable=self.SlotsEntryVar)
                self.SlotsEntry.ConfigureValidation(lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Spell slots must be whole numbers.", MinValue=0, LessThanMinString="Spell slots cannot be less than 0."), "key")
                self.SlotsEntry.grid(row=self.Row, column=1, padx=2, pady=2, sticky=NSEW)

                # Used
                self.UsedEntry = EntryExtended(master, width=1, justify=CENTER, textvariable=self.UsedEntryVar)
                self.UsedEntry.grid(row=self.Row, column=2, padx=2, pady=2, sticky=NSEW)

        class ExpendOrRestoreSpellPointsMenu:
            def __init__(self, master, Mode):
                self.DataSubmitted = BooleanVar()
                self.SpellSlotDropdownVar = StringVar()
                self.ManualAmountEntryVar = StringVar()
                self.Mode = Mode

                # Create Window
                self.Window = Toplevel(master)
                self.Window.wm_attributes("-toolwindow", 1)
                self.Window.wm_title(self.Mode + " Spell Points")

                # Labels
                self.SpellSlotLabel = Label(self.Window, text="Spell Level", bd=2, relief=GROOVE)
                self.SpellSlotLabel.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)
                self.ManualAmountLabel = Label(self.Window, text="Manual Amount", bd=2, relief=GROOVE)
                self.ManualAmountLabel.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)

                # Amount Inputs
                self.SpellSlotDropdown = DropdownExtended(self.Window, textvariable=self.SpellSlotDropdownVar, values=["", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th"], width=4, state="readonly", justify=CENTER)
                self.SpellSlotDropdown.bind("<Return>", lambda event: self.Submit())
                self.SpellSlotDropdown.grid(row=0, column=1, padx=2, pady=2, sticky=NSEW)
                self.ManualAmountEntry = EntryExtended(self.Window, justify=CENTER, width=5, textvariable=self.ManualAmountEntryVar)
                self.ManualAmountEntry.ConfigureValidation(
                    lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Manual amount must be a whole number.", MinValue=0, LessThanMinString="Manual amount cannot be less than 0."), "key")
                self.ManualAmountEntry.bind("<Return>", lambda event: self.Submit())
                self.ManualAmountEntry.grid(row=1, column=1, padx=2, pady=2, sticky=NSEW)

                # Buttons
                self.ButtonsFrame = Frame(self.Window)
                self.ButtonsFrame.grid_columnconfigure(0, weight=1)
                self.ButtonsFrame.grid_columnconfigure(1, weight=1)
                self.ButtonsFrame.grid(row=2, column=0, columnspan=2, sticky=NSEW)
                self.SubmitButton = Button(self.ButtonsFrame, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
                self.SubmitButton.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)
                self.CancelButton = Button(self.ButtonsFrame, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
                self.CancelButton.grid(row=0, column=1, padx=2, pady=2, sticky=NSEW)

                # Prevent Main Window Input
                self.Window.grab_set()

                # Handle Config Window Geometry and Focus
                GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst)
                self.Window.focus_force()
                self.SpellSlotDropdown.focus_set()

            def Submit(self):
                self.DataSubmitted.set(True)
                self.Window.destroy()

            def Cancel(self):
                self.DataSubmitted.set(False)
                self.Window.destroy()

    # Inventory
    class Inventory:
        def __init__(self, master):
            # Variables
            self.CoinsEntryCPVar = SavedStringVar("CoinsEntryCPVar")
            self.CoinsEntryCPVar.trace_add("write", lambda a, b, c: CharacterSheetInst.UpdateStatsAndInventory())
            self.CoinsEntrySPVar = SavedStringVar("CoinsEntrySPVar")
            self.CoinsEntrySPVar.trace_add("write", lambda a, b, c: CharacterSheetInst.UpdateStatsAndInventory())
            self.CoinsEntryEPVar = SavedStringVar("CoinsEntryEPVar")
            self.CoinsEntryEPVar.trace_add("write", lambda a, b, c: CharacterSheetInst.UpdateStatsAndInventory())
            self.CoinsEntryGPVar = SavedStringVar("CoinsEntryGPVar")
            self.CoinsEntryGPVar.trace_add("write", lambda a, b, c: CharacterSheetInst.UpdateStatsAndInventory())
            self.CoinsEntryPPVar = SavedStringVar("CoinsEntryPPVar")
            self.CoinsEntryPPVar.trace_add("write", lambda a, b, c: CharacterSheetInst.UpdateStatsAndInventory())
            self.ValueCP = Decimal(0.01)
            self.ValueSP = Decimal(0.1)
            self.ValueEP = Decimal(0.5)
            self.ValueGP = Decimal(1)
            self.ValuePP = Decimal(10)
            self.WeightPerCoin = Decimal(0.02)
            self.CoinValueEntryVar = StringVar()
            self.CoinWeightEntryVar = StringVar()
            self.CarryingCapacityVar = StringVar()
            self.TotalLoadEntryVar = StringVar()
            self.GearLoadEntryVar = StringVar()
            self.TreasureLoadEntryVar = StringVar()
            self.MiscLoadEntryVar = StringVar()
            self.TotalValueEntryVar = StringVar()
            self.GearValueEntryVar = StringVar()
            self.TreasureValueEntryVar = StringVar()
            self.MiscValueEntryVar = StringVar()
            self.ScrollingDisabledVar = BooleanVar(value=False)

            # Spending Coins Dictionary
            self.SpendingCoins = {}
            self.SpendingCoins["CP"] = self.CoinsEntryCPVar
            self.SpendingCoins["SP"] = self.CoinsEntrySPVar
            self.SpendingCoins["EP"] = self.CoinsEntryEPVar
            self.SpendingCoins["GP"] = self.CoinsEntryGPVar
            self.SpendingCoins["PP"] = self.CoinsEntryPPVar
            self.SpendingCoins["SPValueAsCP"] = Decimal(10)
            self.SpendingCoins["EPValueAsCP"] = Decimal(50)
            self.SpendingCoins["GPValueAsCP"] = Decimal(100)
            self.SpendingCoins["PPValueAsCP"] = Decimal(1000)

            # Denomination Values Dictionary
            self.DenominationValues = {}
            self.DenominationValues["cp"] = self.ValueCP
            self.DenominationValues["sp"] = self.ValueSP
            self.DenominationValues["ep"] = self.ValueEP
            self.DenominationValues["gp"] = self.ValueGP
            self.DenominationValues["pp"] = self.ValuePP
            self.DenominationValues[""] = 0

            # Center Widgets
            master.grid_rowconfigure(0, weight=1)
            master.grid_rowconfigure(3, weight=1)
            master.grid_columnconfigure(0, weight=1)
            master.grid_columnconfigure(2, weight=1)

            # Inventory Data Frame
            self.InventoryDataFrame = Frame(master)
            self.InventoryDataFrame.grid_columnconfigure(1, weight=1)
            self.InventoryDataFrame.grid_columnconfigure(3, weight=1)
            self.InventoryDataFrame.grid_columnconfigure(5, weight=1)
            self.InventoryDataFrame.grid_columnconfigure(7, weight=1)
            self.InventoryDataFrame.grid(row=1, column=1, sticky=NSEW)

            # Carrying Capacity
            self.CarryingCapacityFrame = LabelFrame(self.InventoryDataFrame, text="Carrying Capacity:")
            self.CarryingCapacityFrame.grid_rowconfigure(0, weight=1)
            self.CarryingCapacityFrame.grid_columnconfigure(0, weight=1)
            self.CarryingCapacityFrame.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW, rowspan=2)
            self.CarryingCapacityFont = font.Font(size=30)
            self.CarryingCapacityEntry = EntryExtended(self.CarryingCapacityFrame, width=5, justify=CENTER, textvariable=self.CarryingCapacityVar, cursor="arrow", font=self.CarryingCapacityFont)
            self.CarryingCapacityEntry.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)
            self.CarryingCapacityEntryStatModifierInst = StatModifier(self.CarryingCapacityEntry, "<Button-1>", "Left-click on the carrying capacity to set a stat modifier.", "Carrying Capacity", Prefix="CarryingCapacityEntry")

            # Loads
            self.LoadsFrame = LabelFrame(self.InventoryDataFrame, text="Loads (lbs.):")
            self.LoadsFrame.grid_rowconfigure(0, weight=1)
            self.LoadsFrame.grid_rowconfigure(1, weight=1)
            self.LoadsFrame.grid_rowconfigure(2, weight=1)
            self.LoadsFrame.grid_rowconfigure(3, weight=1)
            self.LoadsFrame.grid(row=0, column=2, padx=2, pady=2, sticky=NSEW, rowspan=2)
            self.TotalLoadLabel = Label(self.LoadsFrame, text="Total", bd=2, relief=GROOVE)
            self.TotalLoadLabel.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
            self.TotalLoadEntry = EntryExtended(self.LoadsFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.TotalLoadEntryVar,
                                                cursor="arrow")
            self.TotalLoadEntry.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
            self.GearLoadLabel = Label(self.LoadsFrame, text="Gear", bd=2, relief=GROOVE)
            self.GearLoadLabel.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
            self.GearLoadEntry = EntryExtended(self.LoadsFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.GearLoadEntryVar, cursor="arrow")
            self.GearLoadEntry.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
            self.TreasureLoadLabel = Label(self.LoadsFrame, text="Treasure", bd=2, relief=GROOVE)
            self.TreasureLoadLabel.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)
            self.TreasureLoadEntry = EntryExtended(self.LoadsFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.TreasureLoadEntryVar,
                                                   cursor="arrow")
            self.TreasureLoadEntry.grid(row=2, column=1, sticky=NSEW, padx=2, pady=2)
            self.MiscLoadLabel = Label(self.LoadsFrame, text="Misc", bd=2, relief=GROOVE)
            self.MiscLoadLabel.grid(row=3, column=0, sticky=NSEW, padx=2, pady=2)
            self.MiscLoadEntry = EntryExtended(self.LoadsFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.MiscLoadEntryVar, cursor="arrow")
            self.MiscLoadEntry.grid(row=3, column=1, sticky=NSEW, padx=2, pady=2)

            # Values
            self.ValuesFrame = LabelFrame(self.InventoryDataFrame, text="Values (gp):")
            self.ValuesFrame.grid_rowconfigure(0, weight=1)
            self.ValuesFrame.grid_rowconfigure(1, weight=1)
            self.ValuesFrame.grid_rowconfigure(2, weight=1)
            self.ValuesFrame.grid_rowconfigure(3, weight=1)
            self.ValuesFrame.grid(row=0, column=4, padx=2, pady=2, sticky=NSEW, rowspan=2)
            self.TotalValueLabel = Label(self.ValuesFrame, text="Total", bd=2, relief=GROOVE)
            self.TotalValueLabel.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
            self.TotalValueEntry = EntryExtended(self.ValuesFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.TotalValueEntryVar,
                                                 cursor="arrow")
            self.TotalValueEntry.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
            self.GearValueLabel = Label(self.ValuesFrame, text="Gear", bd=2, relief=GROOVE)
            self.GearValueLabel.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
            self.GearValueEntry = EntryExtended(self.ValuesFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.GearValueEntryVar,
                                                cursor="arrow")
            self.GearValueEntry.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
            self.TreasureValueLabel = Label(self.ValuesFrame, text="Treasure", bd=2, relief=GROOVE)
            self.TreasureValueLabel.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)
            self.TreasureValueEntry = EntryExtended(self.ValuesFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.TreasureValueEntryVar,
                                                    cursor="arrow")
            self.TreasureValueEntry.grid(row=2, column=1, sticky=NSEW, padx=2, pady=2)
            self.MiscValueLabel = Label(self.ValuesFrame, text="Misc", bd=2, relief=GROOVE)
            self.MiscValueLabel.grid(row=3, column=0, sticky=NSEW, padx=2, pady=2)
            self.MiscValueEntry = EntryExtended(self.ValuesFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.MiscValueEntryVar,
                                                cursor="arrow")
            self.MiscValueEntry.grid(row=3, column=1, sticky=NSEW, padx=2, pady=2)

            # Coins
            self.CoinsFrame = LabelFrame(self.InventoryDataFrame, text="Coins:")
            self.CoinsFrame.grid_rowconfigure(0, weight=1)
            self.CoinsFrame.grid_rowconfigure(4, weight=1)
            self.CoinsFrame.grid_columnconfigure(0, weight=1)
            self.CoinsFrame.grid_columnconfigure(2, weight=1)
            self.CoinsFrame.grid(row=0, column=6, padx=2, pady=2, sticky=NSEW, rowspan=2)
            self.CoinsInputHolderFrame = Frame(self.CoinsFrame)
            self.CoinsInputHolderFrame.grid(row=1, column=1)
            self.CoinsHeaderCP = Label(self.CoinsInputHolderFrame, text="CP", bd=2, relief=GROOVE)
            self.CoinsHeaderCP.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
            self.CoinsEntryCP = CoinsEntry(self.CoinsInputHolderFrame, width=5, justify=CENTER, textvariable=self.CoinsEntryCPVar)
            self.CoinsEntryCP.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
            self.CoinsHeaderSP = Label(self.CoinsInputHolderFrame, text="SP", bd=2, relief=GROOVE)
            self.CoinsHeaderSP.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
            self.CoinsEntrySP = CoinsEntry(self.CoinsInputHolderFrame, width=5, justify=CENTER, textvariable=self.CoinsEntrySPVar)
            self.CoinsEntrySP.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
            self.CoinsHeaderEP = Label(self.CoinsInputHolderFrame, text="EP", bd=2, relief=GROOVE)
            self.CoinsHeaderEP.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
            self.CoinsEntryEP = CoinsEntry(self.CoinsInputHolderFrame, width=5, justify=CENTER, textvariable=self.CoinsEntryEPVar)
            self.CoinsEntryEP.grid(row=1, column=2, sticky=NSEW, padx=2, pady=2)
            self.CoinsHeaderGP = Label(self.CoinsInputHolderFrame, text="GP", bd=2, relief=GROOVE)
            self.CoinsHeaderGP.grid(row=0, column=3, sticky=NSEW, padx=2, pady=2)
            self.CoinsEntryGP = CoinsEntry(self.CoinsInputHolderFrame, width=5, justify=CENTER, textvariable=self.CoinsEntryGPVar)
            self.CoinsEntryGP.grid(row=1, column=3, sticky=NSEW, padx=2, pady=2)
            self.CoinsHeaderPP = Label(self.CoinsInputHolderFrame, text="PP", bd=2, relief=GROOVE)
            self.CoinsHeaderPP.grid(row=0, column=4, sticky=NSEW, padx=2, pady=2)
            self.CoinsEntryPP = CoinsEntry(self.CoinsInputHolderFrame, width=5, justify=CENTER, textvariable=self.CoinsEntryPPVar)
            self.CoinsEntryPP.grid(row=1, column=4, sticky=NSEW, padx=2, pady=2)

            # Coin Value and Weight
            self.CoinValueAndWeightHolderFrame = Frame(self.CoinsFrame)
            self.CoinValueAndWeightHolderFrame.grid_columnconfigure(0, weight=1)
            self.CoinValueAndWeightHolderFrame.grid_columnconfigure(1, weight=1)
            self.CoinValueAndWeightHolderFrame.grid(row=2, column=1, sticky=NSEW)
            self.CoinValueHeader = Label(self.CoinValueAndWeightHolderFrame, text="Coin Value\n(gp)", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.CoinValueHeader.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
            self.CoinValueHeader.bind("<Button-1>", self.GainCoins)
            self.CoinValueHeader.bind("<Button-3>", self.SpendCoins)
            self.CoinValueTooltip = Tooltip(self.CoinValueHeader, "Left-click to gain coins.  Right-click to spend.")
            self.CoinValueEntry = EntryExtended(self.CoinValueAndWeightHolderFrame, width=13, justify=CENTER, textvariable=self.CoinValueEntryVar, state=DISABLED, disabledforeground="black",
                                                disabledbackground="light gray",
                                                cursor="arrow")
            self.CoinValueEntry.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
            self.CoinWeightHeader = Label(self.CoinValueAndWeightHolderFrame, text="Coin Weight\n(lbs.)", bd=2, relief=GROOVE)
            self.CoinWeightHeader.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
            self.CoinWeightEntry = EntryExtended(self.CoinValueAndWeightHolderFrame, width=13, justify=CENTER, textvariable=self.CoinWeightEntryVar, state=DISABLED, disabledforeground="black",
                                                 disabledbackground="light gray",
                                                 cursor="arrow")
            self.CoinWeightEntry.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)

            # Supplies
            self.FoodDisplay = self.SupplyDisplay(self.InventoryDataFrame, "1", "Food")
            self.FoodDisplay.grid(row=0, column=8, padx=2, pady=2, sticky=NSEW)
            self.WaterDisplay = self.SupplyDisplay(self.InventoryDataFrame, "8", "Water")
            self.WaterDisplay.grid(row=1, column=8, padx=2, pady=2, sticky=NSEW)

            # Inventory List Frame
            self.InventoryListFrame = LabelFrame(master, text="Inventory List:")
            self.InventoryListFrame.grid(row=2, column=1, padx=2, pady=2)

            # Inventory List Scrolled Canvas
            self.InventoryListScrolledCanvas = ScrolledCanvas(self.InventoryListFrame, Height=345, Width=693, ScrollingDisabledVar=self.ScrollingDisabledVar)
            self.InventoryListScrolledCanvas.BindEnterAndLeaveToBindMouseWheel()

            # Inventory List Headers
            self.InventoryListNameHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Name", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.InventoryListNameHeader.grid(row=0, column=0, sticky=NSEW)
            self.InventoryListNameHeader.bind("<Button-1>", lambda event: self.Sort("Name"))
            self.InventoryListNameHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Name", SearchMode=True))
            self.InventoryListNameHeader.bind("<Button-3>", lambda event: self.Sort("Name", Reverse=True))
            self.InventoryListNameTooltip = Tooltip(self.InventoryListNameHeader, GlobalInst.SortTooltipString)
            self.InventoryListCountHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Count", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.InventoryListCountHeader.grid(row=0, column=1, sticky=NSEW)
            self.InventoryListCountHeader.bind("<Button-1>", lambda event: self.Sort("Count"))
            self.InventoryListCountHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Count", SearchMode=True))
            self.InventoryListCountHeader.bind("<Button-3>", lambda event: self.Sort("Count", Reverse=True))
            self.InventoryListCountTooltip = Tooltip(self.InventoryListCountHeader, GlobalInst.SortTooltipString)
            self.InventoryListUnitWeightHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Unit Weight\n(lbs.)", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.InventoryListUnitWeightHeader.grid(row=0, column=2, sticky=NSEW)
            self.InventoryListUnitWeightHeader.bind("<Button-1>", lambda event: self.Sort("Unit Weight"))
            self.InventoryListUnitWeightHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Unit Weight", SearchMode=True))
            self.InventoryListUnitWeightHeader.bind("<Button-3>", lambda event: self.Sort("Unit Weight", Reverse=True))
            self.InventoryListUnitWeightTooltip = Tooltip(self.InventoryListUnitWeightHeader, GlobalInst.SortTooltipString)
            self.InventoryListUnitValueHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Unit Value", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.InventoryListUnitValueHeader.grid(row=0, column=3, sticky=NSEW)
            self.InventoryListUnitValueHeader.bind("<Button-1>", lambda event: self.Sort("Unit Value"))
            self.InventoryListUnitValueHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Unit Value", SearchMode=True))
            self.InventoryListUnitValueHeader.bind("<Button-3>", lambda event: self.Sort("Unit Value", Reverse=True))
            self.InventoryListUnitValueTooltip = Tooltip(self.InventoryListUnitValueHeader, GlobalInst.SortTooltipString)
            self.InventoryListUnitValueDenominationHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Value\nDenom.", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.InventoryListUnitValueDenominationHeader.grid(row=0, column=4, sticky=NSEW)
            self.InventoryListUnitValueDenominationHeader.bind("<Button-1>", lambda event: self.Sort("Value Denomination"))
            self.InventoryListUnitValueDenominationHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Value Denomination", SearchMode=True))
            self.InventoryListUnitValueDenominationHeader.bind("<Button-3>", lambda event: self.Sort("Value Denomination", Reverse=True))
            self.InventoryListUnitValueDenominationTooltip = Tooltip(self.InventoryListUnitValueDenominationHeader, GlobalInst.SortTooltipString)
            self.InventoryListTotalWeightHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Total Weight\n(lbs.)", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.InventoryListTotalWeightHeader.grid(row=0, column=5, sticky=NSEW)
            self.InventoryListTotalWeightHeader.bind("<Button-1>", lambda event: self.Sort("Total Weight"))
            self.InventoryListTotalWeightHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Total Weight", SearchMode=True))
            self.InventoryListTotalWeightHeader.bind("<Button-3>", lambda event: self.Sort("Total Weight", Reverse=True))
            self.InventoryListTotalWeightTooltip = Tooltip(self.InventoryListTotalWeightHeader, GlobalInst.SortTooltipString)
            self.InventoryListTotalValueHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Total Value\n(gp)", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.InventoryListTotalValueHeader.grid(row=0, column=6, sticky=NSEW)
            self.InventoryListTotalValueHeader.bind("<Button-1>", lambda event: self.Sort("Total Value"))
            self.InventoryListTotalValueHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Total Value", SearchMode=True))
            self.InventoryListTotalValueHeader.bind("<Button-3>", lambda event: self.Sort("Total Value", Reverse=True))
            self.InventoryListTotalValueTooltip = Tooltip(self.InventoryListTotalValueHeader, GlobalInst.SortTooltipString)
            self.InventoryListTagHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Tag", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.InventoryListTagHeader.grid(row=0, column=7, sticky=NSEW)
            self.InventoryListTagHeader.bind("<Button-1>", lambda event: self.Sort("Tag"))
            self.InventoryListTagHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Tag", SearchMode=True))
            self.InventoryListTagHeader.bind("<Button-3>", lambda event: self.Sort("Tag", Reverse=True))
            self.InventoryListTagTooltip = Tooltip(self.InventoryListTagHeader, GlobalInst.SortTooltipString)
            self.InventoryListSortOrderHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Sort\nOrder", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.InventoryListSortOrderHeader.grid(row=0, column=8, sticky=NSEW)
            self.InventoryListSortOrderHeader.bind("<Button-1>", lambda event: self.Sort("Sort Order"))
            self.InventoryListSortOrderHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Sort Order", SearchMode=True))
            self.InventoryListSortOrderHeader.bind("<Button-3>", lambda event: self.Sort("Sort Order", Reverse=True))
            self.InventoryListSortOrderTooltip = Tooltip(self.InventoryListSortOrderHeader, GlobalInst.SortTooltipString)

            # Inventory Entries List
            self.InventoryEntriesList = []

            # Inventory Entries Count
            self.InventoryEntriesCount = 100

            # Sort Order Values
            self.SortOrderValuesList = [""]
            for CurrentIndex in range(1, self.InventoryEntriesCount + 1):
                self.SortOrderValuesList.append(str(CurrentIndex))

            # Inventory Entries
            for CurrentIndex in range(1, self.InventoryEntriesCount + 1):
                CurrentEntry = self.InventoryEntry(self.InventoryListScrolledCanvas.WindowFrame, self.InventoryEntriesList, self.ScrollingDisabledVar, self.SortOrderValuesList, CurrentIndex)
                CurrentEntry.Display(CurrentIndex)

        def Calculate(self):
            # Carrying Capacity
            CarryingCapacity = (15 * GlobalInst.GetStringVarAsNumber(
                Inst["AbilitiesAndSavingThrows"].StrengthEntry.AbilityEntryTotalVar)) + self.CarryingCapacityEntryStatModifierInst.GetModifier()
            self.CarryingCapacityVar.set(CarryingCapacity)

            # Coin Counts
            CPCount = GlobalInst.GetStringVarAsNumber(self.CoinsEntryCPVar, Mode="Decimal")
            SPCount = GlobalInst.GetStringVarAsNumber(self.CoinsEntrySPVar, Mode="Decimal")
            EPCount = GlobalInst.GetStringVarAsNumber(self.CoinsEntryEPVar, Mode="Decimal")
            GPCount = GlobalInst.GetStringVarAsNumber(self.CoinsEntryGPVar, Mode="Decimal")
            PPCount = GlobalInst.GetStringVarAsNumber(self.CoinsEntryPPVar, Mode="Decimal")
            TotalCoinCount = CPCount + SPCount + EPCount + GPCount + PPCount

            # Coin Value
            CoinValue = Decimal(0)
            CoinValue += CPCount * self.ValueCP
            CoinValue += SPCount * self.ValueSP
            CoinValue += EPCount * self.ValueEP
            CoinValue += GPCount * self.ValueGP
            CoinValue += PPCount * self.ValuePP
            self.CoinValueEntryVar.set(str(CoinValue.quantize(Decimal("0.01"))))

            # Coin Weight
            CoinWeight = Decimal(TotalCoinCount * self.WeightPerCoin)
            self.CoinWeightEntryVar.set(str(CoinWeight.quantize(Decimal("0.01"))))

            # Loads and Values
            Loads = {}
            Loads["Total"] = Decimal(0)
            Loads["Gear"] = Decimal(0)
            Loads["Food"] = Decimal(0)
            Loads["Water"] = Decimal(0)
            Loads["Treasure"] = Decimal(0)
            Loads["Misc."] = Decimal(0)
            Loads[""] = Decimal(0)

            Values = {}
            Values["Total"] = Decimal(0)
            Values["Gear"] = Decimal(0)
            Values["Food"] = Decimal(0)
            Values["Water"] = Decimal(0)
            Values["Treasure"] = Decimal(0)
            Values["Misc."] = Decimal(0)
            Values[""] = Decimal(0)

            # Add Coins to Loads and Values
            Loads["Total"] += CoinWeight
            Loads["Treasure"] += CoinWeight
            Values["Total"] += CoinValue
            Values["Treasure"] += CoinValue

            # Loop Through Inventory List
            for Entry in self.InventoryEntriesList:
                # Set Up Local Variables
                Tag = Entry.CategoryTagVar.get()
                Count = GlobalInst.GetStringVarAsNumber(Entry.CountEntryVar)
                ValueDenomination = Entry.UnitValueDenominationVar.get()

                # Total Weight and Value
                TotalItemWeight = GlobalInst.GetStringVarAsNumber(Entry.UnitWeightEntryVar, Mode="Decimal") * Decimal(Count)
                TotalItemValue = GlobalInst.GetStringVarAsNumber(Entry.UnitValueEntryVar, Mode="Decimal") * Decimal(Count)

                # Calculate Value in GP
                TotalItemValue *= self.DenominationValues[ValueDenomination]

                Entry.TotalWeightEntryVar.set(str(TotalItemWeight.quantize(Decimal("0.01"))))
                Entry.TotalValueEntryVar.set(str(TotalItemValue.quantize(Decimal("0.01"))))

                # Totals
                Loads["Total"] += TotalItemWeight
                Values["Total"] += TotalItemValue

                # Tags
                Loads[Tag] += TotalItemWeight
                Values[Tag] += TotalItemValue

            # Calculate Supply Days
            FoodConsumptionRate = Decimal(self.FoodDisplay.ConsumptionRateVar.get())
            WaterConsumptionRate = Decimal(self.WaterDisplay.ConsumptionRateVar.get())
            if FoodConsumptionRate > Decimal(0):
                FoodDays = str((Loads["Food"] / FoodConsumptionRate).quantize(Decimal("0.01")))
            else:
                FoodDays = "N/A"
            if WaterConsumptionRate > Decimal(0):
                WaterDays = str((Loads["Water"] / WaterConsumptionRate).quantize(Decimal("0.01")))
            else:
                WaterDays = "N/A"

            # Set Entries
            self.TotalLoadEntryVar.set(str(Loads["Total"].quantize(Decimal("0.01"))))
            self.GearLoadEntryVar.set(str(Loads["Gear"].quantize(Decimal("0.01"))))
            self.TreasureLoadEntryVar.set(str(Loads["Treasure"].quantize(Decimal("0.01"))))
            self.MiscLoadEntryVar.set(str(Loads["Misc."].quantize(Decimal("0.01"))))
            self.TotalValueEntryVar.set(str(Values["Total"].quantize(Decimal("0.01"))))
            self.GearValueEntryVar.set(str(Values["Gear"].quantize(Decimal("0.01"))))
            self.TreasureValueEntryVar.set(str(Values["Treasure"].quantize(Decimal("0.01"))))
            self.MiscValueEntryVar.set(str(Values["Misc."].quantize(Decimal("0.01"))))
            self.FoodDisplay.LoadEntryVar.set(str(Loads["Food"].quantize(Decimal("0.01"))))
            self.WaterDisplay.LoadEntryVar.set(str(Loads["Water"].quantize(Decimal("0.01"))))
            self.FoodDisplay.DaysEntryVar.set(FoodDays)
            self.WaterDisplay.DaysEntryVar.set(WaterDays)

            if Loads["Total"] > CarryingCapacity:
                self.TotalLoadEntry.configure(disabledbackground="red", disabledforeground="white")
            else:
                self.TotalLoadEntry.configure(disabledbackground="light gray", disabledforeground="black")

        def Sort(self, Column, Reverse=False, SearchMode=False):
            # List to Sort
            ListToSort = []

            if SearchMode:
                # Get Search String
                SearchStringPrompt = StringPrompt(WindowInst, "Search", "What do you want to search for?")
                WindowInst.wait_window(SearchStringPrompt.Window)
                if SearchStringPrompt.DataSubmitted.get():
                    SearchString = SearchStringPrompt.StringEntryVar.get()
                else:
                    return

                # Add Fields to List
                for CurrentEntry in self.InventoryEntriesList:
                    ListToSort.append((CurrentEntry, CurrentEntry.SortFields[Column].get().lower()))

                # Sort the List
                SortedList = sorted(ListToSort, key=lambda x: (x[1] == "", SearchString not in x[1]))
            else:
                if Column == "Name":
                    # Add Fields to List
                    for CurrentEntry in self.InventoryEntriesList:
                        ListToSort.append((CurrentEntry, CurrentEntry.SortFields[Column].get()))

                    # Sort the List
                    SortedList = sorted(ListToSort, key=lambda x: ((not Reverse and x[1] == "") or (Reverse and x[1] != ""), x[1].lower()), reverse=Reverse)
                elif Column == "Count" or Column == "Sort Order":
                    # Add Fields to List
                    for CurrentEntry in self.InventoryEntriesList:
                        ListToSort.append((CurrentEntry, GlobalInst.GetStringVarAsNumber(CurrentEntry.SortFields[Column])))

                    # Sort the List
                    SortedList = sorted(ListToSort, key=lambda x: ((not Reverse and x[1] == 0) or (Reverse and x[1] != 0), x[1]), reverse=Reverse)
                elif Column == "Unit Value":
                    # Add Fields to List
                    for CurrentEntry in self.InventoryEntriesList:
                        ListToSort.append((CurrentEntry, CurrentEntry.SortFields["Name"].get(), max(1, GlobalInst.GetStringVarAsNumber(CurrentEntry.SortFields["Count"])),
                                           GlobalInst.GetStringVarAsNumber(CurrentEntry.SortFields["Total Value"], Mode="Float")))

                    # Sort the List
                    SortedList = sorted(ListToSort, key=lambda x: ((not Reverse and x[1] == "") or (Reverse and x[1] != ""), x[3] / x[2]), reverse=Reverse)
                elif Column == "Value Denomination" or Column == "Tag":
                    # Add Fields to List
                    for CurrentEntry in self.InventoryEntriesList:
                        ListToSort.append((CurrentEntry, CurrentEntry.SortFields["Name"].get(), CurrentEntry.SortFields[Column].get()))

                    # Sort the List
                    SortedList = sorted(ListToSort, key=lambda x: ((not Reverse and x[1] == "") or (Reverse and x[1] != ""), x[2].lower()), reverse=Reverse)
                elif Column == "Total Weight" or Column == "Total Value" or Column == "Unit Weight":
                    # Add Fields to List
                    for CurrentEntry in self.InventoryEntriesList:
                        ListToSort.append((CurrentEntry, CurrentEntry.SortFields["Name"].get(), GlobalInst.GetStringVarAsNumber(CurrentEntry.SortFields[Column], Mode="Float")))

                    # Sort the List
                    SortedList = sorted(ListToSort, key=lambda x: ((not Reverse and x[1] == "") or (Reverse and x[1] != ""), x[2]), reverse=Reverse)
                else:
                    return

            # Adjust Entries to New Order
            for CurrentIndex in range(len(SortedList)):
                SortedList[CurrentIndex][0].Display(CurrentIndex + 1)

            # Flag Save Prompt
            SavingAndOpeningInst.SavePrompt = True

            # Update Window Title
            WindowInst.UpdateWindowTitle()

        def Clear(self):
            # Confirm
            ClearConfirm = messagebox.askyesno("Clear Inventory", "Are you sure you want to clear the inventory?  This cannot be undone.")
            if not ClearConfirm:
                return

            # Clear
            self.CoinsEntryCPVar.set("")
            self.CoinsEntrySPVar.set("")
            self.CoinsEntryEPVar.set("")
            self.CoinsEntryGPVar.set("")
            self.CoinsEntryPPVar.set("")
            self.CoinValueEntryVar.set("")
            self.CoinWeightEntryVar.set("")
            self.TotalLoadEntryVar.set("")
            self.GearLoadEntryVar.set("")
            self.TreasureLoadEntryVar.set("")
            self.MiscLoadEntryVar.set("")
            self.TotalValueEntryVar.set("")
            self.GearValueEntryVar.set("")
            self.TreasureValueEntryVar.set("")
            self.MiscValueEntryVar.set("")
            for Entry in self.InventoryEntriesList:
                Entry.NameEntryVar.set("")
                Entry.CountEntryVar.set("")
                Entry.UnitWeightEntryVar.set("")
                Entry.UnitValueEntryVar.set("")
                Entry.UnitValueDenominationVar.set("")
                Entry.TotalWeightEntryVar.set("")
                Entry.TotalValueEntryVar.set("")
                Entry.CategoryTagVar.set("")
                Entry.SortOrderVar.set("")

        def OpenCoinCalculator(self):
            # Create Coin Calculator Window and Wait
            self.CoinCalculatorInst = CoinCalculator(WindowInst, DialogMode=True)
            WindowInst.wait_window(self.CoinCalculatorInst.Window)

        def SpendCoins(self, event):
            # Create Config Window and Wait
            SpendCoinsMenuInst = SpendCoinsMenu(WindowInst, self.SpendingCoins)
            WindowInst.wait_window(SpendCoinsMenuInst.Window)

            # Handle Variables
            if SpendCoinsMenuInst.DataSubmitted.get():
                for Denomination in SpendCoinsMenuInst.Remaining.keys():
                    self.SpendingCoins[Denomination].set(SpendCoinsMenuInst.Remaining[Denomination].get())

        def GainCoins(self, event):
            # Create Config Window and Wait
            GainCoinsMenuInst = GainCoinsMenu(WindowInst)
            WindowInst.wait_window(GainCoinsMenuInst.Window)

            # Handle Variables
            if GainCoinsMenuInst.DataSubmitted.get():
                for Denomination, Gain in GainCoinsMenuInst.Gained.items():
                    self.SpendingCoins[Denomination].set(str(GlobalInst.GetStringVarAsNumber(self.SpendingCoins[Denomination]) + GlobalInst.GetStringVarAsNumber(Gain)))

        class InventoryEntry:
            def __init__(self, master, List, ScrollingDisabledVar, SortOrderValuesList, Row):
                # Store Parameters
                self.master = master
                self.ScrollingDisabledVar = ScrollingDisabledVar
                self.SortOrderValuesList = SortOrderValuesList
                self.Row = Row

                # Variables
                self.NameEntryVar = SavedStringVar()
                self.CountEntryVar = SavedStringVar()
                self.CountEntryVar.trace_add("write", lambda a, b, c: CharacterSheetInst.UpdateStatsAndInventory())
                self.UnitWeightEntryVar = SavedStringVar()
                self.UnitWeightEntryVar.trace_add("write", lambda a, b, c: CharacterSheetInst.UpdateStatsAndInventory())
                self.UnitValueEntryVar = SavedStringVar()
                self.UnitValueEntryVar.trace_add("write", lambda a, b, c: CharacterSheetInst.UpdateStatsAndInventory())
                self.UnitValueDenominationVar = SavedStringVar()
                self.UnitValueDenominationVar.trace_add("write", lambda a, b, c: CharacterSheetInst.UpdateStatsAndInventory())
                self.TotalWeightEntryVar = StringVar()
                self.TotalValueEntryVar = StringVar()
                self.CategoryTagVar = SavedStringVar()
                self.CategoryTagVar.trace_add("write", lambda a, b, c: CharacterSheetInst.UpdateStatsAndInventory())
                self.CategoryEntryVar = SavedStringVar()
                self.RarityEntryVar = SavedStringVar()
                self.DescriptionVar = SavedStringVar()
                self.SortOrderVar = SavedStringVar()

                # Item Description Vars
                self.ItemDescriptionVars = {}
                self.ItemDescriptionVars["NameEntryVar"] = self.NameEntryVar
                self.ItemDescriptionVars["CategoryEntryVar"] = self.CategoryEntryVar
                self.ItemDescriptionVars["RarityEntryVar"] = self.RarityEntryVar
                self.ItemDescriptionVars["DescriptionVar"] = self.DescriptionVar

                # Sort Fields
                self.SortFields = {}
                self.SortFields["Name"] = self.NameEntryVar
                self.SortFields["Count"] = self.CountEntryVar
                self.SortFields["Unit Weight"] = self.UnitWeightEntryVar
                self.SortFields["Unit Value"] = self.UnitValueEntryVar
                self.SortFields["Value Denomination"] = self.UnitValueDenominationVar
                self.SortFields["Total Weight"] = self.TotalWeightEntryVar
                self.SortFields["Total Value"] = self.TotalValueEntryVar
                self.SortFields["Tag"] = self.CategoryTagVar
                self.SortFields["Sort Order"] = self.SortOrderVar

                # Add to List
                List.append(self)

                # Name Entry
                self.NameEntry = EntryExtended(master, width=35, textvariable=self.NameEntryVar, justify=CENTER, bg=GlobalInst.ButtonColor)
                self.NameEntry.bind("<Button-3>", self.ConfigureItemDescription)
                self.NameTooltip = Tooltip(self.NameEntry, "Right-click on the name field to set an item description.")

                # Count Entry
                self.CountEntry = InventoryCountEntry(master, width=4, textvariable=self.CountEntryVar, justify=CENTER)

                # Unit Weight Entry
                self.UnitWeightEntry = InventoryWeightEntry(master, width=4, textvariable=self.UnitWeightEntryVar, justify=CENTER)

                # Unit Value Entry
                self.UnitValueEntry = InventoryValueEntry(master, width=4, textvariable=self.UnitValueEntryVar, justify=CENTER)

                # Unit Value Denomination
                self.UnitValueDenomination = DropdownExtended(master, textvariable=self.UnitValueDenominationVar, values=["", "cp", "sp", "ep", "gp", "pp"], width=2, state="readonly", justify=CENTER)
                self.UnitValueDenomination.bind("<Enter>", self.DisableScrolling)
                self.UnitValueDenomination.bind("<Leave>", self.EnableScrolling)

                # Total Weight Entry
                self.TotalWeightEntry = EntryExtended(master, width=4, textvariable=self.TotalWeightEntryVar, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow")

                # Total Value Entry
                self.TotalValueEntry = EntryExtended(master, width=4, textvariable=self.TotalValueEntryVar, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow")

                # Category Tag
                self.CategoryTag = DropdownExtended(master, textvariable=self.CategoryTagVar, values=["", "Gear", "Food", "Water", "Treasure", "Misc."], width=8, state="readonly", justify=CENTER)
                self.CategoryTag.bind("<Enter>", self.DisableScrolling)
                self.CategoryTag.bind("<Leave>", self.EnableScrolling)

                # Sort Order
                self.SortOrder = DropdownExtended(master, textvariable=self.SortOrderVar, values=self.SortOrderValuesList, width=5, state="readonly", justify=CENTER)
                self.SortOrder.bind("<Enter>", self.DisableScrolling)
                self.SortOrder.bind("<Leave>", self.EnableScrolling)

            def DisableScrolling(self, event):
                self.ScrollingDisabledVar.set(True)

            def EnableScrolling(self, event):
                self.ScrollingDisabledVar.set(False)

            def ConfigureItemDescription(self, event):
                # Create Window and Wait
                ItemDescriptionMenuInst = self.ItemDescriptionMenu(WindowInst, self.ItemDescriptionVars)
                WindowInst.wait_window(ItemDescriptionMenuInst.Window)

                # Handle Variables
                if ItemDescriptionMenuInst.DataSubmitted.get():
                    for Tag, Var in ItemDescriptionMenuInst.Vars.items():
                        self.ItemDescriptionVars[Tag].set(Var.get())

            def Display(self, Row):
                self.Row = Row

                # Set Row Size
                self.master.grid_rowconfigure(self.Row, minsize=26)

                # Place in Grid
                self.NameEntry.grid(row=self.Row, column=0, sticky=NSEW)
                self.CountEntry.grid(row=self.Row, column=1, sticky=NSEW)
                self.UnitWeightEntry.grid(row=self.Row, column=2, sticky=NSEW)
                self.UnitValueEntry.grid(row=self.Row, column=3, sticky=NSEW)
                self.UnitValueDenomination.grid(row=self.Row, column=4, sticky=NSEW)
                self.TotalWeightEntry.grid(row=self.Row, column=5, sticky=NSEW)
                self.TotalValueEntry.grid(row=self.Row, column=6, sticky=NSEW)
                self.CategoryTag.grid(row=self.Row, column=7, sticky=NSEW)
                self.SortOrder.grid(row=self.Row, column=8, sticky=NSEW)

                # Update Tab Order
                self.NameEntry.lift()
                self.CountEntry.lift()
                self.UnitWeightEntry.lift()
                self.UnitValueEntry.lift()
                self.UnitValueDenomination.lift()
                self.TotalWeightEntry.lift()
                self.TotalValueEntry.lift()
                self.CategoryTag.lift()
                self.SortOrder.lift()

                # Update Tags
                self.NameEntryVar.UpdateTag("InventoryListNameEntryVar" + str(self.Row))
                self.CountEntryVar.UpdateTag("InventoryListCountEntryVar" + str(self.Row))
                self.UnitWeightEntryVar.UpdateTag("InventoryListUnitWeightEntryVar" + str(self.Row))
                self.UnitValueEntryVar.UpdateTag("InventoryListUnitValueEntryVar" + str(self.Row))
                self.UnitValueDenominationVar.UpdateTag("InventoryListUnitValueDenominationVar" + str(self.Row))
                self.CategoryTagVar.UpdateTag("InventoryListCategoryTagVar" + str(self.Row))
                self.CategoryEntryVar.UpdateTag("InventoryListMagicItemCategoryEntryVar" + str(self.Row))
                self.RarityEntryVar.UpdateTag("InventoryListMagicItemRarityEntryVar" + str(self.Row))
                self.DescriptionVar.UpdateTag("InventoryListMagicItemDescriptionVar" + str(self.Row))
                self.SortOrderVar.UpdateTag("InventoryListSortOrderVar" + str(self.Row))

            class ItemDescriptionMenu:
                def __init__(self, master, ItemDescriptionVars):
                    self.DataSubmitted = BooleanVar()
                    self.Vars = {}
                    self.Vars["NameEntryVar"] = StringVar(value=ItemDescriptionVars["NameEntryVar"].get())
                    self.Vars["CategoryEntryVar"] = StringVar(value=ItemDescriptionVars["CategoryEntryVar"].get())
                    self.Vars["RarityEntryVar"] = StringVar(value=ItemDescriptionVars["RarityEntryVar"].get())
                    self.Vars["DescriptionVar"] = StringVar(value=ItemDescriptionVars["DescriptionVar"].get())

                    # Create Window
                    self.Window = Toplevel(master)
                    self.Window.wm_attributes("-toolwindow", 1)
                    self.Window.wm_title("Item Description")

                    # Name Entry
                    self.NameFrame = LabelFrame(self.Window, text="Name:")
                    self.NameFrame.grid_columnconfigure(0, weight=1)
                    self.NameFrame.grid(row=0, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                    self.NameEntry = EntryExtended(self.NameFrame, justify=CENTER, width=35, textvariable=self.Vars["NameEntryVar"])
                    self.NameEntry.grid(row=0, column=0, sticky=NSEW)

                    # Category Entry
                    self.CategoryFrame = LabelFrame(self.Window, text="Category:")
                    self.CategoryFrame.grid_columnconfigure(0, weight=1)
                    self.CategoryFrame.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)
                    self.CategoryEntry = EntryExtended(self.CategoryFrame, justify=CENTER, textvariable=self.Vars["CategoryEntryVar"], width=15)
                    self.CategoryEntry.grid(row=0, column=0, sticky=NSEW)

                    # Rarity Entry
                    self.RarityFrame = LabelFrame(self.Window, text="Rarity:")
                    self.RarityFrame.grid_columnconfigure(0, weight=1)
                    self.RarityFrame.grid(row=1, column=1, padx=2, pady=2, sticky=NSEW)
                    self.RarityEntry = EntryExtended(self.RarityFrame, justify=CENTER, textvariable=self.Vars["RarityEntryVar"], width=15)
                    self.RarityEntry.grid(row=0, column=0, sticky=NSEW)

                    # Description Field
                    self.DescriptionFrame = LabelFrame(self.Window, text="Description:")
                    self.DescriptionFrame.grid(row=2, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                    self.DescriptionField = ScrolledText(self.DescriptionFrame, Width=250, Height=300)
                    self.DescriptionField.grid(row=0, column=0)
                    self.DescriptionField.Text.insert(1.0, self.Vars["DescriptionVar"].get())

                    # Buttons
                    self.ButtonFrame = Frame(self.Window)
                    self.ButtonFrame.grid_columnconfigure(0, weight=1)
                    self.ButtonFrame.grid_columnconfigure(1, weight=1)
                    self.ButtonFrame.grid(row=3, column=0, columnspan=2, sticky=NSEW)
                    self.SubmitButton = Button(self.ButtonFrame, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
                    self.SubmitButton.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)
                    self.CancelButton = Button(self.ButtonFrame, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
                    self.CancelButton.grid(row=0, column=1, padx=2, pady=2, sticky=NSEW)

                    # Prevent Main Window Input
                    self.Window.grab_set()

                    # Handle Config Window Geometry and Focus
                    GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst)
                    self.Window.focus_force()

                    # Focus on Name Entry
                    self.NameEntry.focus_set()

                def Submit(self):
                    self.DataSubmitted.set(True)
                    self.Vars["DescriptionVar"].set(self.DescriptionField.get())
                    self.Window.destroy()

                def Cancel(self):
                    self.DataSubmitted.set(False)
                    self.Window.destroy()

        class SupplyDisplay:
            def __init__(self, master, ConsumptionRateDefault, Tag):
                # Store Parameters
                self.ConsumptionRateDefault = ConsumptionRateDefault
                self.Tag = Tag

                # Variables
                self.LoadEntryVar = StringVar()
                self.DaysEntryVar = StringVar()
                self.ConsumptionRateVar = SavedStringVar(self.Tag + "ConsumptionRateVar", DefaultValue=self.ConsumptionRateDefault)

                # Supply Display Frame
                self.SupplyDisplayFrame = LabelFrame(master, text=self.Tag + ":")
                self.SupplyDisplayFrame.grid_rowconfigure(0, weight=1)
                self.SupplyDisplayFrame.grid_rowconfigure(1, weight=1)

                # Labels
                self.LoadLabel = Label(self.SupplyDisplayFrame, text="Load (lbs.)", bd=2, relief=GROOVE)
                self.LoadLabel.grid(row=0, column=0, sticky=NSEW)
                self.DaysLabel = Label(self.SupplyDisplayFrame, text="Days", bd=2, relief=GROOVE)
                self.DaysLabel.grid(row=1, column=0, sticky=NSEW)

                # Entries
                self.LoadEntry = EntryExtended(self.SupplyDisplayFrame, textvariable=self.LoadEntryVar, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray",
                                               cursor="arrow")
                self.LoadEntry.grid(row=0, column=1, sticky=NSEW)
                self.DaysEntry = EntryExtended(self.SupplyDisplayFrame, textvariable=self.DaysEntryVar, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground=GlobalInst.ButtonColor,
                                               cursor="arrow")
                self.DaysEntry.grid(row=1, column=1, sticky=NSEW)
                self.DaysEntry.bind("<Button-1>", self.SetConsumptionRate)
                self.DaysTooltip = Tooltip(self.DaysEntry, "Left-click to set the consumption rate per day for supplies.")

            def grid(self, *args, **kwargs):
                self.SupplyDisplayFrame.grid(*args, **kwargs)

            def pack(self, *args, **kwargs):
                self.SupplyDisplayFrame.pack(*args, **kwargs)

            def SetConsumptionRate(self, event):
                ConsumptionRatePromptInst = self.ConsumptionRatePrompt(WindowInst, self.ConsumptionRateVar, self.Tag)
                WindowInst.wait_window(ConsumptionRatePromptInst.Window)
                if ConsumptionRatePromptInst.DataSubmitted.get():
                    self.ConsumptionRateVar.set(str(ConsumptionRatePromptInst.GetData()))

                CharacterSheetInst.UpdateStatsAndInventory()

            class ConsumptionRatePrompt:
                def __init__(self, master, ConsumptionRateVar, Tag):
                    # Store Parameters
                    self.ConsumptionRateVar = ConsumptionRateVar
                    self.Tag = Tag

                    # Variables
                    self.DataSubmitted = BooleanVar()
                    self.ConsumptionRateEntryVar = StringVar(value=self.ConsumptionRateVar.get())

                    # Create Window
                    self.Window = Toplevel(master)
                    self.Window.wm_attributes("-toolwindow", 1)
                    self.Window.wm_title(self.Tag + " Consumption Rate")

                    # Table Frame
                    self.TableFrame = Frame(self.Window)
                    self.TableFrame.grid(row=0, column=0, sticky=NSEW, columnspan=2)

                    # Integer Entry
                    self.ConsumptionRateHeader = Label(self.TableFrame, text="How many pounds of supplies tagged\n\"" + self.Tag + "\" do you consume daily?", bd=2, relief=GROOVE, justify=LEFT)
                    self.ConsumptionRateHeader.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
                    self.ConsumptionRateEntry = EntryExtended(self.TableFrame, width=20, textvariable=self.ConsumptionRateEntryVar, justify=CENTER)
                    self.ConsumptionRateEntry.ConfigureValidation(
                        lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Consumption rate must be a number.", Mode="Float", MinValue=0, LessThanMinString="Consumption rate cannot be less than 0."), "key")
                    self.ConsumptionRateEntry.grid(row=1, column=2, sticky=NSEW, padx=2, pady=2)
                    self.ConsumptionRateEntry.bind("<Return>", lambda event: self.Submit())

                    # Submit Button
                    self.SubmitButton = Button(self.Window, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
                    self.SubmitButton.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)

                    # Cancel Button
                    self.CancelButton = Button(self.Window, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
                    self.CancelButton.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)

                    # Prevent Main Window Input
                    self.Window.grab_set()

                    # Handle Config Window Geometry and Focus
                    GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst)
                    self.Window.focus_force()

                    # Focus On Entry
                    self.ConsumptionRateEntry.focus_set()

                def Submit(self):
                    self.DataSubmitted.set(True)
                    self.Window.destroy()

                def Cancel(self):
                    self.DataSubmitted.set(False)
                    self.Window.destroy()

                    return None

                def GetData(self):
                    return GlobalInst.GetStringVarAsNumber(self.ConsumptionRateEntryVar, Mode="Decimal")

    # Notes
    class Notes:
        def __init__(self, master):
            # Variables
            self.ScrollingDisabledVar = BooleanVar(value=False)

            # Center Widgets
            master.grid_columnconfigure(0, weight=1)
            master.grid_columnconfigure(2, weight=1)
            master.grid_columnconfigure(4, weight=1)
            master.grid_columnconfigure(6, weight=1)

            # Notes Text Boxes
            self.NotesField1 = ScrolledText(master, Width=230, Height=490, SavedDataTag="NotesField1")
            self.NotesField1.grid(row=0, column=1, padx=2, pady=2, sticky=NSEW)
            self.NotesField2 = ScrolledText(master, Width=230, Height=490, SavedDataTag="NotesField2")
            self.NotesField2.grid(row=0, column=3, padx=2, pady=2, sticky=NSEW)

            # Additional Notes Frame
            self.AdditionalNotesFrame = LabelFrame(master, text="Additional Notes:")
            self.AdditionalNotesFrame.grid(row=0, column=5, padx=2, pady=2)

            # Additional Notes Scrolled Canvas
            self.AdditionalNotesScrolledCanvas = ScrolledCanvas(self.AdditionalNotesFrame, ScrollingDisabledVar=self.ScrollingDisabledVar, Height=475, Width=225)
            self.AdditionalNotesScrolledCanvas.BindEnterAndLeaveToBindMouseWheel()

            # Additional Notes Headers
            self.NameHeader = Label(self.AdditionalNotesScrolledCanvas.WindowFrame, text="Name", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.NameHeader.grid(row=0, column=0, sticky=NSEW)
            self.NameHeader.bind("<Button-1>", lambda event: self.Sort("Name"))
            self.NameHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Name", SearchMode=True))
            self.NameHeader.bind("<Button-3>", lambda event: self.Sort("Name", Reverse=True))
            self.NameTooltip = Tooltip(self.NameHeader, GlobalInst.SortTooltipString)
            self.SortOrderHeader = Label(self.AdditionalNotesScrolledCanvas.WindowFrame, text="Sort\nOrder", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.SortOrderHeader.grid(row=0, column=1, sticky=NSEW)
            self.SortOrderHeader.bind("<Button-1>", lambda event: self.Sort("Sort Order"))
            self.SortOrderHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Sort Order", SearchMode=True))
            self.SortOrderHeader.bind("<Button-3>", lambda event: self.Sort("Sort Order", Reverse=True))
            self.SortOrderTooltip = Tooltip(self.SortOrderHeader, GlobalInst.SortTooltipString)

            # Additional Notes Entries List
            self.AdditionalNotesEntriesList = []

            # Additional Notes Entries Count
            self.AdditionalNotesEntriesCount = 100

            # Sort Order Values
            self.SortOrderValuesList = [""]
            for CurrentIndex in range(1, self.AdditionalNotesEntriesCount + 1):
                self.SortOrderValuesList.append(str(CurrentIndex))

            # Additional Notes Entries
            for CurrentIndex in range(1, self.AdditionalNotesEntriesCount + 1):
                CurrentEntry = self.AdditionalNotesEntry(self.AdditionalNotesScrolledCanvas.WindowFrame, self.AdditionalNotesEntriesList, self.ScrollingDisabledVar, self.SortOrderValuesList, CurrentIndex)
                CurrentEntry.Display(CurrentIndex)

        def Sort(self, Column, Reverse=False, SearchMode=False):
            # List to Sort
            ListToSort = []

            if SearchMode:
                # Get Search String
                SearchStringPrompt = StringPrompt(WindowInst, "Search", "What do you want to search for?")
                WindowInst.wait_window(SearchStringPrompt.Window)
                if SearchStringPrompt.DataSubmitted.get():
                    SearchString = SearchStringPrompt.StringEntryVar.get()
                else:
                    return

                # Add Fields to List
                for CurrentEntry in self.AdditionalNotesEntriesList:
                    ListToSort.append((CurrentEntry, CurrentEntry.SortFields[Column].get().lower()))

                # Sort the List
                SortedList = sorted(ListToSort, key=lambda x: (x[1] == "", SearchString not in x[1]))
            else:
                if Column == "Name":
                    # Add Fields to List
                    for CurrentEntry in self.AdditionalNotesEntriesList:
                        ListToSort.append((CurrentEntry, CurrentEntry.SortFields[Column].get()))

                    # Sort the List
                    SortedList = sorted(ListToSort, key=lambda x: ((not Reverse and x[1] == "") or (Reverse and x[1] != ""), x[1].lower()), reverse=Reverse)
                elif Column == "Sort Order":
                    # Add Fields to List
                    for CurrentEntry in self.AdditionalNotesEntriesList:
                        ListToSort.append((CurrentEntry, GlobalInst.GetStringVarAsNumber(CurrentEntry.SortFields[Column])))

                    # Sort the List
                    SortedList = sorted(ListToSort, key=lambda x: ((not Reverse and x[1] == 0) or (Reverse and x[1] != 0), x[1]), reverse=Reverse)
                else:
                    return

            # Adjust Entries to New Order
            for CurrentIndex in range(len(SortedList)):
                SortedList[CurrentIndex][0].Display(CurrentIndex + 1)

            # Flag Save Prompt
            SavingAndOpeningInst.SavePrompt = True

            # Update Window Title
            WindowInst.UpdateWindowTitle()

        class AdditionalNotesEntry:
            def __init__(self, master, List, ScrollingDisabledVar, SortOrderValuesList, Row):
                # Store Parameters
                self.master = master
                self.ScrollingDisabledVar = ScrollingDisabledVar
                self.SortOrderValuesList = SortOrderValuesList
                self.Row = Row

                # Variables
                self.NameEntryVar = SavedStringVar()
                self.SortOrderVar = SavedStringVar()
                self.NoteVar = SavedStringVar()

                # Note Config Vars
                self.NoteConfigVars = {}
                self.NoteConfigVars["NameEntryVar"] = self.NameEntryVar
                self.NoteConfigVars["NoteVar"] = self.NoteVar

                # Sort Fields
                self.SortFields = {}
                self.SortFields["Name"] = self.NameEntryVar
                self.SortFields["Sort Order"] = self.SortOrderVar

                # Add to List
                List.append(self)

                # Name Entry
                self.NameEntry = EntryExtended(master, width=28, justify=CENTER, state=DISABLED, disabledbackground=GlobalInst.ButtonColor, disabledforeground="black", textvariable=self.NameEntryVar, cursor="arrow")
                self.NameEntry.bind("<Button-1>", self.SetNote)
                self.NameTooltip = Tooltip(self.NameEntry, "Left-click on a note entry to set a note.")

                # Sort Order
                self.SortOrder = DropdownExtended(master, textvariable=self.SortOrderVar, values=self.SortOrderValuesList, width=5, state="readonly", justify=CENTER)
                self.SortOrder.bind("<Enter>", self.DisableScrolling)
                self.SortOrder.bind("<Leave>", self.EnableScrolling)

            def SetNote(self, event):
                # Create Config Window and Wait
                NoteConfigInst = self.NoteConfig(WindowInst, self.NoteConfigVars)
                WindowInst.wait_window(NoteConfigInst.Window)

                # Handle Variables
                if NoteConfigInst.DataSubmitted.get():
                    for Tag, Var in NoteConfigInst.Vars.items():
                        self.NoteConfigVars[Tag].set(Var.get())

            def DisableScrolling(self, event):
                self.ScrollingDisabledVar.set(True)

            def EnableScrolling(self, event):
                self.ScrollingDisabledVar.set(False)

            def Display(self, Row):
                self.Row = Row

                # Set Row Size
                self.master.grid_rowconfigure(self.Row, minsize=26)

                # Place in Grid
                self.NameEntry.grid(row=self.Row, column=0, sticky=NSEW)
                self.SortOrder.grid(row=self.Row, column=1, sticky=NSEW)

                # Update Tab Order
                self.NameEntry.lift()
                self.SortOrder.lift()

                # Update Tags
                self.NameEntryVar.UpdateTag("AdditionalNotesNameEntryVar" + str(self.Row))
                self.SortOrderVar.UpdateTag("AdditionalNotesSortOrderVar" + str(self.Row))
                self.NoteVar.UpdateTag("AdditionalNotesNoteVar" + str(self.Row))

            class NoteConfig:
                def __init__(self, master, NoteConfigVars):
                    self.DataSubmitted = BooleanVar()
                    self.Vars = {}
                    self.Vars["NameEntryVar"] = StringVar(value=NoteConfigVars["NameEntryVar"].get())
                    self.Vars["NoteVar"] = StringVar(value=NoteConfigVars["NoteVar"].get())

                    # Create Window
                    self.Window = Toplevel(master)
                    self.Window.wm_attributes("-toolwindow", 1)
                    self.Window.wm_title("Note Entry")

                    # Name Entry
                    self.NameFrame = LabelFrame(self.Window, text="Name:")
                    self.NameFrame.grid_columnconfigure(0, weight=1)
                    self.NameFrame.grid(row=0, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                    self.NameEntry = EntryExtended(self.NameFrame, justify=CENTER, width=20, textvariable=self.Vars["NameEntryVar"])
                    self.NameEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                    # Description Field
                    self.DescriptionFrame = LabelFrame(self.Window, text="Note:")
                    self.DescriptionFrame.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                    self.NoteField = ScrolledText(self.DescriptionFrame, Width=250, Height=300)
                    self.NoteField.grid(row=0, column=0)
                    self.NoteField.Text.insert(1.0, self.Vars["NoteVar"].get())

                    # Submit Button
                    self.SubmitButton = Button(self.Window, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
                    self.SubmitButton.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)

                    # Cancel Button
                    self.CancelButton = Button(self.Window, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
                    self.CancelButton.grid(row=2, column=1, sticky=NSEW, padx=2, pady=2)

                    # Prevent Main Window Input
                    self.Window.grab_set()

                    # Handle Config Window Geometry and Focus
                    GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst)
                    self.Window.focus_force()

                    # Focus on Name Entry
                    self.NameEntry.focus_set()

                def Submit(self):
                    self.DataSubmitted.set(True)
                    self.Vars["NoteVar"].set(self.NoteField.get())
                    self.Window.destroy()

                def Cancel(self):
                    self.DataSubmitted.set(False)
                    self.Window.destroy()

    # Personality and Backstory
    class PersonalityAndBackstory:
        def __init__(self, master):
            # Variables
            self.RaceEntryVar = SavedStringVar("RaceEntryVar")
            self.BackgroundEntryVar = SavedStringVar("BackgroundEntryVar")
            self.AlignmentEntryVar = SavedStringVar("AlignmentEntryVar")
            self.AgeEntryVar = SavedStringVar("AgeEntryVar")

            # Center Widgets
            master.grid_rowconfigure(0, weight=1)
            master.grid_rowconfigure(2, weight=1)
            master.grid_columnconfigure(0, weight=1)
            master.grid_columnconfigure(2, weight=1)
            master.grid_columnconfigure(4, weight=1)
            master.grid_columnconfigure(6, weight=1)
            master.grid_columnconfigure(8, weight=1)

            # First Column
            self.FirstColumnFrame = Frame(master)
            self.FirstColumnFrame.grid(row=1, column=1)

            # Race
            self.RaceFrame = LabelFrame(self.FirstColumnFrame, text="Race:")
            self.RaceFrame.grid_columnconfigure(0, weight=1)
            self.RaceFrame.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)
            self.RaceEntry = EntryExtended(self.RaceFrame, justify=CENTER, textvariable=self.RaceEntryVar, width=22)
            self.RaceEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

            # Background
            self.BackgroundFrame = LabelFrame(self.FirstColumnFrame, text="Background:")
            self.BackgroundFrame.grid_columnconfigure(0, weight=1)
            self.BackgroundFrame.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)
            self.BackgroundEntry = EntryExtended(self.BackgroundFrame, justify=CENTER, textvariable=self.BackgroundEntryVar, width=22)
            self.BackgroundEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

            # Alignment
            self.AlignmentFrame = LabelFrame(self.FirstColumnFrame, text="Alignment:")
            self.AlignmentFrame.grid_columnconfigure(0, weight=1)
            self.AlignmentFrame.grid(row=2, column=0, padx=2, pady=2, sticky=NSEW)
            self.AlignmentEntry = EntryExtended(self.AlignmentFrame, justify=CENTER, textvariable=self.AlignmentEntryVar, width=22)
            self.AlignmentEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

            # Age
            self.AgeFrame = LabelFrame(self.FirstColumnFrame, text="Age:")
            self.AgeFrame.grid_columnconfigure(0, weight=1)
            self.AgeFrame.grid(row=3, column=0, padx=2, pady=2, sticky=NSEW)
            self.AgeEntry = EntryExtended(self.AgeFrame, justify=CENTER, textvariable=self.AgeEntryVar, width=22)
            self.AgeEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

            # Physical Appearance
            self.PhysicalAppearanceFrame = LabelFrame(self.FirstColumnFrame, text="Physical Appearance:")
            self.PhysicalAppearanceFrame.grid(row=4, column=0, padx=2, pady=2)
            self.PhysicalAppearanceField = ScrolledText(self.PhysicalAppearanceFrame, Width=170, Height=289, SavedDataTag="PhysicalAppearanceField")
            self.PhysicalAppearanceField.grid(row=0, column=0)

            # Second Column
            self.SecondColumnFrame = Frame(master)
            self.SecondColumnFrame.grid(row=1, column=3)

            # Personality Traits
            self.PersonalityTraitsFrame = LabelFrame(self.SecondColumnFrame, text="Personality Traits:")
            self.PersonalityTraitsFrame.grid(row=0, column=0, padx=2, pady=2)
            self.PersonalityTraitsField = ScrolledText(self.PersonalityTraitsFrame, Width=170, Height=225, SavedDataTag="PersonalityTraitsField")
            self.PersonalityTraitsField.grid(row=0, column=0)

            # Bonds
            self.BondsFrame = LabelFrame(self.SecondColumnFrame, text="Bonds:")
            self.BondsFrame.grid(row=1, column=0, padx=2, pady=2)
            self.BondsField = ScrolledText(self.BondsFrame, Width=170, Height=225, SavedDataTag="BondsField")
            self.BondsField.grid(row=0, column=0)

            # Third Column
            self.ThirdColumnFrame = Frame(master)
            self.ThirdColumnFrame.grid(row=1, column=5)

            # Ideals
            self.IdealsFrame = LabelFrame(self.ThirdColumnFrame, text="Ideals:")
            self.IdealsFrame.grid(row=0, column=0, padx=2, pady=2)
            self.IdealsField = ScrolledText(self.IdealsFrame, Width=170, Height=225, SavedDataTag="IdealsField")
            self.IdealsField.grid(row=0, column=0)

            # Flaws
            self.FlawsFrame = LabelFrame(self.ThirdColumnFrame, text="Flaws:")
            self.FlawsFrame.grid(row=1, column=0, padx=2, pady=2)
            self.FlawsField = ScrolledText(self.FlawsFrame, Width=170, Height=225, SavedDataTag="FlawsField")
            self.FlawsField.grid(row=0, column=0)

            # Fourth Column
            self.FourthColumnFrame = Frame(master)
            self.FourthColumnFrame.grid(row=1, column=7)

            # Backstory
            self.BackstoryFrame = LabelFrame(self.FourthColumnFrame, text="Backstory:")
            self.BackstoryFrame.grid(row=0, column=0, padx=2, pady=2)
            self.BackstoryField = ScrolledText(self.BackstoryFrame, Width=170, Height=473, SavedDataTag="BackstoryField")
            self.BackstoryField.grid(row=0, column=0)

    # Portrait
    class Portrait():
        def __init__(self, master):
            self.PortraitSelectedVar = SavedBooleanVar("PortraitSelectedVar")
            self.PortraitImage = PhotoImage()

            # Portrait Holder Frame (Center In Page)
            self.PortraitHolderFrame = Frame(master)
            self.PortraitHolderFrame.grid(row=1, column=1)
            master.grid_rowconfigure(0, weight=1)
            master.grid_rowconfigure(2, weight=1)
            master.grid_columnconfigure(0, weight=1)
            master.grid_columnconfigure(3, weight=1)

            # Portrait Canvas
            self.PortraitCanvas = Canvas(self.PortraitHolderFrame, bd=2, relief=GROOVE, width=400, height=400, bg="white")
            self.PortraitCanvas.grid(row=0, column=0, columnspan=3, sticky=NSEW)

            # Portrait Buttons
            self.ImportButton = Button(self.PortraitHolderFrame, text="Import", command=self.Import, bg=GlobalInst.ButtonColor)
            self.ImportButton.grid(row=1, column=0, sticky=NSEW)
            self.ExportButton = Button(self.PortraitHolderFrame, text="Export", command=self.Export, bg=GlobalInst.ButtonColor)
            self.ExportButton.grid(row=1, column=1, sticky=NSEW)
            self.ClearButton = Button(self.PortraitHolderFrame, text="Clear", command=self.Clear, bg=GlobalInst.ButtonColor)
            self.ClearButton.grid(row=1, column=2, sticky=NSEW)

            # Portrait Instructions
            self.PortraitInstructions = Label(self.PortraitHolderFrame, text="Portrait must be a .gif file no larger than 400 x 400.")
            self.PortraitInstructions.grid(row=2, column=0, columnspan=3, sticky=NSEW)

        def Import(self):
            if self.PortraitSelectedVar.get():
                SelectConfirm = messagebox.askyesno("Import Portrait", "Are you sure you want to import a new portrait?  This cannot be undone.")
                if not SelectConfirm:
                    return
            PortraitFileName = filedialog.askopenfilename(filetypes=(("GIF file", "*.gif"), ("All files", "*.*")), defaultextension=".gif", title="Import Portrait File")
            if PortraitFileName != "":
                if PortraitFileName.endswith(".gif"):
                    self.SetPortrait(PortraitFileName)
                else:
                    messagebox.showerror("Invalid File", "Portraits must be .gif files.")
            else:
                StatusBarInst.FlashStatus("No portrait imported!")

        def SetPortrait(self, ImageFileName):
            self.PortraitCanvas.delete("all")
            self.PortraitSelectedVar.set(True)
            self.PortraitImage.configure(file=ImageFileName)
            self.PortraitCanvas.create_image((self.PortraitCanvas.winfo_width() / 2), (self.PortraitCanvas.winfo_height() / 2), image=self.PortraitImage)

        def Export(self):
            ExportFileName = filedialog.asksaveasfilename(filetypes=(("GIF file", "*.gif"), ("All files", "*.*")), defaultextension=".gif", title="Export Portrait File")
            if ExportFileName != "":
                self.PortraitImage.write(ExportFileName)

        def Clear(self):
            if self.PortraitSelectedVar.get():
                ClearConfirm = messagebox.askyesno("Clear Portrait", "Are you sure you want to clear the portrait?  This cannot be undone.")
                if not ClearConfirm:
                    return
            self.PortraitSelectedVar.set(False)
            self.PortraitCanvas.delete("all")

    # Settings Menu
    class SettingsMenu:
        def __init__(self, master, SettingsMenuVars):
            # Variables
            self.DataSubmitted = BooleanVar()
            self.Vars = {}
            self.Vars["SpellcasterBoxVar"] = BooleanVar(value=SettingsMenuVars["SpellcasterBoxVar"].get())
            self.Vars["ConcentrationCheckPromptBoxVar"] = BooleanVar(value=SettingsMenuVars["ConcentrationCheckPromptBoxVar"].get())
            self.Vars["PortraitBoxVar"] = BooleanVar(value=SettingsMenuVars["PortraitBoxVar"].get())
            self.Vars["JackOfAllTradesBoxVar"] = BooleanVar(value=SettingsMenuVars["JackOfAllTradesBoxVar"].get())
            self.Vars["RemarkableAthleteBoxVar"] = BooleanVar(value=SettingsMenuVars["RemarkableAthleteBoxVar"].get())
            self.Vars["ObservantBoxVar"] = BooleanVar(value=SettingsMenuVars["ObservantBoxVar"].get())
            self.Vars["LuckyHalflingBoxVar"] = BooleanVar(value=SettingsMenuVars["LuckyHalflingBoxVar"].get())

            # Create Window
            self.Window = Toplevel(master)
            self.Window.wm_attributes("-toolwindow", 1)
            self.Window.wm_title("Settings")

            # Spellcaster Checkbox
            self.SpellcasterBox = Checkbutton(self.Window, text="Spellcaster", variable=self.Vars["SpellcasterBoxVar"])
            self.SpellcasterBox.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)

            # Concentration Check Prompt Checkbox
            self.ConcentrationCheckPromptBox = Checkbutton(self.Window, text="Concentration Check Prompt", variable=self.Vars["ConcentrationCheckPromptBoxVar"])
            self.ConcentrationCheckPromptBox.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)

            # Portrait Checkbox
            self.PortraitBox = Checkbutton(self.Window, text="Portrait", variable=self.Vars["PortraitBoxVar"])
            self.PortraitBox.grid(row=2, column=0, padx=2, pady=2, sticky=NSEW)

            # Jack of All Trades Checkbox
            self.JackOfAllTradesBox = Checkbutton(self.Window, text="Jack of All Trades", variable=self.Vars["JackOfAllTradesBoxVar"])
            self.JackOfAllTradesBox.grid(row=3, column=0, padx=2, pady=2, sticky=NSEW)

            # Remarkable Athlete Checkbox
            self.RemarkableAthleteBox = Checkbutton(self.Window, text="Remarkable Athlete", variable=self.Vars["RemarkableAthleteBoxVar"])
            self.RemarkableAthleteBox.grid(row=4, column=0, padx=2, pady=2, sticky=NSEW)

            # Observant Checkbox
            self.ObservantBox = Checkbutton(self.Window, text="Observant", variable=self.Vars["ObservantBoxVar"])
            self.ObservantBox.grid(row=5, column=0, padx=2, pady=2, sticky=NSEW)

            # Lucky (Halfling) Checkbox
            self.LuckyHalflingBox = Checkbutton(self.Window, text="Lucky (Halfling)", variable=self.Vars["LuckyHalflingBoxVar"])
            self.LuckyHalflingBox.grid(row=6, column=0, padx=2, pady=2, sticky=NSEW)

            # Buttons
            self.ButtonsFrame = Frame(self.Window)
            self.ButtonsFrame.grid_columnconfigure(0, weight=1)
            self.ButtonsFrame.grid_columnconfigure(1, weight=1)
            self.ButtonsFrame.grid(row=8, column=0, sticky=NSEW)
            self.SubmitButton = Button(self.ButtonsFrame, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
            self.SubmitButton.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
            self.CancelButton = Button(self.ButtonsFrame, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
            self.CancelButton.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)

            # Prevent Main Window Input
            self.Window.grab_set()

            # Handle Config Window Geometry and Focus
            GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst)
            self.Window.focus_force()

        def Submit(self):
            self.DataSubmitted.set(True)
            self.Window.destroy()

        def Cancel(self):
            self.DataSubmitted.set(False)
            self.Window.destroy()


class CoinCalculator:
    def __init__(self, master, DialogMode=False):
        self.CPEntryVar = StringVar()
        self.CPEntryVar.trace_add("write", lambda a, b, c: self.Calculate())
        self.SPEntryVar = StringVar()
        self.SPEntryVar.trace_add("write", lambda a, b, c: self.Calculate())
        self.EPEntryVar = StringVar()
        self.EPEntryVar.trace_add("write", lambda a, b, c: self.Calculate())
        self.GPEntryVar = StringVar()
        self.GPEntryVar.trace_add("write", lambda a, b, c: self.Calculate())
        self.PPEntryVar = StringVar()
        self.PPEntryVar.trace_add("write", lambda a, b, c: self.Calculate())
        self.CPOutputEntryVar = StringVar()
        self.SPOutputEntryVar = StringVar()
        self.EPOutputEntryVar = StringVar()
        self.GPOutputEntryVar = StringVar()
        self.PPOutputEntryVar = StringVar()
        self.WeightOutputEntryVar = StringVar()
        self.ValueCP = Decimal(0.01)
        self.ValueSP = Decimal(0.1)
        self.ValueEP = Decimal(0.5)
        self.ValueGP = Decimal(1)
        self.ValuePP = Decimal(10)
        self.WeightPerCoin = Decimal(0.02)

        # Create Window (Element)
        if not DialogMode:
            self.CoinCalculatorFrame = Frame(master)
            self.CoinCalculatorFrame.grid(row=0, column=0, sticky=NSEW)
            self.WidgetMaster = self.CoinCalculatorFrame
        else:
            self.Window = Toplevel(master)
            self.Window.wm_attributes("-toolwindow", 1)
            self.Window.wm_title("Coin Calculator")
            self.WidgetMaster = self.Window

        # Table Frame
        self.TableFrame = Frame(self.WidgetMaster)
        self.TableFrame.grid(row=0, column=0)

        # Labels
        self.InputLabel = Label(self.TableFrame, text="Input", bd=2, relief=GROOVE)
        self.InputLabel.grid(row=0, column=1, sticky=NSEW)
        self.OutputLabel = Label(self.TableFrame, text="Output", bd=2, relief=GROOVE)
        self.OutputLabel.grid(row=0, column=2, sticky=NSEW)
        self.CPLabel = Label(self.TableFrame, text="CP", bd=2, relief=GROOVE)
        self.CPLabel.grid(row=1, column=0, sticky=NSEW)
        self.SPLabel = Label(self.TableFrame, text="SP", bd=2, relief=GROOVE)
        self.SPLabel.grid(row=2, column=0, sticky=NSEW)
        self.EPLabel = Label(self.TableFrame, text="EP", bd=2, relief=GROOVE)
        self.EPLabel.grid(row=3, column=0, sticky=NSEW)
        self.GPLabel = Label(self.TableFrame, text="GP", bd=2, relief=GROOVE)
        self.GPLabel.grid(row=4, column=0, sticky=NSEW)
        self.PPLabel = Label(self.TableFrame, text="PP", bd=2, relief=GROOVE)
        self.PPLabel.grid(row=5, column=0, sticky=NSEW)
        self.WeightLabel = Label(self.TableFrame, text="Lbs.", bd=2, relief=GROOVE)
        self.WeightLabel.grid(row=6, column=0, sticky=NSEW)

        # Input Entries
        self.CPEntry = CoinsEntry(self.TableFrame, textvariable=self.CPEntryVar, justify=CENTER, width=20)
        self.CPEntry.grid(row=1, column=1, sticky=NSEW)
        self.SPEntry = CoinsEntry(self.TableFrame, textvariable=self.SPEntryVar, justify=CENTER, width=20)
        self.SPEntry.grid(row=2, column=1, sticky=NSEW)
        self.EPEntry = CoinsEntry(self.TableFrame, textvariable=self.EPEntryVar, justify=CENTER, width=20)
        self.EPEntry.grid(row=3, column=1, sticky=NSEW)
        self.GPEntry = CoinsEntry(self.TableFrame, textvariable=self.GPEntryVar, justify=CENTER, width=20)
        self.GPEntry.grid(row=4, column=1, sticky=NSEW)
        self.PPEntry = CoinsEntry(self.TableFrame, textvariable=self.PPEntryVar, justify=CENTER, width=20)
        self.PPEntry.grid(row=5, column=1, sticky=NSEW)

        # Output Entries
        self.CPOutputEntry = EntryExtended(self.TableFrame, textvariable=self.CPOutputEntryVar, justify=CENTER, width=20, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow")
        self.CPOutputEntry.grid(row=1, column=2, sticky=NSEW)
        self.SPOutputEntry = EntryExtended(self.TableFrame, textvariable=self.SPOutputEntryVar, justify=CENTER, width=20, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow")
        self.SPOutputEntry.grid(row=2, column=2, sticky=NSEW)
        self.EPOutputEntry = EntryExtended(self.TableFrame, textvariable=self.EPOutputEntryVar, justify=CENTER, width=20, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow")
        self.EPOutputEntry.grid(row=3, column=2, sticky=NSEW)
        self.GPOutputEntry = EntryExtended(self.TableFrame, textvariable=self.GPOutputEntryVar, justify=CENTER, width=20, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow")
        self.GPOutputEntry.grid(row=4, column=2, sticky=NSEW)
        self.PPOutputEntry = EntryExtended(self.TableFrame, textvariable=self.PPOutputEntryVar, justify=CENTER, width=20, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow")
        self.PPOutputEntry.grid(row=5, column=2, sticky=NSEW)
        self.WeightOutputEntry = EntryExtended(self.TableFrame, textvariable=self.WeightOutputEntryVar, justify=CENTER, width=20, state=DISABLED, disabledforeground="black", disabledbackground="light gray",
                                               cursor="arrow")
        self.WeightOutputEntry.grid(row=6, column=2, sticky=NSEW)

        # Additional Dialog Setup
        if DialogMode:
            # Close Button
            self.CloseButton = Button(self.WidgetMaster, text="Close", command=self.Close, bg=GlobalInst.ButtonColor)
            self.CloseButton.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)

            # Prevent Main Window Input
            self.Window.grab_set()

            # Handle Config Window Geometry and Focus
            GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst)
            self.Window.focus_force()

            # Focus on CP Entry
            self.CPEntry.focus_set()

    def Calculate(self):
        # Get Inputs as Decimals
        CPInput = GlobalInst.GetStringVarAsNumber(self.CPEntryVar, Mode="Decimal")
        SPInput = GlobalInst.GetStringVarAsNumber(self.SPEntryVar, Mode="Decimal")
        EPInput = GlobalInst.GetStringVarAsNumber(self.EPEntryVar, Mode="Decimal")
        GPInput = GlobalInst.GetStringVarAsNumber(self.GPEntryVar, Mode="Decimal")
        PPInput = GlobalInst.GetStringVarAsNumber(self.PPEntryVar, Mode="Decimal")

        # Get Outputs
        CPOutput = ((CPInput * self.ValueCP) + (SPInput * self.ValueSP) + (EPInput * self.ValueEP) + (GPInput * self.ValueGP) + (PPInput * self.ValuePP)) * (Decimal(1) / self.ValueCP)
        SPOutput = ((CPInput * self.ValueCP) + (SPInput * self.ValueSP) + (EPInput * self.ValueEP) + (GPInput * self.ValueGP) + (PPInput * self.ValuePP)) * (Decimal(1) / self.ValueSP)
        EPOutput = ((CPInput * self.ValueCP) + (SPInput * self.ValueSP) + (EPInput * self.ValueEP) + (GPInput * self.ValueGP) + (PPInput * self.ValuePP)) * (Decimal(1) / self.ValueEP)
        GPOutput = ((CPInput * self.ValueCP) + (SPInput * self.ValueSP) + (EPInput * self.ValueEP) + (GPInput * self.ValueGP) + (PPInput * self.ValuePP)) * (Decimal(1) / self.ValueGP)
        PPOutput = ((CPInput * self.ValueCP) + (SPInput * self.ValueSP) + (EPInput * self.ValueEP) + (GPInput * self.ValueGP) + (PPInput * self.ValuePP)) * (Decimal(1) / self.ValuePP)
        WeightOutput = (CPInput + SPInput + EPInput + GPInput + PPInput) * self.WeightPerCoin

        # Display Outputs
        self.CPOutputEntryVar.set(str(CPOutput.quantize(Decimal("0.01"))))
        self.SPOutputEntryVar.set(str(SPOutput.quantize(Decimal("0.01"))))
        self.EPOutputEntryVar.set(str(EPOutput.quantize(Decimal("0.01"))))
        self.GPOutputEntryVar.set(str(GPOutput.quantize(Decimal("0.01"))))
        self.PPOutputEntryVar.set(str(PPOutput.quantize(Decimal("0.01"))))
        self.WeightOutputEntryVar.set(str(WeightOutput.quantize(Decimal("0.01"))))

    def Close(self):
        self.Window.destroy()


class SpendCoinsMenu:
    def __init__(self, master, Coins):
        # Store Parameters
        self.Coins = Coins

        # Variables
        self.DataSubmitted = BooleanVar()
        self.SpendCPEntryVar = StringVar()
        self.SpendCPEntryVar.trace_add("write", lambda a, b, c: self.Calculate())
        self.SpendSPEntryVar = StringVar()
        self.SpendSPEntryVar.trace_add("write", lambda a, b, c: self.Calculate())
        self.SpendEPEntryVar = StringVar()
        self.SpendEPEntryVar.trace_add("write", lambda a, b, c: self.Calculate())
        self.SpendGPEntryVar = StringVar()
        self.SpendGPEntryVar.trace_add("write", lambda a, b, c: self.Calculate())
        self.SpendPPEntryVar = StringVar()
        self.SpendPPEntryVar.trace_add("write", lambda a, b, c: self.Calculate())
        self.RemainingCPEntryVar = StringVar(value=self.Coins["CP"].get())
        self.RemainingCPEntryVar.trace_add("write", lambda a, b, c: self.Calculate())
        self.RemainingSPEntryVar = StringVar(value=self.Coins["SP"].get())
        self.RemainingSPEntryVar.trace_add("write", lambda a, b, c: self.Calculate())
        self.RemainingEPEntryVar = StringVar(value=self.Coins["EP"].get())
        self.RemainingEPEntryVar.trace_add("write", lambda a, b, c: self.Calculate())
        self.RemainingGPEntryVar = StringVar(value=self.Coins["GP"].get())
        self.RemainingGPEntryVar.trace_add("write", lambda a, b, c: self.Calculate())
        self.RemainingPPEntryVar = StringVar(value=self.Coins["PP"].get())
        self.RemainingPPEntryVar.trace_add("write", lambda a, b, c: self.Calculate())
        self.MatchValuesAfterSpendingEntryVar = StringVar()
        self.MatchValuesComparatorEntryVar = StringVar()
        self.MatchValuesRemainingEntryVar = StringVar()

        # Remaining Dictionary
        self.Remaining = {}
        self.Remaining["CP"] = self.RemainingCPEntryVar
        self.Remaining["SP"] = self.RemainingSPEntryVar
        self.Remaining["EP"] = self.RemainingEPEntryVar
        self.Remaining["GP"] = self.RemainingGPEntryVar
        self.Remaining["PP"] = self.RemainingPPEntryVar

        # Create Window
        self.Window = Toplevel(master)
        self.Window.wm_attributes("-toolwindow", 1)
        self.Window.wm_title("Spend Coins")

        # Spend
        self.SpendFrame = LabelFrame(self.Window, text="Spend:")
        self.SpendFrame.grid_columnconfigure(0, weight=1)
        self.SpendFrame.grid_columnconfigure(1, weight=1)
        self.SpendFrame.grid_columnconfigure(2, weight=1)
        self.SpendFrame.grid_columnconfigure(3, weight=1)
        self.SpendFrame.grid_columnconfigure(4, weight=1)
        self.SpendFrame.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
        self.SpendCPHeader = Label(self.SpendFrame, text="CP", bd=2, relief=GROOVE)
        self.SpendCPHeader.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
        self.SpendSPHeader = Label(self.SpendFrame, text="SP", bd=2, relief=GROOVE)
        self.SpendSPHeader.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
        self.SpendEPHeader = Label(self.SpendFrame, text="EP", bd=2, relief=GROOVE)
        self.SpendEPHeader.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
        self.SpendGPHeader = Label(self.SpendFrame, text="GP", bd=2, relief=GROOVE)
        self.SpendGPHeader.grid(row=0, column=3, sticky=NSEW, padx=2, pady=2)
        self.SpendPPHeader = Label(self.SpendFrame, text="PP", bd=2, relief=GROOVE)
        self.SpendPPHeader.grid(row=0, column=4, sticky=NSEW, padx=2, pady=2)
        self.SpendCPEntry = CoinsEntry(self.SpendFrame, textvariable=self.SpendCPEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
        self.SpendCPTooltip = Tooltip(self.SpendCPEntry, "Scroll the mouse wheel or type to change.")
        self.SpendCPEntry.bind("<Return>", lambda event: self.Submit())
        self.SpendCPEntry.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
        self.SpendSPEntry = CoinsEntry(self.SpendFrame, textvariable=self.SpendSPEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
        self.SpendSPTooltip = Tooltip(self.SpendSPEntry, "Scroll the mouse wheel or type to change.")
        self.SpendSPEntry.bind("<Return>", lambda event: self.Submit())
        self.SpendSPEntry.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
        self.SpendEPEntry = CoinsEntry(self.SpendFrame, textvariable=self.SpendEPEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
        self.SpendEPTooltip = Tooltip(self.SpendEPEntry, "Scroll the mouse wheel or type to change.")
        self.SpendEPEntry.bind("<Return>", lambda event: self.Submit())
        self.SpendEPEntry.grid(row=1, column=2, sticky=NSEW, padx=2, pady=2)
        self.SpendGPEntry = CoinsEntry(self.SpendFrame, textvariable=self.SpendGPEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
        self.SpendGPTooltip = Tooltip(self.SpendGPEntry, "Scroll the mouse wheel or type to change.")
        self.SpendGPEntry.bind("<Return>", lambda event: self.Submit())
        self.SpendGPEntry.grid(row=1, column=3, sticky=NSEW, padx=2, pady=2)
        self.SpendPPEntry = CoinsEntry(self.SpendFrame, textvariable=self.SpendPPEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
        self.SpendPPTooltip = Tooltip(self.SpendPPEntry, "Scroll the mouse wheel or type to change.")
        self.SpendPPEntry.bind("<Return>", lambda event: self.Submit())
        self.SpendPPEntry.grid(row=1, column=4, sticky=NSEW, padx=2, pady=2)

        # Match Values
        self.MatchValuesFrame = LabelFrame(self.Window, text="Match Values:")
        self.MatchValuesFrame.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
        self.MatchValuesAfterSpendingHeader = Label(self.MatchValuesFrame, text="Value After\nSpending (CP)", bd=2, relief=GROOVE)
        self.MatchValuesAfterSpendingHeader.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
        self.MatchValuesAfterSpendingEntry = EntryExtended(self.MatchValuesFrame, textvariable=self.MatchValuesAfterSpendingEntryVar, width=20, state=DISABLED, disabledforeground="black",
                                                           disabledbackground="light gray",
                                                           cursor="arrow", justify=CENTER)
        self.MatchValuesAfterSpendingEntry.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
        self.MatchValuesComparatorEntry = EntryExtended(self.MatchValuesFrame, textvariable=self.MatchValuesComparatorEntryVar, width=5, state=DISABLED, disabledforeground="black",
                                                        disabledbackground="lightgray", cursor="arrow",
                                                        justify=CENTER)
        self.MatchValuesComparatorEntry.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
        self.MatchValuesRemainingHeader = Label(self.MatchValuesFrame, text="Remaining Coins\nValue (CP)", bd=2, relief=GROOVE)
        self.MatchValuesRemainingHeader.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
        self.MatchValuesRemainingEntry = EntryExtended(self.MatchValuesFrame, textvariable=self.MatchValuesRemainingEntryVar, width=20, state=DISABLED, disabledforeground="black",
                                                       disabledbackground="light gray",
                                                       cursor="arrow", justify=CENTER)
        self.MatchValuesRemainingEntry.grid(row=1, column=2, sticky=NSEW, padx=2, pady=2)

        # Remaining
        self.RemainingFrame = LabelFrame(self.Window, text="Remaining:")
        self.RemainingFrame.grid_columnconfigure(0, weight=1)
        self.RemainingFrame.grid_columnconfigure(1, weight=1)
        self.RemainingFrame.grid_columnconfigure(2, weight=1)
        self.RemainingFrame.grid_columnconfigure(3, weight=1)
        self.RemainingFrame.grid_columnconfigure(4, weight=1)
        self.RemainingFrame.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)
        self.RemainingCPHeader = Label(self.RemainingFrame, text="CP", bd=2, relief=GROOVE)
        self.RemainingCPHeader.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
        self.RemainingSPHeader = Label(self.RemainingFrame, text="SP", bd=2, relief=GROOVE)
        self.RemainingSPHeader.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
        self.RemainingEPHeader = Label(self.RemainingFrame, text="EP", bd=2, relief=GROOVE)
        self.RemainingEPHeader.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
        self.RemainingGPHeader = Label(self.RemainingFrame, text="GP", bd=2, relief=GROOVE)
        self.RemainingGPHeader.grid(row=0, column=3, sticky=NSEW, padx=2, pady=2)
        self.RemainingPPHeader = Label(self.RemainingFrame, text="PP", bd=2, relief=GROOVE)
        self.RemainingPPHeader.grid(row=0, column=4, sticky=NSEW, padx=2, pady=2)
        self.RemainingCPEntry = CoinsEntry(self.RemainingFrame, textvariable=self.RemainingCPEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
        self.RemainingCPTooltip = Tooltip(self.RemainingCPEntry, "Scroll the mouse wheel or type to change.")
        self.RemainingCPEntry.bind("<Return>", lambda event: self.Submit())
        self.RemainingCPEntry.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
        self.RemainingSPEntry = CoinsEntry(self.RemainingFrame, textvariable=self.RemainingSPEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
        self.RemainingSPTooltip = Tooltip(self.RemainingSPEntry, "Scroll the mouse wheel or type to change.")
        self.RemainingSPEntry.bind("<Return>", lambda event: self.Submit())
        self.RemainingSPEntry.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
        self.RemainingEPEntry = CoinsEntry(self.RemainingFrame, textvariable=self.RemainingEPEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
        self.RemainingEPTooltip = Tooltip(self.RemainingEPEntry, "Scroll the mouse wheel or type to change.")
        self.RemainingEPEntry.bind("<Return>", lambda event: self.Submit())
        self.RemainingEPEntry.grid(row=1, column=2, sticky=NSEW, padx=2, pady=2)
        self.RemainingGPEntry = CoinsEntry(self.RemainingFrame, textvariable=self.RemainingGPEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
        self.RemainingGPTooltip = Tooltip(self.RemainingGPEntry, "Scroll the mouse wheel or type to change.")
        self.RemainingGPEntry.bind("<Return>", lambda event: self.Submit())
        self.RemainingGPEntry.grid(row=1, column=3, sticky=NSEW, padx=2, pady=2)
        self.RemainingPPEntry = CoinsEntry(self.RemainingFrame, textvariable=self.RemainingPPEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
        self.RemainingPPTooltip = Tooltip(self.RemainingPPEntry, "Scroll the mouse wheel or type to change.")
        self.RemainingPPEntry.bind("<Return>", lambda event: self.Submit())
        self.RemainingPPEntry.grid(row=1, column=4, sticky=NSEW, padx=2, pady=2)

        # Values Key
        self.ValuesKeyStringCP = "1 cp"
        self.ValuesKeyStringSP = str(self.Coins["SPValueAsCP"]) + " cp"
        self.ValuesKeyStringEP = str(self.Coins["EPValueAsCP"]) + " cp"
        self.ValuesKeyStringGP = str(self.Coins["GPValueAsCP"]) + " cp"
        self.ValuesKeyStringPP = str(self.Coins["PPValueAsCP"]) + " cp"
        self.ValuesKeyFont = font.Font(size=6)
        self.ValuesKeyCPLabel = Label(self.RemainingFrame, text=self.ValuesKeyStringCP, font=self.ValuesKeyFont)
        self.ValuesKeyCPLabel.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)
        self.ValuesKeySPLabel = Label(self.RemainingFrame, text=self.ValuesKeyStringSP, font=self.ValuesKeyFont)
        self.ValuesKeySPLabel.grid(row=2, column=1, sticky=NSEW, padx=2, pady=2)
        self.ValuesKeyEPLabel = Label(self.RemainingFrame, text=self.ValuesKeyStringEP, font=self.ValuesKeyFont)
        self.ValuesKeyEPLabel.grid(row=2, column=2, sticky=NSEW, padx=2, pady=2)
        self.ValuesKeyGPLabel = Label(self.RemainingFrame, text=self.ValuesKeyStringGP, font=self.ValuesKeyFont)
        self.ValuesKeyGPLabel.grid(row=2, column=3, sticky=NSEW, padx=2, pady=2)
        self.ValuesKeyPPLabel = Label(self.RemainingFrame, text=self.ValuesKeyStringPP, font=self.ValuesKeyFont)
        self.ValuesKeyPPLabel.grid(row=2, column=4, sticky=NSEW, padx=2, pady=2)

        # ButtonsFrame
        self.ButtonsFrame = Frame(self.Window)
        self.ButtonsFrame.grid_columnconfigure(0, weight=1)
        self.ButtonsFrame.grid_columnconfigure(1, weight=1)
        self.ButtonsFrame.grid(row=3, column=0, sticky=NSEW)

        # Submit Button
        self.SubmitButton = Button(self.ButtonsFrame, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
        self.SubmitButton.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Cancel Button
        self.CancelButton = Button(self.ButtonsFrame, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
        self.CancelButton.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)

        # Mouse Wheel Bindings
        if GlobalInst.OS == "Windows" or GlobalInst.OS == "Darwin":
            self.SpendCPEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.SpendCPEntryVar, MinValue=0))
            self.SpendSPEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.SpendSPEntryVar, MinValue=0))
            self.SpendEPEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.SpendEPEntryVar, MinValue=0))
            self.SpendGPEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.SpendGPEntryVar, MinValue=0))
            self.SpendPPEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.SpendPPEntryVar, MinValue=0))
            self.RemainingCPEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.RemainingCPEntryVar, MinValue=0))
            self.RemainingSPEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.RemainingSPEntryVar, MinValue=0))
            self.RemainingEPEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.RemainingEPEntryVar, MinValue=0))
            self.RemainingGPEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.RemainingGPEntryVar, MinValue=0))
            self.RemainingPPEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.RemainingPPEntryVar, MinValue=0))
        elif GlobalInst.OS == "Linux":
            self.SpendCPEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.SpendCPEntryVar, MinValue=0))
            self.SpendCPEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.SpendCPEntryVar, MinValue=0))
            self.SpendSPEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.SpendSPEntryVar, MinValue=0))
            self.SpendSPEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.SpendSPEntryVar, MinValue=0))
            self.SpendEPEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.SpendEPEntryVar, MinValue=0))
            self.SpendEPEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.SpendEPEntryVar, MinValue=0))
            self.SpendGPEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.SpendGPEntryVar, MinValue=0))
            self.SpendGPEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.SpendGPEntryVar, MinValue=0))
            self.SpendPPEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.SpendPPEntryVar, MinValue=0))
            self.SpendPPEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.SpendPPEntryVar, MinValue=0))
            self.RemainingCPEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.RemainingCPEntryVar, MinValue=0))
            self.RemainingCPEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.RemainingCPEntryVar, MinValue=0))
            self.RemainingSPEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.RemainingSPEntryVar, MinValue=0))
            self.RemainingSPEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.RemainingSPEntryVar, MinValue=0))
            self.RemainingEPEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.RemainingEPEntryVar, MinValue=0))
            self.RemainingEPEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.RemainingEPEntryVar, MinValue=0))
            self.RemainingGPEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.RemainingGPEntryVar, MinValue=0))
            self.RemainingGPEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.RemainingGPEntryVar, MinValue=0))
            self.RemainingPPEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.RemainingPPEntryVar, MinValue=0))
            self.RemainingPPEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.RemainingPPEntryVar, MinValue=0))

        # Prevent Main Window Input
        self.Window.grab_set()

        # Handle Config Window Geometry and Focus
        GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst)
        self.Window.focus_force()

        # Initial Calculation
        self.Calculate(ValidateSpending=True)

        # Focus on Spend CP Entry
        self.SpendCPEntry.focus_set()

    def MouseWheelEvent(self, event, EntryVar, MinValue=None, MaxValue=None):
        try:
            OldValue = GlobalInst.GetStringVarAsNumber(EntryVar)
        except ValueError:
            OldValue = 0
        if event.delta > 0:
            ScrollDistance = 1
        elif event.delta < 0:
            ScrollDistance = -1
        else:
            ScrollDistance = 0
        NewValue = OldValue + ScrollDistance
        if MinValue != None:
            NewValue = max(MinValue, NewValue)
        if MaxValue != None:
            NewValue = min(MaxValue, NewValue)
        EntryVar.set(str(NewValue))

    def Submit(self):
        if self.Calculate(ValidateSpending=True):
            pass
        else:
            return
        self.DataSubmitted.set(True)
        self.Window.destroy()

    def Calculate(self, ValidateSpending=False):

        # Get CP Value of Current Coins
        CurrentCoinsCPAsCPValue = GlobalInst.GetStringVarAsNumber(self.Coins["CP"], Mode="Decimal")
        CurrentCoinsSPAsCPValue = GlobalInst.GetStringVarAsNumber(self.Coins["SP"], Mode="Decimal") * self.Coins["SPValueAsCP"]
        CurrentCoinsEPAsCPValue = GlobalInst.GetStringVarAsNumber(self.Coins["EP"], Mode="Decimal") * self.Coins["EPValueAsCP"]
        CurrentCoinsGPAsCPValue = GlobalInst.GetStringVarAsNumber(self.Coins["GP"], Mode="Decimal") * self.Coins["GPValueAsCP"]
        CurrentCoinsPPAsCPValue = GlobalInst.GetStringVarAsNumber(self.Coins["PP"], Mode="Decimal") * self.Coins["PPValueAsCP"]
        CurrentCoinsValue = CurrentCoinsCPAsCPValue + CurrentCoinsSPAsCPValue + CurrentCoinsEPAsCPValue + CurrentCoinsGPAsCPValue + CurrentCoinsPPAsCPValue
        CurrentCoinsValueInt = int(CurrentCoinsValue)

        # Get CP Value of Spend Amount
        SpendCPAsCPValue = GlobalInst.GetStringVarAsNumber(self.SpendCPEntryVar, Mode="Decimal")
        SpendSPAsCPValue = GlobalInst.GetStringVarAsNumber(self.SpendSPEntryVar, Mode="Decimal") * self.Coins["SPValueAsCP"]
        SpendEPAsCPValue = GlobalInst.GetStringVarAsNumber(self.SpendEPEntryVar, Mode="Decimal") * self.Coins["EPValueAsCP"]
        SpendGPAsCPValue = GlobalInst.GetStringVarAsNumber(self.SpendGPEntryVar, Mode="Decimal") * self.Coins["GPValueAsCP"]
        SpendPPAsCPValue = GlobalInst.GetStringVarAsNumber(self.SpendPPEntryVar, Mode="Decimal") * self.Coins["PPValueAsCP"]
        SpendValue = SpendCPAsCPValue + SpendSPAsCPValue + SpendEPAsCPValue + SpendGPAsCPValue + SpendPPAsCPValue
        SpendValueInt = int(SpendValue)

        # Generate Value After Spending
        ValueAfterSpending = CurrentCoinsValueInt - SpendValueInt

        # Get CP Value of Remaining Amount
        RemainingCPAsCPValue = GlobalInst.GetStringVarAsNumber(self.RemainingCPEntryVar, Mode="Decimal")
        RemainingSPAsCPValue = GlobalInst.GetStringVarAsNumber(self.RemainingSPEntryVar, Mode="Decimal") * self.Coins["SPValueAsCP"]
        RemainingEPAsCPValue = GlobalInst.GetStringVarAsNumber(self.RemainingEPEntryVar, Mode="Decimal") * self.Coins["EPValueAsCP"]
        RemainingGPAsCPValue = GlobalInst.GetStringVarAsNumber(self.RemainingGPEntryVar, Mode="Decimal") * self.Coins["GPValueAsCP"]
        RemainingPPAsCPValue = GlobalInst.GetStringVarAsNumber(self.RemainingPPEntryVar, Mode="Decimal") * self.Coins["PPValueAsCP"]
        RemainingValue = RemainingCPAsCPValue + RemainingSPAsCPValue + RemainingEPAsCPValue + RemainingGPAsCPValue + RemainingPPAsCPValue
        RemainingValueInt = int(RemainingValue)

        # Generate Strings
        ValueAfterSpendingString = str(ValueAfterSpending)
        RemainingValueString = str(RemainingValueInt)
        if ValueAfterSpending == RemainingValue:
            ComparatorString = "="
        else:
            if ValueAfterSpending < RemainingValue:
                ComparatorString = "<"
            else:
                ComparatorString = ">"

        # Set Vars
        self.MatchValuesAfterSpendingEntryVar.set(ValueAfterSpendingString)
        self.MatchValuesComparatorEntryVar.set(ComparatorString)
        self.MatchValuesRemainingEntryVar.set(RemainingValueString)

        # Set Match Colors
        EntriesToColor = [self.MatchValuesAfterSpendingEntry, self.MatchValuesComparatorEntry, self.MatchValuesRemainingEntry]
        if ComparatorString in ["<", ">"]:
            for EntryToColor in EntriesToColor:
                EntryToColor.configure(disabledforeground="red")
        else:
            for EntryToColor in EntriesToColor:
                EntryToColor.configure(disabledforeground="green")

        # Check If Spending Is Valid
        if ValidateSpending:
            if ComparatorString == "=":
                return True
            else:
                messagebox.showerror("Spending Invalid", "The value of your coins after spending and the value of the coins you have remaining must match.\n\nAdjust coins remaining until the values are equal.")
                return False

    def Cancel(self):
        self.DataSubmitted.set(False)
        self.Window.destroy()


class GainCoinsMenu:
    def __init__(self, master):
        # Variables
        self.DataSubmitted = BooleanVar()
        self.GainedCPEntryVar = StringVar()
        self.GainedSPEntryVar = StringVar()
        self.GainedEPEntryVar = StringVar()
        self.GainedGPEntryVar = StringVar()
        self.GainedPPEntryVar = StringVar()

        # Gained Dictionary
        self.Gained = {}
        self.Gained["CP"] = self.GainedCPEntryVar
        self.Gained["SP"] = self.GainedSPEntryVar
        self.Gained["EP"] = self.GainedEPEntryVar
        self.Gained["GP"] = self.GainedGPEntryVar
        self.Gained["PP"] = self.GainedPPEntryVar

        # Create Window
        self.Window = Toplevel(master)
        self.Window.wm_attributes("-toolwindow", 1)
        self.Window.wm_title("Gain Coins")

        # Spend
        self.GainFrame = Frame(self.Window)
        self.GainFrame.grid_columnconfigure(0, weight=1)
        self.GainFrame.grid_columnconfigure(1, weight=1)
        self.GainFrame.grid_columnconfigure(2, weight=1)
        self.GainFrame.grid_columnconfigure(3, weight=1)
        self.GainFrame.grid_columnconfigure(4, weight=1)
        self.GainFrame.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
        self.GainCPHeader = Label(self.GainFrame, text="CP", bd=2, relief=GROOVE)
        self.GainCPHeader.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
        self.GainSPHeader = Label(self.GainFrame, text="SP", bd=2, relief=GROOVE)
        self.GainSPHeader.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
        self.GainEPHeader = Label(self.GainFrame, text="EP", bd=2, relief=GROOVE)
        self.GainEPHeader.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
        self.GainGPHeader = Label(self.GainFrame, text="GP", bd=2, relief=GROOVE)
        self.GainGPHeader.grid(row=0, column=3, sticky=NSEW, padx=2, pady=2)
        self.GainPPHeader = Label(self.GainFrame, text="PP", bd=2, relief=GROOVE)
        self.GainPPHeader.grid(row=0, column=4, sticky=NSEW, padx=2, pady=2)
        self.GainCPEntry = CoinsEntry(self.GainFrame, textvariable=self.GainedCPEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
        self.GainCPTooltip = Tooltip(self.GainCPEntry, "Scroll the mouse wheel or type to change.")
        self.GainCPEntry.bind("<Return>", lambda event: self.Submit())
        self.GainCPEntry.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
        self.GainSPEntry = CoinsEntry(self.GainFrame, textvariable=self.GainedSPEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
        self.GainSPTooltip = Tooltip(self.GainSPEntry, "Scroll the mouse wheel or type to change.")
        self.GainSPEntry.bind("<Return>", lambda event: self.Submit())
        self.GainSPEntry.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
        self.GainEPEntry = CoinsEntry(self.GainFrame, textvariable=self.GainedEPEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
        self.GainEPTooltip = Tooltip(self.GainEPEntry, "Scroll the mouse wheel or type to change.")
        self.GainEPEntry.bind("<Return>", lambda event: self.Submit())
        self.GainEPEntry.grid(row=1, column=2, sticky=NSEW, padx=2, pady=2)
        self.GainGPEntry = CoinsEntry(self.GainFrame, textvariable=self.GainedGPEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
        self.GainGPTooltip = Tooltip(self.GainGPEntry, "Scroll the mouse wheel or type to change.")
        self.GainGPEntry.bind("<Return>", lambda event: self.Submit())
        self.GainGPEntry.grid(row=1, column=3, sticky=NSEW, padx=2, pady=2)
        self.GainPPEntry = CoinsEntry(self.GainFrame, textvariable=self.GainedPPEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
        self.GainPPTooltip = Tooltip(self.GainPPEntry, "Scroll the mouse wheel or type to change.")
        self.GainPPEntry.bind("<Return>", lambda event: self.Submit())
        self.GainPPEntry.grid(row=1, column=4, sticky=NSEW, padx=2, pady=2)

        # ButtonsFrame
        self.ButtonsFrame = Frame(self.Window)
        self.ButtonsFrame.grid_columnconfigure(0, weight=1)
        self.ButtonsFrame.grid_columnconfigure(1, weight=1)
        self.ButtonsFrame.grid(row=1, column=0, sticky=NSEW)

        # Submit Button
        self.SubmitButton = Button(self.ButtonsFrame, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
        self.SubmitButton.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Cancel Button
        self.CancelButton = Button(self.ButtonsFrame, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
        self.CancelButton.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)

        # Mouse Wheel Bindings
        if GlobalInst.OS == "Windows" or GlobalInst.OS == "Darwin":
            self.GainCPEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.GainedCPEntryVar, MinValue=0))
            self.GainSPEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.GainedSPEntryVar, MinValue=0))
            self.GainEPEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.GainedEPEntryVar, MinValue=0))
            self.GainGPEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.GainedGPEntryVar, MinValue=0))
            self.GainPPEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.GainedPPEntryVar, MinValue=0))
        elif GlobalInst.OS == "Linux":
            self.GainCPEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.GainedCPEntryVar, MinValue=0))
            self.GainCPEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.GainedCPEntryVar, MinValue=0))
            self.GainSPEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.GainedSPEntryVar, MinValue=0))
            self.GainSPEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.GainedSPEntryVar, MinValue=0))
            self.GainEPEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.GainedEPEntryVar, MinValue=0))
            self.GainEPEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.GainedEPEntryVar, MinValue=0))
            self.GainGPEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.GainedGPEntryVar, MinValue=0))
            self.GainGPEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.GainedGPEntryVar, MinValue=0))
            self.GainPPEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.GainedPPEntryVar, MinValue=0))
            self.GainPPEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.GainedPPEntryVar, MinValue=0))

        # Prevent Main Window Input
        self.Window.grab_set()

        # Handle Config Window Geometry and Focus
        GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst)
        self.Window.focus_force()

        # Focus on Spend CP Entry
        self.GainCPEntry.focus_set()

    def MouseWheelEvent(self, event, EntryVar, MinValue=None, MaxValue=None):
        try:
            OldValue = GlobalInst.GetStringVarAsNumber(EntryVar)
        except ValueError:
            OldValue = 0
        if event.delta > 0:
            ScrollDistance = 1
        elif event.delta < 0:
            ScrollDistance = -1
        else:
            ScrollDistance = 0
        NewValue = OldValue + ScrollDistance
        if MinValue != None:
            NewValue = max(MinValue, NewValue)
        if MaxValue != None:
            NewValue = min(MaxValue, NewValue)
        EntryVar.set(str(NewValue))

    def Submit(self):
        self.DataSubmitted.set(True)
        self.Window.destroy()

    def Cancel(self):
        self.DataSubmitted.set(False)
        self.Window.destroy()


class StatModifier:
    def __init__(self, master, EventString, TooltipText, BonusTo, Cursor="arrow", ACMode=False, DiceRollerMode=False, Prefix="", Suffix=""):
        # Store Parameters
        self.EventString = EventString
        self.TooltipText = TooltipText
        self.BonusTo = BonusTo
        self.ACMode = ACMode
        self.DiceRollerMode = DiceRollerMode

        # Variables
        self.Variables = {}
        self.Variables["StrengthMultiplierEntryVar"] = SavedStringVar(Prefix + "StrengthMultiplierEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["DexterityMultiplierEntryVar"] = SavedStringVar(Prefix + "DexterityMultiplierEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["ConstitutionMultiplierEntryVar"] = SavedStringVar(Prefix + "ConstitutionMultiplierEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["IntelligenceMultiplierEntryVar"] = SavedStringVar(Prefix + "IntelligenceMultiplierEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["WisdomMultiplierEntryVar"] = SavedStringVar(Prefix + "WisdomMultiplierEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["CharismaMultiplierEntryVar"] = SavedStringVar(Prefix + "CharismaMultiplierEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["ProficiencyMultiplierEntryVar"] = SavedStringVar(Prefix + "ProficiencyMultiplierEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["ManualModifierEntryVar"] = SavedStringVar(Prefix + "ManualModifierEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["StrengthMinEntryVar"] = SavedStringVar(Prefix + "StrengthMinEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["DexterityMinEntryVar"] = SavedStringVar(Prefix + "DexterityMinEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["ConstitutionMinEntryVar"] = SavedStringVar(Prefix + "ConstitutionMinEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["IntelligenceMinEntryVar"] = SavedStringVar(Prefix + "IntelligenceMinEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["WisdomMinEntryVar"] = SavedStringVar(Prefix + "WisdomMinEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["CharismaMinEntryVar"] = SavedStringVar(Prefix + "CharismaMinEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["ProficiencyMinEntryVar"] = SavedStringVar(Prefix + "ProficiencyMinEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["StrengthMaxEntryVar"] = SavedStringVar(Prefix + "StrengthMaxEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["DexterityMaxEntryVar"] = SavedStringVar(Prefix + "DexterityMaxEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["ConstitutionMaxEntryVar"] = SavedStringVar(Prefix + "ConstitutionMaxEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["IntelligenceMaxEntryVar"] = SavedStringVar(Prefix + "IntelligenceMaxEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["WisdomMaxEntryVar"] = SavedStringVar(Prefix + "WisdomMaxEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["CharismaMaxEntryVar"] = SavedStringVar(Prefix + "CharismaMaxEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["ProficiencyMaxEntryVar"] = SavedStringVar(Prefix + "ProficiencyMaxEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["StrengthMultiplierRoundUpBoxVar"] = SavedBooleanVar(Prefix + "StrengthMultiplierRoundUpBoxVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["DexterityMultiplierRoundUpBoxVar"] = SavedBooleanVar(Prefix + "DexterityMultiplierRoundUpBoxVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["ConstitutionMultiplierRoundUpBoxVar"] = SavedBooleanVar(Prefix + "ConstitutionMultiplierRoundUpBoxVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["IntelligenceMultiplierRoundUpBoxVar"] = SavedBooleanVar(Prefix + "IntelligenceMultiplierRoundUpBoxVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["WisdomMultiplierRoundUpBoxVar"] = SavedBooleanVar(Prefix + "WisdomMultiplierRoundUpBoxVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["CharismaMultiplierRoundUpBoxVar"] = SavedBooleanVar(Prefix + "CharismaMultiplierRoundUpBoxVar" + Suffix if Prefix != "" or Suffix != "" else None)
        self.Variables["ProficiencyMultiplierRoundUpBoxVar"] = SavedBooleanVar(Prefix + "ProficiencyMultiplierRoundUpBoxVar" + Suffix if Prefix != "" or Suffix != "" else None)
        if self.ACMode:
            self.Variables["ACBaseEntryVar"] = SavedStringVar(Prefix + "ACBaseEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
        if self.DiceRollerMode:
            self.Variables["ModifiersSubmitted"] = SavedBooleanVar(Prefix + "ModifiersSubmitted" + Suffix if Prefix != "" or Suffix != "" else None)
        if WindowInst.Mode == "CharacterSheet":
            self.Variables["LevelMultiplierEntryVar"] = SavedStringVar(Prefix + "LevelMultiplierEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
            self.Variables["LevelMinEntryVar"] = SavedStringVar(Prefix + "LevelMinEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
            self.Variables["LevelMaxEntryVar"] = SavedStringVar(Prefix + "LevelMaxEntryVar" + Suffix if Prefix != "" or Suffix != "" else None)
            self.Variables["LevelMultiplierRoundUpBoxVar"] = SavedBooleanVar(Prefix + "LevelMultiplierRoundUpBoxVar" + Suffix if Prefix != "" or Suffix != "" else None)

        # Configure Master (Should Be Entry Widget)
        master.configure(state=DISABLED if not self.DiceRollerMode else NORMAL, bg=GlobalInst.ButtonColor, fg="black", disabledbackground=GlobalInst.ButtonColor, disabledforeground="black", cursor=Cursor)
        master.bind(self.EventString, lambda event: self.SetModifier(ACMode=self.ACMode, DiceRollerMode=self.DiceRollerMode))
        self.Tooltip = Tooltip(master, self.TooltipText)

    def GetModifier(self):
        StrengthMod = self.GetSingleStatMod(GlobalInst.StatModifierEntries["Strength"], self.Variables["StrengthMultiplierEntryVar"], self.Variables["StrengthMultiplierRoundUpBoxVar"],
                                            self.Variables["StrengthMaxEntryVar"], self.Variables["StrengthMinEntryVar"])
        DexterityMod = self.GetSingleStatMod(GlobalInst.StatModifierEntries["Dexterity"], self.Variables["DexterityMultiplierEntryVar"], self.Variables["DexterityMultiplierRoundUpBoxVar"],
                                             self.Variables["DexterityMaxEntryVar"], self.Variables["DexterityMinEntryVar"])
        ConstitutionMod = self.GetSingleStatMod(GlobalInst.StatModifierEntries["Constitution"], self.Variables["ConstitutionMultiplierEntryVar"], self.Variables["ConstitutionMultiplierRoundUpBoxVar"],
                                                self.Variables["ConstitutionMaxEntryVar"], self.Variables["ConstitutionMinEntryVar"])
        IntelligenceMod = self.GetSingleStatMod(GlobalInst.StatModifierEntries["Intelligence"], self.Variables["IntelligenceMultiplierEntryVar"], self.Variables["IntelligenceMultiplierRoundUpBoxVar"],
                                                self.Variables["IntelligenceMaxEntryVar"], self.Variables["IntelligenceMinEntryVar"])
        WisdomMod = self.GetSingleStatMod(GlobalInst.StatModifierEntries["Wisdom"], self.Variables["WisdomMultiplierEntryVar"], self.Variables["WisdomMultiplierRoundUpBoxVar"],
                                          self.Variables["WisdomMaxEntryVar"], self.Variables["WisdomMinEntryVar"])
        CharismaMod = self.GetSingleStatMod(GlobalInst.StatModifierEntries["Charisma"], self.Variables["CharismaMultiplierEntryVar"], self.Variables["CharismaMultiplierRoundUpBoxVar"],
                                            self.Variables["CharismaMaxEntryVar"], self.Variables["CharismaMinEntryVar"])
        ProficiencyMod = self.GetSingleStatMod(GlobalInst.StatModifierEntries["Proficiency"], self.Variables["ProficiencyMultiplierEntryVar"], self.Variables["ProficiencyMultiplierRoundUpBoxVar"],
                                               self.Variables["ProficiencyMaxEntryVar"], self.Variables["ProficiencyMinEntryVar"])
        ManualMod = GlobalInst.GetStringVarAsNumber(self.Variables["ManualModifierEntryVar"])
        if self.ACMode:
            ACBase = GlobalInst.GetStringVarAsNumber(self.Variables["ACBaseEntryVar"])
        else:
            ACBase = 0
        if WindowInst.Mode == "CharacterSheet":
            LevelMod = self.GetSingleStatMod(GlobalInst.StatModifierEntries["Level"], self.Variables["LevelMultiplierEntryVar"], self.Variables["LevelMultiplierRoundUpBoxVar"], self.Variables["LevelMaxEntryVar"],
                                             self.Variables["LevelMinEntryVar"])
        else:
            LevelMod = 0
        TotalModifier = StrengthMod + DexterityMod + ConstitutionMod + IntelligenceMod + WisdomMod + CharismaMod + ProficiencyMod + LevelMod + ManualMod + ACBase
        return TotalModifier

    def GetPresetDiceRollModifier(self):
        if self.DiceRollerMode:
            if self.Variables["ModifiersSubmitted"].get():
                TotalModifier = self.GetModifier()
                return str(TotalModifier)
            else:
                return ""
        else:
            return ""

    def GetSingleStatMod(self, ModifierVar, MultiplierVar, RoundUpVar, MaxVar, MinVar):
        Mod = GlobalInst.GetStringVarAsNumber(MultiplierVar, Mode="Float") * GlobalInst.GetStringVarAsNumber(ModifierVar, Mode="Float")
        if RoundUpVar.get():
            Mod = math.ceil(Mod)
        else:
            Mod = math.floor(Mod)
        if MaxVar.get() != "":
            Mod = min(Mod, GlobalInst.GetStringVarAsNumber(MaxVar))
        if MinVar.get() != "":
            Mod = max(Mod, GlobalInst.GetStringVarAsNumber(MinVar))
        return Mod

    def SetModifier(self, BonusToOverride=None, ACMode=False, DiceRollerMode=False):
        # Determine Bonus To String
        if BonusToOverride is not None:
            BonusToString = BonusToOverride
        else:
            BonusToString = self.BonusTo

        # Create Config Window and Wait
        ModifierConfigInst = self.ModifierConfig(self.Variables, BonusToString, ACMode=ACMode, DiceRollerMode=DiceRollerMode)
        WindowInst.wait_window(ModifierConfigInst.Window)

        # Handle Variables
        if ModifierConfigInst.DataSubmitted.get():
            SetVars = True
            if self.DiceRollerMode:
                if ModifierConfigInst.Variables["ModifiersSubmitted"].get():
                    pass
                else:
                    SetVars = False
                    self.DefaultValues()
            if SetVars:
                for Tag, Var in ModifierConfigInst.Variables.items():
                    self.Variables[Tag].set(Var.get())

        # Update Stats and Inventory
        if WindowInst.Mode == "CharacterSheet":
            CharacterSheetInst.UpdateStatsAndInventory()
        elif WindowInst.Mode == "NPCSheet":
            CreatureDataInst.UpdateStats()

    def UpdateTags(self, Prefix="", Suffix=""):
        self.Variables["StrengthMultiplierEntryVar"].UpdateTag(Prefix + "StrengthMultiplierEntryVar" + Suffix)
        self.Variables["DexterityMultiplierEntryVar"].UpdateTag(Prefix + "DexterityMultiplierEntryVar" + Suffix)
        self.Variables["ConstitutionMultiplierEntryVar"].UpdateTag(Prefix + "ConstitutionMultiplierEntryVar" + Suffix)
        self.Variables["IntelligenceMultiplierEntryVar"].UpdateTag(Prefix + "IntelligenceMultiplierEntryVar" + Suffix)
        self.Variables["WisdomMultiplierEntryVar"].UpdateTag(Prefix + "WisdomMultiplierEntryVar" + Suffix)
        self.Variables["CharismaMultiplierEntryVar"].UpdateTag(Prefix + "CharismaMultiplierEntryVar" + Suffix)
        self.Variables["ProficiencyMultiplierEntryVar"].UpdateTag(Prefix + "ProficiencyMultiplierEntryVar" + Suffix)
        self.Variables["StrengthMinEntryVar"].UpdateTag(Prefix + "StrengthMinEntryVar" + Suffix)
        self.Variables["DexterityMinEntryVar"].UpdateTag(Prefix + "DexterityMinEntryVar" + Suffix)
        self.Variables["ConstitutionMinEntryVar"].UpdateTag(Prefix + "ConstitutionMinEntryVar" + Suffix)
        self.Variables["IntelligenceMinEntryVar"].UpdateTag(Prefix + "IntelligenceMinEntryVar" + Suffix)
        self.Variables["WisdomMinEntryVar"].UpdateTag(Prefix + "WisdomMinEntryVar" + Suffix)
        self.Variables["CharismaMinEntryVar"].UpdateTag(Prefix + "CharismaMinEntryVar" + Suffix)
        self.Variables["ProficiencyMinEntryVar"].UpdateTag(Prefix + "ProficiencyMinEntryVar" + Suffix)
        self.Variables["StrengthMaxEntryVar"].UpdateTag(Prefix + "StrengthMaxEntryVar" + Suffix)
        self.Variables["DexterityMaxEntryVar"].UpdateTag(Prefix + "DexterityMaxEntryVar" + Suffix)
        self.Variables["ConstitutionMaxEntryVar"].UpdateTag(Prefix + "ConstitutionMaxEntryVar" + Suffix)
        self.Variables["IntelligenceMaxEntryVar"].UpdateTag(Prefix + "IntelligenceMaxEntryVar" + Suffix)
        self.Variables["WisdomMaxEntryVar"].UpdateTag(Prefix + "WisdomMaxEntryVar" + Suffix)
        self.Variables["CharismaMaxEntryVar"].UpdateTag(Prefix + "CharismaMaxEntryVar" + Suffix)
        self.Variables["ProficiencyMaxEntryVar"].UpdateTag(Prefix + "ProficiencyMaxEntryVar" + Suffix)
        self.Variables["ManualModifierEntryVar"].UpdateTag(Prefix + "ManualModifierEntryVar" + Suffix)
        self.Variables["StrengthMultiplierRoundUpBoxVar"].UpdateTag(Prefix + "StrengthMultiplierRoundUpBoxVar" + Suffix)
        self.Variables["DexterityMultiplierRoundUpBoxVar"].UpdateTag(Prefix + "DexterityMultiplierRoundUpBoxVar" + Suffix)
        self.Variables["ConstitutionMultiplierRoundUpBoxVar"].UpdateTag(Prefix + "ConstitutionMultiplierRoundUpBoxVar" + Suffix)
        self.Variables["IntelligenceMultiplierRoundUpBoxVar"].UpdateTag(Prefix + "IntelligenceMultiplierRoundUpBoxVar" + Suffix)
        self.Variables["WisdomMultiplierRoundUpBoxVar"].UpdateTag(Prefix + "WisdomMultiplierRoundUpBoxVar" + Suffix)
        self.Variables["CharismaMultiplierRoundUpBoxVar"].UpdateTag(Prefix + "CharismaMultiplierRoundUpBoxVar" + Suffix)
        self.Variables["ProficiencyMultiplierRoundUpBoxVar"].UpdateTag(Prefix + "ProficiencyMultiplierRoundUpBoxVar" + Suffix)
        if self.ACMode:
            self.Variables["ACBaseEntryVar"].UpdateTag(Prefix + "ACBaseEntryVar" + Suffix)
        if self.DiceRollerMode:
            self.Variables["ModifiersSubmitted"].UpdateTag(Prefix + "ModifiersSubmitted" + Suffix)
        if WindowInst.Mode == "CharacterSheet":
            self.Variables["LevelMultiplierEntryVar"].UpdateTag(Prefix + "LevelMultiplierEntryVar" + Suffix)
            self.Variables["LevelMinEntryVar"].UpdateTag(Prefix + "LevelMinEntryVar" + Suffix)
            self.Variables["LevelMaxEntryVar"].UpdateTag(Prefix + "LevelMaxEntryVar" + Suffix)
            self.Variables["LevelMultiplierRoundUpBoxVar"].UpdateTag(Prefix + "LevelMultiplierRoundUpBoxVar" + Suffix)

    def DefaultValues(self):
        self.Variables["StrengthMultiplierEntryVar"].set("")
        self.Variables["DexterityMultiplierEntryVar"].set("")
        self.Variables["ConstitutionMultiplierEntryVar"].set("")
        self.Variables["IntelligenceMultiplierEntryVar"].set("")
        self.Variables["WisdomMultiplierEntryVar"].set("")
        self.Variables["CharismaMultiplierEntryVar"].set("")
        self.Variables["ProficiencyMultiplierEntryVar"].set("")
        self.Variables["ManualModifierEntryVar"].set("")
        self.Variables["StrengthMinEntryVar"].set("")
        self.Variables["DexterityMinEntryVar"].set("")
        self.Variables["ConstitutionMinEntryVar"].set("")
        self.Variables["IntelligenceMinEntryVar"].set("")
        self.Variables["WisdomMinEntryVar"].set("")
        self.Variables["CharismaMinEntryVar"].set("")
        self.Variables["ProficiencyMinEntryVar"].set("")
        self.Variables["StrengthMaxEntryVar"].set("")
        self.Variables["DexterityMaxEntryVar"].set("")
        self.Variables["ConstitutionMaxEntryVar"].set("")
        self.Variables["IntelligenceMaxEntryVar"].set("")
        self.Variables["WisdomMaxEntryVar"].set("")
        self.Variables["CharismaMaxEntryVar"].set("")
        self.Variables["ProficiencyMaxEntryVar"].set("")
        self.Variables["StrengthMultiplierRoundUpBoxVar"].set(False)
        self.Variables["DexterityMultiplierRoundUpBoxVar"].set(False)
        self.Variables["ConstitutionMultiplierRoundUpBoxVar"].set(False)
        self.Variables["IntelligenceMultiplierRoundUpBoxVar"].set(False)
        self.Variables["WisdomMultiplierRoundUpBoxVar"].set(False)
        self.Variables["CharismaMultiplierRoundUpBoxVar"].set(False)
        self.Variables["ProficiencyMultiplierRoundUpBoxVar"].set(False)
        if self.ACMode:
            self.Variables["ACBaseEntryVar"].set("")
        if self.DiceRollerMode:
            self.Variables["ModifiersSubmitted"].set(False)
        if WindowInst.Mode == "CharacterSheet":
            self.Variables["LevelMultiplierEntryVar"].set("")
            self.Variables["LevelMinEntryVar"].set("")
            self.Variables["LevelMaxEntryVar"].set("")
            self.Variables["LevelMultiplierRoundUpBoxVar"].set(False)

    class ModifierConfig:
        def __init__(self, CurrentVariables, BonusTo, ACMode=False, DiceRollerMode=False):
            # Store Parameters
            self.BonusTo = BonusTo
            self.ACMode = ACMode
            self.DiceRollerMode = DiceRollerMode

            # Variables
            self.DataSubmitted = BooleanVar()
            self.Variables = {}
            self.Variables["StrengthMultiplierEntryVar"] = StringVar(value=CurrentVariables["StrengthMultiplierEntryVar"].get())
            self.Variables["DexterityMultiplierEntryVar"] = StringVar(value=CurrentVariables["DexterityMultiplierEntryVar"].get())
            self.Variables["ConstitutionMultiplierEntryVar"] = StringVar(value=CurrentVariables["ConstitutionMultiplierEntryVar"].get())
            self.Variables["IntelligenceMultiplierEntryVar"] = StringVar(value=CurrentVariables["IntelligenceMultiplierEntryVar"].get())
            self.Variables["WisdomMultiplierEntryVar"] = StringVar(value=CurrentVariables["WisdomMultiplierEntryVar"].get())
            self.Variables["CharismaMultiplierEntryVar"] = StringVar(value=CurrentVariables["CharismaMultiplierEntryVar"].get())
            self.Variables["ProficiencyMultiplierEntryVar"] = StringVar(value=CurrentVariables["ProficiencyMultiplierEntryVar"].get())
            self.Variables["StrengthMinEntryVar"] = StringVar(value=CurrentVariables["StrengthMinEntryVar"].get())
            self.Variables["DexterityMinEntryVar"] = StringVar(value=CurrentVariables["DexterityMinEntryVar"].get())
            self.Variables["ConstitutionMinEntryVar"] = StringVar(value=CurrentVariables["ConstitutionMinEntryVar"].get())
            self.Variables["IntelligenceMinEntryVar"] = StringVar(value=CurrentVariables["IntelligenceMinEntryVar"].get())
            self.Variables["WisdomMinEntryVar"] = StringVar(value=CurrentVariables["WisdomMinEntryVar"].get())
            self.Variables["CharismaMinEntryVar"] = StringVar(value=CurrentVariables["CharismaMinEntryVar"].get())
            self.Variables["ProficiencyMinEntryVar"] = StringVar(value=CurrentVariables["ProficiencyMinEntryVar"].get())
            self.Variables["StrengthMaxEntryVar"] = StringVar(value=CurrentVariables["StrengthMaxEntryVar"].get())
            self.Variables["DexterityMaxEntryVar"] = StringVar(value=CurrentVariables["DexterityMaxEntryVar"].get())
            self.Variables["ConstitutionMaxEntryVar"] = StringVar(value=CurrentVariables["ConstitutionMaxEntryVar"].get())
            self.Variables["IntelligenceMaxEntryVar"] = StringVar(value=CurrentVariables["IntelligenceMaxEntryVar"].get())
            self.Variables["WisdomMaxEntryVar"] = StringVar(value=CurrentVariables["WisdomMaxEntryVar"].get())
            self.Variables["CharismaMaxEntryVar"] = StringVar(value=CurrentVariables["CharismaMaxEntryVar"].get())
            self.Variables["ProficiencyMaxEntryVar"] = StringVar(value=CurrentVariables["ProficiencyMaxEntryVar"].get())
            self.Variables["ManualModifierEntryVar"] = StringVar(value=CurrentVariables["ManualModifierEntryVar"].get())
            self.Variables["StrengthMultiplierRoundUpBoxVar"] = BooleanVar(value=CurrentVariables["StrengthMultiplierRoundUpBoxVar"].get())
            self.Variables["DexterityMultiplierRoundUpBoxVar"] = BooleanVar(value=CurrentVariables["DexterityMultiplierRoundUpBoxVar"].get())
            self.Variables["ConstitutionMultiplierRoundUpBoxVar"] = BooleanVar(value=CurrentVariables["ConstitutionMultiplierRoundUpBoxVar"].get())
            self.Variables["IntelligenceMultiplierRoundUpBoxVar"] = BooleanVar(value=CurrentVariables["IntelligenceMultiplierRoundUpBoxVar"].get())
            self.Variables["WisdomMultiplierRoundUpBoxVar"] = BooleanVar(value=CurrentVariables["WisdomMultiplierRoundUpBoxVar"].get())
            self.Variables["CharismaMultiplierRoundUpBoxVar"] = BooleanVar(value=CurrentVariables["CharismaMultiplierRoundUpBoxVar"].get())
            self.Variables["ProficiencyMultiplierRoundUpBoxVar"] = BooleanVar(value=CurrentVariables["ProficiencyMultiplierRoundUpBoxVar"].get())
            if self.ACMode:
                self.Variables["ACBaseEntryVar"] = StringVar(value=CurrentVariables["ACBaseEntryVar"].get())
            if self.DiceRollerMode:
                self.Variables["ModifiersSubmitted"] = BooleanVar(value=CurrentVariables["ModifiersSubmitted"].get())
            if WindowInst.Mode == "CharacterSheet":
                self.Variables["LevelMultiplierEntryVar"] = StringVar(value=CurrentVariables["LevelMultiplierEntryVar"].get())
                self.Variables["LevelMinEntryVar"] = StringVar(value=CurrentVariables["LevelMinEntryVar"].get())
                self.Variables["LevelMaxEntryVar"] = StringVar(value=CurrentVariables["LevelMaxEntryVar"].get())
                self.Variables["LevelMultiplierRoundUpBoxVar"] = StringVar(value=CurrentVariables["LevelMultiplierRoundUpBoxVar"].get())

            # Window Title
            if self.ACMode:
                self.WindowTitle = "AC Data"
            else:
                self.WindowTitle = self.BonusTo + " Stat Modifier"

            # Create Window
            self.Window = Toplevel(WindowInst)
            self.Window.wm_attributes("-toolwindow", 1)
            self.Window.wm_title(self.WindowTitle)

            # Table Frame
            self.TableFrame = Frame(self.Window)
            self.TableFrame.grid(row=0, column=0, sticky=NSEW)

            if self.ACMode:
                self.ACBaseFrame = LabelFrame(self.TableFrame, text="Base AC")
                self.ACBaseFrame.grid_columnconfigure(0, weight=1)
                self.ACBaseFrame.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2, columnspan=5)
                self.ACBaseEntry = EntryExtended(self.ACBaseFrame, justify=CENTER, width=5, textvariable=self.Variables["ACBaseEntryVar"])
                self.ACBaseEntry.ConfigureValidation(lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Base AC must be a whole number."), "key")
                self.ACBaseEntry.grid(row=0, column=0, sticky=NSEW)

            # Headers
            self.StatHeader = Label(self.TableFrame, text="Stat", bd=2, relief=GROOVE)
            self.StatHeader.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
            self.MultiplierHeader = Label(self.TableFrame, text="Multiplier", bd=2, relief=GROOVE)
            self.MultiplierHeader.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
            self.RoundUpHeader = Label(self.TableFrame, text="Round Up", bd=2, relief=GROOVE)
            self.RoundUpHeader.grid(row=1, column=2, sticky=NSEW, padx=2, pady=2)
            self.MinHeader = Label(self.TableFrame, text="Min", bd=2, relief=GROOVE)
            self.MinHeader.grid(row=1, column=3, sticky=NSEW, padx=2, pady=2)
            self.MaxHeader = Label(self.TableFrame, text="Max", bd=2, relief=GROOVE)
            self.MaxHeader.grid(row=1, column=4, sticky=NSEW, padx=2, pady=2)
            self.StrengthLabel = Label(self.TableFrame, text="Strength")
            self.StrengthLabel.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)
            self.DexterityLabel = Label(self.TableFrame, text="Dexterity")
            self.DexterityLabel.grid(row=3, column=0, sticky=NSEW, padx=2, pady=2)
            self.ConstitutionLabel = Label(self.TableFrame, text="Constitution")
            self.ConstitutionLabel.grid(row=4, column=0, sticky=NSEW, padx=2, pady=2)
            self.IntelligenceLabel = Label(self.TableFrame, text="Intelligence")
            self.IntelligenceLabel.grid(row=5, column=0, sticky=NSEW, padx=2, pady=2)
            self.WisdomLabel = Label(self.TableFrame, text="Wisdom")
            self.WisdomLabel.grid(row=6, column=0, sticky=NSEW, padx=2, pady=2)
            self.CharismaLabel = Label(self.TableFrame, text="Charisma")
            self.CharismaLabel.grid(row=7, column=0, sticky=NSEW, padx=2, pady=2)
            self.ProficiencyLabel = Label(self.TableFrame, text="Proficiency")
            self.ProficiencyLabel.grid(row=8, column=0, sticky=NSEW, padx=2, pady=2)
            if WindowInst.Mode == "CharacterSheet":
                self.LevelLabel = Label(self.TableFrame, text="Level")
                self.LevelLabel.grid(row=9, column=0, sticky=NSEW, padx=2, pady=2)

            # Multiplier Entries
            self.StrengthMultiplierEntry = StatModifierMultiplierEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["StrengthMultiplierEntryVar"])
            self.StrengthMultiplierEntry.grid(row=2, column=1, sticky=NSEW, padx=2, pady=2)
            self.DexterityMultiplierEntry = StatModifierMultiplierEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["DexterityMultiplierEntryVar"])
            self.DexterityMultiplierEntry.grid(row=3, column=1, sticky=NSEW, padx=2, pady=2)
            self.ConstitutionMultiplierEntry = StatModifierMultiplierEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["ConstitutionMultiplierEntryVar"])
            self.ConstitutionMultiplierEntry.grid(row=4, column=1, sticky=NSEW, padx=2, pady=2)
            self.IntelligenceMultiplierEntry = StatModifierMultiplierEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["IntelligenceMultiplierEntryVar"])
            self.IntelligenceMultiplierEntry.grid(row=5, column=1, sticky=NSEW, padx=2, pady=2)
            self.WisdomMultiplierEntry = StatModifierMultiplierEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["WisdomMultiplierEntryVar"])
            self.WisdomMultiplierEntry.grid(row=6, column=1, sticky=NSEW, padx=2, pady=2)
            self.CharismaMultiplierEntry = StatModifierMultiplierEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["CharismaMultiplierEntryVar"])
            self.CharismaMultiplierEntry.grid(row=7, column=1, sticky=NSEW, padx=2, pady=2)
            self.ProficiencyMultiplierEntry = StatModifierMultiplierEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["ProficiencyMultiplierEntryVar"])
            self.ProficiencyMultiplierEntry.grid(row=8, column=1, sticky=NSEW, padx=2, pady=2)
            if WindowInst.Mode == "CharacterSheet":
                self.LevelMultiplierEntry = StatModifierMultiplierEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["LevelMultiplierEntryVar"])
                self.LevelMultiplierEntry.grid(row=9, column=1, sticky=NSEW, padx=2, pady=2)

            # Round Up Boxes
            self.StrengthMultiplierRoundUpBox = Checkbutton(self.TableFrame, variable=self.Variables["StrengthMultiplierRoundUpBoxVar"])
            self.StrengthMultiplierRoundUpBox.grid(row=2, column=2, sticky=NSEW, padx=2, pady=2)
            self.DexterityMultiplierRoundUpBox = Checkbutton(self.TableFrame, variable=self.Variables["DexterityMultiplierRoundUpBoxVar"])
            self.DexterityMultiplierRoundUpBox.grid(row=3, column=2, sticky=NSEW, padx=2, pady=2)
            self.ConstitutionMultiplierRoundUpBox = Checkbutton(self.TableFrame, variable=self.Variables["ConstitutionMultiplierRoundUpBoxVar"])
            self.ConstitutionMultiplierRoundUpBox.grid(row=4, column=2, sticky=NSEW, padx=2, pady=2)
            self.IntelligenceMultiplierRoundUpBox = Checkbutton(self.TableFrame, variable=self.Variables["IntelligenceMultiplierRoundUpBoxVar"])
            self.IntelligenceMultiplierRoundUpBox.grid(row=5, column=2, sticky=NSEW, padx=2, pady=2)
            self.WisdomMultiplierRoundUpBox = Checkbutton(self.TableFrame, variable=self.Variables["WisdomMultiplierRoundUpBoxVar"])
            self.WisdomMultiplierRoundUpBox.grid(row=6, column=2, sticky=NSEW, padx=2, pady=2)
            self.CharismaMultiplierRoundUpBox = Checkbutton(self.TableFrame, variable=self.Variables["CharismaMultiplierRoundUpBoxVar"])
            self.CharismaMultiplierRoundUpBox.grid(row=7, column=2, sticky=NSEW, padx=2, pady=2)
            self.ProficiencyMultiplierRoundUpBox = Checkbutton(self.TableFrame, variable=self.Variables["ProficiencyMultiplierRoundUpBoxVar"])
            self.ProficiencyMultiplierRoundUpBox.grid(row=8, column=2, sticky=NSEW, padx=2, pady=2)
            if WindowInst.Mode == "CharacterSheet":
                self.LevelMultiplierRoundUpBox = Checkbutton(self.TableFrame, variable=self.Variables["LevelMultiplierRoundUpBoxVar"])
                self.LevelMultiplierRoundUpBox.grid(row=9, column=2, sticky=NSEW, padx=2, pady=2)

            # Min Entries
            self.StrengthMinEntry = StatModifierMinMaxEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["StrengthMinEntryVar"])
            self.StrengthMinEntry.grid(row=2, column=3, sticky=NSEW, padx=2, pady=2)
            self.DexterityMinEntry = StatModifierMinMaxEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["DexterityMinEntryVar"])
            self.DexterityMinEntry.grid(row=3, column=3, sticky=NSEW, padx=2, pady=2)
            self.ConstitutionMinEntry = StatModifierMinMaxEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["ConstitutionMinEntryVar"])
            self.ConstitutionMinEntry.grid(row=4, column=3, sticky=NSEW, padx=2, pady=2)
            self.IntelligenceMinEntry = StatModifierMinMaxEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["IntelligenceMinEntryVar"])
            self.IntelligenceMinEntry.grid(row=5, column=3, sticky=NSEW, padx=2, pady=2)
            self.WisdomMinEntry = StatModifierMinMaxEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["WisdomMinEntryVar"])
            self.WisdomMinEntry.grid(row=6, column=3, sticky=NSEW, padx=2, pady=2)
            self.CharismaMinEntry = StatModifierMinMaxEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["CharismaMinEntryVar"])
            self.CharismaMinEntry.grid(row=7, column=3, sticky=NSEW, padx=2, pady=2)
            self.ProficiencyMinEntry = StatModifierMinMaxEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["ProficiencyMinEntryVar"])
            self.ProficiencyMinEntry.grid(row=8, column=3, sticky=NSEW, padx=2, pady=2)
            if WindowInst.Mode == "CharacterSheet":
                self.LevelMinEntry = StatModifierMinMaxEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["LevelMinEntryVar"])
                self.LevelMinEntry.grid(row=9, column=3, sticky=NSEW, padx=2, pady=2)

            # Max Entries
            self.StrengthMaxEntry = StatModifierMinMaxEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["StrengthMaxEntryVar"])
            self.StrengthMaxEntry.grid(row=2, column=4, sticky=NSEW, padx=2, pady=2)
            self.DexterityMaxEntry = StatModifierMinMaxEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["DexterityMaxEntryVar"])
            self.DexterityMaxEntry.grid(row=3, column=4, sticky=NSEW, padx=2, pady=2)
            self.ConstitutionMaxEntry = StatModifierMinMaxEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["ConstitutionMaxEntryVar"])
            self.ConstitutionMaxEntry.grid(row=4, column=4, sticky=NSEW, padx=2, pady=2)
            self.IntelligenceMaxEntry = StatModifierMinMaxEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["IntelligenceMaxEntryVar"])
            self.IntelligenceMaxEntry.grid(row=5, column=4, sticky=NSEW, padx=2, pady=2)
            self.WisdomMaxEntry = StatModifierMinMaxEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["WisdomMaxEntryVar"])
            self.WisdomMaxEntry.grid(row=6, column=4, sticky=NSEW, padx=2, pady=2)
            self.CharismaMaxEntry = StatModifierMinMaxEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["CharismaMaxEntryVar"])
            self.CharismaMaxEntry.grid(row=7, column=4, sticky=NSEW, padx=2, pady=2)
            self.ProficiencyMaxEntry = StatModifierMinMaxEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["ProficiencyMaxEntryVar"])
            self.ProficiencyMaxEntry.grid(row=8, column=4, sticky=NSEW, padx=2, pady=2)
            if WindowInst.Mode == "CharacterSheet":
                self.LevelMaxEntry = StatModifierMinMaxEntry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["LevelMaxEntryVar"])
                self.LevelMaxEntry.grid(row=9, column=4, sticky=NSEW, padx=2, pady=2)

            # Manual Modifier
            self.ManualModifierFrame = LabelFrame(self.TableFrame, text="Manual Modifier:")
            self.ManualModifierFrame.grid_columnconfigure(0, weight=1)
            self.ManualModifierFrame.grid(row=10, column=0, columnspan=5, sticky=NSEW, padx=2, pady=2)
            self.ManualModifierEntry = EntryExtended(self.ManualModifierFrame, justify=CENTER, width=5, textvariable=self.Variables["ManualModifierEntryVar"])
            self.ManualModifierEntry.ConfigureValidation(lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Manual modifier must be a whole number."), "key")
            self.ManualModifierEntry.grid(row=0, column=0, sticky=NSEW)

            # Buttons
            self.ButtonsFrame = Frame(self.Window)
            self.ButtonsFrame.grid_columnconfigure(0, weight=1)
            self.ButtonsFrame.grid_columnconfigure(1, weight=1)
            self.ButtonsFrame.grid(row=1, column=0, sticky=NSEW)
            self.ClearButtonOffset = 0
            self.SubmitButton = Button(self.ButtonsFrame, text="Submit", bg=GlobalInst.ButtonColor, command=self.Submit)
            self.SubmitButton.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
            if self.DiceRollerMode:
                self.ClearButton = Button(self.ButtonsFrame, text="Clear", bg=GlobalInst.ButtonColor, command=self.Clear)
                self.ClearButton.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
                self.ButtonsFrame.grid_columnconfigure(2, weight=1)
                self.ClearButtonOffset = 1
            self.CancelButton = Button(self.ButtonsFrame, text="Cancel", bg=GlobalInst.ButtonColor, command=self.Cancel)
            self.CancelButton.grid(row=0, column=1 + self.ClearButtonOffset, sticky=NSEW, padx=2, pady=2)

            # Prevent Main Window Input
            self.Window.grab_set()

            # Handle Config Window Geometry and Focus
            GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst)
            self.Window.focus_force()

            # Focus on First Entry
            if self.ACMode:
                self.ACBaseEntry.focus_set()
            else:
                self.StrengthMultiplierEntry.focus_set()

        def Submit(self):
            self.DataSubmitted.set(True)
            if self.DiceRollerMode:
                self.Variables["ModifiersSubmitted"].set(True)
            self.Window.destroy()

        def Clear(self):
            if messagebox.askyesno("Clear Preset Roll Modifier", "Are you sure you want to clear modifier data from this preset roll?  This cannot be undone."):
                pass
            else:
                return
            self.DataSubmitted.set(True)
            self.Variables["ModifiersSubmitted"].set(False)
            self.Window.destroy()

        def Cancel(self):
            self.DataSubmitted.set(False)
            self.Window.destroy()


class AbilityScoreDerivatives:
    def __init__(self, master, List, SaveTagPrefix, Column, AttackTypeStringSuffix=""):
        # Store Parameters
        self.SaveTagPrefix = SaveTagPrefix
        self.Column = Column
        self.AttackTypeStringSuffix = AttackTypeStringSuffix

        # Variables
        self.AbilityScoreSelectionDropdownVar = SavedStringVar(self.SaveTagPrefix + "AbilitySelectionDropdownVar" + str(self.Column))
        self.AbilityScoreSelectionDropdownVar.trace_add("write", lambda a, b, c: CharacterSheetInst.UpdateStatsAndInventory())
        self.SaveDCEntryVar = StringVar()
        self.AttackModifierEntryVar = StringVar()

        # Add to List
        List.append(self)

        # Ability Score Selection
        self.AbilityScoreSelectionDropdown = DropdownExtended(master, textvariable=self.AbilityScoreSelectionDropdownVar, values=["", "STR", "DEX", "CON", "INT", "WIS", "CHA"], width=5, state="readonly", justify=CENTER)
        self.AbilityScoreSelectionDropdown.grid(row=0, column=self.Column, padx=2, pady=2, sticky=NSEW)

        # Save DC
        self.SaveDCEntry = EntryExtended(master, justify=CENTER, width=2, textvariable=self.SaveDCEntryVar, cursor="arrow")
        self.SaveDCEntry.grid(row=1, column=self.Column, padx=2, pady=2, sticky=NSEW)
        self.SaveDCEntryStatModifierInst = StatModifier(self.SaveDCEntry, "<Button-1>", "Left-click on a save DC to set a stat modifier.", "Save DC", Prefix=self.SaveTagPrefix + "SaveDC", Suffix=str(self.Column))

        # Attack Modifier
        self.AttackModifierEntry = EntryExtended(master, justify=CENTER, width=2, textvariable=self.AttackModifierEntryVar, cursor="dotbox")
        self.AttackModifierEntry.grid(row=2, column=self.Column, padx=2, pady=2, sticky=NSEW)
        self.AttackModifierEntryStatModifierInst = StatModifier(self.AttackModifierEntry, "<Button-3>", "Left-click on an attack modifier to roll 1d20 with it.  Right-click to set a stat modifier.", "Attack Modifier",
                                                                Cursor="dotbox", Prefix=self.SaveTagPrefix + "AttackModifier", Suffix=str(self.Column))
        self.AttackModifierEntry.bind("<Button-1>", self.RollAttack)

    def RollAttack(self, event):
        try:
            DiceRollerInst.ModifierEntryVar.set(str(GlobalInst.GetStringVarAsNumber(self.AttackModifierEntryVar)))
        except ValueError:
            return
        DiceRollerInst.DiceNumberEntryVar.set(1)
        DiceRollerInst.DieTypeEntryVar.set(20)
        AttackTypeString = self.AbilityScoreSelectionDropdownVar.get()
        if self.AttackTypeStringSuffix != "":
            AttackTypeString += " " + self.AttackTypeStringSuffix
        DiceRollerInst.Roll(AttackTypeString + " Attack:\n")


class CreatureData:
    def __init__(self, master, DialogMode=False, DialogData=None):
        # Standalone and NPC Sheet Mode Variables
        if not DialogMode:
            self.NameEntryVar = SavedStringVar("NameEntryVar")
            self.SizeEntryVar = SavedStringVar("SizeEntryVar")
            self.TypeAndTagsEntryVar = SavedStringVar("TypeAndTagsEntryVar")
            self.AlignmentEntryVar = SavedStringVar("AlignmentEntryVar")
            self.ProficiencyEntryVar = SavedStringVar("ProficiencyEntryVar")
            self.TempHPEntryVar = SavedStringVar("TempHPEntryVar")
            self.CurrentHPEntryVar = SavedStringVar("CurrentHPEntryVar")
            self.MaxHPEntryVar = SavedStringVar("MaxHPEntryVar")
            self.ACEntryVar = SavedStringVar("ACEntryVar")
            self.SpeedEntryVar = SavedStringVar("SpeedEntryVar")
            self.CRAndExperienceEntryVar = SavedStringVar("CRAndExperienceEntryVar")
            self.AbilitiesStrengthEntryVar = SavedStringVar("AbilitiesStrengthEntryVar")
            self.AbilitiesDexterityEntryVar = SavedStringVar("AbilitiesDexterityEntryVar")
            self.AbilitiesConstitutionEntryVar = SavedStringVar("AbilitiesConstitutionEntryVar")
            self.AbilitiesIntelligenceEntryVar = SavedStringVar("AbilitiesIntelligenceEntryVar")
            self.AbilitiesWisdomEntryVar = SavedStringVar("AbilitiesWisdomEntryVar")
            self.AbilitiesCharismaEntryVar = SavedStringVar("AbilitiesCharismaEntryVar")
            if WindowInst.Mode == "NPCSheet":
                self.OpenErrors = False
                self.OpenErrorsString = ""

        # Dialog Mode Variables and Parameters
        else:
            # Store Parameters
            self.DialogData = DialogData

            # Variables
            self.DataSubmitted = BooleanVar()
            self.NameEntryVar = StringVar(value=self.DialogData["NameEntryVar"].get())
            self.SizeEntryVar = StringVar(value=self.DialogData["SizeEntryVar"].get())
            self.TypeAndTagsEntryVar = StringVar(value=self.DialogData["TypeAndTagsEntryVar"].get())
            self.AlignmentEntryVar = StringVar(value=self.DialogData["AlignmentEntryVar"].get())
            self.ProficiencyEntryVar = StringVar(value=self.DialogData["ProficiencyEntryVar"].get())
            self.TempHPEntryVar = StringVar(value=self.DialogData["TempHPEntryVar"].get())
            self.CurrentHPEntryVar = StringVar(value=self.DialogData["CurrentHPEntryVar"].get())
            self.MaxHPEntryVar = StringVar(value=self.DialogData["MaxHPEntryVar"].get())
            self.ACEntryVar = StringVar(value=self.DialogData["ACEntryVar"].get())
            self.SpeedEntryVar = StringVar(value=self.DialogData["SpeedEntryVar"].get())
            self.CRAndExperienceEntryVar = StringVar(value=self.DialogData["CRAndExperienceEntryVar"].get())
            self.AbilitiesStrengthEntryVar = StringVar(value=self.DialogData["AbilitiesStrengthEntryVar"].get())
            self.AbilitiesDexterityEntryVar = StringVar(value=self.DialogData["AbilitiesDexterityEntryVar"].get())
            self.AbilitiesConstitutionEntryVar = StringVar(value=self.DialogData["AbilitiesConstitutionEntryVar"].get())
            self.AbilitiesIntelligenceEntryVar = StringVar(value=self.DialogData["AbilitiesIntelligenceEntryVar"].get())
            self.AbilitiesWisdomEntryVar = StringVar(value=self.DialogData["AbilitiesWisdomEntryVar"].get())
            self.AbilitiesCharismaEntryVar = StringVar(value=self.DialogData["AbilitiesCharismaEntryVar"].get())
            self.SkillSensesAndLanguagesFieldVar = StringVar(value=self.DialogData["SkillSensesAndLanguagesFieldVar"].get())
            self.SavingThrowsFieldVar = StringVar(value=self.DialogData["SavingThrowsFieldVar"].get())
            self.VulnerabilitiesResistancesAndImmunitiesFieldVar = StringVar(value=self.DialogData["VulnerabilitiesResistancesAndImmunitiesFieldVar"].get())
            self.SpecialTraitsFieldVar = StringVar(value=self.DialogData["SpecialTraitsFieldVar"].get())
            self.ActionsFieldVar = StringVar(value=self.DialogData["ActionsFieldVar"].get())
            self.ReactionsFieldVar = StringVar(value=self.DialogData["ReactionsFieldVar"].get())
            self.InventoryFieldVar = StringVar(value=self.DialogData["InventoryFieldVar"].get())
            self.LegendaryActionsAndLairActionsFieldVar = StringVar(value=self.DialogData["LegendaryActionsAndLairActionsFieldVar"].get())
            self.NotesFieldVar = StringVar(value=self.DialogData["NotesFieldVar"].get())
            self.OpenErrors = False
            self.OpenErrorsString = ""

        # Create Window (Element)
        if not DialogMode:
            if WindowInst.Mode == "NPCSheet":
                self.CreatureDataFrame = LabelFrame(master, text="NPC Stats, Inventory, and Notes:")
            else:
                self.CreatureDataFrame = Frame(master)
            self.CreatureDataFrame.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
            self.WidgetMaster = self.CreatureDataFrame
        else:
            self.Window = Toplevel(master)
            self.Window.wm_attributes("-toolwindow", 1)
            self.Window.wm_title("Creature Stats")
            self.WidgetMaster = self.Window

        # Name Entry
        self.NameFrame = LabelFrame(self.WidgetMaster, text="Name:")
        self.NameFrame.grid_columnconfigure(0, weight=1)
        self.NameFrame.grid(row=0, column=0, columnspan=3, padx=2, pady=2, sticky=NSEW)
        self.NameEntry = EntryExtended(self.NameFrame, justify=CENTER, textvariable=self.NameEntryVar)
        self.NameEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Size, Type, Tags, Alignment, and Proficiency Frame
        self.SizeTypeTagsAlignmentAndProficiencyFrame = Frame(self.WidgetMaster)
        self.SizeTypeTagsAlignmentAndProficiencyFrame.grid_columnconfigure(0, weight=1)
        self.SizeTypeTagsAlignmentAndProficiencyFrame.grid_columnconfigure(1, weight=1)
        self.SizeTypeTagsAlignmentAndProficiencyFrame.grid_columnconfigure(2, weight=1)
        self.SizeTypeTagsAlignmentAndProficiencyFrame.grid(row=1, column=0, columnspan=3, sticky=NSEW)

        # Size
        self.SizeFrame = LabelFrame(self.SizeTypeTagsAlignmentAndProficiencyFrame, text="Size:")
        self.SizeFrame.grid_columnconfigure(0, weight=1)
        self.SizeFrame.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
        self.SizeEntry = EntryExtended(self.SizeFrame, justify=CENTER, textvariable=self.SizeEntryVar)
        self.SizeEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Type and Tags
        self.TypeAndTagsFrame = LabelFrame(self.SizeTypeTagsAlignmentAndProficiencyFrame, text="Type and Tags:")
        self.TypeAndTagsFrame.grid_columnconfigure(0, weight=1)
        self.TypeAndTagsFrame.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
        self.TypeAndTagsEntry = EntryExtended(self.TypeAndTagsFrame, justify=CENTER, textvariable=self.TypeAndTagsEntryVar)
        self.TypeAndTagsEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Alignment
        self.AlignmentFrame = LabelFrame(self.SizeTypeTagsAlignmentAndProficiencyFrame, text="Alignment:")
        self.AlignmentFrame.grid_columnconfigure(0, weight=1)
        self.AlignmentFrame.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
        self.AlignmentEntry = EntryExtended(self.AlignmentFrame, justify=CENTER, textvariable=self.AlignmentEntryVar)
        self.AlignmentEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Proficiency
        self.ProficiencyFrame = LabelFrame(self.SizeTypeTagsAlignmentAndProficiencyFrame, text="Proficiency Bonus:")
        self.ProficiencyFrame.grid_columnconfigure(0, weight=1)
        self.ProficiencyFrame.grid(row=0, column=3, sticky=NSEW, padx=2, pady=2)
        self.ProficiencyEntry = EntryExtended(self.ProficiencyFrame, justify=CENTER, width=5, textvariable=self.ProficiencyEntryVar, bg=GlobalInst.ButtonColor)
        self.ProficiencyEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # HP, AC, Speed, CR, and Experience Entries Frame
        self.HPACSpeedCRExperienceEntriesFrame = Frame(self.WidgetMaster)
        self.HPACSpeedCRExperienceEntriesFrame.grid(row=2, column=0, rowspan=2, sticky=NSEW)
        self.HPACSpeedCRExperienceEntriesFrame.grid_rowconfigure(2, weight=1)
        self.HPACSpeedCRExperienceEntriesFrame.grid_rowconfigure(4, weight=1)
        self.HPACSpeedCRExperienceEntriesFrame.grid_rowconfigure(6, weight=1)
        self.HPACSpeedCRExperienceEntriesFrame.grid_rowconfigure(8, weight=1)
        self.HPACSpeedCRExperienceEntriesFrame.grid_rowconfigure(10, weight=1)

        # Temp HP Entry
        self.TempHPFrame = LabelFrame(self.HPACSpeedCRExperienceEntriesFrame, text="Temp HP:")
        self.TempHPFrame.grid_columnconfigure(0, weight=1)
        self.TempHPFrame.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)
        self.TempHPEntry = EntryExtended(self.TempHPFrame, justify=CENTER, width=3, textvariable=self.TempHPEntryVar)
        self.TempHPEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Current HP Entry
        self.CurrentHPFrame = LabelFrame(self.HPACSpeedCRExperienceEntriesFrame, text="Current HP:")
        self.CurrentHPFrame.grid_columnconfigure(0, weight=1)
        self.CurrentHPFrame.grid(row=3, column=0, padx=2, pady=2, sticky=NSEW)
        self.CurrentHPEntry = EntryExtended(self.CurrentHPFrame, justify=CENTER, width=3, textvariable=self.CurrentHPEntryVar, bg=GlobalInst.ButtonColor)
        self.CurrentHPEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
        self.CurrentHPEntry.bind("<Button-3>", lambda event: self.Damage())
        self.CurrentHPEntry.bind("<Shift-Button-3>", lambda event: self.Heal())
        self.CurrentHPTooltip = Tooltip(self.CurrentHPEntry, "Right-click to damage.  Shift+right-click to heal.")

        # Max HP Entry
        self.MaxHPFrame = LabelFrame(self.HPACSpeedCRExperienceEntriesFrame, text="Max HP:")
        self.MaxHPFrame.grid_columnconfigure(0, weight=1)
        self.MaxHPFrame.grid(row=5, column=0, padx=2, pady=2, sticky=NSEW)
        self.MaxHPEntry = EntryExtended(self.MaxHPFrame, justify=CENTER, width=3, textvariable=self.MaxHPEntryVar)
        self.MaxHPEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # AC Entry
        self.ACFrame = LabelFrame(self.HPACSpeedCRExperienceEntriesFrame, text="AC:")
        self.ACFrame.grid_columnconfigure(0, weight=1)
        self.ACFrame.grid(row=7, column=0, padx=2, pady=2, sticky=NSEW)
        self.ACEntry = EntryExtended(self.ACFrame, justify=CENTER, width=3, textvariable=self.ACEntryVar)
        self.ACEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Speed
        self.SpeedFrame = LabelFrame(self.HPACSpeedCRExperienceEntriesFrame, text="Speed:")
        self.SpeedFrame.grid_columnconfigure(0, weight=1)
        self.SpeedFrame.grid(row=9, column=0, padx=2, pady=2, sticky=NSEW)
        self.SpeedEntry = EntryExtended(self.SpeedFrame, justify=CENTER, width=3, textvariable=self.SpeedEntryVar)
        self.SpeedEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # CR and Experience
        self.CRAndExperienceFrame = LabelFrame(self.HPACSpeedCRExperienceEntriesFrame, text="CR and Exp.:")
        self.CRAndExperienceFrame.grid_columnconfigure(0, weight=1)
        self.CRAndExperienceFrame.grid(row=11, column=0, padx=2, pady=2, sticky=NSEW)
        self.CRAndExperienceEntry = EntryExtended(self.CRAndExperienceFrame, justify=CENTER, width=3, textvariable=self.CRAndExperienceEntryVar)
        self.CRAndExperienceEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Abilities
        self.AbilitiesFrame = LabelFrame(self.WidgetMaster, text="Ability Score Modifiers:")
        self.AbilitiesFrame.grid_columnconfigure(0, weight=1)
        self.AbilitiesFrame.grid_columnconfigure(1, weight=1)
        self.AbilitiesFrame.grid_columnconfigure(2, weight=1)
        self.AbilitiesFrame.grid_rowconfigure(1, weight=1)
        self.AbilitiesFrame.grid_rowconfigure(3, weight=1)
        self.AbilitiesFrame.grid(row=2, column=1, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesStrengthHeader = Label(self.AbilitiesFrame, text="STR", bd=2, relief=GROOVE)
        self.AbilitiesStrengthHeader.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesStrengthEntry = EntryExtended(self.AbilitiesFrame, justify=CENTER, width=5, textvariable=self.AbilitiesStrengthEntryVar, bg=GlobalInst.ButtonColor)
        self.AbilitiesStrengthEntry.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesDexterityHeader = Label(self.AbilitiesFrame, text="DEX", bd=2, relief=GROOVE)
        self.AbilitiesDexterityHeader.grid(row=0, column=1, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesDexterityEntry = EntryExtended(self.AbilitiesFrame, justify=CENTER, width=5, textvariable=self.AbilitiesDexterityEntryVar, bg=GlobalInst.ButtonColor)
        self.AbilitiesDexterityEntry.grid(row=1, column=1, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesConstitutionHeader = Label(self.AbilitiesFrame, text="CON", bd=2, relief=GROOVE)
        self.AbilitiesConstitutionHeader.grid(row=0, column=2, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesConstitutionEntry = EntryExtended(self.AbilitiesFrame, justify=CENTER, width=5, textvariable=self.AbilitiesConstitutionEntryVar, bg=GlobalInst.ButtonColor)
        self.AbilitiesConstitutionEntry.grid(row=1, column=2, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesIntelligenceHeader = Label(self.AbilitiesFrame, text="INT", bd=2, relief=GROOVE)
        self.AbilitiesIntelligenceHeader.grid(row=2, column=0, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesIntelligenceEntry = EntryExtended(self.AbilitiesFrame, justify=CENTER, width=5, textvariable=self.AbilitiesIntelligenceEntryVar, bg=GlobalInst.ButtonColor)
        self.AbilitiesIntelligenceEntry.grid(row=3, column=0, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesWisdomHeader = Label(self.AbilitiesFrame, text="WIS", bd=2, relief=GROOVE)
        self.AbilitiesWisdomHeader.grid(row=2, column=1, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesWisdomEntry = EntryExtended(self.AbilitiesFrame, justify=CENTER, width=5, textvariable=self.AbilitiesWisdomEntryVar, bg=GlobalInst.ButtonColor)
        self.AbilitiesWisdomEntry.grid(row=3, column=1, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesCharismaHeader = Label(self.AbilitiesFrame, text="CHA", bd=2, relief=GROOVE)
        self.AbilitiesCharismaHeader.grid(row=2, column=2, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesCharismaEntry = EntryExtended(self.AbilitiesFrame, justify=CENTER, width=5, textvariable=self.AbilitiesCharismaEntryVar, bg=GlobalInst.ButtonColor)
        self.AbilitiesCharismaEntry.grid(row=3, column=2, padx=2, pady=2, sticky=NSEW)

        # Mouse Wheel Configuration
        for EntryWidget in [self.AbilitiesStrengthEntry, self.AbilitiesDexterityEntry, self.AbilitiesConstitutionEntry, self.AbilitiesIntelligenceEntry, self.AbilitiesWisdomEntry, self.AbilitiesCharismaEntry,
                            self.ProficiencyEntry]:
            self.EntryTooltip = Tooltip(EntryWidget, "Scroll the mouse wheel or type to change the modifier.")

        if GlobalInst.OS == "Windows" or GlobalInst.OS == "Darwin":
            self.AbilitiesStrengthEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.AbilitiesStrengthEntryVar))
            self.AbilitiesDexterityEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.AbilitiesDexterityEntryVar))
            self.AbilitiesConstitutionEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.AbilitiesConstitutionEntryVar))
            self.AbilitiesIntelligenceEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.AbilitiesIntelligenceEntryVar))
            self.AbilitiesWisdomEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.AbilitiesWisdomEntryVar))
            self.AbilitiesCharismaEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.AbilitiesCharismaEntryVar))
            self.ProficiencyEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.ProficiencyEntryVar))
        elif GlobalInst.OS == "Linux":
            self.AbilitiesStrengthEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.AbilitiesStrengthEntryVar))
            self.AbilitiesStrengthEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.AbilitiesStrengthEntryVar))
            self.AbilitiesDexterityEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.AbilitiesDexterityEntryVar))
            self.AbilitiesDexterityEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.AbilitiesDexterityEntryVar))
            self.AbilitiesConstitutionEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.AbilitiesConstitutionEntryVar))
            self.AbilitiesConstitutionEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.AbilitiesConstitutionEntryVar))
            self.AbilitiesIntelligenceEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.AbilitiesIntelligenceEntryVar))
            self.AbilitiesIntelligenceEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.AbilitiesIntelligenceEntryVar))
            self.AbilitiesWisdomEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.AbilitiesWisdomEntryVar))
            self.AbilitiesWisdomEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.AbilitiesWisdomEntryVar))
            self.AbilitiesCharismaEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.AbilitiesCharismaEntryVar))
            self.AbilitiesCharismaEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.AbilitiesCharismaEntryVar))
            self.ProficiencyEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.ProficiencyEntryVar))
            self.ProficiencyEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.ProficiencyEntryVar))

        # Proficiency Entry Validation
        self.ProficiencyEntry.ConfigureValidation(lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Proficiency must be a whole number."), "key")

        # Ability Entry Validation
        for AbilityEntryWidget in [self.AbilitiesStrengthEntry, self.AbilitiesDexterityEntry, self.AbilitiesConstitutionEntry, self.AbilitiesIntelligenceEntry, self.AbilitiesWisdomEntry, self.AbilitiesCharismaEntry]:
            AbilityEntryWidget.ConfigureValidation(lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Ability modifiers must be whole numbers."), "key")

        # NPC Sheet Auto Calculation
        if WindowInst.Mode == "NPCSheet":
            self.ProficiencyEntryVar.trace_add("write", lambda a, b, c: self.UpdateStats())
            for AbilityEntryVar in [self.AbilitiesStrengthEntryVar, self.AbilitiesDexterityEntryVar, self.AbilitiesConstitutionEntryVar, self.AbilitiesIntelligenceEntryVar, self.AbilitiesWisdomEntryVar,
                                    self.AbilitiesCharismaEntryVar]:
                AbilityEntryVar.trace_add("write", lambda a, b, c: self.UpdateStats())

        # Skills, Senses, and Languages
        self.SkillSensesAndLanguagesFrame = LabelFrame(self.WidgetMaster, text="Skills, Senses, and Languages:")
        self.SkillSensesAndLanguagesFrame.grid(row=3, column=1, padx=2, pady=2, sticky=NSEW)
        self.SkillSensesAndLanguagesField = ScrolledText(self.SkillSensesAndLanguagesFrame, Width=300, Height=120, SavedDataTag="SkillSensesAndLanguagesFieldVar" if not DialogMode else None)
        self.SkillSensesAndLanguagesField.grid(row=0, column=0)

        # Special Traits
        self.SpecialTraitsFrame = LabelFrame(self.WidgetMaster, text="Special Traits:")
        self.SpecialTraitsFrame.grid(row=2, column=2, padx=2, pady=2, sticky=NSEW)
        self.SpecialTraitsField = ScrolledText(self.SpecialTraitsFrame, Width=383, Height=120, SavedDataTag="SpecialTraitsFieldVar" if not DialogMode else None)
        self.SpecialTraitsField.grid(row=0, column=0)

        # Actions
        self.ActionsFrame = LabelFrame(self.WidgetMaster, text="Actions:")
        self.ActionsFrame.grid(row=3, column=2, padx=2, pady=2, sticky=NSEW)
        self.ActionsField = ScrolledText(self.ActionsFrame, Width=383, Height=120, SavedDataTag="ActionsFieldVar" if not DialogMode else None)
        self.ActionsField.grid(row=0, column=0)

        # Saving Throws
        self.SavingThrowsFrame = LabelFrame(self.WidgetMaster, text="Saving Throws:")
        self.SavingThrowsFrame.grid(row=4, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
        self.SavingThrowsField = ScrolledText(self.SavingThrowsFrame, Width=383, Height=75, SavedDataTag="SavingThrowsFieldVar" if not DialogMode else None)
        self.SavingThrowsField.grid(row=0, column=0)

        # Vulnerabilities, Resistances, and Immunities
        self.VulnerabilitiesResistancesAndImmunitiesFrame = LabelFrame(self.WidgetMaster, text="Vulnerabilities, Resistances, and Immunities:")
        self.VulnerabilitiesResistancesAndImmunitiesFrame.grid(row=5, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
        self.VulnerabilitiesResistancesAndImmunitiesField = ScrolledText(self.VulnerabilitiesResistancesAndImmunitiesFrame, Width=383, Height=75,
                                                                         SavedDataTag="VulnerabilitiesResistancesAndImmunitiesFieldVar" if not DialogMode else None)
        self.VulnerabilitiesResistancesAndImmunitiesField.grid(row=0, column=0)

        # Inventory
        self.InventoryFrame = LabelFrame(self.WidgetMaster, text="Inventory:")
        self.InventoryFrame.grid(row=6, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
        self.InventoryField = ScrolledText(self.InventoryFrame, Width=383, Height=75, SavedDataTag="InventoryFieldVar" if not DialogMode else None)
        self.InventoryField.grid(row=0, column=0)

        # Reactions
        self.ReactionsFrame = LabelFrame(self.WidgetMaster, text="Reactions:")
        self.ReactionsFrame.grid(row=4, column=2, padx=2, pady=2, sticky=NSEW)
        self.ReactionsField = ScrolledText(self.ReactionsFrame, Width=383, Height=75, SavedDataTag="ReactionsFieldVar" if not DialogMode else None)
        self.ReactionsField.grid(row=0, column=0)

        # Legendary Actions and Lair Actions
        self.LegendaryActionsAndLairActionsFrame = LabelFrame(self.WidgetMaster, text="Legendary Actions and Lair Actions:")
        self.LegendaryActionsAndLairActionsFrame.grid(row=5, column=2, padx=2, pady=2, sticky=NSEW)
        self.LegendaryActionsAndLairActionsField = ScrolledText(self.LegendaryActionsAndLairActionsFrame, Width=383, Height=75, SavedDataTag="LegendaryActionsAndLairActionsFieldVar" if not DialogMode else None)
        self.LegendaryActionsAndLairActionsField.grid(row=0, column=0)

        # Notes
        self.NotesFrame = LabelFrame(self.WidgetMaster, text="Notes:")
        self.NotesFrame.grid(row=6, column=2, padx=2, pady=2, sticky=NSEW)
        self.NotesField = ScrolledText(self.NotesFrame, Width=383, Height=75, SavedDataTag="NotesFieldVar" if not DialogMode else None)
        self.NotesField.grid(row=0, column=0)

        # Create Creature Stats Fields Dictionary
        if DialogMode or WindowInst.Mode == "NPCSheet":
            self.CreatureStatsFields = {}
            self.CreatureStatsFields["NameEntryVar"] = self.NameEntryVar
            self.CreatureStatsFields["ACEntryVar"] = self.ACEntryVar
            self.CreatureStatsFields["TempHPEntryVar"] = self.TempHPEntryVar
            self.CreatureStatsFields["CurrentHPEntryVar"] = self.CurrentHPEntryVar
            self.CreatureStatsFields["MaxHPEntryVar"] = self.MaxHPEntryVar
            self.CreatureStatsFields["SizeEntryVar"] = self.SizeEntryVar
            self.CreatureStatsFields["TypeAndTagsEntryVar"] = self.TypeAndTagsEntryVar
            self.CreatureStatsFields["AlignmentEntryVar"] = self.AlignmentEntryVar
            self.CreatureStatsFields["ProficiencyEntryVar"] = self.ProficiencyEntryVar
            self.CreatureStatsFields["SpeedEntryVar"] = self.SpeedEntryVar
            self.CreatureStatsFields["CRAndExperienceEntryVar"] = self.CRAndExperienceEntryVar
            self.CreatureStatsFields["AbilitiesStrengthEntryVar"] = self.AbilitiesStrengthEntryVar
            self.CreatureStatsFields["AbilitiesDexterityEntryVar"] = self.AbilitiesDexterityEntryVar
            self.CreatureStatsFields["AbilitiesConstitutionEntryVar"] = self.AbilitiesConstitutionEntryVar
            self.CreatureStatsFields["AbilitiesIntelligenceEntryVar"] = self.AbilitiesIntelligenceEntryVar
            self.CreatureStatsFields["AbilitiesWisdomEntryVar"] = self.AbilitiesWisdomEntryVar
            self.CreatureStatsFields["AbilitiesCharismaEntryVar"] = self.AbilitiesCharismaEntryVar
            self.CreatureStatsFields["SkillSensesAndLanguagesFieldVar"] = self.SkillSensesAndLanguagesField
            self.CreatureStatsFields["SavingThrowsFieldVar"] = self.SavingThrowsField
            self.CreatureStatsFields["VulnerabilitiesResistancesAndImmunitiesFieldVar"] = self.VulnerabilitiesResistancesAndImmunitiesField
            self.CreatureStatsFields["SpecialTraitsFieldVar"] = self.SpecialTraitsField
            self.CreatureStatsFields["ActionsFieldVar"] = self.ActionsField
            self.CreatureStatsFields["ReactionsFieldVar"] = self.ReactionsField
            self.CreatureStatsFields["InventoryFieldVar"] = self.InventoryField
            self.CreatureStatsFields["LegendaryActionsAndLairActionsFieldVar"] = self.LegendaryActionsAndLairActionsField
            self.CreatureStatsFields["NotesFieldVar"] = self.NotesField

        # Additional Dialog Setup
        if DialogMode:
            # Buttons Frame
            self.ButtonsFrame = Frame(self.WidgetMaster)
            self.ButtonsFrame.grid_columnconfigure(0, weight=4)
            self.ButtonsFrame.grid_columnconfigure(1, weight=1)
            self.ButtonsFrame.grid_columnconfigure(2, weight=1)
            self.ButtonsFrame.grid_columnconfigure(3, weight=1)
            self.ButtonsFrame.grid(row=7, column=0, columnspan=3, sticky=NSEW)

            # Submit Button
            self.SubmitButton = Button(self.ButtonsFrame, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
            self.SubmitButton.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

            # Import Button
            self.ImportButton = Button(self.ButtonsFrame, text="Import", command=self.Import, bg=GlobalInst.ButtonColor)
            self.ImportButton.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)

            # Export Button
            self.ExportButton = Button(self.ButtonsFrame, text="Export", command=self.Export, bg=GlobalInst.ButtonColor)
            self.ExportButton.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)

            # Cancel Button
            self.CancelButton = Button(self.ButtonsFrame, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
            self.CancelButton.grid(row=0, column=3, sticky=NSEW, padx=2, pady=2)

            # Set Text Field Data
            self.SkillSensesAndLanguagesField.set(self.SkillSensesAndLanguagesFieldVar.get())
            self.SavingThrowsField.set(self.SavingThrowsFieldVar.get())
            self.VulnerabilitiesResistancesAndImmunitiesField.set(self.VulnerabilitiesResistancesAndImmunitiesFieldVar.get())
            self.SpecialTraitsField.set(self.SpecialTraitsFieldVar.get())
            self.ActionsField.set(self.ActionsFieldVar.get())
            self.ReactionsField.set(self.ReactionsFieldVar.get())
            self.InventoryField.set(self.InventoryFieldVar.get())
            self.LegendaryActionsAndLairActionsField.set(self.LegendaryActionsAndLairActionsFieldVar.get())
            self.NotesField.set(self.NotesFieldVar.get())

            # Prevent Main Window Input
            self.Window.grab_set()

            # Handle Config Window Geometry and Focus
            GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst)
            self.Window.focus_force()

            # Focus on Name Entry
            self.NameEntry.focus_set()

    def Damage(self):
        if self.ValidLifeValues():
            pass
        else:
            return
        CurrentTempHP = GlobalInst.GetStringVarAsNumber(self.TempHPEntryVar)
        CurrentHPString = self.CurrentHPEntryVar.get()
        if CurrentHPString == "" or CurrentHPString == "+" or CurrentHPString == "-":
            CurrentHP = GlobalInst.GetStringVarAsNumber(self.MaxHPEntryVar)
        else:
            CurrentHP = GlobalInst.GetStringVarAsNumber(self.CurrentHPEntryVar)
        DamagePrompt = IntegerPrompt(WindowInst, "Damage", "How much damage?", MinValue=0)
        WindowInst.wait_window(DamagePrompt.Window)
        if DamagePrompt.DataSubmitted.get():
            Damage = DamagePrompt.GetData()
        else:
            return
        if CurrentTempHP == 0:
            self.CurrentHPEntryVar.set(str(CurrentHP - Damage))
        elif CurrentTempHP >= 1:
            if CurrentTempHP < Damage:
                Damage -= CurrentTempHP
                self.TempHPEntryVar.set(str(0))
                self.CurrentHPEntryVar.set(str(CurrentHP - Damage))
            elif CurrentTempHP >= Damage:
                self.TempHPEntryVar.set(str(CurrentTempHP - Damage))

    def Heal(self):
        if self.ValidLifeValues():
            pass
        else:
            return
        CurrentHP = GlobalInst.GetStringVarAsNumber(self.CurrentHPEntryVar)
        MaxHP = GlobalInst.GetStringVarAsNumber(self.MaxHPEntryVar)
        HealingPrompt = IntegerPrompt(WindowInst, "Heal", "How much healing?", MinValue=0)
        WindowInst.wait_window(HealingPrompt.Window)
        if HealingPrompt.DataSubmitted.get():
            Healing = HealingPrompt.GetData()
        else:
            return
        HealedValue = Healing + max(CurrentHP, 0)
        if HealedValue > MaxHP:
            self.CurrentHPEntryVar.set(str(MaxHP))
        elif HealedValue <= MaxHP:
            self.CurrentHPEntryVar.set(str(HealedValue))

    def ValidLifeValues(self):
        try:
            TempHP = GlobalInst.GetStringVarAsNumber(self.TempHPEntryVar)
            CurrentHP = GlobalInst.GetStringVarAsNumber(self.CurrentHPEntryVar)
            MaxHP = GlobalInst.GetStringVarAsNumber(self.MaxHPEntryVar)
        except:
            messagebox.showerror("Invalid Entry", "HP values must be whole numbers.")
            return False
        if TempHP < 0 or MaxHP < 1:
            messagebox.showerror("Invalid Entry", "Temp HP cannot be negative and max HP must be positive.")
            return False
        return True

    def UpdateStats(self):
        # Calculate Preset Roll Modifiers
        for Entry in Inst["PresetRolls"].PresetRollsList:
            CalculatedModifierString = Entry.PresetRollModifierEntryStatModifierInst.GetPresetDiceRollModifier()
            CurrentModifierString = Entry.PresetRollModifierEntryVar.get()
            if CalculatedModifierString not in ["", CurrentModifierString]:
                Entry.PresetRollModifierEntryVar.set(CalculatedModifierString)

    def MouseWheelEvent(self, event, EntryVar, MinValue=None, MaxValue=None):
        try:
            OldValue = GlobalInst.GetStringVarAsNumber(EntryVar)
        except ValueError:
            OldValue = 0
        if event.delta > 0:
            ScrollDistance = 1
        elif event.delta < 0:
            ScrollDistance = -1
        else:
            ScrollDistance = 0
        NewValue = OldValue + ScrollDistance
        if MinValue != None:
            NewValue = max(MinValue, NewValue)
        if MaxValue != None:
            NewValue = min(MaxValue, NewValue)
        if NewValue > 0:
            PositivePrefix = "+"
        else:
            PositivePrefix = ""
        EntryVar.set(PositivePrefix + str(NewValue))

    def Submit(self):
        self.DataSubmitted.set(True)
        self.SkillSensesAndLanguagesFieldVar.set(self.SkillSensesAndLanguagesField.get())
        self.SavingThrowsFieldVar.set(self.SavingThrowsField.get())
        self.VulnerabilitiesResistancesAndImmunitiesFieldVar.set(self.VulnerabilitiesResistancesAndImmunitiesField.get())
        self.SpecialTraitsFieldVar.set(self.SpecialTraitsField.get())
        self.ActionsFieldVar.set(self.ActionsField.get())
        self.ReactionsFieldVar.set(self.ReactionsField.get())
        self.InventoryFieldVar.set(self.InventoryField.get())
        self.LegendaryActionsAndLairActionsFieldVar.set(self.LegendaryActionsAndLairActionsField.get())
        self.NotesFieldVar.set(self.NotesField.get())
        self.CreatureStatsFields["SkillSensesAndLanguagesFieldVar"] = self.SkillSensesAndLanguagesFieldVar
        self.CreatureStatsFields["SavingThrowsFieldVar"] = self.SavingThrowsFieldVar
        self.CreatureStatsFields["VulnerabilitiesResistancesAndImmunitiesFieldVar"] = self.VulnerabilitiesResistancesAndImmunitiesFieldVar
        self.CreatureStatsFields["SpecialTraitsFieldVar"] = self.SpecialTraitsFieldVar
        self.CreatureStatsFields["ActionsFieldVar"] = self.ActionsFieldVar
        self.CreatureStatsFields["ReactionsFieldVar"] = self.ReactionsFieldVar
        self.CreatureStatsFields["InventoryFieldVar"] = self.InventoryFieldVar
        self.CreatureStatsFields["LegendaryActionsAndLairActionsFieldVar"] = self.LegendaryActionsAndLairActionsFieldVar
        self.CreatureStatsFields["NotesFieldVar"] = self.NotesFieldVar
        self.Window.destroy()

    def Import(self):
        StatusBarInst.StatusBarSetText("Importing creature file...", Lock=True)
        OpenFileName = filedialog.askopenfilename(filetypes=(("Creature file", "*.crea"), ("All files", "*.*")), defaultextension=".crea", title="Import Creature File")
        TextFileName = "Creature Data.txt"
        if OpenFileName != "":
            with ZipFile(OpenFileName, mode="r") as OpenFile:
                with open(OpenFile.extract(TextFileName), mode="r") as TextFile:
                    self.ImportCreatureData(TextFile)
            SavingAndOpeningInst.DeleteFile(TextFileName)
            sleep(0.5)
            if self.OpenErrors:
                OpenErrorsPromptInst = OpenErrorsPrompt(WindowInst, self.OpenErrorsString[:-1])
                WindowInst.wait_window(OpenErrorsPromptInst.Window)
                self.OpenErrors = False
                self.OpenErrorsString = ""
            StatusBarInst.FlashStatus("Imported file:  " + os.path.basename(OpenFileName))
        else:
            StatusBarInst.FlashStatus("No file imported!")

    def ImportCreatureData(self, File):
        for Line in File:
            if Line != "":
                LoadedLine = json.loads(Line)
                for Tag, Field in LoadedLine.items():
                    try:
                        self.CreatureStatsFields[Tag].set(Field)
                    except KeyError:
                        self.OpenErrors = True
                        self.OpenErrorsString += Line

    def Export(self):
        StatusBarInst.StatusBarSetText("Exporting creature file...", Lock=True)
        SaveFileName = filedialog.asksaveasfilename(filetypes=(("Creature file", "*.crea"), ("All files", "*.*")), defaultextension=".crea", title="Export Creature File")
        TextFileName = "Creature Data.txt"
        if SaveFileName != "":
            with ZipFile(SaveFileName, mode="w") as SaveFile:
                with open(TextFileName, mode="w") as TextFile:
                    self.ExportCreatureData(TextFile)
                SaveFile.write(TextFileName)
            SavingAndOpeningInst.DeleteFile(TextFileName)
            sleep(0.5)
            StatusBarInst.FlashStatus("File saved as:  " + os.path.basename(SaveFileName))
        else:
            StatusBarInst.FlashStatus("No file saved!")

    def ExportCreatureData(self, File):
        for Tag, Field in self.CreatureStatsFields.items():
            File.write(json.dumps({Tag: Field.get()}) + "\n")

    def Cancel(self):
        self.DataSubmitted.set(False)
        self.Window.destroy()


class DiceRoller:
    def __init__(self, master):
        # Configure Mode Parameters
        if WindowInst.Mode == "DiceRoller":
            self.Row = 0
            self.Column = 0
            self.RowSpan = 1
            self.DiceEntryAndButtonsFrameColumnSpan = 2
            self.ResultsFieldFrameColumn = 1
            self.ResultsFieldWidth = 200
            self.ResultsFieldHeight = 258
            self.PresetRollsFrameRow = 2
            self.PresetRollsScrolledCanvasHeight = 262
            self.PresetRollsScrolledCanvasWidth = 418
        elif WindowInst.Mode == "EncounterManager":
            self.Row = 0
            self.Column = 1
            self.RowSpan = 2
            self.DiceEntryAndButtonsFrameColumnSpan = 1
            self.ResultsFieldFrameColumn = 0
            self.ResultsFieldWidth = 431
            self.ResultsFieldHeight = 154
            self.PresetRollsFrameRow = 3
            self.PresetRollsScrolledCanvasHeight = 405
            self.PresetRollsScrolledCanvasWidth = 418
        elif WindowInst.Mode == "CharacterSheet":
            self.Row = 0
            self.Column = 1
            self.RowSpan = 1
            self.DiceEntryAndButtonsFrameColumnSpan = 1
            self.ResultsFieldFrameColumn = 0
            self.ResultsFieldWidth = 436
            self.ResultsFieldHeight = 148
            self.PresetRollsFrameRow = 3
            self.PresetRollsScrolledCanvasHeight = 288
            self.PresetRollsScrolledCanvasWidth = 423
        elif WindowInst.Mode == "NPCSheet":
            self.Row = 0
            self.Column = 1
            self.RowSpan = 1
            self.DiceEntryAndButtonsFrameColumnSpan = 1
            self.ResultsFieldFrameColumn = 0
            self.ResultsFieldWidth = 436
            self.ResultsFieldHeight = 148
            self.PresetRollsFrameRow = 3
            self.PresetRollsScrolledCanvasHeight = 402
            self.PresetRollsScrolledCanvasWidth = 423

        # Variables
        self.DiceNumberEntryVar = StringVar(value="1")
        self.DieTypeEntryVar = StringVar(value="20")
        self.ModifierEntryVar = StringVar(value="0")
        self.CritMinimumEntryVar = SavedStringVar("CritMinimumEntryVar", DefaultValue="20")
        if WindowInst.Mode == "CharacterSheet":
            self.InspirationBoxVar = SavedBooleanVar("InspirationBoxVar")
            self.InspirationTrueColor = "#7aff63"
            self.InspirationFalseColor = GlobalInst.ButtonColor

        # Dice Roller Frame
        if WindowInst.Mode == "DiceRoller":
            self.DiceRollerFrame = Frame(master)
        else:
            self.DiceRollerFrame = LabelFrame(master, text="Dice Roller:")
        self.DiceRollerFrame.grid(row=self.Row, column=self.Column, rowspan=self.RowSpan, padx=2, pady=2, sticky=NSEW)

        # Dice Entry and Buttons Frame
        self.DiceEntryAndButtonsFrame = Frame(self.DiceRollerFrame)
        self.DiceEntryAndButtonsFrame.grid_columnconfigure(0, weight=1)
        self.DiceEntryAndButtonsFrame.grid_columnconfigure(2, weight=1)
        self.DiceEntryAndButtonsFrame.grid_columnconfigure(4, weight=1)
        self.DiceEntryAndButtonsFrame.grid(row=0, column=0, columnspan=self.DiceEntryAndButtonsFrameColumnSpan, sticky=NSEW)

        # Dice Entry Font
        self.DiceEntryFont = font.Font(size=18)

        # Number of Dice
        self.DiceNumberEntry = EntryExtended(self.DiceEntryAndButtonsFrame, textvariable=self.DiceNumberEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor, font=self.DiceEntryFont)
        self.DiceNumberEntry.ConfigureValidation(lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Dice number must be a whole number.", MinValue=1, LessThanMinString="Dice number cannot be less than 1."), "key")
        self.DiceNumberEntry.grid(row=0, column=0, rowspan=2, padx=2, pady=2, sticky=NSEW)
        self.DiceNumberTooltip = Tooltip(self.DiceNumberEntry, "Scroll the mouse wheel or type to change the number of dice.")

        # Die Type
        self.DieTypeLabel = Label(self.DiceEntryAndButtonsFrame, text="d", font=self.DiceEntryFont)
        self.DieTypeLabel.grid(row=0, column=1, rowspan=2, sticky=NSEW)
        self.DieTypeEntry = EntryExtended(self.DiceEntryAndButtonsFrame, textvariable=self.DieTypeEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor, font=self.DiceEntryFont)
        self.DieTypeEntry.ConfigureValidation(lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Die type must be a whole number.", MinValue=1, LessThanMinString="Die type cannot be less than 1."), "key")
        self.DieTypeEntry.grid(row=0, column=2, rowspan=2, padx=2, pady=2, sticky=NSEW)
        self.DieTypeTooltip = Tooltip(self.DieTypeEntry, "Scroll the mouse wheel or type to change the die type.")

        # Modifier
        self.ModifierLabel = Label(self.DiceEntryAndButtonsFrame, text="+", font=self.DiceEntryFont)
        self.ModifierLabel.grid(row=0, column=3, rowspan=2, sticky=NSEW)
        self.ModifierEntry = EntryExtended(self.DiceEntryAndButtonsFrame, textvariable=self.ModifierEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor, font=self.DiceEntryFont)
        self.ModifierEntry.ConfigureValidation(lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Modifier must be a whole number."), "key")
        self.ModifierEntry.grid(row=0, column=4, rowspan=2, padx=2, pady=2, sticky=NSEW)
        self.ModifierTooltip = Tooltip(self.ModifierEntry, "Scroll the mouse wheel or type to change the modifier.")

        # Die Steps
        self.DieStep = {}
        self.DieTypes = [4, 6, 8, 10, 12, 20, 100]
        self.DieTypesLength = len(self.DieTypes)
        for CurrentIndex in range(self.DieTypesLength):
            self.DieStep[str(self.DieTypes[CurrentIndex])] = (self.DieTypes[max(0, CurrentIndex - 1)], self.DieTypes[min(self.DieTypesLength - 1, CurrentIndex + 1)])

        # Mouse Wheel Bindings
        if GlobalInst.OS == "Windows" or GlobalInst.OS == "Darwin":
            self.DiceNumberEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.DiceNumberEntryVar, MinValue=1))
            self.DieTypeEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.DieTypeEntryVar, MinValue=1, DieStep=True))
            self.ModifierEntry.bind("<MouseWheel>", lambda event: self.MouseWheelEvent(event, self.ModifierEntryVar))
        elif GlobalInst.OS == "Linux":
            self.DiceNumberEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.DiceNumberEntryVar, MinValue=1))
            self.DiceNumberEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.DiceNumberEntryVar, MinValue=1))
            self.DieTypeEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.DieTypeEntryVar, MinValue=1, DieStep=True))
            self.DieTypeEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.DieTypeEntryVar, MinValue=1, DieStep=True))
            self.ModifierEntry.bind("<Button-4>", lambda event: self.MouseWheelEvent(event, self.ModifierEntryVar))
            self.ModifierEntry.bind("<Button-5>", lambda event: self.MouseWheelEvent(event, self.ModifierEntryVar))

        # Roll Button
        self.RollButtonFont = font.Font(size=16)
        self.RollButton = Button(self.DiceEntryAndButtonsFrame, text="Roll", command=self.Roll, width=7, bg=GlobalInst.ButtonColor, font=self.RollButtonFont)
        self.RollButton.grid(row=0, column=5, padx=2, pady=2, sticky=NSEW, rowspan=2)

        # Average Roll Button
        self.AverageRollButton = Button(self.DiceEntryAndButtonsFrame, text="Avg. Roll", command=self.AverageRoll, width=7, bg=GlobalInst.ButtonColor)
        self.AverageRollButton.grid(row=0, column=6, padx=2, pady=2, sticky=NSEW)

        # Crit Minimum
        self.CritMinimumFrame = LabelFrame(self.DiceEntryAndButtonsFrame, text="Crit Min:")
        self.CritMinimumFrame.grid_columnconfigure(0, weight=1)
        self.CritMinimumFrame.grid(row=1, column=6, padx=2, pady=2, sticky=NSEW)
        self.CritMinimumEntry = EntryExtended(self.CritMinimumFrame, textvariable=self.CritMinimumEntryVar, justify=CENTER, width=5)
        self.CritMinimumEntry.ConfigureValidation(
            lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Crit minimum must be a whole number.", MinValue=1, LessThanMinString="Crit minimum cannot be less than 1.", MaxValue=20,
                                                                MoreThanMaxString="Crit minimum cannot be more than 20."), "key")
        self.CritMinimumEntry.grid(row=0, column=0, sticky=NSEW)

        # Results
        self.ResultsFieldFrame = LabelFrame(self.DiceRollerFrame, text="Results:")
        self.ResultsFieldFrame.grid(row=2, column=self.ResultsFieldFrameColumn, padx=2, pady=2)
        self.ResultsField = ScrolledText(self.ResultsFieldFrame, Width=self.ResultsFieldWidth, Height=self.ResultsFieldHeight, Disabled=True, DisabledBackground=GlobalInst.ButtonColor, SavedDataTag="ResultsField")
        self.ResultsField.grid(row=0, column=0, padx=2, pady=2)
        self.ResultsField.Text.bind("<Button-1>", self.CopyResults)
        self.ResultsField.Text.bind("<Button-3>", self.ClearResults)
        self.ResultsFieldTooltip = Tooltip(self.ResultsField.ScrolledTextFrame, "Left-click to copy results to the clipboard.  Right-click to clear.")

        # Preset Rolls
        self.PresetRollsInst = self.PresetRolls(self.DiceRollerFrame, self.ResultsField, self.CritMinimumEntryVar, self.PresetRollsFrameRow, self.PresetRollsScrolledCanvasHeight, self.PresetRollsScrolledCanvasWidth)
        Inst["PresetRolls"] = self.PresetRollsInst

        # Inspiration Box
        if WindowInst.Mode == "CharacterSheet":
            # Inspiration Box Font
            self.InspirationBoxFont = font.Font(size=16)

            # Box
            self.InspirationBox = Checkbutton(self.DiceRollerFrame, text="Inspiration", variable=self.InspirationBoxVar, font=self.InspirationBoxFont, indicatoron=False, background=self.InspirationFalseColor,
                                              selectcolor=self.InspirationTrueColor)
            self.InspirationBox.grid(row=4, column=0, padx=2, pady=2, sticky=NSEW)

    def UpdateResultsField(self, UpdateText):
        CurrentText = self.ResultsField.get()
        if CurrentText != "":
            UpdateText += ("\n") * 2
        NewText = UpdateText + CurrentText
        self.ResultsField.set(NewText)

    def Roll(self, DescriptorText=""):
        if self.ValidDiceEntry():
            pass
        else:
            return
        CurrentRoll = 1
        Result = 0
        CritSuccess = False
        CritFailure = False
        IndividualRolls = ""
        DiceNumber = GlobalInst.GetStringVarAsNumber(self.DiceNumberEntryVar)
        DieType = GlobalInst.GetStringVarAsNumber(self.DieTypeEntryVar)
        Modifier = GlobalInst.GetStringVarAsNumber(self.ModifierEntryVar)
        while CurrentRoll <= DiceNumber:
            CurrentRollResult = random.randint(1, DieType)
            if CurrentRoll < DiceNumber:
                IndividualRolls += str(CurrentRollResult) + "+"
            elif CurrentRoll == DiceNumber:
                IndividualRolls += str(CurrentRollResult)
            Result += CurrentRollResult
            CurrentRoll += 1
        if DiceNumber == 1 and DieType == 20:
            if Result == 1:
                CritFailure = True
            if Result >= GlobalInst.GetStringVarAsNumber(self.CritMinimumEntryVar):
                CritSuccess = True
        Result += Modifier
        sleep(0.5)
        if CritSuccess:
            CritResultText = " (Crit!)"
        elif CritFailure:
            LuckyText = ""
            if WindowInst.Mode == "CharacterSheet":
                if CharacterSheetInst.LuckyHalflingBoxVar.get():
                    LuckyText = "  But you're lucky, so if this was an attack roll, ability check, or saving throw, you get to roll again one time!"
            CritResultText = " (Crit Fail!" + LuckyText + ")"
        else:
            CritResultText = ""
        ResultText = DescriptorText + str(DiceNumber) + "d" + str(DieType) + "+" + str(Modifier) + " ->\n(" + IndividualRolls + ")+" + str(Modifier) + " ->\n" + str(Result) + CritResultText
        self.UpdateResultsField(ResultText)

    def IntRoll(self, DiceNumber, DieType, Modifier):
        Result = 0
        CurrentRoll = 1
        while CurrentRoll <= DiceNumber:
            CurrentRollResult = random.randint(1, DieType)
            Result += CurrentRollResult
            CurrentRoll += 1
        Result += Modifier
        return int(Result)

    def AverageRoll(self):
        if self.ValidDiceEntry():
            pass
        else:
            return
        CurrentRoll = 1
        TestRolls = 100000
        Result = 0
        DiceNumber = GlobalInst.GetStringVarAsNumber(self.DiceNumberEntryVar)
        DieType = GlobalInst.GetStringVarAsNumber(self.DieTypeEntryVar)
        Modifier = GlobalInst.GetStringVarAsNumber(self.ModifierEntryVar)
        while CurrentRoll <= TestRolls:
            Result += self.IntRoll(DiceNumber, DieType, Modifier)
            CurrentRoll += 1
        sleep(0.5)
        Result /= TestRolls
        ResultText = "Average of " + str(DiceNumber) + "d" + str(DieType) + "+" + str(Modifier) + " over 100,000 rolls:\n" + str(Result)
        self.UpdateResultsField(ResultText)

    def ValidDiceEntry(self):
        DiceNumber = GlobalInst.GetStringVarAsNumber(self.DiceNumberEntryVar)
        DieType = GlobalInst.GetStringVarAsNumber(self.DieTypeEntryVar)
        if DiceNumber < 1 or DieType < 1:
            messagebox.showerror("Invalid Entry", "Can't roll unless dice and die type are positive.")
            return False
        CritMinimum = GlobalInst.GetStringVarAsNumber(self.CritMinimumEntryVar)
        if CritMinimum <= 0 or CritMinimum >= 21:
            messagebox.showerror("Invalid Entry", "Can't roll unless crit minimum is between 1 and 20.")
            return False
        return True

    def MouseWheelEvent(self, event, EntryVar, MinValue=None, MaxValue=None, DieStep=False):
        try:
            OldValue = GlobalInst.GetStringVarAsNumber(EntryVar)
        except ValueError:
            OldValue = 0
        if event.delta > 0:
            ScrollDistance = 1
        elif event.delta < 0:
            ScrollDistance = -1
        else:
            ScrollDistance = 0
        NewValue = OldValue + ScrollDistance
        if MinValue != None:
            NewValue = max(MinValue, NewValue)
        if MaxValue != None:
            NewValue = min(MaxValue, NewValue)
        if DieStep:
            ValueDelta = NewValue - OldValue
            if ValueDelta < 0:
                NextDieIndex = 0
            elif ValueDelta > 0:
                NextDieIndex = 1
            else:
                return
            try:
                NewValue = self.DieStep[str(OldValue)][NextDieIndex]
            except KeyError:
                NewValue = 20
        EntryVar.set(str(NewValue))

    def CopyResults(self, event):
        self.ResultsField.Text.clipboard_clear()
        self.ResultsField.Text.clipboard_append(self.ResultsField.get())
        StatusBarInst.FlashStatus("Results copied to clipboard.")

    def ClearResults(self, event):
        # Confirm
        ClearConfirm = messagebox.askyesno("Clear Results", "Are you sure you want to clear the roll results?  This cannot be undone.")
        if not ClearConfirm:
            return

        # Clear
        self.ResultsField.set("")

    class PresetRolls:
        def __init__(self, master, ResultsField, CritMinimumEntryVar, PresetRollsFrameRow, PresetRollsScrolledCanvasHeight, PresetRollsScrolledCanvasWidth):
            # Store Parameters
            self.ResultsField = ResultsField
            self.CritMinimumEntryVar = CritMinimumEntryVar
            self.PresetRollsFrameRow = PresetRollsFrameRow
            self.PresetRollsScrolledCanvasHeight = PresetRollsScrolledCanvasHeight
            self.PresetRollsScrolledCanvasWidth = PresetRollsScrolledCanvasWidth

            # Variables
            self.ScrollingDisabledVar = BooleanVar(value=False)

            # Preset Rolls Frame
            self.PresetRollsFrame = LabelFrame(master, text="Preset Rolls:")
            self.PresetRollsFrame.grid(row=self.PresetRollsFrameRow, column=0, padx=2, pady=2)

            # Scrolled Canvas
            self.PresetRollsScrolledCanvas = ScrolledCanvas(self.PresetRollsFrame, Height=self.PresetRollsScrolledCanvasHeight, Width=self.PresetRollsScrolledCanvasWidth, ScrollingDisabledVar=self.ScrollingDisabledVar)
            self.PresetRollsScrolledCanvas.BindEnterAndLeaveToBindMouseWheel()

            # Scrolled Canvas Headers
            self.PresetRollsScrolledCanvasNameHeader = Label(self.PresetRollsScrolledCanvas.WindowFrame, text="Name", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.PresetRollsScrolledCanvasNameHeader.grid(row=0, column=0, sticky=NSEW)
            self.PresetRollsScrolledCanvasNameHeader.bind("<Button-1>", lambda event: self.Sort("Name"))
            self.PresetRollsScrolledCanvasNameHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Name", SearchMode=True))
            self.PresetRollsScrolledCanvasNameHeader.bind("<Button-3>", lambda event: self.Sort("Name", Reverse=True))
            self.PresetRollsScrolledCanvasNameTooltip = Tooltip(self.PresetRollsScrolledCanvasNameHeader, GlobalInst.SortTooltipString)
            self.PresetRollsScrolledCanvasRollHeader = Label(self.PresetRollsScrolledCanvas.WindowFrame, text="Roll", bd=2, relief=GROOVE)
            self.PresetRollsScrolledCanvasRollHeader.grid(row=0, column=1, sticky=NSEW, columnspan=6)
            self.PresetRollsScrolledCanvasSortOrderHeader = Label(self.PresetRollsScrolledCanvas.WindowFrame, text="Sort\nOrder", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.PresetRollsScrolledCanvasSortOrderHeader.grid(row=0, column=7, sticky=NSEW)
            self.PresetRollsScrolledCanvasSortOrderHeader.bind("<Button-1>", lambda event: self.Sort("Sort Order"))
            self.PresetRollsScrolledCanvasSortOrderHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Sort Order", SearchMode=True))
            self.PresetRollsScrolledCanvasSortOrderHeader.bind("<Button-3>", lambda event: self.Sort("Sort Order", Reverse=True))
            self.PresetRollsScrolledCanvasSortOrderTooltip = Tooltip(self.PresetRollsScrolledCanvasSortOrderHeader, GlobalInst.SortTooltipString)

            # Preset Rolls List
            self.PresetRollsList = []

            # Preset Rolls Count
            self.PresetRollsCount = 50

            # Preset Rolls Fields Dictionary
            self.DiceRollerFields = {}
            self.DiceRollerFields["ResultsField"] = self.ResultsField
            self.DiceRollerFields["CritMinimumEntryVar"] = self.CritMinimumEntryVar

            # Sort Order Values
            self.SortOrderValuesList = [""]
            for CurrentIndex in range(1, self.PresetRollsCount + 1):
                self.SortOrderValuesList.append(str(CurrentIndex))

            # Preset Rolls
            for CurrentIndex in range(1, self.PresetRollsCount + 1):
                CurrentEntry = self.PresetRollEntry(self.PresetRollsScrolledCanvas.WindowFrame, self.PresetRollsList, self.ScrollingDisabledVar, self.SortOrderValuesList, self.DiceRollerFields, CurrentIndex)
                CurrentEntry.Display(CurrentIndex)

        def Sort(self, Column, Reverse=False, SearchMode=False):
            # List to Sort
            ListToSort = []

            if SearchMode:
                # Get Search String
                SearchStringPrompt = StringPrompt(WindowInst, "Search", "What do you want to search for?")
                WindowInst.wait_window(SearchStringPrompt.Window)
                if SearchStringPrompt.DataSubmitted.get():
                    SearchString = SearchStringPrompt.StringEntryVar.get()
                else:
                    return

                # Add Fields to List
                for CurrentEntry in self.PresetRollsList:
                    ListToSort.append((CurrentEntry, CurrentEntry.SortFields[Column].get().lower()))

                # Sort the List
                SortedList = sorted(ListToSort, key=lambda x: (x[1] == "", SearchString not in x[1]))
            else:
                if Column == "Name":
                    # Add Fields to List
                    for CurrentEntry in self.PresetRollsList:
                        ListToSort.append((CurrentEntry, CurrentEntry.SortFields[Column].get()))

                    # Sort the List
                    SortedList = sorted(ListToSort, key=lambda x: ((not Reverse and x[1] == "") or (Reverse and x[1] != ""), x[1].lower()), reverse=Reverse)
                elif Column == "Sort Order":
                    # Add Fields to List
                    for CurrentEntry in self.PresetRollsList:
                        ListToSort.append((CurrentEntry, GlobalInst.GetStringVarAsNumber(CurrentEntry.SortFields[Column])))

                    # Sort the List
                    SortedList = sorted(ListToSort, key=lambda x: ((not Reverse and x[1] == 0) or (Reverse and x[1] != 0), x[1]), reverse=Reverse)
                else:
                    return

            # Adjust Entries to New Order
            for CurrentIndex in range(len(SortedList)):
                SortedList[CurrentIndex][0].Display(CurrentIndex + 1)

            # Flag Save Prompt
            SavingAndOpeningInst.SavePrompt = True

            # Update Window Title
            WindowInst.UpdateWindowTitle()

        class PresetRollEntry:
            def __init__(self, master, List, ScrollingDisabledVar, SortOrderValuesList, DiceRollerFields, Row):
                # Store Parameters
                self.master = master
                self.ScrollingDisabledVar = ScrollingDisabledVar
                self.SortOrderValuesList = SortOrderValuesList
                self.DiceRollerFields = DiceRollerFields
                self.Row = Row

                # Variables
                self.PresetRollNameEntryVar = SavedStringVar()
                self.PresetRollDiceNumberEntryVar = SavedStringVar()
                self.PresetRollDieTypeEntryVar = SavedStringVar()
                self.PresetRollModifierEntryVar = SavedStringVar()
                self.PresetRollSortOrderVar = SavedStringVar()

                # Sort Fields
                self.SortFields = {}
                self.SortFields["Name"] = self.PresetRollNameEntryVar
                self.SortFields["Sort Order"] = self.PresetRollSortOrderVar

                # Add to List
                List.append(self)

                # Name
                self.PresetRollNameEntry = EntryExtended(master, justify=CENTER, width=33, textvariable=self.PresetRollNameEntryVar)

                # Roll Button
                self.PresetRollButton = Button(master, text="Roll:", command=self.RollPreset, bg=GlobalInst.ButtonColor)

                # Dice Number
                self.PresetRollDiceNumberEntry = EntryExtended(master, justify=CENTER, width=5, textvariable=self.PresetRollDiceNumberEntryVar)

                # Die Type
                self.PresetRollDieTypeLabel = Label(master, text="d")
                self.PresetRollDieTypeEntry = EntryExtended(master, justify=CENTER, width=5, textvariable=self.PresetRollDieTypeEntryVar)

                # Modifier
                self.PresetRollModifierButton = Label(master, text="+")
                self.PresetRollModifierEntry = EntryExtended(master, justify=CENTER, width=5, textvariable=self.PresetRollModifierEntryVar)

                # Character Sheet Modifier Config
                if WindowInst.Mode in ["CharacterSheet", "NPCSheet"]:
                    self.PresetRollModifierEntryStatModifierInst = StatModifier(self.PresetRollModifierEntry, "<Button-3>", "Right-click to set a stat modifier.", "Preset Roll", Cursor="xterm", DiceRollerMode=True)

                # Sort Order
                self.PresetRollSortOrder = DropdownExtended(master, textvariable=self.PresetRollSortOrderVar, values=self.SortOrderValuesList, width=5, state="readonly", justify=CENTER)
                self.PresetRollSortOrder.bind("<Enter>", self.DisableScrolling)
                self.PresetRollSortOrder.bind("<Leave>", self.EnableScrolling)

            def RollPreset(self):
                DiceRollerInst.DiceNumberEntryVar.set(self.PresetRollDiceNumberEntryVar.get())
                DiceRollerInst.DieTypeEntryVar.set(self.PresetRollDieTypeEntryVar.get())
                DiceRollerInst.ModifierEntryVar.set(self.PresetRollModifierEntryVar.get())
                DiceRollerInst.Roll(self.PresetRollNameEntryVar.get() + ":\n")

            def Display(self, Row):
                self.Row = Row

                # Set Row Size
                self.master.grid_rowconfigure(self.Row, minsize=26)

                # Place in Grid
                self.PresetRollNameEntry.grid(row=self.Row, column=0, sticky=NSEW)
                self.PresetRollButton.grid(row=self.Row, column=1, sticky=NSEW)
                self.PresetRollDiceNumberEntry.grid(row=self.Row, column=2, sticky=NSEW)
                self.PresetRollDieTypeLabel.grid(row=self.Row, column=3, sticky=NSEW)
                self.PresetRollDieTypeEntry.grid(row=self.Row, column=4, sticky=NSEW)
                self.PresetRollModifierButton.grid(row=self.Row, column=5, sticky=NSEW)
                self.PresetRollModifierEntry.grid(row=self.Row, column=6, sticky=NSEW)
                self.PresetRollSortOrder.grid(row=self.Row, column=7, sticky=NSEW)

                # Update Tab Order
                self.PresetRollNameEntry.lift()
                self.PresetRollButton.lift()
                self.PresetRollDiceNumberEntry.lift()
                self.PresetRollDieTypeLabel.lift()
                self.PresetRollDieTypeEntry.lift()
                self.PresetRollModifierButton.lift()
                self.PresetRollModifierEntry.lift()
                self.PresetRollSortOrder.lift()

                # Update Tags
                self.PresetRollNameEntryVar.UpdateTag("PresetRollNameEntryVar" + str(self.Row))
                self.PresetRollDiceNumberEntryVar.UpdateTag("PresetRollDiceNumberEntryVar" + str(self.Row))
                self.PresetRollDieTypeEntryVar.UpdateTag("PresetRollDieTypeEntryVar" + str(self.Row))
                self.PresetRollModifierEntryVar.UpdateTag("PresetRollModifierEntryVar" + str(self.Row))
                self.PresetRollSortOrderVar.UpdateTag("PresetRollSortOrderVar" + str(self.Row))
                if WindowInst.Mode in ["CharacterSheet", "NPCSheet"]:
                    self.PresetRollModifierEntryStatModifierInst.UpdateTags(Prefix="PresetRollModifierEntry", Suffix=str(self.Row))

                # Update Dice Roller Fields Dictionary
                self.DiceRollerFields["PresetRollNameEntryVar" + str(self.Row)] = self.PresetRollNameEntryVar
                self.DiceRollerFields["PresetRollDiceNumberEntryVar" + str(self.Row)] = self.PresetRollDiceNumberEntryVar
                self.DiceRollerFields["PresetRollDieTypeEntryVar" + str(self.Row)] = self.PresetRollDieTypeEntryVar
                self.DiceRollerFields["PresetRollModifierEntryVar" + str(self.Row)] = self.PresetRollModifierEntryVar
                self.DiceRollerFields["PresetRollSortOrderVar" + str(self.Row)] = self.PresetRollSortOrderVar

            def DefaultValues(self):
                self.PresetRollNameEntryVar.set("")
                self.PresetRollDiceNumberEntryVar.set("")
                self.PresetRollDieTypeEntryVar.set("")
                self.PresetRollModifierEntryVar.set("")
                self.PresetRollSortOrderVar.set("")
                if WindowInst.Mode in ["CharacterSheet", "NPCSheet"]:
                    self.PresetRollModifierEntryStatModifierInst.DefaultValues()

            def DisableScrolling(self, event):
                self.ScrollingDisabledVar.set(True)

            def EnableScrolling(self, event):
                self.ScrollingDisabledVar.set(False)


class EncounterHeader:
    def __init__(self, master):
        # Variables
        self.EncounterNameEntryVar = SavedStringVar("EncounterNameEntryVar")
        self.CREntryVar = SavedStringVar("CREntryVar")
        self.ExperienceEntryVar = SavedStringVar("ExperienceEntryVar")

        # Encounter Header Frame
        self.EncounterHeaderFrame = LabelFrame(master, text="Basic Encounter Info:")
        self.EncounterHeaderFrame.grid_columnconfigure(2, weight=1)
        self.EncounterHeaderFrame.grid_columnconfigure(7, weight=1)
        self.EncounterHeaderFrame.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Encounter Name
        self.EncounterNameLabel = Label(self.EncounterHeaderFrame, text="Encounter Name:")
        self.EncounterNameLabel.grid(row=0, column=0)
        self.EncounterNameEntry = EntryExtended(self.EncounterHeaderFrame, textvariable=self.EncounterNameEntryVar, justify=CENTER, width=30)
        self.EncounterNameEntry.grid(row=0, column=1, padx=2, pady=2)

        # CR
        self.CRLabel = Label(self.EncounterHeaderFrame, text="CR:")
        self.CRLabel.grid(row=0, column=3)
        self.CREntry = EntryExtended(self.EncounterHeaderFrame, textvariable=self.CREntryVar, justify=CENTER, width=5)
        self.CREntry.grid(row=0, column=4, padx=2, pady=2)

        # Experience
        self.ExperienceLabel = Label(self.EncounterHeaderFrame, text="Experience:")
        self.ExperienceLabel.grid(row=0, column=5)
        self.ExperienceEntry = EntryExtended(self.EncounterHeaderFrame, textvariable=self.ExperienceEntryVar, justify=CENTER, width=10)
        self.ExperienceEntry.grid(row=0, column=6, padx=2, pady=2)

        # Notes
        self.NotesFrame = LabelFrame(self.EncounterHeaderFrame, text="Notes:")
        self.NotesFrame.grid_columnconfigure(1, weight=1)
        self.NotesFrame.grid_columnconfigure(3, weight=1)
        self.NotesFrame.grid(row=1, column=0, columnspan=7, padx=2, pady=2, sticky=NSEW)
        self.NotesHeight = 65
        self.NotesWidth = 155
        self.NotesField1 = ScrolledText(self.NotesFrame, Width=self.NotesWidth, Height=self.NotesHeight, SavedDataTag="NotesField1")
        self.NotesField1.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
        self.NotesField2 = ScrolledText(self.NotesFrame, Width=self.NotesWidth, Height=self.NotesHeight, SavedDataTag="NotesField2")
        self.NotesField2.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
        self.NotesField3 = ScrolledText(self.NotesFrame, Width=self.NotesWidth, Height=self.NotesHeight, SavedDataTag="NotesField3")
        self.NotesField3.grid(row=0, column=4, sticky=NSEW, padx=2, pady=2)

        # Description
        self.DescriptionFrame = LabelFrame(self.EncounterHeaderFrame, text="Description:")
        self.DescriptionFrame.grid(row=0, column=8, sticky=NSEW, rowspan=2, padx=2, pady=2)
        self.DescriptionField = ScrolledText(self.DescriptionFrame, Width=180, Height=100, SavedDataTag="DescriptionField")
        self.DescriptionField.grid(row=0, column=0, sticky=NSEW)

        # Rewards
        self.RewardsFrame = LabelFrame(self.EncounterHeaderFrame, text="Rewards:")
        self.RewardsFrame.grid(row=0, column=9, sticky=NSEW, rowspan=2, padx=2, pady=2)
        self.RewardsField = ScrolledText(self.RewardsFrame, Width=150, Height=100, SavedDataTag="RewardsField")
        self.RewardsField.grid(row=0, column=0, sticky=NSEW)


class InitiativeOrder:
    def __init__(self, master):
        # Variables
        self.RoundEntryVar = SavedStringVar("RoundEntryVar", DefaultValue=str(1))
        self.ScrollingDisabledVar = BooleanVar(value=False)

        # Initiative Order Frame
        self.InitiativeOrderFrame = LabelFrame(master, text="Initiative Order:")
        self.InitiativeOrderFrame.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)

        # Initiative Data Frame
        self.InitiativeDataFrame = Frame(self.InitiativeOrderFrame)
        self.InitiativeDataFrame.grid_columnconfigure(0, weight=1)
        self.InitiativeDataFrame.grid_columnconfigure(1, weight=1)
        self.InitiativeDataFrame.grid_columnconfigure(2, weight=1)
        self.InitiativeDataFrame.grid_columnconfigure(3, weight=1)
        self.InitiativeDataFrame.grid_columnconfigure(4, weight=1)
        self.InitiativeDataFrame.grid(row=0, column=0, sticky=NSEW)

        # Initiative Data Font
        self.InitiativeDataFont = font.Font(size=14)

        # Round Entry
        self.RoundFrame = LabelFrame(self.InitiativeDataFrame, text="Round:")
        self.RoundFrame.grid_columnconfigure(0, weight=1)
        self.RoundFrame.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
        self.RoundEntry = RoundEntry(self.RoundFrame, textvariable=self.RoundEntryVar, font=self.InitiativeDataFont, width=5, justify=CENTER)
        self.RoundEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # New Round Button
        self.NewRoundButton = Button(self.InitiativeDataFrame, text="New Round", command=self.NewRound, bg=GlobalInst.ButtonColor, font=self.InitiativeDataFont)
        self.NewRoundButton.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
        WindowInst.bind("<Control-r>", lambda event: self.NewRound())
        self.NewRoundTooltip = Tooltip(self.NewRoundButton, "Keyboard Shortcut:  Ctrl+R")

        # Next Turn Button
        self.NextTurnButton = Button(self.InitiativeDataFrame, text="Next Turn", command=self.NextTurn, bg=GlobalInst.ButtonColor, font=self.InitiativeDataFont)
        self.NextTurnButton.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
        WindowInst.bind("<Control-t>", lambda event: self.NextTurn())
        self.NextTurnTooltip = Tooltip(self.NextTurnButton, "Keyboard Shortcut:  Ctrl+T")

        # Clear Turns Button
        self.ClearTurnsButton = Button(self.InitiativeDataFrame, text="Clear Turns", command=self.ClearTurns, bg=GlobalInst.ButtonColor, font=self.InitiativeDataFont)
        self.ClearTurnsButton.grid(row=0, column=3, sticky=NSEW, padx=2, pady=2)
        WindowInst.bind("<Control-T>", lambda event: self.ClearTurns())
        self.ClearTurnsTooltip = Tooltip(self.ClearTurnsButton, "Keyboard Shortcut:  Ctrl+Shift+T")

        # Sort Initiative Order Button
        self.SortInitiativeOrderButton = Button(self.InitiativeDataFrame, text="Sort Initiative Order", command=self.SortInitiativeOrder, bg=GlobalInst.ButtonColor, font=self.InitiativeDataFont)
        self.SortInitiativeOrderButton.grid(row=0, column=4, sticky=NSEW, padx=2, pady=2)
        WindowInst.bind("<Control-i>", lambda event: self.SortInitiativeOrder())
        self.SortInitiativeOrderTooltip = Tooltip(self.SortInitiativeOrderButton, "Keyboard Shortcut:  Ctrl+I")

        # Initiative Order Scrolled Canvas
        self.InitiativeOrderScrolledCanvasFrame = Frame(self.InitiativeOrderFrame)
        self.InitiativeOrderScrolledCanvasFrame.grid(row=1, column=0, sticky=NSEW)
        self.InitiativeOrderScrolledCanvas = ScrolledCanvas(self.InitiativeOrderScrolledCanvasFrame, Height=470, Width=839, ScrollingDisabledVar=self.ScrollingDisabledVar)
        self.InitiativeOrderScrolledCanvas.BindEnterAndLeaveToBindMouseWheel()

        # Initiative Header
        self.InitiativeHeader = Label(self.InitiativeOrderScrolledCanvas.WindowFrame, text="Initiative", bd=2, relief=GROOVE)
        self.InitiativeHeader.grid(row=0, column=0, sticky=NSEW)

        # Tie Priority Header
        self.TiePriorityHeader = Label(self.InitiativeOrderScrolledCanvas.WindowFrame, text="Tie\nPriority", bd=2, relief=GROOVE)
        self.TiePriorityHeader.grid(row=0, column=1, sticky=NSEW)

        # Name Header
        self.NameHeader = Label(self.InitiativeOrderScrolledCanvas.WindowFrame, text="Name", bd=2, relief=GROOVE)
        self.NameHeader.grid(row=0, column=2, sticky=NSEW)

        # AC Header
        self.ACHeader = Label(self.InitiativeOrderScrolledCanvas.WindowFrame, text="AC", bd=2, relief=GROOVE)
        self.ACHeader.grid(row=0, column=3, sticky=NSEW)

        # Temp HP Header
        self.TempHPHeader = Label(self.InitiativeOrderScrolledCanvas.WindowFrame, text="Temp\nHP", bd=2, relief=GROOVE)
        self.TempHPHeader.grid(row=0, column=4, sticky=NSEW)

        # Current HP Header
        self.CurrentHPHeader = Label(self.InitiativeOrderScrolledCanvas.WindowFrame, text="Current\nHP", bd=2, relief=GROOVE)
        self.CurrentHPHeader.grid(row=0, column=5, sticky=NSEW)

        # Max HP Header
        self.MaxHPHeader = Label(self.InitiativeOrderScrolledCanvas.WindowFrame, text="Max\nHP", bd=2, relief=GROOVE)
        self.MaxHPHeader.grid(row=0, column=6, sticky=NSEW)

        # Concentration Header
        self.ConcentrationHeader = Label(self.InitiativeOrderScrolledCanvas.WindowFrame, text="Conc.", bd=2, relief=GROOVE)
        self.ConcentrationHeader.grid(row=0, column=7, sticky=NSEW)

        # Conditions Header
        self.ConditionsHeader = Label(self.InitiativeOrderScrolledCanvas.WindowFrame, text="Conditions", bd=2, relief=GROOVE)
        self.ConditionsHeader.grid(row=0, column=8, sticky=NSEW)

        # Location Header
        self.LocationHeader = Label(self.InitiativeOrderScrolledCanvas.WindowFrame, text="Location", bd=2, relief=GROOVE)
        self.LocationHeader.grid(row=0, column=9, sticky=NSEW)

        # Notes Header
        self.NotesHeader = Label(self.InitiativeOrderScrolledCanvas.WindowFrame, text="Notes", bd=2, relief=GROOVE)
        self.NotesHeader.grid(row=0, column=10, sticky=NSEW)

        # Entries List
        self.InitiativeEntriesList = []

        # Initiative Entries Count
        self.InitiativeEntriesCount = 100

        # Initiative Entries
        for CurrentIndex in range(1, self.InitiativeEntriesCount + 1):
            CurrentEntry = self.InitiativeEntry(self.InitiativeOrderScrolledCanvas.WindowFrame, self.InitiativeEntriesList, self.ScrollingDisabledVar, CurrentIndex)
            CurrentEntry.Display(CurrentIndex)

    def NewRound(self):
        if self.ValidRound():
            pass
        else:
            return

        if not messagebox.askyesno("New Round", "Start a new round and clear all turns taken?  This cannot be undone."):
            return
        self.ClearTurns(True)
        CurrentRound = GlobalInst.GetStringVarAsNumber(self.RoundEntryVar)
        NextRound = CurrentRound + 1
        self.RoundEntryVar.set(NextRound)

    def NextTurn(self):
        for Entry in self.InitiativeEntriesList:
            if not Entry.InitiativeEntryTurnDoneVar.get():
                Entry.ToggleTurnDone()
                break

    def ClearTurns(self, NewRound=False):
        if not NewRound:
            if not messagebox.askyesno("Clear Turns", "Clear all turns taken?  This cannot be undone."):
                return
        for Entry in self.InitiativeEntriesList:
            Entry.TurnDoneOff()

    def SortInitiativeOrder(self):
        # List to Sort
        ListToSort = []

        # Add Fields to List
        for CurrentEntry in self.InitiativeEntriesList:
            ListToSort.append((CurrentEntry, CurrentEntry.InitiativeEntryResultEntryVar, CurrentEntry.InitiativeEntryTiePriorityDropdownVar))

        # Sort the List
        SortedList = sorted(ListToSort, key=lambda x: (x[1].get() != "", GlobalInst.GetStringVarAsNumber(x[1]), -1 * GlobalInst.GetStringVarAsNumber(x[2])), reverse=True)

        # Adjust Entries to New Order
        self.InitiativeEntriesList.clear()
        for CurrentIndex in range(len(SortedList)):
            SortedList[CurrentIndex][0].Display(CurrentIndex + 1)
            self.InitiativeEntriesList.append(SortedList[CurrentIndex][0])

        # Flag Save Prompt
        SavingAndOpeningInst.SavePrompt = True

        # Update Window Title
        WindowInst.UpdateWindowTitle()

    def ValidRound(self):
        Round = GlobalInst.GetStringVarAsNumber(self.RoundEntryVar)
        if Round <= 0:
            messagebox.showerror("Invalid Entry", "Round must be greater than 0.")
            return False
        return True

    class InitiativeEntry:
        def __init__(self, master, List, ScrollingDisabledVar, Row):
            # Store Parameters
            self.master = master
            self.List = List
            self.ScrollingDisabledVar = ScrollingDisabledVar
            self.Row = Row

            # Variables
            self.InitiativeEntryResultEntryVar = SavedStringVar()
            self.InitiativeEntryTiePriorityDropdownVar = SavedStringVar(DefaultValue=str("1"))
            self.InitiativeEntryNameEntryVar = SavedStringVar()
            self.InitiativeEntryACEntryVar = SavedStringVar()
            self.InitiativeEntryTempHPEntryVar = SavedStringVar()
            self.InitiativeEntryCurrentHPEntryVar = SavedStringVar()
            self.InitiativeEntryMaxHPEntryVar = SavedStringVar()
            self.ConcentrationTrueColor = "#7aff63"
            self.ConcentrationFalseColor = GlobalInst.ButtonColor
            self.InitiativeEntryConcentrationBoxVar = SavedBooleanVar()
            self.TurnDoneTrueColor = "#7cafff"
            self.InitiativeEntryTurnDoneVar = SavedBooleanVar()
            self.DeadTrueColor = "#ff6d6d"
            self.InitiativeEntryDeadVar = SavedBooleanVar()
            self.InitiativeEntrySizeEntryVar = SavedStringVar()
            self.InitiativeEntryTypeAndTagsEntryVar = SavedStringVar()
            self.InitiativeEntryAlignmentEntryVar = SavedStringVar()
            self.InitiativeEntryProficiencyEntryVar = SavedStringVar()
            self.InitiativeEntrySpeedEntryVar = SavedStringVar()
            self.InitiativeEntryCRAndExperienceEntryVar = SavedStringVar()
            self.InitiativeEntryAbilitiesStrengthEntryVar = SavedStringVar()
            self.InitiativeEntryAbilitiesDexterityEntryVar = SavedStringVar()
            self.InitiativeEntryAbilitiesConstitutionEntryVar = SavedStringVar()
            self.InitiativeEntryAbilitiesIntelligenceEntryVar = SavedStringVar()
            self.InitiativeEntryAbilitiesWisdomEntryVar = SavedStringVar()
            self.InitiativeEntryAbilitiesCharismaEntryVar = SavedStringVar()
            self.InitiativeEntrySkillSensesAndLanguagesFieldVar = SavedStringVar()
            self.InitiativeEntrySavingThrowsFieldVar = SavedStringVar()
            self.InitiativeEntryVulnerabilitiesResistancesAndImmunitiesFieldVar = SavedStringVar()
            self.InitiativeEntrySpecialTraitsFieldVar = SavedStringVar()
            self.InitiativeEntryActionsFieldVar = SavedStringVar()
            self.InitiativeEntryReactionsFieldVar = SavedStringVar()
            self.InitiativeEntryInventoryFieldVar = SavedStringVar()
            self.InitiativeEntryLegendaryActionsAndLairActionsFieldVar = SavedStringVar()
            self.InitiativeEntryNotesFieldVar = SavedStringVar()

            # Add to List
            self.List.append(self)

            # Initiative Entry
            self.InitiativeEntryResultEntry = InitiativeEntry(self.master, textvariable=self.InitiativeEntryResultEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
            self.InitiativeEntryResultEntry.bind("<Button-3>", lambda event: self.ToggleTurnDone())
            self.InitiativeEntryResultTooltip = Tooltip(self.InitiativeEntryResultEntry, "Right-click to toggle turn taken.")

            # Tie Priority Dropdown
            self.InitiativeEntryTiePriorityDropdown = DropdownExtended(self.master, textvariable=self.InitiativeEntryTiePriorityDropdownVar,
                                                                       values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"], width=3, state="readonly",
                                                                       justify=CENTER)
            self.InitiativeEntryTiePriorityDropdown.bind("<Enter>", self.DisableScrolling)
            self.InitiativeEntryTiePriorityDropdown.bind("<Leave>", self.EnableScrolling)

            # Name Entry
            self.InitiativeEntryNameEntry = EntryExtended(self.master, textvariable=self.InitiativeEntryNameEntryVar, justify=CENTER, width=35, bg=GlobalInst.ButtonColor)
            self.InitiativeEntryNameEntry.bind("<Button-3>", self.SetCreatureStats)
            self.InitiativeEntryNameEntry.bind("<Shift-Button-3>", self.Duplicate)
            self.InitiativeEntryNameEntry.bind("<Control-Button-3>", self.Clear)
            self.InitiativeEntryNameTooltip = Tooltip(self.InitiativeEntryNameEntry, "Right-click to set additional creature info.  Shift+right-click to duplicate.  Ctrl+right-click to clear.")

            # AC Entry
            self.InitiativeEntryACEntry = EntryExtended(self.master, textvariable=self.InitiativeEntryACEntryVar, justify=CENTER, width=5)

            # Temp HP Entry
            self.InitiativeEntryTempHPEntry = EntryExtended(self.master, textvariable=self.InitiativeEntryTempHPEntryVar, justify=CENTER, width=5)

            # Current HP Entry
            self.InitiativeEntryCurrentHPEntry = EntryExtended(self.master, textvariable=self.InitiativeEntryCurrentHPEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
            self.InitiativeEntryCurrentHPEntry.bind("<Button-3>", lambda event: self.Damage())
            self.InitiativeEntryCurrentHPEntry.bind("<Shift-Button-3>", lambda event: self.Heal())
            self.InitiativeEntryCurrentHPEntry.bind("<Control-Button-3>", lambda event: self.ToggleDead())
            self.InitiativeEntryCurrentHPTooltip = Tooltip(self.InitiativeEntryCurrentHPEntry, "Right-click to damage.  Shift+right-click to heal.  Control+right-click to toggle dead.")

            # Max HP Entry
            self.InitiativeEntryMaxHPEntry = EntryExtended(self.master, textvariable=self.InitiativeEntryMaxHPEntryVar, justify=CENTER, width=5)

            # Concentration Box
            self.InitiativeEntryConcentrationBox = Checkbutton(self.master, text="Conc.", variable=self.InitiativeEntryConcentrationBoxVar, background=self.ConcentrationFalseColor, selectcolor=self.ConcentrationTrueColor,
                                                               indicatoron=False)

            # Conditions Field
            self.InitiativeEntryConditionsField = ScrolledText(self.master, Width=113, Height=35, FontSize=7)
            self.InitiativeEntryConditionsField.ScrolledTextFrame.bind("<Enter>", self.DisableScrolling)
            self.InitiativeEntryConditionsField.ScrolledTextFrame.bind("<Leave>", self.EnableScrolling)

            # Location Field
            self.InitiativeEntryLocationField = ScrolledText(self.master, Width=113, Height=35, FontSize=7)
            self.InitiativeEntryLocationField.ScrolledTextFrame.bind("<Enter>", self.DisableScrolling)
            self.InitiativeEntryLocationField.ScrolledTextFrame.bind("<Leave>", self.EnableScrolling)

            # Notes Field
            self.InitiativeEntryNotesField = ScrolledText(self.master, Width=113, Height=35, FontSize=7)
            self.InitiativeEntryNotesField.ScrolledTextFrame.bind("<Enter>", self.DisableScrolling)
            self.InitiativeEntryNotesField.ScrolledTextFrame.bind("<Leave>", self.EnableScrolling)

            # Creature Stats Dictionary
            self.CreatureStats = {}
            self.CreatureStats["NameEntryVar"] = self.InitiativeEntryNameEntryVar
            self.CreatureStats["SizeEntryVar"] = self.InitiativeEntrySizeEntryVar
            self.CreatureStats["TypeAndTagsEntryVar"] = self.InitiativeEntryTypeAndTagsEntryVar
            self.CreatureStats["AlignmentEntryVar"] = self.InitiativeEntryAlignmentEntryVar
            self.CreatureStats["ProficiencyEntryVar"] = self.InitiativeEntryProficiencyEntryVar
            self.CreatureStats["TempHPEntryVar"] = self.InitiativeEntryTempHPEntryVar
            self.CreatureStats["CurrentHPEntryVar"] = self.InitiativeEntryCurrentHPEntryVar
            self.CreatureStats["MaxHPEntryVar"] = self.InitiativeEntryMaxHPEntryVar
            self.CreatureStats["ACEntryVar"] = self.InitiativeEntryACEntryVar
            self.CreatureStats["SpeedEntryVar"] = self.InitiativeEntrySpeedEntryVar
            self.CreatureStats["CRAndExperienceEntryVar"] = self.InitiativeEntryCRAndExperienceEntryVar
            self.CreatureStats["AbilitiesStrengthEntryVar"] = self.InitiativeEntryAbilitiesStrengthEntryVar
            self.CreatureStats["AbilitiesDexterityEntryVar"] = self.InitiativeEntryAbilitiesDexterityEntryVar
            self.CreatureStats["AbilitiesConstitutionEntryVar"] = self.InitiativeEntryAbilitiesConstitutionEntryVar
            self.CreatureStats["AbilitiesIntelligenceEntryVar"] = self.InitiativeEntryAbilitiesIntelligenceEntryVar
            self.CreatureStats["AbilitiesWisdomEntryVar"] = self.InitiativeEntryAbilitiesWisdomEntryVar
            self.CreatureStats["AbilitiesCharismaEntryVar"] = self.InitiativeEntryAbilitiesCharismaEntryVar
            self.CreatureStats["SkillSensesAndLanguagesFieldVar"] = self.InitiativeEntrySkillSensesAndLanguagesFieldVar
            self.CreatureStats["SavingThrowsFieldVar"] = self.InitiativeEntrySavingThrowsFieldVar
            self.CreatureStats["VulnerabilitiesResistancesAndImmunitiesFieldVar"] = self.InitiativeEntryVulnerabilitiesResistancesAndImmunitiesFieldVar
            self.CreatureStats["SpecialTraitsFieldVar"] = self.InitiativeEntrySpecialTraitsFieldVar
            self.CreatureStats["ActionsFieldVar"] = self.InitiativeEntryActionsFieldVar
            self.CreatureStats["ReactionsFieldVar"] = self.InitiativeEntryReactionsFieldVar
            self.CreatureStats["InventoryFieldVar"] = self.InitiativeEntryInventoryFieldVar
            self.CreatureStats["LegendaryActionsAndLairActionsFieldVar"] = self.InitiativeEntryLegendaryActionsAndLairActionsFieldVar
            self.CreatureStats["NotesFieldVar"] = self.InitiativeEntryNotesFieldVar

        def Display(self, Row):
            self.Row = Row

            # Place in Grid
            self.InitiativeEntryResultEntry.grid(row=self.Row, column=0, sticky=NSEW)
            self.InitiativeEntryTiePriorityDropdown.grid(row=self.Row, column=1, sticky=NSEW)
            self.InitiativeEntryNameEntry.grid(row=self.Row, column=2, sticky=NSEW)
            self.InitiativeEntryACEntry.grid(row=self.Row, column=3, sticky=NSEW)
            self.InitiativeEntryTempHPEntry.grid(row=self.Row, column=4, sticky=NSEW)
            self.InitiativeEntryCurrentHPEntry.grid(row=self.Row, column=5, sticky=NSEW)
            self.InitiativeEntryMaxHPEntry.grid(row=self.Row, column=6, sticky=NSEW)
            self.InitiativeEntryConcentrationBox.grid(row=self.Row, column=7, sticky=NSEW)
            self.InitiativeEntryConditionsField.grid(row=self.Row, column=8, sticky=NSEW)
            self.InitiativeEntryLocationField.grid(row=self.Row, column=9, sticky=NSEW)
            self.InitiativeEntryNotesField.grid(row=self.Row, column=10, sticky=NSEW)

            # Update Tab Order
            self.InitiativeEntryResultEntry.lift()
            self.InitiativeEntryTiePriorityDropdown.lift()
            self.InitiativeEntryNameEntry.lift()
            self.InitiativeEntryACEntry.lift()
            self.InitiativeEntryTempHPEntry.lift()
            self.InitiativeEntryCurrentHPEntry.lift()
            self.InitiativeEntryMaxHPEntry.lift()
            self.InitiativeEntryConcentrationBox.lift()
            self.InitiativeEntryConditionsField.lift()
            self.InitiativeEntryLocationField.lift()
            self.InitiativeEntryNotesField.lift()

            # Update Tags
            self.InitiativeEntryResultEntryVar.UpdateTag("InitiativeEntryInitiativeEntryVar" + str(self.Row))
            self.InitiativeEntryTiePriorityDropdownVar.UpdateTag("InitiativeEntryTiePriorityDropdownVar" + str(self.Row))
            self.InitiativeEntryNameEntryVar.UpdateTag("InitiativeEntryNameEntryVar" + str(self.Row))
            self.InitiativeEntryACEntryVar.UpdateTag("InitiativeEntryACEntryVar" + str(self.Row))
            self.InitiativeEntryTempHPEntryVar.UpdateTag("InitiativeEntryTempHPEntryVar" + str(self.Row))
            self.InitiativeEntryCurrentHPEntryVar.UpdateTag("InitiativeEntryCurrentHPEntryVar" + str(self.Row))
            self.InitiativeEntryMaxHPEntryVar.UpdateTag("InitiativeEntryMaxHPEntryVar" + str(self.Row))
            self.InitiativeEntryConcentrationBoxVar.UpdateTag("InitiativeEntryConcentrationBoxVar" + str(self.Row))
            self.InitiativeEntryConditionsField.UpdateTag("InitiativeEntryConditionsField" + str(self.Row))
            self.InitiativeEntryLocationField.UpdateTag("InitiativeEntryLocationField" + str(self.Row))
            self.InitiativeEntryNotesField.UpdateTag("InitiativeEntryNotesField" + str(self.Row))
            self.InitiativeEntryTurnDoneVar.UpdateTag("InitiativeEntryTurnDoneVar" + str(self.Row))
            self.InitiativeEntryDeadVar.UpdateTag("InitiativeEntryDeadVar" + str(self.Row))
            self.InitiativeEntrySizeEntryVar.UpdateTag("InitiativeEntrySizeEntryVar" + str(self.Row))
            self.InitiativeEntryTypeAndTagsEntryVar.UpdateTag("InitiativeEntryTypeAndTagsEntryVar" + str(self.Row))
            self.InitiativeEntryAlignmentEntryVar.UpdateTag("InitiativeEntryAlignmentEntryVar" + str(self.Row))
            self.InitiativeEntryProficiencyEntryVar.UpdateTag("InitiativeEntryProficiencyEntryVar" + str(self.Row))
            self.InitiativeEntrySpeedEntryVar.UpdateTag("InitiativeEntrySpeedEntryVar" + str(self.Row))
            self.InitiativeEntryCRAndExperienceEntryVar.UpdateTag("InitiativeEntryCRAndExperienceEntryVar" + str(self.Row))
            self.InitiativeEntryAbilitiesStrengthEntryVar.UpdateTag("InitiativeEntryAbilitiesStrengthEntryVar" + str(self.Row))
            self.InitiativeEntryAbilitiesDexterityEntryVar.UpdateTag("InitiativeEntryAbilitiesDexterityEntryVar" + str(self.Row))
            self.InitiativeEntryAbilitiesConstitutionEntryVar.UpdateTag("InitiativeEntryAbilitiesConstitutionEntryVar" + str(self.Row))
            self.InitiativeEntryAbilitiesIntelligenceEntryVar.UpdateTag("InitiativeEntryAbilitiesIntelligenceEntryVar" + str(self.Row))
            self.InitiativeEntryAbilitiesWisdomEntryVar.UpdateTag("InitiativeEntryAbilitiesWisdomEntryVar" + str(self.Row))
            self.InitiativeEntryAbilitiesCharismaEntryVar.UpdateTag("InitiativeEntryAbilitiesCharismaEntryVar" + str(self.Row))
            self.InitiativeEntrySkillSensesAndLanguagesFieldVar.UpdateTag("InitiativeEntrySkillSensesAndLanguagesFieldVar" + str(self.Row))
            self.InitiativeEntrySavingThrowsFieldVar.UpdateTag("InitiativeEntrySavingThrowsFieldVar" + str(self.Row))
            self.InitiativeEntryVulnerabilitiesResistancesAndImmunitiesFieldVar.UpdateTag("InitiativeEntryVulnerabilitiesResistancesAndImmunitiesFieldVar" + str(self.Row))
            self.InitiativeEntrySpecialTraitsFieldVar.UpdateTag("InitiativeEntrySpecialTraitsFieldVar" + str(self.Row))
            self.InitiativeEntryActionsFieldVar.UpdateTag("InitiativeEntryActionsFieldVar" + str(self.Row))
            self.InitiativeEntryReactionsFieldVar.UpdateTag("InitiativeEntryReactionsFieldVar" + str(self.Row))
            self.InitiativeEntryInventoryFieldVar.UpdateTag("InitiativeEntryInventoryFieldVar" + str(self.Row))
            self.InitiativeEntryLegendaryActionsAndLairActionsFieldVar.UpdateTag("InitiativeEntryLegendaryActionsAndLairActionsFieldVar" + str(self.Row))
            self.InitiativeEntryNotesFieldVar.UpdateTag("InitiativeEntryNotesFieldVar" + str(self.Row))

        def ToggleTurnDone(self):
            if self.InitiativeEntryTurnDoneVar.get():
                self.TurnDoneOff()
            else:
                self.TurnDoneOn()

        def TurnDoneOn(self):
            self.InitiativeEntryResultEntry.configure(background=self.TurnDoneTrueColor)
            self.InitiativeEntryTurnDoneVar.set(True)

        def TurnDoneOff(self):
            self.InitiativeEntryResultEntry.configure(background=GlobalInst.ButtonColor)
            self.InitiativeEntryTurnDoneVar.set(False)

        def ToggleDead(self):
            if self.InitiativeEntryDeadVar.get():
                self.DeadOff()
            else:
                self.DeadOn()

        def DeadOn(self):
            self.InitiativeEntryCurrentHPEntry.configure(background=self.DeadTrueColor)
            self.InitiativeEntryDeadVar.set(True)

        def DeadOff(self):
            self.InitiativeEntryCurrentHPEntry.configure(background=GlobalInst.ButtonColor)
            self.InitiativeEntryDeadVar.set(False)

        def DisableScrolling(self, event):
            self.ScrollingDisabledVar.set(True)

        def EnableScrolling(self, event):
            self.ScrollingDisabledVar.set(False)

        def Damage(self):
            if self.ValidLifeValues():
                pass
            else:
                return
            CurrentTempHP = GlobalInst.GetStringVarAsNumber(self.InitiativeEntryTempHPEntryVar)
            InitiativeEntryCurrentHPString = self.InitiativeEntryCurrentHPEntryVar.get()
            if InitiativeEntryCurrentHPString == "" or InitiativeEntryCurrentHPString == "+" or InitiativeEntryCurrentHPString == "-":
                CurrentHP = GlobalInst.GetStringVarAsNumber(self.InitiativeEntryMaxHPEntryVar)
            else:
                CurrentHP = GlobalInst.GetStringVarAsNumber(self.InitiativeEntryCurrentHPEntryVar)
            DamagePrompt = IntegerPrompt(WindowInst, "Damage", "How much damage?", MinValue=0)
            WindowInst.wait_window(DamagePrompt.Window)
            if DamagePrompt.DataSubmitted.get():
                Damage = DamagePrompt.GetData()
                TotalDamage = Damage
            else:
                return
            if CurrentTempHP == 0:
                self.InitiativeEntryCurrentHPEntryVar.set(str(CurrentHP - Damage))
            elif CurrentTempHP >= 1:
                if CurrentTempHP < Damage:
                    Damage -= CurrentTempHP
                    self.InitiativeEntryTempHPEntryVar.set(str(0))
                    self.InitiativeEntryCurrentHPEntryVar.set(str(CurrentHP - Damage))
                elif CurrentTempHP >= Damage:
                    self.InitiativeEntryTempHPEntryVar.set(str(CurrentTempHP - Damage))
            if self.InitiativeEntryConcentrationBoxVar.get():
                ConcentrationDC = str(max(10, math.ceil(TotalDamage / 2)))
                messagebox.showinfo("Concentration Check", "DC " + ConcentrationDC + " Constitution saving throw required to maintain concentration.")
            if GlobalInst.GetStringVarAsNumber(self.InitiativeEntryCurrentHPEntryVar) <= 0:
                if messagebox.askyesno("Dead", "This creature's health is at or below 0.  Is it dead?"):
                    self.DeadOn()
                else:
                    self.DeadOff()

        def Heal(self):
            if self.ValidLifeValues():
                pass
            else:
                return
            CurrentHP = GlobalInst.GetStringVarAsNumber(self.InitiativeEntryCurrentHPEntryVar)
            MaxHP = GlobalInst.GetStringVarAsNumber(self.InitiativeEntryMaxHPEntryVar)
            HealingPrompt = IntegerPrompt(WindowInst, "Heal", "How much healing?", MinValue=0)
            WindowInst.wait_window(HealingPrompt.Window)
            if HealingPrompt.DataSubmitted.get():
                Healing = HealingPrompt.GetData()
            else:
                return
            HealedValue = Healing + max(CurrentHP, 0)
            if HealedValue > MaxHP:
                self.InitiativeEntryCurrentHPEntryVar.set(str(MaxHP))
            elif HealedValue <= MaxHP:
                self.InitiativeEntryCurrentHPEntryVar.set(str(HealedValue))
            self.DeadOff()

        def ValidLifeValues(self):
            try:
                TempHP = GlobalInst.GetStringVarAsNumber(self.InitiativeEntryTempHPEntryVar)
                CurrentHP = GlobalInst.GetStringVarAsNumber(self.InitiativeEntryCurrentHPEntryVar)
                MaxHP = GlobalInst.GetStringVarAsNumber(self.InitiativeEntryMaxHPEntryVar)
            except:
                messagebox.showerror("Invalid Entry", "HP values must be whole numbers.")
                return False
            if TempHP < 0 or MaxHP < 1:
                messagebox.showerror("Invalid Entry", "Temp HP cannot be negative and max HP must be positive.")
                return False
            return True

        def SetCreatureStats(self, event):
            # Create Config Window and Wait
            CreatureDataInst = CreatureData(WindowInst, DialogMode=True, DialogData=self.CreatureStats)
            WindowInst.wait_window(CreatureDataInst.Window)

            # Handle Variables
            if CreatureDataInst.DataSubmitted.get():
                for Tag, Var in self.CreatureStats.items():
                    Var.set(CreatureDataInst.CreatureStatsFields[Tag].get())

        def Clear(self, event):
            if not messagebox.askyesno("Clear", "Clear this initiative entry?  This cannot be undone."):
                return
            else:
                pass
            self.InitiativeEntryResultEntryVar.set("")
            self.InitiativeEntryTiePriorityDropdownVar.set(str(1))
            self.InitiativeEntryNameEntryVar.set("")
            self.InitiativeEntryACEntryVar.set("")
            self.InitiativeEntryTempHPEntryVar.set("")
            self.InitiativeEntryCurrentHPEntryVar.set("")
            self.InitiativeEntryMaxHPEntryVar.set("")
            self.InitiativeEntryConcentrationBoxVar.set(False)
            self.InitiativeEntrySizeEntryVar.set("")
            self.InitiativeEntryTypeAndTagsEntryVar.set("")
            self.InitiativeEntryAlignmentEntryVar.set("")
            self.InitiativeEntryProficiencyEntryVar.set("")
            self.InitiativeEntrySpeedEntryVar.set("")
            self.InitiativeEntryCRAndExperienceEntryVar.set("")
            self.InitiativeEntryAbilitiesStrengthEntryVar.set("")
            self.InitiativeEntryAbilitiesDexterityEntryVar.set("")
            self.InitiativeEntryAbilitiesConstitutionEntryVar.set("")
            self.InitiativeEntryAbilitiesIntelligenceEntryVar.set("")
            self.InitiativeEntryAbilitiesWisdomEntryVar.set("")
            self.InitiativeEntryAbilitiesCharismaEntryVar.set("")
            self.InitiativeEntrySkillSensesAndLanguagesFieldVar.set("")
            self.InitiativeEntrySavingThrowsFieldVar.set("")
            self.InitiativeEntryVulnerabilitiesResistancesAndImmunitiesFieldVar.set("")
            self.InitiativeEntrySpecialTraitsFieldVar.set("")
            self.InitiativeEntryActionsFieldVar.set("")
            self.InitiativeEntryReactionsFieldVar.set("")
            self.InitiativeEntryInventoryFieldVar.set("")
            self.InitiativeEntryLegendaryActionsAndLairActionsFieldVar.set("")
            self.InitiativeEntryNotesFieldVar.set("")
            self.InitiativeEntryConditionsField.set("")
            self.InitiativeEntryLocationField.set("")
            self.InitiativeEntryNotesField.set("")
            self.TurnDoneOff()
            self.DeadOff()

        def Duplicate(self, event):
            if not self.DuplicateTargetsValid():
                return
            else:
                pass
            for Entry in self.List:
                if Entry.InitiativeEntryNameEntryVar.get() == "DUPLICATE TARGET":
                    Entry.InitiativeEntryResultEntryVar.set(self.InitiativeEntryResultEntryVar.get())
                    Entry.InitiativeEntryTiePriorityDropdownVar.set(self.InitiativeEntryTiePriorityDropdownVar.get())
                    Entry.InitiativeEntryNameEntryVar.set(self.InitiativeEntryNameEntryVar.get())
                    Entry.InitiativeEntryACEntryVar.set(self.InitiativeEntryACEntryVar.get())
                    Entry.InitiativeEntryTempHPEntryVar.set(self.InitiativeEntryTempHPEntryVar.get())
                    Entry.InitiativeEntryCurrentHPEntryVar.set(self.InitiativeEntryCurrentHPEntryVar.get())
                    Entry.InitiativeEntryMaxHPEntryVar.set(self.InitiativeEntryMaxHPEntryVar.get())
                    Entry.InitiativeEntryConcentrationBoxVar.set(self.InitiativeEntryConcentrationBoxVar.get())
                    Entry.InitiativeEntryTurnDoneVar.set(self.InitiativeEntryTurnDoneVar.get())
                    Entry.InitiativeEntrySizeEntryVar.set(self.InitiativeEntrySizeEntryVar.get())
                    Entry.InitiativeEntryTypeAndTagsEntryVar.set(self.InitiativeEntryTypeAndTagsEntryVar.get())
                    Entry.InitiativeEntryAlignmentEntryVar.set(self.InitiativeEntryAlignmentEntryVar.get())
                    Entry.InitiativeEntryProficiencyEntryVar.set(self.InitiativeEntryProficiencyEntryVar.get())
                    Entry.InitiativeEntrySpeedEntryVar.set(self.InitiativeEntrySpeedEntryVar.get())
                    Entry.InitiativeEntryCRAndExperienceEntryVar.set(self.InitiativeEntryCRAndExperienceEntryVar.get())
                    Entry.InitiativeEntryAbilitiesStrengthEntryVar.set(self.InitiativeEntryAbilitiesStrengthEntryVar.get())
                    Entry.InitiativeEntryAbilitiesDexterityEntryVar.set(self.InitiativeEntryAbilitiesDexterityEntryVar.get())
                    Entry.InitiativeEntryAbilitiesConstitutionEntryVar.set(self.InitiativeEntryAbilitiesConstitutionEntryVar.get())
                    Entry.InitiativeEntryAbilitiesIntelligenceEntryVar.set(self.InitiativeEntryAbilitiesIntelligenceEntryVar.get())
                    Entry.InitiativeEntryAbilitiesWisdomEntryVar.set(self.InitiativeEntryAbilitiesWisdomEntryVar.get())
                    Entry.InitiativeEntryAbilitiesCharismaEntryVar.set(self.InitiativeEntryAbilitiesCharismaEntryVar.get())
                    Entry.InitiativeEntrySkillSensesAndLanguagesFieldVar.set(self.InitiativeEntrySkillSensesAndLanguagesFieldVar.get())
                    Entry.InitiativeEntrySavingThrowsFieldVar.set(self.InitiativeEntrySavingThrowsFieldVar.get())
                    Entry.InitiativeEntryVulnerabilitiesResistancesAndImmunitiesFieldVar.set(self.InitiativeEntryVulnerabilitiesResistancesAndImmunitiesFieldVar.get())
                    Entry.InitiativeEntrySpecialTraitsFieldVar.set(self.InitiativeEntrySpecialTraitsFieldVar.get())
                    Entry.InitiativeEntryActionsFieldVar.set(self.InitiativeEntryActionsFieldVar.get())
                    Entry.InitiativeEntryReactionsFieldVar.set(self.InitiativeEntryReactionsFieldVar.get())
                    Entry.InitiativeEntryInventoryFieldVar.set(self.InitiativeEntryInventoryFieldVar.get())
                    Entry.InitiativeEntryLegendaryActionsAndLairActionsFieldVar.set(self.InitiativeEntryLegendaryActionsAndLairActionsFieldVar.get())
                    Entry.InitiativeEntryNotesFieldVar.set(self.InitiativeEntryNotesFieldVar.get())
                    Entry.InitiativeEntryConditionsField.set(self.InitiativeEntryConditionsField.get())
                    Entry.InitiativeEntryLocationField.set(self.InitiativeEntryLocationField.get())
                    Entry.InitiativeEntryNotesField.set(self.InitiativeEntryNotesField.get())
                    Entry.TurnDoneOff()

        def DuplicateTargetsValid(self):
            if self.InitiativeEntryNameEntryVar.get() == "DUPLICATE TARGET":
                messagebox.showerror("Duplicate Error", "Cannot duplicate an entry designated as a target.")
                return False
            for Entry in self.List:
                if Entry.InitiativeEntryNameEntryVar.get() == "DUPLICATE TARGET":
                    return True
            messagebox.showerror("Duplicate Error", "No target entries found.  Designate target entries to overwrite by setting their names to \"DUPLICATE TARGET\".")
            return False


class CompactInitiativeOrder:
    def __init__(self, master):
        # Variables
        self.RoundEntryVar = StringVar(value=str(1))
        self.ScrollingDisabledVar = BooleanVar(value=False)

        # Initiative Data Frame
        self.InitiativeDataFrame = Frame(master)
        self.InitiativeDataFrame.grid_columnconfigure(0, weight=1)
        self.InitiativeDataFrame.grid_columnconfigure(1, weight=1)
        self.InitiativeDataFrame.grid(row=0, column=0, sticky=NSEW)

        # Initiative Data Font
        self.InitiativeDataFont = font.Font(size=14)

        # Round Entry
        self.RoundFrame = LabelFrame(self.InitiativeDataFrame, text="Round:")
        self.RoundFrame.grid_columnconfigure(0, weight=1)
        self.RoundFrame.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2, columnspan=2)
        self.RoundEntry = RoundEntry(self.RoundFrame, textvariable=self.RoundEntryVar, font=self.InitiativeDataFont, width=5, justify=CENTER)
        self.RoundEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Clear Turns Button
        self.ClearTurnsButton = Button(self.InitiativeDataFrame, text="Clear Turns", command=self.ClearTurns, bg=GlobalInst.ButtonColor, font=self.InitiativeDataFont)
        self.ClearTurnsButton.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
        WindowInst.bind("<Control-T>", lambda event: self.ClearTurns())
        self.ClearTurnsTooltip = Tooltip(self.ClearTurnsButton, "Keyboard Shortcut:  Ctrl+Shift+T")

        # Sort Initiative Order Button
        self.SortInitiativeOrderButton = Button(self.InitiativeDataFrame, text="Sort Initiative Order", command=self.SortInitiativeOrder, bg=GlobalInst.ButtonColor, font=self.InitiativeDataFont)
        self.SortInitiativeOrderButton.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
        WindowInst.bind("<Control-i>", lambda event: self.SortInitiativeOrder())
        self.SortInitiativeOrderTooltip = Tooltip(self.SortInitiativeOrderButton, "Keyboard Shortcut:  Ctrl+I")

        # Next Turn Button
        self.NextTurnButton = Button(self.InitiativeDataFrame, text="Next Turn", command=self.NextTurn, bg=GlobalInst.ButtonColor, font=self.InitiativeDataFont)
        self.NextTurnButton.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)
        WindowInst.bind("<Control-t>", lambda event: self.NextTurn())
        self.NextTurnTooltip = Tooltip(self.NextTurnButton, "Keyboard Shortcut:  Ctrl+T")

        # New Round Button
        self.NewRoundButton = Button(self.InitiativeDataFrame, text="New Round", command=self.NewRound, bg=GlobalInst.ButtonColor, font=self.InitiativeDataFont)
        self.NewRoundButton.grid(row=2, column=1, sticky=NSEW, padx=2, pady=2)
        WindowInst.bind("<Control-r>", lambda event: self.NewRound())
        self.NewRoundTooltip = Tooltip(self.NewRoundButton, "Keyboard Shortcut:  Ctrl+R")

        # Initiative Order Scrolled Canvas
        self.InitiativeOrderScrolledCanvasFrame = Frame(master)
        self.InitiativeOrderScrolledCanvasFrame.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
        self.InitiativeOrderScrolledCanvas = ScrolledCanvas(self.InitiativeOrderScrolledCanvasFrame, Height=400, Width=310, ScrollingDisabledVar=self.ScrollingDisabledVar)
        self.InitiativeOrderScrolledCanvas.BindEnterAndLeaveToBindMouseWheel()

        # Initiative Header
        self.InitiativeHeader = Label(self.InitiativeOrderScrolledCanvas.WindowFrame, text="Initiative", bd=2, relief=GROOVE)
        self.InitiativeHeader.grid(row=0, column=0, sticky=NSEW)

        # Tie Priority Header
        self.TiePriorityHeader = Label(self.InitiativeOrderScrolledCanvas.WindowFrame, text="Tie\nPriority", bd=2, relief=GROOVE)
        self.TiePriorityHeader.grid(row=0, column=1, sticky=NSEW)

        # Name Header
        self.NameHeader = Label(self.InitiativeOrderScrolledCanvas.WindowFrame, text="Name", bd=2, relief=GROOVE)
        self.NameHeader.grid(row=0, column=2, sticky=NSEW)

        # Entries List
        self.InitiativeEntriesList = []

        # Entries Count
        self.InitiativeEntriesCount = 100

        # Initiative Entries
        for CurrentIndex in range(1, self.InitiativeEntriesCount + 1):
            CurrentEntry = self.InitiativeEntry(self.InitiativeOrderScrolledCanvas.WindowFrame, self.InitiativeEntriesList, self.ScrollingDisabledVar, CurrentIndex)
            CurrentEntry.Display(CurrentIndex)

    def NewRound(self):
        if self.ValidRound():
            pass
        else:
            return

        if not messagebox.askyesno("New Round", "Start a new round and clear all turns taken?  This cannot be undone."):
            return
        self.ClearTurns(True)
        CurrentRound = GlobalInst.GetStringVarAsNumber(self.RoundEntryVar)
        NextRound = CurrentRound + 1
        self.RoundEntryVar.set(NextRound)

    def NextTurn(self):
        for Entry in self.InitiativeEntriesList:
            if not Entry.InitiativeEntryTurnDoneVar.get():
                Entry.ToggleTurnDone()
                break

    def ClearTurns(self, NewRound=False):
        if not NewRound:
            if not messagebox.askyesno("Clear Turns", "Clear all turns taken?  This cannot be undone."):
                return
        for Entry in self.InitiativeEntriesList:
            Entry.TurnDoneOff()

    def SortInitiativeOrder(self):
        # List to Sort
        ListToSort = []

        # Add Fields to List
        for CurrentEntry in self.InitiativeEntriesList:
            ListToSort.append((CurrentEntry, CurrentEntry.InitiativeEntryResultEntryVar, CurrentEntry.InitiativeEntryTiePriorityDropdownVar))

        # Sort the List
        SortedList = sorted(ListToSort, key=lambda x: (x[1].get() != "", GlobalInst.GetStringVarAsNumber(x[1]), -1 * GlobalInst.GetStringVarAsNumber(x[2])), reverse=True)

        # Adjust Entries to New Order
        self.InitiativeEntriesList.clear()
        for CurrentIndex in range(len(SortedList)):
            SortedList[CurrentIndex][0].Display(CurrentIndex + 1)
            self.InitiativeEntriesList.append(SortedList[CurrentIndex][0])

        # Update Window Title
        WindowInst.UpdateWindowTitle()

    def ValidRound(self):
        Round = GlobalInst.GetStringVarAsNumber(self.RoundEntryVar)
        if Round <= 0:
            messagebox.showerror("Invalid Entry", "Round must be greater than 0.")
            return False
        return True

    class InitiativeEntry:
        def __init__(self, master, List, ScrollingDisabledVar, Row):
            # Store Parameters
            self.master = master
            self.List = List
            self.ScrollingDisabledVar = ScrollingDisabledVar
            self.Row = Row

            # Variables
            self.InitiativeEntryResultEntryVar = StringVar()
            self.InitiativeEntryTiePriorityDropdownVar = StringVar(value=str("1"))
            self.InitiativeEntryNameEntryVar = StringVar()
            self.TurnDoneTrueColor = "#7cafff"
            self.InitiativeEntryTurnDoneVar = BooleanVar()

            # Add to List
            self.List.append(self)

            # Initiative Entry
            self.InitiativeEntryResultEntry = InitiativeEntry(self.master, textvariable=self.InitiativeEntryResultEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
            self.InitiativeEntryResultEntry.bind("<Button-3>", lambda event: self.ToggleTurnDone())
            self.InitiativeEntryResultTooltip = Tooltip(self.InitiativeEntryResultEntry, "Right-click to toggle turn taken.")

            # Tie Priority Dropdown
            self.InitiativeEntryTiePriorityDropdown = DropdownExtended(self.master, textvariable=self.InitiativeEntryTiePriorityDropdownVar,
                                                                       values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"], width=3, state="readonly",
                                                                       justify=CENTER)
            self.InitiativeEntryTiePriorityDropdown.bind("<Enter>", self.DisableScrolling)
            self.InitiativeEntryTiePriorityDropdown.bind("<Leave>", self.EnableScrolling)

            # Name Entry
            self.InitiativeEntryNameEntry = EntryExtended(self.master, textvariable=self.InitiativeEntryNameEntryVar, justify=CENTER, width=35, bg=GlobalInst.ButtonColor)
            self.InitiativeEntryNameEntry.bind("<Button-3>", self.Duplicate)
            self.InitiativeEntryNameEntry.bind("<Shift-Button-3>", self.Clear)
            self.InitiativeEntryNameTooltip = Tooltip(self.InitiativeEntryNameEntry, "Right-click to duplicate.  Shift+right-click to clear.")

        def Display(self, Row):
            self.Row = Row

            # Place in Grid
            self.InitiativeEntryResultEntry.grid(row=self.Row, column=0, sticky=NSEW)
            self.InitiativeEntryTiePriorityDropdown.grid(row=self.Row, column=1, sticky=NSEW)
            self.InitiativeEntryNameEntry.grid(row=self.Row, column=2, sticky=NSEW)

            # Update Tab Order
            self.InitiativeEntryResultEntry.lift()
            self.InitiativeEntryTiePriorityDropdown.lift()
            self.InitiativeEntryNameEntry.lift()

        def ToggleTurnDone(self):
            if self.InitiativeEntryTurnDoneVar.get():
                self.TurnDoneOff()
            else:
                self.TurnDoneOn()

        def TurnDoneOn(self):
            self.InitiativeEntryResultEntry.configure(background=self.TurnDoneTrueColor)
            self.InitiativeEntryTurnDoneVar.set(True)

        def TurnDoneOff(self):
            self.InitiativeEntryResultEntry.configure(background=GlobalInst.ButtonColor)
            self.InitiativeEntryTurnDoneVar.set(False)

        def DisableScrolling(self, event):
            self.ScrollingDisabledVar.set(True)

        def EnableScrolling(self, event):
            self.ScrollingDisabledVar.set(False)

        def Clear(self, event):
            if not messagebox.askyesno("Clear", "Clear this initiative entry?  This cannot be undone."):
                return
            else:
                pass
            self.InitiativeEntryResultEntryVar.set("")
            self.InitiativeEntryTiePriorityDropdownVar.set(str(1))
            self.InitiativeEntryNameEntryVar.set("")
            self.TurnDoneOff()

        def Duplicate(self, event):
            if not self.DuplicateTargetsValid():
                return
            else:
                pass
            for Entry in self.List:
                if Entry.InitiativeEntryNameEntryVar.get() == "DUPLICATE TARGET":
                    Entry.InitiativeEntryResultEntryVar.set(self.InitiativeEntryResultEntryVar.get())
                    Entry.InitiativeEntryTiePriorityDropdownVar.set(self.InitiativeEntryTiePriorityDropdownVar.get())
                    Entry.InitiativeEntryNameEntryVar.set(self.InitiativeEntryNameEntryVar.get())
                    Entry.TurnDoneOff()

        def DuplicateTargetsValid(self):
            if self.InitiativeEntryNameEntryVar.get() == "DUPLICATE TARGET":
                messagebox.showerror("Duplicate Error", "Cannot duplicate an entry designated as a target.")
                return False
            for Entry in self.List:
                if Entry.InitiativeEntryNameEntryVar.get() == "DUPLICATE TARGET":
                    return True
            messagebox.showerror("Duplicate Error", "No target entries found.  Designate target entries to overwrite by setting their names to \"DUPLICATE TARGET\".")
            return False


class HoardSheet:
    def __init__(self, master):
        # Variables
        self.HoardNameEntryVar = SavedStringVar("HoardNameEntryVar")
        self.HoardLocationEntryVar = SavedStringVar("HoardLocationEntryVar")
        self.HoardStorageCostsEntryVar = SavedStringVar("HoardStorageCostsEntryVar")
        self.CoinsEntryCPVar = SavedStringVar("CoinsEntryCPVar")
        self.CoinsEntryCPVar.trace_add("write", lambda a, b, c: self.UpdateHoardStats())
        self.CoinsEntrySPVar = SavedStringVar("CoinsEntrySPVar")
        self.CoinsEntrySPVar.trace_add("write", lambda a, b, c: self.UpdateHoardStats())
        self.CoinsEntryEPVar = SavedStringVar("CoinsEntryEPVar")
        self.CoinsEntryEPVar.trace_add("write", lambda a, b, c: self.UpdateHoardStats())
        self.CoinsEntryGPVar = SavedStringVar("CoinsEntryGPVar")
        self.CoinsEntryGPVar.trace_add("write", lambda a, b, c: self.UpdateHoardStats())
        self.CoinsEntryPPVar = SavedStringVar("CoinsEntryPPVar")
        self.CoinsEntryPPVar.trace_add("write", lambda a, b, c: self.UpdateHoardStats())
        self.ValueCP = Decimal(0.01)
        self.ValueSP = Decimal(0.1)
        self.ValueEP = Decimal(0.5)
        self.ValueGP = Decimal(1)
        self.ValuePP = Decimal(10)
        self.WeightPerCoin = Decimal(0.02)
        self.StatsCoinsValueEntryVar = StringVar()
        self.StatsCoinsWeightEntryVar = StringVar()
        self.StatsItemsValueEntryVar = StringVar()
        self.StatsItemsWeightEntryVar = StringVar()
        self.StatsTotalValueEntryVar = StringVar()
        self.StatsTotalWeightEntryVar = StringVar()
        self.ScrollingDisabledVar = BooleanVar(value=False)

        # Spending Coins Dictionary
        self.SpendingCoins = {}
        self.SpendingCoins["CP"] = self.CoinsEntryCPVar
        self.SpendingCoins["SP"] = self.CoinsEntrySPVar
        self.SpendingCoins["EP"] = self.CoinsEntryEPVar
        self.SpendingCoins["GP"] = self.CoinsEntryGPVar
        self.SpendingCoins["PP"] = self.CoinsEntryPPVar
        self.SpendingCoins["SPValueAsCP"] = Decimal(10)
        self.SpendingCoins["EPValueAsCP"] = Decimal(50)
        self.SpendingCoins["GPValueAsCP"] = Decimal(100)
        self.SpendingCoins["PPValueAsCP"] = Decimal(1000)

        # Denomination Values Dictionary
        self.DenominationValues = {}
        self.DenominationValues["cp"] = self.ValueCP
        self.DenominationValues["sp"] = self.ValueSP
        self.DenominationValues["ep"] = self.ValueEP
        self.DenominationValues["gp"] = self.ValueGP
        self.DenominationValues["pp"] = self.ValuePP
        self.DenominationValues[""] = 0

        # Hoard Header
        self.HoardHeaderFrame = LabelFrame(master, text="Basic Hoard Info:")
        self.HoardHeaderFrame.grid_columnconfigure(1, weight=1)
        self.HoardHeaderFrame.grid_columnconfigure(3, weight=1)
        self.HoardHeaderFrame.grid_columnconfigure(5, weight=1)
        self.HoardHeaderFrame.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2, columnspan=2)
        self.HoardNameLabel = Label(self.HoardHeaderFrame, text="Name or Owners:")
        self.HoardNameLabel.grid(row=0, column=0, sticky=E)
        self.HoardNameEntry = EntryExtended(self.HoardHeaderFrame, textvariable=self.HoardNameEntryVar, justify=CENTER, width=30)
        self.HoardNameEntry.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
        self.HoardLocationLabel = Label(self.HoardHeaderFrame, text="Location:")
        self.HoardLocationLabel.grid(row=0, column=2, sticky=E)
        self.HoardLocationEntry = EntryExtended(self.HoardHeaderFrame, textvariable=self.HoardLocationEntryVar, justify=CENTER, width=30)
        self.HoardLocationEntry.grid(row=0, column=3, sticky=NSEW, padx=2, pady=2)
        self.HoardStorageCostsLabel = Label(self.HoardHeaderFrame, text="Storage Costs:")
        self.HoardStorageCostsLabel.grid(row=0, column=4, sticky=E)
        self.HoardStorageCostsEntry = EntryExtended(self.HoardHeaderFrame, textvariable=self.HoardStorageCostsEntryVar, justify=CENTER, width=30)
        self.HoardStorageCostsEntry.grid(row=0, column=5, sticky=NSEW, padx=2, pady=2)

        # Coins
        self.CoinsFrame = LabelFrame(master, text="Coins:")
        self.CoinsFrame.grid_columnconfigure(0, weight=1)
        self.CoinsFrame.grid_columnconfigure(1, weight=1)
        self.CoinsFrame.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
        self.CoinsInputHolderFrame = Frame(self.CoinsFrame)
        self.CoinsInputHolderFrame.grid_columnconfigure(0, weight=1)
        self.CoinsInputHolderFrame.grid_columnconfigure(1, weight=1)
        self.CoinsInputHolderFrame.grid_columnconfigure(2, weight=1)
        self.CoinsInputHolderFrame.grid_columnconfigure(3, weight=1)
        self.CoinsInputHolderFrame.grid_columnconfigure(4, weight=1)
        self.CoinsInputHolderFrame.grid(row=0, column=0, columnspan=2, sticky=NSEW)
        self.CoinsHeaderCP = Label(self.CoinsInputHolderFrame, text="CP", bd=2, relief=GROOVE)
        self.CoinsHeaderCP.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
        self.CoinsEntryCP = CoinsEntry(self.CoinsInputHolderFrame, width=5, justify=CENTER, textvariable=self.CoinsEntryCPVar)
        self.CoinsEntryCP.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
        self.CoinsHeaderSP = Label(self.CoinsInputHolderFrame, text="SP", bd=2, relief=GROOVE)
        self.CoinsHeaderSP.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
        self.CoinsEntrySP = CoinsEntry(self.CoinsInputHolderFrame, width=5, justify=CENTER, textvariable=self.CoinsEntrySPVar)
        self.CoinsEntrySP.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
        self.CoinsHeaderEP = Label(self.CoinsInputHolderFrame, text="EP", bd=2, relief=GROOVE)
        self.CoinsHeaderEP.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
        self.CoinsEntryEP = CoinsEntry(self.CoinsInputHolderFrame, width=5, justify=CENTER, textvariable=self.CoinsEntryEPVar)
        self.CoinsEntryEP.grid(row=1, column=2, sticky=NSEW, padx=2, pady=2)
        self.CoinsHeaderGP = Label(self.CoinsInputHolderFrame, text="GP", bd=2, relief=GROOVE)
        self.CoinsHeaderGP.grid(row=0, column=3, sticky=NSEW, padx=2, pady=2)
        self.CoinsEntryGP = CoinsEntry(self.CoinsInputHolderFrame, width=5, justify=CENTER, textvariable=self.CoinsEntryGPVar)
        self.CoinsEntryGP.grid(row=1, column=3, sticky=NSEW, padx=2, pady=2)
        self.CoinsHeaderPP = Label(self.CoinsInputHolderFrame, text="PP", bd=2, relief=GROOVE)
        self.CoinsHeaderPP.grid(row=0, column=4, sticky=NSEW, padx=2, pady=2)
        self.CoinsEntryPP = CoinsEntry(self.CoinsInputHolderFrame, width=5, justify=CENTER, textvariable=self.CoinsEntryPPVar)
        self.CoinsEntryPP.grid(row=1, column=4, sticky=NSEW, padx=2, pady=2)
        self.GainCoinsButton = Button(self.CoinsFrame, text="Gain", bg=GlobalInst.ButtonColor, command=self.GainCoins)
        self.GainCoinsButton.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
        self.SpendCoinsButton = Button(self.CoinsFrame, text="Spend", bg=GlobalInst.ButtonColor, command=self.SpendCoins)
        self.SpendCoinsButton.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)

        # Stats
        self.StatsFrame = LabelFrame(master, text="Hoard Stats:")
        self.StatsFrame.grid_columnconfigure(1, weight=1)
        self.StatsFrame.grid_columnconfigure(2, weight=1)
        self.StatsFrame.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)
        self.StatsCoinsHeader = Label(self.StatsFrame, text="Coins", bd=2, relief=GROOVE)
        self.StatsCoinsHeader.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
        self.StatsItemsHeader = Label(self.StatsFrame, text="Items", bd=2, relief=GROOVE)
        self.StatsItemsHeader.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)
        self.StatsTotalHeader = Label(self.StatsFrame, text="Total", bd=2, relief=GROOVE)
        self.StatsTotalHeader.grid(row=3, column=0, sticky=NSEW, padx=2, pady=2)
        self.StatsValueHeader = Label(self.StatsFrame, text="Value (gp)", bd=2, relief=GROOVE)
        self.StatsValueHeader.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
        self.StatsWeightHeader = Label(self.StatsFrame, text="Weight (lbs.)", bd=2, relief=GROOVE)
        self.StatsWeightHeader.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
        self.StatsCoinsValueEntry = EntryExtended(self.StatsFrame, textvariable=self.StatsCoinsValueEntryVar, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow", width=5)
        self.StatsCoinsValueEntry.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
        self.StatsCoinsWeightEntry = EntryExtended(self.StatsFrame, textvariable=self.StatsCoinsWeightEntryVar, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow", width=5)
        self.StatsCoinsWeightEntry.grid(row=1, column=2, sticky=NSEW, padx=2, pady=2)
        self.StatsItemsValueEntry = EntryExtended(self.StatsFrame, textvariable=self.StatsItemsValueEntryVar, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow", width=5)
        self.StatsItemsValueEntry.grid(row=2, column=1, sticky=NSEW, padx=2, pady=2)
        self.StatsItemsWeightEntry = EntryExtended(self.StatsFrame, textvariable=self.StatsItemsWeightEntryVar, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow", width=5)
        self.StatsItemsWeightEntry.grid(row=2, column=2, sticky=NSEW, padx=2, pady=2)
        self.StatsTotalValueEntry = EntryExtended(self.StatsFrame, textvariable=self.StatsTotalValueEntryVar, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow", width=5)
        self.StatsTotalValueEntry.grid(row=3, column=1, sticky=NSEW, padx=2, pady=2)
        self.StatsTotalWeightEntry = EntryExtended(self.StatsFrame, textvariable=self.StatsTotalWeightEntryVar, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow", width=5)
        self.StatsTotalWeightEntry.grid(row=3, column=2, sticky=NSEW, padx=2, pady=2)

        # Notes
        self.HoardNotesFrame = LabelFrame(master, text="Notes:")
        self.HoardNotesFrame.grid(row=3, column=0, sticky=NSEW, padx=2, pady=2)
        self.HoardNotesField = ScrolledText(self.HoardNotesFrame, SavedDataTag="HoardNotesField", Width=286)
        self.HoardNotesField.grid(row=0, column=0, sticky=NSEW)

        # Treasure Items
        self.TreasureItemsFrame = LabelFrame(master, text="Treasure Items:")
        self.TreasureItemsFrame.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2, rowspan=3)

        # Treasure Items Scrolled Canvas
        self.TreasureItemsScrolledCanvas = ScrolledCanvas(self.TreasureItemsFrame, Height=324, Width=622, ScrollingDisabledVar=self.ScrollingDisabledVar)
        self.TreasureItemsScrolledCanvas.BindEnterAndLeaveToBindMouseWheel()

        # Treasure Items Headers
        self.TreasureItemsListNameHeader = Label(self.TreasureItemsScrolledCanvas.WindowFrame, text="Name", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
        self.TreasureItemsListNameHeader.grid(row=0, column=0, sticky=NSEW)
        self.TreasureItemsListNameHeader.bind("<Button-1>", lambda event: self.Sort("Name"))
        self.TreasureItemsListNameHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Name", SearchMode=True))
        self.TreasureItemsListNameHeader.bind("<Button-3>", lambda event: self.Sort("Name", Reverse=True))
        self.TreasureItemsListNameTooltip = Tooltip(self.TreasureItemsListNameHeader, GlobalInst.SortTooltipString)
        self.TreasureItemsListCountHeader = Label(self.TreasureItemsScrolledCanvas.WindowFrame, text="Count", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
        self.TreasureItemsListCountHeader.grid(row=0, column=1, sticky=NSEW)
        self.TreasureItemsListCountHeader.bind("<Button-1>", lambda event: self.Sort("Count"))
        self.TreasureItemsListCountHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Count", SearchMode=True))
        self.TreasureItemsListCountHeader.bind("<Button-3>", lambda event: self.Sort("Count", Reverse=True))
        self.TreasureItemsListCountTooltip = Tooltip(self.TreasureItemsListCountHeader, GlobalInst.SortTooltipString)
        self.TreasureItemsListUnitWeightHeader = Label(self.TreasureItemsScrolledCanvas.WindowFrame, text="Unit Weight\n(lbs.)", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
        self.TreasureItemsListUnitWeightHeader.grid(row=0, column=2, sticky=NSEW)
        self.TreasureItemsListUnitWeightHeader.bind("<Button-1>", lambda event: self.Sort("Unit Weight"))
        self.TreasureItemsListUnitWeightHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Unit Weight", SearchMode=True))
        self.TreasureItemsListUnitWeightHeader.bind("<Button-3>", lambda event: self.Sort("Unit Weight", Reverse=True))
        self.TreasureItemsListUnitWeightTooltip = Tooltip(self.TreasureItemsListUnitWeightHeader, GlobalInst.SortTooltipString)
        self.TreasureItemsListUnitValueHeader = Label(self.TreasureItemsScrolledCanvas.WindowFrame, text="Unit Value", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
        self.TreasureItemsListUnitValueHeader.grid(row=0, column=3, sticky=NSEW)
        self.TreasureItemsListUnitValueHeader.bind("<Button-1>", lambda event: self.Sort("Unit Value"))
        self.TreasureItemsListUnitValueHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Unit Value", SearchMode=True))
        self.TreasureItemsListUnitValueHeader.bind("<Button-3>", lambda event: self.Sort("Unit Value", Reverse=True))
        self.TreasureItemsListUnitValueTooltip = Tooltip(self.TreasureItemsListUnitValueHeader, GlobalInst.SortTooltipString)
        self.TreasureItemsListUnitValueDenominationHeader = Label(self.TreasureItemsScrolledCanvas.WindowFrame, text="Value\nDenom.", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
        self.TreasureItemsListUnitValueDenominationHeader.grid(row=0, column=4, sticky=NSEW)
        self.TreasureItemsListUnitValueDenominationHeader.bind("<Button-1>", lambda event: self.Sort("Value Denomination"))
        self.TreasureItemsListUnitValueDenominationHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Value Denomination", SearchMode=True))
        self.TreasureItemsListUnitValueDenominationHeader.bind("<Button-3>", lambda event: self.Sort("Value Denomination", Reverse=True))
        self.TreasureItemsListUnitValueDenominationTooltip = Tooltip(self.TreasureItemsListUnitValueDenominationHeader, GlobalInst.SortTooltipString)
        self.TreasureItemsListTotalWeightHeader = Label(self.TreasureItemsScrolledCanvas.WindowFrame, text="Total Weight\n(lbs.)", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
        self.TreasureItemsListTotalWeightHeader.grid(row=0, column=5, sticky=NSEW)
        self.TreasureItemsListTotalWeightHeader.bind("<Button-1>", lambda event: self.Sort("Total Weight"))
        self.TreasureItemsListTotalWeightHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Total Weight", SearchMode=True))
        self.TreasureItemsListTotalWeightHeader.bind("<Button-3>", lambda event: self.Sort("Total Weight", Reverse=True))
        self.TreasureItemsListTotalWeightTooltip = Tooltip(self.TreasureItemsListTotalWeightHeader, GlobalInst.SortTooltipString)
        self.TreasureItemsListTotalValueHeader = Label(self.TreasureItemsScrolledCanvas.WindowFrame, text="Total Value\n(gp)", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
        self.TreasureItemsListTotalValueHeader.grid(row=0, column=6, sticky=NSEW)
        self.TreasureItemsListTotalValueHeader.bind("<Button-1>", lambda event: self.Sort("Total Value"))
        self.TreasureItemsListTotalValueHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Total Value", SearchMode=True))
        self.TreasureItemsListTotalValueHeader.bind("<Button-3>", lambda event: self.Sort("Total Value", Reverse=True))
        self.TreasureItemsListTotalValueTooltip = Tooltip(self.TreasureItemsListTotalValueHeader, GlobalInst.SortTooltipString)
        self.TreasureItemsListSortOrderHeader = Label(self.TreasureItemsScrolledCanvas.WindowFrame, text="Sort\nOrder", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
        self.TreasureItemsListSortOrderHeader.grid(row=0, column=7, sticky=NSEW)
        self.TreasureItemsListSortOrderHeader.bind("<Button-1>", lambda event: self.Sort("Sort Order"))
        self.TreasureItemsListSortOrderHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Sort Order", SearchMode=True))
        self.TreasureItemsListSortOrderHeader.bind("<Button-3>", lambda event: self.Sort("Sort Order", Reverse=True))
        self.TreasureItemsListSortOrderTooltip = Tooltip(self.TreasureItemsListSortOrderHeader, GlobalInst.SortTooltipString)

        # Treasure Item Entries List
        self.TreasureItemEntriesList = []

        # Treasure Item Entries Count
        self.TreasureItemEntriesCount = 200

        # Sort Order Values
        self.SortOrderValuesList = [""]
        for CurrentIndex in range(1, self.TreasureItemEntriesCount + 1):
            self.SortOrderValuesList.append(str(CurrentIndex))

        # Treasure Item Entries
        for CurrentIndex in range(1, self.TreasureItemEntriesCount + 1):
            CurrentEntry = self.TreasureItemEntry(self.TreasureItemsScrolledCanvas.WindowFrame, self.TreasureItemEntriesList, self.ScrollingDisabledVar, self.SortOrderValuesList, CurrentIndex)
            CurrentEntry.Display(CurrentIndex)

    def SpendCoins(self):
        # Create Config Window and Wait
        SpendCoinsMenuInst = SpendCoinsMenu(WindowInst, self.SpendingCoins)
        WindowInst.wait_window(SpendCoinsMenuInst.Window)

        # Handle Variables
        if SpendCoinsMenuInst.DataSubmitted.get():
            for Denomination in SpendCoinsMenuInst.Remaining.keys():
                self.SpendingCoins[Denomination].set(SpendCoinsMenuInst.Remaining[Denomination].get())

    def GainCoins(self):
        # Create Config Window and Wait
        GainCoinsMenuInst = GainCoinsMenu(WindowInst)
        WindowInst.wait_window(GainCoinsMenuInst.Window)

        # Handle Variables
        if GainCoinsMenuInst.DataSubmitted.get():
            for Denomination, Gain in GainCoinsMenuInst.Gained.items():
                self.SpendingCoins[Denomination].set(str(GlobalInst.GetStringVarAsNumber(self.SpendingCoins[Denomination]) + GlobalInst.GetStringVarAsNumber(Gain)))

    def UpdateHoardStats(self):
        # Coin Counts
        CPCount = GlobalInst.GetStringVarAsNumber(self.CoinsEntryCPVar, Mode="Decimal")
        SPCount = GlobalInst.GetStringVarAsNumber(self.CoinsEntrySPVar, Mode="Decimal")
        EPCount = GlobalInst.GetStringVarAsNumber(self.CoinsEntryEPVar, Mode="Decimal")
        GPCount = GlobalInst.GetStringVarAsNumber(self.CoinsEntryGPVar, Mode="Decimal")
        PPCount = GlobalInst.GetStringVarAsNumber(self.CoinsEntryPPVar, Mode="Decimal")
        TotalCoinCount = CPCount + SPCount + EPCount + GPCount + PPCount

        # Coin Value
        CoinValue = Decimal(0)
        CoinValue += CPCount * self.ValueCP
        CoinValue += SPCount * self.ValueSP
        CoinValue += EPCount * self.ValueEP
        CoinValue += GPCount * self.ValueGP
        CoinValue += PPCount * self.ValuePP
        self.StatsCoinsValueEntryVar.set(str(CoinValue.quantize(Decimal("0.01"))))

        # Coin Weight
        CoinWeight = Decimal(TotalCoinCount * self.WeightPerCoin)
        self.StatsCoinsWeightEntryVar.set(str(CoinWeight.quantize(Decimal("0.01"))))

        # Weights and Values
        Weights = {}
        Weights["Total"] = Decimal(0)
        Weights["Coins"] = Decimal(0)
        Weights["TreasureItems"] = Decimal(0)
        Weights[""] = Decimal(0)

        Values = {}
        Values["Total"] = Decimal(0)
        Values["Coins"] = Decimal(0)
        Values["TreasureItems"] = Decimal(0)
        Values[""] = Decimal(0)

        # Add Coins to Total Weight and Value
        Weights["Total"] += CoinWeight
        Values["Total"] += CoinValue

        # Loop Through Inventory List
        for Entry in self.TreasureItemEntriesList:
            # Set Up Local Variables
            Count = GlobalInst.GetStringVarAsNumber(Entry.CountEntryVar)
            ValueDenomination = Entry.UnitValueDenominationVar.get()

            # Total Weight and Value
            TotalItemWeight = GlobalInst.GetStringVarAsNumber(Entry.UnitWeightEntryVar, Mode="Decimal") * Decimal(Count)
            TotalItemValue = GlobalInst.GetStringVarAsNumber(Entry.UnitValueEntryVar, Mode="Decimal") * Decimal(Count)

            # Calculate Value in GP
            TotalItemValue *= self.DenominationValues[ValueDenomination]

            Entry.TotalWeightEntryVar.set(str(TotalItemWeight.quantize(Decimal("0.01"))))
            Entry.TotalValueEntryVar.set(str(TotalItemValue.quantize(Decimal("0.01"))))

            # Totals
            Weights["Total"] += TotalItemWeight
            Values["Total"] += TotalItemValue
            Weights["TreasureItems"] += TotalItemWeight
            Values["TreasureItems"] += TotalItemValue

        # Set Entries
        self.StatsTotalWeightEntryVar.set(str(Weights["Total"].quantize(Decimal("0.01"))))
        self.StatsItemsWeightEntryVar.set(str(Weights["TreasureItems"].quantize(Decimal("0.01"))))
        self.StatsTotalValueEntryVar.set(str(Values["Total"].quantize(Decimal("0.01"))))
        self.StatsItemsValueEntryVar.set(str(Values["TreasureItems"].quantize(Decimal("0.01"))))

    def Sort(self, Column, Reverse=False, SearchMode=False):
        # List to Sort
        ListToSort = []

        if SearchMode:
            # Get Search String
            SearchStringPrompt = StringPrompt(WindowInst, "Search", "What do you want to search for?")
            WindowInst.wait_window(SearchStringPrompt.Window)
            if SearchStringPrompt.DataSubmitted.get():
                SearchString = SearchStringPrompt.StringEntryVar.get()
            else:
                return

            # Add Fields to List
            for CurrentEntry in self.TreasureItemEntriesList:
                ListToSort.append((CurrentEntry, CurrentEntry.SortFields[Column].get().lower()))

            # Sort the List
            SortedList = sorted(ListToSort, key=lambda x: (x[1] == "", SearchString not in x[1]))
        else:
            if Column == "Name":
                # Add Fields to List
                for CurrentEntry in self.TreasureItemEntriesList:
                    ListToSort.append((CurrentEntry, CurrentEntry.SortFields[Column].get()))

                # Sort the List
                SortedList = sorted(ListToSort, key=lambda x: ((not Reverse and x[1] == "") or (Reverse and x[1] != ""), x[1].lower()), reverse=Reverse)
            elif Column == "Count" or Column == "Sort Order":
                # Add Fields to List
                for CurrentEntry in self.TreasureItemEntriesList:
                    ListToSort.append((CurrentEntry, GlobalInst.GetStringVarAsNumber(CurrentEntry.SortFields[Column])))

                # Sort the List
                SortedList = sorted(ListToSort, key=lambda x: ((not Reverse and x[1] == 0) or (Reverse and x[1] != 0), x[1]), reverse=Reverse)
            elif Column == "Unit Value":
                # Add Fields to List
                for CurrentEntry in self.TreasureItemEntriesList:
                    ListToSort.append((CurrentEntry, CurrentEntry.SortFields["Name"].get(), max(1, GlobalInst.GetStringVarAsNumber(CurrentEntry.SortFields["Count"])),
                                       GlobalInst.GetStringVarAsNumber(CurrentEntry.SortFields["Total Value"], Mode="Float")))

                # Sort the List
                SortedList = sorted(ListToSort, key=lambda x: ((not Reverse and x[1] == "") or (Reverse and x[1] != ""), x[3] / x[2]), reverse=Reverse)
            elif Column == "Value Denomination":
                # Add Fields to List
                for CurrentEntry in self.TreasureItemEntriesList:
                    ListToSort.append((CurrentEntry, CurrentEntry.SortFields["Name"].get(), CurrentEntry.SortFields[Column].get()))

                # Sort the List
                SortedList = sorted(ListToSort, key=lambda x: ((not Reverse and x[1] == "") or (Reverse and x[1] != ""), x[2].lower()), reverse=Reverse)
            elif Column == "Total Weight" or Column == "Total Value" or Column == "Unit Weight":
                # Add Fields to List
                for CurrentEntry in self.TreasureItemEntriesList:
                    ListToSort.append((CurrentEntry, CurrentEntry.SortFields["Name"].get(), GlobalInst.GetStringVarAsNumber(CurrentEntry.SortFields[Column], Mode="Float")))

                # Sort the List
                SortedList = sorted(ListToSort, key=lambda x: ((not Reverse and x[1] == "") or (Reverse and x[1] != ""), x[2]), reverse=Reverse)
            else:
                return

        # Adjust Entries to New Order
        for CurrentIndex in range(len(SortedList)):
            SortedList[CurrentIndex][0].Display(CurrentIndex + 1)

        # Flag Save Prompt
        SavingAndOpeningInst.SavePrompt = True

        # Update Window Title
        WindowInst.UpdateWindowTitle()

    def OpenCoinCalculator(self):
        # Create Coin Calculator Window and Wait
        self.CoinCalculatorInst = CoinCalculator(WindowInst, DialogMode=True)
        WindowInst.wait_window(self.CoinCalculatorInst.Window)

    class TreasureItemEntry:
        def __init__(self, master, List, ScrollingDisabledVar, SortOrderValuesList, Row):
            # Store Parameters
            self.master = master
            self.ScrollingDisabledVar = ScrollingDisabledVar
            self.SortOrderValuesList = SortOrderValuesList
            self.Row = Row

            # Variables
            self.NameEntryVar = SavedStringVar()
            self.CountEntryVar = SavedStringVar()
            self.CountEntryVar.trace_add("write", lambda a, b, c: HoardSheetInst.UpdateHoardStats())
            self.UnitWeightEntryVar = SavedStringVar()
            self.UnitWeightEntryVar.trace_add("write", lambda a, b, c: HoardSheetInst.UpdateHoardStats())
            self.UnitValueEntryVar = SavedStringVar()
            self.UnitValueEntryVar.trace_add("write", lambda a, b, c: HoardSheetInst.UpdateHoardStats())
            self.UnitValueDenominationVar = SavedStringVar()
            self.UnitValueDenominationVar.trace_add("write", lambda a, b, c: HoardSheetInst.UpdateHoardStats())
            self.TotalWeightEntryVar = StringVar()
            self.TotalValueEntryVar = StringVar()
            self.CategoryEntryVar = SavedStringVar()
            self.RarityEntryVar = SavedStringVar()
            self.DescriptionVar = SavedStringVar()
            self.SortOrderVar = SavedStringVar()

            # Item Description Vars
            self.ItemDescriptionVars = {}
            self.ItemDescriptionVars["NameEntryVar"] = self.NameEntryVar
            self.ItemDescriptionVars["CategoryEntryVar"] = self.CategoryEntryVar
            self.ItemDescriptionVars["RarityEntryVar"] = self.RarityEntryVar
            self.ItemDescriptionVars["DescriptionVar"] = self.DescriptionVar

            # Sort Fields
            self.SortFields = {}
            self.SortFields["Name"] = self.NameEntryVar
            self.SortFields["Count"] = self.CountEntryVar
            self.SortFields["Unit Weight"] = self.UnitWeightEntryVar
            self.SortFields["Unit Value"] = self.UnitValueEntryVar
            self.SortFields["Value Denomination"] = self.UnitValueDenominationVar
            self.SortFields["Total Weight"] = self.TotalWeightEntryVar
            self.SortFields["Total Value"] = self.TotalValueEntryVar
            self.SortFields["Sort Order"] = self.SortOrderVar

            # Add to List
            List.append(self)

            # Name Entry
            self.NameEntry = EntryExtended(master, width=35, textvariable=self.NameEntryVar, justify=CENTER, bg=GlobalInst.ButtonColor)
            self.NameEntry.bind("<Button-3>", self.ConfigureItemDescription)
            self.NameEntry.bind("<Shift-Button-3>", self.ExchangeForCoins)
            self.NameTooltip = Tooltip(self.NameEntry, "Right-click on the name field to set an item description.  Shift+right-click to exchange for coins.")

            # Count Entry
            self.CountEntry = InventoryCountEntry(master, width=4, textvariable=self.CountEntryVar, justify=CENTER)

            # Unit Weight Entry
            self.UnitWeightEntry = InventoryWeightEntry(master, width=4, textvariable=self.UnitWeightEntryVar, justify=CENTER)

            # Unit Value Entry
            self.UnitValueEntry = InventoryValueEntry(master, width=4, textvariable=self.UnitValueEntryVar, justify=CENTER)

            # Unit Value Denomination
            self.UnitValueDenomination = DropdownExtended(master, textvariable=self.UnitValueDenominationVar, values=["", "cp", "sp", "ep", "gp", "pp"], width=2, state="readonly", justify=CENTER)
            self.UnitValueDenomination.bind("<Enter>", self.DisableScrolling)
            self.UnitValueDenomination.bind("<Leave>", self.EnableScrolling)

            # Total Weight Entry
            self.TotalWeightEntry = EntryExtended(master, width=4, textvariable=self.TotalWeightEntryVar, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow")

            # Total Value Entry
            self.TotalValueEntry = EntryExtended(master, width=4, textvariable=self.TotalValueEntryVar, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow")

            # Sort Order
            self.SortOrder = DropdownExtended(master, textvariable=self.SortOrderVar, values=self.SortOrderValuesList, width=5, state="readonly", justify=CENTER)
            self.SortOrder.bind("<Enter>", self.DisableScrolling)
            self.SortOrder.bind("<Leave>", self.EnableScrolling)

        def DisableScrolling(self, event):
            self.ScrollingDisabledVar.set(True)

        def EnableScrolling(self, event):
            self.ScrollingDisabledVar.set(False)

        def ConfigureItemDescription(self, event):
            # Create Window and Wait
            ItemDescriptionMenuInst = self.ItemDescriptionMenu(WindowInst, self.ItemDescriptionVars)
            WindowInst.wait_window(ItemDescriptionMenuInst.Window)

            # Handle Variables
            if ItemDescriptionMenuInst.DataSubmitted.get():
                for Tag, Var in ItemDescriptionMenuInst.Vars.items():
                    self.ItemDescriptionVars[Tag].set(Var.get())

        def ExchangeForCoins(self, event):
            # Confirm
            ExchangeConfirm = messagebox.askyesno("Exchange for Coins", "Are you sure you want to exchange this item entry for coins?  This cannot be undone.")
            if not ExchangeConfirm:
                return

            # Get Var Values
            UnitValueDenom = self.UnitValueDenominationVar.get().upper()
            UnitValue = GlobalInst.GetStringVarAsNumber(self.UnitValueEntryVar)
            Count = GlobalInst.GetStringVarAsNumber(self.CountEntryVar)

            # Exchange If Valid
            if UnitValueDenom != "" and UnitValue > 0 and Count > 0:
                TotalValueGained = UnitValue * Count
                HoardSheetInst.SpendingCoins[UnitValueDenom].set(str(GlobalInst.GetStringVarAsNumber(HoardSheetInst.SpendingCoins[UnitValueDenom]) + TotalValueGained))
            else:
                messagebox.showerror("Invalid Exchange Value", "Unit values and counts must be positive and a denomination must be chosen to exchange an item entry for coins.")
                return

            # Set Entry to Defaults
            self.NameEntryVar.set("")
            self.CategoryEntryVar.set("")
            self.RarityEntryVar.set("")
            self.DescriptionVar.set("")
            self.CountEntryVar.set("")
            self.UnitWeightEntryVar.set("")
            self.UnitValueEntryVar.set("")
            self.UnitValueDenominationVar.set("")
            self.SortOrderVar.set("")

        def Display(self, Row):
            self.Row = Row

            # Set Row Size
            self.master.grid_rowconfigure(self.Row, minsize=26)

            # Place in Grid
            self.NameEntry.grid(row=self.Row, column=0, sticky=NSEW)
            self.CountEntry.grid(row=self.Row, column=1, sticky=NSEW)
            self.UnitWeightEntry.grid(row=self.Row, column=2, sticky=NSEW)
            self.UnitValueEntry.grid(row=self.Row, column=3, sticky=NSEW)
            self.UnitValueDenomination.grid(row=self.Row, column=4, sticky=NSEW)
            self.TotalWeightEntry.grid(row=self.Row, column=5, sticky=NSEW)
            self.TotalValueEntry.grid(row=self.Row, column=6, sticky=NSEW)
            self.SortOrder.grid(row=self.Row, column=7, sticky=NSEW)

            # Update Tab Order
            self.NameEntry.lift()
            self.CountEntry.lift()
            self.UnitWeightEntry.lift()
            self.UnitValueEntry.lift()
            self.UnitValueDenomination.lift()
            self.TotalWeightEntry.lift()
            self.TotalValueEntry.lift()
            self.SortOrder.lift()

            # Update Tags
            self.NameEntryVar.UpdateTag("TreasureItemListNameEntryVar" + str(self.Row))
            self.CountEntryVar.UpdateTag("TreasureItemListCountEntryVar" + str(self.Row))
            self.UnitWeightEntryVar.UpdateTag("TreasureItemListUnitWeightEntryVar" + str(self.Row))
            self.UnitValueEntryVar.UpdateTag("TreasureItemListUnitValueEntryVar" + str(self.Row))
            self.UnitValueDenominationVar.UpdateTag("TreasureItemListUnitValueDenominationVar" + str(self.Row))
            self.CategoryEntryVar.UpdateTag("TreasureItemListMagicItemCategoryEntryVar" + str(self.Row))
            self.RarityEntryVar.UpdateTag("TreasureItemListMagicItemRarityEntryVar" + str(self.Row))
            self.DescriptionVar.UpdateTag("TreasureItemListMagicItemDescriptionVar" + str(self.Row))
            self.SortOrderVar.UpdateTag("TreasureItemListSortOrderVar" + str(self.Row))

        class ItemDescriptionMenu:
            def __init__(self, master, ItemDescriptionVars):
                self.DataSubmitted = BooleanVar()
                self.Vars = {}
                self.Vars["NameEntryVar"] = StringVar(value=ItemDescriptionVars["NameEntryVar"].get())
                self.Vars["CategoryEntryVar"] = StringVar(value=ItemDescriptionVars["CategoryEntryVar"].get())
                self.Vars["RarityEntryVar"] = StringVar(value=ItemDescriptionVars["RarityEntryVar"].get())
                self.Vars["DescriptionVar"] = StringVar(value=ItemDescriptionVars["DescriptionVar"].get())

                # Create Window
                self.Window = Toplevel(master)
                self.Window.wm_attributes("-toolwindow", 1)
                self.Window.wm_title("Item Description")

                # Name Entry
                self.NameFrame = LabelFrame(self.Window, text="Name:")
                self.NameFrame.grid_columnconfigure(0, weight=1)
                self.NameFrame.grid(row=0, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                self.NameEntry = EntryExtended(self.NameFrame, justify=CENTER, width=35, textvariable=self.Vars["NameEntryVar"])
                self.NameEntry.grid(row=0, column=0, sticky=NSEW)

                # Category Entry
                self.CategoryFrame = LabelFrame(self.Window, text="Category:")
                self.CategoryFrame.grid_columnconfigure(0, weight=1)
                self.CategoryFrame.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)
                self.CategoryEntry = EntryExtended(self.CategoryFrame, justify=CENTER, textvariable=self.Vars["CategoryEntryVar"], width=15)
                self.CategoryEntry.grid(row=0, column=0, sticky=NSEW)

                # Rarity Entry
                self.RarityFrame = LabelFrame(self.Window, text="Rarity:")
                self.RarityFrame.grid_columnconfigure(0, weight=1)
                self.RarityFrame.grid(row=1, column=1, padx=2, pady=2, sticky=NSEW)
                self.RarityEntry = EntryExtended(self.RarityFrame, justify=CENTER, textvariable=self.Vars["RarityEntryVar"], width=15)
                self.RarityEntry.grid(row=0, column=0, sticky=NSEW)

                # Description Field
                self.DescriptionFrame = LabelFrame(self.Window, text="Description:")
                self.DescriptionFrame.grid(row=2, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                self.DescriptionField = ScrolledText(self.DescriptionFrame, Width=250, Height=300)
                self.DescriptionField.grid(row=0, column=0)
                self.DescriptionField.Text.insert(1.0, self.Vars["DescriptionVar"].get())

                # Buttons
                self.ButtonFrame = Frame(self.Window)
                self.ButtonFrame.grid_columnconfigure(0, weight=1)
                self.ButtonFrame.grid_columnconfigure(1, weight=1)
                self.ButtonFrame.grid(row=3, column=0, columnspan=2, sticky=NSEW)
                self.SubmitButton = Button(self.ButtonFrame, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
                self.SubmitButton.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)
                self.CancelButton = Button(self.ButtonFrame, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
                self.CancelButton.grid(row=0, column=1, padx=2, pady=2, sticky=NSEW)

                # Prevent Main Window Input
                self.Window.grab_set()

                # Handle Config Window Geometry and Focus
                GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst)
                self.Window.focus_force()

                # Focus on Name Entry
                self.NameEntry.focus_set()

            def Submit(self):
                self.DataSubmitted.set(True)
                self.Vars["DescriptionVar"].set(self.DescriptionField.get())
                self.Window.destroy()

            def Cancel(self):
                self.DataSubmitted.set(False)
                self.Window.destroy()


class MenuBar:
    def __init__(self, master):
        # Menu Bar
        self.MenuBar = Menu(master)
        master.config(menu=self.MenuBar)

        # File Menu
        self.FileMenu = Menu(self.MenuBar, tearoff=0)
        self.FileMenu.add_command(label="New", command=SavingAndOpeningInst.NewButton, accelerator="Ctrl+N")
        WindowInst.bind("<Control-n>", lambda event: SavingAndOpeningInst.NewButton())
        self.FileMenu.add_command(label="Open", command=SavingAndOpeningInst.OpenButton, accelerator="Ctrl+O")
        WindowInst.bind("<Control-o>", lambda event: SavingAndOpeningInst.OpenButton())
        self.FileMenu.add_separator()
        self.FileMenu.add_command(label="Save", command=SavingAndOpeningInst.SaveButton, accelerator="Ctrl+S")
        WindowInst.bind("<Control-s>", lambda event: SavingAndOpeningInst.SaveButton())
        self.FileMenu.add_command(label="Save As", command=lambda: SavingAndOpeningInst.SaveButton(SaveAs=True), accelerator="Ctrl+Shift+S")
        WindowInst.bind("<Control-S>", lambda event: SavingAndOpeningInst.SaveButton(SaveAs=True))
        if WindowInst.Mode == "NPCSheet":
            self.FileMenu.add_separator()
            self.FileMenu.add_command(label="Import Creature Data", command=CreatureDataInst.Import)
            self.FileMenu.add_command(label="Export Creature Data", command=CreatureDataInst.Export)
        if WindowInst.Mode in ["EncounterManager", "CharacterSheet", "NPCSheet"]:
            self.FileMenu.add_separator()
            self.FileMenu.add_command(label="Import Dice Roller Data", command=SavingAndOpeningInst.ImportDiceRoller)
            self.FileMenu.add_command(label="Export Dice Roller Data", command=SavingAndOpeningInst.ExportDiceRoller)
        self.FileMenu.add_separator()
        self.FileMenu.add_command(label="Exit", command=lambda: WindowInst.CloseWindow(CheckForSave=True))
        self.MenuBar.add_cascade(label="File", menu=self.FileMenu)

        if WindowInst.Mode == "CharacterSheet":
            # Commands Menu
            self.CommandsMenu = Menu(self.MenuBar, tearoff=0)
            self.CommandsMenu.add_command(label="Update Stats and Inventory", command=CharacterSheetInst.UpdateStatsAndInventory, accelerator="Ctrl+D")
            WindowInst.bind("<Control-d>", lambda event: CharacterSheetInst.UpdateStatsAndInventory())
            self.CommandsMenu.add_separator()
            self.CommandsMenu.add_command(label="Clear Inventory", command=Inst["Inventory"].Clear)
            self.MenuBar.add_cascade(label="Commands", menu=self.CommandsMenu)

            # Coin Calculator
            self.MenuBar.add_command(label="Coin Calculator", command=Inst["Inventory"].OpenCoinCalculator)

            # Settings Menu
            self.MenuBar.add_command(label="Settings", command=CharacterSheetInst.Settings)

        if WindowInst.Mode == "HoardSheet":
            self.MenuBar.add_command(label="Coin Calculator", command=HoardSheetInst.OpenCoinCalculator)

        if WindowInst.Mode == "NPCSheet":
            # Update Stats Button
            self.MenuBar.add_command(label="Update Stats (Ctrl+D)", command=CreatureDataInst.UpdateStats)
            WindowInst.bind("<Control-d>", lambda event: CreatureDataInst.UpdateStats())


class StatusBar:
    def __init__(self, master):
        # Configure Mode Parameters
        if WindowInst.Mode == "CreatureDataUtility":
            self.Row = 1
            self.Column = 0
            self.ColumnSpan = 1
        if WindowInst.Mode == "DiceRoller":
            self.Row = 1
            self.Column = 0
            self.ColumnSpan = 1
        elif WindowInst.Mode == "EncounterManager":
            self.Row = 2
            self.Column = 0
            self.ColumnSpan = 2
        elif WindowInst.Mode == "CompactInitiativeOrder":
            self.Row = 1
            self.Column = 0
            self.ColumnSpan = 1
        elif WindowInst.Mode == "CharacterSheet":
            self.Row = 1
            self.Column = 0
            self.ColumnSpan = 2
        elif WindowInst.Mode == "NPCSheet":
            self.Row = 1
            self.Column = 0
            self.ColumnSpan = 2
        elif WindowInst.Mode == "HoardSheet":
            self.Row = 1
            self.Column = 0
            self.ColumnSpan = 2

        # Variables
        self.StatusBarTextVar = StringVar(value="Status")
        self.StatusBarLockedVar = BooleanVar(value=False)

        # Status Bar Frame
        self.StatusBarFrame = Frame(master, bg="gray", bd=1, relief=SUNKEN)
        self.StatusBarFrame.grid_columnconfigure(0, weight=1)
        self.StatusBarFrame.grid(row=self.Row, column=self.Column, columnspan=self.ColumnSpan, sticky=NSEW, padx=2, pady=2)

        # Status Bar Label
        self.StatusBarLabel = Label(self.StatusBarFrame, textvariable=self.StatusBarTextVar, fg="white", bg="gray")
        self.StatusBarLabel.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)

    def StatusBarSetText(self, Text, Lock=False, Unlock=False):
        if not Lock and not Unlock:
            if not self.StatusBarLockedVar.get():
                pass
            else:
                return
        if Lock:
            self.StatusBarLockedVar.set(True)
        if Unlock:
            self.StatusBarLockedVar.set(False)
        self.StatusBarTextVar.set(Text)

    def FlashStatus(self, Text, Duration=2000):
        StatusBarInst.StatusBarSetText(Text, Lock=True)
        WindowInst.after(Duration, lambda: self.StatusBarSetText("Status", Unlock=True))


# Scrolled Text
class ScrolledText:
    def __init__(self, master, Width=100, Height=100, Disabled=False, DisabledBackground="light gray", FontSize=None, SavedDataTag=None):
        self.Width = Width
        self.Height = Height
        self.Disabled = Disabled
        self.FontSize = FontSize
        self.SavedDataTag = SavedDataTag

        # Scrolled Text Frame
        self.ScrolledTextFrame = Frame(master, width=self.Width, height=self.Height)
        self.ScrolledTextFrame.pack_propagate(False)
        self.ScrolledTextFrame.grid_propagate(False)

        # Scrollbar
        self.Scrollbar = Scrollbar(self.ScrolledTextFrame, orient=VERTICAL)
        self.Scrollbar.pack(side=RIGHT, fill=Y)

        # Text Widget
        self.Text = self.TrackableText(self.ScrolledTextFrame, wrap=WORD)
        self.Text.pack(side=LEFT, expand=YES, fill=BOTH)
        if self.Disabled:
            self.Text.configure(state=DISABLED, bg=DisabledBackground, cursor="arrow")
        if self.FontSize != None:
            self.Text.configure(font=font.Font(size=self.FontSize))

        # Set Up Scrolling
        self.Text.configure(yscrollcommand=self.Scrollbar.set)
        self.Scrollbar.configure(command=self.Text.yview)

        # Add to Saved Data Dictionary
        if self.SavedDataTag is not None:
            SavingAndOpeningInst.SavedData[self.SavedDataTag] = self

    def get(self):
        return self.Text.get("1.0", "end-1c")

    def set(self, Content):
        if self.Disabled:
            self.Text.configure(state=NORMAL)
        self.Text.delete("1.0", END)
        self.Text.insert("1.0", Content)
        if self.Disabled:
            self.Text.configure(state=DISABLED)

    def grid(self, *args, **kwargs):
        self.ScrolledTextFrame.grid(*args, **kwargs)

    def pack(self, *args, **kwargs):
        self.ScrolledTextFrame.pack(*args, **kwargs)

    def lift(self, *args, **kwargs):
        self.ScrolledTextFrame.lift(*args, **kwargs)

    def UpdateTag(self, Tag):
        self.SavedDataTag = Tag
        SavingAndOpeningInst.SavedData[self.SavedDataTag] = self

    class TrackableText(Text):
        def __init__(self, *args, **kwargs):
            # Init Text
            Text.__init__(self, *args, **kwargs)

            # Create Proxy
            self._orig = self._w + "_orig"
            self.tk.call("rename", self._w, self._orig)
            self.tk.createcommand(self._w, self._proxy)

            # Intercept Events
            GlobalInst.InterceptEvents(self)

            # Create Indent Tags
            self.IndentValue = 15
            self.IndentLevels = 10
            for IndentLevel in range(1, self.IndentLevels + 1):
                self.tag_configure("INDENT" + str(IndentLevel), lmargin1=self.IndentValue * IndentLevel, lmargin2=self.IndentValue * IndentLevel)

        def _proxy(self, command, *args):
            try:
                cmd = (self._orig, command) + args
                result = self.tk.call(cmd)
                if command in ("insert", "delete", "replace"):
                    self.event_generate("<<TextModified>>")
                    self.FormatIndentations()
                return result
            except TclError:
                pass

        def FormatIndentations(self):
            for IndentLevel in range(1, self.IndentLevels + 1):
                # Get Current Tag
                CurrentTag = "INDENT" + str(IndentLevel)
                self.tag_remove(CurrentTag, "1.0", END)

                # Search Text and Add Tags to Matching Lines
                SearchPattern = "*" * IndentLevel
                SearchStart = 1.0
                while True:
                    # Get Match Index
                    MatchIndex = self.search(SearchPattern, SearchStart, END)

                    # No Match Index; Break Loop
                    if not MatchIndex:
                        break

                    # Apply Tag to MatchIndex Line
                    LineStart = MatchIndex + " linestart"
                    LineEnd = MatchIndex + " lineend"
                    if self.compare(MatchIndex, "==", LineStart):
                        self.tag_add(CurrentTag, LineStart, LineEnd)

                    # Move SearchStart Index to Next Character for Next Loop
                    SearchStart = MatchIndex + " + 1 char"


# Scrolled Canvas
class ScrolledCanvas:
    def __init__(self, master, Height=100, Width=100, ScrollingDisabledVar=None, TopMode=False):
        self.Height = Height
        self.Width = Width
        self.ScrollingDisabledVar = ScrollingDisabledVar

        # Canvas
        self.Canvas = Canvas(master, highlightthickness=0, height=self.Height, width=self.Width)
        self.Canvas.grid(row=0, column=0, sticky=NSEW)
        self.VerticalScrollbar = Scrollbar(master, orient=VERTICAL, command=self.Canvas.yview)
        self.VerticalScrollbar.grid(row=0, column=1, sticky=NSEW)
        self.WindowFrame = Frame(self.Canvas)
        self.Canvas.create_window((0, 0), window=self.WindowFrame, anchor=NW)
        self.Canvas.config(yscrollcommand=self.VerticalScrollbar.set)
        self.Canvas.bind("<Configure>", lambda event: self.ConfigureScrolledCanvas())

        # Top Mode
        if TopMode:
            self.HorizontalScrollbar = Scrollbar(master, orient=HORIZONTAL, command=self.Canvas.xview)
            self.HorizontalScrollbar.grid(row=1, column=0, sticky=NSEW)
            self.Canvas.config(xscrollcommand=self.HorizontalScrollbar.set)

    def ConfigureScrolledCanvas(self):
        self.Canvas.configure(scrollregion=self.Canvas.bbox("all"))

    def BindEnterAndLeaveToBindMouseWheel(self):
        self.WindowFrame.bind("<Enter>", self.BindMouseWheel)
        self.WindowFrame.bind("<Leave>", self.UnbindMouseWheel)

    def MouseWheelEvent(self, event):
        if self.ScrollingDisabledVar != None:
            if not self.ScrollingDisabledVar.get():
                pass
            else:
                return
        if event.delta > 0:
            ScrollDistance = 1
        elif event.delta < 0:
            ScrollDistance = -1
        else:
            ScrollDistance = 0
        self.Canvas.yview_scroll(int(-1 * ScrollDistance), "units")

    def BindMouseWheel(self, event):
        if GlobalInst.OS == "Windows" or GlobalInst.OS == "Darwin":
            WindowInst.bind("<MouseWheel>", self.MouseWheelEvent)
        elif GlobalInst.OS == "Linux":
            WindowInst.bind("<Button-4>", self.MouseWheelEvent)
            WindowInst.bind("<Button-5>", self.MouseWheelEvent)

    def UnbindMouseWheel(self, event):
        WindowInst.unbind("<MouseWheel>")


# Extended Entry Widgets
class EntryExtended(Entry):
    def __init__(self, *args, **kwargs):
        Entry.__init__(self, *args, **kwargs)

        # Intercept Bindings
        GlobalInst.InterceptEvents(self)

    def ConfigureValidation(self, ValidationFunction, ValidationTrigger):
        self.ValidationCommand = self.register(ValidationFunction)
        self.configure(validate=ValidationTrigger, validatecommand=(self.ValidationCommand, "%P"))


class CoinsEntry(EntryExtended):
    def __init__(self, *args, **kwargs):
        EntryExtended.__init__(self, *args, **kwargs)
        self.ConfigureValidation(lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Coins must be whole numbers.", MinValue=0, LessThanMinString="Coins cannot be less than 0."), "key")


class InventoryCountEntry(EntryExtended):
    def __init__(self, *args, **kwargs):
        EntryExtended.__init__(self, *args, **kwargs)
        self.ConfigureValidation(lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Inventory item counts must be whole numbers.", MinValue=0, LessThanMinString="Inventory item counts cannot be less than 0."), "key")


class InventoryWeightEntry(EntryExtended):
    def __init__(self, *args, **kwargs):
        EntryExtended.__init__(self, *args, **kwargs)
        self.ConfigureValidation(
            lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Inventory item unit weights must be numbers.", Mode="Float", MinValue=0, LessThanMinString="Inventory item unit weights cannot be less than 0."), "key")


class InventoryValueEntry(EntryExtended):
    def __init__(self, *args, **kwargs):
        EntryExtended.__init__(self, *args, **kwargs)
        self.ConfigureValidation(
            lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Inventory item unit values must be numbers.", Mode="Float", MinValue=0, LessThanMinString="Inventory item unit values cannot be less than 0."), "key")


class RoundEntry(EntryExtended):
    def __init__(self, *args, **kwargs):
        EntryExtended.__init__(self, *args, **kwargs)
        self.ConfigureValidation(lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Round must be a whole number.", MinValue=1, LessThanMinString="Round must be greater than 0."), "key")


class InitiativeEntry(EntryExtended):
    def __init__(self, *args, **kwargs):
        EntryExtended.__init__(self, *args, **kwargs)
        self.ConfigureValidation(lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Initiative roll must be a whole number."), "key")


class MaxHPDataEntry(EntryExtended):
    def __init__(self, *args, **kwargs):
        EntryExtended.__init__(self, *args, **kwargs)
        self.ConfigureValidation(lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "All max HP data must be in the form of whole numbers.", MinValue=0, LessThanMinString="Max HP data cannot be less than 0."), "key")


class StatModifierMultiplierEntry(EntryExtended):
    def __init__(self, *args, **kwargs):
        EntryExtended.__init__(self, *args, **kwargs)
        self.ConfigureValidation(lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Multipliers must be numbers", Mode="Float"), "key")


class StatModifierMinMaxEntry(EntryExtended):
    def __init__(self, *args, **kwargs):
        EntryExtended.__init__(self, *args, **kwargs)
        self.ConfigureValidation(lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Minimums and maximums must be whole numbers."), "key")


# Extended Dropdown Widget
class DropdownExtended(ttk.Combobox):
    def __init__(self, *args, **kwargs):
        ttk.Combobox.__init__(self, *args, **kwargs)

        # Autocompletion Variables
        self.CurrentInput = ""
        self.IDOfScheduledClear = None
        self.WaitTime = 2000
        self.InvalidKeySyms = ["Alt_L", "Alt_R", "Cancel", "Caps_Lock", "Control_L", "Control_R", "Delete", "Down", "End", "Escape", "Execute", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12", "Home",
                               "Insert", "Left", "Linefeed", "KP_Add", "KP_Begin", "KP_Decimal", "KP_Delete", "KP_Divide", "KP_Down", "KP_End", "KP_Enter", "KP_Home", "KP_Insert", "KP_Left", "KP_Multiply", "KP_Next", "KP_Prior",
                               "KP_Right", "KP_Subtract", "KP_Up", "Next", "Num_Lock", "Pause", "Print", "Prior", "Return", "Right", "Scroll_Lock", "Shift_L", "Shift_R", "Tab", "Up"]
        self.ValidChars = string.ascii_letters + string.digits + string.punctuation + " "

        # Bind KeyRelease
        self.bind("<Key>", self.KeyPressed)
        self.bind("<FocusIn>", self.GainedOrLostFocus)
        self.bind("<FocusOut>", self.GainedOrLostFocus)

    def KeyPressed(self, Event):
        KeySym = Event.keysym
        NewChar = Event.char
        if KeySym in self.InvalidKeySyms:
            return
        if KeySym == "BackSpace":
            if len(self.CurrentInput) > 0:
                self.CurrentInput = self.CurrentInput[:-1]
            self.MatchToInput()
        elif NewChar in self.ValidChars:
            self.CurrentInput += NewChar
            self.MatchToInput()
        self.UnscheduleClear()
        if len(self.CurrentInput) > 0:
            self.IDOfScheduledClear = self.after(self.WaitTime, self.ClearCurrentInput)

    def GainedOrLostFocus(self, Event):
        self.UnscheduleClear()
        self.ClearCurrentInput()

    def MatchToInput(self):
        for Element in self["values"]:
            if Element.lower().startswith(self.CurrentInput.lower()):
                self.set(Element)
                break

    def UnscheduleClear(self):
        if self.IDOfScheduledClear:
            self.after_cancel(self.IDOfScheduledClear)
            self.IDOfScheduledClear = None

    def ClearCurrentInput(self):
        self.CurrentInput = ""
        if self.IDOfScheduledClear:
            self.IDOfScheduledClear = None


# Prompts
class IntegerPrompt:
    def __init__(self, master, WindowTitle, Header, MinValue=None, MaxValue=None):
        # Store Parameters
        self.WindowTitle = WindowTitle
        self.Header = Header
        self.MinValue = MinValue
        self.MaxValue = MaxValue

        # Variables
        self.DataSubmitted = BooleanVar()
        self.IntegerEntryVar = StringVar()

        # Create Window
        self.Window = Toplevel(master)
        self.Window.wm_attributes("-toolwindow", 1)
        self.Window.wm_title(self.WindowTitle)

        # Table Frame
        self.TableFrame = Frame(self.Window)
        self.TableFrame.grid(row=0, column=0, sticky=NSEW, columnspan=2)

        # Integer Entry
        self.IntegerHeader = Label(self.TableFrame, text=self.Header, bd=2, relief=GROOVE)
        self.IntegerHeader.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
        self.IntegerEntry = EntryExtended(self.TableFrame, width=20, textvariable=self.IntegerEntryVar, justify=CENTER)
        self.IntegerEntry.ConfigureValidation(self.ValidEntry, "key")
        self.IntegerEntry.grid(row=1, column=2, sticky=NSEW, padx=2, pady=2)
        self.IntegerEntry.bind("<Return>", lambda event: self.Submit())

        # Submit Button
        self.SubmitButton = Button(self.Window, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
        self.SubmitButton.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)

        # Cancel Button
        self.CancelButton = Button(self.Window, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
        self.CancelButton.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)

        # Prevent Main Window Input
        self.Window.grab_set()

        # Handle Config Window Geometry and Focus
        GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst)
        self.Window.focus_force()

        # Focus On Entry
        self.IntegerEntry.focus_set()

    def Submit(self):
        self.DataSubmitted.set(True)
        self.Window.destroy()

    def Cancel(self):
        self.DataSubmitted.set(False)
        self.Window.destroy()

        return None

    def GetData(self):
        return GlobalInst.GetStringVarAsNumber(self.IntegerEntryVar)

    def ValidEntry(self, NewText):
        return GlobalInst.ValidateNumberFromString(NewText, "Must be a whole number.", MinValue=self.MinValue, LessThanMinString="Must be at least " + str(self.MinValue) + ".", MaxValue=self.MaxValue,
                                                   MoreThanMaxString="Must be no more than " + str(self.MaxValue) + ".")


class StringPrompt:
    def __init__(self, master, WindowTitle, Header):
        # Store Parameters
        self.WindowTitle = WindowTitle
        self.Header = Header

        # Variables
        self.DataSubmitted = BooleanVar()
        self.StringEntryVar = StringVar()

        # Create Window
        self.Window = Toplevel(master)
        self.Window.wm_attributes("-toolwindow", 1)
        self.Window.wm_title(self.WindowTitle)

        # Table Frame
        self.TableFrame = Frame(self.Window)
        self.TableFrame.grid(row=0, column=0, sticky=NSEW, columnspan=2)

        # Integer Entry
        self.StringHeader = Label(self.TableFrame, text=self.Header, bd=2, relief=GROOVE)
        self.StringHeader.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
        self.StringEntry = EntryExtended(self.TableFrame, width=20, textvariable=self.StringEntryVar, justify=CENTER)
        self.StringEntry.grid(row=1, column=2, sticky=NSEW, padx=2, pady=2)
        self.StringEntry.bind("<Return>", lambda event: self.Submit())

        # Submit Button
        self.SubmitButton = Button(self.Window, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
        self.SubmitButton.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)

        # Cancel Button
        self.CancelButton = Button(self.Window, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
        self.CancelButton.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)

        # Prevent Main Window Input
        self.Window.grab_set()

        # Handle Config Window Geometry and Focus
        GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst)
        self.Window.focus_force()

        # Focus On Entry
        self.StringEntry.focus_set()

    def Submit(self):
        self.DataSubmitted.set(True)
        self.Window.destroy()

    def Cancel(self):
        self.DataSubmitted.set(False)
        self.Window.destroy()

        return None

    def GetData(self):
        return GlobalInst.GetStringVarAsNumber(self.StringEntryVar)


class OpenErrorsPrompt:
    def __init__(self, master, ErrorString):
        # Store Parameters
        self.ErrorString = ErrorString

        # Create Window
        self.Window = Toplevel(master)
        self.Window.wm_attributes("-toolwindow", 1)
        self.Window.wm_title("Open Errors")

        # Description Label
        self.DescriptionLabel = Label(self.Window, text="Some data in the file could not be opened.  This could be due to changes in the file format.", bd=2, relief=GROOVE)
        self.DescriptionLabel.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Unopened Data
        self.UnopenedDataFrame = LabelFrame(self.Window, text="Unopened Data:")
        self.UnopenedDataFrame.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
        self.UnopenedDataField = ScrolledText(self.UnopenedDataFrame, Width=500, Height=200, Disabled=True)
        self.UnopenedDataField.set(self.ErrorString)
        self.UnopenedDataField.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Buttons
        self.ButtonsFrame = Frame(self.Window)
        self.ButtonsFrame.grid_columnconfigure(0, weight=1)
        self.ButtonsFrame.grid_columnconfigure(1, weight=1)
        self.ButtonsFrame.grid(row=2, column=0, sticky=NSEW)
        self.OKButton = Button(self.ButtonsFrame, text="OK", command=self.OK, bg=GlobalInst.ButtonColor)
        self.OKButton.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
        self.CopyToClipboardButton = Button(self.ButtonsFrame, text="Copy", command=self.CopyToClipboard, bg=GlobalInst.ButtonColor)
        self.CopyToClipboardButton.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)

        # Prevent Main Window Input
        self.Window.grab_set()

        # Handle Config Window Geometry and Focus
        GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst)
        self.Window.focus_force()

    def CopyToClipboard(self):
        self.UnopenedDataField.Text.clipboard_clear()
        self.UnopenedDataField.Text.clipboard_append(self.ErrorString)
        StatusBarInst.FlashStatus("Unopened data copied to clipboard.")

    def OK(self):
        self.Window.destroy()


# Tooltips
class Tooltip:
    def __init__(self, Widget, Text):
        # Store Parameters
        self.Widget = Widget
        self.Text = Text
        self.ID = None
        self.TooltipWindow = None

        # Variables
        self.WaitTime = 1000
        self.WrapLength = 200

        # Bindings
        self.Widget.bind("<Enter>", lambda event: self.ScheduleTooltip())
        self.Widget.bind("<Leave>", lambda event: self.UnscheduleAndHideTooltip())
        self.Widget.bind("<ButtonPress>", lambda event: self.UnscheduleAndHideTooltip())

    def UnscheduleAndHideTooltip(self):
        if self.ID:
            self.Widget.after_cancel(self.ID)
            self.ID = None
        if self.TooltipWindow:
            self.TooltipWindow.destroy()
            self.TooltipWindow = None

    def ScheduleTooltip(self):
        self.ID = self.Widget.after(self.WaitTime, self.ShowTooltip)

    def ShowTooltip(self):
        # Position
        PositionX = WindowInst.winfo_pointerx() + 15
        PositionY = WindowInst.winfo_pointery() + 15

        # Create and Configure Tooltip Window
        self.TooltipWindow = Toplevel(self.Widget)
        self.TooltipWindow.wm_overrideredirect(True)
        self.TooltipWindow.wm_geometry("+" + str(PositionX) + "+" + str(PositionY))

        # Create Label
        TooltipLabel = Label(self.TooltipWindow, text=self.Text, justify=LEFT, background="white", relief=SOLID, bd=1, wraplength=self.WrapLength)
        TooltipLabel.grid(row=0, column=0, ipadx=1, ipady=1)


# Mode Select
class ModeSelect(Tk):
    def __init__(self):
        # Create Window
        Tk.__init__(self)

        # Configure Window
        self.wm_title("Select Mode - " + GlobalInst.ScriptName)
        GlobalInst.WindowIcon(self)
        self.ColumnWidth = 250
        self.grid_columnconfigure(0, minsize=self.ColumnWidth)
        self.grid_columnconfigure(1, minsize=self.ColumnWidth)

        # Variables
        self.ModeSelected = ""

        # Buttons Font
        self.ButtonsFont = font.Font(size=18)

        # Character Sheet Button
        self.CharacterSheetModeButton = Button(self, text="Character Sheet", command=lambda: self.SelectMode("CharacterSheet"), bg=GlobalInst.ButtonColor, font=self.ButtonsFont)
        self.CharacterSheetModeButton.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2, columnspan=2)

        # Hoard Sheet Button
        self.HoardSheetButton = Button(self, text="Hoard Sheet", command=lambda: self.SelectMode("HoardSheet"), bg=GlobalInst.ButtonColor, font=self.ButtonsFont)
        self.HoardSheetButton.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2, columnspan=2)

        # Dice Roller Button
        self.DiceRollerModeButton = Button(self, text="Dice Roller", command=lambda: self.SelectMode("DiceRoller"), bg=GlobalInst.ButtonColor, font=self.ButtonsFont)
        self.DiceRollerModeButton.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)

        # Encounter Manager Button
        self.EncounterManagerModeButton = Button(self, text="Encounter Manager", command=lambda: self.SelectMode("EncounterManager"), bg=GlobalInst.ButtonColor, font=self.ButtonsFont)
        self.EncounterManagerModeButton.grid(row=2, column=1, sticky=NSEW, padx=2, pady=2)

        # Compact Initiative
        self.CompactInitiativeModeButton = Button(self, text="Compact Initiative Order", command=lambda: self.SelectMode("CompactInitiativeOrder"), bg=GlobalInst.ButtonColor, font=self.ButtonsFont)
        self.CompactInitiativeModeButton.grid(row=3, column=0, sticky=NSEW, padx=2, pady=2)

        # NPC Sheet Button
        self.NPCSheetModeButton = Button(self, text="NPC Sheet", command=lambda: self.SelectMode("NPCSheet"), bg=GlobalInst.ButtonColor, font=self.ButtonsFont)
        self.NPCSheetModeButton.grid(row=3, column=1, sticky=NSEW, padx=2, pady=2)

        # Creature Data Utility Button
        self.CreatureDataUtilityModeButton = Button(self, text="Creature Data Utility", command=lambda: self.SelectMode("CreatureDataUtility"), bg=GlobalInst.ButtonColor, font=self.ButtonsFont)
        self.CreatureDataUtilityModeButton.grid(row=4, column=0, sticky=NSEW, padx=2, pady=2)

        # Coin Calculator Button
        self.CoinCalculatorModeButton = Button(self, text="Coin Calculator", command=lambda: self.SelectMode("CoinCalculator"), bg=GlobalInst.ButtonColor, font=self.ButtonsFont)
        self.CoinCalculatorModeButton.grid(row=4, column=1, sticky=NSEW, padx=2, pady=2)

        # Initial Window Behavior
        GlobalInst.WindowGeometry(self)
        self.focus_force()

        # Start Main Loop
        self.mainloop()

    def SelectMode(self, Mode):
        # Set Mode Variable
        self.ModeSelected = Mode

        # Destroy ModeSelect Window
        self.destroy()


# Window
class Window(Tk):
    def __init__(self, Mode, Title):
        # Store Parameters
        self.Mode = Mode

        # Create Window
        Tk.__init__(self)

        # Determine Screen Resolution and Offset
        self.ScreenWidth = self.winfo_screenwidth()
        self.ScreenHeight = self.winfo_screenheight()
        self.ScreenOffset = 200

        # Widget Master
        self.WidgetFrame = Frame(self)
        self.WidgetFrame.grid(row=0, column=0, sticky=NSEW)
        if self.ScreenWidth < MinimumResolutions[self.Mode][0] or self.ScreenHeight < MinimumResolutions[self.Mode][1]:
            self.WidgetCanvas = ScrolledCanvas(self.WidgetFrame, Height=self.ScreenHeight - self.ScreenOffset, Width=self.ScreenWidth - self.ScreenOffset, TopMode=True)
            self.WidgetMaster = self.WidgetCanvas.WindowFrame
            self.LowResolution = True
        else:
            self.WidgetMaster = self.WidgetFrame
            self.LowResolution = False

        # Configure Window
        self.wm_title(Title)
        GlobalInst.WindowIcon(self)
        self.option_add("*Font", "TkDefaultFont")

    def UpdateWindowTitle(self):
        # Prefix
        if self.Mode == "CreatureDataUtility" or self.Mode == "NPCSheet":
            Prefix = CreatureDataInst.NameEntryVar.get()
        elif self.Mode == "EncounterManager":
            Prefix = EncounterHeaderInst.EncounterNameEntryVar.get()
        elif self.Mode == "CharacterSheet":
            Prefix = CharacterSheetInst.CharacterNameEntryVar.get()
        elif self.Mode == "HoardSheet":
            Prefix = HoardSheetInst.HoardNameEntryVar.get()
        else:
            Prefix = ""
        if Prefix != "":
            Prefix += " - "

        # Current Open File and Save Prompt
        if self.Mode in ["CharacterSheet", "EncounterManager", "CreatureDataUtility", "DiceRoller", "NPCSheet", "HoardSheet"]:
            CurrentOpenFile = SavingAndOpeningInst.CurrentOpenFilePath.get()
            if CurrentOpenFile != "":
                CurrentOpenFile = " [" + os.path.basename(CurrentOpenFile) + "]"
            if SavingAndOpeningInst.SavePrompt:
                SavePromptString = " *"
            else:
                SavePromptString = ""
        else:
            CurrentOpenFile = ""
            SavePromptString = ""

        # Set Window Title
        self.wm_title(Prefix + WindowTitles[ModeSelectInst.ModeSelected] + CurrentOpenFile + SavePromptString)


if __name__ == "__main__":
    # Inst Dictionary
    Inst = {}

    # Global Variables and Functions
    GlobalInst = Global()

    # Mode Select
    ModeSelectInst = ModeSelect()

    # Validate Mode
    if ModeSelectInst.ModeSelected == "":
        sys.exit()

    # Window Titles
    WindowTitles = {}
    WindowTitles["CharacterSheet"] = "Character Sheet - " + GlobalInst.ScriptName
    WindowTitles["DiceRoller"] = "Dice Roller - " + GlobalInst.ScriptName
    WindowTitles["EncounterManager"] = "Encounter Manager - " + GlobalInst.ScriptName
    WindowTitles["CompactInitiativeOrder"] = "Compact Initiative Order - " + GlobalInst.ScriptName
    WindowTitles["CreatureDataUtility"] = "Creature Data Utility - " + GlobalInst.ScriptName
    WindowTitles["CoinCalculator"] = "Coin Calculator - " + GlobalInst.ScriptName
    WindowTitles["NPCSheet"] = "NPC Sheet - " + GlobalInst.ScriptName
    WindowTitles["HoardSheet"] = "Hoard Sheet - " + GlobalInst.ScriptName

    # Minimum Resolutions
    MinimumResolutions = {}
    MinimumResolutions["CharacterSheet"] = (1208, 712)
    MinimumResolutions["DiceRoller"] = (675, 451)
    MinimumResolutions["EncounterManager"] = (1331, 794)
    MinimumResolutions["CompactInitiativeOrder"] = (347, 613)
    MinimumResolutions["CreatureDataUtility"] = (802, 766)
    MinimumResolutions["CoinCalculator"] = (291, 216)
    MinimumResolutions["NPCSheet"] = (1262, 785)
    MinimumResolutions["HoardSheet"] = (957, 483)

    # Create Window
    WindowInst = Window(ModeSelectInst.ModeSelected, WindowTitles[ModeSelectInst.ModeSelected])

    # Populate Window
    if WindowInst.Mode == "CoinCalculator":
        CoinCalculatorInst = CoinCalculator(WindowInst.WidgetMaster)
    elif WindowInst.Mode == "CreatureDataUtility":
        StatusBarInst = StatusBar(WindowInst)
        SavingAndOpeningInst = SavingAndOpening()
        MenuBarInst = MenuBar(WindowInst)
        CreatureDataInst = CreatureData(WindowInst.WidgetMaster)
        SavingAndOpeningInst.TrackModifiedFields()
    elif WindowInst.Mode == "DiceRoller":
        StatusBarInst = StatusBar(WindowInst)
        SavingAndOpeningInst = SavingAndOpening()
        DiceRollerInst = DiceRoller(WindowInst.WidgetMaster)
        MenuBarInst = MenuBar(WindowInst)
        SavingAndOpeningInst.TrackModifiedFields()
    elif WindowInst.Mode == "EncounterManager":
        StatusBarInst = StatusBar(WindowInst)
        SavingAndOpeningInst = SavingAndOpening()
        EncounterHeaderInst = EncounterHeader(WindowInst.WidgetMaster)
        InitiativeOrderInst = InitiativeOrder(WindowInst.WidgetMaster)
        DiceRollerInst = DiceRoller(WindowInst.WidgetMaster)
        MenuBarInst = MenuBar(WindowInst)
        SavingAndOpeningInst.TrackModifiedFields()
    elif WindowInst.Mode == "CompactInitiativeOrder":
        StatusBarInst = StatusBar(WindowInst)
        CompactInitiativeOrderInst = CompactInitiativeOrder(WindowInst.WidgetMaster)
    elif WindowInst.Mode == "CharacterSheet":
        StatusBarInst = StatusBar(WindowInst)
        SavingAndOpeningInst = SavingAndOpening()
        CharacterSheetInst = CharacterSheet(WindowInst.WidgetMaster)
        DiceRollerInst = DiceRoller(WindowInst.WidgetMaster)
        MenuBarInst = MenuBar(WindowInst)
        SavingAndOpeningInst.TrackModifiedFields()
        GlobalInst.SetupStatModifiers()
        CharacterSheetInst.UpdateStatsAndInventory()
    elif WindowInst.Mode == "NPCSheet":
        StatusBarInst = StatusBar(WindowInst)
        SavingAndOpeningInst = SavingAndOpening()
        CreatureDataInst = CreatureData(WindowInst.WidgetMaster)
        DiceRollerInst = DiceRoller(WindowInst.WidgetMaster)
        MenuBarInst = MenuBar(WindowInst)
        SavingAndOpeningInst.TrackModifiedFields()
        GlobalInst.SetupStatModifiers()
    elif WindowInst.Mode == "HoardSheet":
        StatusBarInst = StatusBar(WindowInst)
        SavingAndOpeningInst = SavingAndOpening()
        HoardSheetInst = HoardSheet(WindowInst.WidgetMaster)
        MenuBarInst = MenuBar(WindowInst)
        SavingAndOpeningInst.TrackModifiedFields()
        HoardSheetInst.UpdateHoardStats()

    # Configure Window
    GlobalInst.WindowGeometry(WindowInst)
    if WindowInst.LowResolution:
        WindowInst.WidgetCanvas.ConfigureScrolledCanvas()
    WindowInst.focus_force()

    # Main Loop
    WindowInst.mainloop()
