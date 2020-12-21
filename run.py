
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
        10: ('1690', '5289227976704'),
        11: ('2238', '2013'),
        12: ('508', '30761'),
        13: ('370', '894954360381385'),
        14: ('11501064782628', '5142195937660'),
        15: ('706', '19331'),
        16: ('24021', '1289178686687'),
        17: ('286', '960'),
        18: ('701339185745', '4208490449905'),
        19: ('213', '325'),
        20: ('28057939502729', '2489'),
        21: ('2798', 'gbt,rpj,vdxb,dtb,bqmhk,vqzbq,zqjm,nhjrzzj')
    })

    for i in range(1, 1 + 25):
        result = run_day(i)
        if result:
            p1, p2, delta_cp, delta_pypy = result
            result = 'Day %2d' % i
            if p1:
                result += ' | Part 1: ' + ['failed', 'passed'][p1 == expected[i][0]]
            if p2:
                result += ' | Part 2: ' + ['failed', 'passed'][p2 == expected[i][1]]
            result += ' | Time (CPython): ' + format_time(delta_cp) + ' (PyPy): ' + format_time(delta_pypy)
        else:
            result = 'Day %2d | No solution' % i
        print(result)


def run_day(day: int) -> Optional[Tuple[Optional[str], Optional[str], float, float]]:
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
        ret1 = proc.wait()
        then = time.time()
        delta_cp = then - now

        # Try again with pypy, just for timing
        now = time.time()
        proc = subprocess.Popen('pypy3 day%d.py' % day, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while proc.poll() is None:
            proc.stdout.readline()
        ret2 = proc.wait()
        then = time.time()
        delta_pypy = then - now
        if ret1 != 0 or ret2 != 0:
            raise RuntimeError('Bad return codes! %d %d' % (ret1, ret2))
        return part1, part2, delta_cp, delta_pypy
    except:
        return None
    finally:
        os.chdir('../')


def format_time(delta: float) -> str:
    if delta > 1:
        return '%3d  s' % int(delta)
    elif delta > 0.0001:
        return '%3d ms' % int(delta * 1000)
    elif delta > 0.000_0001:
        return '%3d us' % int(delta * 1000_000)
    else:
        return '%3d ns' % int(delta * 1000_000_000)


if __name__ == '__main__':
    main()
