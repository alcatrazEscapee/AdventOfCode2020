# Day 6: Custom Customs
# Results: 110 / 89

from utils import *


def main(text: str):
    part1 = part2 = 0
    for group in text.split('\n\n'):
        people = group.count('\n') + 1
        answers = group.replace('\n', '')
        part1 += len(set(answers))
        part2 += sum(v == people for k, v in Counter(answers).items())
    print('Part 1:', part1)
    print('Part 2:', part2)


if __name__ == '__main__':
    main(get_input())
