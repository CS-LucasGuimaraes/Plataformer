import pygame

from scripts.utils import getxy, restart_level
from scripts.menu.game_over import Game_over

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size, idx=''):
        self.game = game
        self.type = e_type
        self.pos = pos
        self.size = size
        self.idx = idx

        self.game_over = Game_over(self.game, self.game.joysticks)

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
            self.animation = self.game.assets[self.type + str(self.idx) + '/' + self.action].copy()


    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    

    def inside_plataform(self, entity_rect):
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
                    if self.checkpoint[0] != rect[1][0]*tilemap.tile_size or (self.checkpoint[1] < rect[1][1]*tilemap.tile_size-36 and self.checkpoint[1] > rect[1][1]*tilemap.tile_size+36) : 
                        self.checkpoint = [rect[1][0]*tilemap.tile_size, rect[1][1]*tilemap.tile_size]
                        self.game.sounds['checkpoint'].play()
                    return 0
        

        def mario_tiles_collisions(self, tilemap, frame_movement):
            entity_rect = self.rect()
            for rect in tilemap.mario_boxes_around(self.pos):
                if entity_rect.colliderect(rect[0]):
                    if frame_movement[1] < 0:
                        self.game.sounds['collectible'].play()
                        tilemap.tilemap[str(rect[1][0])+';'+str(rect[1][1])]['type'] = 'mario_box_opened'
                        tilemap.tilemap[str(rect[1][0])+';'+str(rect[1][1]-1)] = {"type": "coin", "variant": 0, "pos": [rect[1][0],rect[1][1]-1]}
                        
        
        def next_level_collisions(self, tilemap):
            entity_rect = self.rect()

            for rect in tilemap.next_level_around(self.pos):
                if entity_rect.colliderect(rect[0]):
                    restart_level(self.game, next_level=True)
                    return 0
        

        def collectibles_collisions(self, tilemap):
            entity_rect = self.rect()

            for rect in tilemap.collectibles_around(self.pos):
                if entity_rect.colliderect(rect[0]):
                    self.game.cooperative_status.collectibles[rect[1]] += 1
                    self.game.sounds['collectible'].play()
                    del tilemap.tilemap[rect[2]]

                    return 0


        def gates_collisions(self, tilemap):
            entity_rect = self.rect()

            for rect in tilemap.gates_around(self.pos):
                if entity_rect.colliderect(rect[0]):
                    if self.game.cooperative_status.collectibles['key'] > 0:
                        self.game.cooperative_status.collectibles['key']-=1
                        self.game.sounds['open_crate'].play()
                        
                        del tilemap.tilemap[rect[2]]

                    return 0


        def physics_tiles_collisions_X(self, tilemap, frame_movement):
            entity_rect = self.rect()
            for rect in tilemap.physics_rects_around(self.pos):
                if entity_rect.colliderect(rect):
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
                    if not self.inside_plataform(entity_rect):
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

                    if (frame_movement[1] <= 0) or self.inside_plataform(entity_rect):
                        for key in self.came_from_bottom:
                            self.came_from_bottom[key] = True
                    
                    elif (frame_movement[1] > 0):
                        if not self.inside_plataform(entity_rect):
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
                    self.game.cooperative_status.hearts -= 1
                    self.game.sounds['damage'].play()
                    return 0
        
        def spike_tiles_collisions_X(self, tilemap, frame_movement):
            entity_rect = self.rect()
            if self.type != 'player':
                for rect in tilemap.spike_rects_around(self.pos):
                    if entity_rect.colliderect(rect):
                        if frame_movement[0] > 0:
                            self.collisions['right'] = True
                            entity_rect.right = rect.left
                        elif frame_movement[0] < 0:
                            self.collisions['left'] = True
                            entity_rect.left = rect.right
                        self.pos[0] = entity_rect.x

            elif self.type == 'player':
                for rect in tilemap.spike_rects_around(self.pos):
                    if entity_rect.colliderect(rect):
                        self.pos = self.checkpoint.copy()
                        self.flip = False
                        self.game.sounds['damage'].play()
                        self.game.cooperative_status.hearts -= 1
                        return 0
            
        def spike_tiles_collisions_Y(self, tilemap, frame_movement):
            entity_rect = self.rect()
            if self.type != 'player':
                for rect in tilemap.spike_rects_around(self.pos):
                    if entity_rect.colliderect(rect):
                        if frame_movement[1] < 0:
                            self.collisions['up'] = True
                            entity_rect.top = rect.bottom
                        elif frame_movement[1] > 0:
                            self.collisions['down'] = True
                            entity_rect.bottom = rect.top
                        self.pos[1] = entity_rect.y
            
            elif self.type == 'player':
                for rect in tilemap.spike_rects_around(self.pos):
                    if entity_rect.colliderect(rect):
                        self.pos = self.checkpoint.copy()
                        self.flip = False
                        self.game.sounds['damage'].play()
                        self.game.cooperative_status.hearts -= 1
                        return 0

        return {'checkpoint': checkpoint_collisions, 'next_level': next_level_collisions, 'mario_box': mario_tiles_collisions, 'collectibles': collectibles_collisions, 'gates': gates_collisions, 'physics_X': physics_tiles_collisions_X, 'physics_Y': physics_tiles_collisions_Y, 'plataform_X': plataform_tiles_collisions_X, 'plataform_Y': plataform_tiles_collisions_Y, 'death': death_tiles_collisions, 'spike_X': spike_tiles_collisions_X, 'spike_Y': spike_tiles_collisions_Y}


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
            self.collide['next_level'](self, tilemap)
            self.collide['mario_box'](self, tilemap, frame_movement)
        self.collide['plataform_X'](self, tilemap, frame_movement)
        self.collide['physics_X'](self, tilemap, frame_movement)
        self.collide['spike_X'](self, tilemap, frame_movement)

        
        self.pos[1] += frame_movement[1]
        if self.type == 'player':
            self.collide['gates'](self, tilemap)
            self.collide['collectibles'](self, tilemap)
            self.collide['checkpoint'](self, tilemap)
            self.collide['next_level'](self, tilemap)
            self.collide['mario_box'](self, tilemap, frame_movement)
        self.collide['plataform_Y'](self, tilemap, frame_movement)
        self.collide['physics_Y'](self, tilemap, frame_movement)
        self.collide['spike_Y'](self, tilemap, frame_movement)

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
    def __init__(self, game, pos, size, idx):
        super().__init__(game, 'player', pos, size, idx)

        # self.hearts = 3
        self.max_jumps = 2
        self.jumps = self.max_jumps
        self.air_time = 0
        self.in_air = False
        self.ANIMATION_OFFSET = [2,0]
        self.checkpoint = list(pos).copy()
        # self.collectibles = {'key': 0, 'coin': 0, 'diamond': 0}

    def jump_control(self):
        self.air_time += 1

        if self.air_time > 10:
            self.in_air = True

        if self.collisions['down']:
            self.jumps = self.max_jumps
            self.air_time = 0
            self.in_air = False

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

    def hearts_control(self):
        if self.game.cooperative_status.hearts <= 0:

            self.game.tilemap.render(self.game.display, offset=self.game.render_scroll, mode='game')
            for index in range(len(self.game.enemies)):
                enemy = self.game.enemies[index]
                enemy.render(self.game.display, offset=self.game.render_scroll)
            
            for index in range(len(self.game.players)):
                player = self.game.players[index]
                player.render(self.game.display, offset=self.game.render_scroll)

            self.game.screen.blit(pygame.transform.scale(self.game.display, self.game.screen_size), (0,0))

            self.game.ui.update()
            self.game.ui.render(self.game.screen)

            self.game_over.run(self.game.display)
            self.game.movement = [[False, False],[False, False],[False, False],[False, False]]

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement)

        if movement[0] == 0 or self.in_air:
            self.game.sounds['walk'].stop()
            self.paused = True
        elif self.paused:
            self.game.sounds['walk'].play(-1)
            self.paused = False

        self.hearts_control()

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
            self.game.sounds['jump'].play()

        elif (self.jumps > 0): 
            if (self.jumps != self.max_jumps) or (self.jumps == self.max_jumps and (self.air_time < 10)):
                self.game.sounds['jump'].play()
                self.velocity[1] = -3.1
                self.jumps -= 1
                self.in_air = True

    def render(self, surf, offset=[0, 0]):
            surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] - self.ANIMATION_OFFSET[0], self.pos[1] - offset[1] - self.ANIMATION_OFFSET[1]))

