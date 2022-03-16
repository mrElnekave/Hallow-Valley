from tkinter import N
from tkinter.messagebox import NO
import pygame
import objects
import random
import math
import time
import webbrowser
import Abilities
from BasicClasses import Obj
from images import create_path
import rubato as rb

# Quest System Steps

# 1) Somewhere to remember all of our quests - List
# 2) A format to save our quests that has the completions state and the instructions - Class
#    Things the quests need to know: Instructions, Quest complete state
# 3) A way to display our quests, either in pause menu or on the UI - A part of gameFunctions
# 4) Creating all of our quests main and side - A document/file or somthing

# Reset Main Boss Functionality
# 1) Pause our other functionality - State machine
# 2) Setup a 

# Chunks of the map
class Chunk: 
    def __init__(self, location, image, size, chunk_type: str):
        self.location = location
        self.contents = []
        self.image = image
        self.image = pygame.transform.scale(self.image, size)
        if self.location[0] != 7: 
            for i in range(10): 
                self.image.blit(pygame.image.load(create_path("TallGrass.png")), (random.randint(0,500),random.randint(0,500)))
                
        self.rect = self.image.get_rect()
        self.nightOverlay = pygame.Surface(objects.size)
        self.nightOverlay.fill((0,0,50))
        self.chunk_type = chunk_type
    def render(self):
        objects.display.blit(self.image, self.rect)
        for resource in self.contents: 
            resource.render()
        if self.location[0] is not objects.mapWidth and objects.daytime is False:
            self.nightOverlay.set_alpha(100)
            objects.display.blit(self.nightOverlay, (0,0))
    def update(self): 
        for thing in self.contents:
            thing.update()
    
    def __repr__(self):
        if self.location[0]== objects.mapWidth: 
            return f"{self.chunk_type}"
        return f"{self.location} {self.chunk_type}"
        
class Quest:
    def __init__(self, text, condition, name): # all inputs are strings
        self.text = text 
        self.condition = condition 
        self.name = name 
        self.data = 0
        self.complete = False
    def render(self):
        pass

    def update(self):
        if eval(self.condition): 
            self.complete = True

# Resource Class
class Resource(Obj): 
    def __init__(self, item, quantity, location):
        super().__init__(pygame.image.load(create_path("Gold Coin.png")), location)
        self.item = item
        self.quantity = quantity
        self.type = "resource"
    def update(self):
        if objects.player.rect.colliderect(self.rect):
            objects.currentChunk.contents.remove(self)
            objects.resourceAmounts["coins"] += 10

class Obstacle(Obj): 
    def __init__(self, image, location): 
        super().__init__(image, location)
        self.type = "obstacle"
        self.interact = ["arrow"]
    def update(self):
        if self.rect.colliderect(objects.player.rect): 
            objects.player.hit_this_frame = True

class MovementBarrier(Obj): 
    def __init__(self, image, location): 
        super().__init__(image, location)
        self.type = "obstacle"
    def update(self):
        if self.rect.colliderect(objects.player.rect): 
            objects.player.hit_this_frame = True

class Button(Obj): 
    def __init__(self, image, location, effects):
        super().__init__(image, location)
        self.effects = effects
    def update(self): 
        if pygame.mouse.get_pressed(3)[0]:
            mousePos = objects.mapMousePos(pygame.mouse.get_pos())
            if self.rect.collidepoint(mousePos): 
                for action in self.effects:
                    exec(action)

class Button_func(Obj):
    def __init__(self, image, location, to_run):
        super().__init__(image, location)
        self.to_run = to_run
    
    def update(self):
        if pygame.mouse.get_pressed(3)[0]:
            mousePos = objects.mapMousePos(pygame.mouse.get_pos())
            if self.rect.collidepoint(mousePos): 
                self.to_run()

