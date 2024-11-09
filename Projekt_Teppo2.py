
import pygame
from os.path import join

pygame.init()

screen_width = 960
screen_height = 540
BG = (50, 50, 50)
RED = (255, 0, 0)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Teppo reis koju")

#Frame rate
clock = pygame.time.Clock()
FPS = 60

#Game variables
GRAVITY = 0.75
TILE_SIZE = 40
#Color variables
GREEN = 45, 247, 61
RED = 232, 29, 7
WHITE = 255, 255, 255

#Player action variable
moving_left = False
moving_right = False

#Pick_ups
apple_img = pygame.image.load(join("materjalid", "Dekoratsioonid", "items", "Item_White5.png")).convert_alpha()
apple_img = pygame.transform.scale(apple_img, (100, 100))

items = { 'Health': apple_img}

#define font
font = pygame.font.SysFont('Futura', 30)

#Funktsioonid
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_BG():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 400), (screen_width, 400))

#Jätsin scale, ja char_type vahele
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, w_player, h_player, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.health = 100
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
        #reset movement variables
        dx = 0
        dy = 0
        #assign movement variables if moving left or right
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        #jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -15
            self.jump = False
            self.in_air = True
        
        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #check collision with floor
        if self.rect.bottom + dy > 400:
            dy = 400 - self.rect.bottom
            self.in_air = False
        
        #update rectangle position
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
            #check what kind of item
            if self.item_type == 'Health':
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            #delete item
            self.kill()

class HealthBar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health

    #update healthbar
    def draw(self, health):
        #update with new health
        self.health = health
        #Calculate health ratio
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, WHITE, (self.x - 4, self.y - 4, 158, 28))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))#Järjekord oluline, roheline pärast punast (nagu layerid)
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))


#Sprite groups
item_group = pygame.sprite.Group()

player = Player(200, 200, 100, 50, 5)
health_bar = HealthBar(10, 10, player.health, player.health)

#AJUTISELT

item_box = ItemBox('Health', 400, 300)
item_group.add(item_box)

running = True
while running:

    clock.tick(FPS)

    draw_BG()
    #show health
    health_bar.draw(player.health)
    # draw_text('Health: ', font, GREEN, 10, 35)

    player.move(moving_left, moving_right)
    player.draw()

    item_group.update()
    item_group.draw(screen)

    for event in pygame.event.get():
        #quit game
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