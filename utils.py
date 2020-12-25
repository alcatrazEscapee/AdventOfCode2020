# AoC Utils

import re
import math
import functools
import itertools

from collections import Counter, defaultdict, deque
from enum import IntEnum, auto
from typing import Any, Callable, DefaultDict, Deque, Dict, FrozenSet, Iterable, Iterator, List, Mapping, MutableMapping, Optional, Sequence, Set, Tuple, TypeVar, Union


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
        return abs(int(x.real)) + abs(int(x.imag))
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


def isqrt(x: int) -> int:
    """ Returns the largest integer y such that y * y <= x """
    if x < 0:
        raise ValueError('square root not defined for negative numbers')
    elif x == 0:
        return 0
    n = x
    a, b = divmod(n.bit_length(), 2)
    x = 2 ** (a + b)
    while True:
        y = (x + n // x) // 2
        if y >= x:
            return x
        x = y


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
    def from_text(text: str, default_value: Optional[str] = None) -> 'Grid':
        return Grid([list(line.strip()) for line in text.strip().split('\n')], default_value)

    @staticmethod
    def from_lines(lines: List[str], default_value: Optional[str] = None) -> 'Grid':
        return Grid([list(line) for line in lines], default_value)

    @staticmethod
    def from_function(width: int, height: int, f: Callable[[int, int], str], default_value: Optional[str] = None) -> 'Grid':
        return Grid([[f(x, y) for x in range(width)] for y in range(height)], default_value)

    def __init__(self, grid: List[List[str]], default_value: Optional[str] = None):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])
        self.square = self.width == self.height
        self.default_value = default_value
        assert isinstance(grid, list), 'Grid must be a List[List[str]], got %s' % type(grid)
        assert all(isinstance(row, list) for row in grid), 'Grid must be a List[List[str]], got %s' % str(type(row) for row in grid)

    def copy(self) -> 'Grid':
        """ Creates an identical copy of this grid """
        return Grid([row.copy() for row in self.grid], self.default_value)

    def rotate_cw(self) -> 'Grid':
        """ Creates a copy of this grid, rotated clockwise """
        return self.map_create(lambda x, y: self[y, self.width - 1 - x])

    def rotate_ccw(self) -> 'Grid':
        """ Creates a copy of this grid, rotated counter clockwise """
        return self.map_create(lambda x, y: self[self.height - 1 - y, x])

    def mirror_y(self) -> 'Grid':
        """ Creates a copy of this grid, mirrored over the y-axis """
        return self.map_create(lambda x, y: self[self.width - 1 - x, y])

    def mirror_x(self) -> 'Grid':
        """ Creates a copy of this grid, mirrored over the x-axis """
        return self.map_create(lambda x, y: self[x, self.height - 1 - y])

    def permutations(self) -> Iterator['Grid']:
        """ Iterates through all permutations (rotations and mirrors) of this grid """
        grid = self
        for _ in range(4):
            yield grid
            yield grid.mirror_y()
            grid = grid.rotate_cw()

    def count(self, value: str) -> int:
        """ Counts the number of occurrences of value within the grid """
        return sum(row.count(value) for row in self.grid)

    def locations(self) -> Iterator[Tuple[int, int]]:
        """ An iterator over all coordinate positions within the grid """
        for x in range(self.width):
            for y in range(self.height):
                yield x, y

    def map_create(self, f: Callable[[int, int], str]) -> 'Grid':
        """ Creates a copy of this grid, with each location populated with the required function """
        return Grid.from_function(self.width, self.height, f, self.default_value)

    def __getitem__(self, item: Tuple[int, int]) -> str:
        if isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], int) and isinstance(item[1], int):
            if 0 <= item[0] < self.width and 0 <= item[1] < self.height:
                return self.grid[item[1]][item[0]]
            elif self.default_value is not None:
                return self.default_value
            else:
                raise ValueError('Provided location is out of bounds: %s not in [0, %d) x [0, %d)' % (str(item), self.width, self.height))
        else:
            raise TypeError('Provided index is not an (x, y) tuple: %s' % str(item))

    def __setitem__(self, key: Tuple[int, int], value: str):
        if isinstance(key, tuple) and len(key) == 2 and isinstance(key[0], int) and isinstance(key[1], int):
            if 0 <= key[0] < self.width and 0 <= key[1] < self.height:
                self.grid[key[1]][key[0]] = value
            elif self.default_value is not None:
                return self.default_value
            else:
                raise ValueError('Provided index is out of bounds: %s not in [0, %d) x [0, %d)' % (str(key), self.width, self.height))
        else:
            raise TypeError('Provided index is not an (x, y) tuple: %s' % str(key))

    def __contains__(self, item: Union[Tuple[int, int], str]) -> bool:
        if isinstance(item, tuple) and len(item) == 2 and isinstance(item[0], int) and isinstance(item[1], int):
            return 0 <= item[0] < self.width and 0 <= item[1] < self.height
        if isinstance(item, str):
            return any(item in row for row in self.grid)
        raise TypeError('Provided item is not a key (x, y) pair, or value (str): %s' % str(item))

    def __eq__(self, other: Optional['Grid']) -> bool:
        return other is not None and self.grid == other.grid

    def __str__(self) -> str:
        return '\n'.join(''.join(row) for row in self.grid)


