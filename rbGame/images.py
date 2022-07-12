import rubato as rb
from rubato import Vector, Image

import constants, copy

current_path = constants.current_path + "Pixel Images\\"

def load_img(path, colorkey=(255,255,255), scale = Vector(1,1)):
    return rb.Image(rel_path=create_path(path),scale = scale)# size=colorkey=colorkey)

def create_path(path:str):
    """
    :param path:path is the relative path from the pixel images folder
    :return: the relative path from roots of project
    """
    return current_path + path


# intro
small_bolt = load_img("small_bolt.png", (0, 0, 0))
medium_bolt = load_img("medium_bolt.png", (0, 0, 0))
large_bolt = load_img("large_bolt.png", (0, 0, 0))
clearCloud = load_img("Clear Clouds.png")
stormCloud = load_img("Storm Clouds.png")
#background
menu_base_clear = load_img("menu_base_clear.png")
menu_base_dark = load_img("menu_base_dark.png")
background = load_img("main_menu_bg.png")
#buttons
about_us = load_img("AboutUsButton.png", scale=Vector(.4,.5))
start_button = load_img("StartButton.png")

'''
menu_base_clear = copy.copy(menu_base)
menu_base = menu_base_clear
menu_base_clear.blit(pygame.transform.scale(clearCloud, (60,20)), (15,20))
menu_base_clear.blit(pygame.transform.scale(clearCloud, (70,30)), (70,40))
menu_base_clear.blit(clearCloud, (120,0))
menu_base_clear.blit(pygame.transform.scale(clearCloud, (79,30)), (250,30))
menu_base_clear.blit(clearCloud, (275,0))

menu_base_dark = copy.copy(menu_base)

dark_picture = obscure(menu_base_dark, (0,0,0), 200)

# drawing on all the lightnings
menu_base_dark.blit(dark_picture, (0, 0))
menu_base_dark.blit(pygame.transform.scale(stormCloud, (60,20)), (15,20))
menu_base_dark.blit(pygame.transform.scale(stormCloud, (70,30)), (70,40))
menu_base_dark.blit(stormCloud, (120,0))
menu_base_dark.blit(pygame.transform.scale(stormCloud, (79,30)), (250,30))
menu_base_dark.blit(stormCloud, (275,0))
menu_base_dark.blit(small_bolt, (40, 40))
menu_base_dark.blit(small_bolt, (200, 50))

menu_base_dark.blit(medium_bolt, (100, 70))
menu_base_dark.blit(medium_bolt, (350, 10))

menu_base_dark.blit(medium_bolt, (150, 20))
menu_base_dark.blit(medium_bolt, (300, 60))


# map and notifs
demo_map = pygame.image.load(create_path("Demo Map.png")).convert()
demo_map = pygame.transform.scale(demo_map,(360,360))
demo_mask = demo_map.copy()
demo_mask.fill((0, 0, 0))
simple_map = pygame.image.load(create_path("Simple Map.png")).convert() # 150 by 150

lava = pygame.image.load(create_path("Lava.png"))
poison = pygame.image.load(create_path("Poison Lake.png"))
cactus = pygame.image.load(create_path("Cactus1.png"))
'''