import copy

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QPushButton, QSpinBox, QSizePolicy, QTextEdit, QMessageBox

from Interface.Dialogs.EditModifierDialog import EditModifierDialog
from Interface.Dialogs.PointBuyAbilityScoresDialog import PointBuyAbilityScoresDialog
from Interface.Dialogs.RollForAbilityScoresDialog import RollForAbilityScoresDialog
from Interface.Widgets.IconButtons import EditButton


class EditAbilityScoresDialog(QDialog):
    def __init__(self, CharacterWindow):
        super().__init__(parent=CharacterWindow)

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Variables
        self.PlayerCharacter = CharacterWindow.PlayerCharacter
        self.AbilityScores = self.PlayerCharacter.Stats["Ability Scores"]
        self.AbilityScoresOriginalState = copy.deepcopy(self.AbilityScores)
        self.UnsavedChanges = False
        self.Cancelled = False

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Prompt Label
        self.PromptLabel = QLabel("Set your ability score data:")
        self.PromptLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Roll or Point Buy Buttons
        self.RollButton = QPushButton("Roll for Ability Scores")
        self.RollButton.clicked.connect(self.RollForAbilityScores)
        self.PointBuyButton = QPushButton("Use Point Buy for Ability Scores")
        self.PointBuyButton.clicked.connect(self.PointBuyAbilityScores)

        # Ability Scores Inputs List
        self.AbilityScoresInputsList = []

        # Ability Scores Table Header
        self.AbilityScoreLabel = QLabel("Ability Score")
        self.AbilityScoreLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.AbilityScoreLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.AbilityScoreLabel.setMargin(5)

        self.BaseLabel = QLabel("Base")
        self.BaseLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.BaseLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.BaseLabel.setMargin(5)

        self.RacialLabel = QLabel("Racial")
        self.RacialLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.RacialLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.RacialLabel.setMargin(5)

        self.ASILabel = QLabel("ASI")
        self.ASILabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ASILabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.ASILabel.setMargin(5)

        self.MiscLabel = QLabel("Misc.")
        self.MiscLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MiscLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.MiscLabel.setMargin(5)

        self.OverrideLabel = QLabel("Override")
        self.OverrideLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.OverrideLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.OverrideLabel.setMargin(5)

        self.TotalLabel = QLabel("Total")
        self.TotalLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.TotalLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.TotalLabel.setMargin(5)

        self.AbilityCheckModifierLabel = QLabel("Ability Check Modifier")
        self.AbilityCheckModifierLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.AbilityCheckModifierLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.AbilityCheckModifierLabel.setMargin(5)

        self.SavingThrowModifierLabel = QLabel("Saving Throw Modifier")
        self.SavingThrowModifierLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SavingThrowModifierLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.SavingThrowModifierLabel.setMargin(5)

        self.AbilityScoresInputsList.append((self.AbilityScoreLabel, self.BaseLabel, self.RacialLabel, self.ASILabel, self.MiscLabel, self.OverrideLabel, self.TotalLabel, self.AbilityCheckModifierLabel, self.SavingThrowModifierLabel))

        # Strength Ability Scores Data
        self.StrengthLabel = QLabel("Strength")
        self.StrengthLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.StrengthBaseSpinBox = QSpinBox()
        self.StrengthBaseSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.StrengthBaseSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.StrengthBaseSpinBox.setButtonSymbols(self.StrengthBaseSpinBox.NoButtons)
        self.StrengthBaseSpinBox.setRange(1, 1000000000)
        self.StrengthBaseSpinBox.setValue(self.AbilityScores["Strength Base"])
        self.StrengthBaseSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Strength", "Base", self.StrengthBaseSpinBox.value()))

        self.StrengthRacialSpinBox = QSpinBox()
        self.StrengthRacialSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.StrengthRacialSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.StrengthRacialSpinBox.setButtonSymbols(self.StrengthRacialSpinBox.NoButtons)
        self.StrengthRacialSpinBox.setRange(0, 1000000000)
        self.StrengthRacialSpinBox.setValue(self.AbilityScores["Strength Racial"])
        self.StrengthRacialSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Strength", "Racial", self.StrengthRacialSpinBox.value()))

        self.StrengthASISpinBox = QSpinBox()
        self.StrengthASISpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.StrengthASISpinBox.setSizePolicy(self.InputsSizePolicy)
        self.StrengthASISpinBox.setButtonSymbols(self.StrengthASISpinBox.NoButtons)
        self.StrengthASISpinBox.setRange(0, 1000000000)
        self.StrengthASISpinBox.setValue(self.AbilityScores["Strength ASI"])
        self.StrengthASISpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Strength", "ASI", self.StrengthASISpinBox.value()))

        self.StrengthMiscSpinBox = QSpinBox()
        self.StrengthMiscSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.StrengthMiscSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.StrengthMiscSpinBox.setButtonSymbols(self.StrengthMiscSpinBox.NoButtons)
        self.StrengthMiscSpinBox.setRange(0, 1000000000)
        self.StrengthMiscSpinBox.setValue(self.AbilityScores["Strength Miscellaneous"])
        self.StrengthMiscSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Strength", "Miscellaneous", self.StrengthMiscSpinBox.value()))

        self.StrengthOverrideSpinBox = QSpinBox()
        self.StrengthOverrideSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.StrengthOverrideSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.StrengthOverrideSpinBox.setButtonSymbols(self.StrengthOverrideSpinBox.NoButtons)
        self.StrengthOverrideSpinBox.setRange(0, 1000000000)
        self.StrengthOverrideSpinBox.setSpecialValueText("None")
        self.StrengthOverrideSpinBox.setValue(self.AbilityScores["Strength Override"] if self.AbilityScores["Strength Override"] is not None else 0)
        self.StrengthOverrideSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Strength", "Override", self.StrengthOverrideSpinBox.value() if self.StrengthOverrideSpinBox.value() > 0 else None))

        self.StrengthTotalSpinBox = QSpinBox()
        self.StrengthTotalSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.StrengthTotalSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.StrengthTotalSpinBox.setButtonSymbols(self.StrengthTotalSpinBox.NoButtons)
        self.StrengthTotalSpinBox.setRange(1, 1000000000)
        self.StrengthTotalSpinBox.setValue(self.PlayerCharacter.GetTotalAbilityScore("Strength"))
        self.StrengthTotalSpinBox.setReadOnly(True)
        self.StrengthTotalSpinBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.StrengthAbilityCheckModifierButton = EditButton(lambda: self.EditModifier("Strength Stat Modifier"), Tooltip="Edit Strength Ability Check Modifier")
        self.StrengthAbilityCheckModifierButton.setSizePolicy(self.InputsSizePolicy)

        self.StrengthSavingThrowModifierButton = EditButton(lambda: self.EditModifier("Strength Save Stat Modifier"), Tooltip="Edit Strength Saving Throw Modifier")
        self.StrengthSavingThrowModifierButton.setSizePolicy(self.InputsSizePolicy)

        self.AbilityScoresInputsList.append((self.StrengthLabel, self.StrengthBaseSpinBox, self.StrengthRacialSpinBox, self.StrengthASISpinBox, self.StrengthMiscSpinBox, self.StrengthOverrideSpinBox, self.StrengthTotalSpinBox, self.StrengthAbilityCheckModifierButton, self.StrengthSavingThrowModifierButton))

        # Dexterity Ability Scores Data
        self.DexterityLabel = QLabel("Dexterity")
        self.DexterityLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.DexterityBaseSpinBox = QSpinBox()
        self.DexterityBaseSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.DexterityBaseSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.DexterityBaseSpinBox.setButtonSymbols(self.DexterityBaseSpinBox.NoButtons)
        self.DexterityBaseSpinBox.setRange(1, 1000000000)
        self.DexterityBaseSpinBox.setValue(self.AbilityScores["Dexterity Base"])
        self.DexterityBaseSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Dexterity", "Base", self.DexterityBaseSpinBox.value()))

        self.DexterityRacialSpinBox = QSpinBox()
        self.DexterityRacialSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.DexterityRacialSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.DexterityRacialSpinBox.setButtonSymbols(self.DexterityRacialSpinBox.NoButtons)
        self.DexterityRacialSpinBox.setRange(0, 1000000000)
        self.DexterityRacialSpinBox.setValue(self.AbilityScores["Dexterity Racial"])
        self.DexterityRacialSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Dexterity", "Racial", self.DexterityRacialSpinBox.value()))

        self.DexterityASISpinBox = QSpinBox()
        self.DexterityASISpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.DexterityASISpinBox.setSizePolicy(self.InputsSizePolicy)
        self.DexterityASISpinBox.setButtonSymbols(self.DexterityASISpinBox.NoButtons)
        self.DexterityASISpinBox.setRange(0, 1000000000)
        self.DexterityASISpinBox.setValue(self.AbilityScores["Dexterity ASI"])
        self.DexterityASISpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Dexterity", "ASI", self.DexterityASISpinBox.value()))

        self.DexterityMiscSpinBox = QSpinBox()
        self.DexterityMiscSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.DexterityMiscSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.DexterityMiscSpinBox.setButtonSymbols(self.DexterityMiscSpinBox.NoButtons)
        self.DexterityMiscSpinBox.setRange(0, 1000000000)
        self.DexterityMiscSpinBox.setValue(self.AbilityScores["Dexterity Miscellaneous"])
        self.DexterityMiscSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Dexterity", "Miscellaneous", self.DexterityMiscSpinBox.value()))

        self.DexterityOverrideSpinBox = QSpinBox()
        self.DexterityOverrideSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.DexterityOverrideSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.DexterityOverrideSpinBox.setButtonSymbols(self.DexterityOverrideSpinBox.NoButtons)
        self.DexterityOverrideSpinBox.setRange(0, 1000000000)
        self.DexterityOverrideSpinBox.setSpecialValueText("None")
        self.DexterityOverrideSpinBox.setValue(self.AbilityScores["Dexterity Override"] if self.AbilityScores["Dexterity Override"] is not None else 0)
        self.DexterityOverrideSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Dexterity", "Override", self.DexterityOverrideSpinBox.value() if self.DexterityOverrideSpinBox.value() > 0 else None))

        self.DexterityTotalSpinBox = QSpinBox()
        self.DexterityTotalSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.DexterityTotalSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.DexterityTotalSpinBox.setButtonSymbols(self.DexterityTotalSpinBox.NoButtons)
        self.DexterityTotalSpinBox.setRange(1, 1000000000)
        self.DexterityTotalSpinBox.setValue(self.PlayerCharacter.GetTotalAbilityScore("Dexterity"))
        self.DexterityTotalSpinBox.setReadOnly(True)
        self.DexterityTotalSpinBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.DexterityAbilityCheckModifierButton = EditButton(lambda: self.EditModifier("Dexterity Stat Modifier"), Tooltip="Edit Dexterity Ability Check Modifier")
        self.DexterityAbilityCheckModifierButton.setSizePolicy(self.InputsSizePolicy)

        self.DexteritySavingThrowModifierButton = EditButton(lambda: self.EditModifier("Dexterity Save Stat Modifier"), Tooltip="Edit Dexterity Saving Throw Modifier")
        self.DexteritySavingThrowModifierButton.setSizePolicy(self.InputsSizePolicy)

        self.AbilityScoresInputsList.append((self.DexterityLabel, self.DexterityBaseSpinBox, self.DexterityRacialSpinBox, self.DexterityASISpinBox, self.DexterityMiscSpinBox, self.DexterityOverrideSpinBox, self.DexterityTotalSpinBox, self.DexterityAbilityCheckModifierButton, self.DexteritySavingThrowModifierButton))

        # Constitution Ability Scores Data
        self.ConstitutionLabel = QLabel("Constitution")
        self.ConstitutionLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.ConstitutionBaseSpinBox = QSpinBox()
        self.ConstitutionBaseSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ConstitutionBaseSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.ConstitutionBaseSpinBox.setButtonSymbols(self.ConstitutionBaseSpinBox.NoButtons)
        self.ConstitutionBaseSpinBox.setRange(1, 1000000000)
        self.ConstitutionBaseSpinBox.setValue(self.AbilityScores["Constitution Base"])
        self.ConstitutionBaseSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Constitution", "Base", self.ConstitutionBaseSpinBox.value()))

        self.ConstitutionRacialSpinBox = QSpinBox()
        self.ConstitutionRacialSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ConstitutionRacialSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.ConstitutionRacialSpinBox.setButtonSymbols(self.ConstitutionRacialSpinBox.NoButtons)
        self.ConstitutionRacialSpinBox.setRange(0, 1000000000)
        self.ConstitutionRacialSpinBox.setValue(self.AbilityScores["Constitution Racial"])
        self.ConstitutionRacialSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Constitution", "Racial", self.ConstitutionRacialSpinBox.value()))

        self.ConstitutionASISpinBox = QSpinBox()
        self.ConstitutionASISpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ConstitutionASISpinBox.setSizePolicy(self.InputsSizePolicy)
        self.ConstitutionASISpinBox.setButtonSymbols(self.ConstitutionASISpinBox.NoButtons)
        self.ConstitutionASISpinBox.setRange(0, 1000000000)
        self.ConstitutionASISpinBox.setValue(self.AbilityScores["Constitution ASI"])
        self.ConstitutionASISpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Constitution", "ASI", self.ConstitutionASISpinBox.value()))

        self.ConstitutionMiscSpinBox = QSpinBox()
        self.ConstitutionMiscSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ConstitutionMiscSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.ConstitutionMiscSpinBox.setButtonSymbols(self.ConstitutionMiscSpinBox.NoButtons)
        self.ConstitutionMiscSpinBox.setRange(0, 1000000000)
        self.ConstitutionMiscSpinBox.setValue(self.AbilityScores["Constitution Miscellaneous"])
        self.ConstitutionMiscSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Constitution", "Miscellaneous", self.ConstitutionMiscSpinBox.value()))

        self.ConstitutionOverrideSpinBox = QSpinBox()
        self.ConstitutionOverrideSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ConstitutionOverrideSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.ConstitutionOverrideSpinBox.setButtonSymbols(self.ConstitutionOverrideSpinBox.NoButtons)
        self.ConstitutionOverrideSpinBox.setRange(0, 1000000000)
        self.ConstitutionOverrideSpinBox.setSpecialValueText("None")
        self.ConstitutionOverrideSpinBox.setValue(self.AbilityScores["Constitution Override"] if self.AbilityScores["Constitution Override"] is not None else 0)
        self.ConstitutionOverrideSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Constitution", "Override", self.ConstitutionOverrideSpinBox.value() if self.ConstitutionOverrideSpinBox.value() > 0 else None))

        self.ConstitutionTotalSpinBox = QSpinBox()
        self.ConstitutionTotalSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ConstitutionTotalSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.ConstitutionTotalSpinBox.setButtonSymbols(self.ConstitutionTotalSpinBox.NoButtons)
        self.ConstitutionTotalSpinBox.setRange(1, 1000000000)
        self.ConstitutionTotalSpinBox.setValue(self.PlayerCharacter.GetTotalAbilityScore("Constitution"))
        self.ConstitutionTotalSpinBox.setReadOnly(True)
        self.ConstitutionTotalSpinBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.ConstitutionAbilityCheckModifierButton = EditButton(lambda: self.EditModifier("Constitution Stat Modifier"), Tooltip="Edit Constitution Ability Check Modifier")
        self.ConstitutionAbilityCheckModifierButton.setSizePolicy(self.InputsSizePolicy)

        self.ConstitutionSavingThrowModifierButton = EditButton(lambda: self.EditModifier("Constitution Save Stat Modifier"), Tooltip="Edit Constitution Saving Throw Modifier")
        self.ConstitutionSavingThrowModifierButton.setSizePolicy(self.InputsSizePolicy)

        self.AbilityScoresInputsList.append((self.ConstitutionLabel, self.ConstitutionBaseSpinBox, self.ConstitutionRacialSpinBox, self.ConstitutionASISpinBox, self.ConstitutionMiscSpinBox, self.ConstitutionOverrideSpinBox, self.ConstitutionTotalSpinBox, self.ConstitutionAbilityCheckModifierButton, self.ConstitutionSavingThrowModifierButton))

        # Intelligence Ability Scores Data
        self.IntelligenceLabel = QLabel("Intelligence")
        self.IntelligenceLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.IntelligenceBaseSpinBox = QSpinBox()
        self.IntelligenceBaseSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.IntelligenceBaseSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.IntelligenceBaseSpinBox.setButtonSymbols(self.IntelligenceBaseSpinBox.NoButtons)
        self.IntelligenceBaseSpinBox.setRange(1, 1000000000)
        self.IntelligenceBaseSpinBox.setValue(self.AbilityScores["Intelligence Base"])
        self.IntelligenceBaseSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Intelligence", "Base", self.IntelligenceBaseSpinBox.value()))

        self.IntelligenceRacialSpinBox = QSpinBox()
        self.IntelligenceRacialSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.IntelligenceRacialSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.IntelligenceRacialSpinBox.setButtonSymbols(self.IntelligenceRacialSpinBox.NoButtons)
        self.IntelligenceRacialSpinBox.setRange(0, 1000000000)
        self.IntelligenceRacialSpinBox.setValue(self.AbilityScores["Intelligence Racial"])
        self.IntelligenceRacialSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Intelligence", "Racial", self.IntelligenceRacialSpinBox.value()))

        self.IntelligenceASISpinBox = QSpinBox()
        self.IntelligenceASISpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.IntelligenceASISpinBox.setSizePolicy(self.InputsSizePolicy)
        self.IntelligenceASISpinBox.setButtonSymbols(self.IntelligenceASISpinBox.NoButtons)
        self.IntelligenceASISpinBox.setRange(0, 1000000000)
        self.IntelligenceASISpinBox.setValue(self.AbilityScores["Intelligence ASI"])
        self.IntelligenceASISpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Intelligence", "ASI", self.IntelligenceASISpinBox.value()))

        self.IntelligenceMiscSpinBox = QSpinBox()
        self.IntelligenceMiscSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.IntelligenceMiscSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.IntelligenceMiscSpinBox.setButtonSymbols(self.IntelligenceMiscSpinBox.NoButtons)
        self.IntelligenceMiscSpinBox.setRange(0, 1000000000)
        self.IntelligenceMiscSpinBox.setValue(self.AbilityScores["Intelligence Miscellaneous"])
        self.IntelligenceMiscSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Intelligence", "Miscellaneous", self.IntelligenceMiscSpinBox.value()))

        self.IntelligenceOverrideSpinBox = QSpinBox()
        self.IntelligenceOverrideSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.IntelligenceOverrideSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.IntelligenceOverrideSpinBox.setButtonSymbols(self.IntelligenceOverrideSpinBox.NoButtons)
        self.IntelligenceOverrideSpinBox.setRange(0, 1000000000)
        self.IntelligenceOverrideSpinBox.setSpecialValueText("None")
        self.IntelligenceOverrideSpinBox.setValue(self.AbilityScores["Intelligence Override"] if self.AbilityScores["Intelligence Override"] is not None else 0)
        self.IntelligenceOverrideSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Intelligence", "Override", self.IntelligenceOverrideSpinBox.value() if self.IntelligenceOverrideSpinBox.value() > 0 else None))

        self.IntelligenceTotalSpinBox = QSpinBox()
        self.IntelligenceTotalSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.IntelligenceTotalSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.IntelligenceTotalSpinBox.setButtonSymbols(self.IntelligenceTotalSpinBox.NoButtons)
        self.IntelligenceTotalSpinBox.setRange(1, 1000000000)
        self.IntelligenceTotalSpinBox.setValue(self.PlayerCharacter.GetTotalAbilityScore("Intelligence"))
        self.IntelligenceTotalSpinBox.setReadOnly(True)
        self.IntelligenceTotalSpinBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.IntelligenceAbilityCheckModifierButton = EditButton(lambda: self.EditModifier("Intelligence Stat Modifier"), Tooltip="Edit Intelligence Ability Check Modifier")
        self.IntelligenceAbilityCheckModifierButton.setSizePolicy(self.InputsSizePolicy)

        self.IntelligenceSavingThrowModifierButton = EditButton(lambda: self.EditModifier("Intelligence Save Stat Modifier"), Tooltip="Edit Intelligence Saving Throw Modifier")
        self.IntelligenceSavingThrowModifierButton.setSizePolicy(self.InputsSizePolicy)

        self.AbilityScoresInputsList.append((self.IntelligenceLabel, self.IntelligenceBaseSpinBox, self.IntelligenceRacialSpinBox, self.IntelligenceASISpinBox, self.IntelligenceMiscSpinBox, self.IntelligenceOverrideSpinBox, self.IntelligenceTotalSpinBox, self.IntelligenceAbilityCheckModifierButton, self.IntelligenceSavingThrowModifierButton))

        # Wisdom Ability Scores Data
        self.WisdomLabel = QLabel("Wisdom")
        self.WisdomLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.WisdomBaseSpinBox = QSpinBox()
        self.WisdomBaseSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.WisdomBaseSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.WisdomBaseSpinBox.setButtonSymbols(self.WisdomBaseSpinBox.NoButtons)
        self.WisdomBaseSpinBox.setRange(1, 1000000000)
        self.WisdomBaseSpinBox.setValue(self.AbilityScores["Wisdom Base"])
        self.WisdomBaseSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Wisdom", "Base", self.WisdomBaseSpinBox.value()))

        self.WisdomRacialSpinBox = QSpinBox()
        self.WisdomRacialSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.WisdomRacialSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.WisdomRacialSpinBox.setButtonSymbols(self.WisdomRacialSpinBox.NoButtons)
        self.WisdomRacialSpinBox.setRange(0, 1000000000)
        self.WisdomRacialSpinBox.setValue(self.AbilityScores["Wisdom Racial"])
        self.WisdomRacialSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Wisdom", "Racial", self.WisdomRacialSpinBox.value()))

        self.WisdomASISpinBox = QSpinBox()
        self.WisdomASISpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.WisdomASISpinBox.setSizePolicy(self.InputsSizePolicy)
        self.WisdomASISpinBox.setButtonSymbols(self.WisdomASISpinBox.NoButtons)
        self.WisdomASISpinBox.setRange(0, 1000000000)
        self.WisdomASISpinBox.setValue(self.AbilityScores["Wisdom ASI"])
        self.WisdomASISpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Wisdom", "ASI", self.WisdomASISpinBox.value()))

        self.WisdomMiscSpinBox = QSpinBox()
        self.WisdomMiscSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.WisdomMiscSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.WisdomMiscSpinBox.setButtonSymbols(self.WisdomMiscSpinBox.NoButtons)
        self.WisdomMiscSpinBox.setRange(0, 1000000000)
        self.WisdomMiscSpinBox.setValue(self.AbilityScores["Wisdom Miscellaneous"])
        self.WisdomMiscSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Wisdom", "Miscellaneous", self.WisdomMiscSpinBox.value()))

        self.WisdomOverrideSpinBox = QSpinBox()
        self.WisdomOverrideSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.WisdomOverrideSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.WisdomOverrideSpinBox.setButtonSymbols(self.WisdomOverrideSpinBox.NoButtons)
        self.WisdomOverrideSpinBox.setRange(0, 1000000000)
        self.WisdomOverrideSpinBox.setSpecialValueText("None")
        self.WisdomOverrideSpinBox.setValue(self.AbilityScores["Wisdom Override"] if self.AbilityScores["Wisdom Override"] is not None else 0)
        self.WisdomOverrideSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Wisdom", "Override", self.WisdomOverrideSpinBox.value() if self.WisdomOverrideSpinBox.value() > 0 else None))

        self.WisdomTotalSpinBox = QSpinBox()
        self.WisdomTotalSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.WisdomTotalSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.WisdomTotalSpinBox.setButtonSymbols(self.WisdomTotalSpinBox.NoButtons)
        self.WisdomTotalSpinBox.setRange(1, 1000000000)
        self.WisdomTotalSpinBox.setValue(self.PlayerCharacter.GetTotalAbilityScore("Wisdom"))
        self.WisdomTotalSpinBox.setReadOnly(True)
        self.WisdomTotalSpinBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.WisdomAbilityCheckModifierButton = EditButton(lambda: self.EditModifier("Wisdom Stat Modifier"), Tooltip="Edit Wisdom Ability Check Modifier")
        self.WisdomAbilityCheckModifierButton.setSizePolicy(self.InputsSizePolicy)

        self.WisdomSavingThrowModifierButton = EditButton(lambda: self.EditModifier("Wisdom Save Stat Modifier"), Tooltip="Edit Wisdom Saving Throw Modifier")
        self.WisdomSavingThrowModifierButton.setSizePolicy(self.InputsSizePolicy)

        self.AbilityScoresInputsList.append((self.WisdomLabel, self.WisdomBaseSpinBox, self.WisdomRacialSpinBox, self.WisdomASISpinBox, self.WisdomMiscSpinBox, self.WisdomOverrideSpinBox, self.WisdomTotalSpinBox, self.WisdomAbilityCheckModifierButton, self.WisdomSavingThrowModifierButton))

        # Charisma Ability Scores Data
        self.CharismaLabel = QLabel("Charisma")
        self.CharismaLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.CharismaBaseSpinBox = QSpinBox()
        self.CharismaBaseSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.CharismaBaseSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CharismaBaseSpinBox.setButtonSymbols(self.CharismaBaseSpinBox.NoButtons)
        self.CharismaBaseSpinBox.setRange(1, 1000000000)
        self.CharismaBaseSpinBox.setValue(self.AbilityScores["Charisma Base"])
        self.CharismaBaseSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Charisma", "Base", self.CharismaBaseSpinBox.value()))

        self.CharismaRacialSpinBox = QSpinBox()
        self.CharismaRacialSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.CharismaRacialSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CharismaRacialSpinBox.setButtonSymbols(self.CharismaRacialSpinBox.NoButtons)
        self.CharismaRacialSpinBox.setRange(0, 1000000000)
        self.CharismaRacialSpinBox.setValue(self.AbilityScores["Charisma Racial"])
        self.CharismaRacialSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Charisma", "Racial", self.CharismaRacialSpinBox.value()))

        self.CharismaASISpinBox = QSpinBox()
        self.CharismaASISpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.CharismaASISpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CharismaASISpinBox.setButtonSymbols(self.CharismaASISpinBox.NoButtons)
        self.CharismaASISpinBox.setRange(0, 1000000000)
        self.CharismaASISpinBox.setValue(self.AbilityScores["Charisma ASI"])
        self.CharismaASISpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Charisma", "ASI", self.CharismaASISpinBox.value()))

        self.CharismaMiscSpinBox = QSpinBox()
        self.CharismaMiscSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.CharismaMiscSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CharismaMiscSpinBox.setButtonSymbols(self.CharismaMiscSpinBox.NoButtons)
        self.CharismaMiscSpinBox.setRange(0, 1000000000)
        self.CharismaMiscSpinBox.setValue(self.AbilityScores["Charisma Miscellaneous"])
        self.CharismaMiscSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Charisma", "Miscellaneous", self.CharismaMiscSpinBox.value()))

        self.CharismaOverrideSpinBox = QSpinBox()
        self.CharismaOverrideSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.CharismaOverrideSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CharismaOverrideSpinBox.setButtonSymbols(self.CharismaOverrideSpinBox.NoButtons)
        self.CharismaOverrideSpinBox.setRange(0, 1000000000)
        self.CharismaOverrideSpinBox.setSpecialValueText("None")
        self.CharismaOverrideSpinBox.setValue(self.AbilityScores["Charisma Override"] if self.AbilityScores["Charisma Override"] is not None else 0)
        self.CharismaOverrideSpinBox.valueChanged.connect(lambda: self.UpdateAbilityScores("Charisma", "Override", self.CharismaOverrideSpinBox.value() if self.CharismaOverrideSpinBox.value() > 0 else None))

        self.CharismaTotalSpinBox = QSpinBox()
        self.CharismaTotalSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.CharismaTotalSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CharismaTotalSpinBox.setButtonSymbols(self.CharismaTotalSpinBox.NoButtons)
        self.CharismaTotalSpinBox.setRange(1, 1000000000)
        self.CharismaTotalSpinBox.setValue(self.PlayerCharacter.GetTotalAbilityScore("Charisma"))
        self.CharismaTotalSpinBox.setReadOnly(True)
        self.CharismaTotalSpinBox.setFocusPolicy(QtCore.Qt.NoFocus)

        self.CharismaAbilityCheckModifierButton = EditButton(lambda: self.EditModifier("Charisma Stat Modifier"), Tooltip="Edit Charisma Ability Check Modifier")
        self.CharismaAbilityCheckModifierButton.setSizePolicy(self.InputsSizePolicy)

        self.CharismaSavingThrowModifierButton = EditButton(lambda: self.EditModifier("Charisma Save Stat Modifier"), Tooltip="Edit Charisma Saving Throw Modifier")
        self.CharismaSavingThrowModifierButton.setSizePolicy(self.InputsSizePolicy)

        self.AbilityScoresInputsList.append((self.CharismaLabel, self.CharismaBaseSpinBox, self.CharismaRacialSpinBox, self.CharismaASISpinBox, self.CharismaMiscSpinBox, self.CharismaOverrideSpinBox, self.CharismaTotalSpinBox, self.CharismaAbilityCheckModifierButton, self.CharismaSavingThrowModifierButton))

        # Ability Score Total Spin Boxes Dictionary
        self.AbilityScoreTotalSpinBoxesDictionary = {}
        self.AbilityScoreTotalSpinBoxesDictionary["Strength"] = self.StrengthTotalSpinBox
        self.AbilityScoreTotalSpinBoxesDictionary["Dexterity"] = self.DexterityTotalSpinBox
        self.AbilityScoreTotalSpinBoxesDictionary["Constitution"] = self.ConstitutionTotalSpinBox
        self.AbilityScoreTotalSpinBoxesDictionary["Intelligence"] = self.IntelligenceTotalSpinBox
        self.AbilityScoreTotalSpinBoxesDictionary["Wisdom"] = self.WisdomTotalSpinBox
        self.AbilityScoreTotalSpinBoxesDictionary["Charisma"] = self.CharismaTotalSpinBox

        # Ability Score Notes
        self.AbilityScoreNotesLabel = QLabel("Ability Score Notes")
        self.AbilityScoreNotesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.AbilityScoreNotesLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.AbilityScoreNotesLabel.setMargin(5)

        self.AbilityScoreNotesTextEdit = QTextEdit()
        self.AbilityScoreNotesTextEdit.setTabChangesFocus(True)
        self.AbilityScoreNotesTextEdit.setPlainText(self.AbilityScores["Ability Score Notes"])
        self.AbilityScoreNotesTextEdit.textChanged.connect(self.UpdateAbilityScoreNotes)

        # Dialog Buttons
        self.DoneButton = QPushButton("Done")
        self.DoneButton.clicked.connect(self.Done)
        self.SetToDefaultButton = QPushButton("Set to Default")
        self.SetToDefaultButton.clicked.connect(self.SetToDefault)
        self.CancelButton = QPushButton("Cancel")
        self.CancelButton.clicked.connect(self.Cancel)

        # Layout
        self.Layout = QGridLayout()

        self.Layout.addWidget(self.PromptLabel, 0, 0, 1, 2)

        self.RollOrPointBuyLayout = QGridLayout()
        self.RollOrPointBuyLayout.addWidget(self.RollButton, 0, 0)
        self.RollOrPointBuyLayout.addWidget(self.PointBuyButton, 0, 1)
        self.Layout.addLayout(self.RollOrPointBuyLayout, 1, 0, 1, 2)

        self.AbilityScoresTableLayout = QGridLayout()
        for Row in range(len(self.AbilityScoresInputsList)):
            RowWidgets = self.AbilityScoresInputsList[Row]
            self.AbilityScoresTableLayout.addWidget(RowWidgets[0], Row, 0)
            self.AbilityScoresTableLayout.addWidget(RowWidgets[1], Row, 1)
            self.AbilityScoresTableLayout.addWidget(RowWidgets[2], Row, 2)
            self.AbilityScoresTableLayout.addWidget(RowWidgets[3], Row, 3)
            self.AbilityScoresTableLayout.addWidget(RowWidgets[4], Row, 4)
            self.AbilityScoresTableLayout.addWidget(RowWidgets[5], Row, 5)
            self.AbilityScoresTableLayout.addWidget(RowWidgets[6], Row, 6)
            self.AbilityScoresTableLayout.addWidget(RowWidgets[7], Row, 7)
            self.AbilityScoresTableLayout.addWidget(RowWidgets[8], Row, 8)
            if Row != 0:
                self.AbilityScoresTableLayout.setRowStretch(Row, 1)
        self.Layout.addLayout(self.AbilityScoresTableLayout, 2, 0)

        self.AbilityScoreNotesLayout = QGridLayout()
        self.AbilityScoreNotesLayout.addWidget(self.AbilityScoreNotesLabel, 0, 0)
        self.AbilityScoreNotesLayout.addWidget(self.AbilityScoreNotesTextEdit, 1, 0)
        self.Layout.addLayout(self.AbilityScoreNotesLayout, 2, 1)

        self.DialogButtonsLayout = QGridLayout()
        self.DialogButtonsLayout.addWidget(self.DoneButton, 0, 0)
        self.DialogButtonsLayout.addWidget(self.SetToDefaultButton, 0, 1)
        self.DialogButtonsLayout.addWidget(self.CancelButton, 0, 2)
        self.Layout.addLayout(self.DialogButtonsLayout, 3, 0, 1, 2)

        self.Layout.setRowStretch(2, 1)

        self.setLayout(self.Layout)

        # Set Window Title and Icon
        self.setWindowTitle(self.CharacterWindow.ScriptName)
        self.setWindowIcon(self.CharacterWindow.WindowIcon)

        # Execute Dialog
        self.exec_()

    def RollForAbilityScores(self):
        RollForAbilityScoresDialogInst = RollForAbilityScoresDialog(self, self.CharacterWindow)
        if RollForAbilityScoresDialogInst.RolledAbilityScores is not None:
            self.StrengthBaseSpinBox.setValue(RollForAbilityScoresDialogInst.RolledAbilityScores["Strength"])
            self.DexterityBaseSpinBox.setValue(RollForAbilityScoresDialogInst.RolledAbilityScores["Dexterity"])
            self.ConstitutionBaseSpinBox.setValue(RollForAbilityScoresDialogInst.RolledAbilityScores["Constitution"])
            self.IntelligenceBaseSpinBox.setValue(RollForAbilityScoresDialogInst.RolledAbilityScores["Intelligence"])
            self.WisdomBaseSpinBox.setValue(RollForAbilityScoresDialogInst.RolledAbilityScores["Wisdom"])
            self.CharismaBaseSpinBox.setValue(RollForAbilityScoresDialogInst.RolledAbilityScores["Charisma"])
            self.UnsavedChanges = True

    def PointBuyAbilityScores(self):
        PointBuyAbilityScoresDialogInst = PointBuyAbilityScoresDialog(self, self.CharacterWindow)
        if PointBuyAbilityScoresDialogInst.PointBoughtAbilityScores is not None:
            self.StrengthBaseSpinBox.setValue(PointBuyAbilityScoresDialogInst.PointBoughtAbilityScores["Strength"])
            self.DexterityBaseSpinBox.setValue(PointBuyAbilityScoresDialogInst.PointBoughtAbilityScores["Dexterity"])
            self.ConstitutionBaseSpinBox.setValue(PointBuyAbilityScoresDialogInst.PointBoughtAbilityScores["Constitution"])
            self.IntelligenceBaseSpinBox.setValue(PointBuyAbilityScoresDialogInst.PointBoughtAbilityScores["Intelligence"])
            self.WisdomBaseSpinBox.setValue(PointBuyAbilityScoresDialogInst.PointBoughtAbilityScores["Wisdom"])
            self.CharismaBaseSpinBox.setValue(PointBuyAbilityScoresDialogInst.PointBoughtAbilityScores["Charisma"])
            self.UnsavedChanges = True

    def UpdateAbilityScores(self, Ability, AbilitySubScore, NewValue):
        self.AbilityScores[Ability + " " + AbilitySubScore] = NewValue
        for Ability, TotalSpinBox in self.AbilityScoreTotalSpinBoxesDictionary.items():
            TotalSpinBox.setValue(self.PlayerCharacter.GetTotalAbilityScore(Ability))
        self.UnsavedChanges = True

    def UpdateAbilityScoreNotes(self):
        self.AbilityScores["Ability Score Notes"] = self.AbilityScoreNotesTextEdit.toPlainText()
        self.UnsavedChanges = True

    def EditModifier(self, Modifier):
        EditModifierDialogInst = EditModifierDialog(self, self.CharacterWindow, self.AbilityScores[Modifier], Modifier)
        self.UnsavedChanges = EditModifierDialogInst.UnsavedChanges

    def Done(self):
        self.close()

    def SetToDefault(self):
        Confirm = self.CharacterWindow.DisplayMessageBox("Are you sure you want to set ability score data to default values?  This cannot be undone.", Icon=QMessageBox.Warning, Buttons=(QMessageBox.Yes | QMessageBox.No), Parent=self)
        if Confirm == QMessageBox.Yes:
            DefaultAbilityScoreData = self.CharacterWindow.PlayerCharacter.CreateAbilityScoresStats()
            self.AbilityScores.update(DefaultAbilityScoreData)
            self.UnsavedChanges = True
            self.close()

    def Cancel(self):
        self.AbilityScores.update(self.AbilityScoresOriginalState)
        self.UnsavedChanges = False
        self.Cancelled = True
        self.close()
