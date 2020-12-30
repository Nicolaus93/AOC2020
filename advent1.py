from collections import defaultdict
s = set()
numbers = []


def read_numbers():
    numbers = []
    with open("input.txt") as f:
        for line in f:
            num = int(line)
            numbers.append(num)
    return sorted(numbers)


def check_triplets(sorted_numbers):
    temp = [2020 - i for i in sorted_numbers]
    temp2 = [i - j for (i, j) in zip(temp, sorted_numbers[1:])]
    temp3 = [i - j for (i, j) in zip(temp2, sorted_numbers[2:])]
    return temp3


nums = read_numbers()
found = check_triplets(nums)
# print(found)

with open("input.txt") as f:
    for line in f:
        num = int(line)
        s.add(num)

for i in s:
    possible = 2020 - i
    if possible in s:
        print(i * possible)

s2 = defaultdict(list)
for pos, value in enumerate(nums):
    for j in nums[pos + 1:]:
        s2[(value, j)] = value + j

for i in nums:
    for key in s2:
        if s2[key] + i == 2020:
            print(i, key)
            print(i * key[0] * key[1])
            exit(0)
