from pathlib import Path
from collections import defaultdict

with Path("input7.txt").open() as f:
    data = f.readlines()


def parse_bag_rule(line):
    outer, _, inside = line.partition("contain")
    outer_color = " ".join(outer.strip().split(" ")[:-1])
    res = []
    for e in inside.split(","):
        n, *rest, _ = e.strip().split(" ")
        e_color = " ".join(rest)
        if n == "no":
            res.append((outer_color, 0, None))
        else:
            res.append((outer_color, int(n), e_color))
    return res


def build_graphs(rules):
    dag = defaultdict(dict)
    rdag = defaultdict(dict)
    for group in rules:
        for out, n, inside in group:
            dag[out][inside] = n
            rdag[inside][out] = n
    return dag, rdag

def traverse(dag, current):
    acc = 0
    for c, n in dag[current].items():
        if c:
            acc += n + n*traverse(dag, c)
    return acc

rules = [parse_bag_rule(line) for line in data]
dag, rdag = build_graphs(rules)
bags = traverse(dag, "shiny gold")
print(bags)
