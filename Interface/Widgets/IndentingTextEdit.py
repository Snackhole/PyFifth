from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QTextEdit


class IndentingTextEdit(QTextEdit):
    def __init__(self, TextChangedSlot=None):
        # Initialize Text Edit
        super().__init__()

        # Store Parameters
        self.TextChangedSlot = TextChangedSlot

        # Variables
        self.UpdatingBlockFormat = False

        # Adjust Indent Width
        self.IndentWidth = 10
        self.document().setIndentWidth(self.IndentWidth)

        # Connect Text Changed Slot
        self.textChanged.connect(self.TextChanged)

    def TextChanged(self):
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
        if self.TextChangedSlot is not None:
            self.TextChangedSlot()
