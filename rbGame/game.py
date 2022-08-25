import rubato as rb
import random, webbrowser
from constants import *
import objects, images, classes
import MapLoader, MapClasses
from rubato import GameObject, Display

MapLoader.load_chunks()
objects.main = objects.chunks[0][0]

follow_strength = .5

# player creation
objects.player = classes.PlayerController(moveSpeed)
player = GameObject(pos=Display.center, name="player")
objects.player_go = player
player.add(objects.player)

# tabscreen
objects.tabscreen = GameObject(pos=Display.center)
objects.tabscreen.add(classes.TabScreenController())

# ui
objects.ui = MapClasses.GameUI()


def camera_follow():
    target = objects.player.pos.clamp(Display.center, BASICLEVELSIZE - Display.center)
    rb.Game.camera.pos = rb.Game.camera.pos.lerp(target, follow_strength)


def update():
    camera_follow()
    objects.ui.update()
    if rb.Input.key_pressed("space"):
        objects.player.currentHealth -= 0.1



for row in objects.chunks:
    day_night = rb.wrap(MapClasses.DayNightCycle(), name="daynight", pos=Display.center)
    for chunk in row:
        chunk.update = update
        chunk.add(day_night)
        chunk.add_ui(objects.tabscreen)
        objects.ui.prime(chunk)
        chunk.add(objects.player_go)


classes.spawn_lava(objects.chunks[0][0],rb.Vector(200,200))
classes.spawn_cactus(objects.chunks[0][0],rb.Vector(300,300))
classes.spawn_poison(objects.chunks[0][0],rb.Vector(400,400))




# objects.main.add(player)
