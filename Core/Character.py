import math


class Character:
    def __init__(self):
        self.CreateStaticValues()
        self.CreateStats()

    def CreateStaticValues(self):
        # Abilities
        self.Abilities = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

    def CreateStats(self):
        # Stats Dictionary
        self.Stats = {}

        # Current Health
        self.Stats["Current Health"] = 0

        # Temp Health
        self.Stats["Temp Health"] = 0

        # Speed
        self.Stats["Speed"] = 0

        # Portrait
        self.Stats["Portrait"] = None
        self.Stats["Portrait Enabled"] = True

    def GetDerivedStats(self):
        # Derived Stats Dictionary
        DerivedStats = {}

        # Proficiency
        DerivedStats["Proficiency Modifier"] = self.LevelDerivedValues[str(self.Stats["Level"])]["Proficiency Bonus"]

        # Return Derived Stats Dictionary
        return DerivedStats

    # Stat Calculation Methods
    def CalculateProficiencyModifier(self):
        return None

    def GetBaseAbilityModifier(self, AbilityScore):
        return math.floor((AbilityScore - 10) / 2)
