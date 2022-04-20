from cmath import cos
import pygame
import objects
import math
from BasicClasses import Obj
from images import create_path

class AbilityObject(Obj):
    def __init__(self, image, location=(0,0)):
        super().__init__(image, location)
        self.type = "abilityObject"


class Ability():
    def __init__(self, cost=25, cooldown=30):
        self.cost = cost
        self.cooldown = cooldown 
        self.orignal_cooldown = cooldown

    def update(self):
        # print(self.cooldown, self.cost, object)
        if self.cooldown > 0:
            self.cooldown -= 1
            return False
        
        if objects.currentChunk == None:
            return False

        if objects.resourceAmounts["ghostEnergy"] < self.cost:
            return False
        
        if pygame.mouse.get_pressed(3)[0] and not objects.first_game_frame:
            objects.resourceAmounts["ghostEnergy"] -= self.cost
            self.cooldown = self.orignal_cooldown
            return True

    
    def render(self):
        return

class FireArrow(): # Ability 1: Fires an arrow projectile
    def __init__(self):
        self.fireRate = 0.5*objects.framerate
        self.cooldown = 0

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        if objects.currentChunk == None:
            return

        if pygame.mouse.get_pressed(3)[0]:
            mousePos = objects.mapMousePos(pygame.mouse.get_pos())
            mouseX = mousePos[0]
            mouseY = mousePos[1]
            xGap = mouseX - objects.player.rect.centerx 
            yGap = mouseY - objects.player.rect.centery
            if yGap == 0:
                yGap = 0.01 
            distance = (xGap**2+yGap**2)**(1/2)
            if distance != 0:
                factor = distance/20
                moveX = xGap / factor
                moveY = yGap / factor
                rotation =  math.degrees(math.atan(xGap / yGap)) + 90
                if yGap > 0:
                    rotation += 180
                objects.currentChunk.contents.append(Arrow((moveX, moveY), rotation))
            self.cooldown = self.fireRate
    
    def render(self):
        return

class Arrow(AbilityObject):
    def __init__(self,direction,rotationAngle):
        image = pygame.image.load(create_path("Arrow.png"))
        image = pygame.transform.rotate(image, rotationAngle)
        super().__init__(image, objects.player.rect.center)
        self.direction = direction
        self.attackDamage = 10
        self.type = "arrow"
    def update(self):
        self.rect = self.rect.move(self.direction)
        if not objects.display.get_rect().contains(self.rect):
            objects.currentChunk.contents.remove(self)
        for enemy in objects.currentChunk.contents:
            if enemy.type == "enemy" and self.rect.colliderect(enemy.rect):
                enemy.health -= self.attackDamage
                try:
                    objects.currentChunk.contents.remove(self)
                except ValueError:
                    print(f"something with the arrow {self} is wrong")
                break

class LaunchFireball(Ability):
    def __init__(self):
        super().__init__(25, .1 * objects.framerate)

    def update(self):
        if super().update():
            mousePos = objects.mapMousePos(pygame.mouse.get_pos())
            mouseX = mousePos[0]
            mouseY = mousePos[1]
            xGap = mouseX - objects.player.rect.centerx 
            yGap = mouseY - objects.player.rect.centery
            if yGap == 0:
                yGap = 0.01 
            distance = (xGap**2+yGap**2)**(1/2)
            if distance != 0:
                factor = distance/10
                moveX = xGap / factor
                moveY = yGap / factor
                rotation =  math.degrees(math.atan(xGap / yGap)) + 90
                if yGap > 0:
                    rotation += 180
                level = objects.levels[0] 
                if level == 1: 
                    objects.currentChunk.contents.append(Fireball("medium", "small", None, (moveX, moveY), rotation, objects.player.rect.center))
                elif level == 2: 
                    objects.currentChunk.contents.append(Fireball("large", "small", None, (moveX, moveY), rotation, objects.player.rect.center))
                elif level == 3: 
                    objects.currentChunk.contents.append(Fireball("medium", "medium", "small", (moveX, moveY), rotation, objects.player.rect.center))
                elif level == 4: 
                    objects.currentChunk.contents.append(Fireball("medium", "large", "small", (moveX, moveY), rotation, objects.player.rect.center))
                elif level == 5: 
                    objects.currentChunk.contents.append(Fireball("large", "large", "small", (moveX, moveY), rotation, objects.player.rect.center))

