import rubato as rb
from constants import *

rb.init(
    name="Hallow Valley",
    res=Vector(WIDTH, HEIGHT),
    window_size=WINDOWSIZE,
    icon="Data/Pixel Images/utility/Blue Potion.png",
)

# scenes
main = None
intro = rb.Scene(name="intro")
game_over = rb.Scene(name="game over")
win = rb.Scene(name="win")

# game logic
daytime = True
freeze = False
shopShowing = False


# start with all abilities
op = False

# things in game
abilityPanel = []  # game objects of ability icons
ability_levels = [1, 1, 1, 1, 1, 1, 1, 1]
chunks: list[rb.Scene] = []  # list of scenes
dungeons: list[rb.Scene] = [] # list of scenes

player = None
player_go = None
currentChunk: Vector = Vector.zero
NPC_clicked = False
update_log = None
bosses_killed = 0
inTab = False
tabScreen = None
ui = None
collided = False

visitedChunks = []

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


def switch_chunk(direction: str):
    global main, currentChunk
    save_chunk = currentChunk
    made_switch = False
    if direction == "up":
        if currentChunk.y > 0:
            currentChunk.y -= 1
            made_switch = True
    elif direction == "down":
        if currentChunk.y < len(chunks) - 1:
            currentChunk.y += 1
            made_switch = True
    elif direction == "left":
        if currentChunk.x > 0:
            currentChunk.x -= 1
            made_switch = True
    elif direction == "right":
        if currentChunk.x < len(chunks[0]) - 1:
            currentChunk.x += 1
            made_switch = True
    if made_switch:
        main = chunks[currentChunk.y][currentChunk.x]
        main.switch()

        # if currentChunk not in visitedChunks:
        #     visitedChunks.append(save_chunk)
        #     main.add(player_go)

    return made_switch
