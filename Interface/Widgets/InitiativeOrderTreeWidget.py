from PyQt5 import QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QHeaderView


class InitiativeOrderTreeWidget(QTreeWidget):
    def __init__(self, EncounterWindow):
        super().__init__()

        # Store Parameters
        self.EncounterWindow = EncounterWindow

        # Header Setup
        self.setRootIsDecorated(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setColumnCount(6)
        self.setHeaderLabels(["Initiative", "Tie Priority", "Creature Name", "Conditions", "Location", "Notes"])

    def FillFromInitiativeOrder(self):
        self.clear()
        for EntryIndex in range(len(self.EncounterWindow.Encounter.EncounterData["Initiative Order"])):
            self.invisibleRootItem().addChild(InitiativeOrderWidgetItem(self.EncounterWindow, EntryIndex, self.EncounterWindow.Encounter.EncounterData["Initiative Order"][EntryIndex]))

    def SelectIndex(self, Index):
        DestinationIndex = self.model().index(Index, 0)
        self.setCurrentIndex(DestinationIndex)
        self.scrollToItem(self.currentItem(), self.PositionAtCenter)
        self.horizontalScrollBar().setValue(0)


class InitiativeOrderWidgetItem(QTreeWidgetItem):
    def __init__(self, EncounterWindow, Index, Entry):
        super().__init__()

        # Store Parameters
        self.EncounterWindow = EncounterWindow
        self.Index = Index
        self.Entry = Entry

        # Variables
        self.InitiativeText = str(Entry["Initiative"])
        self.TiePriorityText = str(Entry["Tie Priority"])
        self.CreatureNameText = Entry["Creature Name"]
        self.ConditionsText = Entry["Conditions"]
        self.LocationText = Entry["Location"]
        self.NotesText = Entry["Notes"]
        self.ColumnTextList = [self.InitiativeText, self.TiePriorityText, self.CreatureNameText, self.ConditionsText, self.LocationText, self.NotesText]

        # Set Text and Background Color
        for Column in range(len(self.ColumnTextList)):
            self.setText(Column, self.ColumnTextList[Column])
            self.setToolTip(Column, self.ColumnTextList[Column])
            if Entry["Turn Taken"] and Entry["Alive"]:
                self.setBackground(Column, QColor("darkblue"))
            elif not Entry["Alive"]:
                self.setBackground(Column, QColor("darkred"))

        # Set Alignment
        for Column in range(len(self.ColumnTextList) - 1):
            self.setTextAlignment(Column, QtCore.Qt.AlignCenter)
