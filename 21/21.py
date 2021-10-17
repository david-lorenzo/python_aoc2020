
from collections import defaultdict
from pathlib import Path


def parse_data(text_data):
    res = []
    for line in text_data:
        ingr, allergens = line.replace(")", "").split("(contains ")
        ingr = [i for i in ingr.split(" ") if i != ""]
        allergens = [a for a in allergens.split(", ") if a != ""]
        res.append( (ingr, allergens) )
    return res


text_data = Path("input21.txt").read_text().split("\n")
if text_data[-1] == "": del text_data[-1]

data = parse_data(text_data)

allergens = {}
all_ingrs = set()
for ingrs, allergs in data:
    set_ingrs = set(ingrs)
    all_ingrs |= set_ingrs
    for allerg in allergs:
        if allerg not in allergens:
            allergens[allerg] = set_ingrs.copy()
        allergens[allerg] &= set_ingrs

ingr_allerg = set()
for igrs in allergens.values():
    ingr_allerg |= igrs

ingrs_without_allerg = all_ingrs - ingr_allerg

n_times = 0
for igrs, _ in data:
    for igr in igrs:
        if igr in ingrs_without_allerg:
            n_times += 1
            
print(n_times)

## Part 2
from collections import defaultdict
ingr_allerg = defaultdict(set)
for allerg,ingrs in allergens.items():
    for ingr in ingrs:
        ingr_allerg[ingr].add(allerg)

res = {}
while len(ingr_allerg):
    for k, v in list(ingr_allerg.items()):
        if len(v) == 1:
            res[k] = v.pop()
    for k, v in res.items():
        if k in ingr_allerg:
            del ingr_allerg[k]
        for k1 in ingr_allerg.keys():
            ingr_allerg[k1].discard(v)

res_in_tuples = list(res.items())
# sorting by allergen
res_in_tuples.sort(key=lambda x: x[1])
print(",".join(ingr for ingr, _ in res_in_tuples))

