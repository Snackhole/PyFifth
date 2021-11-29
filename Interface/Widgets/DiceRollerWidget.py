from PyQt5 import QtCore
from PyQt5.QtWidgets import QFrame, QGridLayout, QSizePolicy, QSpinBox, QLabel, QPushButton, QTextEdit

from Interface.Widgets.DieTypeSpinBox import DieTypeSpinBox
from Interface.Widgets.IconButtons import AddButton, CopyButton, DeleteButton, EditButton, MoveDownButton, MoveUpButton, RollButton
from Interface.Widgets.PresetRollsTreeWidget import PresetRollsTreeWidget


class DiceRollerWidget(QFrame):
    def __init__(self, CharacterWindow):
        # Initialize
        super().__init__()

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Styles
        self.RollLabelStyle = "QLabel {font-size: 16pt;}"
        self.SectionLabelStyle = "QLabel {font-size: 10pt; font-weight: bold;}"
        self.SpinBoxStyle = "QSpinBox {font-size: 16pt;}"
        self.ButtonStyle = "QPushButton {font-size: 16pt;}"

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Dice Roller Width
        self.DiceRollerWidth = 80
        self.DiceRollerInputsHeight = 80

        # Dice Number Spin Box
        self.DiceNumberSpinBox = QSpinBox()
        self.DiceNumberSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.DiceNumberSpinBox.setStyleSheet(self.SpinBoxStyle)
        self.DiceNumberSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.DiceNumberSpinBox.setFixedWidth(self.DiceRollerWidth)
        self.DiceNumberSpinBox.setMinimumHeight(self.DiceRollerInputsHeight)
        self.DiceNumberSpinBox.setButtonSymbols(self.DiceNumberSpinBox.NoButtons)
        self.DiceNumberSpinBox.setRange(1, 1000000000)
        self.DiceNumberSpinBox.setValue(1)

        # Die Type Label
        self.DieTypeLabel = QLabel("d")
        self.DieTypeLabel.setStyleSheet(self.RollLabelStyle)
        self.DieTypeLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Die Type Spin Box
        self.DieTypeSpinBox = DieTypeSpinBox()
        self.DieTypeSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.DieTypeSpinBox.setStyleSheet(self.SpinBoxStyle)
        self.DieTypeSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.DieTypeSpinBox.setFixedWidth(self.DiceRollerWidth)
        self.DieTypeSpinBox.setMinimumHeight(self.DiceRollerInputsHeight)
        self.DieTypeSpinBox.setButtonSymbols(self.DieTypeSpinBox.NoButtons)
        self.DieTypeSpinBox.setRange(1, 1000000000)
        self.DieTypeSpinBox.setValue(20)

        # Modifier Label
        self.ModifierLabel = QLabel("+")
        self.ModifierLabel.setStyleSheet(self.RollLabelStyle)
        self.ModifierLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Modifier Spin Box
        self.ModifierSpinBox = QSpinBox()
        self.ModifierSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.ModifierSpinBox.setStyleSheet(self.SpinBoxStyle)
        self.ModifierSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.ModifierSpinBox.setFixedWidth(self.DiceRollerWidth)
        self.ModifierSpinBox.setMinimumHeight(self.DiceRollerInputsHeight)
        self.ModifierSpinBox.setButtonSymbols(self.ModifierSpinBox.NoButtons)
        self.ModifierSpinBox.setRange(-1000000000, 1000000000)
        self.ModifierSpinBox.setValue(0)

        # Roll Button
        self.RollButton = RollButton(lambda: self.CharacterWindow.RollAction.trigger(), "Roll")
        self.RollButton.setSizePolicy(self.InputsSizePolicy)
        self.RollButton.setMinimumHeight(self.DiceRollerInputsHeight)

        # Preset Rolls Label
        self.PresetRollsLabel = QLabel("Preset Rolls")
        self.PresetRollsLabel.setStyleSheet(self.SectionLabelStyle)
        self.PresetRollsLabel.setAlignment(QtCore.Qt.AlignCenter)

        # Preset Rolls Tree Widget
        self.PresetRollsTreeWidget = PresetRollsTreeWidget(self.CharacterWindow)
        self.PresetRollsTreeWidget.itemActivated.connect(lambda: self.CharacterWindow.RollPresetRollAction.trigger())

        # Preset Rolls Buttons
        self.PresetRollsRollButton = RollButton(lambda: self.CharacterWindow.RollPresetRollAction.trigger(), "Roll Preset Roll")
        self.PresetRollsRollButton.setSizePolicy(self.InputsSizePolicy)

        self.PresetRollsAddButton = AddButton(self.CharacterWindow.AddPresetRoll, "Add Preset Roll")
        self.PresetRollsAddButton.setSizePolicy(self.InputsSizePolicy)

        self.PresetRollsDeleteButton = DeleteButton(self.CharacterWindow.DeletePresetRoll, "Delete Preset Roll")
        self.PresetRollsDeleteButton.setSizePolicy(self.InputsSizePolicy)

        self.PresetRollsEditButton = EditButton(self.CharacterWindow.EditPresetRoll, "Edit Preset Roll")
        self.PresetRollsEditButton.setSizePolicy(self.InputsSizePolicy)

        self.PresetRollsCopyButton = CopyButton(self.CharacterWindow.CopyPresetRoll, "Copy Preset Roll")
        self.PresetRollsCopyButton.setSizePolicy(self.InputsSizePolicy)

        self.PresetRollsMoveUpButton = MoveUpButton(self.CharacterWindow.MovePresetRollUp, "Move Preset Roll Up")
        self.PresetRollsMoveUpButton.setSizePolicy(self.InputsSizePolicy)

        self.PresetRollsMoveDownButton = MoveDownButton(self.CharacterWindow.MovePresetRollDown, "Move Preset Roll Down")
        self.PresetRollsMoveDownButton.setSizePolicy(self.InputsSizePolicy)

        # Results Log Label
        self.ResultsLogLabel = QLabel("Results Log")
        self.ResultsLogLabel.setStyleSheet(self.SectionLabelStyle)
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
        self.PresetRollsLayout.addWidget(self.PresetRollsLabel, 0, 0, 1, 7)
        self.PresetRollsLayout.addWidget(self.PresetRollsRollButton, 1, 0)
        self.PresetRollsLayout.addWidget(self.PresetRollsAddButton, 1, 1)
        self.PresetRollsLayout.addWidget(self.PresetRollsDeleteButton, 1, 2)
        self.PresetRollsLayout.addWidget(self.PresetRollsEditButton, 1, 3)
        self.PresetRollsLayout.addWidget(self.PresetRollsCopyButton, 1, 4)
        self.PresetRollsLayout.addWidget(self.PresetRollsMoveUpButton, 1, 5)
        self.PresetRollsLayout.addWidget(self.PresetRollsMoveDownButton, 1, 6)
        self.PresetRollsLayout.addWidget(self.PresetRollsTreeWidget, 2, 0, 1, 7)
        self.PresetRollsLayout.setRowStretch(2, 1)
        self.PresetRollsFrame.setLayout(self.PresetRollsLayout)
        self.Layout.addWidget(self.PresetRollsFrame, 1, 0)

        # Results Log Widgets in Layout
        self.ResultsLogFrame = QFrame()
        self.ResultsLogLayout = QGridLayout()
        self.ResultsLogLayout.addWidget(self.ResultsLogLabel, 0, 0)
        self.ResultsLogLayout.addWidget(self.ResultsLogTextEdit, 1, 0)
        self.ResultsLogLayout.setColumnMinimumWidth(0, 200)
        self.ResultsLogFrame.setLayout(self.ResultsLogLayout)
        self.Layout.addWidget(self.ResultsLogFrame, 0, 1, 2, 1)

        # Set and Configure Layout
        self.Layout.setColumnStretch(1, 1)
        self.setLayout(self.Layout)
