import objects, images, constants
import rubato as rb
from rubato import Component, Vector
import random, math


class Enemy(Component):
    def __init__(self):
        super().__init__()
        self.rect = None
        self.health = None
        self.image = None
        self.attackDamage = None
        self.speed = None
        self.type = None

    def update(self):
        pass

class Boss(Enemy):
    def __init__(self):
        super().__init__()
        self.maxHealth = None
        self.bg_health_bar = rb.Rectangle(200,20, color=rb.Color(15, 15, 15))
        self.health_bar = rb.Rectangle(200,20, color=rb.Color(255, 0, 0))

    def setup(self):
        self.gameobj.add(self.bg_health_bar, self.health_bar)
        self.bg_health_bar.top_left = Vector(300, 20)
        self.health_bar.top_left = Vector(300, 20)

    def update(self):
        # self.image.set_alpha((self.health / self.maxHealth) * 255)
        self.health_bar.width = self.health/self.maxHealth*200
        self.health_bar.top_left = Vector(300, 20)

class FireGhostBoss(Boss):
    def __init__(self):
        super().__init__()
        self.image = images.fire_boss
        self.rect = self.image.get_rect()

        self.attackDamage = 25
        self.speed = 5
        self.type = "enemy"
        self.angle = 0
        self.counter = 0
        self.maxHealth = 200
        self.health = self.maxHealth
    def on_collide(self, manifold: rb.Manifold):
        if manifold.shape_b.gameobj.name == "player":
            if not objects.player.invulnerability:
                objects.player.currentHealth = objects.player.currentHealth - self.attackDamage
            # while self.rect.con: #TODO: bring back next class
            #     self.rect.center = (random.randint(0, objects.WINDOWWIDTH), random.randint(0, objects.WINDOWHEIGHT))
    def setup(self):
        super().setup()
        self.gameobj.add(self.image, self.rect)
        self.rect.center = Vector(250, 250)
        self.rect.on_collide = self.on_collide

    def update(self):
        # Changing directions after bouncing
        if self.rect.left < 0:
            self.angle = random.random() * math.pi - math.pi / 2
        if self.rect.right > constants.WIDTH:
            self.angle = random.random() * math.pi + math.pi / 2
        if self.rect.top < 0:
            self.angle = random.random() * math.pi + math.pi
        if self.rect.bottom > constants.HEIGHT:
            self.angle = random.random() * math.pi
        # Moving

        self.rect.center = Vector(
        self.rect.center.x + self.speed * math.cos(self.angle), self.rect.center.y - self.speed * math.sin(self.angle))
        # Checking for collision with player

        # Shooting fireballs on a timer
        self.counter = self.counter + 1
        # if self.counter == 10:
        #     playerPos = objects.player.rect.center
        #     xGap = playerPos[0] - self.rect.center[0]
        #     yGap = playerPos[1] - self.rect.center[1]
        #     distance = (xGap ** 2 + yGap ** 2) ** (1 / 2)
        #     if yGap == 0:
        #         yGap = .01
        #     if distance != 0:
        #         factor = distance / 5
        #         moveX = xGap / factor
        #         moveY = yGap / factor
        #         rotation = math.degrees(math.atan(xGap / yGap)) + 90  # y/x
        #     if yGap > 0:
        #         rotation += 180
        #     objects.currentChunk.contents.append(EnemyFireball((moveX, moveY), rotation, self.rect.center))
        #     self.counter = 0
        # # Getting hit by arrows
        # for projectile in objects.currentChunk.contents:
        #     if projectile.type == "arrow" and self.rect.colliderect(projectile.rect):
        #         self.health -= projectile.attackDamage
        #         objects.currentChunk.contents.remove(projectile)
        #     if self.health <= 0:
        #         objects.currentChunk.contents.remove(self)
        #         objects.player.maxHealth = objects.player.maxHealth + 25
        #         objects.player.maxEnergy = objects.player.maxEnergy + 25
        #         objects.resourceAmounts["ghostEnergy"] = objects.player.maxEnergy
        #         objects.player.currentHealth = objects.player.maxHealth
        #         objects.abilities[1] = Abilities.LaunchFireball()
        #         objects.reports_on and objects.update_log.addMessage("REPORT: You have defeated the fire ghost.")
        #         objects.reports_on and objects.update_log.addMessage("NEW ABILITY: FIREBALL")
        #         objects.reports_on and objects.update_log.addMessage(
        #             "Ability Information: The fireball ability allows you to launch a fireball that deals high damage and explodes upon contact, launching 4 smaller fireballs in different directions. This ability uses up 10 ghost energy per use. Press 2 to switch to the fireball ability from another ability.")
        #         # objects.FindQuest("The Fire Boss").data = True
        #         data = map_description.portalLocations["fire"]
        #         objects.player.chunk = data[0]
        #         objects.player.rect.center = data[1]
        #
        #         map_description.show_chunk(*(map_description.portalLocations["ice"][0]))
        #
        #         for i in objects.chunks[data[0][0]][data[0][1]].contents:
        #             if type(i) == MapClasses.CollisionButton:
        #                 objects.chunks[data[0][0]][data[0][1]].contents.remove(i)
        #                 return


