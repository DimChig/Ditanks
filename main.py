import math
import random
import time
import numpy as np
import heapq
import pygame

pygame.init()

screen_width = 0
screen_height = 0
grid_size = 20

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#screen = pygame.display.set_mode((1920, 1080))
# screen = pygame.display.set_mode((500, 500))
screen_width = screen.get_width()
screen_height = screen.get_height()

pygame.display.set_caption("Ditanks")
pygame.display.set_icon(pygame.image.load("img/logo.png"))
pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))

# rele куду
isVisualisationOn = False
doBulletsCollide = True


def draw_grid():
    for line in range(0, 20):
        pygame.draw.line(screen, (255, 255, 255), (0, line * tile_size), (screen_height, line * tile_size))
        pygame.draw.line(screen, (255, 255, 255), (line * tile_size, 0), (line * tile_size, screen_height))


def generateWorld():
    arr = []
    corners = []
    global grid_size, sprites_tilemap_box, world_data, world_data_corners, world_maps, world_map_id
    world_data_corners = []
    for i in range(0, grid_size):
        line = []
        for j in range(0, grid_size):
            x = random.randint(0, 2)
            if x == 2:
                x = 1
            else:
                x = 0
            line.append(x)
        arr.append(line)

    # fill borders
    for i in range(0, grid_size):
        arr[i][0] = 1
        arr[0][i] = 1
        arr[i][grid_size - 1] = 1
        arr[grid_size - 1][i] = 1
    arr[int(grid_size / 2)][int(grid_size / 2)] = 0

    while True:
        b = False
        if world_map_id == -1:
            b = True
        new_id = random.randint(0, len(world_maps) - 1 - 1) #kcid +1
        if world_map_id != new_id != -1:
            world_map_id = new_id
            break
        if b == True:
            break

    arr = world_maps[world_map_id]

    # reformat array to tilemap
    for i in range(0, grid_size):
        for j in range(0, grid_size):
            x = arr[i][j]
            corner = 0
            if x > 0:
                p1 = 0
                p2 = 0
                p3 = 0
                p4 = 0
                p5 = 0
                p6 = 0
                p7 = 0
                p8 = 0
                if i > 0:
                    p1 = arr[i - 1][j]
                if j < grid_size - 1:
                    p2 = arr[i][j + 1]
                if i < grid_size - 1:
                    p3 = arr[i + 1][j]
                if j > 0:
                    p4 = arr[i][j - 1]
                if i > 0 and j > 0:
                    p5 = arr[i - 1][j - 1]
                if i > 0 and j < grid_size - 1:
                    p6 = arr[i - 1][j + 1]
                if i < grid_size - 1 and j > 0:
                    p8 = arr[i + 1][j - 1]
                if i < grid_size - 1 and j < grid_size - 1:
                    p7 = arr[i + 1][j + 1]

                if p1 != 0: p1 = 1
                if p2 != 0: p2 = 1
                if p3 != 0: p3 = 1
                if p4 != 0: p4 = 1
                if p5 != 0: p5 = 1
                if p6 != 0: p6 = 1
                if p7 != 0: p7 = 1
                if p8 != 0: p8 = 1

                corners = []
                if p1 == 0 and p2 == 0 and p3 == 0 and p4 == 0:
                    x = 0
                elif p1 == 0 and p2 == 0 and p3 == 0 and p4 == 1:
                    x = 2
                elif p1 == 0 and p2 == 0 and p3 == 1 and p4 == 0:
                    x = 1
                elif p1 == 0 and p2 == 0 and p3 == 1 and p4 == 1:
                    x = 6
                    if p8 == 0: corners.append(4)
                elif p1 == 0 and p2 == 1 and p3 == 0 and p4 == 0:
                    x = 4
                elif p1 == 0 and p2 == 1 and p3 == 0 and p4 == 1:
                    x = 14
                elif p1 == 0 and p2 == 1 and p3 == 1 and p4 == 0:
                    x = 5
                    if p7 == 0: corners.append(3)
                elif p1 == 0 and p2 == 1 and p3 == 1 and p4 == 1:
                    x = 10
                    if p7 == 0: corners.append(3)
                    if p8 == 0: corners.append(4)
                elif p1 == 1 and p2 == 0 and p3 == 0 and p4 == 0:
                    x = 3
                elif p1 == 1 and p2 == 0 and p3 == 0 and p4 == 1:
                    x = 7
                    if p5 == 0: corners.append(1)
                elif p1 == 1 and p2 == 0 and p3 == 1 and p4 == 0:
                    x = 13
                elif p1 == 1 and p2 == 0 and p3 == 1 and p4 == 1:
                    x = 11
                    if p5 == 0: corners.append(1)
                    if p8 == 0: corners.append(4)
                elif p1 == 1 and p2 == 1 and p3 == 0 and p4 == 0:
                    x = 8
                    if p6 == 0: corners.append(2)
                elif p1 == 1 and p2 == 1 and p3 == 0 and p4 == 1:
                    x = 12
                    if p5 == 0: corners.append(1)
                    if p6 == 0: corners.append(2)
                elif p1 == 1 and p2 == 1 and p3 == 1 and p4 == 0:
                    x = 9
                    if p6 == 0: corners.append(2)
                    if p7 == 0: corners.append(3)
                elif p1 == 1 and p2 == 1 and p3 == 1 and p4 == 1:
                    x = 15
                    if p5 == 0: corners.append(1)
                    if p6 == 0: corners.append(2)
                    if p7 == 0: corners.append(3)
                    if p8 == 0: corners.append(4)

                arr[i][j] = x
                for c in corners:
                    world_data_corners.append((c, i, j))
                    # pass
    world_data = arr


def getPlayerSpriteSize():
    global player_collider_size, player_zoom, grid_size
    a = player_collider_size * tile_size * grid_size / player_zoom
    # a2 = int(a/math.sqrt(2))
    return a


# variables
tile_size = int(screen_height / grid_size / 5) * 5
world_data = []
world_data_corners = []
world_map_id = -1

# player
playerX = 0
playerY = 0
player_dirY = 0
player_dirX = 0
player_id = 1
player_zoom = 10  # editable (n,m grid size visible)
player_speed = 40 / grid_size  # editable
player_body_angle = 0
player_body_angle_speed = 1  # editable
player_turret_angle = 0
player_trail = []
player_trail_lifetime = 200
player_trail_frequency = 20
player_health = 0
player_health_max = 100  # editable
player_health_regen_speed = 10  # editable
player_health_regen_delay = 50  # editable
player_health_regen_delay_counter = 0
player_health_regen_time = 3  # editable time to not receive damage
player_health_regen_lasttime = time.time()
player_ultimate = 0
player_ultimate_max = 20
player_ultimate_step = 1
player_score = 0
player_score_for_ai_normal = 50
player_death_time = time.time()
player_death_cooldown = 1  # 2 seconds agter death and restart
isGameOver = False
ai_damage_normal = 0
bullets = []
bullet_distance = 20  # editable (x blocks)
bullet_speed = 4
bullet_lifetime = 0
bullet_lifetime_ai = 0
bullets_max = 3
bullets_frequency = 5
doBulletsCollideWithPlayer = True
animations = []
tanks = []
boosters = []
booster_collider = 0.5

difficulty_new_bots = 1.5 #e %



def getNextPosByAngle(x, y, angle, speed):
    x += speed * math.cos(math.radians(angle))
    y += speed * math.sin(math.radians(angle))
    return x, y


class Bullet:
    def __init__(self, x, y, angle, sprite, lifetime, player_id):
        self.x = x
        self.y = y
        self.idx = 0
        self.angle = angle
        self.sprite = sprite
        self.player_id = player_id
        self.lifetime = lifetime
        self.trail_arr = []
        self.bounces = 0

    def move(self):
        global bullet_speed
        self.x, self.y = getNextPosByAngle(self.x, self.y, self.angle, bullet_speed)


class PlayerTrail:
    def __init__(self, x, y, angle, player_id):
        self.x = x
        self.y = y
        self.angle = angle
        self.idx = 0
        self.player_id = player_id


class Animation:
    def __init__(self, n, sprite_arr, scale, pos, delay, angle):
        self.n = n
        self.sprite_arr = sprite_arr
        self.pos = pos
        self.scale = scale
        self.delay = delay
        self.angle = angle
        self.delay_cnt = 0
        self.idx = 0
        self.isBehindPlayer = False

class BoosterTemplate:
    def __init__(self, id, lifetime, spawnrate):
        self.id = id
        self.lifetime = lifetime
        self.spawnrate = spawnrate

boosters_templates = [BoosterTemplate(0, 20, 20)]



class Booster:
    def __init__(self, i, j, id, lifetime):
        self.i = i
        self.j = j
        self.id = id
        self.lifetime = lifetime #seconds
        self.spawn_time = time.time()
        self.x = self.j * tile_size
        self.y = self.i * tile_size


