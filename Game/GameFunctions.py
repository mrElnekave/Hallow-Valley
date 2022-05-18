import pygame
import MapClasses
import Enemies
import objects
import random
import rubato as rb
import images
from images import create_path
import webbrowser
from helpful import map_description

pygame.init()

def open_guide():
    webbrowser.open("https://docs.google.com/document/d/1MywKXdex3Ny2-qE1z_nNMzU6OQ4gaUB3d9Zq9louTh8/edit?usp=sharing")
    print("Opened Tutorial in your web browser")

def switch_map_notifs():
    pass
buttons = {}

def restart():
    global buttons
    objects.Reset()
    buttons = {
        "game": [
            MapClasses.Button_func(pygame.image.load(create_path("Help Button.png")), (480, 80), open_guide)],
        "tab":[
            MapClasses.Button_func(pygame.image.load(create_path("Blue Potion.png")), (150, 400), switch_map_notifs),
            MapClasses.Button_func(pygame.image.load(create_path("Red Potion.png")), (350, 400), switch_map_notifs),
        ],
        "menu": [
            MapClasses.Button(pygame.transform.scale(pygame.image.load(create_path("StartButton.png")), (300,80)),(250,450), ['objects.gamestate = 1','objects.Reset()']), MapClasses.Button(pygame.transform.scale(pygame.image.load(create_path("AboutUsButton.png")), (300,80)),(250,350), ['webbrowser.open("https://docs.google.com/presentation/d/1fCRW8VGcp_BtFYz1E_SCKFJo4uPcnhw9mEK5d6gdftc/edit?usp=sharing")'])],
        "shop": [
        MapClasses.Button(pygame.transform.scale(pygame.image.load(create_path("Purple Potion.png")),(50,50)),(175,175), ['if objects.resourceAmounts["coins"] >= 25: objects.potions["purple"] += 1;objects.resourceAmounts["coins"] -= 25;print("Bought Purple Potion")', "time.sleep(0.5)"]),
        MapClasses.Button(pygame.transform.scale(pygame.image.load(create_path("Red Potion.png")), (50,50)),(225,175), ['if objects.resourceAmounts["coins"] >= 50: objects.potions["red"] += 1;objects.resourceAmounts["coins"] -= 50;print("Bought Red Potion")', "time.sleep(0.5)"]),
        MapClasses.Button(pygame.transform.scale(pygame.image.load(create_path("Blue Potion.png")),(50,50)),(275,175), ['if objects.resourceAmounts["coins"] >= 50: objects.potions["blue"] += 1;objects.resourceAmounts["coins"] -= 50;print("Bought Blue Potion")', "time.sleep(0.5)"]),
        MapClasses.Button(pygame.transform.scale(pygame.image.load(create_path("Gold Potion.png")),(50,50)),(325,175), ['if objects.resourceAmounts["coins"] >= 100: objects.potions["gold"] += 1;objects.resourceAmounts["coins"] -= 100;print("Bought Gold Potion")', "time.sleep(0.5)","objects.FindQuest('Potion Critic').data += 1"]),
        MapClasses.Button(pygame.Surface((200,50)),(250,325), ['objects.shopShowing = False'])]
    }

objects.player = Enemies.Player()
objects.update_log = MapClasses.UpdateLog((0, 87), objects.archives)
restart()
def DebugCode():
    if objects.debugging and pygame.key.get_pressed()[pygame.K_SPACE]:
        objects.player.currentHealth -= 10
    #if pygame.key.get_pressed()[pygame.K_p]:
       # print(pygame.mouse.get_pos())

