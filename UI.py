
from paths import PathResolver
from adapter import Adapter
from db import DataBase
from typing import Tuple
from parse_config import GameData
import pygame
pygame.init()


BORDER_MARGIN = 50
BORDER_WIDTH = 12

MENU_WIDTH = 900
MENU_HEIGHT = 1350


class UILayout:

    @staticmethod
    def draw_border(window: pygame.surface.Surface) -> None:
        pygame.draw.rect(
            window,
            (0, 100, 255),
            (
                BORDER_MARGIN,
                BORDER_MARGIN,
                2600 - BORDER_MARGIN * 2,
                2000 - BORDER_MARGIN * 2
            ),
            BORDER_WIDTH
        )

    @staticmethod
    def get_menu_position() -> Tuple:
        return ((2600 - 900) // 2, (2000 - 1350) // 2)

    @staticmethod
    def validate_score(score: int) -> str:
        score_str = str(score)
        if len(score_str) < 7:
            displayed_score = score_str
        else:
            displayed_score = score_str[:6] + "..."
        return displayed_score


class Instructions:

    def __init__(self, window: pygame.surface.Surface,
                 menu_img: pygame.surface.Surface) -> None:
        self.window = window
        self.menu_img = menu_img

    def run(self) -> None:
        menu_x, menu_y = UILayout.get_menu_position()

        UILayout.draw_border(self.window)

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

    def __init__(self, window: pygame.surface.Surface,
                 baord_img: pygame.surface.Surface) -> None:
        self.window = window
        self.board_img = baord_img
        self.font = pygame.font.Font(None, 60)

    def run(self, database: DataBase) -> None:
        menu_x, menu_y = UILayout.get_menu_position()

        UILayout.draw_border(self.window)
        in_menu = True
        scores = database.sorted_scores()
        name_x = 310
        score_x = 580
        while in_menu:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

            self.window.blit(self.board_img, (menu_x, menu_y))
            temp = 430
            for score in scores[:10]:
                name = self.font.render(
                        f"{score['name']}",
                        True,
                        (255, 255, 0)
                    )
                valid_score = UILayout.validate_score(score['score'])
                score = self.font.render(
                        valid_score,
                        True,
                        (255, 255, 0)
                    )
                self.window.blit(name, (menu_x + name_x, menu_y + temp))
                self.window.blit(score, (menu_x + score_x, menu_y + temp))
                temp += 60

            pygame.display.flip()
            pygame.time.delay(100)


class GameOver:

    def __init__(self, window: pygame.surface.Surface,
                 database: DataBase) -> None:
        self.window = window
        self.menu_img = pygame.image.load(
            PathResolver.resource_path(
                "menu_images/game_over.png"))
        self.err_img = pygame.image.load(
            PathResolver.resource_path(
                "menu_images/err_message.png"))
        self.font = pygame.font.Font(None, 60)
        self.database = database

    def run(self, data: GameData) -> str | None:
        menu_x, menu_y = UILayout.get_menu_position()

        UILayout.draw_border(self.window)
        in_menu = True
        err = False
        string = ""
        while in_menu:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if not string.strip():
                            err = True
                            string = ""
                        else:
                            self.database.save_score(
                                {"name": string,
                                 "score": data.current_score})
                            return "menu"
                    if event.key == pygame.K_BACKSPACE:
                        string = string[:-1]
                    if len(string) < 10 and (event.unicode.isalnum() or
                                             event.unicode == " "):
                        string += event.unicode

            text = self.font.render(
                string,
                True,
                (255, 255, 0)
            )
            score = self.font.render(
                UILayout.validate_score(data.current_score),
                True,
                (255, 255, 0)
            )

            self.window.blit(self.menu_img, (menu_x, menu_y))
            self.window.blit(text, (menu_x + 290, menu_y + 760))
            self.window.blit(score, (menu_x + 400, menu_y + 500))
            if err:
                self.window.blit(self.err_img, (menu_x + 140, menu_y + 940))

            pygame.display.flip()
            pygame.time.delay(100)
        return None


class Victory:

    def __init__(self, window: pygame.surface.Surface,
                 database: DataBase) -> None:
        self.window = window
        self.menu_img = pygame.image.load(
            PathResolver.resource_path("menu_images/victory_menu.png"))
        self.err_img = pygame.image.load(
            PathResolver.resource_path("menu_images/err_message.png"))
        self.font = pygame.font.Font(None, 60)
        self.database = database

    def run(self, data: GameData) -> str | None:
        menu_x, menu_y = UILayout.get_menu_position()

        UILayout.draw_border(self.window)
        in_menu = True
        err = False
        string = ""
        while in_menu:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if not string.strip():
                            err = True
                            string = ""
                        else:
                            self.database.save_score({"name": string,
                                                      "score":
                                                      data.current_score})
                            return "menu"
                    if event.key == pygame.K_BACKSPACE:
                        string = string[:-1]
                    if len(string) < 10 and (event.unicode.isalnum() or
                                             event.unicode == " "):
                        string += event.unicode

            text = self.font.render(
                string,
                True,
                (255, 255, 0)
            )
            score = self.font.render(
                UILayout.validate_score(data.current_score),
                True,
                (255, 255, 0)
            )

            self.window.blit(self.menu_img, (menu_x, menu_y))
            self.window.blit(text, (menu_x + 290, menu_y + 840))
            self.window.blit(score, (menu_x + 410, menu_y + 610))
            if err:
                self.window.blit(self.err_img, (menu_x + 140, menu_y + 980))

            pygame.display.flip()
            pygame.time.delay(100)
        return None


class Menu:

    def __init__(self, window: pygame.surface.Surface,
                 database: DataBase) -> None:
        self.window = window
        self.menu_img = pygame.image.load(
            PathResolver.resource_path(
                "menu_images/menu.png"))
        self.images = [pygame.image.load(
            PathResolver.resource_path(
                "menu_images/startgame.png")),
                       pygame.image.load(
                        PathResolver.resource_path(
                            "menu_images/high_scores.png")),
                       pygame.image.load(
                        PathResolver.resource_path(
                            "menu_images/instruction.png")),
                       pygame.image.load(
                        PathResolver.resource_path(
                            "menu_images/exit.png"))]
        self.selected_images = [
            pygame.image.
            load(PathResolver.resource_path(
                "menu_images/selected_startgame.png")),
            pygame.image.
            load(PathResolver.resource_path(
                "menu_images/selected_high_scores.png")),
            pygame.image.
            load(PathResolver.resource_path(
                "menu_images/selected_instructions.png")),
            pygame.image.
            load(PathResolver.resource_path(
                "menu_images/selected_exit.png"))]

        self.instructions = Instructions(
                                        window,
                                        pygame.image.load(
                                            PathResolver.resource_path(
                                                "menu_images/"
                                                "instructions_menu.png")))
        self.score_board = Scoreboard(
                                        window,
                                        pygame.image.load(
                                            PathResolver.resource_path(
                                                "menu_images/"
                                                "score_board.png")))
        self.database: DataBase = database

    def run(self) -> str | None:
        menu_x, menu_y = UILayout.get_menu_position()
        BUTTON_WIDTH = 550
        buttons_x = menu_x + (menu_x - BUTTON_WIDTH) // 2

        UILayout.draw_border(self.window)
        buttons_y = [
                    menu_y + 390,
                    menu_y + 550,
                    menu_y + 710,
                    menu_y + 870,]
        in_menu = True
        selected = 0
        while in_menu:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(self.images)
                    elif event.key == pygame.K_UP:
                        selected = (selected - 1) % len(self.images)
                    elif event.key == pygame.K_RETURN:
                        if not selected:
                            return "gameplay"
                        if selected == 1:
                            self.score_board.run(self.database)
                        if selected == 2:
                            self.instructions.run()
                        if selected == 3:
                            return "exit"

            self.window.blit(self.menu_img, (menu_x, menu_y))

            for i, y in enumerate(buttons_y):
                if i == selected:
                    image = self.selected_images[i]
                else:
                    image = self.images[i]

                self.window.blit(image, (buttons_x, y))

            pygame.display.flip()
            pygame.time.delay(10)
        return None


class Pausemenu:

    def __init__(self, window: pygame.surface.Surface) -> None:
        self.window = window
        self.menu_img = pygame.image.load(
            PathResolver.resource_path(
                "menu_images/pause_menu.png"))
        self.images = [pygame.image.load(
            PathResolver.resource_path(
                "menu_images/resume_game.png")),
                       pygame.image.load(
                        PathResolver.resource_path(
                            "menu_images/return_menu.png"))]
        self.selected_images = [
                    pygame.image.load(
                        PathResolver.resource_path(
                            "menu_images/selected_resume_game.png")),
                    pygame.image.load(
                        PathResolver.resource_path(
                            "menu_images/selected_return_menu.png"))]

    def run(self) -> str | None:
        menu_x, menu_y = UILayout.get_menu_position()

        BUTTON_WIDTH = 550
        buttons_x = menu_x + (menu_x - BUTTON_WIDTH) // 2

        buttons_y = [
                    menu_y + 550,
                    menu_y + 710]

        UILayout.draw_border(self.window)

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

            for i, y in enumerate(buttons_y):
                if i == selected:
                    image = self.selected_images[i]
                else:
                    image = self.images[i]

                self.window.blit(image, (buttons_x, y))

            pygame.display.flip()
            pygame.time.delay(10)
        return None


class InGame:

    def __init__(self, window: pygame.surface.Surface,
                 adapter: Adapter) -> None:
        self.window = window
        self.adapter = adapter
        self.font = pygame.font.Font(None, 70)
        self.menu_img = pygame.image.load(
            PathResolver.resource_path(
                "menu_images/in_game_menu2.png"))
        self.live_img = pygame.image.load(
            PathResolver.resource_path(
                "menu_images/lives.png"))

    def run(self, data: GameData, timer: int) -> None:
        time_now = data.level_time - (pygame.time.get_ticks() - timer) // 1000
        lives = data.hearts
        x, y = self.adapter.start_drawing_point

        self.window.blit(self.menu_img, (x - 410, y))

        score_str = str(data.current_score)

        if len(score_str) < 10:
            displayed_score = score_str
        else:
            displayed_score = score_str[:9] + "..."

        text = self.font.render(displayed_score,
                                True, (255, 255, 255))
        self.window.blit(text, (x - 350, y + 300))

        if lives > 3:
            temp = str(lives)
            if len(temp) > 4:
                temp = temp[:4] + "..."
            text = self.font.render(f"X {temp}", True, (255, 255, 255))
            self.window.blit(self.live_img, (x - 350, y + 700))
            self.window.blit(text, (x - 250, y + 710))
        else:
            a = 0
            while lives:
                self.window.blit(self.live_img, (x - 350 + a, y + 700))
                a += 100
                lives -= 1

        text = self.font.render(str(data.level), True, (255, 255, 255))
        self.window.blit(text, (x - 230, y + 1080))

        text = self.font.render(str(time_now), True, (255, 255, 255))
        self.window.blit(text, (x - 240, y + 1400))
