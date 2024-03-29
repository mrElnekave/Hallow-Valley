import pygame, constants, copy
# pygame.init()

pygame.display.set_mode(constants.default_size)
current_path = constants.current_path + "Pixel Images\\"

def load_img(path, colorkey=(255,255,255)):
    img = pygame.image.load(current_path + path).convert()
    img.set_colorkey(colorkey)
    return img

def create_path(path:str):
    """
    :param path:path is the relative path from the pixel images folder
    :return: the relative path from roots of project
    """
    return current_path + path

def darken_except(pic, pos):
    dark_picture = obscure(pic, (0,0,0), 200)
    pygame.draw.circle(dark_picture, (255, 255, 255), pos, 20)
    dark_picture.set_colorkey((255,255,255))
    pic.blit(dark_picture, (0, 0))
    pass

def switch_base():
    global menu_base
    if menu_base == menu_base_dark:
        menu_base = menu_base_clear
    else:
        menu_base = menu_base_dark

def obscure(pic, color, alpha):
    overlay = pygame.Surface(pic.get_size())
    overlay.fill(color)
    overlay.set_alpha(alpha)
    return overlay

# intro
small_bolt = load_img("small_bolt.png", (0, 0, 0))
medium_bolt = load_img("medium_bolt.png", (0, 0, 0))
large_bolt = load_img("large_bolt.png", (0, 0, 0))
clearCloud = pygame.image.load(create_path("Clear Clouds.png"))
stormCloud = pygame.image.load(create_path("Storm Clouds.png"))

mountain_range_height = 200

menu_base = pygame.transform.scale(load_img("main_menu.png"), constants.size)
mountain_1 = load_img("Title Screen Mountain.png", (0, 0, 0))
mountain_2 = load_img("Title Screen Mountain 2.png", (0, 0, 0))
mountain_3 = load_img("Title Screen Mountain 3.png", (0, 0, 0))
pygame.draw.rect(menu_base, (139, 195, 74), pygame.Rect((0,mountain_range_height + mountain_1.get_height() - 20), menu_base.get_size()))

menu_base.blit(mountain_1, (-20, mountain_range_height))
menu_base.blit(mountain_2, (200, mountain_range_height))
menu_base.blit(mountain_3, (120, mountain_range_height))


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
pygame.image.save(menu_base_dark, "../rbGame/Data/Pixel Images/menu/menu_base_dark.png")
pygame.image.save(menu_base_clear, "../rbGame/Data/Pixel Images/menu/menu_base_clear.png")
# map and notifs
demo_map = pygame.image.load(create_path("Demo Map.png")).convert()
demo_map = pygame.transform.scale(demo_map,(360,360))
demo_mask = demo_map.copy()
demo_mask.fill((0, 0, 0))
simple_map = pygame.image.load(create_path("Simple Map.png")).convert() # 150 by 150

lava = pygame.image.load(create_path("Lava.png"))
poison = pygame.image.load(create_path("Poison Lake.png"))
cactus = pygame.image.load(create_path("Cactus1.png"))
