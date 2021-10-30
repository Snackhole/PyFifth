import math


class Character:
    def __init__(self):
        self.CreateStaticValues()
        self.CreateStats()

    def CreateStaticValues(self):
        # Abilities
        self.Abilities = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

        # Level-Derived Values
        self.LevelDerivedValues = {}
        self.LevelDerivedValues["1"] = {"Proficiency Bonus": 2, "Experience Needed": 300}
        self.LevelDerivedValues["2"] = {"Proficiency Bonus": 2, "Experience Needed": 900}
        self.LevelDerivedValues["3"] = {"Proficiency Bonus": 2, "Experience Needed": 2700}
        self.LevelDerivedValues["4"] = {"Proficiency Bonus": 2, "Experience Needed": 6500}
        self.LevelDerivedValues["5"] = {"Proficiency Bonus": 3, "Experience Needed": 14000}
        self.LevelDerivedValues["6"] = {"Proficiency Bonus": 3, "Experience Needed": 23000}
        self.LevelDerivedValues["7"] = {"Proficiency Bonus": 3, "Experience Needed": 34000}
        self.LevelDerivedValues["8"] = {"Proficiency Bonus": 3, "Experience Needed": 48000}
        self.LevelDerivedValues["9"] = {"Proficiency Bonus": 4, "Experience Needed": 64000}
        self.LevelDerivedValues["10"] = {"Proficiency Bonus": 4, "Experience Needed": 85000}
        self.LevelDerivedValues["11"] = {"Proficiency Bonus": 4, "Experience Needed": 100000}
        self.LevelDerivedValues["12"] = {"Proficiency Bonus": 4, "Experience Needed": 120000}
        self.LevelDerivedValues["13"] = {"Proficiency Bonus": 5, "Experience Needed": 140000}
        self.LevelDerivedValues["14"] = {"Proficiency Bonus": 5, "Experience Needed": 165000}
        self.LevelDerivedValues["15"] = {"Proficiency Bonus": 5, "Experience Needed": 195000}
        self.LevelDerivedValues["16"] = {"Proficiency Bonus": 5, "Experience Needed": 225000}
        self.LevelDerivedValues["17"] = {"Proficiency Bonus": 6, "Experience Needed": 265000}
        self.LevelDerivedValues["18"] = {"Proficiency Bonus": 6, "Experience Needed": 305000}
        self.LevelDerivedValues["19"] = {"Proficiency Bonus": 6, "Experience Needed": 355000}
        self.LevelDerivedValues["20"] = {"Proficiency Bonus": 6, "Experience Needed": "N/A"}

    def CreateStats(self):
        # Stats Dictionary
        self.Stats = {}

        # Level
        self.Stats["Level"] = 1

        # Ability Scores
        self.Stats["Ability Scores"] = {}
        for Ability in self.Abilities:
            self.Stats["Ability Scores"][Ability] = 8
            self.Stats["Ability Scores"][Ability + " Save Proficiency"] = False
            self.Stats["Ability Scores"][Ability + " Stat Modifier"] = self.CreateStatModifier()
            self.Stats["Ability Scores"][Ability + " Save Stat Modifier"] = self.CreateStatModifier()

        # AC
        self.Stats["AC Stat Modifier"] = self.CreateStatModifier(ACMode=True)

    def GetDerivedStats(self):
        # Derived Stats Dictionary
        DerivedStats = {}

        # Proficiency and Experience Needed
        DerivedStats["Proficiency Modifier"] = self.LevelDerivedValues[str(self.Stats["Level"])]["Proficiency Bonus"]
        DerivedStats["Experience Needed"] = self.LevelDerivedValues[str(self.Stats["Level"])]["Experience Needed"]

        # Ability and Saving Throw Modifiers
        for Ability in self.Abilities:
            Mods = self.CalculateAbilityModifiers(Ability, DerivedStats)
            DerivedStats[Ability + " Modifier"] = Mods["Ability Modifier"]
            DerivedStats[Ability + " Saving Throw Modifier"] = Mods["Save Modifier"]

        # AC
        DerivedStats["AC"] = self.CalculateStatModifier(self.Stats["AC Stat Modifier"])

        # Return Derived Stats Dictionary
        return DerivedStats

    def CalculateAbilityModifiers(self, Ability, DerivedStats):
        # Variables
        AbilityScore = self.Stats["Ability Scores"][Ability]
        ProficiencyModifier = DerivedStats["Proficiency Modifier"]
        SaveProficiency = self.Stats["Ability Scores"][Ability + " Save Proficiency"]

        # Calculate Mods
        BaseAbilityModifier = self.GetBaseAbilityModifier(AbilityScore)
        CalculatedAbilityStatModifier = self.CalculateStatModifier(self.Stats["Ability Scores"][Ability + " Stat Modifier"])
        CalculatedSaveStatModifier = self.CalculateStatModifier(self.Stats["Ability Scores"][Ability + " Save Stat Modifier"])
        AbilityModifier = BaseAbilityModifier + CalculatedAbilityStatModifier
        SaveModifier = BaseAbilityModifier + CalculatedSaveStatModifier + (ProficiencyModifier if SaveProficiency else 0)

        # Return Mods
        Mods = {}
        Mods["Ability Modifier"] = AbilityModifier
        Mods["Save Modifier"] = SaveModifier
        return Mods

    def CreateStatModifier(self, ACMode=False):
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
        StatModifier["Level Multiplier"] = 0
        StatModifier["Level Multiplier Round Up"] = False
        StatModifier["Level Min"] = None
        StatModifier["Level Max"] = None
        StatModifier["Manual Modifier"] = 0
        if ACMode:
            StatModifier["AC Base"] = 0
        return StatModifier

    def CalculateStatModifier(self, StatModifier):
        CalculatedModifier = 0

        # Ability, Proficiency, and Level Stat Modifiers
        for Stat in (self.Abilities + ["Proficiency", "Level"]):
            StatMod = self.GetBaseAbilityModifier(self.Stats["Ability Scores"][Stat]) * StatModifier[Stat + " Multiplier"]
            if StatModifier[Stat + " Multiplier Round Up"]:
                StatMod = math.ceil(StatMod)
            else:
                StatMod = math.floor(StatMod)
            if StatModifier[Stat + " Max"] is not None:
                StatMod = min(StatMod, StatModifier[Stat + " Max"])
            if StatModifier[Stat + " Min"] is not None:
                StatMod = max(StatMod, StatModifier[Stat + " Min"])
            CalculatedModifier += StatMod

        # Manual Modifier
        CalculatedModifier += StatModifier["Manual Modifier"]

        # AC
        if "AC Base" in StatModifier:
            CalculatedModifier += StatModifier["AC Base"]

        # Return Calculated Modifier
        return CalculatedModifier

    def GetBaseAbilityModifier(self, AbilityScore):
        return math.floor((AbilityScore - 10) / 2)
