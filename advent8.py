
def exec(op):
    op, num = op.split(" ")
    if op == "nop":
        return (0, 1)
    elif op == "acc":
        return (int(num), 1)
    elif op == "jmp":
        return (0, int(num))
    return -1


def run(instructions):
    pointer = count = 0
    visited = {0}
    while True:
        temp, steps = exec(instructions[pointer])
        pointer += steps
        count += temp
        if pointer in visited or pointer >= len(instructions):
            break
        else:
            visited.add(pointer)
    return count, pointer


if __name__ == '__main__':
    with open("input8.txt") as f:
        content = f.readlines()
    content = [i.strip() for i in content]
    pointer = 0
    count = 0
    visited = {0}
    while True:
        temp, steps = exec(content[pointer])
        pointer += steps
        count += temp
        if pointer in visited:
            break
        else:
            visited.add(pointer)

    print("count: {}".format(count))

    # part 2
    jumps = [pos for pos, value in enumerate(content) if value.split(" ")[0] == "jmp"]
    for i in jumps:
        new_content = [value for pos, value in enumerate(content) if pos != i]
        new_content.insert(i, "nop +0")
        count, pointer = run(new_content)
        if pointer == len(new_content):
            print("new count: {}".format(count))
            break