def NightEvent():
    # Spawning normal ghosts in empty chunks
    for y in range(objects.mapHeight): 
        for x in range(objects.mapWidth): 
            chunk = objects.chunks[x][y]
            enemies = False
            for thing in chunk.contents: 
                if thing.type == "enemy": 
                    enemies = True
            if enemies is False: 
                if (chunk.location[0] >= 2 or chunk.location[1] >= 2) and chunk != objects.currentChunk: 
                    for i in range(random.randint(1,5)):
                        chunk.contents.append(Enemies.Ghost((random.randint(0,500),random.randint(0,500))))
    objects.reports_on and objects.update_log.addMessage("REPORT: Ghosts have appeared in uninhabited areas.")
    # Spawning a large ghost in uninhabited chunks
    chunk = objects.chunks[random.randint(0,objects.mapWidth-1)][random.randint(0,objects.mapHeight-1)]
    while (chunk.location[0] < 2 and chunk.location[1] < 2) or chunk == objects.currentChunk:
        chunk = objects.chunks[random.randint(0,objects.mapWidth-1)][random.randint(0,objects.mapHeight-1)]
    objects.reports_on and objects.update_log.addMessage(f"REPORT: A powerful ghost has appeared in chunk {chunk.location}.")
    chunk.contents.append(Enemies.LargeGhost((250,250)))

dayNightCounter = 0
inTab = False
def GameplayUpdate():
    global inTab, dayNightCounter
    for button in buttons["game"]: 
        button.update()
    for quest in objects.quests:
        quest.update()

    # INPUT (Getting stuff that player is doing ex: pressing keys moving keyboard)
    objects.player.last_valid_position = objects.player.rect.center
    keys = pygame.key.get_pressed()
    if not inTab:
        objects.player.getinput(keys)
    if objects.debugging: #keys[pygame.K_i]: # Game Information
        objects.update_log.addMessage("TESTINGLONGER")
        objects.update_log.addMessage("INFORMATION: ")
        # objects.update_log.addMessage("Current Quest: "+objects.quests[objects.currentQuest].name)
        objects.update_log.addMessage("Ghost Energy: "+str(objects.resourceAmounts["ghost energy"]))
        objects.update_log.addMessage("Coins: "+str(objects.resourceAmounts["coins"]))
        objects.update_log.addMessage("Potions: "+str(objects.potions))
        objects.update_log.addMessage("Health: "+str(objects.player.currentHealth))
    # Pressing Keys
    for event in pygame.event.get(pygame.KEYDOWN):
        objects.player.changeAbility(event)
        # Changing ability level 
        if event.key == pygame.K_TAB:
            inTab = not inTab 
        if objects.debugging and event.key == pygame.K_l:
            for i in range(8): 
                level = objects.levels[i]
                level += 1 
                if level > 5: 
                    level = 1
                objects.levels[i] = level
            print(objects.levels)
        if objects.debugging and event.key == pygame.K_k:
            objects.player.changeSkin()
        if objects.debugging and event.key == pygame.K_j:
            map_description.show_type("fire")
        if event.key == pygame.K_r:
            index = objects.player.currentAbility - 1
            if not (objects.player.currentAbility in [0,9]):
                if objects.resourceAmounts["ghostEnergy"] >= 25:
                    objects.resourceAmounts["ghostEnergy"] -= 25
                    newData = list(map_description.portalLocations.values())[index]
                    newChunk = newData[0]
                    newCoordinates = newData[1]
                    objects.player.chunk = newChunk
                    objects.player.rect.center = newCoordinates


    if not inTab:
        for button in buttons["tab"]: 
            button.update()
        # Using Scrollwheel
        for event in pygame.event.get(pygame.MOUSEWHEEL): 
            objects.player.changeAbilityWheel(event)

        # UPDATE (Doing checks in the background ex: checking if something is colliding)

        # Day-Night cycle
        dayNightCounter += 1
        if dayNightCounter / objects.framerate >= objects.dayLength: 
            objects.daytime = not objects.daytime
            if objects.daytime:
                objects.reports_on and objects.update_log.addMessage("REPORT: It is now daytime.")
            else:
                objects.reports_on and objects.update_log.addMessage("REPORT: It is now nighttime")
                NightEvent()
            dayNightCounter = 0
            
        # Updating current chunk and stuff in it  
        objects.currentChunk = objects.chunks[objects.player.chunk[0]][objects.player.chunk[1]]
        if objects.freeze == True: 
            for thing in objects.currentChunk.contents: 
                if thing.type != 'enemy': 
                    thing.update()
            objects.abilities[2].freezeCD()  # the freeze abilities cooldown
        else: 
            objects.currentChunk.update()
        objects.player.update()
        if objects.player.currentHealth <= 0: 
            objects.gamestate = 2
        if objects.resourceAmounts["ghostEnergy"] >= objects.player.maxEnergy: 
            objects.resourceAmounts["ghostEnergy"] = objects.player.maxEnergy
        objects.first_game_frame = False
        objects.NPC_clicked = False
    else:
        objects.first_game_frame = True

        
