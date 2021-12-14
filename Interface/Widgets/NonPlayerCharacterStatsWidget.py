from PyQt5 import QtCore
from PyQt5.QtWidgets import QFrame, QGridLayout, QInputDialog, QLabel, QSizePolicy, QSpinBox

from Interface.Widgets.IconButtons import DamageButton, HealButton


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
        self.CharismaModifierSpinBox.setValue(0)
        self.CharismaModifierSpinBox.valueChanged.connect(lambda: self.CharacterWindow.UpdateStat(("Ability Score Modifiers", "Charisma"), self.CharismaModifierSpinBox.value()))

        # Ability Score Modifiers List
        self.AbilityScoreModifierSpinBoxesList = [(self.StrengthModifierSpinBox, "Strength"), (self.DexterityModifierSpinBox, "Dexterity"), (self.ConstitutionModifierSpinBox, "Constitution"), (self.IntelligenceModifierSpinBox, "Intelligence"), (self.WisdomModifierSpinBox, "Wisdom"), (self.CharismaModifierSpinBox, "Charisma")]

    def CreateMiscStringInputs(self):
        pass

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
                self.CharacterWindow.DisplayMessageBox("DC " + str(ConcentrationDC) + " Constitution saving throw required to maintain concentration.", Parent=self)

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
