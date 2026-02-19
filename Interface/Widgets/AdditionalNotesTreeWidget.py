from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QHeaderView


class AdditionalNotesTreeWidget(QTreeWidget):
    def __init__(self, CharacterWindow):
        super().__init__()

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Header Setup
        self.setHeaderHidden(True)
        self.setRootIsDecorated(False)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    def FillFromAdditionalNotes(self):
        self.clear()
        for AdditionalNoteIndex in range(len(self.CharacterWindow.PlayerCharacter.Stats["Additional Notes"])):
            self.invisibleRootItem().addChild(AdditionalNotesWidgetItem(AdditionalNoteIndex, self.CharacterWindow.PlayerCharacter.Stats["Additional Notes"][AdditionalNoteIndex]))

    def SelectIndex(self, Index):
        DestinationIndex = self.model().index(Index, 0)
        self.setCurrentIndex(DestinationIndex)
        self.scrollToItem(self.currentItem(), self.ScrollHint.PositionAtCenter)
        self.horizontalScrollBar().setValue(0)


class AdditionalNotesWidgetItem(QTreeWidgetItem):
    def __init__(self, Index, AdditionalNote):
        super().__init__()

        # Store Parameters
        self.Index = Index
        self.AdditionalNote = AdditionalNote

        # Set Text
        self.setText(0, self.AdditionalNote["Note Name"])
        self.setToolTip(0, self.AdditionalNote["Note Name"])
