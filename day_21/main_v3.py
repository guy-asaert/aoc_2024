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
        cache[(from_key, to_key, level_number)] = tap_sequences[0]
        return tap_sequences[0]
    
    if len(tap_sequences) > 1:
        assert len(tap_sequences[0]) == len(tap_sequences[1])

    expanded_tap_sequence = []

    for tap_sequence in tap_sequences:
        this_expanded_tap_sequence = ""
        next_from_key = 'A'
        for next_to_key in tap_sequence:
            next_level_tap_sequences = move_from_to_next_pad_sequences(
                next_from_key, next_to_key, DIRECTION_PAD_IDENTIFIER, level_number + 1, max_level)
            # print(f"from_key: {next_from_key}, to_key: {next_to_key}, next_level_tap_sequences: {next_level_tap_sequences}")
            next_from_key = next_to_key
            this_expanded_tap_sequence += next_level_tap_sequences
        expanded_tap_sequence.append(this_expanded_tap_sequence)

    if len(expanded_tap_sequence) > 1:
        cache[(from_key, to_key, level_number)] = min(expanded_tap_sequence, key=lambda x: len(x))
        return min(expanded_tap_sequence, key=lambda x: len(x))
    else:
        cache[(from_key, to_key, level_number)] = expanded_tap_sequence[0]
        return expanded_tap_sequence[0]


# def generate_optimised_move_patrix(pad_identifier):

#     pad = KEY_PADS[pad_identifier].pad

#     # generate all possible movements
#     movements = set(combinations_with_replacement(pad.keys(), 2))
#     other_way_around = list()
#     for movement in movements:
#         other_way_around.append((movement[1], movement[0]))
#     movements.update(other_way_around)

#     # movements = [('A', '0')]
    
#     for from_key, to_key in movements:
#         move_options = move_from_to_next_pad_sequences(from_key, to_key, pad_identifier, level_number=0, max_level=2)
#         print(f"from_key: {from_key}, to_key: {to_key}, move_options: {move_options}")




def main():

    answer = 0
    for code in PUZZLE_CODES.split("\n"):
        from_key = 'A'
        total_taps = 0
        my_code = ""
        for to_key in code:
            taps = move_from_to_next_pad_sequences(
                from_key, to_key, NUMERIC_PAD_IDENTIFIER, level_number=1, max_level=22)
            print(f'from_key: {from_key}, to_key: {to_key}, taps: {len(taps)}')
            total_taps += len(taps)
            my_code += taps
            from_key = to_key
        answer += total_taps * int(code[:3])
        print(f"total_taps for code {code}: {total_taps * int(code[:3])}")
        print(f'The cache has {len(cache)} entries')

    print(f"Answer: {answer}")  

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    profiler.print_stats(sort='time')


# @lru_cache(maxsize=None)
# def move_from_to(from_key, to_key, key_pad_identifier, last_level=False):
#     key_pad = KEY_PADS[key_pad_identifier]
#     # only consider the x then y or y then x moves
#     from_location = key_pad.pad.get(from_key)
#     to_location = key_pad.pad.get(to_key)
#     if not from_location:
#         raise ValueError(f"Invalid key {from_key}")
#     if not to_location:
#         raise ValueError(f"Invalid key {to_key}")
#     x_offset, y_offset = to_location[0] - from_location[0], to_location[1] - from_location[1]
#     x_y_direction_taps, y_x_direction_taps = get_taps(x_offset, y_offset)

#     bad_pattern = key_pad.bad_pattern.get(from_key, "xxxxxxxxxxxxxx")
#     taps_choices = [taps for taps in set([x_y_direction_taps, y_x_direction_taps]) if not taps.startswith(bad_pattern)]

#     if len(taps_choices) > 1:
#         # we have more than one choice, so we need to see which is the best choice by looking at the next level
#         print(f"from_key: {from_key}, to_key: {to_key}, taps_choices: {taps_choices}")
#         if not last_level:
#             # which is the best tap sequence to use? We need to see what the shortest next level tap sequence is
#             shortest_tap_sequence = sys.maxsize
#             chosen_tap_sequence = None
#             for tap_choice in taps_choices:
#                 next_level_taps = tap_code('A' + tap_choice, [DIRECTION_PAD_IDENTIFIER])
#                 if next_level_taps < shortest_tap_sequence:
#                     shortest_tap_sequence = next_level_taps
#                     chosen_tap_sequence = tap_choice
#             print(f"from_key: {from_key}, to_key: {to_key}, chosen_tap_sequence: {chosen_tap_sequence}")
#             return chosen_tap_sequence

#     if len(taps_choices) > 1:
#         print(f"from_key: {from_key}, to_key: {to_key}, taps_choices: {taps_choices}")
#     return taps_choices[0]


# def tap_code(code, key_pad_chain):
#     number_of_taps = 0
#     for index, from_key in enumerate(code[:-1]):
#         key_pad_taps = move_from_to(from_key, code[index+1], key_pad_chain[0], len(key_pad_chain) == 1)
#         if len(key_pad_chain) > 1:
#             number_of_taps += tap_code('A' + key_pad_taps, key_pad_chain[1:])
#         else:
#             number_of_taps += len(key_pad_taps)

#     return number_of_taps
