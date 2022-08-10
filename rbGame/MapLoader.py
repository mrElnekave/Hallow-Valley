import objects
import rubato as rb
from rubato import Vector, Display
import map_description, classes, images#, MapClasses
import random

def add_to_chunk(gameObject, chunk: Vector):
    objects.chunks[chunk.x][chunk.y].add(gameObject)


def createDungeon(index, boss, location, chunk, background, portal_image, name):
    # create a button that moves the player to the dungeon
    # add the image of the dungeon to the button

    # add dungeon chunk to the chunk list
    # add the boss to the dungeon
    pass

# Creating Chunks
objects.mapHeight = len(map_description.map[0])
objects.mapWidth = len(map_description.map)

def from_chunk(surface, chunk):
    type_of_area = map_description.map[chunk[1]][chunk[0]]
    definitions = map_description.color_meaning_by_chunk[type_of_area]
    look_for_colors = definitions.keys()
    for x in range(10):
        for y in range(10):
            color_of_pixel = surface.get_at((x, y))[:-1]
            if color_of_pixel in look_for_colors:
                toInstantiate = definitions[color_of_pixel]
                objects.chunks[chunk[0]][chunk[1]].contents.append(
                    toInstantiate((x*50 + 25,y*50 + 25))
                )
                # instantiate right obstacle
                pass
    pass

def add_coins(chunk):
    for _ in range(4):
        coin_gameobj = rb.GameObject(pos=rb.Vector(random.randint(0,objects.BASICLEVELSIZE.x),random.randint(0,objects.BASICLEVELSIZE.y)))
        coin_component = classes.Coin()
        coin_gameobj.add(coin_component)
        chunk.add(coin_gameobj)

def load_chunks():
    for x_index in range(objects.mapWidth):
        objects.chunks.append(list())
        x_map = x_index * 10

        for y_index in range(objects.mapHeight):
            temp = rb.Scene(name=f"{x_index}_{y_index}")
            background = rb.wrap(images.maps[y_index][x_index], pos=Display.res, z_index=-10)
            temp.add(background)
            objects.chunks[-1].append(temp)
            add_coins(temp)


# --------------------------------------------- HOUSE AND NPC
# objects.chunks[0][0].contents.append(
#     MapClasses.NPC(pygame.image.load(create_path("Player2.png")), (100,100), [
#         "objects.player.changeSkin()"]))
#
#
# objects.chunks[0][0].contents.append(MapClasses.NPC(pygame.image.load(create_path("Shop.png")), (400,400), ["objects.shopShowing = not objects.shopShowing", "time.sleep(0.1)"])) #TODO: Fix glitching and freeze game
#
# # Subchunk list
# objects.chunks.append(list())
#
# # House in spawn area
# objects.chunks[-1].append(MapClasses.Chunk((objects.mapWidth,0), pygame.image.load(create_path("HouseBackground.png")), (500,500), "Shop"))
# objects.chunks[-1][0].contents.append(MapClasses.CollisionButton(pygame.image.load(create_path("DoorFromInside.png")), (250, 475), ["objects.player.chunk = (0,0)","objects.player.rect.center = (400,200)"]))
#
# # Fire Boss Dungeon
# data = map_description.portalLocations["fire"]
# createDungeon(1, Enemies.FireGhostBoss(), data[1], data[0], pygame.image.load(create_path("FireBossBackground.png")), pygame.image.load(create_path("FirePortal.png")), "Fire Dungeon")
#
# # Ice Boss Dungeon
# data = map_description.portalLocations["ice"]
# createDungeon(2, Enemies.IceGhostBoss(), data[1], data[0], pygame.image.load(create_path("Ice Boss Background.png")), pygame.image.load(create_path("Ice Portal.png")), "Ice Dungeon")
#
#
# # Lightning Boss Dungeon
# data = map_description.portalLocations["lightning"]
# createDungeon(3, Enemies.LightningGhostBoss(), data[1], data[0], pygame.image.load(create_path("Lightning Boss Background.png")), pygame.image.load(create_path("Lightning Portal.png")), "Lightning Dungeon")
#
# # Poison boss
# data = map_description.portalLocations["poison"]
# createDungeon(4, Enemies.PoisonGhostBoss(), data[1], data[0],pygame.image.load(create_path("Poison Boss Background.png")), pygame.image.load(create_path("Poison Portal.png")), "Poison Dungeon")
#
# # Summoning Boss
# data = map_description.portalLocations["summoner"]
# createDungeon(5, Enemies.SummoningGhostBoss(), data[1], data[0], pygame.image.load(create_path("Grass.png")), pygame.image.load(create_path("Summoning Portal.png")), "Summoning Dungeon")
#
# # Shield Boss
# data = map_description.portalLocations["shield"]
# createDungeon(6, Enemies.ShieldGhostBoss(), data[1], data[0],pygame.image.load(create_path("Grass.png")), pygame.image.load(create_path("Summoning Portal.png")), "Shield Dungeon")
# objects.chunks[15][6].contents.append(MapClasses.MovementBarrier(pygame.transform.scale(pygame.image.load(create_path("WaterBase.png")), (500,100)),(250,250)))
#
# # Laser Boss
# data = map_description.portalLocations["laser"]
# createDungeon(7, Enemies.LaserGhostBoss(), data[1], data[0],pygame.image.load(create_path("Grass.png")), pygame.image.load(create_path("FirePortal.png")), "Laser Dungeon")
#
# # Water Boss
# data = map_description.portalLocations["water"]
# createDungeon(8, Enemies.WaterGhostBoss(), data[1], data[0],pygame.image.load(create_path("Grass.png")), pygame.image.load(create_path("Ice Portal.png")), "Water Dungeon")
# image = pygame.transform.scale(pygame.image.load(create_path("WaterBase.png")), (300,300))
# image.set_alpha(10)
# objects.chunks[15][8].contents.append(MapClasses.MovementBarrier(image,(250,250)))
#
# # Final Boss
# data = map_description.portalLocations["final"]
# createDungeon(9, Enemies.FinalBossGhost(), data[1], data[0],pygame.image.load(create_path("Grass.png")), pygame.image.load(create_path("Summoning Portal.png")), "final dungeon")
#
# # objects.chunks[0][0].contents.append(MapClasses.Obstacle(pygame.image.load(create_path("House.png")), (250,250)))
#
# for x_index in range(objects.mapWidth):
#     for y_index in range(objects.mapHeight):
#         enemyNum = random.randint(1,5)
#         if x_index >= 2 or y_index >= 2:
#             for e in range(enemyNum):
#                 objects.chunks[x_index][y_index].contents.append(Enemies.Ghost((random.randint(100,400),random.randint(100,400))))
#
#
# # TESTING
#
# #objects.chunks[1][1].contents.append(special_obstacles.Lava((250,250)))
# #objects.chunks[0][0].contents.append(special_obstacles.Poison((250,250)))
# #objects.chunks[0][0].contents.append(special_obstacles.Cactus((150,250)))

