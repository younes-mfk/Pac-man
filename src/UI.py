"""Provide the game menus, end screens, layout, and HUD rendering."""


from paths import PathResolver
from adapter import Adapter
from db import DataBase
from typing import Tuple
from parse_config import GameData
import pygame
from time import sleep
pygame.init()


class UILayout:
    """Provide shared menu positioning, borders, and score formatting."""

    characters = {"dot": pygame.image.load(
            PathResolver.resource_path("chars/dot.png"))}
    for char in "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        characters[char] = pygame.image.load(
            PathResolver.resource_path(f"chars/{char}.png"))

    @staticmethod
    def get_menu_position() -> Tuple:
        """Compute the top-left position that centers a menu on screen.

        Returns:
            Tuple: The (x, y) coordinates at which to blit a menu image
                so that it is centered in the window.
        """
        return ((2600 - 900) // 2, (2000 - 1350) // 2)

    @staticmethod
    def validate_value(score: int) -> str:
        """Format a number so that it fits inside a menu field.

        Values with fewer than seven digits are returned unchanged.
        Longer values are cut to six digits followed by an ellipsis.

        Args:
            score (int): The value (score, level, time, etc.) to format.

        Returns:
            str: The value as a string, truncated with "..." if too long.
        """
        score_str = str(score)
        if len(score_str) < 7:
            displayed_score = score_str
        else:
            displayed_score = score_str[:6] + "..."
        return displayed_score

    @staticmethod
    def draw_text(window: pygame.Surface, text: str, x: int, y: int) -> None:
        for c in text:
            if c == " ":
                x += 20
                continue
            if c != '.':
                c = c.upper()
                img = UILayout.characters[c]
                window.blit(img, (x, y))
                x += 33
            else:
                img = UILayout.characters["dot"]
                window.blit(img, (x, y))
                x += 10


class Instructions:
    """Display the instructions screen until the player leaves it."""

    def __init__(self, window: pygame.surface.Surface,
                 menu_img: pygame.surface.Surface) -> None:
        """Initialize the instructions screen.

        Args:
            window (pygame.surface.Surface): Surface on which to draw.
            menu_img (pygame.surface.Surface): Image of the instructions
                menu to display.

        Returns:
            None.
        """
        self.window = window
        self.menu_img = menu_img

    def run(self) -> None:
        """Show the instructions menu until ESC is pressed.

        Returns:
            None.
        """
        menu_x, menu_y = UILayout.get_menu_position()

        in_menu = True
        while in_menu:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.window.fill((0, 0, 0))
                        return

            self.window.blit(self.menu_img, (menu_x - 100, menu_y))

            pygame.display.flip()
            sleep(0.015)


class Scoreboard:
    """Display the high scores screen until the player leaves it."""

    def __init__(self, window: pygame.surface.Surface,
                 baord_img: pygame.surface.Surface) -> None:
        """Initialize the scoreboard screen.

        Args:
            window (pygame.surface.Surface): Surface on which to draw.
            baord_img (pygame.surface.Surface): Background image of the
                score board.

        Returns:
            None.
        """
        self.window = window
        self.board_img = baord_img

    def run(self, database: DataBase) -> None:
        """Show the ten best scores until ESC is pressed.

        Args:
            database (DataBase): Database from which the sorted scores
                are read.

        Returns:
            None.
        """
        menu_x, menu_y = UILayout.get_menu_position()

        in_menu = True
        scores = database.sorted_scores()
        name_x = 350
        score_x = 800
        while in_menu:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.window.fill((0, 0, 0))
                        return

            self.window.blit(self.board_img, (menu_x, menu_y))
            temp = 400
            for score in scores[:10]:
                valid_score = UILayout.validate_value(score['score'])

                UILayout.draw_text(self.window, score['name'],
                                   menu_x + name_x, menu_y + temp)
                UILayout.draw_text(self.window, valid_score, menu_x + score_x,
                                   menu_y + temp)

                temp += 60

            pygame.display.flip()
            sleep(0.015)


class GameOver:
    """Display the game over screen and record the player's score."""

    def __init__(self, window: pygame.surface.Surface,
                 database: DataBase) -> None:
        """Initialize the game over screen and load its images.

        Args:
            window (pygame.surface.Surface): Surface on which to draw.
            database (DataBase): Database in which the score is saved.

        Returns:
            None.
        """
        self.window = window
        self.menu_img = pygame.image.load(
            PathResolver.resource_path(
                "menu_images/game_over.png"))
        self.err_img = pygame.image.load(
            PathResolver.resource_path(
                "menu_images/err_message.png"))
        self.database = database

    def run(self, data: GameData) -> str | None:
        """Ask the player for a name and save the final score.

        The name accepts up to ten alphanumeric characters or spaces.
        Pressing ENTER with an empty name shows an error message;
        otherwise the score is saved and the screen closes.

        Args:
            data (GameData): Game data holding the current score.

        Returns:
            str | None: "menu" once the score has been saved, or None if
                the loop exits without saving.
        """
        menu_x, menu_y = UILayout.get_menu_position()
        in_menu = True
        err = False
        string = ""
        while in_menu:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if not string:
                            err = True
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

            score = UILayout.validate_value(data.current_score)

            self.window.blit(self.menu_img, (menu_x, menu_y))
            UILayout.draw_text(self.window, string, menu_x + 270, menu_y + 760)
            UILayout.draw_text(self.window, score, menu_x + 350, menu_y + 500)
            if err:
                self.window.blit(self.err_img, (menu_x + 140, menu_y + 940))

            pygame.display.flip()
            sleep(0.015)
        return None


class Victory:
    """Display the victory screen and record the player's score."""

    def __init__(self, window: pygame.surface.Surface,
                 database: DataBase) -> None:
        """Initialize the victory screen and load its images.

        Args:
            window (pygame.surface.Surface): Surface on which to draw.
            database (DataBase): Database in which the score is saved.

        Returns:
            None.
        """
        self.window = window
        self.menu_img = pygame.image.load(
            PathResolver.resource_path("menu_images/victory_menu.png"))
        self.err_img = pygame.image.load(
            PathResolver.resource_path("menu_images/err_message.png"))
        self.database = database

    def run(self, data: GameData) -> str | None:
        """Ask the player for a name and save the winning score.

        The name accepts up to ten alphanumeric characters or spaces.
        Pressing ENTER with an empty name shows an error message;
        otherwise the score is saved and the screen closes.

        Args:
            data (GameData): Game data holding the current score.

        Returns:
            str | None: "menu" once the score has been saved, or None if
                the loop exits without saving.
        """
        menu_x, menu_y = UILayout.get_menu_position()

        in_menu = True
        err = False
        string = ""
        while in_menu:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if not string:
                            err = True
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

            score = UILayout.validate_value(data.current_score)

            self.window.blit(self.menu_img, (menu_x, menu_y))
            UILayout.draw_text(self.window, string, menu_x + 275, menu_y + 840)
            UILayout.draw_text(self.window, score, menu_x + 350, menu_y + 610)
            if err:
                self.window.blit(self.err_img, (menu_x + 140, menu_y + 980))

            pygame.display.flip()
            sleep(0.015)
        return None


class Menu:
    """Display the main menu and handle navigation between its options."""

    def __init__(self, window: pygame.surface.Surface,
                 database: DataBase) -> None:
        """Initialize the main menu, its buttons, and its sub-screens.

        Args:
            window (pygame.surface.Surface): Surface on which to draw.
            database (DataBase): Database used by the scoreboard screen.

        Returns:
            None.
        """
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
        """Run the main menu loop.

        Use the UP and DOWN keys to change the selected button and
        ENTER to activate it.

        Returns:
            str | None: "gameplay" if the player starts the game,
                "exit" if the player quits, or None if the loop ends
                otherwise.
        """
        menu_x, menu_y = UILayout.get_menu_position()
        BUTTON_WIDTH = 550
        buttons_x = menu_x + (menu_x - BUTTON_WIDTH) // 2

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
            sleep(0.015)

        return None


class Pausemenu:
    """Display the pause menu during gameplay."""

    def __init__(self, window: pygame.surface.Surface) -> None:
        """Initialize the pause menu and load its images.

        Args:
            window (pygame.surface.Surface): Surface on which to draw.

        Returns:
            None.
        """
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
        """Run the pause menu loop.

        Use the UP and DOWN keys to change the selected button and
        ENTER to activate it.

        Returns:
            str | None: "gameplay" to resume the game, "menu" to return
                to the main menu, or None if the loop ends otherwise.
        """
        menu_x, menu_y = UILayout.get_menu_position()

        BUTTON_WIDTH = 550
        buttons_x = menu_x + (menu_x - BUTTON_WIDTH) // 2

        buttons_y = [
                    menu_y + 550,
                    menu_y + 710]

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
            sleep(0.015)
        return None


class InGame:
    """Render the in-game HUD (score, lives, level, time, cheat mode)."""

    def __init__(self, window: pygame.surface.Surface,
                 adapter: Adapter) -> None:
        """Initialize the HUD and load its images.

        Args:
            window (pygame.surface.Surface): Surface on which to draw.
            adapter (Adapter): Adapter providing the drawing start point
                of the maze, used to position the HUD.

        Returns:
            None.
        """
        self.window = window
        self.adapter = adapter
        self.menu_img = pygame.image.load(
            PathResolver.resource_path(
                "menu_images/in_game_menu2.png"))
        self.live_img = pygame.image.load(
            PathResolver.resource_path(
                "menu_images/lives.png"))
        self.top_bar = pygame.image.load(
            PathResolver.resource_path(
                "menu_images/top_bar.png"))

    def run(self, data: GameData, timer: int) -> None:
        """Draw the HUD for the current frame.

        Shows the score, remaining lives (as icons, or as a count when
        above three), the current level, the remaining time, and
        whether cheat mode is on.

        Args:
            data (GameData): Game data holding the score, lives, level,
                level time, and cheat mode state.
            timer (int): Tick value, in milliseconds, recorded when the
                level started; used to compute the remaining time.

        Returns:
            None.
        """
        time_now = data.level_time - (pygame.time.get_ticks() - timer) // 1000
        lives = data.hearts
        x, y = self.adapter.start_drawing_point

        self.window.blit(self.menu_img, (x - 410, y))
        self.window.blit(self.top_bar, (x - 410, y - 100))

        displayed_score = UILayout.validate_value(data.current_score)

        UILayout.draw_text(self.window, displayed_score, x - 350, y + 250)

        if lives > 3:
            temp = str(lives)
            if len(temp) > 4:
                temp = temp[:4] + "..."
            self.window.blit(self.live_img, (x - 350, y + 590))
            UILayout.draw_text(self.window, f"X{temp}", x - 270, y + 610)
        else:
            a = 0
            while lives:
                self.window.blit(self.live_img, (x - 350 + a, y + 590))
                a += 100
                lives -= 1

        current_level = UILayout.validate_value(data.level)

        UILayout.draw_text(self.window, current_level, x - 350, y + 900)

        current_time = UILayout.validate_value(time_now)

        UILayout.draw_text(self.window, current_time, x - 350, y + 1200)

        if data.cheat_mode is True:
            UILayout.draw_text(self.window, "ON", x - 250, y + 1470)
        if data.cheat_mode is False:
            UILayout.draw_text(self.window, "OFF", x - 250, y + 1470)
