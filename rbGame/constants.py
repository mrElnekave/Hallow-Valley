import rubato as rb
from rubato import Vector


WIDTH = 500
HEIGHT = 500
WINDOWSIZE = Vector(900, 600)

player_sprite_size = 25

moveSpeed = 150  # pixels per second
mapWidth, mapHeight = 15, 15  # in chunks
dayLength = 5  # seconds
start_chunk = Vector(0, 0)


myFont = rb.Font(size=20)
announcementFont = rb.Font(size=72)
mathFont = rb.Font(size=50)


current_path = "Data\\"

# math
difficulty = 0