# class IceGhostBoss(Ghost):
#     def __init__(self):
#         self.image = pygame.image.load(create_path("Ice Boss.png"))
#         self.rect = self.image.get_rect()
#         self.rect.center = (250, 250)
#         self.type = "enemy"
#         self.speed = 5
#         self.maxHealth = 400
#         self.health = 400
#         self.attackDamage = 10
#         self.direction = 90
#         self.counter = 0
#         self.mul = 1
#
#     def render(self):
#         self.image.set_alpha((self.health / self.maxHealth) * 255)
#         objects.display.blit(self.image, self.rect)
#         pygame.draw.rect(objects.display, (15, 15, 15), pygame.Rect(150, 25, 200, 20))
#         pygame.draw.rect(objects.display, (255, 0, 0), pygame.Rect(150, 25, self.health / self.maxHealth * 200, 20))
#         if self.health <= 250:
#             x = Math.lerp(0, 255, (self.mul - 1) / 0.3)
#             print(int(x))
#             pygame.draw.circle(objects.display, (int(x), 0, 0), self.rect.topleft, 4)
#
#     def update(self):
#         # Changing directions after bouncing
#         if self.rect.left < 0 or self.rect.right > objects.WINDOWWIDTH or self.rect.top < 0 or self.rect.bottom > objects.WINDOWHEIGHT:
#             playerPos = objects.player.rect.center
#             xGap = playerPos[0] - self.rect.centerx
#             yGap = playerPos[1] - self.rect.centery
#             if yGap == 0:
#                 yGap = .01
#             self.direction = math.atan(yGap / xGap)
#             if xGap < 0:
#                 self.direction += math.pi
#         # Moving
#         self.rect.center = (self.rect.centerx + self.speed * math.cos(self.direction),
#                             self.rect.centery + self.speed * math.sin(self.direction))
#         # Checking for collision with player
#         if self.rect.colliderect(objects.player.rect):
#             if not objects.player.invulnerability:
#                 objects.player.currentHealth = objects.player.currentHealth - self.attackDamage
#             while self.rect.colliderect(objects.player.rect):
#                 self.rect.center = (random.randint(0, objects.WINDOWWIDTH), random.randint(0, objects.WINDOWHEIGHT))
#         # Shooting icicles on a timer
#         self.counter = self.counter + 1
#         if self.counter == 60:
#             playerPos = objects.player.rect.center
#             xGap = playerPos[0] - self.rect.center[0]
#             yGap = playerPos[1] - self.rect.center[1]
#             distance = (xGap ** 2 + yGap ** 2) ** (1 / 2)
#             if yGap == 0:
#                 yGap = .01
#             if distance != 0:
#                 factor = distance / 5
#                 moveX = xGap / factor * 2
#                 moveY = yGap / factor * 2
#                 rotation = math.degrees(math.atan(xGap / yGap)) + 90
#             if yGap > 0:
#                 rotation += 180
#             objects.currentChunk.contents.append(EnemyIcicle((moveX, moveY), rotation, self.rect.center))
#             self.counter = 0
#         # rage phase
#         if self.health <= 250:
#             self.mul = Math.lerp(1, 1.3, 1 - self.health / 250)
#             self.rect.center = (self.rect.centerx + self.speed * self.mul * math.cos(self.direction),
#                                 self.rect.centery + self.speed * self.mul * math.sin(self.direction))
#             self.counter = self.counter + 2
#             if self.counter == 60:
#                 playerPos = objects.player.rect.center
#                 xGap = playerPos[0] - self.rect.center[0]
#                 yGap = playerPos[1] - self.rect.center[1]
#                 distance = (xGap ** 2 + yGap ** 2) ** (1 / 2)
#                 if yGap == 0:
#                     yGap = .01
#                 if distance != 0:
#                     factor = distance / 5
#                     moveX = xGap / factor * 2
#                     moveY = yGap / factor * 2
#                     rotation = math.degrees(math.atan(xGap / yGap)) + 90
#                 if yGap > 0:
#                     rotation += 180
#                 objects.currentChunk.contents.append(EnemyIcicle((moveX, moveY), rotation, self.rect.center))
#                 self.counter = 0
#         # Getting hit by arrows
#         if self.health <= 0:
#             objects.currentChunk.contents.remove(self)
#             objects.player.maxHealth = objects.player.maxHealth + 25
#             objects.player.maxEnergy = objects.player.maxEnergy + 25
#             objects.resourceAmounts["ghostEnergy"] = objects.player.maxEnergy
#             objects.player.currentHealth = objects.player.maxHealth
#             objects.abilities[2] = Abilities.Freeze()
#             objects.reports_on and objects.update_log.addMessage("REPORT: You have defeated the ice ghost.")
#             objects.reports_on and objects.update_log.addMessage("NEW ABILITY: FREEZE")
#             objects.reports_on and objects.update_log.addMessage(
#                 "Ability Information: The freeze ability allows you to freeze all enemies on the screen for 3 seconds. This ability uses up 25 ghost energy per use. Press 3 to switch to the freeze ability from another ability.")
#             # objects.FindQuest("The Ice Boss").data = True
#             data = map_description.portalLocations["ice"]
#             objects.player.chunk = data[0]
#             objects.player.rect.center = data[1]
#             map_description.show_chunk(*(map_description.portalLocations["lightning"][0]))
#
#             for i in objects.chunks[data[0][0]][data[0][1]].contents:
#                 if type(i) == MapClasses.CollisionButton:
#                     objects.chunks[data[0][0]][data[0][1]].contents.remove(i)
#                     return
