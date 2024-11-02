import pygame

pygame.init()

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Menüü")

fps = 60
clock = pygame.time.Clock()
main_menu = False
font = pygame.font.Font("fondid/Pixeltype.ttf", 50)

class Button:
    def __init__(self, txt, pos):
        self.text = txt
        self.pos = pos
        self.button = pygame.rect.Rect((self.pos[0], self.pos[1]), (260, 40))

    def draw(self):
        pygame.draw.rect(screen, "light gray", self.button, 0, 5)
        pygame.draw.rect(screen, "dark gray", self.button, 5, 5)
        text = font.render(self.text, True, "black")
        screen.blit(text, (self.pos[0] + 15, self.pos[1] + 7))

    def check_clicked(self):
        if self.button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            return True
        else:
            return False

def draw_game():
    button = Button("Main Menu", (530, 550))
    button.draw()
    return button.check_clicked()

def draw_menu():
    pygame.draw.rect(screen, "black", [155, 75, 500, 450])
    menu_btn = Button("Exit Menu", (277, 475))
    btn1 = Button("Play", (277, 250))
    btn2 = Button("Options", (277, 325))
    btn3 = Button("Yippee", (277, 400))
    menu_btn.draw()
    btn1.draw()
    btn2.draw()
    btn3.draw()
    return not menu_btn.check_clicked()

run = True
while run:
    screen.fill("darkcyan")
    clock.tick(fps)
    if main_menu:
        main_menu = draw_menu()
    else:
        main_menu = draw_game()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()