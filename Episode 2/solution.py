#!/Users/sheepstress/miniforge3/bin/python

import os
from datetime import datetime
from collections import OrderedDict
from itertools import combinations

scriptDir = os.path.dirname(__file__)
trainingClean = "lab_blood_clean.txt"
trainingGen2 = "lab_blood_gen2.txt"
population = "population.txt"
galaxy = "galaxy_map.txt"
tradeRoutes = "trade_routes.txt"
securityLog = "security_log.txt"


def extractSampleLists(file, extractDictionary=False):
    toReturn = []

    for sample in file[:-1]:
        toAppend = []

        if extractDictionary:
            lines = sample.split("\n")

            if lines[0] == "":
                del lines[0]

            toAppend.append(lines[5][3:-1])
            toAppend.append(lines[6][3:-1])
            toAppend.append(lines[7][3:-1])
            toAppend.append(lines[8][3:-1])
            toAppend.append(lines[9][3:-1])
            toAppend.append(lines[10][3:-1])

            toReturn.append(
                {
                    "name": lines[0].split(": ")[-1],
                    "id": int(lines[1].split(": ")[-1]),
                    "homePlanet": lines[2].split(": ")[-1],
                    "bloodSample": toAppend,
                }
            )

            pass
        else:
            lineList = sample.split("  +--------+", 1)[1].split("\n")

            if lineList[0] == "":
                del lineList[0]

            for line in lineList[:-1]:
                toAppend.append(line[3:-1])

            toReturn.append(toAppend)

    return toReturn


# # Training Data / Sanity Check
# trainingCleanFile = open(os.path.join(scriptDir, trainingClean)).read().split("\n\n")
# trainingGen2File = open(os.path.join(scriptDir, trainingGen2)).read().split("\n\n")
# bloodSamplesClean = extractSampleLists(trainingCleanFile)
# bloodSamplesGen2 = extractSampleLists(trainingGen2File)

populationFile = open(os.path.join(scriptDir, population)).read().split("\n\n")
populationList = extractSampleLists(populationFile, True)

galaxyFile = open(os.path.join(scriptDir, galaxy)).read().split("\n")
tradeRoutesFile = open(os.path.join(scriptDir, tradeRoutes)).read().split("\n")

securityLogFile = open(os.path.join(scriptDir, securityLog)).read().split("Place: ")[1:]


