from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QTextEdit


class IndentingTextEdit(QTextEdit):
    def __init__(self, TextChangedSlot=None, InitialContent=""):
        # Initialize Text Edit
        super().__init__()

        # Store Parameters
        self.TextChangedSlot = TextChangedSlot

        # Variables
        self.UpdatingBlockFormat = False

        # Adjust Indent Width
        self.IndentWidth = 10
        self.document().setIndentWidth(self.IndentWidth)

        # Set Initial Content
        self.setPlainText(InitialContent)

        # Connect Text Changed Slot
        self.textChanged.connect(self.Indent)

        # Initial Indent
        self.Indent(SkipTextChangedSlot=True)

    def Indent(self, SkipTextChangedSlot=False):
        if self.UpdatingBlockFormat:
            return

        # Get Block Count
        BlockCount = self.document().blockCount()

        # Indent Blocks
        for BlockIndex in range(BlockCount):
            CurrentBlock = self.document().findBlockByNumber(BlockIndex)
            CurrentBlockText = CurrentBlock.text()
            if CurrentBlockText.startswith("*"):
                Indent = len(CurrentBlockText) - len(CurrentBlockText.lstrip("*"))
            else:
                Indent = 0
            Cursor = QTextCursor(CurrentBlock)
            CurrentBlockFormat = Cursor.blockFormat()
            CurrentBlockFormat.setIndent(Indent)
            self.UpdatingBlockFormat = True
            Cursor.setBlockFormat(CurrentBlockFormat)
            self.UpdatingBlockFormat = False

        # Call Text Changed Slot
        if self.TextChangedSlot is not None and not SkipTextChangedSlot:
            self.TextChangedSlot()
