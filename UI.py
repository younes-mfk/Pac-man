import pygame
pygame.init()


class Instructions:

    def __init__(self, window, menu_img) -> None:
        self.window = window
        self.menu_img = menu_img

    def run(self):
        menu_x = (2600 - 900) // 2
        menu_y = (2000 - 1350) // 2

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
        while in_menu:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            self.window.blit(self.menu_img, (menu_x, menu_y))

            pygame.display.flip()
            pygame.time.delay(100)


class Scoreboard:

    def __init__(self, window, baord_img) -> None:
        self.window = window
        self.board_img = baord_img

    def run(self):
        menu_x = (2600 - 900) // 2
        menu_y = (2000 - 1350) // 2

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
        while in_menu:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            self.window.blit(self.board_img, (menu_x, menu_y))

            pygame.display.flip()
            pygame.time.delay(100)


class Menu:

    def __init__(self, window) -> None:
        self.window = window
        self.menu_img = pygame.image.load("menu_images/menu.png")
        self.images = [pygame.image.load("menu_images/startgame.png"),
                       pygame.image.load("menu_images/high_scores.png"),
                       pygame.image.load("menu_images/instruction.png"),
                       pygame.image.load("menu_images/exit.png")]
        self.selected_images = [
            pygame.image.load("menu_images/selected_startgame.png"),
            pygame.image.load("menu_images/selected_high_scores.png"),
            pygame.image.load("menu_images/selected_instructions.png"),
            pygame.image.load("menu_images/selected_exit.png")]

        self.instructions = Instructions(
                                        window,
                                        pygame.image.load(
                                            "menu_images/"
                                            "instructions_menu.png"))
        self.score_board = Scoreboard(
                                        window,
                                        pygame.image.load(
                                            "menu_images/"
                                            "score_board.png"))

    def run(self):
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
        selected = 0
        while in_menu:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected = (selected + 1) % 4
                    elif event.key == pygame.K_UP:
                        selected = (selected - 1) % 4
                    elif event.key == pygame.K_RETURN:
                        if not selected:
                            return "gameplay"
                        if selected == 1:
                            self.score_board.run()
                        if selected == 2:
                            self.instructions.run()
                        if selected == 3:
                            return "exit"

            self.window.blit(self.menu_img, (menu_x, menu_y))

            if selected:
                self.window.blit(self.images[0], ((buttons_x, menu_y + 390)))
            else:
                self.window.blit(self.selected_images[0], ((buttons_x, menu_y + 390)))

            if selected != 1:
                self.window.blit(self.images[1], ((buttons_x, menu_y + 550)))

            else:
                self.window.blit(self.selected_images[1], ((buttons_x, menu_y + 550)))

            if selected != 2:
                self.window.blit(self.images[2], ((buttons_x, menu_y + 710)))
            else:
                self.window.blit(self.selected_images[2], ((buttons_x, menu_y + 710)))

            if selected != 3:
                self.window.blit(self.images[3], ((buttons_x, menu_y + 870)))
            else:
                self.window.blit(self.selected_images[3], ((buttons_x, menu_y + 870)))

            # font = pygame.font.Font(None, 40)

            # text = font.render(
            #     "YOUNES 24500",    # chehad l9lawi hhh
            #     True,
            #     (255, 255, 0)
            # )

            # self.window.blit(text, (500, 300))

            pygame.display.flip()
            pygame.time.delay(10)


class Pausemenu:

    def __init__(self, window) -> None:
        self.window = window
        self.menu_img = pygame.image.load("menu_images/pause_menu.png")
        self.images = [pygame.image.load("menu_images/resume_game.png"),
                       pygame.image.load("menu_images/return_menu.png")]
        self.selected_images = [
                    pygame.image.load("menu_images/selected_resume_game.png"),
                    pygame.image.load("menu_images/selected_return_menu.png")]

    def run(self):
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
        selected = 0
        while in_menu:
            self.window.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected = (selected + 1) % 2
                    elif event.key == pygame.K_UP:
                        selected = (selected - 1) % 2
                    elif event.key == pygame.K_RETURN:
                        if not selected:
                            return "gameplay"
                        if selected == 1:
                            return "menu"

            self.window.blit(self.menu_img, (menu_x, menu_y))

            if selected:
                self.window.blit(self.images[0], ((buttons_x, menu_y + 550)))
            else:
                self.window.blit(self.selected_images[0], ((buttons_x, menu_y + 550)))

            if selected != 1:
                self.window.blit(self.images[1], ((buttons_x, menu_y + 710)))

            else:
                self.window.blit(self.selected_images[1], ((buttons_x, menu_y + 710)))

            pygame.display.flip()
            pygame.time.delay(10)
