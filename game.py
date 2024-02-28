import pygame

from scripts.tilemap import *
from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1920,1080))
        self.display = pygame.Surface((430, 270))
        self.clock = pygame.time.Clock()

        pygame.display.set_caption('pygame ip')

        self.assets = {
            'grass': load_images('tiles/grass'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump'), img_dur=5),
            'player/slide': Animation(load_images('entities/player/slide'), img_dur=5),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide'), img_dur=5),
        }

        self.tilemap = Tilemap(self)
        self.player = Player(self, [96,40], [8,15])

        self.movement = [False, False]
        

        self.keybinds = {
            'right': [pygame.K_d, pygame.K_RIGHT],
            'left': [pygame.K_a, pygame.K_LEFT],
            'jump': [pygame.K_w, pygame.K_UP, pygame.K_SPACE],
        }

    def run(self):
        while True:
            self.display.fill((120,120,120))
    
            self.tilemap.render(self.display)

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
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    elif event.key == pygame.K_d:
                        self.movement[1] = False

            
            self.player.update(self.tilemap, (self.movement[1]-self.movement[0], 0))
            self.player.render(self.display)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0,0))

            pygame.display.update()
            
            self.clock.tick(60)

        return 1


Game().run()  # Start the program execution
