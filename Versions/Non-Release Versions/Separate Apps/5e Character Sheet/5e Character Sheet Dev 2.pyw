import platform
from tkinter import *
import tkinter.scrolledtext as ScrolledTextClass
from tkinter import filedialog
from tkinter import messagebox
from time import sleep
import random
from tkinter import ttk
import math
import os
from zipfile import ZipFile
from decimal import *
from tkinter import simpledialog

# Global Variables
OS = platform.system()
ButtonColor = "#F1F1D4"

# Create and Configure Window
root = Tk()
root.wm_title("Character Sheet")
root.option_add("*Font", "TkDefaultFont")


# Global Functions
def GetStringVarAsInt(Var):
    VarText = Var.get()
    if len(VarText) == 0:
        VarText = 0
    return int(VarText)


def GetStringVarAsDecimal(Var):
    VarText = Var.get()
    if len(VarText) == 0:
        VarText = 0
    return Decimal(VarText)


def GetStringVarAsFloat(Var):
    VarText = Var.get()
    if len(VarText) == 0:
        VarText = 0
    return float(VarText)


def WindowGeometry(Window, IsDialog):
    Window.update_idletasks()
    BaseWidth = Window.winfo_width()
    BaseHeight = Window.winfo_height()
    BorderWidth = Window.winfo_rootx() - Window.winfo_x()
    WindowWidth = BaseWidth + (2 * BorderWidth)
    TitleHeight = Window.winfo_rooty() - Window.winfo_y()
    WindowHeight = BaseHeight + TitleHeight + BorderWidth
    if IsDialog:
        XCoordinate = root.winfo_x() + ((root.winfo_width() // 2) - (WindowWidth // 2))
        YCoordinate = root.winfo_y() + ((root.winfo_height() // 2) - (WindowHeight // 2))
    else:
        XCoordinate = (Window.winfo_screenwidth() // 2) - (WindowWidth // 2)
        YCoordinate = (Window.winfo_screenheight() // 2) - (WindowHeight // 2)
    Window.geometry("{}x{}+{}+{}".format(BaseWidth, BaseHeight, XCoordinate, YCoordinate))
    Window.resizable(width=False, height=False)


def UnbindMouseWheel(event):
    root.unbind("<MouseWheel>")


def UpdateStatsAndInventory():
    # Test Level Input Validity
    if CharacterSheetHeaderInst.ValidLevelEntry():
        pass
    else:
        return

    # Test Ability Input Validity
    if StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.ValidStatsEntry():
        pass
    else:
        return

    # Store Level
    CharacterLevelValue = GetStringVarAsInt(CharacterSheetHeaderInst.CharacterLevelEntryVar)

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
    if CharacterLevelValue >= 14:
        TotalExperienceNeeded += 25000
        ProficiencyModifier += 1
    if CharacterLevelValue >= 15:
        TotalExperienceNeeded += 30000
    if CharacterLevelValue >= 16:
        TotalExperienceNeeded += 30000
    if CharacterLevelValue >= 17:
        TotalExperienceNeeded += 40000
    if CharacterLevelValue >= 18:
        TotalExperienceNeeded += 40000
        ProficiencyModifier += 1
    if CharacterLevelValue >= 19:
        TotalExperienceNeeded += 50000
    if CharacterLevelValue >= 20:
        TotalExperienceNeeded = "N/A - Max Level"
    CharacterSheetHeaderInst.CharacterExperienceNeededEntryVar.set(TotalExperienceNeeded)
    CharacterSheetHeaderInst.ProficiencyBonusEntryVar.set("+" + str(ProficiencyModifier))

    # Calculate Ability and Saving Throw Modifiers
    for Entry in StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.AbilityEntriesList:
        Entry.CalculateModifiers(ProficiencyModifier)

    # Store Ability Modifiers for Skills
    StrengthModifier = GetStringVarAsInt(StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.StrengthEntry.AbilityEntryModifierVar)
    DexterityModifier = GetStringVarAsInt(StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.DexterityEntry.AbilityEntryModifierVar)
    IntelligenceModifier = GetStringVarAsInt(StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.IntelligenceEntry.AbilityEntryModifierVar)
    WisdomModifier = GetStringVarAsInt(StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.WisdomEntry.AbilityEntryModifierVar)
    CharismaModifier = GetStringVarAsInt(StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.CharismaEntry.AbilityEntryModifierVar)

    # Calculate Skill Modifiers
    for Entry in StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.SkillsInst.SkillsEntriesList:
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
    for Entry in StatsAndDiceRollerFrameInst.DiceRollerInst.PresetRollsInst.PresetRollsList:
        Entry.SetConfiguredModifier()

    # Test Inventory Input Validity
    if StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.InventoryInst.ValidInventoryEntry():
        pass
    else:
        return

    # Calculate Inventory
    StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.InventoryInst.Calculate()

    # Calculate AC
    ACBase = GetStringVarAsInt(StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.ACBaseEntryVar)
    ACModifierString = StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.ACModifierVar.get()
    ACManualBonus = GetStringVarAsInt(StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.ACManualBonusEntryVar)
    if ACModifierString == "Dexterity":
        ACModifier = DexterityModifier
    elif ACModifierString == "Dexterity (Max 2)":
        ACModifier = min(DexterityModifier, 2)
    else:
        ACModifier = 0
    StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.ACEntryVar.set(str(ACBase + ACModifier + ACManualBonus))

    # Calculate Initiative Bonus
    InitiativeManualBonus = GetStringVarAsInt(StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.InitiativeManualBonusEntryVar)
    TotalInitiativeBonus = InitiativeManualBonus + DexterityModifier
    InitiativeBonusSign = ""
    if TotalInitiativeBonus > 0:
        InitiativeBonusSign = "+"
    StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.InitiativeEntryVar.set(InitiativeBonusSign + str(TotalInitiativeBonus))

    # Update Window Title
    CharacterName = CharacterSheetHeaderInst.CharacterNameEntryVar.get()
    if CharacterName != "":
        root.wm_title(CharacterName + " - Character Sheet")


def ConfigureBindings():
    # Update Stats Tooltip
    root.bind("<Control-d>", CharacterSheetHeaderInst.UpdateStatsKeystroke)
    ToolbarAndStatusBarInst.UpdateStatsButton.bind("<Enter>", CharacterSheetHeaderInst.UpdateStatsButtonTooltipSet)
    ToolbarAndStatusBarInst.UpdateStatsButton.bind("<Leave>", ToolbarAndStatusBarInst.ToolbarRevertToPrevious)

    # Preset Rolls Scrolling
    StatsAndDiceRollerFrameInst.DiceRollerInst.PresetRollsInst.PresetRollsFrame.bind("<Enter>", StatsAndDiceRollerFrameInst.DiceRollerInst.PresetRollsInst.BindMouseWheelPresetRolls)
    StatsAndDiceRollerFrameInst.DiceRollerInst.PresetRollsInst.PresetRollsFrame.bind("<Leave>", UnbindMouseWheel)

    # Features Scrolling
    StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.FeaturesInst.FeaturesFrame.bind("<Enter>",
                                                                                                                          StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.FeaturesInst.BindMouseWheelFeatures)
    StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.FeaturesInst.FeaturesFrame.bind("<Leave>", UnbindMouseWheel)

    # Inventory Scrolling
    for Entry in StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.InventoryInst.InventoryEntriesList:
        Entry.NameEntry.bind("<Enter>", StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.InventoryInst.BindMouseWheelInventoryList)
        Entry.NameEntry.bind("<Leave>", UnbindMouseWheel)
        Entry.CountEntry.bind("<Enter>", StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.InventoryInst.BindMouseWheelInventoryList)
        Entry.CountEntry.bind("<Leave>", UnbindMouseWheel)
        Entry.UnitWeightEntry.bind("<Enter>", StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.InventoryInst.BindMouseWheelInventoryList)
        Entry.UnitWeightEntry.bind("<Leave>", UnbindMouseWheel)
        Entry.UnitValueEntry.bind("<Enter>", StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.InventoryInst.BindMouseWheelInventoryList)
        Entry.UnitValueEntry.bind("<Leave>", UnbindMouseWheel)
        Entry.TotalWeightEntry.bind("<Enter>", StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.InventoryInst.BindMouseWheelInventoryList)
        Entry.TotalWeightEntry.bind("<Leave>", UnbindMouseWheel)
        Entry.TotalValueEntry.bind("<Enter>", StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.InventoryInst.BindMouseWheelInventoryList)
        Entry.TotalValueEntry.bind("<Leave>", UnbindMouseWheel)

    # Save and Open Keystrokes and Tooltips
    root.bind("<Control-s>", ToolbarAndStatusBarInst.SaveKeystroke)
    root.bind("<Control-S>", ToolbarAndStatusBarInst.SaveAsKeystroke)
    root.bind("<Control-o>", ToolbarAndStatusBarInst.OpenKeystroke)
    ToolbarAndStatusBarInst.ToolbarSaveButton.bind("<Enter>", ToolbarAndStatusBarInst.ToolbarSaveButtonTooltipSet)
    ToolbarAndStatusBarInst.ToolbarSaveAsButton.bind("<Enter>", ToolbarAndStatusBarInst.ToolbarSaveAsButtonTooltipSet)
    ToolbarAndStatusBarInst.ToolbarOpenButton.bind("<Enter>", ToolbarAndStatusBarInst.ToolbarOpenButtonTooltipSet)
    ToolbarAndStatusBarInst.ToolbarSaveButton.bind("<Leave>", ToolbarAndStatusBarInst.ToolbarRevertToPrevious)
    ToolbarAndStatusBarInst.ToolbarSaveAsButton.bind("<Leave>", ToolbarAndStatusBarInst.ToolbarRevertToPrevious)
    ToolbarAndStatusBarInst.ToolbarOpenButton.bind("<Leave>", ToolbarAndStatusBarInst.ToolbarRevertToPrevious)

    # Ability and Saving Throw Roll Tooltips
    for Entry in StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.AbilityEntriesList:
        Entry.ConfigureTooltipBindings()

    # Skill Roll Tooltips
    for Entry in StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.SkillsInst.SkillsEntriesList:
        Entry.ConfigureTooltipBindings()

    # AC Tooltip
    StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.ACEntry.bind("<Enter>",
                                                                                                       StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.ACEntryTooltipSet)
    StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.ACEntry.bind("<Leave>", ToolbarAndStatusBarInst.ToolbarRevertToPrevious)

    # Initiative Tooltip
    StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.InitiativeEntry.bind("<Enter>",
                                                                                                               StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.InitiativeEntryTooltipSet)
    StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.InitiativeEntry.bind("<Leave>", ToolbarAndStatusBarInst.ToolbarRevertToPrevious)

    # Features Tooltips
    for Entry in StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.FeaturesInst.FeaturesEntriesList:
        Entry.NameEntry.bind("<Enter>", Entry.FeatureEntryTooltipSet)
        Entry.NameEntry.bind("<Leave>", ToolbarAndStatusBarInst.ToolbarRevertToPrevious)


# Window Elements
class CharacterSheetHeader:
    CharacterNameEntryVar = StringVar()
    CharacterLevelEntryVar = StringVar()
    CharacterClassEntryVar = StringVar()
    CharacterExperienceEntryVar = StringVar()
    CharacterExperienceNeededEntryVar = StringVar()
    ProficiencyBonusEntryVar = StringVar()

    def __init__(self, master):
        # Character Sheet Header
        self.CharacterSheetHeaderFrame = LabelFrame(master, text="Basic Character Info:")
        self.CharacterSheetHeaderFrame.pack(side=TOP, expand=True, fill=X, padx=2, pady=2)

        # Character Name
        self.CharacterNameLabel = Label(self.CharacterSheetHeaderFrame, text="Character Name:")
        self.CharacterNameLabel.pack(side=LEFT)
        self.CharacterNameEntry = Entry(self.CharacterSheetHeaderFrame, textvariable=self.CharacterNameEntryVar, justify=CENTER, width=25)
        self.CharacterNameEntry.pack(side=LEFT, padx=2, pady=2)

        # Class
        self.CharacterClassLabel = Label(self.CharacterSheetHeaderFrame, text="Class:")
        self.CharacterClassLabel.pack(side=LEFT)
        self.CharacterClassEntry = Entry(self.CharacterSheetHeaderFrame, textvariable=self.CharacterClassEntryVar, justify=CENTER, width=15)
        self.CharacterClassEntry.pack(side=LEFT, padx=2, pady=2)

        # Character Level
        self.CharacterLevelLabel = Label(self.CharacterSheetHeaderFrame, text="Level:")
        self.CharacterLevelLabel.pack(side=LEFT)
        self.CharacterLevelEntry = Entry(self.CharacterSheetHeaderFrame, textvariable=self.CharacterLevelEntryVar, width=4, justify=CENTER)
        self.CharacterLevelEntry.pack(side=LEFT, padx=2, pady=2)

        # Experience
        self.CharacterExperienceLabel = Label(self.CharacterSheetHeaderFrame, text="Exp.:")
        self.CharacterExperienceLabel.pack(side=LEFT)
        self.CharacterExperienceEntry = Entry(self.CharacterSheetHeaderFrame, textvariable=self.CharacterExperienceEntryVar, width=10, justify=CENTER)
        self.CharacterExperienceEntry.pack(side=LEFT, padx=2, pady=2)
        self.CharacterExperienceNeededLabel = Label(self.CharacterSheetHeaderFrame, text="Needed Exp.:")
        self.CharacterExperienceNeededLabel.pack(side=LEFT)
        self.CharacterExperienceNeededEntry = Entry(self.CharacterSheetHeaderFrame, textvariable=self.CharacterExperienceNeededEntryVar, state=DISABLED, justify=CENTER, width=15, disabledbackground="light gray",
                                                    disabledforeground="black", cursor="arrow")
        self.CharacterExperienceNeededEntry.pack(side=LEFT, padx=2, pady=2)

        # Proficiency Bonus
        self.ProficiencyBonusLabel = Label(self.CharacterSheetHeaderFrame, text="Proficiency Bonus:")
        self.ProficiencyBonusLabel.pack(side=LEFT)
        self.ProficiencyBonusEntry = Entry(self.CharacterSheetHeaderFrame, textvariable=self.ProficiencyBonusEntryVar, state=DISABLED, justify=CENTER, width=3, disabledbackground="light gray", disabledforeground="black",
                                           cursor="arrow")
        self.ProficiencyBonusEntry.pack(side=LEFT, padx=2, pady=2)

    def UpdateStatsKeystroke(self, event):
        UpdateStatsAndInventory()

    def UpdateStatsButtonTooltipSet(self, event):
        ToolbarAndStatusBarInst.StatusBarPreviousTextVar.set(ToolbarAndStatusBarInst.StatusBarTextVar.get())
        ToolbarAndStatusBarInst.StatusBarTextVar.set("Keyboard Shortcut:  Ctrl+D")

    def ValidLevelEntry(self):
        try:
            CharacterLevelValue = GetStringVarAsInt(self.CharacterLevelEntryVar)
        except:
            messagebox.showerror("Invalid Entry", "Character level must be an integer.")
            return False
        if CharacterLevelValue <= 0 or CharacterLevelValue >= 21:
            messagebox.showerror("Invalid Entry", "Character level must be between 1 and 20.")
            return False
        return True


class StatsAndDiceRoller:
    def __init__(self, master):
        # Stats and Dice Roller Frame
        self.StatsAndDiceRollerFrame = Frame(master)
        self.StatsAndDiceRollerFrame.pack(side=TOP)

        # Character Stats
        self.CharacterStatsInventoryAndNotesInst = self.CharacterStatsInventoryAndNotes(self.StatsAndDiceRollerFrame)

        # Dice Roller
        self.DiceRollerInst = self.DiceRoller(self.StatsAndDiceRollerFrame)

    # Character Stats, Inventory, and Notes
    class CharacterStatsInventoryAndNotes:
        def __init__(self, master):
            # Character Stats Frame
            self.CharacterStatsFrame = LabelFrame(master, text="Character Stats, Inventory, and Notes:")
            self.CharacterStatsFrame.pack(side=LEFT, padx=2, pady=2)

            # Character Stats Notebook
            self.CharacterStatsNotebook = ttk.Notebook(self.CharacterStatsFrame, height=500)
            self.CharacterStatsNotebook.pack()
            self.CharacterStatsNotebook.enable_traversal()

            # Abilities and Skills Page
            self.AbilitiesAndSkillsPage = Frame(self.CharacterStatsNotebook)
            self.CharacterStatsNotebook.add(self.AbilitiesAndSkillsPage, text="Abilities and Skills")
            self.AbilitiesAndSkillsInst = self.AbilitiesAndSkills(self.AbilitiesAndSkillsPage)

            # Combat and Features
            self.CombatAndFeaturesPage = Frame(self.CharacterStatsNotebook)
            self.CharacterStatsNotebook.add(self.CombatAndFeaturesPage, text="Combat and Features")
            self.CombatAndFeaturesInst = self.CombatAndFeatures(self.CombatAndFeaturesPage)

            # Spells
            self.SpellsPage = Frame(self.CharacterStatsNotebook)
            self.CharacterStatsNotebook.add(self.SpellsPage, text="Spells")
            self.SpellsInst = self.Spells(self.SpellsPage)

            # Inventory
            self.InventoryPage = Frame(self.CharacterStatsNotebook)
            self.CharacterStatsNotebook.add(self.InventoryPage, text="Inventory")
            self.InventoryInst = self.Inventory(self.InventoryPage)

            # Notes
            self.NotesPage = Frame(self.CharacterStatsNotebook)
            self.CharacterStatsNotebook.add(self.NotesPage, text="Notes")
            self.NotesInst = self.Notes(self.NotesPage)

            # Personality and Backstory
            self.PersonalityAndBackstoryPage = Frame(self.CharacterStatsNotebook)
            self.CharacterStatsNotebook.add(self.PersonalityAndBackstoryPage, text="Personality and Backstory")
            self.PersonalityAndBackstoryInst = self.PersonalityAndBackstory(self.PersonalityAndBackstoryPage)

            # Portrait
            self.PortraitPage = Frame(self.CharacterStatsNotebook)
            self.CharacterStatsNotebook.add(self.PortraitPage, text="Portrait")
            self.PortraitInst = self.Portrait(self.PortraitPage)

        # Abilities and Skills
        class AbilitiesAndSkills:
            def __init__(self, master):
                # Abilities and Saving Throws
                self.AbilitiesAndSavingThrowsFrame = LabelFrame(master, text="Abilities and Saving Throws:")
                self.AbilitiesAndSavingThrowsFrame.grid(row=1, column=1, padx=2, pady=2, sticky=NW)
                self.AbilitiesAndSavingThrowsInst = self.AbilitiesAndSavingThrowsTable(self.AbilitiesAndSavingThrowsFrame)

                # Skills
                self.SkillsFrame = LabelFrame(master, text="Skills:")
                self.SkillsFrame.grid(row=1, column=3, padx=2, pady=2, sticky=N)
                self.SkillsInst = self.SkillsTable(self.SkillsFrame)

                # Center Abilities, Saving Throws, and Skills
                master.grid_rowconfigure(0, weight=1)
                master.grid_rowconfigure(2, weight=1)
                master.grid_columnconfigure(0, weight=1)
                master.grid_columnconfigure(2, weight=1)
                master.grid_columnconfigure(4, weight=1)

            # Abilities and Saving Throws
            class AbilitiesAndSavingThrowsTable:
                def __init__(self, master):
                    self.PointBuyBoxVar = BooleanVar()

                    # Abilities and Saving Throws Holder Frame
                    self.AbilitiesAndSavingThrowsHolderFrame = Frame(master)
                    self.AbilitiesAndSavingThrowsHolderFrame.pack()

                    # Labels
                    self.AbilitiesHeaderAbility = Label(self.AbilitiesAndSavingThrowsHolderFrame, text="Ability", bd=2, relief=GROOVE)
                    self.AbilitiesHeaderTotal = Label(self.AbilitiesAndSavingThrowsHolderFrame, text="Total", bd=2, relief=GROOVE)
                    self.AbilitiesHeaderModifier = Label(self.AbilitiesAndSavingThrowsHolderFrame, text="Modifier", bd=2, relief=GROOVE)
                    self.AbilitiesHeaderSpacer = Frame(self.AbilitiesAndSavingThrowsHolderFrame, width=15)
                    self.AbilitiesHeaderSpacer.grid(rowspan=6, column=3)
                    self.AbilitiesHeaderSavingThrowsProf = Label(self.AbilitiesAndSavingThrowsHolderFrame, text="Prof.", bd=2, relief=GROOVE)
                    self.AbilitiesHeaderSavingThrowsProf.grid(row=0, column=4, sticky=NSEW)
                    self.AbilitiesHeaderSavingThrows = Label(self.AbilitiesAndSavingThrowsHolderFrame, text="Saving Throws", bd=2, relief=GROOVE)
                    self.AbilitiesHeaderSavingThrows.grid(row=0, column=5, sticky=NSEW)
                    self.AbilitiesHeaderAbility.grid(row=0, column=0, sticky=NSEW)
                    self.AbilitiesHeaderTotal.grid(row=0, column=1, sticky=NSEW)
                    self.AbilitiesHeaderModifier.grid(row=0, column=2, sticky=NSEW)

                    # Ability Entries List
                    self.AbilityEntriesList = []

                    # Ability Entries
                    self.StrengthEntry = self.AbilitiesAndSavingThrowsEntry(self.AbilitiesAndSavingThrowsHolderFrame, "Strength", self.AbilityEntriesList, 1)
                    self.DexterityEntry = self.AbilitiesAndSavingThrowsEntry(self.AbilitiesAndSavingThrowsHolderFrame, "Dexterity", self.AbilityEntriesList, 2)
                    self.ConstitutionEntry = self.AbilitiesAndSavingThrowsEntry(self.AbilitiesAndSavingThrowsHolderFrame, "Constitution", self.AbilityEntriesList, 3)
                    self.IntelligenceEntry = self.AbilitiesAndSavingThrowsEntry(self.AbilitiesAndSavingThrowsHolderFrame, "Intelligence", self.AbilityEntriesList, 4)
                    self.WisdomEntry = self.AbilitiesAndSavingThrowsEntry(self.AbilitiesAndSavingThrowsHolderFrame, "Wisdom", self.AbilityEntriesList, 5)
                    self.CharismaEntry = self.AbilitiesAndSavingThrowsEntry(self.AbilitiesAndSavingThrowsHolderFrame, "Charisma", self.AbilityEntriesList, 6)

                    # Abilities Data Config
                    self.AbilitiesDataConfigButton = Button(self.AbilitiesAndSavingThrowsHolderFrame, text="Abilities Data", command=self.ConfigureAbilitiesData, bg=ButtonColor)
                    self.AbilitiesDataConfigButton.grid(row=7, column=0, columnspan=6, padx=2, pady=2)

                    # Abilities Notes
                    self.AbilitiesNotesFrame = LabelFrame(self.AbilitiesAndSavingThrowsHolderFrame, text="Abilities Notes:")
                    self.AbilitiesNotesFrame.grid(row=8, column=0, columnspan=6, padx=2, pady=2)
                    self.AbilitiesNotes = ScrolledTextPixelDim(self.AbilitiesNotesFrame, width=260, height=247, wrap=WORD)
                    self.AbilitiesNotes.pack()

                def ValidStatsEntry(self):
                    try:
                        StrengthBaseValue = GetStringVarAsInt(self.StrengthEntry.AbilityEntryTotalVar)
                        DexterityBaseValue = GetStringVarAsInt(self.DexterityEntry.AbilityEntryTotalVar)
                        ConstitutionBaseValue = GetStringVarAsInt(self.ConstitutionEntry.AbilityEntryTotalVar)
                        IntelligenceBaseValue = GetStringVarAsInt(self.IntelligenceEntry.AbilityEntryTotalVar)
                        WisdomBaseValue = GetStringVarAsInt(self.WisdomEntry.AbilityEntryTotalVar)
                        CharismaBaseValue = GetStringVarAsInt(self.CharismaEntry.AbilityEntryTotalVar)
                    except:
                        messagebox.showerror("Invalid Entry", "Character abilities must be integers.")
                        return False
                    if StrengthBaseValue <= 0 or DexterityBaseValue <= 0 or ConstitutionBaseValue <= 0 or IntelligenceBaseValue <= 0 or WisdomBaseValue <= 0 or CharismaBaseValue <= 0:
                        messagebox.showerror("Invalid Entry", "Character abilities must be greater than 0.")
                        return False
                    return True

                def ConfigureAbilitiesData(self):
                    # Create Window and Wait
                    AbilitiesDataConfigInst = self.AbilitiesDataConfig(root)
                    root.wait_window(AbilitiesDataConfigInst.Window)

                    # Check Whether Data Submitted
                    if AbilitiesDataConfigInst.DataSubmitted.get():
                        # Store Data
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
                        self.AbilityNameVar = StringVar(value=AbilityName)
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
                        self.AbilityLabel.grid(row=Row, column=0, sticky=NSEW)

                        # Total Entry
                        self.AbilityEntryTotal = Entry(master, width=3, justify=CENTER, textvariable=self.AbilityEntryTotalVar, state=DISABLED, disabledbackground="light gray", disabledforeground="black", cursor="arrow")
                        self.AbilityEntryTotal.grid(row=Row, column=1, sticky=NSEW)

                        # Modifier Entry
                        self.AbilityEntryModifier = Entry(master, width=3, justify=CENTER, textvariable=self.AbilityEntryModifierVar, state=DISABLED, disabledbackground=ButtonColor, disabledforeground="black", cursor="dotbox")
                        self.AbilityEntryModifier.grid(row=Row, column=2, sticky=NSEW)
                        self.AbilityEntryModifier.bind("<Button-1>", self.RollAbility)

                        # Saving Throw Proficiency Box
                        self.AbilitySavingThrowProficiencyBox = Checkbutton(master, variable=self.AbilitySavingThrowProficiencyBoxVar)
                        self.AbilitySavingThrowProficiencyBox.grid(row=Row, column=4)

                        # Saving Throw Modifier Entry
                        self.AbilitySavingThrowModifier = Entry(master, width=3, justify=CENTER, textvariable=self.AbilitySavingThrowModifierVar, state=DISABLED, disabledbackground=ButtonColor, disabledforeground="black",
                                                                cursor="dotbox")
                        self.AbilitySavingThrowModifier.grid(row=Row, column=5, sticky=NSEW)
                        self.AbilitySavingThrowModifier.bind("<Button-1>", self.RollSavingThrow)

                    def ConfigureTooltipBindings(self):
                        self.AbilityEntryModifier.bind("<Enter>", self.ToolbarAbilityRollTooltipSet)
                        self.AbilityEntryModifier.bind("<Leave>", ToolbarAndStatusBarInst.ToolbarRevertToPrevious)
                        self.AbilitySavingThrowModifier.bind("<Enter>", self.ToolbarAbilityRollTooltipSet)
                        self.AbilitySavingThrowModifier.bind("<Leave>", ToolbarAndStatusBarInst.ToolbarRevertToPrevious)

                    def ToolbarAbilityRollTooltipSet(self, event):
                        ToolbarAndStatusBarInst.StatusBarPreviousTextVar.set(ToolbarAndStatusBarInst.StatusBarTextVar.get())
                        ToolbarAndStatusBarInst.StatusBarTextVar.set("Click on an ability or saving throw modifier to roll 1d20 with it.")

                    def CalculateModifiers(self, ProficiencyBonus):
                        AbilityModifier = int(math.floor((int(self.AbilityEntryTotalVar.get()) - 10) / 2))
                        AbilityModifierSign = ""
                        if AbilityModifier >= 1:
                            AbilityModifierSign = "+"
                        AbilityModifierString = AbilityModifierSign + str(AbilityModifier)
                        SavingThrowModifier = AbilityModifier
                        if self.AbilitySavingThrowProficiencyBoxVar.get():
                            SavingThrowModifier += ProficiencyBonus
                        SavingThrowSign = ""
                        if SavingThrowModifier >= 1:
                            SavingThrowSign = "+"
                        SavingThrowModifierString = SavingThrowSign + str(SavingThrowModifier)
                        self.AbilityEntryModifierVar.set(AbilityModifierString)
                        self.AbilitySavingThrowModifierVar.set(SavingThrowModifierString)

                    def RollAbility(self, event):
                        StatsAndDiceRollerFrameInst.DiceRollerInst.DiceNumberEntryVar.set(1)
                        StatsAndDiceRollerFrameInst.DiceRollerInst.DieTypeEntryVar.set(20)
                        StatsAndDiceRollerFrameInst.DiceRollerInst.ModifierEntryVar.set(str(GetStringVarAsInt(self.AbilityEntryModifierVar)))
                        StatsAndDiceRollerFrameInst.DiceRollerInst.Roll(self.AbilityNameVar.get() + " Ability Check:\n")

                    def RollSavingThrow(self, event):
                        StatsAndDiceRollerFrameInst.DiceRollerInst.DiceNumberEntryVar.set(1)
                        StatsAndDiceRollerFrameInst.DiceRollerInst.DieTypeEntryVar.set(20)
                        StatsAndDiceRollerFrameInst.DiceRollerInst.ModifierEntryVar.set(str(GetStringVarAsInt(self.AbilitySavingThrowModifierVar)))
                        StatsAndDiceRollerFrameInst.DiceRollerInst.Roll(self.AbilityNameVar.get() + " Saving Throw:\n")

                class AbilitiesDataConfig:
                    def __init__(self, master):
                        self.DataSubmitted = BooleanVar()
                        self.PointBuyBoxVar = BooleanVar(value=StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.PointBuyBoxVar.get())
                        self.PointBuyEntryVar = StringVar()

                        # Create Window
                        self.Window = Toplevel(master)
                        self.Window.wm_attributes("-toolwindow", 1)
                        self.Window.wm_title("Abilities Data")

                        # Table Frame
                        self.TableFrame = Frame(self.Window)
                        self.TableFrame.grid(row=0, column=0, columnspan=2)

                        # Labels
                        self.HeaderLabelAbility = Label(self.TableFrame, text="Ability", bd=2, relief=GROOVE)
                        self.HeaderLabelAbility.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
                        self.HeaderLabelBase = Label(self.TableFrame, text="Base", bd=2, relief=GROOVE)
                        self.HeaderLabelBase.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
                        self.HeaderLabelRacial = Label(self.TableFrame, text="Racial", bd=2, relief=GROOVE)
                        self.HeaderLabelRacial.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
                        self.HeaderLabelASI = Label(self.TableFrame, text="ASI", bd=2, relief=GROOVE)
                        self.HeaderLabelASI.grid(row=0, column=3, sticky=NSEW, padx=2, pady=2)
                        self.HeaderLabelMisc = Label(self.TableFrame, text="Misc.", bd=2, relief=GROOVE)
                        self.HeaderLabelMisc.grid(row=0, column=4, sticky=NSEW, padx=2, pady=2)
                        self.HeaderLabelOverride = Label(self.TableFrame, text="Override", bd=2, relief=GROOVE)
                        self.HeaderLabelOverride.grid(row=0, column=5, sticky=NSEW, padx=2, pady=2)
                        self.HeaderLabelTotal = Label(self.TableFrame, text="Total", bd=2, relief=GROOVE)
                        self.HeaderLabelTotal.grid(row=0, column=6, sticky=NSEW, padx=2, pady=2)

                        # Entries List
                        self.EntriesList = []

                        # Entries
                        self.StrengthConfigEntry = self.AbilitiesDataConfigEntry(self.TableFrame, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.StrengthEntry,
                                                                                 self.EntriesList, 1)
                        self.DexterityConfigEntry = self.AbilitiesDataConfigEntry(self.TableFrame, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.DexterityEntry,
                                                                                  self.EntriesList, 2)
                        self.ConstitutionConfigEntry = self.AbilitiesDataConfigEntry(self.TableFrame,
                                                                                     StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.ConstitutionEntry,
                                                                                     self.EntriesList, 3)
                        self.IntelligenceConfigEntry = self.AbilitiesDataConfigEntry(self.TableFrame,
                                                                                     StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.IntelligenceEntry,
                                                                                     self.EntriesList, 4)
                        self.WisdomConfigEntry = self.AbilitiesDataConfigEntry(self.TableFrame, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.WisdomEntry,
                                                                               self.EntriesList, 5)
                        self.CharismaConfigEntry = self.AbilitiesDataConfigEntry(self.TableFrame, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.CharismaEntry,
                                                                                 self.EntriesList, 6)

                        # Point Buy
                        self.PointBuyBox = Checkbutton(self.TableFrame, text="Using\nPoint\nBuy", variable=self.PointBuyBoxVar)
                        self.PointBuyBox.grid(row=2, column=7, rowspan=3, padx=2, pady=2, sticky=NSEW)
                        self.PointBuyLabel = Label(self.TableFrame, text="Points", bd=2, relief=GROOVE)
                        self.PointBuyLabel.grid(row=5, column=7, padx=2, pady=2, sticky=NSEW)
                        self.PointBuyEntry = Entry(self.TableFrame, state=DISABLED, width=3, disabledbackground="light gray", disabledforeground="black", cursor="arrow", textvariable=self.PointBuyEntryVar, justify=CENTER)
                        self.PointBuyEntry.grid(row=6, column=7, padx=2, pady=2, sticky=NSEW)

                        # Buttons
                        self.CalculateButton = Button(self.TableFrame, text="Calculate", command=self.Calculate, bg=ButtonColor)
                        self.CalculateButton.grid(row=0, column=7, rowspan=2, padx=2, pady=2, sticky=NSEW)
                        self.SubmitButton = Button(self.Window, text="Submit", command=self.Submit, bg=ButtonColor)
                        self.SubmitButton.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)
                        self.CancelButton = Button(self.Window, text="Cancel", command=self.Cancel, bg=ButtonColor)
                        self.CancelButton.grid(row=1, column=1, padx=2, pady=2, sticky=NSEW)

                        # Prevent Main Window Input
                        self.Window.grab_set()

                        # Handle Config Window Geometry and Focus
                        WindowGeometry(self.Window, True)
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
                            if (self.PointBuyBoxVar.get() and GetStringVarAsInt(self.PointBuyEntryVar) >= 0) or not self.PointBuyBoxVar.get():
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
                            self.DataSubmitted.set(True)
                            self.Window.destroy()

                    def Cancel(self):
                        self.DataSubmitted.set(False)
                        self.Window.destroy()

                    class AbilitiesDataConfigEntry:
                        def __init__(self, master, AbilityEntry, List, Row):
                            self.AbilityEntry = AbilityEntry
                            self.AbilityNameVar = StringVar(value=self.AbilityEntry.AbilityNameVar.get())
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
                            self.AbilityEntryBase = Entry(master, width=3, justify=CENTER, textvariable=self.AbilityBaseVar)
                            self.AbilityEntryBase.grid(row=Row, column=1, sticky=NSEW, padx=2, pady=2)

                            # Racial Entry
                            self.AbilityEntryRacial = Entry(master, width=3, justify=CENTER, textvariable=self.AbilityRacialVar)
                            self.AbilityEntryRacial.grid(row=Row, column=2, sticky=NSEW, padx=2, pady=2)

                            # ASI Entry
                            self.AbilityEntryASI = Entry(master, width=3, justify=CENTER, textvariable=self.AbilityASIVar)
                            self.AbilityEntryASI.grid(row=Row, column=3, sticky=NSEW, padx=2, pady=2)

                            # Misc. Entry
                            self.AbilityEntryMisc = Entry(master, width=3, justify=CENTER, textvariable=self.AbilityMiscVar)
                            self.AbilityEntryMisc.grid(row=Row, column=4, sticky=NSEW, padx=2, pady=2)

                            # Override Entry
                            self.AbilityEntryOverride = Entry(master, width=3, justify=CENTER, textvariable=self.AbilityOverrideVar)
                            self.AbilityEntryOverride.grid(row=Row, column=5, sticky=NSEW, padx=2, pady=2)

                            # Total Entry
                            self.AbilityEntryTotal = Entry(master, width=3, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow", textvariable=self.AbilityTotalVar)
                            self.AbilityEntryTotal.grid(row=Row, column=6, sticky=NSEW, padx=2, pady=2)

                        def Calculate(self):
                            Base = GetStringVarAsInt(self.AbilityBaseVar)
                            Racial = GetStringVarAsInt(self.AbilityRacialVar)
                            ASI = GetStringVarAsInt(self.AbilityASIVar)
                            Misc = GetStringVarAsInt(self.AbilityMiscVar)
                            Override = GetStringVarAsInt(self.AbilityOverrideVar)
                            if Override > 0:
                                Total = Override
                            else:
                                Total = Base + Racial + ASI + Misc
                            self.AbilityTotalVar.set(Total)

                        def PointBuyValue(self):
                            Base = GetStringVarAsInt(self.AbilityBaseVar)
                            Value = Base - 8
                            if Base >= 14:
                                Value += 1
                            if Base >= 15:
                                Value += 1
                            return Value

                        def ValidStatsEntries(self):
                            try:
                                Base = GetStringVarAsInt(self.AbilityBaseVar)
                                Racial = GetStringVarAsInt(self.AbilityRacialVar)
                                ASI = GetStringVarAsInt(self.AbilityASIVar)
                                Misc = GetStringVarAsInt(self.AbilityMiscVar)
                                Override = GetStringVarAsInt(self.AbilityOverrideVar)
                            except:
                                messagebox.showerror("Invalid Entry", "Ability score data must be integers.")
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
                            Base = GetStringVarAsInt(self.AbilityBaseVar)
                            Valid = True
                            if Base < 8 or Base > 15:
                                Valid = False
                            return Valid

            # Skills
            class SkillsTable:
                def __init__(self, master):
                    # Skills Holder Frame
                    self.SkillsHolderFrame = Frame(master)
                    self.SkillsHolderFrame.pack()

                    # Labels
                    self.SkillsHeaderProficiency = Label(self.SkillsHolderFrame, text="Prof.", bd=2, relief=GROOVE)
                    self.SkillsHeaderProficiency.grid(row=0, column=0, sticky=NSEW)
                    self.SkillsHeaderSkills = Label(self.SkillsHolderFrame, text="Skill", bd=2, relief=GROOVE)
                    self.SkillsHeaderSkills.grid(row=0, column=1, sticky=NSEW)
                    self.SkillsHeaderModifier = Label(self.SkillsHolderFrame, text="Modifier", bd=2, relief=GROOVE)
                    self.SkillsHeaderModifier.grid(row=0, column=2, sticky=NSEW)

                    # Entries List
                    self.SkillsEntriesList = []

                    # Entries
                    self.SkillsEntryAcrobaticsInst = self.SkillsEntry(self.SkillsHolderFrame, "Acrobatics (DEX)", self.SkillsEntriesList, 1)
                    self.SkillsEntryAnimalHandlingInst = self.SkillsEntry(self.SkillsHolderFrame, "Animal Handling (WIS)", self.SkillsEntriesList, 2)
                    self.SkillsEntryArcanaInst = self.SkillsEntry(self.SkillsHolderFrame, "Arcana (INT)", self.SkillsEntriesList, 3)
                    self.SkillsEntryAthleticsInst = self.SkillsEntry(self.SkillsHolderFrame, "Athletics (STR)", self.SkillsEntriesList, 4)
                    self.SkillsEntryDeceptionInst = self.SkillsEntry(self.SkillsHolderFrame, "Deception (CHA)", self.SkillsEntriesList, 5)
                    self.SkillsEntryHistoryInst = self.SkillsEntry(self.SkillsHolderFrame, "History (INT)", self.SkillsEntriesList, 6)
                    self.SkillsEntryInsightInst = self.SkillsEntry(self.SkillsHolderFrame, "Insight (WIS)", self.SkillsEntriesList, 7)
                    self.SkillsEntryIntimidationInst = self.SkillsEntry(self.SkillsHolderFrame, "Intimidation (CHA)", self.SkillsEntriesList, 8)
                    self.SkillsEntryInvestigationInst = self.SkillsEntry(self.SkillsHolderFrame, "Investigation (INT)", self.SkillsEntriesList, 9)
                    self.SkillsEntryMedicineInst = self.SkillsEntry(self.SkillsHolderFrame, "Medicine (WIS)", self.SkillsEntriesList, 10)
                    self.SkillsEntryNatureInst = self.SkillsEntry(self.SkillsHolderFrame, "Nature (INT)", self.SkillsEntriesList, 11)
                    self.SkillsEntryPerceptionInst = self.SkillsEntry(self.SkillsHolderFrame, "Perception (WIS)", self.SkillsEntriesList, 12)
                    self.SkillsEntryPerformanceInst = self.SkillsEntry(self.SkillsHolderFrame, "Performance (CHA)", self.SkillsEntriesList, 13)
                    self.SkillsEntryPersuasionInst = self.SkillsEntry(self.SkillsHolderFrame, "Persuasion (CHA)", self.SkillsEntriesList, 14)
                    self.SkillsEntryReligionInst = self.SkillsEntry(self.SkillsHolderFrame, "Religion (INT)", self.SkillsEntriesList, 15)
                    self.SkillsEntrySleightOfHandInst = self.SkillsEntry(self.SkillsHolderFrame, "Sleight of Hand (DEX)", self.SkillsEntriesList, 16)
                    self.SkillsEntryStealthInst = self.SkillsEntry(self.SkillsHolderFrame, "Stealth (DEX)", self.SkillsEntriesList, 17)
                    self.SkillsEntrySurvivalInst = self.SkillsEntry(self.SkillsHolderFrame, "Survival (WIS)", self.SkillsEntriesList, 18)

                class SkillsEntry:
                    def __init__(self, master, SkillName, List, Row):
                        self.ProficiencyBox1Var = BooleanVar()
                        self.ProficiencyBox2Var = BooleanVar()
                        self.SkillNameVar = StringVar(value=SkillName)
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
                        self.ModifierEntry = Entry(master, textvariable=self.TotalModifierVar, width=3, disabledforeground="black", disabledbackground=ButtonColor, state=DISABLED, justify=CENTER, cursor="dotbox")
                        self.ModifierEntry.grid(row=Row, column=2, sticky=NSEW)
                        self.ModifierEntry.bind("<Button-1>", self.RollSkill)

                    def ToolbarSkillRollTooltipSet(self, event):
                        ToolbarAndStatusBarInst.StatusBarPreviousTextVar.set(ToolbarAndStatusBarInst.StatusBarTextVar.get())
                        ToolbarAndStatusBarInst.StatusBarTextVar.set("Click on a skill modifier to roll 1d20 with it.")

                    def ConfigureTooltipBindings(self):
                        self.ModifierEntry.bind("<Enter>", self.ToolbarSkillRollTooltipSet)
                        self.ModifierEntry.bind("<Leave>", ToolbarAndStatusBarInst.ToolbarRevertToPrevious)

                    def CalculateSkillModifier(self, Ability, ProficiencyBonus):
                        Modifier = 0
                        if self.ProficiencyBox1Var.get():
                            Modifier += ProficiencyBonus
                        if self.ProficiencyBox2Var.get():
                            Modifier += ProficiencyBonus
                        Modifier += int(Ability)
                        ModifierSign = ""
                        if Modifier >= 1:
                            ModifierSign = "+"
                        self.TotalModifierVar.set(ModifierSign + str(Modifier))

                    def RollSkill(self, event):
                        StatsAndDiceRollerFrameInst.DiceRollerInst.DiceNumberEntryVar.set(1)
                        StatsAndDiceRollerFrameInst.DiceRollerInst.DieTypeEntryVar.set(20)
                        StatsAndDiceRollerFrameInst.DiceRollerInst.ModifierEntryVar.set(str(GetStringVarAsInt(self.TotalModifierVar)))
                        StatsAndDiceRollerFrameInst.DiceRollerInst.Roll(self.SkillNameVar.get() + " Check:\n")

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
                self.ACBaseEntryVar = StringVar()
                self.ACModifierVar = StringVar()
                self.ACManualBonusEntryVar = StringVar()
                self.InitiativeEntryVar = StringVar()
                self.SpeedEntryVar = StringVar()
                self.InitiativeManualBonusEntryVar = StringVar()

                # Center Rows
                master.grid_rowconfigure(0, weight=1)
                master.grid_rowconfigure(2, weight=1)
                master.grid_rowconfigure(4, weight=1)
                master.grid_rowconfigure(6, weight=1)
                master.grid_rowconfigure(8, weight=1)
                master.grid_columnconfigure(0, weight=1)
                master.grid_columnconfigure(2, weight=1)
                master.grid_columnconfigure(4, weight=1)

                # Vitality Frame
                self.VitalityFrame = LabelFrame(master, text="Vitality:")
                self.VitalityFrame.grid(row=1, column=1, padx=2, pady=2)

                # Temp HP
                self.TempHPLabel = Label(self.VitalityFrame, text="Temp HP", bd=2, relief=GROOVE)
                self.TempHPLabel.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
                self.TempHPEntry = Entry(self.VitalityFrame, width=5, justify=CENTER, textvariable=self.TempHPEntryVar)
                self.TempHPEntry.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)

                # Current HP
                self.CurrentHPLabel = Label(self.VitalityFrame, text="Current HP", bd=2, relief=GROOVE)
                self.CurrentHPLabel.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
                self.CurrentHPEntry = Entry(self.VitalityFrame, width=5, justify=CENTER, textvariable=self.CurrentHPEntryVar)
                self.CurrentHPEntry.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)

                # Max HP
                self.MaxHPLabel = Label(self.VitalityFrame, text="Max HP", bd=2, relief=GROOVE)
                self.MaxHPLabel.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)
                self.MaxHPEntry = Entry(self.VitalityFrame, width=5, justify=CENTER, textvariable=self.MaxHPEntryVar)
                self.MaxHPEntry.grid(row=2, column=1, sticky=NSEW, padx=2, pady=2)

                # Hit Dice
                self.HitDiceLabel = Label(self.VitalityFrame, text="Hit Dice", bd=2, relief=GROOVE)
                self.HitDiceLabel.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
                self.HitDiceEntry = Entry(self.VitalityFrame, width=12, justify=CENTER, textvariable=self.HitDiceEntryVar)
                self.HitDiceEntry.grid(row=0, column=3, sticky=NSEW, padx=2, pady=2)
                self.HitDiceRemainingLabel = Label(self.VitalityFrame, text="Remaining", bd=2, relief=GROOVE)
                self.HitDiceRemainingLabel.grid(row=1, column=2, sticky=NSEW, padx=2, pady=2)
                self.HitDiceRemainingEntry = Entry(self.VitalityFrame, width=12, justify=CENTER, textvariable=self.HitDiceRemainingEntryVar)
                self.HitDiceRemainingEntry.grid(row=1, column=3, sticky=NSEW, padx=2, pady=2)

                # Damage Button
                self.DamageButton = Button(self.VitalityFrame, text="Damage", bg=ButtonColor, command=self.Damage)
                self.DamageButton.grid(row=3, column=0, columnspan=2, sticky=NSEW, padx=2, pady=2)

                # Heal Button
                self.HealButton = Button(self.VitalityFrame, text="Heal", bg=ButtonColor, command=self.Heal)
                self.HealButton.grid(row=4, column=0, columnspan=2, sticky=NSEW, padx=2, pady=2)

                # Death Saves
                self.DeathSavingThrowsFrame = LabelFrame(self.VitalityFrame, text="Death Saving Throws:")
                self.DeathSavingThrowsFrame.grid(row=2, column=2, columnspan=2, rowspan=3, sticky=NS, padx=2, pady=2)
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

                # AC, Initiative, and Speed Frame
                self.ACInitiativeSpeedFrame = Frame(master)
                self.ACInitiativeSpeedFrame.grid(row=3, column=1)

                # AC
                self.ACFrame = LabelFrame(self.ACInitiativeSpeedFrame, text="AC:")
                self.ACFrame.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
                self.ACEntry = Entry(self.ACFrame, width=9, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground=ButtonColor, textvariable=self.ACEntryVar, cursor="arrow")
                self.ACEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
                self.ACEntry.bind("<Button-3>", self.ConfigureAC)

                # Initiative
                self.InitiativeFrame = LabelFrame(self.ACInitiativeSpeedFrame, text="Initiative:")
                self.InitiativeFrame.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
                self.InitiativeEntry = Entry(self.InitiativeFrame, width=9, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground=ButtonColor, textvariable=self.InitiativeEntryVar, cursor="dotbox")
                self.InitiativeEntry.bind("<Button-1>", self.RollInitiative)
                self.InitiativeEntry.bind("<Button-3>", self.ConfigureInitiative)
                self.InitiativeEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                # Speed
                self.SpeedFrame = LabelFrame(self.ACInitiativeSpeedFrame, text="Speed:")
                self.SpeedFrame.grid(row=0, column=2, sticky=N, padx=2, pady=2)
                self.SpeedEntry = Entry(self.SpeedFrame, width=9, justify=CENTER, textvariable=self.SpeedEntryVar)
                self.SpeedEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                # Offense Notes
                self.OffenseNotesFrame = LabelFrame(master, text="Offense Notes:")
                self.OffenseNotesFrame.grid(row=5, column=1, padx=2, pady=2)
                self.OffenseNotes = ScrolledTextPixelDim(self.OffenseNotesFrame, height=120, width=254, wrap=WORD)
                self.OffenseNotes.pack()

                # Defense Notes
                self.DefenseNotesFrame = LabelFrame(master, text="Defense Notes:")
                self.DefenseNotesFrame.grid(row=7, column=1, padx=2, pady=2)
                self.DefenseNotes = ScrolledTextPixelDim(self.DefenseNotesFrame, height=120, width=254, wrap=WORD)
                self.DefenseNotes.pack()

                # Features
                self.FeaturesInst = self.Features(master)

            def Damage(self):
                if self.ValidLifeValues():
                    pass
                else:
                    return
                CurrentTempHP = GetStringVarAsInt(self.TempHPEntryVar)
                CurrentHP = GetStringVarAsInt(self.CurrentHPEntryVar)
                Damage = simpledialog.askinteger("Damage", "How much damage?", parent=root, minvalue=1)
                if Damage == None:
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
                CurrentHP = GetStringVarAsInt(self.CurrentHPEntryVar)
                MaxHP = GetStringVarAsInt(self.MaxHPEntryVar)
                Healing = simpledialog.askinteger("Heal", "How much healing?", parent=root, minvalue=1)
                if Healing == None:
                    return
                HealedValue = Healing + max(CurrentHP, 0)
                if HealedValue > MaxHP:
                    self.CurrentHPEntryVar.set(str(MaxHP))
                elif HealedValue <= MaxHP:
                    self.CurrentHPEntryVar.set(str(HealedValue))

            def ValidLifeValues(self):
                try:
                    TempHP = GetStringVarAsInt(self.TempHPEntryVar)
                    CurrentHP = GetStringVarAsInt(self.CurrentHPEntryVar)
                    MaxHP = GetStringVarAsInt(self.MaxHPEntryVar)
                except:
                    messagebox.showerror("Invalid Entry", "HP values must be whole numbers.")
                    return False
                if TempHP < 0 or MaxHP < 1:
                    messagebox.showerror("Invalid Entry", "Temp HP cannot be negative and max HP must be positive.")
                    return False
                return True

            def ConfigureAC(self, event):
                # Test Level Input Validity
                if CharacterSheetHeaderInst.ValidLevelEntry():
                    pass
                else:
                    return

                # Test Ability Input Validity
                if StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.ValidStatsEntry():
                    pass
                else:
                    return

                # Create Config Window and Wait
                ACConfigInst = self.ACConfig(root, self.ACBaseEntryVar, self.ACModifierVar, self.ACManualBonusEntryVar)
                root.wait_window(ACConfigInst.Window)

                # Handle Values
                if ACConfigInst.DataSubmitted.get():
                    self.ACBaseEntryVar.set(ACConfigInst.BaseEntryVar.get())
                    self.ACModifierVar.set(ACConfigInst.ModifierVar.get())
                    self.ACManualBonusEntryVar.set(ACConfigInst.ManualBonusEntryVar.get())

                # Update Stats and Inventory
                UpdateStatsAndInventory()

            def ConfigureInitiative(self, event):
                # Test Level Input Validity
                if CharacterSheetHeaderInst.ValidLevelEntry():
                    pass
                else:
                    return

                # Test Ability Input Validity
                if StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.ValidStatsEntry():
                    pass
                else:
                    return

                # Create Config Window and Wait
                InitiativeConfigInst = self.InitiativeConfig(root, self.InitiativeManualBonusEntryVar)
                root.wait_window(InitiativeConfigInst.Window)

                # Handle Values
                if InitiativeConfigInst.DataSubmitted.get():
                    self.InitiativeManualBonusEntryVar.set(InitiativeConfigInst.ManualBonusEntryVar.get())

                # Update Stats and Inventory
                UpdateStatsAndInventory()

            def RollInitiative(self, event):
                StatsAndDiceRollerFrameInst.DiceRollerInst.DiceNumberEntryVar.set(1)
                StatsAndDiceRollerFrameInst.DiceRollerInst.DieTypeEntryVar.set(20)
                StatsAndDiceRollerFrameInst.DiceRollerInst.ModifierEntryVar.set(str(GetStringVarAsInt(self.InitiativeEntryVar)))
                StatsAndDiceRollerFrameInst.DiceRollerInst.Roll("Initiative:\n")

            def InitiativeEntryTooltipSet(self, event):
                ToolbarAndStatusBarInst.StatusBarPreviousTextVar.set(ToolbarAndStatusBarInst.StatusBarTextVar.get())
                ToolbarAndStatusBarInst.StatusBarTextVar.set("Left-click on the initiative modifier to roll 1d20 with it.  Right-click to set a bonus.")

            def ACEntryTooltipSet(self, event):
                ToolbarAndStatusBarInst.StatusBarPreviousTextVar.set(ToolbarAndStatusBarInst.StatusBarTextVar.get())
                ToolbarAndStatusBarInst.StatusBarTextVar.set("Right-click on AC to set data.")

            class Features:
                def __init__(self, master):
                    # Features Frame
                    self.FeaturesFrame = LabelFrame(master, text="Features:")
                    self.FeaturesFrame.grid(row=1, column=3, rowspan=7, sticky=NSEW, padx=2, pady=2)

                    # Features Scrolling Canvas
                    self.FeaturesScrollingCanvas = Canvas(self.FeaturesFrame, highlightthickness=0, height=335, width=288)
                    self.FeaturesScrollingCanvas.grid(row=0, column=0)
                    self.FeaturesScrollbar = Scrollbar(self.FeaturesFrame, orient=VERTICAL, command=self.FeaturesScrollingCanvas.yview)
                    self.FeaturesScrollbar.grid(row=0, column=1, sticky=NS)
                    self.FeaturesCanvasFrame = Frame(self.FeaturesScrollingCanvas)
                    self.FeaturesScrollingCanvas.create_window((0, 0), window=self.FeaturesCanvasFrame, anchor=NW)
                    self.FeaturesScrollingCanvas.config(yscrollcommand=self.FeaturesScrollbar.set)
                    self.FeaturesScrollingCanvas.bind("<Configure>", self.ConfigureFeaturesScrollingCanvas)

                    # Features Entries List
                    self.FeaturesEntriesList = []

                    # Features Entries
                    self.Feature1 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 1)
                    self.Feature2 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 2)
                    self.Feature3 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 3)
                    self.Feature4 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 4)
                    self.Feature5 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 5)
                    self.Feature6 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 6)
                    self.Feature7 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 7)
                    self.Feature8 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 8)
                    self.Feature9 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 9)
                    self.Feature10 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 10)
                    self.Feature11 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 11)
                    self.Feature12 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 12)
                    self.Feature13 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 13)
                    self.Feature14 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 14)
                    self.Feature15 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 15)
                    self.Feature16 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 16)
                    self.Feature17 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 17)
                    self.Feature18 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 18)
                    self.Feature19 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 19)
                    self.Feature20 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 20)
                    self.Feature21 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 21)
                    self.Feature22 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 22)
                    self.Feature23 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 23)
                    self.Feature24 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 24)
                    self.Feature25 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 25)
                    self.Feature26 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 26)
                    self.Feature27 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 27)
                    self.Feature28 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 28)
                    self.Feature29 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 29)
                    self.Feature30 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 30)
                    self.Feature31 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 31)
                    self.Feature32 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 32)
                    self.Feature33 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 33)
                    self.Feature34 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 34)
                    self.Feature35 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 35)
                    self.Feature36 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 36)
                    self.Feature37 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 37)
                    self.Feature38 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 38)
                    self.Feature39 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 39)
                    self.Feature40 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 40)
                    self.Feature41 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 41)
                    self.Feature42 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 42)
                    self.Feature43 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 43)
                    self.Feature44 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 44)
                    self.Feature45 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 45)
                    self.Feature46 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 46)
                    self.Feature47 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 47)
                    self.Feature48 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 48)
                    self.Feature49 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 49)
                    self.Feature50 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 50)
                    self.Feature51 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 51)
                    self.Feature52 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 52)
                    self.Feature53 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 53)
                    self.Feature54 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 54)
                    self.Feature55 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 55)
                    self.Feature56 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 56)
                    self.Feature57 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 57)
                    self.Feature58 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 58)
                    self.Feature59 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 59)
                    self.Feature60 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 60)
                    self.Feature61 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 61)
                    self.Feature62 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 62)
                    self.Feature63 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 63)
                    self.Feature64 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 64)
                    self.Feature65 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 65)
                    self.Feature66 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 66)
                    self.Feature67 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 67)
                    self.Feature68 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 68)
                    self.Feature69 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 69)
                    self.Feature70 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 70)
                    self.Feature71 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 71)
                    self.Feature72 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 72)
                    self.Feature73 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 73)
                    self.Feature74 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 74)
                    self.Feature75 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 75)
                    self.Feature76 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 76)
                    self.Feature77 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 77)
                    self.Feature78 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 78)
                    self.Feature79 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 79)
                    self.Feature80 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 80)
                    self.Feature81 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 81)
                    self.Feature82 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 82)
                    self.Feature83 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 83)
                    self.Feature84 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 84)
                    self.Feature85 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 85)
                    self.Feature86 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 86)
                    self.Feature87 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 87)
                    self.Feature88 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 88)
                    self.Feature89 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 89)
                    self.Feature90 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 90)
                    self.Feature91 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 91)
                    self.Feature92 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 92)
                    self.Feature93 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 93)
                    self.Feature94 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 94)
                    self.Feature95 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 95)
                    self.Feature96 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 96)
                    self.Feature97 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 97)
                    self.Feature98 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 98)
                    self.Feature99 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 99)
                    self.Feature100 = self.FeatureEntry(self.FeaturesCanvasFrame, self.FeaturesEntriesList, 100)

                    # Features Notes
                    self.FeaturesNotesFrame = LabelFrame(self.FeaturesFrame, text="Features Notes:")
                    self.FeaturesNotesFrame.grid(row=1, column=0, columnspan=2, padx=2, pady=2)
                    self.FeaturesNotes = ScrolledTextPixelDim(self.FeaturesNotesFrame, height=120, width=300, wrap=WORD)
                    self.FeaturesNotes.pack()

                def ConfigureFeaturesScrollingCanvas(self, event):
                    self.FeaturesScrollingCanvas.configure(scrollregion=self.FeaturesScrollingCanvas.bbox('all'))

                def BindMouseWheelFeatures(self, event):
                    if OS == "Windows" or OS == "Darwin":
                        root.bind("<MouseWheel>", self.FeaturesMouseWheelEvent)
                    elif OS == "Linux":
                        root.bind("<Button-4>", self.FeaturesMouseWheelEvent)
                        root.bind("<Button-5>", self.FeaturesMouseWheelEvent)

                def FeaturesMouseWheelEvent(self, event):
                    if OS == "Windows" or OS == "Linux":
                        self.FeaturesScrollingCanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                    elif OS == "Darwin":
                        self.FeaturesScrollingCanvas.yview_scroll(int(-1 * event.delta), "units")

                class FeatureEntry:
                    def __init__(self, master, List, Row):
                        self.Row = Row
                        self.NameEntryVar = StringVar()
                        self.DescriptionVar = StringVar()

                        # Add to List
                        List.append(self)

                        # Name Entry
                        self.NameEntry = Entry(master, width=47, justify=CENTER, state=DISABLED, disabledbackground=ButtonColor, disabledforeground="black", textvariable=self.NameEntryVar, cursor="arrow")
                        self.NameEntry.grid(row=self.Row, column=0, sticky=NSEW)
                        self.NameEntry.bind("<Button-3>", self.Set)

                    def Set(self, event):
                        # Create Config Window and Wait
                        FeatureConfigInst = self.FeatureConfig(root, self.NameEntryVar, self.DescriptionVar)
                        root.wait_window(FeatureConfigInst.Window)

                        # Handle Values
                        if FeatureConfigInst.DataSubmitted.get():
                            self.NameEntryVar.set(FeatureConfigInst.NameEntryVar.get())
                            self.DescriptionVar.set(FeatureConfigInst.DescriptionVar.get())

                    def FeatureEntryTooltipSet(self, event):
                        ToolbarAndStatusBarInst.StatusBarPreviousTextVar.set(ToolbarAndStatusBarInst.StatusBarTextVar.get())
                        ToolbarAndStatusBarInst.StatusBarTextVar.set("Right-click on a feature entry to set a name and description.")

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
                            self.NameFrame.grid(row=0, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                            self.NameEntry = Entry(self.NameFrame, justify=CENTER, width=20, textvariable=self.NameEntryVar)
                            self.NameEntry.pack(fill=X, padx=2, pady=2)

                            # Description Field
                            self.DescriptionFrame = LabelFrame(self.Window, text="Description:")
                            self.DescriptionFrame.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                            self.DescriptionField = ScrolledTextPixelDim(self.DescriptionFrame, height=300, width=250, wrap=WORD)
                            self.DescriptionField.pack()
                            self.DescriptionField.Text.insert(1.0, self.DescriptionVar.get())

                            # Submit Button
                            self.SubmitButton = Button(self.Window, text="Submit", command=self.Submit, bg=ButtonColor)
                            self.SubmitButton.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)

                            # Cancel Button
                            self.CancelButton = Button(self.Window, text="Cancel", command=self.Cancel, bg=ButtonColor)
                            self.CancelButton.grid(row=2, column=1, sticky=NSEW, padx=2, pady=2)

                            # Prevent Main Window Input
                            self.Window.grab_set()

                            # Handle Config Window Geometry and Focus
                            WindowGeometry(self.Window, True)
                            self.Window.focus_force()

                        def Submit(self):
                            self.DataSubmitted.set(True)
                            self.DescriptionVar.set(self.DescriptionField.Text.get("1.0", "end-1c"))
                            self.Window.destroy()

                        def Cancel(self):
                            self.DataSubmitted.set(False)
                            self.Window.destroy()

            class ACConfig:
                def __init__(self, master, ACBaseEntryVar, ACModifierVar, ACManualBonusEntryVar):
                    self.DataSubmitted = BooleanVar()
                    self.BaseEntryVar = StringVar(value=ACBaseEntryVar.get())
                    self.ModifierVar = StringVar(value=ACModifierVar.get())
                    self.ManualBonusEntryVar = StringVar(value=ACManualBonusEntryVar.get())

                    # Create Window
                    self.Window = Toplevel(master)
                    self.Window.wm_attributes("-toolwindow", 1)
                    self.Window.wm_title("AC Data")

                    # Table Frame
                    self.TableFrame = Frame(self.Window)
                    self.TableFrame.grid(row=0, column=0, sticky=NSEW, columnspan=2)

                    # Base AC
                    self.BaseHeader = Label(self.TableFrame, text="Base", bd=2, relief=GROOVE)
                    self.BaseHeader.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
                    self.BaseEntry = Entry(self.TableFrame, width=3, textvariable=self.BaseEntryVar, justify=CENTER)
                    self.BaseEntry.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)

                    # AC Modifier
                    self.ModifierHeader = Label(self.TableFrame, text="Modifier", bd=2, relief=GROOVE)
                    self.ModifierHeader.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
                    self.Modifier = ttk.Combobox(self.TableFrame, textvariable=self.ModifierVar, values=("", "Dexterity", "Dexterity (Max 2)"), width=17, state="readonly")
                    self.Modifier.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)

                    # Manual Bonus
                    self.ManualBonusHeader = Label(self.TableFrame, text="Manual Bonus", bd=2, relief=GROOVE)
                    self.ManualBonusHeader.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
                    self.ManualBonusEntry = Entry(self.TableFrame, width=3, textvariable=self.ManualBonusEntryVar, justify=CENTER)
                    self.ManualBonusEntry.grid(row=1, column=2, sticky=NSEW, padx=2, pady=2)

                    # Submit Button
                    self.SubmitButton = Button(self.Window, text="Submit", command=self.Submit, bg=ButtonColor)
                    self.SubmitButton.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)

                    # Cancel Button
                    self.CancelButton = Button(self.Window, text="Cancel", command=self.Cancel, bg=ButtonColor)
                    self.CancelButton.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)

                    # Prevent Main Window Input
                    self.Window.grab_set()

                    # Handle Config Window Geometry and Focus
                    WindowGeometry(self.Window, True)
                    self.Window.focus_force()

                def Submit(self):
                    if self.ValidEntry():
                        self.DataSubmitted.set(True)
                        self.Window.destroy()

                def Cancel(self):
                    self.DataSubmitted.set(False)
                    self.Window.destroy()

                def ValidEntry(self):
                    try:
                        Base = GetStringVarAsInt(self.BaseEntryVar)
                        GetStringVarAsInt(self.ManualBonusEntryVar)
                    except:
                        messagebox.showerror("Invalid Entry", "Base AC and AC manual bonus must be whole numbers.")
                        return False
                    if Base < 1:
                        messagebox.showerror("Invalid Entry", "Base AC cannot be less than 1.")
                        return False
                    return True

            class InitiativeConfig:
                def __init__(self, master, InitiativeManualBonusEntryVar):
                    self.DataSubmitted = BooleanVar()
                    self.ManualBonusEntryVar = StringVar(value=InitiativeManualBonusEntryVar.get())

                    # Create Window
                    self.Window = Toplevel(master)
                    self.Window.wm_attributes("-toolwindow", 1)
                    self.Window.wm_title("Initiative Data")

                    # Table Frame
                    self.TableFrame = Frame(self.Window)
                    self.TableFrame.grid(row=0, column=0, sticky=NSEW, columnspan=2)

                    # Manual Bonus
                    self.ManualBonusHeader = Label(self.TableFrame, text="Manual Bonus", bd=2, relief=GROOVE)
                    self.ManualBonusHeader.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
                    self.ManualBonusEntry = Entry(self.TableFrame, width=20, textvariable=self.ManualBonusEntryVar, justify=CENTER)
                    self.ManualBonusEntry.grid(row=1, column=2, sticky=NSEW, padx=2, pady=2)

                    # Submit Button
                    self.SubmitButton = Button(self.Window, text="Submit", command=self.Submit, bg=ButtonColor)
                    self.SubmitButton.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)

                    # Cancel Button
                    self.CancelButton = Button(self.Window, text="Cancel", command=self.Cancel, bg=ButtonColor)
                    self.CancelButton.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)

                    # Prevent Main Window Input
                    self.Window.grab_set()

                    # Handle Config Window Geometry and Focus
                    WindowGeometry(self.Window, True)
                    self.Window.focus_force()

                def Submit(self):
                    if self.ValidEntry():
                        self.DataSubmitted.set(True)
                        self.Window.destroy()

                def Cancel(self):
                    self.DataSubmitted.set(False)
                    self.Window.destroy()

                def ValidEntry(self):
                    try:
                        GetStringVarAsInt(self.ManualBonusEntryVar)
                    except:
                        messagebox.showerror("Invalid Entry", "Base AC and AC manual bonus must be whole numbers.")
                        return False
                    return True

        # Spells
        class Spells:
            def __init__(self, master):
                pass

        # Inventory
        class Inventory:
            def __init__(self, master):
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

                # Center Widgets
                master.grid_rowconfigure(0, weight=1)
                master.grid_rowconfigure(3, weight=1)
                master.grid_columnconfigure(0, weight=1)
                master.grid_columnconfigure(2, weight=1)

                # Inventory Data Frame
                self.InventoryDataFrame = Frame(master)
                self.InventoryDataFrame.grid(row=1, column=1, sticky=N)

                # Carrying Capacity
                self.CarryingCapacityFrame = LabelFrame(self.InventoryDataFrame, text="Carrying Capacity:")
                self.CarryingCapacityFrame.grid(row=0, column=0, padx=2, pady=2, sticky=NS)
                self.CarryingCapacityFrame.grid_rowconfigure(0, weight=1)
                self.CarryingCapacityFrame.grid_rowconfigure(2, weight=1)
                self.CarryingCapacityFrame.grid_columnconfigure(0, weight=1)
                self.CarryingCapacityFrame.grid_columnconfigure(2, weight=1)
                self.CarryingCapacityEntry = Entry(self.CarryingCapacityFrame, width=15, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.CarryingCapacityVar,
                                                   cursor="arrow")
                self.CarryingCapacityEntry.grid(row=1, column=1, padx=2, pady=2)

                # Clear Inventory Button
                self.ClearInventoryButton = Button(self.InventoryDataFrame, text="Clear Inventory", command=self.ClearInventory, bg=ButtonColor)
                self.ClearInventoryButton.grid(row=1, column=0, padx=2, pady=2)

                # Loads
                self.LoadsFrame = LabelFrame(self.InventoryDataFrame, text="Loads (lbs.):")
                self.LoadsFrame.grid(row=0, column=1, padx=2, pady=2, sticky=NS, rowspan=2)
                self.TotalLoadLabel = Label(self.LoadsFrame, text="Total")
                self.TotalLoadLabel.grid(row=1, column=1, sticky=W)
                self.TotalLoadEntry = Entry(self.LoadsFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.TotalLoadEntryVar, cursor="arrow")
                self.TotalLoadEntry.grid(row=1, column=2, sticky=NSEW)
                self.GearLoadLabel = Label(self.LoadsFrame, text="Gear")
                self.GearLoadLabel.grid(row=3, column=1, sticky=W)
                self.GearLoadEntry = Entry(self.LoadsFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.GearLoadEntryVar, cursor="arrow")
                self.GearLoadEntry.grid(row=3, column=2, sticky=NSEW)
                self.TreasureLoadLabel = Label(self.LoadsFrame, text="Treasure")
                self.TreasureLoadLabel.grid(row=5, column=1, sticky=W)
                self.TreasureLoadEntry = Entry(self.LoadsFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.TreasureLoadEntryVar, cursor="arrow")
                self.TreasureLoadEntry.grid(row=5, column=2, sticky=NSEW)
                self.MiscLoadLabel = Label(self.LoadsFrame, text="Misc")
                self.MiscLoadLabel.grid(row=7, column=1, sticky=W)
                self.MiscLoadEntry = Entry(self.LoadsFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.MiscLoadEntryVar, cursor="arrow")
                self.MiscLoadEntry.grid(row=7, column=2, sticky=NSEW)
                self.LoadsFrame.grid_rowconfigure(0, weight=1)
                self.LoadsFrame.grid_rowconfigure(2, weight=1)
                self.LoadsFrame.grid_rowconfigure(4, weight=1)
                self.LoadsFrame.grid_rowconfigure(6, weight=1)
                self.LoadsFrame.grid_rowconfigure(8, weight=1)
                self.LoadsFrame.grid_columnconfigure(0, weight=1)
                self.LoadsFrame.grid_columnconfigure(3, weight=1)

                # Coins
                self.CoinsFrame = LabelFrame(self.InventoryDataFrame, text="Coins:")
                self.CoinsFrame.grid(row=0, column=2, padx=2, pady=2, sticky=NS, rowspan=2)
                self.CoinsFrame.grid_rowconfigure(0, weight=1)
                self.CoinsFrame.grid_rowconfigure(4, weight=1)
                self.CoinsFrame.grid_columnconfigure(0, weight=1)
                self.CoinsFrame.grid_columnconfigure(2, weight=1)
                self.CoinsInputHolderFrame = Frame(self.CoinsFrame)
                self.CoinsInputHolderFrame.grid(row=1, column=1)
                self.CoinsHeaderCP = Label(self.CoinsInputHolderFrame, text="CP", bd=2, relief=GROOVE)
                self.CoinsHeaderCP.grid(row=0, column=0, sticky=NSEW)
                self.CoinsEntryCP = Entry(self.CoinsInputHolderFrame, width=5, justify=CENTER, textvariable=self.CoinsEntryCPVar)
                self.CoinsEntryCP.grid(row=1, column=0, sticky=NSEW)
                self.CoinsHeaderSP = Label(self.CoinsInputHolderFrame, text="SP", bd=2, relief=GROOVE)
                self.CoinsHeaderSP.grid(row=0, column=1, sticky=NSEW)
                self.CoinsEntrySP = Entry(self.CoinsInputHolderFrame, width=5, justify=CENTER, textvariable=self.CoinsEntrySPVar)
                self.CoinsEntrySP.grid(row=1, column=1, sticky=NSEW)
                self.CoinsHeaderEP = Label(self.CoinsInputHolderFrame, text="EP", bd=2, relief=GROOVE)
                self.CoinsHeaderEP.grid(row=0, column=2, sticky=NSEW)
                self.CoinsEntryEP = Entry(self.CoinsInputHolderFrame, width=5, justify=CENTER, textvariable=self.CoinsEntryEPVar)
                self.CoinsEntryEP.grid(row=1, column=2, sticky=NSEW)
                self.CoinsHeaderGP = Label(self.CoinsInputHolderFrame, text="GP", bd=2, relief=GROOVE)
                self.CoinsHeaderGP.grid(row=0, column=3, sticky=NSEW)
                self.CoinsEntryGP = Entry(self.CoinsInputHolderFrame, width=5, justify=CENTER, textvariable=self.CoinsEntryGPVar)
                self.CoinsEntryGP.grid(row=1, column=3, sticky=NSEW)
                self.CoinsHeaderPP = Label(self.CoinsInputHolderFrame, text="PP", bd=2, relief=GROOVE)
                self.CoinsHeaderPP.grid(row=0, column=4, sticky=NSEW)
                self.CoinsEntryPP = Entry(self.CoinsInputHolderFrame, width=5, justify=CENTER, textvariable=self.CoinsEntryPPVar)
                self.CoinsEntryPP.grid(row=1, column=4, sticky=NSEW)

                # Coin Value and Weight
                self.CoinValueAndWeightHolderFrame = Frame(self.CoinsFrame)
                self.CoinValueAndWeightHolderFrame.grid(row=2, column=1, padx=2, pady=2)
                self.CoinValueHeader = Label(self.CoinValueAndWeightHolderFrame, text="Coin Value\n(gp)", bd=2, relief=GROOVE)
                self.CoinValueHeader.grid(row=0, column=0, sticky=NSEW)
                self.CoinValueEntry = Entry(self.CoinValueAndWeightHolderFrame, width=13, justify=CENTER, textvariable=self.CoinValueEntryVar, state=DISABLED, disabledforeground="black", disabledbackground="light gray",
                                            cursor="arrow")
                self.CoinValueEntry.grid(row=1, column=0, sticky=NSEW)
                self.CoinWeightHeader = Label(self.CoinValueAndWeightHolderFrame, text="Coin Weight\n(lbs.)", bd=2, relief=GROOVE)
                self.CoinWeightHeader.grid(row=0, column=1, sticky=NSEW)
                self.CoinWeightEntry = Entry(self.CoinValueAndWeightHolderFrame, width=13, justify=CENTER, textvariable=self.CoinWeightEntryVar, state=DISABLED, disabledforeground="black", disabledbackground="light gray",
                                             cursor="arrow")
                self.CoinWeightEntry.grid(row=1, column=1, sticky=NSEW)

                # Coin Calculator
                self.CoinCalculatorButton = Button(self.CoinsFrame, text="Coin Calculator", command=self.OpenCoinCalculator, bg=ButtonColor)
                self.CoinCalculatorButton.grid(row=3, column=1, padx=2, pady=2)

                # Values
                self.ValuesFrame = LabelFrame(self.InventoryDataFrame, text="Values (gp):")
                self.ValuesFrame.grid(row=0, column=3, padx=2, pady=2, sticky=NS, rowspan=2)
                self.TotalValueLabel = Label(self.ValuesFrame, text="Total")
                self.TotalValueLabel.grid(row=1, column=1, sticky=W)
                self.TotalValueEntry = Entry(self.ValuesFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.TotalValueEntryVar, cursor="arrow")
                self.TotalValueEntry.grid(row=1, column=2, sticky=NSEW)
                self.GearValueLabel = Label(self.ValuesFrame, text="Gear")
                self.GearValueLabel.grid(row=3, column=1, sticky=W)
                self.GearValueEntry = Entry(self.ValuesFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.GearValueEntryVar, cursor="arrow")
                self.GearValueEntry.grid(row=3, column=2, sticky=NSEW)
                self.TreasureValueLabel = Label(self.ValuesFrame, text="Treasure")
                self.TreasureValueLabel.grid(row=5, column=1, sticky=W)
                self.TreasureValueEntry = Entry(self.ValuesFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.TreasureValueEntryVar, cursor="arrow")
                self.TreasureValueEntry.grid(row=5, column=2, sticky=NSEW)
                self.MiscValueLabel = Label(self.ValuesFrame, text="Misc")
                self.MiscValueLabel.grid(row=7, column=1, sticky=W)
                self.MiscValueEntry = Entry(self.ValuesFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.MiscValueEntryVar, cursor="arrow")
                self.MiscValueEntry.grid(row=7, column=2, sticky=NSEW)
                self.ValuesFrame.grid_rowconfigure(0, weight=1)
                self.ValuesFrame.grid_rowconfigure(2, weight=1)
                self.ValuesFrame.grid_rowconfigure(4, weight=1)
                self.ValuesFrame.grid_rowconfigure(6, weight=1)
                self.ValuesFrame.grid_rowconfigure(8, weight=1)
                self.ValuesFrame.grid_columnconfigure(0, weight=1)
                self.ValuesFrame.grid_columnconfigure(3, weight=1)

                # Inventory List Frame
                self.InventoryListFrame = LabelFrame(master, text="Inventory List:")
                self.InventoryListFrame.grid(row=2, column=1, padx=2, pady=2)

                # Inventory List Scrolling Canvas
                self.InventoryListScrollingCanvas = Canvas(self.InventoryListFrame, highlightthickness=0, height=325, width=568)
                self.InventoryListScrollingCanvas.pack(side=LEFT)
                self.InventoryListScrollbar = Scrollbar(self.InventoryListFrame, orient=VERTICAL, command=self.InventoryListScrollingCanvas.yview)
                self.InventoryListScrollbar.pack(side=RIGHT, fill=Y)
                self.InventoryListCanvasFrame = Frame(self.InventoryListScrollingCanvas)
                self.InventoryListScrollingCanvas.create_window((0, 0), window=self.InventoryListCanvasFrame, anchor=NW)
                self.InventoryListScrollingCanvas.config(yscrollcommand=self.InventoryListScrollbar.set)
                self.InventoryListScrollingCanvas.bind('<Configure>', self.ConfigureInventoryScrollingCanvas)

                # Inventory List Headers
                self.InventoryListNameHeader = Label(self.InventoryListCanvasFrame, text="Name", bd=2, relief=GROOVE)
                self.InventoryListNameHeader.grid(row=0, column=0, sticky=NSEW)
                self.InventoryListCountHeader = Label(self.InventoryListCanvasFrame, text="Count", bd=2, relief=GROOVE)
                self.InventoryListCountHeader.grid(row=0, column=1, sticky=NSEW)
                self.InventoryListUnitWeightHeader = Label(self.InventoryListCanvasFrame, text="Unit Weight\n(lb.)", bd=2, relief=GROOVE)
                self.InventoryListUnitWeightHeader.grid(row=0, column=2, sticky=NSEW)
                self.InventoryListUnitValueHeader = Label(self.InventoryListCanvasFrame, text="Unit Value", bd=2, relief=GROOVE)
                self.InventoryListUnitValueHeader.grid(row=0, column=3, sticky=NSEW)
                self.InventoryListUnitValueDenominationHeader = Label(self.InventoryListCanvasFrame, text="Value\nDenom.", bd=2, relief=GROOVE)
                self.InventoryListUnitValueDenominationHeader.grid(row=0, column=4, sticky=NSEW)
                self.InventoryListTotalWeightHeader = Label(self.InventoryListCanvasFrame, text="Total Weight\n(lb.)", bd=2, relief=GROOVE)
                self.InventoryListTotalWeightHeader.grid(row=0, column=5, sticky=NSEW)
                self.InventoryListTotalValueHeader = Label(self.InventoryListCanvasFrame, text="Total Value\n(gp)", bd=2, relief=GROOVE)
                self.InventoryListTotalValueHeader.grid(row=0, column=6, sticky=NSEW)
                self.InventoryListTagHeader = Label(self.InventoryListCanvasFrame, text="Tag", bd=2, relief=GROOVE)
                self.InventoryListTagHeader.grid(row=0, column=7, sticky=NSEW)

                # Inventory Entries List
                self.InventoryEntriesList = []

                # Inventory Entries
                self.InventoryEntry1 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 1)
                self.InventoryEntry2 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 2)
                self.InventoryEntry3 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 3)
                self.InventoryEntry4 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 4)
                self.InventoryEntry5 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 5)
                self.InventoryEntry6 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 6)
                self.InventoryEntry7 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 7)
                self.InventoryEntry8 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 8)
                self.InventoryEntry9 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 9)
                self.InventoryEntry10 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 10)
                self.InventoryEntry11 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 11)
                self.InventoryEntry12 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 12)
                self.InventoryEntry13 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 13)
                self.InventoryEntry14 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 14)
                self.InventoryEntry15 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 15)
                self.InventoryEntry16 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 16)
                self.InventoryEntry17 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 17)
                self.InventoryEntry18 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 18)
                self.InventoryEntry19 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 19)
                self.InventoryEntry20 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 20)
                self.InventoryEntry21 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 21)
                self.InventoryEntry22 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 22)
                self.InventoryEntry23 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 23)
                self.InventoryEntry24 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 24)
                self.InventoryEntry25 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 25)
                self.InventoryEntry26 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 26)
                self.InventoryEntry27 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 27)
                self.InventoryEntry28 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 28)
                self.InventoryEntry29 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 29)
                self.InventoryEntry30 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 30)
                self.InventoryEntry31 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 31)
                self.InventoryEntry32 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 32)
                self.InventoryEntry33 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 33)
                self.InventoryEntry34 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 34)
                self.InventoryEntry35 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 35)
                self.InventoryEntry36 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 36)
                self.InventoryEntry37 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 37)
                self.InventoryEntry38 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 38)
                self.InventoryEntry39 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 39)
                self.InventoryEntry40 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 40)
                self.InventoryEntry41 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 41)
                self.InventoryEntry42 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 42)
                self.InventoryEntry43 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 43)
                self.InventoryEntry44 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 44)
                self.InventoryEntry45 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 45)
                self.InventoryEntry46 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 46)
                self.InventoryEntry47 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 47)
                self.InventoryEntry48 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 48)
                self.InventoryEntry49 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 49)
                self.InventoryEntry50 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 50)
                self.InventoryEntry51 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 51)
                self.InventoryEntry52 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 52)
                self.InventoryEntry53 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 53)
                self.InventoryEntry54 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 54)
                self.InventoryEntry55 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 55)
                self.InventoryEntry56 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 56)
                self.InventoryEntry57 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 57)
                self.InventoryEntry58 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 58)
                self.InventoryEntry59 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 59)
                self.InventoryEntry60 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 60)
                self.InventoryEntry61 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 61)
                self.InventoryEntry62 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 62)
                self.InventoryEntry63 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 63)
                self.InventoryEntry64 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 64)
                self.InventoryEntry65 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 65)
                self.InventoryEntry66 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 66)
                self.InventoryEntry67 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 67)
                self.InventoryEntry68 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 68)
                self.InventoryEntry69 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 69)
                self.InventoryEntry70 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 70)
                self.InventoryEntry71 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 71)
                self.InventoryEntry72 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 72)
                self.InventoryEntry73 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 73)
                self.InventoryEntry74 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 74)
                self.InventoryEntry75 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 75)
                self.InventoryEntry76 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 76)
                self.InventoryEntry77 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 77)
                self.InventoryEntry78 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 78)
                self.InventoryEntry79 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 79)
                self.InventoryEntry80 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 80)
                self.InventoryEntry81 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 81)
                self.InventoryEntry82 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 82)
                self.InventoryEntry83 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 83)
                self.InventoryEntry84 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 84)
                self.InventoryEntry85 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 85)
                self.InventoryEntry86 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 86)
                self.InventoryEntry87 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 87)
                self.InventoryEntry88 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 88)
                self.InventoryEntry89 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 89)
                self.InventoryEntry90 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 90)
                self.InventoryEntry91 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 91)
                self.InventoryEntry92 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 92)
                self.InventoryEntry93 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 93)
                self.InventoryEntry94 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 94)
                self.InventoryEntry95 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 95)
                self.InventoryEntry96 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 96)
                self.InventoryEntry97 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 97)
                self.InventoryEntry98 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 98)
                self.InventoryEntry99 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 99)
                self.InventoryEntry100 = self.InventoryEntry(self.InventoryListCanvasFrame, self.InventoryEntriesList, 100)

            def ConfigureInventoryScrollingCanvas(self, event):
                self.InventoryListScrollingCanvas.configure(scrollregion=self.InventoryListScrollingCanvas.bbox('all'))

            def Calculate(self):
                # Carrying Capacity
                self.CarryingCapacityVar.set(15 * GetStringVarAsInt(StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.StrengthEntry.AbilityEntryTotalVar))

                # Coin Counts
                CPCount = GetStringVarAsDecimal(self.CoinsEntryCPVar)
                SPCount = GetStringVarAsDecimal(self.CoinsEntrySPVar)
                EPCount = GetStringVarAsDecimal(self.CoinsEntryEPVar)
                GPCount = GetStringVarAsDecimal(self.CoinsEntryGPVar)
                PPCount = GetStringVarAsDecimal(self.CoinsEntryPPVar)
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
                TotalLoad = Decimal(0)
                GearLoad = Decimal(0)
                TreasureLoad = Decimal(0)
                MiscLoad = Decimal(0)
                TotalValue = Decimal(0)
                GearValue = Decimal(0)
                TreasureValue = Decimal(0)
                MiscValue = Decimal(0)

                # Add Coins to Loads and Values
                TotalLoad += CoinWeight
                TreasureLoad += CoinWeight
                TotalValue += CoinValue
                TreasureValue += CoinValue

                # Loop Through Inventory List
                for Entry in self.InventoryEntriesList:
                    # Set Up Local Variables
                    Tag = Entry.CategoryTagVar.get()
                    Count = GetStringVarAsInt(Entry.CountEntryVar)
                    ValueDenomination = Entry.UnitValueDenominationVar.get()

                    # Total Weight and Value
                    TotalItemWeight = GetStringVarAsDecimal(Entry.UnitWeightEntryVar) * Decimal(Count)
                    TotalItemValue = GetStringVarAsDecimal(Entry.UnitValueEntryVar) * Decimal(Count)

                    # Calculate Value in GP
                    if ValueDenomination == "cp":
                        TotalItemValue *= self.ValueCP
                    if ValueDenomination == "sp":
                        TotalItemValue *= self.ValueSP
                    if ValueDenomination == "ep":
                        TotalItemValue *= self.ValueEP
                    if ValueDenomination == "gp":
                        TotalItemValue *= self.ValueGP
                    if ValueDenomination == "pp":
                        TotalItemValue *= self.ValuePP
                    if ValueDenomination == "":
                        TotalItemValue *= 0

                    Entry.TotalWeightEntryVar.set(str(TotalItemWeight.quantize(Decimal("0.01"))))
                    Entry.TotalValueEntryVar.set(str(TotalItemValue.quantize(Decimal("0.01"))))

                    # Totals
                    TotalLoad += TotalItemWeight
                    TotalValue += TotalItemValue

                    # Tags
                    if Tag == "Gear":
                        GearLoad += TotalItemWeight
                        GearValue += TotalItemValue
                    elif Tag == "Treasure":
                        TreasureLoad += TotalItemWeight
                        TreasureValue += TotalItemValue
                    elif Tag == "Misc.":
                        MiscLoad += TotalItemWeight
                        MiscValue += TotalItemValue

                self.TotalLoadEntryVar.set(str(TotalLoad.quantize(Decimal("0.01"))))
                self.GearLoadEntryVar.set(str(GearLoad.quantize(Decimal("0.01"))))
                self.TreasureLoadEntryVar.set(str(TreasureLoad.quantize(Decimal("0.01"))))
                self.MiscLoadEntryVar.set(str(MiscLoad.quantize(Decimal("0.01"))))
                self.TotalValueEntryVar.set(str(TotalValue.quantize(Decimal("0.01"))))
                self.GearValueEntryVar.set(str(GearValue.quantize(Decimal("0.01"))))
                self.TreasureValueEntryVar.set(str(TreasureValue.quantize(Decimal("0.01"))))
                self.MiscValueEntryVar.set(str(MiscValue.quantize(Decimal("0.01"))))

            def ClearInventory(self):
                ClearConfirm = messagebox.askyesno("Clear Inventory", "Are you sure you want to clear the inventory?  This cannot be undone.")
                if not ClearConfirm:
                    return

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

            def ValidInventoryEntry(self):
                try:
                    CPInt = GetStringVarAsInt(self.CoinsEntryCPVar)
                    SPInt = GetStringVarAsInt(self.CoinsEntrySPVar)
                    EPInt = GetStringVarAsInt(self.CoinsEntryEPVar)
                    GPInt = GetStringVarAsInt(self.CoinsEntryGPVar)
                    PPInt = GetStringVarAsInt(self.CoinsEntryPPVar)
                except:
                    messagebox.showerror("Invalid Entry", "Coins must be whole numbers.")
                    return False
                if CPInt < 0 or SPInt < 0 or EPInt < 0 or GPInt < 0 or PPInt < 0:
                    messagebox.showerror("Invalid Entry", "Coins must be positive or 0.")
                    return False
                for Entry in self.InventoryEntriesList:
                    try:
                        CountInt = GetStringVarAsInt(Entry.CountEntryVar)
                        WeightFloat = GetStringVarAsFloat(Entry.UnitWeightEntryVar)
                        ValueFloat = GetStringVarAsFloat(Entry.UnitValueEntryVar)
                    except:
                        messagebox.showerror("Invalid Entry", "Inventory item counts must be whole numbers, and unit weights and values must be numbers.")
                        return False
                    if CountInt < 0 or WeightFloat < 0 or ValueFloat < 0:
                        messagebox.showerror("Invalid Entry", "Inventory item counts, unit weights, and unit values must be positive or 0.")
                        return False
                return True

            def BindMouseWheelInventoryList(self, event):
                if OS == "Windows" or OS == "Darwin":
                    root.bind("<MouseWheel>", self.InventoryListMouseWheelEvent)
                elif OS == "Linux":
                    root.bind("<Button-4>", self.InventoryListMouseWheelEvent)
                    root.bind("<Button-5>", self.InventoryListMouseWheelEvent)

            def InventoryListMouseWheelEvent(self, event):
                if OS == "Windows" or OS == "Linux":
                    self.InventoryListScrollingCanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                elif OS == "Darwin":
                    self.InventoryListScrollingCanvas.yview_scroll(int(-1 * event.delta), "units")

            def OpenCoinCalculator(self):
                # Create Coin Calculator Window and Wait
                self.CoinCalculatorInst = self.CoinCalculator(root, self.ValueCP, self.ValueSP, self.ValueEP, self.ValueGP, self.ValuePP, self.WeightPerCoin)
                root.wait_window(self.CoinCalculatorInst.Window)

            class InventoryEntry:
                def __init__(self, master, List, Row):
                    self.NameEntryVar = StringVar()
                    self.CountEntryVar = StringVar()
                    self.UnitWeightEntryVar = StringVar()
                    self.UnitValueEntryVar = StringVar()
                    self.UnitValueDenominationVar = StringVar()
                    self.TotalWeightEntryVar = StringVar()
                    self.TotalValueEntryVar = StringVar()
                    self.CategoryTagVar = StringVar()
                    self.Row = Row

                    # Add to List
                    List.append(self)

                    # Name Entry
                    self.NameEntry = Entry(master, width=23, textvariable=self.NameEntryVar, justify=CENTER)
                    self.NameEntry.grid(row=self.Row, column=0, sticky=NSEW)

                    # Count Entry
                    self.CountEntry = Entry(master, width=4, textvariable=self.CountEntryVar, justify=CENTER)
                    self.CountEntry.grid(row=self.Row, column=1, sticky=NSEW)

                    # Unit Weight Entry
                    self.UnitWeightEntry = Entry(master, width=4, textvariable=self.UnitWeightEntryVar, justify=CENTER)
                    self.UnitWeightEntry.grid(row=self.Row, column=2, sticky=NSEW)

                    # Unit Value Entry
                    self.UnitValueEntry = Entry(master, width=4, textvariable=self.UnitValueEntryVar, justify=CENTER)
                    self.UnitValueEntry.grid(row=self.Row, column=3, sticky=NSEW)

                    # Unit Value Denomination
                    self.UnitValueDenomination = ttk.Combobox(master, textvariable=self.UnitValueDenominationVar, values=("", "cp", "sp", "ep", "gp", "pp"), width=2, state="readonly")
                    self.UnitValueDenomination.grid(row=self.Row, column=4, sticky=NSEW)

                    # Total Weight Entry
                    self.TotalWeightEntry = Entry(master, width=4, textvariable=self.TotalWeightEntryVar, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow")
                    self.TotalWeightEntry.grid(row=self.Row, column=5, sticky=NSEW)

                    # Total Value Entry
                    self.TotalValueEntry = Entry(master, width=4, textvariable=self.TotalValueEntryVar, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow")
                    self.TotalValueEntry.grid(row=self.Row, column=6, sticky=NSEW)

                    # Category Tag
                    self.CategoryTag = ttk.Combobox(master, textvariable=self.CategoryTagVar, values=("", "Gear", "Treasure", "Misc."), width=8, state="readonly")
                    self.CategoryTag.grid(row=self.Row, column=7, sticky=NSEW)

            class CoinCalculator:
                def __init__(self, master, ValueCP, ValueSP, ValueEP, ValueGP, ValuePP, WeightPerCoin):
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
                    self.ValueCP = ValueCP
                    self.ValueSP = ValueSP
                    self.ValueEP = ValueEP
                    self.ValueGP = ValueGP
                    self.ValuePP = ValuePP
                    self.WeightPerCoin = WeightPerCoin

                    # Create Window
                    self.Window = Toplevel(master)
                    self.Window.wm_attributes("-toolwindow", 1)
                    self.Window.wm_title("Coin Calculator")

                    # Prevent Main Window Input
                    self.Window.grab_set()

                    # Table Frame
                    self.TableFrame = Frame(self.Window)
                    self.TableFrame.grid(row=0, column=0, columnspan=2)

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
                    self.CalculateButton = Button(self.Window, text="Calculate", command=self.Calculate, bg=ButtonColor)
                    self.CalculateButton.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
                    self.CloseButton = Button(self.Window, text="Close", command=self.Close, bg=ButtonColor)
                    self.CloseButton.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)

                    # Handle Config Window Geometry and Focus
                    WindowGeometry(self.Window, True)
                    self.Window.focus_force()

                def ValidEntry(self):
                    try:
                        CPInput = GetStringVarAsInt(self.CPEntryVar)
                        SPInput = GetStringVarAsInt(self.SPEntryVar)
                        EPInput = GetStringVarAsInt(self.EPEntryVar)
                        GPInput = GetStringVarAsInt(self.GPEntryVar)
                        PPInput = GetStringVarAsInt(self.PPEntryVar)
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
                    CPInput = GetStringVarAsDecimal(self.CPEntryVar)
                    SPInput = GetStringVarAsDecimal(self.SPEntryVar)
                    EPInput = GetStringVarAsDecimal(self.EPEntryVar)
                    GPInput = GetStringVarAsDecimal(self.GPEntryVar)
                    PPInput = GetStringVarAsDecimal(self.PPEntryVar)

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

        # Notes
        class Notes:
            def __init__(self, master):
                # Notes Frame
                # self.NotesFrame = Frame(self.NotesPage)
                # self.NotesFrame.pack(padx=2, pady=2, fill=BOTH)

                # Notes Text Box
                self.NotesField = ScrolledTextPixelDim(master, height=485, wrap=WORD)
                self.NotesField.pack(padx=2, pady=2, fill=BOTH)

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
                self.RaceFrame.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)
                self.RaceEntry = Entry(self.RaceFrame, justify=CENTER, textvariable=self.RaceEntryVar, width=22)
                self.RaceEntry.pack(padx=2, pady=2)

                # Background
                self.BackgroundFrame = LabelFrame(self.FirstColumnFrame, text="Background:")
                self.BackgroundFrame.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)
                self.BackgroundEntry = Entry(self.BackgroundFrame, justify=CENTER, textvariable=self.BackgroundEntryVar, width=22)
                self.BackgroundEntry.pack(padx=2, pady=2)

                # Alignment
                self.AlignmentFrame = LabelFrame(self.FirstColumnFrame, text="Alignment:")
                self.AlignmentFrame.grid(row=2, column=0, padx=2, pady=2, sticky=NSEW)
                self.AlignmentEntry = Entry(self.AlignmentFrame, justify=CENTER, textvariable=self.AlignmentEntryVar, width=22)
                self.AlignmentEntry.pack(padx=2, pady=2)

                # Age
                self.AgeFrame = LabelFrame(self.FirstColumnFrame, text="Age:")
                self.AgeFrame.grid(row=3, column=0, padx=2, pady=2, sticky=NSEW)
                self.AgeEntry = Entry(self.AgeFrame, justify=CENTER, textvariable=self.AgeEntryVar, width=22)
                self.AgeEntry.pack(padx=2, pady=2)

                # Physical Appearance
                self.PhysicalAppearanceFrame = LabelFrame(self.FirstColumnFrame, text="Physical Appearance:")
                self.PhysicalAppearanceFrame.grid(row=4, column=0, padx=2, pady=2)
                self.PhysicalAppearanceField = ScrolledTextPixelDim(self.PhysicalAppearanceFrame, width=140, height=289, wrap=WORD)
                self.PhysicalAppearanceField.pack()

                # Second Column
                self.SecondColumnFrame = Frame(master)
                self.SecondColumnFrame.grid(row=1, column=3)

                # Personality Traits
                self.PersonalityTraitsFrame = LabelFrame(self.SecondColumnFrame, text="Personality Traits:")
                self.PersonalityTraitsFrame.grid(row=0, column=0, padx=2, pady=2)
                self.PersonalityTraitsField = ScrolledTextPixelDim(self.PersonalityTraitsFrame, width=140, height=225, wrap=WORD)
                self.PersonalityTraitsField.pack()

                # Bonds
                self.BondsFrame = LabelFrame(self.SecondColumnFrame, text="Bonds:")
                self.BondsFrame.grid(row=1, column=0, padx=2, pady=2)
                self.BondsField = ScrolledTextPixelDim(self.BondsFrame, width=140, height=225, wrap=WORD)
                self.BondsField.pack()

                # Third Column
                self.ThirdColumnFrame = Frame(master)
                self.ThirdColumnFrame.grid(row=1, column=5)

                # Ideals
                self.IdealsFrame = LabelFrame(self.ThirdColumnFrame, text="Ideals:")
                self.IdealsFrame.grid(row=0, column=0, padx=2, pady=2)
                self.IdealsField = ScrolledTextPixelDim(self.IdealsFrame, width=140, height=225, wrap=WORD)
                self.IdealsField.pack()

                # Flaws
                self.FlawsFrame = LabelFrame(self.ThirdColumnFrame, text="Flaws:")
                self.FlawsFrame.grid(row=1, column=0, padx=2, pady=2)
                self.FlawsField = ScrolledTextPixelDim(self.FlawsFrame, width=140, height=225, wrap=WORD)
                self.FlawsField.pack()

                # Fourth Column
                self.FourthColumnFrame = Frame(master)
                self.FourthColumnFrame.grid(row=1, column=7)

                # Backstory
                self.BackstoryFrame = LabelFrame(self.FourthColumnFrame, text="Backstory:")
                self.BackstoryFrame.grid(row=0, column=0, padx=2, pady=2)
                self.BackstoryField = ScrolledTextPixelDim(self.BackstoryFrame, width=140, height=473, wrap=WORD)
                self.BackstoryField.pack()

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
                self.SelectButton = Button(self.PortraitHolderFrame, text="Select", command=self.Select, bg=ButtonColor)
                self.SelectButton.grid(row=1, column=0, sticky=NSEW)
                self.ExportButton = Button(self.PortraitHolderFrame, text="Export", command=self.Export, bg=ButtonColor)
                self.ExportButton.grid(row=1, column=1, sticky=NSEW)
                self.ClearButton = Button(self.PortraitHolderFrame, text="Clear", command=self.Clear, bg=ButtonColor)
                self.ClearButton.grid(row=1, column=2, sticky=NSEW)

                # Portrait Instructions
                self.PortraitInstructions = Label(self.PortraitHolderFrame, text="Portrait must be a .gif file no larger than 400 x 400.")
                self.PortraitInstructions.grid(row=2, column=0, columnspan=3, sticky=NSEW)

            def Select(self):
                if self.PortraitSelectedVar.get():
                    SelectConfirm = messagebox.askyesno("Select Portrait", "Are you sure you want to select a new portrait?  This cannot be undone.")
                    if not SelectConfirm:
                        return
                PortraitFileName = filedialog.askopenfilename(filetypes=(("GIF file", "*.gif"), ("All files", "*.*")), defaultextension=".gif", title="Select Portrait")
                if PortraitFileName != "":
                    if PortraitFileName.endswith(".gif"):
                        self.SetPortrait(PortraitFileName)
                    else:
                        messagebox.showerror("Invalid Selection", "Portraits must be .gif files.")
                else:
                    ToolbarAndStatusBarInst.StatusBarTextVar.set("No portrait selected!")

            def SetPortrait(self, ImageFileName):
                self.PortraitCanvas.delete("all")
                self.PortraitSelectedVar.set(True)
                self.PortraitImage.configure(file=ImageFileName)
                self.PortraitCanvas.create_image((self.PortraitCanvas.winfo_width() / 2), (self.PortraitCanvas.winfo_height() / 2), image=self.PortraitImage)

            def Export(self):
                ExportFileName = filedialog.asksaveasfilename(filetypes=(("GIF file", "*.gif"), ("All files", "*.*")), defaultextension=".gif", title="Export Portrait")
                self.PortraitImage.write(ExportFileName)

            def Clear(self):
                if self.PortraitSelectedVar.get():
                    ClearConfirm = messagebox.askyesno("Clear Portrait", "Are you sure you want to clear the portrait?  This cannot be undone.")
                    if not ClearConfirm:
                        return
                self.PortraitSelectedVar.set(False)
                self.PortraitCanvas.delete("all")

    # Dice Roller
    class DiceRoller:
        DiceNumberEntryVar = StringVar(value="1")
        DieTypeEntryVar = StringVar(value="20")
        ModifierEntryVar = StringVar(value="0")

        def __init__(self, master):
            # Dice Roller Frame
            self.DiceRollerFrame = LabelFrame(master, text="Dice Roller:")
            self.DiceRollerFrame.pack(side=RIGHT, padx=2, pady=2)

            # Dice Entry Frame
            self.DiceEntryFrame = Frame(self.DiceRollerFrame)
            self.DiceEntryFrame.pack(padx=2, pady=2)

            # Number of Dice
            self.DiceNumberEntry = Entry(self.DiceEntryFrame, textvariable=self.DiceNumberEntryVar, justify=CENTER, width=5)
            self.DiceNumberEntry.pack(side=LEFT, padx=2, pady=2)

            # Die Type
            self.DieTypeLabel = Label(self.DiceEntryFrame, text="d")
            self.DieTypeLabel.pack(side=LEFT)
            self.DieTypeEntry = Entry(self.DiceEntryFrame, textvariable=self.DieTypeEntryVar, justify=CENTER, width=5)
            self.DieTypeEntry.pack(side=LEFT, padx=2, pady=2)

            # Modifier
            self.ModifierLabel = Label(self.DiceEntryFrame, text="+")
            self.ModifierLabel.pack(side=LEFT)
            self.ModifierEntry = Entry(self.DiceEntryFrame, textvariable=self.ModifierEntryVar, justify=CENTER, width=5)
            self.ModifierEntry.pack(side=LEFT, padx=2, pady=2)

            # Dice Buttons Frame
            self.DiceButtonsFrame = Frame(self.DiceRollerFrame)
            self.DiceButtonsFrame.pack(padx=2, pady=2)

            # Roll Button
            self.RollButton = Button(self.DiceButtonsFrame, text="Roll", command=self.Roll, width=7, bg=ButtonColor)
            self.RollButton.pack(side=LEFT, padx=2, pady=2)

            # Average Roll Button
            self.AverageRollButton = Button(self.DiceButtonsFrame, text="Avg. Roll", command=self.AverageRoll, width=7, bg=ButtonColor)
            self.AverageRollButton.pack(side=LEFT, padx=2, pady=2)

            # Results
            self.ResultsFieldFrame = LabelFrame(self.DiceRollerFrame, text="Results:")
            self.ResultsField = ScrolledTextPixelDim(self.ResultsFieldFrame, state=DISABLED, wrap=WORD, height=154, width=335, bg="light gray", cursor="arrow")
            self.ResultsFieldFrame.pack(padx=2, pady=2)
            self.ResultsField.pack(padx=2, pady=2)

            # Preset Rolls
            self.PresetRollsInst = self.PresetRolls(self.DiceRollerFrame)

        def UpdateResultsField(self, UpdateText):
            if self.ResultsField.Text.get(1.0, "end-1c") != "":
                UpdateText += ("\n") * 2
            self.ResultsField.Text.config(state=NORMAL)
            self.ResultsField.Text.insert(1.0, UpdateText)
            self.ResultsField.Text.config(state=DISABLED)

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
            DiceNumber = GetStringVarAsInt(self.DiceNumberEntryVar)
            DieType = GetStringVarAsInt(self.DieTypeEntryVar)
            Modifier = GetStringVarAsInt(self.ModifierEntryVar)
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
                if Result == 20:
                    CritSuccess = True
            Result += Modifier
            sleep(0.5)
            if CritSuccess:
                CritResultText = " (Crit!)"
            elif CritFailure:
                CritResultText = " (Crit Fail!)"
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
            DiceNumber = GetStringVarAsInt(self.DiceNumberEntryVar)
            DieType = GetStringVarAsInt(self.DieTypeEntryVar)
            Modifier = GetStringVarAsInt(self.ModifierEntryVar)
            while CurrentRoll <= TestRolls:
                Result += self.IntRoll(DiceNumber, DieType, Modifier)
                CurrentRoll += 1
            sleep(0.5)
            Result /= TestRolls
            ResultText = "Average of " + str(DiceNumber) + "d" + str(DieType) + "+" + str(Modifier) + " over 100,000 rolls:\n" + str(Result)
            self.UpdateResultsField(ResultText)

        def ValidDiceEntry(self):
            try:
                DiceNumber = GetStringVarAsInt(self.DiceNumberEntryVar)
                DieType = GetStringVarAsInt(self.DieTypeEntryVar)
                Modifier = GetStringVarAsInt(self.ModifierEntryVar)
            except:
                messagebox.showerror("Invalid Entry", "Can't roll anything but whole numbers.")
                return False
            if DiceNumber < 1 or DieType < 1:
                messagebox.showerror("Invalid Entry", "Can't roll unless dice and die type are positive.")
                return False
            return True

        class PresetRolls:
            def __init__(self, master):
                # Preset Rolls Frame
                self.PresetRollsFrame = LabelFrame(master, text="Preset Rolls:")
                self.PresetRollsFrame.pack(padx=2, pady=2)

                # Preset Rolls Scrolling Canvas
                self.PresetRollsScrollingCanvas = Canvas(self.PresetRollsFrame, highlightthickness=0, height=261, width=322)
                self.PresetRollsScrollingCanvas.pack(side=LEFT)
                self.PresetRollsScrollbar = Scrollbar(self.PresetRollsFrame, orient=VERTICAL, command=self.PresetRollsScrollingCanvas.yview)
                self.PresetRollsScrollbar.pack(side=RIGHT, fill=Y)
                self.PresetRollsCanvasFrame = Frame(self.PresetRollsScrollingCanvas)
                self.PresetRollsScrollingCanvas.create_window((0, 0), window=self.PresetRollsCanvasFrame, anchor=NW)
                self.PresetRollsScrollingCanvas.config(yscrollcommand=self.PresetRollsScrollbar.set)
                self.PresetRollsScrollingCanvas.bind('<Configure>', self.ConfigurePresetRollsScrollingCanvas)

                # Preset Rolls List
                self.PresetRollsList = []

                # Preset Rolls
                self.PresetRollEntry1 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 1)
                self.PresetRollEntry2 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 2)
                self.PresetRollEntry3 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 3)
                self.PresetRollEntry4 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 4)
                self.PresetRollEntry5 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 5)
                self.PresetRollEntry6 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 6)
                self.PresetRollEntry7 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 7)
                self.PresetRollEntry8 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 8)
                self.PresetRollEntry9 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 9)
                self.PresetRollEntry10 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 10)
                self.PresetRollEntry11 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 11)
                self.PresetRollEntry12 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 12)
                self.PresetRollEntry13 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 13)
                self.PresetRollEntry14 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 14)
                self.PresetRollEntry15 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 15)
                self.PresetRollEntry16 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 16)
                self.PresetRollEntry17 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 17)
                self.PresetRollEntry18 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 18)
                self.PresetRollEntry19 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 19)
                self.PresetRollEntry20 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 20)
                self.PresetRollEntry21 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 21)
                self.PresetRollEntry22 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 22)
                self.PresetRollEntry23 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 23)
                self.PresetRollEntry24 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 24)
                self.PresetRollEntry25 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 25)
                self.PresetRollEntry26 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 26)
                self.PresetRollEntry27 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 27)
                self.PresetRollEntry28 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 28)
                self.PresetRollEntry29 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 29)
                self.PresetRollEntry30 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 30)
                self.PresetRollEntry31 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 31)
                self.PresetRollEntry32 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 32)
                self.PresetRollEntry33 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 33)
                self.PresetRollEntry34 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 34)
                self.PresetRollEntry35 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 35)
                self.PresetRollEntry36 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 36)
                self.PresetRollEntry37 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 37)
                self.PresetRollEntry38 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 38)
                self.PresetRollEntry39 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 39)
                self.PresetRollEntry40 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 40)
                self.PresetRollEntry41 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 41)
                self.PresetRollEntry42 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 42)
                self.PresetRollEntry43 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 43)
                self.PresetRollEntry44 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 44)
                self.PresetRollEntry45 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 45)
                self.PresetRollEntry46 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 46)
                self.PresetRollEntry47 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 47)
                self.PresetRollEntry48 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 48)
                self.PresetRollEntry49 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 49)
                self.PresetRollEntry50 = self.PresetRollEntry(self.PresetRollsCanvasFrame, self.PresetRollsList, 50)

            def ConfigurePresetRollsScrollingCanvas(self, event):
                self.PresetRollsScrollingCanvas.configure(scrollregion=self.PresetRollsScrollingCanvas.bbox('all'))

            def PresetRollsMouseWheelEvent(self, event):
                if OS == "Windows" or OS == "Linux":
                    self.PresetRollsScrollingCanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                elif OS == "Darwin":
                    self.PresetRollsScrollingCanvas.yview_scroll(int(-1 * event.delta), "units")

            def BindMouseWheelPresetRolls(self, event):
                if OS == "Windows" or OS == "Darwin":
                    root.bind("<MouseWheel>", self.PresetRollsMouseWheelEvent)
                elif OS == "Linux":
                    root.bind("<Button-4>", self.PresetRollsMouseWheelEvent)
                    root.bind("<Button-5>", self.PresetRollsMouseWheelEvent)

            class PresetRollEntry:
                def __init__(self, master, List, Row):
                    self.PresetRollNameEntryVar = StringVar()
                    self.PresetRollDiceNumberEntryVar = StringVar()
                    self.PresetRollDieTypeEntryVar = StringVar()
                    self.PresetRollModifierEntryVar = StringVar()
                    self.ConfigSubmitted = BooleanVar()
                    self.StrengthBoxVar = BooleanVar()
                    self.DexterityBoxVar = BooleanVar()
                    self.ConstitutionBoxVar = BooleanVar()
                    self.IntelligenceBoxVar = BooleanVar()
                    self.WisdomBoxVar = BooleanVar()
                    self.CharismaBoxVar = BooleanVar()
                    self.ProficiencyBoxVar = BooleanVar()
                    self.ManualBonusEntryVar = StringVar()
                    self.Row = Row

                    # Add to List
                    List.append(self)

                    # Name
                    self.PresetRollNameEntry = Entry(master, justify=CENTER, width=25, textvariable=self.PresetRollNameEntryVar)
                    self.PresetRollNameEntry.grid(row=self.Row, column=0, sticky=NSEW)

                    # Roll Button
                    self.PresetRollButton = Button(master, text="Roll:", command=self.RollPreset, bg=ButtonColor)
                    self.PresetRollButton.grid(row=self.Row, column=1, sticky=NSEW)

                    # Dice Number
                    self.PresetRollDiceNumberEntry = Entry(master, justify=CENTER, width=5, textvariable=self.PresetRollDiceNumberEntryVar)
                    self.PresetRollDiceNumberEntry.grid(row=self.Row, column=2, sticky=NSEW)

                    # Die Type
                    self.PresetRollDieTypeLabel = Label(master, text="d")
                    self.PresetRollDieTypeLabel.grid(row=self.Row, column=3, sticky=NSEW)
                    self.PresetRollDieTypeEntry = Entry(master, justify=CENTER, width=5, textvariable=self.PresetRollDieTypeEntryVar)
                    self.PresetRollDieTypeEntry.grid(row=self.Row, column=4, sticky=NSEW)

                    # Modifier
                    self.PresetRollModifierButton = Button(master, text="+", command=self.ConfigureModifier, bg=ButtonColor)
                    self.PresetRollModifierButton.grid(row=self.Row, column=5, sticky=NSEW)
                    self.PresetRollModifierEntry = Entry(master, justify=CENTER, width=5, textvariable=self.PresetRollModifierEntryVar, disabledbackground="light gray", disabledforeground="black")
                    self.PresetRollModifierEntry.grid(row=self.Row, column=6, sticky=NSEW)

                def RollPreset(self):
                    StatsAndDiceRollerFrameInst.DiceRollerInst.DiceNumberEntryVar.set(self.PresetRollDiceNumberEntry.get())
                    StatsAndDiceRollerFrameInst.DiceRollerInst.DieTypeEntryVar.set(self.PresetRollDieTypeEntry.get())
                    StatsAndDiceRollerFrameInst.DiceRollerInst.ModifierEntryVar.set(self.PresetRollModifierEntry.get())
                    StatsAndDiceRollerFrameInst.DiceRollerInst.Roll(self.PresetRollNameEntryVar.get() + ":\n")

                def ConfigureModifier(self):
                    # Test Level Input Validity
                    if CharacterSheetHeaderInst.ValidLevelEntry():
                        pass
                    else:
                        return

                    # Test Ability Input Validity
                    if StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.ValidStatsEntry():
                        pass
                    else:
                        return

                    # Create Config Window and Wait
                    PresetRollModifierConfigInst = self.PresetRollModifierConfig(root, self.StrengthBoxVar, self.DexterityBoxVar, self.ConstitutionBoxVar, self.IntelligenceBoxVar, self.WisdomBoxVar, self.CharismaBoxVar,
                                                                                 self.ProficiencyBoxVar, self.ManualBonusEntryVar)
                    root.wait_window(PresetRollModifierConfigInst.Window)

                    # Handle Entry
                    if PresetRollModifierConfigInst.NewConfigSubmitted.get():
                        # Handle Variables
                        self.ConfigSubmitted.set(True)
                        self.StrengthBoxVar.set(PresetRollModifierConfigInst.StrengthBoxVar.get())
                        self.DexterityBoxVar.set(PresetRollModifierConfigInst.DexterityBoxVar.get())
                        self.ConstitutionBoxVar.set(PresetRollModifierConfigInst.ConstitutionBoxVar.get())
                        self.IntelligenceBoxVar.set(PresetRollModifierConfigInst.IntelligenceBoxVar.get())
                        self.WisdomBoxVar.set(PresetRollModifierConfigInst.WisdomBoxVar.get())
                        self.CharismaBoxVar.set(PresetRollModifierConfigInst.CharismaBoxVar.get())
                        self.ProficiencyBoxVar.set(PresetRollModifierConfigInst.ProficiencyBoxVar.get())
                        self.ManualBonusEntryVar.set(PresetRollModifierConfigInst.ManualBonusEntryVar.get())

                        # Disable Modifier Entry
                        self.PresetRollModifierEntry.configure(state=DISABLED, cursor="arrow")

                        # Update Stats and Inventory
                        UpdateStatsAndInventory()
                    elif PresetRollModifierConfigInst.ConfigCleared.get():
                        # Handle Variables
                        self.ConfigSubmitted.set(False)
                        self.StrengthBoxVar.set(False)
                        self.DexterityBoxVar.set(False)
                        self.ConstitutionBoxVar.set(False)
                        self.IntelligenceBoxVar.set(False)
                        self.WisdomBoxVar.set(False)
                        self.CharismaBoxVar.set(False)
                        self.ProficiencyBoxVar.set(False)
                        self.ManualBonusEntryVar.set("")

                        # Enable Modifier Entry
                        self.PresetRollModifierEntry.configure(state=NORMAL, cursor="xterm")

                def SetConfiguredModifier(self):
                    if self.ConfigSubmitted.get():
                        Modifier = 0
                        if self.StrengthBoxVar.get():
                            Modifier += GetStringVarAsInt(StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.StrengthEntry.AbilityEntryModifierVar)
                        if self.DexterityBoxVar.get():
                            Modifier += GetStringVarAsInt(StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.DexterityEntry.AbilityEntryModifierVar)
                        if self.ConstitutionBoxVar.get():
                            Modifier += GetStringVarAsInt(StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.ConstitutionEntry.AbilityEntryModifierVar)
                        if self.IntelligenceBoxVar.get():
                            Modifier += GetStringVarAsInt(StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.IntelligenceEntry.AbilityEntryModifierVar)
                        if self.WisdomBoxVar.get():
                            Modifier += GetStringVarAsInt(StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.WisdomEntry.AbilityEntryModifierVar)
                        if self.CharismaBoxVar.get():
                            Modifier += GetStringVarAsInt(StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.CharismaEntry.AbilityEntryModifierVar)
                        if self.ProficiencyBoxVar.get():
                            Modifier += GetStringVarAsInt(CharacterSheetHeaderInst.ProficiencyBonusEntryVar)
                        Modifier += GetStringVarAsInt(self.ManualBonusEntryVar)
                        self.PresetRollModifierEntryVar.set(str(Modifier))

                class PresetRollModifierConfig:
                    def __init__(self, master, StrengthBoxVar, DexterityBoxVar, ConstitutionBoxVar, IntelligenceBoxVar, WisdomBoxVar, CharismaBoxVar, ProficiencyBoxVar, ManualBonusEntryVar):
                        self.NewConfigSubmitted = BooleanVar()
                        self.ConfigCleared = BooleanVar()
                        self.StrengthBoxVar = BooleanVar(value=StrengthBoxVar.get())
                        self.DexterityBoxVar = BooleanVar(value=DexterityBoxVar.get())
                        self.ConstitutionBoxVar = BooleanVar(value=ConstitutionBoxVar.get())
                        self.IntelligenceBoxVar = BooleanVar(value=IntelligenceBoxVar.get())
                        self.WisdomBoxVar = BooleanVar(value=WisdomBoxVar.get())
                        self.CharismaBoxVar = BooleanVar(value=CharismaBoxVar.get())
                        self.ProficiencyBoxVar = BooleanVar(value=ProficiencyBoxVar.get())
                        self.ManualBonusEntryVar = StringVar(value=ManualBonusEntryVar.get())

                        # Create Window
                        self.Window = Toplevel(master)
                        self.Window.wm_attributes("-toolwindow", 1)
                        self.Window.wm_title("Modifier")

                        # Label
                        self.InstructionLabel = Label(self.Window, text="Select the modifiers\nto add to this roll.", bd=2, relief=GROOVE)
                        self.InstructionLabel.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=2, pady=2)

                        # Boxes
                        self.StrengthBox = Checkbutton(self.Window, text="Strength", variable=self.StrengthBoxVar)
                        self.StrengthBox.grid(row=1, column=0, sticky=W, padx=2, pady=2, columnspan=2)
                        self.DexterityBox = Checkbutton(self.Window, text="Dexterity", variable=self.DexterityBoxVar)
                        self.DexterityBox.grid(row=2, column=0, sticky=W, padx=2, pady=2, columnspan=2)
                        self.ConstitutionBox = Checkbutton(self.Window, text="Constitution", variable=self.ConstitutionBoxVar)
                        self.ConstitutionBox.grid(row=3, column=0, sticky=W, padx=2, pady=2, columnspan=2)
                        self.IntelligenceBox = Checkbutton(self.Window, text="Intelligence", variable=self.IntelligenceBoxVar)
                        self.IntelligenceBox.grid(row=4, column=0, sticky=W, padx=2, pady=2, columnspan=2)
                        self.WisdomBox = Checkbutton(self.Window, text="Wisdom", variable=self.WisdomBoxVar)
                        self.WisdomBox.grid(row=5, column=0, sticky=W, padx=2, pady=2, columnspan=2)
                        self.CharismaBox = Checkbutton(self.Window, text="Charisma", variable=self.CharismaBoxVar)
                        self.CharismaBox.grid(row=6, column=0, sticky=W, padx=2, pady=2, columnspan=2)
                        self.ProficiencyBox = Checkbutton(self.Window, text="Proficiency", variable=self.ProficiencyBoxVar)
                        self.ProficiencyBox.grid(row=7, column=0, sticky=W, padx=2, pady=2, columnspan=2)

                        # Manual Bonus Entry
                        self.ManualBonusFrame = Frame(self.Window)
                        self.ManualBonusFrame.grid(row=8, column=0, columnspan=2)
                        self.ManualBonusLabel = Label(self.ManualBonusFrame, text="Manual Bonus:")
                        self.ManualBonusLabel.grid(row=0, column=0)
                        self.ManualBonusEntry = Entry(self.ManualBonusFrame, textvariable=self.ManualBonusEntryVar, width=4, justify=CENTER)
                        self.ManualBonusEntry.grid(row=0, column=1, padx=2, pady=2)

                        # Buttons
                        self.SubmitButton = Button(self.Window, text="Submit", command=self.Submit, bg=ButtonColor)
                        self.SubmitButton.grid(row=9, column=0, padx=2, pady=2, sticky=NSEW)
                        self.CancelButton = Button(self.Window, text="Clear", command=self.Clear, bg=ButtonColor)
                        self.CancelButton.grid(row=9, column=1, padx=2, pady=2, sticky=NSEW)

                        # Prevent Main Window Input
                        self.Window.grab_set()

                        # Handle Config Window Geometry and Focus
                        WindowGeometry(self.Window, True)
                        self.Window.focus_force()

                    def Submit(self):
                        if self.ValidManualBonus():
                            self.NewConfigSubmitted.set(True)
                            self.Window.destroy()

                    def Clear(self):
                        self.ConfigCleared.set(True)
                        self.Window.destroy()

                    def ValidManualBonus(self):
                        try:
                            ManualBonus = GetStringVarAsInt(self.ManualBonusEntryVar)
                        except:
                            messagebox.showerror("Invalid Entry", "Manual bonus must be an integer.")
                            return False
                        return True


