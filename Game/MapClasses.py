import pygame
import objects
import random
import math
import time
import webbrowser
import Abilities
from BasicClasses import Obj


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
                self.image.blit(pygame.image.load("Data\Pixel Images\TallGrass.png"), (random.randint(0,500),random.randint(0,500)))
                
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
        super().__init__(pygame.image.load("Data\Pixel Images\Gold Coin.png"), location)
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
        image = pygame.image.load("Data\Pixel Images\QuestionCube.png")
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
