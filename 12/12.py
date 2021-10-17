from functools import reduce
from pathlib import Path

NORTH = ( 0,  1)
EAST  = ( 1,  0)
SOUTH = ( 0, -1)
WEST  = (-1,  0)

data = Path("input12.txt").read_text().split("\n")
del data[-1]

def parse_cmd(cmd):
    return cmd[0], int(cmd[1:])


def apply_cmd(state, cmd):
    position, speed = state
    (x, y), (vx, vy), (c, p) = position, speed, cmd
    if c in ["L", "R"]:
        return ((x, y), turn(speed, cmd))
    if c == "F":
        x, y = (x + p*vx), (y + p*vy)
    elif c == "E":
        x += p
    elif c == "W":
        x -= p
    elif c == "N":
        y += p
    elif c == "S":
        y -= p
    else:
        raise Exception(state, cmd)
    return ((x, y), speed)


def turn(v, cmd):
    # clockwise turns
    vs = [NORTH, EAST, SOUTH, WEST]
    c, p = cmd
    i = vs.index(v)
    sign = 1 if c == "R" else -1
    ni = (i + int(sign*(p/90))) % len(vs)
    return vs[ni]

turn(NORTH, ("R", 90))  == EAST
turn(NORTH, ("R", 180)) == SOUTH
turn(NORTH, ("R", 270)) == WEST
turn(NORTH, ("L", 90))  == WEST
turn(NORTH, ("L", 180)) == SOUTH
turn(NORTH, ("L", 270)) == EAST

turn(SOUTH, ("R", 90))  == WEST
turn(SOUTH, ("R", 180)) == NORTH
turn(SOUTH, ("R", 270)) == EAST
turn(SOUTH, ("L", 90))  == EAST
turn(SOUTH, ("L", 180)) == NORTH
turn(SOUTH, ("L", 270)) == WEST

turn(EAST, ("R", 90))  == SOUTH
turn(EAST, ("R", 180)) == WEST
turn(EAST, ("R", 270)) == NORTH
turn(EAST, ("L", 90))  == NORTH
turn(EAST, ("L", 180)) == WEST
turn(EAST, ("L", 270)) == SOUTH

turn(WEST, ("R", 90))  == NORTH
turn(WEST, ("R", 180)) == EAST
turn(WEST, ("R", 270)) == SOUTH
turn(WEST, ("L", 90))  == SOUTH
turn(WEST, ("L", 180)) == EAST
turn(WEST, ("L", 270)) == NORTH

start_position = (0, 0)
start_speed = EAST
seed = (start_position, start_speed)

res = reduce(apply_cmd,
        map(parse_cmd, data),
        seed)

(x, y), _ = res

print("resultado", res)
print("resultado:", abs(x) + abs(y))

