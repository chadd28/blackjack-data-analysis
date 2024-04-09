import pygame as pg

class Game:
    def __init__(self):
        self.cookies = 0
        self.cps = 1
        self.cookie = pg.Rect(250, 150, 300, 300)
        self.cookie_color = "#522920"
        self.clicked = False

    def draw_score(self):
        self.display_cookies = text_font.render(f"Cookies: {str(self.cookies)}", True, "#ffffff")
        screen.blit(self.display_cookies, (0, 500))

    def click_button(self):
        self.mouse_pos = pg.mouse.get_pos()
        if self.cookie.collidepoint(self.mouse_pos):
            if pg.mouse.get_pressed()[0]:
                self.clicked = True
            else:
                if self.clicked:
                    self.cookies += 1
                    self.clicked = False
        
        pg.draw.rect(screen, self.cookie_color, self.cookie, border_radius=150)
    
    def render(self):
        self.click_button()
        self.draw_score()



pg.init()
screen_width = 800
screen_height = 600

game = Game()

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Cookie Clicker")
text_font = pg.font.Font(None, 50)
title = text_font.render("Cookie Clicker", True, "#000000")
clock = pg.time.Clock()

run = True
while run:
    screen.fill("#0000ff")
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    screen.blit(title, (270,15))

    game.render()

    pg.display.update()
    clock.tick(30)     # 30 frames per second

pg.quit()