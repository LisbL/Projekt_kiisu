import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,600))
screen.fill("darkblue")
pygame.display.set_caption("Teppo Reis Koju")
clock = pygame.time.Clock()
test_font = pygame.font.Font("fondid/Pixeltype.ttf", 75)

test_surface = pygame.image.load("materjalid/Forest/Background.png").convert() # .convert() nii, et pygame suudaks lihtsamini töötada, mäng on kiirem
text_surface = test_font.render("Teppo Reis Koju", False, "White")

black_cat_surface = pygame.image.load("tegelased/Black cat/Cat-2-Sitting.png").convert_alpha()
cat_image_size = (100,100)
black_cat_surface = pygame.transform.scale(black_cat_surface, cat_image_size)
black_cat_x_pos = -150

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(test_surface,(0,-190)) #blit = block image transfer (one surface on another surface)
    screen.blit(text_surface,(225,70))
    black_cat_x_pos += 2
    if black_cat_x_pos > 900: black_cat_x_pos = -150
    screen.blit(black_cat_surface,(black_cat_x_pos,475))

    pygame.display.update()
    clock.tick(60)