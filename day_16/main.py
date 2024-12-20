from utils import read_lines
from dataclasses import dataclass, field
import copy
import sys
import heapq

SAMPLE_INPUT = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""

LEFT_TURN = {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}
RIGHT_TURN = {'N': 'E', 'W': 'N', 'S': 'W', 'E': 'S'}

@dataclass(order=True)
class Path:
    cost: int = field(compare=False)
    row: int = field(compare=False)
    col: int = field(compare=False)
    direction: str = field(default='E', compare=False)
    path: set = field(default_factory=set, compare=False)
    manhattan_distance: int = field(default=0, compare=True)

    def forward_step(self, end_goal):
        self.path.add((self.row, self.col))
        self.cost += 1
        if self.direction == 'N':
            self.row -=1
        elif self.direction == 'S':
            self.row += 1
        elif self.direction == 'E':
            self.col += 1
        elif self.direction == 'W':
            self.col -= 1

        self.manhattan_distance = abs(self.row - end_goal[0]) + abs(self.col - end_goal[1])

    def rotate(self, direction):
        self.cost += 1000
        if direction == 'L':
            self.direction = LEFT_TURN[self.direction]
        elif direction == 'R':
            self.direction = RIGHT_TURN[self.direction]

def print_maze(walls, paths, width, height):
    path_tiles = set()
    for path in paths:
        path_tiles.update(path.path)
    for row in range(height):
        for col in range(width):
            if (row, col) in walls:
                print("#", end="")
            elif (row, col) in path_tiles:
                print("O", end="")
            else:
                print(".", end="")
        print()

def solve_part1():
    walls = set()
    end_goal = None

    # for row, report_line in enumerate(SAMPLE_INPUT.split("\n")):
    for row, report_line in enumerate(read_lines(__file__)):
        print(report_line)
        for col, char in enumerate(report_line):
            if char == "#":
                walls.add((row, col))
            elif char == "S":
                start_pos = Path(0, row, col, manhattan_distance=abs(row - end_goal[0]) + abs(col - end_goal[1]))
            elif char == "E":
                end_goal = (row, col)

    paths = []
    heapq.heappush(paths, start_pos)

    solutions = []
    tile_min_cost = dict()
    min_solution_cost = sys.maxsize


    
    while(paths):
        path = heapq.heappop(paths)

        if (path.row, path.col) in path.path or path.cost > min_solution_cost:
            continue

        t ile_min_cost[(path.row, path.col)] = path.cost

        if (path.row, path.col) == end_goal:
            solutions.append(path)
            min_solution_cost = min(min_solution_cost, path.cost)
            continue

        forward_path = copy.deepcopy(path)
        forward_path.forward_step(end_goal)
        if (forward_path.row, forward_path.col) not in walls:
            heapq.heappush(paths, forward_path)

        left_path = copy.deepcopy(path)
        left_path.rotate('L')
        left_path.forward_step(end_goal)
        if (left_path.row, left_path.col) not in walls:
            heapq.heappush(paths, left_path)

        right_path = copy.deepcopy(path)
        right_path.rotate('R')
        right_path.forward_step(end_goal)
        if (right_path.row, right_path.col) not in walls:
            heapq.heappush(paths, right_path)

    min_cost = min(path.cost for path in solutions)
    print(f'Minimum cost is {min_cost}')

    best_path_tiles = set()
    best_paths = list()
    for path in solutions:
        if path.cost == min_cost:
            best_paths.append(path)
            best_path_tiles.update(path.path)

    width = max(col for col, _ in walls) + 1
    height = max(row for _, row in walls) + 1
    print_maze(walls, best_paths, width, height)
    print(f'Tiles along the best path: {len(best_path_tiles) + 1}')

if __name__ == "__main__":
    solve_part1()

