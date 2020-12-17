# AoC Utils

import re
import math
import functools
import itertools

from collections import defaultdict, deque
from enum import IntEnum, auto
from typing import Any, Callable, Dict, Iterable, Iterator, List, Optional, Sequence, Set, Tuple, Union


def get_input(path: str = './input.txt') -> str:
    with open(path) as f:
        return f.read()


def get_input_lines(path: str = './input.txt') -> List[str]:
    return get_input(path).split('\n')


def ints(text: str, sign_prefixes: bool = True) -> Tuple[int, ...]:
    regex = '([\-+]?\d+)' if sign_prefixes else '(\d+)'
    return tuple(map(int, re.findall(regex, text)))


def floats(text: str) -> Tuple[float, ...]:
    return tuple(map(float, re.findall('([\-+]?\d*(?:\d|\d\.|\.\d)\d*)', text)))


def sum_iter(x: Iterable[int], y: Iterable[int], s: int = 1) -> Tuple[int, ...]:
    """ Returns the equation x + s * y for each element in the sequence x and y """
    return tuple(a + s * b for a, b in zip(x, y))


def dot_iter(x: Iterable[int], y: Iterable[int]) -> int:
    """ Returns the dot product of an sequence """
    return sum(a * b for a, b in zip(x, y))


def differences(x: Sequence[int]) -> Tuple[int, ...]:
    """ Returns the sequence of differences of consecutive elements of x """
    return tuple(x[i + 1] - x[i] for i in range(len(x) - 1))


def manhattan(x: Union[Iterable[int], complex]) -> int:
    """ Returns the magnitude of a sequence using the 1-norm (manhattan distance to the origin). Also works for complex numbers. """
    if isinstance(x, complex):
        x = map(int, (x.real, x.imag))
    return sum(map(abs, x))


def prod(iterable: Iterable[int]) -> int:
    """ Calculates the product of an iterable. In Python 3.8 this can be replaced with a call to math.prod """
    return functools.reduce(lambda x, y: x * y, iterable)


def min_max(x: Iterable[int]) -> Tuple[int, int]:
    """ Returns both the min and max of a sequence.
    This, rather than calling min(x), max(x), will work when a generator (or other single-use iterator) is passed in
    """
    try:
        seq = iter(x)
        start = next(seq)
    except StopIteration:
        raise ValueError('min_max() arg is an empty sequence')
    return functools.reduce(lambda left, right: (min(left[0], right), max(left[1], right)), seq, (start, start))


def sign(a: int) -> int:
    """ Returns the sign of a """
    return 0 if a == 0 else (-1 if a < 0 else 1)


def lcm(a: int, b: int) -> int:
    """ Lowest common multiple. """
    return a * b // math.gcd(a, b)


def gcd_iter(sequence: Iterable[int]) -> int:
    """ Greatest common divisor of a sequence. """
    return functools.reduce(math.gcd, sequence)


def lcm_iter(sequence: Iterable[int]) -> int:
    """ Finds the lowest common multiple of a sequence. """
    return functools.reduce(lcm, sequence)


def extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    """ Extended Euclidean Algorithm. For any a, b, returns values gcd(a, b), x, and y such that a*x + b*y = gcd(a, b) """
    if a == 0:
        return b, 0, 1
    g, x, y = extended_gcd(b % a, a)
    return g, y - (b // a) * x, x


def crt(a1: int, m1: int, a2: int, m2: int) -> Tuple[int, int]:
    """ Generalized Chinese Remainder Theorem (CRT).
    Find x, where x = a1 mod m1, x = a2 mod m2, if such a solution exists.
    It always exists when m1 and m2 are coprime, or if g = gcd(m1, m2), and a1 == a2 mod g
    Returns an x, and the modulus (m1 * m2 for the coprime case)
    """
    g, x, y = extended_gcd(m1, m2)
    if a1 % g == a2 % g:
        ar, mr = (a2 * x * m1 + a1 * y * m2) // g, m1 * m2 // g
    else:
        raise ValueError('The system x = %d mod %d, x = %d mod %d has no solution' % (a1, m1, a2, m2))
    return ar % mr, mr


def mod_inv(a: int, m: int) -> int:
    """ Finds x such that a*x ~= 1 mod m. Uses the extended euclidean algorithm. In python 3.8+ this can be pow(a, -1, m), but this is explicitly written here in order to be PyPy compliant. """
    g, x, y = extended_gcd(a, m)
    if g == 1:
        return ((x % m) + m) % m
    raise ValueError('Modular inverse for a=%d, m=%d does not exist' % (a, m))


def ray_int(start: Iterable[int], end: Iterable[int]) -> list:
    """ Returns a list of tuples of the points in a ray cast from start to end, not including either """
    deltas = sum_iter(end, start, -1)
    delta_gcd = gcd_iter(deltas)
    if delta_gcd > 1:
        return [tuple(s + d * g // delta_gcd for s, d in zip(start, deltas)) for g in range(1, delta_gcd)]
    return []


def moore_neighbors(p: Tuple[int, ...], d: int = 1) -> Iterable[Tuple[int, ...]]:
    """ Returns all points in a Moore neighborhood (points which coordinates differ by at most d, or x, y s.t. |x-y| <= d under the infinity norm """
    zero = (0,) * len(p)
    for dp in itertools.product(range(-d, d + 1), repeat=len(p)):
        if dp != zero:
            yield sum_iter(p, dp)


def von_neumann_neighbors(p: Tuple[int, ...], d: int = 1) -> Iterable[Tuple[int, ...]]:
    """ Returns all points in a Von Neumann neighborhood (points which are at most a distance of d away, using the 1 norm / manhattan distance) """
    n = len(p)
    if d == 1:  # Special case, just iterate through each unit vector
        for i in range(n):
            dp = tuple((1 if j == i else 0 for j in range(n)))
            yield sum_iter(p, dp)
            yield sum_iter(p, dp, -1)
    else:  # Otherwise, compute the moore neighborhood and filter
        zero = (0,) * len(p)
        for dp in itertools.product(range(-d, d + 1), repeat=len(p)):
            if dp != zero and manhattan(dp) <= d:
                yield sum_iter(p, dp)


class Grid:

    @staticmethod
    def from_text(text: str, default_value: Optional[str] = None):
        return Grid([list(line.strip()) for line in text.strip().split('\n')], default_value)

    @staticmethod
    def from_lines(lines: List[str], default_value: Optional[str] = None):
        return Grid([list(line) for line in lines], default_value)

    def __init__(self, grid: List[List[str]], default_value: Optional[str] = None):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])
        self.default_value = default_value

    def copy(self) -> 'Grid':
        return Grid([row.copy() for row in self.grid], self.default_value)

    def count(self, value: str) -> int:
        return sum(row.count(value) for row in self.grid)

    def locations(self) -> Iterator[Tuple[int, int]]:
        for x in range(self.width):
            for y in range(self.height):
                yield x, y

    def map_create(self, f: Callable[[int, int], str]) -> 'Grid':
        return Grid([[f(x, y) for x in range(self.width)] for y in range(self.height)], self.default_value)

    def __getitem__(self, item):
        if isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], int) and isinstance(item[1], int):
            if 0 <= item[0] < self.width and 0 <= item[1] < self.height:
                return self.grid[item[1]][item[0]]
            elif self.default_value is not None:
                return self.default_value
            else:
                raise ValueError('Provided location is out of bounds: %s not in [0, %d) x [0, %d)' % (str(item), self.width, self.height))
        else:
            raise TypeError('Provided index is not an (x, y) tuple: %s' % str(item))

    def __setitem__(self, key, value):
        if isinstance(key, tuple) and len(key) == 2 and isinstance(key[0], int) and isinstance(key[1], int):
            if 0 <= key[0] < self.width and 0 <= key[1] < self.height:
                self.grid[key[1]][key[0]] = value
            elif self.default_value is not None:
                return self.default_value
            else:
                raise ValueError('Provided index is out of bounds: %s not in [0, %d) x [0, %d)' % (str(key), self.width, self.height))
        else:
            raise TypeError('Provided index is not an (x, y) tuple: %s' % str(key))

    def __contains__(self, item):
        if isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], int) and isinstance(item[1], int):
            return 0 <= item[0] < self.width and 0 <= item[1] < self.height
        if isinstance(item, str):
            return any(item in row for row in self.grid)
        raise TypeError('Provided item is not a key (x, y) pair, or value (str): %s' % str(item))

    def __eq__(self, other):
        return other is not None and self.grid == other.grid

    def __str__(self):
        return '\n'.join(''.join(row) for row in self.grid)


def grid_bfs(grid: Grid, passable: Set[str], start: Tuple[int, int]) -> Dict[Tuple[int, int], int]:
    """ A template for a grid based BFS """
    queue = deque()
    queue.append((*start, 0))
    found = {start}
    distances = {start: 0}
    while queue:
        x0, y0, d0 = queue.popleft()
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            p1 = x0 + dx, y0 + dy
            if p1 not in found and p1 in grid and grid[p1] in passable:
                found.add(p1)
                distances[p1] = d0 + 1
                queue.append((*p1, d0 + 1))
    return distances


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

