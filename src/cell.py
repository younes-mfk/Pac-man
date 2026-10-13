class Window:
    """ Class provide the scale of Window"""

    width = 2600
    height = 2000


class Cell:
    """ Class provide a Cell's wall representation"""

    def __init__(self) -> None:
        """ initialize the cell class attributes"""

        self.upper_wall = 0
        self.right_wall = 0
        self.lower_wall = 0
        self.left_wall = 0


class CellDimention:
    """ Class provide the scale of Cell"""

    width = 80
    height = 80
