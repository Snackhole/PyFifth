from PyQt5 import QtCore
from PyQt5.QtWidgets import QFrame, QGridLayout, QSizePolicy, QSpinBox, QLabel, QPushButton, QTextEdit

from Interface.Widgets.DieTypeSpinBox import DieTypeSpinBox
from Interface.Widgets.PresetRollsTreeWidget import PresetRollsTreeWidget


class DiceRollerWidget(QFrame):
    def __init__(self, CharacterWindow):
        # Initialize
        super().__init__()

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Styles
        self.LabelStyle = "QLabel {font-size: 10pt;}"
        self.SpinBoxStyle = "QSpinBox {font-size: 16pt;}"
        self.RollButtonStyle = "QPushButton {font-size: 16pt;}"

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Dice Roller Width
        self.DiceRollerWidth = 80

        # Dice Number Spin Box
        self.DiceNumberSpinBox = QSpinBox()
        self.DiceNumberSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.DiceNumberSpinBox.setStyleSheet(self.SpinBoxStyle)
        self.DiceNumberSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.DiceNumberSpinBox.setFixedWidth(self.DiceRollerWidth)
        self.DiceNumberSpinBox.setButtonSymbols(self.DiceNumberSpinBox.NoButtons)
        self.DiceNumberSpinBox.setRange(1, 1000000000)
        self.DiceNumberSpinBox.setValue(1)

        # Die Type Label
        self.DieTypeLabel = QLabel("d")
        self.DieTypeLabel.setStyleSheet(self.LabelStyle)
        self.DieTypeLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Die Type Spin Box
        self.DieTypeSpinBox = DieTypeSpinBox()
        self.DieTypeSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.DieTypeSpinBox.setStyleSheet(self.SpinBoxStyle)
        self.DieTypeSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.DieTypeSpinBox.setFixedWidth(self.DiceRollerWidth)
        self.DieTypeSpinBox.setButtonSymbols(self.DieTypeSpinBox.NoButtons)
        self.DieTypeSpinBox.setRange(1, 1000000000)
        self.DieTypeSpinBox.setValue(20)

        # Modifier Label
        self.ModifierLabel = QLabel("+")
        self.ModifierLabel.setStyleSheet(self.LabelStyle)
        self.ModifierLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Modifier Spin Box
        self.ModifierSpinBox = QSpinBox()
        self.ModifierSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ModifierSpinBox.setStyleSheet(self.SpinBoxStyle)
        self.ModifierSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.ModifierSpinBox.setFixedWidth(self.DiceRollerWidth)
        self.ModifierSpinBox.setButtonSymbols(self.ModifierSpinBox.NoButtons)
        self.ModifierSpinBox.setRange(-1000000000, 1000000000)
        self.ModifierSpinBox.setValue(0)

        # Roll Button
        self.RollButton = QPushButton("Roll")
        self.RollButton.clicked.connect(lambda: self.CharacterWindow.RollAction.trigger())
        self.RollButton.setSizePolicy(self.InputsSizePolicy)
        self.RollButton.setStyleSheet(self.RollButtonStyle)

        # Preset Rolls Label
        self.PresetRollsLabel = QLabel("Preset Rolls")
        self.PresetRollsLabel.setStyleSheet(self.LabelStyle)
        self.PresetRollsLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Preset Rolls Tree Widget
        self.PresetRollsTreeWidget = PresetRollsTreeWidget(self.CharacterWindow)
        self.PresetRollsTreeWidget.itemActivated.connect(lambda: self.CharacterWindow.RollPresetRollAction.trigger())

        # Preset Rolls Buttons
        self.PresetRollsRollButton = QPushButton("Roll")
        self.PresetRollsRollButton.clicked.connect(lambda: self.CharacterWindow.RollPresetRollAction.trigger())
        self.PresetRollsRollButton.setSizePolicy(self.InputsSizePolicy)

        self.PresetRollsAddButton = QPushButton("+")
        self.PresetRollsAddButton.clicked.connect(self.CharacterWindow.AddPresetRoll)
        self.PresetRollsAddButton.setSizePolicy(self.InputsSizePolicy)

        self.PresetRollsDeleteButton = QPushButton("-")
        self.PresetRollsDeleteButton.clicked.connect(self.CharacterWindow.DeletePresetRoll)
        self.PresetRollsDeleteButton.setSizePolicy(self.InputsSizePolicy)

        self.PresetRollsEditButton = QPushButton("Edit")
        self.PresetRollsEditButton.clicked.connect(self.CharacterWindow.EditPresetRoll)
        self.PresetRollsEditButton.setSizePolicy(self.InputsSizePolicy)

        self.PresetRollsCopyButton = QPushButton("Copy")
        self.PresetRollsCopyButton.clicked.connect(self.CharacterWindow.CopyPresetRoll)
        self.PresetRollsCopyButton.setSizePolicy(self.InputsSizePolicy)

        self.PresetRollsMoveUpButton = QPushButton("\u2191")
        self.PresetRollsMoveUpButton.clicked.connect(self.CharacterWindow.MovePresetRollUp)
        self.PresetRollsMoveUpButton.setSizePolicy(self.InputsSizePolicy)

        self.PresetRollsMoveDownButton = QPushButton("\u2193")
        self.PresetRollsMoveDownButton.clicked.connect(self.CharacterWindow.MovePresetRollDown)
        self.PresetRollsMoveDownButton.setSizePolicy(self.InputsSizePolicy)

        # Results Log Label
        self.ResultsLogLabel = QLabel("Results Log")
        self.ResultsLogLabel.setStyleSheet(self.LabelStyle)
        self.ResultsLogLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Results Log Text Edit
        self.ResultsLogTextEdit = QTextEdit()
        self.ResultsLogTextEdit.setReadOnly(True)

        # Create Layout
        self.Layout = QGridLayout()

        # Dice Roller Inputs in Layout
        self.DiceRollerInputsFrame = QFrame()
        self.DiceRollerInputsLayout = QGridLayout()
        self.DiceRollerInputsLayout.addWidget(self.DiceNumberSpinBox, 0, 0)
        self.DiceRollerInputsLayout.addWidget(self.DieTypeLabel, 0, 1)
        self.DiceRollerInputsLayout.addWidget(self.DieTypeSpinBox, 0, 2)
        self.DiceRollerInputsLayout.addWidget(self.ModifierLabel, 0, 3)
        self.DiceRollerInputsLayout.addWidget(self.ModifierSpinBox, 0, 4)
        self.DiceRollerInputsLayout.addWidget(self.RollButton, 0, 5)
        self.DiceRollerInputsFrame.setLayout(self.DiceRollerInputsLayout)
        self.Layout.addWidget(self.DiceRollerInputsFrame, 0, 0)

        # Preset Rolls in Layout
        self.PresetRollsFrame = QFrame()
        self.PresetRollsLayout = QGridLayout()
        self.PresetRollsLayout.addWidget(self.PresetRollsLabel, 0, 0, 1, 2)
        self.PresetRollsLayout.addWidget(self.PresetRollsTreeWidget, 1, 0, 7, 1)
        self.PresetRollsLayout.addWidget(self.PresetRollsRollButton, 1, 1)
        self.PresetRollsLayout.addWidget(self.PresetRollsAddButton, 2, 1)
        self.PresetRollsLayout.addWidget(self.PresetRollsDeleteButton, 3, 1)
        self.PresetRollsLayout.addWidget(self.PresetRollsEditButton, 4, 1)
        self.PresetRollsLayout.addWidget(self.PresetRollsCopyButton, 5, 1)
        self.PresetRollsLayout.addWidget(self.PresetRollsMoveUpButton, 6, 1)
        self.PresetRollsLayout.addWidget(self.PresetRollsMoveDownButton, 7, 1)
        for Row in range(1, 8):
            self.PresetRollsLayout.setRowStretch(Row, 1)
        self.PresetRollsFrame.setLayout(self.PresetRollsLayout)
        self.Layout.addWidget(self.PresetRollsFrame, 1, 0)

        # Results Log Widgets in Layout
        self.ResultsLogFrame = QFrame()
        self.ResultsLogLayout = QGridLayout()
        self.ResultsLogLayout.addWidget(self.ResultsLogLabel, 0, 0)
        self.ResultsLogLayout.addWidget(self.ResultsLogTextEdit, 1, 0)
        self.ResultsLogFrame.setLayout(self.ResultsLogLayout)
        self.Layout.addWidget(self.ResultsLogFrame, 0, 1, 2, 1)

        # Set and Configure Layout
        self.Layout.setColumnStretch(1, 1)
        self.setLayout(self.Layout)