class Fireball(AbilityObject):
    def __init__(self,size, dropsize, dropsize2, direction,rotationAngle, position):
        super().__init__(pygame.image.load(create_path("Fireball.png")), position)
        self.size = size
        self.dropsize = dropsize
        self.dropsize2 = dropsize2
        self.attackDamage = 10
        if self.size == "small": 
            self.image = pygame.transform.scale(self.image, (20,10))
        elif self.size == "large": 
            self.image = pygame.transform.scale(self.image, (80,40))
        self.image = pygame.transform.rotate(self.image, rotationAngle)
        self.direction = direction
        self.type = "fireball"

    def update(self):
        self.rect = self.rect.move(self.direction)
        if not objects.display.get_rect().contains(self.rect):
            objects.currentChunk.contents.remove(self)
            if self.size == "medium":
                objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (10,0), 0, self.rect.center))
                objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (-10,0), 180, self.rect.center))
                objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (0,-10), 90, self.rect.center))
                objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (0,10), 270, self.rect.center))
            elif self.size == "large": 
                objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (10,0), 0, self.rect.center))
                objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (-10,0), 180, self.rect.center))
                objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (0,-10), 90, self.rect.center))
                objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (0,10), 270, self.rect.center))
                objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (7,7), 315, self.rect.center))
                objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (-7,7), 225, self.rect.center))
                objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (-7,-7), 135, self.rect.center))
                objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (7,-7), 45, self.rect.center))
            return
        for enemy in objects.currentChunk.contents:
            if enemy.type == "enemy" and self.rect.colliderect(enemy.rect):
                enemy.health -= self.attackDamage
                objects.currentChunk.contents.remove(self)
                if self.size == "medium":
                    objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (10,0), 0, self.rect.center))
                    objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (-10,0), 180, self.rect.center))
                    objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (0,-10), 90, self.rect.center))
                    objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (0,10), 270, self.rect.center))
                elif self.size == "large": 
                    objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (10,0), 0, self.rect.center))
                    objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (-10,0), 180, self.rect.center))
                    objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (0,-10), 90, self.rect.center))
                    objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (0,10), 270, self.rect.center))
                    objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (7,7), 315, self.rect.center))
                    objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (-7,7), 225, self.rect.center))
                    objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (-7,-7), 135, self.rect.center))
                    objects.currentChunk.contents.append(Fireball(self.dropsize, self.dropsize2, None, (7,-7), 45, self.rect.center))
                return

class Freeze(Ability): 
    def __init__(self):
        super().__init__(25, 50)
        self.amount_of_freeze = 100
        self.time_left_in_freeze = 0
    def update(self):
        if super().update():
            objects.freeze = True
            self.time_left_in_freeze = self.amount_of_freeze

    def freezeCD(self):
        if self.time_left_in_freeze == 0:
            objects.freeze = False
            return
        self.time_left_in_freeze -= 1