def main():
    puzzle1 = []
    puzzle2 = []
    puzzle3 = []

    # Puzzle 1
    for personOfInterest in populationList:
        if isPositiveSample(personOfInterest.get("bloodSample")):
            puzzle1.append(personOfInterest["name"])

    # Puzzle 2
    planets = []
    planetDict = {}

    for planetLine in galaxyFile[:-1]:
        planet = (
            planetLine.replace("  ", "").replace("(", "").replace(")", "").split(":")
        )

        coords = planet[1].split(",")
        name = planet[0]
        if name.endswith(" "):
            name = name[:-1]

        toAppend = {
            "name": name,
            "coords": {
                "x": int(coords[0]),
                "y": int(coords[1]),
                "z": int(coords[2]),
            },
        }

        planets.append(toAppend)
        planetDict[name] = {
            "x": int(coords[0]),
            "y": int(coords[1]),
            "z": int(coords[2]),
        }

    notToCheck = [
        "Saturus",
        "Beta Geminus",
        "Corpeia V",
        "Menta",
        "Grux",
        "Alpha Beron",
        "Gamma Veni",
        "Beta Earos",
        "Alpha Sexta",
        "Alpha Caprida",
    ]

    planetsOfInterest = []

    scurusV = planetDict["Scurus V"]
    tauriesVII = planetDict["Tauries VII"]

    saturus = planetDict["Saturus"]
    betaGeminus = planetDict["Beta Geminus"]

    corpeiaV = planetDict["Corpeia V"]
    menta = planetDict["Menta"]

    grux = planetDict["Grux"]
    alphaBeron = planetDict["Alpha Beron"]

    gammaVeni = planetDict["Gamma Veni"]
    betaEaros = planetDict["Beta Earos"]

    alphaSexta = planetDict["Alpha Sexta"]
    alphaCaprida = planetDict["Alpha Caprida"]

    betaDradoVI = planetDict["Beta Drado VI"]
    uranis = planetDict["Uranis"]

    for planet in planets:
        if planet["name"] in notToCheck:
            continue

        targetPoint = planet["coords"]

        if distanceSquaredOfPointOnLine(targetPoint, scurusV, tauriesVII) > 100:
            continue

        if distanceSquaredOfPointOnLine(targetPoint, saturus, betaGeminus) <= 100:
            continue

        if distanceSquaredOfPointOnLine(targetPoint, corpeiaV, menta) <= 100:
            continue

        if distanceSquaredOfPointOnLine(targetPoint, grux, alphaBeron) <= 100:
            continue

        if distanceSquaredOfPointOnLine(targetPoint, gammaVeni, betaEaros) <= 100:
            continue

        if distanceSquaredOfPointOnLine(targetPoint, alphaSexta, alphaCaprida) <= 100:
            continue

        if distanceSquaredOfPointOnLine(targetPoint, betaDradoVI, uranis) > 100:
            continue

        planetsOfInterest.append(planet["name"])

    for personOfInterest in populationList:
        if personOfInterest["homePlanet"] in planetsOfInterest:
            puzzle2.append(personOfInterest["name"])

    # Puzzle 3
    betterSecurityLog = {}

    for log in securityLogFile:
        line = log.split("\n\n")

        records = []

        for record in line[1:]:
            recordList = record.split("\n")

            if recordList[0] == "":
                continue

            ins = (
                recordList[1].split("in: ")[1].split(", ")
                if recordList[1].startswith("in: ")
                else False
            )
            outs = (
                recordList[2][5:].split(", ") if ins and len(recordList) == 3 else False
            )

            if not outs and recordList[1].startswith("out: "):
                outs = (
                    recordList[1].split("out: ")[1].split(", ")
                    if not ins and len(recordList)
                    else False
                )

            toAdd = {
                "time": recordList[0],
                "in": ins,
                "out": outs,
            }

            records.append(toAdd)

        place = line[0]

        betterSecurityLog[place] = records

    logsPerPerson = {}

    for place in betterSecurityLog.keys():
        placeLog = betterSecurityLog[place]

        for log in placeLog:
            if log["in"]:
                for entered in log["in"]:
                    while entered.startswith(" "):
                        entered = entered[1:]

                    while entered.endswith(" "):
                        entered = entered[:-1]

                    if not entered in logsPerPerson.keys():
                        logsPerPerson[entered] = []

                    logsPerPerson[entered].append(log["time"])

            if log["out"]:
                for left in log["out"]:
                    while left.startswith(" "):
                        left = left[1:]

                    while left.endswith(" "):
                        left = left[:-1]

                    enteredAt = logsPerPerson[left].pop()

                    enterTime = datetime(
                        1970,
                        1,
                        1,
                        int(enteredAt.split(":")[0]),
                        int(enteredAt.split(":")[1]),
                        0,
                    )
                    leaveTime = datetime(
                        1970,
                        1,
                        1,
                        int(log["time"].split(":")[0]),
                        int(log["time"].split(":")[1]),
                        0,
                    )

                    timeSpentInMins = int((leaveTime - enterTime).total_seconds() / 60)

                    if timeSpentInMins < 80:
                        logsPerPerson[left].append(timeSpentInMins)

    personsOfInterest = []

    for person in logsPerPerson.keys():
        personMinutesList = logsPerPerson[person]

        if len(personMinutesList) == 0:
            continue

        personMinutesList.sort()

        allCombinations = list()
        for i in range(len(personMinutesList) + 1):
            allCombinations += (
                list(item) for item in combinations(personMinutesList, i)
            )

        allSums = []
        for combination in allCombinations:
            total = 0

            for inner in combination:
                total += inner

            allSums.append(total)
        allSums.sort()

        if 79 in allSums:
            personsOfInterest.append(person)

    solution = 0

    puzzle3 = personsOfInterest

    # Solution
    for person in populationList:
        if (
            person["name"] in puzzle1
            and person["name"] in puzzle2
            and person["name"] in puzzle3
        ):
            print(person["name"])
            break


def puzzle1():
    # # Training Data / Sanity Check
    # cleanSamples = []
    # i = 1
    # for sample in bloodSamplesClean:
    #     cleanSamples.append(str(i) + ": " + str(isPositiveSample(sample)))
    #     i += 1

    # positiveSamples = []
    # i = 1
    # for sample in bloodSamplesGen2:
    #     positiveSamples.append(str(i) + ": " + str(isPositiveSample(sample)))
    #     i += 1

    # print("Clean Samples:")
    # print(cleanSamples)
    # print("Positive Gen2 Samples:")
    # print(positiveSamples)

    solution = 0

    for personOfInterest in populationList:
        if isPositiveSample(personOfInterest.get("bloodSample")):
            solution += personOfInterest.get("id")

    print(solution)


