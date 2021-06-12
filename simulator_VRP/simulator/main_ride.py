import pygame
from pygame.locals import *
from pygame.rect import *
import numpy as np
import IVehicle
import ICustomer
import os

# screen setting
win_posx = 100
win_posy = 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (win_posx, win_posy)
size = width, height = 1600 , 900
screen = pygame.display.set_mode(size)
pygame.display.set_caption('VRP visualizer')
background = pygame.image.load("./map.png")

# customer setting
target_node1 = [[411, 293],[253, 407],[327, 493],[591, 470],[783, 481],[450, 824],[198, 174]]
target_id1 = [11,12,13,14,15,16,17]
target_node2 = [[1354, 688],[1299, 817],[1006, 819],[922, 811],[1028, 383],[896, 139],[1133, 20]]
target_id2 = [21,22,23,24,25,26,27]

customers = {0:{}, 1:{}}
for idx,id in enumerate(target_id1):
    customers[0][id] = ICustomer.Customer(screen,target_node1[idx])
for idx,id in enumerate(target_id2):
    customers[1][id] = ICustomer.Customer(screen,target_node2[idx])

customers2 = {0:{}, 1:{}}

# vehicle setting 
vehicle1 = IVehicle.Vehicle(screen,[500,200],target_node1,target_id1,(200,0,0))
vehicle2 = IVehicle.Vehicle(screen,[1300, 450],target_node2,target_id2,(0,200,0))
vehicles = [vehicle1,vehicle2]
counter_show = 0

flag_cus = True
flag_veh = True

# visualizing
clock = pygame.time.Clock()
pygame.init()
running = True
while running:
    clock.tick(60)
    counter_show += 1
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    screen.blit(background, (0, 0))

    if counter_show > 60 and flag_veh:
        for idx, vehicle in enumerate(vehicles):
            vehicle.draw_path()
            vehicle.move()
            if vehicle.isArrived():
                if len(vehicle.id) != 0:
                    customers[idx][vehicle.id[0]].received = True
                    vehicle.id = vehicle.id[1:]
    if flag_veh == False:
        for idx, vehicle in enumerate(vehicles):
            vehicle.draw_path()
            vehicle.move()
            if vehicle.isArrived():
                if len(vehicle.id) != 0:
                    customers2[idx][vehicle.id[0]].received = True
                    vehicle.id = vehicle.id[1:]

    if vehicle1.count_done == 2 and flag_cus==True:
        target_node1 = [[783, 481],[450, 824],[191, 679],[198, 174]]
        target_id1 = [14,15,16,17]
        target_node2 = [[1028, 383],[896, 139],[1133, 20],[1441, 651]]
        target_id2 = [24,25,26,27] 
        flag_cus = False

        for idx,id in enumerate(target_id1):
            customers2[0][id] = ICustomer.Customer(screen,target_node1[idx])
        for idx,id in enumerate(target_id2):
            customers2[1][id] = ICustomer.Customer(screen,target_node2[idx])

    if vehicle1.count_done == 4 and flag_veh == True:
        node1_current = vehicle1.node_current
        node2_current = vehicle2.node_current
        vehicle1 = IVehicle.Vehicle(screen,node1_current,target_node1,target_id1,(200,0,0))
        vehicle2 = IVehicle.Vehicle(screen,node2_current,target_node2,target_id2,(0,200,0))
        vehicles = [vehicle1,vehicle2]
        flag_veh = False
    
    if counter_show > 30 and flag_veh:
        for rider in customers:
            for id in customers[rider]:
                if customers[rider][id].flag == True:
                    pass
                else:
                    customers[rider][id].draw()
    
    if flag_cus == False:
        for rider in customers:
            for id in customers2[rider]:
                if customers2[rider][id].flag == True:
                    pass
                else:
                    customers2[rider][id].draw()
        
    pygame.display.flip()
    
pygame.quit()