from utils import read_lines


SAMPLE_INPUT = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""


def is_safe(data):
    diffs = []
    for i in range(1, len(data)):
        diffs.append(data[i] - data[i - 1])

    if min(diffs) > 0 and max(diffs) <= 3:
        return True
    elif max(diffs) < 0 and min(diffs) >= -3:
        return True
    return False

def solve_part1():
    # Read the input
    # lines = read_lines(__file__)
    safe_data = 0
    # for report_lines in SAMPLE_INPUT.split("\n"):
    for report_lines in read_lines(__file__):
        input_data = []
        for line in report_lines.split():
            input_data.append(int(line))

        if is_safe(input_data):
            safe_data += 1
        else:
            for i in range(0, len(input_data)):
                input_data_dampended = input_data.copy()
                input_data_dampended.pop(i)
                if is_safe(input_data_dampended):
                    safe_data += 1
                    break

        # if min(diffs) > 0 and max(diffs) <= 3:
        #     safe_data += 1
        # elif max(diffs) < 0 and min(diffs) >= -3:
        #     safe_data += 1


    
    print(safe_data)




if __name__ == "__main__":
    solve_part1()

# wrong answers:
# 323
# 330
# 336
