# AoC Utils

import re
import math
import functools

from collections import defaultdict
from enum import IntEnum, auto
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Tuple, TypeVar, Union


def get_input(path: str = './input.txt') -> str:
    with open(path) as f:
        return f.read().replace('\r', '')


def get_input_lines(path: str = './input.txt') -> List[str]:
    return get_input(path).split('\n')


def ints(text: str) -> Tuple[int, ...]:
    return tuple(map(int, re.findall('([\-+]?\d+)', text)))


def floats(text: str) -> Tuple[float, ...]:
    return tuple(map(float, re.findall('([\-+]?\d*(?:\d|\d\.|\.\d)\d*)', text)))


Number = TypeVar('Number', int, float)


# Geometry
def padd(x: Iterable[Number], y: Iterable[Number]) -> Tuple[Number, ...]:
    return tuple(a + b for a, b in zip(x, y))


def psub(x: Iterable[Number], y: Iterable[Number]) -> Tuple[Number, ...]:
    return tuple(a - b for a, b in zip(x, y))


def pmul(x: Iterable[Number], a: Number) -> Tuple[Number, ...]:
    return tuple(a * y for y in x)


def pdot(x: Iterable[Number], y: Iterable[Number]) -> Number:
    return sum(a * b for a, b in zip(x, y))


def pnorm1(x: Iterable[Number], y: Iterable[Number] = None) -> Number:
    if y is not None:
        x = psub(x, y)
    return sum(map(abs, x))


def pnorm2sq(x: Iterable[Number], y: Iterable[Number] = None) -> Number:
    if y is not None:
        x = psub(x, y)
    return sum(i * i for i in x)


def protccw(x: Tuple[Number, Number]) -> Tuple[Number, Number]:
    return -x[1], x[0]


def protcw(x: Tuple[Number, Number]) -> Tuple[Number, Number]:
    return x[1], -x[0]


def psign(x: Iterable[Number]) -> Tuple[Number, ...]:
    return tuple(sign(y) for y in x)


def pabs(x: Iterable[Number]) -> Tuple[Number, ...]:
    return tuple(abs(y) for y in x)


def pdiffs(x: Sequence[Number]) -> Tuple[Number, ...]:
    return tuple(x[i + 1] - x[i] for i in range(len(x) - 1))


def min_max(x: Iterable[Number]) -> Tuple[Number, Number]:
    return min(x), max(x)


def sign(a: Number) -> Number:
    return 0 if a == 0 else (-1 if a < 0 else 1)


def lcm(a: int, b: int) -> int:
    """ Return lowest common multiple. """
    return a * b // math.gcd(a, b)


def gcd_iter(sequence: Iterable[int]) -> int:
    """ Return greatest common divisor of a list """
    return functools.reduce(math.gcd, sequence)


def lcm_iter(sequence: Iterable[int]) -> int:
    return functools.reduce(lcm, sequence)


def mod_inv(x: Number, m: Number) -> int:
    return pow(x, -1, m)


def ray_int(start: Iterable[int], end: Iterable[int]) -> list:
    """ Returns a list of tuples of the points in a ray cast from start to end, not including either """
    deltas = psub(end, start)
    delta_gcd = gcd_iter(deltas)
    points = []
    if delta_gcd > 1:
        for d in range(1, delta_gcd):
            p = padd(start, pmul(deltas, d / delta_gcd))
            if all(int(x) == x for x in p):
                points.append(tuple(int(x) for x in p))
    return points


def make_grid(grid_text: str) -> Dict[Tuple[int, int], Optional[str]]:
    """ Constructs a dictionary based grid from an ASCII / character representation
    :param grid_text:
    :return:
    """
    grid = defaultdict(lambda: None)
    for y, line in enumerate(grid_text.split('\n')):
        for x, c in enumerate(line):
            grid[x, y] = c
    return grid


