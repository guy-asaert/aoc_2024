import cProfile
import sys
from functools import lru_cache
from itertools import permutations, product, combinations_with_replacement
from collections import namedtuple


KeyPad = namedtuple('KeyPad', ['pad', 'bad_pattern'])

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

# list of moves that are not allowed from a key
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

# list of moves that are not allowed from a key
BAD_DIRECTION_PAD_SEQUENCE = {
    '<': '^',
    'A': '<<',
    '<': '^',
}

KEY_PADS = (KeyPad(NUMERIC_PAD, BAD_NUMERIC_PAD_SEQUENCE), KeyPad(DIRECTION_PAD, BAD_DIRECTION_PAD_SEQUENCE))

NUMERIC_PAD_IDENTIFIER = 0
DIRECTION_PAD_IDENTIFIER = 1

SAMPLE_CODES = """029A
980A
179A
456A
379A"""
PUZZLE_CODES = """805A
682A
671A
973A
319A"""


@lru_cache(maxsize=None)
def get_taps(x_offset, y_offset):
    x_y_direction_taps = abs(x_offset) * ('<' if x_offset < 0 else '>') + abs(y_offset) * ('^' if y_offset < 0 else 'v') + 'A'
    y_x_direction_taps = abs(y_offset) * ('^' if y_offset < 0 else 'v') + abs(x_offset) * ('<' if x_offset < 0 else '>') + 'A'
    return x_y_direction_taps, y_x_direction_taps


cache = dict()

def move_from_to_next_pad_sequences(from_key, to_key, pad_identifier, level_number, max_level=3):
    global cache

    if (from_key, to_key, level_number) in cache:
        return cache[(from_key, to_key, level_number)]

    pad_key_locations = KEY_PADS[pad_identifier].pad
    from_location = pad_key_locations.get(from_key)
    to_location = pad_key_locations.get(to_key)
    if not from_location:
        raise ValueError(f"Invalid key {from_key}")
    if not to_location:
        raise ValueError(f"Invalid key {to_key}")
    
    # get the x and y offsets
    x_offset, y_offset = to_location[0] - from_location[0], to_location[1] - from_location[1]
    x_then_y, y_then_x = get_taps(x_offset, y_offset)
    bad_pattern = KEY_PADS[pad_identifier].bad_pattern.get(from_key, "xxxxxxxxxxxxxx")
    tap_sequences = [taps for taps in set([x_then_y, y_then_x]) if not taps.startswith(bad_pattern)]

    if level_number == max_level or len(tap_sequences[0]) < 2:
        cache[(from_key, to_key, level_number)] = len(tap_sequences[0])
        return len(tap_sequences[0])
    
    if len(tap_sequences) > 1:
        assert len(tap_sequences[0]) == len(tap_sequences[1])

    expanded_tap_sequence = []

    for tap_sequence in tap_sequences:
        this_expanded_tap_sequence = 0
        next_from_key = 'A'
        for next_to_key in tap_sequence:
            next_level_tap_sequences = move_from_to_next_pad_sequences(
                next_from_key, next_to_key, DIRECTION_PAD_IDENTIFIER, level_number + 1, max_level)
            # print(f"from_key: {next_from_key}, to_key: {next_to_key}, next_level_tap_sequences: {next_level_tap_sequences}")
            next_from_key = next_to_key
            this_expanded_tap_sequence += next_level_tap_sequences
        expanded_tap_sequence.append(this_expanded_tap_sequence)

    if len(expanded_tap_sequence) > 1:
        ret = min(expanded_tap_sequence) 
        cache[(from_key, to_key, level_number)] = ret
    else:
        ret = expanded_tap_sequence[0]
        cache[(from_key, to_key, level_number)] = ret

    return ret


def main():

    answer = 0
    for code in PUZZLE_CODES.split("\n"):
        from_key = 'A'
        total_taps = 0
        # my_code = ""
        for to_key in code:
            taps = move_from_to_next_pad_sequences(
                from_key, to_key, NUMERIC_PAD_IDENTIFIER, level_number=1, max_level=26)
            print(f'from_key: {from_key}, to_key: {to_key}, taps: {taps}')
            total_taps += taps
            # my_code += taps
            from_key = to_key
        answer += total_taps * int(code[:3])
        print(f"total_taps for code {code}: {total_taps * int(code[:3])}")
        print(f'The cache has {len(cache)} entries')

    print(f"Answer: {answer}")  

if __name__ == "__main__":
    main()