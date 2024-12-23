import cProfile
from collections import defaultdict
from functools import lru_cache
from utils import read_lines

SAMPLE_INPUT = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""



towels_by_length = defaultdict(set)


@lru_cache(maxsize=None)
def match_pattern(pattern, match=""):
    global towels_by_length
    match_count = 0
    for length, towels in towels_by_length.items():
        match_string = pattern[len(match):len(match)+length]
        if match_string in towels:
            next_match = match + match_string
            if pattern == next_match:
                match_count += 1
            else:
                match_count += match_pattern(pattern, next_match)
    return match_count


def solve_part(part=1):

    global towels_by_length
    patterns = []
    # for row, report_line in enumerate(SAMPLE_INPUT.split("\n")):
    for row, report_line in enumerate(read_lines(__file__)):
        if row == 0:
            for towel in report_line.split(", "):
                towels_by_length[len(towel)].add(towel)
        elif report_line:
            patterns.append(report_line)

    match_count = 0
    for i_pattern, pattern in enumerate(patterns):
        print(f'Pattern {i_pattern}/{len(patterns)}')
        match_count += match_pattern(pattern)

    print(f'Matches: {match_count}')

if __name__ == "__main__":
    # profiler = cProfile.Profile()
    # profiler.enable()
    solve_part(part=2)
    # profiler.disable()
    # profiler.print_stats(sort='time')
