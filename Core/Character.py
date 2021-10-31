import math


class Character:
    def __init__(self):
        self.CreateStaticValues()
        self.CreateStats()

    def CreateStaticValues(self):
        # Abilities
        self.Abilities = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

        # Skills
        self.Skills = ["Acrobatics", "Animal Handling", "Arcana", "Athletics", "Deception", "History", "Insight", "Intimidation", "Investigation", "Medicine", "Nature", "Perception", "Performance", "Persuasion", "Religion", "Sleight of Hand", "Stealth", "Survival"]
        self.SkillsAssociatedAbilities = {}
        self.SkillsAssociatedAbilities["Acrobatics"] = "Dexterity"
        self.SkillsAssociatedAbilities["Animal Handling"] = "Wisdom"
        self.SkillsAssociatedAbilities["Arcana"] = "Intelligence"
        self.SkillsAssociatedAbilities["Athletics"] = "Strength"
        self.SkillsAssociatedAbilities["Deception"] = "Charisma"
        self.SkillsAssociatedAbilities["History"] = "Intelligence"
        self.SkillsAssociatedAbilities["Insight"] = "Wisdom"
        self.SkillsAssociatedAbilities["Intimidation"] = "Charisma"
        self.SkillsAssociatedAbilities["Investigation"] = "Intelligence"
        self.SkillsAssociatedAbilities["Medicine"] = "Wisdom"
        self.SkillsAssociatedAbilities["Nature"] = "Intelligence"
        self.SkillsAssociatedAbilities["Perception"] = "Wisdom"
        self.SkillsAssociatedAbilities["Performance"] = "Charisma"
        self.SkillsAssociatedAbilities["Persuasion"] = "Charisma"
        self.SkillsAssociatedAbilities["Religion"] = "Intelligence"
        self.SkillsAssociatedAbilities["Sleight of Hand"] = "Dexterity"
        self.SkillsAssociatedAbilities["Stealth"] = "Dexterity"
        self.SkillsAssociatedAbilities["Survival"] = "Wisdom"

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

        # Character Name
        self.Stats["Character Name"] = ""

        # Character Class
        self.Stats["Character Class"] = ""

        # Level
        self.Stats["Level"] = 1

        # Character Experience Earned
        self.Stats["Character Experience Earned"] = 0

        # Player Name
        self.Stats["Player Name"] = ""

        # Ability Scores
        self.Stats["Ability Scores"] = {}
        for Ability in self.Abilities:
            self.Stats["Ability Scores"][Ability] = 8
            self.Stats["Ability Scores"][Ability + " Stat Modifier"] = self.CreateStatModifier()
            self.Stats["Ability Scores"][Ability + " Save Stat Modifier"] = self.CreateStatModifier()

        # Ability Score Derivatives
        self.Stats["Ability Score Derivatives"] = {}
        for Ability in self.Abilities:
            self.Stats["Ability Score Derivatives"][Ability + " Attack Modifier Stat Modifier"] = self.CreateStatModifier()
            self.Stats["Ability Score Derivatives"][Ability + " Attack Modifier Stat Modifier"][Ability + " Multiplier"] = 1
            self.Stats["Ability Score Derivatives"][Ability + " Attack Modifier Stat Modifier"]["Proficiency Multiplier"] = 1
            self.Stats["Ability Score Derivatives"][Ability + " Save DC Stat Modifier"] = self.CreateStatModifier()
            self.Stats["Ability Score Derivatives"][Ability + " Save DC Stat Modifier"][Ability + " Multiplier"] = 1
            self.Stats["Ability Score Derivatives"][Ability + " Save DC Stat Modifier"]["Proficency Multiplier"] = 1
            self.Stats["Ability Score Derivatives"][Ability + " Save DC Stat Modifier"]["Manual Modifier"] = 8

        # Skills
        self.Stats["Skills"] = {}
        for Skill in self.Skills:
            self.Stats["Skills"][Skill + " Stat Modifier"] = self.CreateStatModifier()
            AssociatedAbility = self.SkillsAssociatedAbilities[Skill]
            self.Stats["Skills"][Skill + " Stat Modifier"][AssociatedAbility + " Multiplier"] = 1
        self.Stats["Skills"]["Passive Perception Stat Modifier"] = self.CreateStatModifier()
        self.Stats["Skills"]["Passive Investigation Stat Modifier"] = self.CreateStatModifier()

        # AC
        self.Stats["AC Stat Modifier 1"] = self.CreateStatModifier(ACMode=True)
        self.Stats["AC Stat Modifier 2"] = self.CreateStatModifier(ACMode=True)
        self.Stats["AC Stat Modifier 3"] = self.CreateStatModifier(ACMode=True)

        # Current Health
        self.Stats["Current Health"] = 0

        # Max Health
        self.Stats["Max Health Per Level"] = {}
        self.Stats["Max Health Per Level"]["1"] = 0
        self.Stats["Max Health Per Level"]["2"] = 0
        self.Stats["Max Health Per Level"]["3"] = 0
        self.Stats["Max Health Per Level"]["4"] = 0
        self.Stats["Max Health Per Level"]["5"] = 0
        self.Stats["Max Health Per Level"]["6"] = 0
        self.Stats["Max Health Per Level"]["7"] = 0
        self.Stats["Max Health Per Level"]["8"] = 0
        self.Stats["Max Health Per Level"]["9"] = 0
        self.Stats["Max Health Per Level"]["10"] = 0
        self.Stats["Max Health Per Level"]["11"] = 0
        self.Stats["Max Health Per Level"]["12"] = 0
        self.Stats["Max Health Per Level"]["13"] = 0
        self.Stats["Max Health Per Level"]["14"] = 0
        self.Stats["Max Health Per Level"]["15"] = 0
        self.Stats["Max Health Per Level"]["16"] = 0
        self.Stats["Max Health Per Level"]["17"] = 0
        self.Stats["Max Health Per Level"]["18"] = 0
        self.Stats["Max Health Per Level"]["19"] = 0
        self.Stats["Max Health Per Level"]["20"] = 0
        self.Stats["Bonus Max Health Per Level"] = 0
        self.Stats["Max Health Override"] = None

        # Temp Health
        self.Stats["Temp Health"] = 0

        # Initiative Stat Modifier
        self.Stats["Initiative Stat Modifier"] = self.CreateStatModifier()
        self.Stats["Initiative Stat Modifier"]["Dexterity Multiplier"] = 1

        # Spellcasting Enabled
        self.Stats["Spellcasting Enabled"] = True

        # Concentrating
        self.Stats["Concentrating"] = True

        # Portrait
        self.Stats["Portrait"] = None
        self.Stats["Portrait Enabled"] = True

        # Stat Calculation Features
        self.Stats["Jack Of All Trades"] = False
        self.Stats["Remarkable Athlete"] = False
        self.Stats["Observant"] = False
        self.Stats["Lucky Halfling"] = False

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

        # Skill Modifiers
        for Skill in self.Skills:
            DerivedStats[Skill + " Modifier"] = self.CalculateStatModifier(self.Stats["Skills"][Skill + " Stat Modifier"])

        # Passive Perception and Investigation
        if self.Stats["Observant"]:
            ObservantBonus = 5
        else:
            ObservantBonus = 0
        DerivedStats["Passive Perception"] = 10 + DerivedStats["Perception Modifier"] + self.CalculateStatModifier(self.Stats["Skills"]["Passive Perception Stat Modifier"]) + ObservantBonus
        DerivedStats["Passive Investigation"] = 10 + DerivedStats["Investigation Modifier"] + self.CalculateStatModifier(self.Stats["Skills"]["Passive Investigation Stat Modifier"]) + ObservantBonus

        # AC
        DerivedStats["AC 1"] = self.CalculateStatModifier(self.Stats["AC Stat Modifier 1"])
        DerivedStats["AC 2"] = self.CalculateStatModifier(self.Stats["AC Stat Modifier 2"])
        DerivedStats["AC 3"] = self.CalculateStatModifier(self.Stats["AC Stat Modifier 3"])

        # Health
        if self.Stats["Max Health Override"] is not None:
            DerivedStats["Max Health"] = self.Stats["Max Health Override"]
        else:
            MaxHealth = 0
            for Level in range(1, self.Stats["Level"] + 1):
                MaxHealth += self.Stats["Max Health Per Level"][str(Level)]
            MaxHealth += (DerivedStats["Constitution Modifier"] + self.Stats["Bonus Max Health Per Level"]) * self.Stats["Level"]
            DerivedStats["Max Health"] = MaxHealth

        # Initiative
        DerivedStats["Initiative Modifier"] = self.CalculateStatModifier(self.Stats["Initiative Stat Modifier"])

        # Ability Score Derivatives
        for Ability in self.Abilities:
            DerivedStats[Ability + " Attack Modifier Stat Modifier"] = self.CalculateStatModifier(self.Stats["Ability Score Derivatives"][Ability + " Attack Modifier Stat Modifier"])
            DerivedStats[Ability + " Save DC Stat Modifier"] = self.CalculateStatModifier(self.Stats["Ability Score Derivatives"][Ability + " Save DC Stat Modifier"])

        # Return Derived Stats Dictionary
        return DerivedStats

    def CalculateAbilityModifiers(self, Ability):
        # Ability Score
        AbilityScore = self.Stats["Ability Scores"][Ability]

        # Calculate Mods
        BaseAbilityModifier = self.GetBaseAbilityModifier(AbilityScore)
        CalculatedAbilityStatModifier = self.CalculateStatModifier(self.Stats["Ability Scores"][Ability + " Stat Modifier"])
        CalculatedSaveStatModifier = self.CalculateStatModifier(self.Stats["Ability Scores"][Ability + " Save Stat Modifier"])
        AbilityModifier = BaseAbilityModifier + CalculatedAbilityStatModifier
        SaveModifier = BaseAbilityModifier + CalculatedSaveStatModifier

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
