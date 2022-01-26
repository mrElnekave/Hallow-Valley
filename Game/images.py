import pygame, constants
pygame.init()

pygame.display.set_mode(constants.default_size)
current_path = "Game\Pixel Images\\"

def load_img(path, colorkey=(255,255,255)):
    # path = os.path.join(current_path, path)
    print(current_path + path)
    img = pygame.image.load(current_path + path).convert()
    img.set_colorkey(colorkey)
    return img


# intro
small_bolt = load_img("small_bolt.png")
medium_bolt = load_img("medium_bolt.png")
large_bolt = load_img("large_bolt.png")

menu_base = pygame.transform.scale(load_img("main_menu.png"), constants.size)
mountain_1 = load_img("Title Screen Mountain.png", (0, 0, 0))
mountain_2 = load_img("Title Screen Mountain 2.png", (0, 0, 0))
mountain_3 = load_img("Title Screen Mountain 3.png", (0, 0, 0))
menu_base.blit(mountain_1, (-20, 200))
menu_base.blit(mountain_2, (200, 200))
menu_base.blit(mountain_3, (120, 200))



def darken_except(pic, pos):
    dark_picture = obscure(pic, (0,0,0), 200)
    pygame.draw.circle(dark_picture, (255, 255, 255), pos, 20)
    dark_picture.set_colorkey((255,255,255))
    pic.blit(dark_picture, (0, 0))
    pass


def obscure(pic, color, alpha):
    overlay = pygame.Surface(pic.get_size())
    overlay.fill(color)
    overlay.set_alpha(alpha)
    return overlay