class ToolbarAndStatusBar:
    StatusBarTextVar = StringVar(value="Status")
    StatusBarPreviousTextVar = StringVar()
    CurrentOpenFilePath = StringVar()
    PreviousOpenFilePath = StringVar()

    def __init__(self, master):
        # Toolbar Frame
        self.ToolbarFrame = Frame(master, bg="gray", bd=1, relief=SUNKEN)
        self.ToolbarFrame.pack(side=TOP, expand=True, fill=X, padx=2, pady=2)

        # Toolbar Open Button
        self.ToolbarOpenButton = Button(self.ToolbarFrame, text="Open", command=self.OpenButton, bg=ButtonColor)
        self.ToolbarOpenButton.pack(side=LEFT, padx=2, pady=2)

        # Toolbar Save Button
        self.ToolbarSaveButton = Button(self.ToolbarFrame, text="Save", command=self.SaveButton, bg=ButtonColor)
        self.ToolbarSaveButton.pack(side=LEFT, padx=2, pady=2)

        # Toolbar Save As Button
        self.ToolbarSaveAsButton = Button(self.ToolbarFrame, text="Save As", command=self.SaveAsButton, bg=ButtonColor)
        self.ToolbarSaveAsButton.pack(side=LEFT, padx=2, pady=2)

        # Status Bar Label
        self.StatusBarLabel = Label(self.ToolbarFrame, textvariable=self.StatusBarTextVar, fg="white", bg="gray")
        self.StatusBarLabel.pack(side=LEFT, fill=X)

        # Update Stats Button
        self.UpdateStatsButton = Button(self.ToolbarFrame, text="Update Stats and Inventory", command=UpdateStatsAndInventory, bg=ButtonColor)
        self.UpdateStatsButton.pack(side=RIGHT, padx=2, pady=2)

    # Save Utility Methods
    def SaveText(self, File, Field, FieldTag):
        TextContent = Field.get("1.0", "end-1c")
        File.write("<" + str(FieldTag) + ">\n" + str(TextContent) + "\n</" + str(FieldTag) + ">\n")

    def SaveVar(self, File, Var, FieldTag):
        VarContent = Var.get()
        File.write("<" + str(FieldTag) + ">\n" + str(VarContent) + "\n</" + str(FieldTag) + ">\n")

    def SavePresetRollFields(self, File):
        for Entry in StatsAndDiceRollerFrameInst.DiceRollerInst.PresetRollsInst.PresetRollsList:
            self.SaveVar(File, Entry.PresetRollNameEntryVar, "PRNameEntry" + str(Entry.Row))
            self.SaveVar(File, Entry.PresetRollDiceNumberEntryVar, "PRDiceNumberEntry" + str(Entry.Row))
            self.SaveVar(File, Entry.PresetRollDieTypeEntryVar, "PRDieTypeEntry" + str(Entry.Row))
            self.SaveVar(File, Entry.PresetRollModifierEntryVar, "PRModifierEntry" + str(Entry.Row))
            self.SaveVar(File, Entry.ConfigSubmitted, "PRConfigSubmitted" + str(Entry.Row))
            self.SaveVar(File, Entry.StrengthBoxVar, "PRStrengthBox" + str(Entry.Row))
            self.SaveVar(File, Entry.DexterityBoxVar, "PRDexterityBox" + str(Entry.Row))
            self.SaveVar(File, Entry.ConstitutionBoxVar, "PRConstitutionBox" + str(Entry.Row))
            self.SaveVar(File, Entry.IntelligenceBoxVar, "PRIntelligenceBox" + str(Entry.Row))
            self.SaveVar(File, Entry.WisdomBoxVar, "PRWisdomBox" + str(Entry.Row))
            self.SaveVar(File, Entry.CharismaBoxVar, "PRCharismaBox" + str(Entry.Row))
            self.SaveVar(File, Entry.ProficiencyBoxVar, "PRProficiencyBox" + str(Entry.Row))
            self.SaveVar(File, Entry.ManualBonusEntryVar, "PRManualBonusEntry" + str(Entry.Row))

    def SaveSkillProficiencies(self, File):
        for Entry in StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.SkillsInst.SkillsEntriesList:
            self.SaveVar(File, Entry.ProficiencyBox1Var, Entry.SkillNameVar.get() + "SkillProficiency1")
            self.SaveVar(File, Entry.ProficiencyBox2Var, Entry.SkillNameVar.get() + "SkillProficiency2")

    def SaveAbilityScoreData(self, File):
        for Entry in StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.AbilityEntriesList:
            AbilityName = Entry.AbilityNameVar.get()
            self.SaveVar(File, Entry.AbilityEntryTotalVar, AbilityName + "Total")
            self.SaveVar(File, Entry.AbilityBaseVar, AbilityName + "Base")
            self.SaveVar(File, Entry.AbilityRacialVar, AbilityName + "Racial")
            self.SaveVar(File, Entry.AbilityASIVar, AbilityName + "ASI")
            self.SaveVar(File, Entry.AbilityMiscVar, AbilityName + "Misc")
            self.SaveVar(File, Entry.AbilityOverrideVar, AbilityName + "Override")
            self.SaveVar(File, Entry.AbilitySavingThrowProficiencyBoxVar, AbilityName + "SavingThrowProficiency")
        self.SaveVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.PointBuyBoxVar, "PointBuy")
        self.SaveText(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.AbilitiesNotes.Text, "AbilitiesNotes")

    def SaveAsButton(self):
        self.PreviousOpenFilePath.set(self.CurrentOpenFilePath.get())
        self.CurrentOpenFilePath.set("")
        self.SaveButton()

    def SaveInventory(self, File):
        # Save Inventory Coins
        self.SaveVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.InventoryInst.CoinsEntryCPVar, "InventoryCP")
        self.SaveVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.InventoryInst.CoinsEntrySPVar, "InventorySP")
        self.SaveVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.InventoryInst.CoinsEntryEPVar, "InventoryEP")
        self.SaveVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.InventoryInst.CoinsEntryGPVar, "InventoryGP")
        self.SaveVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.InventoryInst.CoinsEntryPPVar, "InventoryPP")

        # Save Inventory List
        for Entry in StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.InventoryInst.InventoryEntriesList:
            self.SaveVar(File, Entry.NameEntryVar, "InventoryListName" + str(Entry.Row))
            self.SaveVar(File, Entry.CountEntryVar, "InventoryListCount" + str(Entry.Row))
            self.SaveVar(File, Entry.UnitWeightEntryVar, "InventoryListUnitWeight" + str(Entry.Row))
            self.SaveVar(File, Entry.UnitValueEntryVar, "InventoryListUnitValue" + str(Entry.Row))
            self.SaveVar(File, Entry.UnitValueDenominationVar, "InventoryListUnitValueDenomination" + str(Entry.Row))
            self.SaveVar(File, Entry.CategoryTagVar, "InventoryListCategoryTag" + str(Entry.Row))

    def SaveVitality(self, File):
        self.SaveVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.TempHPEntryVar, "TempHP")
        self.SaveVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.CurrentHPEntryVar, "CurrentHP")
        self.SaveVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.MaxHPEntryVar, "MaxHP")
        self.SaveVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.HitDiceEntryVar, "HitDice")
        self.SaveVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.HitDiceRemainingEntryVar, "HitDiceRemaining")
        self.SaveVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.DeathSavingThrowsBoxSuccess1Var, "DeathSavingThrowsSuccess1")
        self.SaveVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.DeathSavingThrowsBoxSuccess2Var, "DeathSavingThrowsSuccess2")
        self.SaveVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.DeathSavingThrowsBoxSuccess3Var, "DeathSavingThrowsSuccess3")
        self.SaveVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.DeathSavingThrowsBoxFailure1Var, "DeathSavingThrowsFailure1")
        self.SaveVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.DeathSavingThrowsBoxFailure2Var, "DeathSavingThrowsFailure2")
        self.SaveVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.DeathSavingThrowsBoxFailure3Var, "DeathSavingThrowsFailure3")

    def SaveFeatures(self, File):
        # Save Feature Entries
        for Entry in StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.FeaturesInst.FeaturesEntriesList:
            self.SaveVar(File, Entry.NameEntryVar, "FeatureEntryName" + str(Entry.Row))
            self.SaveVar(File, Entry.DescriptionVar, "FeatureEntryDescription" + str(Entry.Row))

        # Save Features Notes
        self.SaveText(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.FeaturesInst.FeaturesNotes.Text, "FeaturesNotes")

    # Saving
    def SaveButton(self):
        self.StatusBarTextVar.set("Saving...")
        CurrentPath = self.CurrentOpenFilePath.get()
        if CurrentPath == "":
            SaveFileName = filedialog.asksaveasfilename(filetypes=(("Character file", "*.char"), ("All files", "*.*")), defaultextension=".char", title="Save Character File As")
        else:
            SaveFileName = CurrentPath
        TextFileName = "Character Data.txt"
        PortraitFileName = "Portrait.gif"
        if SaveFileName != "":
            with ZipFile(SaveFileName, mode="w") as SaveFile:
                with open(TextFileName, mode="w") as TextFile:
                    # Save Character Header Fields
                    self.SaveVar(TextFile, CharacterSheetHeaderInst.CharacterNameEntryVar, "CharacterName")
                    self.SaveVar(TextFile, CharacterSheetHeaderInst.CharacterClassEntryVar, "CharacterClass")
                    self.SaveVar(TextFile, CharacterSheetHeaderInst.CharacterLevelEntryVar, "CharacterLevel")
                    self.SaveVar(TextFile, CharacterSheetHeaderInst.CharacterExperienceEntryVar, "CharacterExperience")

                    # Save Ability Score Data
                    self.SaveAbilityScoreData(TextFile)

                    # Save Skill Proficiencies
                    self.SaveSkillProficiencies(TextFile)

                    # Save Vitality
                    self.SaveVitality(TextFile)

                    # Save AC
                    self.SaveVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.ACBaseEntryVar, "ACBase")
                    self.SaveVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.ACModifierVar, "ACModifier")
                    self.SaveVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.ACManualBonusEntryVar, "ACManualBonus")

                    # Save Initiative
                    self.SaveVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.InitiativeManualBonusEntryVar, "InitiativeManualBonus")

                    # Save Speed
                    self.SaveVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.SpeedEntryVar, "Speed")

                    # Save Combat Notes
                    self.SaveText(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.OffenseNotes.Text, "OffenseNotes")
                    self.SaveText(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.DefenseNotes.Text, "DefenseNotes")

                    # Save Features
                    self.SaveFeatures(TextFile)

                    # Save Inventory
                    self.SaveInventory(TextFile)

                    # Save Notes
                    self.SaveText(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.NotesInst.NotesField.Text, "Notes")

                    # Save Personality and Backstory
                    self.SaveVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PersonalityAndBackstoryInst.RaceEntryVar, "Race")
                    self.SaveVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PersonalityAndBackstoryInst.BackgroundEntryVar, "Background")
                    self.SaveVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PersonalityAndBackstoryInst.AlignmentEntryVar, "Alignment")
                    self.SaveVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PersonalityAndBackstoryInst.AgeEntryVar, "Age")
                    self.SaveText(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PersonalityAndBackstoryInst.PhysicalAppearanceField.Text, "PhysicalAppearance")
                    self.SaveText(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PersonalityAndBackstoryInst.PersonalityTraitsField.Text, "PersonalityTraits")
                    self.SaveText(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PersonalityAndBackstoryInst.BondsField.Text, "Bonds")
                    self.SaveText(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PersonalityAndBackstoryInst.IdealsField.Text, "Ideals")
                    self.SaveText(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PersonalityAndBackstoryInst.FlawsField.Text, "Flaws")
                    self.SaveText(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PersonalityAndBackstoryInst.BackstoryField.Text, "Backstory")

                    # Save Portrait Var
                    self.SaveVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PortraitInst.PortraitSelectedVar, "PortraitSelected")

                    # Save Preset Roll Fields
                    self.SavePresetRollFields(TextFile)
                SaveFile.write(TextFileName)
                PortraitSelected = StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PortraitInst.PortraitSelectedVar.get()
                if PortraitSelected:
                    StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PortraitInst.PortraitImage.write(PortraitFileName)
                    SaveFile.write(PortraitFileName)
                    os.remove(PortraitFileName)
            os.remove(TextFileName)
            self.CurrentOpenFilePath.set(SaveFileName)
            sleep(0.5)
            self.StatusBarTextVar.set("File saved as:  " + os.path.basename(SaveFileName))
            self.StatusBarPreviousTextVar.set("File saved as:  " + os.path.basename(SaveFileName))
        else:
            self.StatusBarTextVar.set("No file saved!")
            self.CurrentOpenFilePath.set(self.PreviousOpenFilePath.get())

    def SaveKeystroke(self, event):
        self.SaveButton()

    def SaveAsKeystroke(self, event):
        self.SaveAsButton()

    # Open Utility Methods
    def OpenText(self, File, Field, FieldTag):
        ReadState = False
        TextContent = ""
        File.seek(0)
        for Line in File:
            if Line == "</" + FieldTag + ">\n":
                break
            if ReadState == True:
                TextContent += Line
            if Line == "<" + FieldTag + ">\n":
                ReadState = True
        Field.delete(1.0, END)
        TextContent = TextContent[:-1]
        Field.insert(1.0, TextContent)

    def OpenVar(self, File, Var, FieldTag):
        ReadState = False
        VarContent = ""
        File.seek(0)
        for Line in File:
            if Line == "</" + FieldTag + ">\n":
                break
            if ReadState == True:
                VarContent += Line.rstrip()
            if Line == "<" + FieldTag + ">\n":
                ReadState = True
        if VarContent != "":
            Var.set(VarContent)

    def OpenVarToTextReadyString(self, File, Var, FieldTag):
        ReadState = False
        VarContent = ""
        File.seek(0)
        for Line in File:
            if Line == "</" + FieldTag + ">\n":
                break
            if ReadState == True:
                VarContent += Line
            if Line == "<" + FieldTag + ">\n":
                ReadState = True
        if VarContent != "":
            VarContent = VarContent[:-1]
            Var.set(VarContent)

    def OpenPresetRollFields(self, File):
        for Entry in StatsAndDiceRollerFrameInst.DiceRollerInst.PresetRollsInst.PresetRollsList:
            self.OpenVar(File, Entry.PresetRollNameEntryVar, "PRNameEntry" + str(Entry.Row))
            self.OpenVar(File, Entry.PresetRollDiceNumberEntryVar, "PRDiceNumberEntry" + str(Entry.Row))
            self.OpenVar(File, Entry.PresetRollDieTypeEntryVar, "PRDieTypeEntry" + str(Entry.Row))
            self.OpenVar(File, Entry.PresetRollModifierEntryVar, "PRModifierEntry" + str(Entry.Row))
            self.OpenVar(File, Entry.ConfigSubmitted, "PRConfigSubmitted" + str(Entry.Row))
            self.OpenVar(File, Entry.StrengthBoxVar, "PRStrengthBox" + str(Entry.Row))
            self.OpenVar(File, Entry.DexterityBoxVar, "PRDexterityBox" + str(Entry.Row))
            self.OpenVar(File, Entry.ConstitutionBoxVar, "PRConstitutionBox" + str(Entry.Row))
            self.OpenVar(File, Entry.IntelligenceBoxVar, "PRIntelligenceBox" + str(Entry.Row))
            self.OpenVar(File, Entry.WisdomBoxVar, "PRWisdomBox" + str(Entry.Row))
            self.OpenVar(File, Entry.CharismaBoxVar, "PRCharismaBox" + str(Entry.Row))
            self.OpenVar(File, Entry.ProficiencyBoxVar, "PRProficiencyBox" + str(Entry.Row))
            self.OpenVar(File, Entry.ManualBonusEntryVar, "PRManualBonusEntry" + str(Entry.Row))
            if Entry.ConfigSubmitted.get():
                Entry.PresetRollModifierEntry.configure(state=DISABLED, cursor="arrow")

    def OpenSkillProficiencies(self, File):
        for Entry in StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.SkillsInst.SkillsEntriesList:
            self.OpenVar(File, Entry.ProficiencyBox1Var, Entry.SkillNameVar.get() + "SkillProficiency1")
            self.OpenVar(File, Entry.ProficiencyBox2Var, Entry.SkillNameVar.get() + "SkillProficiency2")

    def OpenAbilityScoreData(self, File):
        for Entry in StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.AbilityEntriesList:
            AbilityName = Entry.AbilityNameVar.get()
            self.OpenVar(File, Entry.AbilityEntryTotalVar, AbilityName + "Total")
            self.OpenVar(File, Entry.AbilityBaseVar, AbilityName + "Base")
            self.OpenVar(File, Entry.AbilityRacialVar, AbilityName + "Racial")
            self.OpenVar(File, Entry.AbilityASIVar, AbilityName + "ASI")
            self.OpenVar(File, Entry.AbilityMiscVar, AbilityName + "Misc")
            self.OpenVar(File, Entry.AbilityOverrideVar, AbilityName + "Override")
            self.OpenVar(File, Entry.AbilitySavingThrowProficiencyBoxVar, AbilityName + "SavingThrowProficiency")
        self.OpenVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.PointBuyBoxVar, "PointBuy")
        self.OpenText(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.AbilitiesNotes.Text, "AbilitiesNotes")

    def OpenInventory(self, TextFile):
        # Open Inventory Coins
        self.OpenVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.InventoryInst.CoinsEntryCPVar, "InventoryCP")
        self.OpenVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.InventoryInst.CoinsEntrySPVar, "InventorySP")
        self.OpenVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.InventoryInst.CoinsEntryEPVar, "InventoryEP")
        self.OpenVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.InventoryInst.CoinsEntryGPVar, "InventoryGP")
        self.OpenVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.InventoryInst.CoinsEntryPPVar, "InventoryPP")

        # Open Inventory List
        for Entry in StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.InventoryInst.InventoryEntriesList:
            self.OpenVar(TextFile, Entry.NameEntryVar, "InventoryListName" + str(Entry.Row))
            self.OpenVar(TextFile, Entry.CountEntryVar, "InventoryListCount" + str(Entry.Row))
            self.OpenVar(TextFile, Entry.UnitWeightEntryVar, "InventoryListUnitWeight" + str(Entry.Row))
            self.OpenVar(TextFile, Entry.UnitValueEntryVar, "InventoryListUnitValue" + str(Entry.Row))
            self.OpenVar(TextFile, Entry.UnitValueDenominationVar, "InventoryListUnitValueDenomination" + str(Entry.Row))
            self.OpenVar(TextFile, Entry.CategoryTagVar, "InventoryListCategoryTag" + str(Entry.Row))

    def OpenVitality(self, File):
        self.OpenVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.TempHPEntryVar, "TempHP")
        self.OpenVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.CurrentHPEntryVar, "CurrentHP")
        self.OpenVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.MaxHPEntryVar, "MaxHP")
        self.OpenVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.HitDiceEntryVar, "HitDice")
        self.OpenVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.HitDiceRemainingEntryVar, "HitDiceRemaining")
        self.OpenVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.DeathSavingThrowsBoxSuccess1Var, "DeathSavingThrowsSuccess1")
        self.OpenVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.DeathSavingThrowsBoxSuccess2Var, "DeathSavingThrowsSuccess2")
        self.OpenVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.DeathSavingThrowsBoxSuccess3Var, "DeathSavingThrowsSuccess3")
        self.OpenVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.DeathSavingThrowsBoxFailure1Var, "DeathSavingThrowsFailure1")
        self.OpenVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.DeathSavingThrowsBoxFailure2Var, "DeathSavingThrowsFailure2")
        self.OpenVar(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.DeathSavingThrowsBoxFailure3Var, "DeathSavingThrowsFailure3")

    def OpenFeatures(self, File):
        # Open Feature Entries
        for Entry in StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.FeaturesInst.FeaturesEntriesList:
            self.OpenVar(File, Entry.NameEntryVar, "FeatureEntryName" + str(Entry.Row))
            self.OpenVarToTextReadyString(File, Entry.DescriptionVar, "FeatureEntryDescription" + str(Entry.Row))

        # Open Features Notes
        self.OpenText(File, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.FeaturesInst.FeaturesNotes.Text, "FeaturesNotes")

    # Opening
    def OpenButton(self):
        self.StatusBarTextVar.set("Opening...")
        OpenFileName = filedialog.askopenfilename(filetypes=(("Character file", "*.char"), ("All files", "*.*")), defaultextension=".char", title="Open Character File")
        TextFileName = "Character Data.txt"
        PortraitFileName = "Portrait.gif"
        if OpenFileName != "":
            with ZipFile(OpenFileName, mode="r") as OpenFile:
                with open(OpenFile.extract(TextFileName), mode="r") as TextFile:
                    # Open Character Header Fields
                    self.OpenVar(TextFile, CharacterSheetHeaderInst.CharacterNameEntryVar, "CharacterName")
                    self.OpenVar(TextFile, CharacterSheetHeaderInst.CharacterClassEntryVar, "CharacterClass")
                    self.OpenVar(TextFile, CharacterSheetHeaderInst.CharacterLevelEntryVar, "CharacterLevel")
                    self.OpenVar(TextFile, CharacterSheetHeaderInst.CharacterExperienceEntryVar, "CharacterExperience")

                    # Open Ability Score Data
                    self.OpenAbilityScoreData(TextFile)

                    # Open Skill Proficiencies
                    self.OpenSkillProficiencies(TextFile)

                    # Open Vitality
                    self.OpenVitality(TextFile)

                    # Open AC
                    self.OpenVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.ACBaseEntryVar, "ACBase")
                    self.OpenVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.ACModifierVar, "ACModifier")
                    self.OpenVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.ACManualBonusEntryVar, "ACManualBonus")

                    # Open Speed
                    self.OpenVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.SpeedEntryVar, "Speed")

                    # Open Initiative
                    self.OpenVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.InitiativeManualBonusEntryVar, "InitiativeManualBonus")

                    # Open Combat Notes
                    self.OpenText(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.OffenseNotes.Text, "OffenseNotes")
                    self.OpenText(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.DefenseNotes.Text, "DefenseNotes")

                    # Open Features
                    self.OpenFeatures(TextFile)

                    # Open Inventory
                    self.OpenInventory(TextFile)

                    # Open Notes
                    self.OpenText(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.NotesInst.NotesField.Text, "Notes")

                    # Open Personality and Backstory
                    self.OpenVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PersonalityAndBackstoryInst.RaceEntryVar, "Race")
                    self.OpenVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PersonalityAndBackstoryInst.BackgroundEntryVar, "Background")
                    self.OpenVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PersonalityAndBackstoryInst.AlignmentEntryVar, "Alignment")
                    self.OpenVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PersonalityAndBackstoryInst.AgeEntryVar, "Age")
                    self.OpenText(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PersonalityAndBackstoryInst.PhysicalAppearanceField.Text, "PhysicalAppearance")
                    self.OpenText(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PersonalityAndBackstoryInst.PersonalityTraitsField.Text, "PersonalityTraits")
                    self.OpenText(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PersonalityAndBackstoryInst.BondsField.Text, "Bonds")
                    self.OpenText(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PersonalityAndBackstoryInst.IdealsField.Text, "Ideals")
                    self.OpenText(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PersonalityAndBackstoryInst.FlawsField.Text, "Flaws")
                    self.OpenText(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PersonalityAndBackstoryInst.BackstoryField.Text, "Backstory")

                    # Open Portrait Var
                    self.OpenVar(TextFile, StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PortraitInst.PortraitSelectedVar, "PortraitSelected")

                    # Open Preset Roll Fields
                    self.OpenPresetRollFields(TextFile)
                if StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PortraitInst.PortraitSelectedVar.get():
                    OpenFile.extract(PortraitFileName)
                    StatsAndDiceRollerFrameInst.CharacterStatsInventoryAndNotesInst.PortraitInst.SetPortrait(PortraitFileName)
                    os.remove(PortraitFileName)
            os.remove(TextFileName)
            self.CurrentOpenFilePath.set(OpenFileName)
            UpdateStatsAndInventory()
            sleep(0.5)
            self.StatusBarTextVar.set("Opened file:  " + os.path.basename(OpenFileName))
            self.StatusBarPreviousTextVar.set("Opened file:  " + os.path.basename(OpenFileName))
        else:
            self.StatusBarTextVar.set("No file opened!")

    def OpenKeystroke(self, event):
        self.OpenButton()

    # Tooltips
    def ToolbarSaveButtonTooltipSet(self, event):
        self.StatusBarPreviousTextVar.set(self.StatusBarTextVar.get())
        self.StatusBarTextVar.set("Keyboard Shortcut:  Ctrl+S")

    def ToolbarOpenButtonTooltipSet(self, event):
        self.StatusBarPreviousTextVar.set(self.StatusBarTextVar.get())
        self.StatusBarTextVar.set("Keyboard Shortcut:  Ctrl+O")

    def ToolbarSaveAsButtonTooltipSet(self, event):
        self.StatusBarPreviousTextVar.set(self.StatusBarTextVar.get())
        self.StatusBarTextVar.set("Keyboard Shortcut:  Ctrl+Shift+S")

    def ToolbarRevertToPrevious(self, event):
        if self.StatusBarTextVar.get() != "Saving..." and self.StatusBarTextVar.get() != "Opening...":
            self.StatusBarTextVar.set(self.StatusBarPreviousTextVar.get())


# Misc
class ScrolledTextPixelDim(Frame):
    def __init__(self, master, width=0, height=0, **kwargs):
        self.width = width
        self.height = height

        Frame.__init__(self, master, width=self.width, height=self.height)
        self.Text = ScrolledTextClass.ScrolledText(self, **kwargs)
        self.Text.pack(expand=YES, fill=BOTH)

    def pack(self, *args, **kwargs):
        Frame.pack(self, *args, **kwargs)
        self.pack_propagate(False)

    def grid(self, *args, **kwargs):
        Frame.grid(self, *args, **kwargs)
        self.grid_propagate(False)


# Populate Window
CharacterSheetHeaderInst = CharacterSheetHeader(root)
StatsAndDiceRollerFrameInst = StatsAndDiceRoller(root)
ToolbarAndStatusBarInst = ToolbarAndStatusBar(root)

# Inst-Dependent Bindings
ConfigureBindings()

# Initial Window Behavior
WindowGeometry(root, False)
root.focus_force()

# Main Loop
root.mainloop()