# load images
cell_size = tile_size / player_zoom * grid_size
player_collider_size = 0.5
sprite_sand = pygame.transform.scale(pygame.image.load('img/Environment/sand.png'), (cell_size, cell_size))
sprite_dirt = pygame.transform.scale(pygame.image.load('img/Environment/dirt.png'), (cell_size, cell_size))
sprite_plank = pygame.transform.scale(pygame.image.load('img/Environment/plank.png'), (cell_size, cell_size))
sprite_player_ultimate = pygame.image.load('img/ultimate_icon.png')
sprite_gameOver = pygame.image.load('img/gameOver.png')
sprite_gameOver_bg = pygame.transform.scale(pygame.image.load('img/bg_black.png'), (screen_width, screen_height))
sprite_tank_body = pygame.transform.scale(pygame.image.load('img/Tanks/tankGreen_outline.png'),
                                          (getPlayerSpriteSize(), getPlayerSpriteSize()))
sprite_tank_turret = pygame.transform.scale(pygame.image.load('img/Tanks/barrelGreen_outline.png'),
                                            (getPlayerSpriteSize() / 3, getPlayerSpriteSize() / 3 * 2.4))
sprite_bullet = pygame.transform.scale(pygame.image.load('img/Bullets/bulletGreenSilver_outline.png'),
                                       (sprite_tank_turret.get_width(), sprite_tank_turret.get_width() * 1.7))
sprite_tank_ai_body = pygame.transform.scale(pygame.image.load('img/Tanks/tankBlue_outline.png'),
                                             (sprite_tank_body.get_width(), sprite_tank_body.get_height()))
sprite_tank_ai_turret = pygame.transform.scale(pygame.image.load('img/Tanks/barrelBlue_outline.png'),
                                               (sprite_tank_turret.get_width(), sprite_tank_turret.get_height()))
sprite_ai_bullet = pygame.transform.scale(pygame.image.load('img/Bullets/bulletBlueSilver_outline.png'),
                                          (sprite_bullet.get_width(), sprite_bullet.get_height()))
sprite_step = pygame.image.load('img/Environment/step1.png')
sprites_tilemap_box = [
    pygame.transform.scale(pygame.image.load('img/Environment/box/box0.png'), (cell_size, cell_size)),
    pygame.transform.scale(pygame.image.load('img/Environment/box/box1.png'), (cell_size, cell_size)),
    pygame.transform.scale(pygame.image.load('img/Environment/box/box2.png'), (cell_size, cell_size)),
    pygame.transform.scale(pygame.image.load('img/Environment/box/box3.png'), (cell_size, cell_size)),
    pygame.transform.scale(pygame.image.load('img/Environment/box/box4.png'), (cell_size, cell_size)),
    pygame.transform.scale(pygame.image.load('img/Environment/box/box5.png'), (cell_size, cell_size)),
    pygame.transform.scale(pygame.image.load('img/Environment/box/box6.png'), (cell_size, cell_size)),
    pygame.transform.scale(pygame.image.load('img/Environment/box/box7.png'), (cell_size, cell_size)),
    pygame.transform.scale(pygame.image.load('img/Environment/box/box8.png'), (cell_size, cell_size)),
    pygame.transform.scale(pygame.image.load('img/Environment/box/box9.png'), (cell_size, cell_size)),
    pygame.transform.scale(pygame.image.load('img/Environment/box/box10.png'), (cell_size, cell_size)),
    pygame.transform.scale(pygame.image.load('img/Environment/box/box11.png'), (cell_size, cell_size)),
    pygame.transform.scale(pygame.image.load('img/Environment/box/box12.png'), (cell_size, cell_size)),
    pygame.transform.scale(pygame.image.load('img/Environment/box/box13.png'), (cell_size, cell_size)),
    pygame.transform.scale(pygame.image.load('img/Environment/box/box14.png'), (cell_size, cell_size)),
    pygame.transform.scale(pygame.image.load('img/Environment/box/box15.png'), (cell_size, cell_size))]
corners_size = cell_size / 5
print(tile_size, " than ", cell_size, " so ", corners_size)
sprites_tilemap_corners = [
    pygame.transform.scale(pygame.image.load('img/Environment/box/corner1.png'), (corners_size, corners_size)),
    pygame.transform.scale(pygame.image.load('img/Environment/box/corner2.png'), (corners_size, corners_size)),
    pygame.transform.scale(pygame.image.load('img/Environment/box/corner3.png'), (corners_size, corners_size)),
    pygame.transform.scale(pygame.image.load('img/Environment/box/corner4.png'), (corners_size, corners_size))]

boosters_size = 0.5 * cell_size
sprite_boosters = [pygame.transform.scale(pygame.image.load('img/Environment/heal.png'), (boosters_size, boosters_size))]
sprites_anim_fire = [pygame.image.load('img/AnimBulletBurst/anim1.png'),
                     pygame.image.load('img/AnimBulletBurst/anim2.png'),
                     pygame.image.load('img/AnimBulletBurst/anim3.png'),
                     pygame.image.load('img/AnimBulletBurst/anim4.png'),
                     pygame.image.load('img/AnimBulletBurst/anim5.png'),
                     pygame.image.load('img/AnimBulletBurst/anim6.png')]
sprites_death_green = [pygame.image.load('img/AnimTankDestroy/Green/anim1.png'),
                       pygame.image.load('img/AnimTankDestroy/Green/anim2.png'),
                       pygame.image.load('img/AnimTankDestroy/Green/anim3.png'),
                       pygame.image.load('img/AnimTankDestroy/Green/anim4.png')]
sprites_death_blue = [pygame.image.load('img/AnimTankDestroy/Blue/anim1.png'),
                      pygame.image.load('img/AnimTankDestroy/Blue/anim2.png'),
                      pygame.image.load('img/AnimTankDestroy/Blue/anim3.png'),
                      pygame.image.load('img/AnimTankDestroy/Blue/anim4.png')]
sprites_death_explosion = [pygame.image.load('img/AnimTankDestroy/Explosion/anim1.png'),
                           pygame.image.load('img/AnimTankDestroy/Explosion/anim2.png'),
                           pygame.image.load('img/AnimTankDestroy/Explosion/anim3.png'),
                           pygame.image.load('img/AnimTankDestroy/Explosion/anim4.png'),
                           pygame.image.load('img/AnimTankDestroy/Explosion/anim5.png'),
                           pygame.image.load('img/AnimTankDestroy/Explosion/anim6.png')]
sprites_heal = []
for i in range(1, 26): sprites_heal.append(pygame.image.load("img/AnimHeal/heal" + str(i) + ".png"))
sprites_tp1 = []
for i in range(1, 26): sprites_tp1.append(pygame.image.load("img/AnimTankTeleport1/anim" + str(i) + ".png"))
sprites_tp2 = []
for i in range(1, 20): sprites_tp2.append(pygame.image.load("img/AnimTankTeleport2/anim" + str(i) + ".png"))

#SOUNDS
pygame.mixer.init()
sound_shoot_player = pygame.mixer.Sound("sounds/shoot_player.wav")
sound_shoot_player_no_ammo = pygame.mixer.Sound("sounds/no ammo.mp3")
sound_bullet_ricochet = pygame.mixer.Sound("sounds/ricochet.mp3")
sound_explosion = pygame.mixer.Sound("sounds/bot_explosion2.mp3")
sound_explosion_player = pygame.mixer.Sound("sounds/explosion_player.wav")
sound_gameOver = pygame.mixer.Sound("sounds/gameOver.wav")
sound_heal_pick_up = pygame.mixer.Sound("sounds/heal_pick_up.mp3")
sound_player_hit = pygame.mixer.Sound("sounds/body_hit.mp3")
sound_bullet_collide = pygame.mixer.Sound("sounds/bullet_collide2.mp3")
sound_player_teleport = pygame.mixer.Sound("sounds/teleport.wav")
pygame.mixer.music.load('sounds/beat2.wav')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.2)

#I wanted to use the fastest solution for my testing. I could easily add a simple json file, but this was just faster, sorry for this =)
world_maps = [[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1], [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1], [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1], [1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1], [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1], [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1], [1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1], [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1], [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1], [1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1], [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], [1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1], [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1], [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1], [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1], [1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1], [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1], [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1], [1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1], [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1], [1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1], [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1], [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1], [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1], [1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1], [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1], [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1], [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1], [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1], [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1], [1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1], [1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1], [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1], [1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1], [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1], [1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1], [1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1], [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1], [1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1], [1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1], [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1], [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1], [1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]]

pygame.font.init()
font_gameOver = pygame.font.Font("fonts/main.otf", 100)
font_score = pygame.font.Font("fonts/main.otf", 80)
font_debug = pygame.font.Font("fonts/main.otf", 30)


def spawnPlayer():
    global playerX, playerY, tile_size, bullet_lifetime, bullet_lifetime_ai, player_health, player_health_max, player_score, player_death_time, isGameOver, run
    i, j = 1, 1
    dist_from_center = 0.2
    while True:
        i = int(random.uniform(grid_size * (0.5 - dist_from_center), grid_size * (0.5 + dist_from_center)))
        j = int(random.uniform(grid_size * (0.5 - dist_from_center), grid_size * (0.5 + dist_from_center)))
        if world_data[i][j] == 0:
            break


    playerX = j * tile_size + tile_size / 2
    playerY = i * tile_size + tile_size / 2
    player_health = player_health_max
    bullet_lifetime = bullet_distance * 20 / bullet_speed
    bullet_lifetime_ai = bullet_lifetime / 1.5
    player_score = 0
    playerResetRegenTimer()
    player_death_time = time.time()
    playerHandleAiDamage()
    isGameOver = False
    run = True


