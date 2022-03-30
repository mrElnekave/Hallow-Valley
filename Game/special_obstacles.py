import pygame 
import objects 
import constants 
from BasicClasses import Obj 
import images


class InvisibleObj: 
    def __init__(self, location, size=[50, 50]): 
        self.type = "InvisibleObj"
        self.rect = pygame.Rect(0,0,size[0],size[1])
        self.rect.center = location 
    def render(self): 
        pygame.draw.rect(objects.display, (255, 0, 0),  self.rect)
    def update(self): 
        pass

class Lava(InvisibleObj): 
    def __init__(self, location): 
        super().__init__(location)
        self.type = "obstacle"
        self.image = images.lava
    def render(self): 
        objects.display.blit(self.image, self.rect)
    def update(self): 
        if self.rect.colliderect(objects.player.rect): 
            if not objects.player.invulnerability: 
                objects.player.currentHealth -= 0.1 
        for enemy in objects.currentChunk.contents: 
            if enemy.type == "enemy" and enemy.rect.colliderect(self.rect): 
                enemy.health -= 2

class Poison(InvisibleObj): 
    def __init__(self, location): 
        super().__init__(location)
        self.type = "obstacle"
        self.image = images.poison
    def render(self): 
        objects.display.blit(self.image, self.rect)
    def update(self):
        if self.rect.colliderect(objects.player.rect): 
            if not objects.player.invulnerability: 
                objects.player.currentHealth -= 1 

class Cactus(InvisibleObj): 
    def __init__(self, location): 
        super().__init__(location)
        self.type = "obstacle"
        self.image = images.cactus
    def render(self): 
        objects.display.blit(self.image, self.rect)
    def update(self):
        if self.rect.colliderect(objects.player.rect): 
            objects.player.hit_this_frame = True 
            if not objects.player.invulnerability: 
                objects.player.currentHealth -= 0.1 