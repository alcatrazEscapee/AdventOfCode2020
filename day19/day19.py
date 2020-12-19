# Day 19: Monster Messages
# Results: 99 / 846

from utils import *


def main(text: str):
    part1(text)

    # replacements
    lines = text.split('\n')
    replacements = {
        '8: 42': '8: 42 | 42 8',
        '11: 42 31': '11: 42 31 | 42 11 31'
    }
    lines = [replacements[line] if line in replacements else line for line in lines]
    text = '\n'.join(lines)
    part2(text)


def part1(text: str):
    rules_text, examples = text.split('\n\n')

    rules = {}
    for rule_text in rules_text.split('\n'):
        key, rule_spec = rule_text.split(': ')
        key = int(key)
        if '\"' in rule_spec:
            c = rule_spec[1]
            # print('exact rule', key, c)
            rules[key] = c
        else:
            r = []
            for option in rule_spec.split('|'):
                matches = ints(option)
                r.append(matches)
            rules[key] = tuple(r)
            # print('delegate rule', key, r)

    # print('rule zero', rules[0])

    def match_rule(line, rule_idx, pos):
        # print('testing', line, 'against', rules[rule_idx], 'at', pos)
        rule = rules[rule_idx]
        save_start = pos
        if isinstance(rule, str):
            if pos < len(line) and line[pos] == rule:
                return True, pos + 1
            else:
                return False, pos
        else:
            for opt in rule:
                save = pos
                for next_idx in opt:
                    # advance and try rule
                    b, p = match_rule(line, next_idx, pos)
                    # print('ret', b, p)
                    if b:
                        pos = p
                    else:
                        # failed, backtrack
                        pos = save
                        break
                else:
                    # matched the rule completely!
                    if pos <= len(example):
                        return True, pos
            return False, save_start

    c = 0
    for example in examples.split('\n'):
        b, p = match_rule(example, 0, 0)
        # print('ret full', b, p)
        if p == len(example) and b:
            c += 1
            # print('match', example)
        # print(b, p)
    print('Part 1', c)


def part2(text: str):
    rules_text, examples = text.split('\n\n')

    rules = {}
    char_rules = {}
    for rule_text in rules_text.split('\n'):
        key, rule_spec = rule_text.split(': ')
        key = int(key)
        if '\"' in rule_spec:
            c = rule_spec[1]
            # print('exact rule', key, c)
            char_rules[key] = c
        else:
            r = []
            for option in rule_spec.split('|'):
                matches = ints(option)
                r.append(matches)
            rules[key] = tuple(r)

    change = True
    while change:
        change = False
        rules_new = {}
        for k, r in rules.items():
            # print('checking rule', k, 'which is', r)
            r_new = []
            g = True
            for opt in r:
                f = True
                if not isinstance(opt, str):
                    opt_new = []
                    for c in opt:
                        if isinstance(c, str):
                            opt_new.append(c)
                        elif c in char_rules:
                            opt_new.append(char_rules[c])
                        else:
                            # print('oops', c, opt_new, g, f)
                            opt_new.append(c)
                            f = False
                            g = False
                    if f:
                        opt_new = '(' + ''.join(opt_new) + ')'
                    else:
                        opt_new = tuple(opt_new)
                else:
                    opt_new = opt
                r_new.append(opt_new)
            # print('end rule', k, 'with', f, g, r_new)
            if g:
                r_new = '(' + '|'.join(r_new) + ')'
                change = True
                char_rules[k] = r_new
                # print('Reduced rule', k, 'prev', r, 'to', r_new)
            else:
                r_new = tuple(r_new)
                rules_new[k] = r_new

        rules = rules_new

    # print('RULES')
    # for k, v in sorted(rules.items()):
    #     print('rule', k)
    #     for ls in v:
    #         print(ls)

    c = 0
    r8 = rules[8][0] + '{%d,11}'
    r11 = rules[11][1][2] + '{%d,%d}'
    # r8 = A+
    # r11 = AnBn
    # r0 = A>nBn
    for ex in examples.split('\n'):
        #print('try', ex)
        for i in range(1, 10):
            if re.fullmatch((r8 % i) + (r11 % (i, i)), ex):
                c += 1
                #print('match', c, ex, 'with i', i)
                break
    print('Part 2:', c)



if __name__ == '__main__':
    main(get_input())
