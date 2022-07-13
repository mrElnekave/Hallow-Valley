import rubato as rb
import random, webbrowser
from constants import *
import objects, images
from rubato import GameObject, Display

background = GameObject(pos=Display.center)
background.add(images.menu_base_dark)
background.add(images.menu_base_clear)
start_button = GameObject(pos=Vector(250, 450))
start_button.add(images.start_button)
start_button.add(rb.Button(width=images.start_button.get_size().x, height=images.about_us.get_size().y,
                           onclick=lambda: rb.Game.scenes.set(objects.main.id)))
about_us = GameObject(pos=Vector(250, 350))
about_us.add(images.about_us)
about_us.add(rb.Button(width=images.about_us.get_size().x, height=images.about_us.get_size().y,
             onclick=lambda: webbrowser.open
             ("https://docs.google.com/presentation/d/1fCRW8VGcp_BtFYz1E_SCKFJo4uPcnhw9mEK5d6gdftc/edit?usp=sharing")))
text = GameObject(pos=Vector(250, 150 + announcementFont.size / 2))
announcementFont.color = rb.Color(212, 175, 55)
text.add(rb.Text(text="Hallow Valley", font=announcementFont))


def lightning():
    timescale = random.random() * 2 + 0.5
    rb.Time.delayed_call(0 * timescale, images.switch_base)
    rb.Time.delayed_call(500 * timescale, images.switch_base)
    rb.Time.delayed_call(550 * timescale, images.switch_base)
    rb.Time.delayed_call(1000 * timescale, images.switch_base)
    rb.Time.delayed_call(random.randrange(5, 12) * 1000, lightning)


lightning()

objects.intro.add(background, start_button, about_us, text)
