import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,600))
screen.fill("darkblue")
pygame.display.set_caption("Teppo Reis Koju")
clock = pygame.time.Clock()
test_font = pygame.font.Font("fondid/Pixeltype.ttf", 75)

test_surface = pygame.image.load("pildid/pixel-art-display-test.jpg")
text_surface = test_font.render("Teppo Reis Koju", False, "White")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(test_surface,(0,0)) #blit = block image transfer (one surface on another surface)
    screen.blit(text_surface,(215,50))

    pygame.display.update()
    clock.tick(60)