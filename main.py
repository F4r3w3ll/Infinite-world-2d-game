import pygame
import sys
import random
import noise
from pygame import mixer 

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
mixer.init()

screen = pygame.display.set_mode((600,400))
clock = pygame.time.Clock()


true_camera_scroll = [0,0]

#background_objects = [[0.25,[50,100,40,800]],[0.35,[270,200,100,800]],[0.35,[400,100,40,800]],[0.25,[550,50,50,800]]]



def get_image(sheet, frame, width, height, scale, color):

    image = pygame.Surface((width, height))
    image.blit(sheet, (0, 0), (frame * width, 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color)

    return image


class Player:
    def __init__(self):
        self.walk_sound = pygame.mixer.Sound("sounds/walk.mp3")
        self.jump_sound = pygame.mixer.Sound("sounds/jumping.mp3")
        self.coin_sound = pygame.mixer.Sound("sounds/coin.mp3")
        self.jump_sound.set_volume(0.5)
        self.walk_sound.set_volume(0.1)
        self.coin_sound.set_volume(0.01)
        colorkey = (47, 232, 45)
        sprite = pygame.image.load("player/moving2.png").convert_alpha()
        sprite_left = pygame.image.load("player/moving_left.png").convert_alpha()
        sprite_jump = pygame.image.load("player/jumping3.png").convert_alpha()
        self.p = pygame.image.load("player/standing.png").convert_alpha()
        self.p.set_colorkey((47,232,45))
        self.rect = self.p.get_rect()
        self.rect.x = 200
        self.rect.y = 120
        self.jump_h = 3
        self.y_vel = self.jump_h
        self.y_gravity = 0.5
        self.on_ground = False
        self.jumping = False
        self.move = [0,0]
        self.cur_right = 0
        self.cur_left = 0
        self.cur_jump = 0
        self.walk_r = 0
        self.walk_l = 0
        self.jump_timer = 0
        self.walk_right = [get_image(sprite, i, 16, 32, 1, colorkey) for i in range(8)]
        self.walk_left = [get_image(sprite_left, i, 16, 32, 1, colorkey) for i in range(8)]
        self.jump_frame = [get_image(sprite_jump, i, 16, 32, 1, colorkey) for i in range(8)]
        self.grass_t = 0


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
            if self.rect.colliderect(tile):
                collisions.append(tile)
                
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
    

    def coin_coll(self,coins):
        for coin in coins:
            if self.rect.colliderect(coin):
                self.coin_sound.play()
                coin.x = -100
                coin.y = -100



    def update_right(self):

        self.walk_r += 1
        if self.walk_r % 4 == 0:
            self.cur_right += 1
        if self.cur_right == 8:
            self.cur_right = 0


    def update_left(self):

        self.walk_l += 1
        if self.walk_l % 4 == 0:
            self.cur_left += 1
        if self.cur_left == 8:
            self.cur_left = 0


    def update_jump(self):

        self.jump_timer += 1
        if self.jump_timer % 8 == 0:
            self.cur_jump += 1
        if self.cur_jump == 8:
            self.cur_jump = 0


    def walking_sound(self):
        if self.move[0] != 0 and self.on_ground == True:
            if self.grass_t == 0:
                self.walk_sound.play()
                self.grass_t = 20

        
    def render(self):
        if right:
            w_r = self.walk_right[self.cur_right]
            self.update_right()
            player.walking_sound()
            screen.blit(w_r, (self.rect.x-camera_scroll[0], self.rect.y-camera_scroll[1]))
        elif left:
            w_l = self.walk_left[self.cur_left]
            self.update_left()
            player.walking_sound()
            screen.blit(w_l, (self.rect.x-camera_scroll[0], self.rect.y-camera_scroll[1]))
        elif self.jumping:
            j = self.jump_frame[self.cur_jump]
            self.update_jump()
            screen.blit(j, (self.rect.x-camera_scroll[0], self.rect.y-camera_scroll[1]))
        else:
            screen.blit(self.p, (self.rect.x-camera_scroll[0], self.rect.y-camera_scroll[1]))
    

class World:
    def __init__(self):

        color = (252,223,205)
        self.path = "map.txt"

        self.grass = pygame.image.load("images/grass.png").convert_alpha()
        self.grass_img = pygame.transform.scale(self.grass, (32, 32))
        self.dirt = pygame.image.load("images/dirt.png").convert_alpha()
        self.dirt_img = pygame.transform.scale(self.dirt, (32, 32))
        self.plant1 = pygame.image.load("images/plant1.png").convert_alpha()
        self.plant1_img = pygame.transform.scale(self.plant1,(32,32))
        self.plant1_img.set_colorkey(color)
        self.plant2 = pygame.image.load("images/plant2.png").convert_alpha()
        self.plant2_img = pygame.transform.scale(self.plant2,(32,32))
        self.plant2_img.set_colorkey((34,177,76))
        self.plant3 = pygame.image.load("images/plant3.png").convert_alpha()
        self.plant3_img = pygame.transform.scale(self.plant3,(32,32))
        self.plant3_img.set_colorkey(color)


        self.tile = []
        self.chunk_size = 8
        self.chunk_data = []
        self.game_map = {}
        self.target_x = 0
        self.target_y = 0
        self.target_chunk = 0


        self.coin_sprite = []
        self.coin_pos = 0
        self.cur_coin_pos = 0
        g_coin = pygame.image.load("images/coins/gold_coin.png").convert()
        self.g_coin_sprite = [get_image(g_coin, i, 16, 16, 1, (0,0,0)) for i in range(4)]
        s_coin = pygame.image.load("images/coins/silver_coin.png").convert()
        self.s_coin_sprite = [get_image(s_coin, i, 16, 16, 1, (0,0,0)) for i in range(4)]
        r_coin = pygame.image.load("images/coins/ruby_coin.png").convert()
        self.r_coin_sprite = [get_image(r_coin, i, 16, 16, 1, (0,0,0)) for i in range(4)]
        self.coin_tile = []



        self.tile_index = {1:self.dirt_img,
                           2:self.grass_img,
                           3:self.plant1_img,
                           4:self.plant2_img,
                           5:self.plant3_img}
        self.tiles = []
        self.g_clouds = False

        self.clouds = []
        for i in range(1, 6):
            cloud = pygame.image.load(f"clouds/cloud{i}.png")
            cloud.set_colorkey((34, 177, 76))
            self.clouds.append(cloud)


    def update_coin(self):
        self.coin_pos += 0.5
        if self.coin_pos % 1750 == 0:
            self.cur_coin_pos += 1
        if self.cur_coin_pos == 4:
            self.cur_coin_pos = 0


    def generate_chunk(self,x,y):
        self.chunk_data = []
        for y_pos in range(self.chunk_size):
            for x_pos in range(self.chunk_size):
                target_x = x * self.chunk_size + x_pos
                target_y = y * self.chunk_size + y_pos
                height = int(noise.pnoise1(target_x*0.1, repeat=999999999)*5)
                tile_type = 0 #nothing
                if target_y > 8-height:
                    tile_type = 1 #dirt
                elif target_y == 8-height:
                    tile_type = 2 #grass
                elif target_y == 8-height-1:
                    number = random.randint(1,9)
                    if number%3 == 0:#plants
                        type = random.randint(1,3)
                        if type == 1:
                            tile_type = 3
                        if type == 2:
                            tile_type = 4
                        if type == 3:
                            tile_type = 5
                    if number == 9: #coin
                        type = random.randint(1,3)
                        if type == 1:
                            tile_type = 6
                        if type == 2:
                            tile_type = 7
                        if type == 3:
                            tile_type = 8
                        target_x = x * self.chunk_size + x_pos +0.25
                        target_y = 8-height-0.6 
                        self.coin_tile.append(pygame.Rect(target_x*32,target_y*32,16,16))
                if tile_type != 0:
                    self.chunk_data.append([[target_x,target_y],tile_type])

        return self.chunk_data
    
    def chunk_location(self):
        self.tiles = []
        for y in range(3):
            for x in range(4):
                self.target_x = x - 1 + int(round(camera_scroll[0]/(self.chunk_size*32)))
                self.target_y = y - 1 + int(round(camera_scroll[1]/(self.chunk_size*32)))
                self.target_chunk = str(self.target_x) + ";" + str(self.target_y) 
                if self.target_chunk not in self.game_map:
                    self.game_map[self.target_chunk] = self.generate_chunk(self.target_x,self.target_y)
                    self.g_clouds = True
                for t in self.game_map[self.target_chunk]:
                    if t[1] == 6:
                        image = self.g_coin_sprite[self.cur_coin_pos]
                    elif t[1] == 7:
                        image = self.s_coin_sprite[self.cur_coin_pos]
                    elif t[1] == 8:
                        image = self.r_coin_sprite[self.cur_coin_pos]
                    else:
                        image = self.tile_index[t[1]]
                    screen.blit(image,(t[0][0]*32-camera_scroll[0],t[0][1]*32-camera_scroll[1]))
                    self.update_coin()
                    if t[1] in [1,2]:
                        self.tiles.append(pygame.Rect(t[0][0]*32,t[0][1]*32,32,32))
    

    def moving_clouds(self):
        # print(self.target_x)
        # if self.g_clouds:
        for i in range (len(clouds)):
            if random.randint(1,3) == 2:
                screen.blit(clouds[i],((self.target_x + 70 * i ) - camera_scroll[0],(self.target_y + 50 + random.randint(1,50)) - camera_scroll[1]))
            else:
                screen.blit(clouds[i],((self.target_x + 150 * i ) - camera_scroll[0],(self.target_y + 50 + random.randint(1,50)) - camera_scroll[1]))
        # self.g_clouds = False



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


pygame.mixer.music.load("sounds\music\song.mp3")
pygame.mixer.music.play(-1,0,500)
pygame.mixer.music.set_volume(0.05)

left = False
right = False

world = World()
player = Player()


while True:

    if player.grass_t > 0:
        player.grass_t -= 1

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
                    player.jump_sound.play()
                    player.jumping = True
            if event.key == pygame.K_d:
                right = True
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_p:
                pygame.mixer.music.fadeout(500)
            if event.key == pygame.K_o:
                pygame.mixer.music.play(-1,0,500)
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


    screen.fill((0,250,255))
    world.chunk_location()

    player.jump()
    player.collision_check(world.tiles)
    player.move_p(world.tiles)
    player.render()
    player.coin_coll(world.coin_tile)
    pygame.display.update()
    clock.tick(60)
