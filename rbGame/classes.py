import rubato as rb
import objects, images
from constants import *
from rubato import Input, Color, Time, Vector, Manifold, Math

# Component overriding.

class PlayerController(rb.Component):
    def __init__(self, speed):

        super().__init__()  # you must call super().__init__()

        self.image = images.player
        self.rect = self.image.get_rect()
        self.speed = speed

        self.old_pos = None

        self.maxHealth = 100.00
        self.currentHealth = self.maxHealth
        self.energy = 0
        self.maxEnergy = 100

        

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
        if objects.collided:
            self.gameobj.pos = self.old_pos
            objects.collided = False
        else:
            self.old_pos = self.pos
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

    def __init__(self):
        super().__init__()
        self.image = images.demo_map
        self.rect = rb.Rectangle(2, 2, color=Color.white, z_index=1)
        self.image.scale = Vector.one*2

    def setup(self):
        self.gameobj.add(self.image)
        self.gameobj.z_index = TabScreenController.BEHIND
        self.gameobj.add(self.rect)

    def key_down(self):
        if rb.Input.key_pressed("tab"):
            objects.inTab = True
            self.gameobj.z_index = TabScreenController.FRONT

            # show our tab screen, and the players position on the map
        else:
            objects.inTab = False
            self.gameobj.z_index = TabScreenController.BEHIND

    def update(self):
        self.key_down()
        player_pos = objects.player.pos
        player_offset = player_pos-BASICLEVELSIZE/2
        dif = 2

        pos = Vector(12 * objects.currentChunk.x + 1, 12 * objects.currentChunk.y + 1)  # (posx, posy)

        # our position can be from 0 to 1000
        percentage = player_pos / 1000
        pos += Vector(Math.lerp(0, 9, percentage.x), Math.lerp(0, 9, percentage.y))
        pos *= dif
        self.rect.offset = pos-self.image.get_size()/2


    # image
    # update -> draw the player in the correct position
    # update -> if tab is pressed, bring z to front

    # z_index behind the background

class Collider(rb.Component):
    def __init__(self, image, collision_action):
        super().__init__()
        self.image: rb.Image = image
        self.rect = self.image.get_rect()
        self.collision_action = collision_action
        self.rect.on_collide = self.on_collide

    def setup(self):
        self.gameobj.add(self.image)
        self.gameobj.add(self.rect)

    def on_collide(self, manifold):
        if manifold.shape_b.gameobj.name == "player":
            self.collision_action()

def cactus_rules():
    objects.player.currentHealth -= 0.1
    objects.collided = True

def poison_rules():
    objects.player.currentHealth -= 1

def lava_rules():
    objects.player.currentHealth -= 0.2

decoration_z_index = -2

def spawn_cactus(chunk,pos):
    chunk.add(rb.wrap(Collider(images.cactus, cactus_rules), pos=pos, z_index=decoration_z_index))

def spawn_poison(chunk,pos):
    chunk.add(rb.wrap(Collider(images.poison, poison_rules), pos=pos, z_index=decoration_z_index))

def spawn_lava(chunk,pos):
    chunk.add(rb.wrap(Collider(images.lava, lava_rules), pos=pos, z_index=decoration_z_index))

def make_rect_collide_with_player(rect,on_collision):
    def on_collide(manifold):
        if manifold.shape_b.gameobj.name == "player":
            on_collision()
    rect.on_collide = on_collide

