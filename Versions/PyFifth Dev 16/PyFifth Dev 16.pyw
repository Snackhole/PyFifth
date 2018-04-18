# PyFifth is coded in Python 3.6.3 on Windows 10.  Earlier or later versions and other operating systems may or may not work.

import json
import math
import os
import platform
import random
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
        self.OS = platform.system()
        self.ButtonColor = "#F1F1D4"
        self.SortTooltipString = "Left-click/right-click to sort in ascending/descending order.  Shift+left-click to search."

    def GetStringVarAsNumber(self, Var, Mode="Int"):
        VarText = Var.get()
        if len(VarText) == 0:
            VarText = 0
        if Mode == "Int":
            return int(VarText)
        elif Mode == "Decimal":
            return Decimal(VarText)
        elif Mode == "Float":
            return float(VarText)

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
        if WindowInst.Mode is "CharacterSheet":
            self.StatModifierEntries["Strength"] = Inst["AbilitiesAndSavingThrows"].StrengthEntry.AbilityEntryModifierVar
            self.StatModifierEntries["Dexterity"] = Inst["AbilitiesAndSavingThrows"].DexterityEntry.AbilityEntryModifierVar
            self.StatModifierEntries["Constitution"] = Inst["AbilitiesAndSavingThrows"].ConstitutionEntry.AbilityEntryModifierVar
            self.StatModifierEntries["Intelligence"] = Inst["AbilitiesAndSavingThrows"].IntelligenceEntry.AbilityEntryModifierVar
            self.StatModifierEntries["Wisdom"] = Inst["AbilitiesAndSavingThrows"].WisdomEntry.AbilityEntryModifierVar
            self.StatModifierEntries["Charisma"] = Inst["AbilitiesAndSavingThrows"].CharismaEntry.AbilityEntryModifierVar
            self.StatModifierEntries["Proficiency"] = CharacterSheetInst.ProficiencyBonusEntryVar
        elif WindowInst.Mode is "NPCSheet":
            self.StatModifierEntries["Strength"] = CreatureDataInst.AbilitiesStrengthEntryVar
            self.StatModifierEntries["Dexterity"] = CreatureDataInst.AbilitiesDexterityEntryVar
            self.StatModifierEntries["Constitution"] = CreatureDataInst.AbilitiesConstitutionEntryVar
            self.StatModifierEntries["Intelligence"] = CreatureDataInst.AbilitiesIntelligenceEntryVar
            self.StatModifierEntries["Wisdom"] = CreatureDataInst.AbilitiesWisdomEntryVar
            self.StatModifierEntries["Charisma"] = CreatureDataInst.AbilitiesCharismaEntryVar
            self.StatModifierEntries["Proficiency"] = CreatureDataInst.ProficiencyEntryVar


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
                    if WindowMode is "CharacterSheet":
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
                if WindowMode is "CharacterSheet":
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
            if WindowMode is "CharacterSheet":
                CharacterSheetInst.UpdateStatsAndInventory()

            # NPC Sheet Stats
            if WindowMode is "NPCSheet":
                CreatureDataInst.UpdateStats()

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
        if WindowInst.Mode is "Encounter Manager":
            for Entry in InitiativeOrderInst.InitiativeEntriesList:
                if Entry.InitiativeEntryTurnDoneVar.get():
                    Entry.TurnDoneOn()
                else:
                    Entry.TurnDoneOff()
                if Entry.InitiativeEntryDeadVar.get():
                    Entry.DeadOn()
                else:
                    Entry.DeadOff()
        if WindowInst.Mode is "CharacterSheet":
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

        # Reset Saved Fields to Default Values
        for Field in SavingAndOpeningInst.SavedData.values():
            if WindowInst.Mode in ["DiceRoller", "EncounterManager", "CharacterSheet", "NPCSheet"]:
                if Field == DiceRollerInst.CritMinimumEntryVar:
                    Field.set("20")
                    continue
            if WindowInst.Mode is "CharacterSheet":
                if Field in [CharacterSheetInst.SpellcasterBoxVar, CharacterSheetInst.ConcentrationCheckPromptBoxVar, CharacterSheetInst.PortraitBoxVar]:
                    Field.set(True)
                    continue
            if type(Field) == BooleanVar:
                Field.set(False)
            else:
                Field.set("")

        # Dice Roller Defaults
        if WindowInst.Mode in ["DiceRoller", "EncounterManager", "CharacterSheet"]:
            DiceRollerInst.DiceNumberEntryVar.set("1")
            DiceRollerInst.DieTypeEntryVar.set("20")
            DiceRollerInst.ModifierEntryVar.set("0")

        # Encounter Manager Defaults
        if WindowInst.Mode is "EncounterManager":
            for Entry in InitiativeOrderInst.InitiativeEntriesList:
                Entry.TurnDoneOff()
                Entry.DeadOff()

        # Character Sheet Defaults
        if WindowInst.Mode is "CharacterSheet":
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

            # AC and Initiative to Default
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
        if WindowInst.Mode is "NPCSheet":
            # Set All Preset Roll Modifiers to Default Values
            for Entry in Inst["PresetRolls"].PresetRollsList:
                Entry.PresetRollModifierEntryStatModifierInst.DefaultValues()

        # No Current File
        self.CurrentOpenFilePath.set("")

        # No Save Prompt
        SavingAndOpeningInst.SavePrompt = False

        # Update Window Title
        WindowInst.UpdateWindowTitle()

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
        if WindowInst.Mode is "CharacterSheet":
            for Entry in Inst["PresetRolls"].PresetRollsList:
                Entry.PresetRollModifierEntryStatModifierInst.DefaultValues()

    # Field Tracking
    def TrackModifiedFields(self):
        for Field in self.SavedData.values():
            FieldType = type(Field)
            if FieldType == StringVar or FieldType == BooleanVar:
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


