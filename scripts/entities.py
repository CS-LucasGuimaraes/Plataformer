import pygame

from scripts.utils import getxy

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = pos
        self.size = size

        self.action = ''
        
        self.velocity = [1, 1]
        
        self.collisions = {
            'up': False,
            'down': False,
            'right': False,
            'left': False,
        }
        
        self.set_action('idle')
        self.flip = False

        self.plataform_bottom = {}


    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()


    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    

    def side_plataform_collid_update(self, entity_rect):
        for i in self.plataform_bottom:
            if self.plataform_bottom[i]:
                return True
        self.pos[0] = entity_rect.x
        return False
    

    def checkpoint_collisions(self, tilemap):
        entity_rect = self.rect()

        for rect in tilemap.checkpoints_around(self.pos):
            if entity_rect.colliderect(rect[0]):
                self.checkpoint = [rect[1][0]*tilemap.tile_size, rect[1][1]*tilemap.tile_size]

                return 0
    
    
    def collectibles_collisions(self, tilemap):
        entity_rect = self.rect()

        for rect in tilemap.collectibles_around(self.pos):
            if entity_rect.colliderect(rect[0]):
                self.collectibles[rect[1]] += 1
                del tilemap.tilemap[rect[2]]

                return 0


    def gates_collisions(self, tilemap):
        entity_rect = self.rect()

        for rect in tilemap.gates_around(self.pos):
            if entity_rect.colliderect(rect[0]):
                if self.collectibles['key'] > 0:
                    self.collectibles['key']-=1
                    
                    del tilemap.tilemap[rect[2]]

                return 0


    def physics_tiles_collisions_X(self, tilemap, frame_movement):
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if not self.side_plataform_collid_update(entity_rect):
                    if frame_movement[0] > 0:
                        self.collisions['right'] = True
                        entity_rect.right = rect.left
                    elif frame_movement[0] < 0:
                        self.collisions['left'] = True
                        entity_rect.left = rect.right
                    self.pos[0] = entity_rect.x
    

    def physics_tiles_collisions_Y(self, tilemap, frame_movement):
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] < 0:
                    self.collisions['up'] = True
                    entity_rect.top = rect.bottom
                elif frame_movement[1] > 0:
                    self.collisions['down'] = True
                    entity_rect.bottom = rect.top
                self.pos[1] = entity_rect.y

    
    def plataform_tiles_collisions_X(self, tilemap, frame_movement):
        entity_rect = self.rect()
        for rect in tilemap.plataform_rects_around(self.pos):
            if entity_rect.colliderect(rect):                   # CHECKS RECT COLISION FOR IT OF THEN
                if not self.side_plataform_collid_update(entity_rect):
                    if frame_movement[0] < 0:
                        self.collisions['left'] = True
                        entity_rect.left = rect.right               # THE LEFT OF THE ENTITY BECAMES THE RIGHT OF THE RECT
                    elif frame_movement[0] > 0:                       
                        self.collisions['right'] = True
                        entity_rect.right = rect.left               # THE RIGHT OF THE ENTITY BECAMES THE LEFT OF THE RECT
                    self.pos[0] = entity_rect.x


    def plataform_tiles_collisions_Y(self, tilemap, frame_movement):
        entity_rect = self.rect()

        self.plataform_bottom = {(a,b):self.plataform_bottom.get((a,b), False) for (a,b) in [getxy(k) for k in tilemap.plataform_rects_around(self.pos)]}
        
        # if self.plataform_bottom: print(self.plataform_bottom)
        for rect in tilemap.plataform_rects_around(self.pos):

            if entity_rect.colliderect(rect):

                if (frame_movement[1] <= 0) or self.side_plataform_collid_update(entity_rect):
                    for key in self.plataform_bottom:
                        self.plataform_bottom[key] = True
                
                elif (frame_movement[1] > 0):
                    if not self.side_plataform_collid_update(entity_rect):
                        entity_rect.bottom = rect.top
                        self.collisions['down'] = True
                        self.pos[1] = entity_rect.y

            else:
                self.plataform_bottom[getxy(rect)] = False


    def death_tiles_collisions(self, tilemap):
        entity_rect = self.rect()

        for rect in tilemap.death_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                self.pos = self.checkpoint.copy()
                self.flip = False
                self.hearts -= 1
                return 0
    

    def render(self, surf, offset=[0,0]):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0], self.pos[1] - offset[1]))

    def update(self, tilemap, movement=(0,0)):

        self.collisions = {
            'up': False,
            'down': False,
            'right': False,
            'left': False,
        }

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])       # GRAVITY


        self.pos[0] += frame_movement[0]
        if self.type == 'player':
            self.gates_collisions(tilemap)
            self.collectibles_collisions(tilemap)
            self.checkpoint_collisions(tilemap)
        self.plataform_tiles_collisions_X(tilemap, frame_movement)
        self.physics_tiles_collisions_X(tilemap, frame_movement)
        
        
        self.pos[1] += frame_movement[1]
        if self.type == 'player':
            self.gates_collisions(tilemap)
            self.collectibles_collisions(tilemap)
            self.checkpoint_collisions(tilemap)
        self.plataform_tiles_collisions_Y(tilemap, frame_movement)
        self.physics_tiles_collisions_Y(tilemap, frame_movement)

        self.death_tiles_collisions(tilemap)

        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0]-0.1, 0)
        if self.velocity[0] < 0:
            self.velocity[0] = min(self.velocity[0]+0.1, 0)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
    
        if movement[0] > 0:
            self.flip = False

        if movement[0] < 0:
            self.flip = True

        self.animation.update()


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)

        self.hearts = 3
        self.jumps = 2
        self.air_time = 0
        self.in_air = False
        self.ANIMATION_OFFSET = [2,0]
        self.checkpoint = list(pos)
        self.collectibles = {'key': 0, 'coin': 0, 'diamond': 0}


    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement)

        self.air_time += 1

        if self.air_time > 10:
            self.in_air = True

        if self.collisions['down']:
            self.jumps = 2
            self.air_time = 0
            self.in_air = False
            self.plataform_bottom = {}

        if self.in_air:
            if self.collisions['left'] or self.collisions['right']:
                self.set_action('wall_jump')
            else:
                self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')



    def jump(self):
        if self.in_air and (self.collisions['left'] or self.collisions['right']):
            if self.collisions['left']:
                self.velocity[0] = +2.75
                self.flip = True
            elif self.collisions['right']:
                self.velocity[0] = -2.75
                self.flip = False

            self.velocity[1] = -2
            self.jumps = max(0, self.jumps-1)

        elif (self.jumps > 0): 
            if (self.jumps != 2) or (self.jumps == 2 and (self.air_time < 10)):
                self.velocity[1] = -3.1
                self.jumps -= 1
                self.in_air = True



                



    def render(self, surf, offset=[0, 0]):
            surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] - self.ANIMATION_OFFSET[0], self.pos[1] - offset[1] - self.ANIMATION_OFFSET[1]))
