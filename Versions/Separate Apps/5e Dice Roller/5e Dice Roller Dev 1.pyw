import platform
from tkinter import *
import tkinter.scrolledtext as ScrolledTextClass
from tkinter import filedialog
from tkinter import messagebox
from time import sleep
import random
import os
from zipfile import ZipFile

# Global Variables
OS = platform.system()
ButtonColor = "#F1F1D4"

# Create and Configure Window
root = Tk()
root.wm_title("Dice Roller")
root.option_add("*Font", "TkDefaultFont")


# Global Functions
def GetStringVarAsInt(Var):
    VarText = Var.get()
    if len(VarText) == 0:
        VarText = 0
    return int(VarText)


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


def ConfigureBindings():
    # Preset Rolls Scrolling
    DiceRollerInst.PresetRollsInst.PresetRollsFrame.bind("<Enter>", DiceRollerInst.PresetRollsInst.BindMouseWheelPresetRolls)
    DiceRollerInst.PresetRollsInst.PresetRollsFrame.bind("<Leave>", UnbindMouseWheel)

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


# Window Elements
class DiceRoller:
    DiceNumberEntryVar = StringVar(value="1")
    DieTypeEntryVar = StringVar(value="20")
    ModifierEntryVar = StringVar(value="0")

    def __init__(self, master):
        # Dice Roller Frame
        self.DiceRollerFrame = LabelFrame(master, text="Dice Roller:")
        self.DiceRollerFrame.pack(side=TOP, padx=2, pady=2)

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
                self.PresetRollModifierLabel = Label(master, text="+")
                self.PresetRollModifierLabel.grid(row=self.Row, column=5, sticky=NSEW)
                self.PresetRollModifierEntry = Entry(master, justify=CENTER, width=5, textvariable=self.PresetRollModifierEntryVar, disabledbackground="light gray", disabledforeground="black")
                self.PresetRollModifierEntry.grid(row=self.Row, column=6, sticky=NSEW)

            def RollPreset(self):
                DiceRollerInst.DiceNumberEntryVar.set(self.PresetRollDiceNumberEntry.get())
                DiceRollerInst.DieTypeEntryVar.set(self.PresetRollDieTypeEntry.get())
                DiceRollerInst.ModifierEntryVar.set(self.PresetRollModifierEntry.get())
                DiceRollerInst.Roll(self.PresetRollNameEntryVar.get() + ":\n")


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

    # Save Utility Methods
    def SaveText(self, File, Field, FieldTag):
        TextContent = Field.get("1.0", "end-1c")
        File.write("<" + str(FieldTag) + ">\n" + str(TextContent) + "\n</" + str(FieldTag) + ">\n")

    def SaveVar(self, File, Var, FieldTag):
        VarContent = Var.get()
        File.write("<" + str(FieldTag) + ">\n" + str(VarContent) + "\n</" + str(FieldTag) + ">\n")

    def SavePresetRollFields(self, File):
        for Entry in DiceRollerInst.PresetRollsInst.PresetRollsList:
            self.SaveVar(File, Entry.PresetRollNameEntryVar, "PRNameEntry" + str(Entry.Row))
            self.SaveVar(File, Entry.PresetRollDiceNumberEntryVar, "PRDiceNumberEntry" + str(Entry.Row))
            self.SaveVar(File, Entry.PresetRollDieTypeEntryVar, "PRDieTypeEntry" + str(Entry.Row))
            self.SaveVar(File, Entry.PresetRollModifierEntryVar, "PRModifierEntry" + str(Entry.Row))

    def SaveAsButton(self):
        self.PreviousOpenFilePath.set(self.CurrentOpenFilePath.get())
        self.CurrentOpenFilePath.set("")
        self.SaveButton()

    # Saving
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
                    # Save Preset Roll Fields
                    self.SavePresetRollFields(TextFile)
                SaveFile.write(TextFileName)
            os.remove(TextFileName)
            self.CurrentOpenFilePath.set(SaveFileName)
            root.wm_title(os.path.basename(SaveFileName) + " - Dice Roller")
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

    def OpenPresetRollFields(self, File):
        for Entry in DiceRollerInst.PresetRollsInst.PresetRollsList:
            self.OpenVar(File, Entry.PresetRollNameEntryVar, "PRNameEntry" + str(Entry.Row))
            self.OpenVar(File, Entry.PresetRollDiceNumberEntryVar, "PRDiceNumberEntry" + str(Entry.Row))
            self.OpenVar(File, Entry.PresetRollDieTypeEntryVar, "PRDieTypeEntry" + str(Entry.Row))
            self.OpenVar(File, Entry.PresetRollModifierEntryVar, "PRModifierEntry" + str(Entry.Row))
            if Entry.ConfigSubmitted.get():
                Entry.PresetRollModifierEntry.configure(state=DISABLED, cursor="arrow")

    # Opening
    def OpenButton(self):
        self.StatusBarTextVar.set("Opening...")
        OpenFileName = filedialog.askopenfilename(filetypes=(("Roll file", "*.roll"), ("All files", "*.*")), defaultextension=".roll", title="Open Roll File")
        TextFileName = "Roll Data.txt"
        if OpenFileName != "":
            with ZipFile(OpenFileName, mode="r") as OpenFile:
                with open(OpenFile.extract(TextFileName), mode="r") as TextFile:
                    # Open Preset Roll Fields
                    self.OpenPresetRollFields(TextFile)
            os.remove(TextFileName)
            self.CurrentOpenFilePath.set(OpenFileName)
            root.wm_title(os.path.basename(OpenFileName) + " - Dice Roller")
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
DiceRollerInst = DiceRoller(root)
ToolbarAndStatusBarInst = ToolbarAndStatusBar(root)

# Inst-Dependent Bindings
ConfigureBindings()

# Initial Window Behavior
WindowGeometry(root, False)
root.focus_force()

# Main Loop
root.mainloop()
