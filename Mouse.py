from Maze import Maze, Sprite
import time
import os
from colorama import Fore
import heapq

SPEED = 0.05

class Mouse:
    def __init__(self, maze: Maze):
        self.maze = maze
        self.x = 1
        self.y = maze.height - 2
        self.end_x = maze.width - 2
        self.end_y = 1
        self.stack = [] # stack to store the path
        self.visited = set() # set to track visited positions
        self.parent = {}

    def solve(self):
        # Priority queue to store nodes for A* search (f, g, h, x, y)
        # f = g + h, where g is the cost to get to the node and h is the hueristic estimate to the goal
        open_list = []
        heapq.heappush(open_list, (0, 0, self.x, self.y))

        g_cost = {} # Dictionary to store g-costs for each cell
        g_cost[(self.x, self.y)] = 0

        while open_list:
            f, g, cx, cy = heapq.heappop(open_list) # pop the node with the lowest f-cost

            # self.draw()

            if (self.maze.get_value(cx, cy).name == "end"):
                self.reconstruct_path((cx, cy))
                return True
            
            directions = [(-1, 0), (1, 0), (0, 1), (0, -1)] # Up, Down, Right, Left
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy

                if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height:
                    current_cell = self.maze.get_value(nx, ny)

                    if current_cell.name == "wall" or (nx, ny) in self.visited:
                        continue

                    new_g = g + 1 # cost to move to the neighbor is always 1
                    h = abs(nx - self.end_x) + abs(ny - self.end_y) # Manhattan distance heuristic
                    f = new_g + h # Total cost

                    if (nx, ny) not in g_cost or new_g < g_cost[(nx, ny)]:
                        g_cost[(nx, ny)] = new_g
                        heapq.heappush(open_list, (f, new_g, nx, ny))
                        self.parent[(nx, ny)] = (cx, cy)
                        self.visited.add((nx, ny))

        return False

    def reconstruct_path(self, end_pos):
        # Reconstruct the path from the end to start by following the parent cells
        # In this case, we directly mark the path by following the reconstructed steps
        path = []
        current = end_pos
        while current != (self.x, self.y):
            path.append(current)
            current = self.parent[current]
        path.reverse()

        # Mark the path cells
        for (px, py) in path:
            self.maze.set_value(px, py, Sprite(f"{Fore.RED}█{Fore.RESET}", "path"))
            time.sleep(SPEED / 2)
            os.system("clear")
            print(self.maze)
 
if __name__ == "__main__":
    while True:
        maze = Maze(47, 31)
        maze.build()  # Build the maze first
        mouse = Mouse(maze)  # Initialize the mouse with the maze
        mouse.solve()  # Start the maze solving process
        mouse.maze.save_to_file("solved_maze")