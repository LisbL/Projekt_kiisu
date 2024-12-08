import pygame
import button2
import csv

pygame.init()

clock = pygame.time.Clock()
FPS = 60

#Game window
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption("Level Editor")

#Define game variables
ROWS = 15#read MUUTSIN 16-st 15!!!
MAX_COLS = 150#veerud
TILE_TYPES = 24
current_tile = 0
level = 0
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

#Store tiles in a list
img_list = []
for x in range(1, TILE_TYPES):
    img = pygame.image.load(f"materjalid/Tileset/1 Tiles/Tile_{x}.png").convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
for x in range(5, 7):
    img = pygame.image.load(f"materjalid/Dekoratsioonid/items/Item_White{x}.png").convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
for x in range(1, 4):
    img = pygame.image.load(f"materjalid/Dekoratsioonid/3 Objects/Grass/{x}.png").convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE * 0.5))
    img_list.append(img)
for x in range(1, 3):
    img = pygame.image.load(f"materjalid/Dekoratsioonid/spikes/tile_{x}.png").convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE * 0.8))
    img_list.append(img)
img = pygame.image.load(f"materjalid/Dekoratsioonid/3 Objects/Pointers/1.png").convert_alpha()
img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
img_list.append(img)
img = pygame.image.load(f"materjalid/Tegelased/Teppo/Idle/idle_0.png").convert_alpha()
img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
img_list.append(img)

save_img = pygame.image.load("materjalid/Tileset/save_btn.png").convert_alpha()
load_img = pygame.image.load("materjalid/Tileset/load_btn.png").convert_alpha()

#Define colours
BLUE = (52, 207, 235)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

#Define font
font = pygame.font.Font("fondid/Pixeltype.ttf", 30)

#Create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

#Create ground
for tile in range(0, MAX_COLS):
    world_data[ROWS - 1][tile] = 11

#Funktsioon teksti kuvamiseks
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#Funktsioon tausta joonistamiseks
def draw_bg():
    screen.fill(BLUE)
    width = bg_color_img.get_width()
    for i in range(7):
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

    #Function for drawing world tiles
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                if tile == 28 or tile == 29:
                    screen.blit(img_list[tile], 
                                (x * TILE_SIZE - scroll, y * TILE_SIZE + (TILE_SIZE - TILE_SIZE* 0.8)))
                elif tile == 27 or tile == 26 or tile == 25:
                    screen.blit(img_list[tile], 
                                (x * TILE_SIZE - scroll, y * TILE_SIZE + (TILE_SIZE - TILE_SIZE* 0.5)))
                else:
                    screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

#create button
save_button = button2.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = button2.Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)
#make a button list
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button2.Button(SCREEN_WIDTH + (60 * button_col) + 35, 75 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 4:
        button_row += 1
        button_col = 0


run = True
while run:

    clock.tick(FPS)

    draw_bg()
    draw_grid()
    draw_world()

    draw_text(f"Level: {level}", font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text("Press UP or DOWN to change level", font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

    #save and load data
    if save_button.draw(screen):
        #save level data
        with open(f"level{level}_data.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter = ",")
            for row in world_data:
                writer.writerow(row)

    if load_button.draw(screen):
        #load in level data
        #reset scroll back to the start of the level
        scroll = 0
        with open(f"level{level}_data.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter = ",")
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
                

    #draw tile panel and tiles
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

    #choose a tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count

    #highlight selected tile
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    #scroll the map
    if scroll_left == True and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll += 5 * scroll_speed

    #add new tiles to the screen
    #get mouse position
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE

    #Check that the coordinates are withing the tile area
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        #update tile value
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #Keyboard press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN and level > 0:
                level -= 1
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