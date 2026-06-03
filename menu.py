import pygame

from water import Water
from locals import *
import cloud
import util

class Menu:
    logo = None
    sky = None

    def __init__(self, screen, menu, selection = 0):
        self.screen = screen

        self.virtual_screen = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        if not Menu.sky:
            Menu.sky = util.load_image("taivas")

        self.water = Water.global_water
        self.water_sprite = pygame.sprite.Group()
        self.water_sprite.add(self.water)

        if not Menu.logo:
            Menu.logo = util.load_image("logo")

        self.menu = menu
        self.selection = selection
        self.t = 0

    def run(self):
        done = False

        while not done:
            self.virtual_screen.fill((0,0,0))
            self.virtual_screen.blit(Menu.sky, self.virtual_screen.get_rect())
            self.water.update()
            self.water_sprite.draw(self.virtual_screen)

            for i in range(len(self.menu)):
                self.render(i)

            cloud.update()

            cloud.draw(self.virtual_screen)

            rect = Menu.logo.get_rect()
            rect.centerx = self.virtual_screen.get_rect().centerx
            rect.top = 0
            self.virtual_screen.blit(Menu.logo, rect)

            image = util.smallfont.render("http://funnyboat.sourceforge.net/", True, (0,0,0))
            rect = image.get_rect()
            rect.midbottom = self.virtual_screen.get_rect().midbottom
            self.virtual_screen.blit(image, rect)

            window_width, window_height = self.screen.get_size()

            scale = min(
                window_width / SCREEN_WIDTH,
                window_height / SCREEN_HEIGHT
            )

            scaled_width = int(SCREEN_WIDTH * scale)
            scaled_height = int(SCREEN_HEIGHT * scale)

            x = (window_width - scaled_width) // 2
            y = (window_height - scaled_height) // 2

            scaled_surface = pygame.transform.smoothscale(
                self.virtual_screen,
                (scaled_width, scaled_height)
            )

            self.screen.fill((0,0,0))
            self.screen.blit(scaled_surface, (x,y))

            pygame.display.flip()

            self.t += 1

            nextframe = False
            while not nextframe:
                pygame.event.post(pygame.event.wait())
                for event in pygame.event.get():
                    if event.type == VIDEORESIZE:
                        self.screen = pygame.display.set_mode(
                            event.size,
                            pygame.RESIZABLE,
                            32
                        )
                        continue
                    if event.type == QUIT or \
                        event.type == KEYDOWN and event.key == K_ESCAPE:
                        self.selection = -1
                        done = True
                        nextframe = True
                    elif event.type == NEXTFRAME:
                        nextframe = True
                    elif event.type == JOYAXISMOTION:
                        if event.axis == 1:
                            if event.value < -0.5:
                                self.move_up()
                            if event.value > 0.5:
                                self.move_down()
                    elif event.type == JOYBUTTONDOWN:
                        if event.button == 0:
                            done = True
                    elif event.type == KEYDOWN:
                        if event.key == K_UP:
                            self.move_up()
                        elif event.key == K_DOWN:
                            self.move_down()
                        elif event.key == K_SPACE or event.key == K_RETURN:
                            done = True

        return self.selection

    def move_down(self):
        self.selection += 1
        if self.selection >= len(self.menu):
            self.selection = len(self.menu) - 1

    def move_up(self):
        self.selection -= 1
        if self.selection < 0:
            self.selection = 0

    def render(self, id):
        color = (0,0,0)
        if self.selection == id:
            color = (220, 120, 20)

        title = self.menu[id]
        image = util.bigfont.render(title, Variables.alpha, color)
        rect = image.get_rect()
        rect.centerx = self.virtual_screen.get_rect().centerx
        rect.top = Menu.logo.get_height() + id * rect.height * 1.1

        self.virtual_screen.blit(image, rect)
