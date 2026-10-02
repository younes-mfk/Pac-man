
import pygame
from ghosts import Ghost
from mazegenerator.mazegenerator import MazeGenerator

pygame.init()
CELL_HIGHT = 80
CELL_WIDTH = 80
player_image = pygame.image.load("ghosts_images/player.png")
ghost_image = pygame.image.load("ghosts_images/ghost.png")

ghost = Ghost((1, 2), ghost_image, "randow")

x = 0
y = 0
x_reset = 10
y_reset = 15
starting_cell = (0, 0)


maze = MazeGenerator().maze


window = pygame.display.set_mode((2000, 2000))

breake = True


def draw_maze():
    for i, row in enumerate(maze):
        for j, col in enumerate(row):
            x = j * 80
            y = i * 80

            if col & 0B0001000:
                pygame.draw.line(window, (0, 0, 255), (x, y), (x, y + CELL_HIGHT), 4)
            if col & 0B00000001:
                pygame.draw.line(window, (0, 0, 255), (x, y), (x + CELL_WIDTH, y), 4)
            if j == len(row) - 1:
                pygame.draw.line(window, (0, 0, 255), (x + CELL_WIDTH, y), (x + CELL_WIDTH, y + CELL_HIGHT), 4)
            if i == len(maze) - 1:
                pygame.draw.line(window, (0, 0, 255), (x, y + CELL_HIGHT), (x + CELL_WIDTH, y + CELL_HIGHT), 4)


def check_wall(direction, starting_cell, next_cell):
    from_cell = maze[starting_cell[0]][starting_cell[1]]
    to_cell = maze[next_cell[0]][next_cell[1]]
    if direction == "right":
        if (from_cell & 0B00000010) or (to_cell & 0B00001000):
            return 0
    elif direction == "left":
        if from_cell & 0B00001000 or to_cell & 0B00000010:
            return 0
    elif direction == "up":
        if from_cell & 0B00000001 or to_cell & 0B00000100:
            return 0
    elif direction == "down":
        if from_cell & 0B00000100 or to_cell & 0B00000001:
            return 0
    return 1


draw_maze()
while breake:
    pygame.time.delay(150)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            breake = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RIGHT and x < 1200 - CELL_WIDTH - 64:
                next_cell = (starting_cell[0], starting_cell[1] + 1)
                if check_wall("right", starting_cell, next_cell):
                    x += 80
                    starting_cell = next_cell

            elif event.key == pygame.K_LEFT and x > CELL_WIDTH - 64:
                next_cell = (starting_cell[0], starting_cell[1] - 1)
                if check_wall("left", starting_cell, next_cell):
                    x -= 80
                    starting_cell = next_cell

            elif event.key == pygame.K_UP and y > CELL_HIGHT - 64:
                next_cell = (starting_cell[0] - 1, starting_cell[1])
                if check_wall("up", starting_cell, next_cell):
                    y -= 80
                    starting_cell = next_cell

            elif event.key == pygame.K_DOWN and y < 1200 - CELL_HIGHT - 64:
                next_cell = (starting_cell[0] + 1, starting_cell[1])
                if check_wall("down", starting_cell, next_cell):
                    y += 80
                    starting_cell = next_cell

    window.fill((0, 0, 0))

    draw_maze()

    window.blit(player_image, (x, y))
    window.blit(ghost.image, (ghost.current_coords[1] * CELL_WIDTH, ghost.current_coords[0] * CELL_HIGHT))

    ghost.current_coords = ghost.next_cell(maze, ghost.current_coords, starting_cell)

    if starting_cell == ghost.current_coords:
        print(starting_cell)

        window.fill((0, 0, 0))
        draw_maze()

        x = x_reset
        y = y_reset
        starting_cell = (0, 0)

        window.blit(player_image, (x, y))

        ghost.current_coords = ghost.spawn_point

        window.blit(ghost.image,(ghost.current_coords[1] * CELL_WIDTH, ghost.current_coords[0] * CELL_HIGHT))

    pygame.display.update()
