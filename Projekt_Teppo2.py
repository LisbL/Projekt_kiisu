

import pygame

pygame.init()

screen_width = 800
screen_height = 600
BG = (50, 50, 50)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Teppo reis koju")

#Player action variable
moving_left = False
moving_right = False

x = 400
y = 200
x_rect, y_rect = 150, 400
w_rect, h_rect = 100, 50
rect_colour = (3, 252, 227)
scale = 3

player = pygame.Rect(x_rect, y_rect, w_rect, h_rect)


running = True
while running:

    pygame.draw.rect(screen, rect_colour, player)

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            running = False
            #Pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_ESCAPE:
                running = False
            #Released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
    pygame.display.update()

pygame.quit()