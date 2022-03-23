import pygame, sys, time, random, math, neat, os
from pygame.locals import *
pygame.init()
pygame.display.set_caption("Drones")
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()
scoreFont = pygame.font.Font(None,50)
statFont = pygame.font.Font(None,20)
fireImg = pygame.transform.scale(pygame.image.load("images/Fire.png").convert_alpha(), [35,120])
spaceshipImg = pygame.transform.scale(pygame.image.load("images/Spaceship.png").convert_alpha(), [55,55]) 
pointImg = pygame.transform.scale(pygame.image.load("images/Spaceship.png").convert_alpha(), [55,55]) 

dragCoefficientX = 0.0075
dragCoefficientY = 0.003
gravityForce = -0.4
accVerticalForce = 1
accHorizontalForce = 0.4

randomPositionList = []
for i in range(0,1000):
    n = random.randint(10, SCREEN_HEIGHT - 10)
    randomPositionList.append(n)


def blitRotateCenter(surf, image, angle, pos):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = pos).center)
    new_rect.center = pos
    surf.blit(rotated_image, new_rect)

class Spaceship:

    #Initiall screen position
    X_POS = SCREEN_WIDTH//2
    Y_POS = SCREEN_HEIGHT//2

    def __init__(self, img = spaceshipImg, fireImg = fireImg):
        self.image = img
        self.fireImg = fireImg
        self.rightPressed = False
        self.leftPressed = False
        self.upPressed = False
        self.biasLeft = 0
        self.biasRight = 0
        self.biasUp = 0
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, img.get_width(), img.get_height())
        self.points = 0
        self.acc = (0, 0)
        self.vel = (0, 0)
        self.pos = (0, 0)

    def Update(self):

        #Check keypresses and set directionbiases
        self.biasLeft = -1 if self.leftPressed else 0
        self.biasRight = 1 if self.rightPressed else 0
        self.biasUp = -1 if self.upPressed else 0

        #Handle physics
        self.acc[0] += ((self.biasLeft + self.biasRight) * accHorizontalForce)
        self.acc[1] += (self.biasUp * accVerticalForce) - gravityForce
        self.vel[0] += self.acc[0]
        self.vel[1] += self.acc[1]
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]

    def Draw(self, SCREEN):

        #Draw Spaceship
        blitRotateCenter(SCREEN, self.img, 0, [self.rect.x, self.rect.y])

        #Draw potential thrusterfires
        if self.leftPressed:
            blitRotateCenter(SCREEN, self.fireImg, -90, [self.rect.x, self.rect.y])
        if self.rightPressed:
            blitRotateCenter(SCREEN, self.fireImg, 90, [self.rect.x, self.rect.y])
        if self.upPressed:
            blitRotateCenter(SCREEN, self.fireImg, 180, [self.rect.x, self.rect.y])

class Point:
    def __init__(self, img = pointImg, randPosList = randomPositionList):
        self.posIndex = 0
        self.randPosList = randPosList
        self.image = img
        self.rect = pygame.Rect(self.randPosList[1], self.randPosList[2], img.get_width(), img.get_height())

    def updatePos(self):
        self.posIndex += 1
        self.rect.x = self.randPosList[self.posIndex]
        self.rect.y = self.randPosList[self.posIndex + 1]
        
    def draw(self, SCREEN):
        SCREEN.blit(self.image, self.rect)


def eval_genomes(genomes, config):
    global Points, Spaceships, ge, nets
    clock = pygame.time.Clock()

    Points = []
    Spaceships = []
    ge = []
    nets = []
    Points.append(Point())

    for genome_id, genome in genomes:
        Spaceships.append(Spaceship())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    for spaceship in Spaceships:
            spaceship.Update()
            spaceship.Draw(SCREEN)
    for point in Points:
            point.draw(SCREEN)

def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.run(eval_genomes, 500)

if __name__ == '__Game_AI__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)