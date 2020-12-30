from tqdm import trange


def play(nums, n):
    MAX = max(nums)
    linked_list = {i: j for (i, j) in zip(nums, nums[1:])}
    linked_list[nums[-1]] = nums[0]
    pos = nums[0]

    for _ in trange(n):
        pick_up = [linked_list[pos]]
        for _ in range(2):
            pick_up.append(linked_list[pick_up[-1]])

        destination = MAX if pos - 1 == 0 else pos - 1
        while destination in pick_up:
            destination = MAX if destination - 1 == 0 else destination - 1

        linked_list[pos] = linked_list[pick_up[-1]]
        linked_list[pick_up[-1]] = linked_list[destination]
        linked_list[destination] = pick_up[0]
        # update pos
        pos = linked_list[pos]
    return linked_list


if __name__ == '__main__':

    # stdin = '389125467'
    stdin = '326519478'

    nums = [int(i) for i in stdin]
    nums = play(nums, 100)
    result = [nums[1]]
    while result[-1] != 1:
        result.append(nums[result[-1]])
    print(''.join([str(c) for c in result[:-1]]))

    # part 2
    nums = [int(i) for i in stdin] + [i for i in range(10, 10**6 + 1)]
    res = play(nums, 10**7)
    x = res[1]
    y = res[x]
    print(x, y, x * y)
