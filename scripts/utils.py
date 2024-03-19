import os, json
import pygame

BASE_IMG_PATH = 'data/images/'
BASE_SFX_PATH = 'data/sfx/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0,0,0))
    return img

def load_images(path):
    images = []
    for img in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path+'/'+img))
    return images

def load_sound(path):
    return pygame.mixer.Sound(BASE_SFX_PATH + path)

def load_music(path):
    return pygame.mixer.music.load(BASE_SFX_PATH + path)

def getxy(rect):
    return (rect.x, rect.y)

class Animation():
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.img_duration = img_dur
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration*len(self.images) - 1)
            if self.frame >= self.img_duration*len(self.images)-1:
                self.done = True

    def img(self):
        return self.images[int(self.frame/self.img_duration)]

def json_dump(game):
    f = open('saves/'+ str(game.save) +'.json', 'w')
    json.dump({'current_level': game.current_level,
               'current_hearts': game.cooperative_status.hearts,
               'current_collectibles': game.cooperative_status.collectibles,
               }, f)
    f.close()

def restart_level(game, next_level=False):
    if next_level: 
        game.current_level += 1
        pygame.mixer.Sound.play(game.sounds['next_level'])

        json_dump(game)

    game.enemies = []
    game.tilemap.load('levels/level'+str(game.current_level)+'.json')
    for player in game.players:
        player.checkpoint = game.tilemap.spawn_point.copy()
        player.pos = player.checkpoint.copy()

    f = open('saves/'+str(game.save)+'.json', 'r')
    data = json.load(f)
    f.close()

    game.cooperative_status.collectibles['coin'] = data['current_collectibles']['coin']
    game.cooperative_status.collectibles['diamond'] = data['current_collectibles']['diamond']
    game.cooperative_status.collectibles['key'] = data['current_collectibles']['key']