def puzzle2():
    planets = []
    planetDict = {}

    for planetLine in galaxyFile[:-1]:
        planet = (
            planetLine.replace("  ", "").replace("(", "").replace(")", "").split(":")
        )

        coords = planet[1].split(",")
        name = planet[0]
        if name.endswith(" "):
            name = name[:-1]

        toAppend = {
            "name": name,
            "coords": {
                "x": int(coords[0]),
                "y": int(coords[1]),
                "z": int(coords[2]),
            },
        }

        planets.append(toAppend)
        planetDict[name] = {
            "x": int(coords[0]),
            "y": int(coords[1]),
            "z": int(coords[2]),
        }

    notToCheck = [
        "Saturus",
        "Beta Geminus",
        "Corpeia V",
        "Menta",
        "Grux",
        "Alpha Beron",
        "Gamma Veni",
        "Beta Earos",
        "Alpha Sexta",
        "Alpha Caprida",
    ]

    planetsOfInterest = []

    scurusV = planetDict["Scurus V"]
    tauriesVII = planetDict["Tauries VII"]

    saturus = planetDict["Saturus"]
    betaGeminus = planetDict["Beta Geminus"]

    corpeiaV = planetDict["Corpeia V"]
    menta = planetDict["Menta"]

    grux = planetDict["Grux"]
    alphaBeron = planetDict["Alpha Beron"]

    gammaVeni = planetDict["Gamma Veni"]
    betaEaros = planetDict["Beta Earos"]

    alphaSexta = planetDict["Alpha Sexta"]
    alphaCaprida = planetDict["Alpha Caprida"]

    betaDradoVI = planetDict["Beta Drado VI"]
    uranis = planetDict["Uranis"]

    for planet in planets:
        if planet["name"] in notToCheck:
            continue

        targetPoint = planet["coords"]

        if distanceSquaredOfPointOnLine(targetPoint, scurusV, tauriesVII) > 100:
            continue

        if distanceSquaredOfPointOnLine(targetPoint, saturus, betaGeminus) <= 100:
            continue

        if distanceSquaredOfPointOnLine(targetPoint, corpeiaV, menta) <= 100:
            continue

        if distanceSquaredOfPointOnLine(targetPoint, grux, alphaBeron) <= 100:
            continue

        if distanceSquaredOfPointOnLine(targetPoint, gammaVeni, betaEaros) <= 100:
            continue

        if distanceSquaredOfPointOnLine(targetPoint, alphaSexta, alphaCaprida) <= 100:
            continue

        if distanceSquaredOfPointOnLine(targetPoint, betaDradoVI, uranis) > 100:
            continue

        planetsOfInterest.append(planet["name"])

    solution = 0

    for personOfInterest in populationList:
        if personOfInterest["homePlanet"] in planetsOfInterest:
            solution += personOfInterest["id"]

    print(solution)


def puzzle3():
    betterSecurityLog = {}

    for log in securityLogFile:
        line = log.split("\n\n")

        records = []

        for record in line[1:]:
            recordList = record.split("\n")

            if recordList[0] == "":
                continue

            ins = (
                recordList[1].split("in: ")[1].split(", ")
                if recordList[1].startswith("in: ")
                else False
            )
            outs = (
                recordList[2][5:].split(", ") if ins and len(recordList) == 3 else False
            )

            if not outs and recordList[1].startswith("out: "):
                outs = (
                    recordList[1].split("out: ")[1].split(", ")
                    if not ins and len(recordList)
                    else False
                )

            toAdd = {
                "time": recordList[0],
                "in": ins,
                "out": outs,
            }

            records.append(toAdd)

        place = line[0]

        betterSecurityLog[place] = records

    logsPerPerson = {}

    for place in betterSecurityLog.keys():
        placeLog = betterSecurityLog[place]

        for log in placeLog:
            if log["in"]:
                for entered in log["in"]:
                    while entered.startswith(" "):
                        entered = entered[1:]

                    while entered.endswith(" "):
                        entered = entered[:-1]

                    if not entered in logsPerPerson.keys():
                        logsPerPerson[entered] = []

                    logsPerPerson[entered].append(log["time"])

            if log["out"]:
                for left in log["out"]:
                    while left.startswith(" "):
                        left = left[1:]

                    while left.endswith(" "):
                        left = left[:-1]

                    enteredAt = logsPerPerson[left].pop()

                    enterTime = datetime(
                        1970,
                        1,
                        1,
                        int(enteredAt.split(":")[0]),
                        int(enteredAt.split(":")[1]),
                        0,
                    )
                    leaveTime = datetime(
                        1970,
                        1,
                        1,
                        int(log["time"].split(":")[0]),
                        int(log["time"].split(":")[1]),
                        0,
                    )

                    timeSpentInMins = int((leaveTime - enterTime).total_seconds() / 60)

                    if timeSpentInMins < 80:
                        logsPerPerson[left].append(timeSpentInMins)

    personsOfInterest = []

    for person in logsPerPerson.keys():
        personMinutesList = logsPerPerson[person]

        if len(personMinutesList) == 0:
            continue

        personMinutesList.sort()

        allCombinations = list()
        for i in range(len(personMinutesList) + 1):
            allCombinations += (
                list(item) for item in combinations(personMinutesList, i)
            )

        allSums = []
        for combination in allCombinations:
            total = 0

            for inner in combination:
                total += inner

            allSums.append(total)
        allSums.sort()

        if 79 in allSums:
            personsOfInterest.append(person)

    solution = 0

    for person in populationList:
        if person["name"] in personsOfInterest:
            solution += person["id"]

    print(solution)


