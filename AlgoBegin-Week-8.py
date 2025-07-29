import sys
import heapq
import random


class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [["." for _ in range(width)] for _ in range(height)]

    def generate(self, num_monsters, num_traps, num_portals):
        """
        Generate a random maze with the given number of monsters, traps, and portals.
        """
        self.grid[0][0] = "S"
        self.grid[self.height - 1][self.width - 1] = "E"

        # Randomly place monsters, traps, and portals
        self._place_entities("M", num_monsters)
        self._place_entities("T", num_traps)
        self.portals = self._place_portals(num_portals)

    def _place_entities(self, entity, num_entities):
        """
        Randomly place entities in the maze.
        """
        for _ in range(num_entities):
            x, y = self._random_empty_cell()
            self.grid[y][x] = entity

    def _place_portals(self, num_portals):
        """
        Randomly place portals in the maze and return their coordinates.
        """
        portals = []
        for _ in range(num_portals):
            x, y = self._random_empty_cell()
            self.grid[y][x] = "P"
            portals.append((x, y))
        return portals

    def _random_empty_cell(self):
        """
        Return a random empty cell in the maze.
        """
        while True:
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            if self.grid[y][x] == ".":
                return x, y

    def print_maze(self):
        """
        Print the maze.
        """
        for row in self.grid:
            print(" ".join(row))


class PathFinder:
    def __init__(self, maze):
        self.maze = maze

    def dijkstra(self):
        """
        Implement Dijkstra's algorithm to find the shortest path from S to E.
        """
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        queue = [(0, 0, 0)]  # (cost, x, y)
        costs = {(0, 0): 0}

        while queue:
            cost, x, y = heapq.heappop(queue)

            if self.maze.grid[y][x] == "E":
                return cost

            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if self._is_valid_cell(nx, ny):
                    result = self._calculate_cost(cost, nx, ny)
                    if result is not None:
                        new_cost, tx, ty = result
                        if (tx, ty) not in costs or new_cost < costs[(tx, ty)]:
                            costs[(tx, ty)] = new_cost
                            heapq.heappush(queue, (new_cost, tx, ty))

        return -1  # No path found

    def _is_valid_cell(self, x, y):
        """
        Check if a cell is within the maze boundaries.
        """
        return 0 <= x < self.maze.width and 0 <= y < self.maze.height

    def _calculate_cost(self, cost, x, y):
        """
        Calculate the cost of moving to a cell.
        Returns (new_cost, new_x, new_y) or None.
        """
        cell_value = self.maze.grid[y][x]

        if cell_value == "T":
            return cost + 2, x, y
        elif cell_value == "M":
            new_cost = cost - 1
            return (new_cost, x, y) if new_cost >= 0 else None
        elif cell_value == "P":
            if len(self.maze.portals) == 2:
                other_portal = (
                    self.maze.portals[1]
                    if (x, y) == self.maze.portals[0]
                    else self.maze.portals[0]
                )
                return cost, other_portal[0], other_portal[1]
            else:
                return cost + 1, x, y  # fallback if single portal
        else:
            return cost + 1, x, y


def parse_input():
    """
    Parse the input from sys.stdin.
    """
    width, height = map(int, sys.stdin.readline().strip().split())
    num_monsters, num_traps, num_portals = map(
        int, sys.stdin.readline().strip().split()
    )
    return width, height, num_monsters, num_traps, num_portals


def main():
    width, height, num_monsters, num_traps, num_portals = parse_input()
    maze = Maze(width, height)
    maze.generate(num_monsters, num_traps, num_portals)
    maze.print_maze()
    path_finder = PathFinder(maze)
    min_cost = path_finder.dijkstra()
    print("Minimum cost:", min_cost)


if __name__ == "__main__":
    main()
