from utils import read_lines
from enum import Enum
from itertools import product

SAMPLE_INPUT = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

# 6, 0, 1, 4, 1, 4, 0, 7, 0, 1, 4, 0

class OpCode(Enum):
    adv = 0 #
    bxl = 1 #
    bst = 2 #
    jnz = 3 #
    bxc = 4 #
    out = 5 #
    bdv = 6
    cdv = 7


class Computer:
    def __init__(self, program, reg_A, reg_B, reg_C):
        self.program = program
        self.registers = {'A': reg_A, 'B': reg_B, 'C': reg_C}
        self.instruction_pointer = 0
        self.output = []

        self._instructon_map = {OpCode.adv: self._adv,
                                OpCode.bxl: self._bxl,
                                OpCode.bst: self._bst,
                                OpCode.jnz: self._jnz,
                                OpCode.bxc: self._bxc,
                                OpCode.out: self._out,
                                OpCode.bdv: self._bdv,
                                OpCode.cdv: self._cdv}

    def reset(self, reg_A, reg_B, reg_C):
        self.registers = {'A': reg_A, 'B': reg_B, 'C': reg_C}
        self.instruction_pointer = 0
        self.output = []

    def execute_instruction(self, instruction):
        opcode = OpCode(instruction[0])
        self._instructon_map[opcode](instruction[1])

    def _adv(self, operand):
        # print(f"A = A // pow(2, {self.combo_operand_str(operand)})", end='\t')
        self.registers['A'] = self.registers['A'] // pow(2, self.combo_operand_value(operand))
        # print((f"= {self.registers['A']}"))
        self.instruction_pointer += 2

    def _bxl(self, operand):
        # print(f"B = B ^ {operand}")
        self.registers['B'] ^= operand
        self.instruction_pointer += 2

    def _bst(self, operand):
        # print(f"B = {self.combo_operand_str(operand)} % 8")
        self.registers['B'] = self.combo_operand_value(operand) % 8
        self.instruction_pointer += 2

    def _jnz(self, operand):
        if self.registers['A'] != 0:
            # print(f">>>>>>>>>>>>>>>> Jump to {self.combo_operand_str(operand)}")
            self.instruction_pointer = operand
        else:
            # print(f"No jump")
            self.instruction_pointer += 2

    def _bxc(self, operand):
        # print(f"B = B ^ C")
        self.registers['B'] = self.registers['B'] ^ self.registers['C']
        self.instruction_pointer += 2

    def _out(self, operand):
        # print(f"Output {self.combo_operand_str(operand)} % 8")
        self.output.append(self.combo_operand_value(operand) % 8)
        self.instruction_pointer += 2

    def _bdv(self, operand):
        # print(f"B = A // pow(2,{self.combo_operand_str(operand)})")
        self.registers['B'] = self.registers['A'] // pow(2, self.combo_operand_value(operand))
        self.instruction_pointer += 2

    def _cdv(self, operand):
        # print(f"C = A // pow(2,{self.combo_operand_str(operand)})")
        self.registers['C'] = self.registers['A'] // pow(2, self.combo_operand_value(operand))
        self.instruction_pointer += 2

    def combo_operand_value(self, operand):
        if 0 <= operand <= 3:
            return operand
        elif operand == 4:
            return self.registers['A']
        elif operand == 5:
            return self.registers['B']
        elif operand == 6:
            return self.registers['C']
        else:
            raise ValueError(f"Invalid combo operand: {operand}")
    
    def combo_operand_str(self, operand):
        if 0 <= operand <= 3:
            return f"op({operand})"
        elif operand == 4:
            return "A"
        elif operand == 5:
            return "B"
        elif operand == 6:
            return "C"
        else:
            raise ValueError(f"Invalid combo operand: {operand}")
        
    def run_program(self):
        while self.instruction_pointer < len(self.program):
            instruction = (self.program[self.instruction_pointer], self.program[self.instruction_pointer + 1])
            # print(self)
            self.execute_instruction(instruction)
            # print(self)
            # print("=====================================")

    def __str__(self):
        s = "Registers: "
        s += f"A = {self.registers['A']:b}"
        s += f"/ B = {self.registers['B']:b}"
        s += f"/ C = {self.registers['C']:b}"
        return s

def solve_part1():
    # for row, report_line in enumerate(SAMPLE_INPUT.split("\n")):
    for row, report_line in enumerate(read_lines(__file__)):
        if 'Register A:' in report_line:
            reg_A = int(report_line.split(":")[1].strip())
        elif 'Register B:' in report_line:
            reg_B = int(report_line.split(":")[1].strip())
        elif 'Register C:' in report_line:
            reg_C = int(report_line.split(":")[1].strip())
        elif 'Program:' in report_line:
            program = [int(x) for x in report_line.split(":")[1].split(",")]

    computer = Computer(program, reg_A, reg_B, reg_C)
    computer.run_program()
    print(','.join(str(s) for s in computer.output))


