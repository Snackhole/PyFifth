from PyQt5 import QtCore
from PyQt5.QtWidgets import QDoubleSpinBox, QFrame, QGridLayout, QLabel, QSizePolicy, QSpinBox

from Interface.Widgets.IconButtons import EditButton


class PlayerCharacterInventoryWidget(QFrame):
    def __init__(self, CharacterWindow):
        # Initialize Frame
        super().__init__()

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Styles
        self.SectionLabelStyle = "QLabel {font-size: 10pt; font-weight: bold;}"
        self.CarryingCapacityStyle = "QSpinBox {font-size: 16pt;}"
        self.TotalLoadsStyle = "QSpinBox {}"
        self.TotalLoadsEncumberedStyle = "QSpinBox {background-color: darkred;}"

        # Header Label Margin
        self.HeaderLabelMargin = 5

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Create Carrying Capacity
        self.CreateCarryingCapacity()

        # Create Loads and Values
        self.CreateLoadsAndValues()

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

        # Set Layout
        self.setLayout(self.Layout)

    def EditBonusCarryingCapacityStatModifier(self):
        self.CharacterWindow.EditStatModifier(self.CharacterWindow, self.CharacterWindow.PlayerCharacter.Stats["Bonus Carrying Capacity Stat Modifier"], "Bonus Carrying Capacity Stat Modifier")
