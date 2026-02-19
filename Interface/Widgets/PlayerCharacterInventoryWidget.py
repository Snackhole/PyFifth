from PyQt6 import QtCore
from PyQt6.QtWidgets import QDoubleSpinBox, QFrame, QGridLayout, QInputDialog, QLabel, QMessageBox, QSizePolicy, QSpinBox

from Interface.Dialogs.GainCoinsDialog import GainCoinsDialog
from Interface.Dialogs.PlayerCharacterEditItemDialog import PlayerCharacterEditItemDialog
from Interface.Dialogs.SpendCoinsDialog import SpendCoinsDialog
from Interface.Widgets.IconButtons import AddButton, DeleteButton, EditButton, MoveDownButton, MoveUpButton
from Interface.Widgets.PlayerCharacterInventoryTreeWidget import PlayerCharacterInventoryTreeWidget


class PlayerCharacterInventoryWidget(QFrame):
    def __init__(self, CharacterWindow):
        # Initialize Frame
        super().__init__()

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Styles
        self.SectionLabelStyle = "QLabel {font-size: 10pt; font-weight: bold;}"
        self.CarryingCapacityStyle = "QSpinBox {font-size: 16pt;}"
        self.TotalLoadsStyle = "QDoubleSpinBox {}"
        self.TotalLoadsEncumberedStyle = "QDoubleSpinBox {background-color: darkred;}"

        # Header Label Margin
        self.HeaderLabelMargin = 5

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        # Create Carrying Capacity
        self.CreateCarryingCapacity()

        # Create Loads and Values
        self.CreateLoadsAndValues()

        # Create Coins
        self.CreateCoins()

        # Create Food and Water
        self.CreateFoodAndWater()

        # Create Inventory
        self.CreateInventory()

        # Create and Set Layout
        self.CreateAndSetLayout()

    def CreateCarryingCapacity(self):
        # Carrying Capacity Label
        self.CarryingCapacityLabel = QLabel("Carrying Capacity")
        self.CarryingCapacityLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CarryingCapacityLabel.setStyleSheet(self.SectionLabelStyle)
        self.CarryingCapacityLabel.setMargin(self.HeaderLabelMargin)

        # Carrying Capacity Spin Box
        self.CarryingCapacitySpinBox = QSpinBox()
        self.CarryingCapacitySpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CarryingCapacitySpinBox.setStyleSheet(self.CarryingCapacityStyle)
        self.CarryingCapacitySpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CarryingCapacitySpinBox.setButtonSymbols(self.CarryingCapacitySpinBox.ButtonSymbols.NoButtons)
        self.CarryingCapacitySpinBox.setRange(0, 1000000000)
        self.CarryingCapacitySpinBox.setReadOnly(True)
        self.CarryingCapacitySpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        # Carrying Capacity Edit Button
        self.CarryingCapacityEditButton = EditButton(self.EditBonusCarryingCapacityStatModifier, "Edit Bonus Carrying Capacity Stat Modifier")
        self.CarryingCapacityEditButton.setSizePolicy(self.InputsSizePolicy)

    def CreateLoadsAndValues(self):
        # Loads and Values Label
        self.LoadsAndValuesLabel = QLabel("Loads and Values")
        self.LoadsAndValuesLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.LoadsAndValuesLabel.setStyleSheet(self.SectionLabelStyle)
        self.LoadsAndValuesLabel.setMargin(self.HeaderLabelMargin)

        # Header Labels
        self.LoadsLabel = QLabel("Loads (lbs.)")
        self.LoadsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.LoadsLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.LoadsLabel.setMargin(5)
        self.ValuesLabel = QLabel("Values (GP)")
        self.ValuesLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.ValuesLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.ValuesLabel.setMargin(5)

        # Tags Labels
        self.TotalLabel = QLabel("Total")
        self.TotalLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.TotalLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.TotalLabel.setMargin(5)
        self.GearLabel = QLabel("Gear")
        self.GearLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.GearLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.GearLabel.setMargin(5)
        self.TreasureLabel = QLabel("Treasure")
        self.TreasureLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.TreasureLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.TreasureLabel.setMargin(5)
        self.MiscLabel = QLabel("Misc.")
        self.MiscLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.MiscLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.MiscLabel.setMargin(5)

        # Loads Spin Boxes
        self.TotalLoadSpinBox = QDoubleSpinBox()
        self.TotalLoadSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.TotalLoadSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.TotalLoadSpinBox.setButtonSymbols(self.TotalLoadSpinBox.ButtonSymbols.NoButtons)
        self.TotalLoadSpinBox.setRange(0, 1000000000)
        self.TotalLoadSpinBox.setReadOnly(True)
        self.TotalLoadSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.GearLoadSpinBox = QDoubleSpinBox()
        self.GearLoadSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.GearLoadSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.GearLoadSpinBox.setButtonSymbols(self.GearLoadSpinBox.ButtonSymbols.NoButtons)
        self.GearLoadSpinBox.setRange(0, 1000000000)
        self.GearLoadSpinBox.setReadOnly(True)
        self.GearLoadSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.TreasureLoadSpinBox = QDoubleSpinBox()
        self.TreasureLoadSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.TreasureLoadSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.TreasureLoadSpinBox.setButtonSymbols(self.TreasureLoadSpinBox.ButtonSymbols.NoButtons)
        self.TreasureLoadSpinBox.setRange(0, 1000000000)
        self.TreasureLoadSpinBox.setReadOnly(True)
        self.TreasureLoadSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.MiscLoadSpinBox = QDoubleSpinBox()
        self.MiscLoadSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.MiscLoadSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MiscLoadSpinBox.setButtonSymbols(self.MiscLoadSpinBox.ButtonSymbols.NoButtons)
        self.MiscLoadSpinBox.setRange(0, 1000000000)
        self.MiscLoadSpinBox.setReadOnly(True)
        self.MiscLoadSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        # Values Spin Boxes
        self.TotalValueSpinBox = QDoubleSpinBox()
        self.TotalValueSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.TotalValueSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.TotalValueSpinBox.setButtonSymbols(self.TotalValueSpinBox.ButtonSymbols.NoButtons)
        self.TotalValueSpinBox.setRange(0, 1000000000)
        self.TotalValueSpinBox.setReadOnly(True)
        self.TotalValueSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.GearValueSpinBox = QDoubleSpinBox()
        self.GearValueSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.GearValueSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.GearValueSpinBox.setButtonSymbols(self.GearValueSpinBox.ButtonSymbols.NoButtons)
        self.GearValueSpinBox.setRange(0, 1000000000)
        self.GearValueSpinBox.setReadOnly(True)
        self.GearValueSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.TreasureValueSpinBox = QDoubleSpinBox()
        self.TreasureValueSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.TreasureValueSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.TreasureValueSpinBox.setButtonSymbols(self.TreasureValueSpinBox.ButtonSymbols.NoButtons)
        self.TreasureValueSpinBox.setRange(0, 1000000000)
        self.TreasureValueSpinBox.setReadOnly(True)
        self.TreasureValueSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.MiscValueSpinBox = QDoubleSpinBox()
        self.MiscValueSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.MiscValueSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MiscValueSpinBox.setButtonSymbols(self.MiscValueSpinBox.ButtonSymbols.NoButtons)
        self.MiscValueSpinBox.setRange(0, 1000000000)
        self.MiscValueSpinBox.setReadOnly(True)
        self.MiscValueSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

    def CreateCoins(self):
        # Coins Label
        self.CoinsLabel = QLabel("Coins")
        self.CoinsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CoinsLabel.setStyleSheet(self.SectionLabelStyle)
        self.CoinsLabel.setMargin(self.HeaderLabelMargin)

        # Coins Header Labels
        self.CPLabel = QLabel("CP")
        self.CPLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CPLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.CPLabel.setMargin(5)
        self.SPLabel = QLabel("SP")
        self.SPLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SPLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.SPLabel.setMargin(5)
        self.EPLabel = QLabel("EP")
        self.EPLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.EPLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.EPLabel.setMargin(5)
        self.GPLabel = QLabel("GP")
        self.GPLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.GPLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.GPLabel.setMargin(5)
        self.PPLabel = QLabel("PP")
        self.PPLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.PPLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.PPLabel.setMargin(5)

        # Coins Spin Boxes
        self.CPSpinBox = QSpinBox()
        self.CPSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CPSpinBox.setButtonSymbols(self.CPSpinBox.ButtonSymbols.NoButtons)
        self.CPSpinBox.setRange(0, 1000000000)
        self.CPSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Coins", "CP"), self.CPSpinBox.value()))
        self.SPSpinBox = QSpinBox()
        self.SPSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SPSpinBox.setButtonSymbols(self.SPSpinBox.ButtonSymbols.NoButtons)
        self.SPSpinBox.setRange(0, 1000000000)
        self.SPSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Coins", "SP"), self.SPSpinBox.value()))
        self.EPSpinBox = QSpinBox()
        self.EPSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.EPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.EPSpinBox.setButtonSymbols(self.EPSpinBox.ButtonSymbols.NoButtons)
        self.EPSpinBox.setRange(0, 1000000000)
        self.EPSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Coins", "EP"), self.EPSpinBox.value()))
        self.GPSpinBox = QSpinBox()
        self.GPSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.GPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.GPSpinBox.setButtonSymbols(self.GPSpinBox.ButtonSymbols.NoButtons)
        self.GPSpinBox.setRange(0, 1000000000)
        self.GPSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Coins", "GP"), self.GPSpinBox.value()))
        self.PPSpinBox = QSpinBox()
        self.PPSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.PPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.PPSpinBox.setButtonSymbols(self.PPSpinBox.ButtonSymbols.NoButtons)
        self.PPSpinBox.setRange(0, 1000000000)
        self.PPSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Coins", "PP"), self.PPSpinBox.value()))

        # Coins Buttons
        self.GainCoinsButton = AddButton(self.GainCoins, "Gain Coins")
        self.SpendCoinsButton = DeleteButton(self.SpendCoins, "Spend Coins")

        # Coin Value
        self.CoinValueLabel = QLabel("Coin Value (GP)")
        self.CoinValueLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CoinValueLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.CoinValueLabel.setMargin(5)
        self.CoinValueSpinBox = QDoubleSpinBox()
        self.CoinValueSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CoinValueSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CoinValueSpinBox.setButtonSymbols(self.CoinValueSpinBox.ButtonSymbols.NoButtons)
        self.CoinValueSpinBox.setRange(0, 1000000000)
        self.CoinValueSpinBox.setReadOnly(True)
        self.CoinValueSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        # Coin Load
        self.CoinLoadLabel = QLabel("Coin Load (lbs.)")
        self.CoinLoadLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CoinLoadLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.CoinLoadLabel.setMargin(5)
        self.CoinLoadSpinBox = QDoubleSpinBox()
        self.CoinLoadSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CoinLoadSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CoinLoadSpinBox.setButtonSymbols(self.CoinLoadSpinBox.ButtonSymbols.NoButtons)
        self.CoinLoadSpinBox.setRange(0, 1000000000)
        self.CoinLoadSpinBox.setReadOnly(True)
        self.CoinLoadSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

    def CreateFoodAndWater(self):
        # Food and Water Label
        self.FoodAndWaterLabel = QLabel("Food and Water")
        self.FoodAndWaterLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.FoodAndWaterLabel.setStyleSheet(self.SectionLabelStyle)
        self.FoodAndWaterLabel.setMargin(self.HeaderLabelMargin)

        # Header Labels
        self.FoodAndWaterLoadLabel = QLabel("Load (lbs.)")
        self.FoodAndWaterLoadLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.FoodAndWaterLoadLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.FoodAndWaterLoadLabel.setMargin(5)
        self.FoodAndWaterDaysLabel = QLabel("Days")
        self.FoodAndWaterDaysLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.FoodAndWaterDaysLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.FoodAndWaterDaysLabel.setMargin(5)

        # Tags Labels
        self.FoodLabel = QLabel("Food")
        self.FoodLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.FoodLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.FoodLabel.setMargin(5)
        self.WaterLabel = QLabel("Water")
        self.WaterLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.WaterLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.WaterLabel.setMargin(5)

        # Loads Spin Boxes
        self.FoodLoadSpinBox = QDoubleSpinBox()
        self.FoodLoadSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.FoodLoadSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.FoodLoadSpinBox.setButtonSymbols(self.FoodLoadSpinBox.ButtonSymbols.NoButtons)
        self.FoodLoadSpinBox.setRange(0, 1000000000)
        self.FoodLoadSpinBox.setReadOnly(True)
        self.FoodLoadSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.WaterLoadSpinBox = QDoubleSpinBox()
        self.WaterLoadSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.WaterLoadSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.WaterLoadSpinBox.setButtonSymbols(self.WaterLoadSpinBox.ButtonSymbols.NoButtons)
        self.WaterLoadSpinBox.setRange(0, 1000000000)
        self.WaterLoadSpinBox.setReadOnly(True)
        self.WaterLoadSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        # Days Spin Boxes
        self.FoodDaysSpinBox = QDoubleSpinBox()
        self.FoodDaysSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.FoodDaysSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.FoodDaysSpinBox.setButtonSymbols(self.FoodDaysSpinBox.ButtonSymbols.NoButtons)
        self.FoodDaysSpinBox.setRange(0, 1000000000)
        self.FoodDaysSpinBox.setReadOnly(True)
        self.FoodDaysSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.WaterDaysSpinBox = QDoubleSpinBox()
        self.WaterDaysSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.WaterDaysSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.WaterDaysSpinBox.setButtonSymbols(self.WaterDaysSpinBox.ButtonSymbols.NoButtons)
        self.WaterDaysSpinBox.setRange(0, 1000000000)
        self.WaterDaysSpinBox.setReadOnly(True)
        self.WaterDaysSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        # Days Buttons
        self.FoodDaysEditButton = EditButton(lambda: self.EditConsumptionRate("Food"), "Edit Food Consumption Rate")
        self.FoodDaysEditButton.setSizePolicy(self.InputsSizePolicy)
        self.WaterDaysEditButton = EditButton(lambda: self.EditConsumptionRate("Water"), "Edit Water Consumption Rate")
        self.WaterDaysEditButton.setSizePolicy(self.InputsSizePolicy)

    def CreateInventory(self):
        # Inventory Label
        self.InventoryLabel = QLabel("Inventory")
        self.InventoryLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.InventoryLabel.setStyleSheet(self.SectionLabelStyle)
        self.InventoryLabel.setMargin(self.HeaderLabelMargin)

        # Inventory Tree Widget
        self.InventoryTreeWidget = PlayerCharacterInventoryTreeWidget(self.CharacterWindow)
        self.InventoryTreeWidget.itemActivated.connect(self.EditItem)

        # Buttons
        self.AddItemButton = AddButton(self.AddItem, "Add Item")
        self.AddItemButton.setSizePolicy(self.InputsSizePolicy)
        self.DeleteItemButton = DeleteButton(self.DeleteItem, "Delete Item")
        self.DeleteItemButton.setSizePolicy(self.InputsSizePolicy)
        self.EditItemButton = EditButton(self.EditItem, "Edit Item")
        self.EditItemButton.setSizePolicy(self.InputsSizePolicy)
        self.MoveItemUpButton = MoveUpButton(self.MoveItemUp, "Move Item Up")
        self.MoveItemUpButton.setSizePolicy(self.InputsSizePolicy)
        self.MoveItemDownButton = MoveDownButton(self.MoveItemDown, "Move Item Down")
        self.MoveItemDownButton.setSizePolicy(self.InputsSizePolicy)

    def CreateAndSetLayout(self):
        # Create Layout
        self.Layout = QGridLayout()

        # Carrying Capacity
        self.CarryingCapacityLayout = QGridLayout()
        self.CarryingCapacityLayout.addWidget(self.CarryingCapacityLabel, 0, 0, 1, 2)
        self.CarryingCapacityLayout.addWidget(self.CarryingCapacitySpinBox, 1, 0)
        self.CarryingCapacityLayout.addWidget(self.CarryingCapacityEditButton, 1, 1)
        self.CarryingCapacityLayout.setRowStretch(1, 1)
        self.CarryingCapacityLayout.setColumnStretch(0, 1)
        self.Layout.addLayout(self.CarryingCapacityLayout, 0, 0)

        # Loads and Values
        self.LoadsAndValuesLayout = QGridLayout()
        self.LoadsAndValuesLayout.addWidget(self.LoadsAndValuesLabel, 0, 0, 1, 3)
        self.LoadsAndValuesLayout.addWidget(self.LoadsLabel, 1, 1)
        self.LoadsAndValuesLayout.addWidget(self.ValuesLabel, 1, 2)
        self.LoadsAndValuesLayout.addWidget(self.TotalLabel, 2, 0)
        self.LoadsAndValuesLayout.addWidget(self.TotalLoadSpinBox, 2, 1)
        self.LoadsAndValuesLayout.addWidget(self.TotalValueSpinBox, 2, 2)
        self.LoadsAndValuesLayout.addWidget(self.GearLabel, 3, 0)
        self.LoadsAndValuesLayout.addWidget(self.GearLoadSpinBox, 3, 1)
        self.LoadsAndValuesLayout.addWidget(self.GearValueSpinBox, 3, 2)
        self.LoadsAndValuesLayout.addWidget(self.TreasureLabel, 4, 0)
        self.LoadsAndValuesLayout.addWidget(self.TreasureLoadSpinBox, 4, 1)
        self.LoadsAndValuesLayout.addWidget(self.TreasureValueSpinBox, 4, 2)
        self.LoadsAndValuesLayout.addWidget(self.MiscLabel, 5, 0)
        self.LoadsAndValuesLayout.addWidget(self.MiscLoadSpinBox, 5, 1)
        self.LoadsAndValuesLayout.addWidget(self.MiscValueSpinBox, 5, 2)
        for Row in range(2, 6):
            self.LoadsAndValuesLayout.setRowStretch(Row, 1)
        for Column in range(1, 3):
            self.LoadsAndValuesLayout.setColumnStretch(Column, 1)
        self.Layout.addLayout(self.LoadsAndValuesLayout, 0, 1)

        # Coins
        self.CoinsLayout = QGridLayout()
        self.CoinsLayout.addWidget(self.CoinsLabel, 0, 0, 1, 2)
        self.CoinsInputsLayout = QGridLayout()
        self.CoinsInputsLayout.addWidget(self.CPLabel, 0, 0)
        self.CoinsInputsLayout.addWidget(self.SPLabel, 1, 0)
        self.CoinsInputsLayout.addWidget(self.EPLabel, 2, 0)
        self.CoinsInputsLayout.addWidget(self.GPLabel, 3, 0)
        self.CoinsInputsLayout.addWidget(self.PPLabel, 4, 0)
        self.CoinsInputsLayout.addWidget(self.CPSpinBox, 0, 1)
        self.CoinsInputsLayout.addWidget(self.SPSpinBox, 1, 1)
        self.CoinsInputsLayout.addWidget(self.EPSpinBox, 2, 1)
        self.CoinsInputsLayout.addWidget(self.GPSpinBox, 3, 1)
        self.CoinsInputsLayout.addWidget(self.PPSpinBox, 4, 1)
        self.CoinsInputsLayout.setColumnStretch(1, 1)
        self.CoinsLayout.addLayout(self.CoinsInputsLayout, 1, 0, 4, 1)
        self.CoinsLayout.addWidget(self.CoinValueLabel, 1, 1)
        self.CoinsLayout.addWidget(self.CoinValueSpinBox, 2, 1)
        self.CoinsLayout.addWidget(self.CoinLoadLabel, 3, 1)
        self.CoinsLayout.addWidget(self.CoinLoadSpinBox, 4, 1)
        self.CoinButtonsLayout = QGridLayout()
        self.CoinButtonsLayout.addWidget(self.GainCoinsButton, 0, 0)
        self.CoinButtonsLayout.addWidget(self.SpendCoinsButton, 0, 1)
        self.CoinsLayout.addLayout(self.CoinButtonsLayout, 5, 0, 1, 2)
        self.CoinsLayout.setColumnStretch(1, 1)
        for Row in [2, 4]:
            self.CoinsLayout.setRowStretch(Row, 1)
        self.Layout.addLayout(self.CoinsLayout, 0, 2)

        # Food and Water
        self.FoodAndWaterLayout = QGridLayout()
        self.FoodAndWaterLayout.addWidget(self.FoodAndWaterLabel, 0, 0, 1, 4)
        self.FoodAndWaterLayout.addWidget(self.FoodAndWaterLoadLabel, 1, 1)
        self.FoodAndWaterLayout.addWidget(self.FoodAndWaterDaysLabel, 1, 2, 1, 2)
        self.FoodAndWaterLayout.addWidget(self.FoodLabel, 2, 0)
        self.FoodAndWaterLayout.addWidget(self.FoodLoadSpinBox, 2, 1)
        self.FoodAndWaterLayout.addWidget(self.FoodDaysSpinBox, 2, 2)
        self.FoodAndWaterLayout.addWidget(self.FoodDaysEditButton, 2, 3)
        self.FoodAndWaterLayout.addWidget(self.WaterLabel, 3, 0)
        self.FoodAndWaterLayout.addWidget(self.WaterLoadSpinBox, 3, 1)
        self.FoodAndWaterLayout.addWidget(self.WaterDaysSpinBox, 3, 2)
        self.FoodAndWaterLayout.addWidget(self.WaterDaysEditButton, 3, 3)
        for Row in range(2, 4):
            self.FoodAndWaterLayout.setRowStretch(Row, 1)
        self.Layout.addLayout(self.FoodAndWaterLayout, 0, 3)

        # Inventory
        self.InventoryLayout = QGridLayout()
        self.InventoryLayout.addWidget(self.InventoryLabel, 0, 0, 1, 5)
        self.InventoryLayout.addWidget(self.AddItemButton, 1, 0)
        self.InventoryLayout.addWidget(self.DeleteItemButton, 1, 1)
        self.InventoryLayout.addWidget(self.EditItemButton, 1, 2)
        self.InventoryLayout.addWidget(self.MoveItemUpButton, 1, 3)
        self.InventoryLayout.addWidget(self.MoveItemDownButton, 1, 4)
        self.InventoryLayout.addWidget(self.InventoryTreeWidget, 2, 0, 1, 5)
        self.InventoryLayout.setRowStretch(2, 1)
        self.Layout.addLayout(self.InventoryLayout, 1, 0, 1, 4)

        # Layout Stretch
        self.Layout.setColumnStretch(0, 1)
        self.Layout.setRowStretch(1, 1)

        # Set Layout
        self.setLayout(self.Layout)

    def EditBonusCarryingCapacityStatModifier(self):
        self.CharacterWindow.EditStatModifier(self.CharacterWindow, self.CharacterWindow.PlayerCharacter.Stats["Bonus Carrying Capacity Stat Modifier"], "Bonus Carrying Capacity Stat Modifier")

    def GainCoins(self):
        GainCoinsDialogInst = GainCoinsDialog(self.CharacterWindow)
        if GainCoinsDialogInst.Submitted:
            self.CPSpinBox.setValue(self.CharacterWindow.PlayerCharacter.Stats["Coins"]["CP"] + GainCoinsDialogInst.GainedCoins["CP"])
            self.SPSpinBox.setValue(self.CharacterWindow.PlayerCharacter.Stats["Coins"]["SP"] + GainCoinsDialogInst.GainedCoins["SP"])
            self.EPSpinBox.setValue(self.CharacterWindow.PlayerCharacter.Stats["Coins"]["EP"] + GainCoinsDialogInst.GainedCoins["EP"])
            self.GPSpinBox.setValue(self.CharacterWindow.PlayerCharacter.Stats["Coins"]["GP"] + GainCoinsDialogInst.GainedCoins["GP"])
            self.PPSpinBox.setValue(self.CharacterWindow.PlayerCharacter.Stats["Coins"]["PP"] + GainCoinsDialogInst.GainedCoins["PP"])

    def SpendCoins(self):
        SpendCoinsDialogInst = SpendCoinsDialog(self.CharacterWindow)
        if SpendCoinsDialogInst.Submitted:
            self.CPSpinBox.setValue(SpendCoinsDialogInst.RemainingCoins["CP"])
            self.SPSpinBox.setValue(SpendCoinsDialogInst.RemainingCoins["SP"])
            self.EPSpinBox.setValue(SpendCoinsDialogInst.RemainingCoins["EP"])
            self.GPSpinBox.setValue(SpendCoinsDialogInst.RemainingCoins["GP"])
            self.PPSpinBox.setValue(SpendCoinsDialogInst.RemainingCoins["PP"])

    def EditConsumptionRate(self, Consumed):
        ConsumedRate, OK = QInputDialog.getDouble(self.CharacterWindow, f"Edit {Consumed} Consumption Rate", f"{Consumed} consumption rate:", self.CharacterWindow.PlayerCharacter.Stats[f"{Consumed} Consumption Rate"], 0, 1000000000)
        if OK:
            self.CharacterWindow.UpdateStat(f"{Consumed} Consumption Rate", ConsumedRate)

    def AddItem(self):
        ItemIndex = self.CharacterWindow.PlayerCharacter.AddInventoryItem()
        self.CharacterWindow.UpdateDisplay()
        EditItemDialogInst = PlayerCharacterEditItemDialog(self.CharacterWindow, self.CharacterWindow.PlayerCharacter.Stats["Inventory"], ItemIndex, AddMode=True)
        if EditItemDialogInst.Cancelled:
            self.CharacterWindow.PlayerCharacter.DeleteLastInventoryItem()
            self.CharacterWindow.UpdateDisplay()
        else:
            self.CharacterWindow.UpdateUnsavedChangesFlag(True)
            self.InventoryTreeWidget.SelectIndex(ItemIndex)

    def DeleteItem(self):
        CurrentSelection = self.InventoryTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            if self.CharacterWindow.DisplayMessageBox("Are you sure you want to delete this item?  This cannot be undone.", Icon=QMessageBox.Icon.Warning, Buttons=(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)) == QMessageBox.StandardButton.Yes:
                CurrentItem = CurrentSelection[0]
                CurrentItemIndex = CurrentItem.Index
                self.CharacterWindow.PlayerCharacter.DeleteInventoryItem(CurrentItemIndex)
                self.CharacterWindow.UpdateUnsavedChangesFlag(True)
                InventoryLength = len(self.CharacterWindow.PlayerCharacter.Stats["Inventory"])
                if InventoryLength > 0:
                    self.InventoryTreeWidget.SelectIndex(CurrentItemIndex if CurrentItemIndex < InventoryLength else InventoryLength - 1)

    def EditItem(self):
        CurrentSelection = self.InventoryTreeWidget.selectedItems()
        if len(CurrentSelection) > 0:
            CurrentItem = CurrentSelection[0]
            CurrentItemIndex = CurrentItem.Index
            EditItemDialogInst = PlayerCharacterEditItemDialog(self.CharacterWindow, self.CharacterWindow.PlayerCharacter.Stats["Inventory"], CurrentItemIndex)
            if EditItemDialogInst.UnsavedChanges:
                self.CharacterWindow.UpdateUnsavedChangesFlag(True)
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
            if self.CharacterWindow.PlayerCharacter.MoveInventoryItem(CurrentItemIndex, Delta):
                self.CharacterWindow.UpdateUnsavedChangesFlag(True)
                self.InventoryTreeWidget.SelectIndex(CurrentItemIndex + Delta)