def blitRotate(surf, image, pos, originPos, angle):
    angle = 360 - angle
    image_rect = image.get_rect(topleft=(pos[0] - originPos[0], pos[1] - originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
    surf.blit(rotated_image, rotated_image_rect)


def rotatePosByOrigin(pos1, origin, angle):
    px, py = pos1
    ox, oy = origin

    angle = math.radians(angle)

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def handlePlayerBodyRotateAngle():
    global player_body_angle, player_body_angle_speed, player_dirX, player_dirY

    # player_body_angle = -45
    to_angle = player_body_angle
    x = player_dirX
    y = player_dirY
    if x == 0 and y == 0:
        to_angle = player_body_angle
    elif x == 1 and y == 0:
        to_angle = 90
    elif x == -1 and y == 0:
        to_angle = 270
    elif x == 0 and y == 1:
        to_angle = 180
    elif x == 0 and y == -1:
        to_angle = 0

    elif x == 1 and y == 1:
        to_angle = 135
    elif x == 1 and y == -1:
        to_angle = 45
    elif x == -1 and y == 1:
        to_angle = 225
    elif x == -1 and y == -1:
        to_angle = 315

    x = player_body_angle
    y = to_angle
    dir = 0

    if x < y:
        y -= x
        x = 0
        d1 = y
        d2 = 360 - y
        if d1 >= d2:
            dir = -1
        else:
            dir = 1
    elif x > y:
        x -= y
        y = 0
        d1 = x
        d2 = 360 - x
        if (d1 >= d2):
            dir = 1
        else:
            dir = -1

    player_body_angle += dir * player_body_angle_speed
    player_body_angle = player_body_angle % 360


def handlePlayerTurretRotateAngle():
    global player_turret_angle

    to_angle = player_turret_angle

    mouseX, mouseY = pygame.mouse.get_pos()
    angle = math.degrees(math.atan2(mouseY - screen_height / 2, mouseX - screen_width / 2))
    to_angle = (angle + 90) % 360
    player_turret_angle = to_angle


def convertPosToCameraPos(pos):
    global playerX, playerY, grid_size, player_zoom
    x = pos[0] - playerX * grid_size / player_zoom + screen_width / 2
    y = pos[1] - playerY * grid_size / player_zoom + screen_height / 2
    return (x, y)


def convertRealPosToCameraPos(pos):
    global playerX, playerY, grid_size, player_zoom
    x = (pos[0] - playerX) * grid_size / player_zoom + screen_width / 2
    y = (pos[1] - playerY) * grid_size / player_zoom + screen_height / 2
    return (x, y)


def drawMouseAim():
    global player_turret_angle

    mouseX, mouseY = pygame.mouse.get_pos()

    center = (mouseX, mouseY)
    radius1 = 30
    radius2 = 20
    radius3 = 10
    color1 = (255, 0, 0, 20)
    color2 = (255, 0, 0, 50)
    color3 = (255, 0, 0, 100)

    if isVisualisationOn == False:
        target_rect = pygame.Rect(center, (0, 0)).inflate((radius1 * 2, radius1 * 2))
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.circle(shape_surf, color1, (radius1, radius1), radius1)
        pygame.draw.circle(shape_surf, color2, (radius1, radius1), radius2)
        pygame.draw.circle(shape_surf, color3, (radius1, radius1), radius3)
        screen.blit(shape_surf, target_rect)
    else:
        pygame.draw.line(screen, (0, 115, 255), (screen_width / 2, screen_height / 2), (mouseX, mouseY), 7)
        pygame.draw.circle(screen, (0, 137, 217), (mouseX, mouseY), 30, 3)
        pygame.draw.circle(screen, (0, 115, 255), (mouseX, mouseY), 6, 6)

def drawPlayerAmmo():
    global isGameOver, bullets_max, player_id
    if isGameOver:
        return

    x = screen_width / 2
    y = screen_height / 2 - sprite_tank_body.get_height() / 2 - 7
    bar_width = sprite_tank_body.get_width() - 5
    bar_height = 8
    color_ammo = (255, 133, 2)
    color_ammo_outline = (195, 101, 0)
    color_empty = (169, 169, 169)
    color_empty_outline = (137, 137, 137)

    bars_count = bullets_max
    bullets_count = 0
    for b in bullets:
        if b.player_id == player_id: bullets_count += 1

    width = bar_width / bars_count
    x -= bar_width / 2
    for i in range(0, bars_count):
        x1 = x + width * i
        x2 = x1 + width
        if i == bars_count - 1:
            x2 = screen_width / 2 + bar_width / 2 - 1
        y1 = y
        y2 = y1 + bar_height

        c1 = color_ammo
        c2 = color_ammo_outline
        if i >= bullets_max - bullets_count:
            c1 = color_empty
            c2 = color_empty_outline
        pygame.draw.rect(screen, c1, (x1, y1, x2 - x1, y2 - y1))
        pygame.draw.rect(screen, c2, (x1, y1, x2 - x1, y2 - y1), 1)

def drawPlayerHealth():
    global isGameOver
    if isGameOver:
        return

    x = screen_width / 2
    y = screen_height / 2 - sprite_tank_body.get_height() / 2 - 10
    bar_width = sprite_tank_body.get_width() - 5
    bar_height = 8
    bar_width_green = int(bar_width * player_health / player_health_max)
    bar_width_red = bar_width - bar_width_green
    color_green = (0, 220, 0)
    color_red = (220, 0, 0)

    pygame.draw.rect(screen, color_green, (x - bar_width / 2, y - bar_height / 2, bar_width - 1, bar_height), 0)
    pygame.draw.rect(screen, color_red,
                     (x - bar_width / 2 + bar_width_green, y - bar_height / 2, bar_width_red, bar_height), 0)

def drawPlayerUltimate():
    global isGameOver, bullets_max, player_id, sprite_player_ultimate
    if isGameOver:
        return

    width = 150
    height = width
    color_empty = (195, 188, 0)
    color_fill = (255, 234, 0)
    color_outline = (138, 130, 0)

    x = screen_width - width/2 - 50
    y = screen_height - height/2 - 50
    sprite_player_ultimate = pygame.transform.scale(sprite_player_ultimate, (int(width * 0.7), int(height * 0.7)))
    pygame.draw.circle(screen, color_empty, (x, y), width/2)
    #pie
    theta = -90
    stop_angle = theta + int(map(player_ultimate, 0, player_ultimate_max, 0, 360))
    if stop_angle < -89: stop_angle = -91
    center = (x, y)
    radius = width / 2 - 2
    while theta <= stop_angle:
        pygame.draw.line(screen, color_fill, center,
                         (center[0] + radius * math.cos(math.radians(theta)), center[1] + radius * math.sin(math.radians(theta))), 3)
        theta += 1

    pygame.draw.circle(screen, color_outline, (x, y), width/2, 5)
    screen.blit(sprite_player_ultimate, (x - sprite_player_ultimate.get_width() / 2, y - sprite_player_ultimate.get_height() / 2))

def drawPlayer():
    global isGameOver
    if isGameOver:
        return

    player_collider = player_collider_size * tile_size * grid_size / player_zoom
    if isVisualisationOn:
        pygame.draw.rect(screen, (255, 0, 0), (
            screen_width / 2 - player_collider / 2, screen_height / 2 - player_collider / 2, player_collider,
            player_collider), 2)

    handlePlayerBodyRotateAngle()
    blitRotate(screen, sprite_tank_body, (screen_width / 2, screen_height / 2),
               (sprite_tank_body.get_width() / 2, sprite_tank_body.get_height() / 2), player_body_angle)

    handlePlayerTurretRotateAngle()
    drawMouseAim()
    blitRotate(screen, sprite_tank_turret, (screen_width / 2, screen_height / 2),
               (sprite_tank_turret.get_width() / 2, sprite_tank_turret.get_height() - 5), player_turret_angle)

    drawPlayerHealth()
    drawPlayerAmmo()


def drawBullets():
    global bullets
    for i in range(0, len(bullets)):
        bullet = bullets[i]
        x, y = convertRealPosToCameraPos((bullet.x, bullet.y))

        blitRotate(screen, bullet.sprite, (x, y), (sprite_bullet.get_width() / 2, sprite_bullet.get_height() / 2),
                   bullet.angle + 90)

        if (isVisualisationOn):
            collider_size = sprite_bullet.get_width()
            pygame.draw.rect(screen, (0, 194, 0),
                             (x - collider_size / 2, y - collider_size / 2, collider_size, collider_size), 3)
            pygame.draw.circle(screen, (77, 255, 77), (x, y), collider_size * 2, 1)
            pygame.draw.line(screen, (0, 166, 0), (x, y),
                             ((x + (bullet_speed * 40 * math.cos(math.radians(bullet.angle))),
                               y + (bullet_speed * 40 * math.sin(math.radians(bullet.angle))))), 2)


def drawPlayerScore():
    global player_score, font_score
    text = font_score.render(str(int(player_score)), True, (255, 255, 255))
    screen.blit(text, (screen_width - text.get_width() - 20, 10))


def drawWorld():
    global world_data_corners, world_data, playerX, playerY, player_zoom
    screen.fill((231, 223, 194))
    for i in range(0, len(world_data)):
        for j in range(0, len(world_data[0])):
            tile_x = j * cell_size
            tile_y = i * cell_size

            # relative to player
            x, y = convertPosToCameraPos((tile_x, tile_y))
            if (x < 0 - cell_size or x > screen_width + cell_size or y < -cell_size or y > screen_height + cell_size):
                continue

            img = sprite_sand
            type = world_data[i][j]
            if type == 0:
                img = sprite_sand
                screen.blit(img, (x, y))
            else:
                img = sprites_tilemap_box[type]

                screen.blit(img, (x, y))

            corner = 0

            for c in world_data_corners:
                if c[1] == i and c[2] == j:
                    corner = c[0]

                    img = sprites_tilemap_corners[corner - 1]

                    x1 = x
                    y1 = y
                    if corner == 2:
                        x1 = x + cell_size - img.get_width()
                    if corner == 3:
                        x1 = x + cell_size - img.get_width()
                        y1 = y + cell_size - img.get_height()
                    if corner == 4:
                        y1 = y + cell_size - img.get_height()
                    screen.blit(img, (x1, y1))
                    if False:
                        text = font_debug.render(str(int(type)), True, (255, 255, 255))
                        screen.blit(text,
                                (x + cell_size / 2 - text.get_width() / 2, y + cell_size / 2 - text.get_height() / 2))


def map(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)


def checkCollision(pos1, cell_size, pos2, cs):
    # pos1 => border

    s1 = cell_size
    s2 = cs
    x1 = pos1[0]
    y1 = pos1[1]
    x2 = pos2[0]
    y2 = pos2[1]

    collisionX = x1 + s1 >= x2 and x2 + s2 >= x1
    collisionY = y1 + s1 >= y2 and y2 + s2 >= y1

    return collisionX and collisionY


def createPlayerTrail():
    global player_trail, player_body_angle, player_trail_frequency, playerY, playerY, player_id

    if len(player_trail) == 0 or player_trail[len(player_trail) - 1].idx > player_trail_frequency:
        offset = sprite_tank_body.get_width() / 2.5 / grid_size * player_zoom
        randomness = 0.5

        x1, y1 = rotatePosByOrigin((playerX + offset + random.uniform(-randomness, randomness),
                                    playerY + offset + random.uniform(-randomness, randomness)), (playerX, playerY),
                                   player_body_angle)
        x2, y2 = rotatePosByOrigin((playerX - offset + random.uniform(-randomness, randomness),
                                    playerY + offset + random.uniform(-randomness, randomness)), (playerX, playerY),
                                   player_body_angle)

        player_trail.append(PlayerTrail(x1, y1, random.randint(0, 360), player_id))
        player_trail.append(PlayerTrail(x2, y2, random.randint(0, 360), player_id))

def drawBoosters():
    global sprite_boosters
    for booster in boosters:

        id = booster.id
        x, y = convertRealPosToCameraPos((booster.x, booster.y))
        x += cell_size/2
        y += cell_size/2

        seconds = time.time() - booster.spawn_time
        k = map(seconds, 0, booster.lifetime, 1, 0.3)
        if seconds > booster.lifetime:
            boosters.remove(booster)
        if id == 0 and k > 0:
            img = sprite_boosters[id]
            img_copy = img.copy()
            img_copy = pygame.transform.scale(img_copy, (img.get_width() * k, img.get_height() * k))
            screen.blit(img_copy, (x - img_copy.get_width() / 2, y - img_copy.get_height() / 2))


def drawArrow(x, y, color, size):
    arrowX, arrowY = (screen_width / 2, screen_height / 2)
    offset = 10

    dist = math.sqrt(math.pow(x - playerX, 2) + math.pow(y - playerY, 2))

    if dist > screen_width / grid_size * 8: return

    x, y = convertRealPosToCameraPos((x, y))

    if x < 0 or x > screen_width or y < 0 or y > screen_height:
        x2, y2 = (screen_width / 2, screen_height / 2)
        angle = (math.degrees(math.atan2(y - y2, x - x2))) % 360
        type = 0

        while True:
            arrowX, arrowY = getNextPosByAngle(arrowX, arrowY, angle, 10)

            if arrowX < 0 or arrowX > screen_width or arrowY < 0 or arrowY > screen_height:
                break

        if arrowX < offset:
            arrowX = offset
            type = 1
        if arrowX > screen_width - offset:
            arrowX = screen_width - offset
            type = 2
        if arrowY < offset:
            arrowY = offset
            type = 3
        if arrowY > screen_height - offset:
            arrowY = screen_height - offset
            type = 4


        if type == 1:
            pygame.draw.polygon(screen, color, [(arrowX, arrowY), (arrowX + size, arrowY - size / 1.8),
                                                (arrowX + size, arrowY + size / 1.8)])
        if type == 2:
            pygame.draw.polygon(screen, color, [(arrowX, arrowY), (arrowX - size, arrowY - size / 1.8),
                                                (arrowX - size, arrowY + size / 1.8)])
        if type == 3:
            pygame.draw.polygon(screen, color, [(arrowX, arrowY), (arrowX - size / 1.8, arrowY + size),
                                                (arrowX + size / 1.8, arrowY + size)])
        if type == 4:
            pygame.draw.polygon(screen, color, [(arrowX, arrowY), (arrowX - size / 1.8, arrowY - size),
                                                (arrowX + size / 1.8, arrowY - size)])

def drawArrows():
    for tank in tanks:
        color = (30, 167, 255)
        drawArrow(tank.x, tank.y, color, 20)
    for booster in boosters:
        color = -1
        if booster.id == 0:
            color = (4, 208, 77)
        if color == -1: continue
        drawArrow(booster.x, booster.y , color, 30)


def drawPlayerTrail():
    global player_trail, player_trail_lifetime

    for i in range(0, len(player_trail)):
        if i >= len(player_trail):
            break
        trail = player_trail[i]
        trail.idx += 1
        if trail.idx > player_trail_lifetime:
            player_trail.remove(trail)
            continue

        max_size = sprite_tank_body.get_width() / grid_size * player_zoom / 2
        i = player_trail_lifetime - trail.idx
        if (i > player_trail_lifetime / 2):
            size = max_size
        else:
            size = map(i, 0, player_trail_lifetime / 2, 0, max_size)

        img = pygame.transform.scale(sprite_step, (size, size))
        blitRotate(screen, img, convertRealPosToCameraPos((trail.x, trail.y)),
                   (img.get_width() / 2, img.get_height() / 2), trail.angle)

        if isVisualisationOn:
            pygame.draw.circle(screen, (255, 0, 0), convertRealPosToCameraPos((trail.x, trail.y)), size / 2)


def playerResetRegenTimer():
    global player_health_regen_lasttime, player_health_regen_delay_counter
    player_health_regen_lasttime = time.time()
    player_health_regen_delay_counter = 0


def playerReceiveDamage(bullet_pos):
    global player_health, ai_damage_normal, player_body_angle, sprites_death_green, isGameOver, player_death_time
    player_health -= ai_damage_normal
    playerResetRegenTimer()
    if player_health > 0:
        animations.append(Animation(6, sprites_death_explosion, 0.5, bullet_pos, 3, random.randint(0, 360)))
        playSound(sound_player_hit, 1)
    else:
        player_health = 0
        isGameOver = True
        player_death_time = time.time()
        animations.append(Animation(3, sprites_death_green, 0.6, (playerX, playerY), 5, player_body_angle))
        animations.append(Animation(6, sprites_death_explosion, 1, (playerX, playerY), 5, random.randint(0, 360)))
        playSound(sound_explosion_player, 1)


def playerHandleRegen():
    global player_health, player_health_regen_lasttime, player_health_regen_time, player_health_regen_speed, player_health_regen_delay, player_health_regen_delay_counter
    total_secs = round(time.time() - player_health_regen_lasttime)
    if total_secs > player_health_regen_time and player_health < player_health_max:
        player_health_regen_delay_counter += 1
        if player_health_regen_delay_counter > player_health_regen_delay:
            player_health_regen_delay_counter = 0
            player_health += player_health_regen_speed
            if player_health > player_health_max:
                player_health = player_health_max


def playerHandleAiDamage():
    global player_score, player_score_for_ai_normal, ai_damage_normal, player_health_max

    killed = player_score / player_score_for_ai_normal
    max_score = 5000
    max_tanks = max_score / player_score_for_ai_normal
    max_damage = player_health_max - 5

    x = map(killed, 0, max_tanks, 10, 1.1)
    ai_damage_normal = player_health_max / x  # editable
    if killed > max_tanks:
        ai_damage_normal = max_damage


def spawnBooster(booster_template):
    global world_data
    i, j = 1, 1
    dist_from_player = 2 #min distance

    playerI = int(map(playerY, 0, grid_size * tile_size, 0, grid_size))
    playerJ = int(map(playerX, 0, grid_size * tile_size, 0, grid_size))
    while True:

        i = int(random.uniform(0, grid_size))
        j = int(random.uniform(0, grid_size))
        if world_data[i][j] != 0:
            continue

        dist = math.sqrt(math.pow(i - playerI, 2) + math.pow(j - playerJ, 2))
        if dist < dist_from_player:
            continue
        break
    boosters.append(Booster(i, j, booster_template.id, booster_template.lifetime))






def playerKilledTank(tank):
    global player_score, player_score_for_ai_normal, player_ultimate, player_ultimate_max, player_ultimate_step, player_health_max, ai_damage_normal, boosters, boosters_templates
    tank.destroy()
    playSound(sound_explosion, 0.4)

    playerHandleAiDamage()

    player_score += player_score_for_ai_normal
    player_ultimate += player_ultimate_step
    if player_ultimate > player_ultimate_max:
        player_ultimate = player_ultimate

    spawnAiRandom()
    if int(random.uniform(0, 100 / difficulty_new_bots)) == 0:
        spawnAiRandom()


    booster = -1
    for booster_template in boosters_templates:
        if random.randint(0, booster_template.spawnrate) == 0:
            booster = booster_template
    if booster != -1:
        spawnBooster(booster)

def pickUpBooster(booster, x, y):
    global player_health, player_health_max, booster_collider
    id = booster.id
    if id == 0:
        player_health = player_health_max
        playSound(sound_heal_pick_up, 1)
    x += cell_size / 2 - booster_collider * cell_size / 2
    y += cell_size / 2 - booster_collider * cell_size / 2
    animations.append(Animation(25, sprites_heal, 1, (x, y), 3, 0))
    boosters.remove(booster)

def useUltimate():
    global world_data, player_ultimate, doBulletsCollideWithPlayer, player_ultimate_max, playerX, playerY, player_zoom, grid_size, screen_width, screen_height
    print(player_ultimate)
    if player_ultimate < player_ultimate_max: return
    mouseX, mouseY = pygame.mouse.get_pos()
    mouseX = (mouseX - screen_width/2) * player_zoom / grid_size + playerX
    mouseY = (mouseY - screen_height/2) * player_zoom / grid_size + playerY
    cellI = int(map(mouseY, 0, grid_size * tile_size, 0, grid_size))
    cellJ = int(map(mouseX, 0, grid_size * tile_size, 0, grid_size))
    if cellI < 0 or cellJ < 0 or cellI >= grid_size or cellJ >= grid_size: return
    if world_data[cellI][cellJ] != 0: return
    #tp player
    newX = cellJ * tile_size + tile_size/2
    newY = cellI * tile_size + tile_size/2
    angle = (math.degrees(math.atan2(newY - playerY, newX - playerX))) % 360
    speed = 10

    animations.append(Animation(25, sprites_tp1, 1, (playerX, playerY), 3, 0))
    anim2 = Animation(19, sprites_tp2, 1, (newX, newY), 3, 0)
    anim2.isBehindPlayer = True
    animations.append(anim2)

    playSound(sound_player_teleport, 0.5)
    doBulletsCollideWithPlayer = False

    player_ultimate = 0
    while True:
        playerX, playerY = getNextPosByAngle(playerX, playerY, angle, speed)
        clock.tick(60)
        moveBullets()
        drawWorld()
        handleAnimations(True)
        drawArrows()
        drawBoosters()
        drawTanks()
        drawBullets()
        drawPlayerScore()
        drawPlayerUltimate()
        handleAnimations(False)
        pygame.display.update()
        if abs(playerY - newY) < speed and abs(playerX - newX) < speed:
            playerX = newX
            playerY = newY
            break
    doBulletsCollideWithPlayer = True

def movePlayer():
    global isVisualisationOn, isGameOver, booster_collider
    if isGameOver:
        return

    isCollidingX = False
    isCollidingY = False
    forsetX = 0
    forsetY = 0

    global playerX, playerY, player_dirX, player_dirY, player_speed, world_data

    player_cellI = int(map(playerY, 0, grid_size * tile_size, 0, grid_size))
    player_cellJ = int(map(playerX, 0, grid_size * tile_size, 0, grid_size))

    colliding_array = []
    check_distance = 2.2  # cells
    if isVisualisationOn:
        pygame.draw.circle(screen, (255, 71, 71), (screen_width / 2, screen_height / 2),
                           cell_size * (check_distance - 1), 2)
    for i in range(0, grid_size):
        for j in range(0, grid_size):
            if math.sqrt(math.pow(player_cellI - i, 2) + math.pow(player_cellJ - j, 2)) < check_distance:
                x, y = convertPosToCameraPos((j * cell_size, i * cell_size))
                # print((j * cell_size, i * cell_size)," => ",(x, y))
                if world_data[i][j] != 0:
                    colliding_array.append((i, j))
                    if isVisualisationOn:
                        pygame.draw.rect(screen, (255, 0, 0), (x + 2, y + 2, cell_size - 4, cell_size - 4), 5)
                        pygame.draw.line(screen, (171, 0, 0), (screen_width / 2, screen_height / 2),
                                         (x + cell_size / 2, y + cell_size / 2), 5)
                        pygame.draw.circle(screen, (171, 0, 0), (x + cell_size / 2, y + cell_size / 2), 5, 5)

    for pos in colliding_array:
        i = pos[0]
        j = pos[1]

        # on screen position
        block_size = tile_size
        x1, y1 = (j * block_size, i * block_size)

        player_collider = player_collider_size * tile_size

        x2 = playerX - player_collider / 2
        y2 = playerY - player_collider / 2

        new_pos_x = (x2 + player_dirX * player_speed, y2)
        new_pos_y = (x2, y2 + player_dirY * player_speed)

        if isCollidingX == False and checkCollision((x1, y1), block_size, new_pos_x, player_collider) == True:
            isCollidingX = True
            if player_dirX == 1:
                forsetX = -(x2 + player_collider - x1 + 1)
            if player_dirX == -1:
                forsetX = -(x1 + cell_size - x2 + 1)

        if isCollidingY == False and checkCollision((x1, y1), block_size, new_pos_y, player_collider) == True:
            isCollidingY = True
            if player_dirY == 1:
                forsetY = -(y2 + player_collider - y1 + 1)
            if player_dirY == -1:
                forsetY = -(y1 + cell_size - y2 + 1)

    if isCollidingX == False:
        playerX += player_dirX * player_speed
    else:
        if (forsetX > 0 and forsetX < player_collider / 2):
            playerX += player_dirX * forsetX / player_zoom
    if (isCollidingY == False):
        playerY += player_dirY * player_speed
    else:
        if (forsetY > 0 and forsetY < player_collider / 2):
            playerY += player_dirY * forsetY / player_zoom

    #collide with boosters
    for i in range(0, len(boosters)):
        if i >= len(boosters):
            break
        booster = boosters[i]
        booster_collider_size = booster_collider
        pc = player_collider_size * tile_size
        if checkCollision((booster.x, booster.y), booster_collider_size * tile_size, (playerX - pc, playerY - pc), pc):
            pickUpBooster(booster, booster.x, booster.y)


    if (player_dirX != 0 or player_dirY != 0):
        createPlayerTrail()


def createFireAnimation():
    origin = (playerX, playerY)
    pos = (playerX, playerY - sprite_tank_turret.get_height() / 1.1 / grid_size * player_zoom)
    pos = rotatePosByOrigin(pos, origin, player_turret_angle)
    animations.append(Animation(6, sprites_anim_fire, 0.5, pos, 3, 0))


def createBullet():
    global playerX, playerY, player_id, player_turret_angle, bullets_max, bullets_frequency, bullets

    # get last player bullet
    last_bullet = None
    total_bullets = 0
    for i in range(0, len(bullets)):
        b = bullets[len(bullets) - i - 1]
        if b.player_id == player_id:
            if last_bullet is None:
                last_bullet = b
            total_bullets += 1

    if total_bullets >= bullets_max: return False
    if last_bullet is not None and last_bullet.idx < bullets_frequency: return False

    bullet = Bullet(playerX, playerY, player_turret_angle - 90, sprite_bullet, bullet_lifetime, player_id)
    for i in range(0, 8):
        bullet.move()
    bullets.append(bullet)
    playerResetRegenTimer()
    createFireAnimation()
    playSound(sound_shoot_player, 1)
    return True


def fire():
    global animations
    if createBullet() == False:
        playSound(sound_shoot_player_no_ammo, 0.5)


def moveBullets():
    global bullets, bullet_speed
    bullet_collider = sprite_bullet.get_width()
    for i in range(0, len(bullets)):
        if (i >= len(bullets)):
            break
        bullet = bullets[i]
        bullet.idx += 1
        if bullet.idx > bullet.lifetime:
            bullets.remove(bullet)
            continue

        bullet.move()

        bullet_cellI = int(map(bullet.y, 0, grid_size * tile_size, 0, grid_size))
        bullet_cellJ = int(map(bullet.x, 0, grid_size * tile_size, 0, grid_size))

        colliding_array = []
        check_distance = 0.1
        if isVisualisationOn:
            check_distance = 2
        for i in range(0, grid_size):
            for j in range(0, grid_size):
                if (world_data[i][j] != 0 and math.sqrt(
                        math.pow(bullet_cellI - i, 2) + math.pow(bullet_cellJ - j, 2)) < check_distance):
                    colliding_array.append((i, j))
                    if isVisualisationOn:
                        x, y = convertPosToCameraPos((j * cell_size, i * cell_size))
                        bulletPosOnScreen = convertRealPosToCameraPos((bullet.x, bullet.y))
                        pygame.draw.rect(screen, (3, 224, 0), (x + 2, y + 2, cell_size - 4, cell_size - 4), 5)
                        pygame.draw.line(screen, (3, 201, 0), bulletPosOnScreen, (x + cell_size / 2, y + cell_size / 2),
                                         5)
                        pygame.draw.circle(screen, (3, 201, 0), (x + cell_size / 2, y + cell_size / 2), 5, 5)

        # collision
        isColliding = False
        col = bullet_collider / grid_size * player_zoom
        bullet_pos = (bullet.x - col / 2, bullet.y - col / 2)
        for pos in colliding_array:
            i1 = pos[0]
            j1 = pos[1]

            x1 = j1 * tile_size
            y1 = i1 * tile_size

            if checkCollision((x1, y1), tile_size, bullet_pos, col):
                d1 = min(abs(bullet.y - y1), abs(bullet.y - y1 - tile_size))
                d2 = min(abs(bullet.x - x1), abs(bullet.x - x1 - tile_size))

                if d1 > d2:
                    bullet.angle = 180 - bullet.angle
                    bullet.angle = bullet.angle % 360
                else:
                    bullet.angle = 360 - bullet.angle
                    bullet.angle = bullet.angle
                    pass

                bullet.bounces += 1
                if min(d1, d2) > 10 or bullet.bounces > 3:
                    isColliding = True
                if min(d1, d2) < 4:
                    playSound(sound_bullet_ricochet,1)
                break

        # shoot in bots
        if bullet.player_id == player_id:
            for tank in tanks:
                tc = player_collider_size * tile_size
                bc = bullet_collider / grid_size * player_zoom
                if checkCollision((tank.x - tc / 2, tank.y - tc / 2), tc, (bullet.x - bc / 2, bullet.y - bc / 2), bc):
                    isColliding = True
                    playerKilledTank(tank)
                    break
        # shot in player
        if doBulletsCollideWithPlayer == True and bullet.player_id != player_id:
            pc = player_collider_size * 0.7 * tile_size
            bc = 1
            if checkCollision((playerX - pc / 2, playerY - pc / 2), pc, (bullet.x - bc / 2, bullet.y - bc / 2), bc):
                isColliding = True
                playerReceiveDamage((bullet.x, bullet.y))
        # shot in other bullet
        if doBulletsCollide:
            for i in range(0, len(bullets)):
                b = bullets[i]
                bc = 3
                if b != bullet and b.player_id != bullet.player_id:
                    if checkCollision((b.x - bc / 2, b.y - bc / 2), bc, (bullet.x - bc / 2, bullet.y - bc / 2), bc):
                        isColliding = True
                        bullets.remove(b)
                        animations.append(Animation(6, sprites_death_explosion, 0.5, (bullet.x, bullet.y), 3, 0))
                        playSound(sound_bullet_collide, 0.2)
                        break

        if isColliding:
            bullets.remove(bullet)
            continue


def handleAnimations(isBehindPlayer):
    global animations
    for i in range(0, len(animations)):
        if i >= len(animations):
            break
        anim = animations[i]
        if anim.isBehindPlayer != isBehindPlayer: continue
        anim.delay_cnt += 1
        if anim.delay_cnt >= anim.delay:
            anim.delay_cnt = 0
            anim.idx += 1
        if anim.idx >= anim.n:
            animations.remove(anim)
            continue
        img = anim.sprite_arr[anim.idx]
        img = pygame.transform.scale(img, (img.get_width() * anim.scale, img.get_height() * anim.scale))
        pos = convertRealPosToCameraPos(anim.pos)

        blitRotate(screen, img, pos, (img.get_width() / 2, img.get_height() / 2), anim.angle)
        # screen.blit(img, (pos[0] - , pos[1] - img.get_height() / 2))

        if isVisualisationOn:
            pygame.draw.circle(screen, (255, 0, 0), pos, 5)

def playSound(sound, volume):
    #pygame.mixer.Sound.play(sound).set_volume(volume)
    sound.set_volume(volume)
    sound.play()

# A* path finding algorithm
def heuristic(a, b): return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def astar(array, start, goal):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)];
    close_set = set();
    came_from = {};
    gscore = {start: 0};
    fscore = {start: heuristic(start, goal)};
    oheap = [];
    heapq.heappush(oheap, (fscore[start], start))
    while oheap:
        current = heapq.heappop(oheap)[1]
        dist = math.sqrt(math.pow(current[0] - goal[0], 2) + math.pow(current[1] - goal[1], 2))
        if current == goal or dist < 2:
            data = []
            while current in came_from: data.append(current);current = came_from[current]
            return data
        close_set.add(current)
        for (i, j) in neighbors:
            neighbor = current[0] + i, current[1] + j;
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] == 1: continue
                    #if array[current[0]][current[1] + j] == 1: continue
                    #if array[current[0] + i][current[1]] == 1: continue
                    if i != 0 and j != 0 and (array[current[0]][current[1] + j] == 1) or (array[current[0] + i][current[1]] == 1): continue
                else:
                    continue
            else:
                continue
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0): continue
            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]: came_from[
                neighbor] = current;gscore[neighbor] = tentative_g_score;fscore[
                neighbor] = tentative_g_score + heuristic(neighbor, goal);heapq.heappush(oheap,
                                                                                         (fscore[neighbor], neighbor))
    return False


