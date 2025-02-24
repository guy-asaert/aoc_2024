import cProfile
from functools import lru_cache
from itertools import permutations, product


NUMERIC_PAD = {
    '0': (1, 3),
    '1': (0, 2),
    '2': (1, 2),
    '3': (2, 2),
    '4': (0, 1),
    '5': (1, 1),
    '6': (2, 1),
    '7': (0, 0),
    '8': (1, 0),
    '9': (2, 0),
    'A': (2, 3),
    }

BAD_NUMERIC_PAD_SEQUENCE = {
    '7': 'vvv',
    '4': 'vv',
    '1': 'v',
    '0': '<',
    'A': '<<',
}

DIRECTION_PAD = {
    '<': (0, 1),
    '>': (2, 1),
    '^': (1, 0),
    'v': (1, 1),
    'A': (2, 0),
}

BAD_DIRECTION_PAD_SEQUENCE = {
    '^': '<',
    'A': '<<',
    '<': '^',
}

NUMERIC_PAD_IDENTIFIER = 0
DIRECTION_PAD_IDENTIFIER = 1

KEY_PADS = ((NUMERIC_PAD, BAD_NUMERIC_PAD_SEQUENCE), (DIRECTION_PAD, BAD_DIRECTION_PAD_SEQUENCE))

@lru_cache(maxsize=None)
def move_from_to(from_key, to_key, pad_index):
    pad, bad_pattern = KEY_PADS[pad_index]
    from_location = pad.get(from_key)
    to_location = pad.get(to_key)
    if not from_location:
        raise ValueError(f"Invalid key {from_key}")
    if not to_location:
        raise ValueError(f"Invalid key {to_key}")
    
    x_offset, y_offset = to_location[0] - from_location[0], to_location[1] - from_location[1]
    x_y_direction_taps = abs(x_offset) * ('<' if x_offset < 0 else '>') + abs(y_offset) * ('^' if y_offset < 0 else 'v')
    permutations_of_taps = [''.join(k) for k in set(permutations(x_y_direction_taps))]
    bad_pattern = bad_pattern.get(from_key, "xxxxxxxxxx")
    permutations_of_taps = [tap + 'A' for tap in permutations_of_taps if not tap.startswith(bad_pattern)]
    return permutations_of_taps

def tap_code(code, pad_index):
    taps = []
    from_code = 'A'
    for i in range(0, len(code)):
        all_possible_key_sequences = move_from_to(from_code, code[i], pad_index)
        taps += [all_possible_key_sequences]
        from_code = code[i]
    return taps

def main():
#     codes = """029A
# 980A
# 179A
# 456A
# 379A"""

    codes = """805A
682A
671A
973A
319A"""

    # codes = """319A"""
    current_pad = NUMERIC_PAD_IDENTIFIER
    number_of_pads = 3

    complexity = 0
    for code in codes.split('\n'):

        all_key_sequences = [[c] for c in code]

        for i in range(number_of_pads):
            next_level_key_sequences = []
            for combination_of_keys in product(*all_key_sequences):
                key_sequence = ''.join(combination_of_keys)
                ways_tap_code = tap_code(key_sequence, current_pad)
                next_level_key_sequences.extend(tap_code(key_sequence, current_pad))
            current_pad = DIRECTION_PAD_IDENTIFIER
            all_key_sequences = next_level_key_sequences

        pass


        all_tabs = set()
        taps = tap_code(code, NUMERIC_PAD_IDENTIFIER)
        for tap in product(*taps):
            direction_taps = ''.join(tap)
            # print(direction_taps)
            all_tabs.add(direction_taps)

        all_direction_taps = set()

        NUMBER_OF_ROBOTS_IN_CHAIN = 2
        for i in range(NUMBER_OF_ROBOTS_IN_CHAIN):
            print(f'Iteration {i}')
            for direction_taps in all_tabs:
                direction_direction_taps = tap_code(direction_taps, DIRECTION_PAD_IDENTIFIER)
                for direction_direction_tap in product(*direction_direction_taps):
                    next_level_direction_tabs = ''.join(direction_direction_tap)
                    all_direction_taps.add(next_level_direction_tabs)

            all_tabs = all_direction_taps
            # only keep the shortest sequences
            all_direction_taps = set()
        
        print(f'Code {code} has {len(all_tabs)} possible taps')
        shortest_sequence = min(len(tap) for tap in all_tabs)
        longest_sequence = max(len(tap) for tap in all_tabs)
        print(f'Shortest sequence {shortest_sequence}, Longest sequence {longest_sequence}')
        complexity += shortest_sequence * int(code[:3])

    print(complexity)


if __name__ == "__main__":
    # profiler = cProfile.Profile()
    # profiler.enable()
    main()
    # profiler.disable()
    # profiler.print_stats(sort='time')    