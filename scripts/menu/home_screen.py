from scripts.menu.utils import Button
from scripts.utils import load_image
from game import Game

import pygame

class home_screen:
    def __init__(self, main_menu):
        self.main_menu = main_menu

        self.start_button = Button(self.main_menu, (960-190, 100+400), 'NEW GAME')
        self.load_button = Button(self.main_menu, (960-190, 245+400), 'LOAD GAME')
        self.exit_button = Button(self.main_menu, (960-190, 392+400), 'EXIT')


    def render(self, surf, m_pos, clicking):
        surf.fill((46,0,52))
        surf.blit(load_image('logo.png'), (1920/2-384/2,20))
    
        if self.start_button.update(surf, m_pos, clicking):
            self.main_menu.menu_index = 2

        if self.load_button.update(surf, m_pos, clicking):
            self.main_menu.menu_index = 1

        if self.exit_button.update(surf, m_pos, clicking):
            pygame.quit()
        