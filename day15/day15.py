# Day 15: Rambunctious Recitation
# Results: 1963 / 934

from utils import *


def main(run_tests: bool = False):
    part1, part2 = 2020, 30000000

    if run_tests:  # The part 2 tests here actually take a fair amount to run, so skip them for brevity
        assert solve('0,3,6', part1) == 436
        assert solve('1,3,2', part1) == 1
        assert solve('2,1,3', part1) == 10
        assert solve('1,2,3', part1) == 27
        assert solve('2,3,1', part1) == 78
        assert solve('3,2,1', part1) == 438
        assert solve('3,1,2', part1) == 1836

        assert solve('0,3,6', part2) == 175594
        assert solve('1,3,2', part2) == 2578
        assert solve('2,1,3', part2) == 3544142
        assert solve('1,2,3', part2) == 261214
        assert solve('2,3,1', part2) == 6895259
        assert solve('3,2,1', part2) == 18
        assert solve('3,1,2', part2) == 362

    puzzle_input = '0,6,1,7,2,19,20'
    print('Part 1:', solve(puzzle_input, part1))
    print('Part 2:', solve(puzzle_input, part2))


def solve(text: str, stop: int):
    values = ints(text)
    spoken = defaultdict(int)
    turn = 0
    last = None
    for v in values:
        if last is not None:
            spoken[last] = turn
        turn += 1
        last = v

    while turn < stop:
        if last not in spoken:
            spoken[last] = turn
            last = 0
        else:
            new = turn - spoken[last]
            spoken[last] = turn
            last = new
        turn += 1
    return last


if __name__ == '__main__':
    main()
