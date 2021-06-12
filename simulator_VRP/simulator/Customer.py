import pygame
from pygame.locals import *
from pygame.rect import *

import numpy as np

class Customer():
    def __init__(self,screen,location, rad=10):
        self.location = np.array(location)
        self.received = False
        self.screen = screen
        self.customer = Rect(list(self.location-[rad,rad])+[2*rad,2*rad])

        pygame.draw.ellipse(self.screen,(255, 0, 0),self.customer)

    def draw(self):
        if not self.received:
            pygame.draw.ellipse(self.screen,(255, 0, 0),self.customer)
        else:
            pygame.draw.ellipse(self.screen,(0, 255, 0),self.customer)