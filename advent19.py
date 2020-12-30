import re
from collections import defaultdict
from itertools import product


def decode(key):
    res = []
    # ['2 3', '3 2']
    for code in d[key]:
        if code in MEMORY:
            res += MEMORY[code]
        else:
            # '2', '3'
            pattern = re.findall(r'\d+', code)
            if not pattern:
                # ['a']
                return [code]
            else:
                iterables = [possible_values[k] for k in pattern]
                temp = [''.join(i) for i in product(*iterables)]
                MEMORY[code] = temp
                res += temp
    return res


def level(key):
    # add memory
    current = 0
    for code in d[key]:
        pattern = re.findall(r'\d+', code)
        if not pattern:
            return current
        for n in pattern:
            # walrus?
            computed_level = 1 + level(n)
            if computed_level > current:
                current = computed_level
    return current


def part2(to_test):
    len42s = len(possible_values['42'][0])
    len31s = len(possible_values['31'][0])

    count31 = count42 = 0
    rev = to_test[::-1]
    end = rev[:len31s]
    while end[::-1] in thirtyone:
        rev = rev[len31s:]
        end = rev[:len31s]
        count31 += 1

    if count31 == 0:
        return 0

    to_test = rev[::-1]

    beginning = to_test[:len42s]
    while beginning in fortytwo:
        to_test = to_test[len42s:]
        beginning = to_test[:len42s]
        count42 += 1

    if count42 > count31 and count42 * 8 == len(rev):
        return 1

    return 0


def part22(to_test):
    len42s = len(possible_values['42'][0])
    len31s = len(possible_values['31'][0])
    if len(to_test) < (len42s + len31s):
        return 0

    # test now for patterns 42 42 31 (extended)

    # test if in 42
    copy = to_test
    count = 0
    beginning = to_test[:len42s]
    while beginning in fortytwo:
        to_test = to_test[len42s:]
        beginning = to_test[:len42s]
        count += 1

    if len(to_test) == 0 or count <= 2:
        return 0

    to_test = copy[len42s * count:]

    # test if in 31
    count = 0
    beginning = to_test[:len31s]
    while beginning in thirtyone:
        to_test = to_test[len31s:]
        beginning = to_test[:len31s]
        count += 1

    if len(to_test) == 0:
        return 1
    return 0


if __name__ == '__main__':
    lines = open("input19.txt").readlines()
    d = defaultdict(list)
    to_match = []
    for line in lines:
        if re.match(r'\d+:.*', line):
            key, value = line.split(":")
            value = value.strip().replace('"', '')
            d[key] = value.split('|')
        else:
            c_len = len(line.strip())
            to_match.append(line.strip())

    levels = defaultdict(list)
    for key in d:
        n = level(key)
        levels[n].append(key)

    i = 0
    possible_values = defaultdict(list)
    MEMORY = dict()
    while i < len(levels):
        for key in levels[i]:
            possible_values[key] = decode(key)
            lev = i
        i += 1

    zero = set(possible_values['0'])
    fortytwo = set(possible_values['42'])
    thirtyone = set(possible_values['31'])
    print("len42:", len(possible_values['42'][0]))
    print("len31:", len(possible_values['31'][0]))

    count1 = count2 = 0
    for test in to_match:
        if not test:
            continue
        if test in zero:
            count1 += 1
        else:
            count2 += part2(test)

    print("count1: ", count1)
    print("count2: ", count1 + count2)
