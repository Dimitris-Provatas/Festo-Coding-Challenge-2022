#!/Users/sheepstress/miniforge3/bin/python

import os
import math
import numpy as np
import time
from datetime import datetime

scriptDir = os.path.dirname(__file__)
trainingClean = "lab_blood_clean.txt"
trainingGen1 = "lab_blood_gen1.txt"
population = "population.txt"
galaxy = "galaxy_map.txt"
placeSequence = "place_sequence.txt"
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


# Training Data / Sanity Check
# trainingCleanFile = open(os.path.join(scriptDir, trainingClean)).read().split("\n\n")
# trainingGen1File = open(os.path.join(scriptDir, trainingGen1)).read().split("\n\n")
# bloodSamplesClean = extractSampleLists(trainingCleanFile)
# bloodSamplesGen1 = extractSampleLists(trainingGen1File)

populationFile = open(os.path.join(scriptDir, population)).read().split("\n\n")
populationList = extractSampleLists(populationFile, True)

galaxyFile = open(os.path.join(scriptDir, galaxy)).read().split("\n")

placeSequenceFile = open(os.path.join(scriptDir, placeSequence)).read().split("\n")[:-1]
securityLogFile = open(os.path.join(scriptDir, securityLog)).read().split("Place: ")[1:]


def main():
    bloodSampleList = []
    planetInhabitList = []
    securityLogList = []

    planets = []
    coordsList = []

    xList = []
    yList = []
    zList = []

    for planetLine in galaxyFile[:-1]:
        planet = (
            planetLine.replace("  ", "").replace("(", "").replace(")", "").split(":")
        )

        coords = planet[1].split(",")

        toAppend = {
            "name": planet[0],
            "coords": {
                "x": int(coords[0]),
                "y": int(coords[1]),
                "z": int(coords[2]),
            },
        }

        planets.append(toAppend)
        coordsList.append(
            [
                int(coords[0]),
                int(coords[1]),
                int(coords[2]),
            ]
        )

        xList.append(int(coords[0]))
        yList.append(int(coords[1]))
        zList.append(int(coords[2]))

    averageX = 0
    averageY = 0
    averageZ = 0

    for coords in coordsList:
        averageX += coords[0]
        averageY += coords[1]
        averageZ += coords[2]

    averageX = averageX / len(coordsList)
    averageY = averageY / len(coordsList)
    averageZ = averageZ / len(coordsList)

    xi = 0
    yi = 0
    zi = 0

    xy = 0
    xz = 0
    yz = 0

    for idx in range(len(coordsList)):
        xi += (coordsList[idx][0] - averageX) ** 2
        yi += (coordsList[idx][1] - averageY) ** 2
        zi += (coordsList[idx][2] - averageZ) ** 2

        xy += (coordsList[idx][0] - averageX) * (coordsList[idx][1] - averageY)
        xz += (coordsList[idx][0] - averageX) * (coordsList[idx][2] - averageZ)
        yz += (coordsList[idx][1] - averageY) * (coordsList[idx][2] - averageZ)

    nVector = [0, 0, 0]

    ditermC = xi * yi - xy**2
    ditermB = xi * zi - xz**2
    ditermA = yi * zi - yz**2

    d = 0

    if (ditermC > ditermB) and (ditermC > ditermA):
        nVector[0] = xy * yz - xz * yi
        nVector[1] = xy * xz - yz * xi
        nVector[2] = ditermC
    elif (ditermB > ditermA) and (ditermB > ditermC):
        nVector[0] = xz * yz - xy * zi
        nVector[1] = ditermB
        nVector[2] = xy * xz - yz * xi
    else:
        nVector[0] = ditermA
        nVector[1] = xz * yz - xy * zi
        nVector[2] = xy * yz - xz * yi

    d = nVector[0] * averageX + nVector[1] * averageY + nVector[2] * averageZ

    planetsOfInterest = []

    for planet in planets:
        point = [planet["coords"]["x"], planet["coords"]["y"], planet["coords"]["z"]]

        distance = abs(np.dot(nVector, point) - d) / math.sqrt(
            nVector[0] ** 2 + nVector[1] ** 2 + nVector[2] ** 2
        )

        if distance >= 10:
            name = planet["name"]
            if name.endswith(" "):
                name = name[:-1]
            planetsOfInterest.append(name)

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
                recordList[2][4:].split(", ") if ins and len(recordList) == 3 else False
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
        if place not in placeSequenceFile:
            continue

        placeLog = betterSecurityLog[place]

        for logEntry in placeLog:
            if logEntry["in"]:
                for personEntered in logEntry["in"]:
                    name = (
                        personEntered[1:]
                        if personEntered.startswith(" ")
                        else personEntered
                    )

                    if name not in logsPerPerson.keys():
                        logsPerPerson[name] = {place: {"in": logEntry["time"]}}
                    elif place not in logsPerPerson[name].keys():
                        logsPerPerson[name][place] = {"in": logEntry["time"]}
                    elif "in" in logsPerPerson[name][place].keys():
                        logsPerPerson[name][place + " 2"] = {"in": logEntry["time"]}
                    else:
                        logsPerPerson[name][place] = {"in": logEntry["time"]}

            if logEntry["out"]:
                for personLeft in logEntry["out"]:
                    name = personLeft[1:] if personLeft.startswith(" ") else personLeft

                    if "out" in logsPerPerson[name][place].keys():
                        logsPerPerson[name][place + " 2"] = {"out": logEntry["time"]}
                    else:
                        logsPerPerson[name][place]["out"] = logEntry["time"]

    potentialTargets = {}
    mySequence = [
        "Junkyard",
        "Pod Racing Track",
        "Pod Racing Track 2",
        "Palace",
        "Factory",
    ]

    for person in logsPerPerson:
        if len(logsPerPerson[person].keys()) < 5 or not [
            a for a in logsPerPerson[person] if a in mySequence
        ]:
            continue

        potentialTargets[person] = logsPerPerson[person]

    actualTargets = []

    for target in potentialTargets:
        sortedSequence = sorted(
            potentialTargets[target].keys(),
            key=lambda place: (
                datetime(
                    1970,
                    1,
                    1,
                    int(potentialTargets[target][place]["out"].split(":")[0]),
                    int(potentialTargets[target][place]["out"].split(":")[1]),
                    0,
                )
            ),
        )

        if sortedSequence != mySequence:
            continue

        actualTargets.append(target)

    for personOfInterest in populationList:
        if isPositiveSample(personOfInterest["bloodSample"]):
            bloodSampleList.append(personOfInterest["name"])

        if personOfInterest["homePlanet"] in planetsOfInterest:
            planetInhabitList.append(personOfInterest["name"])

        if personOfInterest["name"] in actualTargets:
            securityLogList.append(personOfInterest["name"])

    bloodSampleSet = set(bloodSampleList)
    commonNames = bloodSampleSet.intersection(planetInhabitList)
    commonNames = commonNames.intersection(securityLogList)

    print(commonNames)


