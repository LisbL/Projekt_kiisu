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
import random
import math
import os
from os import listdir
from os.path import isfile, join

pygame.init()

pygame.display.set_caption("Teppo reis koju")

#Globaalsed muutujad
BG_COLOR = (174, 242, 255)
SCREEN_WIDTH, SCREEN_HEIGHT = 1100, 700
FPS = 60
PLAYER_SPEED = 5

WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#Funktsioonid
def get_BG(name):
    image = pygame.image.load(join("materjalid", "Taustad", name))
    _, _, width, height = image.get_rect()
    tiles = []

#PÕHIPROGRAMM
def main(window):
    clock = pygame.time.Clock()

    #Mängu tsükkel
    running = True
    while running:

        #Juhul kui tahame mängu sulgeda
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main(WINDOW)