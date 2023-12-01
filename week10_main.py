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

# Turrets
# They have to be defined here because if I wait until the score hits 
# The sufficient count, the game will NameError when it runs into the
# Code the turrets use.
active_turrets = []
for x in range (2):
    # Something's wrong with the second turret's X location, and I 
    # Can't figure it out for the life of me
    active_turrets.append(turrets.Turret (screen, ((x+1)*600/3)))





#sensors = sensors.SensorContacts()

# Enemy
active_enemies = []
destroyed_enemy_indices = []
num_of_enemies = 6

# Score

score_value = 40
score_font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = score_font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def isCollision(enemyX, enemyY, bulletX, bulletY, blast_radius):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < blast_radius:
        return True
    else:
        return False

# Game Loop
running = True
FPS = 100
    
while running:
    pygameClock.tick(FPS)
    for enemy_index in destroyed_enemy_indices :
        active_enemies.remove(enemy_index)
    destroyed_enemy_indices = []
    
    while (len(active_enemies) < num_of_enemies):
        active_enemies.append(enemies.Enemy_Mk2(screen))

    # We'll use this to get a dest_entity_count later
    enemy_bullet_count = 0
    for enemy in active_enemies:
        if enemy.klass != 1:
            enemy_bullet_count += 1


    # Assembling the list of bullets
    turret_compound_mag = []
    for x in range (2):
        turret_compound_mag.append(active_turrets[x].ammo)
    enemy_compound_mag = []
    for i in range (num_of_enemies):
        if active_enemies[i].klass != 1:
            enemy_compound_mag.append(active_enemies[i].ammo)
    non_player_compound_mag = []
    non_player_compound_mag.append(turret_compound_mag)
    non_player_compound_mag.append(enemy_compound_mag)
    universal_compound_mag = []
    universal_compound_mag.append(player.compound_magazine)
    universal_compound_mag.append(non_player_compound_mag)
    # These are in case we want to add more types of adversarial entities. 
    # It also makes the code a lot cleaner in the collision portion. 
    # Okay so maybe cleaner isn't the right word.
    enemy_team_entities = []
    enemy_team_entities.append(active_enemies)
    # This is for the same
    player_controlled_units = []
    player_controlled_units.append(player)
    player_team_entities = []
    player_team_entities.append(player_controlled_units)
    player_team_entities.append(active_turrets)
    nonbullet_entities = []
    nonbullet_entities.append(enemy_team_entities)
    nonbullet_entities.append(player_team_entities)
    destructible_entities = []
    destructible_entities.append(nonbullet_entities)
    destructible_entities.append(universal_compound_mag)

    # The math here: 16: 5 bullets * 3 magazines + 1 player. 4: 2 turrets + 2 bullets
    dest_entity_count = num_of_enemies + 16 + enemy_bullet_count + 4

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
        for j in range (num_of_enemies):
            if active_enemies[j].X > active_enemies[i].X + 100 or active_enemies[j].X > active_enemies[i].X - 100\
                or active_enemies[j].Y < active_enemies[i].Y:
                active_enemies[i].fire()
    # This is seperate so that it doesn't try to get dead enemies to fire bullets
    for category in destructible_entities:
        for type in category:
            for subtype in type:
                for item in subtype:
                        for mag_type in universal_compound_mag:
                            for mag in mag_type:
                                for bullet in mag:
                                    if bullet.state == bullets.BulletState.FIRE:
                                        if isCollision(item.X, item.Y, bullet.X, bullet.Y, bullet.blast_radius):
                                            if item is not bullet:
                                                explosionSound = pygame.mixer.Sound("explosion.wav")
                                                explosionSound.play()
                                                if item is player:
                                                    for x in range(num_of_enemies):
                                                        active_enemies[x].clear()
                                                    game_over_text()
                                                    break
                                                if isinstance (item, enemies.Enemy):
                                                    score_value += 1
                                                    if (score_value / 5) == int(score_value / 5):
                                                        num_of_enemies = num_of_enemies + 1
                                                    if (score_value / 20) == int(score_value/ 20):
                                                        enemies.Enemy.defaultSpeedFactor = enemies.Enemy.defaultSpeedFactor  * 1.05
                                                    destroyed_enemy_indices.append(item)
                                                if isinstance (item, bullets.Bullet):
                                                    item.reset()
                                                    bullet.reset()
                                                if bullet.detonate_type == bullets.Detonations.INSTANT:
                                                    bullet.reset()
                                                elif bullet.detonate_type == bullets.Detonations.DELAYED:
                                                    bullet.remove_at_round_end = True
                                        else:
                                            if bullet.Y <= 0:
                                                bullet.reset()
        



        '''for mag_type in universal_compound_mag:
            for mag in mag_type:
                for bullet in mag:
                    if bullet.state == bullets.BulletState.FIRE:
                        if isCollision(active_enemies[i].X, active_enemies[i].Y, bullet.X, bullet.Y, bullet.blast_radius):
                            explosionSound = pygame.mixer.Sound("explosion.wav")
                            explosionSound.play()
                            score_value += 1
                            if (score_value / 5) == int(score_value / 5):
                                num_of_enemies = num_of_enemies + 1
                            if (score_value / 20) == int(score_value/ 20):
                                enemies.Enemy.defaultSpeedFactor = enemies.Enemy.defaultSpeedFactor  * 1.05
                            destroyed_enemy_indices.append(i)
                            if bullet.detonate_type == bullets.Detonations.INSTANT:
                                bullet.reset()
                            elif bullet.detonate_type == bullets.Detonations.DELAYED:
                                bullet.remove_at_round_end = True
                        else:
                            if bullet.Y <= 0:
                                bullet.reset()'''
        # Turret Collision
    for mag in player.compound_magazine:
        for bullet in mag:
            if bullet.remove_at_round_end == True:
                bullet.reset()
                bullet.remove_at_round_end = False
    # Check to see if turrets triggered
    if score_value >= 50:
        active_turrets[0].activate()
    if score_value >= 100:
        active_turrets[1].activate()
    for weapon in active_turrets:
        weapon.update()
        if player.X < (weapon.X - 100) or player.X > (weapon.X + 100):
            if weapon.state == turrets.TurretState.ACTIVE:
                weapon.fire()
    player.update()
    show_score(textX, textY)
    pygame.display.update() 