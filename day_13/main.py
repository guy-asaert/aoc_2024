import re
from utils import read_lines
from collections import namedtuple

SAMPLE_INPUT = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""


Machine = namedtuple('Machine', ['ax', 'ay', 'bx', 'by', 'px', 'py'])

def solve_part1():

    machines = []
    # for report_line in SAMPLE_INPUT.split("\n"):
    for report_line in read_lines(__file__):r
        if 'Button A' in report_line or 'Button B' in report_line or 'Prize' in report_line:
            numbers = re.findall(r'\d+', report_line)
                    if 'Button A' in report_line:
                ax, ay = numbers
            elif 'Button B' in report_line:
                bx, by = numbers
            elif 'Prize' in report_line:
                px, py = numbers
                machines.append(Machine(int(ax), int(ay), int(bx), int(by), 10000000000000 + int(px), 10000000000000 + int(py)))
            else:
                raise ValueError(f"Invalid line: {report_line}")
    
    tokens = 0
    for machine_index, machine in enumerate(machines):
        print(machine)

        pb = (machine.ax * machine.py - machine.ay * machine.px) / (machine.ax * machine.by - machine.ay * machine.bx)
        pa = (machine.px - machine.bx * pb) / machine.ax
        if int(pa) == pa and int(pb) == pb:
            print(f"pa: {pa}, pb: {pb}")
            tokens += 3 * int(pa) + int(pb)
            continue
        else:
            print(f"No solution pa: {pa}, pb: {pb}")

            
    print(f"Total tokens: {tokens}")


if __name__ == "__main__":
    solve_part1()
