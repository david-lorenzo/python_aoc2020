import copy
from pathlib import Path

EMPTY = "L"
BUSY  = "#"
FLOOR = "."

def busy_neighbors(state, row, col):
    total_busy = 0
    for i in [-1, 0, 1]:
        nrow = row + i
        if nrow < 0 or nrow >= len(state):
            continue
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            ncol = col + j
            if ncol < 0 or ncol >= len(state[0]):
                continue
            if state[nrow][ncol] == BUSY:
                total_busy += 1
    return total_busy

def next_status(curr_state, busy_neighbors):
    if curr_state == EMPTY and busy_neighbors == 0:
        return BUSY
    elif curr_state == BUSY and busy_neighbors >= 4:
        return EMPTY
    else:
        return curr_state


def run_iteration(current_state, next_state):
    rows, cols = len(current_state), len(current_state[0])
    for x in range(rows):
        for y in range(cols):
            place_status = current_state[x][y]
            if place_status == FLOOR:
                continue
            bn = busy_neighbors(current_state, x, y)
            next_state[x][y] = next_status(place_status, bn)
    return (next_state, current_state)


data = Path("input11.txt").read_text().split("\n")
# data = Path("input11test.txt").read_text().split("\n")
del data[-1]

current_state = [ [c for c in line] for line in data ]
next_state = copy.deepcopy(current_state)

run_first = True
counter = 0
while current_state != next_state or run_first:
    counter += 1
    run_first = False
    current_state, next_state = run_iteration(current_state, next_state)

total_busy = sum([1 for row in current_state for cell in row if cell == BUSY])
print(total_busy)

### PART 2 ###

def next_status_part2(curr_state, busy_neighbors):
    if curr_state == EMPTY and busy_neighbors == 0:
        return BUSY
    elif curr_state == BUSY and busy_neighbors >= 5:
        return EMPTY
    else:
        return curr_state


def find_first(state, x, y, vx, vy):
    nx, ny = x, y
    while True:
        nx, ny = nx + vx, ny + vy
        if nx < 0 or nx >= len(state) \
                or ny < 0 or ny >= len(state[0]):
            return FLOOR
        if state[nx][ny] != FLOOR:
            return state[nx][ny]

def busy_neighbors_part2(state, x, y):
    vs = [
            (-1, -1), # Top Left
            (-1,  0), # Top
            (-1,  1), # Top Right
            ( 0, -1), # Left
            ( 0,  1), # Right
            ( 1, -1), # Bottom Left
            ( 1,  0), # Bottom
            ( 1,  1), # Bottom Right
         ]
    seats = [find_first(state, x, y, v[0], v[1]) for v in vs]
    return sum([1 for c in seats if c == BUSY])


def run_iteration_part2(current_state, next_state):
    rows, cols = len(current_state), len(current_state[0])
    for x in range(rows):
        for y in range(cols):
            place_status = current_state[x][y]
            if place_status == FLOOR:
                continue
            bn = busy_neighbors_part2(current_state, x, y)
            next_state[x][y] = next_status_part2(place_status, bn)
    return (next_state, current_state)

current_state = [ [c for c in line] for line in data ]
next_state = copy.deepcopy(current_state)

run_first = True
counter = 0
while current_state != next_state or run_first:
    counter += 1
    run_first = False
    current_state, next_state = run_iteration_part2(current_state, next_state)
print(counter)

current_state, next_state = run_iteration_part2(current_state, next_state)
total_busy = sum([1 for row in current_state for cell in row if cell == BUSY])
print(total_busy)
