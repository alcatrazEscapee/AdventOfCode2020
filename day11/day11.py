# Day 11: Seating System
# Results: 108 / 441

from utils import *


def main():
    lines = TEST.strip().split('\n')
    assert part1(lines) == 37
    assert part2(lines) == 26

    lines = get_input_lines()
    print('Part 1:', part1(lines))
    print('Part 2:', part2(lines))


def part1(lines: List[str]) -> int:
    prev = None
    state: Grid = Grid.from_lines(lines, '.')

    def advance(x0: int, y0: int) -> str:
        current = state[x0, y0]
        if current != FLOOR:
            adj_occupied = 0
            for dx, dy in DIRECTIONS:
                x1, y1 = x0 + dx, y0 + dy
                if state[x1, y1] == OCCUPIED:
                    adj_occupied += 1
            if current == EMPTY and adj_occupied == 0:
                return OCCUPIED
            elif current == OCCUPIED and adj_occupied >= 4:
                return EMPTY
        return current

    while prev != state:
        prev = state
        state = state.map_create(advance)
    return state.count(OCCUPIED)


def part2(lines: List[str]) -> int:
    prev = None
    state: Grid = Grid.from_lines(lines, '.')

    def advance(x0: int, y0: int) -> str:
        current = state[x0, y0]
        if current != FLOOR:
            adj_occupied = 0
            for dx, dy in DIRECTIONS:
                x1, y1 = x0 + dx, y0 + dy
                while (x1, y1) in state:
                    if state[x1, y1] != FLOOR:
                        if state[x1, y1] == OCCUPIED:
                            adj_occupied += 1
                        break
                    x1 += dx
                    y1 += dy
            if current == EMPTY and adj_occupied == 0:
                return OCCUPIED
            elif current == OCCUPIED and adj_occupied >= 5:
                return EMPTY
        return current

    while prev != state:
        prev = state
        state = state.map_create(advance)
    return state.count(OCCUPIED)


DIRECTIONS = ((0, 1), (0, -1), (-1, 0), (1, 0), (-1, 1), (-1, -1), (1, -1), (1, 1))
FLOOR = '.'
EMPTY = 'L'
OCCUPIED = '#'

TEST = """
L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""

if __name__ == '__main__':
    main()
