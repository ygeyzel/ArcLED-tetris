from itertools import product


class Shape:
    def __init__(self, x, color, bricks_pattern):
        self.x = x
        self.y = 0
        self.color = color
        self._bricks_pattern = self._bricks_pattern_string_list_to_bool(bricks_pattern)

    @staticmethod
    def _bricks_pattern_string_list_to_bool(bricks_pattern_string_list):
        return [[ch == '0' for ch in string] for string in bricks_pattern_string_list]

    @property
    def pattern_dimensions(self):
        return len(self._bricks_pattern), len(self._bricks_pattern[0])

    @property
    def bricks_locations(self):
        return [
            (self.x + i, self.y + j) for (i, j) in product(range(self.pattern_dimensions[0]), range(self.pattern_dimensions[1])) if self._bricks_pattern[i][j]]

    def draw_on_submatrix(self, submatrix):
        for x, y in self.bricks_locations:
            submatrix[x, y] = self.color