freezeOverlay = pygame.Surface(objects.size)
freezeOverlay.fill((255,255,255))
freezeOverlay.set_alpha(100)

def GameplayRender(): 

    # RENDER (Putting stuff on the screen)
    objects.currentChunk.render()
    if objects.freeze == True: 
        global freezeOverlay
        objects.display.blit(freezeOverlay, (0,0))
    objects.player.render()
    
    # UI Rendering
    objects.display.blit(objects.myFont.render("Coins: "+ str(objects.resourceAmounts["coins"]), True, (0,0,0)), (0,50))
    objects.display.blit(objects.myFont.render("Chunk: "+ str(objects.currentChunk), True, (0,0,0)), (280,70))
    '''questName = objects.quests[objects.currentQuest].name
    objects.display.blit(objects.myFont.render(questName, True, (0,0,0)), (200,100))
    '''

    # Draw healthbar
    pygame.draw.rect(objects.display, (15,15,15), pygame.Rect(300,0,200,20))
    pygame.draw.rect(objects.display, (0,255,0), pygame.Rect(300,0,objects.player.currentHealth/objects.player.maxHealth*200,20))
    objects.display.blit(objects.myFont.render(f"Health: {objects.player.currentHealth:.2f} / {objects.player.maxHealth}", True, (0,0,0)),(0,0))
    # Draw energybar
    pygame.draw.rect(objects.display, (15,15,15), pygame.Rect(300,20,200,20))
    pygame.draw.rect(objects.display, (0,0,255), pygame.Rect(300,20,objects.resourceAmounts["ghostEnergy"]/objects.player.maxEnergy*200,20))
    objects.display.blit(objects.myFont.render(f"Ghost Energy: {objects.resourceAmounts['ghostEnergy']} / {objects.player.maxEnergy}", True, (0,0,0)),(0,25))
    
    # Draw ability panel and equipped abiltiy
    for i in range(len(objects.abilityPanel)):
        if i == objects.player.currentAbility:
            objects.abilityPanel[i].set_alpha(255)
        elif objects.abilities[i] != None:
            objects.abilityPanel[i].set_alpha(100)
        else:
            objects.abilityPanel[i].set_alpha(25)
        objects.display.blit(objects.abilityPanel[i], (50 * i, 450))
    
    for button in buttons["game"]: 
        button.render()
    
    if inTab: # render extra ontop
        for button in buttons["tab"]: 
            button.render()
        location = (125, 90)
        objects.display.blit(images.demo_map, location)
        objects.display.blit(images.demo_mask, location)
        map_description.playerPosOnMap(objects.player.rect.center, *objects.player.chunk, location)
        # render the map

        # Update Log
        objects.update_log.tabRender()

    else:
        # Update Log
        objects.update_log.render()



def ShopUpdate():
    for button in buttons["shop"]: 
        button.update()

shopImage = pygame.image.load(create_path("ShopInv.png"))
def ShopRender():
    objects.display.blit(shopImage, (150, 150))

objects.abilityPanel = [pygame.image.load(create_path("Arrow Icon.png")),
                pygame.image.load(create_path("Fireball Icon.png")),
                pygame.image.load(create_path("Freeze Icon.png")),
                pygame.image.load(create_path("Speed Icon.png")),
                pygame.image.load(create_path("Poison Icon.png")),
                pygame.image.load(create_path("Summoning Icon.png")),
                pygame.image.load(create_path("Shield Icon.png")),
                pygame.image.load(create_path("Laser Icon.png")),
                pygame.image.load(create_path("Wave Icon.png")),
                pygame.image.load(create_path("Potion Icon.png"))]


def MenuRender(): 
    objects.display.fill((255,255,255))
    titleScreen = images.menu_base
    
    objects.display.blit(titleScreen, (0, 0))
    for button in buttons["menu"]: 
        button.render()

