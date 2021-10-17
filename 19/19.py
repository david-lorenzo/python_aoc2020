
from pathlib import Path
import re

def parse_subrule(exp):
    sexp = exp.strip()
    if '"a"' == sexp:
        return "a" 
    elif '"b"' == sexp:
        return "b"
    else:
        return [int(n) for n in sexp.split(" ")]

def parse_rule(rule):
    rid, definition = rule.split(":")
    if "|" in definition:
        left, right = definition.split("|")
        left = parse_subrule(left)
        right = parse_subrule(right)
        res = int(rid), [left, right]
    else:
        res = int(rid), [parse_subrule(definition)]
    return res

def _get_from_cache(cache, defs, rid):
    if rid not in cache:
        cache[rid] = _build_regex(cache, defs, rid)
    return cache[rid]

def _build_regex(cache, defs, rid):
    rdef = defs[rid]
    if len(rdef) == 1:
        rdef = rdef[0]
        if type(rdef) == type([]):
            res = ""
            for n in rdef:
                res += _get_from_cache(cache, defs, n)
            return res
        elif type(rdef) == type(""):
            return rdef
        else:
            raise Exception("bad rules")
    else:
        rdef1, rdef2 = rdef
        res1 = ""
        for n in rdef1:
            res1 += _get_from_cache(cache, defs, n)
        res2 = ""
        for n in rdef2:
            res2 += _get_from_cache(cache, defs, n)
        return "(" + res1 + "|" + res2 + ")"

def build_regex(rule_defs):
    rule0 = _get_from_cache({}, rule_defs, 0)
    return "^" + rule0 + "$"


text_data = """
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
""".split("\n")

text_data = Path("input19.txt").read_text().split("\n")

data = [line for line in text_data if line != ""]

rule_definitions = {} 
messages = []
for line in data:
    if ":" in line:
        rid, definition = parse_rule(line)
        rule_definitions[rid] = definition
    elif line == "":
        continue
    else:
        messages.append(line)

regex = build_regex(rule_definitions)

print(len([msg for msg in messages if re.match(regex, msg)]))
