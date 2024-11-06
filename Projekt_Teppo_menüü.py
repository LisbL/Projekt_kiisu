import pygame
import os
from os.path import join

pygame.init()

screen_width = 800
screen_height = int(screen_width*0.8)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Teppo reis koju")

#define game variables
start_game = False

#button images
start_img = pygame.image.load("pildid/Nupud/start_btn.png").convert_alpha()
exit_img = pygame.image.load("pildid/Nupud/exit_btn.png").convert_alpha()

#button class
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

#create buttons
start_button = Button(screen_height // 2 + 75, screen_height // 2 - 10, start_img)
exit_button = Button(screen_height // 2 + 75, screen_height // 2 + 150, exit_img)

run = True
while run:

    if start_game == False:
        screen.fill((60, 60, 88))
        start_button.draw()
        exit_button.draw()
    else:
        pass
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()