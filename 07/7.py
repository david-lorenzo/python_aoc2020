from pathlib import Path

with Path("input7.txt").open() as f:
    data = f.readlines()


def parse_bag_rule(line):
    outer, _, inside = line.partition("contain")
    outer_color = " ".join(outer.strip().split(" ")[:-1])
    res = []
    for e in inside.split(","):
        e_color = " ".join(e.strip().split(" ")[1:-1])
        res.append((outer_color, e_color))
    return res


rules = [parse_bag_rule(line) for line in data]
from collections import defaultdict
all_rules = defaultdict(set)
for group in rules:
    for out, inside in group:
        all_rules[inside].add(out)

all_colors = set([])

new_colors = set(["shiny gold"])
possible_colors = set([])
while new_colors:
    new_batch = set([])
    for nc in new_colors:
        new_batch.update(all_rules[nc])
    new_colors = new_batch - possible_colors
    possible_colors.update(new_batch)

print(len(possible_colors))

