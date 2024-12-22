from Maze import Maze, Sprite
import time
import os
from colorama import Fore

SPEED = 0.05

class Mouse:
    def __init__(self, maze: Maze):
        self.maze = maze
        self.x = 1
        self.y = maze.height - 2
        self.path = []

    def solve(self):
        self.path.append((self.x, self.y))
        if self.explore(self.x, self.y):
            print("Solved.")
            self.mark_path()
        else:
            print("Impossible...?")

    def draw(self, x, y):
        self.maze.set_value(x, y, Sprite(f"{Fore.BLUE}█{Fore.RESET}", "mouse"))
        os.system("clear")
        print(self.maze)
        time.sleep(SPEED)
        self.maze.set_value(x, y, Sprite(" ", "visited"))

    def explore(self, x, y):
        if self.maze.get_value(x, y).name == "end":
            return True

        self.draw(x, y)

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height:
                current_cell = self.maze.get_value(nx, ny)
                if current_cell.name != "wall" and current_cell.name != "visited":
                    self.path.append((nx, ny))  # Add current position to path
                    if self.explore(nx, ny):
                        return True
                    # Instead of popping everything, only remove the last one and backtrack
                    self.path.pop()

        # If no valid move found, backtrack by one step
        if self.path:
            self.draw(x, y)
            last_x, last_y = self.path[-1]
            self.x, self.y = last_x, last_y
            return False

        return False
    
    def mark_path(self):
        for (x, y) in reversed(self.path):
            self.maze.set_value(x, y, Sprite(f"{Fore.RED}█{Fore.RESET}", "path"))
            time.sleep(SPEED)
            os.system('clear')
            print(self.maze)

if __name__ == "__main__":
    maze = Maze(17, 17)
    maze.build()  # Build the maze first
    
    mouse = Mouse(maze)  # Initialize the mouse with the maze
    mouse.solve()  # Start the maze solving process
    os.system("clear")
    print(maze)  # Display the maze with the solved path marked