class ElectroDash(Ability):
    def __init__(self):
        super().__init__(25, .1 * objects.framerate)
        self.dashSpeed = 25
        self.damage = 25
        self.dashPositions = []

    def update(self):
        if len(self.dashPositions) != 0:
            
            # Move to first postition in list
            objects.player.rect.center = self.dashPositions[0]
            # Remove position
            self.dashPositions.remove(self.dashPositions[0])

            # Checking for collision with an obstacle
            for thing in objects.currentChunk.contents: 
                if thing.type == "obstacle" and objects.player.rect.colliderect(thing.rect): 
                    self.dashPositions = [] 
                    objects.player.hit_this_frame = True
                    return

            # Remember any enemies that we collide with
            collided = []
            for enemy in objects.currentChunk.contents: 
                if enemy.type == "enemy": 
                    if objects.player.rect.colliderect(enemy.rect): 
                        collided.append(enemy)
            # Damage collided enemies
            for enemy in collided: 
                enemy.health = enemy.health - self.damage
            if len(self.dashPositions) == 0:
                objects.player.invulnerability = False
                

        if self.cooldown > 0:
            self.cooldown -= 1
            return

        if objects.currentChunk == None:
            return

        if len(self.dashPositions) == 0 and pygame.mouse.get_pressed(3)[0] and objects.resourceAmounts["ghostEnergy"] >= self.cost:
            objects.resourceAmounts["ghostEnergy"] -= self.cost
            mousePos = objects.mapMousePos(pygame.mouse.get_pos())
            # Find the incremental amount to get there
            totalXdist = mousePos[0]-objects.player.rect.centerx
            totalYdist = mousePos[1]-objects.player.rect.centery
            totaldist  = (totalXdist**2+totalYdist**2)**.5
            ratio = totaldist/self.dashSpeed
            if ratio == 0:
                return
            # Find future positions
            if ratio > 1:
                xdist = totalXdist/ratio
                ydist = totalYdist/ratio
                x = objects.player.rect.centerx
                y = objects.player.rect.centery
                self.dashPositions.append((x + xdist, y + ydist))
                ratio -= 1
                while ratio > 1:
                    self.dashPositions.append((self.dashPositions[-1][0]+ xdist, self.dashPositions[-1][1]+ ydist))
                    ratio -= 1
            self.dashPositions.append(mousePos)
            objects.player.invulnerability = True

class SummonPoison(Ability):
    def __init__(self):
        super().__init__()
    
    def update(self):
        if super().update():
            print("summoned")
            mousePos = objects.mapMousePos(pygame.mouse.get_pos())
            objects.currentChunk.contents.append(PoisonField(mousePos))
    


class PoisonField(AbilityObject): 
    def __init__(self, pos): 
        image = pygame.image.load(create_path("Poison Effect.png"))
        image.set_alpha(150)
        super().__init__(image)
        self.rect.center = pos
        self.duration = 5 * objects.framerate
        self.damage = 1

    def update(self): 
        if self.duration >= 0:
            # Check for enemies and damage them
            for thing in objects.currentChunk.contents: 
                if thing.type == "enemy" and thing.rect.colliderect(self.rect): 
                    thing.health -= 1
            self.duration -= 1
        else:
            objects.currentChunk.contents.remove(self)

    def render(self):
        objects.display.blit(self.image, self.rect)

class SummonedGhost(Obj):
    def __init__(self): 
        super().__init__(pygame.image.load(create_path("Ghost Enemy.png")), (250,250))
        self.speed = 10
        self.attackDamage = 20
        self.type = "projectile"
        self.active = False
        self.counter = 10*objects.framerate
        self.lastChunk = objects.currentChunk
        self.rect.center = objects.player.rect.center
    def render(self): 
        self.image.set_alpha(self.counter/(objects.framerate * 10)*200+55)
        objects.display.blit(self.image, self.rect)
    def update(self): 
        # Check if the currentchunk is different
        # if it is move the position back to player
        if objects.currentChunk != self.lastChunk:
            self.rect.center = objects.player.rect.center
            self.lastChunk = objects.currentChunk
        
        mousePos = objects.mapMousePos(pygame.mouse.get_pos())
        xGap = mousePos[0] - self.rect.center[0] 
        yGap = mousePos[1] - self.rect.center[1] 
        distance = (xGap**2+yGap**2)**(1/2)
        if distance != 0:
            factor = distance/self.speed
            moveX = xGap / factor
            moveY = yGap / factor
            self.rect = self.rect.move((moveX, moveY))
        for enemy in objects.currentChunk.contents: 
            if enemy.type == "enemy" and self.rect.colliderect(enemy.rect): 
                enemy.health -= self.attackDamage 
                self.rect.center = objects.player.rect.center
        if self.counter <= 0: 
            objects.currentChunk.contents.remove(self)
        self.counter -= 1

