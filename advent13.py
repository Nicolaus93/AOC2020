from chinese_remainder_thm import chinese_remainder


def euclid_algo(n, m):
    if m > n:
        n, m = m, n
    r = n % m
    if r == 0:
        return int(m)
    else:
        return euclid_algo(m, r)


def lcm(x, y):
    return x * y / euclid_algo(x, y)


def mod_lcm(x, y, z):
    return x * y / euclid_algo(x, z)


if __name__ == '__main__':
    # print(euclid_algo(13, 17))
    # print(lcm(19, 41))
    with open("input13.txt") as f:
        arrive = int(f.readline().strip())
        depart = [int(i) for i in f.readline().strip().split(",") if i.isdigit()]

    waiting_time = 10e6
    for bus in depart:
        time = bus - arrive % bus
        if time < waiting_time:
            waiting_time = time
            best_bus = bus

    print(best_bus * waiting_time)

    # part 2
    print("\npart 2")
    with open("input13.txt") as f:
        first = f.readline()
        test = [(int(value), pos) for pos, value in enumerate(f.readline().strip().split(",")) if value.isdigit()]

    n = [i[0] for i in test]
    a = [-i[1] for i in test]
    print(n, a)
    print(chinese_remainder(n, a))
