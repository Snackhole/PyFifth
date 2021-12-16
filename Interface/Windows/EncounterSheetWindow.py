import copy
import json
import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import QAction, QFrame, QGridLayout, QLabel, QMessageBox, QPushButton, QSizePolicy, QSpinBox

from Core.Encounter import Encounter
from Interface.Dialogs.CoinCalculatorDialog import CoinCalculatorDialog
from Interface.Widgets.CenteredLineEdit import CenteredLineEdit
from Interface.Widgets.IconButtons import AddButton, DeleteButton, EditButton, SortButton
from Interface.Widgets.IndentingTextEdit import IndentingTextEdit
from Interface.Widgets.InitiativeOrderTreeWidget import InitiativeOrderTreeWidget
from Interface.Windows.Window import Window
from SaveAndLoad.SaveAndOpenMixin import SaveAndOpenMixin


class EncounterSheetWindow(Window, SaveAndOpenMixin):
    # Initialization Methods
    def __init__(self, ScriptName, AbsoluteDirectoryPath, AppInst):
        # Store Parameters
        self.ScriptName = ScriptName
        self.AbsoluteDirectoryPath = AbsoluteDirectoryPath
        self.AppInst = AppInst

        # Variables
        self.UpdatingFieldsFromEncounter = False

        # Styles
        self.SectionLabelStyle = "QLabel {font-size: 10pt; font-weight: bold;}"

        # Header Label Margin
        self.HeaderLabelMargin = 5

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Initialize Window
        super().__init__(ScriptName, AbsoluteDirectoryPath, AppInst)

        # Set Up Save and Open
        self.SetUpSaveAndOpen(".pyfifthencounter", "PyFifth Encounter Sheet", (Encounter,))

        # Create Encounter
        self.Encounter = Encounter()

        # Load Configs
        self.LoadConfigs()

        # Update Display
        self.UpdateDisplay()

    def CreateInterface(self):
        super().LoadTheme()

        # Header
        self.NameLabel = QLabel("Encounter Name:")
        self.NameLineEdit = CenteredLineEdit()
        self.NameLineEdit.textChanged.connect(lambda: self.UpdateData("Encounter Name", self.NameLineEdit.text()))

        self.CRLabel = QLabel("CR:")
        self.CRLineEdit = CenteredLineEdit()
        self.CRLineEdit.textChanged.connect(lambda: self.UpdateData("Encounter CR", self.CRLineEdit.text()))

        self.ExperienceLabel = QLabel("Experience:")
        self.ExperienceLineEdit = CenteredLineEdit()
        self.ExperienceLineEdit.textChanged.connect(lambda: self.UpdateData("Encounter Experience", self.ExperienceLineEdit.text()))

        self.DescriptionLabel = QLabel("Description:")
        self.DescriptionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.DescriptionTextEdit = IndentingTextEdit(TextChangedSlot=lambda: self.UpdateData("Encounter Description", self.DescriptionTextEdit.toPlainText()))
        self.DescriptionTextEdit.setTabChangesFocus(True)
        self.DescriptionTextEdit.setMinimumHeight(200)

        self.RewardsLabel = QLabel("Rewards:")
        self.RewardsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.RewardsTextEdit = IndentingTextEdit(TextChangedSlot=lambda: self.UpdateData("Encounter Rewards", self.RewardsTextEdit.toPlainText()))
        self.RewardsTextEdit.setTabChangesFocus(True)
        self.RewardsTextEdit.setMinimumHeight(200)

        self.NotesLabel = QLabel("Notes:")
        self.NotesLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.NotesTextEdit = IndentingTextEdit(TextChangedSlot=lambda: self.UpdateData("Encounter Notes", self.NotesTextEdit.toPlainText()))
        self.NotesTextEdit.setTabChangesFocus(True)
        self.NotesTextEdit.setMinimumHeight(200)

        # Initiative Order
        self.InitiativeOrderLabel = QLabel("Initiative Order")
        self.InitiativeOrderLabel.setStyleSheet(self.SectionLabelStyle)
        self.InitiativeOrderLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.InitiativeOrderLabel.setMargin(self.HeaderLabelMargin)

        self.RoundLabel = QLabel("Round:")
        self.RoundLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.RoundSpinBox = QSpinBox()
        self.RoundSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.RoundSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.RoundSpinBox.setButtonSymbols(self.RoundSpinBox.NoButtons)
        self.RoundSpinBox.setRange(1, 1000000000)
        self.RoundSpinBox.setValue(1)
        self.RoundSpinBox.valueChanged.connect(lambda: self.UpdateData("Round", self.RoundSpinBox.value()))

        self.InitiativeOrderTreeWidget = InitiativeOrderTreeWidget(self)
        self.InitiativeOrderTreeWidget.itemActivated.connect(self.EditEntry)
        self.InitiativeOrderTreeWidget.setMinimumWidth(700)
        self.InitiativeOrderTreeWidget.setMinimumHeight(400)

        self.NewRoundButton = QPushButton("New Round")
        self.NewRoundButton.clicked.connect(self.NewRound)
        self.NextTurnButton = QPushButton("Next Turn")
        self.NextTurnButton.clicked.connect(self.NextTurn)
        self.ClearTurnsButton = QPushButton("Clear Turns")
        self.ClearTurnsButton.clicked.connect(self.ClearTurns)

        self.AddEntryButton = AddButton(self.AddEntry, "Add Entry")
        self.DeleteEntryButton = DeleteButton(self.DeleteEntry, "Delete Entry")
        self.EditEntryButton = EditButton(self.EditEntry, "Edit Entry")
        self.SortInitiativeButton = SortButton(self.SortInitiative, "Sort Initiative")

        # Create and Set Layout
        self.Layout = QGridLayout()

        self.HeaderFrame = QFrame()
        self.HeaderFrame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.HeaderLayout = QGridLayout()
        self.HeaderLayout.addWidget(self.NameLabel, 0, 0)
        self.HeaderLayout.addWidget(self.NameLineEdit, 0, 1)
        self.HeaderLayout.addWidget(self.CRLabel, 0, 2)
        self.HeaderLayout.addWidget(self.CRLineEdit, 0, 3)
        self.HeaderLayout.addWidget(self.ExperienceLabel, 0, 4)
        self.HeaderLayout.addWidget(self.ExperienceLineEdit, 0, 5)
        self.HeaderTextEditsLayout = QGridLayout()
        self.HeaderTextEditsLayout.addWidget(self.DescriptionLabel, 0, 0)
        self.HeaderTextEditsLayout.addWidget(self.DescriptionTextEdit, 1, 0)
        self.HeaderTextEditsLayout.addWidget(self.RewardsLabel, 0, 1)
        self.HeaderTextEditsLayout.addWidget(self.RewardsTextEdit, 1, 1)
        self.HeaderTextEditsLayout.addWidget(self.NotesLabel, 0, 2)
        self.HeaderTextEditsLayout.addWidget(self.NotesTextEdit, 1, 2)
        self.HeaderLayout.addLayout(self.HeaderTextEditsLayout, 1, 0, 1, 6)
        self.HeaderFrame.setLayout(self.HeaderLayout)
        self.Layout.addWidget(self.HeaderFrame, 0, 0)

        self.InitiativeOrderFrame = QFrame()
        self.InitiativeOrderFrame.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.InitiativeOrderLayout = QGridLayout()
        self.InitiativeOrderLayout.addWidget(self.InitiativeOrderLabel, 0, 0, 1, 2)
        self.RoundLayout = QGridLayout()
        self.RoundLayout.addWidget(self.RoundLabel, 0, 0)
        self.RoundLayout.addWidget(self.RoundSpinBox, 1, 0)
        self.InitiativeOrderLayout.addLayout(self.RoundLayout, 1, 0, 2, 1)
        self.TextButtonsLayout = QGridLayout()
        self.TextButtonsLayout.addWidget(self.NewRoundButton, 0, 0)
        self.TextButtonsLayout.addWidget(self.NextTurnButton, 0, 1)
        self.TextButtonsLayout.addWidget(self.ClearTurnsButton, 0, 2)
        self.InitiativeOrderLayout.addLayout(self.TextButtonsLayout, 1, 1)
        self.IconButtonsLayout = QGridLayout()
        self.IconButtonsLayout.addWidget(self.AddEntryButton, 0, 0)
        self.IconButtonsLayout.addWidget(self.DeleteEntryButton, 0, 1)
        self.IconButtonsLayout.addWidget(self.EditEntryButton, 0, 2)
        self.IconButtonsLayout.addWidget(self.SortInitiativeButton, 0, 3)
        self.InitiativeOrderLayout.addLayout(self.IconButtonsLayout, 2, 1)
        self.InitiativeOrderLayout.addWidget(self.InitiativeOrderTreeWidget, 3, 0, 1, 2)
        self.InitiativeOrderLayout.setRowStretch(3, 1)
        self.InitiativeOrderFrame.setLayout(self.InitiativeOrderLayout)
        self.Layout.addWidget(self.InitiativeOrderFrame, 1, 0)

        self.Layout.setRowStretch(1, 1)

        self.Frame.setLayout(self.Layout)

        # Create Actions
        self.CreateActions()

        # Create Menu Bar
        self.CreateMenuBar()

        # Create Status Bar
        self.StatusBar = self.statusBar()

        # Create Keybindings
        self.CreateKeybindings()

    def CreateActions(self):
        self.NewAction = QAction("New")
        self.NewAction.triggered.connect(self.NewActionTriggered)

        self.OpenAction = QAction("Open")
        self.OpenAction.triggered.connect(self.OpenActionTriggered)

        self.SaveAction = QAction("Save")
        self.SaveAction.triggered.connect(self.SaveActionTriggered)

        self.SaveAsAction = QAction("Save As")
        self.SaveAsAction.triggered.connect(self.SaveAsActionTriggered)

        self.GzipModeAction = QAction("Gzip Mode (Smaller Files)")
        self.GzipModeAction.setCheckable(True)
        self.GzipModeAction.setChecked(self.GzipMode)
        self.GzipModeAction.triggered.connect(self.ToggleGzipMode)

        self.QuitAction = QAction("Quit")
        self.QuitAction.triggered.connect(self.close)

        self.CoinCalculatorAction = QAction("Coin Calculator")
        self.CoinCalculatorAction.triggered.connect(self.ShowCoinCalculator)

        self.NewRoundAction = QAction("New Round")
        self.NewRoundAction.triggered.connect(self.NewRound)

        self.NextTurnAction = QAction("Next Turn")
        self.NextTurnAction.triggered.connect(self.NextTurn)

        self.ClearTurnsAction = QAction("Clear Turns")
        self.ClearTurnsAction.triggered.connect(self.ClearTurns)

        self.SortInitiativeAction = QAction("Sort Initiative")
        self.SortInitiativeAction.triggered.connect(self.SortInitiative)

    def CreateMenuBar(self):
        self.MenuBar = self.menuBar()

        self.FileMenu = self.MenuBar.addMenu("File")
        self.FileMenu.addAction(self.NewAction)
        self.FileMenu.addAction(self.OpenAction)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.SaveAction)
        self.FileMenu.addAction(self.SaveAsAction)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.GzipModeAction)
        self.FileMenu.addSeparator()
        self.FileMenu.addAction(self.QuitAction)

        self.InitiativeOrderMenu = self.MenuBar.addMenu("Initiative Order")
        self.InitiativeOrderMenu.addAction(self.NewRoundAction)
        self.InitiativeOrderMenu.addAction(self.NextTurnAction)
        self.InitiativeOrderMenu.addAction(self.ClearTurnsAction)
        self.InitiativeOrderMenu.addAction(self.SortInitiativeAction)

        self.MenuBar.addAction(self.CoinCalculatorAction)

    def CreateKeybindings(self):
        self.DefaultKeybindings = {}
        self.DefaultKeybindings["NewAction"] = "Ctrl+N"
        self.DefaultKeybindings["OpenAction"] = "Ctrl+O"
        self.DefaultKeybindings["SaveAction"] = "Ctrl+S"
        self.DefaultKeybindings["SaveAsAction"] = "Ctrl+Shift+S"
        self.DefaultKeybindings["QuitAction"] = "Ctrl+Q"
        self.DefaultKeybindings["NewRoundAction"] = "Ctrl+R"
        self.DefaultKeybindings["NextTurnAction"] = "Ctrl+T"
        self.DefaultKeybindings["ClearTurnsAction"] = "Ctrl+Shift+T"
        self.DefaultKeybindings["SortInitiativeAction"] = "Ctrl+I"

    def LoadConfigs(self):
        # Keybindings
        KeybindingsFile = self.GetResourcePath("Configs/EncounterKeybindings.cfg")
        if os.path.isfile(KeybindingsFile):
            with open(KeybindingsFile, "r") as ConfigFile:
                self.Keybindings = json.loads(ConfigFile.read())
        else:
            self.Keybindings = copy.deepcopy(self.DefaultKeybindings)
        for Action, Keybinding in self.DefaultKeybindings.items():
            if Action not in self.Keybindings:
                self.Keybindings[Action] = Keybinding
        InvalidBindings = []
        for Action in self.Keybindings.keys():
            if Action not in self.DefaultKeybindings:
                InvalidBindings.append(Action)
        for InvalidBinding in InvalidBindings:
            del self.Keybindings[InvalidBinding]
        for Action, Keybinding in self.Keybindings.items():
            getattr(self, Action).setShortcut(Keybinding)

    def SaveConfigs(self):
        if not os.path.isdir(self.GetResourcePath("Configs")):
            os.mkdir(self.GetResourcePath("Configs"))

        # Keybindings
        with open(self.GetResourcePath("Configs/NPCKeybindings.cfg"), "w") as ConfigFile:
            ConfigFile.write(json.dumps(self.Keybindings, indent=2))

        # Last Opened Directory
        self.SaveLastOpenedDirectory()

        # Gzip Mode
        self.SaveGzipMode()

    # Encounter Methods
    def UpdateData(self, Data, NewValue):
        if not self.UpdatingFieldsFromEncounter:
            self.Encounter.UpdateData(Data, NewValue)
            self.UpdateUnsavedChangesFlag(True)

    def AddEntry(self):
        pass

    def DeleteEntry(self):
        pass

    def EditEntry(self):
        pass

    def SortInitiative(self):
        pass

    def NewRound(self):
        pass

    def NextTurn(self):
        pass

    def ClearTurns(self):
        pass

    # View Methods
    def ShowCoinCalculator(self):
        CoinCalculatorDialog(self)

    # Save and Open Methods
    def NewActionTriggered(self):
        if self.New(self.Encounter):
            self.Encounter = Encounter()
        self.UpdatingFieldsFromEncounter = True
        self.UpdateDisplay()
        self.UpdatingFieldsFromEncounter = False

    def OpenActionTriggered(self):
        OpenData = self.Open(self.Encounter)
        if OpenData is not None:
            self.Encounter = OpenData
        self.UpdatingFieldsFromEncounter = True
        self.UpdateDisplay()
        self.UpdatingFieldsFromEncounter = False

    def SaveActionTriggered(self):
        self.Save(self.Encounter)
        self.UpdateDisplay()

    def SaveAsActionTriggered(self):
        self.Save(self.Encounter, SaveAs=True)
        self.UpdateDisplay()

    def ToggleGzipMode(self):
        self.GzipMode = not self.GzipMode

    def closeEvent(self, event):
        Close = True
        if self.UnsavedChanges:
            SavePrompt = self.DisplayMessageBox("Save unsaved changes before closing?", Icon=QMessageBox.Warning, Buttons=(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel))
            if SavePrompt == QMessageBox.Yes:
                if not self.Save(self.Encounter):
                    Close = False
            elif SavePrompt == QMessageBox.No:
                pass
            elif SavePrompt == QMessageBox.Cancel:
                Close = False
        if not Close:
            event.ignore()
        else:
            self.SaveConfigs()
            event.accept()

    def UpdateUnsavedChangesFlag(self, UnsavedChanges):
        self.UnsavedChanges = UnsavedChanges
        self.UpdateDisplay()

   # Display Update Methods
    def UpdateDisplay(self):
        self.UpdateWindowTitle()

        # Initiative Order
        self.InitiativeOrderTreeWidget.FillFromInitiativeOrder()

        # Updating Fields from Encounter
        if self.UpdatingFieldsFromEncounter:
            # Header
            self.NameLineEdit.setText(self.Encounter.EncounterData["Encounter Name"])
            self.CRLineEdit.setText(self.Encounter.EncounterData["Encounter CR"])
            self.ExperienceLineEdit.setText(self.Encounter.EncounterData["Encounter Experience"])
            self.DescriptionTextEdit.setPlainText(self.Encounter.EncounterData["Encounter Description"])
            self.RewardsTextEdit.setPlainText(self.Encounter.EncounterData["Encounter Rewards"])
            self.NotesTextEdit.setPlainText(self.Encounter.EncounterData["Encounter Notes"])

            # Round
            self.RoundSpinBox.setValue(self.Encounter.EncounterData["Round"])

    def UpdateWindowTitle(self):
        CurrentFileTitleSection = " [" + os.path.basename(self.CurrentOpenFileName) + "]" if self.CurrentOpenFileName != "" else ""
        UnsavedChangesIndicator = " *" if self.UnsavedChanges else ""
        self.setWindowTitle(self.ScriptName + " Encounter Sheet" + CurrentFileTitleSection + UnsavedChangesIndicator)
