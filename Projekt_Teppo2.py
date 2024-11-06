
import pygame

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

#Player action variable
moving_left = False
moving_right = False


def draw_BG():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 400), (screen_width, 400))

#Jätsin scale, ja char_type vahele
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, w_player, h_player, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.alive = True
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.flip = False
        self.image = pygame.Surface((w_player, h_player))
        self.image.fill((3, 252, 227))
        self.player_rect = self.image.get_rect()
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
        #jump
        if self.jump == True:
            self.vel_y = -15
            self.jump = False
        
        #apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        #check collision with floor
        if self.player_rect.bottom + dy > 400:
            dy = 400 - self.player_rect.bottom
        
        #update rectangle position
        self.player_rect.x += dx
        self.player_rect.y += dy

    def draw(self):
        global screen
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.player_rect)


player = Player(200, 200, 100, 50, 5)

running = True
while running:

    clock.tick(FPS)

    draw_BG()

    player.move(moving_left, moving_right)
    player.draw()

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