def puzzle1():
    # Training Data / Sanity Check
    # cleanSamples = []
    # i = 1
    # for sample in bloodSamplesClean:
    #     cleanSamples.append(str(i) + ": " + str(isPositiveSample(sample)))
    #     i += 1

    # positiveSamples = []
    # i = 1
    # for sample in bloodSamplesGen1:
    #     positiveSamples.append(str(i) + ": " + str(isPositiveSample(sample)))
    #     i += 1

    # print("Clean Samples:")
    # print(cleanSamples)
    # print("Positive Gen1 Samples:")
    # print(positiveSamples)

    solution = 0

    for personOfInterest in populationList:
        if isPositiveSample(personOfInterest.get("bloodSample")):
            solution += personOfInterest.get("id")

    print(solution)


def puzzle2():
    planets = []
    coordsList = []

    xList = []
    yList = []
    zList = []

    for planetLine in galaxyFile[:-1]:
        planet = (
            planetLine.replace("  ", "").replace("(", "").replace(")", "").split(":")
        )

        coords = planet[1].split(",")

        toAppend = {
            "name": planet[0],
            "coords": {
                "x": int(coords[0]),
                "y": int(coords[1]),
                "z": int(coords[2]),
            },
        }

        planets.append(toAppend)
        coordsList.append(
            [
                int(coords[0]),
                int(coords[1]),
                int(coords[2]),
            ]
        )

        xList.append(int(coords[0]))
        yList.append(int(coords[1]))
        zList.append(int(coords[2]))

    averageX = 0
    averageY = 0
    averageZ = 0

    for coords in coordsList:
        averageX += coords[0]
        averageY += coords[1]
        averageZ += coords[2]

    averageX = averageX / len(coordsList)
    averageY = averageY / len(coordsList)
    averageZ = averageZ / len(coordsList)

    xi = 0
    yi = 0
    zi = 0

    xy = 0
    xz = 0
    yz = 0

    for idx in range(len(coordsList)):
        xi += (coordsList[idx][0] - averageX) ** 2
        yi += (coordsList[idx][1] - averageY) ** 2
        zi += (coordsList[idx][2] - averageZ) ** 2

        xy += (coordsList[idx][0] - averageX) * (coordsList[idx][1] - averageY)
        xz += (coordsList[idx][0] - averageX) * (coordsList[idx][2] - averageZ)
        yz += (coordsList[idx][1] - averageY) * (coordsList[idx][2] - averageZ)

    nVector = [0, 0, 0]

    ditermC = xi * yi - xy**2
    ditermB = xi * zi - xz**2
    ditermA = yi * zi - yz**2

    d = 0

    if (ditermC > ditermB) and (ditermC > ditermA):
        nVector[0] = xy * yz - xz * yi
        nVector[1] = xy * xz - yz * xi
        nVector[2] = ditermC
    elif (ditermB > ditermA) and (ditermB > ditermC):
        nVector[0] = xz * yz - xy * zi
        nVector[1] = ditermB
        nVector[2] = xy * xz - yz * xi
    else:
        nVector[0] = ditermA
        nVector[1] = xz * yz - xy * zi
        nVector[2] = xy * yz - xz * yi

    d = nVector[0] * averageX + nVector[1] * averageY + nVector[2] * averageZ

    planetsOfInterest = []

    for planet in planets:
        point = [planet["coords"]["x"], planet["coords"]["y"], planet["coords"]["z"]]

        distance = abs(np.dot(nVector, point) - d) / math.sqrt(
            nVector[0] ** 2 + nVector[1] ** 2 + nVector[2] ** 2
        )

        if distance >= 10:
            name = planet["name"]
            if name.endswith(" "):
                name = name[:-1]
            planetsOfInterest.append(name)

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
                recordList[2][4:].split(", ") if ins and len(recordList) == 3 else False
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
        if place not in placeSequenceFile:
            continue

        placeLog = betterSecurityLog[place]

        for logEntry in placeLog:
            if logEntry["in"]:
                for personEntered in logEntry["in"]:
                    name = (
                        personEntered[1:]
                        if personEntered.startswith(" ")
                        else personEntered
                    )

                    if name not in logsPerPerson.keys():
                        logsPerPerson[name] = {place: {"in": logEntry["time"]}}
                    elif place not in logsPerPerson[name].keys():
                        logsPerPerson[name][place] = {"in": logEntry["time"]}
                    elif "in" in logsPerPerson[name][place].keys():
                        logsPerPerson[name][place + " 2"] = {"in": logEntry["time"]}
                    else:
                        logsPerPerson[name][place] = {"in": logEntry["time"]}

            if logEntry["out"]:
                for personLeft in logEntry["out"]:
                    name = personLeft[1:] if personLeft.startswith(" ") else personLeft

                    if "out" in logsPerPerson[name][place].keys():
                        logsPerPerson[name][place + " 2"] = {"out": logEntry["time"]}
                    else:
                        logsPerPerson[name][place]["out"] = logEntry["time"]

    potentialTargets = {}
    mySequence = [
        "Junkyard",
        "Pod Racing Track",
        "Pod Racing Track 2",
        "Palace",
        "Factory",
    ]

    for person in logsPerPerson:
        if len(logsPerPerson[person].keys()) < 5 or not [
            a for a in logsPerPerson[person] if a in mySequence
        ]:
            continue

        potentialTargets[person] = logsPerPerson[person]

    actualTargets = []

    for target in potentialTargets:
        sortedSequence = sorted(
            potentialTargets[target].keys(),
            key=lambda place: (
                datetime(
                    1970,
                    1,
                    1,
                    int(potentialTargets[target][place]["out"].split(":")[0]),
                    int(potentialTargets[target][place]["out"].split(":")[1]),
                    0,
                )
            ),
        )

        if sortedSequence != mySequence:
            continue

        actualTargets.append(target)

    solution = 0

    for person in populationList:
        if person["name"] in actualTargets:
            solution += person["id"]

    print(solution)


