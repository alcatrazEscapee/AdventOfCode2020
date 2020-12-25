# Day 17: Conway Cubes
# Results: 60 / 37

from utils import *


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
        state = advance(state)
    return len(state)


def advance(state: Set[Tuple[int, ...]]):
    new = set()
    neighbors = Counter()
    for p in state:
        for p0 in moore_neighbors(p):
            neighbors[p0] += 1
    for p, c in neighbors.items():
        if (p in state and c in (2, 3)) or (p not in state and c == 3):
            new.add(p)
    return new


if __name__ == '__main__':
    main(get_input_lines())
