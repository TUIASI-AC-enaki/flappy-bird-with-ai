import pygame, sys
import random

from training.cromozom import Chromosome
from training.neural_bird import NeuralBird
from utils import write_to_json_file


def draw_floor():
    screen.blit(floor_sf, (floor_x, 900))
    screen.blit(floor_sf, (floor_x + 576, 900))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


# pygame.mixer.pre_init(frequency=44100, size=16, channels=2, buffer=1024)
pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0

background_sf = pygame.image.load("assets/background-day.png").convert()
background_sf = pygame.transform.scale2x(background_sf)

floor_sf = pygame.image.load("assets/base.png").convert()
floor_sf = pygame.transform.scale2x(floor_sf)
floor_x = 0

bird_surface = pygame.transform.scale2x(pygame.image.load("assets/bluebird-midflap.png").convert_alpha())
bird_rect = bird_surface.get_rect(center=(100, 512))
FLY = pygame.USEREVENT + 1
fly_event = pygame.event.Event(FLY)
#pygame.time.set_timer(FLY, 850)
bird_cromoshome = Chromosome(NeuralBird())
print(bird_cromoshome)

pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 600, 800]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            if len(pipe_list) > 4:
                del pipe_list[0]
                del pipe_list[0]
        if event.type == FLY:
            bird_movement = 0
            bird_movement -= 12
    screen.blit(background_sf, (0, 0))

    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)

        # te uiti la coliziuni
        check_collision(pipe_list)
        write_to_json_file([bird_cromoshome.to_dict()])
        # dai update la neuronii de input
        # dai compute la noua valoare. Daca e True generezi event
        #       pygame.event.post(fly_event)

        #cand mor toti faci gameActive = false
        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
    else:
        # alg genetic

        #salvare parametrii cel mai bun fitness

        #resetare populatie
        game_active = True
        print("game over")
    # Floor
    floor_x -= 1
    draw_floor()
    if floor_x <= -576:
        floor_x = 0

    pygame.display.update()
    clock.tick(120)
