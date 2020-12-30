
def traverse(slope=3, skip=False):
    with open("input3.txt") as f:
        count = trees = 0
        for pos, line in enumerate(f):
            line = line.strip()
            if (pos == 0) or (pos % 2 != 0 and skip):
                continue
            count += slope
            if count >= len(line):
                count = count % (len(line))
            if line[count] is '#':
                trees += 1
    return trees


tot = 1
for i in [1, 3, 5, 7]:
    tot *= traverse(i)
tot *= traverse(1, skip=True)
print(tot)
