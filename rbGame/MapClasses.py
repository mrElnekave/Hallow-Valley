import objects
import random
from images import create_path
import images
import rubato as rb
from rubato import Component, GameObject, Vector
import images

class DayNightCycle(Component):  # TODO: add to GO
    def __init__(self):
        super().__init__()
        self.day = True

        self.darkness_overlay = None

    def switch_day_night(self):
        self.day = not self.day
        # TODO: if its day, hide darkness
        rb.Time.delayed_call(1000 * 10, self.switch_day_night)

    def setup(self):
        rb.Time.delayed_call(1000 * 10, self.switch_day_night)

class Coin(Component):

    values = [5, 10]

    # assign gold or silver
    # value when picked up
    def __init__(self):
        super().__init__()
        self.coin_type = random.randint(0,1)
        self.value = Coin.values[self.coin_type]
        self.image = images.coin_images[self.coin_type] #TODO once fixed .clone()
        self.rect = self.image.get_rect()


    # add the correct image to its game object
    def setup(self):
        self.gameobj.add(self.image)
        self.gameobj.add(self.rect)
        self.rect.on_collide = self.on_collide

    # rect which on collision deletes the coin
    def on_collide(self, manifold):
        if manifold.shape_b.gameobj.name == "player":
            objects.chunks[objects.currentChunk.y][objects.currentChunk.x].delete(self.gameobj) #TODO: figure out why we aren't deleting (Note: This can break the game, our guess is that it is when you collect a coin and get rid of it as you swap chunks)
            self.gameobj.z_index = -100
            objects.resourceAmounts["coins"] += self.value

class NPC(Component):
    # create a rect and add to GO
    def __init__(self, image, effects):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.effects = effects
        self.canClick = True
    def setup(self):
        self.gameobj.add(self.image)
        self.gameobj.add(self.rect)
    def update(self): 
        if self.canClick: 
            if rb.Input.mouse_state()[0]:
                # if the mouse pressed

                rb.world_mouse()
                if self.rect.top_left <= rb.world_mouse() <= self.rect.bottom_right: 
                    objects.NPC_clicked = True
                    self.effects()
                    self.canClick = False
                    rb.Time.delayed_call(1000, self.setCanClick)
    def setCanClick(self): 
        self.canClick = True

