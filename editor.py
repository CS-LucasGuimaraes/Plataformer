import pygame

from scripts.tilemap import *
from scripts.utils import load_image, load_images, Animation

class Editor:
    def __init__(self):
        pygame.init()

        self.screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)

        self.screen = pygame.display.set_mode(self.screen_size)
        self.display = pygame.Surface((480, 270))
        self.clock = pygame.time.Clock()

        self.RENDER_SCALE = self.screen_size[0] / 480

        pygame.display.set_caption('EDITOR')
        
        from scripts.assets import assets

        merge_dict = assets
        
        self.assets = {
        }

        for k in merge_dict:
            self.assets[k] = merge_dict[k]


        self.tilemap = Tilemap(self)

        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.movement = [False, False, False, False]

        self.scroll = [0,0]

        self.clicking = False
        self.right_clicking = False

        self.shift = False
        self.control = False

        self.ongrid = True
        

        self.keybinds = {
            'right': [pygame.K_d, pygame.K_RIGHT],
            'left': [pygame.K_a, pygame.K_LEFT],
            'up': [pygame.K_w, pygame.K_UP],
            'down': [pygame.K_s, pygame.K_DOWN],
        }

    def run(self):
        while True:
            self.display.fill((120,120,120))

            if self.tile_list[self.tile_group] in self.tilemap.ANIMATED_TILES:
                current_tile_img = self.assets[self.tile_list[self.tile_group]].img().copy()
            
            else:
                current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)

            self.display.blit(current_tile_img, (5,5))

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / self.RENDER_SCALE, mpos[1] / self.RENDER_SCALE)

            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size),
                        int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))
            
    
            self.scroll[0] += (self.movement[1] - self.movement[0]) *2
            self.scroll[1] += (self.movement[3] - self.movement[2]) *2


            self.tilemap.render(self.display, offset=self.scroll, mode='editor')


            if self.ongrid:
                self.display.blit(current_tile_img, (tile_pos[0] *self.tilemap.tile_size - self.scroll[0],
                                                     tile_pos[1] *self.tilemap.tile_size - self.scroll[1]))
                if self.clicking:
                    self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
                
                if self.right_clicking:
                    tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                    if tile_loc in self.tilemap.tilemap:
                        del self.tilemap.tilemap[tile_loc]


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
                            self.tilemap.save('map.json')


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

            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))

            pygame.display.update()
            
            self.clock.tick(60)


Editor().run()  # Start the program execution
