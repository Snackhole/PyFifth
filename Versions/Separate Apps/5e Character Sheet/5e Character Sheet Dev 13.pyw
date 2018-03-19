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

# Create and Configure Window
root = Tk()
root.wm_title("Character Sheet")
root.option_add("*Font", "TkDefaultFont")


# Window Elements
class CharacterSheetHeader:
    def __init__(self, master):
        self.CharacterNameEntryVar = StringVar()
        self.CharacterLevelEntryVar = StringVar()
        self.CharacterClassEntryVar = StringVar()
        self.CharacterExperienceEntryVar = StringVar()
        self.CharacterExperienceNeededEntryVar = StringVar()
        self.ProficiencyBonusEntryVar = StringVar()
        self.SpellcasterBoxVar = BooleanVar(value=True)

        # Character Sheet Header Frame
        self.CharacterSheetHeaderFrame = LabelFrame(master, text="Basic Character Info:")
        self.CharacterSheetHeaderFrame.grid_columnconfigure(9, weight=1)
        self.CharacterSheetHeaderFrame.grid(row=0, column=0, sticky=NSEW, columnspan=2, padx=2, pady=2)

        # Character Name
        self.CharacterNameLabel = Label(self.CharacterSheetHeaderFrame, text="Character Name:")
        self.CharacterNameLabel.grid(row=0, column=0)
        self.CharacterNameEntry = Entry(self.CharacterSheetHeaderFrame, textvariable=self.CharacterNameEntryVar, justify=CENTER, width=30)
        self.CharacterNameEntry.grid(row=0, column=1, padx=2, pady=2)

        # Class
        self.CharacterClassLabel = Label(self.CharacterSheetHeaderFrame, text="Class:")
        self.CharacterClassLabel.grid(row=0, column=2)
        self.CharacterClassEntry = Entry(self.CharacterSheetHeaderFrame, textvariable=self.CharacterClassEntryVar, justify=CENTER, width=25)
        self.CharacterClassEntry.grid(row=0, column=3, padx=2, pady=2)

        # Character Level
        self.CharacterLevelLabel = Label(self.CharacterSheetHeaderFrame, text="Level:")
        self.CharacterLevelLabel.grid(row=0, column=4)
        self.CharacterLevelEntry = Entry(self.CharacterSheetHeaderFrame, textvariable=self.CharacterLevelEntryVar, width=4, justify=CENTER)
        self.CharacterLevelEntry.grid(row=0, column=5, padx=2, pady=2)

        # Proficiency Bonus
        self.ProficiencyBonusLabel = Label(self.CharacterSheetHeaderFrame, text="Proficiency Bonus:")
        self.ProficiencyBonusLabel.grid(row=0, column=6)
        self.ProficiencyBonusEntry = Entry(self.CharacterSheetHeaderFrame, textvariable=self.ProficiencyBonusEntryVar, state=DISABLED, justify=CENTER, width=3, disabledbackground="light gray", disabledforeground="black",
                                           cursor="arrow")
        self.ProficiencyBonusEntry.grid(row=0, column=7, padx=2, pady=2)

        # Spellcaster Checkbox
        self.SpellcasterBox = Checkbutton(self.CharacterSheetHeaderFrame, text="Spellcaster", variable=self.SpellcasterBoxVar, command=self.SpellcasterToggle)
        self.SpellcasterBox.grid(row=0, column=8, padx=2, pady=2)

        # Experience
        self.CharacterExperienceLabel = Label(self.CharacterSheetHeaderFrame, text="Exp.:")
        self.CharacterExperienceLabel.grid(row=0, column=10)
        self.CharacterExperienceEntry = Entry(self.CharacterSheetHeaderFrame, textvariable=self.CharacterExperienceEntryVar, width=7, justify=CENTER)
        self.CharacterExperienceEntry.grid(row=0, column=11, padx=2, pady=2)
        self.CharacterExperienceNeededLabel = Label(self.CharacterSheetHeaderFrame, text="Needed Exp.:")
        self.CharacterExperienceNeededLabel.grid(row=0, column=12)
        self.CharacterExperienceNeededEntry = Entry(self.CharacterSheetHeaderFrame, textvariable=self.CharacterExperienceNeededEntryVar, state=DISABLED, justify=CENTER, width=7, disabledbackground="light gray",
                                                    disabledforeground="black", cursor="arrow")
        self.CharacterExperienceNeededEntry.grid(row=0, column=13, padx=2, pady=2)

        # Add Saved Fields to Character Data Dictionary
        GlobalInst.SavedData["CharacterNameEntryVar"] = self.CharacterNameEntryVar
        GlobalInst.SavedData["CharacterLevelEntryVar"] = self.CharacterLevelEntryVar
        GlobalInst.SavedData["CharacterClassEntryVar"] = self.CharacterClassEntryVar
        GlobalInst.SavedData["CharacterExperienceEntryVar"] = self.CharacterExperienceEntryVar
        GlobalInst.SavedData["SpellcasterBoxVar"] = self.SpellcasterBoxVar

    def SpellcasterToggle(self):
        Spellcaster = self.SpellcasterBoxVar.get()
        if Spellcaster:
            CharacterStatsInventoryAndNotesInst.CharacterStatsNotebook.add(CharacterStatsInventoryAndNotesInst.SpellcastingPage)
        if not Spellcaster:
            CharacterStatsInventoryAndNotesInst.CharacterStatsNotebook.hide(2)

    def ValidLevelEntry(self):
        try:
            CharacterLevelValue = GlobalInst.GetStringVarAsNumber(self.CharacterLevelEntryVar)
        except:
            messagebox.showerror("Invalid Entry", "Character level must be an integer.")
            return False
        if CharacterLevelValue <= 0 or CharacterLevelValue >= 21:
            messagebox.showerror("Invalid Entry", "Character level must be between 1 and 20.")
            return False
        return True


