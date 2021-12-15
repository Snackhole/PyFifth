import copy

from PyQt5 import QtCore
from PyQt5.QtWidgets import QComboBox, QDialog, QDoubleSpinBox, QLabel, QLineEdit, QMessageBox, QPushButton, QGridLayout, QSpinBox

from Interface.Widgets.IndentingTextEdit import IndentingTextEdit


class PlayerCharacterEditItemDialog(QDialog):
    def __init__(self, CharacterWindow, Inventory, ItemIndex, AddMode=False):
        super().__init__(parent=CharacterWindow)

        # Store Parameters
        self.CharacterWindow = CharacterWindow
        self.Inventory = Inventory
        self.ItemIndex = ItemIndex

        # Variables
        self.Item = self.Inventory[self.ItemIndex]
        self.ItemOriginalState = copy.deepcopy(self.Item)
        self.UnsavedChanges = False
        self.Cancelled = False

        # Prompt Label
        self.PromptLabel = QLabel("Add this item:" if AddMode else "Edit this item:")
        self.PromptLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Item Name
        self.ItemNameLabel = QLabel("Name:")
        self.ItemNameLineEdit = QLineEdit()
        self.ItemNameLineEdit.setText(self.Item["Item Name"])
        self.ItemNameLineEdit.textChanged.connect(self.UpdateItem)

        # Item Category
        self.ItemCategoryLabel = QLabel("Category:")
        self.ItemCategoryLineEdit = QLineEdit()
        self.ItemCategoryLineEdit.setText(self.Item["Item Category"])
        self.ItemCategoryLineEdit.textChanged.connect(self.UpdateItem)

        # Item Rarity
        self.ItemRarityLabel = QLabel("Rarity:")
        self.ItemRarityLineEdit = QLineEdit()
        self.ItemRarityLineEdit.setText(self.Item["Item Rarity"])
        self.ItemRarityLineEdit.textChanged.connect(self.UpdateItem)

        # Item Count
        self.ItemCountLabel = QLabel("Count:")
        self.ItemCountLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ItemCountSpinBox = QSpinBox()
        self.ItemCountSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ItemCountSpinBox.setButtonSymbols(self.ItemCountSpinBox.NoButtons)
        self.ItemCountSpinBox.setRange(1, 1000000000)
        self.ItemCountSpinBox.setValue(self.Item["Item Count"])
        self.ItemCountSpinBox.valueChanged.connect(self.UpdateItem)

        # Item Unit Weight
        self.ItemUnitWeightLabel = QLabel("Unit Weight:")
        self.ItemUnitWeightLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ItemUnitWeightSpinBox = QDoubleSpinBox()
        self.ItemUnitWeightSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ItemUnitWeightSpinBox.setButtonSymbols(self.ItemUnitWeightSpinBox.NoButtons)
        self.ItemUnitWeightSpinBox.setRange(0, 1000000000)
        self.ItemUnitWeightSpinBox.setSuffix(" lbs.")
        self.ItemUnitWeightSpinBox.setValue(self.Item["Item Unit Weight"])
        self.ItemUnitWeightSpinBox.valueChanged.connect(self.UpdateItem)

        # Item Unit Value
        self.ItemUnitValueLabel = QLabel("Unit Value:")
        self.ItemUnitValueLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ItemUnitValueSpinBox = QDoubleSpinBox()
        self.ItemUnitValueSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ItemUnitValueSpinBox.setButtonSymbols(self.ItemUnitValueSpinBox.NoButtons)
        self.ItemUnitValueSpinBox.setRange(0, 1000000000)
        self.ItemUnitValueSpinBox.setValue(self.Item["Item Unit Value"])
        self.ItemUnitValueSpinBox.valueChanged.connect(self.UpdateItem)
        self.ItemUnitValueDenominationComboBox = QComboBox()
        self.ItemUnitValueDenominationComboBox.setEditable(False)
        self.ItemUnitValueDenominationComboBox.addItems(["CP", "SP", "EP", "GP", "PP"])
        self.ItemUnitValueDenominationComboBox.setCurrentText(self.Item["Item Unit Value Denomination"])
        self.ItemUnitValueDenominationComboBox.currentTextChanged.connect(self.UpdateItem)

        # Item Tag
        self.ItemTagLabel = QLabel("Tag:")
        self.ItemTagLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ItemTagComboBox = QComboBox()
        self.ItemTagComboBox.setEditable(False)
        self.ItemTagComboBox.addItems(["", "Gear", "Food", "Water", "Treasure", "Misc."])
        self.ItemTagComboBox.setCurrentText(self.Item["Item Tag"])
        self.ItemTagComboBox.currentTextChanged.connect(self.UpdateItem)

        # Item Description
        self.ItemDescriptionLabel = QLabel("Description:")
        self.ItemDescriptionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ItemDescriptionTextEdit = IndentingTextEdit(TextChangedSlot=self.UpdateItem)
        self.ItemDescriptionTextEdit.setTabChangesFocus(True)
        self.ItemDescriptionTextEdit.setPlainText(self.Item["Item Description"])

        # Buttons
        self.DoneButton = QPushButton("Done")
        self.DoneButton.clicked.connect(self.Done)
        self.CancelButton = QPushButton("Cancel")
        self.CancelButton.clicked.connect(self.Cancel)

        # Layout
        self.Layout = QGridLayout()

        self.Layout.addWidget(self.PromptLabel, 0, 0)

        self.ItemInputsLayout = QGridLayout()
        self.ItemInputsLayout.addWidget(self.ItemNameLabel, 0, 0)
        self.ItemInputsLayout.addWidget(self.ItemNameLineEdit, 0, 1)
        self.ItemInputsLayout.addWidget(self.ItemCategoryLabel, 1, 0)
        self.ItemInputsLayout.addWidget(self.ItemCategoryLineEdit, 1, 1)
        self.ItemInputsLayout.addWidget(self.ItemRarityLabel, 2, 0)
        self.ItemInputsLayout.addWidget(self.ItemRarityLineEdit, 2, 1)
        self.ItemCalculationInputsLayout = QGridLayout()
        self.ItemCalculationInputsLayout.addWidget(self.ItemCountLabel, 0, 0)
        self.ItemCalculationInputsLayout.addWidget(self.ItemUnitWeightLabel, 0, 1)
        self.ItemCalculationInputsLayout.addWidget(self.ItemUnitValueLabel, 0, 2, 1, 2)
        self.ItemCalculationInputsLayout.addWidget(self.ItemTagLabel, 0, 4)
        self.ItemCalculationInputsLayout.addWidget(self.ItemCountSpinBox, 1, 0)
        self.ItemCalculationInputsLayout.addWidget(self.ItemUnitWeightSpinBox, 1, 1)
        self.ItemCalculationInputsLayout.addWidget(self.ItemUnitValueSpinBox, 1, 2)
        self.ItemCalculationInputsLayout.addWidget(self.ItemUnitValueDenominationComboBox, 1, 3)
        self.ItemCalculationInputsLayout.addWidget(self.ItemTagComboBox, 1, 4)
        for Column in range(3):
            self.ItemCalculationInputsLayout.setColumnStretch(Column, 1)
        self.ItemInputsLayout.addLayout(self.ItemCalculationInputsLayout, 3, 0, 1, 2)
        self.ItemInputsLayout.addWidget(self.ItemDescriptionLabel, 4, 0, 1, 2)
        self.ItemInputsLayout.addWidget(self.ItemDescriptionTextEdit, 5, 0, 1, 2)
        self.Layout.addLayout(self.ItemInputsLayout, 1, 0)

        self.ButtonsLayout = QGridLayout()
        self.ButtonsLayout.addWidget(self.DoneButton, 0, 0)
        self.ButtonsLayout.addWidget(self.CancelButton, 0, 1)
        self.Layout.addLayout(self.ButtonsLayout, 2, 0)

        self.Layout.setRowStretch(1, 1)

        self.setLayout(self.Layout)

        # Set Window Title and Icon
        self.setWindowTitle(self.CharacterWindow.ScriptName)
        self.setWindowIcon(self.CharacterWindow.WindowIcon)

        # Select Text in Name Line Edit
        self.ItemNameLineEdit.selectAll()

        # Execute Dialog
        self.exec_()

    def UpdateItem(self):
        if not self.ValidInput():
            return
        self.Item["Item Name"] = self.ItemNameLineEdit.text()
        self.Item["Item Category"] = self.ItemCategoryLineEdit.text()
        self.Item["Item Rarity"] = self.ItemRarityLineEdit.text()
        self.Item["Item Count"] = self.ItemCountSpinBox.value()
        self.Item["Item Unit Weight"] = self.ItemUnitWeightSpinBox.value()
        self.Item["Item Unit Value"] = self.ItemUnitValueSpinBox.value()
        self.Item["Item Unit Value Denomination"] = self.ItemUnitValueDenominationComboBox.currentText()
        self.Item["Item Tag"] = self.ItemTagComboBox.currentText()
        self.Item["Item Description"] = self.ItemDescriptionTextEdit.toPlainText()
        self.UnsavedChanges = True

    def Done(self):
        if self.ValidInput(Alert=True):
            self.close()

    def Cancel(self):
        self.Item.update(self.ItemOriginalState)
        self.UnsavedChanges = False
        self.Cancelled = True
        self.close()

    def ValidInput(self, Alert=False):
        if self.ItemNameLineEdit.text() == "":
            if Alert:
                self.CharacterWindow.DisplayMessageBox("Items must have a name.", Icon=QMessageBox.Warning, Parent=self)
            return False
        return True
