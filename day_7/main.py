from utils import read_lines
from itertools import product

SAMPLE_INPUT = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

def add(a, b):
    return a + b

def mul(a, b):
    return a * b

def concatenate(a, b):
    return int(str(a) + str(b))

def solve_part1():

    answer = 0
    # for row, report_line in enumerate(SAMPLE_INPUT.split("\n")):
    for row, report_line in enumerate(read_lines(__file__)):
        test_value, equation = report_line.split(":")
        test_value = int(test_value)
        numbers = [int(v) for v in equation.strip().split(" ")]
        for operators in product([add, mul, concatenate], repeat=len(numbers)-1):
            # print(operators)
            result = numbers[0]
            for i, op in enumerate(operators):
                result = op(result, numbers[i+1])
            # print(result)
            if result == test_value:
                print("found", test_value, numbers, operators)
                answer += test_value
                break
    print(f'Answer: {answer}')

if __name__ == "__main__":
    solve_part1()
