from scripts.utils import load_image

import pygame

class Clickable:
    def __init__(self, pos, size, type):
        self.pos = pos
        self.size = size
        self.type = type
    
        self.unpressed = load_image('clickable/'+self.type+'0.png')
        self.pressed = load_image('clickable/'+self.type+'1.png')
        
        self.img = self.unpressed

    def render(self, surf):
        surf.blit(pygame.transform.scale(self.img, self.size), self.pos)
    
    def update(self, surf, mpos, click):

        if self.pos[0]+self.size[0] >= mpos[0] and mpos[0] >= self.pos[0] and self.pos[1]+self.size[1] >= mpos[1] and mpos[1] >= self.pos[1]:
                if click:
                    return True
                else:
                    self.img = self.pressed
        else: 
            self.img = self.unpressed

        self.render(surf)
        return False
    
class Button(Clickable):
    def __init__(self, pos):
        super().__init__(pos, size=(380,98), type='button')

class Panel(Clickable):
    def __init__(self, pos):
        super().__init__(pos, size=(430, 430), type='button')



