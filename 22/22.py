
from pathlib import Path
from collections import deque

def parse_input(data):
    players = []
    player = []
    for line in data:
        if line.startswith("Player"):
            if len(player) != 0:
                players.append(player)
                player = []
            continue
        player.append(int(line))
    players.append(player)
    return players

def play(p1, p2):
    while len(p1) > 0 and len(p2) > 0:
        c1 = p1.popleft()
        c2 = p2.popleft()
        if c1 > c2:
            p1.append(c1)
            p1.append(c2)
        else:
            p2.append(c2)
            p2.append(c1)
    return p1 if len(p1) != 0 else p2


text_data = Path("input22.txt").read_text().split("\n")

data = [line for line in text_data if line != ""]

players = parse_input(data)

player1 = deque(players[0])
player2 = deque(players[1])

winner = play(player1, player2)

res = sum(c*v for c, v in zip(winner, range(len(winner), 0, -1)))
print(res)


## Part 2
LOG = False
def log(msg):
    if LOG: print(msg)

def play(p1, p2, game=1):
    memory = set()
    rond = 0
    log(f"=== Game {game} ===")
    while len(p1) > 0 and len(p2) > 0:
        p1wins = None
        k = tuple(list(p1) + [None] + list(p2))
        if k in memory:
            return True
        memory.add(k)
        rond += 1
        log("")
        log(f"-- Round {rond} (Game {game}) --")
        s1 = ", ".join(map(str, p1))
        log("Player's 1 deck: {s1}")
        s2 = ", ".join(map(str, p2))
        log("Player's 2 deck: {s2}")
        c1, c2 = p1.popleft(), p2.popleft()
        n1, n2 = len(p1), len(p2)
        log(f"Player 1 plays: {c1}")
        log(f"Player 2 plays: {c2}")
        if c1 > n1 or c2 > n2:
            p1wins = c1 > c2
        else:
            q1 = deque(list(p1)[:c1])
            q2 = deque(list(p2)[:c2])
            log("Playing a sub-game to determine the winner...")
            p1wins = play(q1, q2, game+1)
            log("")
            log(f"...anyway, back to game {game}.")
        if p1wins:
            log(f"Player 1 wins round {rond} of game {game}!")
            p1.append(c1)
            p1.append(c2)
        else:
            log(f"Player 2 wins round {rond} of game {game}!")
            p2.append(c2)
            p2.append(c1)
        log("")
    return len(p1) > len(p2)
    
demo = True 
demo = False
if demo:
    player1 = deque([9, 2, 6, 3, 1])
    player2 = deque([5, 8, 4, 7, 10])
else:
    player1 = deque(players[0])
    player2 = deque(players[1])

winner = player1 if play(player1, player2) else player2

res = sum(c*v for c, v in zip(winner, range(len(winner), 0, -1)))
print(res)
