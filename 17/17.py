

# RULES:
# If a cube is active and exactly 2 or 3 of its neighbors are also
# active, the cube remains active. Otherwise, the cube becomes inactive.
#
# If a cube is inactive but exactly 3 of its neighbors are active,
# the cube becomes active. Otherwise, the cube remains inactive.

def neighbors(pos):
    x, y, z = pos
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            for k in [-1, 0, 1]:
                if i == j == k == 0: continue
                nx = x + i
                ny = y + j
                nz = z + k
                yield (nx, ny, nz)


def next_value(cube, pos):
    active_neighbors = sum([1 for p in neighbors(pos) if p in cube and cube[p] == "#"])
    x, y, z= pos
    if x == 1 and y == 2 and z == 0 :
        print(pos, active_neighbors)
        for p in neighbors(pos):
            if p in cube:
                print(p, cube[p])
    if pos in cube and cube[pos] == "#":
        return "#" if active_neighbors in [2, 3] else "."
    else:
        return "#" if active_neighbors == 3 else "."


def indexes(cube, expand=True):
    xs = set(x for x, _, _ in cube.keys())
    ys = set(y for _, y, _ in cube.keys())
    zs = set(z for _, _, z in cube.keys())
    if expand:
        xs.add(max(xs)+1)
        xs.add(min(xs)-1)
        ys.add(max(ys)+1)
        ys.add(min(ys)-1)
        zs.add(max(zs)+1)
        zs.add(min(zs)-1)
    return sorted(list(xs)), sorted(list(ys)), sorted(list(zs))

def run(cube):
    new_cube = {}
    ix, iy, iz = indexes(cube)
    for x in ix:
        for y in iy:
            for z in iz:
                pos = x, y, z
                new_cube[pos] = next_value(cube, pos)
    return new_cube

def print_cube(cube):
    xs, ys, zs = indexes(cube, expand=False)
    for z in zs:
        print(f"\nz = {z}")
        for x in xs:
            for y in ys:
                print(f"{cube[(x,y,z)]}", end="")
            print("")


data = """#.#..###
.#....##
.###...#
..####..
....###.
##.#.#.#
..#..##.
#.....##""".split("\n")

data = """.#.
..#
###""".split("\n")

cells = [list(d) for d in data]

cube = {}
for y in range(len(cells)):
    for x in range(len(cells[0])):
        cube[(x, y, 0)] = cells[x][y]

print("First run")
nc = run(cube)
print_cube(nc)
# 
# print("Second run")
# nc2 = run(nc)
# print_cube(nc2)
# 
# print("Third run")
# nc3 = run(nc2)
# print_cube(nc3)
exit(0)

cube_now = cube.copy()
for _ in range(6):
    cube_now = run(cube_now)

active_cells = sum([1 for cell in cube_now.values() if cell == "#"])
print(active_cells)
