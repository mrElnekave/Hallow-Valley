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
    "summoner":[(7,9),(250,250)],
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
    [((158,158,158), MapClasses.Obstacle)], #village
    [((244,67,54), special_obstacles.Lava ), ((66,66,66),MapClasses.Obstacle )], #Fire
    [((96,125,139), MapClasses.Obstacle )], #Ice
    [((121,85,72), MapClasses.Obstacle)], #Electric
    [((103,58,183), special_obstacles.Poison), ((158,158,158), MapClasses.Obstacle)], #Poison
    [((66,66,66), MapClasses.Obstacle)], #summoner
    [((96,125,139), MapClasses.Obstacle)], #shield
    [((121,85,72), MapClasses.Obstacle)], #laser
    [((76,175,80), special_obstacles.Cactus)], #water
    [((38,50,56),MapClasses.Obstacle)] #final
]



def look_at(start_x, start_y, chunk_type, coords):
    end_x = start_x + 10
    end_y = start_y + 10
    definitions = color_meaning_by_chunk[chunk_type]
    look_for_colors = [color_obstacle_pair[0] for color_obstacle_pair in definitions]

    for i in range(start_x, end_x):
        for j in range(start_y, end_y):
            color_of_pixel = images.demo_map.get_at((i, j))[:-1]
            try:
                index = look_for_colors.index(color_of_pixel)
            except ValueError:
                continue
            to_instantiate = definitions[index][1]
            try:
                if coords[0] > 3: continue
                if coords[1] > 3: continue

                print("instantiate", coords)
                objects.chunks[coords[0]][coords[1]].contents.append(
                    to_instantiate(i*10, j*10)
                )
            except:
                continue
            # instantiate this in the chunk


def load_map():
    for i in range(len(map)):
        row = map[i]
        start_y = 1 + 12 * i

        for j in range(len(row)):
            chunk_type = row[j]
            start_x = 1 + 12 * j

            look_at(start_x, start_y, chunk_type, (i, j))


if __name__ == "__main__":
    load_map()