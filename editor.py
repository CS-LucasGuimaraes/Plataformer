import pygame

from scripts.tilemap import *

class Editor:
    def init_window(self):
        self.screen_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]

        # self.screen_size[0]/=1.5;self.screen_size[1]/=1.5
        self.surface_size = (480,270)       

        self.screen = pygame.display.set_mode((self.screen_size))
        self.display = pygame.Surface(self.surface_size)
        
        pygame.display.set_caption('EDITOR')


    def init_binds(self):
        self.keybinds = {
            'right': [pygame.K_d, pygame.K_RIGHT],
            'left': [pygame.K_a, pygame.K_LEFT],
            'up': [pygame.K_w, pygame.K_UP],
            'down': [pygame.K_s, pygame.K_DOWN],
        }

        self.clicking = False
        self.right_clicking = False

        self.shift = False
        self.control = False

        self.ongrid = True


    def init_camera(self):
        self.RENDER_SCALE = self.screen_size[0] / 480
        self.movement = [False, False, False, False]
        self.scroll = [0,0]


    def init_assets(self):
        from scripts.assets import assets

        merge_dict = assets
        
        self.assets = {
        }

        for k in merge_dict:
            self.assets[k] = merge_dict[k]


        self.tilemap = Tilemap(self)

        try:
            self.tilemap.load(self.map)
            self.spawn_point = self.tilemap.spawn_point
        except FileNotFoundError:
            self.spawn_point = [0,0]
            pass

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0



    def __init__(self):
        pygame.init()

        level = input("Which level do you want to edit? ")

        self.map = 'levels/level'+level+'.json'

        self.init_window()
        self.init_binds()
        self.init_camera()
        self.init_assets()

        self.clock = pygame.time.Clock()


    def process_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:       # LEFT CLICK
                        self.clicking = True
                    elif event.button == 3:     # RIGHT CLICK
                        self.right_clicking = True


                    elif event.button == 4:
                        if not self.shift:
                            self.tile_group = (self.tile_group -1) % len(self.assets)
                            self.tile_variant = 0
                        else:
                            self.tile_variant = (self.tile_variant -1) % len(self.assets[self.tile_list[self.tile_group]])

                    elif event.button == 5:
                        if not self.shift:
                            self.tile_group = (self.tile_group +1) % len(self.assets)
                            self.tile_variant = 0
                        else:
                            self.tile_variant = (self.tile_variant +1) % len(self.assets[self.tile_list[self.tile_group]])

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:       # LEFT CLICK
                        self.clicking = False
                    elif event.button == 3:     # RIGHT CLICK
                        self.right_clicking = False

                elif event.type == pygame.KEYDOWN:
                    
                    if event.key in self.keybinds['left']:
                        self.movement[0] = True
                    elif event.key in self.keybinds['right']:
                        self.movement[1] = True
                    elif event.key in self.keybinds['up']:
                        self.movement[2] = True
                    elif event.key in self.keybinds['down'] and not self.control:
                        self.movement[3] = True

                    elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        self.shift = True
                    elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                        self.control = True

                    if self.control:
                        if event.key == pygame.K_s:
                            self.tilemap.save(self.map)


                elif event.type == pygame.KEYUP:
                    if event.key in self.keybinds['left']:
                        self.movement[0] = False
                    elif event.key in self.keybinds['right']:
                        self.movement[1] = False
                    elif event.key in self.keybinds['up']:
                        self.movement[2] = False
                    elif event.key in self.keybinds['down']:
                        self.movement[3] = False

                    elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                        self.shift = False
                    elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                        self.control = False


    def camera_control(self):
        self.scroll[0] += (self.movement[1] - self.movement[0]) *2
        self.scroll[1] += (self.movement[3] - self.movement[2]) *2


    def get_tile_pos(self):
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / self.RENDER_SCALE, mpos[1] / self.RENDER_SCALE)

            return (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size),
                        int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))


    def tile_preview(self, tile_pos):
        if self.tile_list[self.tile_group] in self.tilemap.ANIMATED_TILES:
            current_tile_img = self.assets[self.tile_list[self.tile_group]].img().copy()
            
        else:
            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
        current_tile_img.set_alpha(100)

        self.display.blit(current_tile_img, (5,5))

        if self.ongrid:
            self.display.blit(current_tile_img, (tile_pos[0] *self.tilemap.tile_size - self.scroll[0], tile_pos[1] *self.tilemap.tile_size - self.scroll[1]))


    def tilemap_update(self, tile_pos):
        if self.ongrid:
            if self.clicking:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}

                if self.tile_list[self.tile_group] == 'spawn_point':
                    self.spawn_point = [int(tile_pos[0]*self.tilemap.tile_size-self.tilemap.tile_size/2), int(tile_pos[1]*self.tilemap.tile_size-self.tilemap.tile_size/2)]
            
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]

    def run(self):
        while True:
            self.process_events()

            self.camera_control()

            tile_pos = self.get_tile_pos()
            self.tilemap.render(self.display, offset=self.scroll, mode='editor')
            self.tilemap_update(tile_pos)            
            self.tile_preview(tile_pos)
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))

            pygame.display.update()
            self.clock.tick(60)


Editor().run()  # Start the program execution
