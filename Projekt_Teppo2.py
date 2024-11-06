

import pygame

pygame.init()

screen_width = 960
screen_height = 540
BG = (50, 50, 50)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Teppo reis koju")

#Frame rate
clock = pygame.time.Clock()
FPS = 60

#Player action variable
moving_left = False
moving_right = False


def draw_BG():
    screen.fill(BG)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, x_player, y_player, w_player, h_player, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.player_rect = pygame.Rect(x_player, y_player, w_player, h_player)
        self.player_rect.center = (x, y)#Määrab rect objekti keskpunkti

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
        
        #update rectangle position
        self.player_rect.x += dx
        self.player_rect.y += dy

    def draw(self, rect_colour):
        global screen
        pygame.draw.rect(screen, rect_colour, self.player_rect)


player = Player(200, 200, 150, 400, 100, 50, 5)

colour = (3, 252, 227)

running = True
while running:

    clock.tick(FPS)

    draw_BG()

    player.move(moving_left, moving_right)
    player.draw(colour)

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