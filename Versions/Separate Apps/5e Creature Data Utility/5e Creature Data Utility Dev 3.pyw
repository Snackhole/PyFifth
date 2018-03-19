import json
import os
import platform
from decimal import *
from time import sleep
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from zipfile import ZipFile

# Create and Configure Window
root = Tk()
root.wm_title("Creature Data Utility")
root.option_add("*Font", "TkDefaultFont")


# Window Elements
class CreatureData:
    def __init__(self, master):
        self.DataSubmitted = BooleanVar()
        self.NameEntryVar = StringVar()
        self.SizeEntryVar = StringVar()
        self.TypeAndTagsEntryVar = StringVar()
        self.AlignmentEntryVar = StringVar()
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

        # Create Window
        self.CreatureDataFrame = Frame(master)
        self.CreatureDataFrame.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Name Entry
        self.NameFrame = LabelFrame(self.CreatureDataFrame, text="Name:")
        self.NameFrame.grid_columnconfigure(0, weight=1)
        self.NameFrame.grid(row=0, column=0, columnspan=3, padx=2, pady=2, sticky=NSEW)
        self.NameEntry = Entry(self.NameFrame, justify=CENTER, textvariable=self.NameEntryVar)
        self.NameEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

        # Size, Type, Tags, and Alignment Frame
        self.SizeTypeTagsAndAlignmentFrame = Frame(self.CreatureDataFrame)
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
        self.HPACSpeedCRExperienceEntriesFrame = Frame(self.CreatureDataFrame)
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
        self.AbilitiesFrame = LabelFrame(self.CreatureDataFrame, text="Ability Scores:")
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
        self.SkillSensesAndLanguagesFrame = LabelFrame(self.CreatureDataFrame, text="Skills, Senses, and Languages:")
        self.SkillSensesAndLanguagesFrame.grid(row=3, column=1, padx=2, pady=2, sticky=NSEW)
        self.SkillSensesAndLanguagesField = ScrolledText(self.SkillSensesAndLanguagesFrame, Width=300, Height=100)
        self.SkillSensesAndLanguagesField.grid(row=0, column=0)

        # Saving Throws
        self.SavingThrowsFrame = LabelFrame(self.CreatureDataFrame, text="Saving Throws:")
        self.SavingThrowsFrame.grid(row=2, column=2, padx=2, pady=2, sticky=NSEW)
        self.SavingThrowsField = ScrolledText(self.SavingThrowsFrame, Width=383, Height=100)
        self.SavingThrowsField.grid(row=0, column=0)

        # Vulnerabilities, Resistances, and Immunities
        self.VulnerabilitiesResistancesAndImmunitiesFrame = LabelFrame(self.CreatureDataFrame, text="Vulnerabilities, Resistances, and Immunities:")
        self.VulnerabilitiesResistancesAndImmunitiesFrame.grid(row=3, column=2, padx=2, pady=2, sticky=NSEW)
        self.VulnerabilitiesResistancesAndImmunitiesField = ScrolledText(self.VulnerabilitiesResistancesAndImmunitiesFrame, Width=383, Height=100)
        self.VulnerabilitiesResistancesAndImmunitiesField.grid(row=0, column=0)

        # Special Traits
        self.SpecialTraitsFrame = LabelFrame(self.CreatureDataFrame, text="Special Traits:")
        self.SpecialTraitsFrame.grid(row=4, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
        self.SpecialTraitsField = ScrolledText(self.SpecialTraitsFrame, Width=383, Height=75)
        self.SpecialTraitsField.grid(row=0, column=0)

        # Actions
        self.ActionsFrame = LabelFrame(self.CreatureDataFrame, text="Actions:")
        self.ActionsFrame.grid(row=5, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
        self.ActionsField = ScrolledText(self.ActionsFrame, Width=383, Height=75)
        self.ActionsField.grid(row=0, column=0)

        # Reactions
        self.ReactionsFrame = LabelFrame(self.CreatureDataFrame, text="Reactions:")
        self.ReactionsFrame.grid(row=6, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
        self.ReactionsField = ScrolledText(self.ReactionsFrame, Width=383, Height=75)
        self.ReactionsField.grid(row=0, column=0)

        # Inventory
        self.InventoryFrame = LabelFrame(self.CreatureDataFrame, text="Inventory:")
        self.InventoryFrame.grid(row=4, column=2, padx=2, pady=2, sticky=NSEW)
        self.InventoryField = ScrolledText(self.InventoryFrame, Width=383, Height=75)
        self.InventoryField.grid(row=0, column=0)

        # Legendary Actions and Lair Actions
        self.LegendaryActionsAndLairActionsFrame = LabelFrame(self.CreatureDataFrame, text="Legendary Actions and Lair Actions:")
        self.LegendaryActionsAndLairActionsFrame.grid(row=5, column=2, padx=2, pady=2, sticky=NSEW)
        self.LegendaryActionsAndLairActionsField = ScrolledText(self.LegendaryActionsAndLairActionsFrame, Width=383, Height=75)
        self.LegendaryActionsAndLairActionsField.grid(row=0, column=0)

        # Notes
        self.NotesFrame = LabelFrame(self.CreatureDataFrame, text="Notes:")
        self.NotesFrame.grid(row=6, column=2, padx=2, pady=2, sticky=NSEW)
        self.NotesField = ScrolledText(self.NotesFrame, Width=383, Height=75)
        self.NotesField.grid(row=0, column=0)

        # Add Saved Fields to Saved Data Dictionary
        GlobalInst.SavedData["NameEntryVar"] = self.NameEntryVar
        GlobalInst.SavedData["ACEntryVar"] = self.ACEntryVar
        GlobalInst.SavedData["MaxHPEntryVar"] = self.MaxHPEntryVar
        GlobalInst.SavedData["SizeEntryVar"] = self.SizeEntryVar
        GlobalInst.SavedData["TypeAndTagsEntryVar"] = self.TypeAndTagsEntryVar
        GlobalInst.SavedData["AlignmentEntryVar"] = self.AlignmentEntryVar
        GlobalInst.SavedData["SpeedEntryVar"] = self.SpeedEntryVar
        GlobalInst.SavedData["CRAndExperienceEntryVar"] = self.CRAndExperienceEntryVar
        GlobalInst.SavedData["AbilitiesStrengthEntryVar"] = self.AbilitiesStrengthEntryVar
        GlobalInst.SavedData["AbilitiesDexterityEntryVar"] = self.AbilitiesDexterityEntryVar
        GlobalInst.SavedData["AbilitiesConstitutionEntryVar"] = self.AbilitiesConstitutionEntryVar
        GlobalInst.SavedData["AbilitiesIntelligenceEntryVar"] = self.AbilitiesIntelligenceEntryVar
        GlobalInst.SavedData["AbilitiesWisdomEntryVar"] = self.AbilitiesWisdomEntryVar
        GlobalInst.SavedData["AbilitiesCharismaEntryVar"] = self.AbilitiesCharismaEntryVar
        GlobalInst.SavedData["SkillSensesAndLanguagesFieldVar"] = self.SkillSensesAndLanguagesField
        GlobalInst.SavedData["SavingThrowsFieldVar"] = self.SavingThrowsField
        GlobalInst.SavedData["VulnerabilitiesResistancesAndImmunitiesFieldVar"] = self.VulnerabilitiesResistancesAndImmunitiesField
        GlobalInst.SavedData["SpecialTraitsFieldVar"] = self.SpecialTraitsField
        GlobalInst.SavedData["ActionsFieldVar"] = self.ActionsField
        GlobalInst.SavedData["ReactionsFieldVar"] = self.ReactionsField
        GlobalInst.SavedData["InventoryFieldVar"] = self.InventoryField
        GlobalInst.SavedData["LegendaryActionsAndLairActionsFieldVar"] = self.LegendaryActionsAndLairActionsField
        GlobalInst.SavedData["NotesFieldVar"] = self.NotesField


class ToolbarAndStatusBar:
    def __init__(self, master):
        self.StatusBarTextVar = StringVar(value="Status")
        self.StatusBarLockedVar = BooleanVar(value=False)
        self.CurrentOpenFilePath = StringVar()
        self.PreviousOpenFilePath = StringVar()
        self.Opening = False
        self.OpenErrors = False
        self.OpenErrorsString = ""

        # Toolbar Frame
        self.ToolbarFrame = Frame(master, bg="gray", bd=1, relief=SUNKEN)
        self.ToolbarFrame.grid_columnconfigure(4, weight=1)
        self.ToolbarFrame.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)

        # Toolbar Open Button
        self.ToolbarOpenButton = Button(self.ToolbarFrame, text="Open", command=self.OpenButton, bg=GlobalInst.ButtonColor)
        self.ToolbarOpenButton.grid(row=0, column=0, padx=2, pady=2)

        # Toolbar New Button
        self.ToolbarNewButton = Button(self.ToolbarFrame, text="New", command=self.NewButton, bg=GlobalInst.ButtonColor)
        self.ToolbarNewButton.grid(row=0, column=1, padx=2, pady=2)

        # Toolbar Save Button
        self.ToolbarSaveButton = Button(self.ToolbarFrame, text="Save", command=self.SaveButton, bg=GlobalInst.ButtonColor)
        self.ToolbarSaveButton.grid(row=0, column=2, padx=2, pady=2)

        # Toolbar Save As Button
        self.ToolbarSaveAsButton = Button(self.ToolbarFrame, text="Save As", command=self.SaveAsButton, bg=GlobalInst.ButtonColor)
        self.ToolbarSaveAsButton.grid(row=0, column=3, padx=2, pady=2)

        # Status Bar Label
        self.StatusBarLabel = Label(self.ToolbarFrame, textvariable=self.StatusBarTextVar, fg="white", bg="gray")
        self.StatusBarLabel.grid(row=0, column=4, padx=2, pady=2, sticky=NSEW)

    # Save Methods
    def SaveButton(self):
        self.ToolbarSetText("Saving...", Lock=True)
        CurrentPath = self.CurrentOpenFilePath.get()
        if CurrentPath == "":
            SaveFileName = filedialog.asksaveasfilename(filetypes=(("Creature file", "*.crea"), ("All files", "*.*")), defaultextension=".crea", title="Save Creature File")
        else:
            SaveFileName = CurrentPath
        TextFileName = "Creature Data.txt"
        if SaveFileName != "":
            with ZipFile(SaveFileName, mode="w") as SaveFile:
                with open(TextFileName, mode="w") as TextFile:
                    self.SaveData(TextFile)
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

    def SaveData(self, File):
        for Tag, Field in GlobalInst.SavedData.items():
            File.write(json.dumps({Tag: Field.get()}) + "\n")

    def SaveAsButton(self):
        self.PreviousOpenFilePath.set(self.CurrentOpenFilePath.get())
        self.CurrentOpenFilePath.set("")
        self.SaveButton()

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
        OpenFileName = filedialog.askopenfilename(filetypes=(("Creature file", "*.crea"), ("All files", "*.*")), defaultextension=".crea", title="Open Creature File")
        TextFileName = "Creature Data.txt"
        if OpenFileName != "":
            with ZipFile(OpenFileName, mode="r") as OpenFile:
                with open(OpenFile.extract(TextFileName), mode="r") as TextFile:
                    self.OpenData(TextFile)
            os.remove(TextFileName)
            self.CurrentOpenFilePath.set(OpenFileName)
            GlobalInst.UpdateWindowTitle()
            sleep(0.5)
            if self.OpenErrors:
                OpenErrorsPromptInst = OpenErrorsPrompt(root, self.OpenErrorsString[:-1])
                root.wait_window(OpenErrorsPromptInst.Window)
                self.OpenErrors = False
                self.OpenErrorsString = ""
            self.ToolbarSetText("Opened file:  " + os.path.basename(OpenFileName), Lock=True)
            root.after(2000, lambda: self.ToolbarSetText("Status", Unlock=True))
            GlobalInst.SavePrompt = False
        else:
            self.ToolbarSetText("No file opened!", Lock=True)
            root.after(2000, lambda: self.ToolbarSetText("Status", Unlock=True))

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
            Field.set("")

        # No Current File
        self.CurrentOpenFilePath.set("")

        # No Save Prompt
        GlobalInst.SavePrompt = False
        GlobalInst.UpdateWindowTitle()

        # Handle Status Bar
        self.ToolbarSetText("New file started.", Lock=True)
        root.after(2000, lambda: self.ToolbarSetText("Status", Unlock=True))

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
        CreatureName = CreatureDataInst.NameEntryVar.get()
        CurrentOpenFile = ToolbarAndStatusBarInst.CurrentOpenFilePath.get()
        SavePromptString = ""
        if CurrentOpenFile != "":
            CurrentOpenFile = " [" + os.path.basename(CurrentOpenFile) + "]"
        if CreatureName != "":
            CreatureName += " - "
        if AddSavePrompt:
            SavePromptString = " *"
        root.wm_title(CreatureName + "Creature Data Utility" + CurrentOpenFile + SavePromptString)

    def ConfigureBindings(self):
        # Save and Open Keystrokes and Tooltips
        root.bind("<Control-s>", lambda event: ToolbarAndStatusBarInst.SaveButton())
        root.bind("<Control-S>", lambda event: ToolbarAndStatusBarInst.SaveAsButton())
        root.bind("<Control-o>", lambda event: ToolbarAndStatusBarInst.OpenButton())
        root.bind("<Control-n>", lambda event: ToolbarAndStatusBarInst.NewButton())
        ToolbarAndStatusBarInst.TooltipConfig(ToolbarAndStatusBarInst.ToolbarSaveButton, "Keyboard Shortcut:  Ctrl+S")
        ToolbarAndStatusBarInst.TooltipConfig(ToolbarAndStatusBarInst.ToolbarSaveAsButton, "Keyboard Shortcut:  Ctrl+Shift+S")
        ToolbarAndStatusBarInst.TooltipConfig(ToolbarAndStatusBarInst.ToolbarOpenButton, "Keyboard Shortcut:  Ctrl+O")
        ToolbarAndStatusBarInst.TooltipConfig(ToolbarAndStatusBarInst.ToolbarNewButton, "Keyboard Shortcut:  Ctrl+N")

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
        ToolbarAndStatusBarInst.ToolbarSetText("Unopened data copied to clipboard.", Lock=True)
        root.after(2000, lambda: ToolbarAndStatusBarInst.ToolbarSetText("Status", Unlock=True))

    def OK(self):
        self.Window.destroy()


# Global Functions and Variables
GlobalInst = Global()

# Populate Window
CreatureDataInst = CreatureData(root)
ToolbarAndStatusBarInst = ToolbarAndStatusBar(root)

# Inst-Dependent Bindings
GlobalInst.ConfigureBindings()

# Initial Window Behavior
GlobalInst.WindowGeometry(root, False)
root.focus_force()

# Main Loop
root.mainloop()
