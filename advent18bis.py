import re


def innermost_parenthesis_in_(line):
    end = line.find(')')
    start = line[:end][::-1].find('(')
    return (-1, -1) if end == -1 else (end - start, end)


def preprocess(nums, signs):
    pos = 0
    while pos < len(signs):
        if signs[pos] == '+':
            signs = signs[:pos] + signs[pos + 1:]
            nums.insert(pos, str(eval(nums[pos] + '+' + nums[pos + 1])))
            nums = nums[:pos + 1] + nums[pos + 3:]
            continue
        pos += 1
    return nums, signs


def evaluate_(line, part2=False):
    while True:
        s, e = innermost_parenthesis_in_(line)
        expr = line[s:e] if s != -1 else line
        nums = re.findall(r'\d+', expr)
        signs = re.findall(r'\+|\*', expr)
        if part2:
            nums, signs = preprocess(nums, signs)
        res = nums[0]
        for n, op in zip(nums[1:], signs):
            res = str(eval(res + op + n))
        if s == -1:
            return int(res)
        line = line[:s - 1] + res + line[e + 1:]


if __name__ == '__main__':

    # part 1, 2
    for i in [False, True]:
        res = 0
        with open("input18.txt") as f:
            for line in f:
                res += evaluate_(line.strip(), part2=i)
        print(res)
