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
TILE_SIZE = 40
#Color variables
GREEN = (45, 247, 61)
RED = (232, 29, 7)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Load music
pygame.mixer.music.load("muusika/audio.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 6000) #Esimene argument = Kui mitu korda ta mängib, teine argument = delay, kolmas argument = duration of fade (muusika ei hakka järsku käima)
#Sound effects
jump_fx = pygame.mixer.Sound("sound_effects/jump/jump_08.wav")
jump_fx.set_volume(0.2)

#Background menu image
BG_menu = pygame.image.load("materjalid/dark forest/Preview.png").convert()
BG_menu = pygame.transform.scale(BG_menu, (960,540))
#Font
font_menu = pygame.font.Font("fondid/Pixeltype.ttf", 125)
font_shadow = pygame.font.Font("fondid/Pixeltype.ttf", 125)
text = font_menu.render("Teppo reis koju", True, "darkslategray")
text_shadow = font_shadow.render("Teppo reis koju", True, "black")
#Button images
start_img = pygame.image.load("pildid/Nupud/start_btn.png").convert_alpha()
exit_img = pygame.image.load("pildid/Nupud/exit_btn.png").convert_alpha()

#create buttons
start_button = button.Button(screen_height // 2 + 205, screen_height // 2 + 30, start_img)
exit_button = button.Button(screen_height // 2 + 205, screen_height // 2 + 180, exit_img)

#Player action variable
moving_left = False
moving_right = False

#Pick_ups
apple_img = pygame.image.load(join("materjalid", "Dekoratsioonid", "items", "Item_White5.png")).convert_alpha()
apple_img = pygame.transform.scale(apple_img, (100, 100))
poison_apple_img = pygame.image.load(join("materjalid", "Dekoratsioonid", "items", "Item_White6.png")).convert_alpha()
poison_apple_img = pygame.transform.scale(poison_apple_img, (100, 100))
items = { 'Health': apple_img, 'Poison': poison_apple_img}

#Funktsioonid
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_BG():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 400), (screen_width, 400))

#Jätsin scale, ja char_type vahele
class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, w_player, h_player, speed):
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
        self.image = pygame.Surface((w_player, h_player))
        self.image.fill((3, 252, 227))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)#Määrab rect objekti keskpunkti

    def move(self, moving_left, moving_right):
        #Reset movement variables
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

        #Check collision with floor
        if self.rect.bottom + dy > 400:
            dy = 400 - self.rect.bottom
            self.in_air = False
        
        #Update rectangle position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        global screen
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def update(self):
        self.check_alive()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False

class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        super().__init__()
        self.item_type = item_type
        self.image = items[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def update(self):
        #Check if it has been picked up by player
        if pygame.sprite.collide_rect(self, player):
            #Check what kind of item
            if self.item_type == 'Health':
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

#Sprite groups
item_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()


#AJUTISELT
item_box = ItemBox('Health', 400, 300)
item_box2 = ItemBox('Poison', 600, 300)
item_group.add(item_box)
item_group.add(item_box2)

player = Player('player', 200, 200, 100, 50, 5)
health_bar = HealthBar(10, 10, player.health, player.health)

enemy = Player('enemy', 500, 350, 90, 40, 0)
enemy_group.add(enemy)

running = True
while running:

    clock.tick(FPS)

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
        #Show health
        health_bar.draw(player.health)

        player.move(moving_left, moving_right)
        player.update()
        player.draw()

        for enemy in enemy_group:
            enemy.move(moving_left,moving_right)
            enemy.update()
            enemy.draw()

        item_group.update()
        item_group.draw(screen)

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