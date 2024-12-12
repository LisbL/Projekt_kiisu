################################################
# Programmeerimine I
# 2024/2025 sügissemester
#
# Projekt
# Teema: Mäng "Teppo reis koju"
#
#
# Autorid: Lisbeth Lepp ja Martti Virnas
#
# mõningane eeskuju: https://www.youtube.com/@CodingWithRuss
#
# Lisakommentaar (nt käivitusjuhend): Käsureale kirjutada: python Projekt_Teppo_main.py
#
##################################################

import pygame
from pygame import mixer
import os
from os.path import join
import button
import csv

mixer.init()
pygame.init()

screen_width = 960
screen_height = 540
BG = (50, 50, 50)


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Teppo reis koju")

#Frame rate
clock = pygame.time.Clock()
FPS = 60

#Game variables
start_game = False
start_intro = False
GRAVITY = 0.75
SCROLL_THRESH = 200
MAX_LEVELS = 2
#Color variables
GREEN = (45, 247, 61)
DARK_GREEN = (75, 128, 102)
RED = (232, 29, 7)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ROWS = 15
COLS = 150
TILE_SIZE = screen_height // ROWS #size'ib ekraani vertikaalselt võrdselt
TILE_TYPES = 32
screen_scroll = 0
bg_scroll = 0
level = 1 #alustab esimesest levelist

