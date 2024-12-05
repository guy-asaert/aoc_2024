from utils import read_lines
import re

SAMPLE_INPUT = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
SAMPLE_INPUT2 = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""

MUL_REGEX = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
DO_REGEX = re.compile(r"do\(\)")
DONT_REGEX = re.compile(r"don't\(\)")

def solve_part1():
    # Read the input
    result = 0
    # for report_lines in SAMPLE_INPUT2.split("\n"):
    collect = True
    for report_lines in read_lines(__file__):
        string_points_of_interest = dict()
        for do in re.finditer(DO_REGEX, report_lines):
            start, _ = do.span()
            string_points_of_interest[start] = "do"

        for dont in re.finditer(DONT_REGEX, report_lines):
            start, _ = dont.span()
            string_points_of_interest[start] = "dont"

        for match in re.finditer(MUL_REGEX, report_lines):
            start, _ = match.span()
            a, b = map(int, match.groups())
            string_points_of_interest[start] = a * b


        for loc in sorted(string_points_of_interest.keys()):
            a = string_points_of_interest[loc]
            if a == "do":
                collect = True
            elif a == "dont":
                collect = False
            
            if collect and isinstance(a, int):
                result += a

    if result >= 97728793:
        print("too high")
    print(result)


if __name__ == "__main__":
    solve_part1()

# 97728793 is too high

