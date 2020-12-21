# Day 16: Ticket Translation
# Results: 248 / 241

from utils import *


def main(text):
    # Abridged parsing
    fields, mine, others = text.split('\n\n')
    fields = [(f.split(':')[0], *ints(f, sign_prefixes=False)) for f in fields.split('\n')]
    mine = ints(mine[1:])
    others = list(map(ints, others.split('\n')[1:]))

    part1 = 0
    tickets = []  # Only record valid tickets for at least one field
    for ticket in others:
        for v in ticket:
            if not any((a <= v <= b) or (c <= v <= d) for n, a, b, c, d in fields):
                part1 += v
                break
        else:
            tickets.append(ticket)

    print('Part 1:', part1)

    # Part 2
    # General Theory: during each iteration, we assume we can identify at least one field which only matches a currently unknown field on all tickets
    # We remove that ticket and field from the pool, and repeat the process, narrowing down the problem space

    graph = {}  # Start out with all fields having all indices as possible values
    for n, a, b, c, d in fields:  # Try every field
        graph[n] = set(range(len(fields)))  # Start out with all fields having all indices as possible values
        for i in range(len(fields)):  # As it compares to each possible index
            if not all(a <= ticket[i] <= b or c <= ticket[i] <= d for ticket in tickets):  # Against every ticket
                if i in graph[n]:  # And if one is invalid, then mark it as unable to satisfy this field
                    graph[n].remove(i)

    match = unique_perfect_matching(graph)
    part2 = prod(mine[match[n]] for n, *_ in fields if n.startswith('departure'))

    print('Part 2:', part2)


if __name__ == '__main__':
    main(get_input())
