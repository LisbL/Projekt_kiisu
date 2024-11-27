import pygame

pygame.init()

clock = pygame.time.Clock()
FPS = 60

#Game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 560
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption("Level Editor")

#Define game variables
ROWS = 16#read
MAX_COLS = 150#veerud
TILE_SIZE = SCREEN_HEIGHT // ROWS

scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1

#Load images
pine1_img = pygame.image.load("materjalid/Taustad/PineForestParallax/MorningLayer1.png"). convert_alpha()
pine1_img = pygame.transform.scale(pine1_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
pine2_img = pygame.image.load("materjalid/Taustad/PineForestParallax/MorningLayer2.png"). convert_alpha()
pine2_img = pygame.transform.scale(pine2_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
pine3_img = pygame.image.load("materjalid/Taustad/PineForestParallax/MorningLayer3.png"). convert_alpha()
pine3_img = pygame.transform.scale(pine3_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
pine4_img = pygame.image.load("materjalid/Taustad/PineForestParallax/MorningLayer4.png"). convert_alpha()
pine4_img = pygame.transform.scale(pine4_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
pine5_img = pygame.image.load("materjalid/Taustad/PineForestParallax/MorningLayer5.png"). convert_alpha()
pine5_img = pygame.transform.scale(pine5_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_color_img = pygame.image.load("materjalid/Taustad/PineForestParallax/MorningLayer6.png"). convert_alpha()
bg_color_img = pygame.transform.scale(bg_color_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

#Define colours
BLUE = (52, 207, 235)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

#Funktsioon tausta joonistamiseks
def draw_bg():
    screen.fill(BLUE)
    width = bg_color_img.get_width()
    for i in range(4):
        screen.blit(bg_color_img, ((i*width) - scroll * 0.4, 0))
        screen.blit(pine5_img, ((i*width) - scroll * 0.5, SCREEN_HEIGHT - pine5_img.get_height()))
        screen.blit(pine4_img, ((i*width) - scroll * 0.6,SCREEN_HEIGHT - pine4_img.get_height()))
        screen.blit(pine3_img, ((i*width) - scroll * 0.7,SCREEN_HEIGHT - pine3_img.get_height()))
        screen.blit(pine2_img, ((i*width) - scroll * 0.8,SCREEN_HEIGHT - pine2_img.get_height()))
        screen.blit(pine1_img, ((i*width) - scroll * 0.9,SCREEN_HEIGHT - pine1_img.get_height()))

    #Draw grid
def draw_grid():
    #Vertikaalsed piirjooned
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
    #Horisontaalsed jooned
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))

run = True
while run:

    clock.tick(FPS)

    draw_bg()
    draw_grid()


    #scroll the map
    if scroll_left == True and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right == True:
        scroll += 5 * scroll_speed

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #Keyboard press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 5
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_RSHIFT:
                scroll_speed = 1


    
    pygame.display.update()

pygame.quit()