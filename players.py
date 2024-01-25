import enum
import random
import pygame
import bullets
import sensors

class WeaponSelect(enum.IntEnum):
    SLOT1 = 0
    SLOT2 = 1
    SLOT3 = 2
    SLOT4 = 3
    SLOT5 = 4
class Player():
    speedFactor = 1.0

    def __init__(self, screen, initX=370, initY=480,loadoutSize=5, magazineSize=5, image='player.png',\
                  font=pygame.font.Font('freesansbold.ttf', 32), loadoutX=310, loadoutY=10, fontColor=(255,255,255)):
        self.screen = screen
        self.image = pygame.image.load(image)
        self.emptyMagazineClickSound = pygame.mixer.Sound("empty_magazine_click.mp3")
        self.displayFont = font
        self.fontColor = fontColor
        self.sensors = sensors.SensorArray()
        self.X = initX
        self.Y = initY
        self.X_change = 0
        self.playerattr = {}
        self.playerattr["flags"] = ["isdestructable", "ismobile", "canshoot", "GOC", "issmart"] # GOC = Game Over Condition
        self.playerattr["unittype"] = ["teamplayer", "typeplayer"]
        self.loadout = []
        self.loadoutX = loadoutX
        self.loadoutY = loadoutY
        for x in range(loadoutSize):
            self.loadout.append([])

        for x in range(magazineSize):
            self.loadout[0].append( bullets.Bullet(screen=screen, Y=self.Y-45) )
            for munitions in self.loadout[0]:
                self.sensors.addContact(munitions.X,munitions.Y,munitions,munitions.bulletattr)
            if loadoutSize > 1:
                self.loadout[1].append( bullets.Bullet_mk2(screen=screen, Y=self.Y-45) )
                for munitions in self.loadout[1]:
                    self.sensors.addContact(munitions.X,munitions.Y,munitions,munitions.bulletattr)
            if loadoutSize > 2:
                self.loadout[2].append( bullets.Bullet_mk3(screen=screen, Y=self.Y-45) )
                for munitions in self.loadout[2]:
                    self.sensors.addContact(munitions.X,munitions.Y,munitions,munitions.bulletattr)

        self.activeSlot = WeaponSelect.SLOT1

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

        minCooldown = self.loadout[self.activeSlot][0].cooldownTime
        cooldownState = ""
        for weapon in self.loadout[self.activeSlot]:
            if weapon.state == bullets.BulletState.FIRE:
                weapon.update()
                cooldownState = cooldownState + "F"
                    
            elif weapon.state is bullets.BulletState.COOLDOWN :
                weapon.resolveCooldown()
                if weapon.remainingCooldownTime < minCooldown:
                    minCooldown = weapon.remainingCooldownTime
                cooldownState = cooldownState + "C"

            elif weapon.state is bullets.BulletState.READY:
                cooldownState = cooldownState + "R"

        self.screen.blit(self.image, (self.X, self.Y))
        loadoutText = self.displayFont.render(str(self.activeSlot + 1) + ": " + str(self.loadout[self.activeSlot][0].__class__.__name__) + f" {cooldownState} ({minCooldown})", True, self.fontColor)
        self.screen.blit(loadoutText, (self.loadoutX, self.loadoutY))

    
    def selectWeapon(self,select) :
        self.activeSlot = select


    def fire(self):
        for weapon in self.loadout[self.activeSlot]:
            if weapon.fire(self.X, self.Y, self.X_change):
                return
            
        # no bullet was READY
        if self.emptyMagazineClickSound is not None:
            self.emptyMagazineClickSound.play()

    def clear(self):
        # set off-screen
        self.Y = 2000
        self.update()

class GroundLauncher(Player):
    def __init__(self, screen, player, initX, initY=550, loadoutSize=1, magazineSize=1, image='turret.png', font=pygame.font.Font('freesansbold.ttf', 10), fontColor=(0,0,0)):
        super().__init__(screen, initX, initY, loadoutSize, magazineSize, image)
        self.emptyMagazineClickSound = None
        self.playerRef = player
        self.turretattr = {}
        self.turretattr["flags"] = ["isdestructable", "canshoot",]
        self.turretattr["unittype"] = ["teamplayer", "typeturret"]
        self.loadoutX = initX - 30
        self.loadoutY = initY + 70
        self.loadout[self.activeSlot][0].cooldownTime /= 2


    def move_left(self):
        self.stop()

    def move_right(self):
        self.stop()

    def fire(self):
        for key in sensors.SensorArray.contacts:
                    contact = sensors.SensorArray.contacts[key]
                    if "teamenemy" in contact.attrlist["unittype"] and ((contact.x_hysteresis[-1] < self.X and self.X - 20 < contact.x_hysteresis[-1]) or (contact.x_hysteresis[-1] > self.X and self.X + 20 > contact.x_hysteresis[-1])):
                        if (not (self.playerRef.X < self.X and self.X - 20 < self.playerRef.X)) and (not (self.playerRef.X > self.X and self.X + 20 > self.playerRef.X)):
                            super().fire()
                            break

    def update(self):
        self.fire()
        super().update()