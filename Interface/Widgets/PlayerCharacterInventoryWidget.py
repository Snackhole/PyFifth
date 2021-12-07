from PyQt5 import QtCore
from PyQt5.QtWidgets import QDoubleSpinBox, QFrame, QGridLayout, QInputDialog, QLabel, QSizePolicy, QSpinBox

from Interface.Dialogs.GainCoinsDialog import GainCoinsDialog
from Interface.Dialogs.SpendCoinsDialog import SpendCoinsDialog
from Interface.Widgets.IconButtons import AddButton, DeleteButton, EditButton


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
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Create Carrying Capacity
        self.CreateCarryingCapacity()

        # Create Loads and Values
        self.CreateLoadsAndValues()

        # Create Coins
        self.CreateCoins()

        # Create Food and Water
        self.CreateFoodAndWater()

        # Create and Set Layout
        self.CreateAndSetLayout()

    def CreateCarryingCapacity(self):
        # Carrying Capacity Label
        self.CarryingCapacityLabel = QLabel("Carrying Capacity")
        self.CarryingCapacityLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.CarryingCapacityLabel.setStyleSheet(self.SectionLabelStyle)
        self.CarryingCapacityLabel.setMargin(self.HeaderLabelMargin)

        # Carrying Capacity Spin Box
        self.CarryingCapacitySpinBox = QSpinBox()
        self.CarryingCapacitySpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.CarryingCapacitySpinBox.setStyleSheet(self.CarryingCapacityStyle)
        self.CarryingCapacitySpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CarryingCapacitySpinBox.setButtonSymbols(self.CarryingCapacitySpinBox.NoButtons)
        self.CarryingCapacitySpinBox.setRange(0, 1000000000)
        self.CarryingCapacitySpinBox.setReadOnly(True)

        # Carrying Capacity Edit Button
        self.CarryingCapacityEditButton = EditButton(self.EditBonusCarryingCapacityStatModifier, "Edit Bonus Carrying Capacity Stat Modifier")
        self.CarryingCapacityEditButton.setSizePolicy(self.InputsSizePolicy)

    def CreateLoadsAndValues(self):
        # Loads and Values Label
        self.LoadsAndValuesLabel = QLabel("Loads and Values")
        self.LoadsAndValuesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.LoadsAndValuesLabel.setStyleSheet(self.SectionLabelStyle)
        self.LoadsAndValuesLabel.setMargin(self.HeaderLabelMargin)

        # Header Labels
        self.LoadsLabel = QLabel("Loads (lbs.)")
        self.LoadsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.LoadsLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.LoadsLabel.setMargin(5)
        self.ValuesLabel = QLabel("Values (GP)")
        self.ValuesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ValuesLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.ValuesLabel.setMargin(5)

        # Tags Labels
        self.TotalLabel = QLabel("Total")
        self.TotalLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.TotalLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.TotalLabel.setMargin(5)
        self.GearLabel = QLabel("Gear")
        self.GearLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.GearLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.GearLabel.setMargin(5)
        self.TreasureLabel = QLabel("Treasure")
        self.TreasureLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.TreasureLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.TreasureLabel.setMargin(5)
        self.MiscLabel = QLabel("Misc.")
        self.MiscLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MiscLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.MiscLabel.setMargin(5)

        # Loads Spin Boxes
        self.TotalLoadSpinBox = QDoubleSpinBox()
        self.TotalLoadSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.TotalLoadSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.TotalLoadSpinBox.setButtonSymbols(self.TotalLoadSpinBox.NoButtons)
        self.TotalLoadSpinBox.setRange(0, 1000000000)
        self.TotalLoadSpinBox.setReadOnly(True)
        self.GearLoadSpinBox = QDoubleSpinBox()
        self.GearLoadSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.GearLoadSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.GearLoadSpinBox.setButtonSymbols(self.GearLoadSpinBox.NoButtons)
        self.GearLoadSpinBox.setRange(0, 1000000000)
        self.GearLoadSpinBox.setReadOnly(True)
        self.TreasureLoadSpinBox = QDoubleSpinBox()
        self.TreasureLoadSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.TreasureLoadSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.TreasureLoadSpinBox.setButtonSymbols(self.TreasureLoadSpinBox.NoButtons)
        self.TreasureLoadSpinBox.setRange(0, 1000000000)
        self.TreasureLoadSpinBox.setReadOnly(True)
        self.MiscLoadSpinBox = QDoubleSpinBox()
        self.MiscLoadSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MiscLoadSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MiscLoadSpinBox.setButtonSymbols(self.MiscLoadSpinBox.NoButtons)
        self.MiscLoadSpinBox.setRange(0, 1000000000)
        self.MiscLoadSpinBox.setReadOnly(True)

        # Values Spin Boxes
        self.TotalValueSpinBox = QDoubleSpinBox()
        self.TotalValueSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.TotalValueSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.TotalValueSpinBox.setButtonSymbols(self.TotalValueSpinBox.NoButtons)
        self.TotalValueSpinBox.setRange(0, 1000000000)
        self.TotalValueSpinBox.setReadOnly(True)
        self.GearValueSpinBox = QDoubleSpinBox()
        self.GearValueSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.GearValueSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.GearValueSpinBox.setButtonSymbols(self.GearValueSpinBox.NoButtons)
        self.GearValueSpinBox.setRange(0, 1000000000)
        self.GearValueSpinBox.setReadOnly(True)
        self.TreasureValueSpinBox = QDoubleSpinBox()
        self.TreasureValueSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.TreasureValueSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.TreasureValueSpinBox.setButtonSymbols(self.TreasureValueSpinBox.NoButtons)
        self.TreasureValueSpinBox.setRange(0, 1000000000)
        self.TreasureValueSpinBox.setReadOnly(True)
        self.MiscValueSpinBox = QDoubleSpinBox()
        self.MiscValueSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MiscValueSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MiscValueSpinBox.setButtonSymbols(self.MiscValueSpinBox.NoButtons)
        self.MiscValueSpinBox.setRange(0, 1000000000)
        self.MiscValueSpinBox.setReadOnly(True)

    def CreateCoins(self):
        # Coins Label
        self.CoinsLabel = QLabel("Coins")
        self.CoinsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.CoinsLabel.setStyleSheet(self.SectionLabelStyle)
        self.CoinsLabel.setMargin(self.HeaderLabelMargin)

        # Coins Header Labels
        self.CPLabel = QLabel("CP")
        self.CPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.CPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.CPLabel.setMargin(5)
        self.SPLabel = QLabel("SP")
        self.SPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.SPLabel.setMargin(5)
        self.EPLabel = QLabel("EP")
        self.EPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.EPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.EPLabel.setMargin(5)
        self.GPLabel = QLabel("GP")
        self.GPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.GPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.GPLabel.setMargin(5)
        self.PPLabel = QLabel("PP")
        self.PPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.PPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.PPLabel.setMargin(5)

        # Coins Spin Boxes
        self.CPSpinBox = QSpinBox()
        self.CPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.CPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CPSpinBox.setButtonSymbols(self.CPSpinBox.NoButtons)
        self.CPSpinBox.setRange(0, 1000000000)
        self.CPSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Coins", "CP"), self.CPSpinBox.value()))
        self.SPSpinBox = QSpinBox()
        self.SPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.SPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SPSpinBox.setButtonSymbols(self.SPSpinBox.NoButtons)
        self.SPSpinBox.setRange(0, 1000000000)
        self.SPSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Coins", "SP"), self.SPSpinBox.value()))
        self.EPSpinBox = QSpinBox()
        self.EPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.EPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.EPSpinBox.setButtonSymbols(self.EPSpinBox.NoButtons)
        self.EPSpinBox.setRange(0, 1000000000)
        self.EPSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Coins", "EP"), self.EPSpinBox.value()))
        self.GPSpinBox = QSpinBox()
        self.GPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.GPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.GPSpinBox.setButtonSymbols(self.GPSpinBox.NoButtons)
        self.GPSpinBox.setRange(0, 1000000000)
        self.GPSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Coins", "GP"), self.GPSpinBox.value()))
        self.PPSpinBox = QSpinBox()
        self.PPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.PPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.PPSpinBox.setButtonSymbols(self.PPSpinBox.NoButtons)
        self.PPSpinBox.setRange(0, 1000000000)
        self.PPSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Coins", "PP"), self.PPSpinBox.value()))

        # Coins Buttons
        self.GainCoinsButton = AddButton(self.GainCoins, "Gain Coins")
        self.SpendCoinsButton = DeleteButton(self.SpendCoins, "Spend Coins")

        # Coin Value
        self.CoinValueLabel = QLabel("Coin Value (GP)")
        self.CoinValueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.CoinValueLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.CoinValueLabel.setMargin(5)
        self.CoinValueSpinBox = QDoubleSpinBox()
        self.CoinValueSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.CoinValueSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CoinValueSpinBox.setButtonSymbols(self.CoinValueSpinBox.NoButtons)
        self.CoinValueSpinBox.setRange(0, 1000000000)
        self.CoinValueSpinBox.setReadOnly(True)

        # Coin Load
        self.CoinLoadLabel = QLabel("Coin Load (lbs.)")
        self.CoinLoadLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.CoinLoadLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.CoinLoadLabel.setMargin(5)
        self.CoinLoadSpinBox = QDoubleSpinBox()
        self.CoinLoadSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.CoinLoadSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CoinLoadSpinBox.setButtonSymbols(self.CoinLoadSpinBox.NoButtons)
        self.CoinLoadSpinBox.setRange(0, 1000000000)
        self.CoinLoadSpinBox.setReadOnly(True)

    def CreateFoodAndWater(self):
        # Food and Water Label
        self.FoodAndWaterLabel = QLabel("Food and Water")
        self.FoodAndWaterLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.FoodAndWaterLabel.setStyleSheet(self.SectionLabelStyle)
        self.FoodAndWaterLabel.setMargin(self.HeaderLabelMargin)

        # Header Labels
        self.FoodAndWaterLoadLabel = QLabel("Load (lbs.)")
        self.FoodAndWaterLoadLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.FoodAndWaterLoadLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.FoodAndWaterLoadLabel.setMargin(5)
        self.FoodAndWaterDaysLabel = QLabel("Days")
        self.FoodAndWaterDaysLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.FoodAndWaterDaysLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.FoodAndWaterDaysLabel.setMargin(5)

        # Tags Labels
        self.FoodLabel = QLabel("Food")
        self.FoodLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.FoodLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.FoodLabel.setMargin(5)
        self.WaterLabel = QLabel("Water")
        self.WaterLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.WaterLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.WaterLabel.setMargin(5)

        # Loads Spin Boxes
        self.FoodLoadSpinBox = QDoubleSpinBox()
        self.FoodLoadSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.FoodLoadSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.FoodLoadSpinBox.setButtonSymbols(self.FoodLoadSpinBox.NoButtons)
        self.FoodLoadSpinBox.setRange(0, 1000000000)
        self.FoodLoadSpinBox.setReadOnly(True)
        self.WaterLoadSpinBox = QDoubleSpinBox()
        self.WaterLoadSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.WaterLoadSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.WaterLoadSpinBox.setButtonSymbols(self.WaterLoadSpinBox.NoButtons)
        self.WaterLoadSpinBox.setRange(0, 1000000000)
        self.WaterLoadSpinBox.setReadOnly(True)

        # Days Spin Boxes
        self.FoodDaysSpinBox = QDoubleSpinBox()
        self.FoodDaysSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.FoodDaysSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.FoodDaysSpinBox.setButtonSymbols(self.FoodDaysSpinBox.NoButtons)
        self.FoodDaysSpinBox.setRange(0, 1000000000)
        self.FoodDaysSpinBox.setReadOnly(True)
        self.WaterDaysSpinBox = QDoubleSpinBox()
        self.WaterDaysSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.WaterDaysSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.WaterDaysSpinBox.setButtonSymbols(self.WaterDaysSpinBox.NoButtons)
        self.WaterDaysSpinBox.setRange(0, 1000000000)
        self.WaterDaysSpinBox.setReadOnly(True)

        # Days Buttons
        self.FoodDaysEditButton = EditButton(lambda: self.EditConsumptionRate("Food"), "Edit Food Consumption Rate")
        self.FoodDaysEditButton.setSizePolicy(self.InputsSizePolicy)
        self.WaterDaysEditButton = EditButton(lambda: self.EditConsumptionRate("Water"), "Edit Water Consumption Rate")
        self.WaterDaysEditButton.setSizePolicy(self.InputsSizePolicy)

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

    # TODO dialog for spending coins
    def SpendCoins(self):
        SpendCoinsDialogInst = SpendCoinsDialog(self.CharacterWindow)
        if SpendCoinsDialogInst.Submitted:
            self.CPSpinBox.setValue(SpendCoinsDialogInst.RemainingCoins["CP"])
            self.SPSpinBox.setValue(SpendCoinsDialogInst.RemainingCoins["SP"])
            self.EPSpinBox.setValue(SpendCoinsDialogInst.RemainingCoins["EP"])
            self.GPSpinBox.setValue(SpendCoinsDialogInst.RemainingCoins["GP"])
            self.PPSpinBox.setValue(SpendCoinsDialogInst.RemainingCoins["PP"])

    def EditConsumptionRate(self, Consumed):
        ConsumedRate, OK = QInputDialog.getDouble(self.CharacterWindow, "Edit " + Consumed + " Consumption Rate", Consumed + " consumption rate:", self.CharacterWindow.PlayerCharacter.Stats[Consumed + " Consumption Rate"], 0, 1000000000)
        if OK:
            self.CharacterWindow.UpdateStat(Consumed + " Consumption Rate", ConsumedRate)
