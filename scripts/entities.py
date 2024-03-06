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

        self.came_from_bottom = {}

        self.collide = self.def_collisions()


    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()


    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    

    def any_came_from_bottom(self, entity_rect):
        for i in self.came_from_bottom:
            if self.came_from_bottom[i]:
                return True
        self.pos[0] = entity_rect.x
        return False
    

    def def_collisions(self):
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
                    if not self.any_came_from_bottom(entity_rect):
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
                    if not self.any_came_from_bottom(entity_rect):
                        if frame_movement[0] < 0:
                            self.collisions['left'] = True
                            entity_rect.left = rect.right               # THE LEFT OF THE ENTITY BECAMES THE RIGHT OF THE RECT
                        elif frame_movement[0] > 0:                       
                            self.collisions['right'] = True
                            entity_rect.right = rect.left               # THE RIGHT OF THE ENTITY BECAMES THE LEFT OF THE RECT
                        self.pos[0] = entity_rect.x


        def plataform_tiles_collisions_Y(self, tilemap, frame_movement):
            entity_rect = self.rect()

            self.came_from_bottom = {(a,b):self.came_from_bottom.get((a,b), False) for (a,b) in [getxy(k) for k in tilemap.plataform_rects_around(self.pos)]}
            
            for rect in tilemap.plataform_rects_around(self.pos):

                if entity_rect.colliderect(rect):

                    if (frame_movement[1] <= 0) or self.any_came_from_bottom(entity_rect):
                        for key in self.came_from_bottom:
                            self.came_from_bottom[key] = True
                    
                    elif (frame_movement[1] > 0):
                        if not self.any_came_from_bottom(entity_rect):
                            entity_rect.bottom = rect.top
                            self.collisions['down'] = True
                            self.pos[1] = entity_rect.y

                else:
                    self.came_from_bottom[getxy(rect)] = False


        def death_tiles_collisions(self, tilemap):
            entity_rect = self.rect()

            for rect in tilemap.death_rects_around(self.pos):
                if entity_rect.colliderect(rect):
                    self.pos = self.checkpoint.copy()
                    self.flip = False
                    self.hearts -= 1
                    return 0

        return {'checkpoint': checkpoint_collisions, 'collectibles': collectibles_collisions, 'gates': gates_collisions, 'physics_X': physics_tiles_collisions_X, 'physics_Y': physics_tiles_collisions_Y, 'plataform_X': plataform_tiles_collisions_X, 'plataform_Y': plataform_tiles_collisions_Y, 'death': death_tiles_collisions}


    def movement_physics(self):
        self.velocity[1] = min(5, self.velocity[1] + 0.1)       # Gravity

        if self.velocity[0] > 0:                                
            self.velocity[0] = max(self.velocity[0]-0.1, 0)     # Right slowdown
        elif self.velocity[0] < 0:                              
            self.velocity[0] = min(self.velocity[0]+0.1, 0)     # Left slowdown

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0


    def facing_side(self, movement):
        if movement[0] > 0:
            self.flip = False

        if movement[0] < 0:
            self.flip = True


    def movement_and_collide(self, tilemap, movement):
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        if self.type == 'player':
            self.collide['gates'](self, tilemap)
            self.collide['collectibles'](self, tilemap)
            self.collide['checkpoint'](self, tilemap)
        self.collide['plataform_X'](self, tilemap, frame_movement)
        self.collide['physics_X'](self, tilemap, frame_movement)
        
        
        self.pos[1] += frame_movement[1]
        if self.type == 'player':
            self.collide['gates'](self, tilemap)
            self.collide['collectibles'](self, tilemap)
            self.collide['checkpoint'](self, tilemap)
        self.collide['plataform_Y'](self, tilemap, frame_movement)
        self.collide['physics_Y'](self, tilemap, frame_movement)

        self.collide['death'](self, tilemap)


    def update(self, tilemap, movement=(0,0)):

        self.collisions = {     # RESET
            'up': False,
            'down': False,
            'right': False,
            'left': False,
        }

        self.movement_and_collide(tilemap, movement)

        self.movement_physics()
    
        self.facing_side(movement)

        self.animation.update()


    def render(self, surf, offset=[0,0]):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0], self.pos[1] - offset[1]))


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)

        self.hearts = 3
        self.max_jumps = 2
        self.jumps = self.max_jumps
        self.air_time = 0
        self.in_air = False
        self.ANIMATION_OFFSET = [2,0]
        self.checkpoint = list(pos)
        self.collectibles = {'key': 0, 'coin': 0, 'diamond': 0}

    def jump_control(self):
        self.air_time += 1

        if self.air_time > 10:
            self.in_air = True

        if self.collisions['down']:
            self.jumps = self.max_jumps
            self.air_time = 0
            self.in_air = False
            self.came_from_bottom = {}

    def action_control(self, movement):
        if self.in_air:
            if self.collisions['left'] or self.collisions['right']:
                self.set_action('wall_jump')
            else:
                self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement)

        self.jump_control()

        self.action_control(movement)

    def wall_jump(self):
        if self.collisions['left']:
                self.velocity[0] = +2.75
                self.flip = True
        elif self.collisions['right']:
            self.velocity[0] = -2.75
            self.flip = False

        self.velocity[1] = -2
        self.jumps = max(0, self.jumps-1)
        
    def jump(self):
        if self.in_air and (self.collisions['left'] or self.collisions['right']):
            self.wall_jump()

        elif (self.jumps > 0): 
            if (self.jumps != self.max_jumps) or (self.jumps == self.max_jumps and (self.air_time < 10)):
                self.velocity[1] = -3.1
                self.jumps -= 1
                self.in_air = True

    def render(self, surf, offset=[0, 0]):
            surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] - self.ANIMATION_OFFSET[0], self.pos[1] - offset[1] - self.ANIMATION_OFFSET[1]))
