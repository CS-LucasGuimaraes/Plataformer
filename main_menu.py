from scripts.menu.home_screen import home_screen
from scripts.menu.character_selection import character_selection
from scripts.menu.save_override import save_override
from scripts.utils import load_image

import pygame

class Menu:
    def init_window(self):
        self.screen_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]

        # self.screen_size[0]/=1.5;self.screen_size[1]/=1.5
        self.surface_size = (480,270)       

        self.screen = pygame.display.set_mode((self.screen_size), flags=pygame.NOFRAME)
        self.display = pygame.Surface(self.surface_size, flags=pygame.SRCALPHA)
        self.interface = pygame.Surface((1920,1080))

        self.home_screen = home_screen(self, self.joysticks)
        self.character_selection = character_selection(self, self.joysticks)
        self.save_override = save_override(self, self.joysticks)

        self.run_bool = True


        pygame.display.set_caption('Menu')


    def __init__(self):
        pygame.init()
        
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        self.init_window()        


        self.menu_index = 0

        self.clicking = False
        self.right_clicking = False

        from scripts.assets import sounds
        self.sounds = sounds
        self.sounds['ambience'].set_volume(0.3)
        self.sounds['ambience'].play(-1)
        self.sounds['music'].play(-1)

        self.clock = pygame.time.Clock()

        self.controller_binds = {
            'A': 0,
            'B': 1,
            'X': 2,
            'Y': 3,
            'l_bumper': 4,
            'r_bumper': 5,
            'start': [6,7,9],
        }


    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                ...

            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == self.controller_binds['A']:
                    for index in range(len(self.joysticks)):
                        joystick = self.joysticks[index]
                        if joystick.get_button(self.controller_binds['A']):
                            self.clicking = True
                elif event.button == self.controller_binds['B']:
                    for index in range(len(self.joysticks)):
                        joystick = self.joysticks[index]
                        if joystick.get_button(self.controller_binds['B']):
                            self.menu_index = 0
                            self.character_selection.joy_button = 0
                            self.character_selection.joy_group = 1

                            self.home_screen.joy_button = 0
                            self.home_screen.joy_group = 0

                            self.save_override.joy_button = 0
                            self.save_override.joy_group = 1

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
        while self.run_bool:
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

        self.sounds['ambience'].stop()
        self.sounds['music'].stop()
        self.sounds['walk'].stop()

while True:
    Menu().run()    # Start the program execution