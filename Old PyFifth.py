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

from Build import VersionedAppName


# Window Elements
class CharacterSheet:

    def UpdateStatsAndInventory(self):

        # Calculate Preset Roll Modifiers
        for Entry in Inst["PresetRolls"].PresetRollsList:
            CalculatedModifierString = Entry.PresetRollModifierEntryStatModifierInst.GetPresetDiceRollModifier()
            CurrentModifierString = Entry.PresetRollModifierEntryVar.get()
            if CalculatedModifierString not in ["", CurrentModifierString]:
                Entry.PresetRollModifierEntryVar.set(CalculatedModifierString)

        # Calculate Inventory
        self.InventoryInst.Calculate()

    # Portrait
    class Portrait():
        def __init__(self, master):
            self.PortraitSelectedVar = BooleanVarExtended("PortraitSelectedVar")
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
            self.ImportButton = ButtonExtended(self.PortraitHolderFrame, text="Import", command=self.Import, bg=GlobalInst.ButtonColor)
            self.ImportButton.grid(row=1, column=0, sticky=NSEW)
            self.ExportButton = ButtonExtended(self.PortraitHolderFrame, text="Export", command=self.Export, bg=GlobalInst.ButtonColor)
            self.ExportButton.grid(row=1, column=1, sticky=NSEW)
            self.ClearButton = ButtonExtended(self.PortraitHolderFrame, text="Clear", command=self.Clear, bg=GlobalInst.ButtonColor)
            self.ClearButton.grid(row=1, column=2, sticky=NSEW)

            # Portrait Instructions
            self.PortraitInstructions = Label(self.PortraitHolderFrame, text="Portrait must be a .gif file no larger than 400 x 400.")
            self.PortraitInstructions.grid(row=2, column=0, columnspan=3, sticky=NSEW)

            # Add to Clearable Fields
            SavingAndOpeningInst.ClearableFields.append(self)

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

        def Clear(self, Force=False):
            if self.PortraitSelectedVar.get() and not Force:
                ClearConfirm = messagebox.askyesno("Clear Portrait", "Are you sure you want to clear the portrait?  This cannot be undone.")
                if not ClearConfirm:
                    return
            self.PortraitSelectedVar.set(False)
            self.PortraitCanvas.delete("all")

        def SetToDefault(self):
            self.Clear(Force=True)

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
            self.SubmitButton = ButtonExtended(self.ButtonsFrame, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
            self.SubmitButton.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
            self.CancelButton = ButtonExtended(self.ButtonsFrame, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
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

    # Gain Experience Menu
    class GainExperienceMenu:
        def __init__(self, master):
            # Variables
            self.DataSubmitted = BooleanVar()
            self.DivideByDropdownVar = StringVar(value="1")
            self.DivideByDropdownVar.trace_add("write", lambda a, b, c: self.Calculate())
            self.TotalExperienceGainedEntryVar = StringVar(value="0")

            # Create Window
            self.Window = Toplevel(master)
            self.Window.wm_attributes("-toolwindow", 1)
            self.Window.wm_title("Gain Experience")

            # Experience Gained
            self.ExperienceGainedFrame = LabelFrame(self.Window, text="Exp. Gained:")
            self.ExperienceGainedFrame.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2, rowspan=3)
            self.ExperienceGainedScrolledCanvas = ScrolledCanvas(self.ExperienceGainedFrame, Width=64, Height=120)
            self.ExperienceGainedEntriesList = []
            for Row in range(50):
                NewEntry = self.ExperienceGainedEntry(self.ExperienceGainedScrolledCanvas.WindowFrame, self.ExperienceGainedEntriesList, Row)
                NewEntry.ExperienceGainedEntryVar.trace_add("write", lambda a, b, c: self.Calculate())
                NewEntry.ExperienceGainedEntry.bind("<FocusIn>", self.ExperienceGainedScrolledCanvas.MakeFocusVisible)

            # Divide By
            self.DivideByFrame = LabelFrame(self.Window, text="Divide By:")
            self.DivideByFrame.grid_columnconfigure(0, weight=1)
            self.DivideByFrame.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)
            self.DivisorList = []
            for Divisor in range(1, 101):
                self.DivisorList.append(str(Divisor))
            self.DivideByDropdown = DropdownExtended(self.DivideByFrame, textvariable=self.DivideByDropdownVar, values=self.DivisorList, width=5, state="readonly", justify=CENTER)
            self.DivideByDropdown.grid(row=0, column=0, sticky=NSEW)

            # Total Experience Gained
            self.TotalExperienceGainedFrame = LabelFrame(self.Window, text="Total Exp. Gained:")
            self.TotalExperienceGainedFrame.grid_columnconfigure(0, weight=1)
            self.TotalExperienceGainedFrame.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2)
            self.TotalExperienceGainedEntry = EntryExtended(self.TotalExperienceGainedFrame, textvariable=self.TotalExperienceGainedEntryVar, justify=CENTER, width=10, state=DISABLED, disabledforeground="black",
                                                            disabledbackground="light gray")
            self.TotalExperienceGainedEntry.grid(row=0, column=0, sticky=NSEW)

            # Buttons
            self.ButtonsFrame = Frame(self.Window)
            self.ButtonsFrame.grid_columnconfigure(0, weight=1)
            self.ButtonsFrame.grid(row=2, column=1, sticky=NSEW)
            self.SubmitButton = ButtonExtended(self.ButtonsFrame, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
            self.SubmitButton.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
            self.CancelButton = ButtonExtended(self.ButtonsFrame, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
            self.CancelButton.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)

            # Prevent Main Window Input
            self.Window.grab_set()

            # Handle Config Window Geometry and Focus
            GlobalInst.WindowGeometry(self.Window, IsDialog=True, DialogMaster=WindowInst)
            self.Window.focus_force()

            # Focus on First Entry
            self.ExperienceGainedEntriesList[0].ExperienceGainedEntry.focus_set()

        def Calculate(self):
            TotalExperienceGained = 0
            for ExperienceGained in self.ExperienceGainedEntriesList:
                TotalExperienceGained += GlobalInst.GetStringVarAsNumber(ExperienceGained.ExperienceGainedEntryVar)
            TotalExperienceGained = math.floor(TotalExperienceGained / GlobalInst.GetStringVarAsNumber(self.DivideByDropdownVar))
            self.TotalExperienceGainedEntryVar.set(str(TotalExperienceGained))

        def Submit(self):
            self.DataSubmitted.set(True)
            self.Window.destroy()

        def Cancel(self):
            self.DataSubmitted.set(False)
            self.Window.destroy()

        class ExperienceGainedEntry:
            def __init__(self, master, List, Row):
                # Store Parameters
                self.Row = Row

                # Variables
                self.ExperienceGainedEntryVar = StringVar()

                # Add to List
                List.append(self)

                # Entry
                self.ExperienceGainedEntry = EntryExtended(master, justify=CENTER, width=10, textvariable=self.ExperienceGainedEntryVar)
                self.ExperienceGainedEntry.ConfigureValidation(
                    lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Experience gained must be a whole number.", MinValue=0, LessThanMinString="Experience gained cannot be less than 0."), "key")
                self.ExperienceGainedEntry.grid(row=self.Row, column=0, sticky=NSEW)


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
            self.CloseButton = ButtonExtended(self.WidgetMaster, text="Close", command=self.Close, bg=GlobalInst.ButtonColor)
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


class AbilityScoreDerivatives:
    def __init__(self, master, List, SaveTagPrefix, Column, AttackTypeStringSuffix=""):
        # Store Parameters
        self.SaveTagPrefix = SaveTagPrefix
        self.Column = Column
        self.AttackTypeStringSuffix = AttackTypeStringSuffix

        # Variables
        self.AbilityScoreSelectionDropdownVar = StringVarExtended(self.SaveTagPrefix + "AbilitySelectionDropdownVar" + str(self.Column), ClearOnNew=True)
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
        self.AttackModifierEntryStatModifierInst = StatModifier(self.AttackModifierEntry, "<Button-3>", "Left-click on an attack modifier to roll 1d20 with it.\n\nRight-click to set a stat modifier.", "Attack Modifier",
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
            self.NameEntryVar = StringVarExtended("NameEntryVar", ClearOnNew=True)
            self.SizeEntryVar = StringVarExtended("SizeEntryVar", ClearOnNew=True)
            self.TypeAndTagsEntryVar = StringVarExtended("TypeAndTagsEntryVar", ClearOnNew=True)
            self.AlignmentEntryVar = StringVarExtended("AlignmentEntryVar", ClearOnNew=True)
            self.ProficiencyEntryVar = StringVarExtended("ProficiencyEntryVar", ClearOnNew=True)
            self.TempHPEntryVar = StringVarExtended("TempHPEntryVar", ClearOnNew=True)
            self.CurrentHPEntryVar = StringVarExtended("CurrentHPEntryVar", ClearOnNew=True)
            self.MaxHPEntryVar = StringVarExtended("MaxHPEntryVar", ClearOnNew=True)
            self.ACEntryVar = StringVarExtended("ACEntryVar", ClearOnNew=True)
            self.SpeedEntryVar = StringVarExtended("SpeedEntryVar", ClearOnNew=True)
            self.CRAndExperienceEntryVar = StringVarExtended("CRAndExperienceEntryVar", ClearOnNew=True)
            self.AbilitiesStrengthEntryVar = StringVarExtended("AbilitiesStrengthEntryVar", ClearOnNew=True)
            self.AbilitiesDexterityEntryVar = StringVarExtended("AbilitiesDexterityEntryVar", ClearOnNew=True)
            self.AbilitiesConstitutionEntryVar = StringVarExtended("AbilitiesConstitutionEntryVar", ClearOnNew=True)
            self.AbilitiesIntelligenceEntryVar = StringVarExtended("AbilitiesIntelligenceEntryVar", ClearOnNew=True)
            self.AbilitiesWisdomEntryVar = StringVarExtended("AbilitiesWisdomEntryVar", ClearOnNew=True)
            self.AbilitiesCharismaEntryVar = StringVarExtended("AbilitiesCharismaEntryVar", ClearOnNew=True)
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
        self.ProficiencyEntry.bind("<Up>", lambda event: self.ArrowKeyEvent("Up", self.ProficiencyEntryVar))
        self.ProficiencyEntry.bind("<Down>", lambda event: self.ArrowKeyEvent("Down", self.ProficiencyEntryVar))
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
        self.CurrentHPEntry.bind("<Return>", lambda event: self.Damage())
        self.CurrentHPEntry.bind("<Shift-Button-3>", lambda event: self.Heal())
        self.CurrentHPEntry.bind("<Shift-Return>", lambda event: self.Heal())
        self.CurrentHPTooltip = Tooltip(self.CurrentHPEntry, "Right-click or enter to damage.\n\nShift+right-click or shift+enter to heal.")

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
        self.AbilitiesStrengthEntry.bind("<Up>", lambda event: self.ArrowKeyEvent("Up", self.AbilitiesStrengthEntryVar))
        self.AbilitiesStrengthEntry.bind("<Down>", lambda event: self.ArrowKeyEvent("Down", self.AbilitiesStrengthEntryVar))
        self.AbilitiesStrengthEntry.grid(row=1, column=0, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesDexterityHeader = Label(self.AbilitiesFrame, text="DEX", bd=2, relief=GROOVE)
        self.AbilitiesDexterityHeader.grid(row=0, column=1, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesDexterityEntry = EntryExtended(self.AbilitiesFrame, justify=CENTER, width=5, textvariable=self.AbilitiesDexterityEntryVar, bg=GlobalInst.ButtonColor)
        self.AbilitiesDexterityEntry.bind("<Up>", lambda event: self.ArrowKeyEvent("Up", self.AbilitiesDexterityEntryVar))
        self.AbilitiesDexterityEntry.bind("<Down>", lambda event: self.ArrowKeyEvent("Down", self.AbilitiesDexterityEntryVar))
        self.AbilitiesDexterityEntry.grid(row=1, column=1, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesConstitutionHeader = Label(self.AbilitiesFrame, text="CON", bd=2, relief=GROOVE)
        self.AbilitiesConstitutionHeader.grid(row=0, column=2, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesConstitutionEntry = EntryExtended(self.AbilitiesFrame, justify=CENTER, width=5, textvariable=self.AbilitiesConstitutionEntryVar, bg=GlobalInst.ButtonColor)
        self.AbilitiesConstitutionEntry.bind("<Up>", lambda event: self.ArrowKeyEvent("Up", self.AbilitiesConstitutionEntryVar))
        self.AbilitiesConstitutionEntry.bind("<Down>", lambda event: self.ArrowKeyEvent("Down", self.AbilitiesConstitutionEntryVar))
        self.AbilitiesConstitutionEntry.grid(row=1, column=2, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesIntelligenceHeader = Label(self.AbilitiesFrame, text="INT", bd=2, relief=GROOVE)
        self.AbilitiesIntelligenceHeader.grid(row=2, column=0, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesIntelligenceEntry = EntryExtended(self.AbilitiesFrame, justify=CENTER, width=5, textvariable=self.AbilitiesIntelligenceEntryVar, bg=GlobalInst.ButtonColor)
        self.AbilitiesIntelligenceEntry.bind("<Up>", lambda event: self.ArrowKeyEvent("Up", self.AbilitiesIntelligenceEntryVar))
        self.AbilitiesIntelligenceEntry.bind("<Down>", lambda event: self.ArrowKeyEvent("Down", self.AbilitiesIntelligenceEntryVar))
        self.AbilitiesIntelligenceEntry.grid(row=3, column=0, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesWisdomHeader = Label(self.AbilitiesFrame, text="WIS", bd=2, relief=GROOVE)
        self.AbilitiesWisdomHeader.grid(row=2, column=1, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesWisdomEntry = EntryExtended(self.AbilitiesFrame, justify=CENTER, width=5, textvariable=self.AbilitiesWisdomEntryVar, bg=GlobalInst.ButtonColor)
        self.AbilitiesWisdomEntry.bind("<Up>", lambda event: self.ArrowKeyEvent("Up", self.AbilitiesWisdomEntryVar))
        self.AbilitiesWisdomEntry.bind("<Down>", lambda event: self.ArrowKeyEvent("Down", self.AbilitiesWisdomEntryVar))
        self.AbilitiesWisdomEntry.grid(row=3, column=1, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesCharismaHeader = Label(self.AbilitiesFrame, text="CHA", bd=2, relief=GROOVE)
        self.AbilitiesCharismaHeader.grid(row=2, column=2, padx=2, pady=2, sticky=NSEW)
        self.AbilitiesCharismaEntry = EntryExtended(self.AbilitiesFrame, justify=CENTER, width=5, textvariable=self.AbilitiesCharismaEntryVar, bg=GlobalInst.ButtonColor)
        self.AbilitiesCharismaEntry.bind("<Up>", lambda event: self.ArrowKeyEvent("Up", self.AbilitiesCharismaEntryVar))
        self.AbilitiesCharismaEntry.bind("<Down>", lambda event: self.ArrowKeyEvent("Down", self.AbilitiesCharismaEntryVar))
        self.AbilitiesCharismaEntry.grid(row=3, column=2, padx=2, pady=2, sticky=NSEW)

        # Mouse Wheel Configuration
        for EntryWidget in [self.AbilitiesStrengthEntry, self.AbilitiesDexterityEntry, self.AbilitiesConstitutionEntry, self.AbilitiesIntelligenceEntry, self.AbilitiesWisdomEntry, self.AbilitiesCharismaEntry,
                            self.ProficiencyEntry]:
            self.EntryTooltip = Tooltip(EntryWidget, "Scroll the mouse wheel, press the up and down keys, or type to change the modifier.")

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
        self.SkillSensesAndLanguagesField = ScrolledText(self.SkillSensesAndLanguagesFrame, Width=300, Height=120, SavedDataTag="SkillSensesAndLanguagesFieldVar" if not DialogMode else None,
                                                         ClearOnNew=True if not DialogMode else False)
        self.SkillSensesAndLanguagesField.grid(row=0, column=0)

        # Special Traits
        self.SpecialTraitsFrame = LabelFrame(self.WidgetMaster, text="Special Traits:")
        self.SpecialTraitsFrame.grid(row=2, column=2, padx=2, pady=2, sticky=NSEW)
        self.SpecialTraitsField = ScrolledText(self.SpecialTraitsFrame, Width=383, Height=120, SavedDataTag="SpecialTraitsFieldVar" if not DialogMode else None, ClearOnNew=True if not DialogMode else False)
        self.SpecialTraitsField.grid(row=0, column=0)

        # Actions
        self.ActionsFrame = LabelFrame(self.WidgetMaster, text="Actions:")
        self.ActionsFrame.grid(row=3, column=2, padx=2, pady=2, sticky=NSEW)
        self.ActionsField = ScrolledText(self.ActionsFrame, Width=383, Height=120, SavedDataTag="ActionsFieldVar" if not DialogMode else None, ClearOnNew=True if not DialogMode else False)
        self.ActionsField.grid(row=0, column=0)

        # Saving Throws
        self.SavingThrowsFrame = LabelFrame(self.WidgetMaster, text="Saving Throws:")
        self.SavingThrowsFrame.grid(row=4, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
        self.SavingThrowsField = ScrolledText(self.SavingThrowsFrame, Width=383, Height=75, SavedDataTag="SavingThrowsFieldVar" if not DialogMode else None, ClearOnNew=True if not DialogMode else False)
        self.SavingThrowsField.grid(row=0, column=0)

        # Vulnerabilities, Resistances, and Immunities
        self.VulnerabilitiesResistancesAndImmunitiesFrame = LabelFrame(self.WidgetMaster, text="Vulnerabilities, Resistances, and Immunities:")
        self.VulnerabilitiesResistancesAndImmunitiesFrame.grid(row=5, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
        self.VulnerabilitiesResistancesAndImmunitiesField = ScrolledText(self.VulnerabilitiesResistancesAndImmunitiesFrame, Width=383, Height=75,
                                                                         SavedDataTag="VulnerabilitiesResistancesAndImmunitiesFieldVar" if not DialogMode else None, ClearOnNew=True if not DialogMode else False)
        self.VulnerabilitiesResistancesAndImmunitiesField.grid(row=0, column=0)

        # Inventory
        self.InventoryFrame = LabelFrame(self.WidgetMaster, text="Inventory:")
        self.InventoryFrame.grid(row=6, column=0, columnspan=2, padx=2, pady=2, sticky=NSEW)
        self.InventoryField = ScrolledText(self.InventoryFrame, Width=383, Height=75, SavedDataTag="InventoryFieldVar" if not DialogMode else None, ClearOnNew=True if not DialogMode else False)
        self.InventoryField.grid(row=0, column=0)

        # Reactions
        self.ReactionsFrame = LabelFrame(self.WidgetMaster, text="Reactions:")
        self.ReactionsFrame.grid(row=4, column=2, padx=2, pady=2, sticky=NSEW)
        self.ReactionsField = ScrolledText(self.ReactionsFrame, Width=383, Height=75, SavedDataTag="ReactionsFieldVar" if not DialogMode else None, ClearOnNew=True if not DialogMode else False)
        self.ReactionsField.grid(row=0, column=0)

        # Legendary Actions and Lair Actions
        self.LegendaryActionsAndLairActionsFrame = LabelFrame(self.WidgetMaster, text="Legendary Actions and Lair Actions:")
        self.LegendaryActionsAndLairActionsFrame.grid(row=5, column=2, padx=2, pady=2, sticky=NSEW)
        self.LegendaryActionsAndLairActionsField = ScrolledText(self.LegendaryActionsAndLairActionsFrame, Width=383, Height=75, SavedDataTag="LegendaryActionsAndLairActionsFieldVar" if not DialogMode else None,
                                                                ClearOnNew=True if not DialogMode else False)
        self.LegendaryActionsAndLairActionsField.grid(row=0, column=0)

        # Notes
        self.NotesFrame = LabelFrame(self.WidgetMaster, text="Notes:")
        self.NotesFrame.grid(row=6, column=2, padx=2, pady=2, sticky=NSEW)
        self.NotesField = ScrolledText(self.NotesFrame, Width=383, Height=75, SavedDataTag="NotesFieldVar" if not DialogMode else None, ClearOnNew=True if not DialogMode else False)
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
            self.SubmitButton = ButtonExtended(self.ButtonsFrame, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
            self.SubmitButton.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)

            # Import Button
            self.ImportButton = ButtonExtended(self.ButtonsFrame, text="Import", command=self.Import, bg=GlobalInst.ButtonColor)
            self.ImportButton.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)

            # Export Button
            self.ExportButton = ButtonExtended(self.ButtonsFrame, text="Export", command=self.Export, bg=GlobalInst.ButtonColor)
            self.ExportButton.grid(row=0, column=2, sticky=NSEW, padx=2, pady=2)

            # Cancel Button
            self.CancelButton = ButtonExtended(self.ButtonsFrame, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
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

    def ArrowKeyEvent(self, Direction, EntryVar, MinValue=None, MaxValue=None):
        try:
            OldValue = GlobalInst.GetStringVarAsNumber(EntryVar)
        except ValueError:
            OldValue = 0
        if Direction == "Up":
            ValueDelta = 1
        elif Direction == "Down":
            ValueDelta = -1
        else:
            ValueDelta = 0
        NewValue = OldValue + ValueDelta
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
            self.PresetRollsScrolledCanvasHeight = 226
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
            self.PresetRollsScrolledCanvasHeight = 369
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
            self.PresetRollsScrolledCanvasHeight = 252
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
            self.PresetRollsScrolledCanvasHeight = 366
            self.PresetRollsScrolledCanvasWidth = 423

        # Variables
        self.DiceNumberEntryVar = StringVarExtended(DefaultValue="1", ClearOnNew=True)
        self.DieTypeEntryVar = StringVarExtended(DefaultValue="20", ClearOnNew=True)
        self.ModifierEntryVar = StringVarExtended(DefaultValue="0", ClearOnNew=True)
        self.CritMinimumEntryVar = StringVarExtended("CritMinimumEntryVar", DefaultValue="20", ClearOnNew=True)
        if WindowInst.Mode == "CharacterSheet":
            self.InspirationBoxVar = BooleanVarExtended("InspirationBoxVar", ClearOnNew=True)
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
        self.DiceNumberEntry.bind("<Up>", lambda event: self.ArrowKeyEvent("Up", self.DiceNumberEntryVar, MinValue=1))
        self.DiceNumberEntry.bind("<Down>", lambda event: self.ArrowKeyEvent("Down", self.DiceNumberEntryVar, MinValue=1))
        self.DiceNumberEntry.grid(row=0, column=0, rowspan=2, padx=2, pady=2, sticky=NSEW)
        self.DiceNumberTooltip = Tooltip(self.DiceNumberEntry, "Scroll the mouse wheel, press the up and down keys, or type to change the number of dice.")

        # Die Type
        self.DieTypeLabel = Label(self.DiceEntryAndButtonsFrame, text="d", font=self.DiceEntryFont)
        self.DieTypeLabel.grid(row=0, column=1, rowspan=2, sticky=NSEW)
        self.DieTypeEntry = EntryExtended(self.DiceEntryAndButtonsFrame, textvariable=self.DieTypeEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor, font=self.DiceEntryFont)
        self.DieTypeEntry.ConfigureValidation(lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Die type must be a whole number.", MinValue=1, LessThanMinString="Die type cannot be less than 1."), "key")
        self.DieTypeEntry.bind("<Up>", lambda event: self.ArrowKeyEvent("Up", self.DieTypeEntryVar, MinValue=1, DieStep=True))
        self.DieTypeEntry.bind("<Down>", lambda event: self.ArrowKeyEvent("Down", self.DieTypeEntryVar, MinValue=1, DieStep=True))
        self.DieTypeEntry.grid(row=0, column=2, rowspan=2, padx=2, pady=2, sticky=NSEW)
        self.DieTypeTooltip = Tooltip(self.DieTypeEntry, "Scroll the mouse wheel, press the up and down keys, or type to change the die type.")

        # Modifier
        self.ModifierLabel = Label(self.DiceEntryAndButtonsFrame, text="+", font=self.DiceEntryFont)
        self.ModifierLabel.grid(row=0, column=3, rowspan=2, sticky=NSEW)
        self.ModifierEntry = EntryExtended(self.DiceEntryAndButtonsFrame, textvariable=self.ModifierEntryVar, justify=CENTER, width=5, bg=GlobalInst.ButtonColor, font=self.DiceEntryFont)
        self.ModifierEntry.ConfigureValidation(lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Modifier must be a whole number."), "key")
        self.ModifierEntry.bind("<Up>", lambda event: self.ArrowKeyEvent("Up", self.ModifierEntryVar))
        self.ModifierEntry.bind("<Down>", lambda event: self.ArrowKeyEvent("Down", self.ModifierEntryVar))
        self.ModifierEntry.grid(row=0, column=4, rowspan=2, padx=2, pady=2, sticky=NSEW)
        self.ModifierTooltip = Tooltip(self.ModifierEntry, "Scroll the mouse wheel, press the up and down keys, or type to change the modifier.")

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
        self.RollButton = ButtonExtended(self.DiceEntryAndButtonsFrame, text="Roll", command=self.Roll, width=7, bg=GlobalInst.ButtonColor, font=self.RollButtonFont)
        self.RollButton.grid(row=0, column=5, padx=2, pady=2, sticky=NSEW, rowspan=2)

        # Average Roll Button
        self.AverageRollButton = ButtonExtended(self.DiceEntryAndButtonsFrame, text="Avg. Roll", command=self.AverageRoll, width=7, bg=GlobalInst.ButtonColor)
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
        self.ResultsField = ScrolledText(self.ResultsFieldFrame, Width=self.ResultsFieldWidth, Height=self.ResultsFieldHeight, Disabled=True, DisabledBackground=GlobalInst.ButtonColor, SavedDataTag="ResultsField", ClearOnNew=True)
        self.ResultsField.grid(row=0, column=0, padx=2, pady=2)
        self.ResultsField.Text.bind("<Button-1>", self.CopyResults)
        self.ResultsField.Text.bind("<Button-3>", self.ClearResults)
        self.ResultsFieldTooltip = Tooltip(self.ResultsField.ScrolledTextFrame, "Left-click to copy results to the clipboard.\n\nRight-click to clear.")

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
        Result = 0
        CritSuccess = False
        CritFailure = False
        IndividualRolls = ""
        DiceNumber = GlobalInst.GetStringVarAsNumber(self.DiceNumberEntryVar)
        DieType = GlobalInst.GetStringVarAsNumber(self.DieTypeEntryVar)
        Modifier = GlobalInst.GetStringVarAsNumber(self.ModifierEntryVar)
        for Roll in range(1, DiceNumber + 1):
            CurrentRollResult = random.randint(1, DieType)
            if Roll < DiceNumber:
                IndividualRolls += str(CurrentRollResult) + "+"
            elif Roll == DiceNumber:
                IndividualRolls += str(CurrentRollResult)
            Result += CurrentRollResult
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
        for CurrentRoll in range(DiceNumber):
            CurrentRollResult = random.randint(1, DieType)
            Result += CurrentRollResult
        Result += Modifier
        return int(Result)

    def AverageRoll(self):
        if self.ValidDiceEntry():
            pass
        else:
            return
        TestRolls = 100000
        Result = 0
        DiceNumber = GlobalInst.GetStringVarAsNumber(self.DiceNumberEntryVar)
        DieType = GlobalInst.GetStringVarAsNumber(self.DieTypeEntryVar)
        Modifier = GlobalInst.GetStringVarAsNumber(self.ModifierEntryVar)
        for Roll in range(TestRolls):
            Result += self.IntRoll(DiceNumber, DieType, Modifier)
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

    def ArrowKeyEvent(self, Direction, EntryVar, MinValue=None, MaxValue=None, DieStep=False):
        try:
            OldValue = GlobalInst.GetStringVarAsNumber(EntryVar)
        except ValueError:
            OldValue = 0
        if Direction == "Up":
            ValueDelta = 1
        elif Direction == "Down":
            ValueDelta = -1
        else:
            ValueDelta = 0
        NewValue = OldValue + ValueDelta
        if MinValue != None:
            NewValue = max(MinValue, NewValue)
        if MaxValue != None:
            NewValue = min(MaxValue, NewValue)
        if DieStep:
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
        self.ResultsField.SetToDefault()

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
            self.PresetRollsScrolledCanvas = ScrolledCanvas(self.PresetRollsFrame, Height=self.PresetRollsScrolledCanvasHeight, Width=self.PresetRollsScrolledCanvasWidth, NumberOfColumns=8,
                                                            ScrollingDisabledVar=self.ScrollingDisabledVar)

            # Scrolled Canvas Headers
            self.PresetRollsScrolledCanvasNameHeader = Label(self.PresetRollsScrolledCanvas.HeaderFrame, text="Name", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.PresetRollsScrolledCanvasNameHeader.grid(row=0, column=0, sticky=NSEW)
            self.PresetRollsScrolledCanvasNameHeader.bind("<Button-1>", lambda event: self.Sort("Name"))
            self.PresetRollsScrolledCanvasNameHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Name", SearchMode=True))
            self.PresetRollsScrolledCanvasNameHeader.bind("<Button-3>", lambda event: self.Sort("Name", Reverse=True))
            self.PresetRollsScrolledCanvasNameTooltip = Tooltip(self.PresetRollsScrolledCanvasNameHeader, GlobalInst.SortTooltipString)
            self.PresetRollsScrolledCanvasRollHeader = Label(self.PresetRollsScrolledCanvas.HeaderFrame, text="Roll", bd=2, relief=GROOVE)
            self.PresetRollsScrolledCanvasRollHeader.grid(row=0, column=1, sticky=NSEW, columnspan=6)
            self.PresetRollsScrolledCanvasSortOrderHeader = Label(self.PresetRollsScrolledCanvas.HeaderFrame, text="Sort\nOrder", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
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
                CurrentEntry = self.PresetRollEntry(self.PresetRollsScrolledCanvas.WindowFrame, self.PresetRollsScrolledCanvas, self.PresetRollsList, self.ScrollingDisabledVar, self.SortOrderValuesList, self.DiceRollerFields,
                                                    CurrentIndex)
                for WidgetToBind in CurrentEntry.WidgetsList:
                    WidgetToBind.bind("<FocusIn>", self.PresetRollsScrolledCanvas.MakeFocusVisible)
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
            UpdatedList = []
            for CurrentIndex in range(len(SortedList)):
                SortedList[CurrentIndex][0].Display(CurrentIndex + 1)
                UpdatedList.append(SortedList[CurrentIndex][0])
                SortedList[CurrentIndex][0].List = UpdatedList
            self.PresetRollsList = UpdatedList

            # Flag Save Prompt
            SavingAndOpeningInst.SavePrompt = True

            # Update Window Title
            WindowInst.UpdateWindowTitle()

        class PresetRollEntry:
            def __init__(self, master, Canvas, List, ScrollingDisabledVar, SortOrderValuesList, DiceRollerFields, Row):
                # Store Parameters
                self.master = master
                self.ScrollingDisabledVar = ScrollingDisabledVar
                self.SortOrderValuesList = SortOrderValuesList
                self.DiceRollerFields = DiceRollerFields
                self.Row = Row
                self.List = List
                self.Canvas = Canvas

                # Variables
                self.PresetRollNameEntryVar = StringVarExtended(ClearOnNew=True)
                self.PresetRollDiceNumberEntryVar = StringVarExtended(ClearOnNew=True)
                self.PresetRollDieTypeEntryVar = StringVarExtended(ClearOnNew=True)
                self.PresetRollModifierEntryVar = StringVarExtended(ClearOnNew=True)
                self.PresetRollSortOrderVar = StringVarExtended(ClearOnNew=True)

                # Sort Fields
                self.SortFields = {}
                self.SortFields["Name"] = self.PresetRollNameEntryVar
                self.SortFields["Sort Order"] = self.PresetRollSortOrderVar

                # Add to List
                self.List.append(self)

                # Name
                self.PresetRollNameEntry = EntryExtended(master, justify=CENTER, width=33, textvariable=self.PresetRollNameEntryVar, bg=GlobalInst.ButtonColor)
                self.PresetRollNameEntry.bind("<Control-Up>", lambda event: self.MoveInList(-1))
                self.PresetRollNameEntry.bind("<Control-Down>", lambda event: self.MoveInList(1))
                self.PresetRollNameEntryTooltip = Tooltip(self.PresetRollNameEntry, "Ctrl+up or ctrl+down to change position in list.")

                # Roll Button
                self.PresetRollButton = ButtonExtended(master, text="Roll:", command=self.RollPreset, bg=GlobalInst.ButtonColor)

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
                    self.PresetRollModifierEntryStatModifierInst = StatModifier(self.PresetRollModifierEntry, "<Button-3>", "Right-click or enter to set a stat modifier.", "Preset Roll", Cursor="xterm", DiceRollerMode=True)

                # Sort Order
                self.PresetRollSortOrder = DropdownExtended(master, textvariable=self.PresetRollSortOrderVar, values=self.SortOrderValuesList, width=5, state="readonly", justify=CENTER)
                self.PresetRollSortOrder.bind("<Enter>", self.DisableScrolling)
                self.PresetRollSortOrder.bind("<Leave>", self.EnableScrolling)

                # List of Widgets
                self.WidgetsList = [self.PresetRollNameEntry, self.PresetRollButton, self.PresetRollDiceNumberEntry, self.PresetRollDieTypeLabel, self.PresetRollDieTypeEntry, self.PresetRollModifierButton,
                                    self.PresetRollModifierEntry]

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
                self.LiftWidgets()

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

            def SetToDefault(self):
                self.PresetRollNameEntryVar.SetToDefault()
                self.PresetRollDiceNumberEntryVar.SetToDefault()
                self.PresetRollDieTypeEntryVar.SetToDefault()
                self.PresetRollModifierEntryVar.SetToDefault()
                self.PresetRollSortOrderVar.SetToDefault()
                if WindowInst.Mode in ["CharacterSheet", "NPCSheet"]:
                    self.PresetRollModifierEntryStatModifierInst.SetToDefault()

            def DisableScrolling(self, event):
                self.ScrollingDisabledVar.set(True)

            def EnableScrolling(self, event):
                self.ScrollingDisabledVar.set(False)

            def MoveInList(self, Delta=0):
                # Row Variables
                LastValidRow = len(self.List)
                CurrentRow = self.Row
                SwapRow = max(1, min(CurrentRow + Delta, LastValidRow))

                # Handle Invalid Swap
                if CurrentRow == SwapRow or Delta == 0:
                    return

                # Swap Rows
                CurrentEntryIndex = CurrentRow - 1
                SwapEntryIndex = SwapRow - 1
                SwapEntry = self.List[SwapEntryIndex]
                SwapEntry.Display(CurrentRow)
                self.Display(SwapRow)
                self.List[SwapEntryIndex] = self
                self.List[CurrentEntryIndex] = SwapEntry

                # Handle Visibility
                WindowInst.update_idletasks()
                self.Canvas.MakeWidgetVisible(self.PresetRollNameEntry)

                # Update Tab Order
                for CurrentEntry in self.List:
                    CurrentEntry.LiftWidgets()

                # Flag Save Prompt
                SavingAndOpeningInst.SavePrompt = True

                # Update Window Title
                WindowInst.UpdateWindowTitle()

            def LiftWidgets(self):
                self.PresetRollNameEntry.lift()
                self.PresetRollButton.lift()
                self.PresetRollDiceNumberEntry.lift()
                self.PresetRollDieTypeLabel.lift()
                self.PresetRollDieTypeEntry.lift()
                self.PresetRollModifierButton.lift()
                self.PresetRollModifierEntry.lift()
                self.PresetRollSortOrder.lift()


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


class TableRoller:
    def __init__(self, master):
        # Variables
        self.TablesDescriptionEntryVar = StringVarExtended("TablesDescriptionEntryVar", ClearOnNew=True)

        # Table Roller Frame
        self.TableRollerFrame = Frame(master)
        self.TableRollerFrame.grid(row=0, column=0, sticky=NSEW)

        # Tables Description
        self.TablesDescriptionFrame = LabelFrame(self.TableRollerFrame, text="Description of Tables:")
        self.TablesDescriptionFrame.grid_columnconfigure(0, weight=1)
        self.TablesDescriptionFrame.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
        self.TablesDescriptionEntry = EntryExtended(self.TablesDescriptionFrame, textvariable=self.TablesDescriptionEntryVar, justify=CENTER)
        self.TablesDescriptionEntry.grid(row=0, column=0, sticky=NSEW)

        # Results Field
        self.ResultsFieldFrame = LabelFrame(self.TableRollerFrame, text="Results:")
        self.ResultsFieldFrame.grid_columnconfigure(0, weight=1)
        self.ResultsFieldFrame.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
        self.ResultsField = ScrolledText(self.ResultsFieldFrame, Disabled=True, DisabledBackground=GlobalInst.ButtonColor, SavedDataTag="TableRollerResultsField", ClearOnNew=True, Height=200)
        self.ResultsField.grid(row=0, column=0, sticky=NSEW)
        self.ResultsField.Text.bind("<Button-1>", self.CopyResults)
        self.ResultsField.Text.bind("<Button-3>", self.ClearResults)
        self.ResultsFieldTooltip = Tooltip(self.ResultsField.ScrolledTextFrame, "Left-click to copy results to the clipboard.\n\nRight-click to clear.")

        # Roll Table Button
        self.RollTableButtonFont = font.Font(size=16)
        self.RollCurrentTableButton = ButtonExtended(self.TableRollerFrame, text="Roll Current Table", bg=GlobalInst.ButtonColor, font=self.RollTableButtonFont, command=self.Roll)
        self.RollCurrentTableButton.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)
        WindowInst.bind("<Control-r>", lambda event: self.Roll())
        self.RollCurrentTableButtonTooltip = Tooltip(self.RollCurrentTableButton, "Keyboard Shortcut:  Ctrl+R")

        # Tables Frame
        self.TablesFrame = LabelFrame(self.TableRollerFrame, text="Tables:")
        self.TablesFrame.grid(row=3, column=0, sticky=NSEW, padx=2, pady=2)

        # Tables Notebook
        self.TablesNotebook = ttk.Notebook(self.TablesFrame, height=423, width=475)
        self.TablesNotebook.grid(row=0, column=0)
        self.TablesNotebook.enable_traversal()

        # List of Roll Tables
        self.ListOfRollTables = []

        # Tables Notebook Pages
        for CurrentIndex in range(1, 11):
            self.RollTable(self.TablesNotebook, str(CurrentIndex), self.ListOfRollTables)

    def Roll(self):
        try:
            CurrentTable = self.ListOfRollTables[self.TablesNotebook.index(self.TablesNotebook.select())]
            UpdateText = CurrentTable.GetTableName() + " Result:\n" + CurrentTable.GetResultString()
        except RecursionError:
            UpdateText = "Recursive table error!"
        TableRollerInst.UpdateResultsField(UpdateText)

    def UpdateResultsField(self, UpdateText):
        CurrentText = self.ResultsField.get()
        if CurrentText != "":
            UpdateText += ("\n") * 2
        NewText = UpdateText + CurrentText
        self.ResultsField.set(NewText)

    def CopyResults(self, event):
        self.ResultsField.Text.clipboard_clear()
        self.ResultsField.Text.clipboard_append(self.ResultsField.get())
        StatusBarInst.FlashStatus("Results copied to clipboard.")

    def ClearResults(self, event):
        # Confirm
        ClearConfirm = messagebox.askyesno("Clear Results", "Are you sure you want to clear the table roll results?  This cannot be undone.")
        if not ClearConfirm:
            return

        # Clear
        self.ResultsField.SetToDefault()

    class RollTable:
        def __init__(self, master, TableIndex, ListOfRollTables):
            # Store Parameters
            self.master = master
            self.TableIndex = TableIndex
            self.ListOfRollTables = ListOfRollTables

            # Variables
            self.TableNameEntryVar = StringVarExtended("Table" + self.TableIndex + "TableNameEntryVar", ClearOnNew=True)
            self.ScrollingDisabledVar = BooleanVar()

            # Append to List
            self.ListOfRollTables.append(self)

            # Roll Table Frame
            self.RollTableFrame = Frame(self.master)
            self.master.add(self.RollTableFrame, text="Table " + self.TableIndex)

            # Table Name
            self.TableNameFrame = LabelFrame(self.RollTableFrame, text="Table Name:")
            self.TableNameFrame.grid_columnconfigure(0, weight=1)
            self.TableNameFrame.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
            self.TableNameEntry = EntryExtended(self.TableNameFrame, textvariable=self.TableNameEntryVar, justify=CENTER)
            self.TableNameEntry.grid(row=0, column=0, sticky=NSEW)

            # Scrolled Canvas
            self.RollTableEntriesScrolledCanvasFrame = Frame(self.RollTableFrame)
            self.RollTableEntriesScrolledCanvasFrame.grid(row=1, column=0, sticky=NSEW)
            self.RollTableEntriesScrolledCanvas = ScrolledCanvas(self.RollTableEntriesScrolledCanvasFrame, NumberOfColumns=3, ScrollingDisabledVar=self.ScrollingDisabledVar, Width=454, Height=345)

            # Scrolled Canvas Headers
            self.RollTableEntriesScrolledCanvasWeightHeader = Label(self.RollTableEntriesScrolledCanvas.HeaderFrame, text="Weight", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.RollTableEntriesScrolledCanvasWeightHeader.grid(row=0, column=0, sticky=NSEW)
            self.RollTableEntriesScrolledCanvasWeightHeader.bind("<Button-1>", lambda event: self.Sort("Weight"))
            self.RollTableEntriesScrolledCanvasWeightHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Weight", SearchMode=True))
            self.RollTableEntriesScrolledCanvasWeightHeader.bind("<Button-3>", lambda event: self.Sort("Weight", Reverse=True))
            self.RollTableEntriesScrolledCanvasWeightTooltip = Tooltip(self.RollTableEntriesScrolledCanvasWeightHeader, GlobalInst.SortTooltipString)
            self.RollTableEntriesScrolledCanvasResultHeader = Label(self.RollTableEntriesScrolledCanvas.HeaderFrame, text="Result", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.RollTableEntriesScrolledCanvasResultHeader.grid(row=0, column=1, sticky=NSEW)
            self.RollTableEntriesScrolledCanvasResultHeader.bind("<Button-1>", lambda event: self.Sort("Result"))
            self.RollTableEntriesScrolledCanvasResultHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Result", SearchMode=True))
            self.RollTableEntriesScrolledCanvasResultHeader.bind("<Button-3>", lambda event: self.Sort("Result", Reverse=True))
            self.RollTableEntriesScrolledCanvasResultTooltip = Tooltip(self.RollTableEntriesScrolledCanvasWeightHeader, GlobalInst.SortTooltipString)
            self.RollTableEntriesScrolledCanvasSortOrderHeader = Label(self.RollTableEntriesScrolledCanvas.HeaderFrame, text="Sort\nOrder", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
            self.RollTableEntriesScrolledCanvasSortOrderHeader.grid(row=0, column=2, sticky=NSEW)
            self.RollTableEntriesScrolledCanvasSortOrderHeader.bind("<Button-1>", lambda event: self.Sort("Sort Order"))
            self.RollTableEntriesScrolledCanvasSortOrderHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Sort Order", SearchMode=True))
            self.RollTableEntriesScrolledCanvasSortOrderHeader.bind("<Button-3>", lambda event: self.Sort("Sort Order", Reverse=True))
            self.RollTableEntriesScrolledCanvasSortOrderTooltip = Tooltip(self.RollTableEntriesScrolledCanvasWeightHeader, GlobalInst.SortTooltipString)

            # Roll Table Entries List
            self.RollTableEntriesList = []

            # Roll Table Entries Count
            self.RollTableEntriesCount = 100

            # Sort Order Values
            self.SortOrderValuesList = [""]
            for CurrentIndex in range(1, self.RollTableEntriesCount + 1):
                self.SortOrderValuesList.append(str(CurrentIndex))

            # Roll Table Entries
            for CurrentIndex in range(1, self.RollTableEntriesCount + 1):
                CurrentEntry = self.RollTableEntry(self.RollTableEntriesScrolledCanvas.WindowFrame, self.RollTableEntriesScrolledCanvas, self.RollTableEntriesList, self.ScrollingDisabledVar, self.SortOrderValuesList,
                                                   self.TableIndex, CurrentIndex)
                for WidgetToBind in CurrentEntry.WidgetsList:
                    WidgetToBind.bind("<FocusIn>", self.RollTableEntriesScrolledCanvas.MakeFocusVisible)
                CurrentEntry.Display(CurrentIndex)

        def GetResultString(self):
            # Compile List of Weights Paired with Results
            ListOfWeightsAndResults = []
            for Entry in self.RollTableEntriesList:
                ListOfWeightsAndResults.append((GlobalInst.GetStringVarAsNumber(Entry.RollTableEntryWeightEntryVar), Entry.RollTableEntryResultEntryVar.get()))

            # Sum Weights
            SumOfWeights = sum(WeightAndResult[0] for WeightAndResult in ListOfWeightsAndResults)

            # Define Result String
            if SumOfWeights <= 0:
                ResultString = "No weights defined!"
            else:
                RolledValue = random.randint(1, SumOfWeights)
                ResultString = ""
                for Weight, Result in ListOfWeightsAndResults:
                    RolledValue -= Weight
                    if RolledValue <= 0:
                        ResultString = Result
                        break

            # Handle White Space Result String
            if ResultString.rstrip() == "":
                ResultString = "Undefined result!"

            # Handle Subtable Result
            if ResultString.startswith(("{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}", "{8}", "{9}", "{10}")):
                ResultTableIndex = int(ResultString.split("}")[0].strip("{")) - 1
                ResultString = self.ListOfRollTables[ResultTableIndex].GetResultString() + " [From " + self.ListOfRollTables[ResultTableIndex].GetTableName() + "]"

            # Return Final Result
            return ResultString

        def Sort(self, Column, Reverse=False, SearchMode=False):
            # List to Sort
            ListToSort = []

            if SearchMode:
                SearchStringPrompt = StringPrompt(WindowInst, "Search", "What do you want to search for?")
                WindowInst.wait_window(SearchStringPrompt.Window)
                if SearchStringPrompt.DataSubmitted.get():
                    SearchString = SearchStringPrompt.StringEntryVar.get()
                else:
                    return

                # Add Fields to List
                for CurrentEntry in self.RollTableEntriesList:
                    ListToSort.append((CurrentEntry, CurrentEntry.SortFields[Column].get().lower()))

                # Sort the List
                SortedList = sorted(ListToSort, key=lambda x: (x[1] == "", SearchString not in x[1]))
            else:
                if Column == "Weight":
                    # Add Fields to List
                    for CurrentEntry in self.RollTableEntriesList:
                        ListToSort.append((CurrentEntry, GlobalInst.GetStringVarAsNumber(CurrentEntry.SortFields[Column])))

                    # Sort the List
                    SortedList = sorted(ListToSort, key=lambda x: ((not Reverse and x[1] == 0) or (Reverse and x[1] != 0), x[1]), reverse=Reverse)
                elif Column == "Result":
                    # Add Fields to List
                    for CurrentEntry in self.RollTableEntriesList:
                        ListToSort.append((CurrentEntry, CurrentEntry.SortFields[Column].get()))

                    # Sort the List
                    SortedList = sorted(ListToSort, key=lambda x: ((not Reverse and x[1] == "") or (Reverse and x[1] != ""), x[1].lower()), reverse=Reverse)
                elif Column == "Sort Order":
                    # Add Fields to List
                    for CurrentEntry in self.RollTableEntriesList:
                        ListToSort.append((CurrentEntry, GlobalInst.GetStringVarAsNumber(CurrentEntry.SortFields[Column])))

                    # Sort the List
                    SortedList = sorted(ListToSort, key=lambda x: ((not Reverse and x[1] == 0) or (Reverse and x[1] != 0), x[1]), reverse=Reverse)
                else:
                    return

            # Adjust Entries to New Order
            UpdatedList = []
            for CurrentIndex in range(len(SortedList)):
                SortedList[CurrentIndex][0].Display(CurrentIndex + 1)
                UpdatedList.append(SortedList[CurrentIndex][0])
                SortedList[CurrentIndex][0].List = UpdatedList
            self.RollTableEntriesList = UpdatedList

            # Flag Save Prompt
            SavingAndOpeningInst.SavePrompt = True

            # Update Window Title
            WindowInst.UpdateWindowTitle()

        def GetTableName(self):
            TableName = self.TableNameEntryVar.get()
            return TableName if TableName.rstrip() != "" else "Table " + self.TableIndex

        class RollTableEntry:
            def __init__(self, master, Canvas, List, ScrollingDisabledVar, SortOrderValuesList, TableIndex, Row):
                # Store Parameters
                self.master = master
                self.ScrollingDisabledVar = ScrollingDisabledVar
                self.SortOrderValuesList = SortOrderValuesList
                self.TableIndex = TableIndex
                self.Row = Row
                self.List = List
                self.Canvas = Canvas

                # Variables
                self.RollTableEntryWeightEntryVar = StringVarExtended(ClearOnNew=True)
                self.RollTableEntryResultEntryVar = StringVarExtended(ClearOnNew=True)
                self.RollTableEntrySortOrderVar = StringVarExtended(ClearOnNew=True)

                # Sort Fields
                self.SortFields = {}
                self.SortFields["Weight"] = self.RollTableEntryWeightEntryVar
                self.SortFields["Result"] = self.RollTableEntryResultEntryVar
                self.SortFields["Sort Order"] = self.RollTableEntrySortOrderVar

                # Add to List
                self.List.append(self)

                # Weight
                self.RollTableEntryWeightEntry = EntryExtended(master, justify=CENTER, width=4, textvariable=self.RollTableEntryWeightEntryVar)
                self.RollTableEntryWeightEntry.ConfigureValidation(lambda NewText: GlobalInst.ValidateNumberFromString(NewText, "Weight must be a whole number.", MinValue=0, LessThanMinString="Weight cannot be negative."), "key")

                # Result
                self.RollTableEntryResultEntry = EntryExtended(master, justify=CENTER, width=59, textvariable=self.RollTableEntryResultEntryVar, bg=GlobalInst.ButtonColor)
                self.RollTableEntryResultEntry.bind("<Control-Up>", lambda event: self.MoveInList(-1))
                self.RollTableEntryResultEntry.bind("<Control-Down>", lambda event: self.MoveInList(1))
                self.RollTableEntryResultEntryTooltip = Tooltip(self.RollTableEntryResultEntry, "Ctrl+up or ctrl+down to change position in list.\n\nStart with \"{1}\", \"{2}\", \"{3}\", etc., to roll on the corresponding table.")

                # Sort Order
                self.RollTableEntrySortOrder = DropdownExtended(master, textvariable=self.RollTableEntrySortOrderVar, values=self.SortOrderValuesList, width=5, state="readonly", justify=CENTER)
                self.RollTableEntrySortOrder.bind("<Enter>", self.DisableScrolling)
                self.RollTableEntrySortOrder.bind("<Leave>", self.EnableScrolling)

                # List of Widgets
                self.WidgetsList = [self.RollTableEntryWeightEntry, self.RollTableEntryResultEntry, self.RollTableEntrySortOrder]

            def Display(self, Row):
                self.Row = Row

                # Set Row Size
                self.master.grid_rowconfigure(self.Row, minsize=26)

                # Place in Grid
                self.RollTableEntryWeightEntry.grid(row=self.Row, column=0, sticky=NSEW)
                self.RollTableEntryResultEntry.grid(row=self.Row, column=1, sticky=NSEW)
                self.RollTableEntrySortOrder.grid(row=self.Row, column=2, sticky=NSEW)

                # Update Tab Order
                self.LiftWidgets()

                # Update Tags
                self.RollTableEntryWeightEntryVar.UpdateTag("Table" + self.TableIndex + "RollTableEntryWeightEntry" + str(self.Row))
                self.RollTableEntryResultEntryVar.UpdateTag("Table" + self.TableIndex + "RollTableEntryResultEntry" + str(self.Row))
                self.RollTableEntrySortOrderVar.UpdateTag("Table" + self.TableIndex + "RollTableEntrySortOrder" + str(self.Row))

            def DisableScrolling(self, event):
                self.ScrollingDisabledVar.set(True)

            def EnableScrolling(self, event):
                self.ScrollingDisabledVar.set(False)

            def MoveInList(self, Delta=0):
                # Row Variables
                LastValidRow = len(self.List)
                CurrentRow = self.Row
                SwapRow = max(1, min(CurrentRow + Delta, LastValidRow))

                # Handle Invalid Swap
                if CurrentRow == SwapRow or Delta == 0:
                    return

                # Swap Rows
                CurrentEntryIndex = CurrentRow - 1
                SwapEntryIndex = SwapRow - 1
                SwapEntry = self.List[SwapEntryIndex]
                SwapEntry.Display(CurrentRow)
                self.Display(SwapRow)
                self.List[SwapEntryIndex] = self
                self.List[CurrentEntryIndex] = SwapEntry

                # Handle Visibility
                WindowInst.update_idletasks()
                self.Canvas.MakeWidgetVisible(self.RollTableEntryWeightEntry)

                # Update Tab Order
                for CurrentEntry in self.List:
                    CurrentEntry.LiftWidgets()

                # Flag Save Prompt
                SavingAndOpeningInst.SavePrompt = True

                # Update Window Title
                WindowInst.UpdateWindowTitle()

            def LiftWidgets(self):
                self.RollTableEntryWeightEntry.lift()
                self.RollTableEntryResultEntry.lift()
                self.RollTableEntrySortOrder.lift()


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


class HoardSheet:
    def __init__(self, master):
        # Variables
        self.HoardNameEntryVar = StringVarExtended("HoardNameEntryVar", ClearOnNew=True)
        self.HoardLocationEntryVar = StringVarExtended("HoardLocationEntryVar", ClearOnNew=True)
        self.HoardStorageCostsEntryVar = StringVarExtended("HoardStorageCostsEntryVar", ClearOnNew=True)
        self.CoinsEntryCPVar = StringVarExtended("CoinsEntryCPVar", ClearOnNew=True)
        self.CoinsEntryCPVar.trace_add("write", lambda a, b, c: self.UpdateHoardStats())
        self.CoinsEntrySPVar = StringVarExtended("CoinsEntrySPVar", ClearOnNew=True)
        self.CoinsEntrySPVar.trace_add("write", lambda a, b, c: self.UpdateHoardStats())
        self.CoinsEntryEPVar = StringVarExtended("CoinsEntryEPVar", ClearOnNew=True)
        self.CoinsEntryEPVar.trace_add("write", lambda a, b, c: self.UpdateHoardStats())
        self.CoinsEntryGPVar = StringVarExtended("CoinsEntryGPVar", ClearOnNew=True)
        self.CoinsEntryGPVar.trace_add("write", lambda a, b, c: self.UpdateHoardStats())
        self.CoinsEntryPPVar = StringVarExtended("CoinsEntryPPVar", ClearOnNew=True)
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
        self.GainCoinsButton = ButtonExtended(self.CoinsFrame, text="Gain", bg=GlobalInst.ButtonColor, command=self.GainCoins)
        self.GainCoinsButton.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)
        self.SpendCoinsButton = ButtonExtended(self.CoinsFrame, text="Spend", bg=GlobalInst.ButtonColor, command=self.SpendCoins)
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
        self.HoardNotesField = ScrolledText(self.HoardNotesFrame, SavedDataTag="HoardNotesField", Width=286, ClearOnNew=True)
        self.HoardNotesField.grid(row=0, column=0, sticky=NSEW)

        # Treasure Items
        self.TreasureItemsFrame = LabelFrame(master, text="Treasure Items:")
        self.TreasureItemsFrame.grid(row=1, column=1, sticky=NSEW, padx=2, pady=2, rowspan=3)

        # Treasure Items Scrolled Canvas
        self.TreasureItemsScrolledCanvas = ScrolledCanvas(self.TreasureItemsFrame, Height=288, Width=622, NumberOfColumns=8, ScrollingDisabledVar=self.ScrollingDisabledVar)

        # Treasure Items Headers
        self.TreasureItemsListNameHeader = Label(self.TreasureItemsScrolledCanvas.HeaderFrame, text="Name", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
        self.TreasureItemsListNameHeader.grid(row=0, column=0, sticky=NSEW)
        self.TreasureItemsListNameHeader.bind("<Button-1>", lambda event: self.Sort("Name"))
        self.TreasureItemsListNameHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Name", SearchMode=True))
        self.TreasureItemsListNameHeader.bind("<Button-3>", lambda event: self.Sort("Name", Reverse=True))
        self.TreasureItemsListNameTooltip = Tooltip(self.TreasureItemsListNameHeader, GlobalInst.SortTooltipString)
        self.TreasureItemsListCountHeader = Label(self.TreasureItemsScrolledCanvas.HeaderFrame, text="Count", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
        self.TreasureItemsListCountHeader.grid(row=0, column=1, sticky=NSEW)
        self.TreasureItemsListCountHeader.bind("<Button-1>", lambda event: self.Sort("Count"))
        self.TreasureItemsListCountHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Count", SearchMode=True))
        self.TreasureItemsListCountHeader.bind("<Button-3>", lambda event: self.Sort("Count", Reverse=True))
        self.TreasureItemsListCountTooltip = Tooltip(self.TreasureItemsListCountHeader, GlobalInst.SortTooltipString)
        self.TreasureItemsListUnitWeightHeader = Label(self.TreasureItemsScrolledCanvas.HeaderFrame, text="Unit Weight\n(lbs.)", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
        self.TreasureItemsListUnitWeightHeader.grid(row=0, column=2, sticky=NSEW)
        self.TreasureItemsListUnitWeightHeader.bind("<Button-1>", lambda event: self.Sort("Unit Weight"))
        self.TreasureItemsListUnitWeightHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Unit Weight", SearchMode=True))
        self.TreasureItemsListUnitWeightHeader.bind("<Button-3>", lambda event: self.Sort("Unit Weight", Reverse=True))
        self.TreasureItemsListUnitWeightTooltip = Tooltip(self.TreasureItemsListUnitWeightHeader, GlobalInst.SortTooltipString)
        self.TreasureItemsListUnitValueHeader = Label(self.TreasureItemsScrolledCanvas.HeaderFrame, text="Unit Value", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
        self.TreasureItemsListUnitValueHeader.grid(row=0, column=3, sticky=NSEW)
        self.TreasureItemsListUnitValueHeader.bind("<Button-1>", lambda event: self.Sort("Unit Value"))
        self.TreasureItemsListUnitValueHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Unit Value", SearchMode=True))
        self.TreasureItemsListUnitValueHeader.bind("<Button-3>", lambda event: self.Sort("Unit Value", Reverse=True))
        self.TreasureItemsListUnitValueTooltip = Tooltip(self.TreasureItemsListUnitValueHeader, GlobalInst.SortTooltipString)
        self.TreasureItemsListUnitValueDenominationHeader = Label(self.TreasureItemsScrolledCanvas.HeaderFrame, text="Value\nDenom.", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
        self.TreasureItemsListUnitValueDenominationHeader.grid(row=0, column=4, sticky=NSEW)
        self.TreasureItemsListUnitValueDenominationHeader.bind("<Button-1>", lambda event: self.Sort("Value Denomination"))
        self.TreasureItemsListUnitValueDenominationHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Value Denomination", SearchMode=True))
        self.TreasureItemsListUnitValueDenominationHeader.bind("<Button-3>", lambda event: self.Sort("Value Denomination", Reverse=True))
        self.TreasureItemsListUnitValueDenominationTooltip = Tooltip(self.TreasureItemsListUnitValueDenominationHeader, GlobalInst.SortTooltipString)
        self.TreasureItemsListTotalWeightHeader = Label(self.TreasureItemsScrolledCanvas.HeaderFrame, text="Total Weight\n(lbs.)", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
        self.TreasureItemsListTotalWeightHeader.grid(row=0, column=5, sticky=NSEW)
        self.TreasureItemsListTotalWeightHeader.bind("<Button-1>", lambda event: self.Sort("Total Weight"))
        self.TreasureItemsListTotalWeightHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Total Weight", SearchMode=True))
        self.TreasureItemsListTotalWeightHeader.bind("<Button-3>", lambda event: self.Sort("Total Weight", Reverse=True))
        self.TreasureItemsListTotalWeightTooltip = Tooltip(self.TreasureItemsListTotalWeightHeader, GlobalInst.SortTooltipString)
        self.TreasureItemsListTotalValueHeader = Label(self.TreasureItemsScrolledCanvas.HeaderFrame, text="Total Value\n(gp)", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
        self.TreasureItemsListTotalValueHeader.grid(row=0, column=6, sticky=NSEW)
        self.TreasureItemsListTotalValueHeader.bind("<Button-1>", lambda event: self.Sort("Total Value"))
        self.TreasureItemsListTotalValueHeader.bind("<Shift-Button-1>", lambda event: self.Sort("Total Value", SearchMode=True))
        self.TreasureItemsListTotalValueHeader.bind("<Button-3>", lambda event: self.Sort("Total Value", Reverse=True))
        self.TreasureItemsListTotalValueTooltip = Tooltip(self.TreasureItemsListTotalValueHeader, GlobalInst.SortTooltipString)
        self.TreasureItemsListSortOrderHeader = Label(self.TreasureItemsScrolledCanvas.HeaderFrame, text="Sort\nOrder", bd=2, relief=GROOVE, bg=GlobalInst.ButtonColor)
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
            CurrentEntry = self.TreasureItemEntry(self.TreasureItemsScrolledCanvas.WindowFrame, self.TreasureItemsScrolledCanvas, self.TreasureItemEntriesList, self.ScrollingDisabledVar, self.SortOrderValuesList, CurrentIndex)
            for WidgetToBind in CurrentEntry.WidgetsList:
                WidgetToBind.bind("<FocusIn>", self.TreasureItemsScrolledCanvas.MakeFocusVisible)
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
        UpdatedList = []
        for CurrentIndex in range(len(SortedList)):
            SortedList[CurrentIndex][0].Display(CurrentIndex + 1)
            UpdatedList.append(SortedList[CurrentIndex][0])
            SortedList[CurrentIndex][0].List = UpdatedList
        self.TreasureItemEntriesList = UpdatedList

        # Flag Save Prompt
        SavingAndOpeningInst.SavePrompt = True

        # Update Window Title
        WindowInst.UpdateWindowTitle()

    def OpenCoinCalculator(self):
        # Create Coin Calculator Window and Wait
        self.CoinCalculatorInst = CoinCalculator(WindowInst, DialogMode=True)
        WindowInst.wait_window(self.CoinCalculatorInst.Window)

    class TreasureItemEntry:
        def __init__(self, master, Canvas, List, ScrollingDisabledVar, SortOrderValuesList, Row):
            # Store Parameters
            self.master = master
            self.ScrollingDisabledVar = ScrollingDisabledVar
            self.SortOrderValuesList = SortOrderValuesList
            self.Row = Row
            self.List = List
            self.Canvas = Canvas

            # Variables
            self.NameEntryVar = StringVarExtended(ClearOnNew=True)
            self.CountEntryVar = StringVarExtended(ClearOnNew=True)
            self.CountEntryVar.trace_add("write", lambda a, b, c: HoardSheetInst.UpdateHoardStats())
            self.UnitWeightEntryVar = StringVarExtended(ClearOnNew=True)
            self.UnitWeightEntryVar.trace_add("write", lambda a, b, c: HoardSheetInst.UpdateHoardStats())
            self.UnitValueEntryVar = StringVarExtended(ClearOnNew=True)
            self.UnitValueEntryVar.trace_add("write", lambda a, b, c: HoardSheetInst.UpdateHoardStats())
            self.UnitValueDenominationVar = StringVarExtended(ClearOnNew=True)
            self.UnitValueDenominationVar.trace_add("write", lambda a, b, c: HoardSheetInst.UpdateHoardStats())
            self.TotalWeightEntryVar = StringVar()
            self.TotalValueEntryVar = StringVar()
            self.CategoryEntryVar = StringVarExtended(ClearOnNew=True)
            self.RarityEntryVar = StringVarExtended(ClearOnNew=True)
            self.DescriptionVar = StringVarExtended(ClearOnNew=True)
            self.SortOrderVar = StringVarExtended(ClearOnNew=True)

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
            self.List.append(self)

            # Name Entry
            self.NameEntry = EntryExtended(master, width=35, textvariable=self.NameEntryVar, justify=CENTER, bg=GlobalInst.ButtonColor)
            self.NameEntry.bind("<Button-3>", self.ConfigureItemDescription)
            self.NameEntry.bind("<Return>", self.ConfigureItemDescription)
            self.NameEntry.bind("<Shift-Button-3>", self.ExchangeForCoins)
            self.NameEntry.bind("<Shift-Return>", self.ExchangeForCoins)
            self.NameEntry.bind("<Control-Up>", lambda event: self.MoveInList(-1))
            self.NameEntry.bind("<Control-Down>", lambda event: self.MoveInList(1))
            self.NameTooltip = Tooltip(self.NameEntry, "Right-click or enter to set an item description.\n\nShift+right-click or shift+enter to exchange for coins.\n\nCtrl+up or ctrl+down to change position in list.")

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

            # List of Widgets
            self.WidgetsList = [self.NameEntry, self.CountEntry, self.UnitWeightEntry, self.UnitValueEntry, self.UnitValueDenomination, self.TotalWeightEntry, self.TotalValueEntry, self.SortOrder]

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
            self.LiftWidgets()

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

        def MoveInList(self, Delta=0):
            # Row Variables
            LastValidRow = len(self.List)
            CurrentRow = self.Row
            SwapRow = max(1, min(CurrentRow + Delta, LastValidRow))

            # Handle Invalid Swap
            if CurrentRow == SwapRow or Delta == 0:
                return

            # Swap Rows
            CurrentEntryIndex = CurrentRow - 1
            SwapEntryIndex = SwapRow - 1
            SwapEntry = self.List[SwapEntryIndex]
            SwapEntry.Display(CurrentRow)
            self.Display(SwapRow)
            self.List[SwapEntryIndex] = self
            self.List[CurrentEntryIndex] = SwapEntry

            # Handle Visibility
            WindowInst.update_idletasks()
            self.Canvas.MakeWidgetVisible(self.NameEntry)

            # Update Tab Order
            for CurrentEntry in self.List:
                CurrentEntry.LiftWidgets()

            # Flag Save Prompt
            SavingAndOpeningInst.SavePrompt = True

            # Update Window Title
            WindowInst.UpdateWindowTitle()

        def LiftWidgets(self):
            self.NameEntry.lift()
            self.CountEntry.lift()
            self.UnitWeightEntry.lift()
            self.UnitValueEntry.lift()
            self.UnitValueDenomination.lift()
            self.TotalWeightEntry.lift()
            self.TotalValueEntry.lift()
            self.SortOrder.lift()

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
                self.SubmitButton = ButtonExtended(self.ButtonFrame, text="Submit", command=self.Submit, bg=GlobalInst.ButtonColor)
                self.SubmitButton.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)
                self.CancelButton = ButtonExtended(self.ButtonFrame, text="Cancel", command=self.Cancel, bg=GlobalInst.ButtonColor)
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
