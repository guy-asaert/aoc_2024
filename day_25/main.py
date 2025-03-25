from utils import read_lines


class Schematic:
    def __init__(self, pattern):
        
        pin_heights = []
        for column in zip(*pattern):
            column_pattern = ''.join(column)
            pin_heights.append(column_pattern.count('#') - 1)
        self._pin_heights = tuple(pin_heights)

    def get_opposite(self):
        op = Schematic([])
        op._pin_heights = tuple([5 - h for h in self._pin_heights])
        return op


    def __hash__(self):
        return hash(self._pin_heights)

    def __eq__(self,other):
        if isinstance(other, self.__class__):
            # Ignoring .b attribute
            return self._pin_heights == other._pin_heights
        else:
            return NotImplemented

    def __repr__(self):
        return "Schematic(%s)" % (self._pin_heights)


def solve_part1():

    schematic = []
    locks =  set()
    keys = set()

    items = 0
    # for row, report_line in enumerate(SAMPLE_INPUT.split("\n"))
    for report_line in read_lines(__file__):
        if report_line == "":
            add_schematic = Schematic(schematic)
            if schematic[0] == '#####':
                assert add_schematic not in locks
                locks.add(add_schematic)
            else:
                assert add_schematic not in keys
                keys.add(add_schematic)
            schematic = []
            items += 1
        else:
            schematic.append(report_line)
        # print(report_line)
    assert items == len(locks) + len(keys)
    
    matching_lock_keys = 0
    for lock in locks:
        key = lock.get_opposite()
        if key in keys:
            matching_lock_keys += 1

    print("Matching lock keys: ", matching_lock_keys)
    return matching_lock_keys


if __name__ == "__main__":
    solve_part1()
    print("All done")
