import numpy as np
import scipy.signal


lines = []
with open("test11.txt") as f:
    for line in f:
        lines.append(line.strip())

mat = np.zeros((len(lines), len(lines[0])), dtype=int)
for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c == 'L':
            mat[i, j] = 1
        elif c == '#':
            mat[i, j] = -8
        else:
            mat[i, j] = 0

print(mat)
zeros = np.where(mat == 0)
transf = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])


# If a seat is empty (L) and there are no occupied seats adjacent to it,
# the seat becomes occupied.
# If a seat is occupied (#) and four or more seats adjacent to it are also occupied,
# the seat becomes empty.

for i in range(10):
    print(i)
    print(mat)
    B = scipy.signal.convolve2d(mat, transf, mode='same')
    print(B)
    new = np.zeros(mat.shape, dtype=int)
    ind1 = np.where(B > 0)
    ind2 = np.where(B <= -32)
    ind3 = np.where((B > - 32) & (B <= 0))
    new[ind1] = -8
    new[ind2] = 1
    new[ind3] = -8
    new[zeros] = 0
    mat = new
    # print(B, ind2)
    # print(B)


# B = scipy.signal.convolve2d(new, transf, mode='same')
# mat = np.ones(mat.shape, dtype=int)
# print(B)



# new = np.zeros(mat.shape, dtype=int)
# new[np.where(B * mat)] = -8
# print(new)
# B = scipy.signal.convolve2d(new, transf, mode='same')
# print(B)
# new = -1 * np.ones(mat.shape, dtype=int)
# new[np.where(B <= -32)] = 1
# new[zeros] = 0
# print(new)
