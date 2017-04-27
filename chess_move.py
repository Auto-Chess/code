from chess_position import ChessPosition


class ChessMove:
    def __init__(self, init_pos, final_pos):
        if isinstance(init_pos, ChessPosition) and isinstance(final_pos, ChessPosition):
            self.init_pos = init_pos
            self.final_pos = final_pos
        else:
            raise TypeError("Parameters of ChessMove must be of type ChessPosition")

    def __str__(self):
        return self.init_pos.__str__() + self.final_pos.__str__()