import re
import bisect


def find_le(a, x):
    'Find rightmost value less than or equal to x'
    i = bisect.bisect_right(a, x)
    if i:
        return i - 1
    return -1


def locate(intervals, n1, n2):
    i1 = find_le(intervals, n1)
    i2 = find_le(intervals, n2)
    if i1 == -1:
        # first is smallest
        if i2 == i1:
            intervals = [n1, n2] + intervals
        else:
            intervals[0] = n1
            if i2 % 2 == 0:
                # P
                intervals = [intervals[0]] + intervals[i2 + 1:]
            else:
                # D
                intervals = [intervals[0]] + intervals[i2:]
    elif i1 == i2:
        if i1 % 2 == 1:
            # non prende il caso in cui bisogna inserire al'inizio
            bisect.insort_left(intervals, n1)
            bisect.insort_left(intervals, n2)
    elif i1 % 2 == 0:
        if i2 % 2 == 0:
            # P/P
            intervals = intervals[:i1 + 1] + intervals[i2 + 1:]
        else:
            # P/D
            intervals[i2] = n2
            intervals = intervals[:i1 + 1] + intervals[i2:]
    else:
        if i2 % 2 == 0:
            # D/P
            intervals[i1 + 1] = n1
            intervals = intervals[:i1 + 2] + intervals[i2 + 1:]
        else:
            # D/D
            intervals[i1] = n1
            intervals[i2] = n2
            intervals = intervals[:i1 + 2] + intervals[i2:]
    return intervals


def candidate(intervals, row):
    for field in intervals:
        int1, int2 = intervals[field]
        flag = True
        for n in row:
            if n < int1[0] or n > int2[1] or (n > int1[1] and n < int2[0]):
                flag = False
                break
        if flag:
            yield field


if __name__ == '__main__':
    stdin = "input16.txt"
    with open(stdin) as f:
        p = re.compile(r".+: (\d+)-(\d+) or (\d+)-(\d+)")
        not_valid = 0
        valid = []
        intervals = []
        all_int = dict()  # for part 2
        for pos, line in enumerate(f):
            nums = p.match(line)
            if nums:
                n1, n2, n3, n4 = [int(i) for i in nums.groups()]
                intervals = locate(intervals, n1, n2)
                intervals = locate(intervals, n3, n4)
                # for part 2
                all_int[pos] = []
                all_int[pos].append((n1, n2))
                all_int[pos].append((n3, n4))
            else:
                only_nums = [int(i) for i in re.findall(r'\d+', line)]
                flag = not_valid  # for part 2
                for n in only_nums:
                    index = find_le(intervals, n)
                    if index % 2 == 1:
                        if n != intervals[index]:
                            not_valid += n
                # for part 2
                if flag == not_valid and only_nums:
                    ticket = [int(i) for i in line.strip().split(",")]
                    valid.append(ticket)

    print("not valid sum:", not_valid)
    my_ticket, valid = valid[0], valid[1:]

    # part 2
    columns = [[row[j] for row in valid] for j in range(len(valid[0]))]
    constraints = [(pos, [j for j in candidate(all_int, value)]) for (pos, value) in enumerate(columns)]

    col_bij = dict()
    for i in sorted(constraints, key=lambda x: len(x[1])):
        col_id, possible_fields = i
        for field in possible_fields:
            if field not in col_bij:
                col_bij[field] = col_id

    prod = 1
    for i in range(6):
        prod *= my_ticket[col_bij[i]]
    print(prod)
