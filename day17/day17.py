# Day 17: Conway Cubes
# Results: 60 / 37

from utils import *
from itertools import product


def main(lines: List[str]):
    print('Part 1:', solve(lines, 3))
    print('Part 2:', solve(lines, 4))


def solve(lines: List[str], dimensions: int) -> int:
    state = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                state.add((x, y, *(0,) * (dimensions - 2)))
    for _ in range(6):
        state = advance(state, dimensions)
    return len(state)


def advance(state: Set[Tuple[int, ...]], dimensions: int):
    new = set()
    zero = (0,) * dimensions
    bounds = [min_max([p[d] for p in state]) for d in range(dimensions)]
    for p in product(*[range(bounds[d][0] - 1, 2 + bounds[d][1]) for d in range(dimensions)]):
        count = 0
        for dp in product(range(-1, 2), repeat=dimensions):
            if dp != zero:
                p0 = sum_iter(p, dp)
                if p0 in state:
                    count += 1
                if count >= 4:
                    break  # Our rules don't care about anything higher than 3, so just exit here
        if (p in state and count in (2, 3)) or (p not in state and count == 3):
            new.add(p)
    return new


if __name__ == '__main__':
    main(get_input_lines())