class CharacterStatsInventoryAndNotes:
    def __init__(self, master):
        # Character Stats Frame
        self.CharacterStatsFrame = LabelFrame(master, text="Character Stats, Inventory, and Notes:")
        self.CharacterStatsFrame.grid(row=1, column=0, rowspan=2, padx=2, pady=2, sticky=NSEW)

        # Character Stats Notebook
        self.CharacterStatsNotebook = ttk.Notebook(self.CharacterStatsFrame, height=500)
        self.CharacterStatsNotebook.grid(row=0, column=0)
        self.CharacterStatsNotebook.enable_traversal()

        # Abilities and Skills Page
        self.AbilitiesAndSkillsPage = Frame(self.CharacterStatsNotebook)
        self.CharacterStatsNotebook.add(self.AbilitiesAndSkillsPage, text="Abilities and Skills")
        self.AbilitiesAndSkillsInst = self.AbilitiesAndSkills(self.AbilitiesAndSkillsPage)

        # Combat and Features
        self.CombatAndFeaturesPage = Frame(self.CharacterStatsNotebook)
        self.CharacterStatsNotebook.add(self.CombatAndFeaturesPage, text="Combat and Features")
        self.CombatAndFeaturesInst = self.CombatAndFeatures(self.CombatAndFeaturesPage)

        # Spellcasting
        self.SpellcastingPage = Frame(self.CharacterStatsNotebook)
        self.CharacterStatsNotebook.add(self.SpellcastingPage, text="Spellcasting")
        self.SpellcastingInst = self.Spellcasting(self.SpellcastingPage)

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
            self.PassivePerceptionEntryVar = StringVar()
            self.PassiveInvestigationEntryVar = StringVar()
            self.PassivePerceptionManualBonusEntryVar = StringVar()
            self.PassiveInvestigationManualBonusEntryVar = StringVar()
            self.JackOfAllTradesBoxVar = BooleanVar()
            self.RemarkableAthleteBoxVar = BooleanVar()

            # Center Abilities, Saving Throws, and Skills
            master.grid_rowconfigure(0, weight=1)
            master.grid_rowconfigure(2, weight=1)
            master.grid_rowconfigure(4, weight=1)
            master.grid_rowconfigure(6, weight=1)
            master.grid_columnconfigure(0, weight=1)
            master.grid_columnconfigure(2, weight=1)
            master.grid_columnconfigure(4, weight=1)
            master.grid_columnconfigure(6, weight=1)
            master.grid_columnconfigure(8, weight=1)

            # Abilities and Saving Throws
            self.AbilitiesAndSavingThrowsFrame = LabelFrame(master, text="Abilities and Saving Throws:")
            self.AbilitiesAndSavingThrowsFrame.grid(row=1, column=1, padx=2, pady=2, columnspan=3)
            self.AbilitiesAndSavingThrowsInst = self.AbilitiesAndSavingThrowsTable(self.AbilitiesAndSavingThrowsFrame)

            # Passive Perception
            self.PassivePerceptionFrame = LabelFrame(master, text="Passive Perception:")
            self.PassivePerceptionFrame.grid_columnconfigure(0, weight=1)
            self.PassivePerceptionFrame.grid(row=3, column=1, padx=2, pady=2)
            self.PassivePerceptionEntry = Entry(self.PassivePerceptionFrame, state=DISABLED, justify=CENTER, width=20, disabledbackground=GlobalInst.ButtonColor, disabledforeground="black", cursor="arrow",
                                                textvariable=self.PassivePerceptionEntryVar)
            self.PassivePerceptionEntry.bind("<Button-1>", self.ConfigurePassivePerception)
            self.PassivePerceptionEntry.grid(row=0, column=0, sticky=NSEW)

            # Passive Investigation
            self.PassiveInvestigationFrame = LabelFrame(master, text="Passive Investigation:")
            self.PassiveInvestigationFrame.grid_columnconfigure(0, weight=1)
            self.PassiveInvestigationFrame.grid(row=3, column=3, padx=2, pady=2)
            self.PassiveInvestigationEntry = Entry(self.PassiveInvestigationFrame, state=DISABLED, justify=CENTER, width=20, disabledbackground=GlobalInst.ButtonColor, disabledforeground="black", cursor="arrow",
                                                   textvariable=self.PassiveInvestigationEntryVar)
            self.PassiveInvestigationEntry.bind("<Button-1>", self.ConfigurePassiveInvestigation)
            self.PassiveInvestigationEntry.grid(row=0, column=0, sticky=NSEW)

            # Jack of All Trades
            self.JackOfAllTradesBox = Checkbutton(master, text="Jack of All Trades", variable=self.JackOfAllTradesBoxVar)
            self.JackOfAllTradesBox.grid(row=5, column=1, padx=2, pady=2)

            # Remarkable Athlete
            self.RemarkableAthleteBox = Checkbutton(master, text="Remarkable Athlete", variable=self.RemarkableAthleteBoxVar)
            self.RemarkableAthleteBox.grid(row=5, column=3, padx=2, pady=2)

            # Skills
            self.SkillsFrame = LabelFrame(master, text="Skills:")
            self.SkillsFrame.grid(row=1, column=5, padx=2, pady=2, rowspan=5, sticky=NSEW)
            self.SkillsInst = self.SkillsTable(self.SkillsFrame)

            # Proficiencies Frame
            self.ProficienciesFrame = LabelFrame(master, text="Proficiencies:")
            self.ProficienciesFrame.grid(row=1, column=7, padx=2, pady=2, rowspan=5, sticky=NSEW)

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

            # Add Saved Fields to Character Data Dictionary
            GlobalInst.SavedData["PassivePerceptionManualBonusEntryVar"] = self.PassivePerceptionManualBonusEntryVar
            GlobalInst.SavedData["PassiveInvestigationManualBonusEntryVar"] = self.PassiveInvestigationManualBonusEntryVar
            GlobalInst.SavedData["ProficienciesWeaponsField"] = self.ProficienciesWeaponsField
            GlobalInst.SavedData["ProficienciesArmorField"] = self.ProficienciesArmorField
            GlobalInst.SavedData["ProficienciesToolsAndInstrumentsField"] = self.ProficienciesToolsAndInstrumentsField
            GlobalInst.SavedData["ProficienciesLanguagesField"] = self.ProficienciesLanguagesField
            GlobalInst.SavedData["ProficienciesOtherField"] = self.ProficienciesOtherField
            GlobalInst.SavedData["JackOfAllTradesBoxVar"] = self.JackOfAllTradesBoxVar
            GlobalInst.SavedData["RemarkableAthleteBoxVar"] = self.RemarkableAthleteBoxVar

        def ConfigurePassivePerception(self, event):
            # Test Level Input Validity
            if CharacterSheetHeaderInst.ValidLevelEntry():
                pass
            else:
                return

            # Test Ability Input Validity
            if CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.ValidStatsEntry():
                pass
            else:
                return

            # Create Config Window and Wait
            PassivePerceptionDataInst = ManualBonusData(root, self.PassivePerceptionManualBonusEntryVar, "Passive Perception")
            root.wait_window(PassivePerceptionDataInst.Window)

            # Handle Values
            if PassivePerceptionDataInst.DataSubmitted.get():
                PassivePerceptionDataInst.GetData(self.PassivePerceptionManualBonusEntryVar)

            # Update Stats and Inventory
            GlobalInst.UpdateStatsAndInventory()

        def ConfigurePassiveInvestigation(self, event):
            # Test Level Input Validity
            if CharacterSheetHeaderInst.ValidLevelEntry():
                pass
            else:
                return

            # Test Ability Input Validity
            if CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.ValidStatsEntry():
                pass
            else:
                return

            # Create Config Window and Wait
            PassiveInvestigationDataInst = ManualBonusData(root, self.PassiveInvestigationManualBonusEntryVar, "Passive Investigation")
            root.wait_window(PassiveInvestigationDataInst.Window)

            # Handle Values
            if PassiveInvestigationDataInst.DataSubmitted.get():
                PassiveInvestigationDataInst.GetData(self.PassiveInvestigationManualBonusEntryVar)

            # Update Stats and Inventory
            GlobalInst.UpdateStatsAndInventory()

        # Abilities and Saving Throws
        class AbilitiesAndSavingThrowsTable:
            def __init__(self, master):
                self.PointBuyBoxVar = BooleanVar()

                # Labels
                self.AbilitiesHeaderAbility = Label(master, text="Ability", bd=2, relief=GROOVE)
                self.AbilitiesHeaderTotal = Label(master, text="Total", bd=2, relief=GROOVE)
                self.AbilitiesHeaderModifier = Label(master, text="Modifier", bd=2, relief=GROOVE)
                self.AbilitiesHeaderSpacer = Frame(master, width=15)
                self.AbilitiesHeaderSpacer.grid(rowspan=6, column=3)
                self.AbilitiesHeaderSavingThrowsProf = Label(master, text="Prof.", bd=2, relief=GROOVE)
                self.AbilitiesHeaderSavingThrowsProf.grid(row=0, column=4, sticky=NSEW)
                self.AbilitiesHeaderSavingThrows = Label(master, text="Saving Throws", bd=2, relief=GROOVE)
                self.AbilitiesHeaderSavingThrows.grid(row=0, column=5, sticky=NSEW)
                self.AbilitiesHeaderAbility.grid(row=0, column=0, sticky=NSEW)
                self.AbilitiesHeaderTotal.grid(row=0, column=1, sticky=NSEW)
                self.AbilitiesHeaderModifier.grid(row=0, column=2, sticky=NSEW)

                # Ability Entries List
                self.AbilityEntriesList = []

                # Ability Entries
                self.StrengthEntry = self.AbilitiesAndSavingThrowsEntry(master, "Strength", self.AbilityEntriesList, 1)
                self.DexterityEntry = self.AbilitiesAndSavingThrowsEntry(master, "Dexterity", self.AbilityEntriesList, 2)
                self.ConstitutionEntry = self.AbilitiesAndSavingThrowsEntry(master, "Constitution", self.AbilityEntriesList, 3)
                self.IntelligenceEntry = self.AbilitiesAndSavingThrowsEntry(master, "Intelligence", self.AbilityEntriesList, 4)
                self.WisdomEntry = self.AbilitiesAndSavingThrowsEntry(master, "Wisdom", self.AbilityEntriesList, 5)
                self.CharismaEntry = self.AbilitiesAndSavingThrowsEntry(master, "Charisma", self.AbilityEntriesList, 6)

                # Abilities Data Config
                self.AbilitiesDataConfigButton = Button(master, text="Abilities Data", command=self.ConfigureAbilitiesData, bg=GlobalInst.ButtonColor)
                self.AbilitiesDataConfigButton.grid(row=7, column=0, columnspan=6, padx=2, pady=2, sticky=NSEW)

                # Abilities Notes
                self.AbilitiesNotesFrame = LabelFrame(master, text="Abilities Notes:")
                self.AbilitiesNotesFrame.grid(row=8, column=0, columnspan=6, padx=2, pady=2)
                self.AbilitiesNotes = ScrolledText(self.AbilitiesNotesFrame, Width=275, Height=150)
                self.AbilitiesNotes.grid(row=0, column=0)

                # Add Saved Fields to Character Data Dictionary
                GlobalInst.SavedData["PointBuyBoxVar"] = self.PointBuyBoxVar
                GlobalInst.SavedData["AbilitiesNotes"] = self.AbilitiesNotes

            def ValidStatsEntry(self):
                try:
                    StrengthBaseValue = GlobalInst.GetStringVarAsNumber(self.StrengthEntry.AbilityEntryTotalVar)
                    DexterityBaseValue = GlobalInst.GetStringVarAsNumber(self.DexterityEntry.AbilityEntryTotalVar)
                    ConstitutionBaseValue = GlobalInst.GetStringVarAsNumber(self.ConstitutionEntry.AbilityEntryTotalVar)
                    IntelligenceBaseValue = GlobalInst.GetStringVarAsNumber(self.IntelligenceEntry.AbilityEntryTotalVar)
                    WisdomBaseValue = GlobalInst.GetStringVarAsNumber(self.WisdomEntry.AbilityEntryTotalVar)
                    CharismaBaseValue = GlobalInst.GetStringVarAsNumber(self.CharismaEntry.AbilityEntryTotalVar)
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
                    self.AbilityEntryModifier = Entry(master, width=3, justify=CENTER, textvariable=self.AbilityEntryModifierVar, state=DISABLED, disabledbackground=GlobalInst.ButtonColor, disabledforeground="black",
                                                      cursor="dotbox")
                    self.AbilityEntryModifier.grid(row=Row, column=2, sticky=NSEW)
                    self.AbilityEntryModifier.bind("<Button-1>", self.RollAbility)

                    # Saving Throw Proficiency Box
                    self.AbilitySavingThrowProficiencyBox = Checkbutton(master, variable=self.AbilitySavingThrowProficiencyBoxVar)
                    self.AbilitySavingThrowProficiencyBox.grid(row=Row, column=4)

                    # Saving Throw Modifier Entry
                    self.AbilitySavingThrowModifier = Entry(master, width=3, justify=CENTER, textvariable=self.AbilitySavingThrowModifierVar, state=DISABLED, disabledbackground=GlobalInst.ButtonColor, disabledforeground="black",
                                                            cursor="dotbox")
                    self.AbilitySavingThrowModifier.grid(row=Row, column=5, sticky=NSEW)
                    self.AbilitySavingThrowModifier.bind("<Button-1>", self.RollSavingThrow)

                    # Add Saved Fields to Character Data Dictionary
                    GlobalInst.SavedData[AbilityName + "AbilityEntryTotalVar"] = self.AbilityEntryTotalVar
                    GlobalInst.SavedData[AbilityName + "AbilityBaseVar"] = self.AbilityBaseVar
                    GlobalInst.SavedData[AbilityName + "AbilityRacialVar"] = self.AbilityRacialVar
                    GlobalInst.SavedData[AbilityName + "AbilityASIVar"] = self.AbilityASIVar
                    GlobalInst.SavedData[AbilityName + "AbilityMiscVar"] = self.AbilityMiscVar
                    GlobalInst.SavedData[AbilityName + "AbilityOverrideVar"] = self.AbilityOverrideVar
                    GlobalInst.SavedData[AbilityName + "AbilitySavingThrowProficiencyBoxVar"] = self.AbilitySavingThrowProficiencyBoxVar

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
                    BaseModifier = GlobalInst.GetStringVarAsNumber(self.AbilityEntryModifierVar)
                    JackOfAllTradesModifier = BaseModifier
                    RemarkableAthleteModifier = BaseModifier
                    ProficiencyBonus = GlobalInst.GetStringVarAsNumber(CharacterSheetHeaderInst.ProficiencyBonusEntryVar)
                    AbilityName = self.AbilityNameVar.get()
                    if CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.RemarkableAthleteBoxVar.get():
                        if AbilityName == "Strength" or AbilityName == "Dexterity" or AbilityName == "Constitution":
                            RemarkableAthleteModifier += math.ceil(ProficiencyBonus / 2)
                    if CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.JackOfAllTradesBoxVar.get():
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
                    self.PointBuyBoxVar = BooleanVar(value=CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.PointBuyBoxVar.get())
                    self.PointBuyEntryVar = StringVar()

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
                    self.StrengthConfigEntry = self.AbilitiesDataConfigEntry(self.Window, CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.StrengthEntry, "STR", self.EntriesList, 1)
                    self.DexterityConfigEntry = self.AbilitiesDataConfigEntry(self.Window, CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.DexterityEntry, "DEX", self.EntriesList, 2)
                    self.ConstitutionConfigEntry = self.AbilitiesDataConfigEntry(self.Window, CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.ConstitutionEntry, "CON", self.EntriesList, 3)
                    self.IntelligenceConfigEntry = self.AbilitiesDataConfigEntry(self.Window, CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.IntelligenceEntry, "INT", self.EntriesList, 4)
                    self.WisdomConfigEntry = self.AbilitiesDataConfigEntry(self.Window, CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.WisdomEntry, "WIS", self.EntriesList, 5)
                    self.CharismaConfigEntry = self.AbilitiesDataConfigEntry(self.Window, CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.CharismaEntry, "CHA", self.EntriesList, 6)

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
                    self.RollButton = Button(self.Window, text="Roll", command=self.RollForAbilities, bg=GlobalInst.ButtonColor)
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
                    GlobalInst.WindowGeometry(self.Window, True)
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

                def RollForAbilities(self):
                    # Create Window and Wait
                    RollForAbilitiesMenuInst = self.RollForAbilitiesMenu(self.Window)
                    root.wait_window(RollForAbilitiesMenuInst.Window)

                    # Handle Variables
                    if RollForAbilitiesMenuInst.DataSubmitted.get():
                        for Assignment in RollForAbilitiesMenuInst.RollAssignFieldsList:
                            for Entry in self.EntriesList:
                                RollLabelVar = Assignment.RollLabelVar.get()
                                RollDropdownVar = Assignment.RollDropdownVar.get()
                                if Entry.AbilityNameShort == RollDropdownVar:
                                    Entry.AbilityBaseVar.set(RollLabelVar)

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
                        Base = GlobalInst.GetStringVarAsNumber(self.AbilityBaseVar)
                        Valid = True
                        if Base < 8 or Base > 15:
                            Valid = False
                        return Valid

                class RollForAbilitiesMenu:
                    def __init__(self, master):
                        self.DataSubmitted = BooleanVar()
                        self.Rolled = False

                        # Create Window
                        self.Window = Toplevel(master)
                        self.Window.wm_attributes("-toolwindow", 1)
                        self.Window.wm_title("Roll for Abilities")

                        # Roll Assign Fields List
                        self.RollAssignFieldsList = []

                        # Roll Assign Fields
                        self.RollAssignField1Inst = self.RollAssignField(self.Window, self.RollAssignFieldsList, Row=0, Column=0)
                        self.RollAssignField2Inst = self.RollAssignField(self.Window, self.RollAssignFieldsList, Row=0, Column=1)
                        self.RollAssignField3Inst = self.RollAssignField(self.Window, self.RollAssignFieldsList, Row=0, Column=2)
                        self.RollAssignField4Inst = self.RollAssignField(self.Window, self.RollAssignFieldsList, Row=1, Column=0)
                        self.RollAssignField5Inst = self.RollAssignField(self.Window, self.RollAssignFieldsList, Row=1, Column=1)
                        self.RollAssignField6Inst = self.RollAssignField(self.Window, self.RollAssignFieldsList, Row=1, Column=2)

                        # Buttons
                        self.RollScoresButton = Button(self.Window, text="Roll\nScores", command=self.RollScores, bg=GlobalInst.ButtonColor)
                        self.RollScoresButton.grid(row=0, column=3, rowspan=2, padx=2, pady=2, sticky=NSEW)
                        self.ButtonsFrame = Frame(self.Window)
                        self.ButtonsFrame.grid_columnconfigure(0, weight=1)
                        self.ButtonsFrame.grid_columnconfigure(1, weight=1)
                        self.ButtonsFrame.grid(row=2, column=0, columnspan=4, sticky=NSEW)
                        self.SubmitButton = Button(self.ButtonsFrame, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
                        self.SubmitButton.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)
                        self.CancelButton = Button(self.ButtonsFrame, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
                        self.CancelButton.grid(row=0, column=1, padx=2, pady=2, sticky=NSEW)

                        # Prevent Main Window Input
                        self.Window.grab_set()

                        # Handle Config Window Geometry and Focus
                        GlobalInst.WindowGeometry(self.Window, True)
                        self.Window.focus_force()

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
                # Labels
                self.SkillsHeaderProficiency = Label(master, text="Prof.", bd=2, relief=GROOVE)
                self.SkillsHeaderProficiency.grid(row=0, column=0, sticky=NSEW)
                self.SkillsHeaderSkills = Label(master, text="Skill", bd=2, relief=GROOVE)
                self.SkillsHeaderSkills.grid(row=0, column=1, sticky=NSEW)
                self.SkillsHeaderModifier = Label(master, text="Modifier", bd=2, relief=GROOVE)
                self.SkillsHeaderModifier.grid(row=0, column=2, sticky=NSEW)

                # Entries List
                self.SkillsEntriesList = []

                # Entries
                self.SkillsEntryAcrobaticsInst = self.SkillsEntry(master, "Acrobatics (DEX)", self.SkillsEntriesList, 1)
                self.SkillsEntryAnimalHandlingInst = self.SkillsEntry(master, "Animal Handling (WIS)", self.SkillsEntriesList, 2)
                self.SkillsEntryArcanaInst = self.SkillsEntry(master, "Arcana (INT)", self.SkillsEntriesList, 3)
                self.SkillsEntryAthleticsInst = self.SkillsEntry(master, "Athletics (STR)", self.SkillsEntriesList, 4)
                self.SkillsEntryDeceptionInst = self.SkillsEntry(master, "Deception (CHA)", self.SkillsEntriesList, 5)
                self.SkillsEntryHistoryInst = self.SkillsEntry(master, "History (INT)", self.SkillsEntriesList, 6)
                self.SkillsEntryInsightInst = self.SkillsEntry(master, "Insight (WIS)", self.SkillsEntriesList, 7)
                self.SkillsEntryIntimidationInst = self.SkillsEntry(master, "Intimidation (CHA)", self.SkillsEntriesList, 8)
                self.SkillsEntryInvestigationInst = self.SkillsEntry(master, "Investigation (INT)", self.SkillsEntriesList, 9)
                self.SkillsEntryMedicineInst = self.SkillsEntry(master, "Medicine (WIS)", self.SkillsEntriesList, 10)
                self.SkillsEntryNatureInst = self.SkillsEntry(master, "Nature (INT)", self.SkillsEntriesList, 11)
                self.SkillsEntryPerceptionInst = self.SkillsEntry(master, "Perception (WIS)", self.SkillsEntriesList, 12)
                self.SkillsEntryPerformanceInst = self.SkillsEntry(master, "Performance (CHA)", self.SkillsEntriesList, 13)
                self.SkillsEntryPersuasionInst = self.SkillsEntry(master, "Persuasion (CHA)", self.SkillsEntriesList, 14)
                self.SkillsEntryReligionInst = self.SkillsEntry(master, "Religion (INT)", self.SkillsEntriesList, 15)
                self.SkillsEntrySleightOfHandInst = self.SkillsEntry(master, "Sleight of Hand (DEX)", self.SkillsEntriesList, 16)
                self.SkillsEntryStealthInst = self.SkillsEntry(master, "Stealth (DEX)", self.SkillsEntriesList, 17)
                self.SkillsEntrySurvivalInst = self.SkillsEntry(master, "Survival (WIS)", self.SkillsEntriesList, 18)

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
                    self.ModifierEntry = Entry(master, textvariable=self.TotalModifierVar, width=3, disabledforeground="black", disabledbackground=GlobalInst.ButtonColor, state=DISABLED, justify=CENTER, cursor="dotbox")
                    self.ModifierEntry.grid(row=Row, column=2, sticky=NSEW)
                    self.ModifierEntry.bind("<Button-1>", self.RollSkill)

                    # Add Saved Fields to Character Data Dictionary
                    GlobalInst.SavedData[SkillName + "SkillProficiency1"] = self.ProficiencyBox1Var
                    GlobalInst.SavedData[SkillName + "SkillProficiency2"] = self.ProficiencyBox2Var

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
                    BaseModifier = GlobalInst.GetStringVarAsNumber(self.TotalModifierVar)
                    JackOfAllTradesModifier = BaseModifier
                    RemarkableAthleteModifier = BaseModifier
                    ProficiencyBonus = GlobalInst.GetStringVarAsNumber(CharacterSheetHeaderInst.ProficiencyBonusEntryVar)
                    Proficiency1 = self.ProficiencyBox1Var.get()
                    Proficiency2 = self.ProficiencyBox2Var.get()
                    SkillName = self.SkillNameVar.get()
                    if not Proficiency1 and not Proficiency2 and CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.RemarkableAthleteBoxVar.get():
                        if SkillName.endswith("(STR)") or SkillName.endswith("(DEX)") or SkillName.endswith("(CON)"):
                            RemarkableAthleteModifier += math.ceil(ProficiencyBonus / 2)
                    if not Proficiency1 and not Proficiency2 and CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.JackOfAllTradesBoxVar.get():
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
            self.ACBaseEntryVar = StringVar()
            self.ACModifierVar = StringVar()
            self.ACManualBonusEntryVar = StringVar()
            self.InitiativeEntryVar = StringVar()
            self.SpeedEntryVar = StringVar()
            self.InitiativeManualBonusEntryVar = StringVar()

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
            self.DamageButton = Button(self.VitalityFrame, text="Damage", bg=GlobalInst.ButtonColor, command=self.Damage)
            self.DamageButton.grid(row=3, column=0, columnspan=2, sticky=NSEW, padx=2, pady=2)

            # Heal Button
            self.HealButton = Button(self.VitalityFrame, text="Heal", bg=GlobalInst.ButtonColor, command=self.Heal)
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
            self.ACInitiativeSpeedFrame.grid_rowconfigure(1, weight=1)
            self.ACInitiativeSpeedFrame.grid_rowconfigure(3, weight=1)
            self.ACInitiativeSpeedFrame.grid(row=1, column=3, sticky=NSEW)

            # AC
            self.ACFrame = LabelFrame(self.ACInitiativeSpeedFrame, text="AC:")
            self.ACFrame.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
            self.ACEntry = Entry(self.ACFrame, width=9, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground=GlobalInst.ButtonColor, textvariable=self.ACEntryVar, cursor="arrow")
            self.ACEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
            self.ACEntry.bind("<Button-1>", self.ConfigureAC)

            # Initiative
            self.InitiativeFrame = LabelFrame(self.ACInitiativeSpeedFrame, text="Initiative:")
            self.InitiativeFrame.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)
            self.InitiativeEntry = Entry(self.InitiativeFrame, width=9, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground=GlobalInst.ButtonColor, textvariable=self.InitiativeEntryVar, cursor="dotbox")
            self.InitiativeEntry.bind("<Button-1>", self.RollInitiative)
            self.InitiativeEntry.bind("<Button-3>", self.ConfigureInitiative)
            self.InitiativeEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

            # Speed
            self.SpeedFrame = LabelFrame(self.ACInitiativeSpeedFrame, text="Speed:")
            self.SpeedFrame.grid(row=4, column=0, sticky=N, padx=2, pady=2)
            self.SpeedEntry = Entry(self.SpeedFrame, width=9, justify=CENTER, textvariable=self.SpeedEntryVar)
            self.SpeedEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

            # Offense Notes
            self.OffenseNotesFrame = LabelFrame(master, text="Offense Notes:")
            self.OffenseNotesFrame.grid(row=3, column=1, padx=2, pady=2, columnspan=3)
            self.OffenseNotes = ScrolledText(self.OffenseNotesFrame, Height=140, Width=330)
            self.OffenseNotes.grid(row=0, column=0)

            # Defense Notes
            self.DefenseNotesFrame = LabelFrame(master, text="Defense Notes:")
            self.DefenseNotesFrame.grid(row=5, column=1, padx=2, pady=2, columnspan=3)
            self.DefenseNotes = ScrolledText(self.DefenseNotesFrame, Height=140, Width=330)
            self.DefenseNotes.grid(row=0, column=0)

            # Features
            self.FeaturesAndCreatureStatsInst = self.FeaturesAndCreatureStats(master)

            # Features Notes
            self.FeaturesNotesFrame = LabelFrame(master, text="Features Notes:")
            self.FeaturesNotesFrame.grid(row=5, column=5, columnspan=2, padx=2, pady=2)
            self.FeaturesNotes = ScrolledText(self.FeaturesNotesFrame, Height=140, Width=330)
            self.FeaturesNotes.grid(row=0, column=0)

            # Add Saved Fields to Character Data Dictionary
            GlobalInst.SavedData["TempHPEntryVar"] = self.TempHPEntryVar
            GlobalInst.SavedData["CurrentHPEntryVar"] = self.CurrentHPEntryVar
            GlobalInst.SavedData["MaxHPEntryVar"] = self.MaxHPEntryVar
            GlobalInst.SavedData["HitDiceEntryVar"] = self.HitDiceEntryVar
            GlobalInst.SavedData["HitDiceRemainingEntryVar"] = self.HitDiceRemainingEntryVar
            GlobalInst.SavedData["DeathSavingThrowsBoxSuccess1Var"] = self.DeathSavingThrowsBoxSuccess1Var
            GlobalInst.SavedData["DeathSavingThrowsBoxSuccess2Var"] = self.DeathSavingThrowsBoxSuccess2Var
            GlobalInst.SavedData["DeathSavingThrowsBoxSuccess3Var"] = self.DeathSavingThrowsBoxSuccess3Var
            GlobalInst.SavedData["DeathSavingThrowsBoxFailure1Var"] = self.DeathSavingThrowsBoxFailure1Var
            GlobalInst.SavedData["DeathSavingThrowsBoxFailure2Var"] = self.DeathSavingThrowsBoxFailure2Var
            GlobalInst.SavedData["DeathSavingThrowsBoxFailure3Var"] = self.DeathSavingThrowsBoxFailure3Var
            GlobalInst.SavedData["ACBaseEntryVar"] = self.ACBaseEntryVar
            GlobalInst.SavedData["ACModifierVar"] = self.ACModifierVar
            GlobalInst.SavedData["ACManualBonusEntryVar"] = self.ACManualBonusEntryVar
            GlobalInst.SavedData["InitiativeManualBonusEntryVar"] = self.InitiativeManualBonusEntryVar
            GlobalInst.SavedData["SpeedEntryVar"] = self.SpeedEntryVar
            GlobalInst.SavedData["OffenseNotes.Text"] = self.OffenseNotes
            GlobalInst.SavedData["DefenseNotes.Text"] = self.DefenseNotes
            GlobalInst.SavedData["FeaturesNotes"] = self.FeaturesNotes

        def Damage(self):
            if self.ValidLifeValues():
                pass
            else:
                return
            CurrentTempHP = GlobalInst.GetStringVarAsNumber(self.TempHPEntryVar)
            CurrentHP = GlobalInst.GetStringVarAsNumber(self.CurrentHPEntryVar)
            DamagePrompt = IntegerPrompt(root, "Damage", "How much damage?", MinValue=1)
            root.wait_window(DamagePrompt.Window)
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
            HealingPrompt = IntegerPrompt(root, "Heal", "How much healing?", MinValue=1)
            root.wait_window(HealingPrompt.Window)
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

        def ConfigureAC(self, event):
            # Test Level Input Validity
            if CharacterSheetHeaderInst.ValidLevelEntry():
                pass
            else:
                return

            # Test Ability Input Validity
            if CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.ValidStatsEntry():
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
            GlobalInst.UpdateStatsAndInventory()

        def ConfigureInitiative(self, event):
            # Test Level Input Validity
            if CharacterSheetHeaderInst.ValidLevelEntry():
                pass
            else:
                return

            # Test Ability Input Validity
            if CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.ValidStatsEntry():
                pass
            else:
                return

            # Create Config Window and Wait
            InitiativeConfigInst = ManualBonusData(root, self.InitiativeManualBonusEntryVar, "Initiative")
            root.wait_window(InitiativeConfigInst.Window)

            # Handle Values
            if InitiativeConfigInst.DataSubmitted.get():
                self.InitiativeManualBonusEntryVar.set(InitiativeConfigInst.ManualBonusEntryVar.get())

            # Update Stats and Inventory
            GlobalInst.UpdateStatsAndInventory()

        def RollInitiative(self, event):
            DiceRollerInst.DiceNumberEntryVar.set(1)
            DiceRollerInst.DieTypeEntryVar.set(20)
            DiceRollerInst.ModifierEntryVar.set(str(GlobalInst.GetStringVarAsNumber(self.InitiativeEntryVar)))
            DiceRollerInst.Roll("Initiative:\n")

        class FeaturesAndCreatureStats:
            def __init__(self, master):
                # Features Frame
                self.FeaturesFrame = LabelFrame(master, text="Features and Creature Stats:")
                self.FeaturesFrame.grid(row=1, column=5, rowspan=3, sticky=NSEW, padx=2, pady=2)

                # Features Scrolled Canvas
                self.FeaturesScrolledCanvas = ScrolledCanvas(self.FeaturesFrame, Height=310, Width=313)

                # Features Entries List
                self.FeaturesEntriesList = []

                # Features Entries
                for CurrentIndex in range(100):
                    self.FeatureOrCreatureStatsEntry(self.FeaturesScrolledCanvas.WindowFrame, self.FeaturesEntriesList, CurrentIndex + 1)

            class FeatureOrCreatureStatsEntry:
                def __init__(self, master, List, Row):
                    self.Row = Row
                    self.NameEntryVar = StringVar()
                    self.SizeTagsAndAlignmentEntryVar = StringVar()
                    self.FeatureDescriptionVar = StringVar()
                    self.MaxHPEntryVar = StringVar()
                    self.ACEntryVar = StringVar()
                    self.SpeedEntryVar = StringVar()
                    self.CREntryVar = StringVar()
                    self.SkillSensesAndLanguagesFieldVar = StringVar()
                    self.FeaturesFieldVar = StringVar()
                    self.ActionsAndReactionsFieldVar = StringVar()
                    self.InventoryAndNotesFieldVar = StringVar()
                    self.AbilitiesStrengthEntryVar = StringVar()
                    self.AbilitiesDexterityEntryVar = StringVar()
                    self.AbilitiesConstitutionEntryVar = StringVar()
                    self.AbilitiesIntelligenceEntryVar = StringVar()
                    self.AbilitiesWisdomEntryVar = StringVar()
                    self.AbilitiesCharismaEntryVar = StringVar()

                    # Set Row Size
                    master.grid_rowconfigure(self.Row, minsize=26)

                    # Add to List
                    List.append(self)

                    # Name Entry
                    self.NameEntry = Entry(master, width=51, justify=CENTER, state=DISABLED, disabledbackground=GlobalInst.ButtonColor, disabledforeground="black", textvariable=self.NameEntryVar, cursor="arrow")
                    self.NameEntry.grid(row=self.Row, column=0, sticky=NSEW)
                    self.NameEntry.bind("<Button-1>", self.SetFeature)
                    self.NameEntry.bind("<Button-3>", self.SetCreatureStats)

                    # Add Saved Fields to Character Data Dictionary
                    GlobalInst.SavedData["FeatureOrCreatureStatsEntryName" + str(self.Row)] = self.NameEntryVar
                    GlobalInst.SavedData["FeatureEntryDescription" + str(self.Row)] = self.FeatureDescriptionVar
                    GlobalInst.SavedData["CreatureMaxHPEntryVar" + str(self.Row)] = self.MaxHPEntryVar
                    GlobalInst.SavedData["CreatureACEntryVar" + str(self.Row)] = self.ACEntryVar
                    GlobalInst.SavedData["CreatureSpeedEntryVar" + str(self.Row)] = self.SpeedEntryVar
                    GlobalInst.SavedData["CreatureCREntryVar" + str(self.Row)] = self.CREntryVar
                    GlobalInst.SavedData["CreatureSkillSensesAndLanguagesFieldVar" + str(self.Row)] = self.SkillSensesAndLanguagesFieldVar
                    GlobalInst.SavedData["CreatureFeaturesFieldVar" + str(self.Row)] = self.FeaturesFieldVar
                    GlobalInst.SavedData["CreatureActionsAndReactionsFieldVar" + str(self.Row)] = self.ActionsAndReactionsFieldVar
                    GlobalInst.SavedData["CreatureInventoryAndNotesFieldVar" + str(self.Row)] = self.InventoryAndNotesFieldVar
                    GlobalInst.SavedData["CreatureAbilitiesStrengthEntryVar" + str(self.Row)] = self.AbilitiesStrengthEntryVar
                    GlobalInst.SavedData["CreatureAbilitiesDexterityEntryVar" + str(self.Row)] = self.AbilitiesDexterityEntryVar
                    GlobalInst.SavedData["CreatureAbilitiesConstitutionEntryVar" + str(self.Row)] = self.AbilitiesConstitutionEntryVar
                    GlobalInst.SavedData["CreatureAbilitiesIntelligenceEntryVar" + str(self.Row)] = self.AbilitiesIntelligenceEntryVar
                    GlobalInst.SavedData["CreatureAbilitiesWisdomEntryVar" + str(self.Row)] = self.AbilitiesWisdomEntryVar
                    GlobalInst.SavedData["CreatureAbilitiesCharismaEntryVar" + str(self.Row)] = self.AbilitiesCharismaEntryVar
                    GlobalInst.SavedData["CreatureSizeTagsAndAlignmentEntryVar" + str(self.Row)] = self.SizeTagsAndAlignmentEntryVar

                def SetFeature(self, event):
                    # Create Config Window and Wait
                    FeatureConfigInst = self.FeatureConfig(root, self.NameEntryVar, self.FeatureDescriptionVar)
                    root.wait_window(FeatureConfigInst.Window)

                    # Handle Values
                    if FeatureConfigInst.DataSubmitted.get():
                        self.NameEntryVar.set(FeatureConfigInst.NameEntryVar.get())
                        self.FeatureDescriptionVar.set(FeatureConfigInst.DescriptionVar.get())

                def SetCreatureStats(self, event):
                    # Create Config Window and Wait
                    CreatureStatsConfigInst = self.CreatureStatsConfig(root, self.NameEntryVar, self.SizeTagsAndAlignmentEntryVar, self.MaxHPEntryVar, self.ACEntryVar, self.SpeedEntryVar, self.CREntryVar,
                                                                       self.SkillSensesAndLanguagesFieldVar, self.FeaturesFieldVar, self.ActionsAndReactionsFieldVar, self.InventoryAndNotesFieldVar,
                                                                       self.AbilitiesStrengthEntryVar, self.AbilitiesDexterityEntryVar, self.AbilitiesConstitutionEntryVar, self.AbilitiesIntelligenceEntryVar,
                                                                       self.AbilitiesWisdomEntryVar, self.AbilitiesCharismaEntryVar)
                    root.wait_window(CreatureStatsConfigInst.Window)

                    # Handle Values
                    if CreatureStatsConfigInst.DataSubmitted.get():
                        self.NameEntryVar.set(CreatureStatsConfigInst.NameEntryVar.get())
                        self.SizeTagsAndAlignmentEntryVar.set(CreatureStatsConfigInst.SizeTagsAndAlignmentEntryVar.get())
                        self.MaxHPEntryVar.set(CreatureStatsConfigInst.MaxHPEntryVar.get())
                        self.ACEntryVar.set(CreatureStatsConfigInst.ACEntryVar.get())
                        self.SpeedEntryVar.set(CreatureStatsConfigInst.SpeedEntryVar.get())
                        self.CREntryVar.set(CreatureStatsConfigInst.CREntryVar.get())
                        self.SkillSensesAndLanguagesFieldVar.set(CreatureStatsConfigInst.SkillSensesAndLanguagesFieldVar.get())
                        self.FeaturesFieldVar.set(CreatureStatsConfigInst.FeaturesFieldVar.get())
                        self.ActionsAndReactionsFieldVar.set(CreatureStatsConfigInst.ActionsAndReactionsFieldVar.get())
                        self.InventoryAndNotesFieldVar.set(CreatureStatsConfigInst.InventoryAndNotesFieldVar.get())
                        self.AbilitiesStrengthEntryVar.set(CreatureStatsConfigInst.AbilitiesStrengthEntryVar.get())
                        self.AbilitiesDexterityEntryVar.set(CreatureStatsConfigInst.AbilitiesDexterityEntryVar.get())
                        self.AbilitiesConstitutionEntryVar.set(CreatureStatsConfigInst.AbilitiesConstitutionEntryVar.get())
                        self.AbilitiesIntelligenceEntryVar.set(CreatureStatsConfigInst.AbilitiesIntelligenceEntryVar.get())
                        self.AbilitiesWisdomEntryVar.set(CreatureStatsConfigInst.AbilitiesWisdomEntryVar.get())
                        self.AbilitiesCharismaEntryVar.set(CreatureStatsConfigInst.AbilitiesCharismaEntryVar.get())

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
                        GlobalInst.WindowGeometry(self.Window, True)
                        self.Window.focus_force()

                    def Submit(self):
                        self.DataSubmitted.set(True)
                        self.DescriptionVar.set(self.DescriptionField.get())
                        self.Window.destroy()

                    def Cancel(self):
                        self.DataSubmitted.set(False)
                        self.Window.destroy()

                class CreatureStatsConfig:
                    def __init__(self, master, NameEntryVar, SizeTagsAndAlignmentEntryVar, MaxHPEntryVar, ACEntryVar, SpeedEntryVar, CREntryVar, SkillSensesAndLanguagesFieldVar, FeaturesFieldVar, ActionsAndReactionsFieldVar,
                                 InventoryAndNotesFieldVar, AbilitiesStrengthEntryVar, AbilitiesDexterityEntryVar, AbilitiesConstitutionEntryVar, AbilitiesIntelligenceEntryVar, AbilitiesWisdomEntryVar,
                                 AbilitiesCharismaEntryVar):
                        self.DataSubmitted = BooleanVar()
                        self.NameEntryVar = StringVar(value=NameEntryVar.get())
                        self.SizeTagsAndAlignmentEntryVar = StringVar(value=SizeTagsAndAlignmentEntryVar.get())
                        self.MaxHPEntryVar = StringVar(value=MaxHPEntryVar.get())
                        self.ACEntryVar = StringVar(value=ACEntryVar.get())
                        self.SpeedEntryVar = StringVar(value=SpeedEntryVar.get())
                        self.CREntryVar = StringVar(value=CREntryVar.get())
                        self.SkillSensesAndLanguagesFieldVar = StringVar(value=SkillSensesAndLanguagesFieldVar.get())
                        self.FeaturesFieldVar = StringVar(value=FeaturesFieldVar.get())
                        self.ActionsAndReactionsFieldVar = StringVar(value=ActionsAndReactionsFieldVar.get())
                        self.InventoryAndNotesFieldVar = StringVar(value=InventoryAndNotesFieldVar.get())
                        self.AbilitiesStrengthEntryVar = StringVar(value=AbilitiesStrengthEntryVar.get())
                        self.AbilitiesDexterityEntryVar = StringVar(value=AbilitiesDexterityEntryVar.get())
                        self.AbilitiesConstitutionEntryVar = StringVar(value=AbilitiesConstitutionEntryVar.get())
                        self.AbilitiesIntelligenceEntryVar = StringVar(value=AbilitiesIntelligenceEntryVar.get())
                        self.AbilitiesWisdomEntryVar = StringVar(value=AbilitiesWisdomEntryVar.get())
                        self.AbilitiesCharismaEntryVar = StringVar(value=AbilitiesCharismaEntryVar.get())

                        # Create Window
                        self.Window = Toplevel(master)
                        self.Window.wm_attributes("-toolwindow", 1)
                        self.Window.wm_title("Creature Stats")

                        # Name Entry
                        self.NameFrame = LabelFrame(self.Window, text="Name:")
                        self.NameFrame.grid_columnconfigure(0, weight=1)
                        self.NameFrame.grid(row=0, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                        self.NameEntry = Entry(self.NameFrame, justify=CENTER, width=20, textvariable=self.NameEntryVar)
                        self.NameEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                        # Size, Tags, and Alignment
                        self.SizeTagsAndAlignmentFrame = LabelFrame(self.Window, text="Size, Tags, and Alignment:")
                        self.SizeTagsAndAlignmentFrame.grid_columnconfigure(0, weight=1)
                        self.SizeTagsAndAlignmentFrame.grid(row=1, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                        self.SizeTagsAndAlignmentEntry = Entry(self.SizeTagsAndAlignmentFrame, justify=CENTER, width=20, textvariable=self.SizeTagsAndAlignmentEntryVar)
                        self.SizeTagsAndAlignmentEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                        # Entries Frame
                        self.EntriesFrame = Frame(self.Window)
                        self.EntriesFrame.grid(row=2, column=0, rowspan=4, sticky=NSEW)
                        self.EntriesFrame.grid_rowconfigure(2, weight=1)
                        self.EntriesFrame.grid_rowconfigure(4, weight=1)
                        self.EntriesFrame.grid_rowconfigure(6, weight=1)

                        # Max HP Entry
                        self.MaxHPFrame = LabelFrame(self.EntriesFrame, text="Max HP:")
                        self.MaxHPFrame.grid_columnconfigure(0, weight=1)
                        self.MaxHPFrame.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)
                        self.MaxHPEntry = Entry(self.MaxHPFrame, justify=CENTER, width=3, textvariable=self.MaxHPEntryVar)
                        self.MaxHPEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                        # AC Entry
                        self.ACFrame = LabelFrame(self.EntriesFrame, text="AC:")
                        self.ACFrame.grid_columnconfigure(0, weight=1)
                        self.ACFrame.grid(row=3, column=0, padx=2, pady=2, sticky=NSEW)
                        self.ACEntry = Entry(self.ACFrame, justify=CENTER, width=3, textvariable=self.ACEntryVar)
                        self.ACEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                        # Speed
                        self.SpeedFrame = LabelFrame(self.EntriesFrame, text="Speed:")
                        self.SpeedFrame.grid_columnconfigure(0, weight=1)
                        self.SpeedFrame.grid(row=5, column=0, padx=2, pady=2, sticky=NSEW)
                        self.SpeedEntry = Entry(self.SpeedFrame, justify=CENTER, width=3, textvariable=self.SpeedEntryVar)
                        self.SpeedEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                        # CR
                        self.CRFrame = LabelFrame(self.EntriesFrame, text="CR:")
                        self.CRFrame.grid_columnconfigure(0, weight=1)
                        self.CRFrame.grid(row=7, column=0, padx=2, pady=2, sticky=NSEW)
                        self.CREntry = Entry(self.CRFrame, justify=CENTER, width=3, textvariable=self.CREntryVar)
                        self.CREntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                        # Abilities
                        self.AbilitiesFrame = LabelFrame(self.Window, text="Abilities:")
                        self.AbilitiesFrame.grid_columnconfigure(0, weight=1)
                        self.AbilitiesFrame.grid_columnconfigure(1, weight=1)
                        self.AbilitiesFrame.grid_columnconfigure(2, weight=1)
                        self.AbilitiesFrame.grid(row=2, column=1, rowspan=2, padx=2, pady=2, sticky=NSEW)
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

                        # Skills, Senses, and Languages
                        self.SkillSensesAndLanguagesFrame = LabelFrame(self.Window, text="Skills, Senses, and Languages:")
                        self.SkillSensesAndLanguagesFrame.grid(row=4, column=1, rowspan=2, padx=2, pady=2, sticky=NSEW)
                        self.SkillSensesAndLanguagesField = ScrolledText(self.SkillSensesAndLanguagesFrame, Width=212, Height=69)
                        self.SkillSensesAndLanguagesField.grid(row=0, column=0)
                        self.SkillSensesAndLanguagesField.Text.insert(1.0, self.SkillSensesAndLanguagesFieldVar.get())

                        # Features
                        self.FeaturesFrame = LabelFrame(self.Window, text="Features:")
                        self.FeaturesFrame.grid(row=6, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                        self.FeaturesField = ScrolledText(self.FeaturesFrame, Width=275, Height=75)
                        self.FeaturesField.grid(row=0, column=0)
                        self.FeaturesField.Text.insert(1.0, self.FeaturesFieldVar.get())

                        # Actions
                        self.ActionsAndReactionsFrame = LabelFrame(self.Window, text="Actions:")
                        self.ActionsAndReactionsFrame.grid(row=7, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                        self.ActionsAndReactionsField = ScrolledText(self.ActionsAndReactionsFrame, Width=275, Height=75)
                        self.ActionsAndReactionsField.grid(row=0, column=0)
                        self.ActionsAndReactionsField.Text.insert(1.0, self.ActionsAndReactionsFieldVar.get())

                        # Inventory and Notes
                        self.InventoryAndNotesFrame = LabelFrame(self.Window, text="Inventory and Notes:")
                        self.InventoryAndNotesFrame.grid(row=8, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                        self.InventoryAndNotesField = ScrolledText(self.InventoryAndNotesFrame, Width=275, Height=50)
                        self.InventoryAndNotesField.grid(row=0, column=0)
                        self.InventoryAndNotesField.Text.insert(1.0, self.InventoryAndNotesFieldVar.get())

                        # Buttons
                        self.ButtonsFrame = Frame(self.Window)
                        self.ButtonsFrame.grid_columnconfigure(0, weight=1)
                        self.ButtonsFrame.grid_columnconfigure(1, weight=1)
                        self.ButtonsFrame.grid(row=9, column=0, columnspan=2, sticky=NSEW)

                        # Submit Button
                        self.SubmitButton = Button(self.ButtonsFrame, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
                        self.SubmitButton.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                        # Cancel Button
                        self.CancelButton = Button(self.ButtonsFrame, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
                        self.CancelButton.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)

                        # Prevent Main Window Input
                        self.Window.grab_set()

                        # Handle Config Window Geometry and Focus
                        GlobalInst.WindowGeometry(self.Window, True)
                        self.Window.focus_force()

                    def Submit(self):
                        self.DataSubmitted.set(True)
                        self.SkillSensesAndLanguagesFieldVar.set(self.SkillSensesAndLanguagesField.Text.get("1.0", "end-1c"))
                        self.FeaturesFieldVar.set(self.FeaturesField.Text.get("1.0", "end-1c"))
                        self.ActionsAndReactionsFieldVar.set(self.ActionsAndReactionsField.Text.get("1.0", "end-1c"))
                        self.InventoryAndNotesFieldVar.set(self.InventoryAndNotesField.Text.get("1.0", "end-1c"))
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
                self.Modifier = ttk.Combobox(self.TableFrame, textvariable=self.ModifierVar, values=("", "Dexterity", "Dexterity (Max 2)"), width=17, state="readonly", justify=CENTER)
                self.Modifier.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)

                # Manual Bonus
                self.ManualBonusHeader = Label(self.TableFrame, text="Manual Bonus", bd=2, relief=GROOVE)
                self.ManualBonusHeader.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
                self.ManualBonusEntry = Entry(self.TableFrame, width=3, textvariable=self.ManualBonusEntryVar, justify=CENTER)
                self.ManualBonusEntry.grid(row=1, column=2, sticky=NSEW, padx=2, pady=2)

                # Submit Button
                self.SubmitButton = Button(self.Window, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
                self.SubmitButton.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)

                # Cancel Button
                self.CancelButton = Button(self.Window, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
                self.CancelButton.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)

                # Prevent Main Window Input
                self.Window.grab_set()

                # Handle Config Window Geometry and Focus
                GlobalInst.WindowGeometry(self.Window, True)
                self.Window.focus_force()

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
                    Base = GlobalInst.GetStringVarAsNumber(self.BaseEntryVar)
                    GlobalInst.GetStringVarAsNumber(self.ManualBonusEntryVar)
                except:
                    messagebox.showerror("Invalid Entry", "Base AC and AC manual bonus must be whole numbers.")
                    return False
                if Base < 1:
                    messagebox.showerror("Invalid Entry", "Base AC cannot be less than 1.")
                    return False
                return True

    # Spellcasting
    class Spellcasting:
        def __init__(self, master):
            self.SpellPointsMaxEntryVar = StringVar()
            self.SpellPointsRemainingEntryVar = StringVar()
            self.SpellUsingSpellPointsBoxVar = BooleanVar()
            self.SpellPointsManualBonusVar = StringVar()

            # Center Rows and Columns
            master.grid_rowconfigure(0, weight=1)
            master.grid_rowconfigure(2, weight=1)
            master.grid_rowconfigure(4, weight=1)
            master.grid_rowconfigure(6, weight=1)
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
            self.SpellcastingAbility1 = self.SpellcastingAbility(self.SpellcastingAbilityFrame, self.SpellcastingAbilitiesList, 1)
            self.SpellcastingAbility2 = self.SpellcastingAbility(self.SpellcastingAbilityFrame, self.SpellcastingAbilitiesList, 2)
            self.SpellcastingAbility3 = self.SpellcastingAbility(self.SpellcastingAbilityFrame, self.SpellcastingAbilitiesList, 3)

            # Spell Notes Frame
            self.SpellNotesFrame = LabelFrame(master, text="Spell Notes:")
            self.SpellNotesFrame.grid(row=3, column=1, padx=2, pady=2, rowspan=3)
            self.SpellNotesField = ScrolledText(self.SpellNotesFrame, Width=225, Height=379)
            self.SpellNotesField.grid(row=0, column=0)

            # Spell Slots Frame
            self.SpellSlotsFrame = LabelFrame(master, text="Spell Slots:")
            self.SpellSlotsFrame.grid(row=3, column=3, padx=2, pady=2)

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
            self.SpellPointsFrame.grid(row=5, column=3, padx=2, pady=2, sticky=NSEW)
            self.SpellUsingSpellPointsBox = Checkbutton(self.SpellPointsFrame, variable=self.SpellUsingSpellPointsBoxVar, text="Using\nSpell\nPoints")
            self.SpellUsingSpellPointsBox.grid(row=0, column=0, columnspan=2)
            self.SpellPointsMaxHeader = Label(self.SpellPointsFrame, text="Max", bd=2, relief=GROOVE)
            self.SpellPointsMaxHeader.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)
            self.SpellPointsMaxEntry = Entry(self.SpellPointsFrame, justify=CENTER, width=5, state=DISABLED, disabledbackground=GlobalInst.ButtonColor, disabledforeground="black", cursor="arrow",
                                             textvariable=self.SpellPointsMaxEntryVar)
            self.SpellPointsMaxEntry.grid(row=1, column=1, padx=2, pady=2, sticky=NSEW)
            self.SpellPointsMaxEntry.bind("<Button-1>", self.ConfigureSpellPoints)
            self.SpellPointsRemainingHeader = Label(self.SpellPointsFrame, text="Remaining", bd=2, relief=GROOVE)
            self.SpellPointsRemainingHeader.grid(row=2, column=0, padx=2, pady=2, sticky=NSEW)
            self.SpellPointsRemainingEntry = Entry(self.SpellPointsFrame, justify=CENTER, width=5, textvariable=self.SpellPointsRemainingEntryVar, state=DISABLED, disabledbackground=GlobalInst.ButtonColor,
                                                   disabledforeground="black",
                                                   cursor="arrow")
            self.SpellPointsRemainingEntry.grid(row=2, column=1, padx=2, pady=2, sticky=NSEW)
            self.SpellPointsRemainingEntry.bind("<Button-1>", self.ExpendSpellPoints)
            self.SpellPointsRemainingEntry.bind("<Button-3>", self.RestoreSpellPoints)

            # Spell Entries Frame
            self.SpellEntriesFrame = LabelFrame(master, text="Spells:")
            self.SpellEntriesFrame.grid(row=1, column=5, padx=2, pady=2, sticky=NSEW, rowspan=5)

            # Spell Entries Notebook
            self.SpellEntriesNotebook = ttk.Notebook(self.SpellEntriesFrame, height=441)
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

            # Add Saved Fields to Character Data Dictionary
            GlobalInst.SavedData["SpellPointsRemainingEntryVar"] = self.SpellPointsRemainingEntryVar
            GlobalInst.SavedData["SpellNotesField"] = self.SpellNotesField
            GlobalInst.SavedData["SpellUsingSpellPointsBoxVar"] = self.SpellUsingSpellPointsBoxVar
            GlobalInst.SavedData["SpellPointsManualBonusVar"] = self.SpellPointsManualBonusVar

        def ConfigureSpellPoints(self, event):
            # Test Level Input Validity
            if CharacterSheetHeaderInst.ValidLevelEntry():
                pass
            else:
                return

            # Test Ability Input Validity
            if CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.ValidStatsEntry():
                pass
            else:
                return

            # Create Config Window and Wait
            SpellPointsDataInst = ManualBonusData(root, self.SpellPointsManualBonusVar, "Spell Points")
            root.wait_window(SpellPointsDataInst.Window)

            # Handle Values
            if SpellPointsDataInst.DataSubmitted.get():
                SpellPointsDataInst.GetData(self.SpellPointsManualBonusVar)

            # Update Stats and Inventory
            GlobalInst.UpdateStatsAndInventory()

        def CalculateSpellPoints(self):
            if self.SpellUsingSpellPointsBoxVar.get():
                TotalPoints = 0
                for Level in self.SpellSlotsList:
                    TotalPoints += (Level.PointValue * GlobalInst.GetStringVarAsNumber(Level.SlotsEntryVar))
                TotalPoints += GlobalInst.GetStringVarAsNumber(self.SpellPointsManualBonusVar)
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
            ExpendSpellPointsMenuInst = self.ExpendOrRestoreSpellPointsMenu(root, "Expend")
            root.wait_window(ExpendSpellPointsMenuInst.Window)

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
            ExpendSpellPointsMenuInst = self.ExpendOrRestoreSpellPointsMenu(root, "Restore")
            root.wait_window(ExpendSpellPointsMenuInst.Window)

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

        class SpellcastingAbility:
            def __init__(self, master, List, Column):
                self.SpellcastingAbilitySelectionDropdownVar = StringVar()
                self.SpellSaveDCEntryVar = StringVar()
                self.SpellAttackModifierEntryVar = StringVar()
                self.SpellAttackModifierManualBonusVar = StringVar()
                self.SpellSaveDCManualBonusVar = StringVar()
                self.Column = Column

                # Add to List
                List.append(self)

                # Spellcasting Ability Selection
                self.SpellcastingAbilitySelectionDropdown = ttk.Combobox(master, textvariable=self.SpellcastingAbilitySelectionDropdownVar, values=("", "STR", "DEX", "CON", "INT", "WIS", "CHA"), width=5,
                                                                         state="readonly", justify=CENTER)
                self.SpellcastingAbilitySelectionDropdown.grid(row=0, column=self.Column, padx=2, pady=2, sticky=NSEW)

                # Spell Save DC
                self.SpellSaveDCEntry = Entry(master, justify=CENTER, state=DISABLED, disabledbackground=GlobalInst.ButtonColor, disabledforeground="black", width=2, textvariable=self.SpellSaveDCEntryVar,
                                              cursor="arrow")
                self.SpellSaveDCEntry.grid(row=1, column=self.Column, padx=2, pady=2, sticky=NSEW)
                self.SpellSaveDCEntry.bind("<Button-1>", self.ConfigureSpellSaveDC)

                # Spell Attack Modifier
                self.SpellAttackModifierEntry = Entry(master, justify=CENTER, state=DISABLED, disabledbackground=GlobalInst.ButtonColor, disabledforeground="black", width=2,
                                                      textvariable=self.SpellAttackModifierEntryVar, cursor="dotbox")
                self.SpellAttackModifierEntry.grid(row=2, column=self.Column, padx=2, pady=2, sticky=NSEW)
                self.SpellAttackModifierEntry.bind("<Button-1>", self.RollSpellAttack)
                self.SpellAttackModifierEntry.bind("<Button-3>", self.ConfigureSpellAttackModifier)

                # Add Saved Fields to Character Data Dictionary
                GlobalInst.SavedData["SpellcastingAbilitySelectionDropdownVar" + str(self.Column)] = self.SpellcastingAbilitySelectionDropdownVar
                GlobalInst.SavedData["SpellAttackModifierManualBonusVar" + str(self.Column)] = self.SpellAttackModifierManualBonusVar
                GlobalInst.SavedData["SpellSaveDCManualBonusVar" + str(self.Column)] = self.SpellSaveDCManualBonusVar

            def RollSpellAttack(self, event):
                DiceRollerInst.DiceNumberEntryVar.set(1)
                DiceRollerInst.DieTypeEntryVar.set(20)
                DiceRollerInst.ModifierEntryVar.set(str(GlobalInst.GetStringVarAsNumber(self.SpellAttackModifierEntryVar)))
                DiceRollerInst.Roll(self.SpellcastingAbilitySelectionDropdownVar.get() + " Spell Attack:\n")

            def ConfigureSpellSaveDC(self, event):
                # Test Level Input Validity
                if CharacterSheetHeaderInst.ValidLevelEntry():
                    pass
                else:
                    return

                # Test Ability Input Validity
                if CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.ValidStatsEntry():
                    pass
                else:
                    return

                # Create Config Window and Wait
                SpellSaveDCDataInst = ManualBonusData(root, self.SpellSaveDCManualBonusVar, "Spell Save DC")
                root.wait_window(SpellSaveDCDataInst.Window)

                # Handle Values
                if SpellSaveDCDataInst.DataSubmitted.get():
                    SpellSaveDCDataInst.GetData(self.SpellSaveDCManualBonusVar)

                # Update Stats and Inventory
                GlobalInst.UpdateStatsAndInventory()

            def ConfigureSpellAttackModifier(self, event):
                # Test Level Input Validity
                if CharacterSheetHeaderInst.ValidLevelEntry():
                    pass
                else:
                    return

                # Test Ability Input Validity
                if CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.ValidStatsEntry():
                    pass
                else:
                    return

                # Create Config Window and Wait
                SpellAttackModifierDataInst = ManualBonusData(root, self.SpellAttackModifierManualBonusVar, "Spell Attack Modifier")
                root.wait_window(SpellAttackModifierDataInst.Window)

                # Handle Values
                if SpellAttackModifierDataInst.DataSubmitted.get():
                    SpellAttackModifierDataInst.GetData(self.SpellAttackModifierManualBonusVar)

                # Update Stats and Inventory
                GlobalInst.UpdateStatsAndInventory()

        class SpellList:
            def __init__(self, master, List, LevelName):
                self.LevelName = LevelName

                # Add to List
                List.append(self)

                # Spell List Frame
                self.SpellListFrame = Frame(master)
                self.SpellListFrame.grid(row=0, column=0)

                # Spell List Entries List
                self.SpellListEntriesList = []

                # Spell List Entries
                for CurrentIndex in range(17):
                    self.SpellListEntry(self.SpellListFrame, self.SpellListEntriesList, self.LevelName, CurrentIndex + 1)

            class SpellListEntry:
                def __init__(self, master, List, LevelName, Row):
                    self.Row = Row
                    self.LevelName = LevelName
                    self.NameEntryVar = StringVar()
                    self.SchoolEntryVar = StringVar()
                    self.CastingTimeVar = StringVar()
                    self.RangeVar = StringVar()
                    self.ComponentsVar = StringVar()
                    self.DurationVar = StringVar()
                    self.DescriptionVar = StringVar()
                    self.PreparedBoxVar = BooleanVar()

                    # Set Row Size
                    master.grid_rowconfigure(self.Row, minsize=26)

                    # Add to List
                    List.append(self)

                    # Prepared Box
                    self.PreparedBox = Checkbutton(master, variable=self.PreparedBoxVar)
                    self.PreparedBox.grid(row=self.Row, column=0, sticky=NSEW)

                    # Name Entry
                    self.NameEntry = Entry(master, width=42, justify=CENTER, state=DISABLED, disabledbackground=GlobalInst.ButtonColor, disabledforeground="black", textvariable=self.NameEntryVar, cursor="arrow")
                    self.NameEntry.grid(row=self.Row, column=1, sticky=NSEW)
                    self.NameEntry.bind("<Button-1>", self.Set)

                    # Add Saved Fields to Character Data Dictionary
                    GlobalInst.SavedData["SpellEntryName" + self.LevelName + str(self.Row)] = self.NameEntryVar
                    GlobalInst.SavedData["SchoolEntryName" + self.LevelName + str(self.Row)] = self.SchoolEntryVar
                    GlobalInst.SavedData["SpellEntryCastingTime" + self.LevelName + str(self.Row)] = self.CastingTimeVar
                    GlobalInst.SavedData["SpellEntryRange" + self.LevelName + str(self.Row)] = self.RangeVar
                    GlobalInst.SavedData["SpellEntryComponents" + self.LevelName + str(self.Row)] = self.ComponentsVar
                    GlobalInst.SavedData["SpellEntryDuration" + self.LevelName + str(self.Row)] = self.DurationVar
                    GlobalInst.SavedData["SpellEntryDescription" + self.LevelName + str(self.Row)] = self.DescriptionVar
                    GlobalInst.SavedData["SpellEntryPrepared" + self.LevelName + str(self.Row)] = self.PreparedBoxVar

                def Set(self, event):
                    # Create Config Window and Wait
                    SpellConfigInst = self.SpellConfig(root, self.NameEntryVar, self.SchoolEntryVar, self.CastingTimeVar, self.RangeVar, self.ComponentsVar, self.DurationVar, self.DescriptionVar)
                    root.wait_window(SpellConfigInst.Window)

                    # Handle Values
                    if SpellConfigInst.DataSubmitted.get():
                        self.NameEntryVar.set(SpellConfigInst.NameEntryVar.get())
                        self.SchoolEntryVar.set(SpellConfigInst.SchoolEntryVar.get())
                        self.CastingTimeVar.set(SpellConfigInst.CastingTimeVar.get())
                        self.RangeVar.set(SpellConfigInst.RangeVar.get())
                        self.ComponentsVar.set(SpellConfigInst.ComponentsVar.get())
                        self.DurationVar.set(SpellConfigInst.DurationVar.get())
                        self.DescriptionVar.set(SpellConfigInst.DescriptionVar.get())

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
                        GlobalInst.WindowGeometry(self.Window, True)
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

                # Add Saved Fields to Character Data Dictionary
                GlobalInst.SavedData[self.SlotLevel + "SlotsEntryVar"] = self.SlotsEntryVar
                GlobalInst.SavedData[self.SlotLevel + "UsedEntryVar"] = self.UsedEntryVar

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
                GlobalInst.WindowGeometry(self.Window, True)
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
            self.CarryingCapacityManualBonusVar = StringVar()
            self.TotalLoadEntryVar = StringVar()
            self.GearLoadEntryVar = StringVar()
            self.TreasureLoadEntryVar = StringVar()
            self.MiscLoadEntryVar = StringVar()
            self.TotalValueEntryVar = StringVar()
            self.GearValueEntryVar = StringVar()
            self.TreasureValueEntryVar = StringVar()
            self.MiscValueEntryVar = StringVar()
            self.ScrollingDisabledVar = BooleanVar(value=False)

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
            self.InventoryDataFrame.grid(row=1, column=1, sticky=NSEW)

            # Carrying Capacity
            self.CarryingCapacityFrame = LabelFrame(self.InventoryDataFrame, text="Carrying Capacity:")
            self.CarryingCapacityFrame.grid_rowconfigure(0, weight=1)
            self.CarryingCapacityFrame.grid_rowconfigure(2, weight=1)
            self.CarryingCapacityFrame.grid_columnconfigure(0, weight=1)
            self.CarryingCapacityFrame.grid_columnconfigure(2, weight=1)
            self.CarryingCapacityFrame.grid(row=0, column=0, padx=2, pady=2, sticky=NS)
            self.CarryingCapacityEntry = Entry(self.CarryingCapacityFrame, width=15, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground=GlobalInst.ButtonColor, textvariable=self.CarryingCapacityVar,
                                               cursor="arrow")
            self.CarryingCapacityEntry.grid(row=1, column=1, padx=2, pady=2)
            self.CarryingCapacityEntry.bind("<Button-1>", self.ConfigureCarryingCapacity)

            # Clear Inventory Button
            self.ClearInventoryButton = Button(self.InventoryDataFrame, text="Clear Inventory", command=self.ClearInventory, bg=GlobalInst.ButtonColor)
            self.ClearInventoryButton.grid(row=1, column=0, padx=2, pady=2)

            # Loads
            self.LoadsFrame = LabelFrame(self.InventoryDataFrame, text="Loads (lbs.):")
            self.LoadsFrame.grid_rowconfigure(0, weight=1)
            self.LoadsFrame.grid_rowconfigure(2, weight=1)
            self.LoadsFrame.grid_rowconfigure(4, weight=1)
            self.LoadsFrame.grid_rowconfigure(6, weight=1)
            self.LoadsFrame.grid_rowconfigure(8, weight=1)
            self.LoadsFrame.grid_columnconfigure(0, weight=1)
            self.LoadsFrame.grid_columnconfigure(3, weight=1)
            self.LoadsFrame.grid(row=0, column=2, padx=2, pady=2, sticky=NS, rowspan=2)
            self.TotalLoadLabel = Label(self.LoadsFrame, text="Total", bd=2, relief=GROOVE)
            self.TotalLoadLabel.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
            self.TotalLoadEntry = Entry(self.LoadsFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.TotalLoadEntryVar, cursor="arrow")
            self.TotalLoadEntry.grid(row=1, column=2, sticky=NSEW, padx=2, pady=2)
            self.GearLoadLabel = Label(self.LoadsFrame, text="Gear", bd=2, relief=GROOVE)
            self.GearLoadLabel.grid(row=3, column=1, sticky=NSEW, padx=2, pady=2)
            self.GearLoadEntry = Entry(self.LoadsFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.GearLoadEntryVar, cursor="arrow")
            self.GearLoadEntry.grid(row=3, column=2, sticky=NSEW, padx=2, pady=2)
            self.TreasureLoadLabel = Label(self.LoadsFrame, text="Treasure", bd=2, relief=GROOVE)
            self.TreasureLoadLabel.grid(row=5, column=1, sticky=NSEW, padx=2, pady=2)
            self.TreasureLoadEntry = Entry(self.LoadsFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.TreasureLoadEntryVar, cursor="arrow")
            self.TreasureLoadEntry.grid(row=5, column=2, sticky=NSEW, padx=2, pady=2)
            self.MiscLoadLabel = Label(self.LoadsFrame, text="Misc", bd=2, relief=GROOVE)
            self.MiscLoadLabel.grid(row=7, column=1, sticky=NSEW, padx=2, pady=2)
            self.MiscLoadEntry = Entry(self.LoadsFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.MiscLoadEntryVar, cursor="arrow")
            self.MiscLoadEntry.grid(row=7, column=2, sticky=NSEW, padx=2, pady=2)

            # Coins
            self.CoinsFrame = LabelFrame(self.InventoryDataFrame, text="Coins:")
            self.CoinsFrame.grid_rowconfigure(0, weight=1)
            self.CoinsFrame.grid_rowconfigure(4, weight=1)
            self.CoinsFrame.grid_columnconfigure(0, weight=1)
            self.CoinsFrame.grid_columnconfigure(2, weight=1)
            self.CoinsFrame.grid(row=0, column=4, padx=2, pady=2, sticky=NS, rowspan=2)
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
            self.CoinValueHeader = Label(self.CoinValueAndWeightHolderFrame, text="Coin Value\n(gp)", bd=2, relief=GROOVE)
            self.CoinValueHeader.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
            self.CoinValueEntry = Entry(self.CoinValueAndWeightHolderFrame, width=13, justify=CENTER, textvariable=self.CoinValueEntryVar, state=DISABLED, disabledforeground="black", disabledbackground="light gray",
                                        cursor="arrow")
            self.CoinValueEntry.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
            self.CoinWeightHeader = Label(self.CoinValueAndWeightHolderFrame, text="Coin Weight\n(lbs.)", bd=2, relief=GROOVE)
            self.CoinWeightHeader.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
            self.CoinWeightEntry = Entry(self.CoinValueAndWeightHolderFrame, width=13, justify=CENTER, textvariable=self.CoinWeightEntryVar, state=DISABLED, disabledforeground="black", disabledbackground="light gray",
                                         cursor="arrow")
            self.CoinWeightEntry.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)

            # Coin Calculator
            self.CoinCalculatorButton = Button(self.CoinsFrame, text="Coin Calculator", command=self.OpenCoinCalculator, bg=GlobalInst.ButtonColor)
            self.CoinCalculatorButton.grid(row=3, column=1, padx=2, pady=2)

            # Values
            self.ValuesFrame = LabelFrame(self.InventoryDataFrame, text="Values (gp):")
            self.ValuesFrame.grid_rowconfigure(0, weight=1)
            self.ValuesFrame.grid_rowconfigure(2, weight=1)
            self.ValuesFrame.grid_rowconfigure(4, weight=1)
            self.ValuesFrame.grid_rowconfigure(6, weight=1)
            self.ValuesFrame.grid_rowconfigure(8, weight=1)
            self.ValuesFrame.grid_columnconfigure(0, weight=1)
            self.ValuesFrame.grid_columnconfigure(3, weight=1)
            self.ValuesFrame.grid(row=0, column=6, padx=2, pady=2, sticky=NS, rowspan=2)
            self.TotalValueLabel = Label(self.ValuesFrame, text="Total", bd=2, relief=GROOVE)
            self.TotalValueLabel.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
            self.TotalValueEntry = Entry(self.ValuesFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.TotalValueEntryVar, cursor="arrow")
            self.TotalValueEntry.grid(row=1, column=2, sticky=NSEW, padx=2, pady=2)
            self.GearValueLabel = Label(self.ValuesFrame, text="Gear", bd=2, relief=GROOVE)
            self.GearValueLabel.grid(row=3, column=1, sticky=NSEW, padx=2, pady=2)
            self.GearValueEntry = Entry(self.ValuesFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.GearValueEntryVar, cursor="arrow")
            self.GearValueEntry.grid(row=3, column=2, sticky=NSEW, padx=2, pady=2)
            self.TreasureValueLabel = Label(self.ValuesFrame, text="Treasure", bd=2, relief=GROOVE)
            self.TreasureValueLabel.grid(row=5, column=1, sticky=NSEW, padx=2, pady=2)
            self.TreasureValueEntry = Entry(self.ValuesFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.TreasureValueEntryVar, cursor="arrow")
            self.TreasureValueEntry.grid(row=5, column=2, sticky=NSEW, padx=2, pady=2)
            self.MiscValueLabel = Label(self.ValuesFrame, text="Misc", bd=2, relief=GROOVE)
            self.MiscValueLabel.grid(row=7, column=1, sticky=NSEW, padx=2, pady=2)
            self.MiscValueEntry = Entry(self.ValuesFrame, width=10, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", textvariable=self.MiscValueEntryVar, cursor="arrow")
            self.MiscValueEntry.grid(row=7, column=2, sticky=NSEW, padx=2, pady=2)

            # Inventory List Frame
            self.InventoryListFrame = LabelFrame(master, text="Inventory List:")
            self.InventoryListFrame.grid(row=2, column=1, padx=2, pady=2)

            # Inventory List Scrolled Canvas
            self.InventoryListScrolledCanvas = ScrolledCanvas(self.InventoryListFrame, Height=315, Width=640, ScrollingDisabledVar=self.ScrollingDisabledVar)

            # Inventory List Headers
            self.InventoryListNameHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Name", bd=2, relief=GROOVE)
            self.InventoryListNameHeader.grid(row=0, column=0, sticky=NSEW)
            self.InventoryListCountHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Count", bd=2, relief=GROOVE)
            self.InventoryListCountHeader.grid(row=0, column=1, sticky=NSEW)
            self.InventoryListUnitWeightHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Unit Weight\n(lb.)", bd=2, relief=GROOVE)
            self.InventoryListUnitWeightHeader.grid(row=0, column=2, sticky=NSEW)
            self.InventoryListUnitValueHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Unit Value", bd=2, relief=GROOVE)
            self.InventoryListUnitValueHeader.grid(row=0, column=3, sticky=NSEW)
            self.InventoryListUnitValueDenominationHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Value\nDenom.", bd=2, relief=GROOVE)
            self.InventoryListUnitValueDenominationHeader.grid(row=0, column=4, sticky=NSEW)
            self.InventoryListTotalWeightHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Total Weight\n(lb.)", bd=2, relief=GROOVE)
            self.InventoryListTotalWeightHeader.grid(row=0, column=5, sticky=NSEW)
            self.InventoryListTotalValueHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Total Value\n(gp)", bd=2, relief=GROOVE)
            self.InventoryListTotalValueHeader.grid(row=0, column=6, sticky=NSEW)
            self.InventoryListTagHeader = Label(self.InventoryListScrolledCanvas.WindowFrame, text="Tag", bd=2, relief=GROOVE)
            self.InventoryListTagHeader.grid(row=0, column=7, sticky=NSEW)

            # Inventory Entries List
            self.InventoryEntriesList = []

            # Inventory Entries
            for CurrentIndex in range(100):
                self.InventoryEntry(self.InventoryListScrolledCanvas.WindowFrame, self.InventoryEntriesList, self.ScrollingDisabledVar, CurrentIndex + 1)

            # Add Saved Fields to Character Data Dictionary
            GlobalInst.SavedData["CoinsEntryCPVar"] = self.CoinsEntryCPVar
            GlobalInst.SavedData["CoinsEntrySPVar"] = self.CoinsEntrySPVar
            GlobalInst.SavedData["CoinsEntryEPVar"] = self.CoinsEntryEPVar
            GlobalInst.SavedData["CoinsEntryGPVar"] = self.CoinsEntryGPVar
            GlobalInst.SavedData["CoinsEntryPPVar"] = self.CoinsEntryPPVar
            GlobalInst.SavedData["CarryingCapacityManualBonusVar"] = self.CarryingCapacityManualBonusVar

        def Calculate(self):
            # Carrying Capacity
            self.CarryingCapacityVar.set((15 * GlobalInst.GetStringVarAsNumber(CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.StrengthEntry.AbilityEntryTotalVar)) +
                                         GlobalInst.GetStringVarAsNumber(self.CarryingCapacityManualBonusVar))

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
                Count = GlobalInst.GetStringVarAsNumber(Entry.CountEntryVar)
                ValueDenomination = Entry.UnitValueDenominationVar.get()

                # Total Weight and Value
                TotalItemWeight = GlobalInst.GetStringVarAsNumber(Entry.UnitWeightEntryVar, Mode="Decimal") * Decimal(Count)
                TotalItemValue = GlobalInst.GetStringVarAsNumber(Entry.UnitValueEntryVar, Mode="Decimal") * Decimal(Count)

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

        def ConfigureCarryingCapacity(self, event):
            # Test Level Input Validity
            if CharacterSheetHeaderInst.ValidLevelEntry():
                pass
            else:
                return

            # Test Ability Input Validity
            if CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.ValidStatsEntry():
                pass
            else:
                return

            # Create Config Window and Wait
            SpellPointsDataInst = ManualBonusData(root, self.CarryingCapacityManualBonusVar, "Carrying Capacity")
            root.wait_window(SpellPointsDataInst.Window)

            # Handle Values
            if SpellPointsDataInst.DataSubmitted.get():
                SpellPointsDataInst.GetData(self.CarryingCapacityManualBonusVar)

            # Update Stats and Inventory
            GlobalInst.UpdateStatsAndInventory()

        def ClearInventory(self):
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

        def ValidInventoryEntry(self):
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
            self.CoinCalculatorInst = self.CoinCalculator(root, self.ValueCP, self.ValueSP, self.ValueEP, self.ValueGP, self.ValuePP, self.WeightPerCoin)
            root.wait_window(self.CoinCalculatorInst.Window)

        class InventoryEntry:
            def __init__(self, master, List, ScrollingDisabledVar, Row):
                self.NameEntryVar = StringVar()
                self.CountEntryVar = StringVar()
                self.UnitWeightEntryVar = StringVar()
                self.UnitValueEntryVar = StringVar()
                self.UnitValueDenominationVar = StringVar()
                self.TotalWeightEntryVar = StringVar()
                self.TotalValueEntryVar = StringVar()
                self.CategoryTagVar = StringVar()
                self.CategoryEntryVar = StringVar()
                self.RarityEntryVar = StringVar()
                self.DescriptionVar = StringVar()
                self.Row = Row
                self.ScrollingDisabledVar = ScrollingDisabledVar

                # Set Row Size
                master.grid_rowconfigure(self.Row, minsize=26)

                # Add to List
                List.append(self)

                # Name Entry
                self.NameEntry = Entry(master, width=35, textvariable=self.NameEntryVar, justify=CENTER, bg=GlobalInst.ButtonColor)
                self.NameEntry.grid(row=self.Row, column=0, sticky=NSEW)
                self.NameEntry.bind("<Button-3>", self.ConfigureMagicItem)

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
                self.UnitValueDenomination = ttk.Combobox(master, textvariable=self.UnitValueDenominationVar, values=("", "cp", "sp", "ep", "gp", "pp"), width=2, state="readonly", justify=CENTER)
                self.UnitValueDenomination.grid(row=self.Row, column=4, sticky=NSEW)
                self.UnitValueDenomination.bind("<Enter>", self.DisableScrolling)
                self.UnitValueDenomination.bind("<Leave>", self.EnableScrolling)

                # Total Weight Entry
                self.TotalWeightEntry = Entry(master, width=4, textvariable=self.TotalWeightEntryVar, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow")
                self.TotalWeightEntry.grid(row=self.Row, column=5, sticky=NSEW)

                # Total Value Entry
                self.TotalValueEntry = Entry(master, width=4, textvariable=self.TotalValueEntryVar, justify=CENTER, state=DISABLED, disabledforeground="black", disabledbackground="light gray", cursor="arrow")
                self.TotalValueEntry.grid(row=self.Row, column=6, sticky=NSEW)

                # Category Tag
                self.CategoryTag = ttk.Combobox(master, textvariable=self.CategoryTagVar, values=("", "Gear", "Treasure", "Misc."), width=8, state="readonly", justify=CENTER)
                self.CategoryTag.grid(row=self.Row, column=7, sticky=NSEW)
                self.CategoryTag.bind("<Enter>", self.DisableScrolling)
                self.CategoryTag.bind("<Leave>", self.EnableScrolling)

                # Add Saved Fields to Character Data Dictionary
                GlobalInst.SavedData["InventoryListNameEntryVar" + str(self.Row)] = self.NameEntryVar
                GlobalInst.SavedData["InventoryListCountEntryVar" + str(self.Row)] = self.CountEntryVar
                GlobalInst.SavedData["InventoryListUnitWeightEntryVar" + str(self.Row)] = self.UnitWeightEntryVar
                GlobalInst.SavedData["InventoryListUnitValueEntryVar" + str(self.Row)] = self.UnitValueEntryVar
                GlobalInst.SavedData["InventoryListUnitValueDenominationVar" + str(self.Row)] = self.UnitValueDenominationVar
                GlobalInst.SavedData["InventoryListCategoryTagVar" + str(self.Row)] = self.CategoryTagVar
                GlobalInst.SavedData["InventoryListMagicItemCategoryEntryVar" + str(self.Row)] = self.CategoryEntryVar
                GlobalInst.SavedData["InventoryListMagicItemRarityEntryVar" + str(self.Row)] = self.RarityEntryVar
                GlobalInst.SavedData["InventoryListMagicItemDescriptionVar" + str(self.Row)] = self.DescriptionVar

            def DisableScrolling(self, event):
                self.ScrollingDisabledVar.set(True)

            def EnableScrolling(self, event):
                self.ScrollingDisabledVar.set(False)

            def ConfigureMagicItem(self, event):
                # Create Window and Wait
                MagicItemMenuInst = self.MagicItemMenu(root, self.NameEntryVar, self.CategoryEntryVar, self.RarityEntryVar, self.DescriptionVar)
                root.wait_window(MagicItemMenuInst.Window)

                # Handle Variables
                if MagicItemMenuInst.DataSubmitted.get():
                    self.NameEntryVar.set(MagicItemMenuInst.NameEntryVar.get())
                    self.CategoryEntryVar.set(MagicItemMenuInst.CategoryEntryVar.get())
                    self.RarityEntryVar.set(MagicItemMenuInst.RarityEntryVar.get())
                    self.DescriptionVar.set(MagicItemMenuInst.DescriptionVar.get())

            class MagicItemMenu:
                def __init__(self, master, NameEntryVar, CategoryEntryVar, RarityEntryVar, DescriptionVar):
                    self.DataSubmitted = BooleanVar()
                    self.NameEntryVar = StringVar(value=NameEntryVar.get())
                    self.CategoryEntryVar = StringVar(value=CategoryEntryVar.get())
                    self.RarityEntryVar = StringVar(value=RarityEntryVar.get())
                    self.DescriptionVar = StringVar(value=DescriptionVar.get())

                    # Create Window
                    self.Window = Toplevel(master)
                    self.Window.wm_attributes("-toolwindow", 1)
                    self.Window.wm_title("Magic Item Description")

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
                    GlobalInst.WindowGeometry(self.Window, True)
                    self.Window.focus_force()

                def Submit(self):
                    self.DataSubmitted.set(True)
                    self.DescriptionVar.set(self.DescriptionField.get())
                    self.Window.destroy()

                def Cancel(self):
                    self.DataSubmitted.set(False)
                    self.Window.destroy()

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
                self.CalculateButton = Button(self.Window, text="Calculate", command=self.Calculate, bg=GlobalInst.ButtonColor)
                self.CalculateButton.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
                self.CloseButton = Button(self.Window, text="Close", command=self.Close, bg=GlobalInst.ButtonColor)
                self.CloseButton.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)

                # Prevent Main Window Input
                self.Window.grab_set()

                # Handle Config Window Geometry and Focus
                GlobalInst.WindowGeometry(self.Window, True)
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

    # Notes
    class Notes:
        def __init__(self, master):
            # Center Widgets
            master.grid_columnconfigure(0, weight=1)
            master.grid_columnconfigure(2, weight=1)
            master.grid_columnconfigure(4, weight=1)
            master.grid_columnconfigure(6, weight=1)

            # Notes Text Boxes
            self.NotesField1 = ScrolledText(master, Height=497, Width=220)
            self.NotesField1.grid(row=0, column=1, padx=2, pady=2)
            self.NotesField2 = ScrolledText(master, Height=497, Width=220)
            self.NotesField2.grid(row=0, column=3, padx=2, pady=2)
            self.NotesField3 = ScrolledText(master, Height=497, Width=220)
            self.NotesField3.grid(row=0, column=5, padx=2, pady=2)

            # Add Saved Field to Character Data Dictionary
            GlobalInst.SavedData["NotesField1"] = self.NotesField1
            GlobalInst.SavedData["NotesField2"] = self.NotesField2
            GlobalInst.SavedData["NotesField3"] = self.NotesField3

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
            self.PhysicalAppearanceField = ScrolledText(self.PhysicalAppearanceFrame, Width=155, Height=289)
            self.PhysicalAppearanceField.grid(row=0, column=0)

            # Second Column
            self.SecondColumnFrame = Frame(master)
            self.SecondColumnFrame.grid(row=1, column=3)

            # Personality Traits
            self.PersonalityTraitsFrame = LabelFrame(self.SecondColumnFrame, text="Personality Traits:")
            self.PersonalityTraitsFrame.grid(row=0, column=0, padx=2, pady=2)
            self.PersonalityTraitsField = ScrolledText(self.PersonalityTraitsFrame, Width=155, Height=225)
            self.PersonalityTraitsField.grid(row=0, column=0)

            # Bonds
            self.BondsFrame = LabelFrame(self.SecondColumnFrame, text="Bonds:")
            self.BondsFrame.grid(row=1, column=0, padx=2, pady=2)
            self.BondsField = ScrolledText(self.BondsFrame, Width=155, Height=225)
            self.BondsField.grid(row=0, column=0)

            # Third Column
            self.ThirdColumnFrame = Frame(master)
            self.ThirdColumnFrame.grid(row=1, column=5)

            # Ideals
            self.IdealsFrame = LabelFrame(self.ThirdColumnFrame, text="Ideals:")
            self.IdealsFrame.grid(row=0, column=0, padx=2, pady=2)
            self.IdealsField = ScrolledText(self.IdealsFrame, Width=155, Height=225)
            self.IdealsField.grid(row=0, column=0)

            # Flaws
            self.FlawsFrame = LabelFrame(self.ThirdColumnFrame, text="Flaws:")
            self.FlawsFrame.grid(row=1, column=0, padx=2, pady=2)
            self.FlawsField = ScrolledText(self.FlawsFrame, Width=155, Height=225)
            self.FlawsField.grid(row=0, column=0)

            # Fourth Column
            self.FourthColumnFrame = Frame(master)
            self.FourthColumnFrame.grid(row=1, column=7)

            # Backstory
            self.BackstoryFrame = LabelFrame(self.FourthColumnFrame, text="Backstory:")
            self.BackstoryFrame.grid(row=0, column=0, padx=2, pady=2)
            self.BackstoryField = ScrolledText(self.BackstoryFrame, Width=155, Height=473)
            self.BackstoryField.grid(row=0, column=0)

            # Add Saved Fields to Character Data Dictionary
            GlobalInst.SavedData["RaceEntryVar"] = self.RaceEntryVar
            GlobalInst.SavedData["BackgroundEntryVar"] = self.BackgroundEntryVar
            GlobalInst.SavedData["AlignmentEntryVar"] = self.AlignmentEntryVar
            GlobalInst.SavedData["AgeEntryVar"] = self.AgeEntryVar
            GlobalInst.SavedData["PhysicalAppearanceField"] = self.PhysicalAppearanceField
            GlobalInst.SavedData["PersonalityTraitsField"] = self.PersonalityTraitsField
            GlobalInst.SavedData["BondsField"] = self.BondsField
            GlobalInst.SavedData["IdealsField"] = self.IdealsField
            GlobalInst.SavedData["FlawsField"] = self.FlawsField
            GlobalInst.SavedData["BackstoryField"] = self.BackstoryField

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
            self.SelectButton = Button(self.PortraitHolderFrame, text="Select", command=self.Select, bg=GlobalInst.ButtonColor)
            self.SelectButton.grid(row=1, column=0, sticky=NSEW)
            self.ExportButton = Button(self.PortraitHolderFrame, text="Export", command=self.Export, bg=GlobalInst.ButtonColor)
            self.ExportButton.grid(row=1, column=1, sticky=NSEW)
            self.ClearButton = Button(self.PortraitHolderFrame, text="Clear", command=self.Clear, bg=GlobalInst.ButtonColor)
            self.ClearButton.grid(row=1, column=2, sticky=NSEW)

            # Portrait Instructions
            self.PortraitInstructions = Label(self.PortraitHolderFrame, text="Portrait must be a .gif file no larger than 400 x 400.")
            self.PortraitInstructions.grid(row=2, column=0, columnspan=3, sticky=NSEW)

            # Add Saved Field to Character Data Dictionary
            GlobalInst.SavedData["PortraitSelectedVar"] = self.PortraitSelectedVar

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
            if ExportFileName != "":
                self.PortraitImage.write(ExportFileName)

        def Clear(self):
            if self.PortraitSelectedVar.get():
                ClearConfirm = messagebox.askyesno("Clear Portrait", "Are you sure you want to clear the portrait?  This cannot be undone.")
                if not ClearConfirm:
                    return
            self.PortraitSelectedVar.set(False)
            self.PortraitCanvas.delete("all")


class DiceRoller:
    def __init__(self, master):
        self.DiceNumberEntryVar = StringVar(value="1")
        self.DieTypeEntryVar = StringVar(value="20")
        self.ModifierEntryVar = StringVar(value="0")

        # Dice Roller Frame
        self.DiceRollerFrame = LabelFrame(master, text="Dice Roller:")
        self.DiceRollerFrame.grid(row=1, column=1, padx=2, pady=2, sticky=NSEW)

        # Dice Entry and Buttons Frame
        self.DiceEntryAndButtonsFrame = Frame(self.DiceRollerFrame)
        self.DiceEntryAndButtonsFrame.grid_columnconfigure(0, weight=1)
        self.DiceEntryAndButtonsFrame.grid_columnconfigure(2, weight=1)
        self.DiceEntryAndButtonsFrame.grid_columnconfigure(4, weight=1)
        self.DiceEntryAndButtonsFrame.grid(row=0, column=0, sticky=NSEW)

        # Dice Entry Font
        self.DiceEntryFont = font.Font(size=18)

        # Number of Dice
        self.DiceNumberEntry = Entry(self.DiceEntryAndButtonsFrame, textvariable=self.DiceNumberEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor, font=self.DiceEntryFont)
        self.DiceNumberEntry.grid(row=0, column=0, rowspan=2, padx=2, pady=2, sticky=NSEW)

        # Die Type
        self.DieTypeLabel = Label(self.DiceEntryAndButtonsFrame, text="d", font=self.DiceEntryFont)
        self.DieTypeLabel.grid(row=0, column=1, rowspan=2, sticky=NSEW)
        self.DieTypeEntry = Entry(self.DiceEntryAndButtonsFrame, textvariable=self.DieTypeEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor, font=self.DiceEntryFont)
        self.DieTypeEntry.grid(row=0, column=2, rowspan=2, padx=2, pady=2, sticky=NSEW)

        # Modifier
        self.ModifierLabel = Label(self.DiceEntryAndButtonsFrame, text="+", font=self.DiceEntryFont)
        self.ModifierLabel.grid(row=0, column=3, rowspan=2, sticky=NSEW)
        self.ModifierEntry = Entry(self.DiceEntryAndButtonsFrame, textvariable=self.ModifierEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor, font=self.DiceEntryFont)
        self.ModifierEntry.grid(row=0, column=4, rowspan=2, padx=2, pady=2, sticky=NSEW)

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
        self.RollButton = Button(self.DiceEntryAndButtonsFrame, text="Roll", command=self.Roll, width=7, bg=GlobalInst.ButtonColor)
        self.RollButton.grid(row=0, column=5, padx=2, pady=2)

        # Average Roll Button
        self.AverageRollButton = Button(self.DiceEntryAndButtonsFrame, text="Avg. Roll", command=self.AverageRoll, width=7, bg=GlobalInst.ButtonColor)
        self.AverageRollButton.grid(row=1, column=5, padx=2, pady=2)

        # Results
        self.ResultsFieldFrame = LabelFrame(self.DiceRollerFrame, text="Results:")
        self.ResultsFieldFrame.grid(row=2, column=0, padx=2, pady=2)
        self.ResultsField = ScrolledText(self.ResultsFieldFrame, Width=335, Height=154, Disabled=True, DisabledBackground=GlobalInst.ButtonColor)
        self.ResultsField.grid(row=0, column=0, padx=2, pady=2)
        self.ResultsField.Text.bind("<Button-1>", self.CopyResults)
        self.ResultsField.Text.bind("<Button-3>", self.ClearResults)

        # Preset Rolls
        self.PresetRollsInst = self.PresetRolls(self.DiceRollerFrame)

        # Add Saved Field to Character Data Dictionary
        GlobalInst.SavedData["ResultsField"] = self.ResultsField

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
        return True

    def MouseWheelEvent(self, event, EntryVar, MinValue=None, MaxValue=None, DieStep=False):
        OldValue = GlobalInst.GetStringVarAsNumber(EntryVar)
        if GlobalInst.OS == "Windows" or GlobalInst.OS == "Linux":
            NewValue = OldValue + int((event.delta / 120))
        elif GlobalInst.OS == "Darwin":
            NewValue = OldValue + int(event.delta)
        else:
            messagebox.showerror("Scrolling Not Supported", "Some scrolling features are not supported on your OS.")
            return
        if MinValue != None:
            NewValue = max(MinValue, NewValue)
        if MaxValue != None:
            NewValue = min(MaxValue, NewValue)
        if DieStep:
            ValueDelta = NewValue - OldValue
            if NewValue < 4:
                NewValue = 4
            elif NewValue > 100:
                NewValue = 100
            else:
                if ValueDelta > 0:
                    if NewValue > 4 and NewValue < 6:
                        NewValue = 6
                    elif NewValue > 6 and NewValue < 8:
                        NewValue = 8
                    elif NewValue > 8 and NewValue < 10:
                        NewValue = 10
                    elif NewValue > 10 and NewValue < 12:
                        NewValue = 12
                    elif NewValue > 12 and NewValue < 20:
                        NewValue = 20
                    elif NewValue > 20:
                        NewValue = 100
                elif ValueDelta < 0:
                    if NewValue > 4 and NewValue < 6:
                        NewValue = 4
                    elif NewValue > 6 and NewValue < 8:
                        NewValue = 6
                    elif NewValue > 8 and NewValue < 10:
                        NewValue = 8
                    elif NewValue > 10 and NewValue < 12:
                        NewValue = 10
                    elif NewValue > 12 and NewValue < 20:
                        NewValue = 12
                    elif NewValue > 20 and NewValue < 100:
                        NewValue = 20
                else:
                    return
        EntryVar.set(str(NewValue))

    def CopyResults(self, event):
        self.ResultsField.Text.clipboard_clear()
        self.ResultsField.Text.clipboard_append(self.ResultsField.get())
        ToolbarAndStatusBarInst.ToolbarSetText("Results copied to clipboard.", Lock=True)
        root.after(2000, lambda: ToolbarAndStatusBarInst.ToolbarSetText("Status", Unlock=True))

    def ClearResults(self, event):
        # Confirm
        ClearConfirm = messagebox.askyesno("Clear Results", "Are you sure you want to clear the roll results?  This cannot be undone.")
        if not ClearConfirm:
            return

        # Clear
        self.ResultsField.set("")

    class PresetRolls:
        def __init__(self, master):
            # Preset Rolls Frame
            self.PresetRollsFrame = LabelFrame(master, text="Preset Rolls:")
            self.PresetRollsFrame.grid(row=3, column=0, padx=2, pady=2)

            # Scrolled Canvas
            self.PresetRollsScrolledCanvas = ScrolledCanvas(self.PresetRollsFrame, Height=220, Width=322)

            # Preset Rolls List
            self.PresetRollsList = []

            # Preset Rolls
            for CurrentIndex in range(50):
                self.PresetRollEntry(self.PresetRollsScrolledCanvas.WindowFrame, self.PresetRollsList, CurrentIndex + 1)

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

                # Set Row Size
                master.grid_rowconfigure(self.Row, minsize=26)

                # Add to List
                List.append(self)

                # Name
                self.PresetRollNameEntry = Entry(master, justify=CENTER, width=25, textvariable=self.PresetRollNameEntryVar)
                self.PresetRollNameEntry.grid(row=self.Row, column=0, sticky=NSEW)

                # Roll Button
                self.PresetRollButton = Button(master, text="Roll:", command=self.RollPreset, bg=GlobalInst.ButtonColor)
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
                self.PresetRollModifierButton = Button(master, text="+", command=self.ConfigureModifier, bg=GlobalInst.ButtonColor)
                self.PresetRollModifierButton.grid(row=self.Row, column=5, sticky=NSEW)
                self.PresetRollModifierEntry = Entry(master, justify=CENTER, width=5, textvariable=self.PresetRollModifierEntryVar, disabledbackground="light gray", disabledforeground="black")
                self.PresetRollModifierEntry.grid(row=self.Row, column=6, sticky=NSEW)

                # Add Saved Fields to Character Data Dictionary
                GlobalInst.SavedData["PresetRollNameEntryVar" + str(self.Row)] = self.PresetRollNameEntryVar
                GlobalInst.SavedData["PresetRollDiceNumberEntryVar" + str(self.Row)] = self.PresetRollDiceNumberEntryVar
                GlobalInst.SavedData["PresetRollDieTypeEntryVar" + str(self.Row)] = self.PresetRollDieTypeEntryVar
                GlobalInst.SavedData["PresetRollModifierEntryVar" + str(self.Row)] = self.PresetRollModifierEntryVar
                GlobalInst.SavedData["ConfigSubmitted" + str(self.Row)] = self.ConfigSubmitted
                GlobalInst.SavedData["StrengthBoxVar" + str(self.Row)] = self.StrengthBoxVar
                GlobalInst.SavedData["DexterityBoxVar" + str(self.Row)] = self.DexterityBoxVar
                GlobalInst.SavedData["ConstitutionBoxVar" + str(self.Row)] = self.ConstitutionBoxVar
                GlobalInst.SavedData["IntelligenceBoxVar" + str(self.Row)] = self.IntelligenceBoxVar
                GlobalInst.SavedData["WisdomBoxVar" + str(self.Row)] = self.WisdomBoxVar
                GlobalInst.SavedData["CharismaBoxVar" + str(self.Row)] = self.CharismaBoxVar
                GlobalInst.SavedData["ProficiencyBoxVar" + str(self.Row)] = self.ProficiencyBoxVar
                GlobalInst.SavedData["ManualBonusEntryVar" + str(self.Row)] = self.ManualBonusEntryVar

            def RollPreset(self):
                DiceRollerInst.DiceNumberEntryVar.set(self.PresetRollDiceNumberEntry.get())
                DiceRollerInst.DieTypeEntryVar.set(self.PresetRollDieTypeEntry.get())
                DiceRollerInst.ModifierEntryVar.set(self.PresetRollModifierEntry.get())
                DiceRollerInst.Roll(self.PresetRollNameEntryVar.get() + ":\n")

            def ConfigureModifier(self):
                # Test Level Input Validity
                if CharacterSheetHeaderInst.ValidLevelEntry():
                    pass
                else:
                    return

                # Test Ability Input Validity
                if CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.ValidStatsEntry():
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
                    GlobalInst.UpdateStatsAndInventory()
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
                        Modifier += GlobalInst.GetStringVarAsNumber(CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.StrengthEntry.AbilityEntryModifierVar)
                    if self.DexterityBoxVar.get():
                        Modifier += GlobalInst.GetStringVarAsNumber(CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.DexterityEntry.AbilityEntryModifierVar)
                    if self.ConstitutionBoxVar.get():
                        Modifier += GlobalInst.GetStringVarAsNumber(CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.ConstitutionEntry.AbilityEntryModifierVar)
                    if self.IntelligenceBoxVar.get():
                        Modifier += GlobalInst.GetStringVarAsNumber(CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.IntelligenceEntry.AbilityEntryModifierVar)
                    if self.WisdomBoxVar.get():
                        Modifier += GlobalInst.GetStringVarAsNumber(CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.WisdomEntry.AbilityEntryModifierVar)
                    if self.CharismaBoxVar.get():
                        Modifier += GlobalInst.GetStringVarAsNumber(CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.CharismaEntry.AbilityEntryModifierVar)
                    if self.ProficiencyBoxVar.get():
                        Modifier += GlobalInst.GetStringVarAsNumber(CharacterSheetHeaderInst.ProficiencyBonusEntryVar)
                    Modifier += GlobalInst.GetStringVarAsNumber(self.ManualBonusEntryVar)
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
                    self.InstructionLabel.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                    # Boxes
                    self.StrengthBox = Checkbutton(self.Window, text="Strength", variable=self.StrengthBoxVar)
                    self.StrengthBox.grid(row=1, column=0, sticky=W, padx=2, pady=2)
                    self.DexterityBox = Checkbutton(self.Window, text="Dexterity", variable=self.DexterityBoxVar)
                    self.DexterityBox.grid(row=2, column=0, sticky=W, padx=2, pady=2)
                    self.ConstitutionBox = Checkbutton(self.Window, text="Constitution", variable=self.ConstitutionBoxVar)
                    self.ConstitutionBox.grid(row=3, column=0, sticky=W, padx=2, pady=2)
                    self.IntelligenceBox = Checkbutton(self.Window, text="Intelligence", variable=self.IntelligenceBoxVar)
                    self.IntelligenceBox.grid(row=4, column=0, sticky=W, padx=2, pady=2)
                    self.WisdomBox = Checkbutton(self.Window, text="Wisdom", variable=self.WisdomBoxVar)
                    self.WisdomBox.grid(row=5, column=0, sticky=W, padx=2, pady=2)
                    self.CharismaBox = Checkbutton(self.Window, text="Charisma", variable=self.CharismaBoxVar)
                    self.CharismaBox.grid(row=6, column=0, sticky=W, padx=2, pady=2)
                    self.ProficiencyBox = Checkbutton(self.Window, text="Proficiency", variable=self.ProficiencyBoxVar)
                    self.ProficiencyBox.grid(row=7, column=0, sticky=W, padx=2, pady=2)

                    # Manual Bonus Entry
                    self.ManualBonusFrame = LabelFrame(self.Window, text="Manual Bonus:")
                    self.ManualBonusFrame.grid_columnconfigure(0, weight=1)
                    self.ManualBonusFrame.grid(row=8, column=0)
                    self.ManualBonusEntry = Entry(self.ManualBonusFrame, textvariable=self.ManualBonusEntryVar, width=4, justify=CENTER)
                    self.ManualBonusEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                    # Buttons
                    self.ButtonsFrame = Frame(self.Window)
                    self.ButtonsFrame.grid_columnconfigure(0, weight=1)
                    self.ButtonsFrame.grid_columnconfigure(1, weight=1)
                    self.ButtonsFrame.grid(row=9, column=0, padx=2, pady=2, sticky=NSEW)
                    self.SubmitButton = Button(self.ButtonsFrame, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
                    self.SubmitButton.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)
                    self.ClearButton = Button(self.ButtonsFrame, text="Clear", command=self.Clear, bg=GlobalInst.ButtonColor)
                    self.ClearButton.grid(row=0, column=1, padx=2, pady=2, sticky=NSEW)

                    # Prevent Main Window Input
                    self.Window.grab_set()

                    # Handle Config Window Geometry and Focus
                    GlobalInst.WindowGeometry(self.Window, True)
                    self.Window.focus_force()

                def Submit(self):
                    if self.ValidManualBonus():
                        pass
                    else:
                        return
                    self.NewConfigSubmitted.set(True)
                    self.Window.destroy()

                def Clear(self):
                    self.ConfigCleared.set(True)
                    self.Window.destroy()

                def ValidManualBonus(self):
                    try:
                        ManualBonus = GlobalInst.GetStringVarAsNumber(self.ManualBonusEntryVar)
                    except:
                        messagebox.showerror("Invalid Entry", "Manual bonus must be an integer.")
                        return False
                    return True


class Inspiration:
    def __init__(self, master):
        self.InspirationBoxVar = BooleanVar()
        self.InspirationTrueColor = "#7aff63"
        self.InspirationFalseColor = GlobalInst.ButtonColor

        # Inspiration Box Font
        self.InspirationBoxFont = font.Font(size=16)

        # Box
        self.InspirationBox = Checkbutton(master, text="Inspiration", variable=self.InspirationBoxVar, font=self.InspirationBoxFont, indicatoron=False, background=self.InspirationFalseColor, selectcolor=self.InspirationTrueColor)
        self.InspirationBox.grid(row=2, column=1, padx=2, pady=2, sticky=NSEW)

        # Add Saved Field to Saved Data Dictionary
        GlobalInst.SavedData["InspirationBoxVar"] = self.InspirationBoxVar


class ToolbarAndStatusBar:
    def __init__(self, master):
        self.StatusBarTextVar = StringVar(value="Status")
        self.StatusBarLockedVar = BooleanVar(value=False)
        self.CurrentOpenFilePath = StringVar()
        self.PreviousOpenFilePath = StringVar()

        # Toolbar Frame
        self.ToolbarFrame = Frame(master, bg="gray", bd=1, relief=SUNKEN)
        self.ToolbarFrame.grid_columnconfigure(3, weight=1)
        self.ToolbarFrame.grid(row=3, column=0, sticky=NSEW, columnspan=2, padx=2, pady=2)

        # Toolbar Open Button
        self.ToolbarOpenButton = Button(self.ToolbarFrame, text="Open", command=self.OpenButton, bg=GlobalInst.ButtonColor)
        self.ToolbarOpenButton.grid(row=0, column=0, padx=2, pady=2)

        # Toolbar Save Button
        self.ToolbarSaveButton = Button(self.ToolbarFrame, text="Save", command=self.SaveButton, bg=GlobalInst.ButtonColor)
        self.ToolbarSaveButton.grid(row=0, column=1, padx=2, pady=2)

        # Toolbar Save As Button
        self.ToolbarSaveAsButton = Button(self.ToolbarFrame, text="Save As", command=self.SaveAsButton, bg=GlobalInst.ButtonColor)
        self.ToolbarSaveAsButton.grid(row=0, column=2, padx=2, pady=2)

        # Status Bar Label
        self.StatusBarLabel = Label(self.ToolbarFrame, textvariable=self.StatusBarTextVar, fg="white", bg="gray")
        self.StatusBarLabel.grid(row=0, column=3, padx=2, pady=2, sticky=NSEW)

        # Update Stats Button
        self.UpdateStatsButton = Button(self.ToolbarFrame, text="Update Stats and Inventory", command=GlobalInst.UpdateStatsAndInventory, bg=GlobalInst.ButtonColor)
        self.UpdateStatsButton.grid(row=0, column=4, padx=2, pady=2)

    # Save Methods
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
                    self.SaveCharacterData(TextFile)
                SaveFile.write(TextFileName)
                PortraitSelected = GlobalInst.SavedData["PortraitSelectedVar"].get()
                if PortraitSelected:
                    CharacterStatsInventoryAndNotesInst.PortraitInst.PortraitImage.write(PortraitFileName)
                    SaveFile.write(PortraitFileName)
                    os.remove(PortraitFileName)
            os.remove(TextFileName)
            self.CurrentOpenFilePath.set(SaveFileName)
            sleep(0.5)
            GlobalInst.UpdateWindowTitle()
            self.ToolbarSetText("File saved as:  " + os.path.basename(SaveFileName), Lock=True)
            root.after(2000, lambda: self.ToolbarSetText("Status", Unlock=True))
            GlobalInst.SavePrompt = False
            return True
        else:
            self.ToolbarSetText("No file saved!", Lock=True)
            root.after(2000, lambda: self.ToolbarSetText("Status", Unlock=True))
            self.CurrentOpenFilePath.set(self.PreviousOpenFilePath.get())
            return False

    def SaveCharacterData(self, File):
        for Tag, Field in GlobalInst.SavedData.items():
            File.write(json.dumps({Tag: Field.get()}) + "\n")

    def SaveAsButton(self):
        self.PreviousOpenFilePath.set(self.CurrentOpenFilePath.get())
        self.CurrentOpenFilePath.set("")
        self.SaveButton()

    def SaveKeystroke(self, event):
        self.SaveButton()

    def SaveAsKeystroke(self, event):
        self.SaveAsButton()

    # Open Methods
    def OpenButton(self):
        self.StatusBarTextVar.set("Opening...")
        OpenFileName = filedialog.askopenfilename(filetypes=(("Character file", "*.char"), ("All files", "*.*")), defaultextension=".char", title="Open Character File")
        TextFileName = "Character Data.txt"
        PortraitFileName = "Portrait.gif"
        if OpenFileName != "":
            with ZipFile(OpenFileName, mode="r") as OpenFile:
                with open(OpenFile.extract(TextFileName), mode="r") as TextFile:
                    self.OpenCharacterData(TextFile)
                if GlobalInst.SavedData["PortraitSelectedVar"].get():
                    OpenFile.extract(PortraitFileName)
                    CharacterStatsInventoryAndNotesInst.PortraitInst.SetPortrait(PortraitFileName)
                    os.remove(PortraitFileName)
            os.remove(TextFileName)
            self.CurrentOpenFilePath.set(OpenFileName)
            GlobalInst.UpdateStatsAndInventory()
            sleep(0.5)
            self.ToolbarSetText("Opened file:  " + os.path.basename(OpenFileName), Lock=True)
            root.after(2000, lambda: self.ToolbarSetText("Status", Unlock=True))
            GlobalInst.SavePrompt = False
        else:
            self.ToolbarSetText("No file opened!", Lock=True)
            root.after(2000, lambda: self.ToolbarSetText("Status", Unlock=True))

    def OpenCharacterData(self, File):
        for Line in File:
            if Line != "":
                LoadedLine = json.loads(Line)
                for Tag, Field in LoadedLine.items():
                    GlobalInst.SavedData[Tag].set(Field)
        for Entry in DiceRollerInst.PresetRollsInst.PresetRollsList:
            if Entry.ConfigSubmitted.get():
                Entry.PresetRollModifierEntry.configure(state=DISABLED, cursor="arrow")
        CharacterSheetHeaderInst.SpellcasterToggle()

    def OpenKeystroke(self, event):
        self.OpenButton()

    # Toolbar Text Methods
    def ToolbarSetText(self, Text, Lock=False, Unlock=False):
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
        Widget.bind("<Enter>", lambda event: ToolbarAndStatusBarInst.ToolbarSetText(TooltipText, Lock=EnterLock, Unlock=EnterUnlock))
        Widget.bind("<Leave>", lambda event: ToolbarAndStatusBarInst.ToolbarSetText(LeaveText, Lock=LeaveLock, Unlock=LeaveUnlock))

    # Update Stats Keystroke
    def UpdateStatsKeystroke(self, event):
        GlobalInst.UpdateStatsAndInventory()


# Misc
class Global:
    def __init__(self):
        self.OS = platform.system()
        self.ButtonColor = "#F1F1D4"
        self.SavedData = {}
        self.SavePrompt = False

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

    def WindowGeometry(self, Window, IsDialog):
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

    def UpdateStatsAndInventory(self):
        # Test Level Input Validity
        if CharacterSheetHeaderInst.ValidLevelEntry():
            pass
        else:
            return

        # Test Ability Input Validity
        if CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.ValidStatsEntry():
            pass
        else:
            return

        # Store Level
        CharacterLevelValue = GlobalInst.GetStringVarAsNumber(CharacterSheetHeaderInst.CharacterLevelEntryVar)

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
            TotalExperienceNeeded = "N/A"
        CharacterSheetHeaderInst.CharacterExperienceNeededEntryVar.set(TotalExperienceNeeded)
        CharacterSheetHeaderInst.ProficiencyBonusEntryVar.set("+" + str(ProficiencyModifier))

        # Calculate Ability and Saving Throw Modifiers
        for Entry in CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.AbilityEntriesList:
            Entry.CalculateModifiers(ProficiencyModifier)

        # Store Ability Modifiers
        StrengthModifier = GlobalInst.GetStringVarAsNumber(CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.StrengthEntry.AbilityEntryModifierVar)
        DexterityModifier = GlobalInst.GetStringVarAsNumber(CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.DexterityEntry.AbilityEntryModifierVar)
        ConstitutionModifier = GlobalInst.GetStringVarAsNumber(CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.ConstitutionEntry.AbilityEntryModifierVar)
        IntelligenceModifier = GlobalInst.GetStringVarAsNumber(CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.IntelligenceEntry.AbilityEntryModifierVar)
        WisdomModifier = GlobalInst.GetStringVarAsNumber(CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.WisdomEntry.AbilityEntryModifierVar)
        CharismaModifier = GlobalInst.GetStringVarAsNumber(CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.CharismaEntry.AbilityEntryModifierVar)

        # Calculate Skill Modifiers
        for Entry in CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.SkillsInst.SkillsEntriesList:
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
        for Entry in DiceRollerInst.PresetRollsInst.PresetRollsList:
            Entry.SetConfiguredModifier()

        # Test Inventory Input Validity
        if CharacterStatsInventoryAndNotesInst.InventoryInst.ValidInventoryEntry():
            pass
        else:
            return

        # Calculate Inventory
        CharacterStatsInventoryAndNotesInst.InventoryInst.Calculate()

        # Calculate AC
        ACBase = GlobalInst.GetStringVarAsNumber(CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.ACBaseEntryVar)
        ACModifierString = CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.ACModifierVar.get()
        ACManualBonus = GlobalInst.GetStringVarAsNumber(CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.ACManualBonusEntryVar)
        if ACModifierString == "Dexterity":
            ACModifier = DexterityModifier
        elif ACModifierString == "Dexterity (Max 2)":
            ACModifier = min(DexterityModifier, 2)
        else:
            ACModifier = 0
        CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.ACEntryVar.set(str(ACBase + ACModifier + ACManualBonus))

        # Calculate Initiative Bonus
        InitiativeManualBonus = GlobalInst.GetStringVarAsNumber(CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.InitiativeManualBonusEntryVar)
        TotalInitiativeBonus = InitiativeManualBonus + DexterityModifier
        InitiativeBonusSign = ""
        if TotalInitiativeBonus > 0:
            InitiativeBonusSign = "+"
        CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.InitiativeEntryVar.set(InitiativeBonusSign + str(TotalInitiativeBonus))

        # Calculate Passive Perception and Investigation
        PassivePerceptionManualBonus = GlobalInst.GetStringVarAsNumber(CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.PassivePerceptionManualBonusEntryVar)
        PassiveInvestigationManualBonus = GlobalInst.GetStringVarAsNumber(CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.PassiveInvestigationManualBonusEntryVar)
        PerceptionBonus = GlobalInst.GetStringVarAsNumber(CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.SkillsInst.SkillsEntryPerceptionInst.TotalModifierVar)
        InvestigationBonus = GlobalInst.GetStringVarAsNumber(CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.SkillsInst.SkillsEntryInvestigationInst.TotalModifierVar)
        CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.PassivePerceptionEntryVar.set(str(10 + PerceptionBonus + PassivePerceptionManualBonus))
        CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.PassiveInvestigationEntryVar.set(str(10 + InvestigationBonus + PassiveInvestigationManualBonus))

        # Calculate Spellcasting
        for Ability in CharacterStatsInventoryAndNotesInst.SpellcastingInst.SpellcastingAbilitiesList:
            SpellcastingAbility = Ability.SpellcastingAbilitySelectionDropdownVar.get()
            SpellcastingAbilityModifier = 0
            SpellAttackModifierManualBonus = GlobalInst.GetStringVarAsNumber(Ability.SpellAttackModifierManualBonusVar)
            SpellSaveDCManualBonus = GlobalInst.GetStringVarAsNumber(Ability.SpellSaveDCManualBonusVar)
            if SpellcastingAbility != "":
                if SpellcastingAbility == "STR":
                    SpellcastingAbilityModifier = StrengthModifier
                elif SpellcastingAbility == "DEX":
                    SpellcastingAbilityModifier = DexterityModifier
                elif SpellcastingAbility == "CON":
                    SpellcastingAbilityModifier = ConstitutionModifier
                elif SpellcastingAbility == "INT":
                    SpellcastingAbilityModifier = IntelligenceModifier
                elif SpellcastingAbility == "WIS":
                    SpellcastingAbilityModifier = WisdomModifier
                elif SpellcastingAbility == "CHA":
                    SpellcastingAbilityModifier = CharismaModifier
                SpellAttackModifier = SpellcastingAbilityModifier + ProficiencyModifier + SpellAttackModifierManualBonus
                SpellAttackModifierSign = ""
                if SpellAttackModifier > 0:
                    SpellAttackModifierSign = "+"
                Ability.SpellAttackModifierEntryVar.set(SpellAttackModifierSign + str(SpellAttackModifier))
                SpellSaveDC = SpellcastingAbilityModifier + ProficiencyModifier + SpellSaveDCManualBonus + 8
                Ability.SpellSaveDCEntryVar.set(str(SpellSaveDC))
            elif SpellcastingAbility == "":
                Ability.SpellAttackModifierEntryVar.set("N/A")
                Ability.SpellSaveDCEntryVar.set("N/A")
        CharacterStatsInventoryAndNotesInst.SpellcastingInst.CalculateSpellPoints()

        # Update Window Title
        self.UpdateWindowTitle(AddSavePrompt=self.SavePrompt)

    def UpdateWindowTitle(self, AddSavePrompt=False):
        CharacterName = CharacterSheetHeaderInst.CharacterNameEntryVar.get()
        CurrentOpenFile = ToolbarAndStatusBarInst.CurrentOpenFilePath.get()
        SavePromptString = ""
        if CurrentOpenFile != "":
            CurrentOpenFile = " [" + os.path.basename(CurrentOpenFile) + "]"
        if CharacterName != "":
            CharacterName += " - "
        if AddSavePrompt:
            SavePromptString = " *"
        root.wm_title(CharacterName + "Character Sheet" + CurrentOpenFile + SavePromptString)

    def ConfigureBindings(self):
        # Update Stats Keystroke and Tooltip
        root.bind("<Control-d>", ToolbarAndStatusBarInst.UpdateStatsKeystroke)
        ToolbarAndStatusBarInst.TooltipConfig(ToolbarAndStatusBarInst.UpdateStatsButton, "Keyboard Shortcut:  Ctrl+D")

        # Scrolling
        DiceRollerInst.PresetRollsInst.PresetRollsScrolledCanvas.BindEnterAndLeaveToBindMouseWheel()
        CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.FeaturesAndCreatureStatsInst.FeaturesScrolledCanvas.BindEnterAndLeaveToBindMouseWheel()
        CharacterStatsInventoryAndNotesInst.InventoryInst.InventoryListScrolledCanvas.BindEnterAndLeaveToBindMouseWheel()

        # Save and Open Keystrokes and Tooltips
        root.bind("<Control-s>", ToolbarAndStatusBarInst.SaveKeystroke)
        root.bind("<Control-S>", ToolbarAndStatusBarInst.SaveAsKeystroke)
        root.bind("<Control-o>", ToolbarAndStatusBarInst.OpenKeystroke)
        ToolbarAndStatusBarInst.TooltipConfig(ToolbarAndStatusBarInst.ToolbarSaveButton, "Keyboard Shortcut:  Ctrl+S")
        ToolbarAndStatusBarInst.TooltipConfig(ToolbarAndStatusBarInst.ToolbarSaveAsButton, "Keyboard Shortcut:  Ctrl+Shift+S")
        ToolbarAndStatusBarInst.TooltipConfig(ToolbarAndStatusBarInst.ToolbarOpenButton, "Keyboard Shortcut:  Ctrl+O")

        # Ability and Saving Throw Roll Tooltips
        for Entry in CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.AbilitiesAndSavingThrowsInst.AbilityEntriesList:
            ToolbarAndStatusBarInst.TooltipConfig(Entry.AbilityEntryModifier, "Left-click on an ability or saving throw modifier to roll 1d20 with it.")
            ToolbarAndStatusBarInst.TooltipConfig(Entry.AbilitySavingThrowModifier, "Left-click on an ability or saving throw modifier to roll 1d20 with it.")

        # Skill Roll Tooltips
        for Entry in CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.SkillsInst.SkillsEntriesList:
            ToolbarAndStatusBarInst.TooltipConfig(Entry.ModifierEntry, "Left-click on a skill modifier to roll 1d20 with it.")

        # Passive Perception and Investigation Tooltips
        ToolbarAndStatusBarInst.TooltipConfig(CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.PassivePerceptionEntry, "Left-click on Passive Perception to set a manual bonus.")
        ToolbarAndStatusBarInst.TooltipConfig(CharacterStatsInventoryAndNotesInst.AbilitiesAndSkillsInst.PassiveInvestigationEntry, "Left-click on Passive Investigation to set a manual bonus.")

        # AC Tooltip
        ToolbarAndStatusBarInst.TooltipConfig(CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.ACEntry, "Left-click on AC to set data.")

        # Initiative Tooltip
        ToolbarAndStatusBarInst.TooltipConfig(CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.InitiativeEntry,
                                              "Left-click on the initiative modifier to roll 1d20 with it.  Right-click to set a bonus.")

        # Features Tooltips
        for Entry in CharacterStatsInventoryAndNotesInst.CombatAndFeaturesInst.FeaturesAndCreatureStatsInst.FeaturesEntriesList:
            ToolbarAndStatusBarInst.TooltipConfig(Entry.NameEntry, "Left-click on a feature or creature stats entry to set a feature.  Right-click to set creature stats.")

        # Spellcasting Tooltips
        for Ability in CharacterStatsInventoryAndNotesInst.SpellcastingInst.SpellcastingAbilitiesList:
            ToolbarAndStatusBarInst.TooltipConfig(Ability.SpellSaveDCEntry, "Left-click on a spell save DC to set a bonus.")
            ToolbarAndStatusBarInst.TooltipConfig(Ability.SpellAttackModifierEntry, "Left-click on a spell attack modifier to roll 1d20 with it.  Right-click to set a bonus.")
        ToolbarAndStatusBarInst.TooltipConfig(CharacterStatsInventoryAndNotesInst.SpellcastingInst.SpellPointsMaxEntry, "Left-click on the spell points max to set a bonus.")
        ToolbarAndStatusBarInst.TooltipConfig(CharacterStatsInventoryAndNotesInst.SpellcastingInst.SpellPointsRemainingEntry,
                                              "Left-click on the spell points remaining to expend points.  Right-click to restore.")
        for SpellList in CharacterStatsInventoryAndNotesInst.SpellcastingInst.SpellListsList:
            for Entry in SpellList.SpellListEntriesList:
                ToolbarAndStatusBarInst.TooltipConfig(Entry.NameEntry, "Left-click on a spell list entry to set a name and description.")

        # Carrying Capacity Tooltip
        ToolbarAndStatusBarInst.TooltipConfig(CharacterStatsInventoryAndNotesInst.InventoryInst.CarryingCapacityEntry, "Left-click on the carrying capacity to set a bonus.")

        # Magic Items Tooltip
        for Entry in CharacterStatsInventoryAndNotesInst.InventoryInst.InventoryEntriesList:
            ToolbarAndStatusBarInst.TooltipConfig(Entry.NameEntry, "Right-click on the name field to set magic item information.")

        # Dice Roller Tooltips
        ToolbarAndStatusBarInst.TooltipConfig(DiceRollerInst.DiceNumberEntry, "Scroll the mouse wheel or type to change the number of dice.")
        ToolbarAndStatusBarInst.TooltipConfig(DiceRollerInst.DieTypeEntry, "Scroll the mouse wheel or type to change the die type.")
        ToolbarAndStatusBarInst.TooltipConfig(DiceRollerInst.ModifierEntry, "Scroll the mouse wheel or type to change the modifier.")
        ToolbarAndStatusBarInst.TooltipConfig(DiceRollerInst.ResultsField.ScrolledTextFrame, "Left-click to copy results to the clipboard.  Right-click to clear.")

        # Track Modified Fields
        for Field in self.SavedData.values():
            FieldType = type(Field)
            if FieldType == StringVar or FieldType == BooleanVar:
                Field.trace("w", lambda a, b, c, Field=Field, FieldType=FieldType: self.CharacterDataModified(Field, FieldType))
            elif FieldType == ScrolledText:
                Field.Text.bind("<<Modified>>", lambda event, Field=Field.Text, FieldType=FieldType: self.CharacterDataModified(Field, FieldType))

        # Bind Closing Protocol
        root.wm_protocol("WM_DELETE_WINDOW", self.CloseWindow)

    def CharacterDataModified(self, Field, FieldType):
        if FieldType == ScrolledText:
            Field.edit_modified(False)
        self.SavePrompt = True
        self.UpdateWindowTitle(AddSavePrompt=True)

    def CloseWindow(self):
        if self.SavePrompt:
            SaveConfirm = messagebox.askyesnocancel("Save", "Save unsaved work before closing?")
            if SaveConfirm == None:
                return
            elif SaveConfirm == True:
                if not ToolbarAndStatusBarInst.SaveButton():
                    return
        root.destroy()


class ScrolledText:
    def __init__(self, master, Width=100, Height=100, Disabled=False, DisabledBackground="light gray"):
        self.Width = Width
        self.Height = Height
        self.Disabled = Disabled

        # Scrolled Text Frame
        self.ScrolledTextFrame = Frame(master, width=self.Width, height=self.Height)
        self.ScrolledTextFrame.pack_propagate(False)
        self.ScrolledTextFrame.grid_propagate(False)

        # Scrollbar
        self.Scrollbar = Scrollbar(self.ScrolledTextFrame, orient=VERTICAL)
        self.Scrollbar.pack(side=RIGHT, fill=Y)

        # Text Widget
        self.Text = Text(self.ScrolledTextFrame, wrap=WORD)
        self.Text.pack(side=LEFT, expand=YES, fill=BOTH)
        if self.Disabled:
            self.Text.configure(state=DISABLED, bg=DisabledBackground, cursor="arrow")

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


class ScrolledCanvas:
    def __init__(self, master, Height=100, Width=100, ScrollingDisabledVar=None):
        self.Height = Height
        self.Width = Width
        self.ScrollingDisabledVar = ScrollingDisabledVar

        # Canvas
        self.Canvas = Canvas(master, highlightthickness=0, height=self.Height, width=self.Width)
        self.Canvas.pack(side=LEFT, expand=YES, fill=BOTH)
        self.Scrollbar = Scrollbar(master, orient=VERTICAL, command=self.Canvas.yview)
        self.Scrollbar.pack(side=RIGHT, fill=Y)
        self.WindowFrame = Frame(self.Canvas)
        self.Canvas.create_window((0, 0), window=self.WindowFrame, anchor=NW)
        self.Canvas.config(yscrollcommand=self.Scrollbar.set)
        self.Canvas.bind("<Configure>", self.ConfigureScrolledCanvas)

    def ConfigureScrolledCanvas(self, event):
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
        if GlobalInst.OS == "Windows" or GlobalInst.OS == "Linux":
            self.Canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif GlobalInst.OS == "Darwin":
            self.Canvas.yview_scroll(int(-1 * event.delta), "units")

    def BindMouseWheel(self, event):
        if GlobalInst.OS == "Windows" or GlobalInst.OS == "Darwin":
            root.bind("<MouseWheel>", self.MouseWheelEvent)
        elif GlobalInst.OS == "Linux":
            root.bind("<Button-4>", self.MouseWheelEvent)
            root.bind("<Button-5>", self.MouseWheelEvent)

    def UnbindMouseWheel(self, event):
        root.unbind("<MouseWheel>")


class ManualBonusData:
    def __init__(self, master, ManualBonusVar, BonusTo):
        self.DataSubmitted = BooleanVar()
        self.ManualBonusEntryVar = StringVar(value=ManualBonusVar.get())
        self.BonusTo = BonusTo
        self.WindowTitle = self.BonusTo + " Data"

        # Create Window
        self.Window = Toplevel(master)
        self.Window.wm_attributes("-toolwindow", 1)
        self.Window.wm_title(self.WindowTitle)

        # Table Frame
        self.TableFrame = Frame(self.Window)
        self.TableFrame.grid(row=0, column=0, sticky=NSEW, columnspan=2)

        # Manual Bonus
        self.ManualBonusHeader = Label(self.TableFrame, text="Manual Bonus", bd=2, relief=GROOVE)
        self.ManualBonusHeader.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
        self.ManualBonusEntry = Entry(self.TableFrame, width=20, textvariable=self.ManualBonusEntryVar, justify=CENTER)
        self.ManualBonusEntry.grid(row=1, column=2, sticky=NSEW, padx=2, pady=2)
        self.ManualBonusEntry.bind("<Return>", lambda event: self.Submit())

        # Submit Button
        self.SubmitButton = Button(self.Window, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
        self.SubmitButton.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)

        # Cancel Button
        self.CancelButton = Button(self.Window, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
        self.CancelButton.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)

        # Prevent Main Window Input
        self.Window.grab_set()

        # Handle Config Window Geometry and Focus
        GlobalInst.WindowGeometry(self.Window, True)
        self.Window.focus_force()

        # Focus On Entry
        self.ManualBonusEntry.focus_set()

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

    def GetData(self, ManualBonusVar):
        ManualBonus = self.ManualBonusEntryVar.get()
        ManualBonusVar.set(ManualBonus)

    def ValidEntry(self):
        try:
            GlobalInst.GetStringVarAsNumber(self.ManualBonusEntryVar)
        except:
            messagebox.showerror("Invalid Entry", self.BonusTo + " manual bonus must be a whole number.")
            return False
        return True


class IntegerPrompt:
    def __init__(self, master, WindowTitle, Header, MinValue=None, MaxValue=None):
        self.DataSubmitted = BooleanVar()
        self.IntegerEntryVar = StringVar()
        self.WindowTitle = WindowTitle
        self.Header = Header
        self.MinValue = MinValue
        self.MaxValue = MaxValue

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
        GlobalInst.WindowGeometry(self.Window, True)
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


# Global Functions and Variables
GlobalInst = Global()

# Populate Window
CharacterSheetHeaderInst = CharacterSheetHeader(root)
CharacterStatsInventoryAndNotesInst = CharacterStatsInventoryAndNotes(root)
DiceRollerInst = DiceRoller(root)
InspirationInst = Inspiration(root)
ToolbarAndStatusBarInst = ToolbarAndStatusBar(root)

# Inst-Dependent Bindings
GlobalInst.ConfigureBindings()

# Initial Window Behavior
GlobalInst.WindowGeometry(root, False)
root.focus_force()

# Main Loop
root.mainloop()
