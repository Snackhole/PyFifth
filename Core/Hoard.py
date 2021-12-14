from decimal import Decimal

from SaveAndLoad.JSONSerializer import SerializableMixin


class Hoard(SerializableMixin):
    def __init__(self):
        # Initialize SerializableMixin
        super().__init__()

        # Create Static Values
        self.CreateStaticValues()

        # Create Inventory
        self.CreateInventory()

    def CreateStaticValues(self):
        # Inventory Item Defaults
        self.InventoryItemDefaults = {}
        self.InventoryItemDefaults["Item Name"] = "Item Name"
        self.InventoryItemDefaults["Item Count"] = 1
        self.InventoryItemDefaults["Item Unit Weight"] = 0.0
        self.InventoryItemDefaults["Item Unit Value"] = 0.0
        self.InventoryItemDefaults["Item Unit Value Denomination"] = "CP"
        self.InventoryItemDefaults["Item Tag"] = ""
        self.InventoryItemDefaults["Item Category"] = ""
        self.InventoryItemDefaults["Item Rarity"] = ""
        self.InventoryItemDefaults["Item Description"] = ""

        # Coin Values
        self.CoinValues = {}
        self.CoinValues["CP"] = Decimal(0.01)
        self.CoinValues["SP"] = Decimal(0.1)
        self.CoinValues["EP"] = Decimal(0.5)
        self.CoinValues["GP"] = Decimal(1)
        self.CoinValues["PP"] = Decimal(10)

        # Load Per Coin
        self.LoadPerCoin = Decimal(0.02)

        # Coin Values in CP
        self.CoinValuesInCP = {}
        self.CoinValuesInCP["CPValueInCP"] = Decimal(1)
        self.CoinValuesInCP["SPValueInCP"] = Decimal(10)
        self.CoinValuesInCP["EPValueInCP"] = Decimal(50)
        self.CoinValuesInCP["GPValueInCP"] = Decimal(100)
        self.CoinValuesInCP["PPValueInCP"] = Decimal(1000)

    def CreateInventory(self):
        self.HoardData = {}
        self.HoardData["Name or Owners"] = ""
        self.HoardData["Location"] = ""
        self.HoardData["Storage Costs"] = ""
        self.HoardData["Coins"] = {}
        self.HoardData["Coins"]["CP"] = 0
        self.HoardData["Coins"]["SP"] = 0
        self.HoardData["Coins"]["EP"] = 0
        self.HoardData["Coins"]["GP"] = 0
        self.HoardData["Coins"]["PP"] = 0
        self.HoardData["Notes"] = ""
        self.HoardData["Inventory"] = []

    # Serialization Methods
    def SetState(self, NewState):
        self.HoardData = NewState["Hoard Data"]

    def GetState(self):
        State = {}
        State["Hoard Data"] = self.HoardData
        return State

    @classmethod
    def CreateFromState(cls, State):
        NewHoard = cls()
        NewHoard.SetState(State)
        return NewHoard
