# Day 18: Operation Order
# Results: Slow

from utils import *


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


def evaluate(text: str, cls: Callable[[str, bool], 'Parser'], debug: bool = False) -> int:
    parser = cls(text, debug)
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

    """
    Template for a recursive descent, deterministic LL(1) parser
    Handles basic tokenization (single characters, removing spaces, and single digit integers), and maintaining a token stack
    Also has basic debugging functionality (as debugging parsers is difficult enough)
    """

    def __init__(self, text: str, debug: bool = False):
        self.text = text.replace(' ', '')
        self.pointer = 0
        self.tokens = []
        self.debug = debug
        self.parse()

    def parse(self):
        raise NotImplementedError

    def get(self) -> str:
        return self.text[self.pointer] if self.pointer < len(self.text) else None

    def accept(self):
        self.pointer += 1

    def debug_print(self, *args):
        if self.debug:
            print('[Debug] -> \'%s\'' % self.text[self.pointer:self.pointer + 4], *args, ':', self.tokens[-1:-5:-1])


class Part1(Parser):

    """ S/SL Specification

    parse:
        @parse1
        {[
            | '+':
                @parse1
                .'+'
            | '*':
                @parse1
                .'*'
            | *:
                >
        ]};

    parse1:
        [
            | '(':
                @parse
                ')'
            | integer:
                .integer
        ];

    """

    def parse(self):
        self.debug_print('parse')
        self.parse1()
        while True:
            c = self.get()
            if c is None:
                break
            if c in '*+':
                self.debug_print('operator', c)
                self.accept()
                self.parse1()
                self.tokens.append(c)
            else:
                break
        self.debug_print('end')

    def parse1(self):
        self.debug_print('parse1')
        c = self.get()
        if c == '(':
            self.debug_print('expression')
            self.accept()
            self.parse()
            self.accept()
        elif c in '123456789':
            self.debug_print('int', c)
            self.tokens.append(int(c))
            self.accept()


class Part2(Parser):

    """ S/SL Specification

    parse:
        @parse1
        {[
            | '*':
                @parse1
                .'*'
        ]};

    parse1:
        @parse2
        {[
            | '+':
                @parse2
                .'+'
        ]};

    parse2:
        [
            | '(':
                @parse
                ')'
            | integer:
                .integer
        ];

    """

    def parse(self):
        self.debug_print('parse')
        self.parse1()
        while self.get() == '*':
            self.debug_print('operator *')
            self.accept()
            self.parse1()
            self.tokens.append('*')

    def parse1(self):
        self.debug_print('parse1')
        self.parse2()
        while self.get() == '+':
            self.debug_print('operator +')
            self.accept()
            self.parse2()
            self.tokens.append('+')

    def parse2(self):
        self.debug_print('parse2')
        if self.get() == '(':
            self.debug_print('expression')
            self.accept()
            self.parse()
            self.accept()
        else:
            self.debug_print('int', self.get())
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
