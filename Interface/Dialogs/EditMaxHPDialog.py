import copy

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QSizePolicy, QLabel, QPushButton, QGridLayout, QSpinBox


class EditMaxHPDialog(QDialog):
    def __init__(self, CharacterWindow):
        super().__init__(parent=CharacterWindow)

        # Store Parameters
        self.CharacterWindow = CharacterWindow

        # Variables
        self.HealthData = CharacterWindow.PlayerCharacter.Stats["Health"]
        self.HealthDataOriginalState = copy.deepcopy(self.HealthData)
        self.UnsavedChanges = False
        self.Cancelled = False

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Prompt Label
        self.PromptLabel = QLabel("The HP calculation automatically accounts for your character level and Constitution modifier.  Max HP gained at each level should be based on your hit dice only.")
        self.PromptLabel.setWordWrap(True)

        # Create Max HP Gained at Each Level
        self.CreateMaxHPGainedAtEachLevel()

        # Bonus Max HP Per Level
        self.BonusMaxHPPerLevelLabel = QLabel("Bonus Max HP Per Level:")
        self.BonusMaxHPPerLevelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.BonusMaxHPPerLevelSpinBox = QSpinBox()
        self.BonusMaxHPPerLevelSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.BonusMaxHPPerLevelSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.BonusMaxHPPerLevelSpinBox.setButtonSymbols(self.BonusMaxHPPerLevelSpinBox.NoButtons)
        self.BonusMaxHPPerLevelSpinBox.setRange(0, 1000000000)
        self.BonusMaxHPPerLevelSpinBox.setValue(self.HealthData["Bonus Max Health Per Level"])
        self.BonusMaxHPPerLevelSpinBox.valueChanged.connect(self.UpdateHealthData)

        # Max HP Override
        self.MaxHPOverrideLabel = QLabel("Max HP Override:")
        self.MaxHPOverrideLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPOverrideSpinBox = QSpinBox()
        self.MaxHPOverrideSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPOverrideSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MaxHPOverrideSpinBox.setButtonSymbols(self.MaxHPOverrideSpinBox.NoButtons)
        self.MaxHPOverrideSpinBox.setRange(0, 1000000000)
        self.MaxHPOverrideSpinBox.setSpecialValueText("None")
        self.MaxHPOverrideSpinBox.setValue(self.HealthData["Max Health Override"] if self.HealthData["Max Health Override"] is not None else 0)
        self.MaxHPOverrideSpinBox.valueChanged.connect(self.UpdateHealthData)

        # Dialog Buttons
        self.DoneButton = QPushButton("Done")
        self.DoneButton.clicked.connect(self.Done)
        self.CancelButton = QPushButton("Cancel")
        self.CancelButton.clicked.connect(self.Cancel)

        # Create and Set Layout
        self.CreateAndSetLayout()

        # Set Window Title and Icon
        self.setWindowTitle(self.CharacterWindow.ScriptName)
        self.setWindowIcon(self.CharacterWindow.WindowIcon)

        # Execute Dialog
        self.exec_()

    def CreateMaxHPGainedAtEachLevel(self):
        # Label
        self.MaxHPGainedAtEachLevelLabel = QLabel("Max HP Gained at Each Level:")
        self.MaxHPGainedAtEachLevelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAtEachLevelLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.MaxHPGainedAtEachLevelLabel.setMargin(5)

        # 1st Level
        self.MaxHPGainedAt1stLevelLabel = QLabel("1st")
        self.MaxHPGainedAt1stLevelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt1stLevelSpinBox = QSpinBox()
        self.MaxHPGainedAt1stLevelSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt1stLevelSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MaxHPGainedAt1stLevelSpinBox.setButtonSymbols(self.MaxHPGainedAt1stLevelSpinBox.NoButtons)
        self.MaxHPGainedAt1stLevelSpinBox.setRange(6, 1000000000)
        self.MaxHPGainedAt1stLevelSpinBox.setValue(self.HealthData["Max Health Per Level"]["1"])
        self.MaxHPGainedAt1stLevelSpinBox.valueChanged.connect(self.UpdateHealthData)

        # 2nd Level
        self.MaxHPGainedAt2ndLevelLabel = QLabel("2nd")
        self.MaxHPGainedAt2ndLevelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt2ndLevelSpinBox = QSpinBox()
        self.MaxHPGainedAt2ndLevelSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt2ndLevelSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MaxHPGainedAt2ndLevelSpinBox.setButtonSymbols(self.MaxHPGainedAt2ndLevelSpinBox.NoButtons)
        self.MaxHPGainedAt2ndLevelSpinBox.setRange(1, 1000000000)
        self.MaxHPGainedAt2ndLevelSpinBox.setValue(self.HealthData["Max Health Per Level"]["2"])
        self.MaxHPGainedAt2ndLevelSpinBox.valueChanged.connect(self.UpdateHealthData)

        # 3rd Level
        self.MaxHPGainedAt3rdLevelLabel = QLabel("3rd")
        self.MaxHPGainedAt3rdLevelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt3rdLevelSpinBox = QSpinBox()
        self.MaxHPGainedAt3rdLevelSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt3rdLevelSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MaxHPGainedAt3rdLevelSpinBox.setButtonSymbols(self.MaxHPGainedAt3rdLevelSpinBox.NoButtons)
        self.MaxHPGainedAt3rdLevelSpinBox.setRange(1, 1000000000)
        self.MaxHPGainedAt3rdLevelSpinBox.setValue(self.HealthData["Max Health Per Level"]["3"])
        self.MaxHPGainedAt3rdLevelSpinBox.valueChanged.connect(self.UpdateHealthData)

        # 4th Level
        self.MaxHPGainedAt4thLevelLabel = QLabel("4th")
        self.MaxHPGainedAt4thLevelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt4thLevelSpinBox = QSpinBox()
        self.MaxHPGainedAt4thLevelSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt4thLevelSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MaxHPGainedAt4thLevelSpinBox.setButtonSymbols(self.MaxHPGainedAt4thLevelSpinBox.NoButtons)
        self.MaxHPGainedAt4thLevelSpinBox.setRange(1, 1000000000)
        self.MaxHPGainedAt4thLevelSpinBox.setValue(self.HealthData["Max Health Per Level"]["4"])
        self.MaxHPGainedAt4thLevelSpinBox.valueChanged.connect(self.UpdateHealthData)

        # 5th Level
        self.MaxHPGainedAt5thLevelLabel = QLabel("5th")
        self.MaxHPGainedAt5thLevelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt5thLevelSpinBox = QSpinBox()
        self.MaxHPGainedAt5thLevelSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt5thLevelSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MaxHPGainedAt5thLevelSpinBox.setButtonSymbols(self.MaxHPGainedAt5thLevelSpinBox.NoButtons)
        self.MaxHPGainedAt5thLevelSpinBox.setRange(1, 1000000000)
        self.MaxHPGainedAt5thLevelSpinBox.setValue(self.HealthData["Max Health Per Level"]["5"])
        self.MaxHPGainedAt5thLevelSpinBox.valueChanged.connect(self.UpdateHealthData)

        # 6th Level
        self.MaxHPGainedAt6thLevelLabel = QLabel("6th")
        self.MaxHPGainedAt6thLevelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt6thLevelSpinBox = QSpinBox()
        self.MaxHPGainedAt6thLevelSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt6thLevelSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MaxHPGainedAt6thLevelSpinBox.setButtonSymbols(self.MaxHPGainedAt6thLevelSpinBox.NoButtons)
        self.MaxHPGainedAt6thLevelSpinBox.setRange(1, 1000000000)
        self.MaxHPGainedAt6thLevelSpinBox.setValue(self.HealthData["Max Health Per Level"]["6"])
        self.MaxHPGainedAt6thLevelSpinBox.valueChanged.connect(self.UpdateHealthData)

        # 7th Level
        self.MaxHPGainedAt7thLevelLabel = QLabel("7th")
        self.MaxHPGainedAt7thLevelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt7thLevelSpinBox = QSpinBox()
        self.MaxHPGainedAt7thLevelSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt7thLevelSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MaxHPGainedAt7thLevelSpinBox.setButtonSymbols(self.MaxHPGainedAt7thLevelSpinBox.NoButtons)
        self.MaxHPGainedAt7thLevelSpinBox.setRange(1, 1000000000)
        self.MaxHPGainedAt7thLevelSpinBox.setValue(self.HealthData["Max Health Per Level"]["7"])
        self.MaxHPGainedAt7thLevelSpinBox.valueChanged.connect(self.UpdateHealthData)

        # 8th Level
        self.MaxHPGainedAt8thLevelLabel = QLabel("8th")
        self.MaxHPGainedAt8thLevelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt8thLevelSpinBox = QSpinBox()
        self.MaxHPGainedAt8thLevelSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt8thLevelSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MaxHPGainedAt8thLevelSpinBox.setButtonSymbols(self.MaxHPGainedAt8thLevelSpinBox.NoButtons)
        self.MaxHPGainedAt8thLevelSpinBox.setRange(1, 1000000000)
        self.MaxHPGainedAt8thLevelSpinBox.setValue(self.HealthData["Max Health Per Level"]["8"])
        self.MaxHPGainedAt8thLevelSpinBox.valueChanged.connect(self.UpdateHealthData)

        # 9th Level
        self.MaxHPGainedAt9thLevelLabel = QLabel("9th")
        self.MaxHPGainedAt9thLevelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt9thLevelSpinBox = QSpinBox()
        self.MaxHPGainedAt9thLevelSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt9thLevelSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MaxHPGainedAt9thLevelSpinBox.setButtonSymbols(self.MaxHPGainedAt9thLevelSpinBox.NoButtons)
        self.MaxHPGainedAt9thLevelSpinBox.setRange(1, 1000000000)
        self.MaxHPGainedAt9thLevelSpinBox.setValue(self.HealthData["Max Health Per Level"]["9"])
        self.MaxHPGainedAt9thLevelSpinBox.valueChanged.connect(self.UpdateHealthData)

        # 10th Level
        self.MaxHPGainedAt10thLevelLabel = QLabel("10th")
        self.MaxHPGainedAt10thLevelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt10thLevelSpinBox = QSpinBox()
        self.MaxHPGainedAt10thLevelSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt10thLevelSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MaxHPGainedAt10thLevelSpinBox.setButtonSymbols(self.MaxHPGainedAt10thLevelSpinBox.NoButtons)
        self.MaxHPGainedAt10thLevelSpinBox.setRange(1, 1000000000)
        self.MaxHPGainedAt10thLevelSpinBox.setValue(self.HealthData["Max Health Per Level"]["10"])
        self.MaxHPGainedAt10thLevelSpinBox.valueChanged.connect(self.UpdateHealthData)

        # 11th Level
        self.MaxHPGainedAt11thLevelLabel = QLabel("11th")
        self.MaxHPGainedAt11thLevelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt11thLevelSpinBox = QSpinBox()
        self.MaxHPGainedAt11thLevelSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt11thLevelSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MaxHPGainedAt11thLevelSpinBox.setButtonSymbols(self.MaxHPGainedAt11thLevelSpinBox.NoButtons)
        self.MaxHPGainedAt11thLevelSpinBox.setRange(1, 1000000000)
        self.MaxHPGainedAt11thLevelSpinBox.setValue(self.HealthData["Max Health Per Level"]["11"])
        self.MaxHPGainedAt11thLevelSpinBox.valueChanged.connect(self.UpdateHealthData)

        # 12th Level
        self.MaxHPGainedAt12thLevelLabel = QLabel("12th")
        self.MaxHPGainedAt12thLevelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt12thLevelSpinBox = QSpinBox()
        self.MaxHPGainedAt12thLevelSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt12thLevelSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MaxHPGainedAt12thLevelSpinBox.setButtonSymbols(self.MaxHPGainedAt12thLevelSpinBox.NoButtons)
        self.MaxHPGainedAt12thLevelSpinBox.setRange(1, 1000000000)
        self.MaxHPGainedAt12thLevelSpinBox.setValue(self.HealthData["Max Health Per Level"]["12"])
        self.MaxHPGainedAt12thLevelSpinBox.valueChanged.connect(self.UpdateHealthData)

        # 13th Level
        self.MaxHPGainedAt13thLevelLabel = QLabel("13th")
        self.MaxHPGainedAt13thLevelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt13thLevelSpinBox = QSpinBox()
        self.MaxHPGainedAt13thLevelSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt13thLevelSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MaxHPGainedAt13thLevelSpinBox.setButtonSymbols(self.MaxHPGainedAt13thLevelSpinBox.NoButtons)
        self.MaxHPGainedAt13thLevelSpinBox.setRange(1, 1000000000)
        self.MaxHPGainedAt13thLevelSpinBox.setValue(self.HealthData["Max Health Per Level"]["13"])
        self.MaxHPGainedAt13thLevelSpinBox.valueChanged.connect(self.UpdateHealthData)

        # 14th Level
        self.MaxHPGainedAt14thLevelLabel = QLabel("14th")
        self.MaxHPGainedAt14thLevelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt14thLevelSpinBox = QSpinBox()
        self.MaxHPGainedAt14thLevelSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt14thLevelSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MaxHPGainedAt14thLevelSpinBox.setButtonSymbols(self.MaxHPGainedAt14thLevelSpinBox.NoButtons)
        self.MaxHPGainedAt14thLevelSpinBox.setRange(1, 1000000000)
        self.MaxHPGainedAt14thLevelSpinBox.setValue(self.HealthData["Max Health Per Level"]["14"])
        self.MaxHPGainedAt14thLevelSpinBox.valueChanged.connect(self.UpdateHealthData)

        # 15th Level
        self.MaxHPGainedAt15thLevelLabel = QLabel("15th")
        self.MaxHPGainedAt15thLevelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt15thLevelSpinBox = QSpinBox()
        self.MaxHPGainedAt15thLevelSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt15thLevelSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MaxHPGainedAt15thLevelSpinBox.setButtonSymbols(self.MaxHPGainedAt15thLevelSpinBox.NoButtons)
        self.MaxHPGainedAt15thLevelSpinBox.setRange(1, 1000000000)
        self.MaxHPGainedAt15thLevelSpinBox.setValue(self.HealthData["Max Health Per Level"]["15"])
        self.MaxHPGainedAt15thLevelSpinBox.valueChanged.connect(self.UpdateHealthData)

        # 16th Level
        self.MaxHPGainedAt16thLevelLabel = QLabel("16th")
        self.MaxHPGainedAt16thLevelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt16thLevelSpinBox = QSpinBox()
        self.MaxHPGainedAt16thLevelSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt16thLevelSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MaxHPGainedAt16thLevelSpinBox.setButtonSymbols(self.MaxHPGainedAt16thLevelSpinBox.NoButtons)
        self.MaxHPGainedAt16thLevelSpinBox.setRange(1, 1000000000)
        self.MaxHPGainedAt16thLevelSpinBox.setValue(self.HealthData["Max Health Per Level"]["16"])
        self.MaxHPGainedAt16thLevelSpinBox.valueChanged.connect(self.UpdateHealthData)

        # 17th Level
        self.MaxHPGainedAt17thLevelLabel = QLabel("17th")
        self.MaxHPGainedAt17thLevelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt17thLevelSpinBox = QSpinBox()
        self.MaxHPGainedAt17thLevelSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt17thLevelSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MaxHPGainedAt17thLevelSpinBox.setButtonSymbols(self.MaxHPGainedAt17thLevelSpinBox.NoButtons)
        self.MaxHPGainedAt17thLevelSpinBox.setRange(1, 1000000000)
        self.MaxHPGainedAt17thLevelSpinBox.setValue(self.HealthData["Max Health Per Level"]["17"])
        self.MaxHPGainedAt17thLevelSpinBox.valueChanged.connect(self.UpdateHealthData)

        # 18th Level
        self.MaxHPGainedAt18thLevelLabel = QLabel("18th")
        self.MaxHPGainedAt18thLevelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt18thLevelSpinBox = QSpinBox()
        self.MaxHPGainedAt18thLevelSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt18thLevelSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MaxHPGainedAt18thLevelSpinBox.setButtonSymbols(self.MaxHPGainedAt18thLevelSpinBox.NoButtons)
        self.MaxHPGainedAt18thLevelSpinBox.setRange(1, 1000000000)
        self.MaxHPGainedAt18thLevelSpinBox.setValue(self.HealthData["Max Health Per Level"]["18"])
        self.MaxHPGainedAt18thLevelSpinBox.valueChanged.connect(self.UpdateHealthData)

        # 19th Level
        self.MaxHPGainedAt19thLevelLabel = QLabel("19th")
        self.MaxHPGainedAt19thLevelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt19thLevelSpinBox = QSpinBox()
        self.MaxHPGainedAt19thLevelSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt19thLevelSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MaxHPGainedAt19thLevelSpinBox.setButtonSymbols(self.MaxHPGainedAt19thLevelSpinBox.NoButtons)
        self.MaxHPGainedAt19thLevelSpinBox.setRange(1, 1000000000)
        self.MaxHPGainedAt19thLevelSpinBox.setValue(self.HealthData["Max Health Per Level"]["19"])
        self.MaxHPGainedAt19thLevelSpinBox.valueChanged.connect(self.UpdateHealthData)

        # 20th Level
        self.MaxHPGainedAt20thLevelLabel = QLabel("20th")
        self.MaxHPGainedAt20thLevelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt20thLevelSpinBox = QSpinBox()
        self.MaxHPGainedAt20thLevelSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.MaxHPGainedAt20thLevelSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.MaxHPGainedAt20thLevelSpinBox.setButtonSymbols(self.MaxHPGainedAt20thLevelSpinBox.NoButtons)
        self.MaxHPGainedAt20thLevelSpinBox.setRange(1, 1000000000)
        self.MaxHPGainedAt20thLevelSpinBox.setValue(self.HealthData["Max Health Per Level"]["20"])
        self.MaxHPGainedAt20thLevelSpinBox.valueChanged.connect(self.UpdateHealthData)

    def CreateAndSetLayout(self):
        self.Layout = QGridLayout()

        self.Layout.addWidget(self.PromptLabel, 0, 0, 1, 2)

        self.MaxHPGainedAtEachLevelLayout = QGridLayout()
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAtEachLevelLabel, 0, 0, 1, 8)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt1stLevelLabel, 1, 0)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt1stLevelSpinBox, 1, 1)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt2ndLevelLabel, 2, 0)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt2ndLevelSpinBox, 2, 1)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt3rdLevelLabel, 3, 0)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt3rdLevelSpinBox, 3, 1)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt4thLevelLabel, 4, 0)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt4thLevelSpinBox, 4, 1)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt5thLevelLabel, 5, 0)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt5thLevelSpinBox, 5, 1)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt6thLevelLabel, 1, 2)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt6thLevelSpinBox, 1, 3)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt7thLevelLabel, 2, 2)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt7thLevelSpinBox, 2, 3)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt8thLevelLabel, 3, 2)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt8thLevelSpinBox, 3, 3)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt9thLevelLabel, 4, 2)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt9thLevelSpinBox, 4, 3)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt10thLevelLabel, 5, 2)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt10thLevelSpinBox, 5, 3)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt11thLevelLabel, 1, 4)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt11thLevelSpinBox, 1, 5)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt12thLevelLabel, 2, 4)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt12thLevelSpinBox, 2, 5)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt13thLevelLabel, 3, 4)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt13thLevelSpinBox, 3, 5)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt14thLevelLabel, 4, 4)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt14thLevelSpinBox, 4, 5)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt15thLevelLabel, 5, 4)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt15thLevelSpinBox, 5, 5)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt16thLevelLabel, 1, 6)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt16thLevelSpinBox, 1, 7)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt17thLevelLabel, 2, 6)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt17thLevelSpinBox, 2, 7)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt18thLevelLabel, 3, 6)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt18thLevelSpinBox, 3, 7)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt19thLevelLabel, 4, 6)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt19thLevelSpinBox, 4, 7)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt20thLevelLabel, 5, 6)
        self.MaxHPGainedAtEachLevelLayout.addWidget(self.MaxHPGainedAt20thLevelSpinBox, 5, 7)
        for Row in range(1, 6):
            self.MaxHPGainedAtEachLevelLayout.setRowStretch(Row, 1)
        for Column in [1, 3, 5, 7]:
            self.MaxHPGainedAtEachLevelLayout.setColumnStretch(Column, 1)
        self.Layout.addLayout(self.MaxHPGainedAtEachLevelLayout, 1, 0, 1, 2)

        self.Layout.addWidget(self.BonusMaxHPPerLevelLabel, 2, 0)
        self.Layout.addWidget(self.BonusMaxHPPerLevelSpinBox, 2, 1)

        self.Layout.addWidget(self.MaxHPOverrideLabel, 3, 0)
        self.Layout.addWidget(self.MaxHPOverrideSpinBox, 3, 1)

        self.DialogButtonsLayout = QGridLayout()
        self.DialogButtonsLayout.addWidget(self.DoneButton, 0, 0)
        self.DialogButtonsLayout.addWidget(self.CancelButton, 0, 1)
        self.Layout.addLayout(self.DialogButtonsLayout, 4, 0, 1, 2)

        self.Layout.setRowStretch(1, 1)
        self.Layout.setColumnStretch(1, 1)

        self.setLayout(self.Layout)

    def UpdateHealthData(self):
        self.HealthData["Max Health Per Level"]["1"] = self.MaxHPGainedAt1stLevelSpinBox.value()
        self.HealthData["Max Health Per Level"]["2"] = self.MaxHPGainedAt2ndLevelSpinBox.value()
        self.HealthData["Max Health Per Level"]["3"] = self.MaxHPGainedAt3rdLevelSpinBox.value()
        self.HealthData["Max Health Per Level"]["4"] = self.MaxHPGainedAt4thLevelSpinBox.value()
        self.HealthData["Max Health Per Level"]["5"] = self.MaxHPGainedAt5thLevelSpinBox.value()
        self.HealthData["Max Health Per Level"]["6"] = self.MaxHPGainedAt6thLevelSpinBox.value()
        self.HealthData["Max Health Per Level"]["7"] = self.MaxHPGainedAt7thLevelSpinBox.value()
        self.HealthData["Max Health Per Level"]["8"] = self.MaxHPGainedAt8thLevelSpinBox.value()
        self.HealthData["Max Health Per Level"]["9"] = self.MaxHPGainedAt9thLevelSpinBox.value()
        self.HealthData["Max Health Per Level"]["10"] = self.MaxHPGainedAt10thLevelSpinBox.value()
        self.HealthData["Max Health Per Level"]["11"] = self.MaxHPGainedAt11thLevelSpinBox.value()
        self.HealthData["Max Health Per Level"]["12"] = self.MaxHPGainedAt12thLevelSpinBox.value()
        self.HealthData["Max Health Per Level"]["13"] = self.MaxHPGainedAt13thLevelSpinBox.value()
        self.HealthData["Max Health Per Level"]["14"] = self.MaxHPGainedAt14thLevelSpinBox.value()
        self.HealthData["Max Health Per Level"]["15"] = self.MaxHPGainedAt15thLevelSpinBox.value()
        self.HealthData["Max Health Per Level"]["16"] = self.MaxHPGainedAt16thLevelSpinBox.value()
        self.HealthData["Max Health Per Level"]["17"] = self.MaxHPGainedAt17thLevelSpinBox.value()
        self.HealthData["Max Health Per Level"]["18"] = self.MaxHPGainedAt18thLevelSpinBox.value()
        self.HealthData["Max Health Per Level"]["19"] = self.MaxHPGainedAt19thLevelSpinBox.value()
        self.HealthData["Max Health Per Level"]["20"] = self.MaxHPGainedAt20thLevelSpinBox.value()

        self.HealthData["Bonus Max Health Per Level"] = self.BonusMaxHPPerLevelSpinBox.value()

        self.HealthData["Max Health Override"] = self.MaxHPOverrideSpinBox.value() if self.MaxHPOverrideSpinBox.value() > 0 else None

        self.UnsavedChanges = True

    def Done(self):
        self.close()

    def Cancel(self):
        self.HealthData.update(self.HealthDataOriginalState)
        self.UnsavedChanges = False
        self.Cancelled = True
        self.close()