#Load music
pygame.mixer.music.load("muusika/audio.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 6000) #Esimene argument = Kui mitu korda ta mängib, teine argument = delay, kolmas argument = duration of fade (muusika ei hakka järsku käima)
#Sound effects
jump_fx = pygame.mixer.Sound("sound_effects/jump/jump_08.wav")
jump_fx.set_volume(0.2)
loaf_fx = pygame.mixer.Sound("sound_effects/loaf/cat_meowing.wav")
loaf_fx.set_volume(0.2)
loaf_fx_played = False
mlem_fx = pygame.mixer.Sound("sound_effects/mlem/mlem.mp3")
mlem_fx.set_volume(0.4)

#Background menu image
BG_menu = pygame.image.load("materjalid/dark forest/Preview.png").convert()
BG_menu = pygame.transform.scale(BG_menu, (960,540))
#Load background images
pine1_img = pygame.image.load("materjalid/Taustad/PineForestParallax/MorningLayer1.png"). convert_alpha()
pine1_img = pygame.transform.scale(pine1_img, (screen_width, screen_height))
pine2_img = pygame.image.load("materjalid/Taustad/PineForestParallax/MorningLayer2.png"). convert_alpha()
pine2_img = pygame.transform.scale(pine2_img, (screen_width, screen_height))
pine3_img = pygame.image.load("materjalid/Taustad/PineForestParallax/MorningLayer3.png"). convert_alpha()
pine3_img = pygame.transform.scale(pine3_img, (screen_width, screen_height))
pine4_img = pygame.image.load("materjalid/Taustad/PineForestParallax/MorningLayer4.png"). convert_alpha()
pine4_img = pygame.transform.scale(pine4_img, (screen_width, screen_height))
pine5_img = pygame.image.load("materjalid/Taustad/PineForestParallax/MorningLayer5.png"). convert_alpha()
pine5_img = pygame.transform.scale(pine5_img, (screen_width, screen_height))
bg_color_img = pygame.image.load("materjalid/Taustad/PineForestParallax/MorningLayer6.png"). convert_alpha()
bg_color_img = pygame.transform.scale(bg_color_img, (screen_width, screen_height))
#Font and text
font_menu = pygame.font.Font("fondid/Pixeltype.ttf", 125)
font_shadow = pygame.font.Font("fondid/Pixeltype.ttf", 125)
text = font_menu.render("Teppo reis koju", True, "darkslategray")
text_shadow = font_shadow.render("Teppo reis koju", True, "black")
font_game_over = pygame.font.Font("fondid/Pixeltype.ttf", 125)
game_over_text = font_game_over.render("Game over", True, "darkslategray")
game_over_shadow = font_shadow.render("Game over", True, "black")
#Button images
start_img = pygame.image.load("pildid/Nupud/start_btn.png").convert_alpha()
exit_img = pygame.image.load("pildid/Nupud/exit_btn.png").convert_alpha()
restart_img = pygame.image.load("pildid/Nupud/restart_btn.png").convert_alpha()

#Muudan restardi nupu suurust eraldi
restart_btn_height = 230
restart_btn_width = 100
restart_img = pygame.transform.scale(restart_img, (restart_btn_height, restart_btn_width))

#create buttons
start_button = button.Button(screen_height // 2 + 205, screen_height // 2 + 30, start_img)
exit_button = button.Button(screen_height // 2 + 205, screen_height // 2 + 180, exit_img)
restart_button = button.Button(screen_height // 2 + 215, screen_height // 2 + 5, restart_img)

#Player action variable
moving_left = False
moving_right = False

#Store tiles in a list
img_list = []
for x in range(1, 24):
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

#Pick_ups
fish_img = pygame.image.load(join("materjalid", "Collectible", "goodfish.png")).convert_alpha()
poison_apple_img = pygame.image.load(join("materjalid", "Dekoratsioonid", "items", "Item_White6.png")).convert_alpha()
items = { 'Health': fish_img, 'Poison': poison_apple_img}

#Funktsioonid
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_BG():
    screen.fill(BG)
    width = bg_color_img.get_width()
    for i in range(7):
        screen.blit(bg_color_img, ((i*width) - bg_scroll * 0.4, 0))
        screen.blit(pine5_img, ((i*width) - bg_scroll * 0.5, screen_height - pine5_img.get_height()))
        screen.blit(pine4_img, ((i*width) - bg_scroll * 0.6,screen_height - pine4_img.get_height()))
        screen.blit(pine3_img, ((i*width) - bg_scroll * 0.7,screen_height - pine3_img.get_height()))
        screen.blit(pine2_img, ((i*width) - bg_scroll * 0.8,screen_height - pine2_img.get_height()))
        screen.blit(pine1_img, ((i*width) - bg_scroll * 0.9,screen_height - pine1_img.get_height()))

#Restart level funktsioon
def reset_level():
    enemy_group.empty()
    item_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()

    #Create emtpy tile list
    data = []
    for row in range (ROWS): #15 korda
        r = [-1] * COLS #teeb järjendi 150-st -1 väärtusega tile'idest
        data.append(r)
    return data


#Jätsin scale vahele
class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.health = 100
        self.char_type = char_type
        self.max_health = self.health
        self.alive = True
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0 #Animation is in the first frame
        self.action = 0
        self.update_time = pygame.time.get_ticks() #when the animation was last updated
        scale = 1.1

        #idle
        temp_list = []
        for i in range(10):
            img_2 = pygame.image.load(f"materjalid/Tegelased/Teppo/Idle/idle_{i}.png")
            img_2 = pygame.transform.scale(img_2, (int(img_2.get_width() * scale), int(img_2.get_height() * scale)))
            temp_list.append(img_2)
        self.animation_list.append(temp_list)

        #running
        temp_list = []
        for i in range(8):
            img_2 = pygame.image.load(f"materjalid/Tegelased/Teppo/Running/run_{i}.png")
            img_2 = pygame.transform.scale(img_2, (int(img_2.get_width() * scale), int(img_2.get_height() * scale)))
            temp_list.append(img_2)
        self.animation_list.append(temp_list)

        #jump
        temp_list = []
        for i in range(2):
            img_2 = pygame.image.load(f"materjalid/Tegelased/Teppo/Jump/jump_{i}.png")
            img_2 = pygame.transform.scale(img_2, (int(img_2.get_width() * scale), int(img_2.get_height() * scale)))
            temp_list.append(img_2)
        self.animation_list.append(temp_list)

        #death (loaf)
        temp_list = []
        for i in range(4):
            img_2 = pygame.image.load(f"materjalid/Tegelased/Teppo/Death/loaf_{i}.png")
            img_2 = pygame.transform.scale(img_2, (int(img_2.get_width() * scale), int(img_2.get_height() * scale)))
            temp_list.append(img_2)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)#Määrab rect objekti keskpunkti
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.last_hit_time = 0 #järgib, millal viimati haiget sai

    def move(self, moving_left, moving_right):
        #Reset movement variables
        screen_scroll = 0
        dx = 0
        dy = 0
        #Assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        #Jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -15
            self.jump = False
            self.in_air = True
        
        #Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #Check for collision
        for tile in world.obstacle_list:
            #check collision in the x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            #check for collision in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if below the ground
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                #check if above the ground
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        #Check for collision with water
        if pygame.sprite.spritecollide(self, water_group, False):
            current_time = pygame.time.get_ticks()
            if current_time - player.last_hit_time > 1000:
                player.health -= 30
                player.last_hit_time = current_time
                if player.health < 0:
                    player.health = 0

        #Check for collision with exit
        level_complete = False
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True

        #Check if fallen off the map
        if self.rect.bottom > screen_height:
            self.health = 0

        #check if going off the edges of the screen
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > screen_width:
                dx = 0
        #Update rectangle position
        self.rect.x += dx
        self.rect.y += dy

        #update scroll based on player pos
        if self.char_type == 'player':
            if (self.rect.right > screen_width - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - screen_width)\
                or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx #kui liigub paremale siis ekraan liigub vasakule

        return screen_scroll, level_complete

    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 130 #Limiteerib kui kiiresti pilt muutub (ms)

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            if self.action == 3:
                if self.frame_index < len(self.animation_list[self.action]) - 1:
                    self.frame_index += 1
            else:
                self.frame_index += 1
                if self.frame_index >= len(self.animation_list[self.action]):
                    self.frame_index = 0

        if self.action == 2:
            if self.vel_y < 0:
                self.frame_index = 0
            else:
                self.frame_index = 1
        else:
            self.image = self.animation_list[self.action][self.frame_index]
            #kontrollib kas piisavalt aega on mööda läinud viimasest värskendamisest
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            #kui animatsioon on tehtud, siis algab uuesti
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]

    def update_action(self, new_action):
        #kontrolli kas uus tegevus on eelmisest erinev
        if new_action != self.action and self.alive:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        global screen
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def update(self):
        self.check_alive()

    def check_alive(self):
        global screen_scroll
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            if self.action != 3:
                self.update_action(3)
            self.alive = False

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('materjalid/Dekoratsioonid/spikes/tile_2.png')
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE * 0.8))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.damage = 10
    
    def update(self):
        if pygame.sprite.collide_rect(self, player):
            current_time = pygame.time.get_ticks()
            if current_time - player.last_hit_time > 1000:
                player.health -= self.damage
                player.last_hit_time = current_time
                if player.health < 0:
                    player.health = 0
        self.rect.x += screen_scroll


    def draw(self):
        global screen
        global bg_scroll
        draw_x = self.rect.x
        draw_y = self.rect.y
        screen.blit(self.image, (draw_x, draw_y))


