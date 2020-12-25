# Day 8: Handheld Halting
# Results: 458 / 191

from utils import *


def main():
    code = []
    for line in get_input_lines():
        parts = line.split(' ')
        code.append((parts[0], int(parts[1])))

    print('Part 1:', halting_problem(code)[1])

    for i, spot in enumerate(code):
        code_test = code[:]
        if code_test[i][0] == 'nop':
            code_test[i] = ('jmp', code_test[i][1])
        elif code_test[i][0] == 'jmp':
            code_test[i] = ('nop', code_test[i][1])

        r, v = halting_problem(code_test)
        if not r:
            print('Part 2:', v)


def halting_problem(code: List[Tuple[str, int]]) -> Tuple[bool, int]:
    pointer = 0
    acc = 0
    ran = set()
    while 0 <= pointer < len(code) and pointer not in ran:
        ran.add(pointer)
        if code[pointer][0] == 'acc':
            acc += code[pointer][1]
            pointer += 1
        elif code[pointer][0] == 'jmp':
            pointer += code[pointer][1]
        elif code[pointer][0] == 'nop':
            pointer += 1
    return pointer in ran, acc


if __name__ == '__main__':
    main()
