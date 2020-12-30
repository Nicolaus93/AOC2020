import re


def matches(line, opendelim='(', closedelim=')'):
    stack = []

    for m in re.finditer(r'[{}{}]'.format(opendelim, closedelim), line):
        pos = m.start()

        c = line[pos]

        if c == opendelim:
            stack.append(pos + 1)

        elif c == closedelim:
            if len(stack) > 0:
                prevpos = stack.pop()
                yield (prevpos, pos, len(stack))
            else:
                # wrong input
                print("encountered extraneous closing quote at pos {}: '{}'"
                      .format(pos, line[pos:]))
                pass

    # for wrong input
    if len(stack) > 0:
        for pos in stack:
            print("expecting closing quote to match open quote starting at: '{}'"
                  .format(line[pos - 1:]))


def get_next(line, part2=False):
    try:
        openpos, closepos, level = next(matches(line))
        temp = line[openpos:closepos]
    except StopIteration:
        temp = line
        openpos = -1
    nums = re.findall(r'\d+', temp)
    signs = re.findall(r'\+|\*', temp)
    if part2:
        nums, signs = preprocess(nums, signs)
    res = solve(nums, signs)
    if openpos == -1:
        return res, 1
    else:
        return line[:openpos - 1] + res + line[closepos + 1:], 0


def transform(line, part2=False):
    s, e = innermost_parenthesis_in_(line)
    expr = line[s:e] if s != -1 else line
    nums = re.findall(r'\d+', expr)
    signs = re.findall(r'\+|\*', expr)
    if part2:
        nums, signs = preprocess(nums, signs)
    res = nums[0]
    for n, op in zip(nums[1:], signs):
        res = str(eval(res + op + n))
    if s != -1:
        return line[:s - 1] + res + line[e + 1:], 0
    else:
        return res, 1


def evaluate(line, part2=False):
    while True:
        line, flag = transform(line, part2=part2)
        if flag:
            return int(line)


def solve(nums, signs):
    res = nums[0]
    for n, op in zip(nums[1:], signs):
        res = str(eval(res + op + n))
    return res


def innermost_parenthesis_in_(line):
    """
    This function doesn't handle wrong inputs.
    """
    start = end = -1
    for pos, value in enumerate(line):
        if value == '(':
            start = pos
        elif value == ')':
            end = pos
            return start + 1, end
    return start, end


def preprocess(nums, signs):
    pos = 0
    while pos < len(signs):
        if signs[pos] == '+':
            signs.pop(pos)
            nums.insert(pos, str(eval(nums[pos] + '+' + nums[pos + 1])))
            nums.pop(pos + 1)
            nums.pop(pos + 1)
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
            return res
        line = line[:s - 1] + res + line[e + 1:]


if __name__ == '__main__':

    # part 1, 2
    for i in [False, True]:
        res = 0
        with open("input18.txt") as f:
            for line in f:
                res += evaluate(line.strip(), part2=i)
        print(res)
