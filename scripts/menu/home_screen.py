from scripts.menu.utils import Button
from scripts.utils import load_image
from game import Game

import pygame

class home_screen:
    def __init__(self, main_menu, joysticks):
        self.main_menu = main_menu

        self.joysticks = joysticks

        self.start_button = Button((960-190, 100+400), 'NEW GAME')
        self.load_button = Button((960-190, 245+400), 'LOAD GAME')
        self.exit_button = Button((960-190, 390+400), 'EXIT')

        self.joy_button = 0
        self.joy_group = 0

        self.joy_map = [
                        ['start'],
                        ['load'],
                        ['exit'],
                       ]


        self.axis = [[0,0] for _ in self.joysticks]


    def controller_movements(self):
        for index in range(len(self.joysticks)):
            joystick = self.joysticks[index]

            if round(joystick.get_axis(0),0) == -1:
                if self.axis[index][0] > 0:
                    self.axis[index][0] = 0
                self.axis[index][0] -= 1

            elif round(joystick.get_axis(0),0) == +1:
                if self.axis[index][0] < 0:
                    self.axis[index][0] = 0
                self.axis[index][0] += 1
            
            else: self.axis[index][0] = 0



            if abs(self.axis[index][0]) == 15:
                self.axis[index][0] = 0



            if round(joystick.get_axis(1),0) == -1:
                if self.axis[index][1] > 0:
                    self.axis[index][1] = 0
                self.axis[index][1] -= 1

            elif round(joystick.get_axis(1),0) == +1:
                if self.axis[index][1] < 0:
                    self.axis[index][1] = 0
                self.axis[index][1] += 1
            
            else: self.axis[index][1] = 0



            if abs(self.axis[index][1]) == 15:
                self.axis[index][1] = 0
            
            if self.axis[index][1] == 1:
                self.joy_group = (self.joy_group+1) % len(self.joy_map) 
            elif self.axis[index][1] == -1:
                self.joy_group = (self.joy_group-1) % len(self.joy_map)

            if self.axis[index][0] == 1:
                self.joy_button = (self.joy_button+1) % len(self.joy_map[self.joy_group]) 
            elif self.axis[index][0] == -1:
                self.joy_button = (self.joy_button-1) % len(self.joy_map[self.joy_group])
            
            
    def render(self, surf, m_pos, clicking):
        surf.fill((46,0,52))
        surf.blit(load_image('logo.png'), (1920/2-384/2,20))
    
        if len(self.joysticks) != 0: 
            self.controller_movements()
            
            if self.joy_group == 0:
                m_pos = (960-190, 100+400)
            
            elif self.joy_group == 1:
                m_pos = (960-190, 245+400)
            
            elif self.joy_group == 2:
                m_pos = (960-190, 390+400)

        if self.start_button.update(surf, m_pos, clicking):
            self.main_menu.menu_index = 2

        if self.load_button.update(surf, m_pos, clicking):
            self.main_menu.menu_index = 1

        if self.exit_button.update(surf, m_pos, clicking):
            pygame.quit()
        