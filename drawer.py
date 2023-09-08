from neopixel import NeoPixel
from machine import Pin


class _SubMatirx:
    def __init__(self, x0, y0, cols, rows, base_matrix):
        self.x0 = x0
        self.y0 = y0
        self.cols = cols
        self.rows = rows

        self.matrix = base_matrix

        assert self.x0 + self.cols <= base_matrix.cols
        assert self.y0 + self.rows <= base_matrix.rows

    @property
    def max_x(self):
        return self.x0 + self.cols
    
    @property
    def max_y(self):
        return self.y0 + self.rows

    def __setitem__(self, xy, color):
        x, y = xy
        x = x + self.x0
        y = y + self.y0
        
        if not(x in range(self.x0, self.max_x) and y in range(self.y0, self.max_y)):
            raise ValueError(f"{(x, y)} is outside sub matrix range: {((self.x0, self.max_x), (self.y0, self.max_y))}")

        self.matrix._set_led(x, y, color)

    def fill(self, color):
        for i in range(self.x0, self.max_x):
            for j in range(self.y0, self.max_y):
                self[i, j] = color

    def clear(self):
        self.fill((0, 0, 0))


class Matrix:
    def __init__(self, pin, cols, rows):
        self.cols = cols
        self.rows = rows
        self.pin = pin

        self._led_array = NeoPixel(Pin(pin), rows * cols)

    def _set_led(self, x, y, color):
        x = x if y % 2 == 0 else self.cols - 1 - x
        loc = self.cols * y + x
        self._led_array[loc] = color

    def create_sub_matrix(self, x0, y0, cols, rows):
        return _SubMatirx(x0, y0, cols, rows, self)

    def show(self):
        self._led_array.write()

    def clear(self):
        for _, sub_matrix in self._sub_matrices.items():
            sub_matrix.clear()
