import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()


player = pygame.rect.Rect(45,45,40,40)
lenght = 12
segemnts = []
# player_rect = player.get_rect()
color_p = (0,0,255)
color_f =  (255,0,0)
color_w  =  (0,0,0)

time, time_step = 0,50

get_random_pos = lambda:(random.randint(80,1240),random.randint(80,680))
food = player.copy()
food.center = get_random_pos()
ob1 = pygame.Rect(540,300,280,60)
ob2 = pygame.Rect(640,200,60,280)
wall1 = pygame.Rect(0,0,40,720) 
wall2 = pygame.Rect(0,680,1280,40)
wall3 = pygame.Rect(1240,0,40,720)
wall4 = pygame.Rect(0,0,1280,40)

speed = 20
snake_dir = (0,0)


def player_wall_coll(player,wall):
    global lenght,lenght, right, left, up, down, speed, snake_dir
    speed = 20  
    if player.colliderect(wall):
        player.x = random.randint(41,1240)
        player.y = random.randint(41,680)
        lenght = 1
        snake_dir = (0,0)


def food_walll_col(wall):
    global food
    if food.colliderect(wall):
        food = pygame.Rect(random.randint(80,1240),random.randint(80,680),40,40)     


def player_food_coll():
    global player, food, segemnts, lenght, speed
    if player.colliderect(food):
        food =  pygame.Rect(random.randint(80,1240),random.randint(80,680),40,40)
        lenght += 1
        speed = lenght*(20*0.1)
    return player, food


def player_self_collision():
    global segemnts, lenght, right, left, up ,down, player, speed, snake_dir
    self_eating = player.collidelist([player,segemnts[:-1]])
    if self_eating:
        speed = 20
        lenght = 1
        player.x = random.randint(41,1240)
        player.y = random.randint(41,680)
        snake_dir = (0,0)


right = False
left = False
up = False
down = False


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if not down:
                snake_dir = (0,-speed)
                right = False
                left = False
                up = True
                down = False
        if keys[pygame.K_s]:
            if not up:
                snake_dir = (0,speed)
                right = False
                left = False
                up = True
                down = False
        if keys[pygame.K_d]:
            if not left:
                snake_dir = (speed,0)
                right = True
                left = False
                up = False
                down = False

        if keys[pygame.K_a]:
            if not right:
                snake_dir = (-speed,0)
                right = False
                left = True
                up = False
                down = False
        if keys[pygame.K_ESCAPE]:
            sys.exit()

    time_now = pygame.time.get_ticks()
    if time_now - time > time_step:
        time = time_now

        old_head = player.copy()

        player.move_ip(snake_dir)

        if player.collidelist(segemnts) != -1:
            speed = 20
            lenght = 1
            segemnts.clear()
            player.x = random.randint(41,1240)
            player.y = random.randint(41,680)
            snake_dir = (0,0)
            continue

        segemnts.insert(0, old_head)
        segemnts[:] = segemnts[:lenght]
        time_now = pygame.time.get_ticks()


    screen.fill('white')
    [pygame.draw.rect(screen,"green",segment) for segment in segemnts]

    pygame.draw.rect(screen,color_w,ob2)
    pygame.draw.rect(screen,color_w,ob1)
    pygame.draw.rect(screen,color_w,wall1)
    pygame.draw.rect(screen,color_w,wall2)
    pygame.draw.rect(screen,color_w,wall3)
    pygame.draw.rect(screen,color_w,wall4)
    pygame.draw.rect(screen,color_f,food)
    

    player_wall_coll(player,ob1)
    player_wall_coll(player,ob2)

    player_wall_coll(player,wall1)
    player_wall_coll(player,wall2)
    player_wall_coll(player,wall3)

    player_wall_coll(player,wall4)
    player_food_coll()

    food_walll_col(ob1)
    food_walll_col(ob2)
    food_walll_col(wall1)
    food_walll_col(wall2)
    food_walll_col(wall3)
    food_walll_col(wall4)


    

    

    # if time_now - time > time_step:
    #     time = time_now
    #     player.move_ip(snake_dir)
    #     if player.collidelist(segemnts[:-1]) != -1:
    #         speed = 20
    #         lenght = 1
    #         segemnts.clear()
    #         player.x = random.randint(41,1240)
    #         player.y = random.randint(41,680)
    #         snake_dir = (0,0)
    #     segemnts.append(player.copy())
    #     segemnts = segemnts[-lenght:]
    #     time_now = pygame.time.get_ticks()

    # player_self_collision()
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
