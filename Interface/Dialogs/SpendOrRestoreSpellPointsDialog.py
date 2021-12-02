from PyQt5 import QtCore
from PyQt5.QtWidgets import QComboBox, QLabel, QPushButton, QDialog, QGridLayout, QSizePolicy, QSpinBox


class SpendOrRestoreSpellPointsDialog(QDialog):
    def __init__(self, CharacterWindow, RestoreMode=False):
        super().__init__(parent=CharacterWindow)

        # Store Parameters
        self.CharacterWindow = CharacterWindow
        self.RestoreMode = RestoreMode

        # Variables
        self.ModeString = "Restore" if self.RestoreMode else "Spend"
        self.SpellLevels = ["None"] + list(self.CharacterWindow.PlayerCharacter.SpellPointValues.keys())
        self.SpellSlotLevel = None
        self.SpellSlotAmount = None
        self.ManualAmount = None
        self.Submitted = False

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Prompt
        self.PromptLabel = QLabel(self.ModeString + " spell points:")
        self.PromptLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Spell Slots
        self.SpellSlotLevelLabel = QLabel("Spell Slot Level:")
        self.SpellSlotLevelLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.SpellSlotLevelComboBox = QComboBox()
        self.SpellSlotLevelComboBox.addItems(self.SpellLevels)
        self.SpellSlotLevelComboBox.setEditable(False)

        self.SpellSlotAmountLabel = QLabel("Spell Slot Amount:")
        self.SpellSlotAmountLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.SpellSlotAmountSpinBox = QSpinBox()
        self.SpellSlotAmountSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.SpellSlotAmountSpinBox.setButtonSymbols(self.SpellSlotAmountSpinBox.NoButtons)
        self.SpellSlotAmountSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SpellSlotAmountSpinBox.setRange(0, 1000000000)
        self.SpellSlotAmountSpinBox.setValue(0)

        # Manual Amount
        self.ManualAmountLabel = QLabel("Manual Amount:")
        self.ManualAmountLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.ManualAmountSpinBox = QSpinBox()
        self.ManualAmountSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ManualAmountSpinBox.setButtonSymbols(self.ManualAmountSpinBox.NoButtons)
        self.ManualAmountSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.ManualAmountSpinBox.setRange(0, 1000000000)
        self.ManualAmountSpinBox.setValue(0)

        # Buttons
        self.SubmitButton = QPushButton(self.ModeString)
        self.SubmitButton.clicked.connect(self.Submit)
        self.CancelButton = QPushButton("Cancel")
        self.CancelButton.clicked.connect(self.Cancel)

        # Layout
        self.Layout = QGridLayout()
        self.Layout.addWidget(self.PromptLabel, 0, 0, 1, 2)
        self.Layout.addWidget(self.SpellSlotLevelLabel, 1, 0)
        self.Layout.addWidget(self.SpellSlotLevelComboBox, 1, 1)
        self.Layout.addWidget(self.SpellSlotAmountLabel, 2, 0)
        self.Layout.addWidget(self.SpellSlotAmountSpinBox, 2, 1)
        self.Layout.addWidget(self.ManualAmountLabel, 3, 0)
        self.Layout.addWidget(self.ManualAmountSpinBox, 3, 1)
        self.ButtonsLayout = QGridLayout()
        self.ButtonsLayout.addWidget(self.SubmitButton, 0, 0)
        self.ButtonsLayout.addWidget(self.CancelButton, 0, 1)
        self.Layout.addLayout(self.ButtonsLayout, 4, 0, 1, 2)
        self.setLayout(self.Layout)

        # Set Window Title and Icon
        self.setWindowTitle(self.CharacterWindow.ScriptName)
        self.setWindowIcon(self.CharacterWindow.WindowIcon)

        # Execute Dialog
        self.exec_()

    def Submit(self):
        self.SpellSlotLevel = self.SpellSlotLevelComboBox.currentText()
        self.SpellSlotAmount = self.SpellSlotAmountSpinBox.value()
        self.ManualAmount = self.ManualAmountSpinBox.value()
        self.Submitted = True
        self.close()

    def Cancel(self):
        self.close()
