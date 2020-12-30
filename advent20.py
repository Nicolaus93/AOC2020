import re
import numpy as np
from collections import defaultdict, Counter
from copy import deepcopy

OPPOSITE = {'up': 'down', 'down': 'up', 'right': 'left', 'left': 'right'}


def encode(mat, d, ind):
    up_row = tuple(mat[0])
    down_row = tuple(mat[-1])
    left_col = tuple(mat[:, 0])
    right_col = tuple(mat[:, -1])
    d[up_row].add(ind)
    d[down_row].add(ind)
    d[left_col].add(ind)
    d[right_col].add(ind)


def find_orientation(mat, pattern, direc):
    for i in range(4):
        mat = np.rot90(mat, k=i)
        if direc == 'up':
            if tuple(mat[0]) == pattern:
                return mat
            elif tuple(mat[0][::-1]) == pattern:
                return np.fliplr(mat)
        elif direc == 'down':
            if tuple(mat[-1]) == pattern:
                return mat
            elif tuple(mat[-1][::-1]) == pattern:
                return np.fliplr(mat)
        elif direc == 'left':
            if tuple(mat[:, 0]) == pattern:
                return mat
            elif tuple(mat[:, 0][::-1]) == pattern:
                return np.flipud(mat)
        elif direc == 'right':
            if tuple(mat[:, -1]) == pattern:
                return mat
            elif tuple(mat[:, -1][::-1]) == pattern:
                return np.flipud(mat)
        else:
            raise ValueError
    return -1


def find_side_of(pattern, mat):
    x1 = tuple(mat[0])
    x2 = tuple(mat[-1])
    x3 = tuple(mat[:, 0])
    x4 = tuple(mat[:, -1])
    if x1 == pattern: return 'up', pattern
    elif x1 == pattern[::-1]: return 'up', pattern[::-1]
    elif x2 == pattern: return 'down', pattern
    elif x2 == pattern[::-1]: return 'down', pattern[::-1]
    elif x3 == pattern: return 'left', pattern
    elif x3 == pattern[::-1]: return 'left', pattern[::-1]
    elif x4 == pattern: return 'right', pattern
    elif x4 == pattern[::-1]: return 'right', pattern[::-1]
    raise ValueError


def build_sol(path, inv_d):
    for pos, value in enumerate(zip(path, path[1:])):
        current, next_one = value
        pattern = inv_d[(current, next_one)] if pos == 0 else previous_match[0]
        mat = tiles[current] if pos == 0 else find_orientation(tiles[current], pattern, previous_match[1])
        if pos == 0:
            side, pattern = find_side_of(pattern, mat)
        else:
            side, pattern = find_side_of(inv_d[(current, next_one)], mat)
        previous_match = (pattern, OPPOSITE[side])
        yield mat, side


def convert_coords(path):
    coords = [(0, 0)]
    for move in path:
        x, y = coords[-1]
        if move == 'up': x -= 1
        elif move == 'down': x += 1
        elif move == 'right': y += 1
        elif move == 'left': y -= 1
        coords.append((x, y))
    min_x = min(coords, key=lambda x: x[0])[0]
    min_y = min(coords, key=lambda x: x[1])[1]
    coords = [(i[0] - min_x, i[1] - min_y) for i in coords]
    return coords


def plot(big_mat, original=False):
    s = ''
    for y, row in enumerate(big_mat):
        if y % 10 == 0 and original:
            s += '\n'
        for x, i in enumerate(row):
            if x % 10 == 0 and original:
                s += ' '
            s += '#' if i == 1 else '.'
        s += '\n'
    print(s)


def count_sea_monsters(mat):
    pattern = '                  # \n#    ##    ##    ###\n #  #  #  #  #  #   '
    array = pattern.split("\n")
    pattern = np.array([[1 if i == '#' else 0 for i in row] for row in array])
    indices = np.where(pattern)
    x, y = np.array(pattern).shape
    func = [lambda z: z, np.flipud, np.fliplr]
    for i in range(4):
        mat = np.rot90(mat, k=i)
        for f in func:
            mat = f(mat)
            count = 0
            for i in range(mat.shape[0] - x):
                for j in range(mat.shape[1] - y):
                    submat = mat[i:i + x, j:j + y]
                    if np.all(submat[indices] == 1):
                        count += 1
            if count > 0:
                return len(np.where(mat)[0]) - count * len(indices[0])
    return 0


if __name__ == '__main__':
    tiles = dict()
    with open("input20.txt") as f:
        current_tile = []
        for line in f:
            if re.match(r'Tile .*', line):
                if len(current_tile) > 0:
                    tiles[int(num)] = np.array(current_tile)
                    current_tile = []
                num = line.strip().split(" ")[1][:-1]
            else:
                row = [1 if i == '#' else 0 for i in line.strip()]
                if row:
                    current_tile.append(row)
        tiles[int(num)] = np.array(current_tile)

    d = defaultdict(set)
    for ind in tiles:
        tile = tiles[ind]
        encode(tile, d, ind)
        encode(np.fliplr(tile), d, ind)
        encode(np.flipud(tile), d, ind)

    # part 1
    num_matchings = Counter()
    for pattern in d:
        if len(d[pattern]) >= 2:
            for ind in d[pattern]:
                num_matchings[ind] += 1

    ans = 1
    for ind in num_matchings:
        if num_matchings[ind] == 4:
            # we are counting every match twice
            # for the first part we only need the corners
            ans *= ind
    print("part 1 answer:", ans)

    # part 2
    graph = defaultdict(set)
    for pattern in d:
        if len(d[pattern]) > 1:
            i, j = list(d[pattern])
            graph[i].add(j)
            graph[j].add(i)

    # print("\nMatrix Corners:")
    corners = []
    for i in graph:
        if len(graph[i]) == 2:
            # print(i, list(graph[i]))
            corners.append(i)

    orig_graph = deepcopy(graph)
    length = len(graph)
    start = corners[0]
    path = [start]
    count = 0
    MAX = len(graph)
    while count < MAX:
        neighbours = sorted(list(graph[start]), key=lambda x: (len(graph[x]), len(orig_graph[x])))
        for node in neighbours:
            graph[node] -= {start}
        try:
            start = neighbours[0]
        except IndexError:
            break
        path.append(start)
        count += 1

    inv_d = dict()
    for pattern in d:
        if len(d[pattern]) >= 2:
            key = tuple(d[pattern])
            inv_d[key] = pattern
            inv_d[key[::-1]] = pattern

    res = [i for i in build_sol(path, inv_d)]
    directions = [i[1] for i in res]
    matrices = [i[0] for i in res]
    matrices.append(tiles[path[-1]])

    dim = len(tiles[path[0]])
    N = int(np.sqrt(len(path)))
    a = np.zeros((N * dim, N * dim), dtype=int)
    for pos, value in zip(convert_coords(directions), matrices):
        x1 = pos[0] * dim
        x2 = x1 + dim
        y1 = pos[1] * dim
        y2 = y1 + dim
        a[x1:x2, y1:y2] = value
    # plot(a, original=True)

    remove = [i * dim for i in range(N)] + [i * dim - 1 for i in range(1, N + 1)]
    to_keep = [i for i in range(N * dim) if i not in remove]
    b = a[to_keep]
    b = b[:, to_keep]
    # plot(b)

    print("part 2 ans:", count_sea_monsters(b))
