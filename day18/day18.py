# Day 18: Operation Order
# Results: Slow

from utils import *
import re


def main():
    assert evaluate('2 * 3 + (4 * 5)', Part1) == 26
    assert evaluate('5 + (8 * 3 + 9 + 3 * 4 * 3)', Part1) == 437
    assert evaluate('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', Part1) == 12240
    assert evaluate('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', Part1) == 13632

    assert evaluate('1 + (2 * 3) + (4 * (5 + 6))', Part2) == 51
    assert evaluate('2 * 3 + (4 * 5)', Part2) == 46
    assert evaluate('5 + (8 * 3 + 9 + 3 * 4 * 3)', Part2) == 1445
    assert evaluate('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', Part2) == 669060
    assert evaluate('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', Part2) == 23340

    lines = get_input_lines()
    print('Part 1:', evaluate_lines(lines, Part1))
    print('Part 2:', evaluate_lines(lines, Part2))



def evaluate_lines(lines: List[str], cls: Callable[[str], 'Parser']) -> int:
    return sum(map(lambda t: evaluate(t, cls), lines))


def evaluate(text: str, cls: Callable[[str], 'Parser']) -> int:
    parser = cls(text)
    stack = []
    for t in parser.tokens:
        if isinstance(t, int):
            stack.append(t)
        elif t == '+':
            stack.append(stack.pop(-1) + stack.pop(-1))
        elif t == '*':
            stack.append(stack.pop(-1) * stack.pop(-1))
    return stack[0]


class Parser:

    def __init__(self, text: str):
        self.text = text.replace(' ', '')
        self.pointer = 0
        self.tokens = []
        self.parse()

    def parse(self):
        raise NotImplementedError

    def get(self) -> str:
        return self.text[self.pointer] if self.pointer < len(self.text) else None

    def accept(self):
        self.pointer += 1

    def expect(self, c):
        if self.get() != c:
            raise RuntimeError('Yer code be bad arrr')
        self.accept()


class Part1(Parser):

    def parse(self):
        self.parse1()
        while True:
            c = self.get()
            if c is None:
                break
            if c in '*+':
                self.accept()
                self.parse1()
                self.tokens.append(c)
            else:
                break

    def parse1(self):
        c = self.get()
        if c == '(':
            self.accept()
            self.parse()
            self.expect(')')
        elif c in '123456789':
            self.tokens.append(int(c))
            self.accept()


class Part2(Parser):

    def parse(self):
        self.parse1()
        while self.get() == '*':
            self.accept()
            self.parse1()
            self.tokens.append('*')

    def parse1(self):
        self.parse2()
        while self.get() == '+':
            self.accept()
            self.parse2()
            self.tokens.append('+')

    def parse2(self):
        if self.get() == '(':
            self.accept()
            self.parse()
            self.expect(')')
        else:
            self.tokens.append(int(self.get()))
            self.accept()


# The awful python solution

def main_badly():
    lines = get_input_lines()
    part1 = part2 = 0

    class Int:
        def __init__(self, i: int):
            self.i = i

        def __add__(self, other):
            return Int(self.i * other.i)

        def __mul__(self, other):
            return Int(self.i + other.i)

        def __sub__(self, other):
            return Int(self.i + other.i)

    for line in lines:
        line = re.sub('([0-9])', r'Int(\1)', line)
        part1 += eval(line.replace('+', '-').replace('*', '+')).i
        part2 += eval(line.replace('*', '?').replace('+', '*').replace('?', '+')).i

    print('Part 1, Badly:', part1)
    print('Part 2, Badly:', part2)


if __name__ == '__main__':
    main()
    main_badly()