class enemy(PhysicsEntity):
    def __init__(self, game, pos, size, players):
        self.players = players
        super().__init__(game, 'enemy', pos, size)

    def update(self, tilemap, index, player_movement):
        for idx in range(len(self.players)):
            player = self.players[idx]
            if self.rect().colliderect(player.rect()):
                frame_movement = (player_movement[idx][0] + player.velocity[0], player_movement[idx][1] + player.velocity[1])


                if frame_movement[1] > 0 and (player.pos[1] <= self.pos[1]-self.size[1] + 2 or player.pos[1] <= self.pos[1]-self.size[1] - 2):
                    self.collisions['up'] = True
                elif frame_movement[1] < 0:
                    self.collisions['down'] = True
                
                if frame_movement[0] < 0:
                    self.collisions['right'] = True
                elif frame_movement[0] > 0:
                    self.collisions['left'] = True

                if self.collisions['up']:
                    self.game.sounds['jump'].play()
                    self.game.sounds['kill'].play()
                    player.velocity[1] = -2
                    self.game.pop_list.append(index)
                elif self.collisions['left'] or self.collisions['right'] or self.collisions['down']:
                    self.game.sounds['damage'].play()
                    self.game.cooperative_status.hearts -= 1
                    player.pos = player.checkpoint.copy()
                    player.flip = False
                
        if not self.flip:
            if self.collisions['right'] or not tilemap.check_fall_right(self.pos):
                self.flip = not self.flip
            else:
                return super().update(tilemap, (0.6,0))
            
        else:
            if self.collisions['left'] or not tilemap.check_fall_left(self.pos):
                self.flip = not self.flip
            else:
                return super().update(tilemap, (-0.6,0))

        return super().update(tilemap, (0,0))

