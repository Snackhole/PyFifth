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
root.wm_title("Encounter Manager")
root.option_add("*Font", "TkDefaultFont")


# Window Elements

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
        GlobalInst.SavedData["EncounterNameEntryVar"] = self.EncounterNameEntryVar
        GlobalInst.SavedData["CREntryVar"] = self.CREntryVar
        GlobalInst.SavedData["ExperienceEntryVar"] = self.ExperienceEntryVar
        GlobalInst.SavedData["NotesField1"] = self.NotesField1
        GlobalInst.SavedData["NotesField2"] = self.NotesField2
        GlobalInst.SavedData["NotesField3"] = self.NotesField3
        GlobalInst.SavedData["DescriptionField"] = self.DescriptionField
        GlobalInst.SavedData["RewardsField"] = self.RewardsField


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

        # Next Turn Button
        self.NextTurnButton = Button(self.InitiativeDataFrame, text="Next Turn", command=self.NextTurn, bg=GlobalInst.ButtonColor, font=self.InitiativeDataFont)
        self.NextTurnButton.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)

        # Clear Turns Button
        self.ClearTurnsButton = Button(self.InitiativeDataFrame, text="Clear Turns", command=self.ClearTurns, bg=GlobalInst.ButtonColor, font=self.InitiativeDataFont)
        self.ClearTurnsButton.grid(row=0, column=3, sticky=NSEW, padx=2, pady=2)

        # Sort Initiative Order Button
        self.SortInitiativeOrderButton = Button(self.InitiativeDataFrame, text="Sort Initiative Order", command=self.SortInitiativeOrder, bg=GlobalInst.ButtonColor, font=self.InitiativeDataFont)
        self.SortInitiativeOrderButton.grid(row=0, column=4, sticky=NSEW, padx=2, pady=2)

        # Initiative Order Scrolled Canvas
        self.InitiativeOrderScrolledCanvasFrame = Frame(self.InitiativeOrderFrame)
        self.InitiativeOrderScrolledCanvasFrame.grid(row=1, column=0, sticky=NSEW)
        self.InitiativeOrderScrolledCanvas = ScrolledCanvas(self.InitiativeOrderScrolledCanvasFrame, Height=470, Width=839, ScrollingDisabledVar=self.ScrollingDisabledVar)

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
        GlobalInst.SavedData["RoundEntryVar"] = self.RoundEntryVar

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
        GlobalInst.SavePrompt = True
        GlobalInst.UpdateWindowTitle(AddSavePrompt=True)

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
            self.InitiativeEntryTiePriorityDropdownVar = StringVar(value=str(1))
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
            self.OpenErrors = False

            # Add to List
            self.List.append(self)

            # Initiative Entry
            self.InitiativeEntryResultEntry = Entry(self.master, textvariable=self.InitiativeEntryResultEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
            self.InitiativeEntryResultEntry.bind("<Button-3>", lambda event: self.ToggleTurnDone())

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
            self.InitiativeEntryNameEntry.bind("<Shift-Button-1>", self.Open)

            # AC Entry
            self.InitiativeEntryACEntry = Entry(self.master, textvariable=self.InitiativeEntryACEntryVar, justify=CENTER, width=5)

            # Temp HP Entry
            self.InitiativeEntryTempHPEntry = Entry(self.master, textvariable=self.InitiativeEntryTempHPEntryVar, justify=CENTER, width=5)

            # Current HP Entry
            self.InitiativeEntryCurrentHPEntry = Entry(self.master, textvariable=self.InitiativeEntryCurrentHPEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
            self.InitiativeEntryCurrentHPEntry.bind("<Button-3>", lambda event: self.Damage())
            self.InitiativeEntryCurrentHPEntry.bind("<Shift-Button-3>", lambda event: self.Heal())
            self.InitiativeEntryCurrentHPEntry.bind("<Control-Button-3>", lambda event: self.ToggleDead())

            # Max HP Entry
            self.InitiativeEntryMaxHPEntry = Entry(self.master, textvariable=self.InitiativeEntryMaxHPEntryVar, justify=CENTER, width=5)

            # Concentration Box
            self.InitiativeEntryConcentrationBox = Checkbutton(self.master, text="Conc.", variable=self.InitiativeEntryConcentrationBoxVar, background=self.ConcentrationFalseColor, selectcolor=self.ConcentrationTrueColor,
                                                               indicatoron=False)

            # Conditions Field
            self.InitiativeEntryConditionsField = ScrolledText(self.master, Width=113, Height=35)
            self.InitiativeEntryConditionsField.ScrolledTextFrame.bind("<Enter>", self.DisableScrolling)
            self.InitiativeEntryConditionsField.ScrolledTextFrame.bind("<Leave>", self.EnableScrolling)

            # Location Field
            self.InitiativeEntryLocationField = ScrolledText(self.master, Width=113, Height=35)
            self.InitiativeEntryLocationField.ScrolledTextFrame.bind("<Enter>", self.DisableScrolling)
            self.InitiativeEntryLocationField.ScrolledTextFrame.bind("<Leave>", self.EnableScrolling)

            # Notes Field
            self.InitiativeEntryNotesField = ScrolledText(self.master, Width=113, Height=35)
            self.InitiativeEntryNotesField.ScrolledTextFrame.bind("<Enter>", self.DisableScrolling)
            self.InitiativeEntryNotesField.ScrolledTextFrame.bind("<Leave>", self.EnableScrolling)

            # Create Creature Stats Fields Dictionary
            self.CreatureStatsFields = {}
            self.CreatureStatsFields["NameEntryVar"] = self.InitiativeEntryNameEntryVar
            self.CreatureStatsFields["ACEntryVar"] = self.InitiativeEntryACEntryVar
            self.CreatureStatsFields["MaxHPEntryVar"] = self.InitiativeEntryMaxHPEntryVar
            self.CreatureStatsFields["SizeEntryVar"] = self.InitiativeEntrySizeEntryVar
            self.CreatureStatsFields["TypeAndTagsEntryVar"] = self.InitiativeEntryTypeAndTagsEntryVar
            self.CreatureStatsFields["AlignmentEntryVar"] = self.InitiativeEntryAlignmentEntryVar
            self.CreatureStatsFields["SpeedEntryVar"] = self.InitiativeEntrySpeedEntryVar
            self.CreatureStatsFields["CRAndExperienceEntryVar"] = self.InitiativeEntryCRAndExperienceEntryVar
            self.CreatureStatsFields["AbilitiesStrengthEntryVar"] = self.InitiativeEntryAbilitiesStrengthEntryVar
            self.CreatureStatsFields["AbilitiesDexterityEntryVar"] = self.InitiativeEntryAbilitiesDexterityEntryVar
            self.CreatureStatsFields["AbilitiesConstitutionEntryVar"] = self.InitiativeEntryAbilitiesConstitutionEntryVar
            self.CreatureStatsFields["AbilitiesIntelligenceEntryVar"] = self.InitiativeEntryAbilitiesIntelligenceEntryVar
            self.CreatureStatsFields["AbilitiesWisdomEntryVar"] = self.InitiativeEntryAbilitiesWisdomEntryVar
            self.CreatureStatsFields["AbilitiesCharismaEntryVar"] = self.InitiativeEntryAbilitiesCharismaEntryVar
            self.CreatureStatsFields["SkillSensesAndLanguagesFieldVar"] = self.InitiativeEntrySkillSensesAndLanguagesFieldVar
            self.CreatureStatsFields["SavingThrowsFieldVar"] = self.InitiativeEntrySavingThrowsFieldVar
            self.CreatureStatsFields["VulnerabilitiesResistancesAndImmunitiesFieldVar"] = self.InitiativeEntryVulnerabilitiesResistancesAndImmunitiesFieldVar
            self.CreatureStatsFields["SpecialTraitsFieldVar"] = self.InitiativeEntrySpecialTraitsFieldVar
            self.CreatureStatsFields["ActionsFieldVar"] = self.InitiativeEntryActionsFieldVar
            self.CreatureStatsFields["ReactionsFieldVar"] = self.InitiativeEntryReactionsFieldVar
            self.CreatureStatsFields["InventoryFieldVar"] = self.InitiativeEntryInventoryFieldVar
            self.CreatureStatsFields["LegendaryActionsAndLairActionsFieldVar"] = self.InitiativeEntryLegendaryActionsAndLairActionsFieldVar
            self.CreatureStatsFields["NotesFieldVar"] = self.InitiativeEntryNotesFieldVar

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
            GlobalInst.SavedData["InitiativeEntryInitiativeEntryVar" + str(self.Row)] = self.InitiativeEntryResultEntryVar
            GlobalInst.SavedData["InitiativeEntryTiePriorityDropdownVar" + str(self.Row)] = self.InitiativeEntryTiePriorityDropdownVar
            GlobalInst.SavedData["InitiativeEntryNameEntryVar" + str(self.Row)] = self.InitiativeEntryNameEntryVar
            GlobalInst.SavedData["InitiativeEntryACEntryVar" + str(self.Row)] = self.InitiativeEntryACEntryVar
            GlobalInst.SavedData["InitiativeEntryTempHPEntryVar" + str(self.Row)] = self.InitiativeEntryTempHPEntryVar
            GlobalInst.SavedData["InitiativeEntryCurrentHPEntryVar" + str(self.Row)] = self.InitiativeEntryCurrentHPEntryVar
            GlobalInst.SavedData["InitiativeEntryMaxHPEntryVar" + str(self.Row)] = self.InitiativeEntryMaxHPEntryVar
            GlobalInst.SavedData["InitiativeEntryConcentrationBoxVar" + str(self.Row)] = self.InitiativeEntryConcentrationBoxVar
            GlobalInst.SavedData["InitiativeEntryConditionsField" + str(self.Row)] = self.InitiativeEntryConditionsField
            GlobalInst.SavedData["InitiativeEntryLocationField" + str(self.Row)] = self.InitiativeEntryLocationField
            GlobalInst.SavedData["InitiativeEntryNotesField" + str(self.Row)] = self.InitiativeEntryNotesField
            GlobalInst.SavedData["InitiativeEntryTurnDoneVar" + str(self.Row)] = self.InitiativeEntryTurnDoneVar
            GlobalInst.SavedData["InitiativeEntryDeadVar" + str(self.Row)] = self.InitiativeEntryDeadVar
            GlobalInst.SavedData["InitiativeEntrySizeEntryVar" + str(self.Row)] = self.InitiativeEntrySizeEntryVar
            GlobalInst.SavedData["InitiativeEntryTypeAndTagsEntryVar" + str(self.Row)] = self.InitiativeEntryTypeAndTagsEntryVar
            GlobalInst.SavedData["InitiativeEntryAlignmentEntryVar" + str(self.Row)] = self.InitiativeEntryAlignmentEntryVar
            GlobalInst.SavedData["InitiativeEntrySpeedEntryVar" + str(self.Row)] = self.InitiativeEntrySpeedEntryVar
            GlobalInst.SavedData["InitiativeEntryCRAndExperienceEntryVar" + str(self.Row)] = self.InitiativeEntryCRAndExperienceEntryVar
            GlobalInst.SavedData["InitiativeEntryAbilitiesStrengthEntryVar" + str(self.Row)] = self.InitiativeEntryAbilitiesStrengthEntryVar
            GlobalInst.SavedData["InitiativeEntryAbilitiesDexterityEntryVar" + str(self.Row)] = self.InitiativeEntryAbilitiesDexterityEntryVar
            GlobalInst.SavedData["InitiativeEntryAbilitiesConstitutionEntryVar" + str(self.Row)] = self.InitiativeEntryAbilitiesConstitutionEntryVar
            GlobalInst.SavedData["InitiativeEntryAbilitiesIntelligenceEntryVar" + str(self.Row)] = self.InitiativeEntryAbilitiesIntelligenceEntryVar
            GlobalInst.SavedData["InitiativeEntryAbilitiesWisdomEntryVar" + str(self.Row)] = self.InitiativeEntryAbilitiesWisdomEntryVar
            GlobalInst.SavedData["InitiativeEntryAbilitiesCharismaEntryVar" + str(self.Row)] = self.InitiativeEntryAbilitiesCharismaEntryVar
            GlobalInst.SavedData["InitiativeEntrySkillSensesAndLanguagesFieldVar" + str(self.Row)] = self.InitiativeEntrySkillSensesAndLanguagesFieldVar
            GlobalInst.SavedData["InitiativeEntrySavingThrowsFieldVar" + str(self.Row)] = self.InitiativeEntrySavingThrowsFieldVar
            GlobalInst.SavedData["InitiativeEntryVulnerabilitiesResistancesAndImmunitiesFieldVar" + str(self.Row)] = self.InitiativeEntryVulnerabilitiesResistancesAndImmunitiesFieldVar
            GlobalInst.SavedData["InitiativeEntrySpecialTraitsFieldVar" + str(self.Row)] = self.InitiativeEntrySpecialTraitsFieldVar
            GlobalInst.SavedData["InitiativeEntryActionsFieldVar" + str(self.Row)] = self.InitiativeEntryActionsFieldVar
            GlobalInst.SavedData["InitiativeEntryReactionsFieldVar" + str(self.Row)] = self.InitiativeEntryReactionsFieldVar
            GlobalInst.SavedData["InitiativeEntryInventoryFieldVar" + str(self.Row)] = self.InitiativeEntryInventoryFieldVar
            GlobalInst.SavedData["InitiativeEntryLegendaryActionsAndLairActionsFieldVar" + str(self.Row)] = self.InitiativeEntryLegendaryActionsAndLairActionsFieldVar
            GlobalInst.SavedData["InitiativeEntryNotesFieldVar" + str(self.Row)] = self.InitiativeEntryNotesFieldVar

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
            DamagePrompt = IntegerPrompt(root, "Damage", "How much damage?", MinValue=1)
            root.wait_window(DamagePrompt.Window)
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
            HealingPrompt = IntegerPrompt(root, "Heal", "How much healing?", MinValue=1)
            root.wait_window(HealingPrompt.Window)
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
            CreatureStatsConfigInst = self.CreatureStatsConfig(root, self.InitiativeEntryNameEntryVar, self.InitiativeEntrySizeEntryVar, self.InitiativeEntryTypeAndTagsEntryVar, self.InitiativeEntryAlignmentEntryVar,
                                                               self.InitiativeEntryMaxHPEntryVar, self.InitiativeEntryACEntryVar, self.InitiativeEntrySpeedEntryVar, self.InitiativeEntryCRAndExperienceEntryVar,
                                                               self.InitiativeEntryAbilitiesStrengthEntryVar, self.InitiativeEntryAbilitiesDexterityEntryVar, self.InitiativeEntryAbilitiesConstitutionEntryVar,
                                                               self.InitiativeEntryAbilitiesIntelligenceEntryVar, self.InitiativeEntryAbilitiesWisdomEntryVar, self.InitiativeEntryAbilitiesCharismaEntryVar,
                                                               self.InitiativeEntrySkillSensesAndLanguagesFieldVar, self.InitiativeEntrySavingThrowsFieldVar, self.InitiativeEntryVulnerabilitiesResistancesAndImmunitiesFieldVar,
                                                               self.InitiativeEntrySpecialTraitsFieldVar, self.InitiativeEntryActionsFieldVar, self.InitiativeEntryReactionsFieldVar, self.InitiativeEntryInventoryFieldVar,
                                                               self.InitiativeEntryLegendaryActionsAndLairActionsFieldVar, self.InitiativeEntryNotesFieldVar)
            root.wait_window(CreatureStatsConfigInst.Window)

            # Handle Values
            if CreatureStatsConfigInst.DataSubmitted.get():
                self.InitiativeEntryNameEntryVar.set(CreatureStatsConfigInst.NameEntryVar.get())
                self.InitiativeEntrySizeEntryVar.set(CreatureStatsConfigInst.SizeEntryVar.get())
                self.InitiativeEntryTypeAndTagsEntryVar.set(CreatureStatsConfigInst.TypeAndTagsEntryVar.get())
                self.InitiativeEntryAlignmentEntryVar.set(CreatureStatsConfigInst.AlignmentEntryVar.get())
                self.InitiativeEntryMaxHPEntryVar.set(CreatureStatsConfigInst.MaxHPEntryVar.get())
                self.InitiativeEntryACEntryVar.set(CreatureStatsConfigInst.ACEntryVar.get())
                self.InitiativeEntrySpeedEntryVar.set(CreatureStatsConfigInst.SpeedEntryVar.get())
                self.InitiativeEntryCRAndExperienceEntryVar.set(CreatureStatsConfigInst.CRAndExperienceEntryVar.get())
                self.InitiativeEntryAbilitiesStrengthEntryVar.set(CreatureStatsConfigInst.AbilitiesStrengthEntryVar.get())
                self.InitiativeEntryAbilitiesDexterityEntryVar.set(CreatureStatsConfigInst.AbilitiesDexterityEntryVar.get())
                self.InitiativeEntryAbilitiesConstitutionEntryVar.set(CreatureStatsConfigInst.AbilitiesConstitutionEntryVar.get())
                self.InitiativeEntryAbilitiesIntelligenceEntryVar.set(CreatureStatsConfigInst.AbilitiesIntelligenceEntryVar.get())
                self.InitiativeEntryAbilitiesWisdomEntryVar.set(CreatureStatsConfigInst.AbilitiesWisdomEntryVar.get())
                self.InitiativeEntryAbilitiesCharismaEntryVar.set(CreatureStatsConfigInst.AbilitiesCharismaEntryVar.get())
                self.InitiativeEntrySkillSensesAndLanguagesFieldVar.set(CreatureStatsConfigInst.SkillSensesAndLanguagesFieldVar.get())
                self.InitiativeEntrySavingThrowsFieldVar.set(CreatureStatsConfigInst.SavingThrowsFieldVar.get())
                self.InitiativeEntryVulnerabilitiesResistancesAndImmunitiesFieldVar.set(CreatureStatsConfigInst.VulnerabilitiesResistancesAndImmunitiesFieldVar.get())
                self.InitiativeEntrySpecialTraitsFieldVar.set(CreatureStatsConfigInst.SpecialTraitsFieldVar.get())
                self.InitiativeEntryActionsFieldVar.set(CreatureStatsConfigInst.ActionsFieldVar.get())
                self.InitiativeEntryReactionsFieldVar.set(CreatureStatsConfigInst.ReactionsFieldVar.get())
                self.InitiativeEntryInventoryFieldVar.set(CreatureStatsConfigInst.InventoryFieldVar.get())
                self.InitiativeEntryLegendaryActionsAndLairActionsFieldVar.set(CreatureStatsConfigInst.LegendaryActionsAndLairActionsFieldVar.get())
                self.InitiativeEntryNotesFieldVar.set(CreatureStatsConfigInst.NotesFieldVar.get())

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

        def Open(self, event):
            ToolbarAndStatusBarInst.ToolbarSetText("Opening creature file...", Lock=True)
            OpenFileName = filedialog.askopenfilename(filetypes=(("Creature file", "*.crea"), ("All files", "*.*")), defaultextension=".crea", title="Open Creature File")
            TextFileName = "Creature Data.txt"
            if OpenFileName != "":
                with ZipFile(OpenFileName, mode="r") as OpenFile:
                    with open(OpenFile.extract(TextFileName), mode="r") as TextFile:
                        self.OpenCreatureData(TextFile)
                os.remove(TextFileName)
                sleep(0.5)
                if self.OpenErrors:
                    messagebox.showerror("Open Errors", "Some data in the file could not be opened.  This could be due to changes in the file format.")
                    self.OpenErrors = False
                ToolbarAndStatusBarInst.ToolbarSetText("Opened file:  " + os.path.basename(OpenFileName), Lock=True)
                root.after(2000, lambda: ToolbarAndStatusBarInst.ToolbarSetText("Status", Unlock=True))
                GlobalInst.SavePrompt = True
                GlobalInst.UpdateWindowTitle(AddSavePrompt=True)
            else:
                ToolbarAndStatusBarInst.ToolbarSetText("No file opened!", Lock=True)
                root.after(2000, lambda: ToolbarAndStatusBarInst.ToolbarSetText("Status", Unlock=True))

        def OpenCreatureData(self, File):
            for Line in File:
                if Line != "":
                    LoadedLine = json.loads(Line)
                    for Tag, Field in LoadedLine.items():
                        try:
                            self.CreatureStatsFields[Tag].set(Field)
                        except KeyError:
                            self.OpenErrors = True

        class CreatureStatsConfig:
            def __init__(self, master, NameEntryVar, SizeEntryVar, TypeAndTagsEntryVar, AlignmentEntryVar, MaxHPEntryVar, ACEntryVar, SpeedEntryVar, CRAndExperienceEntryVar, AbilitiesStrengthEntryVar,
                         AbilitiesDexterityEntryVar, AbilitiesConstitutionEntryVar, AbilitiesIntelligenceEntryVar, AbilitiesWisdomEntryVar, AbilitiesCharismaEntryVar, SkillSensesAndLanguagesFieldVar,
                         SavingThrowsFieldVar, VulnerabilitiesResistancesAndImmunitiesFieldVar, SpecialTraitsFieldVar, ActionsFieldVar, ReactionsFieldVar, InventoryFieldVar, LegendaryActionsAndLairActionsFieldVar,
                         NotesFieldVar):
                self.DataSubmitted = BooleanVar()
                self.NameEntryVar = StringVar(value=NameEntryVar.get())
                self.SizeEntryVar = StringVar(value=SizeEntryVar.get())
                self.TypeAndTagsEntryVar = StringVar(value=TypeAndTagsEntryVar.get())
                self.AlignmentEntryVar = StringVar(value=AlignmentEntryVar.get())
                self.MaxHPEntryVar = StringVar(value=MaxHPEntryVar.get())
                self.ACEntryVar = StringVar(value=ACEntryVar.get())
                self.SpeedEntryVar = StringVar(value=SpeedEntryVar.get())
                self.CRAndExperienceEntryVar = StringVar(value=CRAndExperienceEntryVar.get())
                self.AbilitiesStrengthEntryVar = StringVar(value=AbilitiesStrengthEntryVar.get())
                self.AbilitiesDexterityEntryVar = StringVar(value=AbilitiesDexterityEntryVar.get())
                self.AbilitiesConstitutionEntryVar = StringVar(value=AbilitiesConstitutionEntryVar.get())
                self.AbilitiesIntelligenceEntryVar = StringVar(value=AbilitiesIntelligenceEntryVar.get())
                self.AbilitiesWisdomEntryVar = StringVar(value=AbilitiesWisdomEntryVar.get())
                self.AbilitiesCharismaEntryVar = StringVar(value=AbilitiesCharismaEntryVar.get())
                self.SkillSensesAndLanguagesFieldVar = StringVar(value=SkillSensesAndLanguagesFieldVar.get())
                self.SavingThrowsFieldVar = StringVar(value=SavingThrowsFieldVar.get())
                self.VulnerabilitiesResistancesAndImmunitiesFieldVar = StringVar(value=VulnerabilitiesResistancesAndImmunitiesFieldVar.get())
                self.SpecialTraitsFieldVar = StringVar(value=SpecialTraitsFieldVar.get())
                self.ActionsFieldVar = StringVar(value=ActionsFieldVar.get())
                self.ReactionsFieldVar = StringVar(value=ReactionsFieldVar.get())
                self.InventoryFieldVar = StringVar(value=InventoryFieldVar.get())
                self.LegendaryActionsAndLairActionsFieldVar = StringVar(value=LegendaryActionsAndLairActionsFieldVar.get())
                self.NotesFieldVar = StringVar(value=NotesFieldVar.get())

                # Create Window
                self.Window = Toplevel(master)
                self.Window.wm_attributes("-toolwindow", 1)
                self.Window.wm_title("Creature Stats")

                # Name Entry
                self.NameFrame = LabelFrame(self.Window, text="Name:")
                self.NameFrame.grid_columnconfigure(0, weight=1)
                self.NameFrame.grid(row=0, column=0, columnspan=3, padx=2, pady=2, sticky=NSEW)
                self.NameEntry = Entry(self.NameFrame, justify=CENTER, textvariable=self.NameEntryVar)
                self.NameEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                # Size, Type, Tags, and Alignment Frame
                self.SizeTypeTagsAndAlignmentFrame = Frame(self.Window)
                self.SizeTypeTagsAndAlignmentFrame.grid_columnconfigure(0, weight=1)
                self.SizeTypeTagsAndAlignmentFrame.grid_columnconfigure(1, weight=1)
                self.SizeTypeTagsAndAlignmentFrame.grid_columnconfigure(2, weight=1)
                self.SizeTypeTagsAndAlignmentFrame.grid(row=1, column=0, columnspan=3, sticky=NSEW)

                # Size
                self.SizeFrame = LabelFrame(self.SizeTypeTagsAndAlignmentFrame, text="Size:")
                self.SizeFrame.grid_columnconfigure(0, weight=1)
                self.SizeFrame.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
                self.SizeEntry = Entry(self.SizeFrame, justify=CENTER, textvariable=self.SizeEntryVar)
                self.SizeEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                # Type and Tags
                self.TypeAndTagsFrame = LabelFrame(self.SizeTypeTagsAndAlignmentFrame, text="Type and Tags:")
                self.TypeAndTagsFrame.grid_columnconfigure(0, weight=1)
                self.TypeAndTagsFrame.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
                self.TypeAndTagsEntry = Entry(self.TypeAndTagsFrame, justify=CENTER, textvariable=self.TypeAndTagsEntryVar)
                self.TypeAndTagsEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                # Alignment
                self.AlignmentFrame = LabelFrame(self.SizeTypeTagsAndAlignmentFrame, text="Alignment:")
                self.AlignmentFrame.grid_columnconfigure(0, weight=1)
                self.AlignmentFrame.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
                self.AlignmentEntry = Entry(self.AlignmentFrame, justify=CENTER, textvariable=self.AlignmentEntryVar)
                self.AlignmentEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                # HP, AC, Speed, CR, and Experience Entries Frame
                self.HPACSpeedCRExperienceEntriesFrame = Frame(self.Window)
                self.HPACSpeedCRExperienceEntriesFrame.grid(row=2, column=0, rowspan=2, sticky=NSEW)
                self.HPACSpeedCRExperienceEntriesFrame.grid_rowconfigure(2, weight=1)
                self.HPACSpeedCRExperienceEntriesFrame.grid_rowconfigure(4, weight=1)
                self.HPACSpeedCRExperienceEntriesFrame.grid_rowconfigure(6, weight=1)

                # Max HP Entry
                self.MaxHPFrame = LabelFrame(self.HPACSpeedCRExperienceEntriesFrame, text="HP:")
                self.MaxHPFrame.grid_columnconfigure(0, weight=1)
                self.MaxHPFrame.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)
                self.MaxHPEntry = Entry(self.MaxHPFrame, justify=CENTER, width=3, textvariable=self.MaxHPEntryVar)
                self.MaxHPEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                # AC Entry
                self.ACFrame = LabelFrame(self.HPACSpeedCRExperienceEntriesFrame, text="AC:")
                self.ACFrame.grid_columnconfigure(0, weight=1)
                self.ACFrame.grid(row=3, column=0, padx=2, pady=2, sticky=NSEW)
                self.ACEntry = Entry(self.ACFrame, justify=CENTER, width=3, textvariable=self.ACEntryVar)
                self.ACEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                # Speed
                self.SpeedFrame = LabelFrame(self.HPACSpeedCRExperienceEntriesFrame, text="Speed:")
                self.SpeedFrame.grid_columnconfigure(0, weight=1)
                self.SpeedFrame.grid(row=5, column=0, padx=2, pady=2, sticky=NSEW)
                self.SpeedEntry = Entry(self.SpeedFrame, justify=CENTER, width=3, textvariable=self.SpeedEntryVar)
                self.SpeedEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                # CR and Experience
                self.CRAndExperienceFrame = LabelFrame(self.HPACSpeedCRExperienceEntriesFrame, text="CR and Exp.:")
                self.CRAndExperienceFrame.grid_columnconfigure(0, weight=1)
                self.CRAndExperienceFrame.grid(row=7, column=0, padx=2, pady=2, sticky=NSEW)
                self.CRAndExperienceEntry = Entry(self.CRAndExperienceFrame, justify=CENTER, width=3, textvariable=self.CRAndExperienceEntryVar)
                self.CRAndExperienceEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

                # Abilities
                self.AbilitiesFrame = LabelFrame(self.Window, text="Ability Scores:")
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

                # Skills, Senses, and Languages
                self.SkillSensesAndLanguagesFrame = LabelFrame(self.Window, text="Skills, Senses, and Languages:")
                self.SkillSensesAndLanguagesFrame.grid(row=3, column=1, padx=2, pady=2, sticky=NSEW)
                self.SkillSensesAndLanguagesField = ScrolledText(self.SkillSensesAndLanguagesFrame, Width=300, Height=100)
                self.SkillSensesAndLanguagesField.grid(row=0, column=0)
                self.SkillSensesAndLanguagesField.Text.insert(1.0, self.SkillSensesAndLanguagesFieldVar.get())

                # Saving Throws
                self.SavingThrowsFrame = LabelFrame(self.Window, text="Saving Throws:")
                self.SavingThrowsFrame.grid(row=2, column=2, padx=2, pady=2, sticky=NSEW)
                self.SavingThrowsField = ScrolledText(self.SavingThrowsFrame, Width=383, Height=100)
                self.SavingThrowsField.grid(row=0, column=0)
                self.SavingThrowsField.Text.insert(1.0, self.SavingThrowsFieldVar.get())

                # Vulnerabilities, Resistances, and Immunities
                self.VulnerabilitiesResistancesAndImmunitiesFrame = LabelFrame(self.Window, text="Vulnerabilities, Resistances, and Immunities:")
                self.VulnerabilitiesResistancesAndImmunitiesFrame.grid(row=3, column=2, padx=2, pady=2, sticky=NSEW)
                self.VulnerabilitiesResistancesAndImmunitiesField = ScrolledText(self.VulnerabilitiesResistancesAndImmunitiesFrame, Width=383, Height=100)
                self.VulnerabilitiesResistancesAndImmunitiesField.grid(row=0, column=0)
                self.VulnerabilitiesResistancesAndImmunitiesField.Text.insert(1.0, self.VulnerabilitiesResistancesAndImmunitiesFieldVar.get())

                # Special Traits
                self.SpecialTraitsFrame = LabelFrame(self.Window, text="Special Traits:")
                self.SpecialTraitsFrame.grid(row=4, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                self.SpecialTraitsField = ScrolledText(self.SpecialTraitsFrame, Width=383, Height=75)
                self.SpecialTraitsField.grid(row=0, column=0)
                self.SpecialTraitsField.Text.insert(1.0, self.SpecialTraitsFieldVar.get())

                # Actions
                self.ActionsFrame = LabelFrame(self.Window, text="Actions:")
                self.ActionsFrame.grid(row=5, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                self.ActionsField = ScrolledText(self.ActionsFrame, Width=383, Height=75)
                self.ActionsField.grid(row=0, column=0)
                self.ActionsField.Text.insert(1.0, self.ActionsFieldVar.get())

                # Reactions
                self.ReactionsFrame = LabelFrame(self.Window, text="Reactions:")
                self.ReactionsFrame.grid(row=6, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
                self.ReactionsField = ScrolledText(self.ReactionsFrame, Width=383, Height=75)
                self.ReactionsField.grid(row=0, column=0)
                self.ReactionsField.Text.insert(1.0, self.ReactionsFieldVar.get())

                # Inventory
                self.InventoryFrame = LabelFrame(self.Window, text="Inventory:")
                self.InventoryFrame.grid(row=4, column=2, padx=2, pady=2, sticky=NSEW)
                self.InventoryField = ScrolledText(self.InventoryFrame, Width=383, Height=75)
                self.InventoryField.grid(row=0, column=0)
                self.InventoryField.Text.insert(1.0, self.InventoryFieldVar.get())

                # Legendary Actions and Lair Actions
                self.LegendaryActionsAndLairActionsFrame = LabelFrame(self.Window, text="Legendary Actions and Lair Actions:")
                self.LegendaryActionsAndLairActionsFrame.grid(row=5, column=2, padx=2, pady=2, sticky=NSEW)
                self.LegendaryActionsAndLairActionsField = ScrolledText(self.LegendaryActionsAndLairActionsFrame, Width=383, Height=75)
                self.LegendaryActionsAndLairActionsField.grid(row=0, column=0)
                self.LegendaryActionsAndLairActionsField.Text.insert(1.0, self.LegendaryActionsAndLairActionsFieldVar.get())

                # Notes
                self.NotesFrame = LabelFrame(self.Window, text="Notes:")
                self.NotesFrame.grid(row=6, column=2, padx=2, pady=2, sticky=NSEW)
                self.NotesField = ScrolledText(self.NotesFrame, Width=383, Height=75)
                self.NotesField.grid(row=0, column=0)
                self.NotesField.Text.insert(1.0, self.NotesFieldVar.get())

                # Buttons
                self.ButtonsFrame = Frame(self.Window)
                self.ButtonsFrame.grid_columnconfigure(0, weight=1)
                self.ButtonsFrame.grid_columnconfigure(1, weight=1)
                self.ButtonsFrame.grid(row=7, column=0, columnspan=3, sticky=NSEW)

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
                self.SkillSensesAndLanguagesFieldVar.set(self.SkillSensesAndLanguagesField.get())
                self.SavingThrowsFieldVar.set(self.SavingThrowsField.get())
                self.VulnerabilitiesResistancesAndImmunitiesFieldVar.set(self.VulnerabilitiesResistancesAndImmunitiesField.get())
                self.SpecialTraitsFieldVar.set(self.SpecialTraitsField.get())
                self.ActionsFieldVar.set(self.ActionsField.get())
                self.ReactionsFieldVar.set(self.ReactionsField.get())
                self.InventoryFieldVar.set(self.InventoryField.get())
                self.LegendaryActionsAndLairActionsFieldVar.set(self.LegendaryActionsAndLairActionsField.get())
                self.NotesFieldVar.set(self.NotesField.get())
                self.Window.destroy()

            def Cancel(self):
                self.DataSubmitted.set(False)
                self.Window.destroy()


class DiceRoller:
    def __init__(self, master):
        self.DiceNumberEntryVar = StringVar(value="1")
        self.DieTypeEntryVar = StringVar(value="20")
        self.ModifierEntryVar = StringVar(value="0")
        self.CritRangeEntryVar = StringVar(value="20")

        # Dice Roller Frame
        self.DiceRollerFrame = LabelFrame(master, text="Dice Roller:")
        self.DiceRollerFrame.grid(row=0, column=1, padx=2, pady=2, sticky=NSEW, rowspan=2)

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

        # Crit Range Button
        self.CritRangeButton = Button(self.DiceEntryAndButtonsFrame, text="Crit Range", command=self.CritRange, bg=GlobalInst.ButtonColor)
        self.CritRangeButton.grid(row=1, column=6, padx=2, pady=2, sticky=NSEW)

        # Results
        self.ResultsFieldFrame = LabelFrame(self.DiceRollerFrame, text="Results:")
        self.ResultsFieldFrame.grid(row=2, column=0, padx=2, pady=2)
        self.ResultsField = ScrolledText(self.ResultsFieldFrame, Width=414, Height=154, Disabled=True, DisabledBackground=GlobalInst.ButtonColor)
        self.ResultsField.grid(row=0, column=0, padx=2, pady=2)
        self.ResultsField.Text.bind("<Button-1>", self.CopyResults)
        self.ResultsField.Text.bind("<Button-3>", self.ClearResults)

        # Preset Rolls
        self.PresetRollsInst = self.PresetRolls(self.DiceRollerFrame)

        # Add Saved Fields to Character Data Dictionary
        GlobalInst.SavedData["ResultsField"] = self.ResultsField
        GlobalInst.SavedData["CritRangeEntryVar"] = self.CritRangeEntryVar

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
            if Result >= GlobalInst.GetStringVarAsNumber(self.CritRangeEntryVar):
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

    def CritRange(self):
        # Create Window and Wait
        CritRangeMenuInst = self.CritRangeMenu(root, self.CritRangeEntryVar)
        root.wait_window(CritRangeMenuInst.Window)

        # Handle Variables
        if CritRangeMenuInst.DataSubmitted.get():
            self.CritRangeEntryVar.set(CritRangeMenuInst.CritRangeEntryVar.get())

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
        try:
            OldValue = GlobalInst.GetStringVarAsNumber(EntryVar)
        except ValueError:
            OldValue = 0
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
        ToolbarAndStatusBarInst.ToolbarSetText("Results copied to clipboard.", Lock=True)
        root.after(2000, lambda: ToolbarAndStatusBarInst.ToolbarSetText("Status", Unlock=True))

    def ClearResults(self, event):
        # Confirm
        ClearConfirm = messagebox.askyesno("Clear Results", "Are you sure you want to clear the roll results?  This cannot be undone.")
        if not ClearConfirm:
            return

        # Clear
        self.ResultsField.set("")

        def Submit(self):
            if self.ValidEntry():
                self.DataSubmitted.set(True)
                self.Window.destroy()

        def Cancel(self):
            self.DataSubmitted.set(False)
            self.Window.destroy()

    class PresetRolls:
        def __init__(self, master):
            # Preset Rolls Frame
            self.PresetRollsFrame = LabelFrame(master, text="Preset Rolls:")
            self.PresetRollsFrame.grid(row=3, column=0, padx=2, pady=2)

            # Scrolled Canvas
            self.PresetRollsScrolledCanvas = ScrolledCanvas(self.PresetRollsFrame, Height=405, Width=401)

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
                self.Row = Row

                # Set Row Size
                master.grid_rowconfigure(self.Row, minsize=26)

                # Add to List
                List.append(self)

                # Name
                self.PresetRollNameEntry = Entry(master, justify=CENTER, width=39, textvariable=self.PresetRollNameEntryVar)
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
                self.PresetRollModifierButton = Label(master, text="+")
                self.PresetRollModifierButton.grid(row=self.Row, column=5, sticky=NSEW)
                self.PresetRollModifierEntry = Entry(master, justify=CENTER, width=5, textvariable=self.PresetRollModifierEntryVar, disabledbackground="light gray", disabledforeground="black")
                self.PresetRollModifierEntry.grid(row=self.Row, column=6, sticky=NSEW)

                # Add Saved Fields to Saved Data Dictionary
                GlobalInst.SavedData["PresetRollNameEntryVar" + str(self.Row)] = self.PresetRollNameEntryVar
                GlobalInst.SavedData["PresetRollDiceNumberEntryVar" + str(self.Row)] = self.PresetRollDiceNumberEntryVar
                GlobalInst.SavedData["PresetRollDieTypeEntryVar" + str(self.Row)] = self.PresetRollDieTypeEntryVar
                GlobalInst.SavedData["PresetRollModifierEntryVar" + str(self.Row)] = self.PresetRollModifierEntryVar

            def RollPreset(self):
                DiceRollerInst.DiceNumberEntryVar.set(self.PresetRollDiceNumberEntry.get())
                DiceRollerInst.DieTypeEntryVar.set(self.PresetRollDieTypeEntry.get())
                DiceRollerInst.ModifierEntryVar.set(self.PresetRollModifierEntry.get())
                DiceRollerInst.Roll(self.PresetRollNameEntryVar.get() + ":\n")

    class CritRangeMenu:
        def __init__(self, master, CritRangeEntryVar):
            # Store Parameters
            self.CritRangeEntryVar = StringVar(value=CritRangeEntryVar.get())

            # Variables
            self.DataSubmitted = BooleanVar()

            # Create Window
            self.Window = Toplevel(master)
            self.Window.wm_attributes("-toolwindow", 1)
            self.Window.wm_title("Crit Range")

            # Header
            self.Header = Label(self.Window, text="Crit Between:", bd=2, relief=GROOVE)
            self.Header.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW, columnspan=3)

            # Crit Range Entry
            self.CritRangeEntry = Entry(self.Window, justify=CENTER, width=3, textvariable=self.CritRangeEntryVar)
            self.CritRangeEntry.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)
            self.CritRangeEntry.bind("<Return>", lambda event: self.Submit())

            # Labels
            self.DashLabel = Label(self.Window, text="-")
            self.DashLabel.grid(row=1, column=1, padx=2, pady=2, sticky=NSEW)
            self.TwentyLabel = Label(self.Window, text="20")
            self.TwentyLabel.grid(row=1, column=2, padx=2, pady=2, sticky=NSEW)

            # Buttons
            self.ButtonsFrame = Frame(self.Window)
            self.ButtonsFrame.grid_columnconfigure(0, weight=1)
            self.ButtonsFrame.grid_columnconfigure(1, weight=1)
            self.ButtonsFrame.grid(row=2, column=0, sticky=NSEW, columnspan=3)
            self.SubmitButton = Button(self.ButtonsFrame, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
            self.SubmitButton.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
            self.CancelButton = Button(self.ButtonsFrame, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
            self.CancelButton.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)

            # Prevent Main Window Input
            self.Window.grab_set()

            # Handle Config Window Geometry and Focus
            GlobalInst.WindowGeometry(self.Window, True)
            self.Window.focus_force()

            # Focus On Entry
            self.CritRangeEntry.focus_set()

        def Submit(self):
            if self.ValidEntry():
                self.DataSubmitted.set(True)
                self.Window.destroy()

        def Cancel(self):
            self.DataSubmitted.set(False)
            self.Window.destroy()

        def ValidEntry(self):
            try:
                CritRangeValue = GlobalInst.GetStringVarAsNumber(self.CritRangeEntryVar)
            except:
                messagebox.showerror("Invalid Entry", "Crit range must be a whole number.")
                return False
            if CritRangeValue <= 0 or CritRangeValue >= 21:
                messagebox.showerror("Invalid Entry", "Crit range must be between 1 and 20.")
                return False
            return True


class ToolbarAndStatusBar:
    def __init__(self, master):
        self.StatusBarTextVar = StringVar(value="Status")
        self.StatusBarLockedVar = BooleanVar(value=False)
        self.CurrentOpenFilePath = StringVar()
        self.PreviousOpenFilePath = StringVar()
        self.Opening = False
        self.OpenErrors = False

        # Toolbar Frame
        self.ToolbarFrame = Frame(master, bg="gray", bd=1, relief=SUNKEN)
        self.ToolbarFrame.grid_columnconfigure(3, weight=1)
        self.ToolbarFrame.grid(row=3, column=0, sticky=NSEW, columnspan=3, padx=2, pady=2)

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

    # Save Methods
    def SaveButton(self):
        self.ToolbarSetText("Saving...", Lock=True)
        CurrentPath = self.CurrentOpenFilePath.get()
        if CurrentPath == "":
            SaveFileName = filedialog.asksaveasfilename(filetypes=(("Encounter file", "*.enc"), ("All files", "*.*")), defaultextension=".enc", title="Save Encounter File As")
        else:
            SaveFileName = CurrentPath
        TextFileName = "Encounter Data.txt"
        if SaveFileName != "":
            with ZipFile(SaveFileName, mode="w") as SaveFile:
                with open(TextFileName, mode="w") as TextFile:
                    self.SaveCharacterData(TextFile)
                SaveFile.write(TextFileName)
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
        if GlobalInst.SavePrompt:
            SaveConfirm = messagebox.askyesnocancel("Save", "Save unsaved work before opening?")
            if SaveConfirm == None:
                return
            elif SaveConfirm == True:
                if not ToolbarAndStatusBarInst.SaveButton():
                    return
        self.ToolbarSetText("Opening...", Lock=True)
        OpenFileName = filedialog.askopenfilename(filetypes=(("Encounter file", "*.enc"), ("All files", "*.*")), defaultextension=".enc", title="Open Encounter File")
        TextFileName = "Encounter Data.txt"
        if OpenFileName != "":
            with ZipFile(OpenFileName, mode="r") as OpenFile:
                with open(OpenFile.extract(TextFileName), mode="r") as TextFile:
                    self.OpenEncounterData(TextFile)
            os.remove(TextFileName)
            self.CurrentOpenFilePath.set(OpenFileName)
            sleep(0.5)
            if self.OpenErrors:
                messagebox.showerror("Open Errors", "Some data in the file could not be opened.  This could be due to changes in the file format.")
                self.OpenErrors = False
            self.ToolbarSetText("Opened file:  " + os.path.basename(OpenFileName), Lock=True)
            root.after(2000, lambda: self.ToolbarSetText("Status", Unlock=True))
            GlobalInst.SavePrompt = False
            GlobalInst.UpdateWindowTitle(AddSavePrompt=False)
        else:
            self.ToolbarSetText("No file opened!", Lock=True)
            root.after(2000, lambda: self.ToolbarSetText("Status", Unlock=True))

    def OpenEncounterData(self, File):
        self.Opening = True
        for Line in File:
            if Line != "":
                LoadedLine = json.loads(Line)
                for Tag, Field in LoadedLine.items():
                    try:
                        GlobalInst.SavedData[Tag].set(Field)
                    except KeyError:
                        self.OpenErrors = True
        for Entry in InitiativeOrderInst.InitiativeEntriesList:
            if Entry.InitiativeEntryTurnDoneVar.get():
                Entry.TurnDoneOn()
            else:
                Entry.TurnDoneOff()
            if Entry.InitiativeEntryDeadVar.get():
                Entry.DeadOn()
            else:
                Entry.DeadOff()
        self.Opening = False

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


# Misc
class Global:
    def __init__(self):
        # Variables
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

    def WindowGeometry(self, Window, IsDialog, WidthOffset=0, HeightOffset=0):
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
        Window.geometry("{}x{}+{}+{}".format(BaseWidth + WidthOffset, BaseHeight + HeightOffset, XCoordinate - (WidthOffset // 2), YCoordinate - (HeightOffset // 2)))
        Window.resizable(width=False, height=False)

    def UpdateWindowTitle(self, AddSavePrompt=False):
        EncounterName = EncounterHeaderInst.EncounterNameEntryVar.get()
        CurrentOpenFile = ToolbarAndStatusBarInst.CurrentOpenFilePath.get()
        SavePromptString = ""
        if CurrentOpenFile != "":
            CurrentOpenFile = " [" + os.path.basename(CurrentOpenFile) + "]"
        if EncounterName != "":
            EncounterName += " - "
        if AddSavePrompt:
            SavePromptString = " *"
        root.wm_title(EncounterName + "Encounter Manager" + CurrentOpenFile + SavePromptString)

    def ConfigureBindings(self):
        # Scrolling
        InitiativeOrderInst.InitiativeOrderScrolledCanvas.BindEnterAndLeaveToBindMouseWheel()
        DiceRollerInst.PresetRollsInst.PresetRollsScrolledCanvas.BindEnterAndLeaveToBindMouseWheel()

        # Save and Open Keystrokes and Tooltips
        root.bind("<Control-s>", ToolbarAndStatusBarInst.SaveKeystroke)
        root.bind("<Control-S>", ToolbarAndStatusBarInst.SaveAsKeystroke)
        root.bind("<Control-o>", ToolbarAndStatusBarInst.OpenKeystroke)
        ToolbarAndStatusBarInst.TooltipConfig(ToolbarAndStatusBarInst.ToolbarSaveButton, "Keyboard Shortcut:  Ctrl+S")
        ToolbarAndStatusBarInst.TooltipConfig(ToolbarAndStatusBarInst.ToolbarSaveAsButton, "Keyboard Shortcut:  Ctrl+Shift+S")
        ToolbarAndStatusBarInst.TooltipConfig(ToolbarAndStatusBarInst.ToolbarOpenButton, "Keyboard Shortcut:  Ctrl+O")

        # Initiative List Keystrokes and Tooltips
        root.bind("<Control-r>", lambda event: InitiativeOrderInst.NewRound())
        root.bind("<Control-t>", lambda event: InitiativeOrderInst.NextTurn())
        root.bind("<Control-T>", lambda event: InitiativeOrderInst.ClearTurns())
        root.bind("<Control-i>", lambda event: InitiativeOrderInst.SortInitiativeOrder())
        ToolbarAndStatusBarInst.TooltipConfig(InitiativeOrderInst.NewRoundButton, "Keyboard Shortcut:  Ctrl+R")
        ToolbarAndStatusBarInst.TooltipConfig(InitiativeOrderInst.NextTurnButton, "Keyboard Shortcut:  Ctrl+T")
        ToolbarAndStatusBarInst.TooltipConfig(InitiativeOrderInst.ClearTurnsButton, "Keyboard Shortcut:  Ctrl+Shift+T")
        ToolbarAndStatusBarInst.TooltipConfig(InitiativeOrderInst.SortInitiativeOrderButton, "Keyboard Shortcut:  Ctrl+I")

        # Initiative Entry Tooltips
        for Entry in InitiativeOrderInst.InitiativeEntriesList:
            ToolbarAndStatusBarInst.TooltipConfig(Entry.InitiativeEntryResultEntry, "Right-click to toggle turn taken.")
            ToolbarAndStatusBarInst.TooltipConfig(Entry.InitiativeEntryNameEntry, "Right-click to set additional creature info.  Shift+right-click to duplicate.  Ctrl+right-click to clear.  Shift+left-click to open from a "
                                                                                  "creature file.")
            ToolbarAndStatusBarInst.TooltipConfig(Entry.InitiativeEntryCurrentHPEntry, "Right-click to damage.  Shift+right-click to heal.  Control+right-click to toggle dead.")

        # Dice Roller Tooltips
        ToolbarAndStatusBarInst.TooltipConfig(DiceRollerInst.DiceNumberEntry, "Scroll the mouse wheel or type to change the number of dice.")
        ToolbarAndStatusBarInst.TooltipConfig(DiceRollerInst.DieTypeEntry, "Scroll the mouse wheel or type to change the die type.")
        ToolbarAndStatusBarInst.TooltipConfig(DiceRollerInst.ModifierEntry, "Scroll the mouse wheel or type to change the modifier.")
        ToolbarAndStatusBarInst.TooltipConfig(DiceRollerInst.ResultsField.ScrolledTextFrame, "Left-click to copy results to the clipboard.  Right-click to clear.")

        # Track Modified Fields
        for Field in self.SavedData.values():
            FieldType = type(Field)
            if FieldType == StringVar or FieldType == BooleanVar:
                Field.trace_add("write", lambda a, b, c: self.CharacterDataModified())
            elif FieldType == ScrolledText:
                Field.Text.bind("<<TextModified>>", lambda event: self.CharacterDataModified())

        # Bind Closing Protocol
        root.wm_protocol("WM_DELETE_WINDOW", self.CloseWindow)

    def CharacterDataModified(self):
        if not ToolbarAndStatusBarInst.Opening:
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
        self.Text = self.TrackedText(self.ScrolledTextFrame, wrap=WORD)
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

        def _proxy(self, command, *args):
            cmd = (self._orig, command) + args
            result = self.tk.call(cmd)
            if command in ("insert", "delete", "replace"):
                self.event_generate("<<TextModified>>")
            return result

        def Paste(self, event):
            SelectionRange = self.tag_ranges("sel")
            if SelectionRange:
                SelectionStart = self.index(SEL_FIRST)
                SelectionEnd = self.index(SEL_LAST)
                self.delete(SelectionStart, SelectionEnd)
                self.mark_set(INSERT, SelectionStart)
            self.insert(INSERT, root.clipboard_get())
            self.see(INSERT)
            return "break"


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
        GlobalInst.WindowGeometry(self.Window, True)
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


# Global Functions and Variables
GlobalInst = Global()

# Populate Window
EncounterHeaderInst = EncounterHeader(root)
InitiativeOrderInst = InitiativeOrder(root)
DiceRollerInst = DiceRoller(root)
ToolbarAndStatusBarInst = ToolbarAndStatusBar(root)

# Inst-Dependent Bindings
GlobalInst.ConfigureBindings()

# Initial Window Behavior
GlobalInst.WindowGeometry(root, False)
root.focus_force()

# Main Loop
root.mainloop()
