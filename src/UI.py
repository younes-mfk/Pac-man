"""Provide the game menus, end screens, layout, and HUD rendering."""


from paths import PathResolver
from adapter import Adapter
from db import DataBase
from typing import Tuple
from parse_config import GameData
import pygame
pygame.init()


border_margin = 50
border_width = 12

menu_width = 900
menu_hight = 1350


class UILayout:
    """Provide shared menu positioning, borders, and score formatting."""

    @staticmethod
    def draw_border(window: pygame.surface.Surface) -> None:
        """Draw a blue border around the game window.

        Args:
            window (pygame.surface.Surface): Surface on which to draw.

        Returns:
            None.
        """
        pygame.draw.rect(
            window,
            (0, 100, 255),
            (
                border_margin,
                border_margin,
                2600 - border_margin * 2,
                2000 - border_margin * 2
            ),
            border_width
        )

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
        self.font = pygame.font.Font(None, 60)

    def run(self, database: DataBase) -> None:
        """Show the ten best scores until ESC is pressed.

        Args:
            database (DataBase): Database from which the sorted scores
                are read.

        Returns:
            None.
        """
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
                valid_score = UILayout.validate_value(score['score'])
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
        self.font = pygame.font.Font(None, 60)
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
                UILayout.validate_value(data.current_score),
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
        self.font = pygame.font.Font(None, 60)
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
                UILayout.validate_value(data.current_score),
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
        self.font = pygame.font.Font(None, 70)
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

        score_str = str(data.current_score)

        if len(score_str) < 10:
            displayed_score = score_str
        else:
            displayed_score = score_str[:9] + "..."

        text = self.font.render(displayed_score,
                                True, (255, 255, 255))
        self.window.blit(text, (x - 350, y + 250))

        if lives > 3:
            temp = str(lives)
            if len(temp) > 4:
                temp = temp[:4] + "..."
            text = self.font.render(f"X {temp}", True, (255, 255, 255))
            self.window.blit(self.live_img, (x - 350, y + 590))
            self.window.blit(text, (x - 250, y + 600))
        else:
            a = 0
            while lives:
                self.window.blit(self.live_img, (x - 350 + a, y + 590))
                a += 100
                lives -= 1

        current_level = UILayout.validate_value(data.level)

        text = self.font.render(current_level, True, (255, 255, 255))
        self.window.blit(text, (x - 350, y + 900))

        current_time = UILayout.validate_value(time_now)

        text = self.font.render(current_time, True, (255, 255, 255))
        self.window.blit(text, (x - 350, y + 1200))

        if data.cheat_mode is True:
            text = self.font.render("ON", True, (255, 255, 255))
            self.window.blit(text, (x - 250, y + 1470))
        if data.cheat_mode is False:
            text = self.font.render("OFF", True, (255, 255, 255))
            self.window.blit(text, (x - 250, y + 1470))
