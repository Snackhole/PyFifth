from PyQt5 import QtCore

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QFrame, QGridLayout, QLabel, QMessageBox, QScrollArea

from Interface.Widgets.IconButtons import AddButton, CopyButton, DeleteButton


class PlayerCharacterPortraitWidget(QFrame):
    def __init__(self, CharacterWindow):
        # Initialize Frame
        super().__init__()

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Variables
        self.ExportFilters = {}
        self.ExportFilters[".jpeg"] = "JPEG (*.jpeg)"
        self.ExportFilters[".jpg"] = "JPG (*.jpg)"
        self.ExportFilters[".png"] = "PNG (*.png)"
        self.ExportFilters[".gif"] = "GIF (*.gif)"
        self.ExportFilters[".bmp"] = "BMP (*.bmp)"

        # Create Portrait Display
        self.CreatePortraitDisplay()

        # Create Buttons
        self.CreateButtons()

        # Create and Set Layout
        self.CreateAndSetLayout()

    def CreatePortraitDisplay(self):
        self.PortraitDisplay = QLabel()
        self.PortraitDisplayScrollArea = QScrollArea()
        self.PortraitDisplayScrollArea.setWidget(self.PortraitDisplay)
        self.PortraitDisplayScrollArea.setAlignment(QtCore.Qt.AlignCenter)

    def CreateButtons(self):
        self.AddButton = AddButton(self.AddPortrait, "Add Portrait")
        self.ExportButton = CopyButton(self.ExportPortrait, "Export Portrait")
        self.ClearButton = DeleteButton(self.ClearPortrait, "Clear Portrait")

    def CreateAndSetLayout(self):
        # Create Layout
        self.Layout = QGridLayout()

        self.Layout.addWidget(self.PortraitDisplayScrollArea, 0, 0, 1, 3)
        self.Layout.addWidget(self.AddButton, 1, 0)
        self.Layout.addWidget(self.ExportButton, 1, 1)
        self.Layout.addWidget(self.ClearButton, 1, 2)

        # Set Layout
        self.setLayout(self.Layout)

    def UpdateDisplay(self):
        if not self.CharacterWindow.PlayerCharacter.Stats["Portrait Enabled"]:
            self.PortraitDisplay.clear()
            self.PortraitDisplay.resize(QtCore.QSize(0, 0))
            return
        PortraitBinary = self.CharacterWindow.PlayerCharacter.GetPortraitBinary()
        if PortraitBinary is not None:
            PortraitPixmap = QPixmap()
            PortraitPixmap.loadFromData(PortraitBinary)
            self.PortraitDisplay.setPixmap(PortraitPixmap)
            self.PortraitDisplay.resize(self.PortraitDisplay.pixmap().size())
        else:
            self.PortraitDisplay.clear()
            self.PortraitDisplay.resize(QtCore.QSize(0, 0))

    def AddPortrait(self):
        if self.CharacterWindow.PlayerCharacter.Stats["Portrait"] is not None:
            if self.CharacterWindow.DisplayMessageBox("Are you sure you want to replace the current portrait?  This cannot be undone.", Icon=QMessageBox.Warning, Buttons=(QMessageBox.Yes | QMessageBox.No), Parent=self) == QMessageBox.No:
                return
        ImageFilePath = QFileDialog.getOpenFileName(parent=self, caption="Add Portrait", filter="Images (*.jpg *.jpeg *.png *.gif *.bmp)")[0]
        if ImageFilePath != "":
            self.CharacterWindow.PlayerCharacter.SetPortrait(ImageFilePath)
            self.CharacterWindow.UpdateUnsavedChangesFlag(True)

    def ExportPortrait(self):
        FileExtension = self.CharacterWindow.PlayerCharacter.Stats["Portrait File Extension"]
        ExportFilePath = QFileDialog.getSaveFileName(parent=self, caption="Export Portrait", filter=self.ExportFilters[FileExtension])[0]
        if ExportFilePath != "":
            if not ExportFilePath.endswith(FileExtension):
                ExportFilePath += FileExtension
            self.CharacterWindow.PlayerCharacter.ExportPortrait(ExportFilePath)

    def ClearPortrait(self):
        if self.CharacterWindow.DisplayMessageBox("Are you sure you want to clear the portrait?  This cannot be undone.", Icon=QMessageBox.Warning, Buttons=(QMessageBox.Yes | QMessageBox.No), Parent=self) == QMessageBox.Yes:
            self.CharacterWindow.PlayerCharacter.DeletePortrait()
            self.CharacterWindow.UpdateUnsavedChangesFlag(True)
