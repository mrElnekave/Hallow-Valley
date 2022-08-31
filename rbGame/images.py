import rubato as rb
from rubato import Vector, Image
import constants, copy, map_description

current_path = constants.current_path + "Pixel Images\\"

def load_img(path, colorkey=(255,255,255), scale = Vector(1,1)):
    return Image(rel_path=create_path(path), scale=scale)# colorkey=colorkey)

def create_path(path:str):
    """
    :param path:path is the relative path from the pixel images folder
    :return: the relative path from roots of project
    """
    return current_path + path

def switch_base():
    if menu_base_clear.z_index == -1:
        menu_base_clear.z_index = -2
        menu_base_dark.z_index = -1
    else:
        menu_base_clear.z_index = -1
        menu_base_dark.z_index = -2


# intro
small_bolt = load_img("menu/small_bolt.png", (0, 0, 0))
medium_bolt = load_img("menu/medium_bolt.png", (0, 0, 0))
large_bolt = load_img("menu/large_bolt.png", (0, 0, 0))
clearCloud = load_img("menu/Clear Clouds.png")
stormCloud = load_img("menu/Storm Clouds.png")
# background
menu_base_clear = load_img("menu/menu_base_clear.png")
menu_base_clear.z_index = -1
menu_base_dark = load_img("menu/menu_base_dark.png")
menu_base_dark.z_index = -2
background = load_img("menu/main_menu_bg.png")  # useless unless custom cloud placement
# buttons
about_us = load_img("buttons/AboutUsButton.png", scale=Vector(.4,.5) * 1.5)
start_button = load_img("buttons/StartButton.png", scale=Vector.one * 1.5)
# player
player = load_img("skins/Player1.png")
# NPC
NPC = load_img("skins/Player.png")
#tabscreen
demo_map = load_img("map/Demo Map.png")
# maps
maps: list[list[rb.Image]] = []  # row column
for row in range(len(map_description.map)):
    maps.append(list())
    for col in range(len(map_description.map[0])):
        maps[row].append(load_img(f"map/map_{row}_{col}.png"))
        maps[row][col].z_index = -10
        maps[row][col].resize(constants.BASICLEVELSIZE)

lava = load_img("obstacles/Lava.png")
poison = load_img("obstacles/Poison Lake.png")
cactus = load_img("obstacles/Cactus1.png")

# enemies
ghost = load_img("skins/Ghost Enemy.png")
large_ghost = load_img("skins/Large Ghost.png")
fire_boss = load_img("skins/Fire Boss.png")
ice_boss = load_img("skins/Ice Boss.png")
lightning_boss = load_img("skins/Lightning Boss.png")
poison_boss = load_img("skins/Poison Boss.png")
summoning_boss = load_img("skins/Summoning Boss.png")
laser_boss = load_img("skins/Laser Boss.png")
neutral_final = load_img("skins/NeutralFB.png")
fire_final = load_img("skins/FireFB.png")
ice_final = load_img("skins/IceFB.png")
lightning_final = load_img("skins/LightningFB.png")
poison_final = load_img("skins/PoisonFB.png")
summoning_final = load_img("skins/SummoningFB.png")
shield_final = load_img("skins/ShieldFB.png")
laser_final = load_img("skins/LaserFB.png")
water_final = load_img("skins/WaterFB.png")

# backgrounds
fire_boss_bg = load_img("map/FireBossBackground.png")
# print(fire_boss_bg.get_pixel((0, 0)), "hi")

# coins
silver_coin = load_img("coins/Silver Coin.png")
gold_coin = load_img("coins/Gold Coin.png")
coin_images = [silver_coin, gold_coin]

# ui
help_button = load_img("buttons/Help Button.png")

# portal
portal = load_img("map/Summoning Portal.png")