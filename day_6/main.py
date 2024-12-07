from utils import read_lines
import re

SAMPLE_INPUT = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


guard_turns = { 
    ( 0, -1): ( 1,  0), 
    ( 1,  0): ( 0,  1), 
    ( 0,  1): (-1,  0), 
    (-1,  0): ( 0, -1) 
    }


def print_map(map):
    for row in map:
        print(row)


def is_guard_stuck(map, guard_location, guard_direction, lab_width, lab_height):
    
    visited_squares = set()
    visited_squares.add(guard_location)
    turning_points = set()

    while True:
        next_location = (guard_location[0] + guard_direction[0], guard_location[1] + guard_direction[1])
        if next_location[0] < 0 or next_location[0] >= lab_width or next_location[1] < 0 or next_location[1] >= lab_height:
            break
        if map[next_location[1]][next_location[0]] == "#": # turn
            if (guard_location, guard_direction) in turning_points:
                # stuck
                return visited_squares, True
            turning_points.add((guard_location, guard_direction))
            guard_direction = guard_turns[guard_direction]
        else:
            guard_location = next_location
            visited_squares.add(guard_location)
            # row_str = map[next_location[1]]
            # map[next_location[1]] = row_str[:next_location[0]]  + "X" + row_str[next_location[0] + 1:]
    
    return visited_squares, False


def solve_part1():
    # Read the input

    map = list()
    guard_location = (0, 0)
    guard_direction = (0, -1)
    lab_width = 0
    lab_height = 0
    # for row, report_line in enumerate(SAMPLE_INPUT.split("\n")):
    for row, report_line in enumerate(read_lines(__file__)):
        if '^' in report_line:
            guard_location = (report_line.index('^'), row)
        report_line = report_line.replace("^", ".")
        map.append(report_line)
        lab_width = max(lab_width, len(report_line))
        lab_height += 1
    
    visited_squares, is_struck = is_guard_stuck(map, guard_location, guard_direction, lab_width, lab_height)

    # part 2
    loops = 0
    for row in range(lab_height):
        for col in range(lab_width):
            if map[row][col] == ".":
                map[row] = map[row][:col] + "#" + map[row][col + 1:]
                visited_squares, is_struck = is_guard_stuck(map, guard_location, guard_direction, lab_width, lab_height)
                loops += 1 if is_struck else 0
                map[row] = map[row][:col] + "." + map[row][col + 1:]

    print(f'Visited {len(visited_squares)} squares. Loops: {loops}')

            
def solve_part2():
    pass

if __name__ == "__main__":
    solve_part1()

# 4453 is too low

