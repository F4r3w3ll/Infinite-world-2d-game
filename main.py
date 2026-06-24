import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((600,400))
clock = pygame.time.Clock()

true_camera_scroll = [0,0]

background_objects = [[0.5,[50,100,40,800]],[0.75,[270,200,100,800]],[0.5,[400,100,40,800]],[0.75,[550,50,50,800]]]

class Player:
    def __init__(self):
        self.p = pygame.image.load("standing.png")
        self.p = pygame.transform.scale(self.p, (16, 32))
        self.p.set_colorkey((47,232,45))
        self.rect = self.p.get_rect()
        self.rect.x = 200
        self.rect.y = 220
        self.jump_h = 3
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
        self.on_ground = False
        for tile in col:
            if self.move[1] > 0:
                self.rect.bottom = tile.top
                self.y_vel = self.jump_h
                self.on_ground = True
            if self.move[1] < 0:
                self.rect.top = tile.bottom
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
                    img_rect = self.dirt_img.get_rect()
                    img_rect.x = (col * 32)
                    img_rect.y = (row * 32)
                    til = (self.dirt_img,img_rect)
                    self.tiles.append(til)
                if tile == '2':
                    img_rect = self.grass_img.get_rect()
                    img_rect.x = (col * 32)
                    img_rect.y = (row * 32)
                    til = (self.grass_img, img_rect)
                    self.tiles.append(til)
                col += 1
            row += 1
        return self.tiles

    def draw_world(self):
        for tile in self.tiles:
            screen.blit(tile[0], (tile[1].x - camera_scroll[0], tile[1].y - camera_scroll[1]))



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
right = False

world = World()
player = Player()
while True:

    true_camera_scroll[0] += (player.rect.x-true_camera_scroll[0]-308)/50
    true_camera_scroll[1] += (player.rect.y-true_camera_scroll[1]-216)/50

    camera_scroll = true_camera_scroll.copy()
    camera_scroll[0] = int(camera_scroll[0])
    camera_scroll[1] = int(camera_scroll[1])

    


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0] - camera_scroll[0]*background_object[0],background_object[1][1] - camera_scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(screen,(14,222,150),obj_rect)
        else:
            pygame.draw.rect(screen,(9,91,85),obj_rect)
    world.generate_world()
    world.draw_world()
    screen.blit(player.p,(player.rect.x-camera_scroll[0],player.rect.y-camera_scroll[1]))
    player.jump()
    player.collision_check(world.tiles)
    player.move_p(world.tiles)
    
    clock.tick(60)
    pygame.display.update()
