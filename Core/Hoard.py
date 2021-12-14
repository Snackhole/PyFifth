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

    def UpdateData(self, Data, NewValue):
        if Data in [
            "Name or Owners",
            "Location",
            "Storage Costs",
            "Notes"
        ]:
            self.HoardData[Data] = NewValue
            return True
        elif type(Data) is tuple:
            if len(Data) == 2:
                self.HoardData[Data[0]][Data[1]] = NewValue
                return True

        return False

    def GetDerivedData(self):
        DerivedData = {}

        # Coin Counts
        CPCount = Decimal(self.HoardData["Coins"]["CP"])
        SPCount = Decimal(self.HoardData["Coins"]["SP"])
        EPCount = Decimal(self.HoardData["Coins"]["EP"])
        GPCount = Decimal(self.HoardData["Coins"]["GP"])
        PPCount = Decimal(self.HoardData["Coins"]["PP"])
        TotalCoinCount = CPCount + SPCount + EPCount + GPCount + PPCount

        # Coin Value
        CoinValue = Decimal(0)
        CoinValue += CPCount * self.CoinValues["CP"]
        CoinValue += SPCount * self.CoinValues["SP"]
        CoinValue += EPCount * self.CoinValues["EP"]
        CoinValue += GPCount * self.CoinValues["GP"]
        CoinValue += PPCount * self.CoinValues["PP"]
        DerivedData["Value of Coins"] = CoinValue.quantize(Decimal("0.01"))

        # Coin Load
        CoinLoad = TotalCoinCount * self.LoadPerCoin
        DerivedData["Load of Coins"] = CoinLoad.quantize(Decimal("0.01"))

        # Inventory Load and Value
        InventoryLoad = Decimal(0)
        InventoryValue = Decimal(0)

        # Update Inventory Load and Value from Inventory Items
        for ItemIndex in range(0, len(self.HoardData["Inventory"])):
            # Total Load and Value
            TotalLoadAndValue = self.CalculateItemTotalLoadAndValue(ItemIndex)
            TotalItemLoad = TotalLoadAndValue["Item Total Load"]
            TotalItemValue = TotalLoadAndValue["Item Total Value"]

            # Update Inventory Totals
            InventoryLoad += TotalItemLoad
            InventoryValue += TotalItemValue

        DerivedData["Load of Inventory"] = InventoryLoad.quantize(Decimal("0.01"))
        DerivedData["Value of Inventory"] = InventoryValue.quantize(Decimal("0.01"))

        # Total Value
        DerivedData["Total Value"] = (CoinValue + InventoryValue).quantize(Decimal("0.01"))

        # Total Load
        DerivedData["Total Load"] = (CoinLoad + InventoryLoad).quantize(Decimal("0.01"))

        return DerivedData

    # Hoard Calculation Methods
    def CalculateItemTotalLoadAndValue(self, ItemIndex):
        Item = self.HoardData["Inventory"][ItemIndex]
        Totals = {}
        Totals["Item Total Load"] = Decimal(Item["Item Count"]) * Decimal(Item["Item Unit Weight"])
        Totals["Item Total Value"] = Decimal(Item["Item Count"]) * Decimal(Item["Item Unit Value"]) * Decimal(self.CoinValues[Item["Item Unit Value Denomination"]])
        return Totals

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