# =====AI=====

resized_world_map = []


class TankAI:
    def __init__(self, player_id, x, y, speed, sprite_body, sprite_turret, sprite_bullet, sprites_death):
        self.player_id = player_id
        self.x = x
        self.y = y
        self.sprite_body = sprite_body
        self.sprite_turret = sprite_turret
        self.sprite_bullet = sprite_bullet
        self.sprites_death = sprites_death
        self.speed = speed
        self.body_angle = 0
        self.turret_angle = 0
        self.trail_array = []
        self.dirX = 0
        self.dirY = 0
        self.shoot_frequency = 100
        self.shoot_frequency_counter = 0
        self.path = []
        self.path_accuracy = 1
        self.agro_distance = grid_size * tile_size

        self.path_frequency = 50
        self.path_frequency_counter = self.path_frequency
        self.colliding_array = []
        self.i = -1
        self.j = -1
        # self.path_target = 0

    def isPlayerInSight(self):
        # shoot ray
        block_size = tile_size
        distance = math.sqrt(math.pow(self.x - playerX, 2) + math.pow(self.y - playerY, 2))

        if distance > bullet_lifetime_ai * bullet_speed:
            return False

        frequency = 30  # times

        speed = distance / frequency
        # angle
        x1, y1 = convertRealPosToCameraPos((self.x, self.y))
        x2, y2 = (screen_width / 2, screen_height / 2)
        angle = (math.degrees(math.atan2(y2 - y1, x2 - x1))) % 360

        check_poses = []
        for i in range(0, frequency):
            check_poses.append(getNextPosByAngle(self.x, self.y, angle, speed * i))

        for i1 in range(0, grid_size):
            for j1 in range(0, grid_size):
                if world_data[i1][j1] != 0:
                    for check_pos in check_poses:
                        # pygame.draw.circle(screen, (100, 0, 255), convertRealPosToCameraPos(check_pos), 10)
                        # check if collides
                        isColliding = False

                        x = j1 * block_size
                        y = i1 * block_size
                        x1 = x
                        y1 = y
                        x2 = x + block_size
                        y2 = y + block_size

                        x0 = check_pos[0]
                        y0 = check_pos[1]
                        if (x0 > x1 and x0 < x2 and y0 > y1 and y0 < y2):
                            # pygame.draw.rect(screen, (255, 100, 9), (convertRealPosToCameraPos((x1, y1))[0], convertRealPosToCameraPos((x1, y1))[1],
                            # block_size * grid_size / player_zoom, block_size * grid_size / player_zoom), 5)
                            return False
        return True

    def handleShoot(self):
        self.shoot_frequency_counter += 1
        if self.shoot_frequency_counter > self.shoot_frequency:
            self.shoot_frequency_counter = 0
            if self.isPlayerInSight():
                self.shoot()
            else:
                self.shoot_frequency_counter = self.shoot_frequency * 0.9

    def shoot(self):
        angle = self.turret_angle
        bullet = Bullet(self.x, self.y, angle - 90, self.sprite_bullet, bullet_lifetime_ai, self.player_id)
        for i in range(0, 8):
            bullet.move()
        bullets.append(bullet)

        # animation
        origin = (self.x, self.y)
        pos = (self.x, self.y - self.sprite_turret.get_height() / 1.1 / grid_size * player_zoom)
        pos = rotatePosByOrigin(pos, origin, self.turret_angle)
        animations.append(Animation(6, sprites_anim_fire, 0.5, pos, 3, 0))
        playSound(sound_shoot_player, 0.1)

    def destroy(self):
        global tanks
        tanks.remove(self)

        # animation
        # print(self.sprites_death[0].get_width(), self.sprite_body.get_width())
        animations.append(Animation(3, self.sprites_death, 0.6, (self.x, self.y), 4, self.body_angle))
        animations.append(Animation(6, sprites_death_explosion, 1, (self.x, self.y), 3, random.randint(0, 360)))

    def generatePath(self):
        # if dist to player not big
        dist = math.sqrt(math.pow(self.x - playerX, 2) + math.pow(self.y - playerY, 2))
        if dist > self.agro_distance:
            return

        global resized_world_map
        grid = resized_world_map
        if len(grid) < 2:
            for i in range(0, grid_size):
                line = []
                for j in range(0, grid_size):
                    x = world_data[i][j]
                    if x != 0: x = 1
                    line.append(x)
                grid.append(line)
            grid = np.array(grid)

        resized_world_map = grid
        startPos = (int(map(self.y, 0, grid_size * tile_size, 0, grid_size * self.path_accuracy)),
                    int(map(self.x, 0, grid_size * tile_size, 0, grid_size * self.path_accuracy)))
        endPos = (int(map(playerY, 0, grid_size * tile_size, 0, grid_size * self.path_accuracy)),
                  int(map(playerX, 0, grid_size * tile_size, 0, grid_size * self.path_accuracy)))

        new_path = astar(grid, startPos, endPos)
        if new_path != False:
            self.path = new_path[::-1]

        # reformat path
        for i in range(0, len(self.path)):
            if i >= len(self.path): break
            pos2 = self.path[i]
            pos = (int(map(pos2[1], 0, grid_size * self.path_accuracy, 0, grid_size) + 0.1),
                   int((map(pos2[0], 0, grid_size * self.path_accuracy, 0, grid_size) + 0.1)))
            self.path[i] = pos
        # remove dublicates
        # self.path = list(dict.fromkeys(self.path))

    def drawTrail(self):
        global player_trail, player_trail_lifetime

        for i in range(0, len(self.trail_array)):
            if i >= len(self.trail_array):
                break
            trail = self.trail_array[i]
            trail.idx += 1
            if trail.idx > player_trail_lifetime:
                self.trail_array.remove(trail)
                continue

            max_size = self.sprite_body.get_width() / grid_size * player_zoom / 2
            i = player_trail_lifetime - trail.idx
            if i > player_trail_lifetime / 2:
                size = max_size
            else:
                size = map(i, 0, player_trail_lifetime / 2, 0, max_size)

            img = pygame.transform.scale(sprite_step, (size, size))
            blitRotate(screen, img, convertRealPosToCameraPos((trail.x, trail.y)),
                       (img.get_width() / 2, img.get_height() / 2), trail.angle)

            if isVisualisationOn:
                pygame.draw.circle(screen, (255, 0, 0), convertRealPosToCameraPos((trail.x, trail.y)), size / 2)

    def createTrail(self):
        if len(self.trail_array) == 0 or self.trail_array[
            len(self.trail_array) - 1].idx > player_trail_frequency * player_speed / self.speed:
            offset = self.sprite_body.get_width() / 2.5 / grid_size * player_zoom
            randomness = 0.5

            x1, y1 = rotatePosByOrigin((self.x + offset + random.uniform(-randomness, randomness),
                                        self.y + offset + random.uniform(-randomness, randomness)), (self.x, self.y),
                                       self.body_angle)
            x2, y2 = rotatePosByOrigin((self.x - offset + random.uniform(-randomness, randomness),
                                        self.y + offset + random.uniform(-randomness, randomness)), (self.x, self.y),
                                       self.body_angle)

            self.trail_array.append(PlayerTrail(x1, y1, random.randint(0, 360), self.player_id))
            self.trail_array.append(PlayerTrail(x2, y2, random.randint(0, 360), self.player_id))

    def move(self):
        # find path
        self.path_frequency_counter += 1
        if self.path_frequency_counter > self.path_frequency:
            self.generatePath()
            self.path_frequency_counter = 0

        if isVisualisationOn:
            if len(self.path) >= 2:
                p0 = None
                for i in range(1, len(self.path)):
                    p1 = self.path[i]
                    p1 = convertRealPosToCameraPos((int(map(p1[0], 0, grid_size, 0, grid_size * tile_size)),
                                                    int(map(p1[1], 0, grid_size, 0, grid_size * tile_size))))
                    p1 = (p1[0] + cell_size / 2, p1[1] + cell_size / 2)
                    if p0: pygame.draw.line(screen, (3, 127, 252), p0, p1, 5)
                    pygame.draw.circle(screen, (3, 127, 252), p1, 5)
                    p0 = p1

        if len(self.path) > 1:
            pos = self.path[1]
            pos = (int(map(pos[0], 0, grid_size, 0, grid_size * tile_size) + 0.1),
                   int(map(pos[1], 0, grid_size, 0, grid_size * tile_size) + 0.1))
            pos = (pos[0] + tile_size / 2, pos[1] + tile_size / 2)

            if isVisualisationOn:
                pygame.draw.circle(screen, (52, 153, 235), convertRealPosToCameraPos(pos), 10)

            if abs(self.x - pos[0]) <= self.speed:
                self.x = pos[0]
                self.dirX = 0
            elif self.x < pos[0]:
                self.dirX = 1
            elif self.x > pos[0]:
                self.dirX = -1

            if abs(self.y - pos[1]) <= self.speed:
                self.y = pos[1]
                self.dirY = 0
            elif self.y < pos[1]:
                self.dirY = 1
            elif self.y > pos[1]:
                self.dirY = -1

            if self.x == pos[0] and self.y == pos[1]:
                self.path.remove(self.path[0])
        else:
            # self.path_frequency_counter = self.path_frequency/2
            pass

        isCollidingX = False
        isCollidingY = False
        forsetX = 0
        forsetY = 0

        cellI = int(map(self.y, 0, grid_size * tile_size, 0, grid_size))
        cellJ = int(map(self.x, 0, grid_size * tile_size, 0, grid_size))

        check_distance = 2.2  # cells
        if cellI != self.i or cellJ != self.j:
            self.i = cellI
            self.j = cellJ
            self.colliding_array = []

            for i in range(0, grid_size):
                for j in range(0, grid_size):
                    if math.sqrt(math.pow(cellI - i, 2) + math.pow(cellJ - j, 2)) < check_distance:

                        if world_data[i][j] != 0:
                            self.colliding_array.append((i, j))

        if isVisualisationOn:
            pygame.draw.circle(screen, (0, 94, 201), convertRealPosToCameraPos((self.x, self.y)),
                               cell_size * (check_distance - 1), 2)

            for pos in self.colliding_array:
                x, y = convertPosToCameraPos((pos[1] * cell_size, pos[0] * cell_size))
                pygame.draw.rect(screen, (0, 107, 230), (x + 2, y + 2, cell_size - 4, cell_size - 4), 5)
                pygame.draw.line(screen, (0, 94, 201), convertRealPosToCameraPos((self.x, self.y)),
                                 (x + cell_size / 2, y + cell_size / 2), 1)
                pygame.draw.circle(screen, (0, 94, 201), (x + cell_size / 2, y + cell_size / 2), 5, 5)

        for pos in self.colliding_array:
            i = pos[0]
            j = pos[1]

            # on screen position
            block_size = tile_size
            x1, y1 = (j * block_size, i * block_size)

            tank_collider = player_collider_size * tile_size

            x2 = self.x - tank_collider / 2
            y2 = self.y - tank_collider / 2

            if isVisualisationOn:
                pos = convertRealPosToCameraPos((x2, y2))
                pos2 = convertRealPosToCameraPos((x2 + tank_collider, y2 + tank_collider))
                tk = tank_collider * grid_size / player_zoom
                pygame.draw.rect(screen, (0, 209, 224), (pos[0], pos[1], pos2[0] - pos[0], pos2[1] - pos[1]), 2)

                # pos = convertRealPosToCameraPos((x1, y1))
                # pos2 = convertRealPosToCameraPos((x1 + block_size, y1 + block_size))
                # pygame.draw.rect(screen, (0, 209, 224), (pos[0], pos[1], pos2[0] - pos[0], pos2[1] - pos[1]), 2)

            new_tank_pos_x = (x2 + self.dirX * self.speed, y2)
            new_tank_pos_y = (x2, y2 + self.dirY * self.speed)

            # print((x1, y1), " and ", (x2, y2))

            if isCollidingX == False and checkCollision((x1, y1), block_size, new_tank_pos_x, tank_collider) == True:
                isCollidingX = True
                if self.dirX == 1:
                    forsetX = -(x2 + tank_collider - x1 + 1)
                if self.dirX == -1:
                    forsetX = -(x1 + cell_size - x2 + 1)

                if isVisualisationOn:
                    pos = convertRealPosToCameraPos((x1 + 3, y1 + 3))
                    pygame.draw.rect(screen, (255, 240, 23), (pos[0] - 12, pos[1] - 12, cell_size - 6, cell_size - 6),
                                     7)

            if isCollidingY == False and checkCollision((x1, y1), block_size, new_tank_pos_y, tank_collider) == True:
                isCollidingY = True
                if self.dirY == 1:
                    forsetY = -(y2 + tank_collider - y1 + 1)
                if self.dirY == -1:
                    forsetY = -(y1 + cell_size - y2 + 1)

                if isVisualisationOn:
                    pos = convertRealPosToCameraPos((x1 + 3, y1 + 3))
                    pygame.draw.rect(screen, (31, 255, 23), (pos[0] - 12, pos[1] - 12, cell_size - 6, cell_size - 6), 7)

        if (isCollidingX == False):
            self.x += self.dirX * self.speed
        else:
            if (forsetX > 0 and forsetX < tank_collider / 2):
                self.x += self.dirX * forsetX / player_zoom
        if (isCollidingY == False):
            self.y += self.dirY * self.speed
        else:
            if (forsetY > 0 and forsetY < tank_collider / 2):
                self.y += self.dirY * forsetY / player_zoom

        if self.dirX != 0 or self.dirY != 0:
            self.createTrail()


