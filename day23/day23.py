# Day 23: Crab Cups
# Results: 597 / 95

from typing import List, Optional, Tuple


class Link:
    """ Mutable One-Directional Linked List link. """

    def __init__(self, value: int):
        self.right: Optional['Link'] = None
        self.value: int = value


def main():
    input_values = list(map(int, '872495136'))

    _, start, by_value = build_part1(input_values)
    result = solve(start, by_value, 100, max(input_values)).right
    values = []
    while result.value != 1:
        values.append(result.value)
        result = result.right

    print('Part 1:', ''.join(map(str, values)))

    max_value = 1_000_000
    _, start, by_value = build_part2(input_values, 10, max_value)
    result = solve(start, by_value, 10_000_000, max_value)

    print('Part 2:', result.right.value * result.right.right.value)


def build_part1(input_values: List[int]) -> Tuple[Link, Link, List[Link]]:
    by_value: List[Optional[Link]] = [None] * len(input_values)
    start = link = prev = Link(input_values[0])
    by_value[start.value - 1] = start
    for value in input_values[1:]:
        link = Link(value)
        by_value[value - 1] = link
        if prev is not None:
            prev.right = link
        prev = link

    link.right = start
    return link, start, by_value


def build_part2(input_values: List[int], next_value: int, max_value: int) -> Tuple[Link, Link, List[Link]]:
    prev, link, by_value = build_part1(input_values)  # Build the main linked list from part1, then extend it
    by_value += [None] * (1 + max_value - next_value)
    start = link

    for value in range(next_value, 1 + max_value):
        link = Link(value)
        by_value[value - 1] = link
        prev.right = link
        prev = link

    link.right = start
    return link, start, by_value


def solve(start: Link, links_by_value: List[Link], steps: int, max_value: int) -> Link:
    curr = start
    for _ in range(steps):
        # Extract the next three links, maintaining order
        first = curr.right
        second = first.right
        third = second.right

        # Link the current directly to the one after the removed
        curr.right = third.right

        # Search for a label which matches the destination requirements
        label = curr.value - 1
        removed = {first.value, second.value, third.value}
        while label in removed or label < 1:
            label -= 1
            if label < 0:
                label = max_value
        dest = links_by_value[label - 1]

        old_right = dest.right
        dest.right = first
        third.right = old_right

        curr = curr.right

    return links_by_value[0]  # return the link at the value = 1 position


if __name__ == '__main__':
    main()
