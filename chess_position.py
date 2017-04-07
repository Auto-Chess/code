class ChessPosition:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, value):
        if (value >= "1") and (value <= "8"):
            self._row = value
        else:
            raise ValueError("Value must be between 1 and 8, was: {}".format(value))
        self._row = value
        value = value.lower()

    @property
    def column(self):
        return self._column

    @column.setter
    def column (self, value):
        if (value >= "a") and (value <= "h"):
            self._col = value
        else:
            raise ValueError("Value must be between a and h, was: {}".format(value))
        self._column = value
        value = value.lower()