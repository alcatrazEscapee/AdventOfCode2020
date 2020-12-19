# Day 19: Monster Messages
# Results: 99 / 846

from utils import *


def main():
    rules_text, examples_text = get_input().split('\n\n')
    examples: List[str] = examples_text.split('\n')
    rules: Dict[int, Union[Tuple[Tuple[int, ...]], str]] = {}
    for rule_text in rules_text.split('\n'):
        key, rule_spec = rule_text.split(': ')
        if '\"' in rule_spec:
            rules[int(key)] = rule_spec[1]
        else:
            rules[int(key)] = tuple(ints(option) for option in rule_spec.split('|'))

    # Part 2 Rule Changes
    # 8: 42         ->  8: 42 | 42 8
    # 11: 42 31     ->  11: 42 31 | 42 11 31
    # Notably, Rule 0 is 0: 8 11
    # The condensed form would be 0: 42{m} 31{n} s.t. m > n
    # We can approximate this by just iterating through "enough" values of n and using {1, n} style capture groups, but that's rather poor
    # If we had full PCRE support, we could use the regex r'A+?(A(?1)?B)', which is actually non-regular, but that's also difficult to come up with
    # So instead, I wrote a separate parser which is able to handle A{n}B{m}, m < n specifically with backtracking.

    rule0 = compute_regex(rules, 0)
    rule42 = compute_regex(rules, 42)
    rule31 = compute_regex(rules, 31)

    part1 = part2 = 0
    for ex in examples:
        if re.fullmatch(rule0, ex):
            part1 += 1
        if parse_match(rule42, rule31, ex):
            part2 += 1

    print('Part 1:', part1)
    print('Part 2:', part2)


def compute_regex(rules: Dict[int, Union[Tuple[Tuple[int, ...]], str]], key: int) -> str:
    rule = rules[key]
    if isinstance(rule, str):  # single character rule
        return rule
    elif len(rule) == 1:  # single chained rule
        return ''.join(compute_regex(rules, k) for k in rule[0])
    else:  # multiple choice rule
        return '(?:' + '|'.join(''.join(compute_regex(rules, k) for k in option) for option in rule) + ')'


def parse_match(rule_a: str, rule_b: str, string: str) -> bool:
    """ This parses the non-regular grammar A{m} B{n} s.t. m > n, where A and B are regular expressions given by rule_a and rule_b respectively """

    def parse_match_inner(rule: str, p: int) -> Tuple[bool, int]:
        match = re.match(rule, string[p:])
        if not match:
            return False, p
        return True, p + match.span()[1]

    # Must start by matching A
    count = 0
    matched, pos = parse_match_inner(rule_a, 0)
    while matched and pos <= len(string):
        # Try and match B{1, count}, backtracking to here if necessary
        save = pos
        for _ in range(count):
            matched, pos = parse_match_inner(rule_b, pos)
            if not matched:  # backtrack
                pos = save
                break
            elif pos == len(string):  # matched a number of B < A, and the full string has been consumed
                return True

        # Otherwise, match an A from last saved pos, and increment
        count += 1
        matched, pos = parse_match_inner(rule_a, pos)
    return False


if __name__ == '__main__':
    main()
