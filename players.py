import pygame

class Player():
    def __init__ (self, screen):
        self.screen=screen
        self.X_change = 0
        self.X = 370
        self.Y = 480
        self.playerImg = pygame.image.load('Player.png')
    def update(self):
        self.X=self.X+self.X_change
        if self.X <= 0:
            self.X = 0
        elif self.X >= 736:
            self.X = 736
        self.screen.blit(self.playerImg,(self.X,self.Y))
    def move_left(self):
        self.X_change=-5
    def move_right(self):
        self.X_change=5