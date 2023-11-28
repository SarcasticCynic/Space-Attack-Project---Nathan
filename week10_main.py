import math
import random

import pygame

# Initialize the pygame
pygame.init()

#import sensors
import enemies
import players
import bullets
import turrets

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Sound
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)

# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

pygameClock = pygame.time.Clock()

# Player
player = players.Player(screen)

#sensors = sensors.SensorContacts()

# Enemy
active_enemies = []
destroyed_enemy_indices = []
num_of_enemies = 6

# Turrets
Turret1 = turrets.Turret (screen, 92)
Turret2 = turrets.Turret (screen, 644)

# Score

score_value = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Game Phase
phase = 1

def show_score(x, y):
    score = score_font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
FPS = 100
    
while running:
    pygameClock.tick(FPS)
    
    destroyed_enemy_indices.sort(reverse=True)
    for enemy_index in destroyed_enemy_indices :
        active_enemies.pop(enemy_index)
    destroyed_enemy_indices = []
    
    while (len(active_enemies) < num_of_enemies):
        active_enemies.append(enemies.Enemy(screen))

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.move_left()
            if event.key == pygame.K_RIGHT:
                player.move_right()
            if event.key == pygame.K_SPACE:
                player.fire()
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_1:
                player.state = players.WeaponState.MK1
            if event.key == pygame.K_2:
                player.state = players.WeaponState.MK2
            if event.key == pygame.K_3:
                player.state = players.WeaponState.MK3 

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.stop()

    # Enemy Movement
    for i in range(num_of_enemies):
        if active_enemies[i].Y > 440:
            # Game Over
            for j in range(num_of_enemies):
                active_enemies[j].clear()
            game_over_text()
            break

        active_enemies[i].update()
        
        # Player Mk1 Collision
        for bullet in player.mk1_magazine:
            if bullet.state == bullets.BulletState.FIRE:
                if isCollision(active_enemies[i].X, active_enemies[i].Y, bullet.X, bullet.Y):
                    explosionSound = pygame.mixer.Sound("explosion.wav")
                    explosionSound.play()
                    bullet.reset()
                    score_value += 1
                    if (score_value / 5) == int(score_value / 5):
                        num_of_enemies = num_of_enemies + 1
                    if (score_value / 20) == int(score_value/ 20):
                        enemies.Enemy.defaultSpeedFactor = enemies.Enemy.defaultSpeedFactor  * 1.05
                    destroyed_enemy_indices.append(i)
                else:
                    if bullet.Y <= 0:
                        bullet.reset()
        # Player Mk2 Collision
        for bullet in player.mk2_magazine:
            if bullet.state == bullets.BulletState.FIRE:
                if isCollision(active_enemies[i].X, active_enemies[i].Y, bullet.X, bullet.Y):
                    explosionSound = pygame.mixer.Sound("explosion.wav")
                    explosionSound.play()
                    bullet.reset()
                    score_value += 1
                    if (score_value / 5) == int(score_value / 5):
                        num_of_enemies = num_of_enemies + 1
                    if (score_value / 20) == int(score_value/ 20):
                        enemies.Enemy.defaultSpeedFactor = enemies.Enemy.defaultSpeedFactor  * 1.05
                    destroyed_enemy_indices.append(i)
                else:
                    if bullet.Y <= 0:
                        bullet.reset()

    # Check to see if phase 2/3 is triggered
    if score_value >= 50 and phase == 1:
        Turret1.activate()
        phase = 2
    if score_value >= 100 and phase == 2:
        Turret2.activate()
        phase = 3
    if Turret1.state == turrets.TurretState.ACTIVE:
        Turret1.update()
        Turret1.fire()
    if Turret2.state == turrets.TurretState.ACTIVE:
        Turret2.update()
        Turret2.fire()
    player.update()
    show_score(textX, textY)
    pygame.display.update()