
from pathlib import Path
from collections import defaultdict
import copy

def parse_input(data):
    tiles = {}
    tile_id = None
    tile = []
    for line in data:
        if line == "": continue
        if line.startswith("Tile "):
            if tile_id:
                tiles[tile_id] = tile
                tile = []
            tile_id = int(line.split(" ")[1][:-1])
        else:
            tile.append(line)
    tiles[tile_id] = tile
    return tiles

def top_edge(tile):
    return copy.deepcopy(tile[0])

def bottom_edge(tile):
    return copy.deepcopy(tile[-1])

def left_edge(tile):
    return "".join(l[0] for l in tile)

def right_edge(tile):
    return "".join(l[-1] for l in tile)

def tile_edges(tile):
    top    = top_edge(tile)
    bottom = bottom_edge(tile)
    left   = left_edge(tile)
    right  = right_edge(tile)
    rtop    = "".join(reversed(top))
    rbottom = "".join(reversed(bottom))
    rleft   = "".join(reversed(left))
    rright  = "".join(reversed(right))
    return [top, bottom, left, right,
            rtop, rbottom, rleft, rright]

def print_tile(tile):
    for e in tile:
        print(e)

def print_grid(grid):
    for e in grid:
        print(e)

def map_edges(tiles):
    """creates a map where the key is the edge string and the value
    is the tile id of that edge, it doesn't care which edge it is.
    We assume all the edges are unique"""
    m_edges = defaultdict(list)
    for tile_id, tile in tiles.items():
        for edge in tile_edges(tile):
            m_edges[edge].append(tile_id)
    return m_edges

def find_adjacents(edges):
    """it iterates over the edges values discarding those lists that have only
    one tile. When we have 2 tiles we assume they are connected.

    Again, this works because the edges are unique."""
    adjs = defaultdict(set)
    for e in edges.values():
        if len(e) == 1: continue
        a, b = e
        adjs[a].add(b)
        adjs[b].add(a)
    return adjs


text_data = Path("input20.txt").read_text().split("\n")
#text_data = Path("input20demo.txt").read_text().split("\n")
tiles = parse_input(text_data)

#primero = list(tiles.values())[0]
#print_tile(primero)

#edges_primero = tile_edges(primero)
#print_tile(edges_primero)

medges = map_edges(tiles)
adjl = find_adjacents(medges)
corners = {k:v for k,v in adjl.items() if len(v) == 2}
res = 1
for k in corners.keys():
    res *= k
print(res)

## Part 2
import networkx as nx
from networkx.algorithms.shortest_paths.generic import shortest_path

g = nx.Graph()
g.add_edges_from(( (k,m) for k, adj in adjl.items() for m in adj ))

# locating the corners and filling top and left edges
four_corners = list(corners.keys())
top_left = four_corners[0]
# grid [[int]]
grid = [[None for _ in range(12)] for _ in range(12)]
for o in four_corners[1:]:
    path = shortest_path(g, top_left, o)
    if len(path) == 12:
        if not grid[0][-1]:
            grid[0] = path
        else:
            for (i, e) in enumerate(path):
                grid[i][0] = e
    else:
        grid[-1][-1] = o

# filling right edge
path = shortest_path(g, grid[0][-1], grid[-1][-1])
for (i, e) in enumerate(path):
    grid[i][-1] = e
#print_grid(grid)

# filling the rest of the rows
for i in range(len(grid)):
    left, right = grid[i][0], grid[i][-1]
    grid[i] = shortest_path(g, left, right)
#print_grid(grid)

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

def sumarize(tile):
    """helper function joining all the lines in a string because
    it is a hashable object that can be used in a set"""
    return "".join(tile)

def all_positions(tile):
    """the tile + 3 rotations + all the vertical and horizontal flips
    on the 4 positions, eliminating duplicates"""
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

