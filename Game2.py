import pygame, sys, time, random, math
from pygame.locals import *
pygame.init()
pygame.display.set_caption("Drones")
screen = pygame.display.set_mode((1920,1080))
clock = pygame.time.Clock()

font = pygame.font.Font(None,50)

width, height = pygame.display.get_surface().get_size()

circleRadius = 25

liquidDensity = 1.255

score = 10

leftPressed = False
rightPressed = False
spacePressed = False

biasLeft = 0
biasRight = 0
biasUp = 0

posX = width / 2
posY = height / 2
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

    #detect keystrokes and change booleans accordingly
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_LEFT:
                leftPressed = True
            if event.key == K_RIGHT:
                rightPressed = True
            if event.key == K_SPACE:
                spacePressed = True
        if event.type == pygame.KEYUP:
            if event.key == K_LEFT:
                leftPressed = False
            if event.key == K_RIGHT:
                rightPressed = False
            if event.key == K_SPACE:
                spacePressed = False

    #read key-booleans and set direction-biases
    biasLeft = -1 if leftPressed else 0
    biasRight = 1 if rightPressed else 0
    biasUp = -1 if spacePressed else 0
    
    #reset acceleration
    accX = 0
    accY = 0

    #calculate drag forces, and assign them to dragX and dragY
    dragX = dragCoefficientX * ((abs(velX)*abs(velX))/2)
    if velX != 0:
        dragX = math.copysign(1,velX) * dragX 
    dragY = dragCoefficientY * ((abs(velY)*abs(velY))/2)
    if velY != 0:
        dragY = math.copysign(1,velY) * dragY 

    #calculate acceleration to position (inverse derivative)
    accX += ((biasLeft + biasRight) * accHorizontalForce) - dragX
    accY += (biasUp * accVerticalForce) - gravityForce - dragY
    velX += accX
    velY += accY
    posX += velX
    posY += velY

    #draw circle at posX, posY with green color
    pygame.draw.circle(screen, (0, 255, 0),
                   [posX-(circleRadius/2), posY-(circleRadius/2)], circleRadius, 0)

    #draw score on top-center of screen
    text = font.render("Score: " + str(score), True, (255,255,255))
    text_rect = text.get_rect(center=(width/2, 25))
    screen.blit(text, text_rect)

    #update the display
    pygame.display.update()

