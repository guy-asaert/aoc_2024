from functools import lru_cache
import sys
from utils import read_lines
from enum import Enum
from itertools import combinations
import cProfile
from typing import Dict, List, Optional, Tuple
from collections import Counter, defaultdict, namedtuple
import networkx as nx

SAMPLE_INPUT = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""

SAMPLE_INPUT2 = """x00: 0
x01: 1
x02: 0
x03: 1
x04: 0
x05: 1
y00: 0
y01: 0
y02: 1
y03: 1
y04: 0
y05: 1

x00 AND y00 -> z05
x01 AND y01 -> z02
x02 AND y02 -> z01
x03 AND y03 -> z03
x04 AND y04 -> z04
x05 AND y05 -> z00"""


class Operation(Enum):
    AND = 1
    OR = 2
    XOR = 3

Gate = namedtuple("Gate", "Wire1 Wire2 Operation")

def wires_to_int(wire_values: List[bool]) -> int:
    """
    Converts a list of boolean wire values to an integer.
    Each boolean value in the list represents a binary digit (bit), where True is 1 and False is 0.
    The list is interpreted in reverse order, with the first element being the least significant bit.
    Args:
        wire_values (List[bool]): A list of boolean values representing binary digits.
    Returns:
        int: The integer representation of the binary number.
    """

    result = 0
    for wire in reversed(wire_values):
        if wire:
            result |= 1
        result <<= 1
    result >>= 1
    return result


def int_to_wires(value: int, length: int) -> List[bool]:
    """
    Converts an integer to a list of boolean values representing its binary form.
    Args:
        value (int): The integer value to convert.
        length (int): The length of the resulting list of boolean values.
    Returns:
        List[bool]: A list of boolean values representing the binary form of the input integer.
                    Each boolean value corresponds to a bit in the binary representation, with the
                    least significant bit at index 0.
    """

    return [bool(value & (1 << i)) for i in range(length)]


def calculate_wire_value(
        wire: str, all_wire_values: Dict[str, Optional[bool]], gates: Dict[str, Tuple[str, Operation, str]], 
        depth: int = 0) -> Optional[bool]:
    if depth > 100:
        return None

    gate = gates[wire]
    if all_wire_values[gate.Wire1] is None:
        all_wire_values[gate.Wire1] = calculate_wire_value(gate.Wire1, all_wire_values, gates, depth + 1)

    if all_wire_values[gate.Wire2] is None:
        all_wire_values[gate.Wire2] = calculate_wire_value(gate.Wire2, all_wire_values, gates, depth + 1)

    if all_wire_values[gate.Wire1] is None or all_wire_values[gate.Wire2] is None:
        return None

    if gate.Operation == Operation.AND:
        return all_wire_values[gate.Wire1] and all_wire_values[gate.Wire2]
    elif gate.Operation == Operation.OR:
        return all_wire_values[gate.Wire1] or all_wire_values[gate.Wire2]
    elif gate.Operation == Operation.XOR:
        return all_wire_values[gate.Wire1] ^ all_wire_values[gate.Wire2]
    else:
        raise ValueError(f'Unknown operation: {gate.Operation}')


def execute_circuit(
        wire_values: Dict[str, Optional[bool]], gates: Dict[str, Tuple[str, Operation, str]], 
        z_wires: List[str]) -> Optional[Dict[str, Optional[bool]]]:
    """
    Resolve the circuit and return the wire values for the z wires.

    Args:
        wire_values (Dict[str, Optional[bool]]): Dictionary of wire name to wire value.
        gates (Dict[str, Tuple[str, Operation, str]]): Dictionary of wire name to (wire1, operation, wire2).
        z_wires (List[str]): List of z wires.

    Returns:
        Optional[Dict[str, Optional[bool]]]: The resolved wire values for the z wires, or None if the circuit cannot be resolved.
    """
    for wire in z_wires:
        wire_values[wire] = calculate_wire_value(wire, wire_values, gates)
        if wire_values[wire] is None:
            return None

    return wire_values


