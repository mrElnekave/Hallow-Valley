import MapClasses
import objects

# 2 Steps
# 1) Append the quests
# 2) Add the active code to update data to the quest item

# Need to display our quests (Max)

# Create all of our quests (Yuan)

objects.quests.append(
    MapClasses.Quest("Find the Fire Key!","self.data == True","The Fire Key")
)
objects.quests.append(
    MapClasses.Quest("Defeat the Fire Boss!","self.data == True","The Fire Boss")
)

objects.quests.append(
    MapClasses.Quest("Find the Ice Key!","self.data == True","The Ice Key")
)
objects.quests.append(
    MapClasses.Quest("Defeat the Ice Boss!","self.data == True","The Ice Boss")
)

objects.quests.append(
    MapClasses.Quest("Find the Lightning Key!","self.data == True","The Lightning Key")
)
objects.quests.append(
    MapClasses.Quest("Defeat the Lightning Boss!","self.data == True","The Lightning Boss")
)

objects.quests.append(
    MapClasses.Quest("Find the Poison Key!","self.data == True","The Poison Key")
)
objects.quests.append(
    MapClasses.Quest("Defeat the Poison Boss!","self.data == True","The Poison Boss")
)

objects.quests.append(
    MapClasses.Quest("Find the Summoning Key!","self.data == True","The Summoning Key")
)
objects.quests.append(
    MapClasses.Quest("Defeat the Summoning Boss!","self.data == True","The Summoning Boss")
)

objects.quests.append(
    MapClasses.Quest("Find the Shield Key!","self.data == True","The Shield Key")
)
objects.quests.append(
    MapClasses.Quest("Defeat the Shield Boss!","self.data == True","The Shield Boss")
)

objects.quests.append(
    MapClasses.Quest("Find the Laser Key!","self.data == True","The Laser Key")
)
objects.quests.append(
    MapClasses.Quest("Defeat the Laser Boss!","self.data == True","The Laser Boss")
)

objects.quests.append(
    MapClasses.Quest("Find the Water Key!","self.data == True","The Water Key")
)
objects.quests.append(
    MapClasses.Quest("Defeat the Water Boss!","self.data == True","The Water Boss")
)

objects.quests.append(
    MapClasses.Quest("Defeat the Final Boss!","self.data == True","The Final Boss")
)

objects.quests.append(
    MapClasses.Quest("Buy 3 Gold Potions!","self.data == 3","Potion Critic")
) # Whenever we buy a potion: self.data += 1