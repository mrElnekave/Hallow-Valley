import rubato as rb
import intro
import images


rb.init(name="Untitled Collage")
test_scene = rb.Scene(name="collage")
rb.Game.scenes.set(test_scene.id)


gameobj = rb.wrap(comp=images.stormCloud,pos=rb.Display.center)
test_scene.add(gameobj)

rb.begin()
