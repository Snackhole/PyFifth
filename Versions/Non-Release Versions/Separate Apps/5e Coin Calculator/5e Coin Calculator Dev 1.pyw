from tkinter import *
from decimal import *
from tkinter import messagebox

# Create and Configure Window
root = Tk()
root.wm_title("Coin Calculator")
root.option_add("*Font", "TkDefaultFont")


class CoinCalculator:
    def __init__(self, master):
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

        # Table Frame
        self.TableFrame = Frame(master)
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
        self.CalculateButton = Button(master, text="Calculate", command=self.Calculate, bg=GlobalInst.ButtonColor)
        self.CalculateButton.grid(row=1, column=0, sticky=NSEW, padx=2, pady=2)

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


class Global:
    def __init__(self):
        # Variables
        self.ButtonColor = "#F1F1D4"

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

# Global Functions and Variables
GlobalInst = Global()

# Populate Window
CoinCalculatorInst = CoinCalculator(root)

# Initial Window Behavior
GlobalInst.WindowGeometry(root, False)
root.focus_force()

# Main Loop
root.mainloop()