

def move_pos(pos, waypoint, steps):
    x, y = pos[0], pos[1]
    x += steps * waypoint[0]
    y += steps * waypoint[1]
    return (x, y)


def move_waypoint(waypoint, action, steps):
    x, y = waypoint[0], waypoint[1]
    if action == "N":
        y += steps
    elif action == 'S':
        y -= steps
    elif action == 'E':
        x += steps
    elif action == 'W':
        x -= steps
    elif action == 'R':
        if steps == 90:
            x, y = y, -x
        elif steps == 180:
            x, y = -x, -y
        elif steps == 270:
            x, y = -y, x
    elif action == 'L':
        if steps == 90:
            x, y = -y, x
        elif steps == 180:
            x, y = -x, -y
        elif steps == 270:
            x, y = y, -x
    return (x, y)


pos = (0, 0)
waypoint = (10, 1)
count = 0
with open("input12.txt") as f:
    for line in f:
        i = line.strip()
        action, steps = i[0], int(i[1:])
        if action != 'F':
            waypoint = move_waypoint(waypoint, action, steps)
        else:
            pos = move_pos(pos, waypoint, steps)

# print(pos)
print(abs(pos[0]) + abs(pos[1]))
