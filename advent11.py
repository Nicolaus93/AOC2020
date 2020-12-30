import numpy as np
from tqdm import tqdm


def step(matrix):
    new_mat = np.zeros(matrix.shape, dtype=int)
    for i, row in enumerate(matrix):
        for j, state in enumerate(row):
            rows = [None] * 2
            if i == 0:
                rows[0], rows[1] = i, i + 2
            elif i == matrix.shape[0] - 1:
                rows[0], rows[1] = i - 1, i + 1
            else:
                rows[0], rows[1] = i - 1, i + 2

            cols = [None] * 2
            if j == 0:
                cols[0], cols[1] = j, j + 2
            elif j == matrix.shape[1] - 1:
                cols[0], cols[1] = j - 1, j + 1
            else:
                cols[0], cols[1] = j - 1, j + 2

            submat = matrix[rows[0]:rows[1], cols[0]:cols[1]]
            if matrix[i, j] == 1:
                if -1 not in submat:
                    new_mat[i, j] = -1
                else:
                    new_mat[i, j] = 1
            elif matrix[i, j] == -1:
                count = 0
                for k in submat.flatten():
                    if k == -1:
                        count += 1
                if count > 4:
                    new_mat[i, j] = 1
                else:
                    new_mat[i, j] = -1

    return new_mat


def step2(matrix):
    new_mat = np.zeros(matrix.shape, dtype=int)
    N, M = matrix.shape
    for i, row in enumerate(matrix):
        for j, state in enumerate(row):
            off2 = j - i
            major = np.diagonal(matrix, offset=off2)
            pos2 = min(i, j)
            off1 = -matrix.shape[1] + (j + i) + 1
            minor = np.diagonal(np.rot90(matrix), offset=off1)
            pos1 = min(i, i - off1)
            one = matrix[i, 0:j][::-1]
            two = major[0:pos2][::-1]
            three = matrix[0:i, j][::-1]
            four = minor[0:pos1][::-1]
            five = matrix[i, j + 1:]
            six = major[pos2 + 1:]
            seven = matrix[i + 1:, j]
            eight = minor[pos1 + 1:]
            first_seat = []
            for arr in [one, two, three, four, five, six, seven, eight]:
                try:
                    x = arr[np.where(arr)[0][0]]
                except IndexError:
                    continue
                first_seat.append(x)
            if matrix[i, j] == 1:
                if -1 not in first_seat:
                    new_mat[i, j] = -1
                else:
                    new_mat[i, j] = 1
            elif matrix[i, j] == -1:
                count = 0
                for k in first_seat:
                    if k == -1:
                        count += 1
                if count >= 5:
                    new_mat[i, j] = 1
                else:
                    new_mat[i, j] = -1
    return new_mat


lines = []
with open("input11.txt") as f:
    for line in f:
        lines.append(line.strip())

mat = np.zeros((len(lines), len(lines[0])), dtype=int)
for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c == 'L':
            mat[i, j] = 1
        elif c == '#':
            mat[i, j] = -1
        else:
            mat[i, j] = 0

for i in tqdm(range(1000)):
    new_mat = step2(mat)
    if np.array_equal(new_mat, mat):
        print(sum([1 for i in new_mat.flatten() if i == -1]))
        break
    else:
        mat = new_mat
