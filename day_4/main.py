from utils import read_lines
import re

SAMPLE_INPUT = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

SEARCH_WORD = 'XMAS'

def solve_part1():
    total_count = 0
    # Read the input

    all_lines = []
    # for report_line in SAMPLE_INPUT.split("\n"):
    for report_line in read_lines(__file__):
        total_count += report_line.count(SEARCH_WORD)
        total_count += report_line[::-1].count(SEARCH_WORD)
        all_lines.append(report_line)

    for column in zip(*all_lines):
        total_count += "".join(column).count(SEARCH_WORD)
        total_count += "".join(column[::-1]).count(SEARCH_WORD)

    # diagonal
    right_diagonals = [[] for _ in range(len(all_lines[0]) + len(all_lines) - 1)]
    for i, line in enumerate(all_lines):
        for j, char in enumerate(line):
            column_index = i - j + len(all_lines) - 1
            right_diagonals[column_index].append(char)

    for diagional in right_diagonals:
        total_count += "".join(diagional).count(SEARCH_WORD)
        total_count += "".join(diagional[::-1]).count(SEARCH_WORD)

    left_diagonals = [[] for _ in range(len(all_lines[0]) + len(all_lines) - 1)]
    for i, line in enumerate(all_lines[::-1]):
        for j, char in enumerate(line):
            column_index = i - j + len(all_lines) - 1
            left_diagonals[column_index].append(char)

    for diagional in left_diagonals:
        total_count += "".join(diagional).count(SEARCH_WORD)
        total_count += "".join(diagional[::-1]).count(SEARCH_WORD)


    print(total_count)


def solve_part2():

    VALID_PATTERNS = ["MSAMS", "SMASM", "MMASS", "SSAMM"]
    all_lines = []
    # for report_line in SAMPLE_INPUT.split("\n"):
    for report_line in read_lines(__file__):
        all_lines.append(report_line)


    matches = 0
    searches = 0
    for col in range(len(all_lines[0]) - 2):
        for row in range(len(all_lines) - 2):
            searches += 1
            check_pattern = all_lines[row][col] + all_lines[row][col + 2] + all_lines[row + 1][col + 1] + \
                            all_lines[row + 2][col] + all_lines[row + 2][col + 2]
            if check_pattern in VALID_PATTERNS:
                matches += 1

    print(f"{matches} matches out of {searches} searches")


if __name__ == "__main__":
    solve_part2()

# 1919 is too low

