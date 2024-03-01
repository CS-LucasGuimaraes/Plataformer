import pygame

from scripts.tilemap import *
from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player
from scripts.ui import UI

class Game:
    def __init__(self):
        pygame.init()

        self.screen_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]

        # self.screen_size[0]/=1.5;self.screen_size[1]/=1.5
        self.surface_size = (480,270)       


        self.screen = pygame.display.set_mode((self.screen_size))
        self.display = pygame.Surface(self.surface_size)
        self.clock = pygame.time.Clock()

        pygame.display.set_caption('pygame ip')

        from scripts.assets import assets
        merge_dict = assets

        self.assets = {
            'player/idle': Animation(load_images('entities/blue/idle'), img_dur=16),
            'player/run': Animation(load_images('entities/blue/run'), img_dur=6),
            'player/jump': Animation(load_images('entities/blue/jump'), img_dur=5),
            'player/wall_jump': Animation(load_images('entities/blue/wall_jump'), img_dur=5),
        }

        for k in merge_dict:
            self.assets[k] = merge_dict[k]
        

        self.tilemap = Tilemap(self)

        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass
        
        self.player = Player(self, [96,40], [16,16])

        self.movement = [False, False]

        self.scroll = [0,0]
        

        self.keybinds = {
            'right': [pygame.K_d, pygame.K_RIGHT],
            'left': [pygame.K_a, pygame.K_LEFT],
            'jump': [pygame.K_w, pygame.K_UP, pygame.K_SPACE],
        }

        self.ui = UI(self)

    def run(self):
        while True:
            self.display.fill((120,120,120))
    
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) //30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) //30

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll, mode='game')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in self.keybinds['left']:
                        self.movement[0] = True
                    elif event.key in self.keybinds['right']:
                        self.movement[1] = True
                    elif event.key in self.keybinds['jump']:
                        self.player.jump()
                elif event.type == pygame.KEYUP:
                    if event.key in self.keybinds['left']:
                        self.movement[0] = False
                    elif event.key in self.keybinds['right']:
                        self.movement[1] = False

            
            self.player.update(self.tilemap, (self.movement[1]-self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)
            
            self.ui.update()
            self.screen.blit(pygame.transform.scale(self.display, self.screen_size), (0,0))

            self.ui.render(self.screen)
            pygame.display.update()
            
            self.clock.tick(60)


Game().run()  # Start the program execution
