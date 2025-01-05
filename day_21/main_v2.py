
import cProfile
from functools import lru_cache

CODES = """029A
980A
179A
456A
379A"""

# CODES = """805A
# 682A
# 671A
# 973A
# 319A"""

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

# NUMERIC_ORDER_PREFERENCE = '^>v<'
NUMERIC_ORDER_PREFERENCE_V2 = '<v>^'

BAD_KEYS = {'0': '<', 'A': '<<', '7': 'vvv', '4': 'vv', '1': 'v'}

DIRECTION_PAD = {
    '<': (0, 1),
    '>': (2, 1),
    '^': (1, 0),
    'v': (1, 1),
    'A': (2, 0),
}

DIRECTION_ORDER_PREFERENCE = 'v>^<'

PADS = [NUMERIC_PAD, DIRECTION_PAD]

@lru_cache(maxsize=None)
def move_from_to(from_key, to_key, pad_index, order_preference):
    pad = PADS[pad_index]
    from_location = pad.get(from_key)
    to_location = pad.get(to_key)
    x_offset, y_offset = to_location[0] - from_location[0], to_location[1] - from_location[1]
    horizontal_taps = abs(x_offset) * ('<' if x_offset < 0 else '>')
    vertical_taps = abs(y_offset) * ('^' if y_offset < 0 else 'v')

    if horizontal_taps and vertical_taps:
        if order_preference.index(horizontal_taps[0]) < order_preference.index(vertical_taps[0]):
            part1 = horizontal_taps
            part2 = vertical_taps
        else:
            part1 = vertical_taps
            part2 = horizontal_taps

        bad = BAD_KEYS.get(from_key)
        if bad and part1.startswith(bad):
            direction_taps = part2 + part1
        else:
            direction_taps = part1 + part2
    else:
        direction_taps = horizontal_taps + vertical_taps

    return direction_taps + 'A'

@lru_cache(maxsize=None)
def move_from_to_pattern(current_key, pattern, pad_index, order_preference):
    key_pad_key_presses_list = []
    for key in pattern:
        # print(f"On {current_key} / Go to and tap {key}")
        key_pad_key_presses_list.append(move_from_to(current_key, key, pad_index, order_preference))
        current_key = key

    return key_pad_key_presses_list, current_key


def main():
    complexity = 0
    for code in CODES.split('\n'):
        key_presses_list = []
        current_key = 'A'
        for key in code:
            print(f"On {current_key} / Go to and tap {key}")
            key_presses_list.append(move_from_to(current_key, key, 0, NUMERIC_ORDER_PREFERENCE_V2))
            # key_presses_v2 += move_from_to(current_key, key, NUMERIC_PAD, NUMERIC_ORDER_PREFERENCE_V2)
            current_key = key

        # print(key_presses)
        # print(key_presses_v2)

        # key_presses = key_presses_v2
        ROBOTS = 25
        for i in range(ROBOTS):
            key_pad_key_presses_list = []

            current_key = 'A'
            # key_presses_list[0] = 'A' + key_presses_list[0]
            for key_presses in key_presses_list:
                presses, current_key = move_from_to_pattern(current_key, key_presses, 1, DIRECTION_ORDER_PREFERENCE)
                key_pad_key_presses_list.extend(presses)
                # for key in key_presses:
                #     print(f"On {current_key} / Go to and tap {key}")
                #     key_pad_key_presses_list.append(move_from_to(current_key, key, 1, DIRECTION_ORDER_PREFERENCE))
                #     current_key = key
            key_presses_list = key_pad_key_presses_list
            print((f'Robot {i + 1} key presses list: {len(key_presses_list)}'))

            # print(key_presses)
        code_complexity = sum([len(key_presses) for key_presses in key_presses_list])
        complexity += (code_complexity * int(code[:-1]))
        print(f"Complexity for {code}: {code_complexity} * {int(code[:-1])}")


    print(f"Complexity: {complexity}")

    #               3                                      7               9                         A
    #         ^     A         ^ ^            < <           A       > >     A           v v v         A
    #    <    A  >  A    <    A A    v  <    A A  > >   ^  A   v   A A  ^  A   v  <    A A A  >   ^  A
    # v<<A >>^A vA ^A v<<A >>^A A  v<A <A >>^A A vA A ^<A >A v<A >^A A <A >A v<A <A >>^A A A vA ^<A >A

    #               3                                  7               9                         A
    #         ^     A             <  <         ^ ^     A       > >     A           v v v         A
    #    <    A  >  A   v  < <    A  A  >   ^  A A  >  A   v   A A  ^  A   v  <    A A A  >   ^  A
    # v<<A >>^A vA ^A v<A <A A >>^A  A vA ^<A >A A vA ^A v<A >^A A <A >A v<A <A >>^A A A vA ^<A >A


if __name__ == "__main__":
    # profiler = cProfile.Profile()
    # profiler.enable()
    main()
    # profiler.disable()
    # profiler.print_stats(sort='time')

