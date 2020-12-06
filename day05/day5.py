# Day 5: Binary Boarding
# Results: 695 / 705

from utils import *


def main(lines: List[str]):
    seat_ids = [
        int(''.join({'F': '0', 'B': '1', 'L': '0', 'R': '1'}[c] for c in line), 2)
        for line in lines
    ]

    print('Part 1:', max(seat_ids))

    prev = -1
    for curr in sorted(seat_ids):
        if curr - prev > 1 and prev != -1:
            print('Part 2:', curr - 1)
            break
        prev = curr


if __name__ == '__main__':
    main(get_input_lines())
