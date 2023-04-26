import pygame
import random
import math
import json

image1 = pygame.image.load("sources/bacteria.png")
image2 = pygame.image.load("sources/bacteria2.png")

with open("parameters.json", "r") as f:
    data = json.load(f)["bacteria"]

class BacteriaStats:
    def __init__(self, speed, position, size, detection, keepDirectionChances, canRunAway):
        # changeable caracteristics
        self.size = size
        self.reproductionSize = 100
        self.speed = speed
        self.startPos = position
        self.detection = detection # detection range (size * detection)
        self.keepDirectionChances = keepDirectionChances # chance to keep direction
        self.canRunAway = canRunAway # can run away from phagocytes

class Bacteria(BacteriaStats):
    def __init__(self, speed, position, size, detection, keepDirectionChances, canRunAway):
        BacteriaStats.__init__(self, speed, position, size, detection, keepDirectionChances, canRunAway)

        # unchangeable caracteristics
        self.image = image1
        self.finalImage = self.image
        self.rect = self.image.get_rect()
        self.angle = 0
        self.lifeTime = 0

        self.update([])

        self.rect = self.finalImage.get_rect()
    
    def update(self, phagocytes):
        # check if phagocyte is near
        best = None

        if self.canRunAway:
            bestDistance = 1e10
            for phagocyte in phagocytes:
                distance = math.sqrt((phagocyte.rect.centerx - self.rect.centerx)**2 + (phagocyte.rect.centery - self.rect.centery)**2)
                if distance < data["detectionMultiplier"]*self.detection:
                    # determine the nearest phagocyte
                    if not best or distance < bestDistance:
                        best = phagocyte
                        bestDistance = distance

        if not best:
            # move randomly
            # go in current direction
            self.rect.centerx += round(math.cos(self.angle) * self.speed)
            self.rect.centery += round(math.sin(self.angle) * self.speed)

            # change direction
            if random.randint(0, 200) < self.keepDirectionChances:
                self.angle = random.randint(0, 360)
            
            self.image = image1
        else:
            self.run_away(best)
            self.image = image2
        
        # check if near to the edge
        if self.rect.centerx < self.detection * self.size:
            # get direction of the edge
            self.angle = math.atan2(0 - self.rect.centery, 0 - self.rect.centerx) + 180

        if self.rect.centerx < 0:
            self.rect.centerx = 0
        if self.rect.centery < 0:
            self.rect.centery = 0

        self.finalImage = pygame.transform.rotate(
            pygame.transform.scale(
                self.image, (self.size, self.size)
            ), self.angle
        )
    
    def run_away(self, phagocyte):
        # run away
        self.rect.centerx += round(math.cos(phagocyte.angle) * self.speed)
        self.rect.centery += round(math.sin(phagocyte.angle) * self.speed)
        self.angle = phagocyte.angle