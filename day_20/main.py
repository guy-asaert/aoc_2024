import sys
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum
import heapq
from utils import read_lines
import cProfile

SAMPLE_INPUT = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

sys.setrecursionlimit(10000)

def dijkstra(start, end, walls):
    
    def neighbors(node):
        row, col = node
        for r, c in [(row+1, col), (row-1, col), (row, col+1), (row, col-1)]:
            if (r, c) not in walls:
                yield (r, c)
    
    def heuristic(node):
        return abs(node[0] - end[0]) + abs(node[1] - end[1])
    
    def reconstruct_path(came_from, current):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.insert(0, current)
        return total_path
    
    open_set = {start}
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start)}
    
    while open_set:
        current = min(open_set, key=lambda node: f_score[node])
        if current == end:
            return reconstruct_path(came_from, current)
        
        open_set.remove(current)
        for neighbor in neighbors(current):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor)
                if neighbor not in open_set:
                    open_set.add(neighbor)
    
    return None

class CheatStatus(Enum):
    NOT_CHEATED = 0
    CHEATING = 1
    CHEATED = 2


OFFSETS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def my_dijkstra(start, end, walls, grid_width, grid_height, cheat_length = 0):

    distances = { (r, c): float('inf') for r in range(grid_height) for c in range(grid_width)}
    distances[start] = 0
    priority_queue = [(0, start, 0, CheatStatus.NOT_CHEATED)]

    while priority_queue:
        current_distance, current_node, cheat_count, cheat_status = heapq.heappop(priority_queue)

        if current_node == end:
            return current_distance

        for direction in OFFSETS:
            neighbor = (current_node[0] + direction[0], current_node[1] + direction[1])

            if neighbor[0] < 0 or neighbor[0] >= grid_height or neighbor[1] < 0 or neighbor[1] >= grid_width:
                continue

            if neighbor in walls:
                if cheat_status == CheatStatus.CHEATED: # hit a wall and we already cheated
                    continue
                cheat_count += 1
                if cheat_count >= cheat_length: # ran out of cheat steps
                    continue
            else:
                if cheat_status == CheatStatus.CHEATING:
                    cheat_count += 1
                if cheat_count >= cheat_length:
                    cheat_status = CheatStatus.CHEATED

            distance = current_distance + 1
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor, cheat_count, cheat_status))

    return float('inf')

@dataclass
class Path:
    current_x: int
    current_y: int
    path_travelled: set = field(default_factory=set)
    cheat_start: tuple = None
    cheat_end: tuple = None
    cheat_count: int = 0
    # cheat_status: CheatStatus = CheatStatus.NOT_CHEATED

def find_paths(all_paths, path, start, end, walls, 
               grid_width, grid_height, cheat_length = 0, best_path = float('inf')):

    if len(path.path_travelled) >= best_path:
        return

    if (path.current_x, path.current_y) == (end[0], end[1]):
        # print(f'Found path: {path.path_travelled}')
        all_paths[(path.cheat_start, path.cheat_end)] = len(path.path_travelled)
        if len(all_paths) % 1000 == 0:
            print(f'Found {len(all_paths)} paths')
        return
    
    for direction in OFFSETS:
        if (path.current_x + direction[0], path.current_y + direction[1]) in path.path_travelled:
            continue

        neighbour = Path(path.current_x + direction[0], path.current_y + direction[1], 
                         path.path_travelled, None, None, path.cheat_count)
        if neighbour.current_x < 0 or neighbour.current_x >= grid_height or \
           neighbour.current_y < 0 or neighbour.current_y >= grid_width:
            # outside the grid
            continue

        cheat_count = path.cheat_count
        cheat_start, cheat_end = path.cheat_start, path.cheat_end

        if (neighbour.current_x, neighbour.current_y) in walls:
            if cheat_end: # hit a wall and we already cheated
                continue
            cheat_count += 1
            if cheat_count >= cheat_length: # ran out of cheat steps
                continue
            if not cheat_start:
                cheat_start = (neighbour.current_x, neighbour.current_y)
        else:
            if cheat_start and not cheat_end:
                cheat_count += 1
            if cheat_length and cheat_count >= cheat_length:
                cheat_end = (neighbour.current_x, neighbour.current_y)

        neighbour.path_travelled.add((neighbour.current_x, neighbour.current_y))
        neighbour.cheat_count = cheat_count
        neighbour.cheat_start = cheat_start
        neighbour.cheat_end = cheat_end
        find_paths(all_paths, neighbour, start, end, walls, grid_width, grid_height, cheat_length, best_path)
        neighbour.path_travelled.remove((neighbour.current_x, neighbour.current_y))
        pass


def solve_part1():

    walls = set()
    start = None
    end = None
    
    # for row, report_line in enumerate(SAMPLE_INPUT.split("\n")):
    for row, report_line in enumerate(read_lines(__file__)):
        for col, char in enumerate(report_line):
            if char == "#":
                walls.add((row, col))
            elif char == "S":
                start = (row, col)
            elif char == "E":
                end = (row, col)
    
    print(f'Start: {start}')
    print(f'End: {end}')

    grid_width = max(col for row, col in walls) + 1
    grid_height = max(row for row, col in walls) + 1

    print(f'Path locations: {grid_width * grid_height - len(walls)}')

    all_paths = dict()
    find_paths(all_paths, Path(start[0], start[1]), start, end, walls, grid_width, grid_height, 0)
    best_no_cheat_path = min([no_cheat_path for no_cheat_path in all_paths.values()])
    print(f'Best no cheat path: {best_no_cheat_path}')

    all_cheat_paths = dict()
    find_paths(all_cheat_paths, Path(start[0], start[1]), start, end, walls, grid_width, grid_height, 2, best_no_cheat_path)

    count_cheats = Counter(all_cheat_paths.values())
    for path_length in sorted(count_cheats.keys()):
        if best_no_cheat_path - path_length > 0:
            print(f'There are {count_cheats[path_length]} cheats that save {best_no_cheat_path - path_length} picoseconds')

    # pass


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    solve_part1()
    profiler.disable()
    profiler.print_stats(sort='time')
