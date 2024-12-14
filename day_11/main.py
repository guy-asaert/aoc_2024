import cProfile
import pstats
from io import StringIO
from utils import read_lines
from functools import lru_cache

SAMPLE_INPUT = """125 17"""


@lru_cache(maxsize=None)
def generate_test_ranges():

    test_ranges = []
    lower_rannge = 0
    upper_range = 9
    for i in range(50):
        test_ranges.append((lower_rannge, upper_range))
        lower_rannge = upper_range + 1
        upper_range = 10 * upper_range + 9

    return test_ranges

@lru_cache(maxsize=None)
def split_stone(stone):
    test_ranges = generate_test_ranges()

    for i, (lower, upper) in enumerate(test_ranges):
        if lower <= stone <= upper:
            if i % 2 == 1:
                scaler = 10 ** (i // 2 + 1)
                stone_number = stone
                return stone_number // scaler, stone_number % scaler
            else:
                return None
    raise ValueError(f"Stone {stone} is out of range")


@lru_cache(maxsize=None)
def blink_stones(stone, blink_count, blinks):
    if blink_count == blinks:
        return 1
    
    if stone == 0:
        return blink_stones(1, blink_count + 1, blinks)
    
    split_stones = split_stone(stone)
    if split_stones:
        return blink_stones(split_stones[0], blink_count + 1, blinks) + blink_stones(split_stones[1], blink_count + 1, blinks)
    else:
        return blink_stones(stone * 2024, blink_count + 1, blinks)



def blink(blink_count):
    # for row, report_line in enumerate(SAMPLE_INPUT.split("\n")):
    stones = []
    for row, report_line in enumerate(read_lines(__file__)):
        stones.extend(int(v) for v in report_line.split(" "))

    number_of_stones = sum([blink_stones(stone, 0, blink_count) for stone in stones])
    
    print(f'There are {number_of_stones} stones after {blink_count} blinks')


def solve_part1():
    blink(25)


def solve_part2():
    blink(75)


if __name__ == "__main__":
    # profiler = cProfile.Profile()
    # profiler.enable()
    
    # solve_part1()
    solve_part2()

    # profiler.disable()
    # s = StringIO()
    # sortby = 'cumulative'
    # ps = pstats.Stats(profiler, stream=s).sort_stats(sortby)
    # ps.print_stats()
    # print(s.getvalue())
