import pygame
from images import create_path 
import objects, constants, Abilities
import math, random, rubato
import MapClasses
from rubato import Vector
from BasicClasses import Obj
from helpful import map_description

#IMPORTANT: This includes the player 

# Creating Player Class
class Player(Obj):
    # Player Setup
    def __init__(self):
        super().__init__(pygame.image.load(create_path("Player2.png")))
        self.chunk = constants.start_chunk
        self.currentHealth = 100.00
        self.maxEnergy = 100
        self.maxHealth = 100
        self.rect.topleft = (10, 10)
        self.last_valid_postion = self.rect.center
        self.type = "player"
        self.currentAbility = 0
        self.invulnerability = False
        self.hit_this_frame = False
        self.currentSkin = 0
        self.image = pygame.image.load(create_path("Skin"+str(self.currentSkin)+".png"))

        # Debug all powers immediately
        objects.abilities[0] = Abilities.FireArrow()
        objects.abilities[1] = Abilities.LaunchFireball() 
        objects.abilities[2] = Abilities.Freeze()
        objects.abilities[3] = Abilities.ElectroDash()
        objects.abilities[4] = Abilities.SummonPoison()
        objects.abilities[5] = Abilities.SummonGhost()
        objects.abilities[6] = Abilities.MakeMagicalShield()
        objects.abilities[7] = Abilities.FireLaserArrow()
        objects.abilities[8] = Abilities.LaunchWave()
        objects.abilities[9] = Abilities.PotionAbility()
        #objects.resourceAmounts["ghostEnergy"] = objects.maxEnergys

    # Function to draw player to screen
    def render(self):
        # pygame.draw.rect(objects.screen, "#000000", self.rect)
        super().render()
        objects.abilities[self.currentAbility].render()
        if self.currentHealth > self.maxHealth: 
            self.currentHealth = self.maxHealth
        if objects.resourceAmounts["ghostEnergy"] > self.maxEnergy: 
            objects.resourceAmounts["ghostEnergy"] = self.maxEnergy
    def move(self, x, y): 
        #self.last_valid_position = self.rect.center
        self.rect = self.rect.move(x,y)
    def pos_validate(self):

        if self.hit_this_frame:
            self.rect.center = self.last_valid_postion
            self.hit_this_frame = False
            # return
        do_not_clear = False
        saved = self.chunk
        if self.rect.center[0] < 0: # Moving off left of screen
            if self.chunk[0] == -1 or self.chunk[0] == 0: # If in subchunk or leftmost chunk and boss fights.
                self.rect.centerx = 0 # Move flush to wall
            else:
                self.chunk = (self.chunk[0]-1, self.chunk[1])
                objects.reports_on and print(f'REPORT: Current chunk is {self.chunk}')
                self.rect.centerx = objects.WINDOWWIDTH
        elif self.rect.center[0] > objects.WINDOWWIDTH: # Moving off right of screen
            if self.chunk[0] == -1  or self.chunk[0] == objects.mapWidth-1:
                self.rect.centerx = objects.WINDOWWIDTH 
            else:
                self.chunk = (self.chunk[0]+1, self.chunk[1])
                objects.reports_on and print(f'REPORT: Current chunk is {self.chunk}')
                self.rect.centerx = 0
        elif self.rect.center[1] < 0: # Moving off top of screen
            if self.chunk[0] == -1  or self.chunk[1] == 0:
                self.rect.centery = 0
            else:
                self.chunk = (self.chunk[0],self.chunk[1]-1)
                objects.reports_on and print(f'REPORT: Current chunk is {self.chunk}')
                self.rect.centery = objects.WINDOWHEIGHT
        elif self.rect.center[1] > objects.WINDOWWIDTH: # Moving off bottom of screen
            if self.chunk[0] == -1  or self.chunk[1] == objects.mapHeight-1:
                self.rect.centery = objects.WINDOWHEIGHT
            else:
                self.chunk = (self.chunk[0],self.chunk[1]+1)
                objects.reports_on and print(f'REPORT: Current chunk is {self.chunk}')
                self.rect.centery = 0
        else:
            do_not_clear = True
        
        if not do_not_clear:
            map_description.clear_chunk(saved)

        self.last_valid_postion = self.rect.center
        if not(self.chunk in map_description.shownChunks):
            map_description.shownChunks.append(self.chunk)
            map_description.show_chunk(*self.chunk)
    def cancel_abilities(self):
        if self.currentAbility == 3:
            objects.abilities[3].canceled = True
    def getinput(self, keys): 
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.move(0,-objects.moveSpeed)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.move(0,objects.moveSpeed)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.move(-objects.moveSpeed,0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: 
            self.move(objects.moveSpeed,0)
    def changeAbility(self, event): 
        # Pressing Keys
        if event.key == pygame.K_1 and objects.abilities[0] != None:
            self.currentAbility = 0
        if event.key == pygame.K_2 and objects.abilities[1] != None:  
            self.currentAbility = 1
        if event.key == pygame.K_3 and objects.abilities[2] != None:  
            self.currentAbility = 2
        if event.key == pygame.K_4 and objects.abilities[3] != None:  
            self.currentAbility = 3
        if event.key == pygame.K_5 and objects.abilities[4] != None:  
            self.currentAbility = 4
        if event.key == pygame.K_6 and objects.abilities[5] != None:  
            self.currentAbility = 5
        if event.key == pygame.K_7 and objects.abilities[6] != None:  
            self.currentAbility = 6
        if event.key == pygame.K_8 and objects.abilities[7] != None:  
            self.currentAbility = 7
        if event.key == pygame.K_9 and objects.abilities[8] != None:  
            self.currentAbility = 8
        if event.key == pygame.K_0 and objects.abilities[9] != None:  
            self.currentAbility = 9
    def changeAbilityWheel(self,event):
        # Using Scrollwheel
        if event.y > 0:
            self.currentAbility += 1
            while self.currentAbility > 9 or objects.abilities[self.currentAbility] == None:
                self.currentAbility += 1
                if self.currentAbility > 9: 
                    self.currentAbility = 0
        if event.y < 0: 
            self.currentAbility -= 1
            while self.currentAbility < 0 or objects.abilities[self.currentAbility] == None:
                self.currentAbility -= 1
                if self.currentAbility < 0: 
                   self.currentAbility = 9
    def update(self):
        if not (Vector(*self.chunk) < Vector.two and Vector(*self.chunk) > Vector.zero):
            objects.abilities[self.currentAbility].update()
        self.pos_validate()
    def changeSkin(self): 
        self.currentSkin += 1 
        if self.currentSkin > 25: 
            self.currentSkin = 0
        self.image = pygame.image.load(create_path("Skin"+str(self.currentSkin)+".png"))

class Enemy: 
    def __init__(self, location): 
        self.rect = None
        self.health = None
        self.image = None
        self.attackDamage = None
        self.speed = None
        self.location = location
        self.type = None
    def render(self): 
        objects.display.blit(self.image, self.rect)
    def update(self): 
        pass

class Ghost(Enemy):
    def __init__(self, location): 
        self.maxHealth = 20
        self.health = self.maxHealth
        self.image = pygame.image.load(create_path("Ghost Enemy.png"))
        self.speed = 2
        self.attackDamage = 10
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = "enemy"
        self.drops = 5
        self.knocked = False
        self.direction = (0,0)
    def render(self): 
        
        self.image.set_alpha((self.health/self.maxHealth)*205 + 50)
        objects.display.blit(self.image, self.rect)
        
        pygame.draw.rect(objects.display, (0,0,0), pygame.Rect(self.rect.left,self.rect.top-self.rect[3]*.1,self.rect[2],self.rect[3]*.1))
        pygame.draw.rect(objects.display, (255,0,0), pygame.Rect(self.rect.left,self.rect.top-self.rect[3]*.1,self.rect[2]*(self.health/self.maxHealth),self.rect[3]*.1))
    def update(self):
        if not self.knocked: 
            playerX = objects.player.rect.center[0] 
            playerY = objects.player.rect.center[1]
            xGap = playerX - self.rect.center[0] 
            yGap = playerY - self.rect.center[1] 
            distance = (xGap**2+yGap**2)**(1/2)
            if distance != 0:
                factor = distance/self.speed
                moveX = xGap / factor
                moveY = yGap / factor
                self.direction = (moveX, moveY)
        self.rect = (self.rect.move(self.direction))
        # Check which side of the screen we are off and then move us back on
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 500:
            self.rect.right = 500
        if self.rect.top > 500:
            self.rect.top = 500
        if self.rect.bottom < 0:
            self.rect.bottom = 0

            #self.rect = self.rect.move((-self.direction[0],-self.direction[1])) 
            self.knocked = False
        
        if self.rect.colliderect(objects.player.rect): 
            if not objects.player.invulnerability:      
                objects.player.currentHealth -= self.attackDamage
            while self.rect.colliderect(objects.player.rect): 
                self.rect.center = (random.randint(100,objects.WINDOWWIDTH-100), random.randint(100, objects.WINDOWHEIGHT-100))
        if self.health <= 0: 
            objects.currentChunk.contents.remove(self)
            if objects.currentChunk.location[0]+1 != len(objects.chunks): 
                objects.resourceAmounts["ghostEnergy"] = objects.resourceAmounts["ghostEnergy"] + self.drops
                objects.currentChunk.contents.append(MapClasses.QuestionCube(self.rect.center)) #TODO: bring them back 
            return

class LargeGhost(Ghost): 
    def __init__(self, location): 
        self.maxHealth = 50
        self.health = self.maxHealth
        self.image = pygame.image.load(create_path("Large Ghost.png"))
        self.speed = 5
        self.attackDamage = 20
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = "enemy"
        self.drops = 25
        self.knocked = False

class FireGhostBoss(Enemy):
    def __init__(self):
        self.image = pygame.image.load(create_path("Fire Boss.png"))
        self.rect =  self.image.get_rect()
        self.rect.center = (250,250)
        self.attackDamage = 25
        self.speed = 5
        self.type = "enemy"
        self.angle = 0
        self.counter = 0
        self.maxHealth = 200
        self.health = self.maxHealth
    def render(self): 
        self.image.set_alpha((self.health/self.maxHealth)*255)
        objects.display.blit(self.image, self.rect)
        pygame.draw.rect(objects.display, (15,15,15), pygame.Rect(300,50 ,200,20))
        pygame.draw.rect(objects.display, (255,0,0), pygame.Rect(300,50,self.health,20))

    def update(self):
        # Changing directions after bouncing
        if self.rect.left < 0: 
            self.angle = random.random() * math.pi - math.pi/2
        if self.rect.right > objects.WINDOWWIDTH: 
            self.angle = random.random() * math.pi + math.pi/2
        if self.rect.top < 0: 
            self.angle = random.random() * math.pi + math.pi
        if self.rect.bottom > objects.WINDOWHEIGHT: 
            self.angle = random.random() * math.pi
        # Moving
        
        self.rect.center = (self.rect.centerx + self.speed*math.cos(self.angle), self.rect.centery - self.speed*math.sin(self.angle))
        # Checking for collision with player
        if self.rect.colliderect(objects.player.rect): 
            if not objects.player.invulnerability:
                objects.player.currentHealth = objects.player.currentHealth - self.attackDamage
            while self.rect.colliderect(objects.player.rect): 
                self.rect.center = (random.randint(0,objects.WINDOWWIDTH), random.randint(0, objects.WINDOWHEIGHT))
        # Shooting fireballs on a timer
        self.counter = self.counter + 1
        if self.counter == 10:
            playerPos = objects.player.rect.center
            xGap = playerPos[0] - self.rect.center[0]
            yGap = playerPos[1] - self.rect.center[1] 
            distance = (xGap**2+yGap**2)**(1/2)
            if yGap == 0:
                yGap = .01
            if distance != 0:
                factor = distance/5
                moveX = xGap / factor
                moveY = yGap / factor
                rotation =  math.degrees(math.atan(xGap / yGap)) + 90 # y/x
            if yGap > 0:
                rotation += 180
            objects.currentChunk.contents.append(EnemyFireball((moveX, moveY), rotation, self.rect.center))
            self.counter = 0
        # Getting hit by arrows
        for projectile in objects.currentChunk.contents:
            if projectile.type == "arrow" and self.rect.colliderect(projectile.rect):
                self.health -= projectile.attackDamage
                objects.currentChunk.contents.remove(projectile)
            if self.health <= 0: 
                objects.currentChunk.contents.remove(self)
                objects.player.maxHealth = objects.player.maxHealth + 25
                objects.player.maxEnergy = objects.player.maxEnergy + 25
                objects.resourceAmounts["ghostEnergy"] = objects.player.maxEnergy
                objects.player.currentHealth = objects.player.maxHealth
                objects.abilities[1] = Abilities.LaunchFireball()
                objects.reports_on and print("REPORT: You have defeated the fire ghost.")
                objects.reports_on and print("NEW ABILITY: FIREBALL")
                objects.reports_on and print("Ability Information: The fireball ability allows you to launch a fireball that does high damage and explodes upon contact, launching 4 smaller fireballs in different directions. This ability uses up 10 ghost energy per use. Press 2 to switch to the fireball ability from another ability.")
                objects.FindQuest("The Fire Boss").data = True
                data = map_description.portalLocations["fire"]
                objects.player.chunk = data[0]
                objects.player.rect.center = data[1]

                map_description.show_chunk(*(map_description.portalLocations["ice"][0]))

                for i in objects.chunks[data[0][0]][data[0][1]].contents: 
                    if type(i) == MapClasses.CollisionButton: 
                        objects.chunks[data[0][0]][data[0][1]].contents.remove(i)
                        return

class IceGhostBoss(Ghost): 
    def __init__(self):
        self.image = pygame.image.load(create_path("Ice Boss.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (250,250)
        self.type = "enemy"
        self.speed = 5
        self.maxHealth = 400
        self.health = 400
        self.attackDamage = 10
        self.direction = 90
        self.counter = 0

    def render(self):
        self.image.set_alpha((self.health/self.maxHealth)*255)
        objects.display.blit(self.image, self.rect)
        objects.display.blit(self.image, self.rect)
        pygame.draw.rect(objects.display, (15,15,15), pygame.Rect(150,25,200,20))
        pygame.draw.rect(objects.display, (255,0,0), pygame.Rect(150,25,self.health/self.maxHealth*200,20))

    def update(self):
        # Changing directions after bouncing
        if self.rect.left < 0 or self.rect.right > objects.WINDOWWIDTH or self.rect.top < 0 or self.rect.bottom > objects.WINDOWHEIGHT:
            playerPos = objects.player.rect.center
            xGap = playerPos[0] - self.rect.centerx
            yGap = playerPos[1] - self.rect.centery
            if yGap == 0:
                yGap = .01
            self.direction = math.atan(yGap / xGap)
            if xGap < 0:
                self.direction += math.pi
        # Moving
        self.rect.center = (self.rect.centerx + self.speed*math.cos(self.direction), self.rect.centery + self.speed*math.sin(self.direction))
        # Checking for collision with player
        if self.rect.colliderect(objects.player.rect): 
            if not objects.player.invulnerability: 
                objects.player.currentHealth = objects.player.currentHealth - self.attackDamage
            while self.rect.colliderect(objects.player.rect): 
                self.rect.center = (random.randint(0,objects.WINDOWWIDTH), random.randint(0, objects.WINDOWHEIGHT))
        # Shooting icicles on a timer
        self.counter = self.counter + 1
        if self.counter == 60:
            playerPos = objects.player.rect.center
            xGap = playerPos[0] - self.rect.center[0]
            yGap = playerPos[1] - self.rect.center[1] 
            distance = (xGap**2+yGap**2)**(1/2)
            if yGap == 0:
                yGap = .01
            if distance != 0:
                factor = distance/5
                moveX = xGap / factor * 2
                moveY = yGap / factor * 2
                rotation =  math.degrees(math.atan(xGap / yGap)) + 90
            if yGap > 0:
                rotation += 180
            objects.currentChunk.contents.append(EnemyIcicle((moveX, moveY), rotation, self.rect.center))
            self.counter = 0
        # Getting hit by arrows
        if self.health <= 0: 
            objects.currentChunk.contents.remove(self)
            objects.player.maxHealth = objects.player.maxHealth + 25
            objects.player.maxEnergy = objects.player.maxEnergy + 25
            objects.resourceAmounts["ghostEnergy"] = objects.player.maxEnergy
            objects.player.currentHealth = objects.player.maxHealth
            objects.abilities[2] = Abilities.Freeze()
            objects.reports_on and print("REPORT: You have defeated the ice ghost.")
            objects.reports_on and print("NEW ABILITY: FREEZE")
            objects.reports_on and print("Ability Information: The freeze ability allows you to freeze all enemies on the screen for 3 seconds. This ability uses up 25 ghost energy per use. Press 3 to switch to the freeze ability from another ability.")
            objects.FindQuest("The Ice Boss").data = True
            data = map_description.portalLocations["ice"]
            objects.player.chunk = data[0]
            objects.player.rect.center = data[1]
            map_description.show_chunk(*(map_description.portalLocations["lightning"][0]))

            for i in objects.chunks[data[0][0]][data[0][1]].contents: 
                if type(i) == MapClasses.CollisionButton: 
                    objects.chunks[data[0][0]][data[0][1]].contents.remove(i)
                    return

class LightningGhostBoss(Enemy):
    def __init__(self):
        self.image = pygame.image.load(create_path("Lightning Boss.png"))
        self.shadowImage = pygame.image.load(create_path("Lightning Boss Shadow.png"))
        self.shadowRect = self.shadowImage.get_rect()
        self.rect =  self.image.get_rect()
        self.rect.center = (250,250)
        self.attackDamage = 50
        self.speed = 25
        self.type = "enemy"
        self.nextLocation = (250,250)
        self.shadowRect.center = self.nextLocation
        self.counter = 0
        self.maxHealth = 600
        self.health = self.maxHealth
        self.moving = False
    def render(self): 
        self.image.set_alpha((self.health/self.maxHealth)*255)
        objects.display.blit(self.image, self.rect)
        objects.display.blit(self.image, self.rect)
        pygame.draw.rect(objects.display, (15,15,15), pygame.Rect(150,25,200,20))
        pygame.draw.rect(objects.display, (255,0,0), pygame.Rect(150,25,self.health/self.maxHealth*200,20))
        if self.counter >= objects.framerate/2: 
            objects.display.blit(self.shadowImage, self.shadowRect)
    def update(self):
        # Changing directions after reaching targeted location
        #print(self.counter)
        if self.rect.center == self.nextLocation:
            self.nextLocation = (random.randint(0,500),random.randint(0,500))
            self.shadowRect.center = self.nextLocation
            self.counter = 0
            self.moving = False

        if not self.moving: 
            self.counter += 1
            if self.counter == objects.framerate:
                self.moving = True
        else: 
            # Moving
            xDist = self.nextLocation[0] - self.rect.center[0]
            yDist = self.nextLocation[1] - self.rect.center[1]
            totalDist = (xDist**2 + yDist**2)**.5
            if self.speed > totalDist:
                self.rect.center = self.nextLocation
            else:
                xSpeed = xDist / totalDist * self.speed
                ySpeed = yDist / totalDist * self.speed
                self.rect = self.rect.move(xSpeed, ySpeed)
        # Checking for collision with player
        if self.rect.colliderect(objects.player.rect): 
            if not objects.player.invulnerability:
                objects.player.currentHealth = objects.player.currentHealth - self.attackDamage
            while self.rect.colliderect(objects.player.rect): 
                self.rect.center = (random.randint(0,objects.WINDOWWIDTH), random.randint(0, objects.WINDOWHEIGHT))
            self.counter = 0
            self.moving = False
        # Dying
        if self.health <= 0: 
            objects.currentChunk.contents.remove(self)
            objects.player.maxHealth = objects.player.maxHealth + 25
            objects.player.maxEnergy = objects.player.maxEnergy + 25
            objects.resourceAmounts["ghostEnergy"] = objects.player.maxEnergy
            objects.player.currentHealth = objects.player.maxHealth
            objects.abilities[3] = Abilities.ElectroDash()
            objects.reports_on and print("REPORT: You have defeated the lightning ghost.")
            objects.reports_on and print("NEW ABILITY: ELECTRODASH")
            objects.reports_on and print("Ability Information: The electrodash ability allows you to dash quickly to a spot on the screen, doing damage to everything in your path and not taking damage at all. This ability uses up 25 ghost energy per use. Press 4 to switch to the electrodash ability from another ability.")
            objects.FindQuest("The Lightning Boss").data = True
            data = map_description.portalLocations["lightning"]
            objects.player.chunk = data[0]
            objects.player.rect.center = data[1]
            map_description.show_chunk(*(map_description.portalLocations["poison"][0]))

            for i in objects.chunks[data[0][0]][data[0][1]].contents: 
                if type(i) == MapClasses.CollisionButton: 
                    objects.chunks[data[0][0]][data[0][1]].contents.remove(i)
                    return

class PoisonGhostBoss(Enemy):
    def __init__(self):
        self.image = pygame.image.load(create_path("Poison Boss.png"))
        self.rect =  self.image.get_rect()
        self.rect.center = (50,50)
        self.type = "enemy"
        self.maxHealth = 800
        self.health = self.maxHealth
        self.moving = False
        self.attackDamage = 20
        self.counter = 0
        self.pools = [(50,50),(450,50),(50,450),(450,450)]
        self.waitTime = 5
    def render(self): 
        objects.display.blit(self.image, self.rect)
        pygame.draw.rect(objects.display, (15,15,15), pygame.Rect(150,25,200,20))
        pygame.draw.rect(objects.display, (255,0,0), pygame.Rect(150,25,self.health/self.maxHealth*200,20))
    def update(self):
        # if boss is appearing we want him to fire and then wait around (Yuan)
        if self.counter < 6: 
            y = (self.counter/5)
            self.image.set_alpha(y*((self.health/self.maxHealth)*255))

        elif self.counter == 6:
            objects.currentChunk.contents.append(PoisonDrop(self.rect.center, objects.player.rect.center))
            objects.currentChunk.contents.append(PoisonDrop(self.rect.center, (random.randint(100,400),random.randint(100,400))))
            objects.currentChunk.contents.append(PoisonDrop(self.rect.center, (random.randint(100,400),random.randint(100,400))))

        # waiting around count down till moves again (Max)
        elif self.counter < objects.framerate*self.waitTime:
            pass
        # disappearing then reappear somewhere else
        else:
            y = 255-((self.counter-objects.framerate*self.waitTime)/5)*255
            self.image.set_alpha(y)

        if self.counter == objects.framerate*self.waitTime + 5:
            self.counter = 0
            self.rect.center = random.choice(self.pools)
            #print(self.rect.center)
        else:
            self.counter += 1
            
        # Dying
        if self.health <= 0: 
            objects.currentChunk.contents.remove(self)
            objects.player.maxHealth = objects.player.maxHealth + 25
            objects.player.maxEnergy = objects.player.maxEnergy + 25
            objects.resourceAmounts["ghostEnergy"] = objects.player.maxEnergy
            objects.player.currentHealth = objects.player.maxHealth
            objects.abilities[4] = Abilities.SummonPoison()
            objects.reports_on and print("REPORT: You have defeated the poison ghost.")
            objects.reports_on and print("NEW ABILITY: POISON FIELD")
            objects.reports_on and print("Ability Information: The poison field ability deals damage over time to enemies near you. This ability uses up 25 ghost energy per use. Press 5 to switch to the poison field ability from another ability.")
            objects.FindQuest("The Poison Boss").data = True
            data = map_description.portalLocations["poison"]
            objects.player.chunk = data[0]
            objects.player.rect.center = data[1]
            map_description.show_chunk(*(map_description.portalLocations["summoner"][0]))

            for i in objects.chunks[data[0][0]][data[0][1]].contents: 
                if type(i) == MapClasses.CollisionButton: 
                    objects.chunks[data[0][0]][data[0][1]].contents.remove(i)
                    return

class SummoningGhostBoss(Enemy):
    def __init__(self):
        self.image = pygame.image.load(create_path("Summoning Boss.png"))
        self.rect =  self.image.get_rect()
        self.rect.center = (250,250)
        self.type = "enemy"
        self.maxHealth = 1000
        self.health = self.maxHealth
        self.attackDamage = 75
        self.speed = 2
        self.counter = 0
    def render(self): 
        objects.display.blit(self.image, self.rect)
        pygame.draw.rect(objects.display, (15,15,15), pygame.Rect(150,25,200,20))
        pygame.draw.rect(objects.display, (255,0,0), pygame.Rect(150,25,self.health/self.maxHealth*200,20))
    def update(self):
        # Movement
        playerX = objects.player.rect.center[0] 
        playerY = objects.player.rect.center[1]
        xGap = playerX - self.rect.center[0] 
        yGap = playerY - self.rect.center[1] 
        distance = (xGap**2+yGap**2)**(1/2)
        if distance != 0:
            factor = distance/self.speed
            moveX = xGap / factor
            moveY = yGap / factor
        self.rect = (self.rect.move((moveX, moveY)))
        if self.rect.colliderect(objects.player.rect): 
            if not objects.player.invulnerability: 
                objects.player.currentHealth -= self.attackDamage
            while self.rect.colliderect(objects.player.rect): 
                self.rect.center = (random.randint(0,objects.WINDOWWIDTH), random.randint(0, objects.WINDOWHEIGHT))
        # Spawning
        if self.counter == objects.framerate * 1.5: 
            newGhost = Ghost(self.rect.center)
            newGhost.speed = 4
            objects.currentChunk.contents.append(newGhost)
            self.counter = 0
        else:
            self.counter += 1
        # Dying
        if self.health <= 0: 
            objects.currentChunk.contents.remove(self)
            objects.player.maxHealth = objects.player.maxHealth + 25
            objects.player.maxEnergy = objects.player.maxEnergy + 25
            objects.resourceAmounts["ghostEnergy"] = objects.player.maxEnergy
            objects.player.currentHealth = objects.player.maxHealth
            objects.abilities[5] = Abilities.SummonGhost()
            objects.reports_on and print("REPORT: You have defeated the summoning ghost.")
            objects.reports_on and print("NEW ABILITY: GHOST SUMMONING")
            objects.reports_on and print("Ability Information: The summoning ability summons a ghost that follows your mouse around the screen. This ability uses up 25 ghost energy per use. Press 6 to switch to the summoning ability from another ability.")
            objects.FindQuest("The Summoning Boss").data = True
            data = map_description.portalLocations["summoner"]
            objects.player.chunk = data[0]
            objects.player.rect.center = data[1]
            map_description.show_chunk(*(map_description.portalLocations["shield"][0]))

            for i in objects.chunks[data[0][0]][data[0][1]].contents: 
                if type(i) == MapClasses.CollisionButton: 
                    objects.chunks[data[0][0]][data[0][1]].contents.remove(i)
                    return

class ShieldGhostBoss(Enemy):
    def __init__(self):
        self.image = pygame.image.load(create_path("Summoning Boss.png"))
        self.rect =  self.image.get_rect()
        self.rect.center = (250,50)
        self.type = "enemy"
        self.maxHealth = 1200
        self.health = self.maxHealth
        self.counter = 0
        self.cooldown = objects.framerate*(random.randint(1,3))
        self.direction = (5,0)
        self.attackDamage = 25
    def render(self):
        objects.display.blit(self.image, self.rect)
        pygame.draw.rect(objects.display, (15,15,15), pygame.Rect(150,25,200,20))
        pygame.draw.rect(objects.display, (255,0,0), pygame.Rect(150,25,self.health/self.maxHealth*200,20))
    def update(self):
        # Movement
        self.rect = self.rect.move(self.direction)
        if not pygame.Rect(0,0,500,500).contains(self.rect): 
            self.direction = (-self.direction[0],0)
        if self.rect.colliderect(objects.player.rect): 
            if not objects.player.invulnerability: 
                objects.player.currentHealth -= self.attackDamage
            while self.rect.colliderect(objects.player.rect): 
                self.rect.center = (random.randint(50,objects.WINDOWWIDTH-50), 50)
        if self.counter % self.cooldown == 0: 
            objects.currentChunk.contents.append(Shield(self.rect.centerx))
        self.counter += 1

        # Dying
        if self.health <= 0: 
            objects.currentChunk.contents.remove(self)
            objects.player.maxHealth = objects.player.maxHealth + 25
            objects.player.maxEnergy = objects.player.maxEnergy + 25
            objects.resourceAmounts["ghostEnergy"] = objects.player.maxEnergy
            objects.player.currentHealth = objects.player.maxHealth
            objects.abilities[6] = Abilities.MakeMagicalShield()
            print("REPORT: You have defeated the shield ghost.")
            print("NEW ABILITY: MAGICAL SHIELD")
            print("Ability Information: The magical shield ability makes you immune to taking damage. This ability uses up 25 ghost energy per use. Press 7 to switch to the poison field ability from another ability.")
            objects.FindQuest("The Shield Boss").data = True
            data = map_description.portalLocations["shield"]
            objects.player.chunk = data[0]
            objects.player.rect.center = data[1]
            map_description.show_chunk(*(map_description.portalLocations["laser"][0]))

            for i in objects.chunks[data[0][0]][data[0][1]].contents: 
                if type(i) == MapClasses.CollisionButton: 
                    objects.chunks[data[0][0]][data[0][1]].contents.remove(i)
                    return
            

class LaserGhostBoss(Enemy): 
    def __init__(self):
        self.image = pygame.image.load(create_path("Laser Boss.png"))
        self.rect =  self.image.get_rect()
        self.rect.center = (50,50)
        self.type = "enemy"
        self.maxHealth = 1400
        self.health = self.maxHealth
        self.moving = False
        self.attackDamage = 50
        self.counter = 0
        self.targets = [(50,50),(450,50),(50,450),(450,450)]
        self.target = (450,450)
        self.waitTime = 5
        self.direction = None
        self.speed = 25
        self.laserMoveX = 0
        self.laserMoveY = 0 
        self.laserRotation = 0
    def render(self): 
        
        objects.display.blit(self.image, self.rect)
        pygame.draw.rect(objects.display, (15,15,15), pygame.Rect(150,25,200,20))
        pygame.draw.rect(objects.display, (255,0,0), pygame.Rect(150,25,self.health/self.maxHealth*200,20))
    def update(self):
        # if boss is appearing we want him to fire and then wait around 
        '''if self.counter < 6: 
            pass # don't do anything

        elif self.counter == 6:
            pass # shoot laser'''
        if self.counter == objects.framerate: 
            playerPos = objects.player.rect.center
            xGap = playerPos[0] - self.rect.center[0]
            yGap = playerPos[1] - self.rect.center[1] 
            distance = (xGap**2+yGap**2)**(1/2)
            if yGap == 0:
                yGap = .01
            if distance != 0:
                factor = distance/50 # note: the divisor here is the speed of the laser (for future changes)
                self.laserMoveX = xGap / factor
                self.laserMoveY = yGap / factor
                self.laserRotation =  math.degrees(math.atan(xGap / yGap)) + 90 # y/x
            if yGap > 0:
                self.laserRotation += 180
        # waiting around count down till moves again 
        if self.counter < objects.framerate*(self.waitTime-3) and self.counter > objects.framerate:
            
            objects.currentChunk.contents.append(EnemyLaser((self.laserMoveX, self.laserMoveY), self.laserRotation, self.rect.center))



        # disappearing then reappear somewhere else
        elif self.counter == objects.framerate*self.waitTime:
            while self.target == self.rect.center: 
                self.target = random.choice(self.targets)
            location = self.rect.center 
            xGap = self.target[0]-self.rect.centerx
            yGap = self.target[1]-self.rect.centery 
            distance = (xGap**2+yGap**2)**(1/2)
            if distance != 0:
                factor = distance/self.speed
                moveX = xGap / factor
                moveY = yGap / factor
                self.direction = (moveX, moveY)
                self.moving = True 
        else: 
            pass 
        if self.moving: 
            self.rect = self.rect.move(self.direction[0],self.direction[1])
            if self.rect.center == self.target: 
                self.moving = False 
                self.counter = 0
                self.direction = (0,0)
        else: 
            self.counter += 1
        
        #going diagonally 
        if self.rect.left < 0: 
            self.rect.left = 0 
            self.moving = False
            self.counter = 0
            self.direction = (0,0)
        if self.rect.right > 500: 
            self.rect.right = 500 
            self.moving = False
            self.counter = 0
            self.direction = (0,0)
        if self.rect.top < 0: 
            self.rect.top = 0  
            self.moving = False
            self.counter = 0
            self.direction = (0,0)
        if self.rect.bottom > 500: 
            self.rect.bottom = 500 
            self.moving = False 
            self.counter = 0
            self.direction = (0,0)

        # Dying
        if self.health <= 0: 
            objects.currentChunk.contents.remove(self)
            objects.player.maxHealth = objects.player.maxHealth + 25
            objects.player.maxEnergy = objects.player.maxEnergy + 25
            objects.resourceAmounts["ghostEnergy"] = objects.player.maxEnergy
            objects.player.currentHealth = objects.player.maxHealth
            objects.abilities[7] = Abilities.FireLaserArrow()
            print("REPORT: You have defeated the laser ghost.")
            print("NEW ABILITY: LASER ARROW")
            print("Ability Information: The laser arrow ability allows you to shoot a large arrow that passes through enemies, dealing high damage. This ability uses up 25 ghost energy per use. Press 8 to switch to the laser arrow ability from another ability.")
            objects.FindQuest("The Laser Boss").data = True
            data = map_description.portalLocations["laser"]
            objects.player.chunk = data[0]
            objects.player.rect.center = data[1]
            map_description.show_chunk(*(map_description.portalLocations["water"][0]))

            for i in objects.chunks[data[0][0]][data[0][1]].contents: 
                if type(i) == MapClasses.CollisionButton: 
                    objects.chunks[data[0][0]][data[0][1]].contents.remove(i)
                    return

class WaterGhostBoss: 
    def __init__(self):
        self.image = pygame.image.load(create_path("Ice Boss.png"))
        self.rect =  self.image.get_rect()
        self.rect.center = (250,250)
        self.type = "enemy"
        self.maxHealth = 1600
        self.health = self.maxHealth
        self.moving = False
        self.counter = 0
        self.waitTime = 5
    def render(self): 
        objects.display.blit(self.image, self.rect)
        pygame.draw.rect(objects.display, (15,15,15), pygame.Rect(150,25,200,20))
        pygame.draw.rect(objects.display, (255,0,0), pygame.Rect(150,25,self.health/self.maxHealth*200,20))
    def update(self):
        # if boss is appearing we want him to fire and then wait around (Yuan)
        if self.counter < 6: 
            y = (self.counter/5)
            self.image.set_alpha(y*(self.health/self.maxHealth)*255)

        elif self.counter == 6:
            playerPos = objects.player.rect.center
            xGap = playerPos[0] - self.rect.center[0]
            yGap = playerPos[1] - self.rect.center[1] 
            distance = (xGap**2+yGap**2)**(1/2)
            if yGap == 0:
                yGap = .01
            if distance != 0:
                factor = distance/10 # note: the divisor here is the speed of the wave (for future changes)
                moveX = xGap / factor
                moveY = yGap / factor
                rotationAngle =  math.degrees(math.atan(xGap / yGap)) + 90 # y/x
            if yGap > 0:
                rotationAngle += 180
            objects.currentChunk.contents.append(EnemyWave((moveX, moveY), rotationAngle, self.rect.center))

        # waiting around count down till moves again (Max)
        elif self.counter < objects.framerate*self.waitTime:
            pass
        # disappearing then reappear somewhere else
        else:
            y = 255-((self.counter-objects.framerate*self.waitTime)/5)*255
            self.image.set_alpha(y)

        if self.counter == objects.framerate * self.waitTime + 5:
            self.counter = 0
            self.rect.center = (random.randint(150,350),random.randint(150,350))
            #print(self.rect.center)
        else:
            self.counter += 1
            
        # Dying
        if self.health <= 0: 
            objects.currentChunk.contents.remove(self)
            objects.player.maxHealth = objects.player.maxHealth + 25
            objects.player.maxEnergy = objects.player.maxEnergy + 25
            objects.resourceAmounts["ghostEnergy"] = objects.player.maxEnergy
            objects.player.currentHealth = objects.player.maxHealth
            objects.abilities[8] = Abilities.LaunchWave()
            print("REPORT: You have defeated the water ghost.")
            print("NEW ABILITY: WAVE")
            print("Ability Information: The wave ability launches 4 large waves in different directions. These waves deal damage over time to enemies that they collide with, and pull/push non-boss enemies along with them (dealing more damage). This ability uses up 25 ghost energy per use. Press 9 to switch to the wave ability from another ability.")
            objects.FindQuest("The Water Boss").data = True
            data = map_description.portalLocations["water"]
            objects.player.chunk = data[0]
            objects.player.rect.center = data[1]
            map_description.show_chunk(*(map_description.portalLocations["final"][0]))

            for i in objects.chunks[data[0][0]][data[0][1]].contents: 
                if type(i) == MapClasses.CollisionButton: 
                    objects.chunks[data[0][0]][data[0][1]].contents.remove(i)
                    return

class FinalBossGhost(Enemy):
    def __init__(self): 
        self.neutralImage = pygame.image.load(create_path("NeutralFB.png"))
        self.fireImage = pygame.image.load(create_path("FireFB.png"))
        self.iceImage = pygame.image.load(create_path("IceFB.png"))
        self.lightningImage = pygame.image.load(create_path("LightningFB.png"))
        self.poisonImage = pygame.image.load(create_path("PoisonFB.png"))
        self.summoningImage = pygame.image.load(create_path("SummoningFB.png"))
        self.shieldImage = pygame.image.load(create_path("ShieldFB.png"))
        self.laserImage = pygame.image.load(create_path("LaserFB.png"))
        self.waterImage = pygame.image.load(create_path("WaterFB.png"))
        self.images = [self.neutralImage, self.fireImage, self.iceImage, self.lightningImage, self.poisonImage,self.summoningImage,self.shieldImage, self.laserImage, self.waterImage]
        self.currentState = 0
        self.rect = pygame.Rect(0,0,100,100)
        self.rect.center = (250,150)
        self.maxHealth = 3000 
        self.health = self.maxHealth 
        self.type = "enemy" 
        self.counter = 0
        self.waitTime = 3 
        self.image = self.neutralImage
        self.direction = (0,0)
        self.moving = False
        self.attackDamage = 1
        self.angle = 0
        self.iceDir = 0
        self.shadowImage = pygame.image.load(create_path("Lightning Boss Shadow.png"))
        self.shadowRect = pygame.Rect(0,0,100,100)
        self.nextLocation = (250,150)
        self.lightningCounter = 0
    def render(self): 
        objects.display.blit(self.image, self.rect)
        pygame.draw.rect(objects.display, (15,15,15), pygame.Rect(150,50,200,20))
        pygame.draw.rect(objects.display, (255,0,0), pygame.Rect(150,50,self.health/self.maxHealth*200,20))

        if self.lightningCounter >= objects.framerate/2 and self.currentState == 3: 
            objects.display.blit(self.shadowImage, self.shadowRect)
    def update(self): 
        self.counter += 1
        if self.counter == objects.framerate * self.waitTime: 
            if self.rect.center == (250,150): 
                self.currentState = random.randint(1,8)
                self.image = self.images[self.currentState] 
                self.counter = 0
            else: 
                self.currentState = 0 
                self.image = self.images[0]
                xDist = 250 - self.rect.center[0]
                yDist = 150 - self.rect.center[1]
                totalDist = (xDist**2 + yDist**2)**.5
                '''if 25 > totalDist:
                    self.rect.center = (250,150)
                else:
                '''
                angle = math.atan2(yDist,xDist)
                xSpeed = math.cos(angle)*25
                ySpeed = math.sin(angle)*25
                self.direction = (xSpeed, ySpeed)
        if self.currentState == 1: #Fire 
            if self.rect.left < 0: 
                self.angle = random.random() * math.pi - math.pi/2
            if self.rect.right > objects.WINDOWWIDTH: 
                self.angle = random.random() * math.pi + math.pi/2
            if self.rect.top < 0: 
                self.angle = random.random() * math.pi + math.pi
            if self.rect.bottom > objects.WINDOWHEIGHT: 
                self.angle = random.random() * math.pi
            # Moving
            self.rect.center = (self.rect.centerx + 4*math.cos(self.angle), self.rect.centery - 4*math.sin(self.angle))

            if self.counter % objects.framerate == 0:
                playerPos = objects.player.rect.center
                xGap = playerPos[0] - self.rect.center[0]
                yGap = playerPos[1] - self.rect.center[1] 
                distance = (xGap**2+yGap**2)**(1/2)
                if yGap == 0:
                    yGap = .01
                if distance != 0:
                    factor = distance/5
                    moveX = xGap / factor
                    moveY = yGap / factor
                    rotation =  math.degrees(math.atan(xGap / yGap)) + 90 # y/x
                if yGap > 0:
                    rotation += 180
                objects.currentChunk.contents.append(EnemyFireball((3*moveX, 3*moveY), rotation, self.rect.center))
        if self.currentState == 2: #Ice 
            
            # Changing directions after bouncing
            if self.rect.left < 0 or self.rect.right > objects.WINDOWWIDTH or self.rect.top < 0 or self.rect.bottom > objects.WINDOWHEIGHT:
                playerPos = objects.player.rect.center
                xGap = playerPos[0] - self.rect.centerx
                yGap = playerPos[1] - self.rect.centery
                if xGap == 0:
                    xGap = .01
                self.iceDir = math.atan(yGap / xGap)
                if xGap < 0:
                    self.iceDir += math.pi
            # Moving
            self.rect.center = (self.rect.centerx + 5*math.cos(self.iceDir), self.rect.centery + 5*math.sin(self.iceDir))
            
            # Shooting icicles on a timer
            if self.counter % objects.framerate == 0:
                playerPos = objects.player.rect.center
                xGap = playerPos[0] - self.rect.center[0]
                yGap = playerPos[1] - self.rect.center[1] 
                distance = (xGap**2+yGap**2)**(1/2)
                if yGap == 0:
                    yGap = .01
                if distance != 0:
                    factor = distance/5
                    moveX = xGap / factor * 2
                    moveY = yGap / factor * 2
                    rotation =  math.degrees(math.atan(xGap / yGap)) + 90
                if yGap > 0:
                    rotation += 180
                objects.currentChunk.contents.append(EnemyIcicle((4*moveX, 4*moveY), rotation, self.rect.center))
        if self.currentState == 3: #Lightning 
            if self.rect.center == self.nextLocation:
                self.nextLocation = (random.randint(0,500),random.randint(0,500))
                self.shadowRect.center = self.nextLocation
                self.moving = False
                self.lightningCounter = 0
            self.lightningCounter += 1
            if not self.moving: 
                if self.lightningCounter == objects.framerate:
                    self.moving = True
            else: 
                # Moving
                xDist = self.nextLocation[0] - self.rect.center[0]
                yDist = self.nextLocation[1] - self.rect.center[1]
                totalDist = (xDist**2 + yDist**2)**.5
                if 25 > totalDist:
                    self.rect.center = self.nextLocation
                else:
                    xSpeed = xDist / totalDist * 25
                    ySpeed = yDist / totalDist * 25
                    self.rect = self.rect.move(xSpeed, ySpeed) 
        if self.currentState == 4: #Poison 
            if self.counter == objects.framerate:
                objects.currentChunk.contents.append(PoisonDrop(self.rect.center, objects.player.rect.center))
                objects.currentChunk.contents.append(PoisonDrop(self.rect.center, (random.randint(100,400),random.randint(100,400))))
                objects.currentChunk.contents.append(PoisonDrop(self.rect.center, (random.randint(100,400),random.randint(100,400)))) 
                objects.currentChunk.contents.append(PoisonDrop(self.rect.center, (random.randint(100,400),random.randint(100,400))))
                objects.currentChunk.contents.append(PoisonDrop(self.rect.center, (random.randint(100,400),random.randint(100,400))))
                objects.currentChunk.contents.append(PoisonDrop(self.rect.center, (random.randint(100,400),random.randint(100,400))))
                objects.currentChunk.contents.append(PoisonDrop(self.rect.center, (random.randint(100,400),random.randint(100,400))))
                objects.currentChunk.contents.append(PoisonDrop(self.rect.center, (random.randint(100,400),random.randint(100,400))))
                objects.currentChunk.contents.append(PoisonDrop(self.rect.center, (random.randint(100,400),random.randint(100,400))))
                objects.currentChunk.contents.append(PoisonDrop(self.rect.center, (random.randint(100,400),random.randint(100,400))))
        if self.currentState == 5: #Summoning
            playerX = objects.player.rect.center[0] 
            playerY = objects.player.rect.center[1]
            xGap = playerX - self.rect.center[0] 
            yGap = playerY - self.rect.center[1] 
            distance = (xGap**2+yGap**2)**(1/2)
            if distance != 0:
                factor = distance/2
                moveX = xGap / factor
                moveY = yGap / factor
            self.rect = (self.rect.move((moveX, moveY)))
            if self.rect.colliderect(objects.player.rect): 
                if not objects.player.invulnerability: 
                    objects.player.currentHealth -= self.attackDamage
                while self.rect.colliderect(objects.player.rect): 
                    self.rect.center = (random.randint(0,objects.WINDOWWIDTH), random.randint(0, objects.WINDOWHEIGHT))
            # Spawning
            if self.counter % objects.framerate == 0: 
                newGhost = LargeGhost(self.rect.center)
                newGhost.speed = 5
                objects.currentChunk.contents.append(newGhost)
        if self.currentState == 6: #Shield 
            if self.rect.colliderect(objects.player.rect): 
                if not objects.player.invulnerability: 
                    objects.player.currentHealth -= self.attackDamage
            if self.counter % objects.framerate == 0: 
                objects.currentChunk.contents.append(Shield(self.rect.centerx))
        if self.currentState == 7: #Laser 
            if self.counter == objects.framerate: 
                playerPos = objects.player.rect.center
                xGap = playerPos[0] - self.rect.center[0]
                yGap = playerPos[1] - self.rect.center[1] 
                distance = (xGap**2+yGap**2)**(1/2)
                if yGap == 0:
                    yGap = .01
                if distance != 0:
                    factor = distance/50 # note: the divisor here is the speed of the laser (for future changes)
                    self.laserMoveX = xGap / factor
                    self.laserMoveY = yGap / factor
                    self.laserRotation =  math.degrees(math.atan(xGap / yGap)) + 90 # y/x
                if yGap > 0:
                    self.laserRotation += 180
            # waiting around count down till moves again 
            if self.counter < objects.framerate*(self.waitTime-1) and self.counter > objects.framerate:
                playerPos = objects.player.rect.center
                xGap = playerPos[0] - self.rect.center[0]
                yGap = playerPos[1] - self.rect.center[1] 
                distance = (xGap**2+yGap**2)**(1/2)
                if yGap == 0:
                    yGap = .01
                if distance != 0:
                    factor = distance/15 # note: the divisor here is the speed of the laser (for future changes)
                    self.laserMoveX = xGap / factor
                    self.laserMoveY = yGap / factor
                    self.laserRotation =  math.degrees(math.atan(xGap / yGap)) + 90 # y/x
                if yGap > 0:
                    self.laserRotation += 180
                objects.currentChunk.contents.append(EnemyLaser((self.laserMoveX, self.laserMoveY), self.laserRotation, self.rect.center))
        if self.currentState == 8: #Water 
            if self.counter == objects.framerate:
                playerPos = objects.player.rect.center
                xGap = playerPos[0] - self.rect.center[0]
                yGap = playerPos[1] - self.rect.center[1] 
                distance = (xGap**2+yGap**2)**(1/2)
                if yGap == 0:
                    yGap = .01
                if distance != 0:
                    factor = distance/10 # note: the divisor here is the speed of the wave (for future changes)
                    moveX = xGap / factor
                    moveY = yGap / factor
                    rotationAngle =  math.degrees(math.atan(xGap / yGap)) + 90 # y/x
                if yGap > 0:
                    rotationAngle += 180
                objects.currentChunk.contents.append(EnemyWave((3*moveX, 3*moveY), rotationAngle, self.rect.center))

        if self.rect.colliderect(objects.player.rect): 
            if not objects.player.invulnerability: 
                objects.player.currentHealth = objects.player.currentHealth - self.attackDamage
        
        if self.counter > objects.framerate * self.waitTime: 
            self.rect = self.rect.move(self.direction)
            if self.rect.contains(pygame.Rect(225,125,50,50)): 
                self.rect.center = (250,150)
                self.currentState = random.randint(1,8)
                self.image = self.images[self.currentState] 
                self.counter = 0
                self.direction = (0,0)

        # Dying
        if self.health <= 0: 
            objects.currentChunk.contents.remove(self)
            objects.resourceAmounts["ghostEnergy"] = objects.player.maxEnergy
            objects.player.currentHealth = objects.player.maxHealth
            objects.player.chunk = (0,0)
            objects.player.rect.center = (400,400)
            print("REPORT: You have defeated the dark ghost.")
            print("GAME COMPLETE!")
            data = map_description.portalLocations["final"]
            objects.player.chunk = data[0]
            objects.player.rect.center = data[1]
            for i in objects.chunks[data[0][0]][data[0][1]].contents: 
                if type(i) == MapClasses.CollisionButton: 
                    objects.chunks[data[0][0]][data[0][1]].contents.remove(i)
                    return

class EnemyWave:
    def __init__(self,direction,rotationAngle,location):
        self.image = pygame.image.load(create_path("Wave.png"))
        if rotationAngle > 360: 
            rotationAngle -= 360
        self.image = pygame.transform.scale(self.image, (100,200))
        self.image = pygame.transform.rotate(self.image, rotationAngle)
    
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.direction = direction
        self.attackDamage = 1
        self.type = "wave"
    def render(self):
        #pygame.draw.rect(objects.screen, "#000000", self.rect) 
        objects.display.blit(self.image, self.rect)
    def update(self):
        self.rect = self.rect.move(self.direction)
        if not self.rect.colliderect(pygame.Rect(0,0,500,500)):
            objects.currentChunk.contents.remove(self)
        if self.rect.colliderect(objects.player.rect): 
            objects.player.knocked = True 
            objects.player.rect = objects.player.rect.move(self.direction[0],self.direction[1])
            objects.player.currentHealth -= self.attackDamage

class EnemyLaser: 
    def __init__(self,direction,rotationAngle,spawnPos):
        self.image = pygame.image.load(create_path("Fireball.png"))
        self.image = pygame.transform.rotate(self.image, rotationAngle)
        # self.image = pygame.transform.scale(self.image, (20,10))
        self.rect = self.image.get_rect()
        self.rect.center = spawnPos
        self.direction = direction
        self.attackDamage = 5
        self.type = "enemyProjectile"
    def render(self):
        # pygame.draw.rect(objects.screen, "#000000", self.rect) 
        objects.display.blit(self.image, self.rect)
    def update(self):
        self.rect = self.rect.move(self.direction)
        if self.rect.colliderect(objects.player.rect): 
            if not objects.player.invulnerability: 
                objects.player.currentHealth = objects.player.currentHealth - self.attackDamage 
            objects.currentChunk.contents.remove(self)

        elif not objects.display.get_rect().colliderect(self.rect):
            objects.currentChunk.contents.remove(self)

class Shield: 
    def __init__(self,xPos): 
        self.image = pygame.image.load(create_path("Silver Coin.png"))
        self.image = pygame.transform.scale(self.image, (100,25))
        self.rect = self.image.get_rect() 
        self.rect.top = 100
        self.type = "enemy"
        self.direction = (5,1)
        self.damage = 10
        self.rect.centerx = xPos
        self.maxHealth = 50
        self.health = self.maxHealth
        self.knocked = False
    def render(self): 
        self.image.set_alpha((self.health/self.maxHealth)*255)
        objects.display.blit(self.image, self.rect)
        
        pygame.draw.rect(objects.display, (0,0,0), pygame.Rect(self.rect.left,self.rect.top-self.rect[3]*.1,self.rect[2],self.rect[3]*.1))
        pygame.draw.rect(objects.display, (255,0,0), pygame.Rect(self.rect.left,self.rect.top-self.rect[3]*.1,self.rect[2]*(self.health/self.maxHealth),self.rect[3]*.1))
    def update(self): 
        self.rect = self.rect.move(self.direction)
        if not pygame.Rect(0,0,500,500).contains(self.rect): 
            self.direction = (self.direction[0]*(-1),1)
        if self.rect.bottom > objects.WINDOWHEIGHT: 
            objects.currentChunk.contents.remove(self) 
        elif self.rect.colliderect(objects.player.rect): 
            if not objects.player.invulnerability: 
                objects.player.currentHealth -= self.damage 
            objects.currentChunk.contents.remove(self)
        elif self.health <= 0: 
            objects.currentChunk.contents.remove(self)
    
class PoisonDrop: 
    def __init__(self, start, target): 
        self.start = start
        self.target = target
        self.image = pygame.image.load(create_path("Poison Drop.png"))
        self.rect = self.image.get_rect()
        self.rect.center = self.start
        self.speed = 15
        self.direction = 0
        xGap = self.target[0] - self.start[0]
        yGap = self.target[1] - self.start[1]
        self.direction = math.degrees(math.atan2(yGap,xGap))
        self.image = pygame.transform.rotate(self.image, self.direction + 90)
        self.type = "enemyProjectile"
    def render(self):
        
        objects.display.blit(self.image, self.rect)
        
    def update(self):
        self.rect = self.rect.move(self.speed*math.cos(math.radians(self.direction)), self.speed*math.sin(math.radians(self.direction)))
        if self.rect.colliderect(objects.player.rect) or self.rect.collidepoint(self.target): 
            objects.currentChunk.contents.append(PoisonPool(self.rect.center))
            objects.currentChunk.contents.remove(self)
        elif not objects.display.get_rect().contains(self.rect):
            objects.currentChunk.contents.remove(self)

class PoisonPool:
    def __init__(self,pos):
        self.image = pygame.image.load(create_path("Poison Puddle.png"))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.timer = 0
        self.damage = 1
        self.type = "enemy projectile"
    def update(self):
        # If collide with player do 1 damage
        if self.rect.colliderect(objects.player.rect): 
            if not objects.player.invulnerability: 
                objects.player.currentHealth -= self.damage
        # If timer is 5s delete self
        if self.timer == objects.framerate*10: 
            objects.currentChunk.contents.remove(self)
        # Increase timer
        self.timer += 1
    def render(self):
        objects.display.blit(self.image, self.rect)

class EnemyIcicle:
    def __init__(self,direction,rotationAngle,spawnPos):
        self.image = pygame.image.load(create_path("Icicle.png"))
        self.image = pygame.transform.rotate(self.image, rotationAngle)
        self.rect = self.image.get_rect()
        self.rect.center = spawnPos
        self.direction = direction
        self.attackDamage = 10
        self.type = "enemyProjectile"
    def render(self):
        # pygame.draw.rect(objects.screen, "#000000", self.rect) 
        objects.display.blit(self.image, self.rect)
    def update(self):
        self.rect = self.rect.move(self.direction)
        if self.rect.colliderect(objects.player.rect): 
            if not objects.player.invulnerability: 
                objects.player.currentHealth = objects.player.currentHealth - self.attackDamage 
            objects.currentChunk.contents.remove(self)
        elif not objects.display.get_rect().contains(self.rect):
            objects.currentChunk.contents.remove(self)

class EnemyFireball:
    def __init__(self,direction,rotationAngle,spawnPos):
        self.image = pygame.image.load(create_path("Fireball.png"))
        self.image = pygame.transform.rotate(self.image, rotationAngle)
        self.rect = self.image.get_rect()
        self.rect.center = spawnPos
        self.direction = direction
        self.attackDamage = 10
        self.type = "enemyProjectile"
    def render(self):
        # pygame.draw.rect(objects.screen, "#000000", self.rect) 
        objects.display.blit(self.image, self.rect)
    def update(self):
        self.rect = self.rect.move(self.direction)
        if self.rect.colliderect(objects.player.rect): 
            if not objects.player.invulnerability: 
                objects.player.currentHealth = objects.player.currentHealth - self.attackDamage 
            objects.currentChunk.contents.remove(self)

        elif not objects.display.get_rect().contains(self.rect):
            objects.currentChunk.contents.remove(self)