import pygame

from scripts.tilemap import *
from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player, enemy
from scripts.ui import UI

class Game:
    def init_window(self):
        self.screen_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]

        self.screen_size[0]/=1.5;self.screen_size[1]/=1.5
        self.surface_size = (480,270)       

        self.screen = pygame.display.set_mode((self.screen_size))
        self.display = pygame.Surface(self.surface_size)
        
        pygame.display.set_caption('pygame ip')


    def init_joy(self):
        pygame.joystick.init()

        if pygame.joystick.get_count() == 0: 
            self.joystick = 0 
            self.joy = False
        else: 
            self.joystick = pygame.joystick.Joystick(0)
            self.joy = True


    def init_binds(self):
        self.keybinds = {
            'right': [pygame.K_d, pygame.K_RIGHT],
            'left': [pygame.K_a, pygame.K_LEFT],
            'jump': [pygame.K_w, pygame.K_UP, pygame.K_SPACE],
        }

        self.controller_binds = {
            'jump': [0]
        }


    def init_assets(self):
        from scripts.assets import assets
        merge_dict = assets

        self.assets = {
            'player/idle': Animation(load_images('entities/blue/idle'), img_dur=16),
            'player/run': Animation(load_images('entities/blue/run'), img_dur=6),
            'player/jump': Animation(load_images('entities/blue/jump'), img_dur=5),
            'player/wall_jump': Animation(load_images('entities/blue/wall_jump'), img_dur=5),
            'enemy/idle': Animation(load_images('entities/enemy/run'), img_dur=4),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
        }

        for k in merge_dict:
            self.assets[k] = merge_dict[k]
        

        self.tilemap = Tilemap(self)

        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass


    def init_player(self):
        self.player = Player(self, [96,40], [16,16])
        self.movement = [False, False]


    def __init__(self):
        pygame.init()

        self.init_window()
        self.init_joy()
        self.init_binds()
        self.init_assets()
        self.init_player()

        self.clock = pygame.time.Clock()
        self.scroll = [0,0]

        self.ui = UI(self)

        self.enemies = []


    def camera_control(self):
        self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) //30
        self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) //30

        return (int(self.scroll[0]), int(self.scroll[1]))

    def controller_movements(self):
        if self.joy:
                self.movement[0] = False
                self.movement[1] = False
                if round(self.joystick.get_axis(0),0) == -1:
                    self.movement[0] = True
                if round(self.joystick.get_axis(0),0) == +1:
                    self.movement[1] = True

    def process_events(self):
        if self.joy:
            self.controller_movements()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if not self.joy:
                    if event.key in self.keybinds['left']:
                        self.movement[0] = True
                    elif event.key in self.keybinds['right']:
                        self.movement[1] = True
                    elif event.key in self.keybinds['jump']:
                        self.player.jump()

            elif event.type == pygame.KEYUP:
                if not self.joy:
                    if event.key in self.keybinds['left']:
                        self.movement[0] = False
                    elif event.key in self.keybinds['right']:
                        self.movement[1] = False
            
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button in self.controller_binds['jump']:
                    self.player.jump()
            
            elif event.type == pygame.JOYDEVICEADDED:
                self.joystick = pygame.joystick.Joystick(0)
                self.joy = True
            
            elif event.type == pygame.JOYDEVICEREMOVED:
                self.joy = False

            elif event.type == pygame.QUIT:
                pygame.quit()

    def run(self):
        while True:    
            self.process_events()
            
            render_scroll = self.camera_control()
            
            self.tilemap.render(self.display, offset=render_scroll, mode='game')

            for enemy in self.enemies:
                enemy.update(self.tilemap, self.player.rect())
                enemy.render(self.display, offset=render_scroll)
            
            self.player.update(self.tilemap, (self.movement[1]-self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen_size), (0,0))

            self.ui.update()
            self.ui.render(self.screen)
            
            pygame.display.update()
            self.clock.tick(60)


Game().run()  # Start the program execution
