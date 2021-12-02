from PyQt5 import QtCore
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QHeaderView


class SpellListTreeWidget(QTreeWidget):
    def __init__(self, CharacterWindow):
        super().__init__()

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Header Setup
        self.setHeaderHidden(True)
        self.setRootIsDecorated(False)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)

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

        # Set Text
        self.setText(0, self.Spell["Spell Name"])
        self.setToolTip(0, self.Spell["Spell Name"])

        # Set Check State
        self.setCheckState(self.Spell["Spell Prepared"])

        # Check State Read Only
        self.setFlags(QtCore.Qt.ItemIsSelectable)
