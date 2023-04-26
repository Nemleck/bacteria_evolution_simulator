import pygame
import random
import math
import json

# import classes
from phagocyte import Phagocyte
from bacteria import Bacteria

with open("parameters.json", "r") as f:
    parameters = json.load(f)

def createBacterias(centerPos):
    bacterias = []
    for i in range(parameters["bacteria"]["amount"]):
        bacterias.append(Bacteria(random.randint(1, 5), [
                random.randint(centerPos[0]-500, centerPos[0]+500), 
                random.randint(centerPos[1]-500, centerPos[1]+500)],
                random.randint(10, 100), 
                random.randint(1, 3),
                random.randint(1, 10),
                random.choice([True, False])))
    return bacterias

def createPhagocytes(centerPos):
    phagocytes = []
    for i in range(parameters["phagocyte"]["amount"]):
        phagocytes.append(
            Phagocyte([
                random.randint(centerPos[0]-500, centerPos[0]+500), 
                random.randint(centerPos[1]-500, centerPos[1]+500)]
            )
        )

    return phagocytes

def cloneOneBacteria(bacteria, centerPos):
    newBacteria = Bacteria(bacteria.speed, bacteria.startPos, bacteria.size, bacteria.detection, bacteria.keepDirectionChances, bacteria.canRunAway)

    # mutation
    randomAttr = random.choice(["size", "reproductionSize", "speed", "startPos", "detection", "keepDirectionChances"])

    if randomAttr == "startPos":
        newBacteria.startPos = [random.randint(centerPos[0]-500, centerPos[0]+500), random.randint(centerPos[1]-500, centerPos[1]+500)]
    else:
        # change value of attribute from min to max
        setattr(newBacteria, randomAttr, getattr(newBacteria, randomAttr) + random.randint(parameters["bacteria"][randomAttr][0], parameters["bacteria"][randomAttr][1]))

        # change a little startPos anyway
        newBacteria.startPos[0] += random.randint(-100, 100)
        newBacteria.startPos[1] += random.randint(-100, 100)

    return newBacteria

def cloneAllBacterias(bacterias, centerPos):
    result = bacterias

    for i in range(len(bacterias)):
        result.append(cloneOneBacteria(bacterias[i], centerPos))

    return result