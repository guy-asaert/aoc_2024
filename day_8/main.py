from utils import read_lines
from collections import defaultdict
import itertools
import numpy as np

SAMPLE_INPUT = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""



def solve_part1():

    grid = []
    antenae = defaultdict(list)
    # for row, report_line in enumerate(SAMPLE_INPUT.split("\n")):
    for row, report_line in enumerate(read_lines(__file__)):
        print(report_line)
        grid.append(list(report_line))
        for col, location in enumerate(list(report_line)):
            if location != '.':
                antenae[location].append(np.array((row, col)))
    
    columns = len(grid[0])
    rows = len(grid)

    def inside_grid(loc):
        return 0 <= loc[0] < rows and 0 <= loc[1] < columns
    
    anti_nodes = set()

    for key, value in antenae.items():
        print(key, value)
        for a1, a2 in itertools.combinations(value, 2):
            node_harmony = 0
            while inside_grid(a1 + node_harmony * (a2 - a1)):
                anti_node = a1 + node_harmony * (a2 - a1)
                anti_node.flags.writeable = False
                anti_nodes.add(tuple(anti_node))
                node_harmony += 1

            node_harmony = -1
            while inside_grid(a1 + node_harmony * (a2 - a1)):
                anti_node = a1 + node_harmony * (a2 - a1)
                anti_node.flags.writeable = False
                anti_nodes.add(tuple(anti_node))
                node_harmony -= 1
            

    print(len(anti_nodes))


if __name__ == "__main__":
    solve_part1()
