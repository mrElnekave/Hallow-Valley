import objects

class Obj:
    def __init__(self, image, location=(0,0)):
        self.type = "unassigned"
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = location
    
    def render(self): 
        objects.display.blit(self.image, self.rect)