player_ai_posI = -1
player_ai_posJ = -1


def moveTanks():
    for tank in tanks:
        tank.move()
        if isGameOver == False:
            tank.handleShoot()


def getRotationDirection(x, y):
    dir = 0
    if x < y:
        y -= x
        x = 0
        d1 = y
        d2 = 360 - y
        if d1 >= d2:
            dir = -1
        else:
            dir = 1
    elif x > y:
        x -= y
        y = 0
        d1 = x
        d2 = 360 - x
        if (d1 >= d2):
            dir = 1
        else:
            dir = -1
    return dir


# methods for ai same for player
def handleAIBodyRotateAngle(tank):
    to_angle = tank.body_angle
    x = tank.dirX
    y = tank.dirY
    if x == 0 and y == 0:
        to_angle = tank.body_angle
    elif x == 1 and y == 0:
        to_angle = 90
    elif x == -1 and y == 0:
        to_angle = 270
    elif x == 0 and y == 1:
        to_angle = 180
    elif x == 0 and y == -1:
        to_angle = 0

    elif x == 1 and y == 1:
        to_angle = 135
    elif x == 1 and y == -1:
        to_angle = 45
    elif x == -1 and y == 1:
        to_angle = 225
    elif x == -1 and y == -1:
        to_angle = 315

    x = tank.body_angle
    y = to_angle
    dir = getRotationDirection(x, y)
    tank.body_angle += dir * player_body_angle_speed
    tank.body_angle = tank.body_angle % 360


