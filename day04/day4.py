# Day 4: Passport Processing
# Results: 425 / 426

from utils import *
import re


def main(text: str):
    part1 = part2 = 0

    for passport_text in text.split('\n\n'):
        passport = {}
        for entry in passport_text.replace('\n', ' ').split(' '):
            key, value = entry.split(':')
            passport[key] = value

        # Part 1: Check for required fields
        valid = True
        for key in REQUIRED_FIELDS:
            if key not in passport:
                valid = False
                break

        if valid:
            part1 += 1
            # This is not the most compact way to do this, but it is the way which allows for the best debugging, something that was very needed on the day of solving
            validations = {
                'byr': 1920 <= int(passport['byr']) <= 2002,
                'iyr': 2010 <= int(passport['iyr']) <= 2020,
                'eyr': 2020 <= int(passport['eyr']) <= 2030,
                'hgt': (
                    (passport['hgt'].endswith('in') and 59 <= int(passport['hgt'][:-2]) <= 76) or
                    (passport['hgt'].endswith('cm') and 150 <= int(passport['hgt'][:-2]) <= 193)
                ),
                'hcl': bool(re.fullmatch(HAIR_COLOR_REGEX, passport['hcl'])),
                'ecl': passport['ecl'] in EYE_COLORS,
                'pid': bool(re.fullmatch(PID_REGEX, passport['pid']))
            }
            if all(validations.values()):
                part2 += 1

    print('Part 1:', part1)
    print('Part 2:', part2)


REQUIRED_FIELDS = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
HAIR_COLOR_REGEX = '#[0-9a-f]{6}'
PID_REGEX = '[0-9]{9}'
EYE_COLORS = {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}

if __name__ == '__main__':
    main(get_input())
