from PyQt5 import QtCore
from PyQt5.QtWidgets import QComboBox, QFrame, QGridLayout, QInputDialog, QLabel, QSizePolicy, QSpinBox

from Interface.Widgets.CenteredLineEdit import CenteredLineEdit
from Interface.Widgets.IconButtons import DamageButton, HealButton
from Interface.Widgets.IndentingTextEdit import IndentingTextEdit
from Interface.Widgets.ToggleButtons import ConcentratingButton


class NonPlayerCharacterStatsWidget(QFrame):
    def __init__(self, CharacterWindow):
        # Initialize Frame
        super().__init__()

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Styles
        self.SectionLabelStyle = "QLabel {font-size: 10pt; font-weight: bold;}"
        self.HPSpinBoxStyle = "QSpinBox {font-size: 16pt;}"
        self.NegativeCurrentHealthSpinBoxStyle = "QSpinBox {font-size: 16pt; background-color: darkred;}"
        self.AbilityScoreModifierSpinBoxStyle = "QSpinBox {font-size: 16pt}"

        # Header Label Margin
        self.HeaderLabelMargin = 5

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Create Vitality Table
        self.CreateVitalityTable()

        # Create Ability Score Modifiers
        self.CreateAbilityScoreModifiers()

        # Create Miscellaneous String Inputs
        self.CreateMiscStringInputs()

        # Create Concentrating Button
        self.CreateConcentratingButton()

        # Create and Set Layout
        self.CreateAndSetLayout()

    def CreateVitalityTable(self):
        # Header Label
        self.VitalityLabel = QLabel("Vitality")
        self.VitalityLabel.setStyleSheet(self.SectionLabelStyle)
        self.VitalityLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.VitalityLabel.setMargin(self.HeaderLabelMargin)

        # Temp HP
        self.TempHPLabel = QLabel("Temp HP:")
        self.TempHPLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.TempHPSpinBox = QSpinBox()
        self.TempHPSpinBox.setRange(0, 1000000000)
        self.TempHPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.TempHPSpinBox.setStyleSheet(self.HPSpinBoxStyle)
        self.TempHPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.TempHPSpinBox.setButtonSymbols(self.TempHPSpinBox.NoButtons)
        self.TempHPSpinBox.setValue(0)
        self.TempHPSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat("Temp Health", self.TempHPSpinBox.value()))

        # Current HP
        self.CurrentHPLabel = QLabel("Current HP:")
        self.CurrentHPLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.CurrentHPSpinBox = QSpinBox()
        self.CurrentHPSpinBox.setRange(-1000000000, 1000000000)
        self.CurrentHPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.CurrentHPSpinBox.setStyleSheet(self.HPSpinBoxStyle)
        self.CurrentHPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CurrentHPSpinBox.setButtonSymbols(self.CurrentHPSpinBox.NoButtons)
        self.CurrentHPSpinBox.setValue(1)
        self.CurrentHPSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat("Current Health", self.CurrentHPSpinBox.value()))

        # Max HP
        self.MaxHPLabel = QLabel("Max HP:")
        self.MaxHPLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.MaxHPSpinBox = QSpinBox()
        self.MaxHPSpinBox.setRange(0, 1000000000)
        self.MaxHPSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPSpinBox.setStyleSheet(self.HPSpinBoxStyle)
        self.MaxHPSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MaxHPSpinBox.setButtonSymbols(self.MaxHPSpinBox.NoButtons)
        self.MaxHPSpinBox.setValue(1)
        self.MaxHPSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat("Max Health", self.MaxHPSpinBox.value()))

        # HP Buttons
        self.DamageButton = DamageButton(self.Damage)
        self.HealButton = HealButton(self.Heal)

    def CreateAbilityScoreModifiers(self):
        # Header Label
        self.AbilityScoreModifiersLabel = QLabel("Ability Score Modifiers")
        self.AbilityScoreModifiersLabel.setStyleSheet(self.SectionLabelStyle)
        self.AbilityScoreModifiersLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.AbilityScoreModifiersLabel.setMargin(self.HeaderLabelMargin)

        # Strength Modifier
        self.StrengthModifierLabel = QLabel("Strength")
        self.StrengthModifierLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.StrengthModifierLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.StrengthModifierLabel.setMargin(5)

        self.StrengthModifierSpinBox = QSpinBox()
        self.StrengthModifierSpinBox.setRange(-1000000000, 1000000000)
        self.StrengthModifierSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.StrengthModifierSpinBox.setStyleSheet(self.AbilityScoreModifierSpinBoxStyle)
        self.StrengthModifierSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.StrengthModifierSpinBox.setButtonSymbols(self.StrengthModifierSpinBox.NoButtons)
        self.StrengthModifierSpinBox.setMaximumWidth(75)
        self.StrengthModifierSpinBox.setValue(0)
        self.StrengthModifierSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Ability Score Modifiers", "Strength"), self.StrengthModifierSpinBox.value()))

        # Dexterity Modifier
        self.DexterityModifierLabel = QLabel("Dexterity")
        self.DexterityModifierLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.DexterityModifierLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.DexterityModifierLabel.setMargin(5)

        self.DexterityModifierSpinBox = QSpinBox()
        self.DexterityModifierSpinBox.setRange(-1000000000, 1000000000)
        self.DexterityModifierSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.DexterityModifierSpinBox.setStyleSheet(self.AbilityScoreModifierSpinBoxStyle)
        self.DexterityModifierSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.DexterityModifierSpinBox.setButtonSymbols(self.DexterityModifierSpinBox.NoButtons)
        self.DexterityModifierSpinBox.setMaximumWidth(75)
        self.DexterityModifierSpinBox.setValue(0)
        self.DexterityModifierSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Ability Score Modifiers", "Dexterity"), self.DexterityModifierSpinBox.value()))

        # Constitution Modifier
        self.ConstitutionModifierLabel = QLabel("Constitution")
        self.ConstitutionModifierLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ConstitutionModifierLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.ConstitutionModifierLabel.setMargin(5)

        self.ConstitutionModifierSpinBox = QSpinBox()
        self.ConstitutionModifierSpinBox.setRange(-1000000000, 1000000000)
        self.ConstitutionModifierSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ConstitutionModifierSpinBox.setStyleSheet(self.AbilityScoreModifierSpinBoxStyle)
        self.ConstitutionModifierSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.ConstitutionModifierSpinBox.setButtonSymbols(self.ConstitutionModifierSpinBox.NoButtons)
        self.ConstitutionModifierSpinBox.setMaximumWidth(75)
        self.ConstitutionModifierSpinBox.setValue(0)
        self.ConstitutionModifierSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Ability Score Modifiers", "Constitution"), self.ConstitutionModifierSpinBox.value()))

        # Intelligence Modifier
        self.IntelligenceModifierLabel = QLabel("Intelligence")
        self.IntelligenceModifierLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.IntelligenceModifierLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.IntelligenceModifierLabel.setMargin(5)

        self.IntelligenceModifierSpinBox = QSpinBox()
        self.IntelligenceModifierSpinBox.setRange(-1000000000, 1000000000)
        self.IntelligenceModifierSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.IntelligenceModifierSpinBox.setStyleSheet(self.AbilityScoreModifierSpinBoxStyle)
        self.IntelligenceModifierSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.IntelligenceModifierSpinBox.setButtonSymbols(self.IntelligenceModifierSpinBox.NoButtons)
        self.IntelligenceModifierSpinBox.setMaximumWidth(75)
        self.IntelligenceModifierSpinBox.setValue(0)
        self.IntelligenceModifierSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Ability Score Modifiers", "Intelligence"), self.IntelligenceModifierSpinBox.value()))

        # Wisdom Modifier
        self.WisdomModifierLabel = QLabel("Wisdom")
        self.WisdomModifierLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.WisdomModifierLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.WisdomModifierLabel.setMargin(5)

        self.WisdomModifierSpinBox = QSpinBox()
        self.WisdomModifierSpinBox.setRange(-1000000000, 1000000000)
        self.WisdomModifierSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.WisdomModifierSpinBox.setStyleSheet(self.AbilityScoreModifierSpinBoxStyle)
        self.WisdomModifierSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.WisdomModifierSpinBox.setButtonSymbols(self.WisdomModifierSpinBox.NoButtons)
        self.WisdomModifierSpinBox.setMaximumWidth(75)
        self.WisdomModifierSpinBox.setValue(0)
        self.WisdomModifierSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Ability Score Modifiers", "Wisdom"), self.WisdomModifierSpinBox.value()))

        # Charisma Modifier
        self.CharismaModifierLabel = QLabel("Charisma")
        self.CharismaModifierLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.CharismaModifierLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.CharismaModifierLabel.setMargin(5)

        self.CharismaModifierSpinBox = QSpinBox()
        self.CharismaModifierSpinBox.setRange(-1000000000, 1000000000)
        self.CharismaModifierSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.CharismaModifierSpinBox.setStyleSheet(self.AbilityScoreModifierSpinBoxStyle)
        self.CharismaModifierSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CharismaModifierSpinBox.setButtonSymbols(self.CharismaModifierSpinBox.NoButtons)
        self.CharismaModifierSpinBox.setMaximumWidth(75)
        self.CharismaModifierSpinBox.setValue(0)
        self.CharismaModifierSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Ability Score Modifiers", "Charisma"), self.CharismaModifierSpinBox.value()))

        # Ability Score Modifiers List
        self.AbilityScoreModifierSpinBoxesList = [(self.StrengthModifierSpinBox, "Strength"), (self.DexterityModifierSpinBox, "Dexterity"), (self.ConstitutionModifierSpinBox, "Constitution"), (self.IntelligenceModifierSpinBox, "Intelligence"), (self.WisdomModifierSpinBox, "Wisdom"), (self.CharismaModifierSpinBox, "Charisma")]

    def CreateMiscStringInputs(self):
        # AC
        self.ACLabel = QLabel("AC")
        self.ACLabel.setStyleSheet(self.SectionLabelStyle)
        self.ACLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ACLabel.setMargin(self.HeaderLabelMargin)

        self.ACLineEdit = CenteredLineEdit()
        self.ACLineEdit.textChanged.connect(lambda: self.CharacterWindow.UpdateStat("AC", self.ACLineEdit.text()))

        # Speed
        self.SpeedLabel = QLabel("Speed")
        self.SpeedLabel.setStyleSheet(self.SectionLabelStyle)
        self.SpeedLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SpeedLabel.setMargin(self.HeaderLabelMargin)

        self.SpeedLineEdit = CenteredLineEdit()
        self.SpeedLineEdit.textChanged.connect(lambda: self.CharacterWindow.UpdateStat("Speed", self.SpeedLineEdit.text()))

        # CR
        self.CRLabel = QLabel("CR")
        self.CRLabel.setStyleSheet(self.SectionLabelStyle)
        self.CRLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.CRLabel.setMargin(self.HeaderLabelMargin)

        self.CRComboBox = QComboBox()
        self.CRComboBox.addItems(["0", "1/8", "1/4", "1/2", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"])
        self.CRComboBox.setEditable(False)
        self.CRComboBox.currentTextChanged.connect(lambda: self.CharacterWindow.UpdateStat("CR", self.CRComboBox.currentText()))

        # Experience
        self.ExperienceLabel = QLabel("Experience")
        self.ExperienceLabel.setStyleSheet(self.SectionLabelStyle)
        self.ExperienceLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ExperienceLabel.setMargin(self.HeaderLabelMargin)

        self.ExperienceLineEdit = CenteredLineEdit()
        self.ExperienceLineEdit.textChanged.connect(lambda: self.CharacterWindow.UpdateStat("Experience", self.ExperienceLineEdit.text()))

        # Skills, Senses, and Languages
        self.SkillsSensesAndLanguagesLabel = QLabel("Skills, Senses, and Languages")
        self.SkillsSensesAndLanguagesLabel.setStyleSheet(self.SectionLabelStyle)
        self.SkillsSensesAndLanguagesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SkillsSensesAndLanguagesLabel.setMargin(self.HeaderLabelMargin)

        self.SkillsSensesAndLanguagesTextEdit = IndentingTextEdit(TextChangedSlot=lambda: self.CharacterWindow.UpdateStat("Skills, Senses, and Languages", self.SkillsSensesAndLanguagesTextEdit.toPlainText()))
        self.SkillsSensesAndLanguagesTextEdit.setTabChangesFocus(True)

        # Special Traits
        self.SpecialTraitsLabel = QLabel("Special Traits")
        self.SpecialTraitsLabel.setStyleSheet(self.SectionLabelStyle)
        self.SpecialTraitsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SpecialTraitsLabel.setMargin(self.HeaderLabelMargin)

        self.SpecialTraitsTextEdit = IndentingTextEdit(TextChangedSlot=lambda: self.CharacterWindow.UpdateStat("Special Traits", self.SpecialTraitsTextEdit.toPlainText()))
        self.SpecialTraitsTextEdit.setTabChangesFocus(True)
        self.SpecialTraitsTextEdit.setMinimumWidth(380)

        # Actions and Reactions
        self.ActionsAndReactionsLabel = QLabel("Actions and Reactions")
        self.ActionsAndReactionsLabel.setStyleSheet(self.SectionLabelStyle)
        self.ActionsAndReactionsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ActionsAndReactionsLabel.setMargin(self.HeaderLabelMargin)

        self.ActionsAndReactionsTextEdit = IndentingTextEdit(TextChangedSlot=lambda: self.CharacterWindow.UpdateStat("Actions and Reactions", self.ActionsAndReactionsTextEdit.toPlainText()))
        self.ActionsAndReactionsTextEdit.setTabChangesFocus(True)
        self.ActionsAndReactionsTextEdit.setMinimumWidth(380)

        # Saving Throws
        self.SavingThrowsLabel = QLabel("Saving Throws")
        self.SavingThrowsLabel.setStyleSheet(self.SectionLabelStyle)
        self.SavingThrowsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SavingThrowsLabel.setMargin(self.HeaderLabelMargin)

        self.SavingThrowsTextEdit = IndentingTextEdit(TextChangedSlot=lambda: self.CharacterWindow.UpdateStat("Saving Throws", self.SavingThrowsTextEdit.toPlainText()))
        self.SavingThrowsTextEdit.setTabChangesFocus(True)
        self.SavingThrowsTextEdit.setMinimumWidth(380)

        # Vulnerabilities, Resistances, and Immunities
        self.VulnerabilitiesResistancesAndImmunitiesLabel = QLabel("Vulnerabilities, Resistances, and Immunities")
        self.VulnerabilitiesResistancesAndImmunitiesLabel.setStyleSheet(self.SectionLabelStyle)
        self.VulnerabilitiesResistancesAndImmunitiesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.VulnerabilitiesResistancesAndImmunitiesLabel.setMargin(self.HeaderLabelMargin)

        self.VulnerabilitiesResistancesAndImmunitiesTextEdit = IndentingTextEdit(TextChangedSlot=lambda: self.CharacterWindow.UpdateStat("Vulnerabilities, Resistances, and Immunities", self.VulnerabilitiesResistancesAndImmunitiesTextEdit.toPlainText()))
        self.VulnerabilitiesResistancesAndImmunitiesTextEdit.setTabChangesFocus(True)
        self.VulnerabilitiesResistancesAndImmunitiesTextEdit.setMinimumWidth(380)

        # Inventory
        self.InventoryLabel = QLabel("Inventory")
        self.InventoryLabel.setStyleSheet(self.SectionLabelStyle)
        self.InventoryLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.InventoryLabel.setMargin(self.HeaderLabelMargin)

        self.InventoryTextEdit = IndentingTextEdit(TextChangedSlot=lambda: self.CharacterWindow.UpdateStat("Inventory", self.InventoryTextEdit.toPlainText()))
        self.InventoryTextEdit.setTabChangesFocus(True)
        self.InventoryTextEdit.setMinimumWidth(380)

        # Notes
        self.NotesLabel = QLabel("Notes")
        self.NotesLabel.setStyleSheet(self.SectionLabelStyle)
        self.NotesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.NotesLabel.setMargin(self.HeaderLabelMargin)

        self.NotesTextEdit = IndentingTextEdit(TextChangedSlot=lambda: self.CharacterWindow.UpdateStat("Notes", self.NotesTextEdit.toPlainText()))
        self.NotesTextEdit.setTabChangesFocus(True)
        self.NotesTextEdit.setMinimumWidth(380)

    def CreateConcentratingButton(self):
        self.ConcentratingButton = ConcentratingButton(self.CharacterWindow)

    def CreateAndSetLayout(self):
        # Create Layout
        self.Layout = QGridLayout()

        # Vitality
        self.VitalityLayout = QGridLayout()
        self.VitalityLayout.addWidget(self.VitalityLabel, 0, 0)
        self.VitalityLayout.addWidget(self.TempHPLabel, 1, 0)
        self.VitalityLayout.addWidget(self.TempHPSpinBox, 2, 0)
        self.VitalityLayout.addWidget(self.CurrentHPLabel, 3, 0)
        self.VitalityLayout.addWidget(self.CurrentHPSpinBox, 4, 0)
        self.VitalityLayout.addWidget(self.MaxHPLabel, 5, 0)
        self.VitalityLayout.addWidget(self.MaxHPSpinBox, 6, 0)
        self.HPButtonsLayout = QGridLayout()
        self.HPButtonsLayout.addWidget(self.DamageButton, 0, 0)
        self.HPButtonsLayout.addWidget(self.HealButton, 0, 1)
        self.VitalityLayout.addLayout(self.HPButtonsLayout, 7, 0)
        for Row in [2, 4, 6]:
            self.VitalityLayout.setRowStretch(Row, 1)
        self.Layout.addLayout(self.VitalityLayout, 0, 0)

        # Ability Score Modifiers
        self.AbilityScoreModifiersLayout = QGridLayout()
        self.AbilityScoreModifiersLayout.addWidget(self.AbilityScoreModifiersLabel, 0, 0, 1, 3)
        self.AbilityScoreModifiersLayout.addWidget(self.StrengthModifierLabel, 1, 0)
        self.AbilityScoreModifiersLayout.addWidget(self.StrengthModifierSpinBox, 2, 0)
        self.AbilityScoreModifiersLayout.addWidget(self.DexterityModifierLabel, 1, 1)
        self.AbilityScoreModifiersLayout.addWidget(self.DexterityModifierSpinBox, 2, 1)
        self.AbilityScoreModifiersLayout.addWidget(self.ConstitutionModifierLabel, 1, 2)
        self.AbilityScoreModifiersLayout.addWidget(self.ConstitutionModifierSpinBox, 2, 2)
        self.AbilityScoreModifiersLayout.addWidget(self.IntelligenceModifierLabel, 3, 0)
        self.AbilityScoreModifiersLayout.addWidget(self.IntelligenceModifierSpinBox, 4, 0)
        self.AbilityScoreModifiersLayout.addWidget(self.WisdomModifierLabel, 3, 1)
        self.AbilityScoreModifiersLayout.addWidget(self.WisdomModifierSpinBox, 4, 1)
        self.AbilityScoreModifiersLayout.addWidget(self.CharismaModifierLabel, 3, 2)
        self.AbilityScoreModifiersLayout.addWidget(self.CharismaModifierSpinBox, 4, 2)
        for Row in [2, 4]:
            self.AbilityScoreModifiersLayout.setRowStretch(Row, 1)
        self.Layout.addLayout(self.AbilityScoreModifiersLayout, 0, 1)

        # AC
        self.ACLayout = QGridLayout()
        self.ACLayout.addWidget(self.ACLabel, 0, 0)
        self.ACLayout.addWidget(self.ACLineEdit, 1, 0)
        self.Layout.addLayout(self.ACLayout, 1, 0)

        # Speed
        self.SpeedLayout = QGridLayout()
        self.SpeedLayout.addWidget(self.SpeedLabel, 0, 0)
        self.SpeedLayout.addWidget(self.SpeedLineEdit, 1, 0)
        self.Layout.addLayout(self.SpeedLayout, 2, 0)

        # CR
        self.CRLayout = QGridLayout()
        self.CRLayout.addWidget(self.CRLabel, 0, 0)
        self.CRLayout.addWidget(self.CRComboBox, 1, 0)
        self.Layout.addLayout(self.CRLayout, 3, 0)

        # Experience
        self.ExperienceLayout = QGridLayout()
        self.ExperienceLayout.addWidget(self.ExperienceLabel, 0, 0)
        self.ExperienceLayout.addWidget(self.ExperienceLineEdit, 1, 0)
        self.Layout.addLayout(self.ExperienceLayout, 4, 0)

        # Skills, Senses, and Languages
        self.SkillsSensesAndLanguagesLayout = QGridLayout()
        self.SkillsSensesAndLanguagesLayout.addWidget(self.SkillsSensesAndLanguagesLabel, 0, 0)
        self.SkillsSensesAndLanguagesLayout.addWidget(self.SkillsSensesAndLanguagesTextEdit, 1, 0)
        self.Layout.addLayout(self.SkillsSensesAndLanguagesLayout, 1, 1, 4, 1)

        # Special Traits
        self.SpecialTraitsLayout = QGridLayout()
        self.SpecialTraitsLayout.addWidget(self.SpecialTraitsLabel, 0, 0)
        self.SpecialTraitsLayout.addWidget(self.SpecialTraitsTextEdit, 1, 0)
        self.Layout.addLayout(self.SpecialTraitsLayout, 0, 2)

        # Actions and Reactions
        self.ActionsAndReactionsLayout = QGridLayout()
        self.ActionsAndReactionsLayout.addWidget(self.ActionsAndReactionsLabel, 0, 0)
        self.ActionsAndReactionsLayout.addWidget(self.ActionsAndReactionsTextEdit, 1, 0)
        self.Layout.addLayout(self.ActionsAndReactionsLayout, 1, 2, 4, 1)

        # Saving Throws
        self.SavingThrowsLayout = QGridLayout()
        self.SavingThrowsLayout.addWidget(self.SavingThrowsLabel, 0, 0)
        self.SavingThrowsLayout.addWidget(self.SavingThrowsTextEdit, 1, 0)
        self.Layout.addLayout(self.SavingThrowsLayout, 5, 0, 1, 2)

        # Vulnerabilities, Resistances, and Immunities
        self.VulnerabilitiesResistancesAndImmunitiesLayout = QGridLayout()
        self.VulnerabilitiesResistancesAndImmunitiesLayout.addWidget(self.VulnerabilitiesResistancesAndImmunitiesLabel, 0, 0)
        self.VulnerabilitiesResistancesAndImmunitiesLayout.addWidget(self.VulnerabilitiesResistancesAndImmunitiesTextEdit, 1, 0)
        self.Layout.addLayout(self.VulnerabilitiesResistancesAndImmunitiesLayout, 6, 0, 1, 2)

        # Inventory
        self.InventoryLayout = QGridLayout()
        self.InventoryLayout.addWidget(self.InventoryLabel, 0, 0)
        self.InventoryLayout.addWidget(self.InventoryTextEdit, 1, 0)
        self.Layout.addLayout(self.InventoryLayout, 5, 2)

        # Notes
        self.NotesLayout = QGridLayout()
        self.NotesLayout.addWidget(self.NotesLabel, 0, 0)
        self.NotesLayout.addWidget(self.NotesTextEdit, 1, 0)
        self.Layout.addLayout(self.NotesLayout, 6, 2)

        # Concentrating Button
        self.Layout.addWidget(self.ConcentratingButton, 7, 0, 1, 3)

        # Layout Stretching
        for Column in range(1, 3):
            self.Layout.setColumnStretch(Column, 1)
        for Row in range(5, 7):
            self.Layout.setRowStretch(Row, 1)

        # Set Layout
        self.setLayout(self.Layout)

    def Damage(self):
        DamageAmount, OK = QInputDialog.getInt(self, "Damage", "How much damage?", 1, 1, 1000000000)
        if OK:
            ConcentrationDC = self.CharacterWindow.NonPlayerCharacter.Damage(DamageAmount)
            self.CharacterWindow.UpdatingFieldsFromNonPlayerCharacter = True
            self.TempHPSpinBox.setValue(self.CharacterWindow.NonPlayerCharacter.Stats["Temp Health"])
            self.CurrentHPSpinBox.setValue(self.CharacterWindow.NonPlayerCharacter.Stats["Current Health"])
            self.CharacterWindow.UpdatingFieldsFromNonPlayerCharacter = False
            self.CharacterWindow.UpdateUnsavedChangesFlag(True)
            if ConcentrationDC is not None:
                self.CharacterWindow.DisplayMessageBox(f"DC {str(ConcentrationDC)} Constitution saving throw required to maintain concentration.", Parent=self)

    def Heal(self):
        HealAmount, OK = QInputDialog.getInt(self, "Heal", "Heal how much?", 1, 1, 1000000000)
        if OK:
            self.CharacterWindow.NonPlayerCharacter.Heal(HealAmount, self.CharacterWindow.NonPlayerCharacter.Stats["Max Health"])
            self.CharacterWindow.UpdatingFieldsFromNonPlayerCharacter = True
            self.CurrentHPSpinBox.setValue(self.CharacterWindow.NonPlayerCharacter.Stats["Current Health"])
            self.CharacterWindow.UpdatingFieldsFromNonPlayerCharacter = False
            self.CharacterWindow.UpdateUnsavedChangesFlag(True)

    def UpdateAbilityScoreModifierSigns(self):
        for SpinBoxTuple in self.AbilityScoreModifierSpinBoxesList:
            if self.CharacterWindow.NonPlayerCharacter.Stats["Ability Score Modifiers"][SpinBoxTuple[1]] >= 0:
                SpinBoxTuple[0].setPrefix("+")
            else:
                SpinBoxTuple[0].setPrefix("")