class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data): #world data that we loaded in from our csv file
        self.level_length = len(data[0])
        #iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0: #-1 pole vaja kaasa arvata, sest nad on tühjad kohad
                    img = img_list[tile] #võtab pildi järjendist
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE 
                    img_rect.y = y * TILE_SIZE #annab igale laetud pildile ristküliku
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 5:
                        self.obstacle_list.append(tile_data)
                    if tile >= 10 and tile <= 16:
                        self.obstacle_list.append(tile_data)
                    if tile >= 18 and tile <= 20:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 6 and tile <= 8:
                        self.obstacle_list.append(tile_data) #PLATVORMID!! vajavad tegemist!
                    elif tile == 9:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile == 17:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile >= 21 and tile < 23:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif tile >= 25 and tile <= 27:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 31: #create a player
                        player = Player('player', x * TILE_SIZE, y * TILE_SIZE, 5)
                        health_bar = HealthBar(10, 10, player.health, player.health)
                    elif tile >= 28 and tile <= 29: #enemy (spikes)
                        enemy = Enemy(x * TILE_SIZE, y * TILE_SIZE)
                        enemy_group.add(enemy)
                    elif tile == 23: #hea õun
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_group.add(item_box)
                    elif tile == 24: #paha õun
                        item_box2 = ItemBox('Poison', x * TILE_SIZE, y * TILE_SIZE)
                        item_group.add(item_box2)
                    elif tile == 30: #create exit
                        exit = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exit)

        return player, health_bar

    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])

class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        self.rect.x += screen_scroll

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = items[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        #scroll
        self.rect.x += screen_scroll
        #Check if it has been picked up by player
        if pygame.sprite.collide_rect(self, player):
            #Check what kind of item
            if self.item_type == 'Health':
                mlem_fx.play()
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Poison':
                player.health -= 25
            #Delete item
            self.kill()

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    #Update healthbar
    def draw(self, health):
        #Update with new health
        self.health = health
        #Calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, WHITE, (self.x - 4, self.y - 4, 158, 28))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))#Järjekord oluline, roheline pärast punast (nagu layerid)
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))

