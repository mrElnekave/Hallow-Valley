from traceback import print_tb
from numpy import imag
import images
import special_obstacles
import objects, pygame
from rubato import PMath, Vector

shownChunks = []
map=[
    [0,0,1,1,1,1,6,6,6,6,6,6,6,6,6],
    [0,0,1,1,1,1,6,6,6,6,6,6,6,6,6],
    [1,1,1,1,1,1,6,6,6,6,6,6,6,6,6],
    [4,1,1,1,1,1,1,1,3,3,3,3,3,3,3],
    [4,4,4,1,1,9,9,9,3,3,3,3,3,2,3],
    [4,4,4,4,4,9,9,9,9,3,3,3,2,2,2],
    [4,4,4,4,4,9,9,9,9,9,9,2,2,2,2],
    [4,4,4,4,4,9,9,9,9,9,9,2,2,2,2],
    [4,4,4,4,4,9,9,9,9,9,9,9,2,2,2],
    [4,4,4,4,4,4,5,5,5,9,5,5,2,2,2],
    [4,4,4,5,5,5,5,5,5,5,5,5,8,8,8],
    [4,4,7,5,5,5,5,5,5,5,8,8,8,8,8],
    [7,7,7,7,7,7,5,5,5,8,8,8,8,8,8],
    [7,7,7,7,7,7,8,8,8,8,8,8,8,8,8],
    [7,7,7,7,7,7,8,8,8,8,8,8,8,8,8],
]

portalLocations = {
    "fire":[(4,1),(250,250)],
    "ice":[(13,4),(250,250)],
    "lightning":[(14,4),(350,150)],
    "poison":[(0,6),(250,250)],
    "summoner":[(7,9),(250,300)],
    "shield":[(14,0),(250,250)],
    "laser":[(4,13),(250,250)],
    "water":[(13,14),(350,350)],
    "final":[(7,7),(250,250)]
}

location_log = {
    0 : "town",
    1 : "fire",
    2 : "ice",
    3 : "lightning",
    4 : "poison",
    5 : "summoner",
    6 : "shield",
    7 : "laser",
    8 : "water",
    9 : "final"
}

inv_map = {v: k for k, v in location_log.items()}


color_meaning_by_chunk = [
    {(158,158,158): special_obstacles.InvisibleObj}, #village
    {(244,67,54): special_obstacles.Lava, (66,66,66): special_obstacles.InvisibleObj }, #Fire
    {(96,125,139): special_obstacles.InvisibleObj}, #Ice
    {(121,85,72): special_obstacles.InvisibleObj}, #Electric
    {(103,58,183): special_obstacles.Poison, (158,158,158): special_obstacles.InvisibleObj}, #Poison
    {(66,66,66): special_obstacles.InvisibleObj}, #summoner
    {(96,125,139): special_obstacles.InvisibleObj}, #shield
    {(121,85,72): special_obstacles.InvisibleObj}, #laser
    {(76,175,80): special_obstacles.Cactus}, #water
    {(38,50,56): special_obstacles.InvisibleObj} #final
]

def show_chunk(col,row):
    # show_type should use show_chunk
    dif = 2
    color = (1, 2, 3)
    posx = 12 * col + 1
    posy = 12 * row + 1

    pygame.draw.rect(images.demo_mask, color, pygame.Rect(posx * dif, posy * dif, 10 * dif, 10 * dif))
    images.demo_mask.set_colorkey(color)


def show_type(type):
    dif = 2
    item = inv_map[type]
    for row in range(len(map)):
        for col in range(len(map[0])):
            if map[row][col] == item:
                show_chunk(col,row)
                '''# we need to unblock
                color = (1, 2, 3)
                posx = 12 * col + 1
                posy = 12 * row + 1

                pygame.draw.rect(images.demo_mask, color, pygame.Rect(posx * dif, posy * dif, 10 * dif, 10 * dif))
                images.demo_mask.set_colorkey(color)'''

def playerPosOnMap(playerPos, col, row, location):
    dif = 2

    pos = Vector(12 * col + 1, 12 * row + 1)  # (posx, posy)

    # our position can be from 0 to 500
    percentage = Vector(*playerPos) / 500
    pos += Vector(PMath.lerp(0, 9, percentage.x), PMath.lerp(0, 9, percentage.y))
    pos *= dif
    pos += Vector(*location)


    # should draw onto the screen instead
    # check the position and further testing.
    pygame.draw.rect(objects.display, (255, 255, 255), pygame.Rect(round(pos.x), round(pos.y), 
        *((Vector.ONE * Vector(dif, dif)).to_tuple()))
    )



def clear_chunk(chunk_pos):
    current_chunk = objects.chunks[chunk_pos[0]][chunk_pos[1]]
    bad_types: list = ["unassigned", "fireball", "abilityObject"]
    for obj in current_chunk.contents:
        if obj.type in bad_types:
            current_chunk.contents.remove(obj)
