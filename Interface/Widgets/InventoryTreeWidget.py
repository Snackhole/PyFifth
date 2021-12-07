from decimal import Decimal

from PyQt5 import QtCore
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QHeaderView


class InventoryTreeWidget(QTreeWidget):
    def __init__(self, CharacterWindow):
        super().__init__()

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Header Setup
        self.setRootIsDecorated(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setColumnCount(7)
        self.setHeaderLabels(["Name", "Count", "Unit Weight", "Unit Value", "Total Weight", "Total Value", "Tag"])

    def FillFromInventory(self):
        self.clear()
        for ItemIndex in range(len(self.CharacterWindow.PlayerCharacter.Stats["Inventory"])):
            self.invisibleRootItem().addChild(InventoryWidgetItem(self.CharacterWindow, ItemIndex, self.CharacterWindow.PlayerCharacter.Stats["Inventory"][ItemIndex]))

    def SelectIndex(self, Index):
        DestinationIndex = self.model().index(Index, 0)
        self.setCurrentIndex(DestinationIndex)
        self.scrollToItem(self.currentItem(), self.PositionAtCenter)
        self.horizontalScrollBar().setValue(0)


class InventoryWidgetItem(QTreeWidgetItem):
    def __init__(self, CharacterWindow, Index, Item):
        super().__init__()

        # Store Parameters
        self.CharacterWindow = CharacterWindow
        self.Index = Index
        self.Item = Item

        # Variables
        self.NameText = Item["Item Name"]
        self.CountText = str(Item["Item Count"])
        self.UnitWeightText = str(Item["Item Unit Weight"]) + " lbs."
        self.UnitValueText = str(Item["Item Unit Value"]) + " " + Item["Item Unit Value Denomination"]
        self.TotalWeightText = str(self.CharacterWindow.PlayerCharacter.CalculateItemTotalWeightAndValue(self.Index)["Item Total Weight"].quantize(Decimal("0.01"))) + " lbs."
        self.TotalValueText = str(self.CharacterWindow.PlayerCharacter.CalculateItemTotalWeightAndValue(self.Index)["Item Total Value"].quantize(Decimal("0.01"))) + " GP"
        self.TagText = Item["Item Tag"]
        self.ColumnTextList = [self.NameText, self.CountText, self.UnitWeightText, self.UnitValueText, self.TotalWeightText, self.TotalValueText, self.TagText]

        # Set Text
        for Index in range(len(self.ColumnTextList)):
            self.setText(Index, self.ColumnTextList[Index])
            self.setToolTip(Index, self.ColumnTextList[Index])

        # Set Alignment
        for Index in range(1, 6):
            self.setTextAlignment(Index, QtCore.Qt.AlignCenter)
