import math
from decimal import *
from tkinter import *
from tkinter import font
from tkinter import messagebox


class EncounterHeader:
    def __init__(self, master):
        # Variables
        self.EncounterNameEntryVar = StringVarExtended("EncounterNameEntryVar", ClearOnNew=True)
        self.CREntryVar = StringVarExtended("CREntryVar", ClearOnNew=True)
        self.ExperienceEntryVar = StringVarExtended("ExperienceEntryVar", ClearOnNew=True)

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
        self.NotesField1 = ScrolledText(self.NotesFrame, Width=self.NotesWidth, Height=self.NotesHeight, SavedDataTag="NotesField1", ClearOnNew=True)
        self.NotesField1.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
        self.NotesField2 = ScrolledText(self.NotesFrame, Width=self.NotesWidth, Height=self.NotesHeight, SavedDataTag="NotesField2", ClearOnNew=True)
        self.NotesField2.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
        self.NotesField3 = ScrolledText(self.NotesFrame, Width=self.NotesWidth, Height=self.NotesHeight, SavedDataTag="NotesField3", ClearOnNew=True)
        self.NotesField3.grid(row=0, column=4, sticky=NSEW, padx=2, pady=2)

        # Description
        self.DescriptionFrame = LabelFrame(self.EncounterHeaderFrame, text="Description:")
        self.DescriptionFrame.grid(row=0, column=8, sticky=NSEW, rowspan=2, padx=2, pady=2)
        self.DescriptionField = ScrolledText(self.DescriptionFrame, Width=180, Height=100, SavedDataTag="DescriptionField", ClearOnNew=True)
        self.DescriptionField.grid(row=0, column=0, sticky=NSEW)

        # Rewards
        self.RewardsFrame = LabelFrame(self.EncounterHeaderFrame, text="Rewards:")
        self.RewardsFrame.grid(row=0, column=9, sticky=NSEW, rowspan=2, padx=2, pady=2)
        self.RewardsField = ScrolledText(self.RewardsFrame, Width=150, Height=100, SavedDataTag="RewardsField", ClearOnNew=True)
        self.RewardsField.grid(row=0, column=0, sticky=NSEW)


