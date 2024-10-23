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

color = (255,255,255)
position = (0, 0)

pygame.display.set_caption(title ="Teppo reis koju") 
window = pygame.display.set_mode((800,600)) 

image = pygame.image.load("hampter.jpg")

exit = False
while not exit:
    # Akna kujundamine
    window.fill(color)
    window.blit(image, dest= position)
    	#pygame.event.get() # tagastab aktiivsete sündmuste loendi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    pygame.display.update()


