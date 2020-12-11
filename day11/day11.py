# Day 11: Seating System
# Results: 108 / 441

from utils import *
from typing import List, Tuple, Callable


def main():
    lines = TEST.strip().split('\n')
    assert solve(lines, advance_part1) == 37
    assert solve(lines, advance_part2) == 26

    lines = get_input_lines()
    print('Part 1:', solve(lines, advance_part1))
    print('Part 2:', solve(lines, advance_part2))


def solve(lines: List[str], advance: Callable[[Tuple[Tuple[str, ...], ...], int, int], Tuple[Tuple[str, ...], ...]]) -> int:
    height = len(lines)
    width = len(lines[0])
    prev = None
    state = tuple(map(tuple, lines))
    while prev != state:
        prev = state
        state = advance(state, width, height)
    return sum(sum(v == OCCUPIED for v in row) for row in state)


def advance_part1(state: Tuple[Tuple[str, ...], ...], width: int, height: int) -> Tuple[Tuple[str, ...], ...]:
    def advance(x0: int, y0: int) -> str:
        current = state[y0][x0]
        if current != FLOOR:
            adj_occupied = 0
            for dx, dy in DIRECTIONS:
                x1, y1 = x0 + dx, y0 + dy
                if 0 <= x1 < width and 0 <= y1 < height and state[y1][x1] == OCCUPIED:
                    adj_occupied += 1
            current = state[y0][x0]
            if current == EMPTY and adj_occupied == 0:
                return OCCUPIED
            elif current == OCCUPIED and adj_occupied >= 4:
                return EMPTY
        return current
    return tuple(tuple(advance(x, y) for x in range(width)) for y in range(height))


def advance_part2(state: Tuple[Tuple[str, ...], ...], width: int, height: int) -> Tuple[Tuple[str, ...], ...]:
    def advance(x0: int, y0: int) -> str:
        current = state[y0][x0]
        if current != FLOOR:
            adj_occupied = 0
            for dx, dy in DIRECTIONS:
                x1, y1 = x0 + dx, y0 + dy
                while 0 <= x1 < width and 0 <= y1 < height:
                    if state[y1][x1] != FLOOR:
                        if state[y1][x1] == OCCUPIED:
                            adj_occupied += 1
                        break
                    x1 += dx
                    y1 += dy
            if current == EMPTY and adj_occupied == 0:
                return OCCUPIED
            elif current == OCCUPIED and adj_occupied >= 5:
                return EMPTY
        return current
    return tuple(tuple(advance(x, y) for x in range(width)) for y in range(height))


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
