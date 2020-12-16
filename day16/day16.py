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
            if all(not ((a <= v <= b) or (c <= v <= d)) for n, a, b, c, d in fields):
                part1 += v
                break
        else:
            tickets.append(ticket)

    print('Part 1:', part1)

    # Part 2
    # General Theory: during each iteration, we assume we can identify at least one field which only matches a currently unknown field on all tickets
    # We remove that ticket and field from the pool, and repeat the process, narrowing down the problem space

    possible_matches = {}
    confirmed_matches = {}

    # Start out with all fields having all indices as possible values
    for field in fields:
        possible_matches[field[0]] = set(range(len(fields)))

    modified = True
    while modified:
        modified = False
        for n, a, b, c, d in fields:  # Try every field
            for i in range(len(fields)):  # As it compares to each possible index
                for ticket in tickets:  # Against every ticket
                    if not (a <= ticket[i] <= b or c <= ticket[i] <= d):  # And if one is invalid
                        if i in possible_matches[n]:  # Then mark it as unable to satisfy this field
                            possible_matches[n].remove(i)

        # Confirm any values which have only one possible index - we can then remove them from all other fields
        for name, possible in possible_matches.items():
            if len(possible) == 1:
                v = possible.pop()
                confirmed_matches[name] = v
                for k, v in possible_matches.items():
                    if confirmed_matches[name] in v:
                        v.remove(confirmed_matches[name])
                modified = True

    # Sanity checks to make sure we actually solved enough of the problem
    assert len(confirmed_matches) == len(possible_matches)

    part2 = 1
    for n, a, b, c, d in fields:
        if n.startswith('departure'):
            part2 *= mine[confirmed_matches[n]]

    print('Part 2:', part2)


if __name__ == '__main__':
    main(get_input())