def handleAITurretRotateAngle(tank):
    to_angle = tank.turret_angle
    global playerX, playerY

    x1, y1 = convertRealPosToCameraPos((tank.x, tank.y))
    x2, y2 = (screen_width / 2, screen_height / 2)

    if isVisualisationOn:
        pygame.draw.line(screen, (0, 255, 0), (x1, y1), (x2, y2), 2)
    to_angle = math.degrees(math.atan2(y2 - y1, x2 - x1)) + 90

    speed = 1
    to_angle = to_angle % 360
    if (abs(tank.turret_angle - to_angle) > speed):
        tank.turret_angle += getRotationDirection(tank.turret_angle, to_angle) * speed
    else:
        tank.turret_angle = to_angle
    tank.turret_angle = tank.turret_angle % 360

def generateBotSpeed():
    speed = player_speed * random.uniform(0.2, 0.8) + player_score / player_score_for_ai_normal * 0.0015
    if world_map_id == 3:
        speed += 0.3 #maze
    return speed

def generateBotShootFrequency():
    tanks_killed = player_score / player_score_for_ai_normal
    max_freq = 100
    min_freq = 70
    freq = int(map(tanks_killed, 0, 20, max_freq, min_freq) * random.uniform(0.9, 1.1))
    if freq < min_freq: freq = min_freq
    #print(freq)
    return freq

