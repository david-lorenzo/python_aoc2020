from pathlib import Path
from itertools import count

data = Path("input13.txt").read_text().split("\n")
eta = int(data[0])
buses = list(map(int, filter(lambda x: x != "x", data[1].split(","))))

delays = list(map(lambda x: x*(eta // x + 1) - eta, buses))
p1 = min(delays)
i = delays.index(p1)
p2 = buses[i]

print(p1, p2, p1 * p2)

## part 2

bus_data = data[1].split(",")
buses2 = list(map(lambda x: (int(x[0]), x[1]),
            filter(lambda x: x[0] != "x",
                zip(bus_data, count()))))

def modulo(pair):
    n, a = pair
    return (n, -a % n)

buses20 = map(modulo, buses2)

buses21 = sorted(buses20, reverse=True)

N = 1
for x, _ in buses2:
    N *= x

n0, a0 = buses21[0]
n1, a1 = buses21[1]
n2, a2 = buses21[2]
n3, a3 = buses21[3]
n4, a4 = buses21[4]
n5, a5 = buses21[5]
n6, a6 = buses21[6]
n7, a7 = buses21[7]
n8, a8 = buses21[8]

s0 = n0
for x0 in count(a0, s0):
    if x0 % n1 == a1:
        break

s1 = s0*n1
for x1 in count(x0 + s1, s1):
    if x1 % n2 == a2:
        break

s2 = s1*n2
for x2 in count(x1 + s2, s2):
    if x2 % n3 == a3:
        break

s3 = s2*n3
for x3 in count(x2 + s3, s3):
    if x3 % n4 == a4:
        break

s4 = s3*n4
for x4 in count(x3 + s4, s4):
    if x4 % n5 == a5:
        break

s5 = s4*n5
for x5 in count(x4 + s5, s5):
    if x5 % n6 == a6:
        break

s6 = s5*n6
for x6 in count(x5 + s6, s6):
    if x6 % n7 == a7:
        break

s7 = s6*n7
for x7 in count(x6 + s7, s7):
    if x7 % n8 == a8:
        break

print(x7)
