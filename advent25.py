

def loop_size(value, subject_number):
    n = 1
    for _ in range(value):
        n *= subject_number
        n = n % 20201227
    return n


def find(x):
    n = 1
    loop_size = 1
    while loop_size < 10**9:
        n *= 7
        n = n % 20201227
        if n == x:
            break
        loop_size += 1
    return loop_size


if __name__ == '__main__':
    value = 8
    subject_number = 7
    res = loop_size(value, subject_number)
    print(f"loop size: {value}, subject_number: {subject_number}, res: {res}")

    x = find(5764801)
    y = find(17807724)
    assert loop_size(x, 17807724) == loop_size(y, 5764801)
    print(x, y)
    print(loop_size(x, 17807724))

    x = find(6929599)
    y = find(2448427)
    print(loop_size(x, 2448427))
    print("part 1", loop_size(y, 6929599))