class SummonGhost(Ability):
    def __init__(self): 
        super().__init__()
    
    def update(self): 
        if super().update(): 
            for thing in objects.currentChunk.contents: 
                if type(thing) == SummonedGhost: 
                    thing.counter = 10*objects.framerate
                    return
            objects.currentChunk.contents.append(SummonedGhost())

class MakeMagicalShield(Ability):
    def __init__(self):
        self.shield = MagicalShield()
        super().__init__(cooldown=self.shield.duration+1*objects.framerate)

    def render(self):
        if self.shield.active:
            self.shield.render()   
        
    
    def update(self):
        if super().update():
            self.shield.active = True
            self.shield.cooldown = self.shield.duration
        if self.shield.active:
            self.shield.update()

class MagicalShield(AbilityObject): 
    def __init__(self): 
        super().__init__(pygame.image.load(create_path("Magical Shield.png")))
        self.cooldown = 0
        self.duration = 5 * objects.framerate
        self.cost = 25
        self.active = False
    def render(self): 
        if self.active: 
            objects.display.blit(self.image, self.rect)
    def update(self): 
        self.rect.center = objects.player.rect.center
        objects.player.invulnerability = True 
        self.cooldown -= 1
        if self.cooldown == 0: 
            self.active = False 
            objects.player.invulnerability = False 

class FireLaserArrow(): # Ability 8: Fires a laser arrow projectile
    def __init__(self):
        self.fireRate = .5 * objects.framerate
        self.cooldown = 0
        self.cost = 25
    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        if objects.currentChunk == None:
            return

        if pygame.mouse.get_pressed(3)[0] and objects.resourceAmounts["ghostEnergy"] >= self.cost:
            objects.resourceAmounts["ghostEnergy"] -= self.cost
            mousePos = objects.mapMousePos(pygame.mouse.get_pos())
            mouseX = mousePos[0]
            mouseY = mousePos[1]
            xGap = mouseX - objects.player.rect.centerx 
            yGap = mouseY - objects.player.rect.centery
            if yGap == 0:
                yGap = 0.01 
            distance = (xGap**2+yGap**2)**(1/2)
            if distance != 0:
                factor = distance/20
                moveX = xGap / factor
                moveY = yGap / factor
                rotation =  math.degrees(math.atan(xGap / yGap)) + 90
                if yGap > 0:
                    rotation += 180
                objects.currentChunk.contents.append(LaserArrow((moveX*2, moveY*2), rotation))
            self.cooldown = self.fireRate
    
    def render(self):
        return

class LaserArrow(AbilityObject):
    def __init__(self,direction,rotationAngle):
        image = pygame.image.load(create_path("Laser Arrow.png"))
        image = pygame.transform.scale(image, (40,10))
        image = pygame.transform.rotate(image, rotationAngle)
        
        super().__init__(image, objects.player.rect.center)
        
        self.direction = direction
        self.attackDamage = 25
        self.type = "laserarrow"
    def update(self):
        self.rect = self.rect.move(self.direction)
        if not objects.display.get_rect().contains(self.rect):
            objects.currentChunk.contents.remove(self)
        for enemy in objects.currentChunk.contents:
            if enemy.type == "enemy" and self.rect.colliderect(enemy.rect):
                enemy.health -= self.attackDamage

