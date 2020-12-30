import re


def sum_mask(mask, num):
    res = ''
    for i, j in zip(num, mask):
        if j == 'X':
            res += i
        else:
            res += j
    return res


def sum_mask_2(mask, num):
    res = ''
    for i, j in zip(num, mask):
        if j == 'X':
            res += 'X'
        elif j == '1':
            res += '1'
        elif j == '0':
            res += i
        else:
            raise ValueError
    return res


def decode(masked_num, in_pos=0, current_res=''):
    if in_pos == len(masked_num):
        return current_res
    for pos, value in enumerate(masked_num[in_pos:]):
        if value != 'X':
            current_res += value
        else:
            return (decode(masked_num, in_pos + pos + 1, current_res + '0'),
                    decode(masked_num, in_pos + pos + 1, current_res + '1'))
    return current_res


def flatten(list_of_lists):
    if len(list_of_lists) == 0:
        return list_of_lists
    if isinstance(list_of_lists[0], tuple):
        return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
    return list_of_lists[:1] + flatten(list_of_lists[1:])


if __name__ == '__main__':
    memory = dict()
    with open("input14.txt") as f:
        mask_p = re.compile(r"mask = .*")
        for line in f:
            if mask_p.match(line):
                mask = line.strip().split("=")[1][1:]
            else:
                p = re.compile(r"\d+")
                m = p.findall(line)
                binary_n = "{0:b}".format(int(m[1]))
                binary_n = '0' * (36 - len(binary_n)) + binary_n
                memory[m[0]] = sum_mask(mask, binary_n)

    res = 0
    for address in memory:
        res += int(memory[address], 2)
    print("part1:", res)

    # part 2
    memory = dict()
    with open("input14.txt") as f:
        mask_p = re.compile(r"mask = .*")
        for line in f:
            if mask_p.match(line):
                mask = line.strip().split("=")[1][1:]
            else:
                p = re.compile(r"\d+")
                m = p.findall(line)
                binary_n = "{0:b}".format(int(m[0]))
                binary_n = '0' * (36 - len(binary_n)) + binary_n
                masked_num = sum_mask_2(mask, binary_n)
                for address in flatten(decode(masked_num)):
                    memory[address] = int(m[1])
    res = 0
    for address in memory:
        res += memory[address]
    print("part 2:", res)
