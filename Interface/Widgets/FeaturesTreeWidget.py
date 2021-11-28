from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QHeaderView


class FeaturesTreeWidget(QTreeWidget):
    def __init__(self, CharacterWindow):
        super().__init__()

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Header Setup
        self.setHeaderHidden(True)
        self.setRootIsDecorated(False)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)

    def FillFromFeatures(self):
        self.clear()
        for FeatureIndex in range(len(self.CharacterWindow.PlayerCharacter.Stats["Features"])):
            self.invisibleRootItem().addChild(FeaturesWidgetItem(FeatureIndex, self.CharacterWindow.PlayerCharacter.Stats["Features"][FeatureIndex]))

    def SelectIndex(self, Index):
        DestinationIndex = self.model().index(Index, 0)
        self.setCurrentIndex(DestinationIndex)
        self.scrollToItem(self.currentItem(), self.PositionAtCenter)
        self.horizontalScrollBar().setValue(0)


class FeaturesWidgetItem(QTreeWidgetItem):
    def __init__(self, Index, Feature):
        super().__init__()

        # Store Parameters
        self.Index = Index
        self.Feature = Feature

        # Set Text
        self.setText(0, self.Feature["Feature Name"])
        self.setToolTip(0, self.Feature["Feature Name"])
