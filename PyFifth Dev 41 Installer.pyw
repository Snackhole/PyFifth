import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from zipfile import ZipFile

class Window(Tk):
    def __init__(self):
        # Create Window
        Tk.__init__(self)

        # Variables
        self.InstallLocationEntryVar = StringVar()
        self.DesktopShortcutBoxVar = BooleanVar()
        self.ButtonColor = "#F1F1D4"
        self.ScriptName = os.path.splitext(os.path.basename(__file__))[0]

        # Install Location
        self.InstallLocationEntry = Entry(self, state=DISABLED, textvariable=self.InstallLocationEntryVar, width=40, disabledbackground="light gray", disabledforeground="black")
        self.InstallLocationEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
        self.InstallLocationButton = Button(self, text="Install Location", command=self.SetInstallLocation, bg=self.ButtonColor)
        self.InstallLocationButton.grid(row=0, column=1, sticky=NSEW, padx=2, pady=2)

        # Desktop Shortcut
        self.DesktopShortcutBox = Checkbutton(self, text="Create desktop shortcut?", variable=self.DesktopShortcutBoxVar)
        self.DesktopShortcutBox.grid(row=1, column=0, columnspan=2, sticky=NSEW, padx=2, pady=2)

        # Install Button
        self.InstallButton = Button(self, text="Install", command=self.Install, bg=self.ButtonColor)
        self.InstallButton.grid(row=2, column=0, columnspan=2, sticky=NSEW, padx=2, pady=2)

        # Configure Window
        self.wm_title(self.ScriptName)
        self.WindowIcon()
        self.WindowGeometry()
        self.option_add("*Font", "TkDefaultFont")

        # Main Loop
        self.mainloop()

    def SetInstallLocation(self):
        # Determine Install Path
        pass

    def Install(self):
        # Warning
        if not messagebox.askyesno("Install PyFifth to Chosen Location", "WARNING:  All files currently in the chosen location will be deleted and replaced with PyFifth's files.  Proceed?"):
            return
        else:
            pass

        # Installation Complete
        messagebox.showinfo("Installation Complete", "PyFifth has been installed to the chosen location.")
        self.destroy()

    def WindowGeometry(self):
        self.update_idletasks()
        BaseWidth = self.winfo_width()
        BaseHeight = self.winfo_height()
        BorderWidth = self.winfo_rootx() - self.winfo_x()
        WindowWidth = BaseWidth + (2 * BorderWidth)
        TitleHeight = self.winfo_rooty() - self.winfo_y()
        WindowHeight = BaseHeight + TitleHeight + BorderWidth
        XCoordinate = (self.winfo_screenwidth() // 2) - (WindowWidth // 2)
        YCoordinate = (self.winfo_screenheight() // 2) - (WindowHeight // 2)
        self.geometry("{}x{}+{}+{}".format(BaseWidth, BaseHeight, XCoordinate, YCoordinate))
        self.resizable(width=False, height=False)

    def WindowIcon(self):
        try:
            self.iconbitmap("PyFifthIcon.ico")
        except TclError:
            pass

if __name__ == "__main__":
    WindowInst = Window()