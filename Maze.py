from Matrix_2d import Matrix_2d
import os
import random

class Sprite:
    def __init__(self, char, name):
        self.char = char
        self.name = name

    def __str__(self):
        return self.char
class Maze(Matrix_2d):
    def __init__(self, width, height):
        self.wall = Sprite("█", "wall")
        self.path = Sprite(" ", "path")
        self.start = Sprite(">", "start")
        self.end = Sprite(">", "end")
        super().__init__(width=width, height=height, default_value=self.wall)

    def build(self):
        self.generate_maze(0, 0)
        self.place_start()
        self.place_end()
        self.append_column(0)
        self.append_row(0)
        self.append_column()
        self.append_row()

    def generate_maze(self, x, y):
        # Mark the current cell as a path
        self.set_value(x, y, self.path)

        # Directions: (dx, dy) -> (left, right, up, down)
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]  # Move in steps of 2 (to carve out a path)
        random.shuffle(directions)  # Randomize the direction order for random maze generation

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Check if the new position is within bounds and if it's still a wall
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if self.get_value(nx, ny) == self.wall:  # Only carve through walls
                    # Carve the path
                    self.set_value(nx, ny, self.path)

                    # Carve the wall between the current cell and the next cell
                    self.set_value(x + dx // 2, y + dy // 2, self.path)

                    # Recursively call the function for the next position
                    self.generate_maze(nx, ny)
    
    def place_start(self):
        self.set_value(x=0, y=self.height - 1, value=Sprite(">", "start"))

    def place_end(self):
        self.set_value(x=self.width - 1, y=0,  value=Sprite(">", "end"))

    def make_border(self):
        self.fill_column(column_index=0, value=Sprite("█", 1))
        self.fill_row(row_index=0, value=Sprite("█", 1))
        self.fill_column(column_index=self.width - 1, value=Sprite("█", 1))
        self.fill_row(row_index=self.height - 1, value=Sprite("█", 1))

    def __str__(self):
        return self.to_string()
    
if __name__ == "__main__":
    os.system("clear")
    maze = Maze(51, 51)
    maze.build()
    print(maze)