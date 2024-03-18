from scripts.menu.home_screen import home_screen
from scripts.menu.character_selection import character_selection
from scripts.menu.save_override import save_override
from scripts.utils import load_image

import pygame

from game import Game

class Menu:
    def init_window(self):
        self.screen_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]

        # self.screen_size[0]/=1.5;self.screen_size[1]/=1.5
        self.surface_size = (480,270)       

        self.screen = pygame.display.set_mode((self.screen_size))
        self.display = pygame.Surface(self.surface_size)
        self.interface = pygame.Surface((1920,1080))

        self.home_screen = home_screen(self)
        self.character_selection = character_selection(self)
        self.save_override = save_override(self)

        pygame.display.set_caption('Menu')


    def __init__(self):
        pygame.init()

        self.init_window()        

        self.menu_index = 0

        self.clicking = False
        self.right_clicking = False


        self.clock = pygame.time.Clock()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                ...

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:       # LEFT CLICK
                    self.clicking = True
                elif event.button == 3:     # RIGHT CLICK
                    self.right_clicking = True


            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:       # LEFT CLICK
                    self.clicking = False
                elif event.button == 3:     # RIGHT CLICK
                    self.right_clicking = False

            elif event.type == pygame.QUIT:
                pygame.quit()


    def get_mpos(self):
            RENDER_SCALE = self.screen_size[0]/1920
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)

            return [int(mpos[0]), int(mpos[1])]


    def run(self):
        while True:
            self.process_events()

            m_pos = self.get_mpos()
            
            if self.menu_index == 0:
                self.home_screen.render(self.interface, m_pos, self.clicking)
            elif self.menu_index == 1:
                self.character_selection.render(self.interface, m_pos, self.clicking)           
            elif self.menu_index == 2:
                self.save_override.render(self.interface, m_pos, self.clicking)           
            
            
            self.clicking = False
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen_size), (0,0))
            self.screen.blit(pygame.transform.scale(self.interface, self.screen_size), (0,0))

            pygame.display.update()
            self.clock.tick(60)

Menu().run()    # Start the program execution