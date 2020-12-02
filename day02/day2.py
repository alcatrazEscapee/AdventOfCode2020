# Day 2: Password Philosophy
# Results: 140 / 81

from utils import *


def main(lines: List[str]):
    part1 = part2 = 0
    for data in lines:
        data = data.replace('-', ' ').split(' ')
        x, y = int(data[0]), int(data[1])  # x-y
        c = data[2][0]  # character to consider
        pwd = data[3]  # password
        if x <= pwd.count(c) <= y:  # Part 1: the number of appearances of 'c' must be in [x, y]
            part1 += 1
        if (pwd[x - 1] == c) ^ (pwd[y - 1] == c):  # Part 2: ONE of (xor) index x and y must be 'c' (1 indexed)
            part2 += 1

    print('Part 1:', part1)
    print('Part 2:', part2)


if __name__ == '__main__':
    main(get_input_lines())
