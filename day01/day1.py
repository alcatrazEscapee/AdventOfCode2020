# Day 1: Report Repair
# Results: 503 Service Temporarily Unavailable

from utils import *


def main(values):
    # Initial solution was using nested for loops. This is using itertools.product because it's fancy :)
    print('Part 1:', next(i * j for i, j in itertools.product(values, values) if i + j == 2020))
    print('Part 2:', next(i * j * k for i, j, k in itertools.product(values, values, values) if i + j + k == 2020))


if __name__ == '__main__':
    main(ints(get_input()))
