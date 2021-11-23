import math
from decimal import *

from Core.Character import Character
from Core.DiceRoller import DiceRoller
from SaveAndLoad.JSONSerializer import SerializableMixin


class PlayerCharacter(Character, SerializableMixin):
    def __init__(self):
        # Initialize Character and SerializableMixin
        super().__init__()

        # Create Static Values
        self.CreateStaticValues()

        # Create Stats
        self.CreateStats()

    def CreateStaticValues(self):
        # Common Static Values
        super().CreateStaticValues()

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

        # Spell Slot Levels
        self.SpellSlotLevels = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th"]

        # Spell Point Values
        self.SpellPointValues = {}
        self.SpellPointValues["1st"] = 2
        self.SpellPointValues["2nd"] = 3
        self.SpellPointValues["3rd"] = 5
        self.SpellPointValues["4th"] = 6
        self.SpellPointValues["5th"] = 7
        self.SpellPointValues["6th"] = 9
        self.SpellPointValues["7th"] = 10
        self.SpellPointValues["8th"] = 11
        self.SpellPointValues["9th"] = 13

        # Coin Values
        self.CoinValues = {}
        self.CoinValues["CP"] = Decimal(0.01)
        self.CoinValues["SP"] = Decimal(0.1)
        self.CoinValues["EP"] = Decimal(0.5)
        self.CoinValues["GP"] = Decimal(1)
        self.CoinValues["PP"] = Decimal(10)

        # Weight Per Coin
        self.WeightPerCoin = Decimal(0.02)

        # Coin Values in CP
        self.CoinValuesInCP = {}
        self.CoinValuesInCP["CPValueInCP"] = Decimal(1)
        self.CoinValuesInCP["SPValueInCP"] = Decimal(10)
        self.CoinValuesInCP["EPValueInCP"] = Decimal(50)
        self.CoinValuesInCP["GPValueInCP"] = Decimal(100)
        self.CoinValuesInCP["PPValueInCP"] = Decimal(1000)

        # Point Buy Costs
        self.PointBuyCosts = {}
        self.PointBuyCosts[8] = 0
        self.PointBuyCosts[9] = 1
        self.PointBuyCosts[10] = 2
        self.PointBuyCosts[11] = 3
        self.PointBuyCosts[12] = 4
        self.PointBuyCosts[13] = 5
        self.PointBuyCosts[14] = 7
        self.PointBuyCosts[15] = 9

    def CreateStats(self):
        # Common Character Stats
        super().CreateStats()

        # Character Name
        self.Stats["Character Name"] = ""

        # Character Race
        self.Stats["Character Race"] = ""

        # Character Background
        self.Stats["Character Background"] = ""

        # Character Alignment
        self.Stats["Character Alignment"] = ""

        # Character Age
        self.Stats["Character Age"] = ""

        # Character Physical Appearance
        self.Stats["Character Physical Appearance"] = ""

        # Character Personality Traits
        self.Stats["Character Personality Traits"] = ""

        # Character Bonds
        self.Stats["Character Bonds"] = ""

        # Character Ideals
        self.Stats["Character Ideals"] = ""

        # Character Flaws
        self.Stats["Character Flaws"] = ""

        # Character Backstory
        self.Stats["Character Backstory"] = ""

        # Character Class
        self.Stats["Character Class"] = ""

        # Level
        self.Stats["Character Level"] = 1

        # Character Experience Earned
        self.Stats["Character Experience Earned"] = 0

        # Player Name
        self.Stats["Player Name"] = ""

        # Inspiration
        self.Stats["Inspiration"] = False

        # Ability Scores
        self.Stats["Ability Scores"] = self.CreateAbilityScoresStats()

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
        self.Stats["Skills"] = self.CreateSkillsStats()

        # Proficiencies
        self.Stats["Weapons Proficiencies"] = ""
        self.Stats["Armor Proficiencies"] = ""
        self.Stats["Tools and Instruments Proficiencies"] = ""
        self.Stats["Languages Proficiencies"] = ""
        self.Stats["Other Proficiencies"] = ""

        # AC
        self.Stats["AC Stat Modifier 1"] = self.CreateStatModifier(ACMode=True)
        self.Stats["AC Stat Modifier 1"]["Base AC"] = 10
        self.Stats["AC Stat Modifier 1"]["Dexterity Multiplier"] = 1
        self.Stats["AC Stat Modifier 2"] = self.CreateStatModifier(ACMode=True)
        self.Stats["AC Stat Modifier 2"]["Base AC"] = 10
        self.Stats["AC Stat Modifier 2"]["Dexterity Multiplier"] = 1
        self.Stats["AC Stat Modifier 3"] = self.CreateStatModifier(ACMode=True)
        self.Stats["AC Stat Modifier 3"]["Base AC"] = 10
        self.Stats["AC Stat Modifier 3"]["Dexterity Multiplier"] = 1

        # Current Health
        self.Stats["Current Health"] = 5

        # Max Health
        self.Stats["Health"] = {}
        self.Stats["Health"]["Max Health Per Level"] = {}
        self.Stats["Health"]["Max Health Per Level"]["1"] = 6
        self.Stats["Health"]["Max Health Per Level"]["2"] = 1
        self.Stats["Health"]["Max Health Per Level"]["3"] = 1
        self.Stats["Health"]["Max Health Per Level"]["4"] = 1
        self.Stats["Health"]["Max Health Per Level"]["5"] = 1
        self.Stats["Health"]["Max Health Per Level"]["6"] = 1
        self.Stats["Health"]["Max Health Per Level"]["7"] = 1
        self.Stats["Health"]["Max Health Per Level"]["8"] = 1
        self.Stats["Health"]["Max Health Per Level"]["9"] = 1
        self.Stats["Health"]["Max Health Per Level"]["10"] = 1
        self.Stats["Health"]["Max Health Per Level"]["11"] = 1
        self.Stats["Health"]["Max Health Per Level"]["12"] = 1
        self.Stats["Health"]["Max Health Per Level"]["13"] = 1
        self.Stats["Health"]["Max Health Per Level"]["14"] = 1
        self.Stats["Health"]["Max Health Per Level"]["15"] = 1
        self.Stats["Health"]["Max Health Per Level"]["16"] = 1
        self.Stats["Health"]["Max Health Per Level"]["17"] = 1
        self.Stats["Health"]["Max Health Per Level"]["18"] = 1
        self.Stats["Health"]["Max Health Per Level"]["19"] = 1
        self.Stats["Health"]["Max Health Per Level"]["20"] = 1
        self.Stats["Health"]["Bonus Max Health Per Level"] = 0
        self.Stats["Health"]["Max Health Override"] = None

        # Hit Dice
        self.Stats["Total Hit Dice"] = ""
        self.Stats["Hit Dice Remaining"] = ""

        # Death Saving Throws
        self.Stats["Death Saving Throws"] = {}
        self.Stats["Death Saving Throws"]["Failure 1"] = False
        self.Stats["Death Saving Throws"]["Failure 2"] = False
        self.Stats["Death Saving Throws"]["Failure 3"] = False
        self.Stats["Death Saving Throws"]["Success 1"] = False
        self.Stats["Death Saving Throws"]["Success 2"] = False
        self.Stats["Death Saving Throws"]["Success 3"] = False

        # Initiative Stat Modifier
        self.Stats["Initiative Stat Modifier"] = self.CreateStatModifier()
        self.Stats["Initiative Stat Modifier"]["Dexterity Multiplier"] = 1

        # Combat and Features Notes
        self.Stats["Combat and Features Notes"] = ""

        # Features
        self.Stats["Features"] = []

        # Spellcasting Enabled
        self.Stats["Spellcasting Enabled"] = True

        # Spell Notes
        self.Stats["Spell Notes"] = ""

        # Spell Slots
        self.Stats["Spell Slots"] = {}
        for SpellSlotLevel in self.SpellSlotLevels:
            self.Stats["Spell Slots"][SpellSlotLevel] = {}
            self.Stats["Spell Slots"][SpellSlotLevel]["Current"] = 0
            self.Stats["Spell Slots"][SpellSlotLevel]["Max"] = 0

        # Spell Points
        self.Stats["Spell Points Enabled"] = False
        self.Stats["Current Spell Points"] = 0
        self.Stats["Spell Points Stat Modifier"] = self.CreateStatModifier()

        # Spell List
        self.Stats["Spell List"] = []

        # Carrying Capacity
        self.Stats["Carrying Capacity Stat Modifier"] = self.CreateStatModifier()

        # Inventory
        self.Stats["Inventory"] = []
        self.Stats["Coins"] = {}
        self.Stats["Coins"]["CP"] = 0
        self.Stats["Coins"]["SP"] = 0
        self.Stats["Coins"]["EP"] = 0
        self.Stats["Coins"]["GP"] = 0
        self.Stats["Coins"]["PP"] = 0

        # Supply Consumption Rates
        self.Stats["Food Consumption Rate"] = 1
        self.Stats["Water Consumption Rate"] = 8

        # Stat Calculation Features
        self.Stats["Lucky Halfling"] = False

        # Notes
        self.Stats["Notes 1"] = ""
        self.Stats["Notes 2"] = ""
        self.Stats["Additional Notes"] = []

        # Dice Roller
        self.Stats["Dice Roller"] = DiceRoller(Character=self)

        # Crit Minimum
        self.Stats["Crit Minimum"] = 20

    def UpdateStat(self, Stat, NewValue):
        # Update Common Stats
        if super().UpdateStat(Stat, NewValue):
            return True

        if Stat in [
            "Character Name",
            "Character Race",
            "Character Background",
            "Character Alignment",
            "Character Age",
            "Character Physical Appearance",
            "Character Personality Traits",
            "Character Bonds",
            "Character Ideals",
            "Character Flaws",
            "Character Backstory",
            "Character Class",
            "Character Level",
            "Character Experience Earned",
            "Player Name",
            "Inspiration",
            "Weapons Proficiencies",
            "Armor Proficiencies",
            "Tools and Instruments Proficiencies",
            "Languages Proficiencies",
            "Other Proficiencies",
            "Bonus Max Health Per Level",
            "Max Health Override",
            "Total Hit Dice",
            "Hit Dice Remaining",
            "Combat and Features Notes",
            "Spellcasting Enabled",
            "Spell Notes",
            "Spell Points Enabled",
            "Current Spell Points",
            "Food Consumption Rate",
            "Water Consumption Rate",
            "Lucky Halfling",
            "Notes 1",
            "Notes 2",
            "Crit Minimum"
        ]:
            self.Stats[Stat] = NewValue
            return True
        elif type(Stat) is tuple:
            if len(Stat) == 2:
                self.Stats[Stat[0]][Stat[1]] = NewValue
                return True

        return False

    def CreateAbilityScoresStats(self):
        AbilityScores = {}
        for Ability in self.Abilities:
            AbilityScores[Ability + " Base"] = 8
            AbilityScores[Ability + " Racial"] = 0
            AbilityScores[Ability + " ASI"] = 0
            AbilityScores[Ability + " Miscellaneous"] = 0
            AbilityScores[Ability + " Override"] = None
            AbilityScores[Ability + " Stat Modifier"] = self.CreateStatModifier()
            AbilityScores[Ability + " Stat Modifier"][Ability + " Multiplier"] = 1
            AbilityScores[Ability + " Save Stat Modifier"] = self.CreateStatModifier()
            AbilityScores[Ability + " Save Stat Modifier"][Ability + " Multiplier"] = 1
        AbilityScores["Ability Score Notes"] = ""
        return AbilityScores

    def CreateSkillsStats(self):
        Skills = {}
        for Skill in self.Skills:
            Skills[Skill + " Stat Modifier"] = self.CreateStatModifier()
            AssociatedAbility = self.SkillsAssociatedAbilities[Skill]
            Skills[Skill + " Stat Modifier"][AssociatedAbility + " Multiplier"] = 1
        Skills["Passive Perception Stat Modifier"] = self.CreateStatModifier()
        Skills["Passive Perception Stat Modifier"]["Manual Modifier"] = 10
        Skills["Passive Perception Stat Modifier"]["Wisdom Multiplier"] = 1
        Skills["Passive Investigation Stat Modifier"] = self.CreateStatModifier()
        Skills["Passive Investigation Stat Modifier"]["Manual Modifier"] = 10
        Skills["Passive Investigation Stat Modifier"]["Intelligence Multiplier"] = 1
        return Skills

    def GetDerivedStats(self):
        # Common Derived Stats
        DerivedStats = super().GetDerivedStats()

        # Proficiency
        DerivedStats["Proficiency Bonus"] = self.CalculateProficiencyBonus()

        # Experience Needed
        DerivedStats["Experience Needed"] = self.LevelDerivedValues[str(self.Stats["Character Level"])]["Experience Needed"]

        # Ability and Saving Throw Modifiers
        for Ability in self.Abilities:
            TotalAbilityScore = self.GetTotalAbilityScore(Ability)
            DerivedStats[Ability + " Total Score"] = TotalAbilityScore
            DerivedStats[Ability + " Modifier"] = self.CalculateStatModifier(self.Stats["Ability Scores"][Ability + " Stat Modifier"])
            DerivedStats[Ability + " Saving Throw Modifier"] = self.CalculateStatModifier(self.Stats["Ability Scores"][Ability + " Save Stat Modifier"])

        # Skill Modifiers
        for Skill in self.Skills:
            DerivedStats[Skill + " Modifier"] = self.CalculateStatModifier(self.Stats["Skills"][Skill + " Stat Modifier"])

        # Passive Perception and Investigation
        DerivedStats["Passive Perception"] = self.CalculateStatModifier(self.Stats["Skills"]["Passive Perception Stat Modifier"])
        DerivedStats["Passive Investigation"] = self.CalculateStatModifier(self.Stats["Skills"]["Passive Investigation Stat Modifier"])

        # AC
        DerivedStats["AC 1"] = self.CalculateStatModifier(self.Stats["AC Stat Modifier 1"])
        DerivedStats["AC 2"] = self.CalculateStatModifier(self.Stats["AC Stat Modifier 2"])
        DerivedStats["AC 3"] = self.CalculateStatModifier(self.Stats["AC Stat Modifier 3"])

        # Health
        DerivedStats["Max Health"] = self.CalculateMaxHealth()

        # Initiative
        DerivedStats["Initiative Modifier"] = self.CalculateStatModifier(self.Stats["Initiative Stat Modifier"])

        # Ability Score Derivatives
        for Ability in self.Abilities:
            DerivedStats[Ability + " Attack Modifier Stat Modifier"] = self.CalculateStatModifier(self.Stats["Ability Score Derivatives"][Ability + " Attack Modifier Stat Modifier"])
            DerivedStats[Ability + " Save DC Stat Modifier"] = self.CalculateStatModifier(self.Stats["Ability Score Derivatives"][Ability + " Save DC Stat Modifier"])

        # Spell Points
        if self.Stats["Spell Points Enabled"]:
            DerivedStats["Max Spell Points"] = self.CalculateSpellPoints()
        else:
            DerivedStats["Max Spell Points"] = None

        # Carrying Capacity
        DerivedStats["Carrying Capacity"] = (15 * DerivedStats["Strength Total Score"]) + self.CalculateStatModifier(self.Stats["Carrying Capacity Stat Modifier"])

        # Coin Counts
        CPCount = Decimal(self.Stats["Coins"]["CP"])
        SPCount = Decimal(self.Stats["Coins"]["SP"])
        EPCount = Decimal(self.Stats["Coins"]["EP"])
        GPCount = Decimal(self.Stats["Coins"]["GP"])
        PPCount = Decimal(self.Stats["Coins"]["PP"])
        TotalCoinCount = CPCount + SPCount + EPCount + GPCount + PPCount

        # Coin Value
        CoinValue = Decimal(0)
        CoinValue += CPCount * self.CoinValues["CP"]
        CoinValue += SPCount * self.CoinValues["SP"]
        CoinValue += EPCount * self.CoinValues["EP"]
        CoinValue += GPCount * self.CoinValues["GP"]
        CoinValue += PPCount * self.CoinValues["PP"]
        DerivedStats["Value of Coins"] = CoinValue.quantize(Decimal("0.01"))

        # Coin Weight
        CoinWeight = TotalCoinCount * self.WeightPerCoin
        DerivedStats["Weight of Coins"] = CoinWeight.quantize(Decimal("0.01"))

        # Loads and Values
        Loads = {}
        Loads["Total"] = Decimal(0)
        Loads["Gear"] = Decimal(0)
        Loads["Food"] = Decimal(0)
        Loads["Water"] = Decimal(0)
        Loads["Treasure"] = Decimal(0)
        Loads["Misc."] = Decimal(0)
        Loads[""] = Decimal(0)

        Values = {}
        Values["Total"] = Decimal(0)
        Values["Gear"] = Decimal(0)
        Values["Food"] = Decimal(0)
        Values["Water"] = Decimal(0)
        Values["Treasure"] = Decimal(0)
        Values["Misc."] = Decimal(0)
        Values[""] = Decimal(0)

        # Add Coins to Loads and Values
        Loads["Total"] += CoinWeight
        Loads["Treasure"] += CoinWeight
        Values["Total"] += CoinValue
        Values["Treasure"] += CoinValue

        # Update Loads and Values from Inventory Items
        for ItemIndex in range(0, len(self.Stats["Inventory"])):
            # Per-Item Variables
            Item = self.Stats["Inventory"][ItemIndex]
            Tag = Item["Item Category Tag"]

            # Total Weight and Value
            TotalWeightAndValue = self.CalculateItemTotalWeightAndValue(ItemIndex)
            TotalItemWeight = TotalWeightAndValue["Item Total Weight"]
            TotalItemValue = TotalWeightAndValue["Item Total Value"]

            # Totals
            Loads["Total"] += TotalItemWeight
            Values["Total"] += TotalItemValue

            # Tags
            Loads[Tag] += TotalItemWeight
            Values[Tag] += TotalItemValue

        # Quantize Loads and Values
        Loads["Total"] = Loads["Total"].quantize(Decimal("0.01"))
        Loads["Gear"] = Loads["Gear"].quantize(Decimal("0.01"))
        Loads["Food"] = Loads["Food"].quantize(Decimal("0.01"))
        Loads["Water"] = Loads["Water"].quantize(Decimal("0.01"))
        Loads["Treasure"] = Loads["Treasure"].quantize(Decimal("0.01"))
        Loads["Misc."] = Loads["Misc."].quantize(Decimal("0.01"))
        Loads[""] = Loads[""].quantize(Decimal("0.01"))

        Values["Total"] = Values["Total"].quantize(Decimal("0.01"))
        Values["Gear"] = Values["Gear"].quantize(Decimal("0.01"))
        Values["Food"] = Values["Food"].quantize(Decimal("0.01"))
        Values["Water"] = Values["Water"].quantize(Decimal("0.01"))
        Values["Treasure"] = Values["Treasure"].quantize(Decimal("0.01"))
        Values["Misc."] = Values["Misc."].quantize(Decimal("0.01"))
        Values[""] = Values[""].quantize(Decimal("0.01"))

        # Add Loads and Values to Derived Stats
        DerivedStats["Item Loads"] = Loads
        DerivedStats["Item Values"] = Values

        # Calculate Supply Days
        FoodRate = Decimal(self.Stats["Food Consumption Rate"])
        WaterRate = Decimal(self.Stats["Water Consumption Rate"])
        if FoodRate > Decimal(0):
            FoodDays = (Loads["Food"] / FoodRate).quantize(Decimal("0.01"))
        else:
            FoodDays = None
        if WaterRate > Decimal(0):
            WaterDays = (Loads["Water"] / WaterRate).quantize(Decimal("0.01"))
        else:
            WaterDays = None
        DerivedStats["Days of Food"] = FoodDays
        DerivedStats["Days of Water"] = WaterDays

        # Return Derived Stats Dictionary
        return DerivedStats

    # Stat Calculation Methods
    def CalculateProficiencyBonus(self):
        return self.LevelDerivedValues[str(self.Stats["Character Level"])]["Proficiency Bonus"]

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
            StatModifier["Base AC"] = 0
        return StatModifier

    def CalculateStatModifier(self, StatModifier):
        CalculatedModifier = 0

        # Ability Modifiers
        for Ability in self.Abilities:
            AbilityMod = math.floor((self.GetTotalAbilityScore(Ability) - 10) / 2) * StatModifier[Ability + " Multiplier"]
            if StatModifier[Ability + " Multiplier Round Up"]:
                AbilityMod = math.ceil(AbilityMod)
            else:
                AbilityMod = math.floor(AbilityMod)
            if StatModifier[Ability + " Max"] is not None:
                AbilityMod = min(AbilityMod, StatModifier[Ability + " Max"])
            if StatModifier[Ability + " Min"] is not None:
                AbilityMod = max(AbilityMod, StatModifier[Ability + " Min"])
            CalculatedModifier += AbilityMod

        # Level Modifier
        LevelMod = self.Stats["Character Level"] * StatModifier["Level Multiplier"]
        if StatModifier["Level Multiplier Round Up"]:
            LevelMod = math.ceil(LevelMod)
        else:
            LevelMod = math.floor(LevelMod)
        if StatModifier["Level Max"] is not None:
            LevelMod = min(LevelMod, StatModifier["Level Max"])
        if StatModifier["Level Min"] is not None:
            LevelMod = max(LevelMod, StatModifier["Level Min"])
        CalculatedModifier += LevelMod

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

        # AC
        if "Base AC" in StatModifier:
            CalculatedModifier += StatModifier["Base AC"]

        # Return Calculated Modifier
        return CalculatedModifier

    def GetTotalAbilityScore(self, Ability):
        TotalAbilityScore = self.Stats["Ability Scores"][Ability + " Base"]
        TotalAbilityScore += self.Stats["Ability Scores"][Ability + " Racial"]
        TotalAbilityScore += self.Stats["Ability Scores"][Ability + " ASI"]
        TotalAbilityScore += self.Stats["Ability Scores"][Ability + " Miscellaneous"]
        if self.Stats["Ability Scores"][Ability + " Override"] is not None:
            TotalAbilityScore = self.Stats["Ability Scores"][Ability + " Override"]
        return TotalAbilityScore

    def GetRolledAbilityScores(self):
        RolledScores = []
        for RolledScore in range(6):
            CurrentRolls = []
            for CurrentRoll in range(4):
                Results = self.Stats["Dice Roller"].RollDice(1, 6, 0, SkipLogging=True)
                CurrentRolls.append(Results["Total"])
            CurrentRolls.remove(min(CurrentRolls))
            RolledScores.append(sum(CurrentRolls))
        return RolledScores

    def CalculatePointBuyPointsRemaining(self, Scores):
        PointsRemaining = 27
        for Score in Scores:
            PointsRemaining -= self.PointBuyCosts[Score]
        return PointsRemaining

    def CalculateMaxHealth(self):
        if self.Stats["Health"]["Max Health Override"] is not None:
            MaxHealth = self.Stats["Health"]["Max Health Override"]
        else:
            ConstitutionModifier = self.CalculateStatModifier(self.Stats["Ability Scores"]["Constitution Stat Modifier"])
            MaxHealth = 0
            for Level in range(1, self.Stats["Character Level"] + 1):
                MaxHealth += max(self.Stats["Health"]["Max Health Per Level"][str(Level)] + ConstitutionModifier + self.Stats["Health"]["Bonus Max Health Per Level"], 1)
        return MaxHealth

    # Combat Methods
    def RollInitiative(self):
        self.Stats["Dice Roller"].RollDice(1, 20, self.Stats["Initiative Stat Modifier"], LogPrefix="Initiative:\n")

    # Feature Methods
    def AddFeature(self, FeatureName, FeatureText):
        NewFeature = {}
        NewFeature["Feature Name"] = FeatureName
        NewFeature["Feature Text"] = FeatureText
        self.Stats["Features"].append(NewFeature)

    def EditFeature(self, FeatureIndex, FeatureName, FeatureText):
        Feature = self.Stats["Features"][FeatureIndex]
        Feature["Feature Name"] = FeatureName
        Feature["Feature Text"] = FeatureText

    def DeleteFeature(self, FeatureIndex):
        del self.Stats["Features"][FeatureIndex]

    def MoveFeature(self, FeatureIndex, Delta):
        TargetIndex = FeatureIndex + Delta
        if TargetIndex < 0 or TargetIndex >= len(self.Stats["Features"]):
            return
        SwapTarget = self.Stats["Features"][TargetIndex]
        self.Stats["Features"][TargetIndex] = self.Stats["Features"][FeatureIndex]
        self.Stats["Features"][FeatureIndex] = SwapTarget

    # Spellcasting Methods
    def CalculateSpellPoints(self):
        TotalPoints = 0
        for SpellSlotLevel in self.SpellSlotLevels:
            TotalPoints += self.Stats["Spell Slots"][SpellSlotLevel]["Max"] * self.SpellPointValues[SpellSlotLevel]
        TotalPoints += self.CalculateStatModifier(self.Stats["Spell Points Stat Modifier"])
        return TotalPoints

    def ExpendSpellPoints(self, SpellSlotLevel, SpellSlotAmount, ManualSpellPointsAmount):
        if not self.Stats["Spell Points Enabled"]:
            return None
        CurrentSpellPoints = self.Stats["Current Spell Points"]
        ExpendedPoints = 0
        if SpellSlotLevel != "None" and SpellSlotAmount > 0:
            ExpendedPoints += SpellSlotAmount * self.SpellPointValues[SpellSlotLevel]
        if ManualSpellPointsAmount > 0:
            ExpendedPoints += ManualSpellPointsAmount
        self.Stats["Current Spell Points"] = max(0, CurrentSpellPoints - ExpendedPoints)

    def RestoreSpellPoints(self, SpellSlotLevel, SpellSlotAmount, ManualSpellPointsAmount):
        if not self.Stats["Spell Points Enabled"]:
            return None
        CurrentSpellPoints = self.Stats["Current Spell Points"]
        MaxSpellPoints = self.CalculateSpellPoints()
        RestoredPoints = 0
        if SpellSlotLevel != "None" and SpellSlotAmount > 0:
            RestoredPoints += SpellSlotAmount * self.SpellPointValues[SpellSlotLevel]
        if ManualSpellPointsAmount > 0:
            RestoredPoints += ManualSpellPointsAmount
        self.Stats["Current Spell Points"] = min(MaxSpellPoints, CurrentSpellPoints + RestoredPoints)

    def AddSpell(self, SpellName, SpellSchool, SpellCastingTime, SpellRange, SpellComponents, SpellDuration, SpellText, SpellPrepared):
        NewSpell = {}
        NewSpell["Spell Name"] = SpellName
        NewSpell["Spell School"] = SpellSchool
        NewSpell["Spell Casting Time"] = SpellCastingTime
        NewSpell["Spell Range"] = SpellRange
        NewSpell["Spell Components"] = SpellComponents
        NewSpell["Spell Duration"] = SpellDuration
        NewSpell["Spell Text"] = SpellText
        NewSpell["Spell Prepared"] = SpellPrepared
        self.Stats["Spell List"].append(NewSpell)

    def EditSpell(self, SpellIndex, SpellName, SpellSchool, SpellCastingTime, SpellRange, SpellComponents, SpellDuration, SpellText, SpellPrepared):
        Spell = self.Stats["Spell List"][SpellIndex]
        Spell["Spell Name"] = SpellName
        Spell["Spell School"] = SpellSchool
        Spell["Spell Casting Time"] = SpellCastingTime
        Spell["Spell Range"] = SpellRange
        Spell["Spell Components"] = SpellComponents
        Spell["Spell Duration"] = SpellDuration
        Spell["Spell Text"] = SpellText
        Spell["Spell Prepared"] = SpellPrepared

    def DeleteSpell(self, SpellIndex):
        del self.Stats["Spell List"][SpellIndex]

    def MoveSpell(self, SpellIndex, Delta):
        TargetIndex = SpellIndex + Delta
        if TargetIndex < 0 or TargetIndex >= len(self.Stats["Spell List"]):
            return
        SwapTarget = self.Stats["Spell List"][TargetIndex]
        self.Stats["Spell List"][TargetIndex] = self.Stats["Spell List"][SpellIndex]
        self.Stats["Spell List"][SpellIndex] = SwapTarget

    # Inventory Methods
    def AddInventoryItem(self, ItemName, ItemCount, ItemUnitWeight, ItemUnitValue, ItemUnitValueDenomination, ItemCategoryTag, ItemRarity, ItemDescription):
        NewItem = {}
        NewItem["Item Name"] = ItemName
        NewItem["Item Count"] = ItemCount
        NewItem["Item Unit Weight"] = ItemUnitWeight
        NewItem["Item Unit Value"] = ItemUnitValue
        NewItem["Item Unit Value Denomination"] = ItemUnitValueDenomination
        NewItem["Item Category Tag"] = ItemCategoryTag
        NewItem["Item Rarity"] = ItemRarity
        NewItem["Item Description"] = ItemDescription
        self.Stats["Inventory"].append(NewItem)

    def EditInventoryItem(self, ItemIndex, ItemName, ItemCount, ItemUnitWeight, ItemUnitValue, ItemUnitValueDenomination, ItemCategoryTag, ItemRarity, ItemDescription):
        Item = self.Stats["Inventory"][ItemIndex]
        Item["Item Name"] = ItemName
        Item["Item Count"] = ItemCount
        Item["Item Unit Weight"] = ItemUnitWeight
        Item["Item Unit Value"] = ItemUnitValue
        Item["Item Unit Value Denomination"] = ItemUnitValueDenomination
        Item["Item Category Tag"] = ItemCategoryTag
        Item["Item Rarity"] = ItemRarity
        Item["Item Description"] = ItemDescription

    def DeleteInventoryItem(self, ItemIndex):
        del self.Stats["Inventory"][ItemIndex]

    def MoveInventoryItem(self, ItemIndex, Delta):
        TargetIndex = ItemIndex + Delta
        if TargetIndex < 0 or TargetIndex >= len(self.Stats["Inventory"]):
            return
        SwapTarget = self.Stats["Inventory"][TargetIndex]
        self.Stats["Inventory"][TargetIndex] = self.Stats["Inventory"][ItemIndex]
        self.Stats["Inventory"][ItemIndex] = SwapTarget

    def CalculateItemTotalWeightAndValue(self, ItemIndex):
        Item = self.Stats["Inventory"][ItemIndex]
        Totals = {}
        Totals["Item Total Weight"] = Decimal(Item["Item Count"]) * Decimal(Item["Item Unit Weight"])
        Totals["Item Total Value"] = Decimal(Item["Item Count"]) * Decimal(Item["Item Unit Value"]) * Decimal(self.CoinValues[Item["Item Unit Value Denomination"]])

    def AlterCoinCounts(self, AlteredCounts):
        for Denomination, Count in AlteredCounts.items():
            self.Stats["Coins"][Denomination] = Count

    # Additional Notes Methods
    def AddNote(self, NoteName, NoteText):
        NewNote = {}
        NewNote["Note Name"] = NoteName
        NewNote["Note Text"] = NoteText
        self.Stats["Additional Notes"].append(NewNote)

    def EditNote(self, NoteIndex, NoteName, NoteText):
        Note = self.Stats["Additional Notes"][NoteIndex]
        Note["Note Name"] = NoteName
        Note["Note Text"] = NoteText

    def DeleteNote(self, NoteIndex):
        del self.Stats["Additional Notes"][NoteIndex]

    def MoveNote(self, NoteIndex, Delta):
        TargetIndex = NoteIndex + Delta
        if TargetIndex < 0 or TargetIndex >= len(self.Stats["Additional Notes"]):
            return
        SwapTarget = self.Stats["Additional Notes"][TargetIndex]
        self.Stats["Additional Notes"][TargetIndex] = self.Stats["Additional Notes"][NoteIndex]
        self.Stats["Additional Notes"][NoteIndex] = SwapTarget

    # Serialization Methods
    def SetState(self, NewState):
        self.Stats = NewState["Stats"]

    def GetState(self):
        State = {}
        State["Stats"] = self.Stats
        return State

    @classmethod
    def CreateFromState(cls, State):
        NewPlayerCharacter = cls()
        NewPlayerCharacter.SetState(State)
        return NewPlayerCharacter
