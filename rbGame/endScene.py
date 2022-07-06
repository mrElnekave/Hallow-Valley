import rubato as rb
import objects

# Game Over Scene

game_over_bigFont = rb.Font(size=100,color=rb.Color(200,0,0))
game_over_smallFont = rb.Font(size=25,color=rb.Color(200,0,0))

game_over_background_gameobj = rb.GameObject(name="game over background", pos=rb.Display.center, z_index=-1)
game_over_background_rect = rb.Rectangle(width=objects.WIDTH,height=objects.HEIGHT,color=rb.Color(0,0,0))
game_over_background_gameobj.add(game_over_background_rect)

game_over_text_gameobj = rb.GameObject(name="game over text gameobj",pos=rb.Vector(rb.Display.center.x,rb.Display.center.y-100))
game_over_text = rb.Text(text="Game Over",font=game_over_bigFont)
game_over_text_gameobj.add(game_over_text)

game_over_text_gameobj_2 = rb.GameObject(name="game over text gameobj 2",pos=rb.Vector(rb.Display.center.x,rb.Display.center.y+100))
game_over_text_2 = rb.Text(text="Press C to continue",font=game_over_smallFont)
game_over_text_gameobj_2.add(game_over_text_2)

objects.game_over.add(game_over_background_gameobj, game_over_text_gameobj, game_over_text_gameobj_2)

def game_over_update():
    if rb.Input.key_pressed("c"):
        rb.Game.scenes.set(objects.intro.id)

objects.game_over.update = game_over_update

# Win Scene

win_bigFont = rb.Font(size=100,color=rb.Color(255,200,0))
win_smallFont = rb.Font(size=25,color=rb.Color(255,200,0))

win_background_gameobj = rb.GameObject(name="win background", pos=rb.Display.center, z_index=-1)
win_background_rect = rb.Rectangle(width=objects.WIDTH,height=objects.HEIGHT,color=rb.Color(255,255,255))
win_background_gameobj.add(win_background_rect)

win_text_gameobj = rb.GameObject(name="win text gameobj",pos=rb.Vector(rb.Display.center.x,rb.Display.center.y-100))
win_text = rb.Text(text="You Win!",font=win_bigFont)
win_text_gameobj.add(win_text)

win_text_gameobj_2 = rb.GameObject(name="win text gameobj 2",pos=rb.Vector(rb.Display.center.x,rb.Display.center.y+100))
win_text_2 = rb.Text(text="Exit and reopen the game to continue",font=win_smallFont)
win_text_gameobj_2.add(win_text_2)

objects.win.add(win_background_gameobj, win_text_gameobj, win_text_gameobj_2)
