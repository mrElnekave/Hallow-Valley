import pygame, sys
pygame.init()
import objects


current_width = WINDOWWIDTH
current_height = WINDOWHEIGHT


screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
screen.fill((255,255,255))


while 1: 
    screen.fill((255,255,255))
    for event in pygame.event.get(pygame.QUIT):
        pygame.quit()
        sys.exit()
    for event in pygame.event.get(pygame.VIDEORESIZE):
        current_width = event.size[0]
        current_height = event.size[1]
        screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
    
    ratio = current_height/current_width

    x_offset = 0
    y_offset = 0

    if ratio > 1: # height is too tall
        display_width = current_width
        display_height = display_width * RATIO
        y_offset = (current_height - display_height) / 2

    else:
        display_height = current_height 
        display_width = display_height / RATIO
        x_offset = (current_width - display_width) / 2

    screen.blit(pygame.transform.scale(display, (int(display_width), int(display_height))), (int(x_offset), int(y_offset)))
    pygame.display.update()

