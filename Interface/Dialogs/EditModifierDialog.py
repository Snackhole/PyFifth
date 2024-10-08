import copy

from PyQt5 import QtCore
from PyQt5.QtWidgets import QCheckBox, QDialog, QDoubleSpinBox, QGridLayout, QLabel, QMessageBox, QPushButton, QSizePolicy, QSpinBox


class EditModifierDialog(QDialog):
    def __init__(self, Parent, CharacterWindow, StatModifier, StatModifierDescription="Stat Modifier"):
        super().__init__(parent=Parent)

        # Store Parameters
        self.CharacterWindow = CharacterWindow
        self.StatModifier = StatModifier

        # Variables
        self.StatModifierOriginalState = copy.deepcopy(self.StatModifier)
        self.UnsavedChanges = False
        self.Cancelled = False

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Prompt Label
        self.PromptLabel = QLabel(f"Edit {StatModifierDescription}:")
        self.PromptLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Base AC
        if "Base AC" in self.StatModifier:
            self.BaseACLabel = QLabel("Base AC")
            self.BaseACLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.BaseACLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
            self.BaseACLabel.setMargin(5)
            self.BaseACSpinBox = QSpinBox()
            self.BaseACSpinBox.setAlignment(QtCore.Qt.AlignCenter)
            self.BaseACSpinBox.setButtonSymbols(self.BaseACSpinBox.NoButtons)
            self.BaseACSpinBox.setRange(0, 1000000000)
            self.BaseACSpinBox.setValue(StatModifier["Base AC"])
            self.BaseACSpinBox.valueChanged.connect(self.UpdateStatModifier)

        # Multipliers List
        self.MultipliersList = []

        # Multiplier Header Labels
        self.StatLabel = QLabel("Stat")
        self.StatLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.StatLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.StatLabel.setMargin(5)
        self.MultiplierLabel = QLabel("Multiplier")
        self.MultiplierLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MultiplierLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.MultiplierLabel.setMargin(5)
        self.RoundUpLabel = QLabel("Round Up")
        self.RoundUpLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.RoundUpLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.RoundUpLabel.setMargin(5)
        self.MinLabel = QLabel("Min")
        self.MinLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MinLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.MinLabel.setMargin(5)
        self.MaxLabel = QLabel("Max")
        self.MaxLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.MaxLabel.setMargin(5)

        self.MultipliersList.append((self.StatLabel, self.MultiplierLabel, self.RoundUpLabel, self.MinLabel, self.MaxLabel))

        # Strength Multiplier
        self.StrengthMultiplierLabel = QLabel("Strength")
        self.StrengthMultiplierLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.StrengthMultiplierSpinBox = QDoubleSpinBox()
        self.StrengthMultiplierSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.StrengthMultiplierSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.StrengthMultiplierSpinBox.setButtonSymbols(self.StrengthMultiplierSpinBox.NoButtons)
        self.StrengthMultiplierSpinBox.setRange(-1000000000.0, 1000000000.0)
        self.StrengthMultiplierSpinBox.setValue(StatModifier["Strength Multiplier"])
        self.StrengthMultiplierSpinBox.valueChanged.connect(self.UpdateStatModifier)

        self.StrengthMultiplierRoundUpCheckBox = QCheckBox()
        self.StrengthMultiplierRoundUpCheckBox.setChecked(StatModifier["Strength Multiplier Round Up"])
        self.StrengthMultiplierRoundUpCheckBox.stateChanged.connect(self.UpdateStatModifier)

        self.StrengthMinSpinBox = QSpinBox()
        self.StrengthMinSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.StrengthMinSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.StrengthMinSpinBox.setButtonSymbols(self.StrengthMinSpinBox.NoButtons)
        self.StrengthMinSpinBox.setRange(-1, 1000000000)
        self.StrengthMinSpinBox.setSpecialValueText("None")
        self.StrengthMinSpinBox.setValue(StatModifier["Strength Min"] if StatModifier["Strength Min"] is not None else -1)
        self.StrengthMinSpinBox.valueChanged.connect(self.UpdateStatModifier)

        self.StrengthMaxSpinBox = QSpinBox()
        self.StrengthMaxSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.StrengthMaxSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.StrengthMaxSpinBox.setButtonSymbols(self.StrengthMaxSpinBox.NoButtons)
        self.StrengthMaxSpinBox.setRange(-1, 1000000000)
        self.StrengthMaxSpinBox.setSpecialValueText("None")
        self.StrengthMaxSpinBox.setValue(StatModifier["Strength Max"] if StatModifier["Strength Max"] is not None else -1)
        self.StrengthMaxSpinBox.valueChanged.connect(self.UpdateStatModifier)

        self.MultipliersList.append((self.StrengthMultiplierLabel, self.StrengthMultiplierSpinBox, self.StrengthMultiplierRoundUpCheckBox, self.StrengthMinSpinBox, self.StrengthMaxSpinBox))

        # Dexterity Multiplier
        self.DexterityMultiplierLabel = QLabel("Dexterity")
        self.DexterityMultiplierLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.DexterityMultiplierSpinBox = QDoubleSpinBox()
        self.DexterityMultiplierSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.DexterityMultiplierSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.DexterityMultiplierSpinBox.setButtonSymbols(self.DexterityMultiplierSpinBox.NoButtons)
        self.DexterityMultiplierSpinBox.setRange(-1000000000.0, 1000000000.0)
        self.DexterityMultiplierSpinBox.setValue(StatModifier["Dexterity Multiplier"])
        self.DexterityMultiplierSpinBox.valueChanged.connect(self.UpdateStatModifier)

        self.DexterityMultiplierRoundUpCheckBox = QCheckBox()
        self.DexterityMultiplierRoundUpCheckBox.setChecked(StatModifier["Dexterity Multiplier Round Up"])
        self.DexterityMultiplierRoundUpCheckBox.stateChanged.connect(self.UpdateStatModifier)

        self.DexterityMinSpinBox = QSpinBox()
        self.DexterityMinSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.DexterityMinSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.DexterityMinSpinBox.setButtonSymbols(self.DexterityMinSpinBox.NoButtons)
        self.DexterityMinSpinBox.setRange(-1, 1000000000)
        self.DexterityMinSpinBox.setSpecialValueText("None")
        self.DexterityMinSpinBox.setValue(StatModifier["Dexterity Min"] if StatModifier["Dexterity Min"] is not None else -1)
        self.DexterityMinSpinBox.valueChanged.connect(self.UpdateStatModifier)

        self.DexterityMaxSpinBox = QSpinBox()
        self.DexterityMaxSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.DexterityMaxSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.DexterityMaxSpinBox.setButtonSymbols(self.DexterityMaxSpinBox.NoButtons)
        self.DexterityMaxSpinBox.setRange(-1, 1000000000)
        self.DexterityMaxSpinBox.setSpecialValueText("None")
        self.DexterityMaxSpinBox.setValue(StatModifier["Dexterity Max"] if StatModifier["Dexterity Max"] is not None else -1)
        self.DexterityMaxSpinBox.valueChanged.connect(self.UpdateStatModifier)

        self.MultipliersList.append((self.DexterityMultiplierLabel, self.DexterityMultiplierSpinBox, self.DexterityMultiplierRoundUpCheckBox, self.DexterityMinSpinBox, self.DexterityMaxSpinBox))

        # Constitution Multiplier
        self.ConstitutionMultiplierLabel = QLabel("Constitution")
        self.ConstitutionMultiplierLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.ConstitutionMultiplierSpinBox = QDoubleSpinBox()
        self.ConstitutionMultiplierSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.ConstitutionMultiplierSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ConstitutionMultiplierSpinBox.setButtonSymbols(self.ConstitutionMultiplierSpinBox.NoButtons)
        self.ConstitutionMultiplierSpinBox.setRange(-1000000000.0, 1000000000.0)
        self.ConstitutionMultiplierSpinBox.setValue(StatModifier["Constitution Multiplier"])
        self.ConstitutionMultiplierSpinBox.valueChanged.connect(self.UpdateStatModifier)

        self.ConstitutionMultiplierRoundUpCheckBox = QCheckBox()
        self.ConstitutionMultiplierRoundUpCheckBox.setChecked(StatModifier["Constitution Multiplier Round Up"])
        self.ConstitutionMultiplierRoundUpCheckBox.stateChanged.connect(self.UpdateStatModifier)

        self.ConstitutionMinSpinBox = QSpinBox()
        self.ConstitutionMinSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.ConstitutionMinSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ConstitutionMinSpinBox.setButtonSymbols(self.ConstitutionMinSpinBox.NoButtons)
        self.ConstitutionMinSpinBox.setRange(-1, 1000000000)
        self.ConstitutionMinSpinBox.setSpecialValueText("None")
        self.ConstitutionMinSpinBox.setValue(StatModifier["Constitution Min"] if StatModifier["Constitution Min"] is not None else -1)
        self.ConstitutionMinSpinBox.valueChanged.connect(self.UpdateStatModifier)

        self.ConstitutionMaxSpinBox = QSpinBox()
        self.ConstitutionMaxSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.ConstitutionMaxSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ConstitutionMaxSpinBox.setButtonSymbols(self.ConstitutionMaxSpinBox.NoButtons)
        self.ConstitutionMaxSpinBox.setRange(-1, 1000000000)
        self.ConstitutionMaxSpinBox.setSpecialValueText("None")
        self.ConstitutionMaxSpinBox.setValue(StatModifier["Constitution Max"] if StatModifier["Constitution Max"] is not None else -1)
        self.ConstitutionMaxSpinBox.valueChanged.connect(self.UpdateStatModifier)

        self.MultipliersList.append((self.ConstitutionMultiplierLabel, self.ConstitutionMultiplierSpinBox, self.ConstitutionMultiplierRoundUpCheckBox, self.ConstitutionMinSpinBox, self.ConstitutionMaxSpinBox))

        # Intelligence Multiplier
        self.IntelligenceMultiplierLabel = QLabel("Intelligence")
        self.IntelligenceMultiplierLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.IntelligenceMultiplierSpinBox = QDoubleSpinBox()
        self.IntelligenceMultiplierSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.IntelligenceMultiplierSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.IntelligenceMultiplierSpinBox.setButtonSymbols(self.IntelligenceMultiplierSpinBox.NoButtons)
        self.IntelligenceMultiplierSpinBox.setRange(-1000000000.0, 1000000000.0)
        self.IntelligenceMultiplierSpinBox.setValue(StatModifier["Intelligence Multiplier"])
        self.IntelligenceMultiplierSpinBox.valueChanged.connect(self.UpdateStatModifier)

        self.IntelligenceMultiplierRoundUpCheckBox = QCheckBox()
        self.IntelligenceMultiplierRoundUpCheckBox.setChecked(StatModifier["Intelligence Multiplier Round Up"])
        self.IntelligenceMultiplierRoundUpCheckBox.stateChanged.connect(self.UpdateStatModifier)

        self.IntelligenceMinSpinBox = QSpinBox()
        self.IntelligenceMinSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.IntelligenceMinSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.IntelligenceMinSpinBox.setButtonSymbols(self.IntelligenceMinSpinBox.NoButtons)
        self.IntelligenceMinSpinBox.setRange(-1, 1000000000)
        self.IntelligenceMinSpinBox.setSpecialValueText("None")
        self.IntelligenceMinSpinBox.setValue(StatModifier["Intelligence Min"] if StatModifier["Intelligence Min"] is not None else -1)
        self.IntelligenceMinSpinBox.valueChanged.connect(self.UpdateStatModifier)

        self.IntelligenceMaxSpinBox = QSpinBox()
        self.IntelligenceMaxSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.IntelligenceMaxSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.IntelligenceMaxSpinBox.setButtonSymbols(self.IntelligenceMaxSpinBox.NoButtons)
        self.IntelligenceMaxSpinBox.setRange(-1, 1000000000)
        self.IntelligenceMaxSpinBox.setSpecialValueText("None")
        self.IntelligenceMaxSpinBox.setValue(StatModifier["Intelligence Max"] if StatModifier["Intelligence Max"] is not None else -1)
        self.IntelligenceMaxSpinBox.valueChanged.connect(self.UpdateStatModifier)

        self.MultipliersList.append((self.IntelligenceMultiplierLabel, self.IntelligenceMultiplierSpinBox, self.IntelligenceMultiplierRoundUpCheckBox, self.IntelligenceMinSpinBox, self.IntelligenceMaxSpinBox))

        # Wisdom Multiplier
        self.WisdomMultiplierLabel = QLabel("Wisdom")
        self.WisdomMultiplierLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.WisdomMultiplierSpinBox = QDoubleSpinBox()
        self.WisdomMultiplierSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.WisdomMultiplierSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.WisdomMultiplierSpinBox.setButtonSymbols(self.WisdomMultiplierSpinBox.NoButtons)
        self.WisdomMultiplierSpinBox.setRange(-1000000000.0, 1000000000.0)
        self.WisdomMultiplierSpinBox.setValue(StatModifier["Wisdom Multiplier"])
        self.WisdomMultiplierSpinBox.valueChanged.connect(self.UpdateStatModifier)

        self.WisdomMultiplierRoundUpCheckBox = QCheckBox()
        self.WisdomMultiplierRoundUpCheckBox.setChecked(StatModifier["Wisdom Multiplier Round Up"])
        self.WisdomMultiplierRoundUpCheckBox.stateChanged.connect(self.UpdateStatModifier)

        self.WisdomMinSpinBox = QSpinBox()
        self.WisdomMinSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.WisdomMinSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.WisdomMinSpinBox.setButtonSymbols(self.WisdomMinSpinBox.NoButtons)
        self.WisdomMinSpinBox.setRange(-1, 1000000000)
        self.WisdomMinSpinBox.setSpecialValueText("None")
        self.WisdomMinSpinBox.setValue(StatModifier["Wisdom Min"] if StatModifier["Wisdom Min"] is not None else -1)
        self.WisdomMinSpinBox.valueChanged.connect(self.UpdateStatModifier)

        self.WisdomMaxSpinBox = QSpinBox()
        self.WisdomMaxSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.WisdomMaxSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.WisdomMaxSpinBox.setButtonSymbols(self.WisdomMaxSpinBox.NoButtons)
        self.WisdomMaxSpinBox.setRange(-1, 1000000000)
        self.WisdomMaxSpinBox.setSpecialValueText("None")
        self.WisdomMaxSpinBox.setValue(StatModifier["Wisdom Max"] if StatModifier["Wisdom Max"] is not None else -1)
        self.WisdomMaxSpinBox.valueChanged.connect(self.UpdateStatModifier)

        self.MultipliersList.append((self.WisdomMultiplierLabel, self.WisdomMultiplierSpinBox, self.WisdomMultiplierRoundUpCheckBox, self.WisdomMinSpinBox, self.WisdomMaxSpinBox))

        # Charisma Multiplier
        self.CharismaMultiplierLabel = QLabel("Charisma")
        self.CharismaMultiplierLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.CharismaMultiplierSpinBox = QDoubleSpinBox()
        self.CharismaMultiplierSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CharismaMultiplierSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.CharismaMultiplierSpinBox.setButtonSymbols(self.CharismaMultiplierSpinBox.NoButtons)
        self.CharismaMultiplierSpinBox.setRange(-1000000000.0, 1000000000.0)
        self.CharismaMultiplierSpinBox.setValue(StatModifier["Charisma Multiplier"])
        self.CharismaMultiplierSpinBox.valueChanged.connect(self.UpdateStatModifier)

        self.CharismaMultiplierRoundUpCheckBox = QCheckBox()
        self.CharismaMultiplierRoundUpCheckBox.setChecked(StatModifier["Charisma Multiplier Round Up"])
        self.CharismaMultiplierRoundUpCheckBox.stateChanged.connect(self.UpdateStatModifier)

        self.CharismaMinSpinBox = QSpinBox()
        self.CharismaMinSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CharismaMinSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.CharismaMinSpinBox.setButtonSymbols(self.CharismaMinSpinBox.NoButtons)
        self.CharismaMinSpinBox.setRange(-1, 1000000000)
        self.CharismaMinSpinBox.setSpecialValueText("None")
        self.CharismaMinSpinBox.setValue(StatModifier["Charisma Min"] if StatModifier["Charisma Min"] is not None else -1)
        self.CharismaMinSpinBox.valueChanged.connect(self.UpdateStatModifier)

        self.CharismaMaxSpinBox = QSpinBox()
        self.CharismaMaxSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CharismaMaxSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.CharismaMaxSpinBox.setButtonSymbols(self.CharismaMaxSpinBox.NoButtons)
        self.CharismaMaxSpinBox.setRange(-1, 1000000000)
        self.CharismaMaxSpinBox.setSpecialValueText("None")
        self.CharismaMaxSpinBox.setValue(StatModifier["Charisma Max"] if StatModifier["Charisma Max"] is not None else -1)
        self.CharismaMaxSpinBox.valueChanged.connect(self.UpdateStatModifier)

        self.MultipliersList.append((self.CharismaMultiplierLabel, self.CharismaMultiplierSpinBox, self.CharismaMultiplierRoundUpCheckBox, self.CharismaMinSpinBox, self.CharismaMaxSpinBox))

        # Proficiency Multiplier
        self.ProficiencyMultiplierLabel = QLabel("Proficiency")
        self.ProficiencyMultiplierLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.ProficiencyMultiplierSpinBox = QDoubleSpinBox()
        self.ProficiencyMultiplierSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.ProficiencyMultiplierSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ProficiencyMultiplierSpinBox.setButtonSymbols(self.ProficiencyMultiplierSpinBox.NoButtons)
        self.ProficiencyMultiplierSpinBox.setRange(-1000000000.0, 1000000000.0)
        self.ProficiencyMultiplierSpinBox.setValue(StatModifier["Proficiency Multiplier"])
        self.ProficiencyMultiplierSpinBox.valueChanged.connect(self.UpdateStatModifier)

        self.ProficiencyMultiplierRoundUpCheckBox = QCheckBox()
        self.ProficiencyMultiplierRoundUpCheckBox.setChecked(StatModifier["Proficiency Multiplier Round Up"])
        self.ProficiencyMultiplierRoundUpCheckBox.stateChanged.connect(self.UpdateStatModifier)

        self.ProficiencyMinSpinBox = QSpinBox()
        self.ProficiencyMinSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.ProficiencyMinSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ProficiencyMinSpinBox.setButtonSymbols(self.ProficiencyMinSpinBox.NoButtons)
        self.ProficiencyMinSpinBox.setRange(-1, 1000000000)
        self.ProficiencyMinSpinBox.setSpecialValueText("None")
        self.ProficiencyMinSpinBox.setValue(StatModifier["Proficiency Min"] if StatModifier["Proficiency Min"] is not None else -1)
        self.ProficiencyMinSpinBox.valueChanged.connect(self.UpdateStatModifier)

        self.ProficiencyMaxSpinBox = QSpinBox()
        self.ProficiencyMaxSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.ProficiencyMaxSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ProficiencyMaxSpinBox.setButtonSymbols(self.ProficiencyMaxSpinBox.NoButtons)
        self.ProficiencyMaxSpinBox.setRange(-1, 1000000000)
        self.ProficiencyMaxSpinBox.setSpecialValueText("None")
        self.ProficiencyMaxSpinBox.setValue(StatModifier["Proficiency Max"] if StatModifier["Proficiency Max"] is not None else -1)
        self.ProficiencyMaxSpinBox.valueChanged.connect(self.UpdateStatModifier)

        self.MultipliersList.append((self.ProficiencyMultiplierLabel, self.ProficiencyMultiplierSpinBox, self.ProficiencyMultiplierRoundUpCheckBox, self.ProficiencyMinSpinBox, self.ProficiencyMaxSpinBox))

        # Level Multiplier
        if "Level Multiplier" in self.StatModifier:
            self.LevelMultiplierLabel = QLabel("Level")
            self.LevelMultiplierLabel.setAlignment(QtCore.Qt.AlignCenter)

            self.LevelMultiplierSpinBox = QDoubleSpinBox()
            self.LevelMultiplierSpinBox.setSizePolicy(self.InputsSizePolicy)
            self.LevelMultiplierSpinBox.setAlignment(QtCore.Qt.AlignCenter)
            self.LevelMultiplierSpinBox.setButtonSymbols(self.LevelMultiplierSpinBox.NoButtons)
            self.LevelMultiplierSpinBox.setRange(-1000000000.0, 1000000000.0)
            self.LevelMultiplierSpinBox.setValue(StatModifier["Level Multiplier"])
            self.LevelMultiplierSpinBox.valueChanged.connect(self.UpdateStatModifier)

            self.LevelMultiplierRoundUpCheckBox = QCheckBox()
            self.LevelMultiplierRoundUpCheckBox.setChecked(StatModifier["Level Multiplier Round Up"])
            self.LevelMultiplierRoundUpCheckBox.stateChanged.connect(self.UpdateStatModifier)

            self.LevelMinSpinBox = QSpinBox()
            self.LevelMinSpinBox.setSizePolicy(self.InputsSizePolicy)
            self.LevelMinSpinBox.setAlignment(QtCore.Qt.AlignCenter)
            self.LevelMinSpinBox.setButtonSymbols(self.LevelMinSpinBox.NoButtons)
            self.LevelMinSpinBox.setRange(-1, 1000000000)
            self.LevelMinSpinBox.setSpecialValueText("None")
            self.LevelMinSpinBox.setValue(StatModifier["Level Min"] if StatModifier["Level Min"] is not None else -1)
            self.LevelMinSpinBox.valueChanged.connect(self.UpdateStatModifier)

            self.LevelMaxSpinBox = QSpinBox()
            self.LevelMaxSpinBox.setSizePolicy(self.InputsSizePolicy)
            self.LevelMaxSpinBox.setAlignment(QtCore.Qt.AlignCenter)
            self.LevelMaxSpinBox.setButtonSymbols(self.LevelMaxSpinBox.NoButtons)
            self.LevelMaxSpinBox.setRange(-1, 1000000000)
            self.LevelMaxSpinBox.setSpecialValueText("None")
            self.LevelMaxSpinBox.setValue(StatModifier["Level Max"] if StatModifier["Level Max"] is not None else -1)
            self.LevelMaxSpinBox.valueChanged.connect(self.UpdateStatModifier)

            self.MultipliersList.append((self.LevelMultiplierLabel, self.LevelMultiplierSpinBox, self.LevelMultiplierRoundUpCheckBox, self.LevelMinSpinBox, self.LevelMaxSpinBox))

        # Manual Modifier
        self.ManualModifierLabel = QLabel("Manual Modifier")
        self.ManualModifierLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ManualModifierLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.ManualModifierLabel.setMargin(5)
        self.ManualModifierSpinBox = QSpinBox()
        self.ManualModifierSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.ManualModifierSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ManualModifierSpinBox.setButtonSymbols(self.ManualModifierSpinBox.NoButtons)
        self.ManualModifierSpinBox.setRange(-1000000000, 1000000000)
        self.ManualModifierSpinBox.setValue(StatModifier["Manual Modifier"])
        self.ManualModifierSpinBox.valueChanged.connect(self.UpdateStatModifier)

        # Buttons
        self.DoneButton = QPushButton("Done")
        self.DoneButton.clicked.connect(self.Done)
        self.CancelButton = QPushButton("Cancel")
        self.CancelButton.clicked.connect(self.Cancel)

        # Layout
        self.Layout = QGridLayout()
        self.Layout.addWidget(self.PromptLabel, 0, 0, 1, 2)

        if "Base AC" in self.StatModifier:
            self.Layout.addWidget(self.BaseACLabel, 1, 0, 1, 2)
            self.Layout.addWidget(self.BaseACSpinBox, 2, 0, 1, 2)

        self.MultipliersLayout = QGridLayout()
        for Row in range(len(self.MultipliersList)):
            RowWidgets = self.MultipliersList[Row]
            self.MultipliersLayout.addWidget(RowWidgets[0], Row, 0)
            self.MultipliersLayout.addWidget(RowWidgets[1], Row, 1)
            self.MultipliersLayout.addWidget(RowWidgets[2], Row, 2, QtCore.Qt.AlignCenter)
            self.MultipliersLayout.addWidget(RowWidgets[3], Row, 3)
            self.MultipliersLayout.addWidget(RowWidgets[4], Row, 4)
        for Row in range(1, len(self.MultipliersList)):
            self.MultipliersLayout.setRowStretch(Row, 1)
        for Column in [1, 3, 4]:
            self.MultipliersLayout.setColumnStretch(Column, 1)
        self.Layout.addLayout(self.MultipliersLayout, 3, 0, 1, 2)

        self.Layout.addWidget(self.ManualModifierLabel, 4, 0, 1, 2)
        self.Layout.addWidget(self.ManualModifierSpinBox, 5, 0, 1, 2)

        self.Layout.addWidget(self.DoneButton, 6, 0)
        self.Layout.addWidget(self.CancelButton, 6, 1)

        self.Layout.setRowStretch(3, 1)

        self.setLayout(self.Layout)

        # Set Window Title and Icon
        self.setWindowTitle(self.CharacterWindow.ScriptName)
        self.setWindowIcon(self.CharacterWindow.WindowIcon)

        # Update Display
        self.UpdateDisplay()

        # Execute Dialog
        self.exec_()

    def UpdateStatModifier(self):
        if not self.ValidInput():
            return

        # Base AC
        if "Base AC" in self.StatModifier:
            self.StatModifier["Base AC"] = self.BaseACSpinBox.value()

        # Strength Multiplier
        self.StatModifier["Strength Multiplier"] = self.StrengthMultiplierSpinBox.value()
        self.StatModifier["Strength Multiplier Round Up"] = self.StrengthMultiplierRoundUpCheckBox.isChecked()
        self.StatModifier["Strength Min"] = self.StrengthMinSpinBox.value() if self.StrengthMinSpinBox.value() != -1 else None
        self.StatModifier["Strength Max"] = self.StrengthMaxSpinBox.value() if self.StrengthMaxSpinBox.value() != -1 else None

        # Dexterity Multiplier
        self.StatModifier["Dexterity Multiplier"] = self.DexterityMultiplierSpinBox.value()
        self.StatModifier["Dexterity Multiplier Round Up"] = self.DexterityMultiplierRoundUpCheckBox.isChecked()
        self.StatModifier["Dexterity Min"] = self.DexterityMinSpinBox.value() if self.DexterityMinSpinBox.value() != -1 else None
        self.StatModifier["Dexterity Max"] = self.DexterityMaxSpinBox.value() if self.DexterityMaxSpinBox.value() != -1 else None

        # Constitution Multiplier
        self.StatModifier["Constitution Multiplier"] = self.ConstitutionMultiplierSpinBox.value()
        self.StatModifier["Constitution Multiplier Round Up"] = self.ConstitutionMultiplierRoundUpCheckBox.isChecked()
        self.StatModifier["Constitution Min"] = self.ConstitutionMinSpinBox.value() if self.ConstitutionMinSpinBox.value() != -1 else None
        self.StatModifier["Constitution Max"] = self.ConstitutionMaxSpinBox.value() if self.ConstitutionMaxSpinBox.value() != -1 else None

        # Intelligence Multiplier
        self.StatModifier["Intelligence Multiplier"] = self.IntelligenceMultiplierSpinBox.value()
        self.StatModifier["Intelligence Multiplier Round Up"] = self.IntelligenceMultiplierRoundUpCheckBox.isChecked()
        self.StatModifier["Intelligence Min"] = self.IntelligenceMinSpinBox.value() if self.IntelligenceMinSpinBox.value() != -1 else None
        self.StatModifier["Intelligence Max"] = self.IntelligenceMaxSpinBox.value() if self.IntelligenceMaxSpinBox.value() != -1 else None

        # Wisdom Multiplier
        self.StatModifier["Wisdom Multiplier"] = self.WisdomMultiplierSpinBox.value()
        self.StatModifier["Wisdom Multiplier Round Up"] = self.WisdomMultiplierRoundUpCheckBox.isChecked()
        self.StatModifier["Wisdom Min"] = self.WisdomMinSpinBox.value() if self.WisdomMinSpinBox.value() != -1 else None
        self.StatModifier["Wisdom Max"] = self.WisdomMaxSpinBox.value() if self.WisdomMaxSpinBox.value() != -1 else None

        # Charisma Multiplier
        self.StatModifier["Charisma Multiplier"] = self.CharismaMultiplierSpinBox.value()
        self.StatModifier["Charisma Multiplier Round Up"] = self.CharismaMultiplierRoundUpCheckBox.isChecked()
        self.StatModifier["Charisma Min"] = self.CharismaMinSpinBox.value() if self.CharismaMinSpinBox.value() != -1 else None
        self.StatModifier["Charisma Max"] = self.CharismaMaxSpinBox.value() if self.CharismaMaxSpinBox.value() != -1 else None

        # Proficiency Multiplier
        self.StatModifier["Proficiency Multiplier"] = self.ProficiencyMultiplierSpinBox.value()
        self.StatModifier["Proficiency Multiplier Round Up"] = self.ProficiencyMultiplierRoundUpCheckBox.isChecked()
        self.StatModifier["Proficiency Min"] = self.ProficiencyMinSpinBox.value() if self.ProficiencyMinSpinBox.value() != -1 else None
        self.StatModifier["Proficiency Max"] = self.ProficiencyMaxSpinBox.value() if self.ProficiencyMaxSpinBox.value() != -1 else None

        # Level Multiplier
        if "Level Multiplier" in self.StatModifier:
            self.StatModifier["Level Multiplier"] = self.LevelMultiplierSpinBox.value()
            self.StatModifier["Level Multiplier Round Up"] = self.LevelMultiplierRoundUpCheckBox.isChecked()
            self.StatModifier["Level Min"] = self.LevelMinSpinBox.value() if self.LevelMinSpinBox.value() != -1 else None
            self.StatModifier["Level Max"] = self.LevelMaxSpinBox.value() if self.LevelMaxSpinBox.value() != -1 else None

        # Manual Modifier
        self.StatModifier["Manual Modifier"] = self.ManualModifierSpinBox.value()

        # Update Unsaved Changes
        self.UnsavedChanges = True

        # Update Display
        self.UpdateDisplay()

    def UpdateDisplay(self):
        SpinBoxes = [self.StrengthMultiplierSpinBox, self.DexterityMultiplierSpinBox, self.ConstitutionMultiplierSpinBox, self.IntelligenceMultiplierSpinBox, self.WisdomMultiplierSpinBox, self.CharismaMultiplierSpinBox, self.ProficiencyMultiplierSpinBox, self.ManualModifierSpinBox]
        if "Base AC" in self.StatModifier:
            SpinBoxes.append(self.BaseACSpinBox)
        if "Level Multiplier" in self.StatModifier:
            SpinBoxes.append(self.LevelMultiplierSpinBox)

        for SpinBox in SpinBoxes:
            if type(SpinBox) is QDoubleSpinBox:
                StyleSheetPrefix = "QDoubleSpinBox "
            else:
                StyleSheetPrefix = "QSpinBox "
            PositiveStyleSheet = f"{StyleSheetPrefix}{{background-color: darkgreen;}}"
            ZeroStyleSheet = f"{StyleSheetPrefix}{{}}"
            NegativeStyleSheet = f"{StyleSheetPrefix}{{background-color: darkred;}}"
            if SpinBox.value() > 0.0:
                SpinBox.setStyleSheet(PositiveStyleSheet)
            elif SpinBox.value() == 0.0:
                SpinBox.setStyleSheet(ZeroStyleSheet)
            else:
                SpinBox.setStyleSheet(NegativeStyleSheet)

    def Done(self):
        if self.ValidInput(Alert=True):
            self.close()

    def Cancel(self):
        self.StatModifier.update(self.StatModifierOriginalState)
        self.UnsavedChanges = False
        self.Cancelled = True
        self.close()

    def ValidInput(self, Alert=False):
        MinsAndMaxes = [(self.StrengthMinSpinBox, self.StrengthMaxSpinBox), (self.DexterityMinSpinBox, self.DexterityMaxSpinBox), (self.ConstitutionMinSpinBox, self.ConstitutionMaxSpinBox), (self.IntelligenceMinSpinBox, self.IntelligenceMaxSpinBox), (self.WisdomMinSpinBox, self.WisdomMaxSpinBox), (self.CharismaMinSpinBox, self.CharismaMaxSpinBox), (self.ProficiencyMinSpinBox, self.ProficiencyMaxSpinBox)]
        if "Level Multiplier" in self.StatModifier:
            MinsAndMaxes.append((self.LevelMinSpinBox, self.LevelMaxSpinBox))
        for MinAndMax in MinsAndMaxes:
            if MinAndMax[0].value() > MinAndMax[1].value():
                if Alert:
                    self.CharacterWindow.DisplayMessageBox("Multiplier minimums must be less than or equal to maximums.", Icon=QMessageBox.Warning, Parent=self)
                return False
        return True
