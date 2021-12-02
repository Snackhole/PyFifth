import copy

from PyQt5 import QtCore
from PyQt5.QtWidgets import QComboBox, QDialog, QPushButton, QGridLayout, QLabel, QSizePolicy


class AlternateAbilityScoreSkillRollDialog(QDialog):
    def __init__(self, CharacterWindow):
        super().__init__(parent=CharacterWindow)

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Variables
        self.RollData = None
        self.AbilityScoreAbbreviations = {}
        self.AbilityScoreAbbreviations["Strength"] = "STR"
        self.AbilityScoreAbbreviations["Dexterity"] = "DEX"
        self.AbilityScoreAbbreviations["Constitution"] = "CON"
        self.AbilityScoreAbbreviations["Intelligence"] = "INT"
        self.AbilityScoreAbbreviations["Wisdom"] = "WIS"
        self.AbilityScoreAbbreviations["Charisma"] = "CHA"

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Prompt Label
        self.PromptLabel = QLabel("Roll a skill with an alternative ability score:")
        self.PromptLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Skills
        self.SkillsLabel = QLabel("Skill:")
        self.SkillsComboBox = QComboBox()
        self.SkillsComboBox.setSizePolicy(self.InputsSizePolicy)
        self.SkillsComboBox.setEditable(False)
        self.SkillsComboBox.addItems(self.CharacterWindow.PlayerCharacter.Skills)
        self.SkillsComboBox.currentTextChanged.connect(self.UpdateAbilityScoresComboBox)

        # Ability Scores
        self.AbilityScoresLabel = QLabel("Ability Score:")
        self.AbilityScoresComboBox = QComboBox()
        self.AbilityScoresComboBox.setSizePolicy(self.InputsSizePolicy)
        self.AbilityScoresComboBox.setEditable(False)

        # Buttons
        self.RollButton = QPushButton("Roll")
        self.RollButton.clicked.connect(self.Roll)
        self.CancelButton = QPushButton("Cancel")
        self.CancelButton.clicked.connect(self.Cancel)

        # Layout
        self.Layout = QGridLayout()
        self.Layout.addWidget(self.PromptLabel, 0, 0, 1, 2)
        self.Layout.addWidget(self.SkillsLabel, 1, 0)
        self.Layout.addWidget(self.SkillsComboBox, 1, 1)
        self.Layout.addWidget(self.AbilityScoresLabel, 2, 0)
        self.Layout.addWidget(self.AbilityScoresComboBox, 2, 1)
        self.ButtonsLayout = QGridLayout()
        self.ButtonsLayout.addWidget(self.RollButton, 0, 0)
        self.ButtonsLayout.addWidget(self.CancelButton, 0, 1)
        self.Layout.addLayout(self.ButtonsLayout, 3, 0, 1, 2)
        for Row in [1, 2]:
            self.Layout.setRowStretch(Row, 1)
        self.Layout.setColumnStretch(1, 1)
        self.setLayout(self.Layout)

        # Set Window Title and Icon
        self.setWindowTitle(self.CharacterWindow.ScriptName)
        self.setWindowIcon(self.CharacterWindow.WindowIcon)

        # Update Ability Scores Combo Box
        self.UpdateAbilityScoresComboBox()

        # Execute Dialog
        self.exec_()

    def UpdateAbilityScoresComboBox(self):
        Skill = self.SkillsComboBox.currentText()
        Abilities = copy.copy(self.CharacterWindow.PlayerCharacter.Abilities)
        SkillAssociatedAbility = self.CharacterWindow.PlayerCharacter.SkillsAssociatedAbilities[Skill]
        Abilities.remove(SkillAssociatedAbility)
        self.AbilityScoresComboBox.clear()
        self.AbilityScoresComboBox.addItems(Abilities)

    def Roll(self):
        # Get Inputs
        Skill = self.SkillsComboBox.currentText()
        Ability = self.AbilityScoresComboBox.currentText()

        # Get Ability Abbreviation
        AbilityAbbreviation = self.AbilityScoreAbbreviations[Ability]

        # Create Roll Data
        self.RollData = {}

        # Roll Data Prefix
        self.RollData["Prefix"] = Skill + " (" + AbilityAbbreviation + ") Check:\n"

        # Roll Data Stat Modifier
        self.RollData["Stat Modifier"] = self.CharacterWindow.PlayerCharacter.CreateStatModifier()
        self.RollData["Stat Modifier"][Ability + " Multiplier"] = 1
        SkillStatModifier = self.CharacterWindow.PlayerCharacter.Stats["Skills"][Skill + " Stat Modifier"]
        self.RollData["Stat Modifier"]["Proficiency Multiplier"] = SkillStatModifier["Proficiency Multiplier"]
        self.RollData["Stat Modifier"]["Proficiency Multiplier Round Up"] = SkillStatModifier["Proficiency Multiplier Round Up"]
        self.RollData["Stat Modifier"]["Proficiency Min"] = SkillStatModifier["Proficiency Min"]
        self.RollData["Stat Modifier"]["Proficiency Max"] = SkillStatModifier["Proficiency Max"]

        # Close Dialog
        self.close()

    def Cancel(self):
        self.close()
