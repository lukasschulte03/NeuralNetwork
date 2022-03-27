from turtle import Screen
import pygame, sys, time, random, math, neat, os
import numpy as np
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Drones")
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()
scoreFont = pygame.font.Font(None,50)
statFont = pygame.font.Font(None,20)
fireImg = pygame.transform.scale(pygame.image.load("images/Fire.png").convert_alpha(), [35,120])
spaceshipImg = pygame.transform.scale(pygame.image.load("images/Spaceship.png").convert_alpha(), [55,55]) 
pointImg = pygame.transform.scale(pygame.image.load("images/Spaceship.png").convert_alpha(), [55,55]) 

FONT = pygame.font.Font(None, 20)

dragCoefficientX = 0.0075
dragCoefficientY = 0.003
gravityForce = -0.2/2
accVerticalForce = 0.5/4
accHorizontalForce = 0.02/2
fps = 150
BestFitness = 0

def GenerateRandomPositionList():
    randomPositionList = []
    for i in range(0,1000):
        n = (random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 100) ) 
        randomPositionList.append(n)
    return randomPositionList

def statistics():
        global Spaceships, BestFitness

        for i, genome in enumerate(ge):
            if genome.fitness > BestFitness:
                BestFitness = genome.fitness

        text_1 = FONT.render(f'Spaceships Alive:  {str(len(Spaceships))}', True, (0, 0, 0))
        text_2 = FONT.render(f'Generation:  {pop.generation+1}', True, (0, 0, 0))
        text_4 = FONT.render(f'Best Fitness:  {str(BestFitness)}', True, (0, 0, 0))

        SCREEN.blit(text_1, (50, 450))
        SCREEN.blit(text_2, (50, 480))
        SCREEN.blit(text_4, (50, 510))

def distance(pos_a, pos_b):
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    return math.sqrt(dx**2 + dy**2)

def blitRotateCenter(surf, image, angle, pos):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = pos).center)
    new_rect.center = pos
    surf.blit(rotated_image, new_rect)

def min_angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    ans1 = np.rad2deg((ang1 - ang2) % (2 * np.pi))
    ans2 = np.rad2deg((ang2 - ang1) % (2 * np.pi))
    return min(ans1, ans2)

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
        self.accX = 0
        self.accY = 0
        self.velX = 0
        self.velY = 0

    def Update(self):

        #Check keypresses and set directionbiases
        self.biasLeft = -1 if self.leftPressed else 0
        self.biasRight = 1 if self.rightPressed else 0
        self.biasUp = -1 if self.upPressed else 0

        #Handle physics
        self.accX += ((self.biasLeft + self.biasRight) * accHorizontalForce)
        self.accY += (self.biasUp * accVerticalForce) - gravityForce
        self.velX += self.accX
        self.velY += self.accY
        self.rect.x += self.velX
        self.rect.y += self.velY

    def Draw(self, SCREEN):
        #Draw potential thrusterfires
        if self.leftPressed:
            blitRotateCenter(SCREEN, self.fireImg, -90, [self.rect.x, self.rect.y])
        if self.rightPressed:
            blitRotateCenter(SCREEN, self.fireImg, 90, [self.rect.x, self.rect.y])
        if self.upPressed:
            blitRotateCenter(SCREEN, self.fireImg, 180, [self.rect.x, self.rect.y])

        #Draw Spaceship
        blitRotateCenter(SCREEN, self.image, 0, [self.rect.x, self.rect.y])

class Point:
    def __init__(self, img = pointImg, randPosList = [(0,0),(0,0)]):
        self.posIndex = 0
        self.randPosList = GenerateRandomPositionList()
        self.image = img
        self.rect = pygame.Rect(self.randPosList[self.posIndex][0], self.randPosList[self.posIndex][1], img.get_width(), img.get_height())
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        self.pointsTaken = 0

    def updatePos(self):
        self.posIndex += 1
        self.pointsTaken += 1
        self.rect.x = self.randPosList[self.posIndex][0]
        self.rect.y = self.randPosList[self.posIndex][1]
        
    def draw(self, SCREEN):
        pygame.draw.circle(SCREEN, self.color, [self.rect.x, self.rect.y], 20)


def eval_genomes(genomes, config):
    global Points, Spaceships, ge, nets, fps
    timer = 0
    timeSinceStart = time.time()
    clock = pygame.time.Clock()

    Points = []
    Spaceships = []
    ge = []
    nets = []

    for genome_id, genome in genomes:
        Spaceships.append(Spaceship())
        Points.append(Point())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0
    
    #posList = GenerateRandomPositionList()

    run = True
    while run:
        MousePos = pygame.mouse.get_pos()
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    fps = 150
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    fps = 6
    
        timer += 1

        SCREEN.fill((255,255,255))

        if len(Spaceships) == 0 or time.time() - timeSinceStart > 10:
            break

        for spaceship in Spaceships:
                spaceship.Update()
                spaceship.Draw(SCREEN)
        for point in Points:
                point.draw(SCREEN)


        for i, spaceship in enumerate(Spaceships):
            pygame.draw.line(SCREEN, Points[i].color, (Points[i].rect.x, Points[i].rect.y), (Spaceships[i].rect.x, Spaceships[i].rect.y), 3)
            if distance((Points[i].rect.x, Points[i].rect.y), (Spaceships[i].rect.x, Spaceships[i].rect.y)) < 60:
                Points[i].updatePos()
                #Points[i].pointsTaken*100
            vector = np.array([Spaceships[i].velX, Spaceships[i].velY])
            magnitude = np.sqrt(vector.dot(vector))
            ge[i].fitness += SCREEN_WIDTH/(distance((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), (Spaceships[i].rect.x, Spaceships[i].rect.y)) + 1) #((180/(min_angle_between((Spaceships[i].velX, Spaceships[i].velY), (Points[i].rect.x - Spaceships[i].rect.x, Points[i].rect.y - Spaceships[i].rect.y))+1))/(360))*magnitude
            inBounds = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT).collidepoint(Spaceships[i].rect.x, Spaceships[i].rect.y)
            if inBounds != True:
                ge[i].fitness -= 1
                Spaceships.pop(i)
                ge.pop(i)
                Points.pop(i)



        for i, spaceship in enumerate(Spaceships):
            #angle = math.atan2(Points[i].rect.y - Spaceships[i].rect.y, Points[i].rect.x - Spaceships[i].rect.x)            
            angle = math.atan2(SCREEN_HEIGHT/2 - Spaceships[i].rect.y, SCREEN_WIDTH/2 - Spaceships[i].rect.x)            
            inputs = [
                Spaceships[i].velX, Spaceships[i].velY, 
                Spaceships[i].rect.x, Spaceships[i].rect.y,
                #Points[i].rect.x - Spaceships[i].rect.x, Points[i].rect.y - Spaceships[i].rect.y,
                #distance((Points[i].rect.x, Points[i].rect.y), (Spaceships[i].rect.x, Spaceships[i].rect.y)),
                distance((SCREEN_WIDTH/2, SCREEN_HEIGHT/2), (Spaceships[i].rect.x, Spaceships[i].rect.y)),
                math.cos(angle),
                math.sin(angle)]
            
            #Store outputs
            output = nets[i].activate(inputs)

            #outputs
            Spaceships[i].leftPressed = True if output[0] < 0 else False
            Spaceships[i].rightPressed = True if output[1] < 0 else False
            Spaceships[i].upPressed = True if output[2] < 0 else False

        statistics()
        pygame.display.update()

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
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.run(eval_genomes, n=None)
    

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)