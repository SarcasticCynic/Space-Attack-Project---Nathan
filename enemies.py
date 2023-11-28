import random
import pygame

class Enemy() :
    defaultSpeedFactor = 1.0

    def __init__(self,screen) :
        self.image = pygame.image.load('enemy.png')
        self.X = random.randint(0, 736)
        self.Y = random.randint(50, 150)
        self.X_change = 4
        self.Y_change = 40
        self.screen = screen
        self.speedFactor = Enemy.defaultSpeedFactor

    def update(self) :
        self.X += self.X_change
        if self.X <= 0:
            self.X_change = (4 * self.speedFactor)
            self.Y += self.Y_change
        elif self.X >= 736:
            self.X_change = (-4 * self.speedFactor)
            self.Y += self.Y_change
        self.screen.blit(self.image, (self.X, self.Y))

    def clear(self):
        # set off-screen
        self.Y = 2000

class Enemy_Mk2 ():
    def __init__ (self, screen):
        super.__init__ (self, screen)
        self.image = pygame.image.load('enemy_mk2.png')