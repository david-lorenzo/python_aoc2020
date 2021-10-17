from pathlib import Path

data = Path("input16.txt").read_text().split("\n")

rules = []
for line in data[:20]:
    criteria = line.split(":")[1]
    c1, c2 = criteria.split(" or ")
    a, b = [int(c) for c in c1.split("-")]
    c, d = [int(c) for c in c2.split("-")]
    rules.append([a, b, c, d])

tickets = []
scan = False
for line in data[20:]:
    if line == "": continue
    if line == "nearby tickets:":
        scan = True
        continue
    if scan:
        tickets.append([int(v) for v in line.split(",")])

your_ticket = [151,103,173,199,211,107,167,59,113,179,53,197,83,163,101,149,109,79,181,73]

def check_value(a, b, c, d, v):
    return (a <= v <= b) or (c <= v <= d)

def check_value2(r, v):
    a,b,c,d = r
    return check_value(a,b,c,d,v)
    
def maybe_right(v):
    return any(check_value(a,b,c,d,v) for a,b,c,d in rules)

def check_ticket(t):
    return all(maybe_right(v) for v in t)

ok_tickets = []
for t in tickets:
    if check_ticket(t):
        ok_tickets.append(t)

ok_tickets.append(your_ticket)

options = [list() for _ in range(20)]
for c in range(20):
    vs = [t[c] for t in ok_tickets]
    for j, r in enumerate(rules):
        if all([check_value2(r, v) for v in vs]):
            options[c].append(j)

MAP = [None for _ in range(20)]
while None in MAP:
    for i, o in enumerate(options):
        if MAP[i]: continue
        r = [x for x in o if x not in MAP]
        if len(r) == 1:
            MAP[i] = r[0]

res = 1
for i, x in enumerate(MAP):
    if x < 6:
        res *= your_ticket[i]

print(res)
