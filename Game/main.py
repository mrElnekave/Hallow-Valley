import pygame, sys

WINDOWWIDTH = 500
WINDOWHEIGHT = 500
RATIO = WINDOWHEIGHT/WINDOWWIDTH
current_width = WINDOWWIDTH
current_height = WINDOWHEIGHT

while 1: 
    for event in pygame.event.get(pygame.QUIT):
        pygame.quit()
        sys.exit()
    for event in pygame.event.get(pygame.VIDEORESIZE):
        current_width = event.size[0]
        current_height = event.size[1]

