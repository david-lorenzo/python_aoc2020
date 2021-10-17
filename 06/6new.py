from pathlib import Path
from collections import Counter

groups = Path("input6.txt").read_text().split("\n\n")

cs = [Counter(g.replace("\n", "")) for g in groups]
ls = [len(g.split("\n")) for g in groups]
b  = [len([x for x in c.values() if x == s]) for c, s in zip(cs, ls)]
print("Part 1:", sum([len(c) for c in cs]))
print("Part 2:", sum(b))
