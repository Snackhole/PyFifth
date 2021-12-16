import copy

from SaveAndLoad.JSONSerializer import SerializableMixin


class Encounter(SerializableMixin):
    def __init__(self):
        # Initialize SerializableMixin
        super().__init__()

        # Create Static Values
        self.CreateStaticValues()

        # Create Encounter Data
        self.CreateEncounterData()

    def CreateStaticValues(self):
        # Initiative Entry Defaults
        self.InitiativeEntryDefaults = {}
        self.InitiativeEntryDefaults["Initiative"] = 0
        self.InitiativeEntryDefaults["Tie Priority"] = 1
        self.InitiativeEntryDefaults["Creature Name"] = "Creature Name"
        self.InitiativeEntryDefaults["Conditions"] = ""
        self.InitiativeEntryDefaults["Location"] = ""
        self.InitiativeEntryDefaults["Notes"] = ""
        self.InitiativeEntryDefaults["Alive"] = True
        self.InitiativeEntryDefaults["Turn Taken"] = False

    def CreateEncounterData(self):
        self.EncounterData = {}
        self.EncounterData["Encounter Name"] = ""
        self.EncounterData["Encounter CR"] = ""
        self.EncounterData["Encounter Experience"] = ""
        self.EncounterData["Encounter Description"] = ""
        self.EncounterData["Encounter Rewards"] = ""
        self.EncounterData["Encounter Notes"] = ""
        self.EncounterData["Round"] = 1
        self.EncounterData["Initiative Order"] = []

    def UpdateData(self, Data, NewValue):
        if Data in [
            "Encounter Name",
            "Encounter CR",
            "Encounter Experience",
            "Encounter Description",
            "Encounter Rewards",
            "Encounter Notes",
            "Round"
        ]:
            self.EncounterData[Data] = NewValue
            return True

        return False

    # Initiative Order Methods
    def CreateInitiativeEntry(self):
        InitiativeEntry = copy.deepcopy(self.InitiativeEntryDefaults)
        return InitiativeEntry

    def AddInitiativeEntry(self):
        NewEntry = self.CreateInitiativeEntry()
        self.EncounterData["Initiative Order"].append(NewEntry)
        EntryIndex = len(self.EncounterData["Initiative Order"]) - 1
        return EntryIndex

    def DeleteInitiativeEntry(self, EntryIndex):
        del self.EncounterData["Initiative Order"][EntryIndex]

    def DeleteLastInitiativeEntry(self):
        EntryIndex = len(self.EncounterData["Initiative Order"]) - 1
        self.DeleteInitiativeEntry(EntryIndex)

    def CopyInitiativeEntry(self, EntryIndex):
        self.EncounterData["Initiative Order"].append(copy.deepcopy(self.EncounterData["Initiative Order"][EntryIndex]))
        NewInitiativeEntryIndex = len(self.EncounterData["Initiative Order"]) - 1
        return NewInitiativeEntryIndex

    def SortInitiativeOrder(self):
        self.EncounterData["Initiative Order"].sort(key=lambda Entry: (Entry["Initiative"], -1 * Entry["Tie Priority"]), reverse=True)

    def NewRound(self):
        self.SortInitiativeOrder()
        self.EncounterData["Round"] += 1
        self.ClearTurns()

    def NextTurn(self):
        self.SortInitiativeOrder()
        for Entry in self.EncounterData["Initiative Order"]:
            if Entry["Turn Taken"]:
                continue
            else:
                Entry["Turn Taken"] = True
                if Entry["Alive"]:
                    break

    def ClearTurns(self):
        for Entry in self.EncounterData["Initiative Order"]:
            Entry["Turn Taken"] = False

    # Serialization Methods
    def SetState(self, NewState):
        self.EncounterData = NewState["Encounter Data"]

    def GetState(self):
        State = {}
        State["Encounter Data"] = self.EncounterData
        return State

    @classmethod
    def CreateFromState(cls, State):
        NewEncounter = cls()
        NewEncounter.SetState(State)
        return NewEncounter