def lightning():
    timescale = random.random() * 2 + 0.5
    rb.Time.delayed_call(0 * timescale, images.switch_base)
    rb.Time.delayed_call(500 * timescale, images.switch_base)
    rb.Time.delayed_call(550 * timescale, images.switch_base)
    rb.Time.delayed_call(1000 * timescale, images.switch_base)
    rb.Time.delayed_call(random.randrange(5, 12) * 1000, lightning)

rb.Time.delayed_call(1000, lightning)
def MenuUpdate():
    for button in buttons["menu"]: 
        button.update()

def GameOverUpdate(): 
    pygame.event.pump()
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_c]: 
        restart()
        objects.gamestate = 0

def GameOverRender(): 
    objects.display.fill((0,0,0))
    objects.display.blit(objects.announcementFont.render("Game Over", True, (255,0,0)), (100,50))
    objects.display.blit(objects.myFont.render("Press C to continue to the main menu.", True, (255, 0, 0)), (100, 300))

# Create list of buttons
a = [pygame.Rect(20, 110,100,100),"1",True]
b = [pygame.Rect(140,110,100,100),"2",True]
c = [pygame.Rect(260,110,100,100),"3",True]
d = [pygame.Rect(380,110,100,100),"4",True]
plus = [pygame.Rect(20,250,100,100),"+"]
minus = [pygame.Rect(140,250,100,100),"-"]
times = [pygame.Rect(260,250,100,100),"*"]
divide = [pygame.Rect(20,370,100,100),"/"]
startparen = [pygame.Rect(140,370,100,100),"("]
endparen = [pygame.Rect(260,370,100,100),")"]
backspace = pygame.Rect(380,250,100,100)
enter = pygame.Rect(380,370,100,100)

numbers = [a,b,c,d]
operations = [plus,minus,times,divide] 
parentheses = [startparen,endparen]
answerString = ""
values = ["1","2","3","4","5","6","7","8","9","0"]
def MathUpdate(): 
    objects.first_game_frame = True
    a[1] = objects.currentProblem[0]
    b[1] = objects.currentProblem[1]
    c[1] = objects.currentProblem[2]
    d[1] = objects.currentProblem[3]
    global answerString
    for event in pygame.event.get(): 
        if event.type == pygame.MOUSEBUTTONDOWN: 
            mousePos = objects.mapMousePos(pygame.mouse.get_pos())
            if answerString != "" and answerString[-1] in values: 
                pass
            else: 
                for i in numbers: 
                    if i[2] and i[0].collidepoint(mousePos): 
                        answerString += i[1]
                        i[2] = False
            for i in operations: 
                if answerString != "" and (answerString[-1] in values or answerString[-1] == endparen[1]) and i[0].collidepoint(mousePos): 
                    answerString += i[1]
            for i in parentheses: 
                if i[0].collidepoint(mousePos): 
                    answerString += i[1]
            if backspace.collidepoint(mousePos) and len(answerString) > 0:
                answerString = ""
                for i in numbers: 
                    i[2] = True
            if answerString != "" and enter.collidepoint(mousePos):
                try:
                    answer = eval(answerString)
                    if answer == 24 or answer == 23.99999999999999:
                        MapClasses.QuestionCube.randBoost()
                    objects.gamestate = 1  # no boost
                    answerString = ""
                except SyntaxError:
                    answerString = ""

            #    if eval(answerString) in results: 
            #        gamestate = 3
            #    else: 
            #        gamestate = 4

panelImage = pygame.image.load(create_path("MathPanel.png"))
panelRect = panelImage.get_rect()
def MathRender():
    # Display our background
    objects.display.fill((0,255,0))
    objects.display.blit(panelImage, panelRect)
    # Display the numbers
    submissionText = objects.mathFont.render(answerString, False, (0,0,0))
    objects.display.blit(submissionText, (10,25))
    aText = objects.mathFont.render(a[1], False, (0,0,0))
    objects.display.blit(aText, (45, 135))
    bText = objects.mathFont.render(b[1], False, (0,0,0))
    objects.display.blit(bText, (165, 135))
    cText = objects.mathFont.render(c[1], False, (0,0,0))
    objects.display.blit(cText, (285, 135))
    dText = objects.mathFont.render(d[1], False, (0,0,0))
    objects.display.blit(dText, (405, 135))

