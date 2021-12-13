import math

from Core.Character import Character
from Core.DiceRoller import DiceRoller
from SaveAndLoad.JSONSerializer import SerializableMixin


class NonPlayerCharacter(Character, SerializableMixin):
    def __init__(self):
        # Initialize NPC and SerializableMixin
        super().__init__()

        # Create Static Values
        self.CreateStaticValues()

        # Create Stats
        self.CreateStats()

    def CreateStaticValues(self):
        # Common Static Values
        super().CreateStaticValues()

        # Proficiency Bonus by CR
        self.ProficiencyBonusByCR = {}
        self.ProficiencyBonusByCR["0"] = 2
        self.ProficiencyBonusByCR["1/8"] = 2
        self.ProficiencyBonusByCR["1/4"] = 2
        self.ProficiencyBonusByCR["1/2"] = 2
        self.ProficiencyBonusByCR["1"] = 2
        self.ProficiencyBonusByCR["2"] = 2
        self.ProficiencyBonusByCR["3"] = 2
        self.ProficiencyBonusByCR["4"] = 2
        self.ProficiencyBonusByCR["5"] = 3
        self.ProficiencyBonusByCR["6"] = 3
        self.ProficiencyBonusByCR["7"] = 3
        self.ProficiencyBonusByCR["8"] = 3
        self.ProficiencyBonusByCR["9"] = 4
        self.ProficiencyBonusByCR["10"] = 4
        self.ProficiencyBonusByCR["11"] = 4
        self.ProficiencyBonusByCR["12"] = 4
        self.ProficiencyBonusByCR["13"] = 5
        self.ProficiencyBonusByCR["14"] = 5
        self.ProficiencyBonusByCR["15"] = 5
        self.ProficiencyBonusByCR["16"] = 5
        self.ProficiencyBonusByCR["17"] = 6
        self.ProficiencyBonusByCR["18"] = 6
        self.ProficiencyBonusByCR["19"] = 6
        self.ProficiencyBonusByCR["20"] = 6
        self.ProficiencyBonusByCR["21"] = 7
        self.ProficiencyBonusByCR["22"] = 7
        self.ProficiencyBonusByCR["23"] = 7
        self.ProficiencyBonusByCR["24"] = 7
        self.ProficiencyBonusByCR["25"] = 8
        self.ProficiencyBonusByCR["26"] = 8
        self.ProficiencyBonusByCR["27"] = 8
        self.ProficiencyBonusByCR["28"] = 8
        self.ProficiencyBonusByCR["29"] = 9
        self.ProficiencyBonusByCR["30"] = 9

    def CreateStats(self):
        # Common Character Stats
        super().CreateStats()

        # NPC Name
        self.Stats["NPC Name"] = ""

        # Size
        self.Stats["Size"] = ""

        # Type and Tags
        self.Stats["Type and Tags"] = ""

        # Alignment
        self.Stats["Alignment"] = ""

        # AC
        self.Stats["AC"] = ""

        # CR
        self.Stats["CR"] = "0"

        # Experience
        self.Stats["Experience"] = ""

        # Ability Score Modifiers
        self.Stats["Ability Score Modifiers"] = {}
        self.Stats["Ability Score Modifiers"]["Strength"] = 0
        self.Stats["Ability Score Modifiers"]["Dexterity"] = 0
        self.Stats["Ability Score Modifiers"]["Constitution"] = 0
        self.Stats["Ability Score Modifiers"]["Intelligence"] = 0
        self.Stats["Ability Score Modifiers"]["Wisdom"] = 0
        self.Stats["Ability Score Modifiers"]["Charisma"] = 0

        # Skills, Senses, and Languages
        self.Stats["Skills, Senses, and Languages"] = ""

        # Special Traits
        self.Stats["Special Traits"] = ""

        # Actions
        self.Stats["Actions"] = ""

        # Saving Throws
        self.Stats["Saving Throws"] = ""

        # Vulnerabilities, Resistances, and Immunities
        self.Stats["Vulnerabilities, Resistances, and Immunities"] = ""

        # Inventory
        self.Stats["Inventory"] = ""

        # Reactions
        self.Stats["Reactions"] = ""

        # Legendary Actions and Lair Actions
        self.Stats["Legendary Actions and Lair Actions"] = ""

        # Notes
        self.Stats["Notes"] = ""

        # Dice Roller
        self.Stats["Dice Roller"] = DiceRoller(Character=self)

        # Crit Minimum
        self.Stats["Crit Minimum"] = 20

    def UpdateStat(self, Stat, NewValue):
        # Update Common Stats
        if super().UpdateStat(Stat, NewValue):
            return True

        if Stat in [
            "NPC Name",
            "Size",
            "Type and Tags",
            "Alignment",
            "AC",
            "CR",
            "Experience",
            "Skills, Senses, and Languages",
            "Special Traits",
            "Actions",
            "Saving Throws",
            "Vulnerabilities, Resistances, and Immunities",
            "Inventory",
            "Reactions",
            "Legendary Actions and Lair Actions",
            "Notes",
            "Crit Minimum"
        ]:
            self.Stats[Stat] = NewValue
            return True
        elif type(Stat) is tuple:
            if len(Stat) == 2:
                self.Stats[Stat[0]][Stat[1]] = NewValue
                return True

        return False

    def GetDerivedStats(self):
        # Common Derived Stats
        DerivedStats = super().GetDerivedStats()

        # Proficiency
        DerivedStats["Proficiency Bonus"] = self.CalculateProficiencyBonus()

    # Stat Calculation Methods
    def CalculateProficiencyBonus(self):
        return self.ProficiencyBonusByCR[self.Stats["CR"]]

    def CreateStatModifier(self):
        StatModifier = {}
        for Ability in self.Abilities:
            StatModifier[Ability + " Multiplier"] = 0
            StatModifier[Ability + " Multiplier Round Up"] = False
            StatModifier[Ability + " Min"] = None
            StatModifier[Ability + " Max"] = None
        StatModifier["Proficiency Multiplier"] = 0
        StatModifier["Proficiency Multiplier Round Up"] = False
        StatModifier["Proficiency Min"] = None
        StatModifier["Proficiency Max"] = None
        StatModifier["CR Multiplier"] = 0
        StatModifier["CR Multiplier Round Up"] = False
        StatModifier["CR Min"] = None
        StatModifier["CR Max"] = None
        StatModifier["Manual Modifier"] = 0
        return StatModifier

    def CalculateStatModifier(self, StatModifier):
        CalculatedModifier = 0

        # Ability Modifiers
        for Ability in self.Abilities:
            AbilityMod = self.Stats["Ability Score Modifiers"][Ability] * StatModifier[Ability + " Multiplier"]
            if StatModifier[Ability + " Multiplier Round Up"]:
                AbilityMod = math.ceil(AbilityMod)
            else:
                AbilityMod = math.floor(AbilityMod)
            if StatModifier[Ability + " Max"] is not None:
                AbilityMod = min(AbilityMod, StatModifier[Ability + " Max"])
            if StatModifier[Ability + " Min"] is not None:
                AbilityMod = max(AbilityMod, StatModifier[Ability + " Min"])
            CalculatedModifier += AbilityMod

        # CR Modifier
        CRMod = self.Stats["CR"] * StatModifier["CR Multiplier"]
        if StatModifier["CR Multiplier Round Up"]:
            CRMod = math.ceil(CRMod)
        else:
            CRMod = math.floor(CRMod)
        if StatModifier["CR Max"] is not None:
            CRMod = min(CRMod, StatModifier["CR Max"])
        if StatModifier["CR Min"] is not None:
            CRMod = max(CRMod, StatModifier["CR Min"])
        CalculatedModifier += CRMod

        # Proficiency Modifier
        ProficiencyMod = self.CalculateProficiencyBonus() * StatModifier["Proficiency Multiplier"]
        if StatModifier["Proficiency Multiplier Round Up"]:
            ProficiencyMod = math.ceil(ProficiencyMod)
        else:
            ProficiencyMod = math.floor(ProficiencyMod)
        if StatModifier["Proficiency Max"] is not None:
            ProficiencyMod = min(ProficiencyMod, StatModifier["Proficiency Max"])
        if StatModifier["Proficiency Min"] is not None:
            ProficiencyMod = max(ProficiencyMod, StatModifier["Proficiency Min"])
        CalculatedModifier += ProficiencyMod

        # Manual Modifier
        CalculatedModifier += StatModifier["Manual Modifier"]

        # Return Calculated Modifier
        return CalculatedModifier

    # Serialization Methods
    def SetState(self, NewState):
        self.Stats = NewState["Stats"]

    def GetState(self):
        State = {}
        State["Stats"] = self.Stats
        return State

    @classmethod
    def CreateFromState(cls, State):
        NewNonPlayerCharacter = cls()
        NewNonPlayerCharacter.SetState(State)
        return NewNonPlayerCharacter
