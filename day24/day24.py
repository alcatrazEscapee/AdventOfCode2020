# Day 24: Lobby Layout
# Results: 684 / 306

from utils import *

# Axial Coordinates (q, r)
# From: https://www.redblobgames.com/grids/hexagons/
HEX_GRID = {
    'e': (1, 0),
    'se': (0, 1),
    'sw': (-1, 1),
    'w': (-1, 0),
    'ne': (1, -1),
    'nw': (0, -1)
}


def main():
    lines = get_input_lines()
    black = set()  # Two state cellular automata - record a set of 'alive' states
    for line in lines:
        q = r = 0
        pointer = 0
        while pointer < len(line):
            # Due to the way the directions are set up, each segment of text will only match one of the directions
            # AKA, there's no need to ensure we match the longest sequence (e.g. if both N and NW were valid)
            for cardinal, dqr in HEX_GRID.items():
                if line[pointer:].startswith(cardinal):
                    q += dqr[0]
                    r += dqr[1]
                    pointer += len(cardinal)
                    break
        pos = q, r
        if pos in black:
            black.remove(pos)
        else:
            black.add(pos)

    print('Part 1:', len(black))

    for _ in range(100):
        adjacent = Counter()  # Track adjacent 'live' counts, also serves as a bounds-checking mechanic
        next_black = set()  # Next state
        for q, r in black:
            for dq, dr in HEX_GRID.values():
                adjacent[q + dq, r + dr] += 1

        for p, adj in adjacent.items():
            if adj == 2 or (p in black and adj == 1):
                next_black.add(p)

        black = next_black

    print('Part 2:', len(black))


if __name__ == '__main__':
    main()
