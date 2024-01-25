import pygame
import enum
import sensors

class BulletState(enum.Enum):
        READY = 0    # Ready - You can't see the bullet on the screen
        FIRE = 1     # Fire - The bullet is currently moving
        COOLDOWN = 2 # Cooldown - bullet safely reloading


class Bullet() :

    speedFactor = 1.0

    def reset(self) :
        self.X = self.resetX
        self.Y = self.resetY
        self.X_change = self.resetX_change
        self.Y_change = self.resetY_change
        self.cooldownTime = self.resetCoolDownTime
        self.state = BulletState.COOLDOWN
        self.detectRadius = 27
        self.detonationRange = 27
        self.blastRadius = 27

    def __init__(self, screen, X=0, Y=480, X_change=0, Y_change=-10, cooldownTime=2000) :
        self.image = pygame.image.load('bullet.png')
        self.sound = pygame.mixer.Sound("laser.wav")
        self.sensors = sensors.SensorArray()

        self.resetX = X
        self.resetY = Y
        self.resetX_change = X_change
        self.resetY_change = Y_change
        self.resetCoolDownTime = cooldownTime
        self.reset()

        self.state = BulletState.READY
        self.fireTime = 0
        self.screen = screen

        self.bulletattr = {}
        self.bulletattr["flags"] = ["isdestructable", "ismobile",]
        self.bulletattr["unittype"] = ["teamnone", "typebullet"]

    def resolveCooldown(self):
        if self.state == BulletState.READY:
            return True
        elif self.state == BulletState.COOLDOWN:
            currentTime = pygame.time.get_ticks()
            if (currentTime - self.fireTime) > self.cooldownTime:
                self.state = BulletState.READY
                self.remainingCooldownTime = 0
            else:
                self.remainingCooldownTime = self.cooldownTime - (currentTime - self.fireTime)
                return False

            return True
        else:
            return False

    def update(self) :
        self.resolveCooldown()
        rotated_image = self.image
        if self.Y_change > 0:
            pygame.transform.rotate(self.image, 90)
            rotate_rect = self.image.get_rect().copy()
            rotate_rect.center = rotated_image.get_rect().center
            rotated_image = rotated_image.subsurface(rotate_rect).copy()
        self.screen.blit(rotated_image, (self.X + 16, self.Y + self.Y_change))
        self.Y += self.Y_change
        self.X += self.X_change

    def fire(self, x, y, inertia=0) :
        if self.resolveCooldown():
            self.state = BulletState.FIRE
            self.fireTime = pygame.time.get_ticks()
            self.sound.play()
            self.X = x
            self.Y = y + ((self.Y_change / abs(self.Y_change)) * max(self.detonationRange, self.blastRadius) + 1)

            self.update()
            return True
        else:
            return False

class Bullet_mk2(Bullet) :

    def fire(self, x, y, inertia):
        self.X_change = inertia
        return super().fire(x, y, inertia)

class Bullet_mk3(Bullet) :
    
    def reset(self) :
        super().reset()
        self.blastRadius = 40

class Blast() :

    def __init__(self,screen,x,y,radius,color=(255,0,0),linger=100) :
        self.screen = screen
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.linger = linger
        self.redStep   = self.color[0] / self.linger
        self.blueStep  = self.color[1] / self.linger
        self.greenStep = self.color[2] / self.linger

    def update(self) :
        if self.linger > 0 :
            pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.radius)
            red = self.color[0] - self.redStep
            blue = self.color[1] - self.blueStep
            green = self.color[2] - self.greenStep
            self.color = (red, green, blue)
            self.linger -= 1
            return True
        else :
            return False