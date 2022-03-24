from asyncio.windows_events import NULL
import pygame, random, os, sys, math, neat, time

pygame.init()

BestFitness = 2

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load("Assets/Dino/DinoRun1.png").convert_alpha(),
           pygame.image.load("Assets/Dino/DinoRun2.png").convert_alpha()]
JUMPING = pygame.image.load("Assets/Dino/DinoJump.png").convert_alpha()

SMALL_CACTUS = [pygame.image.load("Assets/Cactus/SmallCactus1.png").convert_alpha(),
                pygame.image.load("Assets/Cactus/SmallCactus2.png").convert_alpha(),
                pygame.image.load("Assets/Cactus/SmallCactus2.png").convert_alpha()]
LARGE_CACTUS = [pygame.image.load("Assets/Cactus/LargeCactus1.png").convert_alpha(),
                pygame.image.load("Assets/Cactus/LargeCactus2.png").convert_alpha(),
                pygame.image.load("Assets/Cactus/LargeCactus2.png").convert_alpha()]

BG = pygame.image.load("Assets/Other/Track.png").convert_alpha()

FONT = pygame.font.Font(None, 20)

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    JUMP_VEL = 8.5

    def __init__(self, img=RUNNING[0]):
        self.image = img
        self.dino_run = True
        self.dino_jump = False
        self.jump_vel = self.JUMP_VEL
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, img.get_width(), img.get_height())
        self.step_index = 0
        self.jumpCount = 0

    def update(self):
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()
        if self.step_index >= 10:
            self.step_index = 0

    def jump(self):
        self.image = JUMPING
        if self.dino_jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
            self.jumpCount += 0.5
        if self.jump_vel <= -self.JUMP_VEL:
            self.dino_jump = False
            self.dino_run = True
            self.jump_vel = self.JUMP_VEL

    def run(self):
        self.image = RUNNING[self.step_index // 5]
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index += 1

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

class Obstacle:
    def __init__(self, image, number_of_cacti):
        self.image = image
        self.type = number_of_cacti
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH
        self.lifeDistance = random.randint(45,90)
        self.startDistance = points

    def update(self):
        self.rect.x -= game_speed
        if points - self.startDistance > self.lifeDistance:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image, number_of_cacti):
        super().__init__(image, number_of_cacti)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image, number_of_cacti):
        super().__init__(image, number_of_cacti)
        self.rect.y = 300

def remove(index):
    dinosaurs.pop(index)
    ge.pop(index)
    nets.pop(index)

def distance(pos_a, pos_b):
    if pos_a != NULL and pos_b != NULL:
        dx = pos_a[0] - pos_b[0]
        dy = pos_a[1] - pos_b[1]
        return dx
    else:
        return 1000

def eval_genomes(genomes, config):
    global game_speed, x_pos_bg, y_pos_bg, obstacles, dinosaurs, ge, nets, points
    clock = pygame.time.Clock()
    points = 0

    obstacles = []
    dinosaurs = []
    ge = []
    nets = []
    obstacles.append(SmallCactus(SMALL_CACTUS, random.randint(0,2)))

    for genome_id, genome in genomes:
        dinosaurs.append(Dinosaur())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 20

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1
        text = FONT.render(f'Points: {str(points)}', True, (0,0,0))
        SCREEN.blit(text, (950, 50))

    def statistics():
        global dinosaurs, game_speed, ge, BestFitness, points

        jumpCounts = [] 
        for i, dinosaur in enumerate(dinosaurs):
            jumpCounts.append(int(dinosaur.jumpCount))
        if len(jumpCounts) != 0:
            if points / (min(jumpCounts)/5 +1) > BestFitness:
                BestFitness = points / (min(jumpCounts)/5 +1)

        text_1 = FONT.render(f'Dinosaurs Alive:  {str(len(dinosaurs))}', True, (0, 0, 0))
        text_2 = FONT.render(f'Generation:  {pop.generation+1}', True, (0, 0, 0))
        text_3 = FONT.render(f'Game Speed:  {str(game_speed)}', True, (0, 0, 0))
        text_4 = FONT.render(f'Best Fitness:  {str(BestFitness)}', True, (0, 0, 0))

        SCREEN.blit(text_1, (50, 450))
        SCREEN.blit(text_2, (50, 480))
        SCREEN.blit(text_3, (50, 510))
        SCREEN.blit(text_4, (50, 540))

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    run = True
    fps = 150
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    fps = 40
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    fps = 150
    
        SCREEN.fill((255,255,255))

        for dinosaur in dinosaurs:
            dinosaur.update()
            dinosaur.draw(SCREEN)

        if len(dinosaurs) == 0:
            break

        if len(obstacles) == 0:
            rand_int = random.randint(0,1)
            if rand_int == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS, random.randint(0,2)))
            else:
                obstacles.append(LargeCactus(LARGE_CACTUS, random.randint(0,2)))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            for i, dinosaur in enumerate(dinosaurs):
                if dinosaur.rect.colliderect(obstacle.rect):
                    ge[i].fitness += points / ((dinosaurs[i].jumpCount +1)/5)
                    remove(i)

        for i, dinosaur in enumerate(dinosaurs):
            output = nets[i].activate((dinosaur.rect.y,
                                        obstacle.rect.x - dinosaur.rect.x,
                                        game_speed))
            print(obstacle.rect.x - dinosaur.rect.x)
            if output[0] < 0.5 and dinosaur.rect.y == dinosaur.Y_POS:
                dinosaur.dino_jump = True
                dinosaur.dino_run = False

        statistics()
        score()
        background()
        clock.tick(fps)
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
    pop.run(eval_genomes, 500)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)