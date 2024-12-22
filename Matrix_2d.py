import json

class Matrix_2d:
    def __init__(self, width: int = 0, height: int = 0, default_value=None):
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
    def set_value(self, x: int, y: int, value = None):
        if 0 <= x < self.width and 0 <= y < self.width:
            self.matrix[y][x] = self.default_value 
            if value is not None:
                self.matrix[y][x] = value
        else:
            print (f"Attempted to set a value outside of the matrix.\nValid ranges: ( x: (0-{self.width - 1}), y: (0-{self.height - 1}) )\nAttempt: ({x}, {y})")
    
    def fill(self, value = None):
        self.matrix = [[value for _ in range(self.width)] for _ in range(self.height)]
    def clear(self):
        self.fill(self.default_value)
    def reset(self):
        self.matrix = []
        self.default_value = None
        self.height = 0
        self.width = 0

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

    def transpose(self):
        self.matrix = [list(row) for row in zip(*self.matrix)]
        self.width, self.height = self.height, self.width

    def append_row(self, row_index: int = None, value = None):
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
    def fill_row(self, row_index: int = 0, value = None):
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

    def save_to_file(self, filename):
        DATA = {
            "width": self.width,
            "height": self.height,
            "default_value": self.default_value,
            "matrix": self.matrix
        }
        with open(f"{filename}.json", 'w') as file:
            json.dump(DATA, file, indent=4)
    def load_from_file(self, filename):
        try:
            with open(f"{filename}.json", 'r') as file:
                DATA = json.load(file)
                self.width = DATA.get('width')
                self.height = DATA.get('height')
                self.default_value = DATA.get('default_value')
                self.matrix = DATA.get('matrix')

                if not isinstance(self.width, int) or self.width <= 0:
                    raise ValueError(f"Invalid width: {self.width}")
                if not isinstance(self.height, int) or self.height <= 0:
                    raise ValueError(f"Invalid height: {self.height}")

                if len(self.matrix) != self.height:
                    raise ValueError(f"Matrix height {len(self.matrix)} does not match the expected height: {self.height}")
                
                for row in self.matrix:
                    if len(row) != self.width:
                        raise ValueError(f"Row length {len(row)} does not match the expected width: {self.width}")

        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.reset()
            print(f"Error loading file {filename}.json, reseting matrix to default settings: {e}")

        except ValueError as e:
            self.reset()
            print(f"Invalid data: {e}\nReset matrix to default settings.")
        
        else:
            print("File loaded into matrix successfully.")

if __name__ == "__main__":
    M1 = Matrix_2d(20, 20, default_value=0)
    M1.fill_row(row_index=3, value=1)
    M1.save_to_file("matrix")

    M2 = Matrix_2d()
    M2.load_from_file("matrix")
    M2.print_details()   
    if len(M2.matrix):
        M2.print()