import pygame

class BulletState(enumerate):
        READY = 0    # Ready - You can't see the bullet on the screen
        FIRE = 1     # Fire - The bullet is currently moving
        COOLDOWN = 2 # Cooldown - bullet safely reloading


class Bullet() :

    speedFactor = 1.0

    def reset(self) :
        self.X = 0
        self.Y = 480
        self.X_change = 0
        self.Y_change = 10
        self.cooldownTime = 2000
        self.state = BulletState.COOLDOWN

    def __init__(self,screen) :
        self.image = pygame.image.load('bullet.png')
        self.sound = pygame.mixer.Sound("laser.wav")
        self.reset()
        self.state = BulletState.READY
        self.fireTime = 0
        self.screen = screen

    def resolveCooldown(self):
        self.currentTime = pygame.time.get_ticks()
        if self.state == BulletState.READY:
            return True
        elif self.state == BulletState.COOLDOWN and (( self.currentTime - self.fireTime) > self.cooldownTime):
            self.state = BulletState.READY
            return True
        else:
            return False

    def update(self) :
        self.resolveCooldown()
        self.screen.blit(self.image, (self.X + 16, self.Y + 10))
        self.Y = self.Y - self.Y_change
        self.X = self.X + self.X_change

    def fire(self, X, Y) :
        if self.resolveCooldown():
            self.state = BulletState.FIRE
            self.fireTime = pygame.time.get_ticks()
            self.sound.play()
            self.X = X
            self.Y = Y
            self.update()
            return True
        else:
            return False

class Bullet_Mk2 (Bullet):
    def fire (self, X, Y, host_X_change):
        if self.resolveCooldown():
            # Couldn't find a way to use super().fire() here,
            # But I probably could've looked harder
            self.X_change = host_X_change
            self.X = X
            self.Y = Y
            self.state = BulletState.FIRE
            self.fireTime = pygame.time.get_ticks()
            self.sound.play()
            self.update()
            return True
        else:
            return False
