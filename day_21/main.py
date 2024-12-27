from utils import read_lines
from itertools import permutations

SAMPLE_INPUT = """029A
980A
179A
456A
379A"""

DOOR_KEYPAD = {
    '7': (0, 0),
    '8': (1, 0),
    '9': (2, 0),
    '4': (0, 1),
    '5': (1, 1),
    '6': (2, 1),
    '1': (0, 2),
    '2': (1, 2),
    '3': (2, 2),
    '' : (0, 3),
    '0': (1, 3),
    'A': (2, 3)
}

ROBOT_KEYPAD = {
    '' : (0, 0),
    '^': (1, 0),
    'A': (2, 0),
    '<': (0, 1),
    'v': (1, 1),
    '>': (2, 1),
}


def type_code(key_pad_code, key_pads):

    if not key_pads:
        return key_pad_code
    
    current_key = 'A'
    current_key_pad = key_pads[0]

    all_key_pad_codes = []
    for next_key in key_pad_code:
        offset_x = current_key_pad[next_key][0] - current_key_pad[current_key][0]
        offset_y = current_key_pad[next_key][1] - current_key_pad[current_key][1]

        single_key_code = []

        offset_seq = ''
        if offset_x != 0:
            if offset_x < 0:
                offset_seq += '<' * abs(offset_x)
            elif offset_x > 0:
                offset_seq += '>' * offset_x

        if offset_y != 0:
            if offset_y < 0:
                offset_seq += '^' * abs(offset_y)
            elif offset_y > 0:
                offset_seq += 'v' * offset_y

        print(f'Type {next_key} from {current_key} with offset {offset_seq}')
        for code in set(permutations(offset_seq)):
            tap_code = ''.join(code) + 'A'
            print(f'Code: {tap_code}')
            single_key_code.append(type_code(tap_code, key_pads[1:]))

        all_key_pad_codes.append(single_key_code)
        current_key = next_key

    return all_key_pad_codes



def solve_part1():

    complexity = 0

    key_pads = [DOOR_KEYPAD, ROBOT_KEYPAD, ROBOT_KEYPAD, ROBOT_KEYPAD]

    for door_paypad_code in SAMPLE_INPUT.split('\n'):
        ret = type_code(door_paypad_code, key_pads)
        pass


    print(f'Complexity: {complexity}')


if __name__ == "__main__":
    solve_part1()
