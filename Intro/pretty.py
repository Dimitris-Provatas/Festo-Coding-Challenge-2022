#!/Users/sheepstress/miniforge3/bin/python

import csv
import os
import time
from datetime import datetime

scriptDir = os.path.dirname(__file__)
filename = "office_database.csv"
targetFilePath = os.path.join(scriptDir, filename)
file = open(targetFilePath)

targetTime = datetime(1970, 1, 1, 7, 14, 0)

database = csv.DictReader(file, skipinitialspace=True)


def main():
    target = None
    puzzle1 = 0
    puzzle2 = 0
    puzzle3 = 0

    for row in database:
        idInt = idToInt(row.get("ID"))

        isIdOfInterest = checkId(row.get("ID"))

        hasAccessRights = checkAccess(int(row.get("Access Key")))

        inTimeOfInterest = checkTime(row.get("First Login Time"))

        if isIdOfInterest:
            puzzle1 += idInt

        if hasAccessRights:
            puzzle2 += idInt

        if inTimeOfInterest:
            puzzle3 += idInt

        if not isIdOfInterest or not hasAccessRights or not inTimeOfInterest:
            continue

        target = row

    print(f"Puzzle 1: {puzzle1}")
    print(f"Puzzle 2: {puzzle2}")
    print(f"Puzzle 3: {puzzle3}")
    print(f"Final Target: {target.get('Username')}")


def idToInt(id: str):
    return int(id)


def checkId(id: str):
    return "814" in id


def checkAccess(access: int):
    binary = bin(int(access))[2:]

    binary = binary.rjust(8, "0")

    return binary[4] == "1"


def checkTime(timeStr: str):
    if timeStr == "99:99":
        return False

    timeArray = list(map(int, timeStr.split(":")))

    timeObj = datetime(1970, 1, 1, timeArray[0], timeArray[1], 0)

    return timeObj.time() < targetTime.time()


if __name__ == "__main__":
    main()
