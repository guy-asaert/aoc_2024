from collections import Counter, defaultdict
from utils import read_lines

SAMPLE_INPUT = """1
2
3
2024"""



def get_next_secret_number(secret_number):

    secret_number ^= 64 * secret_number
    secret_number %= 16777216

    secret_number ^= secret_number // 32
    secret_number %= 16777216

    secret_number ^= 2048 * secret_number
    secret_number %= 16777216

    return secret_number


pattern_payoff = Counter()

def solve_part1():

    result = 0
    # for row, report_line in enumerate(SAMPLE_INPUT.split("\n")):
    for row, report_line in enumerate(read_lines(__file__)):
        # print(report_line)
        secret_number = int(report_line)
        four_changes = []

        found_patterns = set()
        for i in range(2000):
            next_secret_number = get_next_secret_number(secret_number)
            change = (next_secret_number % 10) - (secret_number % 10)
            four_changes.append(change)
            if len(four_changes) >= 4:
                pattern = tuple(four_changes)
                if pattern not in found_patterns:
                    # if pattern == (-2,1,-1,3):
                    #     print(f'Found pattern: {next_secret_number % 10}')
                    found_patterns.add(pattern)
                    pattern_payoff[pattern] += next_secret_number % 10
                four_changes.pop(0)
            secret_number = next_secret_number
        result += secret_number
        # if row % 1000 == 0:
        #     print(f'Row {row}, result: {result}')

    most_bananas = 0
    pattern = None
    for key, value in pattern_payoff.items():
        if value > most_bananas:
            most_bananas = value
            pattern = key
    
    print(f'Result: {result}')
    print(f'Pattern: {pattern}, Bananas: {most_bananas}')

if __name__ == "__main__":
    solve_part1()
