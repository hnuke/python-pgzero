import random
import math
from pgzero.actor import Actor
from pygame import Rect 

WIDTH = 1200
HEIGHT = 600
GRAVITY_FORCE = 0.5
HORIZONTAL_VELOCITY = 5

# Ground
ground = Rect((0, HEIGHT - 40), (WIDTH, 40))

# ---- PLAYER ----
class Player:
    def __init__(self, x, y):
        self.actor = Actor('player/idle0', (x, y))
        
        # Framesad
        self.idle_frames = ['player/idle0', 'player/idle1', 'player/idle2', 'player/idle3']
        self.walk_right_frames = ['player/walkright0', 'player/walkright1', 'player/walkright2',
        'player/walkright3', 'player/walkright4', 'player/walkright5', 'player/walkright6']
        self.walk_left_frames = ['player/walkleft0', 'player/walkleft1', 'player/walkleft2', 
        'player/walkleft3', 'player/walkleft4', 'player/walkleft5', 'player/walkleft6']
        # Walk + Jump frames
        self.jump_right_frames = ['player/jump_right0', 'player/jump_right1', 'player/jump_right2', 
        'player/jump_right3', 'player/jump_right4', 'player/jump_right5']

        self.jump_left_frames = ['player/jump_left0', 'player/jump_left1', 'player/jump_left2', 
        'player/jump_left3', 'player/jump_left4', 'player/jump_left5'
]


        # Atributos
        self.vertical_velocity = 0
        self.horizontal_velocity = HORIZONTAL_VELOCITY
        self.moving = False
        self.jumping = False
        self.facing_left = False

        self.current_frame = 0
        self.frame_counter = 1

    def update(self):
        self.apply_movement()
        self.apply_physics()
        self.apply_animation()

    def draw(self):
        self.actor.draw()

    def apply_movement(self):
        self.moving = False
        keys = keyboard

        if keys.a:
            self.actor.x -= self.horizontal_velocity
            self.moving = True
            self.facing_left = True
        if keys.d:
            self.actor.x += self.horizontal_velocity
            self.moving = True
            self.facing_left = False

    def apply_physics(self):
        self.vertical_velocity += GRAVITY_FORCE
        self.actor.y += self.vertical_velocity

        if self.actor.bottom > ground.top:
            self.actor.bottom = ground.top
            self.vertical_velocity = 0
            self.jumping = False

    def apply_animation(self):
        self.frame_counter += 1
        if self.frame_counter <= 10:
            return

        if self.moving:
            frames = self.walk_left_frames if self.facing_left else self.walk_right_frames
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.actor.image = frames[self.current_frame]
        elif not self.moving and not self.jumping:
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            self.actor.image = self.idle_frames[self.current_frame]

        self.frame_counter = 0


player = Player(WIDTH / 2, HEIGHT / 2)


# ---- MAIN FUNCTION ----
def draw():
    screen.clear()
    player.draw()
def update():
    player.update()
