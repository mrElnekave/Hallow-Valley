import rubato as rb
import random, webbrowser
from constants import *
import objects, images, classes
from rubato import GameObject, Display

follow_strength = 5


# def camera_follow():
#     target = objects.player.pos.clamp(Display.center, BASICLEVELSIZE - Display.center)
#     rb.Game.camera.pos = rb.Game.camera.pos.lerp(target, follow_strength)
#
# objects.main.update = camera_follow

objects.player = classes.PlayerController(200)
player = GameObject(pos=Display.center)
player.add(objects.player)

objects.main.add(player)