def solve_part1() -> None:
    wire_values: Dict[str, Optional[bool]] = dict()
    gates: Dict[str, Tuple[str, Operation, str]] = dict()
    # for row, report_line in enumerate(SAMPLE_INPUT.split("\n")):
    for row, report_line in enumerate(read_lines(__file__)):
        if ':' in report_line:
            wire, value = report_line.split(': ')
            print(f'wire: {wire}, value: {value}')
            wire_values[wire] = True if value == '1' else False
        # print(report_line)
        elif '->' in report_line:
            wire1, operation, wire2, _, wire3 = report_line.split()
            gates[wire3] = Gate(wire1, wire2, Operation[operation])
            if wire1 not in wire_values:
                wire_values[wire1] = None
            if wire2 not in wire_values:
                wire_values[wire2] = None
            if wire3 not in wire_values:
                wire_values[wire3] = None

    z_wires = sorted([wire for wire in wire_values if wire.startswith('z')])
    wire_values = execute_circuit(wire_values, gates, z_wires)

    print(f'Result: {wires_to_int([wire_values[wire] for wire in z_wires])}')


def swap_wires(
        gates: Dict[str, Tuple[str, Operation, str]], wire1: str, wire2: str) -> Dict[str, Tuple[str, Operation, str]]:
    gate1 = gates[wire1]
    gates[wire1] = gates[wire2]
    gates[wire2] = gate1
    return gates


def trace_circuit(gates: Dict[str, Tuple[str, Operation, str]], wire: str) -> set:
    wires = {wire}
    trace_wires = [wire]
    for wire in trace_wires:
        if wire not in gates:
            continue
        wire1, _, wire2 = gates[wire]
        wires.add(wire1)
        wires.add(wire2)
        trace_wires.append(wire1)
        trace_wires.append(wire2)

    return wires


def check_circuit(
        wire_values: Dict[str, Optional[bool]], gates: Dict[str, Tuple[str, Operation, str]], 
        x_wires: List[str], y_wires: List[str], z_wires: List[str]) -> set:
    """ Check if the circuit correctly calculates the sum of x and y
    Return the set of wires that are part of the circuit that connect to z wires that give an incorrect result

    :param wire_values: dictionary of wire name to wire value
    :param gates: dictionary of wire name to (wire1, operation, wire2)
    :param x_wires: list of x wires
    :param y_wires: list of y wires
    :param z_wires: list of z wires
    :return: set of wires that are part of the circuit that connect to z wires that give an incorrect result
    """
    wires_that_matter = set()
    wires_that_work = set()
    trouble_wires = dict()

    x = 1
    y = 1

    def calc(x: int, y: int) -> int:
        return x + y

    # only swap wires that are part of the circuit that connect to z wires that give an incorrect result
    # max_value = 1 << len(x_wires)

    for i_wire in range(len(x_wires)):

        for wire in wire_values.keys():
            wire_values[wire] = None

        x_value = int_to_wires(x, len(x_wires))
        for i, wire in enumerate(x_wires):
            wire_values[wire] = x_value[i]
        y_value = int_to_wires(y, len(y_wires))
        for i, wire in enumerate(y_wires):
            wire_values[wire] = y_value[i]

        new_wire_values = execute_circuit(wire_values, gates, z_wires)

        if not new_wire_values:
            return None
        z_wires_values = [new_wire_values[wire] for wire in z_wires]

        # check bitwise sum
        calced_value = calc(x, y)
        check_z_wires_values = int_to_wires(calced_value, len(z_wires))
        for i in range(len(z_wires_values)):
            if z_wires_values[i] != check_z_wires_values[i]:
                circuitry = trace_circuit(gates, z_wires[i])
                trouble_wires[z_wires[i]] = circuitry
                wires_that_matter.update(circuitry)
            else:
                ok_circuitry = trace_circuit(gates, z_wires[i])
                pass

        x <<= 1
        y <<= 1

    check_wires = wires_that_matter - wires_that_work
    return check_wires


