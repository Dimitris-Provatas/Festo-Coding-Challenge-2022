#!/Users/sheepstress/miniforge3/bin/python

import csv
import os
import time
from datetime import datetime

scriptDir = os.path.dirname(__file__)
filename = "office_database.csv"
targetFilePath = os.path.join(scriptDir, filename)
file = open(targetFilePath)

# For Puzzle 3
targetTime = datetime(1970, 1, 1, 7, 14, 0)

database = csv.DictReader(file, skipinitialspace=True)
# Row Example: {
# 'Username': 'abc',
# 'ID': '123',
# 'Access Key': '123',
# 'First Login Time': '69:42'
# }


def main():
    for row in database:
        # Puzzle 3
        timeString = row.get("First Login Time")

        if timeString == "99:99":
            continue

        timeArray = list(map(int, timeString.split(":")))

        timeObj = datetime(1970, 1, 1, timeArray[0], timeArray[1], 0)

        if timeObj.time() > targetTime.time():
            continue

        # Puzzle 1
        if "814" not in row.get("ID"):
            continue

        # Puzzle 2
        binary = bin(int(row.get("Access Key")))[2:]

        binary = binary.rjust(8, "0")

        if binary[4] != "1":
            continue

        # Get result
        print(row)


def puzzle1():
    solution = 0

    for row in database:
        if "814" in row.get("ID"):
            solution += int(row.get("ID"))

    print(solution)


def puzzle2():
    solution = 0

    for row in database:
        binary = bin(int(row.get("Access Key")))[2:]

        binary = binary.rjust(8, "0")

        if binary[4] == "1":
            solution += int(row.get("ID"))

    print(solution)


def puzzle3():
    solution = 0

    for row in database:
        timeString = row.get("First Login Time")

        if timeString == "99:99":
            continue

        timeArray = list(map(int, timeString.split(":")))

        timeObj = datetime(1970, 1, 1, timeArray[0], timeArray[1], 0)

        if timeObj.time() > targetTime.time():
            continue

        solution += int(row.get("ID"))

    print(solution)


if __name__ == "__main__":
    main()
    # puzzle1()
    # puzzle2()
    # puzzle3()
