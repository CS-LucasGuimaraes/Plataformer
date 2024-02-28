import pygame

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

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        

    def check_collision_X(self, tilemap, frame_movement):
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    self.collisions['right'] = True
                    entity_rect.right = rect.left
                if frame_movement[0] < 0:
                    self.collisions['left'] = True
                    entity_rect.left = rect.right
                self.pos[0] = entity_rect.x
    
    def check_collision_Y(self, tilemap, frame_movement):
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] < 0:
                    self.collisions['up'] = True
                    entity_rect.top = rect.bottom
                if frame_movement[1] > 0:
                    self.collisions['down'] = True
                    entity_rect.bottom = rect.top
                self.pos[1] = entity_rect.y



    def render(self, surf):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), self.pos)

    def update(self, tilemap, movement=(0,0)):
        self.collisions = {
            'up': False,
            'down': False,
            'right': False,
            'left': False,
        }

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])       # GRAVITY


        self.pos[0] += frame_movement[0]
        self.check_collision_X(tilemap, frame_movement)
        
        self.pos[1] += frame_movement[1]
        self.check_collision_Y(tilemap, frame_movement)

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

        self.jumps = 2
        self.air_time = 0
        self.in_air = False

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement)

        self.air_time += 1

        if self.air_time > 10:
            self.in_air = True

        if self.collisions['down']:
            self.jumps = 2
            self.air_time = 0
            self.in_air = False

        if self.in_air:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')


    def jump(self):
        if (self.jumps > 0): 
            if (self.jumps != 2) or (self.jumps == 2 and (self.air_time < 10)):
                self.velocity[1] = -3.1
                self.jumps -= 1