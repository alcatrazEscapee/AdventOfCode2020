
import os
import time
import subprocess

from typing import Optional, Tuple, DefaultDict
from collections import defaultdict


def main():
    expected: DefaultDict[int, Tuple[str, str]] = defaultdict(lambda: ('', ''), {
        1: ('1020099', '49214880'),
        2: ('393', '690'),
        3: ('272', '3898725600'),
        4: ('230', '156'),
        5: ('888', '522'),
        6: ('6735', '3221'),
        7: ('224', '1488'),
        8: ('1610', '1703'),
        9: ('25918798', '3340942'),
        10: ('1690', '5289227976704')
    })
    for i in range(1, 1 + 25):
        result = run_day(i)
        if result:
            p1, p2, delta, err = result
            result = 'Day %2d' % i
            if err:
                result += err
            else:
                if p1:
                    result += ' | Part 1: ' + ['failed', 'passed'][p1 == expected[i][0]]
                if p2:
                    result += ' | Part 2: ' + ['failed', 'passed'][p2 == expected[i][1]]
                result += ' | Time: ' + format_time(delta)
        else:
            result = 'Day %2d | No solution' % i
        print(result)


def run_day(day: int) -> Optional[Tuple[Optional[str], Optional[str], float, Optional[str]]]:
    try:
        os.chdir('day%02d' % day)
    except:
        return None
    try:
        part1 = part2 = None
        now = time.time()
        proc = subprocess.Popen('python day%d.py' % day, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while proc.poll() is None:
            output = proc.stdout.readline().decode('utf-8').replace('\r', '').replace('\n', '')
            if output.startswith('Part 1: '):
                part1 = output[8:]
            elif output.startswith('Part 2: '):
                part2 = output[8:]
            elif output != '':
                print('Day %2d |' % day, output)
        ret = proc.wait()
        then = time.time()
        delta = then - now
        if ret == 0:
            return part1, part2, delta, None
        return part1, part2, delta, 'Failed with return value %d' % ret
    except:
        return None
    finally:
        os.chdir('../')


def format_time(delta: float) -> str:
    if delta > 1:
        return '%d s' % int(delta)
    elif delta > 0.0001:
        return '%d ms' % int(delta * 1000)
    elif delta > 0.000_0001:
        return '%d us' % int(delta * 1000_000)
    else:
        return '%d ns' % int(delta * 1000_000_000)


if __name__ == '__main__':
    main()
