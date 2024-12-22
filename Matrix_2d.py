import os
import time

class Matrix_2d:
    def __init__(self, width: int, height: int, default_value=None):
        self.width = width
        self.height = height
        self.default_value = default_value
        self.matrix = [[default_value for _ in range(width)] for _ in range(height)]
    
    def get(self):
        return self.matrix
    def get_value(self, x: int, y: int):
        if (0 <= x < self.width and 0 <= y < self.height):
            return self.matrix[y][x]
        else:
            print(f"Attempted to get a value outside of the matrix.\nValid ranges: ( x: (0-{self.width - 1}), y: (0-{self.height - 1}) )\nAttempt: ({x}, {y})")
    
    def set(self, matrix):
        self.matrix = matrix
    def set_value(self, x: int, y: int, value=None):
        if 0 <= x < self.width and 0 <= y < self.width:
            self.matrix[y][x] = self.default_value 
            if value is not None:
                self.matrix[y][x] = value
        else:
            print (f"Attempted to set a value outside of the matrix.\nValid ranges: ( x: (0-{self.width - 1}), y: (0-{self.height - 1}) )\nAttempt: ({x}, {y})")
    
    def fill(self, value):
        self.matrix = [[value for _ in range(self.width)] for _ in range(self.height)]
    def clear(self):
        self.fill(self.default_value)

    def print(self):
        for row in self.matrix:
            print(' '.join(str(cell) if cell is not None else 'X' for cell in row))
    def print_details(self):
        print("Width:", self.width)
        print("Heigth:", self.height)
        print("Default value:", self.default_value)
    def to_string(self):
        strings = []
        for row in self.matrix:
            row_string = ''.join(str(cell) + str(cell) if cell is not None else '  ' for cell in row)
            strings.append(row_string)
        return "\n".join(strings)

    def rotate(self, dir: int = 1):
        """
        Rotates matrix 90 degrees, clockwise or counterclockwise

        {param} dir: 1 or -1, 1 being clockwise
        """
        if dir not in (1, -1):
            print("Rotate Error: incorrect direction parameter.")
            return
        
        if dir == 1:
            self.matrix = [list(row) for row in zip(*self.matrix[::-1])]
        if dir == -1:
            self.matrix = [list(row) for row in zip(*self.matrix)][::-1]
        self.width, self.height = self.height, self.width

    def append_row(self, row_index: int = None, value=None):
        if row_index is None:
            row_index = self.height  # Default to appending to the end
        elif not (0 <= row_index <= self.height):  # Check if index is valid
            print(f"Cannot append row: Row index {row_index} is out of bounds.")
            return

        new_row = [self.default_value if value is None else value for _ in range(self.width)]
        self.matrix.insert(row_index, new_row)
        self.height += 1
    def remove_row(self, row_index: int = 0):
        if 0 <= row_index < self.height:
            self.matrix.pop(row_index)
            self.height -= 1
        else:
            print(f"Cannot remove row: Row index {row_index} is out of bounds.")
    def fill_row(self, row_index: int = 0, value=None):
        if 0 <= row_index < self.height:
            self.matrix[row_index] = [self.default_value if value is None else value for _ in range(self.width)]
        else:
            print(f"Cannot fill row: Row index {row_index} is out of bounds.")

    def append_column(self, column_index: int = None, value=None):
        if column_index is None:
            column_index = self.width  # Default to appending to the end
        elif not (0 <= column_index <= self.width):  # Check if index is valid
            print(f"Cannot append column: Column index {column_index} is out of bounds.")
            return

        for row in self.matrix:
            row.insert(column_index, self.default_value if value is None else value)
        self.width += 1
    def remove_column(self, column_index: int = 0):
        if 0 <= column_index < self.width:
            for row in self.matrix:
                row.pop(column_index)
            self.width -= 1
        else:
            print(f"Cannot remove column: Column index {column_index} is out of bounds.")
    def fill_column(self, column_index: int = 0, value=None):
        if 0 <= column_index < self.width:
            for row in self.matrix:
                row[column_index] = self.default_value if value is None else value
        else:
            print(f"Cannot fill column: Column index {column_index} is out of bounds.")

    def get_adjacent(self, x, y):
        """
        Grab a list of the 8 bordering tiles in a matrix
        """
        adjacent_tiles = []
        directions = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

        for dx, dy in directions:
            new_x = x + dx
            new_y = y + dy

            if 0 <= new_x < self.width and 0 <= new_y < self.height:
                adjacent_tiles.append((new_x, new_y, self.get_value(new_x, new_y)))
        
        return adjacent_tiles

if __name__ == "__main__":
    column_index = 1
    row_index = 1
    column_mover = 1
    row_mover = 1
    M = Matrix_2d(30, 30)
    while True:
        column_index += column_mover
        row_index += row_mover
        if (column_index >= M.width - 1 or column_index < 2):
            column_mover *= -1
        if (row_index >= M.width - 1 or row_index < 2):
            row_mover *= -1
        os.system("clear")
        M.clear()
        M.append_column(row_index, "|")
        M.append_row(column_index, "=")
        M.set_value(row_index, column_index, "O")
        M.remove_column()
        M.remove_row()
        print(M.to_string())
        M.print_details()
        time.sleep(0.02)