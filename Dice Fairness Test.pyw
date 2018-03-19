import random

# Set Parameters
DieSize = 20
NumberOfRolls = 1000000

# Set Up Value Collection
RollCounts = {}
for Result in range(1, DieSize + 1):
    RollCounts[str(Result)] = 0

RollValues = []

# Roll
for Roll in range(NumberOfRolls):
    RollResult = random.randint(1, DieSize)
    RollCounts[str(RollResult)] += 1
    RollValues.append(RollResult)

# Compute and Print Results
print("Die Size:  " + str(DieSize))
print("Number of Rolls:  " + str(NumberOfRolls))

ResultTotalCounts = 0

print("\nResults:")
for Result, Count in RollCounts.items():
    print("   " + Result + ":  " + str(Count))
    ResultTotalCounts += Count

print("\nAverage Count per Result:  " + str((ResultTotalCounts / DieSize)))
print("Theoretical Average Count per Result:  " + str((NumberOfRolls / DieSize)))

RollValuesAverage = 0

for RollValue in RollValues:
    RollValuesAverage += RollValue

RollValuesAverage /= NumberOfRolls

print("\nAverage Die Roll:  " + str(RollValuesAverage))
print("Theoretical Average Die Roll:  " + str((DieSize / 2) + 0.5))
