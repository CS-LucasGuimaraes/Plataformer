from scripts.menu.utils import Button

import pygame

class home_screen:
    def __init__(self, game):
        self.Game = game


        self.start_button = Button((960-190, 100+400))
        self.load_button = Button((960-190, 245+400))
        self.exit_button = Button((960-190, 392+400))


    def render(self, surf, m_pos, clicking):
        surf.fill((165,229,255))
    
        if self.start_button.update(surf, m_pos, clicking):
            self.Game.run()

        if self.load_button.update(surf, m_pos, clicking):
            self.Game.run()

        if self.exit_button.update(surf, m_pos, clicking):
            pygame.quit()
        