from collections import defaultdict
from tqdm import trange


def play(count, previous, steps=2020):
    pos = len(count)
    for i in trange(pos + 1, steps + 1):
        try:
            previous = count[previous][-1] - count[previous][-2]
        except IndexError:
            previous = 0
        count[previous].append(i)
    return previous


def alt(count, previous, steps=2020):
    pos = len(count)
    for i in trange(pos + 1, steps):
        spoken = 0 if previous not in count else i - count[previous]
        count[previous] = i
        previous = spoken
    return previous


if __name__ == '__main__':
    spoken = [0, 3, 6]
    # spoken = [1, 3, 2]
    # spoken = [3, 2, 1]
    # spoken = [7, 12, 1, 0, 16, 2]
    # spoken = [3, 1, 2]
    count = defaultdict(list)
    for pos, value in enumerate(spoken):
        count[value].append(pos + 1)

    print(play(count, spoken[-1], 30000000))
    count = {value: pos + 1 for (pos, value) in enumerate(spoken[:-1])}
    print(count)
    print("res:", alt(count, spoken[-1], 30000000))
