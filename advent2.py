import re


def check(user_input):
    lower, upper, letter, password = re.split('-| |: |', user_input)
    count = password.count(letter)
    if count > int(upper) or count < int(lower):
        return 0
    return 1


def new_rule(user_input):
    lower, upper, letter, password = re.split('-| |: |', user_input)
    a = password[int(lower) - 1] is letter
    b = password[int(upper) - 1] is letter
    return a ^ b


test = ["1-3 a: abcde", "1-3 b: cdefg", "2-9 c: ccccccccc"]
for i in test:
    print(new_rule(i))

with open("input2.txt") as f:
    valid = 0
    for line in f:
        valid += new_rule(line)

print(valid)
