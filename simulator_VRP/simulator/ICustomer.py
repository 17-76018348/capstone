import pygame
from pygame.locals import *
from pygame.rect import *

import numpy as np

class Customer():
    def __init__(self,screen,location, rad=10):
        self.location = np.array(location)
        self.received = False
        self.screen = screen
        #self.customer = Rect(list(self.location-[rad,rad])+[2*rad,2*rad])

        self.home_wait = pygame.image.load("home.png")
        self.home_wait.convert()

        self.home_done = pygame.image.load("clear.png")
        self.home_done.convert()

        self.rect = self.home_wait.get_rect()
        self.rect.center = (location[0],location[1])
        self.screen.blit(self.home_wait,self.rect)

        self.count = 0
        self.flag = False

    def draw(self):
        if not self.received:
            self.screen.blit(self.home_wait,self.rect)
        else:
            self.screen.blit(self.home_done,self.rect)
            self.count += 1
            if self.count > 60:
                self.flag = True
            