import math
import random

import pygame

# Intialize the pygame
pygame.init()

import bullets
import enemies
import players

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

# Player
player = players.Player(screen)

# Enemy
active_enemies = []
destroyed_enemy_indices = []

# Score

score_value = 0
scrore_font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = scrore_font.render("Score : " + str(score_value), True, (255, 255, 255))
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
pygameClock = pygame.time.Clock()
projectiles = [bullets.Bullet(screen),\
               bullets.Bullet(screen),\
               bullets.Bullet(screen),\
               bullets.Bullet(screen),\
               bullets.Bullet(screen)]
num_of_bullets = 5

while running:
    pygameClock.tick(FPS)
    
    for enemy_index in destroyed_enemy_indices :
        active_enemies.pop(enemy_index)
    destroyed_enemy_indices = []
    
    while (len(active_enemies) < enemies.Enemy.Enemy_count):
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
                for k in range(num_of_bullets):
                    if projectiles[k].state is bullets.BulletState.READY:
                        for l in range(num_of_bullets):
                            if projectiles[l].state == bullets.BulletState.READY:
                                projectiles[l].state = bullets.BulletState.COOLDOWN
                                projectiles[l].cooldown_track += 10
                        projectiles[k].fire(player.X)
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.X_change = 0


    # Enemy Movement
    for i in range(enemies.Enemy.Enemy_count):

        # Game Over
        if active_enemies[i].Y > 440:
            for j in range(enemies.Enemy.Enemy_count):
                active_enemies[j].clear()
            game_over_text()
            break

        active_enemies[i].update()
        
        # Collision
        for k in range(num_of_bullets):
            if isCollision(active_enemies[i].X, active_enemies[i].Y, projectiles[k].X, projectiles[k].Y):
                explosionSound = pygame.mixer.Sound("explosion.wav")
                explosionSound.play()
                projectiles[k].reset()
                score_value += 1
                # Had to put the value in enemies.Enemy so that buff_spd() could reset it, 
                # but had to reference it here in order to increment it per collision.
                enemies.Enemy.spd_death_count += 1
                # Same here
                enemies.Enemy.rein_death_count += 1
                destroyed_enemy_indices.append(i)
            active_enemies[i].buff_spd()
            active_enemies[i].reinforce()



    # Bullet Movement
    for k in range(num_of_bullets):
        if projectiles[k].Y <= 0:
            projectiles[k].reset()
        if projectiles[k].state is not bullets.BulletState.READY :
            projectiles[k].update()

    player.update()
    show_score(textX, textY)
    pygame.display.update()
