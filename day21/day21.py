# Day 21: Allergen Assessment
# Results: Slow

from utils import *


def main(lines: List[str]):
    foods: List[Tuple[List[str], List[str]]] = []  # Parse input into a list of pairs of (ingredients, allergens)
    for line in lines:
        fi, fa = line.split(' (contains ')
        foods.append((list(fi.split(' ')), fa.replace(',', '')[:-1].split(' ')))

    all_i, all_a = functools.reduce(lambda x, y: (x[0] | y[0], x[1] | y[1]), ((set(fi), set(fa)) for fi, fa in foods))  # collect all allergens and ingredients in a set
    graph = dict((
        a,
        functools.reduce(lambda x, y: x & y, (set(fi) for fi, fa in foods if a in fa))
    ) for a in all_a)  # for each allergen, collect the intersection of all ingredients under which that allergen must be found
    match = invert_injective(unique_perfect_matching(graph))  # find the allergen <-> ingredient map, invert to get ingredient -> allergen
    allergen_ingredients = set(match.keys())
    safe_ingredients = set(all_i) - allergen_ingredients
    part1 = sum(
        i in safe_ingredients
        for fi, fa in foods
        for i in fi
    )  # the number of instances of all ingredients which do not contain an allergen
    part2 = ','.join(sorted(allergen_ingredients, key=lambda x: match[x]))  # the allergen containing ingredients, sorted by allergen

    print('Part 1:', part1)
    print('Part 2:', part2)


if __name__ == '__main__':
    main(get_input_lines())
