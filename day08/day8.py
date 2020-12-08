# Day 8: Handheld Halting
# Results: 458 / 191

from utils import *


def main(lines: List[str]):

    code = []
    for line in lines:
        parts = line.split(' ')
        code.append((parts[0], int(parts[1])))

    for i, spot in enumerate(code):
        code_test = code[:]
        if code_test[i][0] == 'nop':
            code_test[i] = ('jmp', code_test[i][1])
        elif code_test[i][0] == 'jmp':
            code_test[i] = ('nop', code_test[i][1])

        r = halting_problem(code_test)
        if r is not None:
            print('halted', r)


def halting_problem(code):
    pointer = 0
    acc = 0
    ran = set()
    while True:
        if pointer < 0 or pointer >= len(code):
            return acc
        if pointer in ran:
            return None
        ran.add(pointer)
        if code[pointer][0] == 'acc':
            acc += code[pointer][1]
            pointer += 1
        elif code[pointer][0] == 'jmp':
            pointer += code[pointer][1]
        elif code[pointer][0] == 'nop':
            pointer += 1


if __name__ == '__main__':
    main(get_input_lines())
