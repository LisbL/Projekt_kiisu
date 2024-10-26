################################################
# Programmeerimine I
# 2024/2025 sügissemester
#
# Projekt
# Teema:
#
#
# Autorid: Lisbeth Lepp ja Martti Virnas
#
# mõningane eeskuju:
#
# Lisakommentaar (nt käivitusjuhend):
#
##################################################

import pygame

pygame.init()

#ristkülik
color = (255,255,255)
position = (0, 0)
rect_color = (41, 219, 130)

#Gravitatsioon
jumping = False

y_grav = 1
jump_height = 20
y_velocity = jump_height

window_w, window_h = 1100, 720
pygame.display.set_caption(title ="Teppo reis koju") 
window = pygame.display.set_mode((window_w,window_h)) 
clock = pygame.time.Clock()

#Player parameetrid
player_width, player_height = 100, 100
player_x, player_y = window_w // 4, window_h // 4
player_speed = 10
player = pygame.draw.rect(window, color, (player_x, player_y, player_width, player_height))


image = pygame.image.load("hampter.jpg")


exit = False
while not exit:
    #Akna kujundamine
    window.fill(color)
    window.blit(image, dest= position)
    #pygame.event.get() # tagastab aktiivsete sündmuste loendi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True


    #Player input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    if keys[pygame.K_SPACE]:
        jumping = True
    
    if jumping:
        player_y -= y_velocity
        y_velocity -= y_grav
        if y_velocity < -jump_height:
            jumping = False
            y_velocity = jump_height


    #Collision detection
    if player_x < 0:
        player_x = 0
    if player_x > window_w - player_width:
        player_x = window_w - player_width
    if player_y < 0:
        player_y = 0
    if player_y > window_h - player_height:
        player_y = window_h - player_height


    # Ristkülik
    pygame.draw.rect(window, rect_color, pygame.Rect(250, 10, 100, 200))

    #värskendus
    pygame.display.update()

    clock.tick(60)


