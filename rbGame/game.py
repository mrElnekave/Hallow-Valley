import rubato as rb
import random, webbrowser
from constants import *
import objects, images, classes
import MapLoader, MapClasses
from rubato import GameObject, Display

MapLoader.load_chunks()
objects.main = objects.chunks[0][0]

follow_strength = .5

def camera_follow():
    target = objects.player.pos.clamp(Display.center, BASICLEVELSIZE - Display.center)
    rb.Game.camera.pos = rb.Game.camera.pos.lerp(target, follow_strength)


def update():
    camera_follow()


for row in objects.chunks:
    day_night = rb.wrap(MapClasses.DayNightCycle(), name="daynight", pos=Display.center)
    for chunk in row:
        chunk.update = update
        chunk.add(day_night)

objects.player = classes.PlayerController(moveSpeed)
player = GameObject(pos=Display.center)
objects.player_go = player
player.add(objects.player)
# go = rb.wrap(comp=images.maps[0][0], pos=Display.res)
# print(go)





objects.main.add(player)
