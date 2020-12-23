# Day 22: Crab Combat
# Results: 113 / 380

from utils import *
from collections import deque
from typing import Deque


def main():

    assert score([9, 2, 6, 3, 1], [5, 8, 4, 7, 10], False) == 306
    assert score([9, 2, 6, 3, 1], [5, 8, 4, 7, 10], True) == 291

    p1, p2 = map(lambda t: ints(t)[1:], get_input().split('\n\n'))
    print('Part 1:', score(p1, p2, False))
    print('Part 2:', score(p1, p2, True))


def score(p1: Sequence[int], p2: Sequence[int], recursive: bool) -> int:
    p1, p2 = map(deque, (p1, p2))
    _, pw = (play_recursive if recursive else play)(p1, p2)
    return sum(e * (len(pw) - i) for i, e in enumerate(pw))


def play(p1: Deque[int], p2: Deque[int]) -> Tuple[bool, Deque[int]]:
    """ Play non-recursive, return True if P1 won, False otherwise, plus the winning player's deck """
    while p1 and p2:
        p1c, p2c = p1.popleft(), p2.popleft()
        if p1c > p2c:
            p1.append(p1c)
            p1.append(p2c)
        else:
            p2.append(p2c)
            p2.append(p1c)
    return bool(p1), p1 if p1 else p2


def play_recursive(p1: Deque[int], p2: Deque[int]) -> Tuple[bool, Deque[int]]:
    rounds = set()

    def freeze(p1_: Deque[int], p2_: Deque[int]) -> Tuple[Tuple[int, ...], Tuple[int, ...]]:
        return tuple(p1_), tuple(p2_)

    while p1 and p2:
        k = freeze(p1, p2)
        if k in rounds:  # if the game state is exactly the same, end the game in P1's favor
            return True, p1
        rounds.add(k)

        p1c = p1.popleft()
        p2c = p2.popleft()
        if len(p1) >= p1c and len(p2) >= p2c:  # Recurse
            p1r = deque(itertools.islice(p1, p1c))
            p2r = deque(itertools.islice(p2, p2c))
            p1_win, _ = play_recursive(p1r, p2r)
        else:
            p1_win = p1c > p2c

        if p1_win:
            p1.append(p1c)
            p1.append(p2c)
        else:
            p2.append(p2c)
            p2.append(p1c)
    return bool(p1), p1 if p1 else p2


if __name__ == '__main__':
    main()