# Window Elements
class CharacterSheet:
    def __init__(self, master):
        # Variables
        self.CharacterNameEntryVar = StringVar()
        self.CharacterLevelEntryVar = StringVar()
        self.CharacterClassEntryVar = StringVar()
        self.CharacterExperienceEntryVar = StringVar()
        self.CharacterExperienceNeededEntryVar = StringVar()
        self.ProficiencyBonusEntryVar = StringVar()
        self.SpellcasterBoxVar = BooleanVar(value=True)
        self.ConcentrationCheckPromptBoxVar = BooleanVar(value=True)
        self.PortraitBoxVar = BooleanVar(value=True)
        self.JackOfAllTradesBoxVar = BooleanVar()
        self.RemarkableAthleteBoxVar = BooleanVar()
        self.ObservantBoxVar = BooleanVar()
        self.LuckyHalflingBoxVar = BooleanVar()

        # Character Sheet Frame
        self.CharacterSheetFrame = Frame(master)
        self.CharacterSheetFrame.grid(row=0, column=0, sticky=NSEW)

        # Character Sheet Header Frame
        self.CharacterSheetHeaderFrame = LabelFrame(self.CharacterSheetFrame, text="Basic Character Info:")
        self.CharacterSheetHeaderFrame.grid_columnconfigure(2, weight=1)
        self.CharacterSheetHeaderFrame.grid_columnconfigure(5, weight=1)
        self.CharacterSheetHeaderFrame.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Character Name
        self.CharacterNameLabel = Label(self.CharacterSheetHeaderFrame, text="Name:")
        self.CharacterNameLabel.grid(row=0, column=0, sticky=E)
        self.CharacterNameEntry = Entry(self.CharacterSheetHeaderFrame, textvariable=self.CharacterNameEntryVar, justify=CENTER, width=50)
        self.CharacterNameEntry.grid(row=0, column=1, sticky=E, padx=2, pady=2)

        # Class
        self.CharacterClassLabel = Label(self.CharacterSheetHeaderFrame, text="Class:")
        self.CharacterClassLabel.grid(row=1, column=0, sticky=E)
        self.CharacterClassEntry = Entry(self.CharacterSheetHeaderFrame, textvariable=self.CharacterClassEntryVar, justify=CENTER, width=50)
        self.CharacterClassEntry.grid(row=1, column=1, sticky=E, padx=2, pady=2)

        # Character Level
        self.CharacterLevelLabel = Label(self.CharacterSheetHeaderFrame, text="Level:")
        self.CharacterLevelLabel.grid(row=0, column=3, sticky=E)
        self.CharacterLevelEntry = Entry(self.CharacterSheetHeaderFrame, textvariable=self.CharacterLevelEntryVar, width=5, justify=CENTER)
        self.CharacterLevelEntry.grid(row=0, column=4, sticky=NSEW, padx=2, pady=2)

        # Proficiency Bonus
        self.ProficiencyBonusLabel = Label(self.CharacterSheetHeaderFrame, text="Proficiency Bonus:")
        self.ProficiencyBonusLabel.grid(row=1, column=3, sticky=E)
        self.ProficiencyBonusEntry = Entry(self.CharacterSheetHeaderFrame, textvariable=self.ProficiencyBonusEntryVar, state=DISABLED, justify=CENTER, width=5, disabledbackground="light gray", disabledforeground="black",
                                           cursor="arrow")
        self.ProficiencyBonusEntry.grid(row=1, column=4, sticky=NSEW, padx=2, pady=2)

        # Experience
        self.CharacterExperienceLabel = Label(self.CharacterSheetHeaderFrame, text="Exp.:")
        self.CharacterExperienceLabel.grid(row=0, column=6, sticky=E)
        self.CharacterExperienceEntry = Entry(self.CharacterSheetHeaderFrame, textvariable=self.CharacterExperienceEntryVar, width=10, justify=CENTER)
        self.CharacterExperienceEntry.grid(row=0, column=7, sticky=NSEW, padx=2, pady=2)

        # Needed Experience
        self.CharacterExperienceNeededLabel = Label(self.CharacterSheetHeaderFrame, text="Needed Exp.:")
        self.CharacterExperienceNeededLabel.grid(row=1, column=6, sticky=E)
        self.CharacterExperienceNeededEntry = Entry(self.CharacterSheetHeaderFrame, textvariable=self.CharacterExperienceNeededEntryVar, state=DISABLED, justify=CENTER, width=10, disabledbackground="light gray",
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

        # Add Saved Fields to Saved Data Dictionary
        SavingAndOpeningInst.SavedData["CharacterNameEntryVar"] = self.CharacterNameEntryVar
        SavingAndOpeningInst.SavedData["CharacterLevelEntryVar"] = self.CharacterLevelEntryVar
        SavingAndOpeningInst.SavedData["CharacterClassEntryVar"] = self.CharacterClassEntryVar
        SavingAndOpeningInst.SavedData["CharacterExperienceEntryVar"] = self.CharacterExperienceEntryVar
        SavingAndOpeningInst.SavedData["SpellcasterBoxVar"] = self.SpellcasterBoxVar
        SavingAndOpeningInst.SavedData["ConcentrationCheckPromptBoxVar"] = self.ConcentrationCheckPromptBoxVar
        SavingAndOpeningInst.SavedData["PortraitBoxVar"] = self.PortraitBoxVar
        SavingAndOpeningInst.SavedData["JackOfAllTradesBoxVar"] = self.JackOfAllTradesBoxVar
        SavingAndOpeningInst.SavedData["RemarkableAthleteBoxVar"] = self.RemarkableAthleteBoxVar
        SavingAndOpeningInst.SavedData["ObservantBoxVar"] = self.ObservantBoxVar
        SavingAndOpeningInst.SavedData["LuckyHalflingBoxVar"] = self.LuckyHalflingBoxVar

    def ValidStatsEntry(self):
        try:
            CharacterLevelValue = GlobalInst.GetStringVarAsNumber(self.CharacterLevelEntryVar)
        except:
            messagebox.showerror("Invalid Entry", "Character level must be a whole number.")
            return False
        if CharacterLevelValue <= 0 or CharacterLevelValue >= 21:
            messagebox.showerror("Invalid Entry", "Character level must be between 1 and 20.")
            return False
        try:
            StrengthBaseValue = GlobalInst.GetStringVarAsNumber(Inst["AbilitiesAndSavingThrows"].StrengthEntry.AbilityEntryTotalVar)
            DexterityBaseValue = GlobalInst.GetStringVarAsNumber(Inst["AbilitiesAndSavingThrows"].DexterityEntry.AbilityEntryTotalVar)
            ConstitutionBaseValue = GlobalInst.GetStringVarAsNumber(Inst["AbilitiesAndSavingThrows"].ConstitutionEntry.AbilityEntryTotalVar)
            IntelligenceBaseValue = GlobalInst.GetStringVarAsNumber(Inst["AbilitiesAndSavingThrows"].IntelligenceEntry.AbilityEntryTotalVar)
            WisdomBaseValue = GlobalInst.GetStringVarAsNumber(Inst["AbilitiesAndSavingThrows"].WisdomEntry.AbilityEntryTotalVar)
            CharismaBaseValue = GlobalInst.GetStringVarAsNumber(Inst["AbilitiesAndSavingThrows"].CharismaEntry.AbilityEntryTotalVar)
        except:
            messagebox.showerror("Invalid Entry", "Character abilities must be whole numbers.")
            return False
        if StrengthBaseValue <= 0 or DexterityBaseValue <= 0 or ConstitutionBaseValue <= 0 or IntelligenceBaseValue <= 0 or WisdomBaseValue <= 0 or CharismaBaseValue <= 0:
            messagebox.showerror("Invalid Entry", "Character abilities must be greater than 0.")
            return False
        return True

    def UpdateStatsAndInventory(self):
        # Test Stats Input Validity
        if self.ValidStatsEntry():
            pass
        else:
            return

        # Store Level
        CharacterLevelValue = GlobalInst.GetStringVarAsNumber(self.CharacterLevelEntryVar)

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
            Entry.PresetRollModifierEntryVar.set(Entry.PresetRollModifierEntryStatModifierInst.GetModifier())

        # Test Inventory Input Validity
        if self.InventoryInst.ValidInventoryEntry():
            pass
        else:
            return

        # Calculate Inventory
        self.InventoryInst.Calculate()

        # Calculate AC
        self.CombatAndFeaturesInst.ACEntryVar.set(str(self.CombatAndFeaturesInst.ACEntryStatModifierInst.GetModifier()))

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

        # Update Window Title
        WindowInst.UpdateWindowTitle()

    def Settings(self):
        # Test Stats Input Validity
        if self.ValidStatsEntry():
            pass
        else:
            return

        # Create Config Window and Wait
        SettingsMenuInst = self.SettingsMenu(WindowInst, self.SpellcasterBoxVar, self.ConcentrationCheckPromptBoxVar, self.PortraitBoxVar, self.JackOfAllTradesBoxVar, self.RemarkableAthleteBoxVar, self.ObservantBoxVar,
                                             self.LuckyHalflingBoxVar)
        WindowInst.wait_window(SettingsMenuInst.Window)

        # Handle Values
        if SettingsMenuInst.DataSubmitted.get():
            self.SpellcasterBoxVar.set(SettingsMenuInst.SpellcasterBoxVar.get())
            self.ConcentrationCheckPromptBoxVar.set(SettingsMenuInst.ConcentrationCheckPromptBoxVar.get())
            self.PortraitBoxVar.set(SettingsMenuInst.PortraitBoxVar.get())
            self.JackOfAllTradesBoxVar.set(SettingsMenuInst.JackOfAllTradesBoxVar.get())
            self.RemarkableAthleteBoxVar.set(SettingsMenuInst.RemarkableAthleteBoxVar.get())
            self.ObservantBoxVar.set(SettingsMenuInst.ObservantBoxVar.get())
            self.LuckyHalflingBoxVar.set(SettingsMenuInst.LuckyHalflingBoxVar.get())
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
            self.PassivePerceptionEntry = Entry(self.PassiveScoresFrame, justify=CENTER, width=20, textvariable=self.PassivePerceptionEntryVar)
            self.PassivePerceptionEntry.grid(row=1, column=0, sticky=NSEW)
            self.PassivePerceptionStatModifierInst = StatModifier(self.PassivePerceptionEntry, "<Button-1>", "Left-click on Passive Perception to set a stat modifier.", "Passive Perception")
            self.PassiveInvestigationHeader = Label(self.PassiveScoresFrame, text="Investigation", bd=2, relief=GROOVE)
            self.PassiveInvestigationHeader.grid(row=0, column=1, sticky=NSEW)
            self.PassiveInvestigationEntry = Entry(self.PassiveScoresFrame, justify=CENTER, width=20, textvariable=self.PassiveInvestigationEntryVar)
            self.PassiveInvestigationEntry.grid(row=1, column=1, sticky=NSEW)
            self.PassiveInvestigationStatModifierInst = StatModifier(self.PassiveInvestigationEntry, "<Button-1>", "Left-click on Passive Investigation to set a stat modifier.", "Passive Investigation")

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
            self.ProficienciesWeaponsField = ScrolledText(self.ProficienciesWeaponsFieldFrame, Width=130, Height=73)
            self.ProficienciesWeaponsField.grid(row=0, column=0)

            # Armor Proficiencies
            self.ProficienciesArmorHeader = Label(self.ProficienciesFrame, text="Armor", bd=2, relief=GROOVE)
            self.ProficienciesArmorHeader.grid(row=2, column=0, sticky=NSEW)
            self.ProficienciesArmorFieldFrame = Frame(self.ProficienciesFrame)
            self.ProficienciesArmorFieldFrame.grid(row=3, column=0)
            self.ProficienciesArmorField = ScrolledText(self.ProficienciesArmorFieldFrame, Width=130, Height=73)
            self.ProficienciesArmorField.grid(row=0, column=0)

            # Tool and Instrument Proficiencies
            self.ProficienciesToolsAndInstrumentsHeader = Label(self.ProficienciesFrame, text="Tools and Instruments", bd=2, relief=GROOVE)
            self.ProficienciesToolsAndInstrumentsHeader.grid(row=4, column=0, sticky=NSEW)
            self.ProficienciesToolsAndInstrumentsFieldFrame = Frame(self.ProficienciesFrame)
            self.ProficienciesToolsAndInstrumentsFieldFrame.grid(row=5, column=0)
            self.ProficienciesToolsAndInstrumentsField = ScrolledText(self.ProficienciesToolsAndInstrumentsFieldFrame, Width=130, Height=73)
            self.ProficienciesToolsAndInstrumentsField.grid(row=0, column=0)

            # Language Proficiencies
            self.ProficienciesLanguagesHeader = Label(self.ProficienciesFrame, text="Languages", bd=2, relief=GROOVE)
            self.ProficienciesLanguagesHeader.grid(row=6, column=0, sticky=NSEW)
            self.ProficienciesLanguagesFieldFrame = Frame(self.ProficienciesFrame)
            self.ProficienciesLanguagesFieldFrame.grid(row=7, column=0)
            self.ProficienciesLanguagesField = ScrolledText(self.ProficienciesLanguagesFieldFrame, Width=130, Height=73)
            self.ProficienciesLanguagesField.grid(row=0, column=0)

            # Other Proficiencies
            self.ProficienciesOtherHeader = Label(self.ProficienciesFrame, text="Other", bd=2, relief=GROOVE)
            self.ProficienciesOtherHeader.grid(row=8, column=0, sticky=NSEW)
            self.ProficienciesOtherFieldFrame = Frame(self.ProficienciesFrame)
            self.ProficienciesOtherFieldFrame.grid(row=9, column=0)
            self.ProficienciesOtherField = ScrolledText(self.ProficienciesOtherFieldFrame, Width=130, Height=73)
            self.ProficienciesOtherField.grid(row=0, column=0)

            # Add Saved Fields to Saved Data Dictionary
            SavingAndOpeningInst.SavedData["ProficienciesWeaponsField"] = self.ProficienciesWeaponsField
            SavingAndOpeningInst.SavedData["ProficienciesArmorField"] = self.ProficienciesArmorField
            SavingAndOpeningInst.SavedData["ProficienciesToolsAndInstrumentsField"] = self.ProficienciesToolsAndInstrumentsField
            SavingAndOpeningInst.SavedData["ProficienciesLanguagesField"] = self.ProficienciesLanguagesField
            SavingAndOpeningInst.SavedData["ProficienciesOtherField"] = self.ProficienciesOtherField
            self.PassivePerceptionStatModifierInst.AddToSavedData(Prefix="PassivePerception")
            self.PassiveInvestigationStatModifierInst.AddToSavedData(Prefix="PassiveInvestigation")

        # Abilities and Saving Throws
        class AbilitiesAndSavingThrowsTable:
            def __init__(self, master):
                self.PointBuyBoxVar = BooleanVar()

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
                self.AbilitiesNotes = ScrolledText(self.AbilitiesNotesFrame, Width=275, Height=180)
                self.AbilitiesNotes.grid(row=0, column=0)

                # Add Saved Fields to Saved Data Dictionary
                SavingAndOpeningInst.SavedData["PointBuyBoxVar"] = self.PointBuyBoxVar
                SavingAndOpeningInst.SavedData["AbilitiesNotes"] = self.AbilitiesNotes

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

                    # Store Point Buy
                    self.PointBuyBoxVar.set(AbilitiesDataConfigInst.PointBuyBoxVar.get())

            class AbilitiesAndSavingThrowsEntry:
                def __init__(self, master, AbilityName, List, Row):
                    # Store Parameters
                    self.AbilityName = AbilityName
                    self.Row = Row

                    # Variables
                    self.AbilityNameVar = StringVar(value=self.AbilityName)
                    self.AbilityEntryTotalVar = StringVar()
                    self.AbilityEntryModifierVar = StringVar()
                    self.AbilitySavingThrowProficiencyBoxVar = BooleanVar()
                    self.AbilitySavingThrowModifierVar = StringVar()

                    # Config Variables
                    self.AbilityBaseVar = StringVar()
                    self.AbilityRacialVar = StringVar()
                    self.AbilityASIVar = StringVar()
                    self.AbilityMiscVar = StringVar()
                    self.AbilityOverrideVar = StringVar()

                    # Add to List
                    List.append(self)

                    # Label
                    self.AbilityLabel = Label(master, textvariable=self.AbilityNameVar)
                    self.AbilityLabel.grid(row=self.Row, column=0, sticky=NSEW)

                    # Total Entry
                    self.AbilityEntryTotal = Entry(master, width=3, justify=CENTER, textvariable=self.AbilityEntryTotalVar, state=DISABLED, disabledbackground="light gray", disabledforeground="black", cursor="arrow")
                    self.AbilityEntryTotal.grid(row=self.Row, column=1, sticky=NSEW)

                    # Ability And Saving Throw Tooltip String
                    self.AbilityAndSavingThrowTooltipString = "Left-click on an ability or saving throw modifier to roll 1d20 with it.  Right-click to set a stat modifier."

                    # Modifier Entry
                    self.AbilityEntryModifier = Entry(master, width=3, justify=CENTER, textvariable=self.AbilityEntryModifierVar, cursor="dotbox")
                    self.AbilityEntryModifier.grid(row=self.Row, column=2, sticky=NSEW)
                    self.AbilityEntryModifierStatModifierInst = StatModifier(self.AbilityEntryModifier, "<Button-3>", self.AbilityAndSavingThrowTooltipString, self.AbilityName + " Modifier", Cursor="dotbox")
                    self.AbilityEntryModifier.bind("<Button-1>", self.RollAbility)

                    # Saving Throw Proficiency Box
                    self.AbilitySavingThrowProficiencyBox = Checkbutton(master, variable=self.AbilitySavingThrowProficiencyBoxVar)
                    self.AbilitySavingThrowProficiencyBox.grid(row=self.Row, column=4, sticky=NSEW)

                    # Saving Throw Modifier Entry
                    self.AbilitySavingThrowModifier = Entry(master, width=3, justify=CENTER, textvariable=self.AbilitySavingThrowModifierVar, cursor="dotbox")
                    self.AbilitySavingThrowModifier.grid(row=self.Row, column=5, sticky=NSEW)
                    self.AbilitySavingThrowModifierStatModifierInst = StatModifier(self.AbilitySavingThrowModifier, "<Button-3>", self.AbilityAndSavingThrowTooltipString, self.AbilityName + " Saving Throw", Cursor="dotbox")
                    self.AbilitySavingThrowModifier.bind("<Button-1>", self.RollSavingThrow)

                    # Add Saved Fields to Saved Data Dictionary
                    SavingAndOpeningInst.SavedData[self.AbilityName + "AbilityEntryTotalVar"] = self.AbilityEntryTotalVar
                    SavingAndOpeningInst.SavedData[self.AbilityName + "AbilityBaseVar"] = self.AbilityBaseVar
                    SavingAndOpeningInst.SavedData[self.AbilityName + "AbilityRacialVar"] = self.AbilityRacialVar
                    SavingAndOpeningInst.SavedData[self.AbilityName + "AbilityASIVar"] = self.AbilityASIVar
                    SavingAndOpeningInst.SavedData[self.AbilityName + "AbilityMiscVar"] = self.AbilityMiscVar
                    SavingAndOpeningInst.SavedData[self.AbilityName + "AbilityOverrideVar"] = self.AbilityOverrideVar
                    SavingAndOpeningInst.SavedData[self.AbilityName + "AbilitySavingThrowProficiencyBoxVar"] = self.AbilitySavingThrowProficiencyBoxVar
                    self.AbilityEntryModifierStatModifierInst.AddToSavedData(Prefix=self.AbilityName + "AbilityEntryModifier")
                    self.AbilitySavingThrowModifierStatModifierInst.AddToSavedData(Prefix=self.AbilityName + "AbilitySavingThrowModifier")

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
                    self.DataSubmitted = BooleanVar()
                    self.PointBuyBoxVar = BooleanVar(value=Inst["AbilitiesAndSavingThrows"].PointBuyBoxVar.get())
                    self.PointBuyEntryVar = StringVar()
                    self.RollButtonVar = BooleanVar()

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

                    # Point Buy
                    self.PointBuyBox = Checkbutton(self.Window, text="Using Point Buy", variable=self.PointBuyBoxVar)
                    self.PointBuyBox.grid(row=4, column=7, padx=2, pady=2, sticky=NSEW)
                    self.PointBuyLabel = Label(self.Window, text="Points", bd=2, relief=GROOVE)
                    self.PointBuyLabel.grid(row=5, column=7, padx=2, pady=2, sticky=NSEW)
                    self.PointBuyEntry = Entry(self.Window, state=DISABLED, width=9, disabledbackground="light gray", disabledforeground="black", cursor="arrow", textvariable=self.PointBuyEntryVar, justify=CENTER)
                    self.PointBuyEntry.grid(row=6, column=7, padx=2, pady=2, sticky=NSEW)

                    # Buttons
                    self.CalculateButton = Button(self.Window, text="Calculate", command=self.Calculate, bg=GlobalInst.ButtonColor)
                    self.CalculateButton.grid(row=0, column=7, rowspan=2, padx=2, pady=2, sticky=NSEW)
                    self.RollButton = Checkbutton(self.Window, text="Roll", variable=self.RollButtonVar, command=self.CreateRollForAbilitiesMenu, bg=GlobalInst.ButtonColor, indicatoron=False, selectcolor=GlobalInst.ButtonColor)
                    self.RollButton.grid(row=2, column=7, rowspan=2, padx=2, pady=2, sticky=NSEW)
                    self.ButtonsFrame = Frame(self.Window)
                    self.ButtonsFrame.grid_columnconfigure(0, weight=1)
                    self.ButtonsFrame.grid_columnconfigure(1, weight=1)
                    self.ButtonsFrame.grid(row=7, column=0, columnspan=8, sticky=NSEW)
                    self.SubmitButton = Button(self.ButtonsFrame, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
                    self.SubmitButton.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)
                    self.CancelButton = Button(self.ButtonsFrame, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
                    self.CancelButton.grid(row=0, column=1, padx=2, pady=2, sticky=NSEW)

                    # Prevent Main Window Input
                    self.Window.grab_set()

                    # Handle Config Window Geometry and Focus
                    GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst)
                    self.Window.focus_force()

                    # Calculate Point Buy Values
                    self.CalculatePointBuyValues()

                def Calculate(self):
                    if self.ValidStatsEntries():
                        pass
                    else:
                        return False
                    self.StrengthConfigEntry.Calculate()
                    self.DexterityConfigEntry.Calculate()
                    self.ConstitutionConfigEntry.Calculate()
                    self.IntelligenceConfigEntry.Calculate()
                    self.WisdomConfigEntry.Calculate()
                    self.CharismaConfigEntry.Calculate()
                    if self.CalculatePointBuyValues():
                        if (self.PointBuyBoxVar.get() and GlobalInst.GetStringVarAsNumber(self.PointBuyEntryVar) >= 0) or not self.PointBuyBoxVar.get():
                            pass
                        else:
                            messagebox.showerror("Invalid Entry", "Not enough points for these ability scores.")
                            return False
                    else:
                        return False
                    return True

                def CalculatePointBuyValues(self):
                    if self.PointBuyBoxVar.get():
                        if self.StrengthConfigEntry.ValidPointBuyValue() and self.DexterityConfigEntry.ValidPointBuyValue() and self.ConstitutionConfigEntry.ValidPointBuyValue() and self.IntelligenceConfigEntry.ValidPointBuyValue() and self.WisdomConfigEntry.ValidPointBuyValue() and self.CharismaConfigEntry.ValidPointBuyValue():
                            PointsRemaining = 27 - self.StrengthConfigEntry.PointBuyValue() - self.DexterityConfigEntry.PointBuyValue() - self.ConstitutionConfigEntry.PointBuyValue() - self.IntelligenceConfigEntry.PointBuyValue() - self.WisdomConfigEntry.PointBuyValue() - self.CharismaConfigEntry.PointBuyValue()
                            self.PointBuyEntryVar.set(str(PointsRemaining))
                            return True
                        else:
                            messagebox.showerror("Invalid Entry", "Base ability scores must be between 8 and 15 when using point buy.")
                            return False
                    else:
                        self.PointBuyEntryVar.set("N/A")
                        return True

                def ValidStatsEntries(self):
                    if not self.StrengthConfigEntry.ValidStatsEntries():
                        return False
                    if not self.DexterityConfigEntry.ValidStatsEntries():
                        return False
                    if not self.ConstitutionConfigEntry.ValidStatsEntries():
                        return False
                    if not self.IntelligenceConfigEntry.ValidStatsEntries():
                        return False
                    if not self.WisdomConfigEntry.ValidStatsEntries():
                        return False
                    if not self.CharismaConfigEntry.ValidStatsEntries():
                        return False
                    return True

                def Submit(self):
                    if self.Calculate():
                        pass
                    else:
                        return
                    self.DataSubmitted.set(True)
                    self.Window.destroy()

                def Cancel(self):
                    self.DataSubmitted.set(False)
                    self.Window.destroy()

                def CreateRollForAbilitiesMenu(self):
                    if self.RollButtonVar.get():
                        # Create Menu
                        self.RollForAbilitiesMenuInst = self.RollForAbilitiesMenu(self.Window, self)

                        # Adjust Geometry
                        GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst, WidthOffset=163)
                    else:
                        # Destroy Menu
                        self.RollForAbilitiesMenuInst.RollForAbilitiesFrame.destroy()

                        # Adjust Geometry
                        GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst, WidthOffset=-163)

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
                        self.AbilityEntryBase = Entry(master, width=9, justify=CENTER, textvariable=self.AbilityBaseVar)
                        self.AbilityEntryBase.grid(row=Row, column=1, sticky=NSEW, padx=2, pady=2)

                        # Racial Entry
                        self.AbilityEntryRacial = Entry(master, width=9, justify=CENTER, textvariable=self.AbilityRacialVar)
                        self.AbilityEntryRacial.grid(row=Row, column=2, sticky=NSEW, padx=2, pady=2)

                        # ASI Entry
                        self.AbilityEntryASI = Entry(master, width=9, justify=CENTER, textvariable=self.AbilityASIVar)
                        self.AbilityEntryASI.grid(row=Row, column=3, sticky=NSEW, padx=2, pady=2)

                        # Misc. Entry
                        self.AbilityEntryMisc = Entry(master, width=9, justify=CENTER, textvariable=self.AbilityMiscVar)
                        self.AbilityEntryMisc.grid(row=Row, column=4, sticky=NSEW, padx=2, pady=2)

                        # Override Entry
                        self.AbilityEntryOverride = Entry(master, width=9, justify=CENTER, textvariable=self.AbilityOverrideVar)
                        self.AbilityEntryOverride.grid(row=Row, column=5, sticky=NSEW, padx=2, pady=2)

                        # Total Entry
                        self.AbilityEntryTotal = Entry(master, width=9, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow", textvariable=self.AbilityTotalVar)
                        self.AbilityEntryTotal.grid(row=Row, column=6, sticky=NSEW, padx=2, pady=2)

                    def Calculate(self):
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

                    def PointBuyValue(self):
                        Base = GlobalInst.GetStringVarAsNumber(self.AbilityBaseVar)
                        Value = Base - 8
                        if Base >= 14:
                            Value += 1
                        if Base >= 15:
                            Value += 1
                        return Value

                    def ValidStatsEntries(self):
                        try:
                            Base = GlobalInst.GetStringVarAsNumber(self.AbilityBaseVar)
                            Racial = GlobalInst.GetStringVarAsNumber(self.AbilityRacialVar)
                            ASI = GlobalInst.GetStringVarAsNumber(self.AbilityASIVar)
                            Misc = GlobalInst.GetStringVarAsNumber(self.AbilityMiscVar)
                            Override = GlobalInst.GetStringVarAsNumber(self.AbilityOverrideVar)
                        except:
                            messagebox.showerror("Invalid Entry", "Ability score data must be whole numbers.")
                            return False
                        if Base <= 0:
                            messagebox.showerror("Invalid Entry", "Base ability scores must be greater than 0.")
                            return False
                        OverrideBlank = (self.AbilityOverrideVar.get() == "")
                        if Override <= 0 and not OverrideBlank:
                            messagebox.showerror("Invalid Entry", "Overrides must be greater than 0.")
                            return False
                        return True

                    def ValidPointBuyValue(self):
                        Base = GlobalInst.GetStringVarAsNumber(self.AbilityBaseVar)
                        Valid = True
                        if Base < 8 or Base > 15:
                            Valid = False
                        return Valid

                class RollForAbilitiesMenu:
                    def __init__(self, master, AbilitiesDataConfigInst):
                        self.master = master
                        self.DataSubmitted = BooleanVar()
                        self.Rolled = False
                        self.AbilitiesDataConfigInst = AbilitiesDataConfigInst

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

                        # Buttons
                        self.RollScoresButton = Button(self.RollForAbilitiesFrame, text="Roll\nScores", command=self.RollScores, bg=GlobalInst.ButtonColor)
                        self.RollScoresButton.grid(row=0, column=2, rowspan=3, padx=2, pady=2, sticky=NSEW)
                        self.AcceptButton = Button(self.RollForAbilitiesFrame, text="Accept", command=self.Accept, bg=GlobalInst.ButtonColor)
                        self.AcceptButton.grid(row=3, column=0, columnspan=4, padx=2, pady=2, sticky=NSEW)

                    def Accept(self):
                        if self.ValidEntry():
                            pass
                        else:
                            return
                        self.AbilitiesDataConfigInst.RollButtonVar.set(False)
                        for Assignment in self.RollAssignFieldsList:
                            for Entry in self.AbilitiesDataConfigInst.EntriesList:
                                RollLabelVar = Assignment.RollLabelVar.get()
                                RollDropdownVar = Assignment.RollDropdownVar.get()
                                if Entry.AbilityNameShort == RollDropdownVar:
                                    Entry.AbilityBaseVar.set(RollLabelVar)
                        self.RollForAbilitiesFrame.destroy()
                        GlobalInst.WindowGeometry(self.master, IsDialog=True, DialogMaster=WindowInst, WidthOffset=-163)

                    def RollScores(self):
                        FinalRolls = []
                        for Index in range(6):
                            Rolls = []
                            Total = 0
                            for Roll in range(4):
                                Rolls.append(DiceRollerInst.IntRoll(1, 6, 0))
                            Rolls.remove(min(Rolls))
                            for Roll in Rolls:
                                Total += Roll
                            FinalRolls.append(Total)
                        for Index in range(6):
                            self.RollAssignFieldsList[Index].RollLabelVar.set(str(FinalRolls[Index]))
                        self.Rolled = True

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
                            self.RollLabelVar = StringVar(value="-")
                            self.RollDropdownVar = StringVar()
                            self.Row = Row
                            self.Column = Column

                            # Add to List
                            List.append(self)

                            # Frame
                            self.FieldFrame = Frame(master)
                            self.FieldFrame.grid(row=self.Row, column=self.Column, sticky=NSEW)

                            # Label
                            self.RollLabel = Label(self.FieldFrame, textvariable=self.RollLabelVar, bd=2, relief=GROOVE)
                            self.RollLabel.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)

                            # Dropdown
                            self.RollDropdown = ttk.Combobox(self.FieldFrame, textvariable=self.RollDropdownVar, values=("", "STR", "DEX", "CON", "INT", "WIS", "CHA"), width=5, state="readonly", justify=CENTER)
                            self.RollDropdown.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)

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
                    self.ProficiencyBox1Var = BooleanVar()
                    self.ProficiencyBox2Var = BooleanVar()
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
                    self.ModifierEntry = Entry(master, textvariable=self.TotalModifierVar, width=3, justify=CENTER, cursor="dotbox")
                    self.ModifierEntry.grid(row=Row, column=2, sticky=NSEW)
                    self.ModifierEntryStatModifierInst = StatModifier(self.ModifierEntry, "<Button-3>", "Left-click on a skill modifier to roll 1d20 with it.  Right-click to set a bonus.", self.SkillName, Cursor="dotbox")
                    self.ModifierEntry.bind("<Button-1>", self.RollSkill)

                    # Add Saved Fields to Saved Data Dictionary
                    SavingAndOpeningInst.SavedData[self.SkillName + "SkillProficiency1"] = self.ProficiencyBox1Var
                    SavingAndOpeningInst.SavedData[self.SkillName + "SkillProficiency2"] = self.ProficiencyBox2Var
                    self.ModifierEntryStatModifierInst.AddToSavedData(Prefix=self.SkillName + "ModifierEntry")

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
            self.TempHPEntryVar = StringVar()
            self.CurrentHPEntryVar = StringVar()
            self.MaxHPEntryVar = StringVar()
            self.HitDiceEntryVar = StringVar()
            self.HitDiceRemainingEntryVar = StringVar()
            self.DeathSavingThrowsBoxSuccess1Var = BooleanVar()
            self.DeathSavingThrowsBoxSuccess2Var = BooleanVar()
            self.DeathSavingThrowsBoxSuccess3Var = BooleanVar()
            self.DeathSavingThrowsBoxFailure1Var = BooleanVar()
            self.DeathSavingThrowsBoxFailure2Var = BooleanVar()
            self.DeathSavingThrowsBoxFailure3Var = BooleanVar()
            self.ACEntryVar = StringVar()
            self.InitiativeEntryVar = StringVar()
            self.SpeedEntryVar = StringVar()

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
            self.TempHPEntry = Entry(self.TempHPFrame, width=5, justify=CENTER, textvariable=self.TempHPEntryVar, font=self.VitalityFontSize)
            self.TempHPEntry.grid(row=0, column=0, sticky=NSEW)

            # Current HP
            self.CurrentHPFrame = LabelFrame(self.HPFrame, text="Current HP:")
            self.CurrentHPFrame.grid_columnconfigure(0, weight=1)
            self.CurrentHPFrame.grid_rowconfigure(0, weight=1)
            self.CurrentHPFrame.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
            self.CurrentHPEntry = Entry(self.CurrentHPFrame, width=5, justify=CENTER, textvariable=self.CurrentHPEntryVar, bg=GlobalInst.ButtonColor, font=self.VitalityFontSize)
            self.CurrentHPEntry.grid(row=0, column=0, sticky=NSEW)
            self.CurrentHPEntry.bind("<Button-3>", lambda event: self.Damage())
            self.CurrentHPEntry.bind("<Shift-Button-3>", lambda event: self.Heal())
            StatusBarInst.TooltipConfig(self.CurrentHPEntry, "Right-click to damage.  Shift+right-click to heal.")

            # Max HP
            self.MaxHPFrame = LabelFrame(self.HPFrame, text="Max HP:")
            self.MaxHPFrame.grid_columnconfigure(0, weight=1)
            self.MaxHPFrame.grid_rowconfigure(0, weight=1)
            self.MaxHPFrame.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)
            self.MaxHPEntry = Entry(self.MaxHPFrame, width=5, justify=CENTER, textvariable=self.MaxHPEntryVar, font=self.VitalityFontSize)
            self.MaxHPEntry.grid(row=0, column=0, sticky=NSEW)

            # Hit Dice
            self.HitDiceFrame = LabelFrame(self.VitalityFrame, text="Hit Dice:")
            self.HitDiceFrame.grid_columnconfigure(0, weight=1)
            self.HitDiceFrame.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
            self.HitDiceEntry = Entry(self.HitDiceFrame, width=12, justify=CENTER, textvariable=self.HitDiceEntryVar)
            self.HitDiceEntry.grid(row=0, column=0, sticky=NSEW)
            self.HitDiceRemainingFrame = LabelFrame(self.VitalityFrame, text="Hit Dice Remaining:")
            self.HitDiceRemainingFrame.grid_columnconfigure(0, weight=1)
            self.HitDiceRemainingFrame.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
            self.HitDiceRemainingEntry = Entry(self.HitDiceRemainingFrame, width=12, justify=CENTER, textvariable=self.HitDiceRemainingEntryVar)
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
            self.ACEntry = Entry(self.ACFrame, width=9, justify=CENTER, textvariable=self.ACEntryVar, font=self.ACInitiativeSpeedFontSize)
            self.ACEntry.grid(row=0, column=0, sticky=NSEW)
            self.ACEntryStatModifierInst = StatModifier(self.ACEntry, "<Button-1>", "Left-click to set AC data.", "", ACMode=True)
            StatusBarInst.TooltipConfig(self.ACEntry, "Left-click on AC to set data.")

            # Initiative
            self.InitiativeFrame = LabelFrame(self.ACInitiativeSpeedFrame, text="Initiative:")
            self.InitiativeFrame.grid_rowconfigure(0, weight=1)
            self.InitiativeFrame.grid(row=1, column=0, sticky=NSEW)
            self.InitiativeEntry = Entry(self.InitiativeFrame, width=9, justify=CENTER, textvariable=self.InitiativeEntryVar, cursor="dotbox", font=self.ACInitiativeSpeedFontSize)
            self.InitiativeEntry.grid(row=0, column=0, sticky=NSEW)
            self.InitiativeEntry.bind("<Button-1>", self.RollInitiative)
            self.InitiativeEntryStatModifierInst = StatModifier(self.InitiativeEntry, "<Button-3>", "Left-click on the initiative modifier to roll 1d20 with it.  Right-click to set a stat modifier.", "Initiative", Cursor="dotbox")

            # Speed
            self.SpeedFrame = LabelFrame(self.ACInitiativeSpeedFrame, text="Speed:")
            self.SpeedFrame.grid_rowconfigure(0, weight=1)
            self.SpeedFrame.grid(row=2, column=0, sticky=NSEW)
            self.SpeedEntry = Entry(self.SpeedFrame, width=9, justify=CENTER, textvariable=self.SpeedEntryVar, font=self.ACInitiativeSpeedFontSize)
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
            self.CombatAndFeaturesNotes = ScrolledText(self.CombatAndFeaturesNotesFrame, Height=180, Width=344)
            self.CombatAndFeaturesNotes.grid(row=0, column=0)

            # Features
            self.FeaturesAndCreatureStatsInst = self.FeaturesAndCreatureStats(master)
            Inst["FeaturesAndCreatureStats"] = self.FeaturesAndCreatureStatsInst

            # Add Saved Fields to Saved Data Dictionary
            SavingAndOpeningInst.SavedData["TempHPEntryVar"] = self.TempHPEntryVar
            SavingAndOpeningInst.SavedData["CurrentHPEntryVar"] = self.CurrentHPEntryVar
            SavingAndOpeningInst.SavedData["MaxHPEntryVar"] = self.MaxHPEntryVar
            SavingAndOpeningInst.SavedData["HitDiceEntryVar"] = self.HitDiceEntryVar
            SavingAndOpeningInst.SavedData["HitDiceRemainingEntryVar"] = self.HitDiceRemainingEntryVar
            SavingAndOpeningInst.SavedData["DeathSavingThrowsBoxSuccess1Var"] = self.DeathSavingThrowsBoxSuccess1Var
            SavingAndOpeningInst.SavedData["DeathSavingThrowsBoxSuccess2Var"] = self.DeathSavingThrowsBoxSuccess2Var
            SavingAndOpeningInst.SavedData["DeathSavingThrowsBoxSuccess3Var"] = self.DeathSavingThrowsBoxSuccess3Var
            SavingAndOpeningInst.SavedData["DeathSavingThrowsBoxFailure1Var"] = self.DeathSavingThrowsBoxFailure1Var
            SavingAndOpeningInst.SavedData["DeathSavingThrowsBoxFailure2Var"] = self.DeathSavingThrowsBoxFailure2Var
            SavingAndOpeningInst.SavedData["DeathSavingThrowsBoxFailure3Var"] = self.DeathSavingThrowsBoxFailure3Var
            SavingAndOpeningInst.SavedData["SpeedEntryVar"] = self.SpeedEntryVar
            SavingAndOpeningInst.SavedData["CombatAndFeaturesNotes"] = self.CombatAndFeaturesNotes
            self.InitiativeEntryStatModifierInst.AddToSavedData(Prefix="InitiativeEntry")
            self.ACEntryStatModifierInst.AddToSavedData(Prefix="ACEntry")

        def Damage(self):
            if self.ValidLifeValues():
                pass
            else:
                return
            CurrentTempHP = GlobalInst.GetStringVarAsNumber(self.TempHPEntryVar)
            if self.CurrentHPEntryVar.get() == "":
                CurrentHP = GlobalInst.GetStringVarAsNumber(self.MaxHPEntryVar)
            else:
                CurrentHP = GlobalInst.GetStringVarAsNumber(self.CurrentHPEntryVar)
            DamagePrompt = IntegerPrompt(WindowInst, "Damage", "How much damage?", MinValue=1)
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
            HealingPrompt = IntegerPrompt(WindowInst, "Heal", "How much healing?", MinValue=1)
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
            DiceRollerInst.DiceNumberEntryVar.set(1)
            DiceRollerInst.DieTypeEntryVar.set(20)
            DiceRollerInst.ModifierEntryVar.set(str(GlobalInst.GetStringVarAsNumber(self.InitiativeEntryVar)))
            DiceRollerInst.Roll("Initiative:\n")

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
                StatusBarInst.TooltipConfig(self.NameHeader, GlobalInst.SortTooltipString)
                self.SortOrderHeader = Label(self.FeaturesScrolledCanvas.WindowFrame, text="Sort\nOrder", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
                self.SortOrderHeader.grid(row=0, column=1, sticky=NSEW)
                self.SortOrderHeader.bind("<Button-1>", lambda event: self.Sort("Sort Order"))
                self.SortOrderHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Sort Order", SearchMode=True))
                self.SortOrderHeader.bind("<Button-3>", lambda event: self.Sort("Sort Order", Reverse=True))
                StatusBarInst.TooltipConfig(self.SortOrderHeader, GlobalInst.SortTooltipString)

                # Features Entries List
                self.FeatureOrCreatureStatsEntriesList = []

                # Sort Order Values
                self.SortOrderValuesString = "\"\""
                for CurrentIndex in range(1, 101):
                    self.SortOrderValuesString += "," + str(CurrentIndex)
                self.SortOrderValuesTuple = eval(self.SortOrderValuesString)

                # Features Entries
                for CurrentIndex in range(1, 101):
                    CurrentEntry = self.FeatureOrCreatureStatsEntry(self.FeaturesScrolledCanvas.WindowFrame, self.FeatureOrCreatureStatsEntriesList, self.ScrollingDisabledVar, self.SortOrderValuesTuple, CurrentIndex)
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
                            ListToSort.append((CurrentEntry, CurrentEntry.SortFields["Name"].get(), GlobalInst.GetStringVarAsNumber(CurrentEntry.SortFields[Column])))

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

            class FeatureOrCreatureStatsEntry:
                def __init__(self, master, List, ScrollingDisabledVar, SortOrderValuesTuple, Row):
                    # Store Parameters
                    self.master = master
                    self.ScrollingDisabledVar = ScrollingDisabledVar
                    self.SortOrderValuesTuple = SortOrderValuesTuple
                    self.Row = Row

                    # Variables
                    self.NameEntryVar = StringVar()
                    self.SortOrderVar = StringVar()
                    self.FeatureDescriptionVar = StringVar()
                    self.SizeEntryVar = StringVar()
                    self.TypeAndTagsEntryVar = StringVar()
                    self.AlignmentEntryVar = StringVar()
                    self.ProficiencyEntryVar = StringVar()
                    self.TempHPEntryVar = StringVar()
                    self.CurrentHPEntryVar = StringVar()
                    self.MaxHPEntryVar = StringVar()
                    self.ACEntryVar = StringVar()
                    self.SpeedEntryVar = StringVar()
                    self.CRAndExperienceEntryVar = StringVar()
                    self.AbilitiesStrengthEntryVar = StringVar()
                    self.AbilitiesDexterityEntryVar = StringVar()
                    self.AbilitiesConstitutionEntryVar = StringVar()
                    self.AbilitiesIntelligenceEntryVar = StringVar()
                    self.AbilitiesWisdomEntryVar = StringVar()
                    self.AbilitiesCharismaEntryVar = StringVar()
                    self.SkillSensesAndLanguagesFieldVar = StringVar()
                    self.SavingThrowsFieldVar = StringVar()
                    self.VulnerabilitiesResistancesAndImmunitiesFieldVar = StringVar()
                    self.SpecialTraitsFieldVar = StringVar()
                    self.ActionsFieldVar = StringVar()
                    self.ReactionsFieldVar = StringVar()
                    self.InventoryFieldVar = StringVar()
                    self.LegendaryActionsAndLairActionsFieldVar = StringVar()
                    self.NotesFieldVar = StringVar()

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
                    self.NameEntry = Entry(master, width=45, justify=CENTER, state=DISABLED, disabledbackground=GlobalInst.ButtonColor, disabledforeground="black", textvariable=self.NameEntryVar, cursor="arrow")
                    self.NameEntry.bind("<Button-1>", self.SetFeature)
                    self.NameEntry.bind("<Button-3>", self.SetCreatureStats)
                    StatusBarInst.TooltipConfig(self.NameEntry, "Left-click on a feature or creature stats entry to set a feature.  Right-click to set creature stats.")

                    # Sort Order
                    self.SortOrder = ttk.Combobox(master, textvariable=self.SortOrderVar, values=self.SortOrderValuesTuple, width=5, state="readonly", justify=CENTER)
                    self.SortOrder.bind("<Enter>", self.DisableScrolling)
                    self.SortOrder.bind("<Leave>", self.EnableScrolling)

                def SetFeature(self, event):
                    # Create Config Window and Wait
                    FeatureConfigInst = self.FeatureConfig(WindowInst, self.NameEntryVar, self.FeatureDescriptionVar)
                    WindowInst.wait_window(FeatureConfigInst.Window)

                    # Handle Values
                    if FeatureConfigInst.DataSubmitted.get():
                        self.NameEntryVar.set(FeatureConfigInst.NameEntryVar.get())
                        self.FeatureDescriptionVar.set(FeatureConfigInst.DescriptionVar.get())

                def SetCreatureStats(self, event):
                    # Create Config Window and Wait
                    CreatureDataInst = CreatureData(WindowInst, DialogMode=True, DialogData=self.CreatureStats)
                    WindowInst.wait_window(CreatureDataInst.Window)

                    # Handle Values
                    if CreatureDataInst.DataSubmitted.get():
                        for Tag, Var in self.CreatureStats.items():
                            Var.set(CreatureDataInst.CreatureStatsFields[Tag].get())

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

                    # Add Saved Fields to Saved Data Dictionary
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsNameEntryVar" + str(self.Row)] = self.NameEntryVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsSortOrderVar" + str(self.Row)] = self.SortOrderVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsFeatureDescriptionVar" + str(self.Row)] = self.FeatureDescriptionVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsSizeEntryVar" + str(self.Row)] = self.SizeEntryVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsTypeAndTagsEntryVar" + str(self.Row)] = self.TypeAndTagsEntryVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsAlignmentEntryVar" + str(self.Row)] = self.AlignmentEntryVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsProficiencyEntryVar" + str(self.Row)] = self.ProficiencyEntryVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsTempHPEntryVar" + str(self.Row)] = self.TempHPEntryVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsCurrentHPEntryVar" + str(self.Row)] = self.CurrentHPEntryVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsMaxHPEntryVar" + str(self.Row)] = self.MaxHPEntryVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsACEntryVar" + str(self.Row)] = self.ACEntryVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsSpeedEntryVar" + str(self.Row)] = self.SpeedEntryVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsCRAndExperienceEntryVar" + str(self.Row)] = self.CRAndExperienceEntryVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsAbilitiesStrengthEntryVar" + str(self.Row)] = self.AbilitiesStrengthEntryVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsAbilitiesDexterityEntryVar" + str(self.Row)] = self.AbilitiesDexterityEntryVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsAbilitiesConstitutionEntryVar" + str(self.Row)] = self.AbilitiesConstitutionEntryVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsAbilitiesIntelligenceEntryVar" + str(self.Row)] = self.AbilitiesIntelligenceEntryVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsAbilitiesWisdomEntryVar" + str(self.Row)] = self.AbilitiesWisdomEntryVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsAbilitiesCharismaEntryVar" + str(self.Row)] = self.AbilitiesCharismaEntryVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsSkillSensesAndLanguagesFieldVar" + str(self.Row)] = self.SkillSensesAndLanguagesFieldVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsSavingThrowsFieldVar" + str(self.Row)] = self.SavingThrowsFieldVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsVulnerabilitiesResistancesAndImmunitiesFieldVar" + str(self.Row)] = self.VulnerabilitiesResistancesAndImmunitiesFieldVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsSpecialTraitsFieldVar" + str(self.Row)] = self.SpecialTraitsFieldVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsActionsFieldVar" + str(self.Row)] = self.ActionsFieldVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsReactionsFieldVar" + str(self.Row)] = self.ReactionsFieldVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsInventoryFieldVar" + str(self.Row)] = self.InventoryFieldVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsLegendaryActionsAndLairActionsFieldVar" + str(self.Row)] = self.LegendaryActionsAndLairActionsFieldVar
                    SavingAndOpeningInst.SavedData["FeatureOrCreatureStatsNotesFieldVar" + str(self.Row)] = self.NotesFieldVar

                class FeatureConfig:
                    def __init__(self, master, NameEntryVar, DescriptionVar):
                        self.DataSubmitted = BooleanVar()
                        self.NameEntryVar = StringVar(value=NameEntryVar.get())
                        self.DescriptionVar = StringVar(value=DescriptionVar.get())

                        # Create Window
                        self.Window = Toplevel(master)
                        self.Window.wm_attributes("-toolwindow", 1)
                        self.Window.wm_title("Feature Description")

                        # Name Entry
                        self.NameFrame = LabelFrame(self.Window, text="Name:")
                        self.NameFrame.grid_columnconfigure(0, weight=1)
                        self.NameFrame.grid(row=0, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                        self.NameEntry = Entry(self.NameFrame, justify=CENTER, width=20, textvariable=self.NameEntryVar)
                        self.NameEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                        # Description Field
                        self.DescriptionFrame = LabelFrame(self.Window, text="Description:")
                        self.DescriptionFrame.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                        self.DescriptionField = ScrolledText(self.DescriptionFrame, Height=300, Width=250)
                        self.DescriptionField.grid(row=0, column=0)
                        self.DescriptionField.Text.insert(1.0, self.DescriptionVar.get())

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

                    def Submit(self):
                        self.DataSubmitted.set(True)
                        self.DescriptionVar.set(self.DescriptionField.get())
                        self.Window.destroy()

                    def Cancel(self):
                        self.DataSubmitted.set(False)
                        self.Window.destroy()

    # Spellcasting
    class Spellcasting:
        def __init__(self, master):
            self.SpellPointsMaxEntryVar = StringVar()
            self.SpellPointsRemainingEntryVar = StringVar()
            self.SpellUsingSpellPointsBoxVar = BooleanVar()
            self.ConcentrationBoxVar = BooleanVar()

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
            self.SpellNotesField = ScrolledText(self.SpellNotesFrame, Width=225, Height=330)
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
            self.SpellPointsMaxEntry = Entry(self.SpellPointsFrame, justify=CENTER, width=5, cursor="arrow", textvariable=self.SpellPointsMaxEntryVar)
            self.SpellPointsMaxEntry.grid(row=1, column=1, padx=2, pady=2, sticky=NSEW)
            self.SpellPointsMaxEntryStatModifierInst = StatModifier(self.SpellPointsMaxEntry, "<Button-1>", "Left-click on the spell points max to set a stat modifier.", "Spell Points Max")
            self.SpellPointsRemainingHeader = Label(self.SpellPointsFrame, text="Remaining", bd=2, relief=GROOVE)
            self.SpellPointsRemainingHeader.grid(row=2, column=0, padx=2, pady=2, sticky=NSEW)
            self.SpellPointsRemainingEntry = Entry(self.SpellPointsFrame, justify=CENTER, width=5, textvariable=self.SpellPointsRemainingEntryVar, state=DISABLED, disabledbackground=GlobalInst.ButtonColor,
                                                   disabledforeground="black",
                                                   cursor="arrow")
            self.SpellPointsRemainingEntry.grid(row=2, column=1, padx=2, pady=2, sticky=NSEW)
            self.SpellPointsRemainingEntry.bind("<Button-1>", self.ExpendSpellPoints)
            self.SpellPointsRemainingEntry.bind("<Button-3>", self.RestoreSpellPoints)
            StatusBarInst.TooltipConfig(self.SpellPointsRemainingEntry, "Left-click on the spell points remaining to expend points.  Right-click to restore.")

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

            # Add Saved Fields to Saved Data Dictionary
            SavingAndOpeningInst.SavedData["SpellPointsRemainingEntryVar"] = self.SpellPointsRemainingEntryVar
            SavingAndOpeningInst.SavedData["SpellNotesField"] = self.SpellNotesField
            SavingAndOpeningInst.SavedData["SpellUsingSpellPointsBoxVar"] = self.SpellUsingSpellPointsBoxVar
            SavingAndOpeningInst.SavedData["ConcentrationBoxVar"] = self.ConcentrationBoxVar
            self.SpellPointsMaxEntryStatModifierInst.AddToSavedData(Prefix="SpellPointsMaxEntry")

        def CalculateSpellPoints(self):
            if self.SpellUsingSpellPointsBoxVar.get():
                TotalPoints = 0
                for Level in self.SpellSlotsList:
                    TotalPoints += (Level.PointValue * GlobalInst.GetStringVarAsNumber(Level.SlotsEntryVar))
                TotalPoints += self.SpellPointsMaxEntryStatModifierInst.GetModifier()
                self.SpellPointsMaxEntryVar.set(str(TotalPoints))
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

            # Handle Values
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

            # Handle Values
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
                StatusBarInst.TooltipConfig(self.PreparedHeader, GlobalInst.SortTooltipString[:-29])
                self.NameHeader = Label(self.SpellListScrolledCanvas.WindowFrame, text="Name", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
                self.NameHeader.grid(row=0, column=1, sticky=NSEW)
                self.NameHeader.bind("<Button-1>", lambda event: self.Sort("Name"))
                self.NameHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Name", SearchMode=True))
                self.NameHeader.bind("<Button-3>", lambda event: self.Sort("Name", Reverse=True))
                StatusBarInst.TooltipConfig(self.NameHeader, GlobalInst.SortTooltipString)
                self.SortOrderHeader = Label(self.SpellListScrolledCanvas.WindowFrame, text="Sort\nOrder", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
                self.SortOrderHeader.grid(row=0, column=2, sticky=NSEW)
                self.SortOrderHeader.bind("<Button-1>", lambda event: self.Sort("Sort Order"))
                self.SortOrderHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Sort Order", SearchMode=True))
                self.SortOrderHeader.bind("<Button-3>", lambda event: self.Sort("Sort Order", Reverse=True))
                StatusBarInst.TooltipConfig(self.SortOrderHeader, GlobalInst.SortTooltipString)

                # Spell List Entries List
                self.SpellListEntriesList = []

                # Sort Order Values
                self.SortOrderValuesString = "\"\""
                for CurrentIndex in range(1, 26):
                    self.SortOrderValuesString += "," + str(CurrentIndex)
                self.SortOrderValuesTuple = eval(self.SortOrderValuesString)

                # Spell List Entries
                for CurrentIndex in range(1, 26):
                    CurrentEntry = self.SpellListEntry(self.SpellListScrolledCanvas, self.SpellListEntriesList, self.LevelName, self.SortOrderValuesTuple, self.ScrollingDisabledVar, CurrentIndex)
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
                            ListToSort.append((CurrentEntry, CurrentEntry.SortFields["Name"].get(), GlobalInst.GetStringVarAsNumber(CurrentEntry.SortFields[Column])))

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

            class SpellListEntry:
                def __init__(self, master, List, LevelName, SortOrderValuesTuple, ScrollingDisabledVar, Row):
                    # Store Parameters
                    self.master = master
                    self.LevelName = LevelName
                    self.SortOrderValuesTuple = SortOrderValuesTuple
                    self.ScrollingDisabledVar = ScrollingDisabledVar
                    self.Row = Row

                    # Variables
                    self.NameEntryVar = StringVar()
                    self.SchoolEntryVar = StringVar()
                    self.CastingTimeVar = StringVar()
                    self.RangeVar = StringVar()
                    self.ComponentsVar = StringVar()
                    self.DurationVar = StringVar()
                    self.DescriptionVar = StringVar()
                    self.PreparedBoxVar = BooleanVar()
                    self.SortOrderVar = StringVar()

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
                    self.NameEntry = Entry(master.WindowFrame, width=42, justify=CENTER, state=DISABLED, disabledbackground=GlobalInst.ButtonColor, disabledforeground="black", textvariable=self.NameEntryVar, cursor="arrow")
                    self.NameEntry.bind("<Button-1>", self.Set)
                    StatusBarInst.TooltipConfig(self.NameEntry, "Left-click on a spell list entry to set a name and description.")

                    # Sort Order
                    self.SortOrder = ttk.Combobox(master.WindowFrame, textvariable=self.SortOrderVar, values=self.SortOrderValuesTuple, width=5, state="readonly", justify=CENTER)
                    self.SortOrder.bind("<Enter>", self.DisableScrolling)
                    self.SortOrder.bind("<Leave>", self.EnableScrolling)

                    # Add Saved Fields to Saved Data Dictionary
                    SavingAndOpeningInst.SavedData["SpellEntryName" + self.LevelName + str(self.Row)] = self.NameEntryVar
                    SavingAndOpeningInst.SavedData["SchoolEntryName" + self.LevelName + str(self.Row)] = self.SchoolEntryVar
                    SavingAndOpeningInst.SavedData["SpellEntryCastingTime" + self.LevelName + str(self.Row)] = self.CastingTimeVar
                    SavingAndOpeningInst.SavedData["SpellEntryRange" + self.LevelName + str(self.Row)] = self.RangeVar
                    SavingAndOpeningInst.SavedData["SpellEntryComponents" + self.LevelName + str(self.Row)] = self.ComponentsVar
                    SavingAndOpeningInst.SavedData["SpellEntryDuration" + self.LevelName + str(self.Row)] = self.DurationVar
                    SavingAndOpeningInst.SavedData["SpellEntryDescription" + self.LevelName + str(self.Row)] = self.DescriptionVar
                    SavingAndOpeningInst.SavedData["SpellEntryPrepared" + self.LevelName + str(self.Row)] = self.PreparedBoxVar

                def Set(self, event):
                    # Create Config Window and Wait
                    SpellConfigInst = self.SpellConfig(WindowInst, self.NameEntryVar, self.SchoolEntryVar, self.CastingTimeVar, self.RangeVar, self.ComponentsVar, self.DurationVar, self.DescriptionVar)
                    WindowInst.wait_window(SpellConfigInst.Window)

                    # Handle Values
                    if SpellConfigInst.DataSubmitted.get():
                        self.NameEntryVar.set(SpellConfigInst.NameEntryVar.get())
                        self.SchoolEntryVar.set(SpellConfigInst.SchoolEntryVar.get())
                        self.CastingTimeVar.set(SpellConfigInst.CastingTimeVar.get())
                        self.RangeVar.set(SpellConfigInst.RangeVar.get())
                        self.ComponentsVar.set(SpellConfigInst.ComponentsVar.get())
                        self.DurationVar.set(SpellConfigInst.DurationVar.get())
                        self.DescriptionVar.set(SpellConfigInst.DescriptionVar.get())

                def Display(self, Row):
                    self.Row = Row

                    # Set Row Size
                    self.master.WindowFrame.grid_rowconfigure(self.Row, minsize=26)

                    # Place in Grid
                    self.PreparedBox.grid(row=self.Row, column=0, sticky=NSEW)
                    self.NameEntry.grid(row=self.Row, column=1, sticky=NSEW)
                    self.SortOrder.grid(row=self.Row, column=2, sticky=NSEW)

                    # Add Saved Fields to Saved Data Dictionary
                    SavingAndOpeningInst.SavedData["SpellEntryPrepared" + self.LevelName + str(self.Row)] = self.PreparedBoxVar
                    SavingAndOpeningInst.SavedData["SpellEntryName" + self.LevelName + str(self.Row)] = self.NameEntryVar
                    SavingAndOpeningInst.SavedData["SpellEntrySortOrder" + self.LevelName + str(self.Row)] = self.SortOrderVar
                    SavingAndOpeningInst.SavedData["SchoolEntryName" + self.LevelName + str(self.Row)] = self.SchoolEntryVar
                    SavingAndOpeningInst.SavedData["SpellEntryCastingTime" + self.LevelName + str(self.Row)] = self.CastingTimeVar
                    SavingAndOpeningInst.SavedData["SpellEntryRange" + self.LevelName + str(self.Row)] = self.RangeVar
                    SavingAndOpeningInst.SavedData["SpellEntryComponents" + self.LevelName + str(self.Row)] = self.ComponentsVar
                    SavingAndOpeningInst.SavedData["SpellEntryDuration" + self.LevelName + str(self.Row)] = self.DurationVar
                    SavingAndOpeningInst.SavedData["SpellEntryDescription" + self.LevelName + str(self.Row)] = self.DescriptionVar

                def DisableScrolling(self, event):
                    self.ScrollingDisabledVar.set(True)

                def EnableScrolling(self, event):
                    self.ScrollingDisabledVar.set(False)

                class SpellConfig:
                    def __init__(self, master, NameEntryVar, SchoolEntryVar, CastingTimeVar, RangeVar, ComponentsVar, DurationVar, DescriptionVar):
                        self.DataSubmitted = BooleanVar()
                        self.NameEntryVar = StringVar(value=NameEntryVar.get())
                        self.SchoolEntryVar = StringVar(value=SchoolEntryVar.get())
                        self.CastingTimeVar = StringVar(value=CastingTimeVar.get())
                        self.RangeVar = StringVar(value=RangeVar.get())
                        self.ComponentsVar = StringVar(value=ComponentsVar.get())
                        self.DurationVar = StringVar(value=DurationVar.get())
                        self.DescriptionVar = StringVar(value=DescriptionVar.get())

                        # Create Window
                        self.Window = Toplevel(master)
                        self.Window.wm_attributes("-toolwindow", 1)
                        self.Window.wm_title("Spell Description")

                        # Name Entry
                        self.NameFrame = LabelFrame(self.Window, text="Name:")
                        self.NameFrame.grid_columnconfigure(0, weight=1)
                        self.NameFrame.grid(row=0, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                        self.NameEntry = Entry(self.NameFrame, justify=CENTER, width=20, textvariable=self.NameEntryVar)
                        self.NameEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                        # School Entry
                        self.SchoolFrame = LabelFrame(self.Window, text="School:")
                        self.SchoolFrame.grid_columnconfigure(0, weight=1)
                        self.SchoolFrame.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                        self.SchoolEntry = Entry(self.SchoolFrame, justify=CENTER, width=10, textvariable=self.SchoolEntryVar)
                        self.SchoolEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                        # Casting Time
                        self.CastingTimeFrame = LabelFrame(self.Window, text="Casting Time:")
                        self.CastingTimeFrame.grid(row=2, column=0, padx=2, pady=2, sticky=NSEW)
                        self.CastingTimeField = ScrolledText(self.CastingTimeFrame, Height=34, Width=121)
                        self.CastingTimeField.grid(row=0, column=0)
                        self.CastingTimeField.Text.insert(1.0, self.CastingTimeVar.get())

                        # Range
                        self.RangeFrame = LabelFrame(self.Window, text="Range:")
                        self.RangeFrame.grid(row=2, column=1, padx=2, pady=2, sticky=NSEW)
                        self.RangeField = ScrolledText(self.RangeFrame, Height=34, Width=121)
                        self.RangeField.grid(row=0, column=0)
                        self.RangeField.Text.insert(1.0, self.RangeVar.get())

                        # Components
                        self.ComponentsFrame = LabelFrame(self.Window, text="Components:")
                        self.ComponentsFrame.grid(row=3, column=0, padx=2, pady=2, sticky=NSEW)
                        self.ComponentsField = ScrolledText(self.ComponentsFrame, Height=34, Width=121)
                        self.ComponentsField.grid(row=0, column=0)
                        self.ComponentsField.Text.insert(1.0, self.ComponentsVar.get())

                        # Duration
                        self.DurationFrame = LabelFrame(self.Window, text="Duration:")
                        self.DurationFrame.grid(row=3, column=1, padx=2, pady=2, sticky=NSEW)
                        self.DurationField = ScrolledText(self.DurationFrame, Height=34, Width=121)
                        self.DurationField.grid(row=0, column=0)
                        self.DurationField.Text.insert(1.0, self.DurationVar.get())

                        # Description Field
                        self.DescriptionFrame = LabelFrame(self.Window, text="Description:")
                        self.DescriptionFrame.grid(row=4, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                        self.DescriptionField = ScrolledText(self.DescriptionFrame, Height=300, Width=250)
                        self.DescriptionField.grid(row=0, column=0)
                        self.DescriptionField.Text.insert(1.0, self.DescriptionVar.get())

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

                    def Submit(self):
                        self.DataSubmitted.set(True)
                        self.CastingTimeVar.set(self.CastingTimeField.Text.get("1.0", "end-1c"))
                        self.RangeVar.set(self.RangeField.Text.get("1.0", "end-1c"))
                        self.ComponentsVar.set(self.ComponentsField.Text.get("1.0", "end-1c"))
                        self.DurationVar.set(self.DurationField.Text.get("1.0", "end-1c"))
                        self.DescriptionVar.set(self.DescriptionField.Text.get("1.0", "end-1c"))
                        self.Window.destroy()

                    def Cancel(self):
                        self.DataSubmitted.set(False)
                        self.Window.destroy()

        class SpellSlotsLevel:
            def __init__(self, master, List, SlotLevel, PointValue, Row):
                self.Row = Row
                self.SlotLevel = SlotLevel
                self.SlotsEntryVar = StringVar()
                self.UsedEntryVar = StringVar()
                self.PointValue = PointValue

                # Add to List
                List.append(self)

                # Label
                self.SlotLabel = Label(master, text=self.SlotLevel, bd=2, relief=GROOVE)
                self.SlotLabel.grid(row=self.Row, column=0, padx=2, pady=2, sticky=NSEW)

                # Slots
                self.SlotsEntry = Entry(master, width=1, justify=CENTER, textvariable=self.SlotsEntryVar)
                self.SlotsEntry.grid(row=self.Row, column=1, padx=2, pady=2, sticky=NSEW)

                # Used
                self.UsedEntry = Entry(master, width=1, justify=CENTER, textvariable=self.UsedEntryVar)
                self.UsedEntry.grid(row=self.Row, column=2, padx=2, pady=2, sticky=NSEW)

                # Add Saved Fields to Saved Data Dictionary
                SavingAndOpeningInst.SavedData[self.SlotLevel + "SlotsEntryVar"] = self.SlotsEntryVar
                SavingAndOpeningInst.SavedData[self.SlotLevel + "UsedEntryVar"] = self.UsedEntryVar

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
                self.SpellSlotDropdown = ttk.Combobox(self.Window, textvariable=self.SpellSlotDropdownVar, values=("", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th"), width=4, state="readonly", justify=CENTER)
                self.SpellSlotDropdown.grid(row=0, column=1, padx=2, pady=2, sticky=NSEW)
                self.ManualAmountEntry = Entry(self.Window, justify=CENTER, width=5, textvariable=self.ManualAmountEntryVar)
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

            def Submit(self):
                if self.ValidManualInput():
                    pass
                else:
                    return
                self.DataSubmitted.set(True)
                self.Window.destroy()

            def Cancel(self):
                self.DataSubmitted.set(False)
                self.Window.destroy()

            def ValidManualInput(self):
                try:
                    ManualInput = GlobalInst.GetStringVarAsNumber(self.ManualAmountEntryVar)
                except:
                    messagebox.showerror("Invalid Entry", "Manual amount must be a whole number.")
                    return False
                if ManualInput < 0:
                    messagebox.showerror("Invalid Entry", "Manual amount cannot be negative.")
                    return False
                return True

    # Inventory
    class Inventory:
        def __init__(self, master):
            # Variables
            self.CoinsEntryCPVar = StringVar()
            self.CoinsEntrySPVar = StringVar()
            self.CoinsEntryEPVar = StringVar()
            self.CoinsEntryGPVar = StringVar()
            self.CoinsEntryPPVar = StringVar()
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
            self.CarryingCapacityEntry = Entry(self.CarryingCapacityFrame, width=5, justify=CENTER, textvariable=self.CarryingCapacityVar, cursor="arrow", font=self.CarryingCapacityFont)
            self.CarryingCapacityEntry.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)
            self.CarryingCapacityEntryStatModifierInst = StatModifier(self.CarryingCapacityEntry, "<Button-1>", "Left-click on the carrying capacity to set a stat modifier.", "Carrying Capacity")

            # Loads
            self.LoadsFrame = LabelFrame(self.InventoryDataFrame, text="Loads (lbs.):")
            self.LoadsFrame.grid_rowconfigure(0, weight=1)
            self.LoadsFrame.grid_rowconfigure(1, weight=1)
            self.LoadsFrame.grid_rowconfigure(2, weight=1)
            self.LoadsFrame.grid_rowconfigure(3, weight=1)
            self.LoadsFrame.grid(row=0, column=2, padx=2, pady=2, sticky=NSEW, rowspan=2)
            self.TotalLoadLabel = Label(self.LoadsFrame, text="Total", bd=2, relief=GROOVE)
            self.TotalLoadLabel.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
            self.TotalLoadEntry = Entry(self.LoadsFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.TotalLoadEntryVar, cursor="arrow")
            self.TotalLoadEntry.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
            self.GearLoadLabel = Label(self.LoadsFrame, text="Gear", bd=2, relief=GROOVE)
            self.GearLoadLabel.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
            self.GearLoadEntry = Entry(self.LoadsFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.GearLoadEntryVar, cursor="arrow")
            self.GearLoadEntry.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
            self.TreasureLoadLabel = Label(self.LoadsFrame, text="Treasure", bd=2, relief=GROOVE)
            self.TreasureLoadLabel.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)
            self.TreasureLoadEntry = Entry(self.LoadsFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.TreasureLoadEntryVar, cursor="arrow")
            self.TreasureLoadEntry.grid(row=2, column=1, sticky=NSEW, padx=2, pady=2)
            self.MiscLoadLabel = Label(self.LoadsFrame, text="Misc", bd=2, relief=GROOVE)
            self.MiscLoadLabel.grid(row=3, column=0, sticky=NSEW, padx=2, pady=2)
            self.MiscLoadEntry = Entry(self.LoadsFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.MiscLoadEntryVar, cursor="arrow")
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
            self.TotalValueEntry = Entry(self.ValuesFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.TotalValueEntryVar, cursor="arrow")
            self.TotalValueEntry.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
            self.GearValueLabel = Label(self.ValuesFrame, text="Gear", bd=2, relief=GROOVE)
            self.GearValueLabel.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
            self.GearValueEntry = Entry(self.ValuesFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.GearValueEntryVar, cursor="arrow")
            self.GearValueEntry.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
            self.TreasureValueLabel = Label(self.ValuesFrame, text="Treasure", bd=2, relief=GROOVE)
            self.TreasureValueLabel.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)
            self.TreasureValueEntry = Entry(self.ValuesFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.TreasureValueEntryVar, cursor="arrow")
            self.TreasureValueEntry.grid(row=2, column=1, sticky=NSEW, padx=2, pady=2)
            self.MiscValueLabel = Label(self.ValuesFrame, text="Misc", bd=2, relief=GROOVE)
            self.MiscValueLabel.grid(row=3, column=0, sticky=NSEW, padx=2, pady=2)
            self.MiscValueEntry = Entry(self.ValuesFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.MiscValueEntryVar, cursor="arrow")
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
            self.CoinsEntryCP = Entry(self.CoinsInputHolderFrame, width=5, justify=CENTER, textvariable=self.CoinsEntryCPVar)
            self.CoinsEntryCP.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
            self.CoinsHeaderSP = Label(self.CoinsInputHolderFrame, text="SP", bd=2, relief=GROOVE)
            self.CoinsHeaderSP.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
            self.CoinsEntrySP = Entry(self.CoinsInputHolderFrame, width=5, justify=CENTER, textvariable=self.CoinsEntrySPVar)
            self.CoinsEntrySP.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
            self.CoinsHeaderEP = Label(self.CoinsInputHolderFrame, text="EP", bd=2, relief=GROOVE)
            self.CoinsHeaderEP.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
            self.CoinsEntryEP = Entry(self.CoinsInputHolderFrame, width=5, justify=CENTER, textvariable=self.CoinsEntryEPVar)
            self.CoinsEntryEP.grid(row=1, column=2, sticky=NSEW, padx=2, pady=2)
            self.CoinsHeaderGP = Label(self.CoinsInputHolderFrame, text="GP", bd=2, relief=GROOVE)
            self.CoinsHeaderGP.grid(row=0, column=3, sticky=NSEW, padx=2, pady=2)
            self.CoinsEntryGP = Entry(self.CoinsInputHolderFrame, width=5, justify=CENTER, textvariable=self.CoinsEntryGPVar)
            self.CoinsEntryGP.grid(row=1, column=3, sticky=NSEW, padx=2, pady=2)
            self.CoinsHeaderPP = Label(self.CoinsInputHolderFrame, text="PP", bd=2, relief=GROOVE)
            self.CoinsHeaderPP.grid(row=0, column=4, sticky=NSEW, padx=2, pady=2)
            self.CoinsEntryPP = Entry(self.CoinsInputHolderFrame, width=5, justify=CENTER, textvariable=self.CoinsEntryPPVar)
            self.CoinsEntryPP.grid(row=1, column=4, sticky=NSEW, padx=2, pady=2)

            # Coin Value and Weight
            self.CoinValueAndWeightHolderFrame = Frame(self.CoinsFrame)
            self.CoinValueAndWeightHolderFrame.grid_columnconfigure(0, weight=1)
            self.CoinValueAndWeightHolderFrame.grid_columnconfigure(1, weight=1)
            self.CoinValueAndWeightHolderFrame.grid(row=2, column=1, sticky=NSEW)
            self.CoinValueHeader = Label(self.CoinValueAndWeightHolderFrame, text="Coin Value\n(gp)", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.CoinValueHeader.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
            self.CoinValueHeader.bind("<Button-1>", self.SpendCoins)
            StatusBarInst.TooltipConfig(self.CoinValueHeader, "Left-click to spend coins.")
            self.CoinValueEntry = Entry(self.CoinValueAndWeightHolderFrame, width=13, justify=CENTER, textvariable=self.CoinValueEntryVar, state=DISABLED, disabledforeground="black", disabledbackground="light gray",
                                        cursor="arrow")
            self.CoinValueEntry.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
            self.CoinWeightHeader = Label(self.CoinValueAndWeightHolderFrame, text="Coin Weight\n(lbs.)", bd=2, relief=GROOVE)
            self.CoinWeightHeader.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
            self.CoinWeightEntry = Entry(self.CoinValueAndWeightHolderFrame, width=13, justify=CENTER, textvariable=self.CoinWeightEntryVar, state=DISABLED, disabledforeground="black", disabledbackground="light gray",
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
            StatusBarInst.TooltipConfig(self.InventoryListNameHeader, GlobalInst.SortTooltipString)
            self.InventoryListCountHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Count", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.InventoryListCountHeader.grid(row=0, column=1, sticky=NSEW)
            self.InventoryListCountHeader.bind("<Button-1>", lambda event: self.Sort("Count"))
            self.InventoryListCountHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Count", SearchMode=True))
            self.InventoryListCountHeader.bind("<Button-3>", lambda event: self.Sort("Count", Reverse=True))
            StatusBarInst.TooltipConfig(self.InventoryListCountHeader, GlobalInst.SortTooltipString)
            self.InventoryListUnitWeightHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Unit Weight\n(lb.)", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.InventoryListUnitWeightHeader.grid(row=0, column=2, sticky=NSEW)
            self.InventoryListUnitWeightHeader.bind("<Button-1>", lambda event: self.Sort("Unit Weight"))
            self.InventoryListUnitWeightHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Unit Weight", SearchMode=True))
            self.InventoryListUnitWeightHeader.bind("<Button-3>", lambda event: self.Sort("Unit Weight", Reverse=True))
            StatusBarInst.TooltipConfig(self.InventoryListUnitWeightHeader, GlobalInst.SortTooltipString)
            self.InventoryListUnitValueHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Unit Value", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.InventoryListUnitValueHeader.grid(row=0, column=3, sticky=NSEW)
            self.InventoryListUnitValueHeader.bind("<Button-1>", lambda event: self.Sort("Unit Value"))
            self.InventoryListUnitValueHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Unit Value", SearchMode=True))
            self.InventoryListUnitValueHeader.bind("<Button-3>", lambda event: self.Sort("Unit Value", Reverse=True))
            StatusBarInst.TooltipConfig(self.InventoryListUnitValueHeader, GlobalInst.SortTooltipString)
            self.InventoryListUnitValueDenominationHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Value\nDenom.", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.InventoryListUnitValueDenominationHeader.grid(row=0, column=4, sticky=NSEW)
            self.InventoryListUnitValueDenominationHeader.bind("<Button-1>", lambda event: self.Sort("Value Denomination"))
            self.InventoryListUnitValueDenominationHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Value Denomination", SearchMode=True))
            self.InventoryListUnitValueDenominationHeader.bind("<Button-3>", lambda event: self.Sort("Value Denomination", Reverse=True))
            StatusBarInst.TooltipConfig(self.InventoryListUnitValueDenominationHeader, GlobalInst.SortTooltipString)
            self.InventoryListTotalWeightHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Total Weight\n(lb.)", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.InventoryListTotalWeightHeader.grid(row=0, column=5, sticky=NSEW)
            self.InventoryListTotalWeightHeader.bind("<Button-1>", lambda event: self.Sort("Total Weight"))
            self.InventoryListTotalWeightHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Total Weight", SearchMode=True))
            self.InventoryListTotalWeightHeader.bind("<Button-3>", lambda event: self.Sort("Total Weight", Reverse=True))
            StatusBarInst.TooltipConfig(self.InventoryListTotalWeightHeader, GlobalInst.SortTooltipString)
            self.InventoryListTotalValueHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Total Value\n(gp)", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.InventoryListTotalValueHeader.grid(row=0, column=6, sticky=NSEW)
            self.InventoryListTotalValueHeader.bind("<Button-1>", lambda event: self.Sort("Total Value"))
            self.InventoryListTotalValueHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Total Value", SearchMode=True))
            self.InventoryListTotalValueHeader.bind("<Button-3>", lambda event: self.Sort("Total Value", Reverse=True))
            StatusBarInst.TooltipConfig(self.InventoryListTotalValueHeader, GlobalInst.SortTooltipString)
            self.InventoryListTagHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Tag", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.InventoryListTagHeader.grid(row=0, column=7, sticky=NSEW)
            self.InventoryListTagHeader.bind("<Button-1>", lambda event: self.Sort("Tag"))
            self.InventoryListTagHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Tag", SearchMode=True))
            self.InventoryListTagHeader.bind("<Button-3>", lambda event: self.Sort("Tag", Reverse=True))
            StatusBarInst.TooltipConfig(self.InventoryListTagHeader, GlobalInst.SortTooltipString)
            self.InventoryListSortOrderHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Sort\nOrder", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.InventoryListSortOrderHeader.grid(row=0, column=8, sticky=NSEW)
            self.InventoryListSortOrderHeader.bind("<Button-1>", lambda event: self.Sort("Sort Order"))
            self.InventoryListSortOrderHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Sort Order", SearchMode=True))
            self.InventoryListSortOrderHeader.bind("<Button-3>", lambda event: self.Sort("Sort Order", Reverse=True))
            StatusBarInst.TooltipConfig(self.InventoryListSortOrderHeader, GlobalInst.SortTooltipString)

            # Inventory Entries List
            self.InventoryEntriesList = []

            # Sort Order Values
            self.SortOrderValuesString = "\"\""
            for CurrentIndex in range(1, 101):
                self.SortOrderValuesString += "," + str(CurrentIndex)
            self.SortOrderValuesTuple = eval(self.SortOrderValuesString)

            # Inventory Entries
            for CurrentIndex in range(1, 101):
                CurrentEntry = self.InventoryEntry(self.InventoryListScrolledCanvas.WindowFrame, self.InventoryEntriesList, self.ScrollingDisabledVar, self.SortOrderValuesTuple, CurrentIndex)
                CurrentEntry.Display(CurrentIndex)

            # Add Saved Fields to Saved Data Dictionary
            SavingAndOpeningInst.SavedData["CoinsEntryCPVar"] = self.CoinsEntryCPVar
            SavingAndOpeningInst.SavedData["CoinsEntrySPVar"] = self.CoinsEntrySPVar
            SavingAndOpeningInst.SavedData["CoinsEntryEPVar"] = self.CoinsEntryEPVar
            SavingAndOpeningInst.SavedData["CoinsEntryGPVar"] = self.CoinsEntryGPVar
            SavingAndOpeningInst.SavedData["CoinsEntryPPVar"] = self.CoinsEntryPPVar
            self.CarryingCapacityEntryStatModifierInst.AddToSavedData(Prefix="CarryingCapacityEntry")

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
            if self.ValidInventoryEntry():
                pass
            else:
                return

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
                        ListToSort.append((CurrentEntry, CurrentEntry.SortFields["Name"].get(), GlobalInst.GetStringVarAsNumber(CurrentEntry.SortFields[Column])))

                    # Sort the List
                    SortedList = sorted(ListToSort, key=lambda x: ((not Reverse and x[1] == "") or (Reverse and x[1] != ""), x[2]), reverse=Reverse)
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

        def ValidCoinsEntry(self):
            try:
                CPInt = GlobalInst.GetStringVarAsNumber(self.CoinsEntryCPVar)
                SPInt = GlobalInst.GetStringVarAsNumber(self.CoinsEntrySPVar)
                EPInt = GlobalInst.GetStringVarAsNumber(self.CoinsEntryEPVar)
                GPInt = GlobalInst.GetStringVarAsNumber(self.CoinsEntryGPVar)
                PPInt = GlobalInst.GetStringVarAsNumber(self.CoinsEntryPPVar)
            except:
                messagebox.showerror("Invalid Entry", "Coins must be whole numbers.")
                return False
            if CPInt < 0 or SPInt < 0 or EPInt < 0 or GPInt < 0 or PPInt < 0:
                messagebox.showerror("Invalid Entry", "Coins must be positive or 0.")
                return False
            return True

        def ValidInventoryEntry(self):
            if self.ValidCoinsEntry():
                pass
            else:
                return False
            for Entry in self.InventoryEntriesList:
                try:
                    CountInt = GlobalInst.GetStringVarAsNumber(Entry.CountEntryVar)
                    WeightFloat = GlobalInst.GetStringVarAsNumber(Entry.UnitWeightEntryVar, Mode="Float")
                    ValueFloat = GlobalInst.GetStringVarAsNumber(Entry.UnitValueEntryVar, Mode="Float")
                except:
                    messagebox.showerror("Invalid Entry", "Inventory item counts must be whole numbers, and unit weights and values must be numbers.")
                    return False
                if CountInt < 0 or WeightFloat < 0 or ValueFloat < 0:
                    messagebox.showerror("Invalid Entry", "Inventory item counts, unit weights, and unit values must be positive or 0.")
                    return False
            return True

        def OpenCoinCalculator(self):
            # Create Coin Calculator Window and Wait
            self.CoinCalculatorInst = CoinCalculator(WindowInst, DialogMode=True)
            WindowInst.wait_window(self.CoinCalculatorInst.Window)

        def SpendCoins(self, event):
            # Valid Coins Entry
            if self.ValidCoinsEntry():
                pass
            else:
                return

            # Create Config Window and Wait
            SpendCoinsMenuInst = self.SpendCoinsMenu(WindowInst, self.SpendingCoins)
            WindowInst.wait_window(SpendCoinsMenuInst.Window)

            # Handle Values
            if SpendCoinsMenuInst.DataSubmitted.get():
                for Denomination in SpendCoinsMenuInst.Remaining.keys():
                    self.SpendingCoins[Denomination].set(SpendCoinsMenuInst.Remaining[Denomination].get())

        class SpendCoinsMenu:
            def __init__(self, master, Coins):
                # Store Parameters
                self.Coins = Coins

                # Variables
                self.DataSubmitted = BooleanVar()
                self.SpendCPEntryVar = StringVar()
                self.SpendSPEntryVar = StringVar()
                self.SpendEPEntryVar = StringVar()
                self.SpendGPEntryVar = StringVar()
                self.SpendPPEntryVar = StringVar()
                self.RemainingCPEntryVar = StringVar(value=self.Coins["CP"].get())
                self.RemainingSPEntryVar = StringVar(value=self.Coins["SP"].get())
                self.RemainingEPEntryVar = StringVar(value=self.Coins["EP"].get())
                self.RemainingGPEntryVar = StringVar(value=self.Coins["GP"].get())
                self.RemainingPPEntryVar = StringVar(value=self.Coins["PP"].get())
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
                self.SpendCPEntry = Entry(self.SpendFrame, textvariable=self.SpendCPEntryVar, justify=CENTER, width=5)
                self.SpendCPEntry.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
                self.SpendSPEntry = Entry(self.SpendFrame, textvariable=self.SpendSPEntryVar, justify=CENTER, width=5)
                self.SpendSPEntry.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
                self.SpendEPEntry = Entry(self.SpendFrame, textvariable=self.SpendEPEntryVar, justify=CENTER, width=5)
                self.SpendEPEntry.grid(row=1, column=2, sticky=NSEW, padx=2, pady=2)
                self.SpendGPEntry = Entry(self.SpendFrame, textvariable=self.SpendGPEntryVar, justify=CENTER, width=5)
                self.SpendGPEntry.grid(row=1, column=3, sticky=NSEW, padx=2, pady=2)
                self.SpendPPEntry = Entry(self.SpendFrame, textvariable=self.SpendPPEntryVar, justify=CENTER, width=5)
                self.SpendPPEntry.grid(row=1, column=4, sticky=NSEW, padx=2, pady=2)

                # Match Values
                self.MatchValuesFrame = LabelFrame(self.Window, text="Match Values:")
                self.MatchValuesFrame.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
                self.MatchValuesAfterSpendingHeader = Label(self.MatchValuesFrame, text="Value After\nSpending (CP)", bd=2, relief=GROOVE)
                self.MatchValuesAfterSpendingHeader.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
                self.MatchValuesAfterSpendingEntry = Entry(self.MatchValuesFrame, textvariable=self.MatchValuesAfterSpendingEntryVar, width=20, state=DISABLED, disabledforeground="black", disabledbackground="light gray",
                                                           cursor="arrow", justify=CENTER)
                self.MatchValuesAfterSpendingEntry.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
                self.MatchValuesComparatorEntry = Entry(self.MatchValuesFrame, textvariable=self.MatchValuesComparatorEntryVar, width=5, state=DISABLED, disabledforeground="black", disabledbackground="lightgray", cursor="arrow",
                                                        justify=CENTER)
                self.MatchValuesComparatorEntry.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
                self.MatchValuesRemainingHeader = Label(self.MatchValuesFrame, text="Remaining Coins\nValue (CP)", bd=2, relief=GROOVE)
                self.MatchValuesRemainingHeader.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
                self.MatchValuesRemainingEntry = Entry(self.MatchValuesFrame, textvariable=self.MatchValuesRemainingEntryVar, width=20, state=DISABLED, disabledforeground="black", disabledbackground="light gray",
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
                self.RemainingCPEntry = Entry(self.RemainingFrame, textvariable=self.RemainingCPEntryVar, justify=CENTER, width=5)
                self.RemainingCPEntry.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
                self.RemainingSPEntry = Entry(self.RemainingFrame, textvariable=self.RemainingSPEntryVar, justify=CENTER, width=5)
                self.RemainingSPEntry.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
                self.RemainingEPEntry = Entry(self.RemainingFrame, textvariable=self.RemainingEPEntryVar, justify=CENTER, width=5)
                self.RemainingEPEntry.grid(row=1, column=2, sticky=NSEW, padx=2, pady=2)
                self.RemainingGPEntry = Entry(self.RemainingFrame, textvariable=self.RemainingGPEntryVar, justify=CENTER, width=5)
                self.RemainingGPEntry.grid(row=1, column=3, sticky=NSEW, padx=2, pady=2)
                self.RemainingPPEntry = Entry(self.RemainingFrame, textvariable=self.RemainingPPEntryVar, justify=CENTER, width=5)
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
                self.ButtonsFrame.grid_columnconfigure(2, weight=1)
                self.ButtonsFrame.grid(row=3, column=0, sticky=NSEW)

                # Submit Button
                self.SubmitButton = Button(self.ButtonsFrame, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
                self.SubmitButton.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                # Calculate Button
                self.CalculateButton = Button(self.ButtonsFrame, text="Calculate", command=self.Calculate, bg=GlobalInst.ButtonColor)
                self.CalculateButton.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)

                # Cancel Button
                self.CancelButton = Button(self.ButtonsFrame, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
                self.CancelButton.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)

                # Prevent Main Window Input
                self.Window.grab_set()

                # Handle Config Window Geometry and Focus
                GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst)
                self.Window.focus_force()

                # Initial Calculation
                self.Calculate(ValidateSpending=True)

            def Submit(self):
                if self.Calculate(ValidateSpending=True):
                    pass
                else:
                    return
                self.DataSubmitted.set(True)
                self.Window.destroy()

            def ValidEntry(self):
                try:
                    SpendCPInt = GlobalInst.GetStringVarAsNumber(self.SpendCPEntryVar)
                    SpendSPInt = GlobalInst.GetStringVarAsNumber(self.SpendSPEntryVar)
                    SpendEPInt = GlobalInst.GetStringVarAsNumber(self.SpendEPEntryVar)
                    SpendGPInt = GlobalInst.GetStringVarAsNumber(self.SpendGPEntryVar)
                    SpendPPInt = GlobalInst.GetStringVarAsNumber(self.SpendPPEntryVar)
                    RemainingCPInt = GlobalInst.GetStringVarAsNumber(self.RemainingCPEntryVar)
                    RemainingSPInt = GlobalInst.GetStringVarAsNumber(self.RemainingSPEntryVar)
                    RemainingEPInt = GlobalInst.GetStringVarAsNumber(self.RemainingEPEntryVar)
                    RemainingGPInt = GlobalInst.GetStringVarAsNumber(self.RemainingGPEntryVar)
                    RemainingPPInt = GlobalInst.GetStringVarAsNumber(self.RemainingPPEntryVar)
                except:
                    messagebox.showerror("Invalid Entry", "Coins must be whole numbers.")
                    return False
                CoinIntsList = [SpendCPInt, SpendSPInt, SpendEPInt, SpendGPInt, SpendPPInt, RemainingCPInt, RemainingSPInt, RemainingEPInt, RemainingGPInt, RemainingPPInt]
                for CoinInt in CoinIntsList:
                    if CoinInt < 0:
                        messagebox.showerror("Invalid Entry", "Coins must be positive or 0.")
                        return False
                return True

            def Calculate(self, ValidateSpending=False):
                # Validate Entry
                if self.ValidEntry():
                    pass
                else:
                    return

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
                    if ComparatorString is "=":
                        return True
                    else:
                        messagebox.showerror("Spending Invalid", "The value of your coins after spending and the value of the coins you have remaining must match.\n\nAdjust coins remaining until the values are equal.")
                        return False

            def Cancel(self):
                self.DataSubmitted.set(False)
                self.Window.destroy()

        class InventoryEntry:
            def __init__(self, master, List, ScrollingDisabledVar, SortOrderValuesTuple, Row):
                # Store Parameters
                self.master = master
                self.ScrollingDisabledVar = ScrollingDisabledVar
                self.SortOrderValuesTuple = SortOrderValuesTuple
                self.Row = Row

                # Variables
                self.NameEntryVar = StringVar()
                self.CountEntryVar = StringVar()
                self.UnitWeightEntryVar = StringVar()
                self.UnitValueEntryVar = StringVar()
                self.UnitValueDenominationVar = StringVar()
                self.TotalWeightEntryVar = StringVar()
                self.TotalValueEntryVar = StringVar()
                self.CategoryTagVar = StringVar()
                self.SortOrderVar = StringVar()
                self.CategoryEntryVar = StringVar()
                self.RarityEntryVar = StringVar()
                self.DescriptionVar = StringVar()

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
                self.NameEntry = Entry(master, width=35, textvariable=self.NameEntryVar, justify=CENTER, bg=GlobalInst.ButtonColor)
                self.NameEntry.bind("<Button-3>", self.ConfigureMagicItem)
                StatusBarInst.TooltipConfig(self.NameEntry, "Right-click on the name field to set an item description.")

                # Count Entry
                self.CountEntry = Entry(master, width=4, textvariable=self.CountEntryVar, justify=CENTER)

                # Unit Weight Entry
                self.UnitWeightEntry = Entry(master, width=4, textvariable=self.UnitWeightEntryVar, justify=CENTER)

                # Unit Value Entry
                self.UnitValueEntry = Entry(master, width=4, textvariable=self.UnitValueEntryVar, justify=CENTER)

                # Unit Value Denomination
                self.UnitValueDenomination = ttk.Combobox(master, textvariable=self.UnitValueDenominationVar, values=("", "cp", "sp", "ep", "gp", "pp"), width=2, state="readonly", justify=CENTER)
                self.UnitValueDenomination.bind("<Enter>", self.DisableScrolling)
                self.UnitValueDenomination.bind("<Leave>", self.EnableScrolling)

                # Total Weight Entry
                self.TotalWeightEntry = Entry(master, width=4, textvariable=self.TotalWeightEntryVar, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow")

                # Total Value Entry
                self.TotalValueEntry = Entry(master, width=4, textvariable=self.TotalValueEntryVar, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow")

                # Category Tag
                self.CategoryTag = ttk.Combobox(master, textvariable=self.CategoryTagVar, values=("", "Gear", "Food", "Water", "Treasure", "Misc."), width=8, state="readonly", justify=CENTER)
                self.CategoryTag.bind("<Enter>", self.DisableScrolling)
                self.CategoryTag.bind("<Leave>", self.EnableScrolling)

                # Sort Order
                self.SortOrder = ttk.Combobox(master, textvariable=self.SortOrderVar, values=self.SortOrderValuesTuple, width=5, state="readonly", justify=CENTER)
                self.SortOrder.bind("<Enter>", self.DisableScrolling)
                self.SortOrder.bind("<Leave>", self.EnableScrolling)

            def DisableScrolling(self, event):
                self.ScrollingDisabledVar.set(True)

            def EnableScrolling(self, event):
                self.ScrollingDisabledVar.set(False)

            def ConfigureMagicItem(self, event):
                # Create Window and Wait
                MagicItemMenuInst = self.ItemDescriptionMenu(WindowInst, self.NameEntryVar, self.CategoryEntryVar, self.RarityEntryVar, self.DescriptionVar)
                WindowInst.wait_window(MagicItemMenuInst.Window)

                # Handle Variables
                if MagicItemMenuInst.DataSubmitted.get():
                    self.NameEntryVar.set(MagicItemMenuInst.NameEntryVar.get())
                    self.CategoryEntryVar.set(MagicItemMenuInst.CategoryEntryVar.get())
                    self.RarityEntryVar.set(MagicItemMenuInst.RarityEntryVar.get())
                    self.DescriptionVar.set(MagicItemMenuInst.DescriptionVar.get())

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

                # Add Saved Fields to Saved Data Dictionary
                SavingAndOpeningInst.SavedData["InventoryListNameEntryVar" + str(self.Row)] = self.NameEntryVar
                SavingAndOpeningInst.SavedData["InventoryListCountEntryVar" + str(self.Row)] = self.CountEntryVar
                SavingAndOpeningInst.SavedData["InventoryListUnitWeightEntryVar" + str(self.Row)] = self.UnitWeightEntryVar
                SavingAndOpeningInst.SavedData["InventoryListUnitValueEntryVar" + str(self.Row)] = self.UnitValueEntryVar
                SavingAndOpeningInst.SavedData["InventoryListUnitValueDenominationVar" + str(self.Row)] = self.UnitValueDenominationVar
                SavingAndOpeningInst.SavedData["InventoryListCategoryTagVar" + str(self.Row)] = self.CategoryTagVar
                SavingAndOpeningInst.SavedData["InventoryListMagicItemCategoryEntryVar" + str(self.Row)] = self.CategoryEntryVar
                SavingAndOpeningInst.SavedData["InventoryListMagicItemRarityEntryVar" + str(self.Row)] = self.RarityEntryVar
                SavingAndOpeningInst.SavedData["InventoryListMagicItemDescriptionVar" + str(self.Row)] = self.DescriptionVar
                SavingAndOpeningInst.SavedData["SortOrderVar" + str(self.Row)] = self.SortOrderVar

            class ItemDescriptionMenu:
                def __init__(self, master, NameEntryVar, CategoryEntryVar, RarityEntryVar, DescriptionVar):
                    self.DataSubmitted = BooleanVar()
                    self.NameEntryVar = StringVar(value=NameEntryVar.get())
                    self.CategoryEntryVar = StringVar(value=CategoryEntryVar.get())
                    self.RarityEntryVar = StringVar(value=RarityEntryVar.get())
                    self.DescriptionVar = StringVar(value=DescriptionVar.get())

                    # Create Window
                    self.Window = Toplevel(master)
                    self.Window.wm_attributes("-toolwindow", 1)
                    self.Window.wm_title("Item Description")

                    # Name Entry
                    self.NameFrame = LabelFrame(self.Window, text="Name:")
                    self.NameFrame.grid_columnconfigure(0, weight=1)
                    self.NameFrame.grid(row=0, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                    self.NameEntry = Entry(self.NameFrame, justify=CENTER, width=35, textvariable=self.NameEntryVar)
                    self.NameEntry.grid(row=0, column=0, sticky=NSEW)

                    # Category Entry
                    self.CategoryFrame = LabelFrame(self.Window, text="Category:")
                    self.CategoryFrame.grid_columnconfigure(0, weight=1)
                    self.CategoryFrame.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)
                    self.CategoryEntry = Entry(self.CategoryFrame, justify=CENTER, textvariable=self.CategoryEntryVar, width=15)
                    self.CategoryEntry.grid(row=0, column=0, sticky=NSEW)

                    # Rarity Entry
                    self.RarityFrame = LabelFrame(self.Window, text="Rarity:")
                    self.RarityFrame.grid_columnconfigure(0, weight=1)
                    self.RarityFrame.grid(row=1, column=1, padx=2, pady=2, sticky=NSEW)
                    self.RarityEntry = Entry(self.RarityFrame, justify=CENTER, textvariable=self.RarityEntryVar, width=15)
                    self.RarityEntry.grid(row=0, column=0, sticky=NSEW)

                    # Description Field
                    self.DescriptionFrame = LabelFrame(self.Window, text="Description:")
                    self.DescriptionFrame.grid(row=2, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                    self.DescriptionField = ScrolledText(self.DescriptionFrame, Height=300, Width=250)
                    self.DescriptionField.grid(row=0, column=0)
                    self.DescriptionField.Text.insert(1.0, self.DescriptionVar.get())

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

                def Submit(self):
                    self.DataSubmitted.set(True)
                    self.DescriptionVar.set(self.DescriptionField.get())
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
                self.ConsumptionRateVar = StringVar(value=self.ConsumptionRateDefault)

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
                self.LoadEntry = Entry(self.SupplyDisplayFrame, textvariable=self.LoadEntryVar, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow")
                self.LoadEntry.grid(row=0, column=1, sticky=NSEW)
                self.DaysEntry = Entry(self.SupplyDisplayFrame, textvariable=self.DaysEntryVar, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground=GlobalInst.ButtonColor, cursor="arrow")
                self.DaysEntry.grid(row=1, column=1, sticky=NSEW)
                self.DaysEntry.bind("<Button-1>", self.SetConsumptionRate)
                StatusBarInst.TooltipConfig(self.DaysEntry, "Left-click to set the consumption rate per day for supplies.")

                # Add Saved Field to Saved Data Dictionary
                SavingAndOpeningInst.SavedData[self.Tag + "ConsumptionRateVar"] = self.ConsumptionRateVar

            def grid(self, *args, **kwargs):
                self.SupplyDisplayFrame.grid(*args, **kwargs)

            def pack(self, *args, **kwargs):
                self.SupplyDisplayFrame.pack(*args, **kwargs)

            def SetConsumptionRate(self, event):
                # Test Stats Input Validity
                if CharacterSheetInst.ValidStatsEntry():
                    pass
                else:
                    return

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
                    self.ConsumptionRateHeader = Label(self.TableFrame, text="How many pounds of supplies tagged\n\"" + self.Tag + "\" do you consume daily?", bd=2, relief=GROOVE)
                    self.ConsumptionRateHeader.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
                    self.ConsumptionRateEntry = Entry(self.TableFrame, width=20, textvariable=self.ConsumptionRateEntryVar, justify=CENTER)
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
                    if self.ValidEntry():
                        pass
                    else:
                        return
                    self.DataSubmitted.set(True)
                    self.Window.destroy()

                def Cancel(self):
                    self.DataSubmitted.set(False)
                    self.Window.destroy()

                    return None

                def GetData(self):
                    return GlobalInst.GetStringVarAsNumber(self.ConsumptionRateEntryVar, Mode="Decimal")

                def ValidEntry(self):
                    try:
                        EntryValue = GlobalInst.GetStringVarAsNumber(self.ConsumptionRateEntryVar, Mode="Decimal")
                    except:
                        messagebox.showerror("Invalid Entry", "Must be a number.")
                        return False
                    if EntryValue < 0:
                        messagebox.showerror("Invalid Entry", "Must be at least 0.")
                        return False
                    return True

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
            self.NotesField1 = ScrolledText(master, Height=490, Width=230)
            self.NotesField1.grid(row=0, column=1, padx=2, pady=2, sticky=NSEW)
            self.NotesField2 = ScrolledText(master, Height=490, Width=230)
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
            StatusBarInst.TooltipConfig(self.NameHeader, GlobalInst.SortTooltipString)
            self.SortOrderHeader = Label(self.AdditionalNotesScrolledCanvas.WindowFrame, text="Sort\nOrder", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.SortOrderHeader.grid(row=0, column=1, sticky=NSEW)
            self.SortOrderHeader.bind("<Button-1>", lambda event: self.Sort("Sort Order"))
            self.SortOrderHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Sort Order", SearchMode=True))
            self.SortOrderHeader.bind("<Button-3>", lambda event: self.Sort("Sort Order", Reverse=True))
            StatusBarInst.TooltipConfig(self.SortOrderHeader, GlobalInst.SortTooltipString)

            # Additional Notes Entries List
            self.AdditionalNotesEntriesList = []

            # Sort Order Values
            self.SortOrderValuesString = "\"\""
            for CurrentIndex in range(1, 101):
                self.SortOrderValuesString += "," + str(CurrentIndex)
            self.SortOrderValuesTuple = eval(self.SortOrderValuesString)

            # Additional Notes Entries
            for CurrentIndex in range(1, 101):
                CurrentEntry = self.AdditionalNotesEntry(self.AdditionalNotesScrolledCanvas.WindowFrame, self.AdditionalNotesEntriesList, self.ScrollingDisabledVar, self.SortOrderValuesTuple, CurrentIndex)
                CurrentEntry.Display(CurrentIndex)

            # Add Saved Field to Saved Data Dictionary
            SavingAndOpeningInst.SavedData["NotesField1"] = self.NotesField1
            SavingAndOpeningInst.SavedData["NotesField2"] = self.NotesField2

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
                        ListToSort.append((CurrentEntry, CurrentEntry.SortFields["Name"].get(), GlobalInst.GetStringVarAsNumber(CurrentEntry.SortFields[Column])))

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

        class AdditionalNotesEntry:
            def __init__(self, master, List, ScrollingDisabledVar, SortOrderValuesTuple, Row):
                # Store Parameters
                self.master = master
                self.ScrollingDisabledVar = ScrollingDisabledVar
                self.SortOrderValuesTuple = SortOrderValuesTuple
                self.Row = Row

                # Variables
                self.NameEntryVar = StringVar()
                self.SortOrderVar = StringVar()
                self.NoteVar = StringVar()

                # Sort Fields
                self.SortFields = {}
                self.SortFields["Name"] = self.NameEntryVar
                self.SortFields["Sort Order"] = self.SortOrderVar

                # Add to List
                List.append(self)

                # Name Entry
                self.NameEntry = Entry(master, width=28, justify=CENTER, state=DISABLED, disabledbackground=GlobalInst.ButtonColor, disabledforeground="black", textvariable=self.NameEntryVar, cursor="arrow")
                self.NameEntry.bind("<Button-1>", self.SetNote)
                StatusBarInst.TooltipConfig(self.NameEntry, "Left-click on a note entry to set a note.")

                # Sort Order
                self.SortOrder = ttk.Combobox(master, textvariable=self.SortOrderVar, values=self.SortOrderValuesTuple, width=5, state="readonly", justify=CENTER)
                self.SortOrder.bind("<Enter>", self.DisableScrolling)
                self.SortOrder.bind("<Leave>", self.EnableScrolling)

            def SetNote(self, event):
                # Create Config Window and Wait
                NoteConfigInst = self.NoteConfig(WindowInst, self.NameEntryVar, self.NoteVar)
                WindowInst.wait_window(NoteConfigInst.Window)

                # Handle Values
                if NoteConfigInst.DataSubmitted.get():
                    self.NameEntryVar.set(NoteConfigInst.NameEntryVar.get())
                    self.NoteVar.set(NoteConfigInst.NoteVar.get())

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

                # Add Saved Fields to Saved Data Dictionary
                SavingAndOpeningInst.SavedData["AdditionalNotesNameEntryVar" + str(self.Row)] = self.NameEntryVar
                SavingAndOpeningInst.SavedData["AdditionalNotesSortOrderVar" + str(self.Row)] = self.SortOrderVar
                SavingAndOpeningInst.SavedData["AdditionalNotesNoteVar" + str(self.Row)] = self.NoteVar

            class NoteConfig:
                def __init__(self, master, NameEntryVar, NoteVar):
                    self.DataSubmitted = BooleanVar()
                    self.NameEntryVar = StringVar(value=NameEntryVar.get())
                    self.NoteVar = StringVar(value=NoteVar.get())

                    # Create Window
                    self.Window = Toplevel(master)
                    self.Window.wm_attributes("-toolwindow", 1)
                    self.Window.wm_title("Note Entry")

                    # Name Entry
                    self.NameFrame = LabelFrame(self.Window, text="Name:")
                    self.NameFrame.grid_columnconfigure(0, weight=1)
                    self.NameFrame.grid(row=0, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                    self.NameEntry = Entry(self.NameFrame, justify=CENTER, width=20, textvariable=self.NameEntryVar)
                    self.NameEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                    # Description Field
                    self.DescriptionFrame = LabelFrame(self.Window, text="Note:")
                    self.DescriptionFrame.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                    self.NoteField = ScrolledText(self.DescriptionFrame, Height=300, Width=250)
                    self.NoteField.grid(row=0, column=0)
                    self.NoteField.Text.insert(1.0, self.NoteVar.get())

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

                def Submit(self):
                    self.DataSubmitted.set(True)
                    self.NoteVar.set(self.NoteField.get())
                    self.Window.destroy()

                def Cancel(self):
                    self.DataSubmitted.set(False)
                    self.Window.destroy()

    # Personality and Backstory
    class PersonalityAndBackstory:
        def __init__(self, master):
            self.RaceEntryVar = StringVar()
            self.BackgroundEntryVar = StringVar()
            self.AlignmentEntryVar = StringVar()
            self.AgeEntryVar = StringVar()

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
            self.RaceEntry = Entry(self.RaceFrame, justify=CENTER, textvariable=self.RaceEntryVar, width=22)
            self.RaceEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

            # Background
            self.BackgroundFrame = LabelFrame(self.FirstColumnFrame, text="Background:")
            self.BackgroundFrame.grid_columnconfigure(0, weight=1)
            self.BackgroundFrame.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)
            self.BackgroundEntry = Entry(self.BackgroundFrame, justify=CENTER, textvariable=self.BackgroundEntryVar, width=22)
            self.BackgroundEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

            # Alignment
            self.AlignmentFrame = LabelFrame(self.FirstColumnFrame, text="Alignment:")
            self.AlignmentFrame.grid_columnconfigure(0, weight=1)
            self.AlignmentFrame.grid(row=2, column=0, padx=2, pady=2, sticky=NSEW)
            self.AlignmentEntry = Entry(self.AlignmentFrame, justify=CENTER, textvariable=self.AlignmentEntryVar, width=22)
            self.AlignmentEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

            # Age
            self.AgeFrame = LabelFrame(self.FirstColumnFrame, text="Age:")
            self.AgeFrame.grid_columnconfigure(0, weight=1)
            self.AgeFrame.grid(row=3, column=0, padx=2, pady=2, sticky=NSEW)
            self.AgeEntry = Entry(self.AgeFrame, justify=CENTER, textvariable=self.AgeEntryVar, width=22)
            self.AgeEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

            # Physical Appearance
            self.PhysicalAppearanceFrame = LabelFrame(self.FirstColumnFrame, text="Physical Appearance:")
            self.PhysicalAppearanceFrame.grid(row=4, column=0, padx=2, pady=2)
            self.PhysicalAppearanceField = ScrolledText(self.PhysicalAppearanceFrame, Width=170, Height=289)
            self.PhysicalAppearanceField.grid(row=0, column=0)

            # Second Column
            self.SecondColumnFrame = Frame(master)
            self.SecondColumnFrame.grid(row=1, column=3)

            # Personality Traits
            self.PersonalityTraitsFrame = LabelFrame(self.SecondColumnFrame, text="Personality Traits:")
            self.PersonalityTraitsFrame.grid(row=0, column=0, padx=2, pady=2)
            self.PersonalityTraitsField = ScrolledText(self.PersonalityTraitsFrame, Width=170, Height=225)
            self.PersonalityTraitsField.grid(row=0, column=0)

            # Bonds
            self.BondsFrame = LabelFrame(self.SecondColumnFrame, text="Bonds:")
            self.BondsFrame.grid(row=1, column=0, padx=2, pady=2)
            self.BondsField = ScrolledText(self.BondsFrame, Width=170, Height=225)
            self.BondsField.grid(row=0, column=0)

            # Third Column
            self.ThirdColumnFrame = Frame(master)
            self.ThirdColumnFrame.grid(row=1, column=5)

            # Ideals
            self.IdealsFrame = LabelFrame(self.ThirdColumnFrame, text="Ideals:")
            self.IdealsFrame.grid(row=0, column=0, padx=2, pady=2)
            self.IdealsField = ScrolledText(self.IdealsFrame, Width=170, Height=225)
            self.IdealsField.grid(row=0, column=0)

            # Flaws
            self.FlawsFrame = LabelFrame(self.ThirdColumnFrame, text="Flaws:")
            self.FlawsFrame.grid(row=1, column=0, padx=2, pady=2)
            self.FlawsField = ScrolledText(self.FlawsFrame, Width=170, Height=225)
            self.FlawsField.grid(row=0, column=0)

            # Fourth Column
            self.FourthColumnFrame = Frame(master)
            self.FourthColumnFrame.grid(row=1, column=7)

            # Backstory
            self.BackstoryFrame = LabelFrame(self.FourthColumnFrame, text="Backstory:")
            self.BackstoryFrame.grid(row=0, column=0, padx=2, pady=2)
            self.BackstoryField = ScrolledText(self.BackstoryFrame, Width=170, Height=473)
            self.BackstoryField.grid(row=0, column=0)

            # Add Saved Fields to Saved Data Dictionary
            SavingAndOpeningInst.SavedData["RaceEntryVar"] = self.RaceEntryVar
            SavingAndOpeningInst.SavedData["BackgroundEntryVar"] = self.BackgroundEntryVar
            SavingAndOpeningInst.SavedData["AlignmentEntryVar"] = self.AlignmentEntryVar
            SavingAndOpeningInst.SavedData["AgeEntryVar"] = self.AgeEntryVar
            SavingAndOpeningInst.SavedData["PhysicalAppearanceField"] = self.PhysicalAppearanceField
            SavingAndOpeningInst.SavedData["PersonalityTraitsField"] = self.PersonalityTraitsField
            SavingAndOpeningInst.SavedData["BondsField"] = self.BondsField
            SavingAndOpeningInst.SavedData["IdealsField"] = self.IdealsField
            SavingAndOpeningInst.SavedData["FlawsField"] = self.FlawsField
            SavingAndOpeningInst.SavedData["BackstoryField"] = self.BackstoryField

    # Portrait
    class Portrait():
        def __init__(self, master):
            self.PortraitSelectedVar = BooleanVar()
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

            # Add Saved Field to Saved Data Dictionary
            SavingAndOpeningInst.SavedData["PortraitSelectedVar"] = self.PortraitSelectedVar

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
        def __init__(self, master, SpellcasterBoxVar, ConcentrationCheckPromptBoxVar, PortraitBoxVar, JackOfAllTradesBoxVar, RemarkableAthleteBoxVar, ObservantBoxVar, LuckyHalflingBoxVar):
            # Variables
            self.DataSubmitted = BooleanVar()
            self.SpellcasterBoxVar = BooleanVar(value=SpellcasterBoxVar.get())
            self.ConcentrationCheckPromptBoxVar = BooleanVar(value=ConcentrationCheckPromptBoxVar.get())
            self.PortraitBoxVar = BooleanVar(value=PortraitBoxVar.get())
            self.JackOfAllTradesBoxVar = BooleanVar(value=JackOfAllTradesBoxVar.get())
            self.RemarkableAthleteBoxVar = BooleanVar(value=RemarkableAthleteBoxVar.get())
            self.ObservantBoxVar = BooleanVar(value=ObservantBoxVar.get())
            self.LuckyHalflingBoxVar = BooleanVar(value=LuckyHalflingBoxVar.get())

            # Create Window
            self.Window = Toplevel(master)
            self.Window.wm_attributes("-toolwindow", 1)
            self.Window.wm_title("Settings")

            # Spellcaster Checkbox
            self.SpellcasterBox = Checkbutton(self.Window, text="Spellcaster", variable=self.SpellcasterBoxVar)
            self.SpellcasterBox.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)

            # Concentration Check Prompt Checkbox
            self.ConcentrationCheckPromptBox = Checkbutton(self.Window, text="Concentration Check Prompt", variable=self.ConcentrationCheckPromptBoxVar)
            self.ConcentrationCheckPromptBox.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)

            # Portrait Checkbox
            self.PortraitBox = Checkbutton(self.Window, text="Portrait", variable=self.PortraitBoxVar)
            self.PortraitBox.grid(row=2, column=0, padx=2, pady=2, sticky=NSEW)

            # Jack of All Trades Checkbox
            self.JackOfAllTradesBox = Checkbutton(self.Window, text="Jack of All Trades", variable=self.JackOfAllTradesBoxVar)
            self.JackOfAllTradesBox.grid(row=3, column=0, padx=2, pady=2, sticky=NSEW)

            # Remarkable Athlete Checkbox
            self.RemarkableAthleteBox = Checkbutton(self.Window, text="Remarkable Athlete", variable=self.RemarkableAthleteBoxVar)
            self.RemarkableAthleteBox.grid(row=4, column=0, padx=2, pady=2, sticky=NSEW)

            # Observant Checkbox
            self.ObservantBox = Checkbutton(self.Window, text="Observant", variable=self.ObservantBoxVar)
            self.ObservantBox.grid(row=5, column=0, padx=2, pady=2, sticky=NSEW)

            # Lucky (Halfling) Checkbox
            self.LuckyHalflingBox = Checkbutton(self.Window, text="Lucky (Halfling)", variable=self.LuckyHalflingBoxVar)
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
        self.SPEntryVar = StringVar()
        self.EPEntryVar = StringVar()
        self.GPEntryVar = StringVar()
        self.PPEntryVar = StringVar()
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
        self.CPEntry = Entry(self.TableFrame, textvariable=self.CPEntryVar, justify=CENTER, width=20)
        self.CPEntry.grid(row=1, column=1, sticky=NSEW)
        self.SPEntry = Entry(self.TableFrame, textvariable=self.SPEntryVar, justify=CENTER, width=20)
        self.SPEntry.grid(row=2, column=1, sticky=NSEW)
        self.EPEntry = Entry(self.TableFrame, textvariable=self.EPEntryVar, justify=CENTER, width=20)
        self.EPEntry.grid(row=3, column=1, sticky=NSEW)
        self.GPEntry = Entry(self.TableFrame, textvariable=self.GPEntryVar, justify=CENTER, width=20)
        self.GPEntry.grid(row=4, column=1, sticky=NSEW)
        self.PPEntry = Entry(self.TableFrame, textvariable=self.PPEntryVar, justify=CENTER, width=20)
        self.PPEntry.grid(row=5, column=1, sticky=NSEW)

        # Output Entries
        self.CPOutputEntry = Entry(self.TableFrame, textvariable=self.CPOutputEntryVar, justify=CENTER, width=20, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow")
        self.CPOutputEntry.grid(row=1, column=2, sticky=NSEW)
        self.SPOutputEntry = Entry(self.TableFrame, textvariable=self.SPOutputEntryVar, justify=CENTER, width=20, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow")
        self.SPOutputEntry.grid(row=2, column=2, sticky=NSEW)
        self.EPOutputEntry = Entry(self.TableFrame, textvariable=self.EPOutputEntryVar, justify=CENTER, width=20, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow")
        self.EPOutputEntry.grid(row=3, column=2, sticky=NSEW)
        self.GPOutputEntry = Entry(self.TableFrame, textvariable=self.GPOutputEntryVar, justify=CENTER, width=20, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow")
        self.GPOutputEntry.grid(row=4, column=2, sticky=NSEW)
        self.PPOutputEntry = Entry(self.TableFrame, textvariable=self.PPOutputEntryVar, justify=CENTER, width=20, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow")
        self.PPOutputEntry.grid(row=5, column=2, sticky=NSEW)
        self.WeightOutputEntry = Entry(self.TableFrame, textvariable=self.WeightOutputEntryVar, justify=CENTER, width=20, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow")
        self.WeightOutputEntry.grid(row=6, column=2, sticky=NSEW)

        # Buttons
        self.ButtonsFrame = Frame(self.WidgetMaster)
        self.ButtonsFrame.grid_columnconfigure(0, weight=1)
        self.ButtonsFrame.grid(row=1, column=0, sticky=NSEW)
        self.CalculateButton = Button(self.ButtonsFrame, text="Calculate", command=self.Calculate, bg=GlobalInst.ButtonColor)
        self.CalculateButton.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Additional Dialog Setup
        if DialogMode:
            self.ButtonsFrame.grid_columnconfigure(1, weight=1)
            self.CloseButton = Button(self.ButtonsFrame, text="Close", command=self.Close, bg=GlobalInst.ButtonColor)
            self.CloseButton.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)

            # Prevent Main Window Input
            self.Window.grab_set()

            # Handle Config Window Geometry and Focus
            GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst)
            self.Window.focus_force()

    def ValidEntry(self):
        try:
            CPInput = GlobalInst.GetStringVarAsNumber(self.CPEntryVar)
            SPInput = GlobalInst.GetStringVarAsNumber(self.SPEntryVar)
            EPInput = GlobalInst.GetStringVarAsNumber(self.EPEntryVar)
            GPInput = GlobalInst.GetStringVarAsNumber(self.GPEntryVar)
            PPInput = GlobalInst.GetStringVarAsNumber(self.PPEntryVar)
        except:
            messagebox.showerror("Invalid Entry", "Coins must be whole numbers.")
            return False
        if CPInput < 0 or SPInput < 0 or EPInput < 0 or GPInput < 0 or PPInput < 0:
            messagebox.showerror("Invalid Entry", "Coins cannot be negative.")
            return False
        return True

    def Calculate(self):
        # Check Inputs
        if self.ValidEntry():
            pass
        else:
            return

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


class StatModifier:
    def __init__(self, master, EventString, TooltipText, BonusTo, Cursor="arrow", ACMode=False):
        # Store Parameters
        self.EventString = EventString
        self.TooltipText = TooltipText
        self.BonusTo = BonusTo
        self.ACMode = ACMode

        # Variables
        self.Variables = {}
        self.Variables["StrengthMultiplierEntryVar"] = StringVar()
        self.Variables["DexterityMultiplierEntryVar"] = StringVar()
        self.Variables["ConstitutionMultiplierEntryVar"] = StringVar()
        self.Variables["IntelligenceMultiplierEntryVar"] = StringVar()
        self.Variables["WisdomMultiplierEntryVar"] = StringVar()
        self.Variables["CharismaMultiplierEntryVar"] = StringVar()
        self.Variables["ProficiencyMultiplierEntryVar"] = StringVar()
        self.Variables["ManualModifierEntryVar"] = StringVar()
        self.Variables["StrengthMinEntryVar"] = StringVar()
        self.Variables["DexterityMinEntryVar"] = StringVar()
        self.Variables["ConstitutionMinEntryVar"] = StringVar()
        self.Variables["IntelligenceMinEntryVar"] = StringVar()
        self.Variables["WisdomMinEntryVar"] = StringVar()
        self.Variables["CharismaMinEntryVar"] = StringVar()
        self.Variables["ProficiencyMinEntryVar"] = StringVar()
        self.Variables["StrengthMaxEntryVar"] = StringVar()
        self.Variables["DexterityMaxEntryVar"] = StringVar()
        self.Variables["ConstitutionMaxEntryVar"] = StringVar()
        self.Variables["IntelligenceMaxEntryVar"] = StringVar()
        self.Variables["WisdomMaxEntryVar"] = StringVar()
        self.Variables["CharismaMaxEntryVar"] = StringVar()
        self.Variables["ProficiencyMaxEntryVar"] = StringVar()
        self.Variables["StrengthMultiplierRoundUpBoxVar"] = BooleanVar()
        self.Variables["DexterityMultiplierRoundUpBoxVar"] = BooleanVar()
        self.Variables["ConstitutionMultiplierRoundUpBoxVar"] = BooleanVar()
        self.Variables["IntelligenceMultiplierRoundUpBoxVar"] = BooleanVar()
        self.Variables["WisdomMultiplierRoundUpBoxVar"] = BooleanVar()
        self.Variables["CharismaMultiplierRoundUpBoxVar"] = BooleanVar()
        self.Variables["ProficiencyMultiplierRoundUpBoxVar"] = BooleanVar()
        if self.ACMode:
            self.Variables["ACBaseEntryVar"] = StringVar()

        # Configure Master (Should Be Entry Widget)
        master.configure(state=DISABLED, disabledbackground=GlobalInst.ButtonColor, disabledforeground="black", cursor=Cursor)
        master.bind(self.EventString, lambda event: self.SetModifier(ACMode=self.ACMode))
        StatusBarInst.TooltipConfig(master, self.TooltipText)

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
        TotalModifier = StrengthMod + DexterityMod + ConstitutionMod + IntelligenceMod + WisdomMod + CharismaMod + ProficiencyMod + ManualMod + ACBase
        return TotalModifier

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

    def SetModifier(self, BonusToOverride=None, ACMode=False):
        # Test Stats Input Validity
        if WindowInst.Mode is "CharacterSheet":
            if CharacterSheetInst.ValidStatsEntry():
                pass
            else:
                return
        elif WindowInst.Mode is "NPCSheet":
            if CreatureDataInst.ValidStatsEntry():
                pass
            else:
                return

        # Determine Bonus To String
        if BonusToOverride is not None:
            BonusToString = BonusToOverride
        else:
            BonusToString = self.BonusTo

        # Create Config Window and Wait
        ModifierConfigInst = self.ModifierConfig(self.Variables, BonusToString, ACMode=ACMode)
        WindowInst.wait_window(ModifierConfigInst.Window)

        # Handle Values
        if ModifierConfigInst.DataSubmitted.get():
            for Tag, Var in ModifierConfigInst.Variables.items():
                self.Variables[Tag].set(Var.get())

        # Update Stats and Inventory
        if WindowInst.Mode is "CharacterSheet":
            CharacterSheetInst.UpdateStatsAndInventory()
        elif WindowInst.Mode is "NPCSheet":
            CreatureDataInst.UpdateStats()

    def AddToSavedData(self, Prefix="", Suffix=""):
        SavingAndOpeningInst.SavedData[Prefix + "StrengthMultiplierEntryVar" + Suffix] = self.Variables["StrengthMultiplierEntryVar"]
        SavingAndOpeningInst.SavedData[Prefix + "DexterityMultiplierEntryVar" + Suffix] = self.Variables["DexterityMultiplierEntryVar"]
        SavingAndOpeningInst.SavedData[Prefix + "ConstitutionMultiplierEntryVar" + Suffix] = self.Variables["ConstitutionMultiplierEntryVar"]
        SavingAndOpeningInst.SavedData[Prefix + "IntelligenceMultiplierEntryVar" + Suffix] = self.Variables["IntelligenceMultiplierEntryVar"]
        SavingAndOpeningInst.SavedData[Prefix + "WisdomMultiplierEntryVar" + Suffix] = self.Variables["WisdomMultiplierEntryVar"]
        SavingAndOpeningInst.SavedData[Prefix + "CharismaMultiplierEntryVar" + Suffix] = self.Variables["CharismaMultiplierEntryVar"]
        SavingAndOpeningInst.SavedData[Prefix + "ProficiencyMultiplierEntryVar" + Suffix] = self.Variables["ProficiencyMultiplierEntryVar"]
        SavingAndOpeningInst.SavedData[Prefix + "StrengthMinEntryVar" + Suffix] = self.Variables["StrengthMinEntryVar"]
        SavingAndOpeningInst.SavedData[Prefix + "DexterityMinEntryVar" + Suffix] = self.Variables["DexterityMinEntryVar"]
        SavingAndOpeningInst.SavedData[Prefix + "ConstitutionMinEntryVar" + Suffix] = self.Variables["ConstitutionMinEntryVar"]
        SavingAndOpeningInst.SavedData[Prefix + "IntelligenceMinEntryVar" + Suffix] = self.Variables["IntelligenceMinEntryVar"]
        SavingAndOpeningInst.SavedData[Prefix + "WisdomMinEntryVar" + Suffix] = self.Variables["WisdomMinEntryVar"]
        SavingAndOpeningInst.SavedData[Prefix + "CharismaMinEntryVar" + Suffix] = self.Variables["CharismaMinEntryVar"]
        SavingAndOpeningInst.SavedData[Prefix + "ProficiencyMinEntryVar" + Suffix] = self.Variables["ProficiencyMinEntryVar"]
        SavingAndOpeningInst.SavedData[Prefix + "StrengthMaxEntryVar" + Suffix] = self.Variables["StrengthMaxEntryVar"]
        SavingAndOpeningInst.SavedData[Prefix + "DexterityMaxEntryVar" + Suffix] = self.Variables["DexterityMaxEntryVar"]
        SavingAndOpeningInst.SavedData[Prefix + "ConstitutionMaxEntryVar" + Suffix] = self.Variables["ConstitutionMaxEntryVar"]
        SavingAndOpeningInst.SavedData[Prefix + "IntelligenceMaxEntryVar" + Suffix] = self.Variables["IntelligenceMaxEntryVar"]
        SavingAndOpeningInst.SavedData[Prefix + "WisdomMaxEntryVar" + Suffix] = self.Variables["WisdomMaxEntryVar"]
        SavingAndOpeningInst.SavedData[Prefix + "CharismaMaxEntryVar" + Suffix] = self.Variables["CharismaMaxEntryVar"]
        SavingAndOpeningInst.SavedData[Prefix + "ProficiencyMaxEntryVar" + Suffix] = self.Variables["ProficiencyMaxEntryVar"]
        SavingAndOpeningInst.SavedData[Prefix + "ManualModifierEntryVar" + Suffix] = self.Variables["ManualModifierEntryVar"]
        SavingAndOpeningInst.SavedData[Prefix + "StrengthMultiplierRoundUpBoxVar" + Suffix] = self.Variables["StrengthMultiplierRoundUpBoxVar"]
        SavingAndOpeningInst.SavedData[Prefix + "DexterityMultiplierRoundUpBoxVar" + Suffix] = self.Variables["DexterityMultiplierRoundUpBoxVar"]
        SavingAndOpeningInst.SavedData[Prefix + "ConstitutionMultiplierRoundUpBoxVar" + Suffix] = self.Variables["ConstitutionMultiplierRoundUpBoxVar"]
        SavingAndOpeningInst.SavedData[Prefix + "IntelligenceMultiplierRoundUpBoxVar" + Suffix] = self.Variables["IntelligenceMultiplierRoundUpBoxVar"]
        SavingAndOpeningInst.SavedData[Prefix + "WisdomMultiplierRoundUpBoxVar" + Suffix] = self.Variables["WisdomMultiplierRoundUpBoxVar"]
        SavingAndOpeningInst.SavedData[Prefix + "CharismaMultiplierRoundUpBoxVar" + Suffix] = self.Variables["CharismaMultiplierRoundUpBoxVar"]
        SavingAndOpeningInst.SavedData[Prefix + "ProficiencyMultiplierRoundUpBoxVar" + Suffix] = self.Variables["ProficiencyMultiplierRoundUpBoxVar"]
        if self.ACMode:
            SavingAndOpeningInst.SavedData[Prefix + "ACBaseEntryVar" + Suffix] = self.Variables["ACBaseEntryVar"]

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

    class ModifierConfig:
        def __init__(self, CurrentVariables, BonusTo, ACMode=False):
            # Store Parameters
            self.BonusTo = BonusTo
            self.ACMode = ACMode

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
                self.ACBaseEntry = Entry(self.ACBaseFrame, justify=CENTER, width=5, textvariable=self.Variables["ACBaseEntryVar"])
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

            # Multiplier Entries
            self.StrengthMultiplierEntry = Entry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["StrengthMultiplierEntryVar"])
            self.StrengthMultiplierEntry.grid(row=2, column=1, sticky=NSEW, padx=2, pady=2)
            self.DexterityMultiplierEntry = Entry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["DexterityMultiplierEntryVar"])
            self.DexterityMultiplierEntry.grid(row=3, column=1, sticky=NSEW, padx=2, pady=2)
            self.ConstitutionMultiplierEntry = Entry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["ConstitutionMultiplierEntryVar"])
            self.ConstitutionMultiplierEntry.grid(row=4, column=1, sticky=NSEW, padx=2, pady=2)
            self.IntelligenceMultiplierEntry = Entry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["IntelligenceMultiplierEntryVar"])
            self.IntelligenceMultiplierEntry.grid(row=5, column=1, sticky=NSEW, padx=2, pady=2)
            self.WisdomMultiplierEntry = Entry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["WisdomMultiplierEntryVar"])
            self.WisdomMultiplierEntry.grid(row=6, column=1, sticky=NSEW, padx=2, pady=2)
            self.CharismaMultiplierEntry = Entry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["CharismaMultiplierEntryVar"])
            self.CharismaMultiplierEntry.grid(row=7, column=1, sticky=NSEW, padx=2, pady=2)
            self.ProficiencyMultiplierEntry = Entry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["ProficiencyMultiplierEntryVar"])
            self.ProficiencyMultiplierEntry.grid(row=8, column=1, sticky=NSEW, padx=2, pady=2)

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

            # Min Entries
            self.StrengthMinEntry = Entry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["StrengthMinEntryVar"])
            self.StrengthMinEntry.grid(row=2, column=3, sticky=NSEW, padx=2, pady=2)
            self.DexterityMinEntry = Entry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["DexterityMinEntryVar"])
            self.DexterityMinEntry.grid(row=3, column=3, sticky=NSEW, padx=2, pady=2)
            self.ConstitutionMinEntry = Entry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["ConstitutionMinEntryVar"])
            self.ConstitutionMinEntry.grid(row=4, column=3, sticky=NSEW, padx=2, pady=2)
            self.IntelligenceMinEntry = Entry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["IntelligenceMinEntryVar"])
            self.IntelligenceMinEntry.grid(row=5, column=3, sticky=NSEW, padx=2, pady=2)
            self.WisdomMinEntry = Entry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["WisdomMinEntryVar"])
            self.WisdomMinEntry.grid(row=6, column=3, sticky=NSEW, padx=2, pady=2)
            self.CharismaMinEntry = Entry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["CharismaMinEntryVar"])
            self.CharismaMinEntry.grid(row=7, column=3, sticky=NSEW, padx=2, pady=2)
            self.ProficiencyMinEntry = Entry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["ProficiencyMinEntryVar"])
            self.ProficiencyMinEntry.grid(row=8, column=3, sticky=NSEW, padx=2, pady=2)

            # Max Entries
            self.StrengthMaxEntry = Entry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["StrengthMaxEntryVar"])
            self.StrengthMaxEntry.grid(row=2, column=4, sticky=NSEW, padx=2, pady=2)
            self.DexterityMaxEntry = Entry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["DexterityMaxEntryVar"])
            self.DexterityMaxEntry.grid(row=3, column=4, sticky=NSEW, padx=2, pady=2)
            self.ConstitutionMaxEntry = Entry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["ConstitutionMaxEntryVar"])
            self.ConstitutionMaxEntry.grid(row=4, column=4, sticky=NSEW, padx=2, pady=2)
            self.IntelligenceMaxEntry = Entry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["IntelligenceMaxEntryVar"])
            self.IntelligenceMaxEntry.grid(row=5, column=4, sticky=NSEW, padx=2, pady=2)
            self.WisdomMaxEntry = Entry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["WisdomMaxEntryVar"])
            self.WisdomMaxEntry.grid(row=6, column=4, sticky=NSEW, padx=2, pady=2)
            self.CharismaMaxEntry = Entry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["CharismaMaxEntryVar"])
            self.CharismaMaxEntry.grid(row=7, column=4, sticky=NSEW, padx=2, pady=2)
            self.ProficiencyMaxEntry = Entry(self.TableFrame, justify=CENTER, width=5, textvariable=self.Variables["ProficiencyMaxEntryVar"])
            self.ProficiencyMaxEntry.grid(row=8, column=4, sticky=NSEW, padx=2, pady=2)

            # Manual Modifier
            self.ManualModifierFrame = LabelFrame(self.TableFrame, text="Manual Modifier:")
            self.ManualModifierFrame.grid_columnconfigure(0, weight=1)
            self.ManualModifierFrame.grid(row=9, column=0, columnspan=5, sticky=NSEW, padx=2, pady=2)
            self.ManualModifierEntry = Entry(self.ManualModifierFrame, justify=CENTER, width=5, textvariable=self.Variables["ManualModifierEntryVar"])
            self.ManualModifierEntry.grid(row=0, column=0, sticky=NSEW)

            # Buttons
            self.ButtonsFrame = Frame(self.Window)
            self.ButtonsFrame.grid_columnconfigure(0, weight=1)
            self.ButtonsFrame.grid_columnconfigure(1, weight=1)
            self.ButtonsFrame.grid(row=1, column=0, sticky=NSEW)
            self.SubmitButton = Button(self.ButtonsFrame, text="Submit", bg=GlobalInst.ButtonColor, command=self.Submit)
            self.SubmitButton.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
            self.CancelButton = Button(self.ButtonsFrame, text="Cancel", bg=GlobalInst.ButtonColor, command=self.Cancel)
            self.CancelButton.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)

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
            if self.ValidEntry():
                pass
            else:
                return
            self.DataSubmitted.set(True)
            self.Window.destroy()

        def Cancel(self):
            self.DataSubmitted.set(False)
            self.Window.destroy()

        def ValidEntry(self):
            try:
                GlobalInst.GetStringVarAsNumber(self.Variables["StrengthMultiplierEntryVar"], Mode="Float")
                GlobalInst.GetStringVarAsNumber(self.Variables["DexterityMultiplierEntryVar"], Mode="Float")
                GlobalInst.GetStringVarAsNumber(self.Variables["ConstitutionMultiplierEntryVar"], Mode="Float")
                GlobalInst.GetStringVarAsNumber(self.Variables["IntelligenceMultiplierEntryVar"], Mode="Float")
                GlobalInst.GetStringVarAsNumber(self.Variables["WisdomMultiplierEntryVar"], Mode="Float")
                GlobalInst.GetStringVarAsNumber(self.Variables["CharismaMultiplierEntryVar"], Mode="Float")
                GlobalInst.GetStringVarAsNumber(self.Variables["ProficiencyMultiplierEntryVar"], Mode="Float")
            except:
                messagebox.showerror("Invalid Entry", "Multipliers must be numbers.")
                return False
            try:
                GlobalInst.GetStringVarAsNumber(self.Variables["StrengthMinEntryVar"])
                GlobalInst.GetStringVarAsNumber(self.Variables["DexterityMinEntryVar"])
                GlobalInst.GetStringVarAsNumber(self.Variables["ConstitutionMinEntryVar"])
                GlobalInst.GetStringVarAsNumber(self.Variables["IntelligenceMinEntryVar"])
                GlobalInst.GetStringVarAsNumber(self.Variables["WisdomMinEntryVar"])
                GlobalInst.GetStringVarAsNumber(self.Variables["CharismaMinEntryVar"])
                GlobalInst.GetStringVarAsNumber(self.Variables["ProficiencyMinEntryVar"])
                GlobalInst.GetStringVarAsNumber(self.Variables["StrengthMaxEntryVar"])
                GlobalInst.GetStringVarAsNumber(self.Variables["DexterityMaxEntryVar"])
                GlobalInst.GetStringVarAsNumber(self.Variables["ConstitutionMaxEntryVar"])
                GlobalInst.GetStringVarAsNumber(self.Variables["IntelligenceMaxEntryVar"])
                GlobalInst.GetStringVarAsNumber(self.Variables["WisdomMaxEntryVar"])
                GlobalInst.GetStringVarAsNumber(self.Variables["CharismaMaxEntryVar"])
                GlobalInst.GetStringVarAsNumber(self.Variables["ProficiencyMaxEntryVar"])
            except:
                messagebox.showerror("Invalid Entry", "Minimums and maximums must be whole numbers.")
                return False
            try:
                GlobalInst.GetStringVarAsNumber(self.Variables["ManualModifierEntryVar"])
            except:
                messagebox.showerror("Invalid Entry", "Manual modifier must be a whole number.")
                return False
            if self.ACMode:
                try:
                    GlobalInst.GetStringVarAsNumber(self.Variables["ACBaseEntryVar"])
                except:
                    messagebox.showerror("Invalid Entry", "Base AC must be a whole number.")
                    return False
            return True


