from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QHeaderView


class PresetRollsTreeWidget(QTreeWidget):
    def __init__(self, CharacterWindow):
        super().__init__()

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Header Setup
        self.setHeaderHidden(True)
        self.setRootIsDecorated(False)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)

    def FillFromPresetRolls(self):
        self.clear()
        Character = self.CharacterWindow.GetCharacter()
        for PresetRollIndex in range(len(Character.Stats["Dice Roller"].PresetRolls)):
            self.invisibleRootItem().addChild(PresetRollsWidgetItem(PresetRollIndex, Character.Stats["Dice Roller"].PresetRolls[PresetRollIndex], Character))

    def SelectIndex(self, Index):
        DestinationIndex = self.model().index(Index, 0)
        self.setCurrentIndex(DestinationIndex)
        self.scrollToItem(self.currentItem(), self.PositionAtCenter)
        self.horizontalScrollBar().setValue(0)


class PresetRollsWidgetItem(QTreeWidgetItem):
    def __init__(self, Index, PresetRoll, Character):
        super().__init__()

        # Store Parameters
        self.Index = Index
        self.PresetRoll = PresetRoll
        self.Character = Character

        # Variables
        self.Modifier = self.Character.CalculateStatModifier(self.PresetRoll["Modifier"])
        self.Sign = "" if self.Modifier < 0 else "+"
        self.ModifierString = self.Sign + str(self.Modifier)

        # Set Text
        self.setText(0, self.PresetRoll["Name"] + " (" + str(self.PresetRoll["Dice Number"]) + "d" + str(self.PresetRoll["Die Type"]) + self.ModifierString + ")")
        self.setToolTip(0, self.PresetRoll["Name"] + " (" + str(self.PresetRoll["Dice Number"]) + "d" + str(self.PresetRoll["Die Type"]) + self.ModifierString + ")")
