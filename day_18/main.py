import heapq
from utils import read_lines

SAMPLE_INPUT = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""


def print_grid(grid, start, target):
    rows, cols = len(grid), len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if (r, c) == start:
                print("S", end="")
            elif (r, c) == target:
                print("T", end="")
            else:
                print(grid[r][c], end="")
        print()

def dijkstra(grid, start, target):
    rows, cols = len(grid), len(grid[0])
    distances = { (r, c): float('inf') for r in range(rows) for c in range(cols) }
    distances[start] = 0
    priority_queue = [(0, start)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == target:
            return current_distance

        for direction in directions:
            neighbor = (current_node[0] + direction[0], current_node[1] + direction[1])
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == '#':
                    continue
                distance = current_distance + 1
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

    return float('inf')

def solve_part1():
    # grid_width = 7
    # grid_height = 7
    grid_width = 71
    grid_height = 71

    bytes = list()
    # for row, report_line in enumerate(SAMPLE_INPUT.split("\n")):
    for row, report_line in enumerate(read_lines(__file__)):
        # print(report_line)
        bytes.append(tuple(int(i) for i in report_line.split(",")))

    grid = [[0] * grid_width for _ in range(grid_height)]
    for x, y in bytes[:1024]:
        grid[y][x] = '#'

    start_pos = (0, 0)
    target_pos = (grid_width-1, grid_height-1)
    # print_grid(grid, start_pos, target_pos)

    shortest_path_length = dijkstra(grid, start_pos, target_pos)
    print(f"Shortest path length: {shortest_path_length}")


def solve_part2():
    # grid_width = 7
    # grid_height = 7
    grid_width = 71
    grid_height = 71

    bytes = list()
    # for report_line in SAMPLE_INPUT.split("\n"):
    for report_line in read_lines(__file__):
        bytes.append(tuple(int(i) for i in report_line.split(",")))

    lower_bound = 0
    upper_bound = len(bytes)

    while lower_bound < upper_bound:
        mid = (lower_bound + upper_bound) // 2
        grid = [[0] * grid_width for _ in range(grid_height)]
        for x, y in bytes[:mid]:
            grid[y][x] = '#'

        start_pos = (0, 0)
        target_pos = (grid_width-1, grid_height-1)
        shortest_path_length = dijkstra(grid, start_pos, target_pos)
        if shortest_path_length == float('inf'):
            upper_bound = mid
        else:
            lower_bound = mid + 1

    print(f"First bytes that blocks the path: {bytes[mid]}")


if __name__ == "__main__":
    solve_part2()
