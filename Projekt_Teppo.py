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
BLACK = (0, 0, 0)

#Funktsioonid
def draw_BG():
    for x in range(5):
        speed = 1
        for i in BG_images:
            WINDOW.blit(i, ((x*BG_width) - scroll * speed, 0))#Pildid laevad üksteise peale
            speed += 0.02
def draw_ground():
    for x in range(15):
        WINDOW.blit(ground_image, ((x*ground_width) - scroll * 2.2, SCREEN_HEIGHT - ground_height))
def get_image(sheet, frame, width, height, scale, colour):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame*width), 0, width, height))
    #Suuruse muutmiseks
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colour)
    return image

#Sprite frame
frame_0 = get_image(sprite_sheet_image, 0, 24, 24, 2, BLACK)
frame_1 = get_image(sprite_sheet_image, 1, 24, 24, 2, BLACK)
frame_2 = get_image(sprite_sheet_image, 2, 24, 24, 2, BLACK)
frame_3 = get_image(sprite_sheet_image, 3, 24, 24, 2, BLACK)

#PÕHIPROGRAMM
def main(window):
    global scroll
    #Mängu tsükkel
    running = True
    while running:
        #Tausta laadimiseks
        draw_BG()
        draw_ground()

        #Display image frame
        WINDOW.blit(frame_0, (0,0))
        WINDOW.blit(frame_1, (40,0))
        WINDOW.blit(frame_2, (80,0))
        WINDOW.blit(frame_3, (120,0))
        #Juhul kui tahame mängu sulgeda
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
        clock.tick(FPS)

        #keypresses
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and scroll > 0:
            scroll -= 3
        if key[pygame.K_RIGHT] and scroll < 600:
            scroll += 3

    pygame.quit()


if __name__ == "__main__":
    main(WINDOW)