import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((600,400))
clock = pygame.time.Clock()

scroll = [0,0]

class Player:
    def __init__(self):
        self.p = pygame.image.load("standing.png")
        self.p = pygame.transform.scale(self.p, (16, 26))
        self.rect = self.p.get_rect()
        self.rect.x = 200
        self.rect.y = 220
        self.jump_h = 4
        self.y_vel = self.jump_h
        self.y_gravity = 0.5
        self.on_ground = False
        self.jumping = False
        self.move = [0,0]

    def gravity(self):
        if self.jumping == False and player.on_ground == False:
            self.move[1] += self.y_gravity

    def jump(self):
        if self.jumping:
            self.move[1] -= self.y_vel
            self.y_vel -= self.y_gravity
            if self.y_vel < -self.jump_h:
                self.y_vel = self.jump_h
                self.jumping = False
        else:
            self.gravity()


    def collision_check(self,tiles):
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile[1]):
                collisions.append(tile[1])
                
        return collisions
    
    def move_p(self,tiles):
        self.rect.x += self.move[0]
        col = self.collision_check(tiles)
        for tile in col:
            if self.move[0] > 0:
                self.rect.right = tile.left
            if self.move[0] < 0:
                self.rect.left = tile.right
        self.rect.y += self.move[1]
        col = self.collision_check(tiles)
        for tile in col:
            if self.move[1] > 0:
                self.rect.bottom = tile.top
                self.on_ground = True
                # self.move[1] = 0
            # if movement[1] < 0:
            #     player.top = tile.bottom
        return player
    



class World:
    def __init__(self):
        self.path = "map.txt"
        self.grass = pygame.image.load("grass.png")
        self.grass_img = pygame.transform.scale(self.grass, (32, 32))
        self.dirt = pygame.image.load("dirt.png")
        self.dirt_img = pygame.transform.scale(self.dirt, (32, 32))
        self.tile = []
    def generate_world(self):
        self.tiles = []
        with open(self.path,"r") as f:
            file = f.readlines()
        row = 0
        for line in file:
            col = 0
            for tile in line:
                if tile == '1':
                    img_rect = self.dirt.get_rect()
                    img_rect.x = col * 32 #- scroll[0]
                    img_rect.y = row * 32 #- scroll[1]
                    til = (self.dirt_img,img_rect)
                    self.tiles.append(til)
                if tile == '2':
                    img_rect = self.grass.get_rect()
                    img_rect.x = col * 32 #- scroll[0]
                    img_rect.y = row * 32 #- scroll[1]
                    til = (self.grass_img, img_rect)
                    self.tiles.append(til)
                col += 1
            row += 1
        return self.tiles

    def draw_world(self):
        for tile in self.tiles:
            screen.blit(tile[0],tile[1])



# chunk_size = 8
# def generate_chunk(x,y):
#     chunk_data = []
#     for y_pos in range(chunk_size):
#         for x_pos in range(chunk_size):
#             trage_x = x * chunk_size + x_pos
#             trage_y = y * chunk_size + y_pos
#             tile_type = 0 #nothing
#             if tatget_y > 10:
#                 tile_type = 2 #grass
#             elif target_y == 10:
#                 tile_type = 1 #dirt
#             if tile_type != 0:
#                 chunk_data.append([[target_x,target_y],tile_type])
#     return chank_data


left = False
down = False
up = False
right = False

world = World()
player = Player()
while True:

    # scroll[0] += (player_rect.x-scroll[0]-300)/40
    # scroll[1] += (player_rect.y-scroll[1]-200)/40

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        keys = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if player.on_ground == True:
                    player.jumping = True
            if event.key == pygame.K_d:
                right = True
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                right = False
                player.move[0] = 0
            if event.key == pygame.K_a:
                left = False
                player.move[0] = 0
    if right:
        player.move[0] = 3
    if left:
        player.move[0] = -3


    screen.fill((255,255,255))
    world.generate_world()
    world.draw_world()
    screen.blit(player.p,(player.rect.x,player.rect.y))
    player.collision_check(world.tiles)
    player.jump()
    player.move_p(world.tiles)
    pygame.display.update()
    clock.tick(60)
