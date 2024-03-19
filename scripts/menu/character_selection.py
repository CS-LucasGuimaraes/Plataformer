from scripts.utils import load_image
from scripts.menu.utils import Button, Panel
from game import Game
import json

import pygame

class character_selection:
    def __init__(self, main_menu, joysticks):
        self.main_menu = main_menu
        self.joysticks = joysticks
        self.font = pygame.font.Font('data/fonts/Kenney Future.ttf', 36)
        self.font2 = pygame.font.Font('data/fonts/Kenney Future.ttf', 18)

        self.LEVELS_COUNT = 3

        self.back_button = Button((100, 100), 'Back to menu')    

        self.p1 = Panel((40,480))
        self.p2 = Panel((430+40*2,480))
        self.p3 = Panel((430*2+40*3,480))
        self.p4 = Panel((430*3+40*4,480))

        self.colors = [(255,255,255),(255,255,255),(255,255,255),(255,255,255)]

        self.joy_button = 0
        self.joy_group = 1

        self.joy_map = [
                        ['BACK'],
                        ['p1','p2','p3','p4'],
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

    def render_panels(self, surf, m_pos, clicking):
        if self.p1.update(surf, m_pos, clicking):
            Game(1, self.main_menu.screen_size, self.main_menu.surface_size, self.main_menu.screen, self.main_menu.display, 1, self.main_menu).run()

        if self.p2.update(surf, m_pos, clicking):
            Game(2, self.main_menu.screen_size, self.main_menu.surface_size, self.main_menu.screen, self.main_menu.display, 2, self.main_menu).run()
        
        if self.p3.update(surf, m_pos, clicking):
            Game(3, self.main_menu.screen_size, self.main_menu.surface_size, self.main_menu.screen, self.main_menu.display, 3, self.main_menu).run()
        
        if self.p4.update(surf, m_pos, clicking):
            Game(4, self.main_menu.screen_size, self.main_menu.surface_size, self.main_menu.screen, self.main_menu.display, 4, self.main_menu).run()


    def render_portraits(self, surf):
        surf.blit(load_image('portraits/blue.png'),(20+(430/2)-42,480-42))
        surf.blit(load_image('portraits/green.png'),(20+(430/2)-42+470*1,480-42))
        surf.blit(load_image('portraits/pink.png'),(20+(430/2)-42+470*2,480-42))
        surf.blit(load_image('portraits/yellow.png'),(20+(430/2)-42+470*3,480-42))


    def load_json(self):
        s1 = open('saves/1.json', 'r')
        self.data_l1 = json.load(s1)
        s1.close()

        s2 = open('saves/2.json', 'r')
        self.data_l2 = json.load(s2)
        s2.close()

        s3 = open('saves/3.json', 'r')
        self.data_l3 = json.load(s3)
        s3.close()

        s4 = open('saves/4.json', 'r')
        self.data_l4 = json.load(s4)
        s4.close()


    def render_parameters(self, surf, offset, text, attribute, subattribute=''):
        if subattribute == '':
            text1 = self.font2.render(text+str(self.data_l1[attribute]), True, self.colors[0])
            text_rect1 = text1.get_rect(center=(430*0+40*1 +380/2 ,480+60+offset))
            surf.blit(text1, text_rect1)
        
            text2 = self.font2.render(text+str(self.data_l2[attribute]), True, self.colors[1])
            text_rect2 = text2.get_rect(center=(430*1+40*2 +380/2 ,480+60+offset))
            surf.blit(text2, text_rect2)
            
            text3 = self.font2.render(text+str(self.data_l3[attribute]), True, self.colors[2])
            text_rect3 = text3.get_rect(center=(430*2+40*3 +380/2 ,480+60+offset))
            surf.blit(text3, text_rect3)
            
            text4 = self.font2.render(text+str(self.data_l4[attribute]), True, self.colors[3])
            text_rect4 = text4.get_rect(center=(430*3+40*4 +380/2 ,480+60+offset))
            surf.blit(text4, text_rect4)
        else:
            text1 = self.font2.render(text+str(self.data_l1[attribute][subattribute]), True, self.colors[0])
            text_rect1 = text1.get_rect(center=(430*0+40*1 +380/2 ,480+60+offset))
            surf.blit(text1, text_rect1)
        
            text2 = self.font2.render(text+str(self.data_l2[attribute][subattribute]), True, self.colors[1])
            text_rect2 = text2.get_rect(center=(430*1+40*2 +380/2 ,480+60+offset))
            surf.blit(text2, text_rect2)
            
            text3 = self.font2.render(text+str(self.data_l3[attribute][subattribute]), True, self.colors[2])
            text_rect3 = text3.get_rect(center=(430*2+40*3 +380/2 ,480+60+offset))
            surf.blit(text3, text_rect3)
            
            text4 = self.font2.render(text+str(self.data_l4[attribute][subattribute]), True, self.colors[3])
            text_rect4 = text4.get_rect(center=(430*3+40*4 +380/2 ,480+60+offset))
            surf.blit(text4, text_rect4)


    def render(self, surf, m_pos, clicking, override=False):
        surf.fill((46,0,52))
        surf.blit(load_image('logo.png'), (1920/2-384/2,20))

        if len(self.joysticks) != 0: 
            self.controller_movements()
            
            if self.joy_group == 0:
                m_pos = (100, 100)
            
            elif self.joy_group == 1:
                if self.joy_button == 0:
                    m_pos = (40,480)
                if self.joy_button == 1:
                    m_pos = (430+40*2,480)

                if self.joy_button == 2:
                    m_pos = (430*2+40*3,480)

                if self.joy_button == 3:
                    m_pos = (430*3+40*4,480)                


        if self.back_button.update(surf, m_pos, clicking):
            self.main_menu.menu_index = 0

        self.render_panels(surf, m_pos, clicking)
        self.render_portraits(surf)

        self.colors = [(255,255,255),(255,255,255),(255,255,255),(255,255,255)]

        if self.p1.hovering: 
            self.colors[0] = (0,0,0)
        elif self.p2.hovering: 
            self.colors[1] = (0,0,0)
        elif self.p3.hovering: 
            self.colors[2] = (0,0,0)
        elif self.p4.hovering: 
            self.colors[3] = (0,0,0)
    
        text1 = self.font.render('PLAYER 1', True, self.colors[0])
        text_rect1 = text1.get_rect(center=(430*0+40*1 +380/2 ,480+60))
        surf.blit(text1, text_rect1)
    
        text2 = self.font.render('PLAYER 2', True, self.colors[1])
        text_rect2 = text2.get_rect(center=(430*1+40*2 +380/2 ,480+60))
        surf.blit(text2, text_rect2)
        
        text3 = self.font.render('PLAYER 3', True, self.colors[2])
        text_rect3 = text3.get_rect(center=(430*2+40*3 +380/2 ,480+60))
        surf.blit(text3, text_rect3)
        
        text4 = self.font.render('PLAYER 4', True, self.colors[3])
        text_rect4 = text4.get_rect(center=(430*3+40*4 +380/2 ,480+60))
        surf.blit(text4, text_rect4)


        self.load_json()


        text1 = self.font.render(str(self.data_l1['current_level']*100//self.LEVELS_COUNT)+'%', True, self.colors[0])
        text_rect1 = text1.get_rect(center=(430*0+40*1 +380/2 ,480+60+40))
        surf.blit(text1, text_rect1)
    
        text2 = self.font.render(str(self.data_l2['current_level']*100//self.LEVELS_COUNT)+'%', True, self.colors[1])
        text_rect2 = text2.get_rect(center=(430*1+40*2 +380/2 ,480+60+40))
        surf.blit(text2, text_rect2)
        
        text3 = self.font.render(str(self.data_l3['current_level']*100//self.LEVELS_COUNT)+'%', True, self.colors[2])
        text_rect3 = text3.get_rect(center=(430*2+40*3 +380/2 ,480+60+40))
        surf.blit(text3, text_rect3)
        
        text4 = self.font.render(str(self.data_l4['current_level']*100//self.LEVELS_COUNT)+'%', True, self.colors[3])
        text_rect4 = text4.get_rect(center=(430*3+40*4 +380/2 ,480+60+40))
        surf.blit(text4, text_rect4)


        self.render_parameters(surf, 60+60, 'Current level: ', 'current_level')
        self.render_parameters(surf, 60+100, 'Current Hearts: ', 'current_hearts')
        self.render_parameters(surf, 60+140, 'Current Coins: ', 'current_collectibles','coin')
        self.render_parameters(surf, 60+180, 'Current Diamonds: ', 'current_collectibles','diamond')
        self.render_parameters(surf, 60+220, 'Current Keys: ', 'current_collectibles','key')

        if override:
            text = self.font.render('Choose a save to override:', True, (255,255,255))
            text_rect = text.get_rect(center=(1920/2,420))
            surf.blit(text, text_rect)