class Production(IntEnum):
    LITERAL = auto()
    SEQUENCE = auto()
    GROUP = auto()


class TopDownParser:
    """
    This is a Non-Deterministic, Backtracking, Top Down Parser implementation, using the specification provided by an underlying grammar
    The grammar must be specified as a series of rules, with integer IDs. These rules are identified as per the Production enum, and have one extra piece of data specific to the rule.

    This parser WILL encounter issues with left recursion. e.g. the grammar
    1: 1 2 | 2
    2: 'a'
    which collectively describes all strings consisting of 'a's only
    will generate an infinite sequence of [2, 1, 1, 1, 1...]

    LITERAL rules: A str indicating a required piece of text to parse
    SEQUENCE rules: A Tuple[int] of rule IDs to be parsed in sequence
    GROUP rules: A Tuple[Tuple[int]] of of rule IDs, where one of the tuples must match (and will be interpreted as a sequence rule)
    """

    def __init__(self, grammar: Dict[int, Tuple[Production, Any]], root: int = 0):
        self.grammar = dict(grammar)
        self.root = root

    def parse(self, text: str, start_rule: int = 0) -> bool:
        group_stack = []
        rule_stack = [self.grammar[start_rule]]
        pointer = 0
        backtracking = False
        while True:
            if backtracking:
                # Backtrack to the most recent group, and check other possible group values
                if not group_stack:
                    return False  # Nowhere to backtrack to, we must've ended the entire string
                else:
                    # Compute the top backtrack location on the stack
                    group = group_stack.pop(-1)
                    save_stack, save_rule, save_index, save_pointer = group
                    if save_index < len(save_rule[1]):
                        # This group can still be tried with a subsequent entry
                        # Append the adjusted group back to the group stack, and restore the current location
                        backtracking = False
                        rule_stack = list(save_stack)
                        rule_stack.append((Production.SEQUENCE, save_rule[1][save_index]))
                        pointer = save_pointer
                        group_stack.append((save_stack, save_rule, save_index + 1, save_pointer))
            else:
                # Not backtracking
                if not rule_stack:
                    # No remaining rules. If we've reached the end of the string, the string is valid. If not, start backtracking
                    if pointer == len(text):
                        return True
                    else:
                        backtracking = True
                else:
                    # Compute the top rule on the stack
                    rule = rule_stack.pop(-1)
                    key = rule[0]
                    if key == Production.LITERAL:
                        if text[pointer:].startswith(rule[1]):
                            pointer += len(rule[1])
                        else:
                            backtracking = True
                    elif key == Production.SEQUENCE:
                        # Append the next rules to the stack in reverse order
                        # Ex: stack = [A ... B, SEQ], and SEQ = [1, 2, 3] -> stack = [A ... B, 3, 2, 1]
                        for r in rule[1][::-1]:
                            rule_stack.append(self.grammar[r])
                    elif key == Production.GROUP:
                        # Save this position on the group stack, marking the remaining rule stack, this group rule, the chosen path, and the current pointer
                        # Then, expand the first group choice onto the rule stack
                        group_stack.append((tuple(rule_stack), rule, 1, pointer))  # 1 = the next index to try
                        rule_stack.append((Production.SEQUENCE, rule[1][0]))
                    else:
                        raise TypeError('Unknown production: %s' % repr(rule))


def unique_perfect_matching(graph: Mapping[Any, Set[Any]]) -> Dict[Any, Any]:
    """ Given a bipartite graph with a unique perfect match, finds such match.
    The graph is a Dict[Key, Set[Value]], and the result is a Dict[Key, Value] s.t. for k, v in match, v in graph[k]"""
    graph = dict((k, set(v)) for k, v in graph.items())
    match = {}
    while len(match) < len(graph):
        for k, vs in graph.items():
            if len(vs) == 1:
                v = vs.pop()
                match[k] = v
                break
        else:
            raise ValueError('Unable to find a unique perfect matching!')
        for k, vs in graph.items():
            if v in vs:
                vs.remove(v)
    return match


def invert_injective(d: Mapping[Any, Any]) -> Dict[Any, Any]:
    """ Given an injective mapping d : X -> Y, returns the inverse mapping  d0: Y -> X """
    d0 = {}
    for k, v in d.items():
        if v not in d0:
            d0[v] = k
        else:
            raise ValueError('Dictionary is not injective: keys %s, %s -> %s' % (repr(k), repr(d0[v]), repr(v)))
    return d0

