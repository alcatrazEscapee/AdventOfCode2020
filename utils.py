from re import findall
from typing import Iterable, Dict, Any, Tuple, List, TypeVar, Callable
from collections import defaultdict
from functools import reduce
from math import gcd

Number = TypeVar('Number', int, float)


# Input Reading
def get_input(path: str = './input.txt') -> str:
    with open(path) as f:
        return f.read()


def get_input_lines(path: str = './input.txt') -> List[str]:
    return get_input(path).split('\n')


def ints(text: str) -> Tuple[int, ...]:
    return tuple(map(int, findall('([\-+]?\d+)', text)))


def floats(text: str) -> Tuple[float, ...]:
    return tuple(map(float, findall('([\-+]?\d*(?:\d|\d\.|\.\d)\d*)', text)))


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


def print_grid(grid_objects: Dict[Tuple[int, int], Any], values_map: Dict[Any, str] or None = None, padding: int = 0, reverse_y: bool = False, reverse_x: bool = False):
    """ Prints a grid, represented as a map from points to values, to the console. Default is top right = positive x, y """
    def pixel(p: Any) -> str:
        if values_map is None:
            return str(p)
        else:
            return values_map[p] if p in values_map else '?'

    min_x, max_x = min_max([p[0] for p in grid_objects.keys()])
    min_y, max_y = min_max([p[1] for p in grid_objects.keys()])
    min_x -= padding
    min_y -= padding
    max_x += padding
    max_y += padding
    range_x = range(max_x, min_x - 1, -1) if reverse_x else range(min_x, max_x + 1)
    range_y = range(min_y, max_y + 1) if reverse_y else range(max_y, min_y - 1, -1)

    print('\n'.join(''.join(pixel(grid_objects[(x, y)]) for x in range_x) for y in range_y))


def min_max(x: Iterable[Number]) -> Tuple[Number, Number]:
    return min(x), max(x)


def sign(a: Number) -> Number:
    return 0 if a == 0 else (-1 if a < 0 else 1)


def lcm(a: int, b: int) -> int:
    """ Return lowest common multiple. """
    return a * b // gcd(a, b)


def gcd_iter(sequence: Iterable[int]) -> int:
    """ Return greatest common divisor of a list """
    return reduce(gcd, sequence)


def lcm_iter(sequence: Iterable[int]) -> int:
    return reduce(lcm, sequence)


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


def bin_search(low: int, high: int, target: int, data: Callable[[int], int]) -> int:
    while low < high:
        mid = (low + high + 1) // 2
        if data(mid) <= target:
            low = mid
        else:
            high = mid - 1
    return low