# A script runs all the time, and will the game objects moving them around.
# TODO: Make the UI manager a script, holding different Game Objects.
class GameUI:
    INFRONT = 10
    # all the UI IMAGES
    # TEXT
    def __init__(self):
        self.help_button = images.help_button
        self.health = rb.Text(text="Health: "+str(objects.player.currentHealth)+"/"+str(objects.player.maxHealth), font=objects.myFont)
        self.ghost_energy = rb.Text(text="Ghost Energy: "+str(objects.player.energy)+"/"+str(objects.player.maxEnergy), font=objects.myFont)
        self.health_bar_bg = rb.Rectangle(width=200,height=20, color = rb.Color.black)
        self.health_bar = rb.Rectangle(width=200,height=20, color = rb.Color(0,255,0))
        self.ghost_energy_bar = rb.Rectangle(width=200,height=20, color=rb.Color.blue)
        self.ghost_energy_bar_bg = rb.Rectangle(width=200,height=20, color=rb.Color.black)

        self.gos = []
        self.gos.append(rb.wrap(self.health, pos=rb.Vector(rb.Display.center.x*0.4,rb.Display.center.y/10), z_index=GameUI.INFRONT))
        self.gos.append(rb.wrap(self.help_button, "help", pos=Vector(), z_index=GameUI.INFRONT)) # TODO: max pos for help button
        self.gos.append(rb.wrap(self.ghost_energy, pos=rb.Vector(rb.Display.center.x*0.4,rb.Display.center.y/5), z_index=GameUI.INFRONT))
        self.gos.append(rb.wrap(self.health_bar_bg, z_index = GameUI.INFRONT+1))
        self.gos.append(rb.wrap(self.health_bar, z_index = GameUI.INFRONT+1))
        self.gos.append(rb.wrap(self.ghost_energy_bar_bg, z_index=GameUI.INFRONT+1))
        self.gos.append(rb.wrap(self.ghost_energy_bar, z_index=GameUI.INFRONT+1))
        self.health_bar.top_left = rb.Vector(300,0)
        self.health_bar_bg.top_left = rb.Vector(300,0)
        self.ghost_energy_bar.top_left = rb.Vector(300,20)
        self.ghost_energy_bar_bg.top_left = rb.Vector(300,20)
    def prime(self, scene):
        scene.add_ui(*self.gos)

    def update(self): #Fix UI bar so that it moves according to player health, each time width changes, need to set top left
        self.health.text = f"Health: {objects.player.currentHealth: .2f}/{objects.player.maxHealth: .2f}"
        self.health_bar.width = rb.Math.clamp(objects.player.currentHealth/objects.player.maxHealth*200, 0, 200)
        self.health_bar.top_left = rb.Vector(300,0)
    def draw(self, camera): # THIS IS BAD
        # draw the text
        # Health
        rb.Draw.queue_text(text="Health: "+str(objects.player.currentHealth)+"/"+str(objects.player.maxHealth), font=objects.myFont, pos=rb.Vector(rb.Display.center.x*0.4,rb.Display.center.y/10), z_index=10)
        rb.Draw.queue_rect(width=200,height=20,center=rb.Vector(375,rb.Display.center.y/10),fill=rb.Color.black,z_index=11)
        rb.Draw.queue_rect(width=int(200*objects.player.currentHealth/objects.player.maxHealth), height=20, center=rb.Vector(275+100*objects.player.currentHealth/objects.player.maxHealth, rb.Display.center.y / 10), fill=rb.Color(0,255,0),z_index=12)
        # Ghost Energy
        rb.Draw.queue_text(text="Ghost Energy: "+str(objects.player.energy)+"/"+str(objects.player.maxEnergy), font=objects.myFont, pos=rb.Vector(rb.Display.center.x*0.4,rb.Display.center.y/5), z_index=10)
        rb.Draw.queue_rect(width=200,height=20,center=rb.Vector(375,rb.Display.center.y/5),fill=rb.Color.black,z_index=11)
        rb.Draw.queue_rect(width=int(200*objects.player.energy/objects.player.maxEnergy), height=20, center=rb.Vector(275+100*objects.player.energy/objects.player.maxEnergy, rb.Display.center.y / 5), fill=rb.Color(0,0,255),z_index=12)


