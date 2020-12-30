from itertools import product
from functools import partial
import operator


def check(p, grid, dim=3):
    return sum(fast_add(p, i, dim=dim) in grid for i in product(
        range(-1, 2), repeat=dim)) - (p in grid)


def add(x, y):
    return tuple(map(operator.add, x, y))


def fast_add(x, y, dim=3):
    if dim == 3:
        return (x[0] + y[0], x[1] + y[1], x[2] + y[2])
    else:
        return (x[0] + y[0], x[1] + y[1], x[2] + y[2], x[3] + y[3])

def count(stdin='input17.txt', dim=3):

    grid = set()
    with open(stdin) as f:
        for i, line in enumerate(f):
            for j, value in enumerate(line.strip()):
                if value == '#':
                    grid.add((j, i, 0, 0)[:dim])

    for _ in range(6):
        new_grid = set()
        memory = set()
        for point in grid:
            neighbours = map(partial(fast_add, y=point, dim=dim), product(range(-1, 2), repeat=dim))
            for p in neighbours:
                if p in memory:
                    continue
                memory.add(p)
                neigh_active = check(p, grid, dim=dim)
                if p in grid and neigh_active in (2, 3) or p not in grid and neigh_active == 3:
                    new_grid.add(p)
        grid = new_grid

    return len(grid)


if __name__ == '__main__':
    stdin = 'input17.txt'
    c1 = count(dim=3, stdin=stdin)
    print(f"part1: {c1}")
    c2 = count(dim=4, stdin=stdin)
    print(f"part2: {c2}")
