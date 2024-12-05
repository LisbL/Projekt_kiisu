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
restart_img = pygame.image.load("pildid/Nupud/restart_btn.png").convert_alpha()

#create buttons
start_button = button.Button(screen_height // 2 + 205, screen_height // 2 + 30, start_img)
exit_button = button.Button(screen_height // 2 + 205, screen_height // 2 + 180, exit_img)
restat_button = button.Button(screen_height // 2 + 205, screen_height // 2 + 30, restart_img)

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
        self.animation_list = []
        self.frame_index = 0 #Animation is in the first frame
        self.action = 0
        self.update_time = pygame.time.get_ticks() #when the animation was last updated
        scale = 2

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
        self.last_hit_time = 0 #järgib, millal viimati haiget sai

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
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            if self.action != 3:
                self.update_action(3)
            self.alive = False

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_w, enemy_h):
        super().__init__()
        self.image = pygame.Surface((enemy_w, enemy_h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.damage = 10
    
    def update(self):
        if pygame.sprite.collide_rect(self, player):
            current_time = pygame.time.get_ticks()
            if current_time - player.last_hit_time > 1000:
                player.health -= self.damage
                player.last_hit_time = current_time
                if player.health < 0:
                    player.health = 0


    def draw(self):
        global screen
        screen.blit(self.image, self.rect)


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

enemy = Enemy(500, 390, 50, 40)
enemy_group.add(enemy)

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


        #Show health
        health_bar.draw(player.health)

        player.update()
        player.draw()

        for enemy in enemy_group:
            enemy.update()
            enemy.draw()

        item_group.update()
        item_group.draw(screen)

        if player.alive:
            if player.in_air:
                    player.update_action(2) # 2 = jump
            elif moving_left or moving_right:
                player.update_action(1) # 1 = running
            else:
                player.update_action(0) # 0 = idle
            player.move(moving_left, moving_right)
        else:
            player.update_action(3) # 3 = loaf

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