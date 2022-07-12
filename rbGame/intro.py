import rubato as rb
import objects
from constants import *
from rubato import GameObject, Display
import images

background = GameObject(pos = Display.center)
background.add(images.background)
start_button = GameObject(pos = Vector(250,450))
start_button.add(images.start_button)
start_button.add(rb.Button(width=images.start_button.get_size().x, height=images.about_us.get_size().y, onclick=lambda:rb.Game.scenes.set(objects.main.id)))
about_us = GameObject(pos = Vector(250,350))
about_us.add(images.about_us)
about_us.add(rb.Button(width = images.about_us.get_size().x, height = images.about_us.get_size().y))
text = GameObject(pos = Vector(250,150))
announcementFont.color = rb.Color(212,175,55)
text.add(rb.Text(text = "Hallow Valley", font=announcementFont))


objects.intro.add(background, start_button, about_us, text)

