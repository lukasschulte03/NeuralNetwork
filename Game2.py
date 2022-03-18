from numpy import True_
import pygame, sys, time, random, math
from pygame.locals import *
pygame.init()
pygame.display.set_caption("Drones")
screen = pygame.display.set_mode((1920,1080))
clock = pygame.time.Clock()
scoreFont = pygame.font.Font(None,50)
statFont = pygame.font.Font(None,20)
width, height = pygame.display.get_surface().get_size() 
fireImg = pygame.transform.scale(pygame.image.load("Fire.png").convert_alpha(), [35,120]) 

circleRadius = 25

liquidDensity = 1.255

score = -1

leftPressed = False
rightPressed = False
spacePressed = False

collected = True

biasLeft = 0
biasRight = 0
biasUp = 0

posX = width / 2
posY = height / 2
velX = 0
velY = 0
accX = 0
accY = 0

pointPosX = 0
pointPosY = 0

dragCoefficientX = 0#0.0075
dragCoefficientY = 0#0.003
gravityForce = -0.4
accVerticalForce = 1
accHorizontalForce = 0.4

manualBot = False

#print 'amount' number of empty lines
def LineSpam(amount):
    for i in range(amount):
        print(" \n ")

#rotate a image, maintaining position. Then blit it  
def blitRotateCenter(surf, image, topleft, angle, pos):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    new_rect.center = pos

    surf.blit(rotated_image, new_rect)

#loop forever
while True:

    #set program refresh-speed
    clock.tick(60)

    #--------------------------------------------------------------------------
    if manualBot:
        leftPressed = True if posX > pointPosX else False
        rightPressed = True if posX < pointPosX else False
        spacePressed = True if posY > pointPosY else False
    #--------------------------------------------------------------------------

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

    #check key-booleans and draw fire thrusters accordingly
    if leftPressed:
        blitRotateCenter(screen, fireImg, [posX,posY], -90, [posX,posY])
    if rightPressed:
        blitRotateCenter(screen, fireImg, [posX,posY], 90, [posX,posY])
    if spacePressed:
        blitRotateCenter(screen, fireImg, [posX,posY], 180, [posX,posY])

    #draw circle at posX, posY with color
    pygame.draw.circle(screen, (100, 100, 255),
                   [posX, posY], circleRadius, 0)

    #draw line from ball to point
    pygame.draw.line(screen, (255,255,255), (posX,posY), (pointPosX, pointPosY), 1)

    #measure distance from ball to point, and collect
    distance = math.sqrt(pow(posX-pointPosX, 2) + pow(posY-pointPosY, 2))
    if distance < circleRadius:
        collected = True

    #update point position if collected
    if collected:
            pointPosX = random.randint(0,width)
            pointPosY = random.randint(0,height)
            score +=1
            collected = False

    #draw collectable point
    pygame.draw.circle(screen, (100, 255, 100),
        [pointPosX, pointPosY], circleRadius/3, 0)

    #draw score on top-center of screen
    text = scoreFont.render("Score: " + str(score), True, (255,255,255))
    text_rect = text.get_rect(center=(width/2, 25))
    screen.blit(text, text_rect)

    #blit statistics
    screen.blit(statFont.render("distance: "+str(int(distance)),True,(255,255,255)),(5,25))
    screen.blit(statFont.render("ball pos: "+str(int(posX))+", "+str(int(posY)),True,(255,255,255)),(5,50))
    screen.blit(statFont.render("point pos: "+str(int(pointPosX))+", "+str(int(pointPosX)),True,(255,255,255)),(5,75))
    screen.blit(statFont.render("Dx: "+str(int(pointPosX - posX)),True,(255,255,255)),(5,100))
    screen.blit(statFont.render("Dy: "+str(int(pointPosY - posY)),True,(255,255,255)),(5,125))


    #update the display
    pygame.display.update()
