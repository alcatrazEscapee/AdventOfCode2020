# Day 8: Handheld Halting
# Results: 458 / 191

from utils import *


def main(lines: List[str]):
    code = Asm.parse(lines)
    print('Part 1:', halting_problem(code).accumulator)
    for i in range(len(code)):
        code_test = code[:]
        inst = code_test[i]
        if inst[0] in (Opcode.nop, Opcode.jmp):
            code_test[i] = (Opcode.nop if inst[0] == Opcode.jmp else Opcode.jmp, *inst[1:])
            r = halting_problem(code_test)
            if not r.running:
                print('Part 2:', r.accumulator)


def halting_problem(code: List[Tuple[int, ...]]) -> Asm:
    runner = Asm(code)
    runner.running = True
    hits = set()
    while runner.running and runner.pointer not in hits:
        hits.add(runner.pointer)
        runner.tick()
    return runner


if __name__ == '__main__':
    main(get_input_lines())
