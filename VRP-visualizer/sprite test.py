import pygame as pyg

from pygame.locals import *
from pygame.rect import *

img_deliver = pyg.image.load("delivery.png")
img_deliver.convert()
rect = img_deliver.get_rect()
rect.center = 350,120
img_deliver = pyg.transform.rotozoom(img_deliver, 0, 0.1)
size = width, height = 700, 350
speed = [2,5]
screen = pyg.display.set_mode(size)
bgColor = (127,127,127)
caption = 'BG Color : ' + str(bgColor)
pyg.display.set_caption(caption)
screen.fill(bgColor)
pyg.display.update()
 
pyg.init()
 
 
clock = pyg.time.Clock()
 
running = True
while running:
    clock.tick(60)
 
    for pyEvent in pyg.event.get():
        if pyEvent.type == QUIT:
            running = False
    screen.fill(bgColor)
    screen.blit(img_deliver,rect)
    pyg.display.flip()
 
pyg.quit()
 