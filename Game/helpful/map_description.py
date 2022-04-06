import images
import MapClasses
import special_obstacles
import objects, pygame


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