class InitiativeOrder:
    def __init__(self, master):
        # Variables
        self.RoundEntryVar = StringVarExtended("RoundEntryVar", DefaultValue="1", ClearOnNew=True)
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
        self.NewRoundButton = ButtonExtended(self.InitiativeDataFrame, text="New Round", command=self.NewRound, bg=GlobalInst.ButtonColor, font=self.InitiativeDataFont)
        self.NewRoundButton.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
        WindowInst.bind("<Control-r>", lambda event: self.NewRound())
        self.NewRoundTooltip = Tooltip(self.NewRoundButton, "Keyboard Shortcut:  Ctrl+R")

        # Next Turn Button
        self.NextTurnButton = ButtonExtended(self.InitiativeDataFrame, text="Next Turn", command=self.NextTurn, bg=GlobalInst.ButtonColor, font=self.InitiativeDataFont)
        self.NextTurnButton.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)
        WindowInst.bind("<Control-t>", lambda event: self.NextTurn())
        self.NextTurnTooltip = Tooltip(self.NextTurnButton, "Keyboard Shortcut:  Ctrl+T")

        # Clear Turns Button
        self.ClearTurnsButton = ButtonExtended(self.InitiativeDataFrame, text="Clear Turns", command=self.ClearTurns, bg=GlobalInst.ButtonColor, font=self.InitiativeDataFont)
        self.ClearTurnsButton.grid(row=0, column=3, sticky=NSEW, padx=2, pady=2)
        WindowInst.bind("<Control-T>", lambda event: self.ClearTurns())
        self.ClearTurnsTooltip = Tooltip(self.ClearTurnsButton, "Keyboard Shortcut:  Ctrl+Shift+T")

        # Sort Initiative Order Button
        self.SortInitiativeOrderButton = ButtonExtended(self.InitiativeDataFrame, text="Sort Initiative Order", command=self.SortInitiativeOrder, bg=GlobalInst.ButtonColor, font=self.InitiativeDataFont)
        self.SortInitiativeOrderButton.grid(row=0, column=4, sticky=NSEW, padx=2, pady=2)
        WindowInst.bind("<Control-i>", lambda event: self.SortInitiativeOrder())
        self.SortInitiativeOrderTooltip = Tooltip(self.SortInitiativeOrderButton, "Keyboard Shortcut:  Ctrl+I")

        # Initiative Order Scrolled Canvas
        self.InitiativeOrderScrolledCanvasFrame = Frame(self.InitiativeOrderFrame)
        self.InitiativeOrderScrolledCanvasFrame.grid(row=1, column=0, sticky=NSEW)
        self.InitiativeOrderScrolledCanvas = ScrolledCanvas(self.InitiativeOrderScrolledCanvasFrame, Height=434, Width=839, NumberOfColumns=11, ScrollingDisabledVar=self.ScrollingDisabledVar)

        # Initiative Header
        self.InitiativeHeader = Label(self.InitiativeOrderScrolledCanvas.HeaderFrame, text="Initiative", bd=2, relief=GROOVE)
        self.InitiativeHeader.grid(row=0, column=0, sticky=NSEW)

        # Tie Priority Header
        self.TiePriorityHeader = Label(self.InitiativeOrderScrolledCanvas.HeaderFrame, text="Tie\nPriority", bd=2, relief=GROOVE)
        self.TiePriorityHeader.grid(row=0, column=1, sticky=NSEW)

        # Name Header
        self.NameHeader = Label(self.InitiativeOrderScrolledCanvas.HeaderFrame, text="Name", bd=2, relief=GROOVE)
        self.NameHeader.grid(row=0, column=2, sticky=NSEW)

        # AC Header
        self.ACHeader = Label(self.InitiativeOrderScrolledCanvas.HeaderFrame, text="AC", bd=2, relief=GROOVE)
        self.ACHeader.grid(row=0, column=3, sticky=NSEW)

        # Temp HP Header
        self.TempHPHeader = Label(self.InitiativeOrderScrolledCanvas.HeaderFrame, text="Temp\nHP", bd=2, relief=GROOVE)
        self.TempHPHeader.grid(row=0, column=4, sticky=NSEW)

        # Current HP Header
        self.CurrentHPHeader = Label(self.InitiativeOrderScrolledCanvas.HeaderFrame, text="Current\nHP", bd=2, relief=GROOVE)
        self.CurrentHPHeader.grid(row=0, column=5, sticky=NSEW)

        # Max HP Header
        self.MaxHPHeader = Label(self.InitiativeOrderScrolledCanvas.HeaderFrame, text="Max\nHP", bd=2, relief=GROOVE)
        self.MaxHPHeader.grid(row=0, column=6, sticky=NSEW)

        # Concentration Header
        self.ConcentrationHeader = Label(self.InitiativeOrderScrolledCanvas.HeaderFrame, text="Conc.", bd=2, relief=GROOVE)
        self.ConcentrationHeader.grid(row=0, column=7, sticky=NSEW)

        # Conditions Header
        self.ConditionsHeader = Label(self.InitiativeOrderScrolledCanvas.HeaderFrame, text="Conditions", bd=2, relief=GROOVE)
        self.ConditionsHeader.grid(row=0, column=8, sticky=NSEW)

        # Location Header
        self.LocationHeader = Label(self.InitiativeOrderScrolledCanvas.HeaderFrame, text="Location", bd=2, relief=GROOVE)
        self.LocationHeader.grid(row=0, column=9, sticky=NSEW)

        # Notes Header
        self.NotesHeader = Label(self.InitiativeOrderScrolledCanvas.HeaderFrame, text="Notes", bd=2, relief=GROOVE)
        self.NotesHeader.grid(row=0, column=10, sticky=NSEW)

        # Entries List
        self.InitiativeEntriesList = []

        # Initiative Entries Count
        self.InitiativeEntriesCount = 100

        # Initiative Entries
        for CurrentIndex in range(1, self.InitiativeEntriesCount + 1):
            CurrentEntry = self.InitiativeEntry(self.InitiativeOrderScrolledCanvas.WindowFrame, self.InitiativeEntriesList, self.ScrollingDisabledVar, CurrentIndex)
            for WidgetToBind in CurrentEntry.WidgetsList:
                WidgetToBind.bind("<FocusIn>", self.InitiativeOrderScrolledCanvas.MakeFocusVisible)
            CurrentEntry.Display(CurrentIndex)

        # Add to Clearable Fields
        SavingAndOpeningInst.ClearableFields.append(self)

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

    def SetToDefault(self):
        for Entry in self.InitiativeEntriesList:
            Entry.TurnDoneOff()
            Entry.DeadOff()

    class InitiativeEntry:
        def __init__(self, master, List, ScrollingDisabledVar, Row):
            # Store Parameters
            self.master = master
            self.List = List
            self.ScrollingDisabledVar = ScrollingDisabledVar
            self.Row = Row

            # Variables
            self.InitiativeEntryResultEntryVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntryTiePriorityDropdownVar = StringVarExtended(DefaultValue="1", ClearOnNew=True)
            self.InitiativeEntryNameEntryVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntryACEntryVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntryTempHPEntryVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntryCurrentHPEntryVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntryMaxHPEntryVar = StringVarExtended(ClearOnNew=True)
            self.ConcentrationTrueColor = "#7aff63"
            self.ConcentrationFalseColor = GlobalInst.ButtonColor
            self.InitiativeEntryConcentrationBoxVar = BooleanVarExtended(ClearOnNew=True)
            self.TurnDoneTrueColor = "#7cafff"
            self.InitiativeEntryTurnDoneVar = BooleanVarExtended(ClearOnNew=True)
            self.DeadTrueColor = "#ff6d6d"
            self.InitiativeEntryDeadVar = BooleanVarExtended(ClearOnNew=True)
            self.InitiativeEntrySizeEntryVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntryTypeAndTagsEntryVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntryAlignmentEntryVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntryProficiencyEntryVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntrySpeedEntryVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntryCRAndExperienceEntryVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntryAbilitiesStrengthEntryVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntryAbilitiesDexterityEntryVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntryAbilitiesConstitutionEntryVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntryAbilitiesIntelligenceEntryVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntryAbilitiesWisdomEntryVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntryAbilitiesCharismaEntryVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntrySkillSensesAndLanguagesFieldVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntrySavingThrowsFieldVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntryVulnerabilitiesResistancesAndImmunitiesFieldVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntrySpecialTraitsFieldVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntryActionsFieldVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntryReactionsFieldVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntryInventoryFieldVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntryLegendaryActionsAndLairActionsFieldVar = StringVarExtended(ClearOnNew=True)
            self.InitiativeEntryNotesFieldVar = StringVarExtended(ClearOnNew=True)

            # Add to List
            self.List.append(self)

            # Initiative Entry
            self.InitiativeEntryResultEntry = InitiativeEntry(self.master, textvariable=self.InitiativeEntryResultEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
            self.InitiativeEntryResultEntry.bind("<Button-3>", lambda event: self.ToggleTurnDone())
            self.InitiativeEntryResultEntry.bind("<Return>", lambda event: self.ToggleTurnDone())
            self.InitiativeEntryResultTooltip = Tooltip(self.InitiativeEntryResultEntry, "Right-click or enter to toggle turn taken.")

            # Tie Priority Dropdown
            self.InitiativeEntryTiePriorityDropdown = DropdownExtended(self.master, textvariable=self.InitiativeEntryTiePriorityDropdownVar,
                                                                       values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"], width=3, state="readonly",
                                                                       justify=CENTER)
            self.InitiativeEntryTiePriorityDropdown.bind("<Enter>", self.DisableScrolling)
            self.InitiativeEntryTiePriorityDropdown.bind("<Leave>", self.EnableScrolling)

            # Name Entry
            self.InitiativeEntryNameEntry = EntryExtended(self.master, textvariable=self.InitiativeEntryNameEntryVar, justify=CENTER, width=35, bg=GlobalInst.ButtonColor)
            self.InitiativeEntryNameEntry.bind("<Button-3>", self.SetCreatureStats)
            self.InitiativeEntryNameEntry.bind("<Return>", self.SetCreatureStats)
            self.InitiativeEntryNameEntry.bind("<Shift-Button-3>", self.Duplicate)
            self.InitiativeEntryNameEntry.bind("<Shift-Return>", self.Duplicate)
            self.InitiativeEntryNameEntry.bind("<Control-Button-3>", self.Clear)
            self.InitiativeEntryNameEntry.bind("<Control-Return>", self.Clear)
            self.InitiativeEntryNameTooltip = Tooltip(self.InitiativeEntryNameEntry,
                                                      "Right-click or enter to set additional creature info.\n\nShift+right-click or shift+enter to duplicate.\n\nCtrl+right-click or ctrl+enter to clear.")

            # AC Entry
            self.InitiativeEntryACEntry = EntryExtended(self.master, textvariable=self.InitiativeEntryACEntryVar, justify=CENTER, width=5)

            # Temp HP Entry
            self.InitiativeEntryTempHPEntry = EntryExtended(self.master, textvariable=self.InitiativeEntryTempHPEntryVar, justify=CENTER, width=5)

            # Current HP Entry
            self.InitiativeEntryCurrentHPEntry = EntryExtended(self.master, textvariable=self.InitiativeEntryCurrentHPEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
            self.InitiativeEntryCurrentHPEntry.bind("<Button-3>", lambda event: self.Damage())
            self.InitiativeEntryCurrentHPEntry.bind("<Return>", lambda event: self.Damage())
            self.InitiativeEntryCurrentHPEntry.bind("<Shift-Button-3>", lambda event: self.Heal())
            self.InitiativeEntryCurrentHPEntry.bind("<Shift-Return>", lambda event: self.Heal())
            self.InitiativeEntryCurrentHPEntry.bind("<Control-Button-3>", lambda event: self.ToggleDead())
            self.InitiativeEntryCurrentHPEntry.bind("<Control-Return>", lambda event: self.ToggleDead())
            self.InitiativeEntryCurrentHPTooltip = Tooltip(self.InitiativeEntryCurrentHPEntry, "Right-click or enter to damage.\n\nShift+right-click or shift+enter to heal.\n\nCtrl+right-click or ctrl+enter to toggle dead.")

            # Max HP Entry
            self.InitiativeEntryMaxHPEntry = EntryExtended(self.master, textvariable=self.InitiativeEntryMaxHPEntryVar, justify=CENTER, width=5)

            # Concentration Box
            self.InitiativeEntryConcentrationBox = Checkbutton(self.master, text="Conc.", variable=self.InitiativeEntryConcentrationBoxVar, background=self.ConcentrationFalseColor, selectcolor=self.ConcentrationTrueColor,
                                                               indicatoron=False)

            # Conditions Field
            self.InitiativeEntryConditionsField = ScrolledText(self.master, Width=113, Height=35, FontSize=7, ClearOnNew=True)
            self.InitiativeEntryConditionsField.ScrolledTextFrame.bind("<Enter>", self.DisableScrolling)
            self.InitiativeEntryConditionsField.ScrolledTextFrame.bind("<Leave>", self.EnableScrolling)

            # Location Field
            self.InitiativeEntryLocationField = ScrolledText(self.master, Width=113, Height=35, FontSize=7, ClearOnNew=True)
            self.InitiativeEntryLocationField.ScrolledTextFrame.bind("<Enter>", self.DisableScrolling)
            self.InitiativeEntryLocationField.ScrolledTextFrame.bind("<Leave>", self.EnableScrolling)

            # Notes Field
            self.InitiativeEntryNotesField = ScrolledText(self.master, Width=113, Height=35, FontSize=7, ClearOnNew=True)
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

            # List of Widgets
            self.WidgetsList = [self.InitiativeEntryResultEntry, self.InitiativeEntryTiePriorityDropdown, self.InitiativeEntryNameEntry, self.InitiativeEntryACEntry, self.InitiativeEntryTempHPEntry,
                                self.InitiativeEntryCurrentHPEntry, self.InitiativeEntryMaxHPEntry, self.InitiativeEntryConcentrationBox, self.InitiativeEntryConditionsField.ScrolledTextFrame,
                                self.InitiativeEntryLocationField.ScrolledTextFrame, self.InitiativeEntryNotesField.ScrolledTextFrame]

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
            self.LiftWidgets()

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

        def LiftWidgets(self):
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


class CompactInitiativeOrder:
    def __init__(self, master):
        # Variables
        self.RoundEntryVar = StringVar(value="1")
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
        self.ClearTurnsButton = ButtonExtended(self.InitiativeDataFrame, text="Clear Turns", command=self.ClearTurns, bg=GlobalInst.ButtonColor, font=self.InitiativeDataFont)
        self.ClearTurnsButton.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
        WindowInst.bind("<Control-T>", lambda event: self.ClearTurns())
        self.ClearTurnsTooltip = Tooltip(self.ClearTurnsButton, "Keyboard Shortcut:  Ctrl+Shift+T")

        # Sort Initiative Order Button
        self.SortInitiativeOrderButton = ButtonExtended(self.InitiativeDataFrame, text="Sort Initiative Order", command=self.SortInitiativeOrder, bg=GlobalInst.ButtonColor, font=self.InitiativeDataFont)
        self.SortInitiativeOrderButton.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
        WindowInst.bind("<Control-i>", lambda event: self.SortInitiativeOrder())
        self.SortInitiativeOrderTooltip = Tooltip(self.SortInitiativeOrderButton, "Keyboard Shortcut:  Ctrl+I")

        # Next Turn Button
        self.NextTurnButton = ButtonExtended(self.InitiativeDataFrame, text="Next Turn", command=self.NextTurn, bg=GlobalInst.ButtonColor, font=self.InitiativeDataFont)
        self.NextTurnButton.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)
        WindowInst.bind("<Control-t>", lambda event: self.NextTurn())
        self.NextTurnTooltip = Tooltip(self.NextTurnButton, "Keyboard Shortcut:  Ctrl+T")

        # New Round Button
        self.NewRoundButton = ButtonExtended(self.InitiativeDataFrame, text="New Round", command=self.NewRound, bg=GlobalInst.ButtonColor, font=self.InitiativeDataFont)
        self.NewRoundButton.grid(row=2, column=1, sticky=NSEW, padx=2, pady=2)
        WindowInst.bind("<Control-r>", lambda event: self.NewRound())
        self.NewRoundTooltip = Tooltip(self.NewRoundButton, "Keyboard Shortcut:  Ctrl+R")

        # Initiative Order Scrolled Canvas
        self.InitiativeOrderScrolledCanvasFrame = Frame(master)
        self.InitiativeOrderScrolledCanvasFrame.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
        self.InitiativeOrderScrolledCanvas = ScrolledCanvas(self.InitiativeOrderScrolledCanvasFrame, Height=364, Width=310, NumberOfColumns=3, ScrollingDisabledVar=self.ScrollingDisabledVar)

        # Initiative Header
        self.InitiativeHeader = Label(self.InitiativeOrderScrolledCanvas.HeaderFrame, text="Initiative", bd=2, relief=GROOVE)
        self.InitiativeHeader.grid(row=0, column=0, sticky=NSEW)

        # Tie Priority Header
        self.TiePriorityHeader = Label(self.InitiativeOrderScrolledCanvas.HeaderFrame, text="Tie\nPriority", bd=2, relief=GROOVE)
        self.TiePriorityHeader.grid(row=0, column=1, sticky=NSEW)

        # Name Header
        self.NameHeader = Label(self.InitiativeOrderScrolledCanvas.HeaderFrame, text="Name", bd=2, relief=GROOVE)
        self.NameHeader.grid(row=0, column=2, sticky=NSEW)

        # Entries List
        self.InitiativeEntriesList = []

        # Entries Count
        self.InitiativeEntriesCount = 100

        # Initiative Entries
        for CurrentIndex in range(1, self.InitiativeEntriesCount + 1):
            CurrentEntry = self.InitiativeEntry(self.InitiativeOrderScrolledCanvas.WindowFrame, self.InitiativeEntriesList, self.ScrollingDisabledVar, CurrentIndex)
            for WidgetToBind in CurrentEntry.WidgetsList:
                WidgetToBind.bind("<FocusIn>", self.InitiativeOrderScrolledCanvas.MakeFocusVisible)
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
            self.InitiativeEntryTiePriorityDropdownVar = StringVar(value="1")
            self.InitiativeEntryNameEntryVar = StringVar()
            self.TurnDoneTrueColor = "#7cafff"
            self.InitiativeEntryTurnDoneVar = BooleanVar()

            # Add to List
            self.List.append(self)

            # Initiative Entry
            self.InitiativeEntryResultEntry = InitiativeEntry(self.master, textvariable=self.InitiativeEntryResultEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor)
            self.InitiativeEntryResultEntry.bind("<Button-3>", lambda event: self.ToggleTurnDone())
            self.InitiativeEntryResultEntry.bind("<Return>", lambda event: self.ToggleTurnDone())
            self.InitiativeEntryResultTooltip = Tooltip(self.InitiativeEntryResultEntry, "Right-click or enter to toggle turn taken.")

            # Tie Priority Dropdown
            self.InitiativeEntryTiePriorityDropdown = DropdownExtended(self.master, textvariable=self.InitiativeEntryTiePriorityDropdownVar,
                                                                       values=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"], width=3, state="readonly",
                                                                       justify=CENTER)
            self.InitiativeEntryTiePriorityDropdown.bind("<Enter>", self.DisableScrolling)
            self.InitiativeEntryTiePriorityDropdown.bind("<Leave>", self.EnableScrolling)

            # Name Entry
            self.InitiativeEntryNameEntry = EntryExtended(self.master, textvariable=self.InitiativeEntryNameEntryVar, justify=CENTER, width=35, bg=GlobalInst.ButtonColor)
            self.InitiativeEntryNameEntry.bind("<Button-3>", self.Duplicate)
            self.InitiativeEntryNameEntry.bind("<Return>", self.Duplicate)
            self.InitiativeEntryNameEntry.bind("<Shift-Button-3>", self.Clear)
            self.InitiativeEntryNameEntry.bind("<Shift-Return>", self.Clear)
            self.InitiativeEntryNameTooltip = Tooltip(self.InitiativeEntryNameEntry, "Right-click or enter to duplicate.\n\nShift+right-click or shift+enter to clear.")

            # List of Widgets
            self.WidgetsList = [self.InitiativeEntryResultEntry, self.InitiativeEntryTiePriorityDropdown, self.InitiativeEntryNameEntry]

        def Display(self, Row):
            self.Row = Row

            # Place in Grid
            self.InitiativeEntryResultEntry.grid(row=self.Row, column=0, sticky=NSEW)
            self.InitiativeEntryTiePriorityDropdown.grid(row=self.Row, column=1, sticky=NSEW)
            self.InitiativeEntryNameEntry.grid(row=self.Row, column=2, sticky=NSEW)

            # Update Tab Order
            self.LiftWidgets()

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

        def LiftWidgets(self):
            self.InitiativeEntryResultEntry.lift()
            self.InitiativeEntryTiePriorityDropdown.lift()
            self.InitiativeEntryNameEntry.lift()
