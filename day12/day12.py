# Day 12: Rain Risk
# Results: 159 / 39

from utils import *


def main(lines: List[str]):

    directions = {'N': 1j, 'S': -1j, 'E': 1, 'W': -1}
    rotations = {'L': 1j, 'R': -1j}

    ship1 = ship2 = 0
    direction = 1  # Part 1
    waypoint = 10 + 1j  # Part 2

    for line in lines:
        key = line[0]
        value = int(line[1:])
        if key in 'NSEW':
            d = directions[key]
            ship1 += d * value
            waypoint += d * value
        elif key == 'F':
            ship1 += direction * value
            ship2 += waypoint * value
        elif key in 'LR':
            rot = pow(rotations[key], value // 90)
            direction *= rot
            waypoint *= rot

    print('Part 1:', int(abs(ship1.real) + abs(ship1.imag)))
    print('Part 2:', int(abs(ship2.real) + abs(ship2.imag)))


if __name__ == '__main__':
    main(get_input_lines())
