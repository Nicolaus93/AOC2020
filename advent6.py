

with open("input6test.txt") as f:
    count = 0
    group = set()
    for line in f:
        if not line.strip():
            count += len(group)
            group = set()
        else:
            for c in line.strip():
                group.add(c)
    count += len(group)

print("part 1:", count)


with open("input6.txt") as f:
    count = 0
    answer = f.readline().strip()
    group = set([i for i in answer])
    answer = f.readline()
    while answer:
        ans = answer.strip()
        if not ans:
            count += len(group)
            try:
                ans = f.readline().strip()
                group = set([i for i in ans])
            except:
                exit(0)
        else:
            c = set([i for i in ans])
            group = group & c
        answer = f.readline()
    count += len(group)

print("part 2:", count)
