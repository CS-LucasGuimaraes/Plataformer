from scripts.utils import load_image
from scripts.menu.utils import Panel
# import pygame

class character_selection:
    def __init__(self):
        self.panel = Panel((40,480))

    def render(self, surf, m_pos, clicking):
        surf.fill((165,229,255))

        if self.panel.update(surf, m_pos, clicking):
            # self.Game.run()
            print(1)
        # surf.blit(pygame.transform.scale(self.panel, (430, 430)), (40,480))
        # surf.blit(pygame.transform.scale(self.panel, (430, 430)), (430+40*2,480))
        # surf.blit(pygame.transform.scale(self.panel, (430, 430)), (430*2+40*3,480))
        # surf.blit(pygame.transform.scale(self.panel, (430, 430)), (430*3+40*4,480))