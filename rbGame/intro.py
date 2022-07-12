import rubato as rb
import objects
from constants import *
from rubato import GameObject, Display

background = GameObject(pos = Display.center)
background.add(rb.Image(rel_path="Data/Pixel Images/main_menu_bg.png"))
start_button = GameObject(pos = Vector(250,450))
start_button.add(img:= rb.Image(rel_path="Data/Pixel Images/StartButton.png"))
start_button.add(rb.Button(width=img.get_size().x, height=img.get_size().y, onclick=lambda:rb.Game.scenes.set(objects.main.id)))
help_button = GameObject(pos = Vector(480,80))
help_button.add(rb.Image(rel_path="Data/Pixel Images/Help Button.png"))
about_us = GameObject(pos = Vector(250,350))
about_us.add(img:= rb.Image(rel_path = "Data/Pixel Images/AboutUsButton.png", scale=Vector(.4,.5)))
about_us.add(rb.Button(width = img.get_size().x, height = img.get_size().y))


objects.intro.add(background)
objects.intro.add(start_button)
objects.intro.add(about_us)
objects.intro.add(help_button)
