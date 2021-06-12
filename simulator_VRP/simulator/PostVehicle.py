import pygame
from pygame.locals import *
from pygame.rect import *

import numpy as np

class Vehicle():
    def __init__(self,screen,start,target,rad=25):
        self.node_current = np.array(start)
        self.set_target(target)
        
        self.vehicle = Rect(list(self.node_current-[rad,rad])+[2*rad,2*rad])

        
        self.screen = screen
        
        pygame.draw.ellipse(self.screen,(0, 0, 255),self.vehicle)
        
    def move(self):
        self.vehicle.move_ip(self.speed)
        self.node_current = self.vehicle.center
        pygame.draw.ellipse(self.screen,(0, 0, 255),self.vehicle)
        
    def isArrived(self):
        distance = self.node_current - self.node_target
        distance = np.linalg.norm(distance)

        if distance < 1:
            self.set_target([500,500])
            return True
        else:
            return False
    
    def set_target(self,target):
        self.node_target = np.array(target)
        self.speed = list((self.node_target-self.node_current)/120)
