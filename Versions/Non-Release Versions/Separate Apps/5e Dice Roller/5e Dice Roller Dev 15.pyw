import json
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
root.wm_title("Dice Roller")
root.option_add("*Font", "TkDefaultFont")


# Window Elements
class DiceRoller:
    def __init__(self, master):
        self.DiceNumberEntryVar = StringVar(value="1")
        self.DieTypeEntryVar = StringVar(value="20")
        self.ModifierEntryVar = StringVar(value="0")
        self.CritRangeEntryVar = StringVar(value="20")

        # Dice Roller Frame
        self.DiceRollerFrame = Frame(master)
        self.DiceRollerFrame.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)

        # Dice Entry and Buttons Frame
        self.DiceEntryAndButtonsFrame = Frame(self.DiceRollerFrame)
        self.DiceEntryAndButtonsFrame.grid_columnconfigure(0, weight=1)
        self.DiceEntryAndButtonsFrame.grid_columnconfigure(2, weight=1)
        self.DiceEntryAndButtonsFrame.grid_columnconfigure(4, weight=1)
        self.DiceEntryAndButtonsFrame.grid(row=0, column=0, columnspan=2, sticky=NSEW)

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
        self.ResultsFieldFrame.grid(row=2, column=1, padx=2, pady=2)
        self.ResultsField = ScrolledText(self.ResultsFieldFrame, Width=200, Height=258, Disabled=True, DisabledBackground=GlobalInst.ButtonColor)
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
        ToolbarAndStatusBarInst.StatusBarSetText("Results copied to clipboard.", Lock=True)
        root.after(2000, lambda: ToolbarAndStatusBarInst.StatusBarSetText("Status", Unlock=True))

    def ClearResults(self, event):
        # Confirm
        ClearConfirm = messagebox.askyesno("Clear Results", "Are you sure you want to clear the roll results?  This cannot be undone.")
        if not ClearConfirm:
            return

        # Clear
        self.ResultsField.set("")

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

    class PresetRolls:
        def __init__(self, master):
            # Variables
            self.ScrollingDisabledVar = BooleanVar(value=False)

            # Preset Rolls Frame
            self.PresetRollsFrame = LabelFrame(master, text="Preset Rolls:")
            self.PresetRollsFrame.grid(row=2, column=0, padx=2, pady=2)

            # Scrolled Canvas
            self.PresetRollsScrolledCanvas = ScrolledCanvas(self.PresetRollsFrame, Height=262, Width=418, ScrollingDisabledVar=self.ScrollingDisabledVar)

            # Scrolled Canvas Headers
            self.PresetRollsScrolledCanvasNameHeader = Label(self.PresetRollsScrolledCanvas.WindowFrame, text="Name", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.PresetRollsScrolledCanvasNameHeader.grid(row=0, column=0, sticky=NSEW)
            self.PresetRollsScrolledCanvasNameHeader.bind("<Button-1>", lambda event: self.Sort("Name"))
            self.PresetRollsScrolledCanvasNameHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Name", SearchMode=True))
            self.PresetRollsScrolledCanvasNameHeader.bind("<Button-3>", lambda event: self.Sort("Name", Reverse=True))
            self.PresetRollsScrolledCanvasRollHeader = Label(self.PresetRollsScrolledCanvas.WindowFrame, text="Roll", bd=2, relief=GROOVE)
            self.PresetRollsScrolledCanvasRollHeader.grid(row=0, column=1, sticky=NSEW, columnspan=6)
            self.PresetRollsScrolledCanvasSortOrderHeader = Label(self.PresetRollsScrolledCanvas.WindowFrame, text="Sort\nOrder", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.PresetRollsScrolledCanvasSortOrderHeader.grid(row=0, column=7, sticky=NSEW)
            self.PresetRollsScrolledCanvasSortOrderHeader.bind("<Button-1>", lambda event: self.Sort("Sort Order"))
            self.PresetRollsScrolledCanvasSortOrderHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Sort Order", SearchMode=True))
            self.PresetRollsScrolledCanvasSortOrderHeader.bind("<Button-3>", lambda event: self.Sort("Sort Order", Reverse=True))

            # Preset Rolls List
            self.PresetRollsList = []

            # Sort Order Values
            self.SortOrderValuesString = "\"\""
            for CurrentIndex in range(1, 51):
                self.SortOrderValuesString += "," + str(CurrentIndex)
            self.SortOrderValuesTuple = eval(self.SortOrderValuesString)

            # Preset Rolls
            for CurrentIndex in range(1, 51):
                CurrentEntry = self.PresetRollEntry(self.PresetRollsScrolledCanvas.WindowFrame, self.PresetRollsList, self.ScrollingDisabledVar, self.SortOrderValuesTuple, CurrentIndex)
                CurrentEntry.Display(CurrentIndex)

        def Sort(self, Column, Reverse=False, SearchMode=False):
            # List to Sort
            ListToSort = []

            if SearchMode:
                # Get Search String
                SearchStringPrompt = StringPrompt(root, "Search", "What do you want to search for?")
                root.wait_window(SearchStringPrompt.Window)
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
            GlobalInst.SavePrompt = True
            GlobalInst.UpdateWindowTitle(AddSavePrompt=True)

        class PresetRollEntry:
            def __init__(self, master, List, ScrollingDisabledVar, SortOrderValuesTuple, Row):
                # Store Parameters
                self.master = master
                self.ScrollingDisabledVar = ScrollingDisabledVar
                self.SortOrderValuesTuple = SortOrderValuesTuple
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
                self.PresetRollModifierEntry = Entry(master, justify=CENTER, width=5, textvariable=self.PresetRollModifierEntryVar, disabledbackground="light gray", disabledforeground="black")

                # Sort Order
                self.PresetRollSortOrder = ttk.Combobox(master, textvariable=self.PresetRollSortOrderVar, values=self.SortOrderValuesTuple, width=5, state="readonly", justify=CENTER)
                self.PresetRollSortOrder.bind("<Enter>", self.DisableScrolling)
                self.PresetRollSortOrder.bind("<Leave>", self.EnableScrolling)

            def RollPreset(self):
                DiceRollerInst.DiceNumberEntryVar.set(self.PresetRollDiceNumberEntry.get())
                DiceRollerInst.DieTypeEntryVar.set(self.PresetRollDieTypeEntry.get())
                DiceRollerInst.ModifierEntryVar.set(self.PresetRollModifierEntry.get())
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
                GlobalInst.SavedData["PresetRollNameEntryVar" + str(self.Row)] = self.PresetRollNameEntryVar
                GlobalInst.SavedData["PresetRollDiceNumberEntryVar" + str(self.Row)] = self.PresetRollDiceNumberEntryVar
                GlobalInst.SavedData["PresetRollDieTypeEntryVar" + str(self.Row)] = self.PresetRollDieTypeEntryVar
                GlobalInst.SavedData["PresetRollModifierEntryVar" + str(self.Row)] = self.PresetRollModifierEntryVar
                GlobalInst.SavedData["PresetRollSortOrderVar" + str(self.Row)] = self.PresetRollSortOrderVar

            def DisableScrolling(self, event):
                self.ScrollingDisabledVar.set(True)

            def EnableScrolling(self, event):
                self.ScrollingDisabledVar.set(False)


class MenuAndStatusBar:
    def __init__(self, master):
        # Variables
        self.StatusBarTextVar = StringVar(value="Status")
        self.StatusBarLockedVar = BooleanVar(value=False)
        self.CurrentOpenFilePath = StringVar()
        self.Opening = False
        self.OpenErrors = False
        self.OpenErrorsString = ""

        # Menu Bar
        self.MenuBar = Menu(master)
        master.config(menu=self.MenuBar)

        # File Menu
        self.FileMenu = Menu(self.MenuBar, tearoff=0)
        self.FileMenu.add_command(label="New", command=self.NewButton, accelerator="Ctrl+N")
        self.FileMenu.add_command(label="Open", command=self.OpenButton, accelerator="Ctrl+O")
        self.FileMenu.add_separator()
        self.FileMenu.add_command(label="Save", command=self.SaveButton, accelerator="Ctrl+S")
        self.FileMenu.add_command(label="Save As", command=lambda: self.SaveButton(SaveAs=True), accelerator="Ctrl+Shift+S")
        self.FileMenu.add_separator()
        self.FileMenu.add_command(label="Exit", command=GlobalInst.CloseWindow)
        self.MenuBar.add_cascade(label="File", menu=self.FileMenu)

        # Toolbar Frame
        self.ToolbarFrame = Frame(master, bg="gray", bd=1, relief=SUNKEN)
        self.ToolbarFrame.grid_columnconfigure(0, weight=1)
        self.ToolbarFrame.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)

        # Status Bar Label
        self.StatusBarLabel = Label(self.ToolbarFrame, textvariable=self.StatusBarTextVar, fg="white", bg="gray")
        self.StatusBarLabel.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)

    # Save Methods
    def SaveButton(self, SaveAs=False):
        self.StatusBarSetText("Saving...", Lock=True)
        CurrentPath = self.CurrentOpenFilePath.get()
        if CurrentPath == "" or SaveAs:
            SaveFileName = filedialog.asksaveasfilename(filetypes=(("Roll file", "*.roll"), ("All files", "*.*")), defaultextension=".roll", title="Save Roll File")
        else:
            SaveFileName = CurrentPath
        TextFileName = "Roll Data.txt"
        if SaveFileName != "":
            try:
                with ZipFile(SaveFileName, mode="w") as SaveFile:
                    with open(TextFileName, mode="w") as TextFile:
                        self.SaveData(TextFile)
                    SaveFile.write(TextFileName)
            except PermissionError:
                messagebox.showerror("Save File Permission Error",
                                     "Could not save the following file due to a permission error:\n\n" + SaveFileName + "\n\nIt could be open in another program or in a location that you don't have permission to write to.")
                self.StatusBarSetText("No file saved!", Lock=True)
                root.after(2000, lambda: self.StatusBarSetText("Status", Unlock=True))
                return False
            GlobalInst.DeleteFile(TextFileName)
            self.CurrentOpenFilePath.set(SaveFileName)
            sleep(0.5)
            GlobalInst.UpdateWindowTitle()
            self.StatusBarSetText("File saved as:  " + os.path.basename(SaveFileName), Lock=True)
            root.after(2000, lambda: self.StatusBarSetText("Status", Unlock=True))
            GlobalInst.SavePrompt = False
            return True
        else:
            self.StatusBarSetText("No file saved!", Lock=True)
            root.after(2000, lambda: self.StatusBarSetText("Status", Unlock=True))
            return False

    def SaveData(self, File):
        for Tag, Field in GlobalInst.SavedData.items():
            File.write(json.dumps({Tag: Field.get()}) + "\n")

    # Open Methods
    def OpenButton(self):
        if GlobalInst.SavePrompt:
            SaveConfirm = messagebox.askyesnocancel("Save", "Save unsaved work before opening?")
            if SaveConfirm == None:
                return
            elif SaveConfirm == True:
                if not ToolbarAndStatusBarInst.SaveButton():
                    return
        self.StatusBarSetText("Opening...", Lock=True)
        OpenFileName = filedialog.askopenfilename(filetypes=(("Roll file", "*.roll"), ("All files", "*.*")), defaultextension=".roll", title="Open Roll File")
        TextFileName = "Roll Data.txt"
        if OpenFileName != "":
            with ZipFile(OpenFileName, mode="r") as OpenFile:
                with open(OpenFile.extract(TextFileName), mode="r") as TextFile:
                    self.OpenData(TextFile)
            GlobalInst.DeleteFile(TextFileName)
            self.CurrentOpenFilePath.set(OpenFileName)
            GlobalInst.UpdateWindowTitle()
            sleep(0.5)
            if self.OpenErrors:
                OpenErrorsPromptInst = OpenErrorsPrompt(root, self.OpenErrorsString[:-1])
                root.wait_window(OpenErrorsPromptInst.Window)
                self.OpenErrors = False
                self.OpenErrorsString = ""
            self.StatusBarSetText("Opened file:  " + os.path.basename(OpenFileName), Lock=True)
            root.after(2000, lambda: self.StatusBarSetText("Status", Unlock=True))
            GlobalInst.SavePrompt = False
        else:
            self.StatusBarSetText("No file opened!", Lock=True)
            root.after(2000, lambda: self.StatusBarSetText("Status", Unlock=True))

    def OpenData(self, File):
        self.Opening = True
        for Line in File:
            if Line != "":
                LoadedLine = json.loads(Line)
                for Tag, Field in LoadedLine.items():
                    try:
                        GlobalInst.SavedData[Tag].set(Field)
                    except KeyError:
                        self.OpenErrors = True
                        self.OpenErrorsString += Line
        self.Opening = False

    def NewButton(self):
        # Check for Save Prompt
        if GlobalInst.SavePrompt:
            SaveConfirm = messagebox.askyesnocancel("New", "Save unsaved work before starting a new file?")
            if SaveConfirm == None:
                return
            elif SaveConfirm == True:
                if not ToolbarAndStatusBarInst.SaveButton():
                    return

        # Reset Saved Fields to Default Values
        for Field in GlobalInst.SavedData.values():
            if type(Field) == BooleanVar:
                Field.set(False)
            elif Field == DiceRollerInst.CritRangeEntryVar:
                Field.set("20")
            else:
                Field.set("")

        # Dice Roller Defaults
        DiceRollerInst.DiceNumberEntryVar.set("1")
        DiceRollerInst.DieTypeEntryVar.set("20")
        DiceRollerInst.ModifierEntryVar.set("0")

        # No Current File
        self.CurrentOpenFilePath.set("")

        # No Save Prompt
        GlobalInst.SavePrompt = False
        GlobalInst.UpdateWindowTitle()

        # Handle Status Bar
        self.StatusBarSetText("New file started.", Lock=True)
        root.after(2000, lambda: self.StatusBarSetText("Status", Unlock=True))

    # Status Bar Text Methods
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
        Widget.bind("<Enter>", lambda event: ToolbarAndStatusBarInst.StatusBarSetText(TooltipText, Lock=EnterLock, Unlock=EnterUnlock))
        Widget.bind("<Leave>", lambda event: ToolbarAndStatusBarInst.StatusBarSetText(LeaveText, Lock=LeaveLock, Unlock=LeaveUnlock))


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

    def UpdateWindowTitle(self, AddSavePrompt=False):
        CurrentOpenFile = ToolbarAndStatusBarInst.CurrentOpenFilePath.get()
        SavePromptString = ""
        if CurrentOpenFile != "":
            CurrentOpenFile = " [" + os.path.basename(CurrentOpenFile) + "]"
        if AddSavePrompt:
            SavePromptString = " *"
        root.wm_title("Dice Roller" + CurrentOpenFile + SavePromptString)

    def ConfigureBindings(self):
        # Scrolling
        DiceRollerInst.PresetRollsInst.PresetRollsScrolledCanvas.BindEnterAndLeaveToBindMouseWheel()

        # Save and Open Keystrokes
        root.bind("<Control-s>", lambda event: ToolbarAndStatusBarInst.SaveButton())
        root.bind("<Control-S>", lambda event: ToolbarAndStatusBarInst.SaveButton(SaveAs=True))
        root.bind("<Control-o>", lambda event: ToolbarAndStatusBarInst.OpenButton())
        root.bind("<Control-n>", lambda event: ToolbarAndStatusBarInst.NewButton())

        # Sort Tooltip String
        SortTooltipString = "Left-click/right-click to sort in ascending/descending order.  Shift+left-click to search."

        # Dice Roller Tooltips
        ToolbarAndStatusBarInst.TooltipConfig(DiceRollerInst.DiceNumberEntry, "Scroll the mouse wheel or type to change the number of dice.")
        ToolbarAndStatusBarInst.TooltipConfig(DiceRollerInst.DieTypeEntry, "Scroll the mouse wheel or type to change the die type.")
        ToolbarAndStatusBarInst.TooltipConfig(DiceRollerInst.ModifierEntry, "Scroll the mouse wheel or type to change the modifier.")
        ToolbarAndStatusBarInst.TooltipConfig(DiceRollerInst.ResultsField.ScrolledTextFrame, "Left-click to copy results to the clipboard.  Right-click to clear.")
        ToolbarAndStatusBarInst.TooltipConfig(DiceRollerInst.PresetRollsInst.PresetRollsScrolledCanvasNameHeader, SortTooltipString)
        ToolbarAndStatusBarInst.TooltipConfig(DiceRollerInst.PresetRollsInst.PresetRollsScrolledCanvasSortOrderHeader, SortTooltipString)

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

    def DeleteFile(self, File):
        try:
            os.remove(File)
        except PermissionError:
            messagebox.showerror("Temporary File Permission Error", "Could not delete the following temporary file due to a permission error:\n\n" + File + "\n\nTry again or delete the file manually.")


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
        GlobalInst.WindowGeometry(self.Window, True)
        self.Window.focus_force()

    def CopyToClipboard(self):
        self.UnopenedDataField.Text.clipboard_clear()
        self.UnopenedDataField.Text.clipboard_append(self.ErrorString)
        ToolbarAndStatusBarInst.StatusBarSetText("Unopened data copied to clipboard.", Lock=True)
        root.after(2000, lambda: ToolbarAndStatusBarInst.StatusBarSetText("Status", Unlock=True))

    def OK(self):
        self.Window.destroy()


# Global Functions and Variables
GlobalInst = Global()

# Populate Window
DiceRollerInst = DiceRoller(root)
ToolbarAndStatusBarInst = MenuAndStatusBar(root)

# Inst-Dependent Bindings
GlobalInst.ConfigureBindings()

# Initial Window Behavior
GlobalInst.WindowGeometry(root, False)
root.focus_force()

# Main Loop
root.mainloop()
