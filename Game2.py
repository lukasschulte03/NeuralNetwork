import pygame, sys, time, random, math
from pygame.locals import *
pygame.init()
pygame.display.set_caption("Drones")
screen = pygame.display.set_mode((1920//2,1080//2))
clock = pygame.time.Clock()

circleRadius = 25

liquidDensity = 1.255

leftPressed = False
rightPressed = False
spacePressed = False

biasLeft = 0
biasRight = 0
biasUp = 0

posX = 1920//4
posY = 1080//4
velX = 0
velY = 0
accX = 0
accY = 0

dragCoefficientX = 0.01
dragCoefficientY = 0.005
gravityForce = -0.05
accVerticalForce = 0.1
accHorizontalForce = 0.05


def LineSpam(amount):
    for i in range(amount):
        print(" \n ")

    
while True:
    #set program refresh-speed
    clock.tick(144)

    #background fill the game-window
    screen.fill((0,0,0))

    #detect keystrokes and change booleans
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            print(pygame.key.name(event.key))
            if event.key == K_LEFT:
                leftPressed = True
            if event.key == K_RIGHT:
                rightPressed = True
            if event.key == K_SPACE:
                spacePressed = True
        if event.type == pygame.KEYUP:
            print(pygame.key.name(event.key))
            if event.key == K_LEFT:
                leftPressed = False
            if event.key == K_RIGHT:
                rightPressed = False
            if event.key == K_SPACE:
                spacePressed = False

    #set direction-biases
    if leftPressed:
        biasLeft = -1
    else:
        biasLeft = 0
    if rightPressed:
        biasRight = 1
    else:
        biasRight = 0
    if spacePressed:
        biasUp = -1
    else:
        biasUp = 0
    
    #reset acceleration
    accX = 0
    accY = 0

    #add drag
    drag = dragCoefficientX * ((abs(velX)*abs(velX))/2)# * math.pi * math.pow(circleRadius,2)
    print(drag)
    if velX != 0:
        accX -= (velX/abs(velX)) * drag 
    drag = dragCoefficientY * ((abs(velY)*abs(velY))/2)# * math.pi * math.pow(circleRadius,2)
    print(drag)
    if velY != 0:
        accY -= (velY/abs(velY)) * drag 

    #calculate acceleration to position
    accX += (biasLeft + biasRight)*accHorizontalForce
    accY += (biasUp * accVerticalForce) - gravityForce
    velX += accX
    velY += accY
    posX += velX
    posY += velY

    #draw circle at posX, posY with green color
    pygame.draw.circle(screen, (0, 255, 0),
                   [posX-(circleRadius/2), posY-(circleRadius/2)], circleRadius, 0)

    #update the display
    pygame.display.update()

