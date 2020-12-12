# Day 12: Rain Risk
# Results: 159 / 39

from utils import *


def main(lines: List[str]):

    # Part 1
    ship = 0
    face = 1
    for line in lines:
        p = line[0]
        amount = int(line[1:])
        if p == 'N':
            ship += 1j * amount
        elif p == 'S':
            ship += -1j * amount
        elif p == 'E':
            ship += 1 * amount
        elif p == 'W':
            ship += -1 * amount
        elif p == 'F':
            ship += face * amount
        elif p == 'L':
            face *= pow(1j, (amount // 90))
        elif p == 'R':
            face *= pow(-1j, (amount // 90))

    print('Part 1:', int(abs(ship.real) + abs(ship.imag)))

    ship = 0
    waypoint = 10 + 1j
    for line in lines:
        key = line[0]
        value = int(line[1:])
        if key == 'N':
            waypoint += 1j * value
        elif key == 'S':
            waypoint += -1j * value
        elif key == 'E':
            waypoint += 1 * value
        elif key == 'W':
            waypoint += -1 * value
        elif key == 'F':
            ship += waypoint * value
        elif key == 'L':
            waypoint *= pow(1j, (value // 90))
        elif key == 'R':
            waypoint *= pow(-1j, (value // 90))

    print('Part 2:', int(abs(ship.real) + abs(ship.imag)))


if __name__ == '__main__':
    main(get_input_lines())
