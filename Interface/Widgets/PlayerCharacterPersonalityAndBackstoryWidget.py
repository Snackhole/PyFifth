from PyQt6 import QtCore
from PyQt6.QtWidgets import QFrame, QGridLayout, QLabel, QSizePolicy

from Interface.Widgets.CenteredLineEdit import CenteredLineEdit
from Interface.Widgets.IndentingTextEdit import IndentingTextEdit


class PlayerCharacterPersonalityAndBackstoryWidget(QFrame):
    def __init__(self, CharacterWindow):
        # Initialize Frame
        super().__init__()

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Styles
        self.SectionLabelStyle = "QLabel {font-size: 10pt; font-weight: bold;}"

        # Header Label Margin
        self.HeaderLabelMargin = 5

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        # Create Interface Elements
        self.CreateInterfaceElements()

        # Create and Set Layout
        self.CreateAndSetLayout()

    def CreateInterfaceElements(self):
        # Race
        self.RaceLabel = QLabel("Race")
        self.RaceLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.RaceLabel.setStyleSheet(self.SectionLabelStyle)
        self.RaceLabel.setMargin(self.HeaderLabelMargin)
        self.RaceLineEdit = CenteredLineEdit()
        self.RaceLineEdit.textChanged.connect(lambda: self.CharacterWindow.UpdateStat("Character Race", self.RaceLineEdit.text()))

        # Background
        self.BackgroundLabel = QLabel("Background")
        self.BackgroundLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.BackgroundLabel.setStyleSheet(self.SectionLabelStyle)
        self.BackgroundLabel.setMargin(self.HeaderLabelMargin)
        self.BackgroundLineEdit = CenteredLineEdit()
        self.BackgroundLineEdit.textChanged.connect(lambda: self.CharacterWindow.UpdateStat("Character Background", self.BackgroundLineEdit.text()))

        # Alignment
        self.AlignmentLabel = QLabel("Alignment")
        self.AlignmentLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.AlignmentLabel.setStyleSheet(self.SectionLabelStyle)
        self.AlignmentLabel.setMargin(self.HeaderLabelMargin)
        self.AlignmentLineEdit = CenteredLineEdit()
        self.AlignmentLineEdit.textChanged.connect(lambda: self.CharacterWindow.UpdateStat("Character Alignment", self.AlignmentLineEdit.text()))

        # Age
        self.AgeLabel = QLabel("Age")
        self.AgeLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.AgeLabel.setStyleSheet(self.SectionLabelStyle)
        self.AgeLabel.setMargin(self.HeaderLabelMargin)
        self.AgeLineEdit = CenteredLineEdit()
        self.AgeLineEdit.textChanged.connect(lambda: self.CharacterWindow.UpdateStat("Character Age", self.AgeLineEdit.text()))

        # Physical Appearance
        self.PhysicalAppearanceLabel = QLabel("Physical Appearance")
        self.PhysicalAppearanceLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.PhysicalAppearanceLabel.setStyleSheet(self.SectionLabelStyle)
        self.PhysicalAppearanceLabel.setMargin(self.HeaderLabelMargin)
        self.PhysicalAppearanceTextEdit = IndentingTextEdit(TextChangedSlot=lambda: self.CharacterWindow.UpdateStat("Character Physical Appearance", self.PhysicalAppearanceTextEdit.toPlainText()))
        self.PhysicalAppearanceTextEdit.setTabChangesFocus(True)

        # Personality Traits
        self.PersonalityTraitsLabel = QLabel("Personality Traits")
        self.PersonalityTraitsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.PersonalityTraitsLabel.setStyleSheet(self.SectionLabelStyle)
        self.PersonalityTraitsLabel.setMargin(self.HeaderLabelMargin)
        self.PersonalityTraitsTextEdit = IndentingTextEdit(TextChangedSlot=lambda: self.CharacterWindow.UpdateStat("Character Personality Traits", self.PersonalityTraitsTextEdit.toPlainText()))
        self.PersonalityTraitsTextEdit.setTabChangesFocus(True)

        # Bonds
        self.BondsLabel = QLabel("Bonds")
        self.BondsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.BondsLabel.setStyleSheet(self.SectionLabelStyle)
        self.BondsLabel.setMargin(self.HeaderLabelMargin)
        self.BondsTextEdit = IndentingTextEdit(TextChangedSlot=lambda: self.CharacterWindow.UpdateStat("Character Bonds", self.BondsTextEdit.toPlainText()))
        self.BondsTextEdit.setTabChangesFocus(True)

        # Ideals
        self.IdealsLabel = QLabel("Ideals")
        self.IdealsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.IdealsLabel.setStyleSheet(self.SectionLabelStyle)
        self.IdealsLabel.setMargin(self.HeaderLabelMargin)
        self.IdealsTextEdit = IndentingTextEdit(TextChangedSlot=lambda: self.CharacterWindow.UpdateStat("Character Ideals", self.IdealsTextEdit.toPlainText()))
        self.IdealsTextEdit.setTabChangesFocus(True)

        # Flaws
        self.FlawsLabel = QLabel("Flaws")
        self.FlawsLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.FlawsLabel.setStyleSheet(self.SectionLabelStyle)
        self.FlawsLabel.setMargin(self.HeaderLabelMargin)
        self.FlawsTextEdit = IndentingTextEdit(TextChangedSlot=lambda: self.CharacterWindow.UpdateStat("Character Flaws", self.FlawsTextEdit.toPlainText()))
        self.FlawsTextEdit.setTabChangesFocus(True)

        # Backstory
        self.BackstoryLabel = QLabel("Backstory")
        self.BackstoryLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.BackstoryLabel.setStyleSheet(self.SectionLabelStyle)
        self.BackstoryLabel.setMargin(self.HeaderLabelMargin)
        self.BackstoryTextEdit = IndentingTextEdit(TextChangedSlot=lambda: self.CharacterWindow.UpdateStat("Character Backstory", self.BackstoryTextEdit.toPlainText()))
        self.BackstoryTextEdit.setTabChangesFocus(True)

    def CreateAndSetLayout(self):
        # Create Layout
        self.Layout = QGridLayout()

        # Race
        self.Layout.addWidget(self.RaceLabel, 0, 0)
        self.Layout.addWidget(self.RaceLineEdit, 1, 0)

        # Background
        self.Layout.addWidget(self.BackgroundLabel, 2, 0)
        self.Layout.addWidget(self.BackgroundLineEdit, 3, 0)

        # Alignment
        self.Layout.addWidget(self.AlignmentLabel, 4, 0)
        self.Layout.addWidget(self.AlignmentLineEdit, 5, 0)

        # Age
        self.Layout.addWidget(self.AgeLabel, 6, 0)
        self.Layout.addWidget(self.AgeLineEdit, 7, 0)

        # Physical Appearance
        self.Layout.addWidget(self.PhysicalAppearanceLabel, 8, 0)
        self.Layout.addWidget(self.PhysicalAppearanceTextEdit, 9, 0)

        # Traits, Ideals, Bonds, and Flaws
        self.PersonalityLayout = QGridLayout()
        self.PersonalityLayout.addWidget(self.PersonalityTraitsLabel, 0, 0)
        self.PersonalityLayout.addWidget(self.PersonalityTraitsTextEdit, 1, 0)
        self.PersonalityLayout.addWidget(self.IdealsLabel, 0, 1)
        self.PersonalityLayout.addWidget(self.IdealsTextEdit, 1, 1)
        self.PersonalityLayout.addWidget(self.BondsLabel, 2, 0)
        self.PersonalityLayout.addWidget(self.BondsTextEdit, 3, 0)
        self.PersonalityLayout.addWidget(self.FlawsLabel, 2, 1)
        self.PersonalityLayout.addWidget(self.FlawsTextEdit, 3, 1)
        self.Layout.addLayout(self.PersonalityLayout, 0, 1, 10, 1)

        # Backstory
        self.Layout.addWidget(self.BackstoryLabel, 0, 2)
        self.Layout.addWidget(self.BackstoryTextEdit, 1, 2, 9, 1)

        # Set Layout
        self.setLayout(self.Layout)
