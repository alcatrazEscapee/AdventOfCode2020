# Day 9: Encoding Error
# Results: 102 / 65

from utils import *
import itertools


def main(text):
    values = ints(text)
    target = part1(values)
    print('Part 1:', target)
    print('Part 2:', part2(values, target))


def part1(values: Tuple[int, ...]) -> int:
    """ Identify a value which is not the sum of the 25 preceding values, and return it """
    for i in range(len(values) - 25):
        target = values[i + 25]
        for j, k in itertools.product(range(i, i + 25), range(i, i + 25)):
            if j != k and values[j] + values[k] == target:
                break
        else:
            return target
    raise RuntimeError('Failed to find a value!')


def part2(values: Tuple[int, ...], target: int) -> int:
    """ Identify a consecutive sequence of numbers in values which sum up to target, and return the sum of the min and max of that sequence """
    for length in range(2, 1 + len(values)):
        for start in range(0, 1 + len(values) - length):
            splice = values[start:start + length]
            if sum(splice) == target:
                return sum(min_max(splice))
    raise RuntimeError('Failed to find a value!')


if __name__ == '__main__':
    main(get_input())
