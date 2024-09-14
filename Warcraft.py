import random
import sys
from sys import exit

import pygame
from pygame.locals import *

sys.path.append('c:/Users/shubham/Desktop/new/MDC/Projects/Warcraft')  # Adjust the path as needed
from Warcraft import \
    Opponent  # Ensure the module exists in the specified directory

pygame.init()
SCREEN_WIDTH = 800  # Define the screen width
SCREEN_HEIGHT = 600  # Define the screen height
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Aircraft War Game')

# Load sounds and set volumes
BULLETSHOT_SOUNDTEST = pygame.mixer.Sound('image/sound/bullet.wav')
OPPONENT1_DOWN_SOUNDTEST = pygame.mixer.Sound('image/sound/opponent1_down.wav')
GAMEOVER_SOUNDTEST = pygame.mixer.Sound('image/sound/game_over.wav')
BULLETSHOT_SOUNDTEST.set_volume(0.3)
OPPONENT1_DOWN_SOUNDTEST.set_volume(0.3)
GAMEOVER_SOUNDTEST.set_volume(0.3)
pygame.mixer.music.load('image/sound/game_music.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

# Load images
GAME_BACKGROUND = pygame.image.load('image/image/background.png').convert()
GAME_OVER = pygame.image.load('image/image/gameover.png')
filename = 'image/image/aircraft_shooter.png'
AIRCRAFT_IMAGES = pygame.image.load(filename)

# Player and opponent setup
AIRCRAFT_PLAYER = [
    pygame.Rect(0, 99, 102, 126),
    pygame.Rect(165, 360, 102, 126),
    pygame.Rect(165, 234, 102, 126),
    pygame.Rect(330, 624, 102, 126),
    pygame.Rect(330, 498, 102, 126),
    pygame.Rect(432, 624, 102, 126)
]
AIRCRAFT_PLAYER_POSITION = [200, 600]
OPPONENT = Opponent(AIRCRAFT_IMAGES, AIRCRAFT_PLAYER, AIRCRAFT_PLAYER_POSITION)

# Bullet setup
AIRCRAFT_BULLET = pygame.Rect(1004, 987, 9, 21)
BULLET_IMAGES = AIRCRAFT_IMAGES.subsurface(AIRCRAFT_BULLET)

# Opponent setup
OPPONENT1 = pygame.Rect(534, 612, 57, 43)
OPPONENT1_IMAGES = AIRCRAFT_IMAGES.subsurface(OPPONENT1)
OPPONENT1_DOWN_IMAGES = [
    AIRCRAFT_IMAGES.subsurface(pygame.Rect(267, 347, 57, 43)),
    AIRCRAFT_IMAGES.subsurface(pygame.Rect(873, 697, 57, 43)),
    AIRCRAFT_IMAGES.subsurface(pygame.Rect(267, 296, 57, 43)),
    AIRCRAFT_IMAGES.subsurface(pygame.Rect(930, 697, 57, 43))
]

CHALLENGER1 = pygame.sprite.Group()
CHALLENGER_DOWN = pygame.sprite.Group()

SHOOT_DISTANCE = 0
CHALLENGER_DISTANCE = 0
OPPONENT_DOWN_INDEX = 16
SCORE = 0
CLOCK = pygame.time.Clock()
RUNNING = True

# Main game loop
while RUNNING:
    CLOCK.tick(60)

    # Opponent shooting
    if not OPPONENT.is_hit:
        if SHOOT_DISTANCE % 15 == 0:
            BULLETSHOT_SOUNDTEST.play()
            OPPONENT.shoot(BULLET_IMAGES)
        SHOOT_DISTANCE += 1
    if SHOOT_DISTANCE >= 15:
        SHOOT_DISTANCE = 0

    # Challengers
    if SHOOT_DISTANCE % 50 == 0:
        CHALLENGER1_POSITION = [random.randint(0, SCREEN_WIDTH - OPPONENT1.width), 0]
        CHALLENGERS1 = Opponent(OPPONENT1_IMAGES, OPPONENT1_DOWN_IMAGES, CHALLENGER1_POSITION)
        CHALLENGER1.add(CHALLENGERS1)
    CHALLENGER_DISTANCE += 1
    if CHALLENGER_DISTANCE >= 100:
        CHALLENGER_DISTANCE = 0

    # Bullet movement
    for bullet in OPPONENT.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            OPPONENT.bullets.remove(bullet)

    # Challenger movement and collision
    for CHALLENGER in CHALLENGER1:
        CHALLENGER.move()
        if pygame.sprite.collide_circle(CHALLENGER, OPPONENT):
            CHALLENGER_DOWN.add(CHALLENGER)
            CHALLENGER1.remove(CHALLENGER)
            OPPONENT.is_hit = True
            GAMEOVER_SOUNDTEST.play()
            RUNNING = False
            break
        if CHALLENGER.rect.top > SCREEN_HEIGHT:
            CHALLENGER1.remove(CHALLENGER)

    # Update screen
    screen.fill(0)
    screen.blit(GAME_BACKGROUND, (0, 0))

    # Draw player and challengers
    if not OPPONENT.is_hit:
        screen.blit(OPPONENT.image[OPPONENT.img_index], OPPONENT.rect)
        OPPONENT.img_index = SHOOT_DISTANCE // 8
    else:
        OPPONENT.img_index = OPPONENT_DOWN_INDEX // 8
        screen.blit(OPPONENT.image[OPPONENT.img_index], OPPONENT.rect)
        OPPONENT_DOWN_INDEX += 1
        if OPPONENT_DOWN_INDEX > 47:
            RUNNING = False

    for CHALLENGERS_DOWN in CHALLENGER_DOWN:
        if CHALLENGERS_DOWN.down_index == 0:
            OPPONENT1_DOWN_SOUNDTEST.play()
        if CHALLENGERS_DOWN.down_index > 7:
            CHALLENGER_DOWN.remove(CHALLENGERS_DOWN)
            SCORE += 1000
            continue
        screen.blit(CHALLENGERS_DOWN.down_imgs[CHALLENGERS_DOWN.down_index // 2], CHALLENGERS_DOWN.rect)
        CHALLENGERS_DOWN.down_index += 1

    OPPONENT.bullets.draw(screen)
    CHALLENGER1.draw(screen)

    # Display score
    SCORE_FONT = pygame.font.Font(None, 36)
    SCORE_TXT = SCORE_FONT.render(str(SCORE), True, (255, 255, 0))
    TXT_AIRCRAFT = SCORE_TXT.get_rect()
    TXT_AIRCRAFT.topleft = [10, 10]
    screen.blit(SCORE_TXT, TXT_AIRCRAFT)

    pygame.display.update()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Key pressed events
    KEY_PRESSED_ENTER = pygame.key.get_pressed()

    if not OPPONENT.is_hit:
        if KEY_PRESSED_ENTER[K_r] or KEY_PRESSED_ENTER[K_UP]:
            OPPONENT.moveUp()
        if KEY_PRESSED_ENTER[K_f] or KEY_PRESSED_ENTER[K_DOWN]:
            OPPONENT.moveDown()
        if KEY_PRESSED_ENTER[K_d] or KEY_PRESSED_ENTER[K_LEFT]:
            OPPONENT.moveLeft()
        if KEY_PRESSED_ENTER[K_g] or KEY_PRESSED_ENTER[K_RIGHT]:
            OPPONENT.moveRight()

# Game over screen
FONT = pygame.font.Font(None, 60)
TXT = FONT.render('Score: ' + str(SCORE), True, (255, 255, 0))
TXT_AIRCRAFT = TXT.get_rect()
TXT_AIRCRAFT.centerx = screen.get_rect().centerx
TXT_AIRCRAFT.centery = screen.get_rect().centery + 24
screen.blit(GAME_OVER, (0, 0))
screen.blit(TXT, TXT_AIRCRAFT)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
