# Day 3: Toboggan Trajectory
# Results: Sloooooooow

from utils import *
from math import prod


def main(lines: List[str]):
    print('Part 1:', count_trees_hit(lines, 3, 1))
    print('Part 2:', prod(count_trees_hit(lines, x, y) for x, y in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))))


def count_trees_hit(lines: List[str], x: int, y: int):
    return sum(lines[i * y][(i * x) % len(lines[i * y])] == '#' for i in range(0, len(lines) // y))


if __name__ == '__main__':
    main(get_input_lines())
