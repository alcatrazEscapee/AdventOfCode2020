# Day 25: Name
# Results: Sloooooooooow


def main():
    k1, k2 = 17607508, 15065270
    modulo = 20201227
    subject = 7
    k = 1
    for n in range(1, modulo):
        k = (k * subject) % modulo
        if k == k1:
            print('Part 1:', pow(k2, n, modulo))
            break


if __name__ == '__main__':
    main()
