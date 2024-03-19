from scripts.utils import load_image

import pygame

class Clickable:
    def __init__(self, pos, size, type, text):
        self.pos = pos
        self.size = size
        self.type = type
        self.text = text

        self.font = pygame.font.Font('data/fonts/Kenney Future.ttf', 36)

        self.hovering = False

        self.released_img = load_image('clickable/'+self.type+'0.png')
        self.hovering_img = load_image('clickable/'+self.type+'1.png')
        
        self.img = self.released_img

    def render(self, surf, text):

        text_rect = text.get_rect(center=(self.pos[0] + (self.size[0]/2), self.pos[1] + (self.size[1]/2)))

        surf.blit(pygame.transform.scale(self.img, self.size), self.pos)
        
        surf.blit(text, text_rect)

    
    def update(self, surf, mpos, click):
        text = self.font.render(self.text, True, (255,255,255))
        if self.pos[0]+self.size[0] >= mpos[0] and mpos[0] >= self.pos[0] and self.pos[1]+self.size[1] >= mpos[1] and mpos[1] >= self.pos[1]:
            if click:
                return True
            else:
                text = self.font.render(self.text, True, (0,0,0))
                self.hovering = True
                self.img = self.hovering_img
            
        else:
            self.hovering = False
            self.img = self.released_img

        self.render(surf, text)
        return False
    
class Button(Clickable):
    def __init__(self, pos, text=''):
        super().__init__(pos, (380,98), 'button', text)

class Panel(Clickable):
    def __init__(self, pos, text=''):
        super().__init__(pos, (380,510), 'panel', text)