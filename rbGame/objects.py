import rubato as rb
from constants import *

rb.init(res=Vector(WIDTH, HEIGHT), window_size=WINDOWSIZE)

# scenes
main = rb.Scene(name="main")
intro = rb.Scene(name="intro")

# game logic
daytime = True
freeze = False
shopShowing = False

# start with all abilities
op = False

# things in game
abilityPanel = []  # game objects of ability icons
ability_levels = [1, 1, 1, 1, 1, 1, 1, 1]
chunks = []  # different scenes ? maybe
player = None
currentChunk = None
NPC_clicked = False
update_log = None
bosses_killed = 0

# player resources
resourceAmounts = {
    "coins": 0,
    "ghostEnergy": 1000
}
potions = {
    "purple": 0,
    "red": 0,
    "blue": 0,
    "gold": 0
}

# runnables
potionEffects = {
    "purple": ["objects.player.currentHealth += objects.player.maxHealth * .2",
               "objects.resourceAmounts['ghostEnergy'] += objects.player.maxHealth * .2"],
    "red": ["objects.player.currentHealth = objects.player.maxHealth"],
    "blue": ["objects.resourceAmounts['ghostEnergy'] = objects.player.maxEnergy"],
    "gold": ["objects.player.currentHealth = objects.player.maxHealth",
             "objects.resourceAmounts['ghostEnergy'] = objects.player.maxEnergy"],
}

# logs
archives = []

# math
problems = []


# reset
def Reset():  # TODO: won't work
    global currentChunk
    if player:
        player.currentHealth = player.maxHealth
        player.chunk = start_chunk
        player.rect.topleft = (20, 150)
        currentChunk = chunks[player.chunk[1]][player.chunk[0]]

    resourceAmounts["ghost energy"] = 0
    for chunkList in chunks:
        for chunk in chunkList:
            for thing in chunk.contents:
                if thing.type == "enemy":
                    thing.health = thing.maxHealth
