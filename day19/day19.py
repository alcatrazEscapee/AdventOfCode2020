# Day 19: Monster Messages
# Results: 99 / 846

from utils import *


def main():
    rules_text, examples_text = get_input().split('\n\n')
    examples: List[str] = examples_text.split('\n')
    rules: Dict[int, Tuple[Production, Any], str] = {}
    for rule_text in rules_text.split('\n'):
        key, rule_spec = rule_text.split(': ')
        key = int(key)
        if '\"' in rule_spec:
            rules[key] = (Production.LITERAL, rule_spec[1])
        elif '|' in rule_spec:
            rules[key] = (Production.GROUP, tuple(ints(option) for option in rule_spec.split('|')))
        else:
            rules[key] = (Production.SEQUENCE, ints(rule_spec))

    parser = TopDownParser(rules)
    print('Part 1:', sum(parser.parse(ex) for ex in examples))

    # Part 2 Rule Changes
    # 8: 42         ->  8: 42 | 42 8
    # 11: 42 31     ->  11: 42 31 | 42 11 31
    rules[8] = (Production.GROUP, ((42,), (42, 8)))
    rules[11] = (Production.GROUP, ((42, 31), (42, 11, 31)))

    parser = TopDownParser(rules)
    print('Part 2:', sum(parser.parse(ex) for ex in examples))


if __name__ == '__main__':
    main()
