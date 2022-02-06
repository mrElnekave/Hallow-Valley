import MapClasses 
import Enemies 
import objects
import pygame
import random
import time

file = {
    "chunks":
    {
        "chunk00": {
            "obstacles": [(250, 250)]
        },
        "chunk33": {
            "obstacles": [(100, 200)]
        }
    }
}

def createDungeon(index, boss, location, chunk, background, portal_image, name):
    objects.chunks[chunk[0]][chunk[1]].contents.append(
        MapClasses.CollisionButton(portal_image, location,
        ["objects.player.chunk = (-1,"+str(index)+")","objects.player.rect.center = (250,450)"]))
    objects.chunks[-1].append(MapClasses.Chunk((objects.mapWidth,0),
    background,
      (500,500),
      name))
    objects.chunks[-1][index].contents.append(boss)

# Creating List
for x in range(objects.mapWidth): 
    objects.chunks.append(list())
    for y in range(objects.mapHeight):
        objects.chunks[-1].append(MapClasses.Chunk((x,y), pygame.image.load("RPGGameMVP\Pixel Images\Grass.png"), (500,500), "Overworld"))
        enemyNum = random.randint(1,5)
        coinNum = 2
        if x == 3 and y == 3:
            coinNum = 4
        # if x != 0 or y != 0: 
        #     for e in range(enemyNum): 
        #         objects.chunks[x][y].contents.append(Enemies.Ghost((random.randint(100,400),random.randint(100,400))))
        for coin in range(coinNum): 
            objects.chunks[x][y].contents.append(MapClasses.Resource("coins", 10, (random.randint(0,500),random.randint(0,500))))

# Manual addition of objects to chunks
#objects.chunks[0][1].contents.append(
#            MapClasses.Obstacle(pygame.transform.scale(pygame.image.load("TestImage.png"), (50,50)), (250, 250))
#            )

# --------------------------------------------- HOUSE AND NPC
objects.chunks[0][0].contents.append(
    MapClasses.NPC(pygame.image.load("RPGGameMVP\Pixel Images\Player.png"), (100,100), [
        "if objects.resourceAmounts['coins'] >= 50: objects.player.currentHealth = objects.player.maxHealth;objects.resourceAmounts['coins'] -= 50"]))

# objects.chunks[0][0].contents.append(MapClasses.Building(pygame.image.load("RPGGameMVP\Pixel Images\House.png"), (100,0), 0, (24,50)))

objects.chunks[0][0].contents.append(MapClasses.NPC(pygame.image.load("RPGGameMVP\Pixel Images\Shop.png"), (400,400), ["objects.shopShowing = not objects.shopShowing", "time.sleep(0.1)"])) #TODO: Fix glitching and freeze game

# Subchunk list
objects.chunks.append(list())

# House in spawn area
objects.chunks[-1].append(MapClasses.Chunk((objects.mapWidth,0), pygame.image.load("RPGGameMVP\Pixel Images\HouseBackground.png"), (500,500), "Shop"))
objects.chunks[-1][0].contents.append(MapClasses.CollisionButton(pygame.image.load("RPGGameMVP\Pixel Images\DoorFromInside.png"), (250, 475), ["objects.player.chunk = (0,0)","objects.player.rect.center = (400,200)"]))

# Fire Boss Dungeon
createDungeon(1, Enemies.FireGhostBoss(), (250,250), (1,0), pygame.image.load("RPGGameMVP\Pixel Images\FireBossBackground.png"), pygame.image.load("RPGGameMVP\Pixel Images\FirePortal.png"), "fire dungeon")

# Ice Boss Dungeon
createDungeon(2, Enemies.IceGhostBoss(), (250,250), (0,1), pygame.image.load("RPGGameMVP\Pixel Images\Ice Boss Background.png"), pygame.image.load("RPGGameMVP\Pixel Images\Ice Portal.png"), "ice dungeon")


# Lightning Boss Dungeon
createDungeon(3, Enemies.LightningGhostBoss(), (250,250), (2,0), pygame.image.load("RPGGameMVP\Pixel Images\Lightning Boss Background.png"), pygame.image.load("RPGGameMVP\Pixel Images\Lightning Portal.png"), "lightning dungeon")

# Poison boss
createDungeon(4, Enemies.PoisonGhostBoss(), (250,250), (1,5),pygame.image.load("RPGGameMVP\Pixel Images\Poison Boss Background.png"), pygame.image.load("RPGGameMVP\Pixel Images\Poison Portal.png"), "poison dungeon")

# Summoning Boss 
createDungeon(5, Enemies.SummoningGhostBoss(), (250,250),(4,3),pygame.image.load("RPGGameMVP\Pixel Images\Grass.png"), pygame.image.load("RPGGameMVP\Pixel Images\Summoning Portal.png"), "summoning dungeon")

# Shield Boss 
createDungeon(6, Enemies.ShieldGhostBoss(), (250,250),(5,6),pygame.image.load("RPGGameMVP\Pixel Images\Grass.png"), pygame.image.load("RPGGameMVP\Pixel Images\Summoning Portal.png"), "shield dungeon")
objects.chunks[7][6].contents.append(MapClasses.MovementBarrier(pygame.transform.scale(pygame.image.load("RPGGameMVP\Pixel Images\WaterBase.png"), (500,100)),(250,250)))

# Laser Boss 
createDungeon(7, Enemies.LaserGhostBoss(), (250,250),(3,5),pygame.image.load("RPGGameMVP\Pixel Images\Grass.png"), pygame.image.load("RPGGameMVP\Pixel Images\FirePortal.png"), "laser dungeon")

# Water Boss 
createDungeon(8, Enemies.WaterGhostBoss(), (250,250),(1,4),pygame.image.load("RPGGameMVP\Pixel Images\Grass.png"), pygame.image.load("RPGGameMVP\Pixel Images\Ice Portal.png"), "water dungeon")
image = pygame.transform.scale(pygame.image.load("RPGGameMVP\Pixel Images\WaterBase.png"), (300,300))
image.set_alpha(10)
objects.chunks[7][8].contents.append(MapClasses.MovementBarrier(image,(250,250)))

# Final Boss 
createDungeon(9, Enemies.FinalBossGhost(), (250,250),(3,3),pygame.image.load("RPGGameMVP\Pixel Images\Grass.png"), pygame.image.load("RPGGameMVP\Pixel Images\Summoning Portal.png"), "final dungeon")

# objects.chunks[0][0].contents.append(MapClasses.Obstacle(pygame.image.load("RPGGameMVP\Pixel Images\House.png"), (250,250)))

for x in range(objects.mapWidth): 
    for y in range(objects.mapHeight):
        enemyNum = random.randint(1,5)
        if x != 0 or y != 0: 
            for e in range(enemyNum): 
                objects.chunks[x][y].contents.append(Enemies.Ghost((random.randint(100,400),random.randint(100,400))))

def load():
    position = file["chunks"]["chunk33"]["obstacles"][0]
    #objects.chunks[3][3].contents.append(
        #MapClasses.Obstacle(pygame.transform.scale(pygame.image.load("TestImage.png"), (50,50)), position)
        #)
