import random
import pygame
import bullets

class FireState (enumerate):
    LOADED = 0
    FIRED = 1
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
        self.screen.blit(self.image, (self.X + 32, self.Y +32))

    def clear(self):
        # set off-screen
        self.Y = 2000

class Enemy_Mk2 (Enemy):
    def __init__ (self, screen):
        super().__init__ (screen)
        #self.image = pygame.image.load('enemy_mk2.png')
        self.state = FireState.LOADED
        self.klass = random.randint(1,3)
        if self.klass == 2:
            self.ammo = bullets.Bullet (screen)
            self.ammo.Y_change = -10
            self.ammo.image = pygame.image.load('enemy_bullet.png')
            self.X_change = 2
            self.Y_change = 80
        if self.klass == 3:
            self.ammo = bullets.Bullet_Mk2 (screen)
            self.ammo.Y_change = -10
            self.ammo.image = pygame.image.load('enemy_bullet.png')
            self.X_change = 2
            self.Y_change = 80
    def fire(self):
        if self.state == FireState.LOADED:
            if self.klass == 2:
                self.ammo.fire(self.X,self.Y)
                self.Y_change = 60
                self.state = FireState.FIRED
            if self.klass == 3:
                self.ammo.fire(self.X,self.Y,self.X_change)
                self.Y_change = 60
                self.state = FireState.FIRED
    def update(self):
        self.X += self.X_change
        if self.klass == 1:
            if self.X <= 0:
                self.X = 0
                self.X_change = (4 * self.speedFactor)
                self.Y += self.Y_change
            elif self.X >= 736:
                self.X = 736
                self.X_change = (-4 * self.speedFactor)
                self.Y += self.Y_change
        elif self.state == FireState.LOADED:
            if self.X <= 0:
                self.X_change = (2 * self.speedFactor)
                self.Y += self.Y_change
            elif self.X >= 736:
                self.X_change = (-2 * self.speedFactor)
                self.Y += self.Y_change
        else:
            if self.X <= 0:
                self.X_change = (3 * self.speedFactor)
                self.Y += self.Y_change
            elif self.X >= 736:
                self.X_change = (-3 * self.speedFactor)
                self.Y += self.Y_change
        self.screen.blit(self.image, (self.X, self.Y))
        if self.state == FireState.FIRED:
            self.ammo.update()
