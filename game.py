import pygame

from scripts.tilemap import *
from scripts.utils import load_image, load_images, Animation, restart_level
from scripts.entities import PhysicsEntity, Player, enemy
from scripts.ui import UI
from scripts.cooperative import cooperative
from scripts.menu.pause import Pause

class Game:
    def init_window(self, screen, display, screen_size, surface_size):
        self.screen_size = screen_size
        self.surface_size = surface_size
        
        self.screen = screen
        self.display = display

        pygame.display.set_caption('pygame ip')


    def init_joy(self):
        pygame.joystick.init()

        if pygame.joystick.get_count() == 0:
            self.joysticks = []
            self.joy = False
        else: 
            self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

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


    def init_assets(self, player_color):
        from scripts.assets import assets, sounds
        merge_dict = assets

        colors = ['blue', 'green', 'pink', 'yellow']

        self.assets = {
            'player0/idle': Animation(load_images('entities/' + colors[(0+player_color-1)%4] +'/idle'), img_dur=16),
            'player0/run': Animation(load_images('entities/' + colors[(0+player_color-1)%4] + '/run'), img_dur=6),
            'player0/jump': Animation(load_images('entities/' + colors[(0+player_color-1)%4] + '/jump'), img_dur=5),
            'player0/wall_jump': Animation(load_images('entities/' + colors[(0+player_color-1)%4] + '/wall_jump'), img_dur=5),

            'player1/idle': Animation(load_images('entities/' + colors[(1+player_color-1)%4] +'/idle'), img_dur=16),
            'player1/run': Animation(load_images('entities/' + colors[(1+player_color-1)%4] + '/run'), img_dur=6),
            'player1/jump': Animation(load_images('entities/' + colors[(1+player_color-1)%4] + '/jump'), img_dur=5),
            'player1/wall_jump': Animation(load_images('entities/' + colors[(1+player_color-1)%4] + '/wall_jump'), img_dur=5),

            'player2/idle': Animation(load_images('entities/' + colors[(2+player_color-1)%4] +'/idle'), img_dur=16),
            'player2/run': Animation(load_images('entities/' + colors[(2+player_color-1)%4] + '/run'), img_dur=6),
            'player2/jump': Animation(load_images('entities/' + colors[(2+player_color-1)%4] + '/jump'), img_dur=5),
            'player2/wall_jump': Animation(load_images('entities/' + colors[(2+player_color)%4] + '/wall_jump'), img_dur=5),

            'player3/idle': Animation(load_images('entities/' + colors[(3+player_color-1)%4] +'/idle'), img_dur=16),
            'player3/run': Animation(load_images('entities/' + colors[(3+player_color-1)%4] + '/run'), img_dur=6),
            'player3/jump': Animation(load_images('entities/' + colors[(3+player_color-1)%4] + '/jump'), img_dur=5),
            'player3/wall_jump': Animation(load_images('entities/' + colors[(3+player_color-1)%4] + '/wall_jump'), img_dur=5),
            
            
            'enemy/idle': Animation(load_images('entities/enemy/run'), img_dur=3),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=3),
        }

        for k in merge_dict:
            self.assets[k] = merge_dict[k]
        
        self.sounds = sounds

        self.tilemap = Tilemap(self)

        self.tilemap.load('levels/level'+str(self.current_level)+'.json')

    def init_player(self):
        self.cooperative_status = cooperative(3, 0, 0, 0) 
        self.players = [Player(self, self.tilemap.spawn_point.copy(), [16,16], x) for x in range(max(len(self.joysticks),1))]
        self.movement = [[False, False],[False, False],[False, False],[False, False]]
        self.cooperative_status.hearts = self.data['current_hearts']
        self.cooperative_status.collectibles['coin'] = self.data['current_collectibles']['coin']
        self.cooperative_status.collectibles['diamond'] = self.data['current_collectibles']['diamond']
        self.cooperative_status.collectibles['key'] = self.data['current_collectibles']['key']

    def init_save(self, save):
        self.save = save

        f = open('saves/'+str(save)+'.json', 'r')
        self.data = json.load(f)
        f.close()

        self.current_level = self.data['current_level']


    def __init__(self, player_color, screen_size, surface_size, screen, display, save):
        self.init_window(screen, display, screen_size, surface_size)
        self.init_save(save)
        self.init_joy()
        self.init_binds()
        self.init_assets(player_color)
        self.init_player()

        self.pause = Pause(self, self.joysticks)

        self.clock = pygame.time.Clock()
        self.scroll = [0,0]

        self.ui = UI(self)

        self.enemies = []

        self.sounds['ambience'].set_volume(0.3)
        self.sounds['ambience'].play(-1)
        self.sounds['music'].play(-1)
        self.pop_list = []

    def camera_control(self):
        player_averege_pos = [0,0]
        for player in self.players:
            player_averege_pos[0] += player.rect().centerx
            player_averege_pos[1] += player.rect().centery

        player_averege_pos[0] /= len(self.players)
        player_averege_pos[1] /= len(self.players)

        self.scroll[0] += (player_averege_pos[0] - self.display.get_width() / 2 - self.scroll[0]) //30
        self.scroll[1] += (player_averege_pos[1] - self.display.get_height() / 2 - self.scroll[1]) //30

        return (int(self.scroll[0]), int(self.scroll[1]))

    def controller_movements(self):
        if self.joy:
                
                self.movement = [[False, False],[False, False],[False, False],[False, False]]

                for index in range(len(self.joysticks)):
                    joystick = self.joysticks[index]

                    if round(joystick.get_axis(0),0) == -1:
                        self.movement[index][0] = True
                    if round(joystick.get_axis(0),0) == +1:
                        self.movement[index][1] = True

    def process_events(self):
        if self.joy:
            self.controller_movements()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # if not self.joy:
                    if event.key in self.keybinds['left']:
                        self.movement[0][0] = True
                    elif event.key in self.keybinds['right']:
                        self.movement[0][1] = True
                    elif event.key in self.keybinds['jump']:
                        self.players[0].jump()
                    elif event.key == pygame.K_ESCAPE:
                        self.pause.pause(self.display)
                        self.movement = [[False, False],[False, False],[False, False],[False, False]]
                        

            elif event.type == pygame.KEYUP:
                # if not self.joy:
                    if event.key in self.keybinds['left']:
                        self.movement[0][0] = False
                    elif event.key in self.keybinds['right']:
                        self.movement[0][1] = False
            
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button in self.controller_binds['jump']:
                    for index in range(len(self.joysticks)):
                        joystick = self.joysticks[index]
                        if joystick.get_button(0):
                            self.players[index].jump()
                    
            
            elif event.type == pygame.JOYDEVICEADDED:
                # self.joystick = pygame.joystick.Joystick(0)
                self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

                self.joy = True
            
            elif event.type == pygame.JOYDEVICEREMOVED:
                # self.joy = False
                ...

            elif event.type == pygame.QUIT:
                pygame.quit()

    def run(self):
        while True:    
            self.process_events()
            

            self.render_scroll = self.camera_control()
            
            self.tilemap.render(self.display, offset=self.render_scroll, mode='game')

            for index in range(len(self.enemies)):
                enemy = self.enemies[index]
                enemy.update(self.tilemap, index, self.movement)
                enemy.render(self.display, offset=self.render_scroll)
            
            self.pop_list.sort(reverse=True)

            for index in self.pop_list:
                self.enemies.pop(index)
            self.pop_list=[]

            for index in range(len(self.players)):
                player = self.players[index]
                player.update(self.tilemap, (self.movement[index][1]-self.movement[index][0], 0))
                player.render(self.display, offset=self.render_scroll)

            self.screen.blit(pygame.transform.scale(self.display, self.screen_size), (0,0))

            self.ui.update()
            self.ui.render(self.screen)

            
            pygame.display.update()
            self.clock.tick(60)


# Game().run()  # Start the program execution
