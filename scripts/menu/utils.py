from scripts.utils import load_image

import pygame

class Clickable:
    def __init__(self, pos, size, type, text1, text2, main_menu):
        self.main_menu = main_menu
        self.pos = pos
        self.size = size
        self.type = type
        self.text1 = text1
        self.text2 = text2

        self.font = pygame.font.Font('data/fonts/Kenney Future.ttf', 36)

        self.released = load_image('clickable/'+self.type+'0.png')
        self.hovering = load_image('clickable/'+self.type+'1.png')
        
        self.img = self.released

    def render(self, surf):
        text1 = self.font.render(self.text1, True, (255,255,255))
        text2 = self.font.render(self.text2, True, (255,255,255))
        
        if self.text2 == '':
            text_rect1 = text1.get_rect(center=(self.pos[0] + (self.size[0]/2), self.pos[1] + (self.size[1]/2)))

        else:
            ...

        surf.blit(pygame.transform.scale(self.img, self.size), self.pos)
        
        if self.text2 == '':
            surf.blit(text1, text_rect1)
        else:
            ...
    
    def update(self, surf, mpos, click):

        if self.pos[0]+self.size[0] >= mpos[0] and mpos[0] >= self.pos[0] and self.pos[1]+self.size[1] >= mpos[1] and mpos[1] >= self.pos[1]:
            if click:
                return True
            else:
                self.img = self.hovering
            
        else: 
            self.img = self.released

        self.render(surf)
        return False
    
class Button(Clickable):
    def __init__(self, main_menu, pos, text1='', text2=''):
        super().__init__(pos, (380,98), 'button', text1, text2, main_menu)

class Panel(Clickable):
    def __init__(self, main_menu, pos, text1='', text2=''):
        super().__init__(pos, (380,510), 'panel', text1, text2, main_menu)