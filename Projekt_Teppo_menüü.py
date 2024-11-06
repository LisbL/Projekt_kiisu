import pygame
import os
from os.path import join
import button

pygame.init()

screen_width = 960
screen_height = 540

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Teppo reis koju")

#define game variables
start_game = False
#background image
BG = pygame.image.load("materjalid/dark forest/Preview.png").convert()
BG = pygame.transform.scale(BG, (960,540))
#button images
start_img = pygame.image.load("pildid/Nupud/start_btn.png").convert_alpha()
exit_img = pygame.image.load("pildid/Nupud/exit_btn.png").convert_alpha()

#create buttons
start_button = button.Button(screen_height // 2 + 205, screen_height // 2 + 30, start_img)
exit_button = button.Button(screen_height // 2 + 205, screen_height // 2 + 180, exit_img)

run = True
while run:

    if start_game == False:
        screen.blit(BG, (0,0))
        if start_button.draw(screen):
            start_game = True
        if exit_button.draw(screen):
            run = False
    else:
        pass
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()