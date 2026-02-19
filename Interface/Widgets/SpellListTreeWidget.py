from PyQt6 import QtCore
from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QHeaderView


class SpellListTreeWidget(QTreeWidget):
    def __init__(self, CharacterWindow):
        super().__init__()

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Header Setup
        self.setRootIsDecorated(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.setColumnCount(3)
        self.setHeaderLabels(["Prep.", "Name", "Level"])

    def FillFromSpellList(self):
        self.clear()
        for SpellIndex in range(len(self.CharacterWindow.PlayerCharacter.Stats["Spell List"])):
            self.invisibleRootItem().addChild(SpellListWidgetItem(SpellIndex, self.CharacterWindow.PlayerCharacter.Stats["Spell List"][SpellIndex]))

    def SelectIndex(self, Index):
        DestinationIndex = self.model().index(Index, 0)
        self.setCurrentIndex(DestinationIndex)
        self.scrollToItem(self.currentItem(), self.ScrollHint.PositionAtCenter)
        self.horizontalScrollBar().setValue(0)


class SpellListWidgetItem(QTreeWidgetItem):
    def __init__(self, Index, Spell):
        super().__init__()

        # Store Parameters
        self.Index = Index
        self.Spell = Spell

        # Variables
        self.PreparedText = "\u2713" if self.Spell["Spell Prepared"] else ""
        self.NameText = self.Spell["Spell Name"]
        self.LevelText = self.Spell["Spell Level"] if self.Spell["Spell Level"] != "" else ""
        self.ColumnTextList = [self.PreparedText, self.NameText, self.LevelText]

        # Set Text
        for Column in range(len(self.ColumnTextList)):
            self.setText(Column, self.ColumnTextList[Column])
            self.setToolTip(Column, self.ColumnTextList[Column])

        # Set Alignment
        for Column in range(len(self.ColumnTextList) - 1):
            self.setTextAlignment(Column, QtCore.Qt.AlignmentFlag.AlignCenter)
