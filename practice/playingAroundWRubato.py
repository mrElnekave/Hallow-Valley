import rubato as rb
rb.init()

# Rubato works on scenes
main_scene = rb.Scene()
rb.game.scenes.add(main_scene)

# objects in that scene
sprite = rb.Sprite().add_component(rb.Image())

# our general update for main
def main_update():
    # input
    # update
    pass
main_scene.update = main_update

# add all of our objects in the scene
main_scene.add(sprite)

# Start the game loop (always at the end)
rb.begin()
