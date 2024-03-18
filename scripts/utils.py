import os

import pygame

BASE_IMG_PATH = 'data/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0,0,0))
    return img

def load_images(path):
    images = []
    for img in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path+'/'+img))
    return images

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
    
def restart_level(game, next_level=False):
    if next_level: 
        game.current_level += 1
    game.enemies = []
    game.tilemap.load('levels/level'+str(game.current_level)+'.json')
    game.player.pos = game.tilemap.spawn_point
    game.player.checkpoint = game.player.pos