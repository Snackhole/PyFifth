import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from zipfile import ZipFile
import shutil
import winshell
from win32com.client import Dispatch

class Window(Tk):
    def __init__(self):
        # Create Window
        Tk.__init__(self)

        # Variables
        self.InstallLocationEntryVar = StringVar()
        self.DesktopShortcutBoxVar = BooleanVar()
        self.ButtonColor = "#F1F1D4"
        self.ScriptName = os.path.splitext(os.path.basename(__file__))[0]
        self.ProgramZip = "Executables/PyFifth Dev 41.zip"

        # Install Location
        self.InstallLocationScrollbar = Scrollbar(self, orient=HORIZONTAL, command=self.ScrollInstallLocationEntry)
        self.InstallLocationEntry = Entry(self, state=DISABLED, textvariable=self.InstallLocationEntryVar, width=50, disabledbackground="light gray", disabledforeground="black", xscrollcommand=self.InstallLocationScrollbar.set)
        self.InstallLocationEntry.grid(row=0, column=0, sticky=NSEW, padx=2, pady=2)
        self.InstallLocationScrollbar.grid(row=1, column=0, sticky=NSEW)
        self.InstallLocationButton = Button(self, text="Install Location", command=self.SetInstallLocation, bg=self.ButtonColor)
        self.InstallLocationButton.grid(row=0, column=1, rowspan=2, sticky=NSEW, padx=2, pady=2)

        # Desktop Shortcut
        self.DesktopShortcutBox = Checkbutton(self, text="Create desktop shortcut?", variable=self.DesktopShortcutBoxVar)
        self.DesktopShortcutBox.grid(row=2, column=0, sticky=NSEW, padx=2, pady=2)

        # Install Button
        self.InstallButton = Button(self, text="Install", command=self.Install, bg=self.ButtonColor)
        self.InstallButton.grid(row=2, column=1, sticky=NSEW, padx=2, pady=2)

        # Configure Window
        self.wm_title(self.ScriptName)
        self.WindowIcon()
        self.WindowGeometry()
        self.option_add("*Font", "TkDefaultFont")

        # Main Loop
        self.mainloop()

    def SetInstallLocation(self):
        # Determine Install Path
        InstallPath = filedialog.askdirectory()
        if InstallPath != "":
            self.InstallLocationEntryVar.set(InstallPath)

    def Install(self):
        InstallLocation = self.InstallLocationEntryVar.get()

        # No Location
        if InstallLocation == "":
            messagebox.showerror("No Install Location", "Cannot install until a location has been chosen.")
            return

        # Warning
        if not messagebox.askyesno("Install PyFifth to Chosen Location", "WARNING:  All files currently in the chosen location will be deleted and replaced with PyFifth's files.  Proceed?"):
            return
        else:
            pass

        try:
            for File in os.listdir(InstallLocation):
                FilePath = os.path.join(InstallLocation, File)
                if os.path.isfile(FilePath):
                    os.unlink(FilePath)
                elif os.path.isdir(FilePath):
                    shutil.rmtree(FilePath)
            with ZipFile(self.ProgramZip, mode="r") as Program:
                Program.extractall(InstallLocation)
            if self.DesktopShortcutBoxVar.get():
                ShortcutTarget = os.path.join(InstallLocation, "PyFifth.exe")
                Shell = Dispatch("WScript.Shell")
                Shortcut = Shell.CreateShortCut(os.path.join(winshell.desktop(), "PyFifth.lnk"))
                Shortcut.Targetpath = ShortcutTarget
                Shortcut.WorkingDirectory = InstallLocation
                Shortcut.IconLocation = ShortcutTarget
                Shortcut.save()
        except:
            messagebox.showerror("Installation Error", "An error occurred during installation, possibly due to a file permission error.  Please try again.")
            return

        # Installation Complete
        messagebox.showinfo("Installation Complete", "PyFifth has been installed to the chosen location.")
        self.destroy()

    def ScrollInstallLocationEntry(self, *args):
        Operation = args[0]
        Distance = args[1]
        if Operation == "scroll":
            Units = args[2]
            self.InstallLocationEntry.xview_scroll(Distance, Units)
        elif Operation == "moveto":
            self.InstallLocationEntry.xview_moveto(Distance)

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