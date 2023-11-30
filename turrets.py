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
        self.ammo.cooldownTime = 1000
    def activate(self):
        self.state = TurretState.ACTIVE
        self.Y = 550
    def fire(self):
        self.ammo.fire(self.X, self.Y)
    def update(self):
        self.screen.blit(self.image, (self.X,self.Y + 30))
        if self.ammo.state == bullets.BulletState.FIRE or self.ammo.state == bullets.BulletState.FIRING:
            self.ammo.update()

        elif self.ammo.state is bullets.BulletState.COOLDOWN :
            self.ammo.resolveCooldown()

