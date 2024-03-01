import pygame

from scripts.utils import load_image, load_images

class UI:
    def __init__(self,Game):

        self.game = Game
        
        self.player = Game.player
        self.pos = (0,0)
        
        self.font = pygame.font.Font('data/fonts/Kenney Future.ttf',int(12*self.game.screen_size[0]//self.game.surface_size[0]))
        
        self.heart_img = (
            pygame.transform.scale_by(load_image('hearts/00.png'), (self.game.screen_size[0]//self.game.surface_size[0])),
            pygame.transform.scale_by(load_image('hearts/02.png'), (self.game.screen_size[0]//self.game.surface_size[0]))
        )
        self.key_img = pygame.transform.scale_by(load_image('tiles/key/00.png'), (self.game.screen_size[0]//self.game.surface_size[0]))
        self.coin_img = pygame.transform.scale_by(load_image('tiles/coin/00.png'), (self.game.screen_size[0]//self.game.surface_size[0]))
        self.diamond_img = pygame.transform.scale_by(load_image('tiles/diamond/00.png'), (self.game.screen_size[0]//self.game.surface_size[0]))
        
        self.offset = (18*self.game.screen_size[0]//self.game.surface_size[0])*0.2
        self.size = 18*self.game.screen_size[0]//self.game.surface_size[0]

        self.coins = self.font.render('0', True, (255,255,255))
        self.diamonds = self.font.render('0', True, (255,255,255))
        self.keys = self.font.render('0', True, (255,255,255))

    def update(self):
        self.coins = self.font.render(str(self.player.collectibles['coin']), False, (255,255,255))
        self.diamonds = self.font.render(str(self.player.collectibles['diamond']), False, (255,255,255))
        self.keys = self.font.render(str(self.player.collectibles['key']), False, (255,255,255))



    def render(self, surf):
        
        k1 = 1 if self.player.hearts >= 1 else 0
        k2 = 1 if self.player.hearts >= 2 else 0
        k3 = 1 if self.player.hearts >= 3 else 0

        surf.blit(self.heart_img[k1], (self.offset*1+self.size*0.0, self.offset))
        surf.blit(self.heart_img[k2], (self.offset*2+self.size*0.7, self.offset))
        surf.blit(self.heart_img[k3], (self.offset*3+self.size*1.4, self.offset))

        surf.blit(self.coin_img, (self.game.screen_size[0]-self.offset*1-self.size*6, self.offset))
        surf.blit(self.coins, (self.game.screen_size[0]-self.offset*1-self.size*5, self.offset*1.5))
        
        surf.blit(self.key_img, (self.game.screen_size[0]-self.offset*1-self.size*4, self.offset))
        surf.blit(self.keys, (self.game.screen_size[0]-self.offset*0.3-self.size*3, self.offset*1.5))
        
        
        surf.blit(self.diamond_img, (self.game.screen_size[0]-self.offset*1-self.size*2, self.offset))
        surf.blit(self.diamonds, (self.game.screen_size[0]-self.offset*1-self.size*1, self.offset*1.5))

