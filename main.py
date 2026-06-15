import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((600,400))
clock = pygame.time.Clock()
move = [0,0]

scroll = [0,0]
jumping = False

player = pygame.image.load("standing.png")
player = pygame.transform.scale(player, (16, 26))
player_rect = player.get_rect()
player_rect.x = 200
player_rect.y = 20
grass = pygame.image.load("grass.png")
grass_img = pygame.transform.scale(grass, (32, 32))
dirt = pygame.image.load("dirt.png")
dirt_img = pygame.transform.scale(dirt, (32, 32))

path = "map.txt"

jump_h = 5
y_vel = jump_h
gravity = 0.5
on_ground = False

def gravity_force():
    global jumping, on_ground
    if on_ground == False:
        move[1] += 0.5


def jump():
    global jumping,y_vel,jump_h,gravity, on_ground
    if jumping == True:
        on_ground = False
        move[1] -= y_vel
        y_vel -= gravity
        if y_vel == -jump_h:
            y_vel = jump_h
            move[1] = 0
            jumping = False



def generate_world():
    tiles = []
    with open(path,"r") as f:
        file = f.readlines()
    row = 0
    for line in file:
        col = 0
        for tile in line:
            if tile == '1':
                img_rect = dirt.get_rect()
                img_rect.x = col * 32 #- scroll[0]
                img_rect.y = row * 32 #- scroll[1]
                til = (dirt_img,img_rect)
                tiles.append(til)
            if tile == '2':
                img_rect = grass.get_rect()
                img_rect.x = col * 32 #- scroll[0]
                img_rect.y = row * 32 #- scroll[1]
                til = (grass_img, img_rect)
                tiles.append(til)
            col += 1
        row += 1
    return tiles


def draw_world(tiles):
    for tile in tiles:
        screen.blit(tile[0],tile[1])

chunk_size = 8
def generate_chunk(x,y):
    chunk_data = []
    for y_pos in range(chunk_size):
        for x_pos in range(chunk_size):
            trage_x = x * chunk_size + x_pos
            trage_y = y * chunk_size + y_pos
            tile_type = 0 #nothing
            if tatget_y > 10:
                tile_type = 2 #grass
            elif target_y == 10:
                tile_type = 1 #dirt
            if tile_type != 0:
                chunk_data.append([[target_x,target_y],tile_type])
    return chank_data

            
def collision_check(player,tiles):
    global on_ground
    collisions = []
    for tile in tiles:
        if player.colliderect(tile[1]):
            collisions.append(tile[1])
            
    return collisions


def move_p(player,movement,tiles):
    global on_ground
    player.x += movement[0]
    col = collision_check(player,tiles)
    for tile in col:
        if movement[0] > 0:
            player.right = tile.left
        if movement[0] < 0:
            player.left = tile.right
    player.y += movement[1]
    col = collision_check(player,tiles)
    for tile in col:
        if movement[1] > 0:
            player.bottom = tile.top
            on_ground = True
        # if movement[1] < 0:
        #     player.top = tile.bottom
    return player

left = False
down = False
up = False
right = False


tiles = generate_world()
while True:

    # scroll[0] += (player_rect.x-scroll[0]-300)/40
    # scroll[1] += (player_rect.y-scroll[1]-200)/40

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            jumping = True
            jump()
            on_ground = False
            jumping = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                right = True
            if event.key == pygame.K_a:
                left = True
            # if event.key == pygame.K_w:
            #     up = True
            # if event.key == pygame.K_s:
            #     down = True
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                right = False
                move[0] = 0
            if event.key == pygame.K_a:
                left = False
                move[0] = 0
            # if event.key == pygame.K_w:
            #     up = False
            #     move[1] = 0
            # if event.key == pygame.K_s:
            #     down = False
            #     move[1] = 0
    if right:
        move[0] = 3
    if left:
        move[0] = -3
    # if up:
    #     move[1] = -3
    # if down:
    #     move[1] = 3



    screen.fill((255,255,255))
    screen.blit(player,(player_rect.x-scroll[0],player_rect.y-scroll[1]))
    draw_world(tiles)
    #tiles = generate_world()
    # print(on_ground)
    move_p(player_rect,move,tiles)  
    gravity_force()
    # print(player_rect.x)
    print(on_ground)
    pygame.display.update()
    clock.tick(60)