#Animatsioon ekraanide vahel
class ScreenFade():
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):
        fade_complete = False
        self.fade_counter += self.speed
        if self.direction == 1: #Terve ekraani fade
            pygame.draw.rect(screen, self.colour, (0 - self.fade_counter, 0, screen_width // 2, screen_height)) #See ristkülik liigub vasakule
            pygame.draw.rect(screen, self.colour, (screen_width // 2 + self.fade_counter, 0, screen_width, screen_height)) #Ristkülik liigub paremale
            pygame.draw.rect(screen, self.colour, (0, 0 - self.fade_counter, screen_width, screen_height // 2)) #Läheb üles
            pygame.draw.rect(screen, self.colour, (0, screen_height // 2 + self.fade_counter, screen_width, screen_height)) #Läheb alla
        if self.direction == 2: #Vertikaalne ekraani fade down
            pygame.draw.rect(screen, self.colour, (0, 0, screen_width, 0 + self.fade_counter))
        if self.fade_counter >= screen_width:
            fade_complete = True

        return fade_complete
    
#Create screen fades
intro_fade = ScreenFade(1, BLACK, 4)
death_fade = ScreenFade(2, DARK_GREEN, 4)

#Sprite groups
item_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#Create empty tile list
world_data = []
for row in range (ROWS): #15 korda
    r = [-1] * COLS #teeb järjendi 150-st -1 väärtusega tile'idest
    world_data.append(r)
#load in level data and create world
with open(f"level{level}_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",") #delimiter ütleb nt kus -1 muutub mingiks muuks väärtuseks (mingiks teiseks plokiks)
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)
world = World()
player, health_bar = world.process_data(world_data)

running = True
while running:

    clock.tick(FPS)

    player.update_animation()

    if start_game == False:
        screen.blit(BG_menu, (0,0))
        screen.blit(text_shadow, (180,40))
        screen.blit(text, (175,40))
        if start_button.draw(screen):
            start_game = True
            start_intro = True #Kui toimub nupu vajutus, siis intro läheb käima
        if exit_button.draw(screen):
            running = False
    else:
        draw_BG()

        #draw world map
        world.draw()
        #Show health
        health_bar.draw(player.health)

        player.update()
        player.draw()

        for enemy in enemy_group:
            enemy.update()
            enemy.draw()

        item_group.update()
        item_group.draw(screen)
        decoration_group.update()
        decoration_group.draw(screen)
        water_group.update()
        water_group.draw(screen)
        exit_group.update()
        exit_group.draw(screen)

        if player.alive:
            if player.in_air:
                    player.update_action(2) # 2 = jump
            elif moving_left or moving_right:
                player.update_action(1) # 1 = running
            else:
                player.update_action(0) # 0 = idle
            screen_scroll, level_complete = player.move(moving_left, moving_right)
            bg_scroll -= screen_scroll
            #Check if player has completed the level
            if level_complete:
                start_intro = True
                level += 1
                bg_scroll = 0
                world_data = reset_level()
                if level <= MAX_LEVELS:
                    with open(f"level{level}_data.csv", newline="") as csvfile:
                        reader = csv.reader(csvfile, delimiter=",")
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data)

        else:
            if player.health <= 0:
                if not loaf_fx_played:
                    loaf_fx.play()
                    loaf_fx_played = True
            player.update_action(3) # 3 = loaf
            screen_scroll = 0
            if death_fade.fade():
                if restart_button.draw(screen):
                    death_fade.fade_counter = 0
                    start_intro = True
                    bg_scroll = 0
                    loaf_fx_played = False
                    world_data = reset_level()
                    with open(f"level{level}_data.csv", newline="") as csvfile:
                        reader = csv.reader(csvfile, delimiter=",")
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(world_data)
                if not player.alive:
                    screen.blit(game_over_shadow, (screen_width // 3 - 22, screen_height // 3 - 80))
                    screen.blit(game_over_text, (screen_width // 3 - 25, screen_height // 3 - 80))

        #Show intro
        if start_intro == True:
            if intro_fade.fade():
                start_intro = False
                intro_fade.fade_counter = 0 #Intro on tehtud ja võib tagasi 0-väärtuseks minna

    for event in pygame.event.get():
        #Quit game
        if event.type == pygame.QUIT:
            running = False

            #Key pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
                jump_fx.play()
            if event.key == pygame.K_ESCAPE:
                running = False
            #Key released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

        
    pygame.display.update()

pygame.quit()