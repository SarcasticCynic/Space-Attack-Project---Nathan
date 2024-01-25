import math
import random

import pygame

# Initialize the pygame
pygame.init()

import sensors
import enemies
import players
import bullets

sensors = sensors.SensorArray()

# create the screen
gamebounds_X = 800
gamebounds_Y = 700
screen = pygame.display.set_mode((gamebounds_X, gamebounds_Y))

# Background
background = pygame.image.load('background.png')

# Sound
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.25)


# Caption and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

pygameClock = pygame.time.Clock()

# Player
active_players = []
destroyed_player_indices = []
userPlayer = players.Player(screen)
active_players.append(userPlayer)
sensors.addContact(userPlayer.X,userPlayer.Y,userPlayer,userPlayer.playerattr)

# Enemy
active_enemies = []
destroyed_enemy_indices = []
blasts = []
expiredBlasts = []
num_of_enemies = 1

orphaned_weapons = []
destroyed_weapons = []

# Score

score_value = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def showScore(x, y):
    score = score_font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def isWithinRange(enemyX, enemyY, bulletX, bulletY, detonationRange):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < detonationRange:
        return True
    else:
        return False


# Game Loop
running = True
game_over = False
FPS = 100
random.seed()
    

while running:
    pygameClock.tick(FPS)

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))

    # Background Image
    screen.blit(background, (0, 0))

    while ( not game_over and len(active_enemies) < num_of_enemies):
        enemySelect = random.randrange(2)
        if enemySelect == 0:
            active_enemies.append(enemies.Enemy(screen))
        elif enemySelect == 1:
            active_enemies.append(enemies.Enemy_mk2(screen))
        sensors.addContact(active_enemies[-1].X,active_enemies[-1].Y,active_enemies[-1],active_enemies[-1].enemyattr)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not game_over:
                    userPlayer.move_left()
            if event.key == pygame.K_RIGHT:
                if not game_over:
                    userPlayer.move_right()
            if event.key == pygame.K_1:
                userPlayer.selectWeapon(players.WeaponSelect.SLOT1)
            if event.key == pygame.K_2:
                userPlayer.selectWeapon(players.WeaponSelect.SLOT2)
            if event.key == pygame.K_3:
                userPlayer.selectWeapon(players.WeaponSelect.SLOT3)
            if event.key == pygame.K_SPACE:
                if not game_over:
                    userPlayer.fire()
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_EQUALS:
                pygame.mixer.music.stop()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                userPlayer.stop()

    if not game_over :
        # Enemy Movement
        for updatedEnemy in active_enemies :
            updatedEnemy.update()
        
        for player in active_players:
            player.update()

        for weapon in orphaned_weapons:
            weapon.update()

        # Collision
        active_weapons = []
        for player in active_players:
            for weapon in player.loadout[player.activeSlot] :
                if weapon.state == bullets.BulletState.FIRE:
                    active_weapons.append(weapon)
        for enemy in active_enemies:
            if enemy.loadoutType is not None:
                for weapon in enemy.loadout :
                    if weapon.state == bullets.BulletState.FIRE:
                        active_weapons.append(weapon)

        for weapon in orphaned_weapons:
            if weapon.state == bullets.BulletState.FIRE:
                active_weapons.append(weapon)
            else:
                assert(0)
        
        targets = active_enemies + active_players + active_weapons + orphaned_weapons

        detonation = False
        for weapon in active_weapons:
            if weapon.state == bullets.BulletState.FIRE:
                for target in targets:
                    if weapon.state != bullets.BulletState.FIRE:
                        break # to next weapon

                    if     weapon is target \
                        or target in destroyed_enemy_indices \
                        or target in destroyed_player_indices :
                        continue


                    if isWithinRange(target.X, target.Y, weapon.X, weapon.Y, weapon.detonationRange):
                        detonation = True
                        blasts.append(bullets.Blast(screen, weapon.X, weapon.Y, weapon.blastRadius))

                        for potentiallyDamagedEnemy in active_enemies :
                            if isWithinRange(potentiallyDamagedEnemy.X, potentiallyDamagedEnemy.Y, weapon.X, weapon.Y, weapon.blastRadius) :
                                if potentiallyDamagedEnemy not in destroyed_enemy_indices:
                                    destroyed_enemy_indices.append(potentiallyDamagedEnemy)
                                    score_value += 1
                                    if (score_value / 5) == int(score_value / 5):
                                        num_of_enemies += 1
                                    if (score_value / 20) == int(score_value/ 20):
                                        enemies.Enemy.defaultSpeedFactor *= 1.05
                                    if (score_value == 5):
                                        active_players.append(players.GroundLauncher(screen, userPlayer, 92))
                                        sensors.addContact(active_players[-1].X,active_players[-1].Y,active_players[-1],active_players[-1].playerattr)
                                    if (score_value == 10):
                                        active_players.append(players.GroundLauncher(screen, userPlayer, 644))
                                        sensors.addContact(active_players[-1].X,active_players[-1].Y,active_players[-1],active_players[-1].playerattr)

                        for potentiallyDamagedPlayer in active_players:
                            if isWithinRange(potentiallyDamagedPlayer.X, potentiallyDamagedPlayer.Y, weapon.X, weapon.Y, weapon.blastRadius) :
                                if potentiallyDamagedPlayer not in destroyed_player_indices:
                                    destroyed_player_indices.append(potentiallyDamagedPlayer)

                        for targetWeapon in active_weapons:
                            if target is targetWeapon:
                                targetWeapon.reset()


                        weapon.reset()
                    else:
                        if weapon.X < 0 or weapon.X > gamebounds_X or weapon.Y < 0 or weapon.Y > gamebounds_Y:
                            weapon.reset()

        if detonation:
            explosionSound = pygame.mixer.Sound("explosion.wav")
            explosionSound.play()

        for blast in blasts :
            if not blast.update() :
                expiredBlasts.append( blast )

        for destroyedPlayer in destroyed_player_indices :
            active_players.remove(destroyedPlayer)
            for weapon in destroyedEnemy.loadout:
                    if weapon.state == bullets.BulletState.FIRE:
                        orphaned_weapons.append(weapon)
            sensors.ridContact(destroyedPlayer)
        destroyed_player_indices = []

        for destroyedEnemy in destroyed_enemy_indices :
            if destroyedEnemy.loadoutType is not None:
                for weapon in destroyedEnemy.loadout:
                    if weapon.state == bullets.BulletState.FIRE:
                        orphaned_weapons.append(weapon)
            active_enemies.remove(destroyedEnemy)

            sensors.ridContact(destroyedEnemy)
        destroyed_enemy_indices = []

        for expiredBlast in expiredBlasts :
            blasts.remove( expiredBlast )
        expiredBlasts = []

        for weapon in orphaned_weapons:
            if weapon.state != bullets.BulletState.FIRE:
                destroyed_weapons.append(weapon)
        for weapon in destroyed_weapons:
            orphaned_weapons.remove(weapon)
            sensors.ridContact(weapon)
        destroyed_weapons = []


        # Game Over
        if userPlayer not in active_players:
            game_over = True
        for enemy in active_enemies :
            if enemy.Y > 440:
                game_over = True

        for enemy in active_enemies:
            sensors.updateContact(enemy.X,enemy.Y,enemy)
        for player in active_players:
            sensors.updateContact(player.X,player.Y,player)
        for weapon in active_weapons:
            sensors.updateContact(weapon.X,weapon.Y,weapon)

    if game_over :
        for enemy in active_enemies:
            enemy.clear()
        active_enemies.clear()
        for player in active_players:
            player.clear()
        game_over_text()

    showScore(textX, textY)
    pygame.display.update()
