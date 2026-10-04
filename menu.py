import pygame
pygame.init()


class Menu:

    def __init__(self, window, menu_img, images,
                 selected_images) -> None:
        self.window = window
        self.menu_img = menu_img
        self.images = images
        self.selected_images = selected_images

    def test(self):
        i = 0
        menu_x = (2600 - 900) // 2
        menu_y = (2000 - 1350) // 2
        BUTTON_WIDTH = 550
        buttons_x = menu_x + (menu_x - BUTTON_WIDTH) // 2

        BLUE = (0, 100, 255)

        BORDER_MARGIN = 50
        BORDER_WIDTH = 12

        pygame.draw.rect(
            self.window,
            BLUE,
            (
                BORDER_MARGIN,
                BORDER_MARGIN,
                2600 - BORDER_MARGIN * 2,
                2000 - BORDER_MARGIN * 2
            ),
            BORDER_WIDTH
        )
        in_menu = True
        image = self.images[0]
        while in_menu:

            self.window.blit(self.menu_img, (menu_x, menu_y))
            self.window.blit(image, ((buttons_x, menu_y + 390)))
            self.window.blit(self.images[1], ((buttons_x, menu_y + 550)))
            self.window.blit(self.images[2], ((buttons_x, menu_y + 710)))
            self.window.blit(self.images[3], ((buttons_x, menu_y + 870)))
            pygame.display.flip()
            pygame.time.delay(1000)
            # in_menu = False
            if i:
                image = self.images[0]
                i = 0
            else:
                image = self.selected_images[0]
                i = 1
