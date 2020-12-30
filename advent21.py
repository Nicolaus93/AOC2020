import re
from collections import defaultdict


food = defaultdict(set)
all_ingredients = []
with open("input21.txt") as f:
    for line in f:
        part1, part2 = line.split('(')
        ingredients = re.findall(r'\w+', part1)
        all_ingredients += ingredients
        allergens = [i for i in re.findall(r'\w+', part2) if i != 'contains']
        for i in allergens:
            if i in food:
                food[i] &= set(ingredients)
            else:
                food[i] = set(ingredients)

# part 1
print(food)
all_allerg = set()
for i in food:
    all_allerg |= food[i]
print(len(all_allerg) == len(food))

count = 0
for i in all_ingredients:
    if i not in all_allerg:
        count += 1
print(count)


# part 2
def assignx(food, correspondence, assigned):
    for i in food:
        remaining = food[i] - assigned
        if len(remaining) == 1:
            correspondence[i] = list(remaining)[0]
            assigned = remaining
            del food[i]
            for j in food:
                food[j] -= assigned
            return assigned
    raise ValueError


eccolo = dict()
count = 0
assigned = set()
while food and count <= 100:
    assigned = assignx(food, eccolo, assigned)
    count += 1

s = ''
for i in sorted(eccolo.keys()):
    s += eccolo[i] + ','
print(s[:-1])
