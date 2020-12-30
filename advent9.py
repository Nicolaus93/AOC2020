from itertools import combinations


def search(x, numbers):
    for pos, value in enumerate(numbers):
        current_sum = 0
        temp = []
        for j in numbers[pos:]:
            current_sum += j
            temp.append(j)
            if current_sum > x:
                break
            elif current_sum == x:
                s_temp = sorted(temp)
                return s_temp[0] + s_temp[-1]


with open("input9.txt") as f:
    lines = [int(i.strip()) for i in f]

n = 25
for pos, value in enumerate(lines[n:]):
    s = set(sum(i) for i in combinations(lines[pos:pos + n], 2))
    if value not in s:
        break

print("part 1:", value)
print("part 2:", search(value, lines))
