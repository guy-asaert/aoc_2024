from utils import read_lines


SAMPLE_INPUT = """3   4
4   3
2   5
1   3
3   9
3   3"""

def part1():
    # Read the input
    lines = read_lines(__file__)
    # lines = SAMPLE_INPUT.split("\n")

    input_data = []
    for line in lines:
        input_data.append(list(map(int, line.split())))

    list1, list2 = zip(*input_data)
    list1 = sorted(list(list1))
    list2 = sorted(list(list2))

    diff = [abs(x - y) for x, y in zip(list1, list2)]
    print(sum(diff))


def part2():
    # lines = SAMPLE_INPUT.split("\n")
    lines = read_lines(__file__)

    input_data = []
    for line in lines:
        input_data.append(list(map(int, line.split())))

    list1, list2 = zip(*input_data)
    similarity = 0
    for num in list1:
        similarity += list2.count(num) * num

    print(similarity)

if __name__ == "__main__":
    part2()