def check_if_circuit_is_correct(
        wire_values: Dict[str, Optional[bool]], gates: Dict[str, Tuple[str, Operation, str]], 
        x_wires: List[str], y_wires: List[str], z_wires: List[str]) -> bool:
    """ Check if the circuit correctly calculates the sum of x and y
    :param wire_values: dictionary of wire name to wire value
    :param gates: dictionary of wire name to (wire1, operation, wire2)
    :param x_wires: list of x wires
    :param y_wires: list of y wires
    :param z_wires: list of z wires
    """
    x = 1
    y = 1

    def calc(x: int, y: int) -> int:
        return x + y

    for i_wire in range(len(x_wires)):
        for wire in wire_values.keys():
            wire_values[wire] = None

        x_value = int_to_wires(x, len(x_wires))
        for i, wire in enumerate(x_wires):
            wire_values[wire] = x_value[i]
        y_value = int_to_wires(y, len(y_wires))
        for i, wire in enumerate(y_wires):
            wire_values[wire] = y_value[i]

        new_wire_values = execute_circuit(wire_values, gates, z_wires)
        if not new_wire_values:
            return False

        z_wires_values = [new_wire_values[wire] for wire in z_wires]

        # check bitwise sum
        calced_value = calc(x, y)
        check_z_wires_values = int_to_wires(calced_value, len(z_wires))
        for i in range(len(z_wires_values)):
            if z_wires_values[i] != check_z_wires_values[i]:
                return False

        x <<= 1
        y <<= 1

    return True


@lru_cache(maxsize=None)
def get_all_pairings(elements: Tuple[str, ...]) -> List[List[Tuple[str, str]]]:
    if len(elements) == 2:
        return [[tuple(elements)]]  # Base case: only one pair possible

    first, rest = elements[0], elements[1:]
    pairings = []

    for second in rest:
        pair = (first, second)
        remaining = [e for e in rest if e != second]

        for sub_pairs in get_all_pairings(tuple(remaining)):
            pairings.append([pair] + sub_pairs)

    return pairings


def check_ancestors(ancestors, x_wires, y_wires) -> None:
    no_ancester_nodes = [wire for wire, count in ancestors.items() if count == 0]
    for x_wire in x_wires:
        if x_wire not in no_ancester_nodes:
            print(f'x_wire {x_wire} should have no ancestors')
    for y_wire in y_wires:
        if y_wire not in no_ancester_nodes:
            print(f'y_wire {y_wire} should have no ancestors')

