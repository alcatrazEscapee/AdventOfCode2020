# Day 10: Adapter Array
# Results: 701 / 674

from utils import *


def main(text: str):
    values = ints(text)
    diffs = differences([0, *sorted(values), max(values) + 3])
    print('Part 1:', diffs.count(1) * diffs.count(3))

    length = 0
    part2 = 1
    for d in diffs:
        length += 1
        if d == 3 and length > 0:
            part2 *= solve_sequence(length)
            length = 0

    print('Part 2:', part2)


def solve_sequence(n: int) -> int:
    sequence = [1, *[0] * (n - 1)]
    for i, v in enumerate(sequence):
        for j in range(1 + i, min(i + 4, n)):
            sequence[j] += v
    return sequence[-1]


if __name__ == '__main__':
    main(get_input())
