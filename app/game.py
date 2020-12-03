import pygame, sys
import random
from training import NeuralBird
from training.models.chromosome import Chromosome


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


def check_collision(pipes, bird_rect):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        death_sound.play()
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def rotate_ai(bird):
    new_bird = pygame.transform.rotozoom(bird, -ai_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def ai_animation():
    new_bird = ai_frames[ai_index]
    new_bird_rect = new_bird.get_rect(center=(100+ai_distance_from_bird, ai_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == "main_game" or game_state == "init":
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render("You win!" if not player_lost else "You lost!", True, (0, 255, 0) if not player_lost else (255, 0, 0))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        score_surface = game_font.render(f"Score: {str(int(score))}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 150))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"High Score: {str(int(high_score))}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


# pygame.mixer.pre_init(frequency=44100, size=16, channels=2, buffer=1024)
pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font("assets/04B_19.ttf", 40)

# Game Variables
scale_factor = 70
gravity = 0.35 * scale_factor
up_velocity = 10
bird_movement = 0
game_active = False
score = 0
high_score = 0
get_ticks_last_frame = 0
velocity = 300
dt = 0.01
player_lost = True

background_sf = pygame.image.load("assets/background-day.png").convert()
background_sf = pygame.transform.scale2x(background_sf)

floor_sf = pygame.image.load("assets/base.png").convert()
floor_sf = pygame.transform.scale2x(floor_sf)
floor_x = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-downflap.png").convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-midflap.png").convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load("assets/bluebird-upflap.png").convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap, bird_midflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 512))

ai_downflap = pygame.transform.scale2x(pygame.image.load("assets/redbird-downflap.png").convert_alpha())
ai_midflap = pygame.transform.scale2x(pygame.image.load("assets/redbird-midflap.png").convert_alpha())
ai_upflap = pygame.transform.scale2x(pygame.image.load("assets/redbird-upflap.png").convert_alpha())
ai_frames = [ai_downflap, ai_midflap, ai_upflap, ai_midflap]
ai_index = 0
ai_surface = ai_frames[ai_index]

ai_distance_from_bird = 150
ai_rect = bird_surface.get_rect(center=(100+ai_distance_from_bird, 512))
ai_movement = 0
ai_weights = Chromosome.read_best_from_file("training.json")
ai_bird = NeuralBird(ai_weights if ai_weights else [-0.6104996159116265, -0.29878728694945544, -0.681547440207237, -0.8945106674755301, -0.1442154288454358])

BIRDFLAP = pygame.USEREVENT + 1
AIFLAP = pygame.USEREVENT + 11
pygame.time.set_timer(BIRDFLAP, 200)
pygame.time.set_timer(AIFLAP, 200)

# bird_surface = pygame.image.load("assets/bluebird-midflap.png").convert_alpha()
# bird_surface = pygame.transform.scale2x(bird_surface)
# bird_rect = bird_surface.get_rect(center=(100, 512))

pipe_surface = pygame.image.load("assets/pipe-green.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1600)
pipe_height = [i for i in range(400, 850, 50)]

game_over_surface = pygame.transform.scale2x(pygame.image.load("assets/message.png").convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(288, 512))

flap_sound = pygame.mixer.Sound("assets/sounds/sfx_wing.wav")
death_sound = pygame.mixer.Sound("assets/sounds/sfx_hit.wav")
score_sound = pygame.mixer.Sound("assets/sounds/sfx_point.wav")
score_sound_countdown = 100

AI_EVENT = pygame.USEREVENT + 10

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= up_velocity
                flap_sound.play()
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                ai_rect.center = (200, 512)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            if len(pipe_list) > 4:
                del pipe_list[0]
                del pipe_list[0]
        if event.type == BIRDFLAP:
            bird_index = (bird_index + 1) % len(bird_frames)
            bird_surface, bird_rect = bird_animation()

        if event.type == AI_EVENT:
            ai_movement = 0
            ai_movement -= up_velocity
        if event.type == AIFLAP:
            ai_index = (ai_index + 1) % len(ai_frames)
            ai_surface, ai_rect = ai_animation()

    screen.blit(background_sf, (0, 0))

    if game_active:
        # Bird
        bird_movement += gravity * dt
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list, bird_rect)
        player_lost = True
        # AI
        ai_movement += gravity * dt
        if not len(pipe_list) == 0:
            rotated_ai = rotate_ai(ai_surface)
            ai_rect.centery += ai_movement
            screen.blit(rotated_ai, ai_rect)
        else:
            screen.blit(ai_surface, ai_rect)

        if game_active:
            game_active = check_collision(pipe_list, ai_rect)
            player_lost = False
        distance = 1
        pipe_down = 1
        pipe_up = 1
        for i in range(0, len(pipe_list), 2):
            distance = pipe_list[i].bottomright[0] + 1 - ai_rect.bottomleft[0]
            pipe_down = pipe_list[i].midtop[1] - ai_rect.bottomleft[1]
            pipe_up = pipe_list[i + 1].midbottom[1] - ai_rect.topleft[1]
            if distance > 0:
                break

        ai_bird.update_inputs(distance, ai_rect.centery, pipe_up, pipe_down, velocity)
        if ai_bird.compute_output():
            pygame.event.post(pygame.event.Event(AI_EVENT))
            pygame.event.post(pygame.event.Event(AIFLAP))
            # you can comment this if you don;t like ai flappy flap
            flap_sound.play()

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        if len(pipe_list) > 0:
            if len(list(filter(lambda pipe: 92 <= pipe.centerx <= 97, pipe_list))) == 2:
                score += 1
                score_sound.play()

        score_display("main_game")
    else:
        high_score = update_score(score, high_score)
        screen.blit(game_over_surface, game_over_rect)
        if score > 0:
            score_display("game_over")
        else:
            score_display("init")

    # Floor
    floor_x -= 1
    draw_floor()
    if floor_x <= -576:
        floor_x = 0

    pygame.display.update()
    pygame.display.update()
    t = pygame.time.get_ticks()
    dt = (t - get_ticks_last_frame) / 1000
    get_ticks_last_frame = t
    clock.tick(60)
