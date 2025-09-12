import random
import math
from pgzero.actor import Actor
from pygame import Rect 

WIDTH = 1200
HEIGHT = 600
GRAVITY_FORCE = 0.5
HORIZONTAL_VELOCITY = 5
JUMP_FORCE = -14

# Ground
platforms = [
    Rect((0, HEIGHT - 40), (WIDTH, 40)),
    Rect((WIDTH / 2, HEIGHT - 160), (200, 40)),
    Rect((0, HEIGHT / 2), ((200,40)))
    ]

# ---- PLAYER ----
class Player:
    def __init__(self, x, y):
        self.actor = Actor('player/idle0', (x, y))
        
        # Frames
        self.idle_right_frames = ['player/idle_right0', 'player/idle_right1', 'player/idle_right2', 'player/idle_right3']
        self.idle_left_frames = ['player/idle_left0', 'player/idle_left1', 'player/idle_left2', 'player/idle_left3']
        self.walk_right_frames = ['player/walkright0', 'player/walkright1', 'player/walkright2',
        'player/walkright3', 'player/walkright4', 'player/walkright5', 'player/walkright6']
        self.walk_left_frames = ['player/walkleft0', 'player/walkleft1', 'player/walkleft2', 
        'player/walkleft3', 'player/walkleft4', 'player/walkleft5', 'player/walkleft6']
        self.jump_right_frames = ['player/jump_right3','player/jump_right4']
        self.jump_left_frames = ['player/jump_left1', 'player/jump_left2']

        # Atributos
        self.vertical_velocity = 0
        self.horizontal_velocity = HORIZONTAL_VELOCITY
        self.moving = False
        self.jumping = False
        self.flip_x = False

        self.current_frame = 0
        self.frame_counter = 1

    def update(self):
        self.apply_movement()
        self.apply_physics()
        self.apply_animation()
        self.apply_boundary()

    def draw(self):
        self.actor.draw()

    def apply_movement(self):
        self.moving = False

        if keyboard.a:
            self.actor.x -= self.horizontal_velocity
            self.moving = True
            self.flip_x = True
        if keyboard.d:
            self.actor.x += self.horizontal_velocity
            self.moving = True
            self.flip_x = False
        if keyboard.space and not self.jumping:
            self.jumping = True
            self.vertical_velocity = JUMP_FORCE

    def apply_physics(self):
        self.vertical_velocity += GRAVITY_FORCE
        self.actor.y += self.vertical_velocity

        for platform in platforms:
            if not self.actor.colliderect(platform):
                continue
            if self.vertical_velocity > 0 and self.actor.bottom > platform.top:
                self.actor.bottom = platform.top
                self.vertical_velocity = 0
                self.jumping = False

    def apply_animation(self):
        self.frame_counter += 1
        if self.frame_counter <= 10: # Avoiding nested if
            return
        if self.jumping:
            frames = self.jump_left_frames if self.flip_x else self.jump_right_frames
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.actor.image = frames[self.current_frame]
        elif self.moving:
            frames = self.walk_left_frames if self.flip_x else self.walk_right_frames
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.actor.image = frames[self.current_frame]
        elif not self.moving and not self.jumping:
            self.current_frame = (self.current_frame + 1) % len(self.idle_right_frames)
            self.actor.image = self.idle_frames[self.current_frame]


        self.frame_counter = 0

    def apply_boundary(self):
        self.actor.x = 0 if self.actor.x < 0 else self.actor.x
        self.actor.x = WIDTH if self.actor.x > WIDTH else self.actor.x

player = Player(WIDTH / 2, HEIGHT / 2)

def drawing_platforms():
    for platform in platforms:
        screen.draw.rect(platform, (255,0,0))

# ---- MAIN FUNCTION ----
def draw():
    screen.clear()
    player.draw()
    drawing_platforms()
def update():
    player.update()
