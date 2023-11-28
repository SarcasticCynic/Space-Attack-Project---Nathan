import pygame
import players
import bullets

class TurretState (enumerate):
    INACTIVE = 0
    ACTIVE = 1

class Turret ():
    def __init__ (self, screen, X):
        self.screen = screen
        self.X = X
        self.Y = 1000
        self.state = TurretState.INACTIVE
        self.image = pygame.image.load('turret.png')
        self.ammo = bullets.Bullet(screen)
    def activate(self):
        self.state = TurretState.ACTIVE
        self.Y = 550
    def fire(self):
        self.ammo.fire(self.X, self.Y)
    def update(self):
        self.screen.blit(self.image, (self.X+30,self.Y+30))

