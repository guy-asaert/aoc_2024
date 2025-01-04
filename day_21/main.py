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
    direction_taps = abs(x_offset) * ('<' if x_offset < 0 else '>') + abs(y_offset) * ('^' if y_offset < 0 else 'v')
    permutations_of_taps = [''.join(k) for k in set(permutations(direction_taps))]
    bad_pattern = bad_pattern.get(from_key, "xxxxxxxxxx")
    permutations_of_taps = [tap + 'A' for tap in permutations_of_taps if not tap.startswith(bad_pattern)]

    # keep the shortest sequence
    shortest_sequence = min(len(tap) for tap in permutations_of_taps)
    permutations_of_taps = [tap for tap in permutations_of_taps if len(tap) == shortest_sequence]

    return permutations_of_taps

def tap_code(code, pad_index):
    taps = []
    code = 'A' + code
    for i in range(1, len(code)):
        taps += [move_from_to(code[i - 1], code[i], pad_index)]
    return taps

def main():
#     codes = """029A
# 980A
# 179A
# 456A
# 379A"""

#     codes = """805A
# 682A
# 671A
# 973A
# 319A"""

    codes = """319A"""

    complexity = 0
    for code in codes.split('\n'):
        all_tabs = set()
        taps = tap_code(code, 0)
        for tap in product(*taps):
            direction_taps = ''.join(tap)
            # print(direction_taps)
            all_tabs.add(direction_taps)

        all_direction_taps = set()
        for i in range(2):
            print(f'Iteration {i}')
            for direction_taps in all_tabs:
                direction_direction_taps = tap_code(direction_taps, 1)
                for direction_direction_tap in product(*direction_direction_taps):
                    next_level_direction_tabs = ''.join(direction_direction_tap)
                    all_direction_taps.add(next_level_direction_tabs)

            all_tabs = all_direction_taps
            # only keep the shortest sequences
            all_direction_taps = set()
        
        print(f'Code {code} has {len(all_tabs)} possible taps')
        shortest_sequence = min(len(tap) for tap in all_tabs)
        complexity += shortest_sequence * int(code[:3])

    print(complexity)


if __name__ == "__main__":
    # profiler = cProfile.Profile()
    # profiler.enable()
    main()
    # profiler.disable()
    # profiler.print_stats(sort='time')    