import pygame
import enum
# Have to define screen in this file so that it uses the same "screen" variable as main
screen = pygame.display.set_mode((800, 600))
class BulletState (enumerate):
    # These don't have to be any particular value, so I'm defining the variable 
    # as the variable name as a string so that it doesn't collide with anything
    FIRE=0
    READY=1

class Bullet():
    # Imports the image and sound
    bulletImg=pygame.image.load("bullet.png")
    sound=pygame.mixer.Sound("laser.wav")
    #Removed bulletX_change b/c it was never used
    bulletY_change = 10
    # Initial X and Y value off the edge of the screen, so it doesn't colide with anything on accident
    X=0
    Y=480
    # Need it to have an initial state, otherwise main won't trigger the fire() function [main.py line 108]
    state=BulletState.READY
    # __init__ needs the display parameter to know which screen to draw the sprite on.
    # I had it as "screen", but changed it to display to disambiguify things.
    def __init__(self,display):
        self.display=display
    # The playerX parameter is named after the argument given it in [main.py line 110]
    def fire(self,playerX):
        self.playerX=playerX
        Bullet.X=playerX
        Bullet.sound.play()
        Bullet.state=BulletState.FIRE
    def reset(self):
        # Changes the bullet's Y value back to the original, off screen location.
        Bullet.Y=480
        Bullet.state=BulletState.READY
    def update(self):
        # Really irritated it won't let me reference local variables without using the "Bullet." prefix.
        # Is there some more convenient way I'm missing?
        Bullet.Y-=Bullet.bulletY_change
        # Defining the screen variable [bullet.py line 4] also saves a decent amount of space down here
        screen.blit(Bullet.bulletImg,(Bullet.X+16,Bullet.Y+10))