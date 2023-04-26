import pygame
import math

image = pygame.image.load("sources/phagocyte.png")

class Phagocyte:
    def __init__(self, position):
        self.size = 50
        self.angle = 0

        self.image = image
        self.finalImage = self.image
        self.rect = self.image.get_rect()
        self.speed = 3
        self.target = None

        self.startPos = position

        self.update()

        self.rect = self.finalImage.get_rect()
    
    def update(self):
        if self.target:
            # move to target
            self.angle = math.atan2(self.target.rect.centery - self.rect.centery, self.target.rect.centerx - self.rect.centerx)
        
        # move based on angle
        self.move(round(math.cos(self.angle) * self.speed), round(math.sin(self.angle) * self.speed))
        
        self.finalImage = pygame.transform.rotate(
            pygame.transform.scale(
                self.image, (self.size, self.size)
            ), round(self.angle * 180 / math.pi) + 90
        )
    
    def move(self, addX, addY):
        self.rect.centerx += addX
        self.rect.centery += addY