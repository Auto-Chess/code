from chess_position import ChessPosition


class ChessMove:
    def __init__(self, init_pos, final_pos):
        self.init_pos = init_pos
        self.final_pos = final_pos

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.init_pos == other.init_pos and self.final_pos == other.final_pos
        return False

    def __str__(self):
        return self.init_pos.__str__() + self.final_pos.__str__()