def distanceSquaredOfPointOnLine(targetPoint, linePoint1, linePoint2):
    distanceSquare = 0

    distanceOfPointsOnLineSeg = (
        (linePoint2["x"] - linePoint1["x"]) ** 2
        + (linePoint2["y"] - linePoint1["y"]) ** 2
        + (linePoint2["z"] - linePoint1["z"]) ** 2
    )

    dotOfDiffs = (
        (targetPoint["x"] - linePoint1["x"]) * (linePoint2["x"] - linePoint1["x"])
        + (targetPoint["y"] - linePoint1["y"]) * (linePoint2["y"] - linePoint1["y"])
        + (targetPoint["z"] - linePoint1["z"]) * (linePoint2["z"] - linePoint1["z"])
    )

    t = dotOfDiffs / distanceOfPointsOnLineSeg

    if t >= 1:
        distanceSquare = (
            (targetPoint["x"] - linePoint2["x"]) ** 2
            + (targetPoint["y"] - linePoint2["y"]) ** 2
            + (targetPoint["z"] - linePoint2["z"]) ** 2
        )
    elif t <= 0:
        distanceSquare = (
            (targetPoint["x"] - linePoint1["x"]) ** 2
            + (targetPoint["y"] - linePoint1["y"]) ** 2
            + (targetPoint["z"] - linePoint1["z"]) ** 2
        )
    else:
        distanceSquare = (
            (
                targetPoint["x"]
                - (linePoint1["x"] + t * (linePoint2["x"] - linePoint1["x"]))
            )
            ** 2
            + (
                targetPoint["y"]
                - (linePoint1["y"] + t * (linePoint2["y"] - linePoint1["y"]))
            )
            ** 2
            + (
                targetPoint["z"]
                - (linePoint1["z"] + t * (linePoint2["z"] - linePoint1["z"]))
            )
            ** 2
        )

    return distanceSquare


def isPositiveSample(sample):
    lineNum = 0
    isPositive = False

    for lineNum in range(len(sample)):
        line = sample[lineNum]
        idx = 0

        for idx in range(len(line)):
            if line[idx] != "p":
                continue

            isPositive = checkSample(sample, lineNum, idx)

            if isPositive:
                break

        if isPositive:
            break

    return isPositive


def checkSample(sample, lineNumber, linePosition, currentCharIdx=0):
    charSequence = "picoico"

    if (
        currentCharIdx == len(charSequence) - 1
        and sample[lineNumber][linePosition] == "o"
    ):
        return True

    directionsToCheck = []

    if lineNumber > 0:
        directionsToCheck.append("up")

    if lineNumber < len(sample) - 1:
        directionsToCheck.append("down")

    if linePosition > 0:
        directionsToCheck.append("left")

    if linePosition < len(sample[lineNumber]) - 1:
        directionsToCheck.append("right")

    for direction in directionsToCheck:
        found = False

        if direction == "up":
            if sample[lineNumber - 1][linePosition] == charSequence[currentCharIdx + 1]:
                found = checkSample(
                    sample, lineNumber - 1, linePosition, currentCharIdx + 1
                )
        elif direction == "down":
            if sample[lineNumber + 1][linePosition] == charSequence[currentCharIdx + 1]:
                found = checkSample(
                    sample, lineNumber + 1, linePosition, currentCharIdx + 1
                )
        elif direction == "left":
            if sample[lineNumber][linePosition - 1] == charSequence[currentCharIdx + 1]:
                found = checkSample(
                    sample, lineNumber, linePosition - 1, currentCharIdx + 1
                )
        elif direction == "right":
            if sample[lineNumber][linePosition + 1] == charSequence[currentCharIdx + 1]:
                found = checkSample(
                    sample, lineNumber, linePosition + 1, currentCharIdx + 1
                )
        else:
            raise RuntimeError("Wrong direction")

        if found:
            return True

    return False


if __name__ == "__main__":
    main()
    # puzzle1()
    # puzzle2()
    # puzzle3()