class AbilityScoreDerivatives:
    def __init__(self, master, List, SaveTagPrefix, Column, AttackTypeStringSuffix=""):
        # Store Parameters
        self.SaveTagPrefix = SaveTagPrefix
        self.Column = Column
        self.AttackTypeStringSuffix = AttackTypeStringSuffix

        # Variables
        self.AbilityScoreSelectionDropdownVar = StringVar()
        self.SaveDCEntryVar = StringVar()
        self.AttackModifierEntryVar = StringVar()

        # Add to List
        List.append(self)

        # Ability Score Selection
        self.AbilityScoreSelectionDropdown = ttk.Combobox(master, textvariable=self.AbilityScoreSelectionDropdownVar, values=("", "STR", "DEX", "CON", "INT", "WIS", "CHA"), width=5, state="readonly", justify=CENTER)
        self.AbilityScoreSelectionDropdown.grid(row=0, column=self.Column, padx=2, pady=2, sticky=NSEW)

        # Save DC
        self.SaveDCEntry = Entry(master, justify=CENTER, width=2, textvariable=self.SaveDCEntryVar, cursor="arrow")
        self.SaveDCEntry.grid(row=1, column=self.Column, padx=2, pady=2, sticky=NSEW)
        self.SaveDCEntryStatModifierInst = StatModifier(self.SaveDCEntry, "<Button-1>", "Left-click on a save DC to set a stat modifier.", "Save DC")

        # Attack Modifier
        self.AttackModifierEntry = Entry(master, justify=CENTER, width=2, textvariable=self.AttackModifierEntryVar, cursor="dotbox")
        self.AttackModifierEntry.grid(row=2, column=self.Column, padx=2, pady=2, sticky=NSEW)
        self.AttackModifierEntryStatModifierInst = StatModifier(self.AttackModifierEntry, "<Button-3>", "Left-click on an attack modifier to roll 1d20 with it.  Right-click to set a stat modifier.", "Attack Modifier",
                                                                Cursor="dotbox")
        self.AttackModifierEntry.bind("<Button-1>", self.RollAttack)

        # Add Saved Fields to Saved Data Dictionary
        SavingAndOpeningInst.SavedData[self.SaveTagPrefix + "AbilitySelectionDropdownVar" + str(self.Column)] = self.AbilityScoreSelectionDropdownVar
        self.SaveDCEntryStatModifierInst.AddToSavedData(Prefix=self.SaveTagPrefix + "SaveDC", Suffix=str(self.Column))
        self.AttackModifierEntryStatModifierInst.AddToSavedData(Prefix=self.SaveTagPrefix + "AttackModifier", Suffix=str(self.Column))

    def RollAttack(self, event):
        try:
            DiceRollerInst.ModifierEntryVar.set(str(GlobalInst.GetStringVarAsNumber(self.AttackModifierEntryVar)))
        except ValueError:
            return
        DiceRollerInst.DiceNumberEntryVar.set(1)
        DiceRollerInst.DieTypeEntryVar.set(20)
        AttackTypeString = self.AbilityScoreSelectionDropdownVar.get()
        if self.AttackTypeStringSuffix is not "":
            AttackTypeString += " " + self.AttackTypeStringSuffix
        DiceRollerInst.Roll(AttackTypeString + " Attack:\n")


