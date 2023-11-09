import pygame

class BulletState (enumerate):
    FIRING = 0
    COOLDOWN = 1
    READY = 2

class Bullet():
    bulletY_change = 10  
    def __init__(self,screen):
        self.screen=screen
        self.Img = pygame.image.load("bullet.png")
        self.sound = pygame.mixer.Sound("laser.wav")
        self.Y = 480
        self.X = 0
        self.state=BulletState.READY
        self.cooldown_track = 0
    def fire(self,playerX):
        self.playerX=playerX
        self.X = playerX
        self.Y = 480
        self.sound.play()
        self.state=BulletState.FIRING
        self.cooldown_track = 100
    def reset(self):
        self.Y = 550
        self.X = 20
        self.state = BulletState.COOLDOWN
    def update(self):
        if self.state == BulletState.FIRING:
            pass
        elif self.cooldown_track == 0:
            self.state = BulletState.READY
        elif self.cooldown_track > 0:
            self.cooldown_track -= 1
        if self.state == BulletState.FIRING:
            self.Y-=self.bulletY_change
            self.screen.blit(self.Img,(self.X+16,self.Y+10))