from itertools import product
from functools import partial
from collections import Counter
import operator


def check(p, grid, dim=3):
    r = range(-1, 2)
    if dim == 3:
        return sum(grid[map_add(p, i)] for i in product(r, r, r)) - grid[p]
    else:
        return sum(grid[(p[0] + i[0], p[1] + i[1], p[2] + i[2], p[3] + i[3])]
                   for i in product(r, r, r, r)) - grid[p]


def add(x, y):
    return tuple((i + j) for (i, j) in zip(x, y))

# @profile
def map_add(x, y):
    return tuple(map(operator.add, x, y))
    # return tuple(map(int.__add__, x, y))

def fast_add(x, y):
    return (x[0] + y[0], x[1] + y[1], x[2] + y[2])

# @profile
def count(stdin='test17.txt', dim=3):

    grid = Counter()
    with open(stdin) as f:
        for i, line in enumerate(f):
            for j, value in enumerate(line.strip()):
                if dim == 3:
                    grid[(j, i, 0)] = 1 if value == '#' else 0
                else:
                    grid[(j, i, 0, 0)] = 1 if value == '#' else 0

    for n in range(6):
        new_grid = Counter()
        for p in grid:
            if grid[p]:
                f = partial(map_add, y=p)
                for pos in map(f, product(range(-1, 2), repeat=dim)):
                    active = check(pos, grid, dim=dim)
                    if grid[pos]:
                        new_grid[pos] = 1 if active in (2, 3) else 0
                    else:
                        new_grid[pos] = 1 if active == 3 else 0
        grid = new_grid

    return sum(i for (_, i) in grid.items())


if __name__ == '__main__':
    stdin = 'test17.txt'
    c1 = count(dim=3, stdin=stdin)
    print(f"part1: {c1}")
    c2 = count(dim=4, stdin=stdin)
    print(f"part2: {c2}")