def print_grid(grid_objects: Dict[Tuple[int, int], Any], values_map: Optional[Dict[Any, str]] = None, padding: int = 0, reverse_y: bool = True, reverse_x: bool = False):
    """ Prints a grid, represented as a map from points to values, to the console.
    Default reverse_x = False, reverse_y = True uses quadrant IV sign convention (Right = +x, Down = +y)
    With reverse_y = True, uses quadrant I sign convention (Right = +x, Up = +y)
    """
    def pixel(p: Any) -> str:
        if values_map is None:
            return str(p)
        else:
            return values_map[p] if p in values_map else '?'

    min_x = min(p[0] for p in grid_objects.keys()) - padding
    max_x = max(p[0] for p in grid_objects.keys()) + padding
    min_y = min(p[1] for p in grid_objects.keys()) - padding
    max_y = max(p[1] for p in grid_objects.keys()) + padding
    range_x = range(max_x, min_x - 1, -1) if reverse_x else range(min_x, max_x + 1)
    range_y = range(min_y, max_y + 1) if reverse_y else range(max_y, min_y - 1, -1)

    print('\n'.join(''.join(pixel(grid_objects[(x, y)]) for x in range_x) for y in range_y))


class Cycle:
    """
    Computes a cycle, identified by a state transition map f: X -> X
    Allows for optimized operations using that cycle, such as computing the state at a far future location or slice, or computing the number of states between two points.
    """

    def __init__(self, start: Any, generator: Callable[[Any], Any]):
        self.generator = generator
        self.prefix = []
        self.cycle = []

        seen = set()
        state = start
        i = 0
        while state not in seen:
            seen.add(state)
            self.prefix.append(state)
            state = generator(state)
            i += 1

        index = self.prefix.index(state)
        self.cycle = self.prefix[index:]
        self.prefix = self.prefix[:index]

        self.period = len(self.cycle)
        self.prefix_len = len(self.prefix)

    def values(self, min_inclusive: int, max_exclusive: int) -> List[Tuple[Any, int]]:
        """ Get all the states and the number of each from the slice [min_inclusive, max_exclusive) """
        values = defaultdict(int)
        i = min_inclusive
        while i < self.prefix_len and i < max_exclusive:  # iterate prefix values
            values[self[i]] += 1
            i += 1
        while (i - self.prefix_len) % self.period != 0 and i < max_exclusive:  # iterate until we reach the start of a cycle
            values[self[i]] += 1
            i += 1
        for item in self.cycle:
            counts = 1 + (max_exclusive - 1 - i) // self.period
            if counts > 0:
                values[item] += counts
            i += 1
        return list(values.items())

    def __getitem__(self, item):
        """ Access an individual item of the cycle as if it was a list from [0, infinity). Supports bounded slicing. """
        if isinstance(item, int):
            if item < 0:
                raise TypeError('Cannot index a cycle with a negative value: %d' % item)
            if item < len(self.prefix):
                return self.prefix[item]
            else:
                return self.cycle[(item - len(self.prefix)) % len(self.cycle)]
        if isinstance(item, slice):
            if item.stop is None:
                raise TypeError('Slice of Cycle must be bounded')
            return [self[i] for i in range(0 if item.start is None else item.start, item.stop, 1 if item.step is None else item.step)]

    def __str__(self):
        return 'Cycle{prefix=%s, cycle=%s}' % (str(self.prefix), str(self.cycle))


class Opcode(IntEnum):
    nop = auto()
    acc = auto()
    jmp = auto()


class Asm:
    """ An abstraction for the yet-unnamed assembly code used in Day 8 """

    @staticmethod
    def parse(lines: List[str]) -> List[Tuple[Union[Opcode, int], ...]]:
        code = []
        for line in lines:
            opcode, *args = line.split(' ')
            code.append((Opcode[opcode], *map(int, args)))
        return code

    def __init__(self, code: List[Tuple[Union['Opcode', int], ...]]):
        self.code: List[Tuple[Union['Opcode', int], ...]] = code
        self.pointer: int = 0
        self.accumulator: int = 0
        self.running: bool = False

    def run(self) -> 'Asm':
        self.running = True
        while self.running:
            self.tick()
        return self

    def tick(self):
        if self.valid():
            opcode = self.code[self.pointer][0]
            if opcode == Opcode.nop:  # nop
                self.pointer += 1
            elif opcode == Opcode.acc:  # acc [value] -> increment the accumulator by [value]
                self.accumulator += self.code[self.pointer][1]
                self.pointer += 1
            elif opcode == Opcode.jmp:  # jmp [offset] -> unconditional branch by [offset]
                self.pointer += self.code[self.pointer][1]
        else:
            self.running = False

    def valid(self):
        return 0 <= self.pointer < len(self.code)

    def __str__(self):
        return 'Asm{p=%d, code[p]=%s, acc=%d}' % (self.pointer, str(self.code[self.pointer]) if self.valid() else '???', self.accumulator)

