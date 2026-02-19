import copy
import json
import os

from PyQt6 import QtCore
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QDoubleSpinBox, QFrame, QGridLayout, QLabel, QMessageBox, QSizePolicy, QSpinBox

from Core.Hoard import Hoard
from Interface.Dialogs.CoinCalculatorDialog import CoinCalculatorDialog
from Interface.Dialogs.GainCoinsDialog import GainCoinsDialog
from Interface.Dialogs.HoardEditItemDialog import HoardEditItemDialog
from Interface.Dialogs.SpendCoinsDialog import SpendCoinsDialog
from Interface.Widgets.CenteredLineEdit import CenteredLineEdit
from Interface.Widgets.HoardInventoryTreeWidget import HoardInventoryTreeWidget
from Interface.Widgets.IconButtons import AddButton, DeleteButton, EditButton, MoveDownButton, MoveUpButton
from Interface.Widgets.IndentingTextEdit import IndentingTextEdit
from Interface.Windows.Window import Window
from SaveAndLoad.SaveAndOpenMixin import SaveAndOpenMixin


class HoardSheetWindow(Window, SaveAndOpenMixin):
    # Initialization Methods
    def __init__(self, ScriptName, AbsoluteDirectoryPath, AppInst):
        # Store Parameters
        self.ScriptName = ScriptName
        self.AbsoluteDirectoryPath = AbsoluteDirectoryPath
        self.AppInst = AppInst

        # Variables
        self.UpdatingFieldsFromHoard = False

        # Styles
        self.SectionLabelStyle = "QLabel {font-size: 10pt; font-weight: bold;}"

        # Header Label Margin
        self.HeaderLabelMargin = 5

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        # Initialize Window
        super().__init__(ScriptName, AbsoluteDirectoryPath, AppInst)

        # Set Up Save and Open
        self.SetUpSaveAndOpen(".pyfifthhoard", "PyFifth Hoard Sheet", (Hoard,))

        # Create Hoard
        self.Hoard = Hoard()

        # Derived Data
        self.DerivedData = self.Hoard.GetDerivedData()

        # Load Configs
        self.LoadConfigs()

        # Update Display
        self.UpdateDisplay()

    def CreateInterface(self):
        super().LoadTheme()

        # Header
        self.NameOrOwnersLabel = QLabel("Name or Owners:")
        self.NameOrOwnersLineEdit = CenteredLineEdit()
        self.NameOrOwnersLineEdit.textChanged.connect(lambda: self.UpdateData("Name or Owners", self.NameOrOwnersLineEdit.text()))

        self.LocationLabel = QLabel("Location:")
        self.LocationLineEdit = CenteredLineEdit()
        self.LocationLineEdit.textChanged.connect(lambda: self.UpdateData("Location", self.LocationLineEdit.text()))

        self.StorageCostsLabel = QLabel("Storage Costs:")
        self.StorageCostsLineEdit = CenteredLineEdit()
        self.StorageCostsLineEdit.textChanged.connect(lambda: self.UpdateData("Storage Costs", self.StorageCostsLineEdit.text()))

        # Coins
        self.CoinsLabel = QLabel("Coins")
        self.CoinsLabel.setStyleSheet(self.SectionLabelStyle)
        self.CoinsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CoinsLabel.setMargin(self.HeaderLabelMargin)

        # CP
        self.CPLabel = QLabel("CP")
        self.CPLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CPLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.CPLabel.setMargin(5)
        self.CPSpinBox = QSpinBox()
        self.CPSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CPSpinBox.setButtonSymbols(self.CPSpinBox.ButtonSymbols.NoButtons)
        self.CPSpinBox.setRange(0, 1000000000)
        self.CPSpinBox.valueChanged.connect(lambda: self.UpdateData(("Coins", "CP"), self.CPSpinBox.value()))

        # SP
        self.SPLabel = QLabel("SP")
        self.SPLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SPLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.SPLabel.setMargin(5)
        self.SPSpinBox = QSpinBox()
        self.SPSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SPSpinBox.setButtonSymbols(self.SPSpinBox.ButtonSymbols.NoButtons)
        self.SPSpinBox.setRange(0, 1000000000)
        self.SPSpinBox.valueChanged.connect(lambda: self.UpdateData(("Coins", "SP"), self.SPSpinBox.value()))

        # EP
        self.EPLabel = QLabel("EP")
        self.EPLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.EPLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.EPLabel.setMargin(5)
        self.EPSpinBox = QSpinBox()
        self.EPSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.EPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.EPSpinBox.setButtonSymbols(self.EPSpinBox.ButtonSymbols.NoButtons)
        self.EPSpinBox.setRange(0, 1000000000)
        self.EPSpinBox.valueChanged.connect(lambda: self.UpdateData(("Coins", "EP"), self.EPSpinBox.value()))

        # GP
        self.GPLabel = QLabel("GP")
        self.GPLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.GPLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.GPLabel.setMargin(5)
        self.GPSpinBox = QSpinBox()
        self.GPSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.GPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.GPSpinBox.setButtonSymbols(self.GPSpinBox.ButtonSymbols.NoButtons)
        self.GPSpinBox.setRange(0, 1000000000)
        self.GPSpinBox.valueChanged.connect(lambda: self.UpdateData(("Coins", "GP"), self.GPSpinBox.value()))

        # PP
        self.PPLabel = QLabel("PP")
        self.PPLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.PPLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.PPLabel.setMargin(5)
        self.PPSpinBox = QSpinBox()
        self.PPSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.PPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.PPSpinBox.setButtonSymbols(self.PPSpinBox.ButtonSymbols.NoButtons)
        self.PPSpinBox.setRange(0, 1000000000)
        self.PPSpinBox.valueChanged.connect(lambda: self.UpdateData(("Coins", "PP"), self.PPSpinBox.value()))

        # Coins Buttons
        self.GainCoinsButton = AddButton(self.GainCoins, "Gain Coins")
        self.SpendCoinsButton = DeleteButton(self.SpendCoins, "Spend Coins")

        # Hoard Stats
        self.HoardStatsLabel = QLabel("Hoard Stats")
        self.HoardStatsLabel.setStyleSheet(self.SectionLabelStyle)
        self.HoardStatsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.HoardStatsLabel.setMargin(self.HeaderLabelMargin)

        self.ValueColumnLabel = QLabel("Value")
        self.ValueColumnLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ValueColumnLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.ValueColumnLabel.setMargin(5)

        self.LoadColumnLabel = QLabel("Load (lbs.)")
        self.LoadColumnLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.LoadColumnLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.LoadColumnLabel.setMargin(5)

        self.CoinsRowLabel = QLabel("Coins")
        self.CoinsRowLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CoinsRowLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.CoinsRowLabel.setMargin(5)

        self.ItemsRowLabel = QLabel("Items")
        self.ItemsRowLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ItemsRowLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.ItemsRowLabel.setMargin(5)

        self.TotalRowLabel = QLabel("Total")
        self.TotalRowLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.TotalRowLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.TotalRowLabel.setMargin(5)

        self.CoinValueSpinBox = QDoubleSpinBox()
        self.CoinValueSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CoinValueSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CoinValueSpinBox.setButtonSymbols(self.CoinValueSpinBox.ButtonSymbols.NoButtons)
        self.CoinValueSpinBox.setRange(0, 1000000000)
        self.CoinValueSpinBox.setReadOnly(True)
        self.CoinValueSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.CoinLoadSpinBox = QDoubleSpinBox()
        self.CoinLoadSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CoinLoadSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CoinLoadSpinBox.setButtonSymbols(self.CoinLoadSpinBox.ButtonSymbols.NoButtons)
        self.CoinLoadSpinBox.setRange(0, 1000000000)
        self.CoinLoadSpinBox.setReadOnly(True)
        self.CoinLoadSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.ItemsValueSpinBox = QDoubleSpinBox()
        self.ItemsValueSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ItemsValueSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.ItemsValueSpinBox.setButtonSymbols(self.ItemsValueSpinBox.ButtonSymbols.NoButtons)
        self.ItemsValueSpinBox.setRange(0, 1000000000)
        self.ItemsValueSpinBox.setReadOnly(True)
        self.ItemsValueSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.ItemsLoadSpinBox = QDoubleSpinBox()
        self.ItemsLoadSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ItemsLoadSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.ItemsLoadSpinBox.setButtonSymbols(self.ItemsLoadSpinBox.ButtonSymbols.NoButtons)
        self.ItemsLoadSpinBox.setRange(0, 1000000000)
        self.ItemsLoadSpinBox.setReadOnly(True)
        self.ItemsLoadSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.TotalValueSpinBox = QDoubleSpinBox()
        self.TotalValueSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.TotalValueSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.TotalValueSpinBox.setButtonSymbols(self.TotalValueSpinBox.ButtonSymbols.NoButtons)
        self.TotalValueSpinBox.setRange(0, 1000000000)
        self.TotalValueSpinBox.setReadOnly(True)
        self.TotalValueSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        self.TotalLoadSpinBox = QDoubleSpinBox()
        self.TotalLoadSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.TotalLoadSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.TotalLoadSpinBox.setButtonSymbols(self.TotalLoadSpinBox.ButtonSymbols.NoButtons)
        self.TotalLoadSpinBox.setRange(0, 1000000000)
        self.TotalLoadSpinBox.setReadOnly(True)
        self.TotalLoadSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        # Notes
        self.NotesLabel = QLabel("Notes")
        self.NotesLabel.setStyleSheet(self.SectionLabelStyle)
        self.NotesLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.NotesLabel.setMargin(self.HeaderLabelMargin)

        self.NotesTextEdit = IndentingTextEdit(TextChangedSlot=lambda: self.UpdateData("Notes", self.NotesTextEdit.toPlainText()))
        self.NotesTextEdit.setMinimumHeight(200)
        self.NotesTextEdit.setTabChangesFocus(True)

        # Inventory
        self.InventoryLabel = QLabel("Inventory")
        self.InventoryLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.InventoryLabel.setStyleSheet(self.SectionLabelStyle)
        self.InventoryLabel.setMargin(self.HeaderLabelMargin)

        self.InventoryTreeWidget = HoardInventoryTreeWidget(self)
        self.InventoryTreeWidget.itemActivated.connect(self.EditItem)
        self.InventoryTreeWidget.setMinimumWidth(600)

        self.AddItemButton = AddButton(self.AddItem, "Add Item")
        self.DeleteItemButton = DeleteButton(self.DeleteItem, "Delete Item")
        self.EditItemButton = EditButton(self.EditItem, "Edit Item")
        self.MoveItemUpButton = MoveUpButton(self.MoveItemUp, "Move Item Up")
        self.MoveItemDownButton = MoveDownButton(self.MoveItemDown, "Move Item Down")

        # Create and Set Layout
        self.Layout = QGridLayout()

        self.HeaderFrame = QFrame()
        self.HeaderFrame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
        self.HeaderLayout = QGridLayout()
        self.HeaderLayout.addWidget(self.NameOrOwnersLabel, 0, 0)
        self.HeaderLayout.addWidget(self.NameOrOwnersLineEdit, 0, 1)
        self.HeaderLayout.addWidget(self.LocationLabel, 0, 2)
        self.HeaderLayout.addWidget(self.LocationLineEdit, 0, 3)
        self.HeaderLayout.addWidget(self.StorageCostsLabel, 0, 4)
        self.HeaderLayout.addWidget(self.StorageCostsLineEdit, 0, 5)
        for Column in [1, 3, 5]:
            self.HeaderLayout.setColumnStretch(Column, 1)
        self.HeaderFrame.setLayout(self.HeaderLayout)
        self.Layout.addWidget(self.HeaderFrame, 0, 0)

        self.HoardFrame = QFrame()
        self.HoardFrame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
        self.HoardLayout = QGridLayout()

        self.CoinsLayout = QGridLayout()
        self.CoinsLayout.addWidget(self.CoinsLabel, 0, 0, 1, 5)
        self.CoinsLayout.addWidget(self.CPLabel, 1, 0)
        self.CoinsLayout.addWidget(self.CPSpinBox, 2, 0)
        self.CoinsLayout.addWidget(self.SPLabel, 1, 1)
        self.CoinsLayout.addWidget(self.SPSpinBox, 2, 1)
        self.CoinsLayout.addWidget(self.EPLabel, 1, 2)
        self.CoinsLayout.addWidget(self.EPSpinBox, 2, 2)
        self.CoinsLayout.addWidget(self.GPLabel, 1, 3)
        self.CoinsLayout.addWidget(self.GPSpinBox, 2, 3)
        self.CoinsLayout.addWidget(self.PPLabel, 1, 4)
        self.CoinsLayout.addWidget(self.PPSpinBox, 2, 4)
        self.CoinButtonsLayout = QGridLayout()
        self.CoinButtonsLayout.addWidget(self.GainCoinsButton, 0, 0)
        self.CoinButtonsLayout.addWidget(self.SpendCoinsButton, 0, 1)
        self.CoinsLayout.addLayout(self.CoinButtonsLayout, 3, 0, 1, 5)
        self.HoardLayout.addLayout(self.CoinsLayout, 0, 0)

        self.HoardStatsLayout = QGridLayout()
        self.HoardStatsLayout.addWidget(self.HoardStatsLabel, 0, 0, 1, 3)
        self.HoardStatsLayout.addWidget(self.ValueColumnLabel, 1, 1)
        self.HoardStatsLayout.addWidget(self.LoadColumnLabel, 1, 2)
        self.HoardStatsLayout.addWidget(self.CoinsRowLabel, 2, 0)
        self.HoardStatsLayout.addWidget(self.CoinValueSpinBox, 2, 1)
        self.HoardStatsLayout.addWidget(self.CoinLoadSpinBox, 2, 2)
        self.HoardStatsLayout.addWidget(self.ItemsRowLabel, 3, 0)
        self.HoardStatsLayout.addWidget(self.ItemsValueSpinBox, 3, 1)
        self.HoardStatsLayout.addWidget(self.ItemsLoadSpinBox, 3, 2)
        self.HoardStatsLayout.addWidget(self.TotalRowLabel, 4, 0)
        self.HoardStatsLayout.addWidget(self.TotalValueSpinBox, 4, 1)
        self.HoardStatsLayout.addWidget(self.TotalLoadSpinBox, 4, 2)
        self.HoardLayout.addLayout(self.HoardStatsLayout, 1, 0)

        self.NotesLayout = QGridLayout()
        self.NotesLayout.addWidget(self.NotesLabel, 0, 0)
        self.NotesLayout.addWidget(self.NotesTextEdit, 1, 0)
        self.HoardLayout.addLayout(self.NotesLayout, 2, 0)

        self.InventoryLayout = QGridLayout()
        self.InventoryLayout.addWidget(self.InventoryLabel, 0, 0, 1, 5)
        self.InventoryLayout.addWidget(self.AddItemButton, 1, 0)
        self.InventoryLayout.addWidget(self.DeleteItemButton, 1, 1)
        self.InventoryLayout.addWidget(self.EditItemButton, 1, 2)
        self.InventoryLayout.addWidget(self.MoveItemUpButton, 1, 3)
        self.InventoryLayout.addWidget(self.MoveItemDownButton, 1, 4)
        self.InventoryLayout.addWidget(self.InventoryTreeWidget, 2, 0, 1, 5)
        self.HoardLayout.addLayout(self.InventoryLayout, 0, 1, 3, 1)

        self.HoardLayout.setColumnStretch(1, 1)

        self.HoardFrame.setLayout(self.HoardLayout)
        self.Layout.addWidget(self.HoardFrame, 1, 0)

        self.Layout.setRowStretch(1, 1)

        self.Frame.setLayout(self.Layout)

        # Create Actions
        self.CreateActions()

        # Create Menu Bar
        self.CreateMenuBar()

        # Create Status Bar
        self.StatusBar = self.statusBar()

        # Create Keybindings
        self.CreateKeybindings()

    def CreateActions(self):
        self.NewAction = QAction("New")
        self.NewAction.triggered.connect(self.NewActionTriggered)

        self.OpenAction = QAction("Open")
        self.OpenAction.triggered.connect(self.OpenActionTriggered)

        self.SaveAction = QAction("Save")
        self.SaveAction.triggered.connect(self.SaveActionTriggered)

        self.SaveAsAction = QAction("Save As")
        self.SaveAsAction.triggered.connect(self.SaveAsActionTriggered)

        self.GzipModeAction = QAction("Gzip Mode (Smaller Files)")
        self.GzipModeAction.setCheckable(True)
        self.GzipModeAction.setChecked(self.GzipMode)
        self.GzipModeAction.triggered.connect(self.ToggleGzipMode)

        self.QuitAction = QAction("Quit")
        self.QuitAction.triggered.connect(self.close)

        self.CoinCalculatorAction = QAction("Coin Calculator")
        self.CoinCalculatorAction.triggered.connect(self.ShowCoinCalculator)

    def CreateMenuBar(self):
        self.MenuBar = self.menuBar()

        self.FileMenu = self.MenuBar.addMenu("File")
        self.FileMenu.addAction(self.NewAction)
        self.FileMenu.addAction(self.OpenAction)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.SaveAction)
        self.FileMenu.addAction(self.SaveAsAction)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.GzipModeAction)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.QuitAction)

        self.MenuBar.addAction(self.CoinCalculatorAction)

    def CreateKeybindings(self):
        self.DefaultKeybindings = {}
        self.DefaultKeybindings["NewAction"] = "Ctrl+N"
        self.DefaultKeybindings["OpenAction"] = "Ctrl+O"
        self.DefaultKeybindings["SaveAction"] = "Ctrl+S"
        self.DefaultKeybindings["SaveAsAction"] = "Ctrl+Shift+S"
        self.DefaultKeybindings["QuitAction"] = "Ctrl+Q"

    def LoadConfigs(self):
        # Keybindings
        KeybindingsFile = self.GetResourcePath("Configs/HoardKeybindings.cfg")
        if os.path.isfile(KeybindingsFile):
            with open(KeybindingsFile, "r") as ConfigFile:
                self.Keybindings = json.loads(ConfigFile.read())
        else:
            self.Keybindings = copy.deepcopy(self.DefaultKeybindings)
        for Action, Keybinding in self.DefaultKeybindings.items():
            if Action not in self.Keybindings:
                self.Keybindings[Action] = Keybinding
        InvalidBindings = []
        for Action in self.Keybindings.keys():
            if Action not in self.DefaultKeybindings:
                InvalidBindings.append(Action)
        for InvalidBinding in InvalidBindings:
            del self.Keybindings[InvalidBinding]
        for Action, Keybinding in self.Keybindings.items():
            getattr(self, Action).setShortcut(Keybinding)

    def SaveConfigs(self):
        if not os.path.isdir(self.GetResourcePath("Configs")):
            os.mkdir(self.GetResourcePath("Configs"))

        # Keybindings
        with open(self.GetResourcePath("Configs/NPCKeybindings.cfg"), "w") as ConfigFile:
            ConfigFile.write(json.dumps(self.Keybindings, indent=2))

        # Last Opened Directory
        self.SaveLastOpenedDirectory()

        # Gzip Mode
        self.SaveGzipMode()

    # Hoard Methods
    def UpdateData(self, Data, NewValue):
        if not self.UpdatingFieldsFromHoard:
            self.Hoard.UpdateData(Data, NewValue)
            self.UpdateUnsavedChangesFlag(True)

    def GainCoins(self):
        GainCoinsDialogInst = GainCoinsDialog(self)
        if GainCoinsDialogInst.Submitted:
            self.CPSpinBox.setValue(self.Hoard.HoardData["Coins"]["CP"] + GainCoinsDialogInst.GainedCoins["CP"])
            self.SPSpinBox.setValue(self.Hoard.HoardData["Coins"]["SP"] + GainCoinsDialogInst.GainedCoins["SP"])
            self.EPSpinBox.setValue(self.Hoard.HoardData["Coins"]["EP"] + GainCoinsDialogInst.GainedCoins["EP"])
            self.GPSpinBox.setValue(self.Hoard.HoardData["Coins"]["GP"] + GainCoinsDialogInst.GainedCoins["GP"])
            self.PPSpinBox.setValue(self.Hoard.HoardData["Coins"]["PP"] + GainCoinsDialogInst.GainedCoins["PP"])

    def SpendCoins(self):
        SpendCoinsDialogInst = SpendCoinsDialog(self)
        if SpendCoinsDialogInst.Submitted:
            self.CPSpinBox.setValue(SpendCoinsDialogInst.RemainingCoins["CP"])
            self.SPSpinBox.setValue(SpendCoinsDialogInst.RemainingCoins["SP"])
            self.EPSpinBox.setValue(SpendCoinsDialogInst.RemainingCoins["EP"])
            self.GPSpinBox.setValue(SpendCoinsDialogInst.RemainingCoins["GP"])
            self.PPSpinBox.setValue(SpendCoinsDialogInst.RemainingCoins["PP"])

    def GetCurrentCoinCounts(self):
        CurrentCoinCounts = {}
        CurrentCoinCounts["CP"] = self.Hoard.HoardData["Coins"]["CP"]
        CurrentCoinCounts["SP"] = self.Hoard.HoardData["Coins"]["SP"]
        CurrentCoinCounts["EP"] = self.Hoard.HoardData["Coins"]["EP"]
        CurrentCoinCounts["GP"] = self.Hoard.HoardData["Coins"]["GP"]
        CurrentCoinCounts["PP"] = self.Hoard.HoardData["Coins"]["PP"]
        return CurrentCoinCounts

    def AddItem(self):
        ItemIndex = self.Hoard.AddInventoryItem()
        self.UpdateDisplay()
        EditItemDialogInst = HoardEditItemDialog(self, self.Hoard.HoardData["Inventory"], ItemIndex, AddMode=True)
        if EditItemDialogInst.Cancelled:
            self.Hoard.DeleteLastInventoryItem()
            self.UpdateDisplay()
        else:
            self.UpdateUnsavedChangesFlag(True)
            self.InventoryTreeWidget.SelectIndex(ItemIndex)

    def DeleteItem(self):
        CurrentSelection = self.InventoryTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            if self.DisplayMessageBox("Are you sure you want to delete this item?  This cannot be undone.", Icon=QMessageBox.Icon.Warning, Buttons=(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)) == QMessageBox.StandardButton.Yes:
                CurrentItem = CurrentSelection[0]
                CurrentItemIndex = CurrentItem.Index
                self.Hoard.DeleteInventoryItem(CurrentItemIndex)
                self.UpdateUnsavedChangesFlag(True)
                InventoryLength = len(self.Hoard.HoardData["Inventory"])
                if InventoryLength > 0:
                    self.InventoryTreeWidget.SelectIndex(CurrentItemIndex if CurrentItemIndex < InventoryLength else InventoryLength - 1)

    def EditItem(self):
        CurrentSelection = self.InventoryTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentItem = CurrentSelection[0]
            CurrentItemIndex = CurrentItem.Index
            EditItemDialogInst = HoardEditItemDialog(self, self.Hoard.HoardData["Inventory"], CurrentItemIndex)
            if EditItemDialogInst.UnsavedChanges:
                self.UpdateUnsavedChangesFlag(True)
                self.InventoryTreeWidget.SelectIndex(CurrentItemIndex)

    def MoveItemUp(self):
        self.MoveItem(-1)

    def MoveItemDown(self):
        self.MoveItem(1)

    def MoveItem(self, Delta):
        CurrentSelection = self.InventoryTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentItem = CurrentSelection[0]
            CurrentItemIndex = CurrentItem.Index
            if self.Hoard.MoveInventoryItem(CurrentItemIndex, Delta):
                self.UpdateUnsavedChangesFlag(True)
                self.InventoryTreeWidget.SelectIndex(CurrentItemIndex + Delta)

    # View Methods
    def ShowCoinCalculator(self):
        CoinCalculatorDialog(self)

    # Save and Open Methods
    def NewActionTriggered(self):
        if self.New(self.Hoard):
            self.Hoard = Hoard()
        self.UpdatingFieldsFromHoard = True
        self.UpdateDisplay()
        self.UpdatingFieldsFromHoard = False

    def OpenActionTriggered(self):
        OpenData = self.Open(self.Hoard)
        if OpenData is not None:
            self.Hoard = OpenData
        self.UpdatingFieldsFromHoard = True
        self.UpdateDisplay()
        self.UpdatingFieldsFromHoard = False

    def SaveActionTriggered(self):
        self.Save(self.Hoard)
        self.UpdateDisplay()

    def SaveAsActionTriggered(self):
        self.Save(self.Hoard, SaveAs=True)
        self.UpdateDisplay()

    def ToggleGzipMode(self):
        self.GzipMode = not self.GzipMode

    def closeEvent(self, event):
        Close = True
        if self.UnsavedChanges:
            SavePrompt = self.DisplayMessageBox("Save unsaved changes before closing?", Icon=QMessageBox.Icon.Warning, Buttons=(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel))
            if SavePrompt == QMessageBox.StandardButton.Yes:
                if not self.Save(self.Hoard):
                    Close = False
            elif SavePrompt == QMessageBox.StandardButton.No:
                pass
            elif SavePrompt == QMessageBox.StandardButton.Cancel:
                Close = False
        if not Close:
            event.ignore()
        else:
            self.SaveConfigs()
            event.accept()

    def UpdateUnsavedChangesFlag(self, UnsavedChanges):
        self.UnsavedChanges = UnsavedChanges
        self.UpdateDisplay()

   # Display Update Methods
    def UpdateDisplay(self):
        self.UpdateWindowTitle()

        # Update Derived Data
        self.DerivedData = self.Hoard.GetDerivedData()

        # Hoard Stats
        self.CoinValueSpinBox.setValue(self.DerivedData["Value of Coins"])
        self.CoinLoadSpinBox.setValue(self.DerivedData["Load of Coins"])
        self.ItemsValueSpinBox.setValue(self.DerivedData["Value of Inventory"])
        self.ItemsLoadSpinBox.setValue(self.DerivedData["Load of Inventory"])
        self.TotalValueSpinBox.setValue(self.DerivedData["Total Value"])
        self.TotalLoadSpinBox.setValue(self.DerivedData["Total Load"])

        # Inventory
        self.InventoryTreeWidget.FillFromInventory()

        # Updating Fields from Hoard
        if self.UpdatingFieldsFromHoard:
            # Header
            self.NameOrOwnersLineEdit.setText(self.Hoard.HoardData["Name or Owners"])
            self.LocationLineEdit.setText(self.Hoard.HoardData["Location"])
            self.StorageCostsLineEdit.setText(self.Hoard.HoardData["Storage Costs"])

            # Coins
            self.CPSpinBox.setValue(self.Hoard.HoardData["Coins"]["CP"])
            self.SPSpinBox.setValue(self.Hoard.HoardData["Coins"]["SP"])
            self.EPSpinBox.setValue(self.Hoard.HoardData["Coins"]["EP"])
            self.GPSpinBox.setValue(self.Hoard.HoardData["Coins"]["GP"])
            self.PPSpinBox.setValue(self.Hoard.HoardData["Coins"]["PP"])

            # Notes
            self.NotesTextEdit.setPlainText(self.Hoard.HoardData["Notes"])

    def UpdateWindowTitle(self):
        CurrentFileTitleSection = f" [{os.path.basename(self.CurrentOpenFileName)}]" if self.CurrentOpenFileName != "" else ""
        UnsavedChangesIndicator = " *" if self.UnsavedChanges else ""
        self.setWindowTitle(f"{self.ScriptName} Hoard Sheet{CurrentFileTitleSection}{UnsavedChangesIndicator}")