class LaunchWave(Ability): # Ability 9: Fires a wave projectile with knockback
    def __init__(self):
        super().__init__()
    def update(self):
        if super().update(): 
            mousePos = objects.mapMousePos(pygame.mouse.get_pos())
            mouseX = mousePos[0]
            mouseY = mousePos[1]
            xGap = mouseX - objects.player.rect.centerx 
            yGap = mouseY - objects.player.rect.centery
            if yGap == 0:
                yGap = 0.01 
            distance = (xGap**2+yGap**2)**(1/2)
            if distance != 0:
                factor = distance/20
                moveX = xGap / factor
                moveY = yGap / factor
                rotation =  math.degrees(math.atan(xGap / yGap)) + 90
                if yGap > 0:
                    rotation += 180
                objects.currentChunk.contents.append(Wave((moveX, moveY), rotation))
                objects.currentChunk.contents.append(Wave((moveX*-1, moveY*-1), rotation+180))
                objects.currentChunk.contents.append(Wave((moveY, moveX*-1), rotation+90))
                objects.currentChunk.contents.append(Wave((moveY*-1, moveX), rotation+270))

class Wave(AbilityObject):
    def __init__(self,direction,rotationAngle):
        image = pygame.image.load(create_path("Wave.png"))
        if rotationAngle > 360: 
            rotationAngle -= 360
        image = pygame.transform.scale(image, (100,200))
        image = pygame.transform.rotate(image, rotationAngle)

        super().__init__(image, objects.player.rect.center)
        self.direction = direction
        self.attackDamage = 1
        self.type = "wave"
    def update(self):
        self.rect = self.rect.move(self.direction)
        if not self.rect.colliderect(pygame.Rect(0,0,500,500)):
            objects.currentChunk.contents.remove(self) 
        for enemy in objects.currentChunk.contents: 
            if enemy.type == "enemy" and self.rect.colliderect(enemy.rect):
                if enemy.maxHealth < 200: 
                    enemy.rect = enemy.rect.move(self.direction)
                enemy.health -= self.attackDamage

class PotionAbility: 
    types = ["purple","red","blue","gold"]
    images = [pygame.transform.scale(pygame.image.load(create_path("Purple Potion.png")),(50,50)),pygame.transform.scale(pygame.image.load(create_path("Red Potion.png")),(50,50)),pygame.transform.scale(pygame.image.load(create_path("Blue Potion.png")),(50,50)),pygame.transform.scale(pygame.image.load(create_path("Gold Potion.png")),(50,50))]
    number = 0
    def __init__(self): 
        self.image = pygame.image.load(create_path("Poison Effect.png"))
        self.mousePressed = False
        self.cooldown = 0
        self.duration = objects.framerate
    def update(self): 
        if pygame.mouse.get_pressed(3)[2] and self.mousePressed == False: 
            self.mousePressed = True
            PotionAbility.number += 1
            if PotionAbility.number == 4: 
                PotionAbility.number = 0
            objects.abilityPanel[9] = PotionAbility.images[PotionAbility.number]
        if not pygame.mouse.get_pressed(3)[2]: 
            self.mousePressed = False
        
        if self.cooldown == 0 and pygame.mouse.get_pressed(3)[0] and objects.potions[PotionAbility.types[PotionAbility.number]] >= 1:
            self.cooldown = self.duration
            objects.potions[PotionAbility.types[PotionAbility.number]] -= 1
            for i in objects.potionEffects[PotionAbility.types[PotionAbility.number]]: 
                exec(i)

        if self.cooldown > 0:
            self.cooldown -= 1
            
    def render(self):
        potionText = objects.myFont.render("Amount of Equipped Potion ["+PotionAbility.types[PotionAbility.number]+"]: "+str(objects.potions[PotionAbility.types[PotionAbility.number]]),False,(0,0,0))
        objects.display.blit(potionText, (0,100))
        potionText = objects.myFont.render("Left button to use, Right to switch",False,(0,0,0))
        objects.display.blit(potionText, (0,125))