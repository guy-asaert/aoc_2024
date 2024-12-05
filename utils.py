import os


def read_lines(code_file, sample=False, conversion=None):
    with open(os.path.join(os.path.dirname(code_file), "sample.txt" if sample else "puzzle.txt"), 'r') as f:
        return [conversion(line) if conversion else line for line in f.read().splitlines()]


def iter_lines(code_file, file_name, conversion=None):
    with open(os.path.join(os.path.dirname(code_file), file_name), 'r') as f:
        for line in f.read().splitlines():
            yield conversion(line) if conversion else line
