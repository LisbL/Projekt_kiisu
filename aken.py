import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800,600))
screen.fill("darkblue")
pygame.display.set_caption("Teppo Reis Koju")
clock = pygame.time.Clock()

test_surface = pygame.image.load("pildid/pixel-art-display-test.jpg")


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(test_surface,(0,0)) #blit = block image transfer (one surface on another surface)

    pygame.display.update()
    clock.tick(60)