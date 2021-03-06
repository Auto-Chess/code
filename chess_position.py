class ChessPosition:
    def __init__(self, col, row):
        self.col = col
        self.row = row

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, value):
        value = value.lower()
        if (value >= "a") and (value <= "h"):
            self._col = value
        else:
            raise ValueError("Value must be between a and h, was: {}".format(value))

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, value):
        if (value >= 1) and (value <= 8):
            self._row = value
        else:
            raise ValueError("Value must be between 1 and 8, was: {}".format(value))


    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.row == other.row and self.col == other.col
        return False

    def __str__(self):
        return self.col + str(self.row)

    def col_to_int(self):
        return ord(self.col) - 96 - 1
