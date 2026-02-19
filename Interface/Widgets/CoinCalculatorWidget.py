from decimal import Decimal
import json
import os

from PyQt6 import QtCore
from PyQt6.QtGui import QIcon, QPalette, QColor
from PyQt6.QtWidgets import QFrame, QSizePolicy, QLabel, QSpinBox, QDoubleSpinBox, QGridLayout, QApplication


class CoinCalculatorWidget(QFrame):
    def __init__(self, ScriptName=None, AbsoluteDirectoryPath=None, AppInst=None):
        # Initialize Frame
        super().__init__()

        # Store Parameters
        self.ScriptName = ScriptName
        self.AbsoluteDirectoryPath = AbsoluteDirectoryPath
        self.AppInst = AppInst

        # Variables
        self.WindowMode = self.ScriptName is not None and self.AbsoluteDirectoryPath is not None and self.AppInst is not None
        self.CoinValues = {}
        self.CoinValues["CP"] = Decimal(0.01)
        self.CoinValues["SP"] = Decimal(0.1)
        self.CoinValues["EP"] = Decimal(0.5)
        self.CoinValues["GP"] = Decimal(1)
        self.CoinValues["PP"] = Decimal(10)
        self.LoadPerCoin = Decimal(0.02)

        # Window Icon
        if self.WindowMode:
            self.WindowIcon = QIcon(self.GetResourcePath("Assets/PyFifth Icon.png"))
            self.setWindowIcon(self.WindowIcon)

        # Styles
        self.SectionLabelStyle = "QLabel {font-size: 10pt; font-weight: bold;}"

        # Header Label Margin
        self.HeaderLabelMargin = 5

        # Inputs Size Policy
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        # Window Theme
        if self.WindowMode:
            self.LoadTheme()

        # Coin Calculator Label
        self.CoinCalculatorLabel = QLabel("Coin Calculator")
        self.CoinCalculatorLabel.setStyleSheet(self.SectionLabelStyle)
        self.CoinCalculatorLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CoinCalculatorLabel.setMargin(self.HeaderLabelMargin)

        # Header Labels
        self.InputLabel = QLabel("Input")
        self.InputLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.InputLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.InputLabel.setMargin(5)
        self.OutputLabel = QLabel("Output")
        self.OutputLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.OutputLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.OutputLabel.setMargin(5)

        # Row Labels
        self.CPLabel = QLabel("CP")
        self.CPLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CPLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.CPLabel.setMargin(5)
        self.SPLabel = QLabel("SP")
        self.SPLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SPLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.SPLabel.setMargin(5)
        self.EPLabel = QLabel("EP")
        self.EPLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.EPLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.EPLabel.setMargin(5)
        self.GPLabel = QLabel("GP")
        self.GPLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.GPLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.GPLabel.setMargin(5)
        self.PPLabel = QLabel("PP")
        self.PPLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.PPLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.PPLabel.setMargin(5)
        self.LoadLabel = QLabel("Lbs.")
        self.LoadLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.LoadLabel.setFrameStyle(QLabel.Shape.StyledPanel | QLabel.Shadow.Plain)
        self.LoadLabel.setMargin(5)

        # Row Inputs
        self.CPInputSpinBox = QSpinBox()
        self.CPInputSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CPInputSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CPInputSpinBox.setButtonSymbols(self.CPInputSpinBox.ButtonSymbols.NoButtons)
        self.CPInputSpinBox.setRange(0, 1000000000)
        self.CPInputSpinBox.setValue(0)
        self.CPInputSpinBox.valueChanged.connect(self.Calculate)
        self.SPInputSpinBox = QSpinBox()
        self.SPInputSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SPInputSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SPInputSpinBox.setButtonSymbols(self.SPInputSpinBox.ButtonSymbols.NoButtons)
        self.SPInputSpinBox.setRange(0, 1000000000)
        self.SPInputSpinBox.setValue(0)
        self.SPInputSpinBox.valueChanged.connect(self.Calculate)
        self.EPInputSpinBox = QSpinBox()
        self.EPInputSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.EPInputSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.EPInputSpinBox.setButtonSymbols(self.EPInputSpinBox.ButtonSymbols.NoButtons)
        self.EPInputSpinBox.setRange(0, 1000000000)
        self.EPInputSpinBox.setValue(0)
        self.EPInputSpinBox.valueChanged.connect(self.Calculate)
        self.GPInputSpinBox = QSpinBox()
        self.GPInputSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.GPInputSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.GPInputSpinBox.setButtonSymbols(self.GPInputSpinBox.ButtonSymbols.NoButtons)
        self.GPInputSpinBox.setRange(0, 1000000000)
        self.GPInputSpinBox.setValue(0)
        self.GPInputSpinBox.valueChanged.connect(self.Calculate)
        self.PPInputSpinBox = QSpinBox()
        self.PPInputSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.PPInputSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.PPInputSpinBox.setButtonSymbols(self.PPInputSpinBox.ButtonSymbols.NoButtons)
        self.PPInputSpinBox.setRange(0, 1000000000)
        self.PPInputSpinBox.setValue(0)
        self.PPInputSpinBox.valueChanged.connect(self.Calculate)

        # Row Outputs
        self.CPOutputSpinBox = QDoubleSpinBox()
        self.CPOutputSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CPOutputSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CPOutputSpinBox.setButtonSymbols(self.CPOutputSpinBox.ButtonSymbols.NoButtons)
        self.CPOutputSpinBox.setRange(0, 1000000000)
        self.CPOutputSpinBox.setValue(0)
        self.CPOutputSpinBox.setReadOnly(True)
        self.CPOutputSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.SPOutputSpinBox = QDoubleSpinBox()
        self.SPOutputSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.SPOutputSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SPOutputSpinBox.setButtonSymbols(self.SPOutputSpinBox.ButtonSymbols.NoButtons)
        self.SPOutputSpinBox.setRange(0, 1000000000)
        self.SPOutputSpinBox.setValue(0)
        self.SPOutputSpinBox.setReadOnly(True)
        self.SPOutputSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.EPOutputSpinBox = QDoubleSpinBox()
        self.EPOutputSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.EPOutputSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.EPOutputSpinBox.setButtonSymbols(self.EPOutputSpinBox.ButtonSymbols.NoButtons)
        self.EPOutputSpinBox.setRange(0, 1000000000)
        self.EPOutputSpinBox.setValue(0)
        self.EPOutputSpinBox.setReadOnly(True)
        self.EPOutputSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.GPOutputSpinBox = QDoubleSpinBox()
        self.GPOutputSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.GPOutputSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.GPOutputSpinBox.setButtonSymbols(self.GPOutputSpinBox.ButtonSymbols.NoButtons)
        self.GPOutputSpinBox.setRange(0, 1000000000)
        self.GPOutputSpinBox.setValue(0)
        self.GPOutputSpinBox.setReadOnly(True)
        self.GPOutputSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.PPOutputSpinBox = QDoubleSpinBox()
        self.PPOutputSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.PPOutputSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.PPOutputSpinBox.setButtonSymbols(self.PPOutputSpinBox.ButtonSymbols.NoButtons)
        self.PPOutputSpinBox.setRange(0, 1000000000)
        self.PPOutputSpinBox.setValue(0)
        self.PPOutputSpinBox.setReadOnly(True)
        self.PPOutputSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.LoadOutputSpinBox = QDoubleSpinBox()
        self.LoadOutputSpinBox.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.LoadOutputSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.LoadOutputSpinBox.setButtonSymbols(self.LoadOutputSpinBox.ButtonSymbols.NoButtons)
        self.LoadOutputSpinBox.setRange(0, 1000000000)
        self.LoadOutputSpinBox.setValue(0)
        self.LoadOutputSpinBox.setReadOnly(True)
        self.LoadOutputSpinBox.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)

        # Layout
        self.Layout = QGridLayout()

        self.Layout.addWidget(self.CoinCalculatorLabel, 0, 0, 1, 3)

        self.Layout.addWidget(self.InputLabel, 1, 1)
        self.Layout.addWidget(self.OutputLabel, 1, 2)

        self.Layout.addWidget(self.CPLabel, 2, 0)
        self.Layout.addWidget(self.CPInputSpinBox, 2, 1)
        self.Layout.addWidget(self.CPOutputSpinBox, 2, 2)

        self.Layout.addWidget(self.SPLabel, 3, 0)
        self.Layout.addWidget(self.SPInputSpinBox, 3, 1)
        self.Layout.addWidget(self.SPOutputSpinBox, 3, 2)

        self.Layout.addWidget(self.EPLabel, 4, 0)
        self.Layout.addWidget(self.EPInputSpinBox, 4, 1)
        self.Layout.addWidget(self.EPOutputSpinBox, 4, 2)

        self.Layout.addWidget(self.GPLabel, 5, 0)
        self.Layout.addWidget(self.GPInputSpinBox, 5, 1)
        self.Layout.addWidget(self.GPOutputSpinBox, 5, 2)

        self.Layout.addWidget(self.PPLabel, 6, 0)
        self.Layout.addWidget(self.PPInputSpinBox, 6, 1)
        self.Layout.addWidget(self.PPOutputSpinBox, 6, 2)

        self.Layout.addWidget(self.LoadLabel, 7, 0)
        self.Layout.addWidget(self.LoadOutputSpinBox, 7, 2)

        for Row in range(2, 8):
            self.Layout.setRowStretch(Row, 1)
        for Column in range(1, 3):
            self.Layout.setColumnStretch(Column, 1)

        self.setLayout(self.Layout)

        # Window Mode
        if self.WindowMode:
            self.setWindowTitle(f"{self.ScriptName} Coin Calculator")
            self.show()
            self.SetGeometryToMinimum()
            self.Center()

        # Select CP Input Spin Box Contents
        self.CPInputSpinBox.selectAll()

    def Calculate(self):
        # Coin Counts
        CPCount = Decimal(self.CPInputSpinBox.value())
        SPCount = Decimal(self.SPInputSpinBox.value())
        EPCount = Decimal(self.EPInputSpinBox.value())
        GPCount = Decimal(self.GPInputSpinBox.value())
        PPCount = Decimal(self.PPInputSpinBox.value())
        TotalCoinCount = CPCount + SPCount + EPCount + GPCount + PPCount

        # Coin Value
        CoinValue = Decimal(0)
        CoinValue += CPCount * self.CoinValues["CP"]
        CoinValue += SPCount * self.CoinValues["SP"]
        CoinValue += EPCount * self.CoinValues["EP"]
        CoinValue += GPCount * self.CoinValues["GP"]
        CoinValue += PPCount * self.CoinValues["PP"]

        # Coin Values Per Denomination
        CoinValueInCP = (CoinValue / self.CoinValues["CP"]).quantize(Decimal("0.01"))
        CoinValueInSP = (CoinValue / self.CoinValues["SP"]).quantize(Decimal("0.01"))
        CoinValueInEP = (CoinValue / self.CoinValues["EP"]).quantize(Decimal("0.01"))
        CoinValueInGP = CoinValue.quantize(Decimal("0.01"))
        CoinValueInPP = (CoinValue / self.CoinValues["PP"]).quantize(Decimal("0.01"))

        # Coin Weight
        CoinLoad = (TotalCoinCount * self.LoadPerCoin).quantize(Decimal("0.01"))

        # Set Output Values
        self.CPOutputSpinBox.setValue(CoinValueInCP)
        self.SPOutputSpinBox.setValue(CoinValueInSP)
        self.EPOutputSpinBox.setValue(CoinValueInEP)
        self.GPOutputSpinBox.setValue(CoinValueInGP)
        self.PPOutputSpinBox.setValue(CoinValueInPP)
        self.LoadOutputSpinBox.setValue(CoinLoad)

    def GetResourcePath(self, RelativeLocation):
        return os.path.join(self.AbsoluteDirectoryPath, RelativeLocation)

    def SetGeometryToMinimum(self):
        FrameGeometryRectangle = self.frameGeometry()
        FrameGeometryRectangle.setWidth(self.minimumWidth())
        FrameGeometryRectangle.setHeight(self.minimumHeight())
        self.setGeometry(FrameGeometryRectangle)

    def Center(self):
        FrameGeometryRectangle = self.frameGeometry()
        DesktopCenterPoint = QApplication.primaryScreen().availableGeometry().center()
        FrameGeometryRectangle.moveCenter(DesktopCenterPoint)
        self.move(FrameGeometryRectangle.topLeft())

    def CreateThemes(self):
        self.Themes = {}

        # Light
        self.Themes["Light"] = QPalette()
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(120, 120, 120, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.AlternateBase, QColor(247, 247, 247, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, QColor(0, 0, 0, 128))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(120, 120, 120, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(120, 120, 120, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Light, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Midlight, QColor(247, 247, 247, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Mid, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Shadow, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Highlight, QColor(0, 120, 215, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.HighlightedText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Link, QColor(0, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.LinkVisited, QColor(255, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.AlternateBase, QColor(233, 231, 227, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, QColor(0, 0, 0, 128))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Light, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Midlight, QColor(227, 227, 227, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Mid, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Shadow, QColor(105, 105, 105, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight, QColor(0, 120, 215, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.HighlightedText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Link, QColor(0, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.LinkVisited, QColor(255, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.AlternateBase, QColor(233, 231, 227, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, QColor(0, 0, 0, 128))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Light, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Midlight, QColor(227, 227, 227, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Mid, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Shadow, QColor(105, 105, 105, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Highlight, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.HighlightedText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Link, QColor(0, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.LinkVisited, QColor(255, 0, 255, 255))

        # Dark
        self.Themes["Dark"] = QPalette()
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.AlternateBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, QColor(239, 240, 241, 128))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Light, QColor(24, 27, 29, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Midlight, QColor(36, 40, 44, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Mid, QColor(65, 72, 78, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Shadow, QColor(0, 0, 0, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Highlight, QColor(65, 72, 78, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.HighlightedText, QColor(36, 40, 44, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Link, QColor(41, 128, 185, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.LinkVisited, QColor(127, 140, 141, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, QColor(35, 38, 41, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.AlternateBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, QColor(239, 240, 241, 128))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Light, QColor(24, 27, 29, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Midlight, QColor(36, 40, 44, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Mid, QColor(65, 72, 78, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Shadow, QColor(0, 0, 0, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight, QColor(61, 174, 233, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.HighlightedText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Link, QColor(41, 128, 185, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.LinkVisited, QColor(127, 140, 141, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, QColor(35, 38, 41, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.AlternateBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, QColor(239, 240, 241, 128))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Light, QColor(24, 27, 29, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Midlight, QColor(36, 40, 44, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Mid, QColor(65, 72, 78, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Shadow, QColor(0, 0, 0, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Highlight, QColor(61, 174, 233, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.HighlightedText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Link, QColor(41, 128, 185, 255))
        self.Themes["Dark"].setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.LinkVisited, QColor(127, 140, 141, 255))

    def LoadTheme(self):
        self.CreateThemes()
        ThemeFile = self.GetResourcePath("Configs/Theme.cfg")
        if os.path.isfile(ThemeFile):
            with open(ThemeFile, "r") as ConfigFile:
                self.Theme = json.loads(ConfigFile.read())
        else:
            self.Theme = "Light"
        self.AppInst.setStyle("Fusion")
        self.AppInst.setPalette(self.Themes[self.Theme])
