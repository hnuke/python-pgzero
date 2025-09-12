import random
import math
from pgzero.actor import Actor
from pygame import Rect 


# Game Variables and methods
WIDTH = 1200
HEIGHT = 600
GRAVITY_FORCE = 0.5
HORIZONTAL_VELOCITY = 5
JUMP_FORCE = -11.5
PLAYER_POS_START = (WIDTH - 120, HEIGHT / 2)

# Enemy spawn positions
ENEMY1_POS = (200, HEIGHT - 160)
ENEMY2_POS = (500, HEIGHT - 280)
ENEMY3_POS = (800, HEIGHT - 160)
ENEMY4_POS = (900, HEIGHT - 280)


def reset_game():
    player.collision_rect.center = PLAYER_POS_START
    player.vertical_velocity = 0
    player.jumping = False
    player.moving = False
    player.current_frame = 0
    reset_pos_enemy()

def reset_pos_enemy():
    enemies[0].actor.pos = (ENEMY1_POS[0], ENEMY1_POS[1])
    enemies[1].actor.pos = (ENEMY2_POS[0], ENEMY2_POS[1])
    enemies[2].actor.pos = (ENEMY3_POS[0], ENEMY3_POS[1])
    enemies[3].actor.pos = (ENEMY4_POS[0], ENEMY4_POS[1])

    



# Tiles
platform_size = (128, 32)
platforms = [
    Rect((0, HEIGHT - 40), (WIDTH, 32)),
    Rect((WIDTH / 2, HEIGHT - 160), platform_size),
    Rect((WIDTH / 4, HEIGHT - 160), platform_size),
    Rect((0, HEIGHT / 1.5), ((192,32))),
    Rect((WIDTH / 8, HEIGHT / 2), platform_size),
    Rect((WIDTH / 3, HEIGHT / 2), platform_size),
    Rect((WIDTH / 1.9, HEIGHT / 2), platform_size),
    Rect((WIDTH / 1.4, HEIGHT / 3), platform_size),
    ]

tile_width = 64
tile_height = 64
def apply_tiles_in_platforms():
    for platform in platforms:
        num_tiles = math.ceil(platform.width / tile_width)
        for i in range(num_tiles):
            x_tile = platform.x + i * tile_width
            y_tile = platform.y
            screen.blit("tiles/center", (x_tile, y_tile))
def drawing_platforms():
    for platform in platforms:
        screen.draw.rect(platform, (255,0,0))
    apply_tiles_in_platforms()


# ---- PLAYER ----
class Player:
    def __init__(self, x, y):
        # Sprite
        self.actor = Actor('player/idle_right0', (x, y))

        # Frames
        self.idle_right_frames = ['player/idle_right0', 'player/idle_right1', 'player/idle_right2', 'player/idle_right3']
        self.idle_left_frames = ['player/idle_left0', 'player/idle_left1', 'player/idle_left2', 'player/idle_left3']
        self.walk_right_frames = ['player/walkright0', 'player/walkright1', 'player/walkright2',
        'player/walkright3', 'player/walkright4', 'player/walkright5', 'player/walkright6']
        self.walk_left_frames = ['player/walkleft0', 'player/walkleft1', 'player/walkleft2', 
        'player/walkleft3', 'player/walkleft4', 'player/walkleft5', 'player/walkleft6']
        self.jump_right_frames = ['player/jump_right3','player/jump_right4']
        self.jump_left_frames = ['player/jump_left1', 'player/jump_left2']

        # Hitbox (collider) - less size than the actor sprite player, for avoiding bug
        hitbox_width = 36
        hitbox_height = 61
        self.collision_rect = Rect(
            x - hitbox_width // 2,
            y - hitbox_height // 2,
            hitbox_width,
            hitbox_height
        )

        # Movement attributes
        self.vertical_velocity = 0
        self.horizontal_velocity = HORIZONTAL_VELOCITY
        self.moving = False
        self.jumping = False
        self.flip_x = False
        self.previous_bottom = self.collision_rect.bottom  # Para controle de colisão

        self.current_frame = 0
        self.frame_counter = 1

    def update(self):
        self.previous_bottom = self.collision_rect.bottom
        self.apply_movement()
        self.apply_physics()
        self.apply_animation()
        self.apply_boundary()

    def draw(self):
        # Sprite follows the collider
        self.actor.x = self.collision_rect.centerx
        self.actor.y = self.collision_rect.centery
        self.actor.draw()
        # for debug
        # screen.draw.rect(self.collision_rect, (0, 255, 0))

    def apply_movement(self):
        self.moving = False

        if keyboard.a:
            self.collision_rect.x -= self.horizontal_velocity
            self.moving = True
            self.flip_x = True
        if keyboard.d:
            self.collision_rect.x += self.horizontal_velocity
            self.moving = True
            self.flip_x = False
        if keyboard.space and not self.jumping:
            self.jumping = True
            self.vertical_velocity = JUMP_FORCE

    def apply_physics(self):
        self.vertical_velocity += GRAVITY_FORCE
        self.collision_rect.y += self.vertical_velocity

        for platform in platforms:
            if not self.collision_rect.colliderect(platform):
                continue
            # Collision from above (player falling onto the platform)
            if self.vertical_velocity > 0 and self.previous_bottom <= platform.top and self.collision_rect.bottom > platform.top:
                self.collision_rect.bottom = platform.top
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
            frames = self.idle_left_frames if self.flip_x else self.idle_right_frames
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.actor.image = frames[self.current_frame]
        self.frame_counter = 0

    def apply_boundary(self):
        if self.collision_rect.left < 0:
            self.collision_rect.left = 0
        if self.collision_rect.right > WIDTH:
            self.collision_rect.right = WIDTH
        if self.collision_rect.top < 0:
            self.collision_rect.top = 0
        if self.collision_rect.bottom > HEIGHT:
            self.collision_rect.bottom = HEIGHT