def isPositiveSample(sample):
    lineNum = 0

    for lineNum in range(len(sample)):
        line = sample[lineNum]
        idx = 0

        for idx in range(len(line)):
            if line[idx] != "p":
                continue

            if idx > 2:
                if checkSampleInDirection("left", sample, lineNum, idx):
                    return True

            if idx < len(line) - 3:
                if checkSampleInDirection("right", sample, lineNum, idx):
                    return True

            if lineNum > 2:
                if checkSampleInDirection("up", sample, lineNum, idx):
                    return True

            if lineNum < len(sample) - 3:
                if checkSampleInDirection("down", sample, lineNum, idx):
                    return True

    return False


def checkSampleInDirection(direction, sample, lineNumber, linePosition):
    if direction == "up":
        if sample[lineNumber - 1][linePosition] == "i":
            if sample[lineNumber - 2][linePosition] == "c":
                if sample[lineNumber - 3][linePosition] == "o":
                    return True
    elif direction == "down":
        if sample[lineNumber + 1][linePosition] == "i":
            if sample[lineNumber + 2][linePosition] == "c":
                if sample[lineNumber + 3][linePosition] == "o":
                    return True
    elif direction == "left":
        if sample[lineNumber][linePosition - 1] == "i":
            if sample[lineNumber][linePosition - 2] == "c":
                if sample[lineNumber][linePosition - 3] == "o":
                    return True
    elif direction == "right":
        if sample[lineNumber][linePosition + 1] == "i":
            if sample[lineNumber][linePosition + 2] == "c":
                if sample[lineNumber][linePosition + 3] == "o":
                    return True
    else:
        raise RuntimeError("Wrong direction")

    return False


if __name__ == "__main__":
    main()
    # puzzle1()
    # puzzle2()
    # puzzle3()
