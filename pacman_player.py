from moves import Move


class PacMan:
    def __init__(self, start_pos, speed=470):
        self.speed = speed
        self.start_pos = start_pos
        self.current_frame = start_pos

        self.mortal = True
        self.move = Move(start_pos, start_pos,
                         float(start_pos[0]),
                         float(start_pos[1]),
                         start_pos)

    def restart_move(self, pacman):
        pacman.move = Move(pacman.start_pos,
                           pacman.start_pos,
                           float(pacman.start_pos[0]),
                           float(pacman.start_pos[1]),
                           pacman.start_pos)
        pacman.current_frame = pacman.start_pos
