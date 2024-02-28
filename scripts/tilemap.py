import pygame

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]
PHYSICS_TILES = {'grass'}

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {
            "5;7": {"type": "grass", "variant": 4, "pos": [5, 7]},
            "6;7": {"type": "grass", "variant": 4, "pos": [6, 7]},
            "7;7": {"type": "grass", "variant": 4, "pos": [7, 7]},
            "8;7": {"type": "grass", "variant": 4, "pos": [8, 7]},
            "9;7": {"type": "grass", "variant": 4, "pos": [9, 7]},
            "10;7": {"type": "grass", "variant": 4, "pos": [10, 7]},
            "10;6": {"type": "grass", "variant": 4, "pos": [10, 6]},
            "10;5": {"type": "grass", "variant": 4, "pos": [10, 5]},
            }
        self.offgrid_tiles = []

    def render(self, surf):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0]*self.tile_size, tile['pos'][1]*self.tile_size))

    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0]+ offset[0]) + ';' + str(tile_loc[1]+offset[1])
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])
        return tiles
    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile['type'] in PHYSICS_TILES:
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects