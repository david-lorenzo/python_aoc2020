
from pathlib import Path

class Cell:
    def __init__(self):
        self.ne = None
        self.nw = None
        self.e = None
        self.w = None
        self.se = None
        self.sw = None
        self.value = True
    def move(self, direction, flip=False):
        # flipping the tile
        if flip:
            self.value = not self.value
        next_tile = None
        if direction == "e":
            next_tile = self.e
        elif direction == "w":
            next_tile = self.w
        elif direction == "nw":
            next_tile = self.nw
        elif direction == "ne":
            next_tile = self.ne
        elif direction == "sw":
            next_tile = self.sw
        elif direction == "se":
            next_tile = self.se
        else:
            raise Exception("bad move", direction)
        if next_tile is None:
            raise Exception("Board is too small")
        return next_tile

def create_board(n=11):
    board = [[Cell() for _ in range(n)] for _ in range(n)]
    for i, line in enumerate(board):
        for j, cell in enumerate(line):
            if j > 0:
                cell.w = line[j-1]
            if j < (n-1):
                cell.e = line[j+1]
            # north links
            if (i%2) == 1:
                if i > 0:
                    if j > 0:
                        cell.nw = board[i-1][j-1]
                    cell.ne = board[i-1][j]
            else:
                if i > 0:
                    cell.nw = board[i-1][j]
                    if j < (n-1):
                        cell.ne = board[i-1][j+1]
            # south links
            if (i%2) == 1:
                if i < (n-1):
                    if j > 0:
                        cell.sw = board[i+1][j-1]
                    cell.se = board[i+1][j]
            else:
                if i < (n-1):
                    cell.sw = board[i+1][j]
                    if j < (n-1):
                        cell.se = board[i+1][j+1]
    return board[n//2][n//2], board


def tiles_in_path(path):
    i = 0
    while i < len(path):
        if path[i] in ["e", "w"]:
            yield path[i]
            i += 1
        elif path[i] in ["s", "n"]:
            yield path[i:i+2]
            i += 2
        else:
            raise Exception("Bad path", path, i)


text_data = Path("input24.txt").read_text().split("\n")
#text_data = Path("input24demo.txt").read_text().split("\n")
data = [line for line in text_data if line != ""]

# True  -> White
# False -> Black
N = 201 
start, board = create_board(n=N)
start2, board2 = create_board(n=N)

for path in data:
    pos = start
    for to in tiles_in_path(path):
        pos = pos.move(to)
    pos.value = not pos.value

res = []
for path in data:
    pos = start
    for to in tiles_in_path(path):
        pos = pos.move(to)
    res.append(pos)

print("resultado")
#print([p.value for p in res])
print(len([p.value for p in res if not p.value]))

# int_board = [[" 1" if c.value else " 0" for c in line] for line in board]
# start_pos = len(int_board) // 2
# int_board[start_pos][start_pos] = " X" 
# for i, line in enumerate(int_board):
#     if i%2:
#         print(" " + "".join(line))
#     else:
#         print("".join(line))

## Part 2

def run(tile):
    links = [e for e in [tile.w, tile.e, tile.nw, tile.ne, tile.sw, tile.se] if e]
    blacks = len([e for e in links if not e.value])
    if tile.value:
        if blacks == 2:
            return False
        else:
            return True
    else:
        if blacks == 0 or blacks > 2:
            return True
        else:
            return False

curr_board = board
next_board = board2
for j in range(100):
    for curr_line, next_line in zip(curr_board, next_board):
        for curr_cell, next_cell in zip(curr_line, next_line):
            next_cell.value = run(curr_cell)
    curr_board, next_board = next_board, curr_board
    for i in range(len(curr_board)):
        if not curr_board[i][0].value:
            print(j)
            raise Exception("board is small")
        if not curr_board[i][-1].value:
            print(j)
            raise Exception("board is small")
    for cell in curr_board[0]:
        if not cell.value:
            print(j)
            raise Exception("board is small")
    for cell in curr_board[-1]:
        if not cell.value:
            print(j)
            raise Exception("board is small")

blacks = 0
for line in curr_board:
    for cell in line:
        if not cell.value:
            blacks += 1
print("Black cells:", blacks)
