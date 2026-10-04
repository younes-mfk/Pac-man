import pygame
pygame.init()


class Menu:

    def __init__(self, window, menu_img, images,
                 selected_images=None) -> None:
        self.window = window
        self.menu_img = menu_img
        self.images = images
        self.selected_images = selected_images

    def test(self):
        menu_x = (2600 - 900) // 2
        menu_y = (2000 - 1350) // 2
        BUTTON_WIDTH = 620
        buttons_x = menu_x - BUTTON_WIDTH

        in_menu = True
        while in_menu:
            self.window.blit(self.menu_img, (menu_x, menu_y))
            self.window.blit(self.images[0], ((990, menu_y + 390)))
            pygame.display.flip()
            pygame.time.delay(5000)
            in_menu = False

