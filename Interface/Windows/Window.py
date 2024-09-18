import json
import os

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QFrame, QMessageBox


class Window(QMainWindow):
    def __init__(self, ScriptName, AbsoluteDirectoryPath, AppInst):
        super().__init__()

        # Store Parameters
        self.ScriptName = ScriptName
        self.AbsoluteDirectoryPath = AbsoluteDirectoryPath
        self.AppInst = AppInst

        # Window Icon
        self.WindowIcon = QIcon(self.GetResourcePath("Assets/PyFifth Icon.png"))
        self.setWindowIcon(self.WindowIcon)

        # Create Central Frame
        self.Frame = QFrame()

        # Create Interface
        self.CreateInterface()

        # Update Window Title
        self.UpdateWindowTitle()

        # Create Status Bar
        self.StatusBar = self.statusBar()

        # Set Central Frame
        self.setCentralWidget(self.Frame)

        # Show Window
        self.show()
        self.SetGeometryToMinimum()
        self.Center()

    def CreateInterface(self):
        # Load Theme
        self.LoadTheme()

    def UpdateWindowTitle(self):
        self.setWindowTitle(self.ScriptName)

    def DisplayMessageBox(self, Message, Icon=QMessageBox.Information, Buttons=QMessageBox.Ok, Parent=None):
        MessageBox = QMessageBox(self if Parent is None else Parent)
        MessageBox.setWindowIcon(self.WindowIcon)
        MessageBox.setWindowTitle(self.ScriptName)
        MessageBox.setIcon(Icon)
        MessageBox.setText(Message)
        MessageBox.setStandardButtons(Buttons)
        return MessageBox.exec_()

    def FlashStatusBar(self, Status, Duration=2000):
        self.StatusBar.showMessage(Status)
        QTimer.singleShot(Duration, self.StatusBar.clearMessage)

    def GetResourcePath(self, RelativeLocation):
        return os.path.join(self.AbsoluteDirectoryPath, RelativeLocation)

    # Window Management Methods
    def SetGeometryToMinimum(self):
        FrameGeometryRectangle = self.frameGeometry()
        FrameGeometryRectangle.setWidth(self.minimumWidth())
        FrameGeometryRectangle.setHeight(self.minimumHeight())
        self.setGeometry(FrameGeometryRectangle)

    def Center(self):
        FrameGeometryRectangle = self.frameGeometry()
        DesktopCenterPoint = QApplication.primaryScreen().availableGeometry().center()
        FrameGeometryRectangle.moveCenter(DesktopCenterPoint)
        self.move(FrameGeometryRectangle.topLeft())

    def CreateThemes(self):
        self.Themes = {}

        # Light
        self.Themes["Light"] = QPalette()
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Window, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.WindowText, QColor(120, 120, 120, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Base, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.AlternateBase, QColor(247, 247, 247, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.ToolTipBase, QColor(255, 255, 220, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.ToolTipText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.PlaceholderText, QColor(0, 0, 0, 128))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Text, QColor(120, 120, 120, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Button, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.ButtonText, QColor(120, 120, 120, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Light, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Midlight, QColor(247, 247, 247, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Dark, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Mid, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Shadow, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Highlight, QColor(0, 120, 215, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Link, QColor(0, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.LinkVisited, QColor(255, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Window, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.WindowText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Base, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.AlternateBase, QColor(233, 231, 227, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.ToolTipBase, QColor(255, 255, 220, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.ToolTipText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.PlaceholderText, QColor(0, 0, 0, 128))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Text, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Button, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.ButtonText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Light, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Midlight, QColor(227, 227, 227, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Dark, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Mid, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Shadow, QColor(105, 105, 105, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Highlight, QColor(0, 120, 215, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.HighlightedText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Link, QColor(0, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.LinkVisited, QColor(255, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Window, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.WindowText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Base, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.AlternateBase, QColor(233, 231, 227, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.ToolTipBase, QColor(255, 255, 220, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.ToolTipText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.PlaceholderText, QColor(0, 0, 0, 128))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Text, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Button, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.ButtonText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Light, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Midlight, QColor(227, 227, 227, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Dark, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Mid, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Shadow, QColor(105, 105, 105, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Highlight, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.HighlightedText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Link, QColor(0, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.LinkVisited, QColor(255, 0, 255, 255))

        # Dark
        self.Themes["Dark"] = QPalette()
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Window, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.WindowText, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Base, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.AlternateBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.ToolTipBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.ToolTipText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.PlaceholderText, QColor(239, 240, 241, 128))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Text, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Button, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.ButtonText, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Light, QColor(24, 27, 29, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Midlight, QColor(36, 40, 44, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Dark, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Mid, QColor(65, 72, 78, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Shadow, QColor(0, 0, 0, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Highlight, QColor(65, 72, 78, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(36, 40, 44, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Link, QColor(41, 128, 185, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.LinkVisited, QColor(127, 140, 141, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Window, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.WindowText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Base, QColor(35, 38, 41, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.AlternateBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.ToolTipBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.ToolTipText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.PlaceholderText, QColor(239, 240, 241, 128))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Text, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Button, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.ButtonText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Light, QColor(24, 27, 29, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Midlight, QColor(36, 40, 44, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Dark, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Mid, QColor(65, 72, 78, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Shadow, QColor(0, 0, 0, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Highlight, QColor(61, 174, 233, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.HighlightedText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Link, QColor(41, 128, 185, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.LinkVisited, QColor(127, 140, 141, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Window, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.WindowText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Base, QColor(35, 38, 41, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.AlternateBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.ToolTipBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.ToolTipText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.PlaceholderText, QColor(239, 240, 241, 128))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Text, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Button, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.ButtonText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Light, QColor(24, 27, 29, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Midlight, QColor(36, 40, 44, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Dark, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Mid, QColor(65, 72, 78, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Shadow, QColor(0, 0, 0, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Highlight, QColor(61, 174, 233, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.HighlightedText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Link, QColor(41, 128, 185, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.LinkVisited, QColor(127, 140, 141, 255))

    def LoadTheme(self):
        self.CreateThemes()
        ThemeFile = self.GetResourcePath("Configs/Theme.cfg")
        if os.path.isfile(ThemeFile):
            with open(ThemeFile, "r") as ConfigFile:
                self.Theme = json.loads(ConfigFile.read())
        else:
            self.Theme = "Light"
        self.AppInst.setStyle("Fusion")
        self.AppInst.setPalette(self.Themes[self.Theme])