def do_match1(a_edge, b_tiles, pb):
    res = []
    for b in b_tiles:
        if a_edge == pb(b):
            res.append( b )
    return res

def do_match2(a_tiles, b_tiles, pa, pb):
    res = []
    for a in a_tiles:
        a_edge = pa(a)
        for b in do_match1(a_edge, b_tiles, pb):
            res.append( (a, b) )
    return res

def cut_tile(tile):
    """this function removes the outer most edges: top, left, bottom, right

    final height is h - 2, final width is w - 2
    """
    return [e[1:-1] for e in tile[1:-1]]

# placing top left corner and the one to its right
ai = grid[0][0]
bi = grid[0][1]
a = tiles[ai]
b = tiles[bi]
a_tiles = all_positions(a)
b_tiles = all_positions(b)
res = do_match2(a_tiles, b_tiles, right_edge, left_edge)[0]
the_map = {}
the_map[ai] = res[0]
the_map[bi] = res[1]

# placing the first row
for i in range(2, len(grid[0])):
    pi = grid[0][i-1]
    ii = grid[0][i]
    re = right_edge(the_map[pi])
    ii_tiles = all_positions(tiles[ii])
    iis = do_match1(re, ii_tiles, left_edge)
    assert(len(iis) == 1)
    the_map[ii] = iis[0]

# placing the rest of the board, from top to bottom
for i in range(1, len(grid)):
    for j in range(0, len(grid[i])):
        pi = grid[i-1][j]
        ii = grid[i][j]
        be = bottom_edge(the_map[pi])
        ii_tiles = all_positions(tiles[ii])
        iis = do_match1(be, ii_tiles, top_edge)
        assert(len(iis) == 1)
        the_map[ii] = iis[0]

# cutting the tiles
total_map_tiled = [[None for _ in range(12)] for _ in range(12)]
for i in range(12):
    for j in range(12):
        tid = grid[i][j]
        tile = the_map[tid]
        total_map_tiled[i][j] = cut_tile(tile)

def fuse_row(tiled_row):
    """this function fuse a list of tiles"""
    res = []
    for i in range(len(tiled_row[0])):
        res.append("".join(e[i] for e in tiled_row))
    return res

def fuse_tiles(tiled_map):
    """this function fuse a list of list of tiles, where each element is a row of tiles"""
    res = []
    for i in range(len(tiled_map)):
        res.extend(fuse_row(tiled_map[i]))
    return res

total_map_fused = fuse_tiles(total_map_tiled)
#print_tile(total_map_fused)

monster = Path("monster20.txt").read_text().split("\n")
if monster[-1] == "": monster = monster[:-1]
all_monsters = all_positions(monster)
# for e in all_monsters:
#     print("--")
#     print_tile(e)

def match_monster(tile, i, j, monster):
    """scanning the moster at a (i, j) position in the map"""
    for m in range(len(monster)):
        for n in range(len(monster[0])):
            tc = tile[i+m][j+n]
            mc = monster[m][n]
            if mc == "#" and tc not in ("#", "O"):
                return False
    return True


def find_num_monsters(tile, monster):
    """scanning monsters over the full map, like a mask"""
    n = 0
    mh, mw = len(monster), len(monster[0])
    th, tw = len(tile), len(tile[0])
    for i in range(th - mh):
        for j in range(tw - mw):
            if match_monster(tile, i, j, monster):
                n += 1
    return n

def count_sharps(tile):
    return len( [e for line in tile for e in line if e == "#"] )

total_sharps = count_sharps(total_map_fused)
monster_sharps = count_sharps(monster)
print("Map sharps:", total_sharps)
print("Monster sharps:", monster_sharps)
res = []
for monstr in all_monsters:
    res.append(find_num_monsters(total_map_fused, monstr))

res = [e for e in res if e != 0]
assert(len(res) == 1)
res = res[0]
print("Number of monsters (should be 15): ", res)
print("Final_result: ", total_sharps - res * monster_sharps)