def drawTanks():
    for i in range(0, len(tanks)):
        if (i >= len(tanks)):
            break
        tank = tanks[i]

        pos = convertRealPosToCameraPos((tank.x, tank.y))
        # pygame.draw.circle(screen, (0, 0, 255), pos, sprite_tank_body.get_width()/2)

        #tank.drawTrail()

        handleAIBodyRotateAngle(tank)
        blitRotate(screen, tank.sprite_body, pos,
                   (tank.sprite_body.get_width() / 2, tank.sprite_body.get_height() / 2), tank.body_angle)

        handleAITurretRotateAngle(tank)
        blitRotate(screen, tank.sprite_turret, pos,
                   (tank.sprite_turret.get_width() / 2, tank.sprite_turret.get_height() - 5), tank.turret_angle)


def spawnAi(i, j):
    y = (i + 0.5) * tile_size
    x = (j + 0.5) * tile_size

    tank = TankAI(player_id + 1 + len(tanks), x, y,
                  generateBotSpeed(),
                  sprite_tank_ai_body, sprite_tank_ai_turret, sprite_ai_bullet, sprites_death_blue)
    tank.shoot_frequency = generateBotShootFrequency()
    tanks.append(tank)


def spawnAiRandom():
    i = -1
    j = -1
    radius_min_from_player = 8
    radius_max_from_player = grid_size
    radius_from_other_tanks = 3
    while True:
        i = random.randint(1, grid_size - 1)
        j = random.randint(1, grid_size - 1)
        if world_data[i][j] != 0: continue
        # check player
        playerI = int(map(playerY, 0, grid_size * tile_size, 0, grid_size))
        playerJ = int(map(playerX, 0, grid_size * tile_size, 0, grid_size))
        dist = math.sqrt(math.pow(playerI - i, 2) + math.pow(playerJ - j, 2))
        if dist < radius_min_from_player or dist > radius_max_from_player: continue
        # check all other tanks
        for tank in tanks:
            tankI = int(map(tank.i, 0, grid_size * tile_size, 0, grid_size))
            tankJ = int(map(tank.j, 0, grid_size * tile_size, 0, grid_size))
            dist = math.sqrt(math.pow(tankI - i, 2) + math.pow(tankJ - j, 2))
            if dist < radius_from_other_tanks: continue
        # coordinates are good
        break
    spawnAi(i, j)

