import pygame
from pygame.locals import *
from pygame.rect import *
import numpy as np
import IVehicle
import ICustomer
import os

# screen setting
win_posx = 500
win_posy = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (win_posx, win_posy)
size = width, height = 800,600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('VRP visualizer')


# customer setting
target_node1 = [[300,200],[200,140],[200,60],[300,60],[500,140],[600,220],[700,220]]
target_id1 = [11,12,13,14,15,16,17]
target_node2 = [[300,380],[400,460],[500,540],[500,440],[600,440],[700,440],[600,340]]
target_id2 = [21,22,23,24,25,26,27]

customers = {}
for idx,id in enumerate(target_id1):
    customers[id] = ICustomer.Customer(screen,target_node1[idx])
for idx,id in enumerate(target_id2):
    customers[id] = ICustomer.Customer(screen,target_node2[idx])

# vehicle setting 
vehicle1 = IVehicle.Vehicle(screen,[400,300],target_node1,target_id1)
vehicle2 = IVehicle.Vehicle(screen,[400,300],target_node2,target_id2)
vehicles = [vehicle1,vehicle2]

# visualizing
clock = pygame.time.Clock()
pygame.init()
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
    screen.fill((204, 204, 255))

    for vehicle in vehicles:
        vehicle.draw_path()
        vehicle.move()
        if vehicle.isArrived():
            if len(vehicle.id) != 0:
                customers[vehicle.id[0]].received = True
                vehicle.id = vehicle.id[1:]

    for id in customers:
        customers[id].draw()
        
    pygame.display.flip()
    
pygame.quit()