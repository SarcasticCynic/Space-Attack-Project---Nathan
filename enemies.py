import enum
import random
import pygame
import sensors
import bullets


class Enemy() :
    defaultSpeedFactor = 1.0
    displayFont = pygame.font.Font('freesansbold.ttf', 16)
    counter = 0

    def __init__(self, screen, loadoutType=None, loadoutSize=0) :
        self.sensors = sensors.SensorArray()
        self.enemyattr = {}
        self.enemyattr["flags"] = ["isdestructable", "ismobile",]
        self.enemyattr["unittype"] = ["teamenemy", "typeenemy"] 
        self.image = pygame.image.load('enemy.png')
        self.X = random.randint(0, 736)
        self.Y = random.randint(50, 150)
        self.birth = pygame.time.get_ticks()
        self.screen = screen
        self.enemyId = Enemy.counter
        self.canevade = True
        self.loadoutType = loadoutType
        self.loadout = []
        if loadoutType is not None:
            for x in range(loadoutSize):
                self.loadout.append(loadoutType(screen=screen, Y_change=10))
                self.sensors.addContact(self.loadout[x].X, self.loadout[x].Y, self.loadout[x], self.loadout[x].bulletattr)
        self.autoFuse = random.randrange(10000)
        self.speedFactor = Enemy.defaultSpeedFactor
        if self.loadoutType is not None:
            self.speedFactor /= 2
        self.X_change = 4 * self.speedFactor
        self.Y_change = 40 * self.speedFactor
        Enemy.counter += 1

    def fire(self):
        if self.loadoutType is None:
            weaponState = "N"
        else:
            if self.loadout[0].state == bullets.BulletState.READY:
                weaponState = "R"
                currentTime = pygame.time.get_ticks()
                for key in sensors.SensorArray.contacts:
                    contact = sensors.SensorArray.contacts[key]
                    if "teamplayer" in contact.attrlist["unittype"] and ((contact.x_hysteresis[-1] < self.X and self.X + self.X_change < contact.x_hysteresis[-1]) or (contact.x_hysteresis[-1] > self.X and self.X + self.X_change > contact.x_hysteresis[-1])):
                        self.loadout[0].fire(self.X, self.Y, self.X_change)
                        self.speedFactor *= 1.5
                        break
            elif self.loadout[0].state == bullets.BulletState.FIRE:
                weaponState = "F"
                self.loadout[0].update()
            elif self.loadout[0].state == bullets.BulletState.COOLDOWN:
                weaponState = "C"
                

    def evade(self):
        if self.canevade == True and self.X > 40 and self.X < 696:
            for key in sensors.SensorArray.contacts:
                contact = sensors.SensorArray.contacts[key]
                if "typebullet" in contact.attrlist["unittype"] and (contact.y_hysteresis[-1] < self.Y) and ((contact.x_hysteresis[-1] < self.X and self.X - 20 < contact.x_hysteresis[-1]) or (contact.x_hysteresis[-1] > self.X and self.X + 20 > contact.x_hysteresis[-1])):
                    self.X_change *= -1
                    self.canevade = False
                    break

    def update(self) :
        self.X += self.X_change
        if self.X <= 0:
            self.X_change = (4 * self.speedFactor)
            self.Y += self.Y_change
            self.canevade = True
        elif self.X >= 736:
            self.X_change = (-4 * self.speedFactor)
            self.Y += self.Y_change
            self.canevade = True
        weaponState = ""
        self.fire()
        self.evade()

        self.screen.blit(self.image, (self.X, self.Y))
        displayId = self.displayFont.render(str(self.enemyId) + ": " + str(self.__class__.__name__) + f" {weaponState}", True, (255, 255, 255))
        self.screen.blit(displayId, (self.X, self.Y))

    def clear(self):
        # set off-screen
        self.Y = 2000
        self.update()

class Enemy_mk2(Enemy):
    def __init__(self,screen):
        loadoutType = None
        self.enemyattr = {}
        self.enemyattr["flags"] = ["isdestructable", "ismobile",]
        self.enemyattr["unittype"] = ["teamenemy", "typeenemy2"] 
        loadoutSelect = random.randrange(3)
        if loadoutSelect == 1:
            loadoutType = bullets.Bullet
            self.enemyattr["flags"].append("isarmed")
        if loadoutSelect == 2:
            loadoutType = bullets.Bullet_mk2
            self.enemyattr["flags"].append("isarmed2")



        super().__init__(screen,loadoutType, 1)