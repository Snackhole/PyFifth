import json
import os

from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QIcon, QPalette, QColor
from PyQt6.QtWidgets import QMainWindow, QApplication, QFrame, QMessageBox


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

    def DisplayMessageBox(self, Message, Icon=QMessageBox.Icon.Information, Buttons=QMessageBox.StandardButton.Ok, Parent=None):
        MessageBox = QMessageBox(self if Parent is None else Parent)
        MessageBox.setWindowIcon(self.WindowIcon)
        MessageBox.setWindowTitle(self.ScriptName)
        MessageBox.setIcon(Icon)
        MessageBox.setText(Message)
        MessageBox.setStandardButtons(Buttons)
        return MessageBox.exec()

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
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(120, 120, 120, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.AlternateBase, QColor(247, 247, 247, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, QColor(0, 0, 0, 128))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(120, 120, 120, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(120, 120, 120, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Light, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Midlight, QColor(247, 247, 247, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Mid, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Shadow, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Highlight, QColor(0, 120, 215, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.HighlightedText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Link, QColor(0, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.LinkVisited, QColor(255, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.AlternateBase, QColor(233, 231, 227, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, QColor(0, 0, 0, 128))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Light, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Midlight, QColor(227, 227, 227, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Mid, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Shadow, QColor(105, 105, 105, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight, QColor(0, 120, 215, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.HighlightedText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Link, QColor(0, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.LinkVisited, QColor(255, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.AlternateBase, QColor(233, 231, 227, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, QColor(0, 0, 0, 128))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Light, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Midlight, QColor(227, 227, 227, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Mid, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Shadow, QColor(105, 105, 105, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Highlight, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.HighlightedText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Link, QColor(0, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.LinkVisited, QColor(255, 0, 255, 255))

        # Dark
        self.Themes["Dark"] = QPalette()
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.AlternateBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, QColor(239, 240, 241, 128))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Light, QColor(24, 27, 29, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Midlight, QColor(36, 40, 44, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Mid, QColor(65, 72, 78, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Shadow, QColor(0, 0, 0, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Highlight, QColor(65, 72, 78, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.HighlightedText, QColor(36, 40, 44, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Link, QColor(41, 128, 185, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.LinkVisited, QColor(127, 140, 141, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, QColor(35, 38, 41, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.AlternateBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, QColor(239, 240, 241, 128))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Light, QColor(24, 27, 29, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Midlight, QColor(36, 40, 44, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Mid, QColor(65, 72, 78, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Shadow, QColor(0, 0, 0, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight, QColor(61, 174, 233, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.HighlightedText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Link, QColor(41, 128, 185, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.LinkVisited, QColor(127, 140, 141, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, QColor(35, 38, 41, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.AlternateBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, QColor(239, 240, 241, 128))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Light, QColor(24, 27, 29, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Midlight, QColor(36, 40, 44, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Mid, QColor(65, 72, 78, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Shadow, QColor(0, 0, 0, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Highlight, QColor(61, 174, 233, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.HighlightedText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Link, QColor(41, 128, 185, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.LinkVisited, QColor(127, 140, 141, 255))

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
