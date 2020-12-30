
numbers = []
with open("test10.txt") as f:
    for line in f:
        numbers.append(int(line.strip()))

s_numbers = sorted(numbers)
diff = [j - i for i, j in zip(s_numbers, s_numbers[1:])]
count_1 = sum(1 if i == 1 else 0 for i in diff) + 1
count_3 = sum(1 if i == 3 else 0 for i in diff) + 1
print(count_1 * count_3)

# part 2
count = dict()
s_numbers = [0] + s_numbers + [s_numbers[-1] + 3]
count = {i: 0 for i in s_numbers}
rev = [i for i in reversed(s_numbers)]
for pos, value in enumerate(rev):
    if pos == 0:
        count[value] = 1
        continue
    nodes = rev[max(0, pos - 3):pos]
    for i in nodes:
        if i - value <= 3:
            count[value] += count[i]

print(count[0])
