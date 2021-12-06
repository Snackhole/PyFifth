from PyQt5 import QtCore
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QHeaderView


class SpellListTreeWidget(QTreeWidget):
    def __init__(self, CharacterWindow):
        super().__init__()

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Header Setup
        self.setRootIsDecorated(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setColumnCount(3)
        self.setHeaderLabels(["Prep.", "Name", "Level"])

    def FillFromSpellList(self):
        self.clear()
        for SpellIndex in range(len(self.CharacterWindow.PlayerCharacter.Stats["Spell List"])):
            self.invisibleRootItem().addChild(SpellListWidgetItem(SpellIndex, self.CharacterWindow.PlayerCharacter.Stats["Spell List"][SpellIndex]))

    def SelectIndex(self, Index):
        DestinationIndex = self.model().index(Index, 0)
        self.setCurrentIndex(DestinationIndex)
        self.scrollToItem(self.currentItem(), self.PositionAtCenter)
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

        # Set Text
        self.setText(0, self.PreparedText)
        self.setTextAlignment(0, QtCore.Qt.AlignCenter)
        self.setToolTip(0, self.PreparedText)
        self.setText(1, self.NameText)
        self.setToolTip(1, self.NameText)
        self.setText(2, self.LevelText)
        self.setToolTip(2, self.LevelText)
