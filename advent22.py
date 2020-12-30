import re
from copy import deepcopy


def single_round(players):
    p1, p2 = players
    n1, n2 = p1.pop(0), p2.pop(0)
    if n1 > n2:
        p1 += [n1, n2]
    else:
        p2 += [n2, n1]


def update_winner(ind, players, n1, n2):
    if ind == 0:
        players[0] += [n1, n2]
    elif ind == 1:
        players[1] += [n2, n1]
    else:
        raise ValueError


def recursive_combat(players, count=1, game=1, verbose=True):
    ###
    if verbose: print(f"=== Game {game} ===\n")
    MEMORY = set()
    p1, p2 = players
    new_game_count = 1
    while p1 and p2:
        if verbose: print(f"-- Round {count} (Game {game}) --")
        ###
        if verbose: print(f"Player 1's deck: {p1}")
        if verbose: print(f"Player 2's deck: {p2}")
        ###
        if len(p1) > 1 and len(p2) > 1:
            current_state = (tuple(p1), tuple(p2))
            if current_state in MEMORY:
                if verbose: print("Infinite Loop!")
                return 0
            else:
                MEMORY.add(current_state)
        n1, n2 = p1.pop(0), p2.pop(0)
        ###
        if verbose: print(f"Player 1 plays {n1}")
        if verbose: print(f"Player 2 plays {n2}")
        ###
        if len(p1) >= n1 and len(p2) >= n2:
            new_p1 = deepcopy(p1[:n1])
            new_p2 = deepcopy(p2[:n2])
            new_game_count += 1
            if verbose: print("Playing a sub-game to determine the winner...\n")
            winner = recursive_combat([new_p1, new_p2], game=new_game_count, verbose=verbose)
            update_winner(winner, players, n1, n2)
        else:
            if n1 > n2:
                p1 += [n1, n2]
                if verbose: print(f"Player 1 wins round {count} of game {game}!")
            else:
                p2 += [n2, n1]
                if verbose: print(f"Player 2 wins round {count} of game {game}!")
        # update count
        count += 1
        # if count >= 100:
        #     return -1
        if not p1:
            if verbose: print(f"The winner of game {game} is player 2!")
            return 1
        elif not p2:
            if verbose: print(f"The winner of game {game} is player 1!")
            return 0
        if verbose: print()


if __name__ == '__main__':
    player1 = []
    player2 = []
    players = [player1, player2]
    ind = -1
    with open("input22.txt") as f:
        for line in f:
            if re.match(r'Player .*', line):
                ind += 1
                player = players[ind]
                continue
            else:
                try:
                    card = int(line.strip())
                    player.append(card)
                except ValueError:
                    continue

    P2 = deepcopy(players)
    count = 0

    print("\nPART 1")
    while players[0] and players[1]:
        single_round(players)
        count += 1

    print(count, players)
    res = 0
    for p in players:
        r = reversed(p)
        for pos, value in enumerate(r):
            res += (pos + 1) * value

    print(f"answer: {res}")

    print("\nPART 2")
    winner = recursive_combat(P2, verbose=False)
    res = 0
    for p in P2:
        r = reversed(p)
        for pos, value in enumerate(r):
            res += (pos + 1) * value
    print(f"answer: {res}")
