import re

COLORS = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}


def analyze(passport):
    necessary = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    flag = 1
    for field in necessary:
        if field not in passport:
            flag = 0
            break
    return flag


def verified(field, value):
    if field is "byr":
        value = int(value)
        return value <= 2002 and value >= 1920
    elif field is "iyr":
        value = int(value)
        return value <= 2020 and value >= 2010
    elif field is "eyr":
        value = int(value)
        return value >= 2020 and value <= 2030
    elif field is "hgt":
        return re.search(r'1[5-8][0-9]cm|19[0-3]cm|59in|6[0-9]in|7[0-6]in', value) is not None
    elif field is "hcl":
        return re.search(r'#([a-f,0-9]{6})', value) is not None
    elif field is "ecl":
        return value in COLORS
    elif field is "pid":
        return re.search(r'\b[0-9]{9}\b', value) is not None
    return False


def second_part(passport):
    necessary = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    flag = 1
    for field in necessary:
        if field not in passport or not verified(field, passport[field]):
            flag = 0
            break
    return flag


def pass_generator_2():
    with open("input4.txt") as f:
        passport = {}
        for pos, line in enumerate(f):
            reading = line.strip()
            if not reading:
                yield passport
                passport = {}
                continue
            r = re.split('[ ]', reading)
            for i in r:
                key, value = i.split(':')
                passport[key] = value
        yield passport


def pass_generator():
    with open("input4.txt") as f:
        passport = set()
        for pos, line in enumerate(f):
            reading = line.strip()
            if not reading:
                yield passport
                passport = set()
                continue
            r = re.split('[: ]', reading)
            for i in r:
                passport.add(i)
        yield passport


if __name__ == '__main__':
    count = 0
    for passport in pass_generator():
        count += analyze(passport)
    print("part 1:", count)

    # part 2
    count = 0
    for passport in pass_generator_2():
        count += second_part(passport)
    print("part 2:", count)
