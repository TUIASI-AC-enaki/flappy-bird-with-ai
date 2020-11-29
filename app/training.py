import pygame, sys
import random

from training.evolutionary_algorithm import one_generation_evolution
from training.models.chromosome import Chromosome
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
        pipe.centerx -= velocity * dt
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes, bird_rect):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return True

    return False


def rotate_bird(bird, index):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement[index] * 3, 1)
    return new_bird


def score_display():
    score_surface = game_font.render(str(score), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(288, 100))
    screen.blit(score_surface, score_rect)

    high_score_surface = game_font.render(f"High Score: {str(high_score)}", True, (255, 255, 255))
    high_score_rect = high_score_surface.get_rect(center=(288, 850))
    screen.blit(high_score_surface, high_score_rect)


# pygame.mixer.pre_init(frequency=44100, size=16, channels=2, buffer=1024)
pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font("assets/04B_19.ttf", 40)

# Game Variables
scale_factor = 70
gravity = 0.35 * scale_factor
up_velocity = 12

game_active = True
score = 0
high_score = 0
velocity = 375
number_of_birds = 150
bird_movement = [0 for _ in range(number_of_birds)]

crossover_probability = 1.0
mutation_probability = 0.05
percentage_for_parenting = 0.5
MAX_GENERATII = 200000
get_ticks_last_frame = 0
dt = 0.01

background_sf = pygame.image.load("assets/background-day.png").convert()
background_sf = pygame.transform.scale2x(background_sf)

floor_sf = pygame.image.load("assets/base.png").convert()
floor_sf = pygame.transform.scale2x(floor_sf)
floor_x = 0

bird_surface = pygame.transform.scale2x(pygame.image.load("assets/bluebird-midflap.png").convert_alpha())

FLY = [pygame.USEREVENT + i for i in range(1, number_of_birds + 1)]
fly_events = [pygame.event.Event(FLY[i]) for i in range(number_of_birds)]
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

for current_generation in range(MAX_GENERATII):
    score = 0
    print("CURRENT GENERATION: {}".format(current_generation))
    bird_rects = [bird_surface.get_rect(center=(100, 512)) for _ in range(number_of_birds)]
    active_birds = [True] * number_of_birds

    # pygame.time.set_timer(FLY, 850)

    # bird_cromoshomes = [Chromosome(NeuralBird()) for _ in range(number_of_birds)]
    bird_cromoshomes = Chromosome.read_from_file("training.json", population_size=number_of_birds)

    bird_cromoshomes = one_generation_evolution(bird_cromoshomes,
                                                crossover_probability=crossover_probability,
                                                mutation_probability=mutation_probability,
                                                finale_population_size=number_of_birds,
                                                percentage_for_parenting=percentage_for_parenting)

    pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
    pipe_surface = pygame.transform.scale2x(pipe_surface)
    pipe_list = []

    pipe_height = [400, 600, 800]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == SPAWNPIPE:
                pipe_list.extend(create_pipe())
                if len(pipe_list) > 8:
                    del pipe_list[0]
                    del pipe_list[0]
            if event.type in FLY:
                ind = event.type - FLY[0]
                bird_movement[ind] = 0
                bird_movement[ind] -= up_velocity
        screen.blit(background_sf, (0, 0))

        if game_active:
            # Bird
            bird_movement = list(map(lambda x: x + gravity * dt, bird_movement))
            rotated_bird = [rotate_bird(bird_surface, i) for i in range(number_of_birds)]
            for index in range(number_of_birds):
                if active_birds[index]:
                    bird_rects[index].centery += bird_movement[index]
                    screen.blit(rotated_bird[index], bird_rects[index])
                    # te uiti la coliziuni
                    if check_collision(pipe_list, bird_rects[index]):
                        active_birds[index] = False

                        bird_cromoshomes[index].complete_training(score)

                distance = 10000
                pipe_up = 10000
                pipe_down = 10000

                # dai update la neuronii de input
                for i in range(0, len(pipe_list), 2):
                    distance = pipe_list[i].bottomleft[0] - bird_rects[index].bottomright[0]
                    pipe_down = pipe_list[i].topright[1] - bird_rects[index].bottomleft[1]
                    pipe_up = pipe_list[i + 1].bottomright[1] - bird_rects[index].topleft[1]
                    if distance > 0:
                        break

                bird_cromoshomes[index].bird.update_inputs(distance=distance, bird_height=bird_rects[index].centery,
                                                           pipe_bottom_height=pipe_down, pipe_top_height=pipe_up,
                                                           velocity=velocity)

                # dai compute la noua valoare. Daca e True generezi event
                # print("Bird {}: {}".format(index, bird_cromoshomes[index].bird.compute_output()))
                if bird_cromoshomes[index].bird.compute_output():
                    pygame.event.post(fly_events[index])

            # cand mor toti faci gameActive = false
            game_active = any(active_birds)

            # Pipes
            pipe_list = move_pipes(pipe_list)
            draw_pipes(pipe_list)

            score += 0.01
            score_display()
        else:
            # alg genetic

            # salvare parametrii cel mai bun fitness

            # resetare populatie
            game_active = True
            write_to_json_file([bird_cromoshomes[i].to_dict() for i in range(number_of_birds)])
            if score > high_score:
                high_score = score
            print("game over")
            break
            pygame.quit()
            sys.exit()
        # Floor
        floor_x -= 1
        draw_floor()
        if floor_x <= -576:
            floor_x = 0

        pygame.display.update()
        t = pygame.time.get_ticks()
        dt = (t - get_ticks_last_frame) / 1000
        get_ticks_last_frame = t
