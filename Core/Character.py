import math
import os

from Core.Base64Converters import GetBase64StringFromFilePath, WriteFileFromBase64String


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
        self.Stats["Current Health"] = 1

        # Temp Health
        self.Stats["Temp Health"] = 0

        # Speed
        self.Stats["Speed"] = 0

        # Concentrating
        self.Stats["Concentrating"] = False
        self.Stats["Enable Concentration Check"] = True

        # Portrait
        self.Stats["Portrait"] = None
        self.Stats["Portrait File Extension"] = None
        self.Stats["Portrait Enabled"] = True

    def UpdateStat(self, Stat, NewValue):
        if Stat in [
            "Current Health",
            "Temp Health",
            "Speed",
            "Concentrating",
            "Enable Concentration Check",
            "Portrait",
            "Portrait File Extension",
            "Portrait Enabled"
        ]:
            self.Stats[Stat] = NewValue
            return True

        return False

    def GetDerivedStats(self):
        # Derived Stats Dictionary
        DerivedStats = {}

        # Return Derived Stats Dictionary
        return DerivedStats

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

    # Portrait Methods
    def SetPortrait(self, PortraitFilePath):
        self.Stats["Portrait"] = GetBase64StringFromFilePath(PortraitFilePath)
        self.Stats["Portrait File Extension"] = os.path.splitext(PortraitFilePath)[1]

    def ExportPortrait(self, ExportFilePath):
        WriteFileFromBase64String(self.Stats["Portrait"], ExportFilePath)

    def DeletePortrait(self):
        self.Stats["Portrait"] = None
        self.Stats["Portrait File Extension"] = None
