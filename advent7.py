import re


def memoize_color(f):
    memory = {}

    def inner(graph, col):
        if col not in memory:
            memory[col] = f(graph, col)
        return memory[col]

    return inner


@memoize_color
def search(graph, color):
    if color not in graph:
        return 0
    ans = 0
    for i in graph[color]:
        if i == "shiny gold":
            return 1
        ans += search(graph, i)
    return ans


@memoize_color
def count_cols(graph, color):
    if color not in graph:
        return 1
    ans = 0
    for i in graph[color]:
        new_col, how_many = i
        ans += (1 + count_cols(graph, new_col)) * how_many
    return ans


def first_part():
    colors = dict()
    with open("input7.txt") as f:
        for line in f:
            r = re.findall(r"(\w+ \w+)(?= bags*)", line)
            container, *contained = r
            colors[container] = contained
    count = 0
    for c in colors:
        if search(colors, c) > 0:
            count += 1
    return count


def second_part():
    colors = dict()
    with open("input7.txt") as f:
        for line in f:
            r = re.findall(r"(\d \w+ \w+|\w+ \w+)(?= bags*)", line)
            container, *contained = r
            colors[container] = list()
            for i in contained:
                splitted = i.split(" ", 1)
                if splitted[0].isnumeric():
                    colors[container].append((splitted[1], int(splitted[0])))
                else:
                    colors[container].append((None, 0))
    return count_cols(colors, "shiny gold")


if __name__ == '__main__':
    print(first_part())
    print(second_part())