class NPC(Obj): 
    def __init__(self, image, location, effects):
        super().__init__(image, location)
        self.effects = effects
        self.type = "NPC" #TODO: wait till up before being pressed down
    def update(self): 
        if pygame.mouse.get_pressed(3)[0]:
            mousePos = objects.mapMousePos(pygame.mouse.get_pos())
            if self.rect.collidepoint(mousePos): 
                for action in self.effects:
                    exec(action)

def blit_alpha(target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)

class UpdateLog(Obj):
    def __init__(self, location, archives):
        self.capsule = pygame.Surface((175, 25))
        self.capsule.fill((0, 0, 0))
        self.exclamation_black = pygame.image.load(create_path("Notification Button.png"))
        self.exclamation_white = pygame.image.load(create_path("White Notification Button.png"))
        self.exclamation = self.exclamation_black
        self.image = pygame.Surface((1, 1))  # just for super
        self.text = None

        super().__init__(self.image, location)
        self.message: str = ""
        self.archived = archives
    
    def in_relation(self, x, y):
        return (self.rect.x + x, self.rect.y + y)

    def render(self): 
        blit_alpha(objects.display, self.capsule, self.in_relation(25, 0), 10)
        if self.text != None:
            objects.display.blit(self.text, self.in_relation(25, 0))
        objects.display.blit(self.exclamation, self.in_relation(0, 0))
    
    def regenerate_image(self):
        message = self.clamp_message(self.message)
        self.text = objects.myFont.render(message, True, (200,0,0))

    def clamp_message(self, message):
        text_width, text_height = objects.myFont.size(message)

        while text_width > self.capsule.get_size()[0] - 5:
            text_width, text_height = objects.myFont.size(message)
            message = message[:-1]
        return message


    def addMessage(self, message: str):
        self.archived.append(message)
        self.message = message
        self.regenerate_image()
        # def todo():
        #     self.log.remove(message)
        #     self.regenerate_image()
        #     print("TODONE")
        # rb.Time.delayed_call(5 * 1000, todo)





class Building(Obj):
    def __init__(self, image, location, subchunk, doorSize):
        super().__init__(image, location)
        self.subchunk = subchunk
        self.type = "building"
        self.doorRect = pygame.Rect((0,0), doorSize)
        self.doorRect.midbottom = self.rect.midbottom
    def update(self):
        if objects.player.rect.colliderect(self.doorRect): 
            objects.player.chunk = (objects.mapWidth, self.subchunk)
            objects.player.rect.center = (250, 425)
            
        
        #for obj in objects.currentChunk.contents:
        #    if obj.type in self.interact: 
        #        if self.rect.colliderect(obj.rect): 
        #            if obj.type == "projectile": 
        #                objects.currentChunk.contents.remove(obj)
        #if self.rect.colliderect(objects.player.rect): 
        #    if objects.player.rect.center = objects.player.last_valid_position

class CollisionButton(Obj): 
    def __init__(self, image, location, effects): 
        self.effects = effects
        super().__init__(image, location)
        self.type = "collisionButton"
    def update(self): 
        if objects.player.rect.colliderect(self.rect): 
            for effect in self.effects: 
                exec(effect)

class QuestionCube(Obj): 
    boosts = [["objects.player.currentHealth += 25", 25], ["objects.resourceAmounts['ghostEnergy'] += 25", 50], ["objects.moveSpeed = 10", 60],["objects.resourceAmountsr['purple']", 65],["objects.resourceAmounts['red']", 67],["objects.resourceAmounts['blue']", 69],["objects.resourceAmounts['gold']", 70],["print('10s infinite health')", 80], ["print('10s infinite energy')", 90], ["print('key')"]]

    def __init__(self, location): 
        image = pygame.image.load(create_path("QuestionCube.png"))
        super().__init__(image, location)
        self.type = "qcube"
    def update(self): 
        if objects.player.rect.colliderect(self.rect): 
            objects.currentChunk.contents.remove(self)
            objects.gamestate = 3
            objects.currentProblem = random.choice(objects.problems)
    def randBoost(): 
        choice = random.randint(1,100)
        for boost in QuestionCube.boosts:
            if choice <= boost[1]:
                exec(boost[0])
                return
