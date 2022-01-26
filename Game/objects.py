# from tkinter.messagebox import NO
import pygame
pygame.init()
from constants import *

display = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))

# game logic
gamestate = 0
daytime = True
freeze = False
shopShowing = False


# things in game
abilities = [None, None, None, None, None, None, None, None, None, None]
abilityPanel = []
levels = [1,1,1,1,1,1,1,1]
quests = []
chunks = []
player = None
currentChunk = None


# player resources
resourceAmounts = {
    "coins": 1000000, 
    "ghostEnergy": 0
    }
potions = {
    "purple": 0, 
    "red": 0, 
    "blue": 0, 
    "gold": 0
}


# runnables
potionEffects = {
    "purple":["objects.player.currentHealth += objects.player.maxHealth * .2","objects.resourceAmounts['ghostEnergy'] += objects.player.maxHealth * .2"],
    "red":["objects.player.currentHealth = objects.player.maxHealth"],
    "blue":["objects.resourceAmounts['ghostEnergy'] = objects.player.maxEnergy"],
    "gold":["objects.player.currentHealth = objects.player.maxHealth","objects.resourceAmounts['ghostEnergy'] = objects.player.maxEnergy"],
}

# quests
"""#"Find the Fire Key! ","Defeat the Fire Ghost! ","Find the Ice Key! ","Defeat the Ice Ghost! ","Find the Lightning Key! ","Defeat the Lightning Ghost! ","Find the Poison Key! ","Defeat the Poison Ghost! ","Find the Summoning Key! ","Defeat the Summoner Ghost! ","Find the Shield Key! ","Defeat the Shield Ghost! ","Find the Laser Key! ","Defeat the Laser Ghost! ","Find the Water Key! ","Defeat the Water Ghost! ","Find the Boss Key! ","Defeat the Dark Ghost! "]
currentQuest = 0
achievements = [
    "Buy 3 gold potions!",
    "Defeat 100 enemies!",
    "Travel the entire map! ",
    "Defeat 5 fire ghosts!",
    "Survive for 10 days!",
    "Take 1000 damage (careful with your health)!",
    "Have infinite health for 3 minutes overall!",
    "Defeat 5 enemies in one electrodash!",
    "Use the laser arrows at least 50 times! ", 
    "Upgrade one aspect of the player to the highest level! ", 
    "Buy the highest level upgrade of every ability! ", 
    "Pick up 100 Question Cubes!", 
    "PLEASE ENTER MORE HERE"
    ]""" # TODO: implement achievments


# math
problems = []

# reset
def Reset():
    player.currentHealth = player.maxHealth
    resourceAmounts["ghost energy"] = 0
    player.chunk = (0, 0)
    currentChunk = chunks[player.chunk[1]][player.chunk[0]]
    player.rect.topleft = (0,0)
    for chunkList in chunks:
        for chunk in chunkList:
            for thing in chunk.contents:
                if thing.type == "enemy": 
                    thing.health = thing.maxHealth

# map mouse
def mapMousePos(mx, my):
    pass

# Helper debug stuffs
class Point: 
    def __init__(self, position): 
        self.color = (255,0,0) 
        self.position = position
        self.type = "marker"
    def render(self): 
        pygame.draw.circle(display, self.color, self.position, 5)
    def update(self): 
        pass
'''
pygame.font.init()
myFont = pygame.font.SysFont("Comic Sans", 24)
announcementFont = pygame.font.SysFont("Comic Sans", 72)
mathFont = pygame.font.SysFont("Comic Sans", 50)

gamestate = 0
chunks = []
mathQuestions = None
currentProblem = ['a','b','c','d']

# we have a 7, 7 map meaning chunks are two dimensional list and 7 by 7
# Every index in the 2D list houses a "Chunk" object
# Every thing displayed on a chunk is housed in the chunks "contents" variable, that is including portals
# Additionally we store our boss rooms in our chunks list by creating another "8th" list as the 7th index

resourceAmounts = {
    "coins": 1000000, 
    "ghostEnergy": 0
    }
potions = {
    "purple": 0, 
    "red": 0, 
    "blue": 0, 
    "gold": 0
}
potionEffects = {
    "purple":["objects.player.currentHealth += objects.player.maxHealth * .2","objects.resourceAmounts['ghostEnergy'] += objects.player.maxHealth * .2"],
    "red":["objects.player.currentHealth = objects.player.maxHealth"],
    "blue":["objects.resourceAmounts['ghostEnergy'] = objects.player.maxEnergy"],
    "gold":["objects.player.currentHealth = objects.player.maxHealth","objects.resourceAmounts['ghostEnergy'] = objects.player.maxEnergy"],
}
screen = pygame.display.set_mode(size)
daytime = True
freeze = False
abilities = [None, None, None, None, None, None, None, None, None, None]
abilityPanel = []
levels = [1,1,1,1,1,1,1,1]
shopShowing = False
quests = []
#"Find the Fire Key! ","Defeat the Fire Ghost! ","Find the Ice Key! ","Defeat the Ice Ghost! ","Find the Lightning Key! ","Defeat the Lightning Ghost! ","Find the Poison Key! ","Defeat the Poison Ghost! ","Find the Summoning Key! ","Defeat the Summoner Ghost! ","Find the Shield Key! ","Defeat the Shield Ghost! ","Find the Laser Key! ","Defeat the Laser Ghost! ","Find the Water Key! ","Defeat the Water Ghost! ","Find the Boss Key! ","Defeat the Dark Ghost! "]
currentQuest = 0
achievements = [
    "Buy 3 gold potions!",
    "Defeat 100 enemies!",
    "Travel the entire map! ",
    "Defeat 5 fire ghosts!",
    "Survive for 10 days!",
    "Take 1000 damage (careful with your health)!",
    "Have infinite health for 3 minutes overall!",
    "Defeat 5 enemies in one electrodash!",
    "Use the laser arrows at least 50 times! ", 
    "Upgrade one aspect of the player to the highest level! ", 
    "Buy the highest level upgrade of every ability! ", 
    "Pick up 100 Question Cubes!", 
    "PLEASE ENTER MORE HERE"
    ]

'''
