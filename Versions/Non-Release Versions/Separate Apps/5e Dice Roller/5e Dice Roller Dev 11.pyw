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
        ToolbarAndStatusBarInst.ToolbarSetText("Results copied to clipboard.", Lock=True)
        root.after(2000, lambda: ToolbarAndStatusBarInst.ToolbarSetText("Status", Unlock=True))

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
            # Preset Rolls Frame
            self.PresetRollsFrame = LabelFrame(master, text="Preset Rolls:")
            self.PresetRollsFrame.grid(row=2, column=0, padx=2, pady=2)

            self.PresetRollsScrolledCanvas = ScrolledCanvas(self.PresetRollsFrame, Height=262, Width=317)

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
                self.PresetRollModifierButton = Label(master, text="+")
                self.PresetRollModifierButton.grid(row=self.Row, column=5, sticky=NSEW)
                self.PresetRollModifierEntry = Entry(master, justify=CENTER, width=5, textvariable=self.PresetRollModifierEntryVar, disabledbackground="light gray", disabledforeground="black")
                self.PresetRollModifierEntry.grid(row=self.Row, column=6, sticky=NSEW)

                # Add Saved Fields to Character Data Dictionary
                GlobalInst.SavedData["PresetRollNameEntryVar" + str(self.Row)] = self.PresetRollNameEntryVar
                GlobalInst.SavedData["PresetRollDiceNumberEntryVar" + str(self.Row)] = self.PresetRollDiceNumberEntryVar
                GlobalInst.SavedData["PresetRollDieTypeEntryVar" + str(self.Row)] = self.PresetRollDieTypeEntryVar
                GlobalInst.SavedData["PresetRollModifierEntryVar" + str(self.Row)] = self.PresetRollModifierEntryVar

            def RollPreset(self):
                DiceRollerInst.DiceNumberEntryVar.set(self.PresetRollDiceNumberEntry.get())
                DiceRollerInst.DieTypeEntryVar.set(self.PresetRollDieTypeEntry.get())
                DiceRollerInst.ModifierEntryVar.set(self.PresetRollModifierEntry.get())
                DiceRollerInst.Roll(self.PresetRollNameEntryVar.get() + ":\n")


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
        self.ToolbarFrame.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)

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
        self.StatusBarTextVar.set("Saving...")
        CurrentPath = self.CurrentOpenFilePath.get()
        if CurrentPath == "":
            SaveFileName = filedialog.asksaveasfilename(filetypes=(("Roll file", "*.roll"), ("All files", "*.*")), defaultextension=".roll", title="Save Rolls As")
        else:
            SaveFileName = CurrentPath
        TextFileName = "Roll Data.txt"
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
        self.StatusBarTextVar.set("Opening...")
        OpenFileName = filedialog.askopenfilename(filetypes=(("Roll file", "*.roll"), ("All files", "*.*")), defaultextension=".roll", title="Open Rolls")
        TextFileName = "Roll Data.txt"
        if OpenFileName != "":
            with ZipFile(OpenFileName, mode="r") as OpenFile:
                with open(OpenFile.extract(TextFileName), mode="r") as TextFile:
                    self.OpenRollData(TextFile)
            os.remove(TextFileName)
            self.CurrentOpenFilePath.set(OpenFileName)
            GlobalInst.UpdateWindowTitle()
            sleep(0.5)
            if self.OpenErrors:
                messagebox.showerror("Open Errors", "Some data in the file could not be opened.  This could be due to changes in the file format.")
                self.OpenErrors = False
            self.ToolbarSetText("Opened file:  " + os.path.basename(OpenFileName), Lock=True)
            root.after(2000, lambda: self.ToolbarSetText("Status", Unlock=True))
            GlobalInst.SavePrompt = False
        else:
            self.ToolbarSetText("No file opened!", Lock=True)
            root.after(2000, lambda: self.ToolbarSetText("Status", Unlock=True))

    def OpenRollData(self, File):
        self.Opening = True
        for Line in File:
            if Line != "":
                LoadedLine = json.loads(Line)
                for Tag, Field in LoadedLine.items():
                    try:
                        GlobalInst.SavedData[Tag].set(Field)
                    except KeyError:
                        self.OpenErrors = True
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

        # Save and Open Keystrokes and Tooltips
        root.bind("<Control-s>", ToolbarAndStatusBarInst.SaveKeystroke)
        root.bind("<Control-S>", ToolbarAndStatusBarInst.SaveAsKeystroke)
        root.bind("<Control-o>", ToolbarAndStatusBarInst.OpenKeystroke)
        ToolbarAndStatusBarInst.TooltipConfig(ToolbarAndStatusBarInst.ToolbarSaveButton, "Keyboard Shortcut:  Ctrl+S")
        ToolbarAndStatusBarInst.TooltipConfig(ToolbarAndStatusBarInst.ToolbarSaveAsButton, "Keyboard Shortcut:  Ctrl+Shift+S")
        ToolbarAndStatusBarInst.TooltipConfig(ToolbarAndStatusBarInst.ToolbarOpenButton, "Keyboard Shortcut:  Ctrl+O")

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


# Global Functions and Variables
GlobalInst = Global()

# Populate Window
DiceRollerInst = DiceRoller(root)
ToolbarAndStatusBarInst = ToolbarAndStatusBar(root)

# Inst-Dependent Bindings
GlobalInst.ConfigureBindings()

# Initial Window Behavior
GlobalInst.WindowGeometry(root, False)
root.focus_force()

# Main Loop
root.mainloop()