def solve_part2() -> None:
    gates: Dict[str, Tuple[str, Operation, str]] = dict()
    wire_values: Dict[str, Optional[bool]] = dict()

    # for row, report_line in enumerate(SAMPLE_INPUT2.split("\n")):
    for _, report_line in enumerate(read_lines(__file__)):
        if ':' in report_line:
            # ignore the value. not needed here
            wire, value = report_line.split(': ')
        elif '->' in report_line:
            wire1, operation, wire2, _, wire3 = report_line.split()
            gates[wire3] = Gate(wire1, wire2, Operation[operation])
            wire_values[wire1] = None
            wire_values[wire2] = None
            wire_values[wire3] = None
    
    x_wires = sorted([wire for wire in wire_values.keys() if wire.startswith('x')])
    y_wires = sorted([wire for wire in wire_values.keys() if wire.startswith('y')])
    z_wires = sorted([wire for wire in wire_values.keys() if wire.startswith('z')])

    gates_out_wires = defaultdict(list)
    DG = nx.DiGraph()
    for node, gate in gates.items():
        gates_out_wires[gate.Operation].append(node)
        DG.add_edge(gate.Wire1, node)
        DG.add_edge(gate.Wire2, node)

    # check if all the z wires are connected to the same number of ancestors
    ancestors = Counter()
    previous = 6
    for wire in wire_values.keys():
        ancestors[wire] = len(nx.ancestors(DG, wire))
        
    # nothing fouund here btw
    check_ancestors(ancestors, x_wires, y_wires)

    # looks like z16, z21, z31 and z37 have a problem
    swap_wires_z = ['z16', 'z21', 'z31', 'z37']
    
    wires_to_swap = set()
    for wire in swap_wires_z:
        wires_to_swap.add(wire)
        wires_to_swap.update([wire for wire in nx.ancestors(DG, wire) if not wire.startswith('x') and not wire.startswith('y')])
        print(f"wire: {wire}, ancestors: {sorted(list(nx.ancestors(DG, wire)))}")

    pass




    previous = ancestors[z_wires[0]]
    for z_wire in z_wires[1:]:
        if ancestors[z_wire] - previous != 6:
            print(f"z_wire {z_wire} differs from previous by {ancestors[z_wire] - previous}")
        previous = ancestors[z_wire]

    non_xyz_ancestors = Counter()
    for wire, count in ancestors.items():
        if wire not in x_wires and wire not in y_wires and wire not in z_wires:
            non_xyz_ancestors[count] += 1
    
    def sum_circuit(x_value: int, y_value: int, x_wires, y_wires, z_wires) -> int:
        for wire, value in zip(x_wires, int_to_wires(x_value, len(x_wires))):
            wire_values[wire] = value
        for wire, value in zip(y_wires, int_to_wires(y_value, len(y_wires))):
            wire_values[wire] = value

        out_wires = execute_circuit(wire_values, gates, z_wires)
        return wires_to_int([out_wires[wire] for wire in z_wires])

    # run some test values through the circuit
    x_value = 0b111111111111111111111111111111111111111111111
    y_value = 0 # 0b111111111111111111111111111111111111111111111

    the_sum = sum_circuit(x_value, y_value, x_wires, y_wires, z_wires)
    if the_sum != x_value + y_value:
        difference = the_sum ^ (x_value + y_value)
        print(f"Expected {x_value + y_value}, got {the_sum}: difference: {bin(difference)}")
        # print(f"The circuit is not working correctly. Expected {x_value + y_value}, got {the_sum}")
    print(f"sum: {sum_circuit(x_value, y_value, x_wires, y_wires, z_wires)}")

    #  0b1111111110000001111111110111110000000000000000
    #    5432109876543210987654321098765432109876543210

    for wire, value in zip(x_wires, int_to_wires(x_value, len(x_wires))):
        wire_values[wire] = value
    for wire, value in zip(y_wires, int_to_wires(y_value, len(y_wires))):
        wire_values[wire] = value

    check_wires = execute_circuit(wire_values, gates, z_wires)
    binary_code = ''.join(['1' if wire_values[wire] else '0' for wire in reversed(z_wires)])

    # look at z16, z21, z31
    print(f'Result: {binary_code}') # 1111111111111101111111110111111111111111111110

    z_16_ancestors = nx.ancestors(DG, 'z16')


    z_21_ancestors = nx.ancestors(DG, 'z21')
    z_31_ancestors = nx.ancestors(DG, 'z31')
    z_37_ancestors = nx.ancestors(DG, 'z37')

    pass
    # print(f"check_wires: {','.join(sorted(check_wires))}")

    # all_wires = check_wires

    # for ix, wire_group in enumerate(combinations(all_wires, 8)):
    #     if ix > 200:
    #         break
    #     if ix % 100 == 0:
    #         print(f'Checking group {ix}')

    #     for swap_these_wires in get_all_pairings(tuple(wire_group)):
    #         for wire1, wire2 in swap_these_wires:
    #             gates = swap_wires(gates, wire1, wire2)

    #     check_wires = check_if_circuit_is_correct(wire_values, gates, x_wires, y_wires, z_wires)

    #     if check_wires:
    #         print(f"Found solution: {','.join(sorted(swap_these_wires))}")
    #         sys.exit(0)

    #     for wire1, wire2 in swap_these_wires:
    #         gates = swap_wires(gates, wire1, wire2)

    print("COMPLETE")


if __name__ == "__main__":
    # profiler = cProfile.Profile()
    # profiler.enable()
    solve_part2()
    # profiler.disable()
    # profiler.print_stats(sort='time')
