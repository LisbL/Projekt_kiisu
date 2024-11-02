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
import os
from os import listdir
from os.path import isfile, join
import spritesheet

pygame.init()

pygame.display.set_caption("Teppo reis koju")

#Globaalsed muutujad
SCREEN_WIDTH, SCREEN_HEIGHT = 320, 180
FPS = 60
PLAYER_SPEED = 5
clock = pygame.time.Clock()
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#BG muutujad
scroll = 0

ground_image = pygame.image.load(join("materjalid", "Taustad", "Free", "Jungle", "4.Ground.png")).convert_alpha()
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

BG_images = []
for i in range(1, 4):
    BG_image = pygame.image.load(join("materjalid", "Taustad", "Free", "Jungle", f"{i}_layer.png" )).convert_alpha()
    BG_images.append(BG_image)
BG_width = BG_images[0].get_width()
#Sprite sheet muutujad
sprite_sheet_image = pygame.image.load(join("materjalid", "Tegelased", "vita.png")).convert_alpha()
#Instance
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
BLACK = (0, 0, 0)

#Funktsioonid
def draw_BG():
    for x in range(5):
        speed = 1
        for i in BG_images:
            WINDOW.blit(i, ((x*BG_width) - scroll * speed, 0))#Pildid laevad üksteise peale
            speed += 0.000000000000000000000000000000000000000000000000001
def draw_ground():
    for x in range(15):
        WINDOW.blit(ground_image, ((x*ground_width) - scroll * 2.2, SCREEN_HEIGHT - ground_height))

#Animation list
animation_list = []
animation_steps = [4, 6, 3, 4, 7]
action = 0
last_update = pygame.time.get_ticks()
animation_cooldown = 75
frame = 0
step_counter = 0

for animation in animation_steps:
    temp_img_list = []
    for _ in range(animation):
        temp_img_list.append(sprite_sheet.get_image(step_counter, 24, 24, 2, BLACK))
        step_counter += 1
    animation_list.append(temp_img_list)

#PÕHIPROGRAMM
#Mängu tsükkel
running = True
while running:
    #Tausta laadimiseks
    draw_BG()
    draw_ground()

    #Update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list[action]):
            frame = 0

    #Display image frame
    WINDOW.blit(animation_list[action][frame], (50,0))


    #Juhul kui tahame mängu sulgeda
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and action > 0:
                action -= 1
                frame = 0
            if event.key == pygame.K_UP and action < len(animation_list) - 1:
                action += 1
                frame = 0

    pygame.display.update()
    clock.tick(FPS)

    #keypresses
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and scroll > 0:
        scroll -= 3
    if key[pygame.K_RIGHT] and scroll < 600:
        scroll += 3

pygame.quit()
