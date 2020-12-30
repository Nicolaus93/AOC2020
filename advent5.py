

def read_passes():
    highest_id = -1
    with open("boarding_pass.txt") as f:
        for b_pass in f:
            row, column = decode(b_pass)
            seat_id = row * 8 + column
            if seat_id > highest_id:
                highest_id = seat_id
    return highest_id


def decode(boarding_pass):
    row = 0
    column = 0
    for pos, value in enumerate(boarding_pass):
        if value is 'B':
            row += 2**(6 - pos)
    for pos, value in enumerate(boarding_pass[7:]):
        if value is 'R':
            column += 2**(2 - pos)
    return row, column


def get_ids():
    ids = []
    with open("boarding_pass.txt") as f:
        for b_pass in f:
            row, column = decode(b_pass)
            ids.append(row * 8 + column)
    return ids


if __name__ == '__main__':
    code = 'FBFBBFF'
    codes = ['BFFFBBFRRR', 'FFFBBBFRRR', 'BBFFBBFRLL']
    for i in codes:
        row, column = decode(i)
        print("row {}, colums {}, sead ID {}".format(row, column, row * 8 + column))

    print(read_passes())
    all_ids = sorted(get_ids())
    inspect = [i - j for (i, j) in zip(all_ids, all_ids[1:])]
    for pos, value in enumerate(inspect):
        if value != -1:
            print(all_ids[pos], all_ids[pos + 1])
