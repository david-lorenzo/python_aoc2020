from pathlib import Path
import copy

def sumarize(tile):
    return "".join(tile)

def rotate_right(tile):
    s = len(tile)
    cols = len(tile[0])
    max_index = s - 1
    res = [[None for _ in range(s)] for _ in range(cols)]
    for (i, line) in enumerate(tile):
        for (j, e) in enumerate(tile[i]):
            res[j][max_index - i] = e
    return ["".join(r) for r in res]

def horizontal_flip(tile):
    s = len(tile)
    cols = len(tile[0])
    max_index = s - 1
    res = [[None for _ in range(cols)] for _ in range(s)]
    for i in range(s):
        for j in range(cols):
            res[max_index - i][j] = tile[i][j]
    return ["".join(r) for r in res]

def vertical_flip(tile):
    s = len(tile)
    cols = len(tile[0])
    max_index = s - 1
    res = [[None for _ in range(cols)] for _ in range(s)]
    for i in range(s):
        for j in range(cols):
            res[i][max_index - j] = tile[i][j]
    return ["".join(r) for r in res]

def all_positions(tile):
    itile = copy.deepcopy(tile)
    res = [itile]
    seen = set([sumarize(itile)])
    for _ in range(3):
        itile = rotate_right(itile)
        tile_sum = sumarize(itile)
        if tile_sum not in seen:
            res.append(itile)
            seen.add(tile_sum)
    for t in res[:4]:
        ht = horizontal_flip(t)
        tile_sum = sumarize(ht)
        if tile_sum not in seen:
            res.append(ht)
            seen.add(tile_sum)
    for t in res[:4]:
        vt = horizontal_flip(t)
        tile_sum = sumarize(vt)
        if tile_sum not in seen:
            res.append(vt)
            seen.add(tile_sum)
    return res

def match_monster(tile, i, j, monster):
    log = False
    if i == 2 and j == 2:
        log = True
    h, w = len(monster), len(monster[0])
    if log:
        print_tile(monster)
    for m in range(h):
        for n in range(w):
            t_c = tile[i+m][j+n]
            m_c = monster[m][n]
            if log:
                print(m, n)
                print("hola", t_c, ",", m_c, "fin")
            if m_c == "#" and t_c not in ("#", "O"):
                return False
    return True

def find_num_monsters(tile, monster):
    mh, mw = len(monster), len(monster[0])
    th, tw = len(tile), len(tile[0])
    n = 0
    for i in range(th - mh):
        for j in range(tw - mw):
            if match_monster(tile, i, j, monster):
                n += 1
    return n

def print_tile(tile):
    for e in tile:
        print(e)

monster = Path("monster20.txt").read_text().split("\n")
if monster[-1] == "": monster = monster[:-1]
all_monsters = all_positions(monster)

fused_map = Path("demo20.txt").read_text().split("\n")
if fused_map[-1] == "": fused_map = fused_map[:-1]

print_tile(monster)
res = find_num_monsters(fused_map, monster)
print(res)
