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
        pass

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
