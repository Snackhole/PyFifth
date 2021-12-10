from decimal import Decimal
import json
import os

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import QFrame, QSizePolicy, QLabel, QSpinBox, QDoubleSpinBox, QGridLayout, QApplication


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
        self.InputsSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # Window Theme
        if self.WindowMode:
            self.LoadTheme()

        # Coin Calculator Label
        self.CoinCalculatorLabel = QLabel("Coin Calculator")
        self.CoinCalculatorLabel.setStyleSheet(self.SectionLabelStyle)
        self.CoinCalculatorLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.CoinCalculatorLabel.setMargin(self.HeaderLabelMargin)

        # Header Labels
        self.InputLabel = QLabel("Input")
        self.InputLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.InputLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.InputLabel.setMargin(5)
        self.OutputLabel = QLabel("Output")
        self.OutputLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.OutputLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.OutputLabel.setMargin(5)

        # Row Labels
        self.CPLabel = QLabel("CP")
        self.CPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.CPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.CPLabel.setMargin(5)
        self.SPLabel = QLabel("SP")
        self.SPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.SPLabel.setMargin(5)
        self.EPLabel = QLabel("EP")
        self.EPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.EPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.EPLabel.setMargin(5)
        self.GPLabel = QLabel("GP")
        self.GPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.GPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.GPLabel.setMargin(5)
        self.PPLabel = QLabel("PP")
        self.PPLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.PPLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.PPLabel.setMargin(5)
        self.LoadLabel = QLabel("Lbs.")
        self.LoadLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.LoadLabel.setFrameStyle(QLabel.StyledPanel | QLabel.Plain)
        self.LoadLabel.setMargin(5)

        # Row Inputs
        self.CPInputSpinBox = QSpinBox()
        self.CPInputSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.CPInputSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CPInputSpinBox.setButtonSymbols(self.CPInputSpinBox.NoButtons)
        self.CPInputSpinBox.setRange(0, 1000000000)
        self.CPInputSpinBox.setValue(0)
        self.CPInputSpinBox.valueChanged.connect(self.Calculate)
        self.SPInputSpinBox = QSpinBox()
        self.SPInputSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.SPInputSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SPInputSpinBox.setButtonSymbols(self.SPInputSpinBox.NoButtons)
        self.SPInputSpinBox.setRange(0, 1000000000)
        self.SPInputSpinBox.setValue(0)
        self.SPInputSpinBox.valueChanged.connect(self.Calculate)
        self.EPInputSpinBox = QSpinBox()
        self.EPInputSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.EPInputSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.EPInputSpinBox.setButtonSymbols(self.EPInputSpinBox.NoButtons)
        self.EPInputSpinBox.setRange(0, 1000000000)
        self.EPInputSpinBox.setValue(0)
        self.EPInputSpinBox.valueChanged.connect(self.Calculate)
        self.GPInputSpinBox = QSpinBox()
        self.GPInputSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.GPInputSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.GPInputSpinBox.setButtonSymbols(self.GPInputSpinBox.NoButtons)
        self.GPInputSpinBox.setRange(0, 1000000000)
        self.GPInputSpinBox.setValue(0)
        self.GPInputSpinBox.valueChanged.connect(self.Calculate)
        self.PPInputSpinBox = QSpinBox()
        self.PPInputSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.PPInputSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.PPInputSpinBox.setButtonSymbols(self.PPInputSpinBox.NoButtons)
        self.PPInputSpinBox.setRange(0, 1000000000)
        self.PPInputSpinBox.setValue(0)
        self.PPInputSpinBox.valueChanged.connect(self.Calculate)

        # Row Outputs
        self.CPOutputSpinBox = QDoubleSpinBox()
        self.CPOutputSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.CPOutputSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.CPOutputSpinBox.setButtonSymbols(self.CPOutputSpinBox.NoButtons)
        self.CPOutputSpinBox.setRange(0, 1000000000)
        self.CPOutputSpinBox.setValue(0)
        self.CPOutputSpinBox.setReadOnly(True)
        self.CPOutputSpinBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.SPOutputSpinBox = QDoubleSpinBox()
        self.SPOutputSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.SPOutputSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.SPOutputSpinBox.setButtonSymbols(self.SPOutputSpinBox.NoButtons)
        self.SPOutputSpinBox.setRange(0, 1000000000)
        self.SPOutputSpinBox.setValue(0)
        self.SPOutputSpinBox.setReadOnly(True)
        self.SPOutputSpinBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.EPOutputSpinBox = QDoubleSpinBox()
        self.EPOutputSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.EPOutputSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.EPOutputSpinBox.setButtonSymbols(self.EPOutputSpinBox.NoButtons)
        self.EPOutputSpinBox.setRange(0, 1000000000)
        self.EPOutputSpinBox.setValue(0)
        self.EPOutputSpinBox.setReadOnly(True)
        self.EPOutputSpinBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.GPOutputSpinBox = QDoubleSpinBox()
        self.GPOutputSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.GPOutputSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.GPOutputSpinBox.setButtonSymbols(self.GPOutputSpinBox.NoButtons)
        self.GPOutputSpinBox.setRange(0, 1000000000)
        self.GPOutputSpinBox.setValue(0)
        self.GPOutputSpinBox.setReadOnly(True)
        self.GPOutputSpinBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.PPOutputSpinBox = QDoubleSpinBox()
        self.PPOutputSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.PPOutputSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.PPOutputSpinBox.setButtonSymbols(self.PPOutputSpinBox.NoButtons)
        self.PPOutputSpinBox.setRange(0, 1000000000)
        self.PPOutputSpinBox.setValue(0)
        self.PPOutputSpinBox.setReadOnly(True)
        self.PPOutputSpinBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.LoadOutputSpinBox = QDoubleSpinBox()
        self.LoadOutputSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.LoadOutputSpinBox.setSizePolicy(self.InputsSizePolicy)
        self.LoadOutputSpinBox.setButtonSymbols(self.LoadOutputSpinBox.NoButtons)
        self.LoadOutputSpinBox.setRange(0, 1000000000)
        self.LoadOutputSpinBox.setValue(0)
        self.LoadOutputSpinBox.setReadOnly(True)
        self.LoadOutputSpinBox.setFocusPolicy(QtCore.Qt.NoFocus)

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
            self.setWindowTitle(self.ScriptName + " Coin Calculator")
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
        return self.AbsoluteDirectoryPath + "/" + RelativeLocation

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
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Window, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.WindowText, QColor(120, 120, 120, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Base, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.AlternateBase, QColor(247, 247, 247, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.ToolTipBase, QColor(255, 255, 220, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.ToolTipText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.PlaceholderText, QColor(0, 0, 0, 128))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Text, QColor(120, 120, 120, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Button, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.ButtonText, QColor(120, 120, 120, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Light, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Midlight, QColor(247, 247, 247, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Dark, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Mid, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Shadow, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Highlight, QColor(0, 120, 215, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.Link, QColor(0, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.Disabled, QPalette.LinkVisited, QColor(255, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Window, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.WindowText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Base, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.AlternateBase, QColor(233, 231, 227, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.ToolTipBase, QColor(255, 255, 220, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.ToolTipText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.PlaceholderText, QColor(0, 0, 0, 128))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Text, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Button, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.ButtonText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Light, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Midlight, QColor(227, 227, 227, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Dark, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Mid, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Shadow, QColor(105, 105, 105, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Highlight, QColor(0, 120, 215, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.HighlightedText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.Link, QColor(0, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.Active, QPalette.LinkVisited, QColor(255, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Window, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.WindowText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Base, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.AlternateBase, QColor(233, 231, 227, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.ToolTipBase, QColor(255, 255, 220, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.ToolTipText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.PlaceholderText, QColor(0, 0, 0, 128))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Text, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Button, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.ButtonText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Light, QColor(255, 255, 255, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Midlight, QColor(227, 227, 227, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Dark, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Mid, QColor(160, 160, 160, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Shadow, QColor(105, 105, 105, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Highlight, QColor(240, 240, 240, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.HighlightedText, QColor(0, 0, 0, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.Link, QColor(0, 0, 255, 255))
        self.Themes["Light"].setColor(QPalette.Inactive, QPalette.LinkVisited, QColor(255, 0, 255, 255))

        # Dark
        self.Themes["Dark"] = QPalette()
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Window, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.WindowText, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Base, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.AlternateBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.ToolTipBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.ToolTipText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.PlaceholderText, QColor(239, 240, 241, 128))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Text, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Button, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.ButtonText, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Light, QColor(24, 27, 29, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Midlight, QColor(36, 40, 44, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Dark, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Mid, QColor(65, 72, 78, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Shadow, QColor(0, 0, 0, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Highlight, QColor(65, 72, 78, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.HighlightedText, QColor(36, 40, 44, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.Link, QColor(41, 128, 185, 255))
        self.Themes["Dark"].setColor(QPalette.Disabled, QPalette.LinkVisited, QColor(127, 140, 141, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Window, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.WindowText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Base, QColor(35, 38, 41, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.AlternateBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.ToolTipBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.ToolTipText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.PlaceholderText, QColor(239, 240, 241, 128))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Text, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Button, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.ButtonText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Light, QColor(24, 27, 29, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Midlight, QColor(36, 40, 44, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Dark, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Mid, QColor(65, 72, 78, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Shadow, QColor(0, 0, 0, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Highlight, QColor(61, 174, 233, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.HighlightedText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.Link, QColor(41, 128, 185, 255))
        self.Themes["Dark"].setColor(QPalette.Active, QPalette.LinkVisited, QColor(127, 140, 141, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Window, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.WindowText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Base, QColor(35, 38, 41, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.AlternateBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.ToolTipBase, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.ToolTipText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.PlaceholderText, QColor(239, 240, 241, 128))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Text, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Button, QColor(49, 54, 59, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.ButtonText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.BrightText, QColor(255, 255, 255, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Light, QColor(24, 27, 29, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Midlight, QColor(36, 40, 44, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Dark, QColor(98, 108, 118, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Mid, QColor(65, 72, 78, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Shadow, QColor(0, 0, 0, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Highlight, QColor(61, 174, 233, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.HighlightedText, QColor(239, 240, 241, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.Link, QColor(41, 128, 185, 255))
        self.Themes["Dark"].setColor(QPalette.Inactive, QPalette.LinkVisited, QColor(127, 140, 141, 255))

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
