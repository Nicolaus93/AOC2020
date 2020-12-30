
def west(pos, steps):
    return pos[0], pos[1] - steps


def east(pos, steps):
    return pos[0], pos[1] + steps


def north(pos, steps):
    return pos[0] + steps, pos[1]


def south(pos, steps):
    return pos[0] - steps, pos[1]


def move(pos, orient, spec):
    action, steps = spec[0], spec[1]
    if action == 'N':
        pos = north(pos, steps)
    elif action == 'S':
        pos = south(pos, steps)
    elif action == 'E':
        pos = east(pos, steps)
    elif action == 'W':
        pos = west(pos, steps)
    elif action == 'R':
        orient -= steps // 90
        if orient < 0:
            orient += 4
    elif action == 'L':
        orient += steps // 90
        if orient > 3:
            orient -= 4
    elif action == 'F':
        if orient == 0:
            pos = east(pos, steps)
        elif orient == 1:
            pos = north(pos, steps)
        elif orient == 2:
            pos = west(pos, steps)
        elif orient == 3:
            pos = south(pos, steps)
        else:
            raise IndexError
    else:
        raise IndexError
    return pos, orient


if __name__ == '__main__':
    inst = []
    pos = (0, 0)
    orient = 0
    count = 0
    with open("input12.txt") as f:
        for line in f:
            i = line.strip()
            j, k = i[0], int(i[1:])
            spec = (j, k)
            pos, orient = move(pos, orient, spec)

    print(abs(pos[0]) + abs(pos[1]))
