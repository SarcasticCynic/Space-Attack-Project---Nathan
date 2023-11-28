import random
import pygame
import bullets

class WeaponState (enumerate):
    MK1 = 0
    MK2 = 1
    MK3 = 2
class Player():
    speedFactor = 1.0

    def __init__(self,screen):
        self.screen = screen
        self.image = pygame.image.load('player.png')
        self.emptyMagazineClickSound = pygame.mixer.Sound("empty_magazine_click.mp3")
        self.X = 370
        self.Y = 480
        self.X_change = 0
        self.mk1_magazine = []
        self.state = WeaponState.MK1
        for x in range(5):
            self.mk1_magazine.append( bullets.Bullet(screen) )
        self.mk2_magazine = []
        for x in range(5):
            self.mk2_magazine.append( bullets.Bullet_Mk2(screen))
        self.compound_magazine = []
        self.compound_magazine.append(self.mk1_magazine)
        self.compound_magazine.append(self.mk2_magazine)

    def move_left(self):
        self.X_change = -5

    def move_right(self):
        self.X_change = 5

    def stop(self):
        self.X_change = 0

    def update(self):
        self.X += self.X_change
        if self.X <= 0:
            self.X = 0
        elif self.X >= 736:
            self.X = 736

        for magazine in self.compound_magazine:
            for bullet in magazine:
                if bullet.state == bullets.BulletState.FIRE:
                    bullet.update()

                elif bullet.state is bullets.BulletState.COOLDOWN :
                    bullet.resolveCooldown()
#        for bullet in self.mk2_magazine:
#            if bullet.state == bullets.BulletState.FIRE:
#                bullet.update()
#                    
#            elif bullet.state is bullets.BulletState.COOLDOWN :
#                bullet.resolveCooldown()

        self.screen.blit(self.image, (self.X, self.Y))

    def fire(self):
        for magazine in self.compound_magazine:
            for bullet in magazine:
                if self.state == WeaponState.MK1:
                    try:
                        bullet.fire(self.X, self.Y)
                        return
                    except TypeError:
                        return
                if self.state == WeaponState.MK2:
                    try:
                        bullet.fire(self.X, self.Y, self.X_change)
                        return
                    except TypeError:
                        return
        # no bullet was READY
        self.emptyMagazineClickSound.play()
#    def fire_mk2(self):
#        for bullet in self.mk2_magazine:
#            if bullet.fire(self.X, self.Y, self.X_change):
#                return
#            
#        self.emptyMagazineClickSound.play()