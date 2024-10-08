import copy
import random

from SaveAndLoad.JSONSerializer import SerializableMixin


class DiceRoller(SerializableMixin):
    def __init__(self, Character=None):
        # Initialize SerializableMixin
        super().__init__()

        # Store Parameters
        self.Character = Character

        # Randomizer
        self.Randomizer = random.Random()

        # Preset Rolls
        self.PresetRolls = []
        self.PresetRollsDefaults = {}
        self.PresetRollsDefaults["Name"] = "New Preset Roll"
        self.PresetRollsDefaults["Dice Number"] = 1
        self.PresetRollsDefaults["Die Type"] = 20
        self.PresetRollsDefaults["Modifier"] = self.Character.CreateStatModifier() if not Character is None else 0
        self.PresetRollsDefaults["Result Messages"] = []
        self.ResultMessageDefaults = {}
        self.ResultMessageDefaults["Result Min"] = 1
        self.ResultMessageDefaults["Result Max"] = 1
        self.ResultMessageDefaults["Result Text"] = "New Result Message"

        # Results Log
        self.ResultsLog = []

    # Rolling Methods
    def RollDice(self, DiceNumber=1, DieType=6, Modifier=0, ResultMessages=None, LogPrefix="", SkipLogging=False):
        if ResultMessages is None:
            ResultMessages = []

        if type(Modifier) is dict:
            Modifier = self.Character.CalculateStatModifier(Modifier)

        # Results Dictionary
        Results = {}
        Results["Dice Number"] = DiceNumber
        Results["Die Type"] = DieType
        Results["Modifier"] = Modifier
        Results["Rolls"] = []
        Results["Total"] = 0
        Results["Log Prefix"] = LogPrefix
        Results["Log Suffix"] = ""

        # Roll
        for Roll in range(DiceNumber):
            CurrentRollResult = self.Randomizer.randint(1, DieType)
            Results["Rolls"].append(CurrentRollResult)

        # Total Roll Results
        Results["Total"] = sum(Results["Rolls"]) + Modifier

        # Logging
        if not SkipLogging:
            # Log Suffix
            for ResultMessage in ResultMessages:
                if Results["Total"] >= ResultMessage["Result Min"] and Results["Total"] <= ResultMessage["Result Max"]:
                    Results["Log Suffix"] += f"\n{ResultMessage["Result Text"]}"
            if not self.Character is None:
                if Results["Dice Number"] == 1 and Results["Die Type"] == 20 and Results["Rolls"][0] >= self.Character.Stats["Crit Minimum"]:
                    Results["Log Suffix"] += "\nCrit!"
                elif Results["Dice Number"] == 1 and Results["Die Type"] == 20 and Results["Rolls"][0] == 1:
                    Results["Log Suffix"] += "\nCrit Fail!"
                    if self.Character.Stats["Lucky Halfling"]:
                        Results["Log Suffix"] += "  But you're lucky, so if this was an attack roll, ability check, or saving throw, you get to roll again one time!"

            # Add to Log
            self.ResultsLog.append(self.CreateLogEntryText(Results))

        return Results

    def RollPresetRoll(self, PresetRollIndex):
        PresetRoll = self.PresetRolls[PresetRollIndex]
        Results = self.RollDice(PresetRoll["Dice Number"], PresetRoll["Die Type"], PresetRoll["Modifier"], PresetRoll["Result Messages"], LogPrefix=f"{PresetRoll["Name"]}:\n")
        return Results

    def AverageRoll(self, DiceNumber=1, DieType=6, Modifier=0, NumberRolls=100000):
        RollResults = []
        for Roll in range(NumberRolls):
            RollResults.append(self.RollDice(DiceNumber, DieType, Modifier, SkipLogging=True)["Total"])
        AverageResult = sum(RollResults) / len(RollResults)
        return AverageResult

    # Preset Roll Methods
    def CreatePresetRoll(self):
        PresetRoll = copy.deepcopy(self.PresetRollsDefaults)
        return PresetRoll

    def AddPresetRoll(self):
        PresetRoll = self.CreatePresetRoll()
        self.PresetRolls.append(PresetRoll)
        PresetRollIndex = len(self.PresetRolls) - 1
        return PresetRollIndex

    def DeletePresetRoll(self, PresetRollIndex):
        del self.PresetRolls[PresetRollIndex]

    def DeleteLastPresetRoll(self):
        PresetRollIndex = len(self.PresetRolls) - 1
        self.DeletePresetRoll(PresetRollIndex)

    def CopyPresetRoll(self, PresetRollIndex):
        self.PresetRolls.append(copy.deepcopy(self.PresetRolls[PresetRollIndex]))
        NewPresetRollIndex = len(self.PresetRolls) - 1
        return NewPresetRollIndex

    def MovePresetRoll(self, PresetRollIndex, Delta):
        TargetIndex = PresetRollIndex + Delta
        if TargetIndex < 0 or TargetIndex >= len(self.PresetRolls):
            return False
        SwapTarget = self.PresetRolls[TargetIndex]
        self.PresetRolls[TargetIndex] = self.PresetRolls[PresetRollIndex]
        self.PresetRolls[PresetRollIndex] = SwapTarget
        return True

    def CreateDieClock(self, Name, DieType, ComplicationThreshold):
        DieClockPresetRolls = []
        for ClockValue in range(DieType + 1):
            CurrentClockValuePresetRoll = self.CreatePresetRoll()
            CurrentClockValuePresetRoll["Name"] = f"{Name}; Current Value:  {str(ClockValue)}{" (Complication Threshold)" if ClockValue == ComplicationThreshold else ""}{" (Beyond Complication Threshold)" if ClockValue > ComplicationThreshold else ""}"
            CurrentClockValuePresetRoll["Die Type"] = DieType
            DieClockPresetRolls.append(CurrentClockValuePresetRoll)
            if ClockValue < ComplicationThreshold:
                BelowThresholdResultMessage = self.CreateResultMessage()
                BelowThresholdResultMessage["Result Min"] = 1
                BelowThresholdResultMessage["Result Max"] = DieType
                BelowThresholdResultMessage["Result Text"] = f"{Name} does not go off; current value below complication threshold."
                CurrentClockValuePresetRoll["Result Messages"].append(BelowThresholdResultMessage)
            elif ClockValue >= ComplicationThreshold and ClockValue != DieType:
                AboveThresholdLowerRollResultMessage = self.CreateResultMessage()
                AboveThresholdLowerRollResultMessage["Result Min"] = 1
                AboveThresholdLowerRollResultMessage["Result Max"] = ClockValue - 1
                AboveThresholdLowerRollResultMessage["Result Text"] = f"Current clock value exceeds roll result; {Name} goes off!"
                AboveThresholdHigherRollResultMessage = self.CreateResultMessage()
                AboveThresholdHigherRollResultMessage["Result Min"] = ClockValue
                AboveThresholdHigherRollResultMessage["Result Max"] = DieType
                AboveThresholdHigherRollResultMessage["Result Text"] = f"Roll result equals or exceeds current clock value; {Name} does not go off."
                CurrentClockValuePresetRoll["Result Messages"].append(AboveThresholdLowerRollResultMessage)
                CurrentClockValuePresetRoll["Result Messages"].append(AboveThresholdHigherRollResultMessage)
            else:
                MaximumClockValueResultMessage = self.CreateResultMessage()
                MaximumClockValueResultMessage["Result Min"] = 1
                MaximumClockValueResultMessage["Result Max"] = DieType
                MaximumClockValueResultMessage["Result Text"] = f"{Name} at maximum value; {Name} goes off!"
                CurrentClockValuePresetRoll["Result Messages"].append(MaximumClockValueResultMessage)
        self.PresetRolls = self.PresetRolls + DieClockPresetRolls

    # Result Message Methods
    def CreateResultMessage(self):
        ResultMessage = copy.deepcopy(self.ResultMessageDefaults)
        return ResultMessage

    def AddResultMessage(self, PresetRollIndex):
        PresetRoll = self.PresetRolls[PresetRollIndex]
        ResultMessage = self.CreateResultMessage()
        PresetRoll["Result Messages"].append(ResultMessage)
        ResultMessageIndex = len(PresetRoll["Result Messages"]) - 1
        return ResultMessageIndex

    def DeleteResultMessage(self, PresetRollIndex, ResultMessageIndex):
        PresetRoll = self.PresetRolls[PresetRollIndex]
        del PresetRoll["Result Messages"][ResultMessageIndex]

    def DeleteLastResultMessage(self, PresetRollIndex):
        PresetRoll = self.PresetRolls[PresetRollIndex]
        ResultMessageIndex = len(PresetRoll["Result Messages"]) - 1
        self.DeleteResultMessage(PresetRollIndex, ResultMessageIndex)

    def CopyResultMessage(self, PresetRollIndex, ResultMessageIndex):
        PresetRoll = self.PresetRolls[PresetRollIndex]
        PresetRoll["Result Messages"].append(copy.deepcopy(PresetRoll["Result Messages"][ResultMessageIndex]))
        NewResultMessageIndex = len(PresetRoll["Result Messages"]) - 1
        return NewResultMessageIndex

    def MoveResultMessage(self, PresetRollIndex, ResultMessageIndex, Delta):
        PresetRoll = self.PresetRolls[PresetRollIndex]
        TargetIndex = ResultMessageIndex + Delta
        if TargetIndex < 0 or TargetIndex >= len(PresetRoll["Result Messages"]):
            return False
        SwapTarget = PresetRoll["Result Messages"][TargetIndex]
        PresetRoll["Result Messages"][TargetIndex] = PresetRoll["Result Messages"][ResultMessageIndex]
        PresetRoll["Result Messages"][ResultMessageIndex] = SwapTarget
        return True

    # Log Methods
    def CreateLogEntryText(self, Results):
        ResultText = Results["Log Prefix"]
        ResultText += f"{str(Results["Dice Number"])}d{str(Results["Die Type"])}{"+" if Results["Modifier"] >= 0 else ""}{str(Results["Modifier"])} ->\n"
        ResultText += f"{str(Results["Rolls"])}{"+" if Results["Modifier"] >= 0 else ""}{str(Results["Modifier"])} ->\n"
        ResultText += str(Results["Total"])
        ResultText += Results["Log Suffix"]
        return ResultText

    def CreateLogText(self):
        LogText = ""
        for ResultsIndex in reversed(range(len(self.ResultsLog))):
            LogText += self.ResultsLog[ResultsIndex]
            if not ResultsIndex == 0:
                LogText += "\n\n---\n\n"
        return LogText

    def AddLogEntry(self, LogText):
        self.ResultsLog.append(LogText)

    def RemoveLastLogEntry(self):
        self.ResultsLog = self.ResultsLog[:-1]

    def ClearLog(self):
        self.ResultsLog.clear()

    # Serialization Methods
    def SetState(self, NewState):
        self.PresetRolls = NewState["PresetRolls"]
        self.PresetRollsDefaults = NewState["PresetRollsDefaults"]
        self.ResultMessageDefaults = NewState["ResultMessageDefaults"]
        self.ResultsLog = NewState["ResultsLog"]

    def GetState(self):
        State = {}
        State["PresetRolls"] = self.PresetRolls
        State["PresetRollsDefaults"] = self.PresetRollsDefaults
        State["ResultMessageDefaults"] = self.ResultMessageDefaults
        State["ResultsLog"] = self.ResultsLog
        return State

    @classmethod
    def CreateFromState(cls, State):
        NewDiceRoller = cls()
        NewDiceRoller.SetState(State)
        return NewDiceRoller
