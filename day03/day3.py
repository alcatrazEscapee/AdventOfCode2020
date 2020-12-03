# Day 3: Toboggan Trajectory
# Results: Sloooooooow

from utils import *
from math import prod


def main(lines: List[str]):
    print('Part 1:', count_trees_hit(lines, 3, 1))
    print('Part 2:', prod(count_trees_hit(lines, x, y) for x, y in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))))


def count_trees_hit(lines: List[str], step_x: int, step_y: int):
    trees = 0
    for i in range(0, len(lines) // step_y):
        line = lines[i * step_y]
        if line[(i * step_x) % len(line)] == '#':
            trees += 1
    return trees


if __name__ == '__main__':
    main(get_input_lines())
