import re
from collections import Counter

directions = {'se': (1, -1), 'sw': (-1, -1), 'ne': (1, 1), 'nw': (-1, 1), 'e': (2, 0), 'w': (-2, 0)}


def neigh_colors(coord, colors):
    x1, y1 = coord
    blacks = 0
    neighbours = []
    for i in directions:
        x2, y2 = directions[i]
        neigh_coord = (x1 + x2, y1 + y2)
        if colors[neigh_coord] == 1:
            blacks += 1
        neighbours.append(neigh_coord)
    return blacks, neighbours


def move(coord, direction):
    x1, y1 = coord
    x2, y2 = directions[direction]
    return x1 + x2, y1 + y2


def flip(tile, color, blacks):
    if color[tile] == 1 and (blacks == 0 or blacks > 2):
        return 1
    elif color[tile] == 0 and blacks == 2:
        return 1
    return 0


if __name__ == '__main__':
    color = Counter()
    with open('input24.txt') as f:
        for line in f:
            instr = re.findall(r'se|sw|ne|nw|w|e', line)
            pos = (0, 0)
            for i in instr:
                pos = move(pos, i)
            color[pos] = 1 - color[pos]

    black = len([i for i in color if color[i] == 1])
    print("part 1:", black)

    # part 2
    n = 100
    for _ in range(n):
        flipping = []
        checked = set()
        for tile in color:
            # check only black tiles and their neighbours
            if color[tile] == 1:
                blacks, neighbours = neigh_colors(tile, color)
                central_plus_around = [tile] + neighbours
                for i in central_plus_around:
                    if i not in checked:
                        checked.add(i)
                        blacks, _ = neigh_colors(i, color)
                        if flip(i, color, blacks):
                            flipping.append(i)
        # flip colors
        for tile in flipping:
            color[tile] = 1 - color[tile]

    print("part 2:", len([i for i in color if color[i] == 1]))