class CreatureData:
    def __init__(self, master, DialogMode=False, DialogData=None):
        # Standalone and NPC Sheet Mode Variables
        if not DialogMode:
            self.NameEntryVar = StringVar()
            self.SizeEntryVar = StringVar()
            self.TypeAndTagsEntryVar = StringVar()
            self.AlignmentEntryVar = StringVar()
            self.ProficiencyEntryVar = StringVar()
            self.TempHPEntryVar = StringVar()
            self.CurrentHPEntryVar = StringVar()
            self.MaxHPEntryVar = StringVar()
            self.ACEntryVar = StringVar()
            self.SpeedEntryVar = StringVar()
            self.CRAndExperienceEntryVar = StringVar()
            self.AbilitiesStrengthEntryVar = StringVar()
            self.AbilitiesDexterityEntryVar = StringVar()
            self.AbilitiesConstitutionEntryVar = StringVar()
            self.AbilitiesIntelligenceEntryVar = StringVar()
            self.AbilitiesWisdomEntryVar = StringVar()
            self.AbilitiesCharismaEntryVar = StringVar()
            if WindowInst.Mode is "NPCSheet":
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
            if WindowInst.Mode is "NPCSheet":
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
        self.NameEntry = Entry(self.NameFrame, justify=CENTER, textvariable=self.NameEntryVar)
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
        self.SizeEntry = Entry(self.SizeFrame, justify=CENTER, textvariable=self.SizeEntryVar)
        self.SizeEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Type and Tags
        self.TypeAndTagsFrame = LabelFrame(self.SizeTypeTagsAlignmentAndProficiencyFrame, text="Type and Tags:")
        self.TypeAndTagsFrame.grid_columnconfigure(0, weight=1)
        self.TypeAndTagsFrame.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
        self.TypeAndTagsEntry = Entry(self.TypeAndTagsFrame, justify=CENTER, textvariable=self.TypeAndTagsEntryVar)
        self.TypeAndTagsEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Alignment
        self.AlignmentFrame = LabelFrame(self.SizeTypeTagsAlignmentAndProficiencyFrame, text="Alignment:")
        self.AlignmentFrame.grid_columnconfigure(0, weight=1)
        self.AlignmentFrame.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
        self.AlignmentEntry = Entry(self.AlignmentFrame, justify=CENTER, textvariable=self.AlignmentEntryVar)
        self.AlignmentEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Proficiency
        self.ProficiencyFrame = LabelFrame(self.SizeTypeTagsAlignmentAndProficiencyFrame, text="Proficiency Bonus:")
        self.ProficiencyFrame.grid_columnconfigure(0, weight=1)
        self.ProficiencyFrame.grid(row=0, column=3, sticky=NSEW, padx=2, pady=2)
        self.ProficiencyEntry = Entry(self.ProficiencyFrame, justify=CENTER, width=5, textvariable=self.ProficiencyEntryVar)
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
        self.TempHPEntry = Entry(self.TempHPFrame, justify=CENTER, width=3, textvariable=self.TempHPEntryVar)
        self.TempHPEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Current HP Entry
        self.CurrentHPFrame = LabelFrame(self.HPACSpeedCRExperienceEntriesFrame, text="Current HP:")
        self.CurrentHPFrame.grid_columnconfigure(0, weight=1)
        self.CurrentHPFrame.grid(row=3, column=0, padx=2, pady=2, sticky=NSEW)
        self.CurrentHPEntry = Entry(self.CurrentHPFrame, justify=CENTER, width=3, textvariable=self.CurrentHPEntryVar)
        self.CurrentHPEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
        if WindowInst.Mode is "NPCSheet":
            self.CurrentHPEntry.configure(bg=GlobalInst.ButtonColor)
            self.CurrentHPEntry.bind("<Button-3>", lambda event: self.Damage())
            self.CurrentHPEntry.bind("<Shift-Button-3>", lambda event: self.Heal())
            StatusBarInst.TooltipConfig(self.CurrentHPEntry, "Right-click to damage.  Shift+right-click to heal.")

        # Max HP Entry
        self.MaxHPFrame = LabelFrame(self.HPACSpeedCRExperienceEntriesFrame, text="Max HP:")
        self.MaxHPFrame.grid_columnconfigure(0, weight=1)
        self.MaxHPFrame.grid(row=5, column=0, padx=2, pady=2, sticky=NSEW)
        self.MaxHPEntry = Entry(self.MaxHPFrame, justify=CENTER, width=3, textvariable=self.MaxHPEntryVar)
        self.MaxHPEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # AC Entry
        self.ACFrame = LabelFrame(self.HPACSpeedCRExperienceEntriesFrame, text="AC:")
        self.ACFrame.grid_columnconfigure(0, weight=1)
        self.ACFrame.grid(row=7, column=0, padx=2, pady=2, sticky=NSEW)
        self.ACEntry = Entry(self.ACFrame, justify=CENTER, width=3, textvariable=self.ACEntryVar)
        self.ACEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Speed
        self.SpeedFrame = LabelFrame(self.HPACSpeedCRExperienceEntriesFrame, text="Speed:")
        self.SpeedFrame.grid_columnconfigure(0, weight=1)
        self.SpeedFrame.grid(row=9, column=0, padx=2, pady=2, sticky=NSEW)
        self.SpeedEntry = Entry(self.SpeedFrame, justify=CENTER, width=3, textvariable=self.SpeedEntryVar)
        self.SpeedEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # CR and Experience
        self.CRAndExperienceFrame = LabelFrame(self.HPACSpeedCRExperienceEntriesFrame, text="CR and Exp.:")
        self.CRAndExperienceFrame.grid_columnconfigure(0, weight=1)
        self.CRAndExperienceFrame.grid(row=11, column=0, padx=2, pady=2, sticky=NSEW)
        self.CRAndExperienceEntry = Entry(self.CRAndExperienceFrame, justify=CENTER, width=3, textvariable=self.CRAndExperienceEntryVar)
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
        self.AbilitiesStrengthEntry = Entry(self.AbilitiesFrame, justify=CENTER, width=5, textvariable=self.AbilitiesStrengthEntryVar)
        self.AbilitiesStrengthEntry.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesDexterityHeader = Label(self.AbilitiesFrame, text="DEX", bd=2, relief=GROOVE)
        self.AbilitiesDexterityHeader.grid(row=0, column=1, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesDexterityEntry = Entry(self.AbilitiesFrame, justify=CENTER, width=5, textvariable=self.AbilitiesDexterityEntryVar)
        self.AbilitiesDexterityEntry.grid(row=1, column=1, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesConstitutionHeader = Label(self.AbilitiesFrame, text="CON", bd=2, relief=GROOVE)
        self.AbilitiesConstitutionHeader.grid(row=0, column=2, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesConstitutionEntry = Entry(self.AbilitiesFrame, justify=CENTER, width=5, textvariable=self.AbilitiesConstitutionEntryVar)
        self.AbilitiesConstitutionEntry.grid(row=1, column=2, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesIntelligenceHeader = Label(self.AbilitiesFrame, text="INT", bd=2, relief=GROOVE)
        self.AbilitiesIntelligenceHeader.grid(row=2, column=0, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesIntelligenceEntry = Entry(self.AbilitiesFrame, justify=CENTER, width=5, textvariable=self.AbilitiesIntelligenceEntryVar)
        self.AbilitiesIntelligenceEntry.grid(row=3, column=0, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesWisdomHeader = Label(self.AbilitiesFrame, text="WIS", bd=2, relief=GROOVE)
        self.AbilitiesWisdomHeader.grid(row=2, column=1, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesWisdomEntry = Entry(self.AbilitiesFrame, justify=CENTER, width=5, textvariable=self.AbilitiesWisdomEntryVar)
        self.AbilitiesWisdomEntry.grid(row=3, column=1, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesCharismaHeader = Label(self.AbilitiesFrame, text="CHA", bd=2, relief=GROOVE)
        self.AbilitiesCharismaHeader.grid(row=2, column=2, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesCharismaEntry = Entry(self.AbilitiesFrame, justify=CENTER, width=5, textvariable=self.AbilitiesCharismaEntryVar)
        self.AbilitiesCharismaEntry.grid(row=3, column=2, padx=2, pady=2, sticky=NSEW)

        # NPC Sheet Mouse Wheel Configuration
        if WindowInst.Mode is "NPCSheet":
            for EntryWidget in [self.AbilitiesStrengthEntry, self.AbilitiesDexterityEntry, self.AbilitiesConstitutionEntry, self.AbilitiesIntelligenceEntry, self.AbilitiesWisdomEntry, self.AbilitiesCharismaEntry,
                                self.ProficiencyEntry]:
                EntryWidget.configure(bg=GlobalInst.ButtonColor)
                StatusBarInst.TooltipConfig(EntryWidget, "Scroll the mouse wheel or type to change the modifier.")

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

        # Skills, Senses, and Languages
        self.SkillSensesAndLanguagesFrame = LabelFrame(self.WidgetMaster, text="Skills, Senses, and Languages:")
        self.SkillSensesAndLanguagesFrame.grid(row=3, column=1, padx=2, pady=2, sticky=NSEW)
        self.SkillSensesAndLanguagesField = ScrolledText(self.SkillSensesAndLanguagesFrame, Width=300, Height=120)
        self.SkillSensesAndLanguagesField.grid(row=0, column=0)

        # Special Traits
        self.SpecialTraitsFrame = LabelFrame(self.WidgetMaster, text="Special Traits:")
        self.SpecialTraitsFrame.grid(row=2, column=2, padx=2, pady=2, sticky=NSEW)
        self.SpecialTraitsField = ScrolledText(self.SpecialTraitsFrame, Width=383, Height=120)
        self.SpecialTraitsField.grid(row=0, column=0)

        # Actions
        self.ActionsFrame = LabelFrame(self.WidgetMaster, text="Actions:")
        self.ActionsFrame.grid(row=3, column=2, padx=2, pady=2, sticky=NSEW)
        self.ActionsField = ScrolledText(self.ActionsFrame, Width=383, Height=120)
        self.ActionsField.grid(row=0, column=0)

        # Saving Throws
        self.SavingThrowsFrame = LabelFrame(self.WidgetMaster, text="Saving Throws:")
        self.SavingThrowsFrame.grid(row=4, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
        self.SavingThrowsField = ScrolledText(self.SavingThrowsFrame, Width=383, Height=75)
        self.SavingThrowsField.grid(row=0, column=0)

        # Vulnerabilities, Resistances, and Immunities
        self.VulnerabilitiesResistancesAndImmunitiesFrame = LabelFrame(self.WidgetMaster, text="Vulnerabilities, Resistances, and Immunities:")
        self.VulnerabilitiesResistancesAndImmunitiesFrame.grid(row=5, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
        self.VulnerabilitiesResistancesAndImmunitiesField = ScrolledText(self.VulnerabilitiesResistancesAndImmunitiesFrame, Width=383, Height=75)
        self.VulnerabilitiesResistancesAndImmunitiesField.grid(row=0, column=0)

        # Inventory
        self.InventoryFrame = LabelFrame(self.WidgetMaster, text="Inventory:")
        self.InventoryFrame.grid(row=6, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
        self.InventoryField = ScrolledText(self.InventoryFrame, Width=383, Height=75)
        self.InventoryField.grid(row=0, column=0)

        # Reactions
        self.ReactionsFrame = LabelFrame(self.WidgetMaster, text="Reactions:")
        self.ReactionsFrame.grid(row=4, column=2, padx=2, pady=2, sticky=NSEW)
        self.ReactionsField = ScrolledText(self.ReactionsFrame, Width=383, Height=75)
        self.ReactionsField.grid(row=0, column=0)

        # Legendary Actions and Lair Actions
        self.LegendaryActionsAndLairActionsFrame = LabelFrame(self.WidgetMaster, text="Legendary Actions and Lair Actions:")
        self.LegendaryActionsAndLairActionsFrame.grid(row=5, column=2, padx=2, pady=2, sticky=NSEW)
        self.LegendaryActionsAndLairActionsField = ScrolledText(self.LegendaryActionsAndLairActionsFrame, Width=383, Height=75)
        self.LegendaryActionsAndLairActionsField.grid(row=0, column=0)

        # Notes
        self.NotesFrame = LabelFrame(self.WidgetMaster, text="Notes:")
        self.NotesFrame.grid(row=6, column=2, padx=2, pady=2, sticky=NSEW)
        self.NotesField = ScrolledText(self.NotesFrame, Width=383, Height=75)
        self.NotesField.grid(row=0, column=0)

        # Create Creature Stats Fields Dictionary
        if DialogMode or WindowInst.Mode is "NPCSheet":
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

        # Add Saved Fields to Saved Data Dictionary in Standalone Mode
        if not DialogMode:
            SavingAndOpeningInst.SavedData["NameEntryVar"] = self.NameEntryVar
            SavingAndOpeningInst.SavedData["ACEntryVar"] = self.ACEntryVar
            SavingAndOpeningInst.SavedData["TempHPEntryVar"] = self.TempHPEntryVar
            SavingAndOpeningInst.SavedData["CurrentHPEntryVar"] = self.CurrentHPEntryVar
            SavingAndOpeningInst.SavedData["MaxHPEntryVar"] = self.MaxHPEntryVar
            SavingAndOpeningInst.SavedData["SizeEntryVar"] = self.SizeEntryVar
            SavingAndOpeningInst.SavedData["TypeAndTagsEntryVar"] = self.TypeAndTagsEntryVar
            SavingAndOpeningInst.SavedData["AlignmentEntryVar"] = self.AlignmentEntryVar
            SavingAndOpeningInst.SavedData["ProficiencyEntryVar"] = self.ProficiencyEntryVar
            SavingAndOpeningInst.SavedData["SpeedEntryVar"] = self.SpeedEntryVar
            SavingAndOpeningInst.SavedData["CRAndExperienceEntryVar"] = self.CRAndExperienceEntryVar
            SavingAndOpeningInst.SavedData["AbilitiesStrengthEntryVar"] = self.AbilitiesStrengthEntryVar
            SavingAndOpeningInst.SavedData["AbilitiesDexterityEntryVar"] = self.AbilitiesDexterityEntryVar
            SavingAndOpeningInst.SavedData["AbilitiesConstitutionEntryVar"] = self.AbilitiesConstitutionEntryVar
            SavingAndOpeningInst.SavedData["AbilitiesIntelligenceEntryVar"] = self.AbilitiesIntelligenceEntryVar
            SavingAndOpeningInst.SavedData["AbilitiesWisdomEntryVar"] = self.AbilitiesWisdomEntryVar
            SavingAndOpeningInst.SavedData["AbilitiesCharismaEntryVar"] = self.AbilitiesCharismaEntryVar
            SavingAndOpeningInst.SavedData["SkillSensesAndLanguagesFieldVar"] = self.SkillSensesAndLanguagesField
            SavingAndOpeningInst.SavedData["SavingThrowsFieldVar"] = self.SavingThrowsField
            SavingAndOpeningInst.SavedData["VulnerabilitiesResistancesAndImmunitiesFieldVar"] = self.VulnerabilitiesResistancesAndImmunitiesField
            SavingAndOpeningInst.SavedData["SpecialTraitsFieldVar"] = self.SpecialTraitsField
            SavingAndOpeningInst.SavedData["ActionsFieldVar"] = self.ActionsField
            SavingAndOpeningInst.SavedData["ReactionsFieldVar"] = self.ReactionsField
            SavingAndOpeningInst.SavedData["InventoryFieldVar"] = self.InventoryField
            SavingAndOpeningInst.SavedData["LegendaryActionsAndLairActionsFieldVar"] = self.LegendaryActionsAndLairActionsField
            SavingAndOpeningInst.SavedData["NotesFieldVar"] = self.NotesField

    def Damage(self):
        if self.ValidLifeValues():
            pass
        else:
            return
        CurrentTempHP = GlobalInst.GetStringVarAsNumber(self.TempHPEntryVar)
        if self.CurrentHPEntryVar.get() == "":
            CurrentHP = GlobalInst.GetStringVarAsNumber(self.MaxHPEntryVar)
        else:
            CurrentHP = GlobalInst.GetStringVarAsNumber(self.CurrentHPEntryVar)
        DamagePrompt = IntegerPrompt(WindowInst, "Damage", "How much damage?", MinValue=1)
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
        HealingPrompt = IntegerPrompt(WindowInst, "Heal", "How much healing?", MinValue=1)
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

    def ValidStatsEntry(self):
        try:
            GlobalInst.GetStringVarAsNumber(self.ProficiencyEntryVar)
        except:
            messagebox.showerror("Invalid Entry", "Proficiency must be a whole number.")
            return False
        try:
            GlobalInst.GetStringVarAsNumber(self.AbilitiesStrengthEntryVar)
            GlobalInst.GetStringVarAsNumber(self.AbilitiesDexterityEntryVar)
            GlobalInst.GetStringVarAsNumber(self.AbilitiesConstitutionEntryVar)
            GlobalInst.GetStringVarAsNumber(self.AbilitiesIntelligenceEntryVar)
            GlobalInst.GetStringVarAsNumber(self.AbilitiesWisdomEntryVar)
            GlobalInst.GetStringVarAsNumber(self.AbilitiesCharismaEntryVar)
        except:
            messagebox.showerror("Invalid Entry", "Ability modifiers must be whole numbers.")
            return False
        return True

    def UpdateStats(self):
        # Test Stats Input Validity
        if self.ValidStatsEntry():
            pass
        else:
            return

        # Calculate Preset Roll Modifiers
        for Entry in Inst["PresetRolls"].PresetRollsList:
            Entry.PresetRollModifierEntryVar.set(Entry.PresetRollModifierEntryStatModifierInst.GetModifier())

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
        if WindowInst.Mode is "DiceRoller":
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
        elif WindowInst.Mode is "EncounterManager":
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
        elif WindowInst.Mode is "CharacterSheet":
            self.Row = 0
            self.Column = 1
            self.RowSpan = 1
            self.DiceEntryAndButtonsFrameColumnSpan = 1
            self.ResultsFieldFrameColumn = 0
            self.ResultsFieldWidth = 436
            self.ResultsFieldHeight = 148
            self.PresetRollsFrameRow = 3
            self.PresetRollsScrolledCanvasHeight = 284
            self.PresetRollsScrolledCanvasWidth = 423
        elif WindowInst.Mode is "NPCSheet":
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
        self.CritMinimumEntryVar = StringVar(value="20")
        if WindowInst.Mode is "CharacterSheet":
            self.InspirationBoxVar = BooleanVar()
            self.InspirationTrueColor = "#7aff63"
            self.InspirationFalseColor = GlobalInst.ButtonColor

        # Dice Roller Frame
        if WindowInst.Mode is "DiceRoller":
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
        self.DiceNumberEntry = Entry(self.DiceEntryAndButtonsFrame, textvariable=self.DiceNumberEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor, font=self.DiceEntryFont)
        self.DiceNumberEntry.grid(row=0, column=0, rowspan=2, padx=2, pady=2, sticky=NSEW)
        StatusBarInst.TooltipConfig(self.DiceNumberEntry, "Scroll the mouse wheel or type to change the number of dice.")

        # Die Type
        self.DieTypeLabel = Label(self.DiceEntryAndButtonsFrame, text="d", font=self.DiceEntryFont)
        self.DieTypeLabel.grid(row=0, column=1, rowspan=2, sticky=NSEW)
        self.DieTypeEntry = Entry(self.DiceEntryAndButtonsFrame, textvariable=self.DieTypeEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor, font=self.DiceEntryFont)
        self.DieTypeEntry.grid(row=0, column=2, rowspan=2, padx=2, pady=2, sticky=NSEW)
        StatusBarInst.TooltipConfig(self.DieTypeEntry, "Scroll the mouse wheel or type to change the die type.")

        # Modifier
        self.ModifierLabel = Label(self.DiceEntryAndButtonsFrame, text="+", font=self.DiceEntryFont)
        self.ModifierLabel.grid(row=0, column=3, rowspan=2, sticky=NSEW)
        self.ModifierEntry = Entry(self.DiceEntryAndButtonsFrame, textvariable=self.ModifierEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor, font=self.DiceEntryFont)
        self.ModifierEntry.grid(row=0, column=4, rowspan=2, padx=2, pady=2, sticky=NSEW)
        StatusBarInst.TooltipConfig(self.ModifierEntry, "Scroll the mouse wheel or type to change the modifier.")

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
        self.CritMinimumEntry = Entry(self.CritMinimumFrame, textvariable=self.CritMinimumEntryVar, justify=CENTER, width=5)
        self.CritMinimumEntry.grid(row=0, column=0, sticky=NSEW)

        # Results
        self.ResultsFieldFrame = LabelFrame(self.DiceRollerFrame, text="Results:")
        self.ResultsFieldFrame.grid(row=2, column=self.ResultsFieldFrameColumn, padx=2, pady=2)
        self.ResultsField = ScrolledText(self.ResultsFieldFrame, Width=self.ResultsFieldWidth, Height=self.ResultsFieldHeight, Disabled=True, DisabledBackground=GlobalInst.ButtonColor)
        self.ResultsField.grid(row=0, column=0, padx=2, pady=2)
        self.ResultsField.Text.bind("<Button-1>", self.CopyResults)
        self.ResultsField.Text.bind("<Button-3>", self.ClearResults)
        StatusBarInst.TooltipConfig(self.ResultsField.ScrolledTextFrame, "Left-click to copy results to the clipboard.  Right-click to clear.")

        # Preset Rolls
        self.PresetRollsInst = self.PresetRolls(self.DiceRollerFrame, self.ResultsField, self.CritMinimumEntryVar, self.PresetRollsFrameRow, self.PresetRollsScrolledCanvasHeight, self.PresetRollsScrolledCanvasWidth)
        Inst["PresetRolls"] = self.PresetRollsInst

        # Inspiration Box
        if WindowInst.Mode is "CharacterSheet":
            # Inspiration Box Font
            self.InspirationBoxFont = font.Font(size=16)

            # Box
            self.InspirationBox = Checkbutton(self.DiceRollerFrame, text="Inspiration", variable=self.InspirationBoxVar, font=self.InspirationBoxFont, indicatoron=False, background=self.InspirationFalseColor,
                                              selectcolor=self.InspirationTrueColor)
            self.InspirationBox.grid(row=4, column=0, padx=2, pady=2, sticky=NSEW)

        # Add Saved Fields to Saved Data Dictionary
        SavingAndOpeningInst.SavedData["ResultsField"] = self.ResultsField
        SavingAndOpeningInst.SavedData["CritMinimumEntryVar"] = self.CritMinimumEntryVar
        if WindowInst.Mode is "CharacterSheet":
            SavingAndOpeningInst.SavedData["InspirationBoxVar"] = self.InspirationBoxVar

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
            if WindowInst.Mode is "CharacterSheet":
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
        try:
            DiceNumber = GlobalInst.GetStringVarAsNumber(self.DiceNumberEntryVar)
            DieType = GlobalInst.GetStringVarAsNumber(self.DieTypeEntryVar)
            Modifier = GlobalInst.GetStringVarAsNumber(self.ModifierEntryVar)
        except:
            messagebox.showerror("Invalid Entry", "Can't roll anything but whole numbers.")
            return False
        if DiceNumber < 1 or DieType < 1:
            messagebox.showerror("Invalid Entry", "Can't roll unless dice and die type are positive.")
            return False
        try:
            CritRangeValue = GlobalInst.GetStringVarAsNumber(self.CritMinimumEntryVar)
        except:
            messagebox.showerror("Invalid Entry", "Crit range must be a whole number.")
            return False
        if CritRangeValue <= 0 or CritRangeValue >= 21:
            messagebox.showerror("Invalid Entry", "Crit range must be between 1 and 20.")
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
            StatusBarInst.TooltipConfig(self.PresetRollsScrolledCanvasNameHeader, GlobalInst.SortTooltipString)
            self.PresetRollsScrolledCanvasRollHeader = Label(self.PresetRollsScrolledCanvas.WindowFrame, text="Roll", bd=2, relief=GROOVE)
            self.PresetRollsScrolledCanvasRollHeader.grid(row=0, column=1, sticky=NSEW, columnspan=6)
            self.PresetRollsScrolledCanvasSortOrderHeader = Label(self.PresetRollsScrolledCanvas.WindowFrame, text="Sort\nOrder", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.PresetRollsScrolledCanvasSortOrderHeader.grid(row=0, column=7, sticky=NSEW)
            self.PresetRollsScrolledCanvasSortOrderHeader.bind("<Button-1>", lambda event: self.Sort("Sort Order"))
            self.PresetRollsScrolledCanvasSortOrderHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Sort Order", SearchMode=True))
            self.PresetRollsScrolledCanvasSortOrderHeader.bind("<Button-3>", lambda event: self.Sort("Sort Order", Reverse=True))
            StatusBarInst.TooltipConfig(self.PresetRollsScrolledCanvasSortOrderHeader, GlobalInst.SortTooltipString)

            # Preset Rolls List
            self.PresetRollsList = []

            # Preset Rolls Fields Dictionary
            self.DiceRollerFields = {}
            self.DiceRollerFields["ResultsField"] = self.ResultsField
            self.DiceRollerFields["CritMinimumEntryVar"] = self.CritMinimumEntryVar

            # Sort Order Values
            self.SortOrderValuesString = "\"\""
            for CurrentIndex in range(1, 51):
                self.SortOrderValuesString += "," + str(CurrentIndex)
            self.SortOrderValuesTuple = eval(self.SortOrderValuesString)

            # Preset Rolls
            for CurrentIndex in range(1, 51):
                CurrentEntry = self.PresetRollEntry(self.PresetRollsScrolledCanvas.WindowFrame, self.PresetRollsList, self.ScrollingDisabledVar, self.SortOrderValuesTuple, self.DiceRollerFields, CurrentIndex)
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
                        ListToSort.append((CurrentEntry, CurrentEntry.SortFields["Name"].get(), GlobalInst.GetStringVarAsNumber(CurrentEntry.SortFields[Column])))

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

        class PresetRollEntry:
            def __init__(self, master, List, ScrollingDisabledVar, SortOrderValuesTuple, DiceRollerFields, Row):
                # Store Parameters
                self.master = master
                self.ScrollingDisabledVar = ScrollingDisabledVar
                self.SortOrderValuesTuple = SortOrderValuesTuple
                self.DiceRollerFields = DiceRollerFields
                self.Row = Row

                # Variables
                self.PresetRollNameEntryVar = StringVar()
                self.PresetRollDiceNumberEntryVar = StringVar()
                self.PresetRollDieTypeEntryVar = StringVar()
                self.PresetRollModifierEntryVar = StringVar()
                self.PresetRollSortOrderVar = StringVar()

                # Sort Fields
                self.SortFields = {}
                self.SortFields["Name"] = self.PresetRollNameEntryVar
                self.SortFields["Sort Order"] = self.PresetRollSortOrderVar

                # Add to List
                List.append(self)

                # Name
                self.PresetRollNameEntry = Entry(master, justify=CENTER, width=33, textvariable=self.PresetRollNameEntryVar)

                # Roll Button
                self.PresetRollButton = Button(master, text="Roll:", command=self.RollPreset, bg=GlobalInst.ButtonColor)

                # Dice Number
                self.PresetRollDiceNumberEntry = Entry(master, justify=CENTER, width=5, textvariable=self.PresetRollDiceNumberEntryVar)

                # Die Type
                self.PresetRollDieTypeLabel = Label(master, text="d")
                self.PresetRollDieTypeEntry = Entry(master, justify=CENTER, width=5, textvariable=self.PresetRollDieTypeEntryVar)

                # Modifier
                self.PresetRollModifierButton = Label(master, text="+")
                self.PresetRollModifierEntry = Entry(master, justify=CENTER, width=5, textvariable=self.PresetRollModifierEntryVar)

                # Character Sheet Modifier Config
                if WindowInst.Mode in ["CharacterSheet", "NPCSheet"]:
                    self.PresetRollModifierEntryStatModifierInst = StatModifier(self.PresetRollModifierEntry, "<Button-1>", "Left-click to set a stat modifier.", "Preset Roll")

                # Sort Order
                self.PresetRollSortOrder = ttk.Combobox(master, textvariable=self.PresetRollSortOrderVar, values=self.SortOrderValuesTuple, width=5, state="readonly", justify=CENTER)
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

                # Add Saved Fields to Saved Data Dictionary
                SavingAndOpeningInst.SavedData["PresetRollNameEntryVar" + str(self.Row)] = self.PresetRollNameEntryVar
                SavingAndOpeningInst.SavedData["PresetRollDiceNumberEntryVar" + str(self.Row)] = self.PresetRollDiceNumberEntryVar
                SavingAndOpeningInst.SavedData["PresetRollDieTypeEntryVar" + str(self.Row)] = self.PresetRollDieTypeEntryVar
                SavingAndOpeningInst.SavedData["PresetRollModifierEntryVar" + str(self.Row)] = self.PresetRollModifierEntryVar
                SavingAndOpeningInst.SavedData["PresetRollSortOrderVar" + str(self.Row)] = self.PresetRollSortOrderVar
                if WindowInst.Mode in ["CharacterSheet", "NPCSheet"]:
                    self.PresetRollModifierEntryStatModifierInst.AddToSavedData(Prefix="PresetRollModifierEntry", Suffix=str(self.Row))

                # Add Saved Fields to Dice Roller Fields Dictionary
                self.DiceRollerFields["PresetRollNameEntryVar" + str(self.Row)] = self.PresetRollNameEntryVar
                self.DiceRollerFields["PresetRollDiceNumberEntryVar" + str(self.Row)] = self.PresetRollDiceNumberEntryVar
                self.DiceRollerFields["PresetRollDieTypeEntryVar" + str(self.Row)] = self.PresetRollDieTypeEntryVar
                self.DiceRollerFields["PresetRollModifierEntryVar" + str(self.Row)] = self.PresetRollModifierEntryVar
                self.DiceRollerFields["PresetRollSortOrderVar" + str(self.Row)] = self.PresetRollSortOrderVar

            def DisableScrolling(self, event):
                self.ScrollingDisabledVar.set(True)

            def EnableScrolling(self, event):
                self.ScrollingDisabledVar.set(False)


class EncounterHeader:
    def __init__(self, master):
        self.EncounterNameEntryVar = StringVar()
        self.CREntryVar = StringVar()
        self.ExperienceEntryVar = StringVar()

        # Encounter Header Frame
        self.EncounterHeaderFrame = LabelFrame(master, text="Basic Encounter Info:")
        self.EncounterHeaderFrame.grid_columnconfigure(2, weight=1)
        self.EncounterHeaderFrame.grid_columnconfigure(7, weight=1)
        self.EncounterHeaderFrame.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Encounter Name
        self.EncounterNameLabel = Label(self.EncounterHeaderFrame, text="Encounter Name:")
        self.EncounterNameLabel.grid(row=0, column=0)
        self.EncounterNameEntry = Entry(self.EncounterHeaderFrame, textvariable=self.EncounterNameEntryVar, justify=CENTER, width=30)
        self.EncounterNameEntry.grid(row=0, column=1, padx=2, pady=2)

        # CR
        self.CRLabel = Label(self.EncounterHeaderFrame, text="CR:")
        self.CRLabel.grid(row=0, column=3)
        self.CREntry = Entry(self.EncounterHeaderFrame, textvariable=self.CREntryVar, justify=CENTER, width=5)
        self.CREntry.grid(row=0, column=4, padx=2, pady=2)

        # Experience
        self.ExperienceLabel = Label(self.EncounterHeaderFrame, text="Experience:")
        self.ExperienceLabel.grid(row=0, column=5)
        self.ExperienceEntry = Entry(self.EncounterHeaderFrame, textvariable=self.ExperienceEntryVar, justify=CENTER, width=10)
        self.ExperienceEntry.grid(row=0, column=6, padx=2, pady=2)

        # Notes
        self.NotesFrame = LabelFrame(self.EncounterHeaderFrame, text="Notes:")
        self.NotesFrame.grid_columnconfigure(1, weight=1)
        self.NotesFrame.grid_columnconfigure(3, weight=1)
        self.NotesFrame.grid(row=1, column=0, columnspan=7, padx=2, pady=2, sticky=NSEW)
        self.NotesHeight = 65
        self.NotesWidth = 155
        self.NotesField1 = ScrolledText(self.NotesFrame, Height=self.NotesHeight, Width=self.NotesWidth)
        self.NotesField1.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
        self.NotesField2 = ScrolledText(self.NotesFrame, Height=self.NotesHeight, Width=self.NotesWidth)
        self.NotesField2.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
        self.NotesField3 = ScrolledText(self.NotesFrame, Height=self.NotesHeight, Width=self.NotesWidth)
        self.NotesField3.grid(row=0, column=4, sticky=NSEW, padx=2, pady=2)

        # Description
        self.DescriptionFrame = LabelFrame(self.EncounterHeaderFrame, text="Description:")
        self.DescriptionFrame.grid(row=0, column=8, sticky=NSEW, rowspan=2, padx=2, pady=2)
        self.DescriptionField = ScrolledText(self.DescriptionFrame, Height=100, Width=180)
        self.DescriptionField.grid(row=0, column=0, sticky=NSEW)

        # Rewards
        self.RewardsFrame = LabelFrame(self.EncounterHeaderFrame, text="Rewards:")
        self.RewardsFrame.grid(row=0, column=9, sticky=NSEW, rowspan=2, padx=2, pady=2)
        self.RewardsField = ScrolledText(self.RewardsFrame, Height=100, Width=150)
        self.RewardsField.grid(row=0, column=0, sticky=NSEW)

        # Add Saved Fields to Saved Data Dictionary
        SavingAndOpeningInst.SavedData["EncounterNameEntryVar"] = self.EncounterNameEntryVar
        SavingAndOpeningInst.SavedData["CREntryVar"] = self.CREntryVar
        SavingAndOpeningInst.SavedData["ExperienceEntryVar"] = self.ExperienceEntryVar
        SavingAndOpeningInst.SavedData["NotesField1"] = self.NotesField1
        SavingAndOpeningInst.SavedData["NotesField2"] = self.NotesField2
        SavingAndOpeningInst.SavedData["NotesField3"] = self.NotesField3
        SavingAndOpeningInst.SavedData["DescriptionField"] = self.DescriptionField
        SavingAndOpeningInst.SavedData["RewardsField"] = self.RewardsField


class InitiativeOrder:
    def __init__(self, master):
        # Variables
        self.RoundEntryVar = StringVar(value=str(1))
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
        self.RoundEntry = Entry(self.RoundFrame, textvariable=self.RoundEntryVar, font=self.InitiativeDataFont, width=5, justify=CENTER)
        self.RoundEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # New Round Button
        self.NewRoundButton = Button(self.InitiativeDataFrame, text="New Round", command=self.NewRound, bg=GlobalInst.ButtonColor, font=self.InitiativeDataFont)
        self.NewRoundButton.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
        WindowInst.bind("<Control-r>", lambda event: self.NewRound())
        StatusBarInst.TooltipConfig(self.NewRoundButton, "Keyboard Shortcut:  Ctrl+R")

        # Next Turn Button
        self.NextTurnButton = Button(self.InitiativeDataFrame, text="Next Turn", command=self.NextTurn, bg=GlobalInst.ButtonColor, font=self.InitiativeDataFont)
        self.NextTurnButton.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
        WindowInst.bind("<Control-t>", lambda event: self.NextTurn())
        StatusBarInst.TooltipConfig(self.NextTurnButton, "Keyboard Shortcut:  Ctrl+T")

        # Clear Turns Button
        self.ClearTurnsButton = Button(self.InitiativeDataFrame, text="Clear Turns", command=self.ClearTurns, bg=GlobalInst.ButtonColor, font=self.InitiativeDataFont)
        self.ClearTurnsButton.grid(row=0, column=3, sticky=NSEW, padx=2, pady=2)
        WindowInst.bind("<Control-T>", lambda event: self.ClearTurns())
        StatusBarInst.TooltipConfig(self.ClearTurnsButton, "Keyboard Shortcut:  Ctrl+Shift+T")

        # Sort Initiative Order Button
        self.SortInitiativeOrderButton = Button(self.InitiativeDataFrame, text="Sort Initiative Order", command=self.SortInitiativeOrder, bg=GlobalInst.ButtonColor, font=self.InitiativeDataFont)
        self.SortInitiativeOrderButton.grid(row=0, column=4, sticky=NSEW, padx=2, pady=2)
        WindowInst.bind("<Control-i>", lambda event: self.SortInitiativeOrder())
        StatusBarInst.TooltipConfig(self.SortInitiativeOrderButton, "Keyboard Shortcut:  Ctrl+I")

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

        # Initiative Entries
        for CurrentIndex in range(1, 101):
            CurrentEntry = self.InitiativeEntry(self.InitiativeOrderScrolledCanvas.WindowFrame, self.InitiativeEntriesList, self.ScrollingDisabledVar, CurrentIndex)
            CurrentEntry.Display(CurrentIndex)

        # Add Saved Fields to Saved Data Dictionary
        SavingAndOpeningInst.SavedData["RoundEntryVar"] = self.RoundEntryVar

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
        if self.ValidInitiatives():
            pass
        else:
            return

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
        try:
            Round = GlobalInst.GetStringVarAsNumber(self.RoundEntryVar)
        except:
            messagebox.showerror("Invalid Entry", "Round must be a whole number.")
            return False
        if Round <= 0:
            messagebox.showerror("Invalid Entry", "Round must be greater than 0.")
            return False
        return True

    def ValidInitiatives(self):
        for Entry in self.InitiativeEntriesList:
            try:
                GlobalInst.GetStringVarAsNumber(Entry.InitiativeEntryResultEntryVar)
            except:
                messagebox.showerror("Invalid Entry", "Initiative rolls must be whole numbers.")
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
            self.InitiativeEntryTiePriorityDropdownVar = StringVar(value=str(""))
            self.InitiativeEntryNameEntryVar = StringVar()
            self.InitiativeEntryACEntryVar = StringVar()
            self.InitiativeEntryTempHPEntryVar = StringVar()
            self.InitiativeEntryCurrentHPEntryVar = StringVar()
            self.InitiativeEntryMaxHPEntryVar = StringVar()
            self.ConcentrationTrueColor = "#7aff63"
            self.ConcentrationFalseColor = GlobalInst.ButtonColor
            self.InitiativeEntryConcentrationBoxVar = BooleanVar()
            self.TurnDoneTrueColor = "#7cafff"
            self.InitiativeEntryTurnDoneVar = BooleanVar()
            self.DeadTrueColor = "#ff6d6d"
            self.InitiativeEntryDeadVar = BooleanVar()
            self.InitiativeEntrySizeEntryVar = StringVar()
            self.InitiativeEntryTypeAndTagsEntryVar = StringVar()
            self.InitiativeEntryAlignmentEntryVar = StringVar()
            self.InitiativeEntryProficiencyEntryVar = StringVar()
            self.InitiativeEntrySpeedEntryVar = StringVar()
            self.InitiativeEntryCRAndExperienceEntryVar = StringVar()
            self.InitiativeEntryAbilitiesStrengthEntryVar = StringVar()
            self.InitiativeEntryAbilitiesDexterityEntryVar = StringVar()
            self.InitiativeEntryAbilitiesConstitutionEntryVar = StringVar()
            self.InitiativeEntryAbilitiesIntelligenceEntryVar = StringVar()
            self.InitiativeEntryAbilitiesWisdomEntryVar = StringVar()
            self.InitiativeEntryAbilitiesCharismaEntryVar = StringVar()
            self.InitiativeEntrySkillSensesAndLanguagesFieldVar = StringVar()
            self.InitiativeEntrySavingThrowsFieldVar = StringVar()
            self.InitiativeEntryVulnerabilitiesResistancesAndImmunitiesFieldVar = StringVar()
            self.InitiativeEntrySpecialTraitsFieldVar = StringVar()
            self.InitiativeEntryActionsFieldVar = StringVar()
            self.InitiativeEntryReactionsFieldVar = StringVar()
            self.InitiativeEntryInventoryFieldVar = StringVar()
            self.InitiativeEntryLegendaryActionsAndLairActionsFieldVar = StringVar()
            self.InitiativeEntryNotesFieldVar = StringVar()

            # Add to List
            self.List.append(self)

            # Initiative Entry
            self.InitiativeEntryResultEntry = Entry(self.master, textvariable=self.InitiativeEntryResultEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
            self.InitiativeEntryResultEntry.bind("<Button-3>", lambda event: self.ToggleTurnDone())
            StatusBarInst.TooltipConfig(self.InitiativeEntryResultEntry, "Right-click to toggle turn taken.")

            # Tie Priority Dropdown
            self.InitiativeEntryTiePriorityDropdown = ttk.Combobox(self.master, textvariable=self.InitiativeEntryTiePriorityDropdownVar,
                                                                   values=("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"), width=3, state="readonly", justify=CENTER)
            self.InitiativeEntryTiePriorityDropdown.bind("<Enter>", self.DisableScrolling)
            self.InitiativeEntryTiePriorityDropdown.bind("<Leave>", self.EnableScrolling)

            # Name Entry
            self.InitiativeEntryNameEntry = Entry(self.master, textvariable=self.InitiativeEntryNameEntryVar, justify=CENTER, width=35, bg=GlobalInst.ButtonColor)
            self.InitiativeEntryNameEntry.bind("<Button-3>", self.SetCreatureStats)
            self.InitiativeEntryNameEntry.bind("<Shift-Button-3>", self.Duplicate)
            self.InitiativeEntryNameEntry.bind("<Control-Button-3>", self.Clear)
            StatusBarInst.TooltipConfig(self.InitiativeEntryNameEntry, "Right-click to set additional creature info.  Shift+right-click to duplicate.  Ctrl+right-click to clear.")

            # AC Entry
            self.InitiativeEntryACEntry = Entry(self.master, textvariable=self.InitiativeEntryACEntryVar, justify=CENTER, width=5)

            # Temp HP Entry
            self.InitiativeEntryTempHPEntry = Entry(self.master, textvariable=self.InitiativeEntryTempHPEntryVar, justify=CENTER, width=5)

            # Current HP Entry
            self.InitiativeEntryCurrentHPEntry = Entry(self.master, textvariable=self.InitiativeEntryCurrentHPEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
            self.InitiativeEntryCurrentHPEntry.bind("<Button-3>", lambda event: self.Damage())
            self.InitiativeEntryCurrentHPEntry.bind("<Shift-Button-3>", lambda event: self.Heal())
            self.InitiativeEntryCurrentHPEntry.bind("<Control-Button-3>", lambda event: self.ToggleDead())
            StatusBarInst.TooltipConfig(self.InitiativeEntryCurrentHPEntry, "Right-click to damage.  Shift+right-click to heal.  Control+right-click to toggle dead.")

            # Max HP Entry
            self.InitiativeEntryMaxHPEntry = Entry(self.master, textvariable=self.InitiativeEntryMaxHPEntryVar, justify=CENTER, width=5)

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

            # Add Saved Fields to Saved Data Dictionary
            SavingAndOpeningInst.SavedData["InitiativeEntryInitiativeEntryVar" + str(self.Row)] = self.InitiativeEntryResultEntryVar
            SavingAndOpeningInst.SavedData["InitiativeEntryTiePriorityDropdownVar" + str(self.Row)] = self.InitiativeEntryTiePriorityDropdownVar
            SavingAndOpeningInst.SavedData["InitiativeEntryNameEntryVar" + str(self.Row)] = self.InitiativeEntryNameEntryVar
            SavingAndOpeningInst.SavedData["InitiativeEntryACEntryVar" + str(self.Row)] = self.InitiativeEntryACEntryVar
            SavingAndOpeningInst.SavedData["InitiativeEntryTempHPEntryVar" + str(self.Row)] = self.InitiativeEntryTempHPEntryVar
            SavingAndOpeningInst.SavedData["InitiativeEntryCurrentHPEntryVar" + str(self.Row)] = self.InitiativeEntryCurrentHPEntryVar
            SavingAndOpeningInst.SavedData["InitiativeEntryMaxHPEntryVar" + str(self.Row)] = self.InitiativeEntryMaxHPEntryVar
            SavingAndOpeningInst.SavedData["InitiativeEntryConcentrationBoxVar" + str(self.Row)] = self.InitiativeEntryConcentrationBoxVar
            SavingAndOpeningInst.SavedData["InitiativeEntryConditionsField" + str(self.Row)] = self.InitiativeEntryConditionsField
            SavingAndOpeningInst.SavedData["InitiativeEntryLocationField" + str(self.Row)] = self.InitiativeEntryLocationField
            SavingAndOpeningInst.SavedData["InitiativeEntryNotesField" + str(self.Row)] = self.InitiativeEntryNotesField
            SavingAndOpeningInst.SavedData["InitiativeEntryTurnDoneVar" + str(self.Row)] = self.InitiativeEntryTurnDoneVar
            SavingAndOpeningInst.SavedData["InitiativeEntryDeadVar" + str(self.Row)] = self.InitiativeEntryDeadVar
            SavingAndOpeningInst.SavedData["InitiativeEntrySizeEntryVar" + str(self.Row)] = self.InitiativeEntrySizeEntryVar
            SavingAndOpeningInst.SavedData["InitiativeEntryTypeAndTagsEntryVar" + str(self.Row)] = self.InitiativeEntryTypeAndTagsEntryVar
            SavingAndOpeningInst.SavedData["InitiativeEntryAlignmentEntryVar" + str(self.Row)] = self.InitiativeEntryAlignmentEntryVar
            SavingAndOpeningInst.SavedData["InitiativeEntryProficiencyEntryVar" + str(self.Row)] = self.InitiativeEntryProficiencyEntryVar
            SavingAndOpeningInst.SavedData["InitiativeEntrySpeedEntryVar" + str(self.Row)] = self.InitiativeEntrySpeedEntryVar
            SavingAndOpeningInst.SavedData["InitiativeEntryCRAndExperienceEntryVar" + str(self.Row)] = self.InitiativeEntryCRAndExperienceEntryVar
            SavingAndOpeningInst.SavedData["InitiativeEntryAbilitiesStrengthEntryVar" + str(self.Row)] = self.InitiativeEntryAbilitiesStrengthEntryVar
            SavingAndOpeningInst.SavedData["InitiativeEntryAbilitiesDexterityEntryVar" + str(self.Row)] = self.InitiativeEntryAbilitiesDexterityEntryVar
            SavingAndOpeningInst.SavedData["InitiativeEntryAbilitiesConstitutionEntryVar" + str(self.Row)] = self.InitiativeEntryAbilitiesConstitutionEntryVar
            SavingAndOpeningInst.SavedData["InitiativeEntryAbilitiesIntelligenceEntryVar" + str(self.Row)] = self.InitiativeEntryAbilitiesIntelligenceEntryVar
            SavingAndOpeningInst.SavedData["InitiativeEntryAbilitiesWisdomEntryVar" + str(self.Row)] = self.InitiativeEntryAbilitiesWisdomEntryVar
            SavingAndOpeningInst.SavedData["InitiativeEntryAbilitiesCharismaEntryVar" + str(self.Row)] = self.InitiativeEntryAbilitiesCharismaEntryVar
            SavingAndOpeningInst.SavedData["InitiativeEntrySkillSensesAndLanguagesFieldVar" + str(self.Row)] = self.InitiativeEntrySkillSensesAndLanguagesFieldVar
            SavingAndOpeningInst.SavedData["InitiativeEntrySavingThrowsFieldVar" + str(self.Row)] = self.InitiativeEntrySavingThrowsFieldVar
            SavingAndOpeningInst.SavedData["InitiativeEntryVulnerabilitiesResistancesAndImmunitiesFieldVar" + str(self.Row)] = self.InitiativeEntryVulnerabilitiesResistancesAndImmunitiesFieldVar
            SavingAndOpeningInst.SavedData["InitiativeEntrySpecialTraitsFieldVar" + str(self.Row)] = self.InitiativeEntrySpecialTraitsFieldVar
            SavingAndOpeningInst.SavedData["InitiativeEntryActionsFieldVar" + str(self.Row)] = self.InitiativeEntryActionsFieldVar
            SavingAndOpeningInst.SavedData["InitiativeEntryReactionsFieldVar" + str(self.Row)] = self.InitiativeEntryReactionsFieldVar
            SavingAndOpeningInst.SavedData["InitiativeEntryInventoryFieldVar" + str(self.Row)] = self.InitiativeEntryInventoryFieldVar
            SavingAndOpeningInst.SavedData["InitiativeEntryLegendaryActionsAndLairActionsFieldVar" + str(self.Row)] = self.InitiativeEntryLegendaryActionsAndLairActionsFieldVar
            SavingAndOpeningInst.SavedData["InitiativeEntryNotesFieldVar" + str(self.Row)] = self.InitiativeEntryNotesFieldVar

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
            if self.InitiativeEntryCurrentHPEntryVar.get() == "":
                CurrentHP = GlobalInst.GetStringVarAsNumber(self.InitiativeEntryMaxHPEntryVar)
            else:
                CurrentHP = GlobalInst.GetStringVarAsNumber(self.InitiativeEntryCurrentHPEntryVar)
            DamagePrompt = IntegerPrompt(WindowInst, "Damage", "How much damage?", MinValue=1)
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
            HealingPrompt = IntegerPrompt(WindowInst, "Heal", "How much healing?", MinValue=1)
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

            # Handle Values
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
        if WindowInst.Mode is "NPCSheet":
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

        if WindowInst.Mode is "CharacterSheet":
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

        if WindowInst.Mode is "NPCSheet":
            # Update Stats Button
            self.MenuBar.add_command(label="Update Stats (Ctrl+D)", command=CreatureDataInst.UpdateStats)
            WindowInst.bind("<Control-d>", lambda event: CreatureDataInst.UpdateStats())


class StatusBar:
    def __init__(self, master):
        # Configure Mode Parameters
        if WindowInst.Mode is "CreatureDataUtility":
            self.Row = 1
            self.Column = 0
            self.ColumnSpan = 1
        if WindowInst.Mode is "DiceRoller":
            self.Row = 1
            self.Column = 0
            self.ColumnSpan = 1
        elif WindowInst.Mode is "EncounterManager":
            self.Row = 2
            self.Column = 0
            self.ColumnSpan = 2
        elif WindowInst.Mode is "CharacterSheet":
            self.Row = 1
            self.Column = 0
            self.ColumnSpan = 2
        elif WindowInst.Mode is "NPCSheet":
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

    def TooltipConfig(self, Widget, TooltipText, LeaveText="Status", EnterLock=False, EnterUnlock=False, LeaveLock=False, LeaveUnlock=False):
        Widget.bind("<Enter>", lambda event: self.StatusBarSetText(TooltipText, Lock=EnterLock, Unlock=EnterUnlock))
        Widget.bind("<Leave>", lambda event: self.StatusBarSetText(LeaveText, Lock=LeaveLock, Unlock=LeaveUnlock))

    def FlashStatus(self, Text, Duration=2000):
        StatusBarInst.StatusBarSetText(Text, Lock=True)
        WindowInst.after(Duration, lambda: self.StatusBarSetText("Status", Unlock=True))


class ScrolledText:
    def __init__(self, master, Width=100, Height=100, Disabled=False, DisabledBackground="light gray", FontSize=None):
        self.Width = Width
        self.Height = Height
        self.Disabled = Disabled
        self.FontSize = FontSize

        # Scrolled Text Frame
        self.ScrolledTextFrame = Frame(master, width=self.Width, height=self.Height)
        self.ScrolledTextFrame.pack_propagate(False)
        self.ScrolledTextFrame.grid_propagate(False)

        # Scrollbar
        self.Scrollbar = Scrollbar(self.ScrolledTextFrame, orient=VERTICAL)
        self.Scrollbar.pack(side=RIGHT, fill=Y)

        # Text Widget
        self.Text = self.TrackedText(self.ScrolledTextFrame, wrap=WORD)
        self.Text.pack(side=LEFT, expand=YES, fill=BOTH)
        if self.Disabled:
            self.Text.configure(state=DISABLED, bg=DisabledBackground, cursor="arrow")
        if self.FontSize != None:
            self.Text.configure(font=font.Font(size=self.FontSize))

        # Set Up Scrolling
        self.Text.configure(yscrollcommand=self.Scrollbar.set)
        self.Scrollbar.configure(command=self.Text.yview)

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

    class TrackedText(Text):
        def __init__(self, *args, **kwargs):
            # Init Text
            Text.__init__(self, *args, **kwargs)

            # Create Proxy
            self._orig = self._w + "_orig"
            self.tk.call("rename", self._w, self._orig)
            self.tk.createcommand(self._w, self._proxy)

            # Intercept Paste Event
            self.bind("<<Paste>>", self.Paste)

            # Create Indent Tags
            self.IndentValue = 15
            self.IndentLevels = 10
            for IndentLevel in range(1, self.IndentLevels + 1):
                self.tag_configure("INDENT" + str(IndentLevel), lmargin1=self.IndentValue * IndentLevel, lmargin2=self.IndentValue * IndentLevel)

        def _proxy(self, command, *args):
            cmd = (self._orig, command) + args
            result = self.tk.call(cmd)
            if command in ("insert", "delete", "replace"):
                self.event_generate("<<TextModified>>")
                self.FormatIndentations()
            return result

        def Paste(self, event):
            SelectionRange = self.tag_ranges("sel")
            if SelectionRange:
                SelectionStart = self.index(SEL_FIRST)
                SelectionEnd = self.index(SEL_LAST)
                self.delete(SelectionStart, SelectionEnd)
                self.mark_set(INSERT, SelectionStart)
            self.insert(INSERT, self.clipboard_get())
            self.see(INSERT)
            return "break"

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
        self.IntegerEntry = Entry(self.TableFrame, width=20, textvariable=self.IntegerEntryVar, justify=CENTER)
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
        if self.ValidEntry():
            pass
        else:
            return
        self.DataSubmitted.set(True)
        self.Window.destroy()

    def Cancel(self):
        self.DataSubmitted.set(False)
        self.Window.destroy()

        return None

    def GetData(self):
        return GlobalInst.GetStringVarAsNumber(self.IntegerEntryVar)

    def ValidEntry(self):
        try:
            EntryValue = GlobalInst.GetStringVarAsNumber(self.IntegerEntryVar)
        except:
            messagebox.showerror("Invalid Entry", "Must be a whole number.")
            return False
        if self.MinValue != None:
            if EntryValue < self.MinValue:
                messagebox.showerror("Invalid Entry", "Must be at least " + str(self.MinValue) + ".")
                return False
        if self.MaxValue != None:
            if EntryValue > self.MaxValue:
                messagebox.showerror("Invalid Entry", "Must be no more than " + str(self.MaxValue) + ".")
                return False
        return True


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
        self.StringEntry = Entry(self.TableFrame, width=20, textvariable=self.StringEntryVar, justify=CENTER)
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
        self.UnopenedDataField = ScrolledText(self.UnopenedDataFrame, Disabled=True, Width=500, Height=200)
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


# Mode Select
class ModeSelect(Tk):
    def __init__(self):
        # Create Window
        Tk.__init__(self)

        # Configure Window
        self.wm_title("Select Mode - PyFifth")
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
        self.CharacterSheetModeButton.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Dice Roller Button
        self.DiceRollerModeButton = Button(self, text="Dice Roller", command=lambda: self.SelectMode("DiceRoller"), bg=GlobalInst.ButtonColor, font=self.ButtonsFont)
        self.DiceRollerModeButton.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)

        # Encounter Manager Button
        self.EncounterManagerModeButton = Button(self, text="Encounter Manager", command=lambda: self.SelectMode("EncounterManager"), bg=GlobalInst.ButtonColor, font=self.ButtonsFont)
        self.EncounterManagerModeButton.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)

        # NPC Sheet Button
        self.NPCSheetModeButton = Button(self, text="NPC Sheet", command=lambda: self.SelectMode("NPCSheet"), bg=GlobalInst.ButtonColor, font=self.ButtonsFont)
        self.NPCSheetModeButton.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)

        # Creature Data Utility Button
        self.CreatureDataUtilityModeButton = Button(self, text="Creature Data Utility", command=lambda: self.SelectMode("CreatureDataUtility"), bg=GlobalInst.ButtonColor, font=self.ButtonsFont)
        self.CreatureDataUtilityModeButton.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)

        # Coin Calculator Button
        self.CoinCalculatorModeButton = Button(self, text="Coin Calculator", command=lambda: self.SelectMode("CoinCalculator"), bg=GlobalInst.ButtonColor, font=self.ButtonsFont)
        self.CoinCalculatorModeButton.grid(row=2, column=1, sticky=NSEW, padx=2, pady=2)

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
        if self.Mode is "CreatureDataUtility" or self.Mode is "NPCSheet":
            Prefix = CreatureDataInst.NameEntryVar.get()
        elif self.Mode is "EncounterManager":
            Prefix = EncounterHeaderInst.EncounterNameEntryVar.get()
        elif self.Mode is "CharacterSheet":
            Prefix = CharacterSheetInst.CharacterNameEntryVar.get()
        else:
            Prefix = ""
        if Prefix != "":
            Prefix += " - "

        # Current Open File and Save Prompt
        if self.Mode in ["CharacterSheet", "EncounterManager", "CreatureDataUtility", "DiceRoller", "NPCSheet"]:
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
    if ModeSelectInst.ModeSelected is "":
        sys.exit()

    # Window Titles
    WindowTitles = {}
    WindowTitles["CharacterSheet"] = "Character Sheet - PyFifth"
    WindowTitles["DiceRoller"] = "Dice Roller - PyFifth"
    WindowTitles["EncounterManager"] = "Encounter Manager - PyFifth"
    WindowTitles["CreatureDataUtility"] = "Creature Data Utility - PyFifth"
    WindowTitles["CoinCalculator"] = "Coin Calculator - PyFifth"
    WindowTitles["NPCSheet"] = "NPC Sheet - PyFifth"

    # Minimum Resolutions
    MinimumResolutions = {}
    MinimumResolutions["CharacterSheet"] = (1208, 708)
    MinimumResolutions["DiceRoller"] = (675, 451)
    MinimumResolutions["EncounterManager"] = (1331, 794)
    MinimumResolutions["CreatureDataUtility"] = (802, 766)
    MinimumResolutions["CoinCalculator"] = (291, 216)
    MinimumResolutions["NPCSheet"] = (1262, 785)

    # Create Window
    WindowInst = Window(ModeSelectInst.ModeSelected, WindowTitles[ModeSelectInst.ModeSelected])

    # Populate Window
    if WindowInst.Mode is "CoinCalculator":
        CoinCalculatorInst = CoinCalculator(WindowInst.WidgetMaster)
    elif WindowInst.Mode is "CreatureDataUtility":
        StatusBarInst = StatusBar(WindowInst)
        SavingAndOpeningInst = SavingAndOpening()
        MenuBarInst = MenuBar(WindowInst)
        CreatureDataInst = CreatureData(WindowInst.WidgetMaster)
        SavingAndOpeningInst.TrackModifiedFields()
    elif WindowInst.Mode is "DiceRoller":
        StatusBarInst = StatusBar(WindowInst)
        SavingAndOpeningInst = SavingAndOpening()
        DiceRollerInst = DiceRoller(WindowInst.WidgetMaster)
        MenuBarInst = MenuBar(WindowInst)
        SavingAndOpeningInst.TrackModifiedFields()
    elif WindowInst.Mode is "EncounterManager":
        StatusBarInst = StatusBar(WindowInst)
        SavingAndOpeningInst = SavingAndOpening()
        EncounterHeaderInst = EncounterHeader(WindowInst.WidgetMaster)
        InitiativeOrderInst = InitiativeOrder(WindowInst.WidgetMaster)
        DiceRollerInst = DiceRoller(WindowInst.WidgetMaster)
        MenuBarInst = MenuBar(WindowInst)
        SavingAndOpeningInst.TrackModifiedFields()
    elif WindowInst.Mode is "CharacterSheet":
        StatusBarInst = StatusBar(WindowInst)
        SavingAndOpeningInst = SavingAndOpening()
        CharacterSheetInst = CharacterSheet(WindowInst.WidgetMaster)
        DiceRollerInst = DiceRoller(WindowInst.WidgetMaster)
        MenuBarInst = MenuBar(WindowInst)
        SavingAndOpeningInst.TrackModifiedFields()
        GlobalInst.SetupStatModifiers()
    elif WindowInst.Mode is "NPCSheet":
        StatusBarInst = StatusBar(WindowInst)
        SavingAndOpeningInst = SavingAndOpening()
        CreatureDataInst = CreatureData(WindowInst.WidgetMaster)
        DiceRollerInst = DiceRoller(WindowInst.WidgetMaster)
        MenuBarInst = MenuBar(WindowInst)
        SavingAndOpeningInst.TrackModifiedFields()
        GlobalInst.SetupStatModifiers()

    # Configure Window
    GlobalInst.WindowGeometry(WindowInst)
    if WindowInst.LowResolution:
        WindowInst.WidgetCanvas.ConfigureScrolledCanvas()
    WindowInst.focus_force()

    # Main Loop
    WindowInst.mainloop()
