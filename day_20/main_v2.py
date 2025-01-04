
from collections import Counter
from utils import read_lines

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



OFFSETS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def find_path(walls, start, end):

    path = [start]

    current_loc = start
    while current_loc != end:
        row, col = current_loc
        for offset in OFFSETS:
            r, c = offset
            next_loc = (row+r, col+c)
            if next_loc not in walls and next_loc not in path:
                current_loc = (row+r, col+c)
                break
        path.append(current_loc)

    return path

def find_cheats(path, cheat_length, threshold):

    cheats = Counter()
    for i, path_loc in enumerate(path):
        for j in range(i + cheat_length + 1, len(path)):
            if abs(path[j][0] - path_loc[0]) + abs(path[j][1] - path_loc[1]) <= cheat_length:
                # print(f'Found cheat path from {i} to {j}')
                save_length = j - i - (abs(path[j][0] - path_loc[0]) + abs(path[j][1] - path_loc[1]))
                if save_length >= threshold:
                    cheats[save_length] += 1

    for length, count in cheats.items():
        print(f'There are {count} cheats that save {length} picoseconds')

    print(f'Puzzle answer is: {sum(cheats.values())}')


def main():
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

    path = find_path(walls, start, end)
    print(f'Nornal path length: {len(path)}')

    # now find the cheat paths
    cheat_length = 20
    find_cheats(path, cheat_length, 100)


if __name__ == "__main__":
    main()