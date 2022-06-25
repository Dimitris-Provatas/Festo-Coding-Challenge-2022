#!/Users/sheepstress/miniforge3/bin/python

import csv

file = open("office_database.csv")
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
        time = row.get("First Login Time")

        if time == "99:99":
            continue

        timeArray = list(map(int, time.split(":")))

        if timeArray[0] > 7 or timeArray[1] > 14:
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
        time = row.get("First Login Time")

        if time == "99:99":
            continue

        timeArray = list(map(int, time.split(":")))

        if timeArray[0] > 7 or timeArray[1] > 14:
            continue

        solution += int(row.get("ID"))

    print(solution)


if __name__ == "__main__":
    # main()
    # puzzle1()
    # puzzle2()
    puzzle3()
