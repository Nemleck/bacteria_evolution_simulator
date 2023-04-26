# import pygame and initialize it
import pygame, time, datetime
pygame.init()

from bacteria import BacteriaStats
from AI import *

# create a screen
screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)

# create a surface
surface = pygame.Surface([2000,2000], pygame.SRCALPHA, 32)
surface = surface.convert_alpha()
surfaceRect = surface.get_rect()
surfaceRect.center = screen.get_rect().center

# init phagocytes and bacterias
bacterias = createBacterias(surface.get_rect().center)
phagocytes = createPhagocytes(list(surface.get_rect().center))

bestBacterias = bacterias

# variables
generation = 0
genTicks = 0
ticks = 0
fps = 60
cursor = pygame.transform.scale(pygame.image.load("sources/cursor.png"), (40,40))
oldSec = 0
background = pygame.image.load("sources/background.png")

with open("parameters.json", "r") as f:
    data = json.load(f)

# main loop
while True:
    # tp every phagocyte and bacteria at the start point
    for phagocyte in phagocytes:
        phagocyte.rect.center = phagocyte.startPos
    for bacteria in bacterias:
        bacteria.rect.center = bacteria.startPos
    
    while len(bacterias) > data["bacteria"]["amountToChangeGeneration"]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        # player surface moves
        if pygame.key.get_pressed()[pygame.K_UP]:
            surfaceRect.y += 30
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            surfaceRect.y -= 30
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            surfaceRect.x += 30
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            surfaceRect.x -= 30
        
        # check F11 key
        if pygame.key.get_pressed()[pygame.K_F11]:
            screen = pygame.display.set_mode((0, 0), (pygame.FULLSCREEN))

        # make surface transparent
        surface.fill((255, 0, 0, 10))
        
        # update phagocytes
        for phagocyte in phagocytes:
            phagocyte.update()
            phagocyte.target = None
            targetDistance = 1e10

            # find the closest bacteria
            for bacteria in bacterias:
                distance = math.sqrt((bacteria.rect.centerx - phagocyte.rect.centerx) ** 2 + (bacteria.rect.centery - phagocyte.rect.centery) ** 2)
                if not phagocyte.target or distance < targetDistance:
                    phagocyte.target = bacteria
                    targetDistance = distance

            # eat the closest bacteria
            if phagocyte.target != None:
                if phagocyte.rect.colliderect(phagocyte.target.rect):
                    bacterias.remove(phagocyte.target)
                    phagocyte.target = None
        
        # kill bacterias that are out of the screen
        for bacteria in bacterias:
            if not surfaceRect.colliderect(bacteria.rect):
                bacterias.remove(bacteria)

        # update bacterias
        for bacteria in bacterias:
            bacteria.update(phagocytes)

        # blit every object
        screen.blit(background, (0, 0))

        for phagocyte in phagocytes:
            surface.blit(phagocyte.finalImage, phagocyte.rect)
        for bacteria in bacterias:
            surface.blit(bacteria.finalImage, bacteria.rect)

            # show the bacteria's stats
            # if bacteria.rect.colliderect(cursor.get_rect()):
            #     bacterias[0].image = pygame.image.load("sources/bacteria2.png")

            #     font = pygame.font.SysFont("Arial", 10)
            #     for attribute in range(len(bacteria.__dict__)):
            #         text = font.render(str(list(bacteria.__dict__.keys())[attribute]) + ": " + str(list(bacteria.__dict__.values())[attribute]), True, (255, 255, 255))
            #         screen.blit(text, (bacteria.rect.centerx, bacteria.rect.centery + attribute * 10))
        
        # blit the surface
        screen.blit(surface, surfaceRect)
        
        # show generation
        font = pygame.font.SysFont("Arial", 30)
        text = font.render("Generation: " + str(generation), True, (255, 255, 255))
        screen.blit(text, (0, 0))

        # show the amount of bacterias left
        text = font.render("Bacterias left: " + str(len(bacterias)), True, (255, 255, 255))
        screen.blit(text, (0, 30))

        # show ticks
        text = font.render("Ticks: " + str(genTicks), True, (255, 255, 255))
        screen.blit(text, (0, 60))

        # show the best bacterias from last generation
        if generation > 0:
            font = pygame.font.SysFont("Arial", 10)
            for i in range(len(bestBacterias)):
                for attribute in range(len(bestBacterias[i].__dict__)): # show all attributes
                    text = font.render(str(list(bestBacterias[i].__dict__.keys())[attribute]) + ": " + str(list(bestBacterias[i].__dict__.values())[attribute]), True, (255, 255, 255))
                    screen.blit(text, (0, 100 + attribute * 10 + i*70))
        
        # show cursor in the middle of the screen and coordinates based on the surface
        screen.blit(cursor, screen.get_rect().center)
        font = pygame.font.SysFont("Arial", 20)
        text = font.render(str(((surfaceRect.x - screen.get_width()//2) * -1, (surfaceRect.y - screen.get_height()//2) * -1)), True, (255, 255, 255))
        screen.blit(text, (screen.get_rect().centerx - 25, screen.get_rect().centery + 50))

        # show FPS
        sec = datetime.datetime.now().second

        if sec != oldSec:
            fps = ticks
            ticks = 0

        font = pygame.font.SysFont("Arial", 20)
        text = font.render("FPS: " + str(fps), True, (255, 255, 255))
        screen.blit(text, (0, screen.get_height() - 20))

        # update
        pygame.display.flip()

        # make the game run slower if the player presses the space bar
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            time.sleep(1)
        else:
            time.sleep(1/60)
        
        # old second
        oldSec = sec
        genTicks += 1
        ticks += 1

        for bacteria in bacterias:
            bacteria.lifeTime += 1

    # mutate bacterias
    bestBacterias = [BacteriaStats(elm.speed, elm.rect.center, elm.size, elm.detection, elm.keepDirectionChances, elm.canRunAway) for elm in bacterias]
    bacterias = cloneAllBacterias(bacterias, surfaceRect.center)

    generation += 1
    genTicks = 0