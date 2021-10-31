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

        # Concentrating
        self.Stats["Concentrating"] = False
        self.Stats["Enable Concentration Check"] = True

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

    # Combat Methods
    def Damage(self, DamageAmount):
        TotalDamageAmount = DamageAmount
        CurrentTempHealth = self.Stats["Temp Health"]
        CurrentHealth = self.Stats["Current Health"]
        if CurrentTempHealth == 0:
            self.Stats["Current Health"] = CurrentHealth - DamageAmount
        elif CurrentTempHealth >= 1:
            if CurrentTempHealth < DamageAmount:
                DamageAmount -= CurrentTempHealth
                self.Stats["Temp Health"] = 0
                self.Stats["Current Health"] = CurrentHealth - DamageAmount
            elif CurrentTempHealth >= DamageAmount:
                self.Stats["Temp Health"] = CurrentTempHealth - DamageAmount
        if self.Stats["Concentrating"] and self.Stats["Enable Concentration Check"]:
            ConcentrationDC = max(10, math.ceil(TotalDamageAmount / 2))
            return ConcentrationDC
        else:
            return None

    def Heal(self, HealingAmount, MaxHealth):
        CurrentHealth = self.Stats["Current Health"]
        HealedValue = HealingAmount + max(CurrentHealth, 0)
        HealedValue = min(HealedValue, MaxHealth)
        self.Stats["Current Health"] = HealedValue
