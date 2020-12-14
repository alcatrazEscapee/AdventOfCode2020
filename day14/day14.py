# Day 14: Docking Data
# Results: 84 / 99

from utils import *


def main(lines: List[str]):
    mask = '0' * 36
    floating_bits = 0
    part1, part2 = defaultdict(int), defaultdict(int)
    for line in lines:
        if line.startswith('mask'):
            mask = line.split(' = ')[1][::-1]  # order the mask LSB -> MSB for cleaner iteration
            floating_bits = mask.count('X')  # Used for part 2
        elif line.startswith('mem'):
            addr0, val0 = ints(line)

            # Part 1: use the mask as a marker to force certain bits of the value
            val = val0
            for i, c in enumerate(mask):
                if c == '1':
                    val |= (1 << i)
                elif c == '0':
                    val &= ~(1 << i)
            part1[addr0] = val

            # Part 2: use the mask and 'floating' bits to set all possible values
            # This works as there are not many floating values per mask. If there were too many, a better solution would've been needed
            # We iterate through (1 << floating_bits), using each bit of j as the replacement index into the address
            for j in range(1 << floating_bits):
                addr = addr0
                xc = 0
                for i, c in enumerate(mask):
                    if c == 'X':
                        addr = (addr & ~(1 << i)) | (((j >> xc) & 1) << i)  # Set the i-th bit to zero, then OR it with the xc-th bit of j
                        xc += 1
                    elif c == '1':
                        addr |= (1 << i)
                part2[addr] = val0

    print('Part 1:', sum(part1.values()))
    print('Part 2:', sum(part2.values()))


if __name__ == '__main__':
    main(get_input_lines())
