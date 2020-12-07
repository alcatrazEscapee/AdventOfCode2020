# Day 7: Handy Haversacks
# Results: 906 / 382

from utils import *


def main(lines: List[str], target_color: str):
    bags: Dict[str, Tuple[Tuple[int, str], ...]] = {}
    for line in lines:
        match = re.fullmatch('([a-z ]+) bags contain ([\da-z,. ]+)', line)
        parent, children = match.groups()
        bag = []
        if 'no other bags' not in children:
            for child in children.split(','):
                match = re.match(' ?([\d+]) ([a-z ]+) bags?', child)
                bag.append((int(match.group(1)), match.group(2)))
        bags[parent] = tuple(bag)

    part1 = 0
    for color in bags.keys():
        bags_in_bags = defaultdict(int)
        collect_all(bags_in_bags, bags, color)
        if target_color in bags_in_bags:
            part1 += 1

    print('Part 1:', part1)

    bags_in_target = defaultdict(int)
    collect_all(bags_in_target, bags, target_color)

    print('Part 2:', sum(bags_in_target.values()))


def collect_all(parent: Dict[str, int], bags: Dict[str, Tuple[Tuple[int, str], ...]], col: str, amount: int = 1, first: bool = True):
    if not first:  # Bags should not contain themselves
        parent[col] += amount
    for entry in bags[col]:
        next_amount, next_col = entry
        collect_all(parent, bags, next_col, next_amount * amount, False)


if __name__ == '__main__':
    main(get_input_lines(), 'shiny gold')
