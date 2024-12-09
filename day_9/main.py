from utils import read_lines

SAMPLE_INPUT = """2333133121414131402"""


def get_disk_data():
    disk_map = []

    # for row, report_line in enumerate(SAMPLE_INPUT.split("\n")):
    for row, report_line in enumerate(read_lines(__file__)):
        disk_map = [int(v) for v in report_line]

    disk_data = []
    for i, count in enumerate(disk_map):
        if i % 2 == 0:
            disk_data.extend( count * [i//2])
        else:
            disk_data.extend( count * ['.'])
    return disk_data

def solve_part1():
    disk_data = get_disk_data()
    
    while '.' in disk_data:
        free_Space = disk_data.index('.')
        disk_data[free_Space] = disk_data[-1]
        del disk_data[-1]

    check_sum = 0
    for loc, identity in enumerate(disk_data):
        check_sum += loc * identity

    print(f'Checksum is {check_sum}')

def solve_part2():
    disk_data = get_disk_data()

    disk_length = len(disk_data)
    current_id = disk_data[-1]
    disk_pattern = ''.join([v if v == '.' else 'x' for v in disk_data])
    while current_id > 0:
        start = disk_data.index(current_id)
        end = disk_length - disk_data[::-1].index(current_id)
        data_length = end - start
        search_pattern = data_length * '.'
        loc = disk_pattern.find(search_pattern)
        if loc != -1 and loc < start:
            disk_pattern = disk_pattern[:loc] + 'x' * data_length + disk_pattern[loc + data_length:]
            disk_data[loc: loc + data_length] = disk_data[start: end]
            disk_data[start: end] = search_pattern
        current_id -= 1
        # print(''.join([str(v) for v in disk_data]))

    check_sum = 0
    for loc, identity in enumerate(disk_data):
        if identity == '.':
            continue
        check_sum += loc * identity

    print(f'Checksum is {check_sum}')



if __name__ == "__main__":
    solve_part2()
