# at cycle:
# @PiThon Protectors @Python Vipers @Eco Hero

# python path
# ~\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\python.exe

import pygame, sys, objects, MapLoader, mathsets, rubato, music
mathsets.LoadMath()
from GameFunctions import *
from constants import *
import constants
pygame.init()

# Game Name: H@LLOW VALLEYs
objects.reports_on and objects.update_log.addMessage("REPORT: Welcome to the game. Your goal is to find 9 portals on the map and defeat the 9 bosses within them. Controls: arrow keys to move, click to shoot an arrow towards the mouse. Later in the game, when you have other abilities, you can press 1 to switch back to arrows. ")

# screen
current_width, current_height = constants.default_size

screen = pygame.display.set_mode(constants.default_size, pygame.RESIZABLE)
screen.fill((255,255,255))

# basic screen like resizing and such

def mapPosHelper(mx, my):
    x_offset = 0
    y_offset = 0
    mx = float(mx)
    my = float(my)
    ratio = current_height/current_width
    if ratio > 1: # height is too tall
        display_width = current_width
        display_height = display_width * RATIO
        y_offset = (current_height - display_height) / 2
    else:
        display_height = current_height 
        display_width = display_height / RATIO
        x_offset = (current_width - display_width) / 2
    mx = min(max(mx, x_offset), display_width + x_offset) - x_offset
    my = min(max(my, y_offset), display_height + y_offset) - y_offset
    return (mx/display_width) * WINDOWWIDTH, (my/display_height) * WINDOWHEIGHT

def mapMousePos(mousePos):
    mx, my = mousePos
    nx, ny = mapPosHelper(mx, my)
    
    return int(nx), int(ny)
objects.mapMousePos = mapMousePos


def input_basics():
    global screen, current_height, current_width
    for event in pygame.event.get(pygame.QUIT):
        pygame.quit()
        sys.exit()
    for event in pygame.event.get(pygame.VIDEORESIZE):
        current_width = event.size[0]
        current_height = event.size[1]
        screen = pygame.display.set_mode((current_width, current_height), pygame.RESIZABLE)
 
screen_update_frame = True
def screen_update():
    global screen, screen_update_frame
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
    if screen_update_frame:
        screen.blit(pygame.transform.scale(objects.display, (int(display_width), int(display_height))), (int(x_offset), int(y_offset)))
        pygame.display.update()
        screen.fill((0,0,0))
    # screen_update_frame = not screen_update_frame


# Game Loop
clock = pygame.time.Clock()
while 1: 
    input_basics()
    rubato.Time.process_calls()
    if objects.debugging: # Debugging code
        DebugCode()
    
    if objects.gamestate == 0: # Menu Code
        MenuUpdate()
        MenuRender()
    
    if objects.gamestate == 1: # Gameplay
        if objects.shopShowing:
            ShopUpdate()
        else:
            GameplayUpdate()

        GameplayRender()
        if objects.shopShowing:
            ShopRender()

    if objects.gamestate == 2: # Game Over
        GameOverUpdate()
        GameOverRender()

    if objects.gamestate == 3: # Question Cubes
        MathUpdate() 
        MathRender()

    screen_update()
    clock.tick(objects.framerate)
