import rubato as rb
import intro
import images
import random
import copy

test_images = [images.stormCloud,images.clearCloud,images.small_bolt,images.medium_bolt,images.large_bolt]
rb.init(name="Untitled Collage",res=rb.Vector(360,360))
test_scene = rb.Scene(name="collage")
rb.Game.scenes.set(test_scene.id)

for _ in range(100):
    test_scene.add(rb.wrap(comp=copy.copy(random.choice(test_images)),pos=rb.Vector(random.randint(0,rb.Display.res.x),random.randint(0,rb.Display.res.y))))

rb.begin()
