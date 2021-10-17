
from pathlib import Path
from collections import defaultdict

UL = {"TOP", "LEFT"}
UR = {"TOP", "RIGHT"}
DL = {"BOTTOM", "LEFT"}
DR = {"BOTTOM", "RIGHT"}

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

def tile_edges(tile):
    top    = tile[0]
    bottom = tile[-1]
    left   = "".join([l[0] for l in tile])
    right  = "".join([l[-1] for l in tile])
    rtop    = "".join(reversed(top))
    rbottom = "".join(reversed(bottom))
    rleft   = "".join(reversed(left))
    rright  = "".join(reversed(right))
    return [top, bottom, left, right,
            rtop, rbottom, rleft, rright]

def print_tile(tile):
    for e in tile:
        print(e)

def map_edges(tiles):
    m_edges = defaultdict(list)
    for tile_id, tile in tiles.items():
        for edge in tile_edges(tile):
            m_edges[edge].append(tile_id)
    return m_edges

def find_adjacents(edges):
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

primero = list(tiles.values())[0]
print_tile(primero)

edges_primero = tile_edges(primero)
print_tile(edges_primero)

medges = map_edges(tiles)

adjl = find_adjacents(medges)

corners = {k:v for k,v in adjl.items() if len(v) == 2}

res = 1
for k in corners.keys():
    res *= k

print(res)

