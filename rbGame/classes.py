import rubato as rb
import objects, images
from constants import *
from rubato import Input, Color, Time, Vector, Manifold

# Component overriding.

class PlayerController(rb.Component):
    def __init__(self, speed):

        super().__init__()  # you must call super().__init__()

        self.image = images.player
        self.rect = self.image.get_rect()
        self.speed = speed

    @property
    def pos(self):  # TODO: explain next class properly
        return self.gameobj.pos

    @pos.setter
    def pos(self, new):
        self.gameobj.pos = new

    def setup(self):
        """
        Here you have access to the GameObject of the component and is where you should set any variables that depend
        on the GameObject.
        Automatically run once before the first update call.
        """
        # Only here can we get the rect from our game object and assign the image

        # resizing our image to our hitbox's size
        # self.image.resize(Vector(50, 50))
        self.gameobj.add(self.image)
        self.gameobj.add(self.rect)

    def update(self):
        """
        Called once per frame. Before the draw function.
        """
        # We moved the input into here. And changed it all to use delta_time
        if Input.key_pressed("a"):
            self.gameobj.pos.x -= self.speed * Time.delta_time
        if Input.key_pressed("w"):
            self.gameobj.pos.y -= self.speed * Time.delta_time
        if Input.key_pressed("s"):
            self.gameobj.pos.y += self.speed * Time.delta_time
        if Input.key_pressed("d"):
            self.gameobj.pos.x += self.speed * Time.delta_time

        # self.gameobj.pos = self.gameobj.pos.clamp(Vector.zero + self.image.get_size() / 2,
        #                                           BASICLEVELSIZE - self.image.get_size() / 2)
        if self.gameobj.pos.x < 0:
            if objects.switch_chunk("left"):
                self.gameobj.pos.x = BASICLEVELSIZE.x - self.image.get_size().x / 2
            else:
                self.gameobj.pos.x = 0
        if self.gameobj.pos.y < 0:
            if objects.switch_chunk("up"):
                self.gameobj.pos.y = BASICLEVELSIZE.y
            else:
                self.gameobj.pos.y = 0
        if self.gameobj.pos.x > BASICLEVELSIZE.x:
            if objects.switch_chunk("right"):
                self.gameobj.pos.x = 0
            else:
                self.gameobj.pos.x = BASICLEVELSIZE.x
        if self.gameobj.pos.y > BASICLEVELSIZE.y:
            if objects.switch_chunk("down"):
                self.gameobj.pos.y = 0
            else:
                self.gameobj.pos.y = BASICLEVELSIZE.y

class EnemyController(rb.Component):
    def __init__(self):
        super().__init__()
        self.image = rb.Image(rel_path="../art/Ghost Enemy.png")
        self.rect = rb.Rectangle(width=self.image.get_size().x, height=self.image.get_size().y)
        self.speed = 20

    def setup(self):
        self.gameobj.add(self.image)
        self.gameobj.add(self.rect)

    def update(self):
        pos = self.gameobj.pos
        direction = pos.dir_to(objects.player.pos)
        self.gameobj.pos += direction * (self.speed * Time.delta_time)


class TabScreenController(rb.Component):
    BEHIND = -100
    FRONT = 100

    def key_down():
        if rb.Input.key_pressed("tab"):
            objects.inTab = True

            # show our tab screen, and the players position on the map
            print("hi")
        else:
            objects.inTab = False
    # image
    # update -> draw the player in the correct position
    # update -> if tab is pressed, bring z to front

    # z_index behind the background