def solve_part2():
    # for row, report_line in enumerate(SAMPLE_INPUT.split("\n")):
    for row, report_line in enumerate(read_lines(__file__)):
        if 'Register A:' in report_line:
            reg_A = int(report_line.split(":")[1].strip())
        elif 'Register B:' in report_line:
            reg_B = int(report_line.split(":")[1].strip())
        elif 'Register C:' in report_line:
            reg_C = int(report_line.split(":")[1].strip())
        elif 'Program:' in report_line:
            program = [int(x) for x in report_line.split(":")[1].split(",")]

    target_output = [2,4,1,3,7,5,4,2,0,3,1,5,5,5,3,0]

    computer = Computer(program, reg_A, reg_B, reg_C)
    
    step = 0
    mask = pow(2, 16*3) - 1 ^ 0b111
    reg_A = 0
    solutions = [0]
    while step < len(target_output):
        step += 1
        next_solutions = []
        while solutions:
            solution = solutions.pop()
            reg_A = solution
            reg_A <<= 3
            for i in range(8):
                reg_A &= mask
                reg_A |= i
                computer.reset(reg_A, reg_B, reg_C)
                computer.run_program()
                print(f"Output: {computer.output}")
                if computer.output == target_output[-step:]:
                    print(f"Solution found: {reg_A} ({computer.output} = {target_output[-step:]})")
                    next_solutions.append(reg_A)
        if not next_solutions:
            raise ValueError(f"No solution found for step {step}")
        solutions = next_solutions

    if solutions:
        reg_A = min(solutions)
        print(f"Solution found: {reg_A}")
        computer.reset(reg_A, reg_B, reg_C)
        computer.run_program()
        print(','.join(str(s) for s in computer.output))
        print(f"Target: {target_output}") 

       # for i, reg_a_parts in enumerate(product([0,1,2,3,4,5,6,7], repeat=16)):
    #     reg_A = 0
    #     for i, part in enumerate(reg_a_parts):
    #         reg_A |= part << (i * 3)
    #     computer.run_program()
    #     if i % 1000000 == 0:
    #         print(f"Checking step {i}")
            
    #     if computer.output == target_output:
    #         print(f"Solution found: {reg_A}")
    #         solutions.append(reg_a_parts)

    # while solutions:
    #     reg_a_parts = solutions.pop()
    #     number_of_parts = len(reg_a_parts)
    #     reg_A = 0
    #     for i, part in enumerate(reg_a_parts):
    #         reg_A |= part << (i * 3)
    #     for next_part in [0,1,2,3,4,5,6,7]:
    #         reg_AA = reg_A | (next_part << number_of_parts * 3)
    #         computer = Computer(program, reg_AA, reg_B, reg_C)
    #         computer.run_program()
    #         if computer.output[:number_of_parts-1] == target_output[:number_of_parts-1]:
    #             reg_a_parts_new = reg_a_parts + (next_part,)
    #             solutions.append(reg_a_parts_new)
    #             print(f"Reg AA = {reg_a_parts_new}: {','.join(str(s) for s in computer.output)}")

            # solutions = []
            # for next_part in [0,1,2,3,4,5,6,7]:
            #     reg_AA = reg_A | (next_part << 4 * 3)
            #     computer = Computer(program, reg_AA, reg_B, reg_C)
            #     computer.run_program()
            #     if computer.output[:3] == target_output[:3]:
            #        solutions.append(reg_AA)
            #        print(f"Reg AA = {reg_A}: {','.join(str(s) for s in computer.output)}")


    # mapping = {}
    # for i in range(8):
    #     reg_A = i
    #     computer = Computer(program, reg_A, reg_B, reg_C)
    #     computer.run_program()
    #     mapping[computer.output[0]] = reg_A
    #     print(f"Reg A = {reg_A}: {','.join(str(s) for s in computer.output)}")

    # input_code = 0
    # for i, program_code in enumerate((reversed(program[0:2]))):
    #     if i > 0:
    #         input_code <<= 3
    #     # print(f"{program}: {mapping[program_code]}")
    #     input_code |= mapping.get(program_code, 0)

    # print(f"Input code: {input_code}")
    # computer = Computer(program, input_code, reg_B, reg_C)
    # computer.run_program()
    # print(','.join(str(s) for s in computer.output))


def examples():
    # computer = Computer([5,0,5,1,5,4], 10, 0, 0)
    # computer.run_program()

    # computer = Computer([0,1,5,4,3,0], 2024, 0, 0)
    # computer.run_program()

    # computer = Computer([1,7], 0, 29, 0)
    # computer.run_program()

    computer = Computer([4,0], 0, 2024, 43690)
    computer.run_program()
    pass


if __name__ == "__main__":
    solve_part2()
