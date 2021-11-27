from PyQt5 import QtCore
from PyQt5.QtWidgets import QComboBox, QFrame, QGridLayout, QLabel

from Interface.Widgets.CenteredLineEdit import CenteredLineEdit
from Interface.Widgets.EditButton import EditButton
from Interface.Widgets.RollButton import RollButton


class AbilityScoreDerivativeWidget(QFrame):
    def __init__(self, Parent, CharacterWindow, Index):
        super().__init__(parent=Parent)

        # Store Parameters
        self.Parent = Parent
        self.CharacterWindow = CharacterWindow
        self.Index = Index

        # Ability
        self.AbilityLabel = QLabel("Ability:")
        self.AbilityLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.AbilityComboBox = QComboBox()
        self.AbilityComboBox.setSizePolicy(self.Parent.InputsSizePolicy)
        self.AbilityComboBox.setEditable(False)
        self.AbilityComboBox.addItems(["", "Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"])
        self.AbilityComboBox.currentTextChanged.connect(self.UpdateAbility)

        # Save DC
        self.SaveDCLabel = QLabel("Save DC:")
        self.SaveDCLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.SaveDCLineEdit = CenteredLineEdit()
        self.SaveDCLineEdit.setSizePolicy(self.Parent.InputsSizePolicy)
        self.SaveDCLineEdit.setText("N/A")
        self.SaveDCLineEdit.setReadOnly(True)

        self.SaveDCEditButton = EditButton(self.EditSaveDC, "Edit Save DC")
        self.SaveDCEditButton.setSizePolicy(self.Parent.InputsSizePolicy)

        # Attack Modifier
        self.AttackModifierLabel = QLabel("Attack Modifier:")
        self.AttackModifierLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.AttackModifierLineEdit = CenteredLineEdit()
        self.AttackModifierLineEdit.setSizePolicy(self.Parent.InputsSizePolicy)
        self.AttackModifierLineEdit.setText("N/A")
        self.AttackModifierLineEdit.setReadOnly(True)

        self.AttackModifierRollButton = RollButton(self.RollAttackModifier, "Roll Attack Modifier")
        self.AttackModifierRollButton.setSizePolicy(self.Parent.InputsSizePolicy)

        self.AttackModifierEditButton = EditButton(self.EditAttackModifier, "Edit Attack Modifier")
        self.AttackModifierEditButton.setSizePolicy(self.Parent.InputsSizePolicy)

        # Layout
        self.Layout = QGridLayout()
        self.Layout.addWidget(self.AbilityLabel, 0, 0)
        self.Layout.addWidget(self.AbilityComboBox, 0, 1, 1, 3)
        self.Layout.addWidget(self.SaveDCLabel, 1, 0)
        self.Layout.addWidget(self.SaveDCLineEdit, 1, 1, 1, 2)
        self.Layout.addWidget(self.SaveDCEditButton, 1, 3)
        self.Layout.addWidget(self.AttackModifierLabel, 2, 0)
        self.Layout.addWidget(self.AttackModifierLineEdit, 2, 1)
        self.Layout.addWidget(self.AttackModifierRollButton, 2, 2)
        self.Layout.addWidget(self.AttackModifierEditButton, 2, 3)
        self.Layout.setColumnStretch(0, 2)
        for Row in [1, 2]:
            self.Layout.setRowStretch(Row, 1)
        self.setLayout(self.Layout)

    def UpdateAbility(self):
        Ability = self.AbilityComboBox.currentText()
        self.CharacterWindow.PlayerCharacter.Stats["Ability Score Derivatives"]["Ability Score Derivatives Displayed"][self.Index] = Ability
        if not self.CharacterWindow.UpdatingFieldsFromPlayerCharacter:
            self.CharacterWindow.UpdateUnsavedChangesFlag(True)

    def EditSaveDC(self):
        Ability = self.CharacterWindow.PlayerCharacter.Stats["Ability Score Derivatives"]["Ability Score Derivatives Displayed"][self.Index]
        if Ability != "":
            self.CharacterWindow.EditStatModifier(self, self.CharacterWindow.PlayerCharacter.Stats["Ability Score Derivatives"][Ability + " Save DC Stat Modifier"], Ability + " Save DC Stat Modifier")

    def RollAttackModifier(self):
        Ability = self.CharacterWindow.PlayerCharacter.Stats["Ability Score Derivatives"]["Ability Score Derivatives Displayed"][self.Index]
        if Ability != "":
            self.CharacterWindow.PlayerCharacter.Stats["Dice Roller"].RollDice(1, 20, self.CharacterWindow.PlayerCharacter.Stats["Ability Score Derivatives"][Ability + " Attack Modifier Stat Modifier"], LogPrefix=Ability + " Attack:\n")
            self.CharacterWindow.UpdateUnsavedChangesFlag(True)

    def EditAttackModifier(self):
        Ability = self.CharacterWindow.PlayerCharacter.Stats["Ability Score Derivatives"]["Ability Score Derivatives Displayed"][self.Index]
        if Ability != "":
            self.CharacterWindow.EditStatModifier(self, self.CharacterWindow.PlayerCharacter.Stats["Ability Score Derivatives"][Ability + " Attack Modifier Stat Modifier"], Ability + " Attack Modifier Stat Modifier")