# class UpdateLog(Obj):
#     def __init__(self, location, archives):
#         self.capsule = pygame.Surface((175, 25))
#         self.capsule.fill((0, 0, 0))
#         self.exclamation_black = pygame.image.load(create_path("Notification Button.png"))
#         self.exclamation_white = pygame.image.load(create_path("White Notification Button.png"))
#         self.exclamation = self.exclamation_black
#         self.image = pygame.Surface((1, 1))  # just for super
#         self.text = None
#         self.tab_start = rb.Vector(100, 100)
#
#         super().__init__(self.image, location)
#         self.message: str = ""
#         self.archived = archives
#
#     def in_relation(self, x, y):
#         return (self.rect.x + x, self.rect.y + y)
#
#     #if player in dungeon: return
#     def render(self):
#         if objects.player.chunk[0] != -1:
#             blit_alpha(objects.display, self.capsule, self.in_relation(25, 0), 10)
#             # if self.text != None:
#             #     objects.display.blit(self.text, self.in_relation(25, 0))
#             objects.display.blit(self.exclamation, self.in_relation(0, 0))
#
#     def tabRender(self):
#         for i in range(len(self.archived)):
#             message = self.clamp_message(self.archived[i])
#             image = objects.myFont.render(message, True, (200,0,0))
#             objects.display.blit(self.image, self.tab_in_relation(0, i*objects.myFont.get_height()))
#
#     def tab_in_relation(self, x, y):
#         return self.tab_start.x + x, self.tab_start.y + y
#
#     def regenerate_image(self):
#         message = self.clamp_message(self.message)
#         self.text = objects.myFont.render(message, True, (200,0,0))
#
#     def clamp_message(self, message):
#         text_width, text_height = objects.myFont.size(message)
#
#         while text_width > self.capsule.get_size()[0] - 5:
#             text_width, text_height = objects.myFont.size(message)
#             message = message[:-1]
#         return message
#
#     def addMessage(self, message: str):
#         self.archived.append(message)
#         self.message = message
#         self.regenerate_image()
#         # def todo():
#         #     self.log.remove(message)
#         #     self.regenerate_image()
#         #     print("TODONE")
#         # rb.Time.delayed_call(5 * 1000, todo)
#
# class Building(Obj):
#     def __init__(self, image, location, subchunk, doorSize):
#         super().__init__(image, location)
#         self.subchunk = subchunk
#         self.type = "building"
#         self.doorRect = pygame.Rect((0,0), doorSize)
#         self.doorRect.midbottom = self.rect.midbottom
#     def update(self):
#         if objects.player.rect.colliderect(self.doorRect):
#             objects.player.chunk = (objects.mapWidth, self.subchunk)
#             objects.player.rect.center = (250, 425)
#
#
#         #for obj in objects.currentChunk.contents:
#         #    if obj.type in self.interact:
#         #        if self.rect.colliderect(obj.rect):
#         #            if obj.type == "projectile":
#         #                objects.currentChunk.contents.remove(obj)
#         #if self.rect.colliderect(objects.player.rect):
#         #    if objects.player.rect.center = objects.player.last_valid_position
#
# class CollisionButton(Obj):
#     def __init__(self, image, location, effects):
#         self.effects = effects
#         super().__init__(image, location)
#         self.type = "collisionButton"
#     def update(self):
#         if objects.player.rect.colliderect(self.rect):
#             objects.player.cancel_abilities()
#             for effect in self.effects:
#                 exec(effect)
#
# class QuestionCube(Obj):
#     boosts = [
#         ["objects.player.currentHealth += 25", 25, "25 health"],
#         ["objects.resourceAmounts['ghostEnergy'] += 25", 50,"25 ghost energy"],
#         ["objects.moveSpeed = 10; rb.Time.delayed_call(10*1000, QuestionCube.decrement_speed)", 60,"a speed boost"],
#         ["objects.resourceAmounts['purple'] += 1", 65,"a purple potion"],
#         ["objects.resourceAmounts['red'] += 1", 67,"a red potion"],
#         ["objects.resourceAmounts['blue'] += 1", 69,"a blue potion"],
#         ["objects.resourceAmounts['gold'] += 1", 70,"a gold potion"],
#         ]
#     count = 0
#     @staticmethod
#     def decrement_speed():
#         objects.moveSpeed = 5
#     def __init__(self, location):
#         image = pygame.image.load(create_path("QuestionCube.png"))
#         super().__init__(image, location)
#         self.type = "qcube"
#     def update(self):
#         if objects.player.rect.colliderect(self.rect):
#             objects.currentChunk.contents.remove(self)
#             QuestionCube.count += 1
#         if QuestionCube.count >= 5:
#             objects.gamestate = 3
#             QuestionCube.count -= 5
#             objects.currentProblem = random.choice(objects.problems)
#
#     @staticmethod
#     def randBoost():
#         choice = random.randint(1,70)
#         for boost in QuestionCube.boosts:
#             if choice <= boost[1]:
#                 exec(boost[0])
#                 objects.update_log.addMessage("You used 5 question cubes and got..."+boost[2]+"!")
#                 return
