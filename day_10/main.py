from utils import read_lines

SAMPLE_INPUT = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""



def solve_part1():

    map = []
    for row, report_line in enumerate(SAMPLE_INPUT.split("\n")):
    # for row, report_line in enumerate(read_lines(__file__)):
        row = [int(c) for c in report_line]
        map.append(row)
    
    pass

if __name__ == "__main__":
    solve_part1()
