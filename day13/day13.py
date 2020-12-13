# Day 13: Shuttle Search
# Results: 288 / 1326

from utils import *


def main():
    assert part1(939, '7,13,x,x,59,x,31,19') == 295

    time, schedule, *_ = get_input_lines()
    print('Part 1:', part1(int(time), schedule))

    # Provided test cases
    assert part2('17,x,13,19') == 3417
    assert part2('67,7,59,61') == 754018
    assert part2('67,x,7,59,61') == 779210
    assert part2('67,7,x,59,61') == 1261476
    assert part2('1789,37,47,1889') == 1202161486
    assert part2('7,13,x,x,59,x,31,19') == 1068781

    # Generalized test cases (from <https://www.reddit.com/r/adventofcode/comments/kc94h1/2020_day_13_part_2_generalization/>)
    assert part2('14,x,x,x,335,x,x,x,39,x,x,x,x,x,x,x,x,187,19') == 124016326
    assert part2('73,x,x,x,x,x,x,67,x,25,x,x,x,x,x,343,x,x,9') == 369373941
    assert part2('77,97,x,x,x,x,x,x,57,x,x,x,x,x,62,x,x,x,x,78,x,x,x,65') == -1
    assert part2('7,24,x,x,9,13,x,x,x,20,x,x,x,33') == 173831
    assert part2('71,x,x,x,x,x,x,x,375,x,x,x,x,x,x,x,x,726,x,x,x,x,x,76,67,53,x,x,x,94') == 21428909746117
    assert part2('59,x,x,x,117,x,x,x,x,x,x,x,x,x,x,x,189,x,61,x,x,137') == -1
    assert part2('173,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,1287,x,x,2173,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,1275,x,x,x,x,x,x,x,x,x,x,x,671,x,x,x,x,x,x,2674') == 27208285429450535
    assert part2('1997,x,x,x,x,x,x,1747,x,x,x,x,x,2003,x,x,x,x,x,x,1883,x,x,x,x,x,1667,x,x,x,x,x,x,x,1701') == 4756544012204563475

    print('Part 2:', part2(schedule))


def part1(time: int, schedule: str):
    # This is straightforward. The while all() is used to iterate until at least one bus matches t = total
    # At that point, the answer is the product of the difference between time and total, and the bus ID.
    # Since we know there's only one valid bus ID, we use a next() with an iterator to find it
    busses = [int(x) for x in schedule.split(',') if x != 'x']
    total = time
    while all(total % b != 0 for b in busses):
        total += 1
    return next(b for b in busses if total % b == 0) * (total - time)


def part2(schedule: str):
    # Each schedule element is a pair (m, a), which stipulates that for any time t, we must have t + a mod m == 0
    # This can be converted to the form required for chinese remainder theorem by subtracting a from both sides.
    # Then we have for (a1, m1), (a2, m2), t % m1 = -a1 and t % m2 = -a2. crt() gets this such t, and then is negated again into bus form.
    # functools.reduce() is used to reduce down to one constraint, at which point the answer is such an x
    busses = [(int(x), i) for i, x in enumerate(schedule.split(',')) if x != 'x']
    try:
        bus = functools.reduce(reduce, busses)
        return -bus[1]
    except ValueError:
        return -1  # In the case a solution does not exist, for solving the more generalized problem


def reduce(a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[int, int]:
    x, m = crt(-a[1], a[0], -b[1], b[0])
    return m, -x


if __name__ == '__main__':
    main()