def spawnAis():
    global playerX, playerY, tile_size
    for i in range(0, 5):
        spawnAiRandom()


def restartGame():
    global tanks, world_data, resized_world_map, isGameOver, run, boosters, player_ultimate

    tanks = []
    boosters = []
    player_ultimate = 0
    generateWorld()
    resized_world_map = []
    spawnPlayer()
    spawnAis()
    isGameOver = False
    run = True


def gameOver():
    global sprite_gameOver, sprite_gameOver_bg, font_gameOver, player_score
    screen.blit(sprite_gameOver_bg, (0, 0))
    screen.blit(sprite_gameOver, (
        screen_width / 2 - sprite_gameOver.get_width() / 2, screen_height / 2 - sprite_gameOver.get_height() / 2))
    text = font_gameOver.render(str(int(player_score)), True, (0, 255, 0))
    screen.blit(text, (screen_width / 2 + 50, screen_height / 2 - text.get_height() / 2 + 100))
    pygame.display.update()
    playSound(sound_gameOver, 1)
    time.sleep(1.5)
    restartGame()


restartGame()
flag_bullet = 0
run = True
flag_ultimate = 0
flag_esc = 0
clock = pygame.time.Clock()
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and isGameOver == False:
            if flag_bullet == 0:
                fire()
                flag_bullet = 1
        if event.type == pygame.MOUSEBUTTONUP:
            if flag_bullet == 1:
                flag_bullet = 0

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_w] and keys[pygame.K_s]) or (keys[pygame.K_w] == False and keys[pygame.K_s] == False):
        player_dirY = 0
    else:
        if keys[pygame.K_w]:
            player_dirY = -1
        elif keys[pygame.K_s]:
            player_dirY = 1

    if (keys[pygame.K_a] and keys[pygame.K_d]) or (keys[pygame.K_a] == False and keys[pygame.K_d] == False):
        player_dirX = 0
    else:
        if keys[pygame.K_a]:
            player_dirX = -1
        elif keys[pygame.K_d]:
            player_dirX = 1

    if flag_ultimate == 0 and keys[pygame.K_SPACE]:
        useUltimate()
        flag_ultimate = 1
    elif flag_ultimate == 1 and not keys[pygame.K_SPACE]:
        flag_ultimate = 0

    if (keys[pygame.K_r]):
        isVisualisationOn = True
    else:
        isVisualisationOn = False


    if flag_esc== 0 and keys[pygame.K_ESCAPE]:
        restartGame()
        flag_esc = 1
    elif flag_esc == 1 and not keys[pygame.K_ESCAPE]:
        flag_esc = 0

    drawWorld()
    movePlayer()
    moveTanks()
    moveBullets()
    playerHandleRegen()

    handleAnimations(True)
    drawPlayerTrail()
    drawArrows()
    drawBoosters()
    drawTanks()
    drawPlayer()
    drawBullets()
    drawPlayerScore()
    drawPlayerUltimate()
    handleAnimations(False)
    #useUltimate()
    pygame.display.update()

    # check gameOver
    if isGameOver:
        # print(round(time.time() - player_death_time))
        if round(time.time() - player_death_time) > player_death_cooldown:
            run = False
            gameOver()

    if keys[pygame.K_q]:
        pygame.quit()
        break

pygame.quit()
