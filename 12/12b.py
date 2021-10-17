from functools import reduce
from pathlib import Path

data = Path("input12.txt").read_text().split("\n")
del data[-1]

def parse_cmd(cmd):
    return cmd[0], int(cmd[1:])

def apply_cmd(state, cmd):
    vessel   = state["vessel"]
    waypoint = state["waypoint"]
    (x, y), (wx, wy), (c, p) = vessel, waypoint, cmd
    if c == "N":
        wy += p
    elif c == "S":
        wy -= p
    elif c == "E":
        wx += p
    elif c == "W":
        wx -= p
    elif c == "F":
        x, y = move_vessel(vessel, waypoint, p)
    elif c in ["R", "L"]:
        wx, wy = rotate_waypoint(vessel, waypoint, cmd)
    else:
        raise Exception(waypoint, vessel, cmd)
    return { "vessel": (x, y), "waypoint": (wx, wy) }


def move_vessel(vessel, waypoint, p):
    (x, y), (wx, wy) = vessel, waypoint
    return (x + wx*p), (y + wy*p)


def rotate_waypoint(vessel, waypoint, cmd):
    (x, y), (wx, wy), (c, p) = vessel, waypoint, cmd
    sign = -1 if c == "R" else 1
    theta = sign * p
    sin = { 90: 1, 180: 0, 270: -1, -90: -1, -180: 0, -270: 1, }[theta]
    cos = { 90: 0, 180: -1, 270: 0, -90: 0, -180: -1, -270: 0, }[theta]
    return (wx*cos - wy*sin), (wx*sin + wy*cos)


def manhattan_dist(end, start):
    (sx, sy), (ex, ey) = start, end
    return abs(ex - sx) + abs(ey - sy)


waypoint_start_pos = (10, 1)
vessel_start_pos = (0, 0)
seed = {
    "waypoint": waypoint_start_pos,
    "vessel": vessel_start_pos,
}

res = reduce(apply_cmd, map(parse_cmd, data), seed)
md = manhattan_dist(vessel_start_pos, res["vessel"])
print("resultado", res)
print("resultado:", md)

