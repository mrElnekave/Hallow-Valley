import pygame, sys
pygame.init()

WINDOWWIDTH = 500
WINDOWHEIGHT = 500
RATIO = WINDOWHEIGHT/WINDOWWIDTH
current_width = WINDOWWIDTH
current_height = WINDOWHEIGHT


screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
screen.fill((255,255,255))
display = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
display.fill((0, 0, 0))

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

    if ratio > 1: # height is too tall
        display_width = current_width
        display_height = display_width * RATIO
    else:
        display_height = current_height 
        display_width = display_height / RATIO

    screen.blit(pygame.transform.scale(display, (int(display_width), int(display_height))), (0, 0))
    pygame.display.update()

