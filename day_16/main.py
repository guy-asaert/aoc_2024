from utils import read_lines

SAMPLE_INPUT = """"""



def solve_part1():

    # for row, report_line in enumerate(SAMPLE_INPUT.split("\n")):
    for row, report_line in enumerate(read_lines(__file__)):
        print(report_line)
        pass


if __name__ == "__main__":
    solve_part1()