player = Player(PLAYER_POS_START[0], PLAYER_POS_START[1])

# ---- ENEMY ----
class Enemy:
    def __init__(self, x, y):
        self.actor = Actor("enemy/bee_left0", (x,y))
        
        # Frames
        self.left_frames = ["enemy/bee_left0", "enemy/bee_left1"]
        self.right_frames = ["enemy/bee_right0", "enemy/bee_right1"]

        # Attributes
        self.horizontal_velocity = 2
        self.direction = -1
        self.left_limit = 10
        self.right_limit = WIDTH - 10

        self.current_frame = 0
        self.frame_counter = 1

    def apply_animation(self):
        self.frame_counter += 1
        if self.frame_counter <= 10: # Avoiding nested if
            return
        frames = self.left_frames if self.direction == -1 else self.right_frames
        self.current_frame = (self.current_frame + 1) % len(frames)
        self.actor.image = frames[self.current_frame]
        self.frame_counter = 0

    def apply_movement(self):
        self.actor.x += self.horizontal_velocity * self.direction
        if self.actor.x <= self.left_limit or self.actor.x >= self.right_limit:
            self.direction *= -1
        
    def apply_physics(self):
        if self.actor.colliderect(player.collision_rect):
            reset_game()
    
    def draw(self):
        self.actor.draw()

    def update(self):
        self.apply_movement()
        self.apply_physics()
        self.apply_animation()

enemies = [
    Enemy(ENEMY1_POS[0], ENEMY1_POS[1]),
    Enemy(ENEMY2_POS[0], ENEMY2_POS[1]),
    Enemy(ENEMY3_POS[0], ENEMY3_POS[1]),
    Enemy(ENEMY4_POS[0], ENEMY4_POS[1])
]


enemy = Enemy(WIDTH / 2, HEIGHT / 2)

# ---- GOAL ----
class Goal:
    def __init__(self, x, y):
        self.actor = Actor('goal', (x,y))

    def draw(self):
        self.actor.draw()

    def check_collision(self, player):
        if self.actor.colliderect(player.collision_rect):
            reset_game()

goal = Goal(WIDTH - 50, 50)
# ---- MAIN FUNCTION ----
def draw():
    screen.clear()
    screen.blit('background', (-WIDTH / 1.2, -HEIGHT / 1.2))
    drawing_platforms()
    goal.draw()
    for enemy in enemies:
        enemy.draw()
    player.draw()

def update():
    player.update()
    goal.check_collision(player)
    for enemy in enemies:
        enemy.update()

