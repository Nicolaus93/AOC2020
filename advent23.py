# FAILING APPROACH

from itertools import cycle
from collections import deque
from tqdm import trange
import numpy as np


def move(nums, ind, verbose=False):
    if verbose: print(f"cups: {nums}, current: {nums[ind]}")
    n = m = nums[ind]
    take_away = []
    for _ in range(3):
        new_ind = ind + 1 if ind + 1 < len(nums) else 0
        take_away.append(nums.pop(new_ind))

    if verbose: print("pick up:", take_away)
    pos_to_insert = None
    while n >= min(nums):
        try:
            pos_to_insert = nums.index(n - 1)
            break
        except ValueError:
            n -= 1
    # not found
    if pos_to_insert is None:
        pos_to_insert = nums.index(max(nums))
    if verbose: print("destination:", nums[pos_to_insert])

    if pos_to_insert <= len(nums) - 1:
        if pos_to_insert == len(nums) - 1:
            nums += take_away
        else:
            nums = nums[:pos_to_insert + 1] + take_away + nums[pos_to_insert + 1:]
    else:
        nums = take_away + nums
    # rearrange around ind
    ind2 = nums.index(m)
    if ind2 != ind:
        n = abs(ind2 - ind)
        nums = nums[n:] + nums[:n]
    return nums


def allez(nums, indices, pos=0):
    n = nums[pos]
    pick_up_ind = [i if i < len(nums) else i - len(nums) for i in range(pos + 1, pos + 4)]
    pick_up = [nums[i] for i in pick_up_ind]

    x = n - 1
    dest_index = indices[x]
    while nums[dest_index] in pick_up:
        dest_index = indices[x - 1]
        x -= 1

    for i in pick_up_ind:
        nums.pop(i)

    for pos, value in enumerate(pick_up):
        nums.insert(dest_index + pos + 1, value)

    pos = pos + 4 if dest_index < pos else pos + 1
    indices = [0] * len(nums)
    for pos, value in enumerate(nums):
        indices[value - 1] = pos
    return nums, indices, pos


def move(nums, indices, pos=0, verbose=False):
    n = nums[pos]
    pick_up_ind = [i if i < len(nums) else i - len(nums) for i in range(pos + 1, pos + 4)]
    pick_up = nums[pick_up_ind]
    x = n - 1
    dest_index = indices[x]
    while nums[dest_index] in pick_up:
        dest_index = indices[x - 1]
        x -= 1

    if verbose:
        print(f"cups: {nums + 1}, {nums[pos] + 1}\npick up: {pick_up + 1}\ndestination: {nums[dest_index] + 1}")
    if dest_index > pos:
        diff = dest_index + 1 - (pos + 4)
        to_shift_ind = np.arange(pos + 4, dest_index + 1)
        to_shift = nums[to_shift_ind]
        indices[to_shift] -= 3
        indices[pick_up] += diff
        indices[pick_up] %= len(nums)
        nums[indices[pick_up]] = pick_up
        nums[indices[to_shift]] = to_shift
        pos += 1
    else:
        diff = pos - dest_index
        to_shift_ind = np.arange(dest_index + 1, pos + 1)  # % len(nums)
        to_shift = nums[to_shift_ind]
        indices[to_shift] += 3
        indices[to_shift[-3:]] %= len(nums)
        indices[pick_up] -= diff
        indices[pick_up] %= len(nums)
        nums[indices[pick_up]] = pick_up
        nums[indices[to_shift]] = to_shift
        pos += 4

    return nums, indices, pos


def run(stdin, part2=False):
    if not part2:
        nums = np.array([int(i) for i in stdin]) - 1
        moves = 100
    else:
        nums = np.hstack((np.array([int(i) for i in stdin]) - 1, np.arange(9, 10**6)))
        moves = 10**5
    ind = np.argsort(nums)
    count = pos = 0
    while count < moves:
        if count % 1000 == 0:
            print(count)
        nums, ind, pos = move(nums, ind, pos)
        pos = pos - len(nums) if pos >= len(nums) else pos
        count += 1
    return nums, ind


if __name__ == '__main__':

    stdin = "389125467"
    # stdin = '326519478'

    nums, ind = run(stdin)
    print(nums + 1)
    print(np.roll(nums + 1, -ind[0])[1:])

    # # part 2
    # nums, ind = run(stdin, part2=True)
    # ind1 = ind[0]
    # print(nums[ind1 + 1], nums[ind1 + 2])

    cyclic = [int(i) for i in stdin]
    total_moves = 10**2
    count = 0
    verbose = False
    for pos in cycle(range(len(cyclic))):
        if verbose: print(f"\n-- move {count + 1} --")
        cyclic = move(cyclic, pos, verbose=verbose)
        count += 1
        if count >= total_moves:
            break

    print(cyclic)
    ind = cyclic.index(1)
    try:
        a = cyclic[ind + 1:] + cyclic[:ind]
    except IndexError:
        a = cyclic[:ind]
    print(''.join([str(i) for i in a]))

    exit(0)

    # part 2
    stdin = "389125467"
    cyclic = [int(i) for i in stdin] + [i for i in range(10, 10**6 + 1)]
    total_moves = 10**4
    count = 0
    verbose = False
    for pos in cycle(range(len(cyclic))):
        print(count)
        cyclic = move(cyclic, pos)
        count += 1
        if count >= total_moves:
            break
