from decimal import Decimal

from PyQt5.QtWidgets import QHeaderView, QTreeWidget, QTreeWidgetItem


class HoardInventoryTreeWidget(QTreeWidget):
    def __init__(self, HoardWindow):
        super().__init__()

        # Store Parameters
        self.HoardWindow = HoardWindow

        # Header Setup
        self.setRootIsDecorated(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setColumnCount(6)
        self.setHeaderLabels(["Name", "Count", "Unit Weight", "Unit Value", "Total Weight", "Total Value"])

    def FillFromInventory(self):
        self.clear()
        for ItemIndex in range(len(self.HoardWindow.Hoard.HoardData["Inventory"])):
            self.invisibleRootItem().addChild(HoardInventoryTreeWidgetItem(self.HoardWindow, ItemIndex, self.HoardWindow.Hoard.HoardData["Inventory"][ItemIndex]))

    def SelectIndex(self, Index):
        DestinationIndex = self.model().index(Index, 0)
        self.setCurrentIndex(DestinationIndex)
        self.scrollToItem(self.currentItem(), self.PositionAtCenter)
        self.horizontalScrollBar().setValue(0)


class HoardInventoryTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, HoardWindow, Index, Item):
        super().__init__()

        # Store Parameters
        self.HoardWindow = HoardWindow
        self.Index = Index
        self.Item = Item

        # Variables
        self.NameText = Item["Item Name"]
        self.CountText = str(Item["Item Count"])
        self.UnitWeightText = str(Item["Item Unit Weight"]) + " lbs."
        self.UnitValueText = str(Item["Item Unit Value"]) + " " + Item["Item Unit Value Denomination"]
        self.TotalWeightText = str(self.HoardWindow.Hoard.CalculateItemTotalLoadAndValue(self.Index)["Item Total Load"].quantize(Decimal("0.01"))) + " lbs."
        self.TotalValueText = str(self.HoardWindow.Hoard.CalculateItemTotalLoadAndValue(self.Index)["Item Total Value"].quantize(Decimal("0.01"))) + " GP"
        self.ColumnTextList = [self.NameText, self.CountText, self.UnitWeightText, self.UnitValueText, self.TotalWeightText, self.TotalValueText]
