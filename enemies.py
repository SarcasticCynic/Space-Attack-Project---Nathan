import pygame
import random

class Enemy():
    X_change=4
    Enemy_count=6
    spd_death_count = 0
    rein_death_count = 0
    def __init__(self,screen):
        self.screen=screen
        self.enemyImg = pygame.image.load('enemy.png')
        self.X = random.randint(0, 736)
        self.Y = random.randint(50, 150)
        self.enemyY_change = 40
        # This creates two separate X_change variables: one that tells the computer
        # To give all new enemies a certain X_change value, and one that is unique
        # To the instance so that individual enemies can change direction.
        self.X_change=Enemy.X_change
    def update(self):
        self.X+=self.X_change
        if self.X > 736:
            self.Y+=self.enemyY_change
            self.X_change=self.X_change * (-1)
        elif self.X < 0:
            self.Y+=self.enemyY_change
            self.X_change=self.X_change * (-1)
        self.screen.blit(self.enemyImg,(self.X,self.Y))
    def clear(self):
        self.Y=2000
        # This is the function used to increase the enemy speed
    def buff_spd(self):
        if Enemy.spd_death_count == 20:
            # This changes the speed for all new enemies
            Enemy.X_change=Enemy.X_change * 1.05
            # And this changes it for all current enemies
            for i in range(Enemy.Enemy_count):
                self.X_change=self.X_change * 1.05
            Enemy.spd_death_count = 0
    def reinforce(self):
        if Enemy.rein_death_count == 5:
            Enemy.Enemy_count += 1
            Enemy.rein_death_count = 0