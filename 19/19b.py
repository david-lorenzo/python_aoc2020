
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
            return "(" + res + ")"
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

def build_regex(rule_defs, modify=False):
    cache = {}
    if modify:
        # "8: 42 | 42 8"
        # "11: 42 31 | 42 11 31"
        r42 = _get_from_cache(cache, rule_defs, 42)
        r8 = "(" + r42 + ")+"
        cache[8] = r8
        #print("r42", r42)
        #print("r8", r8)
        r31 = _get_from_cache(cache, rule_defs, 31)
        #r11 = "((" + r42 + r31 +")|((" + r42 + ")+" + r31 +"(" + r31 + ")?))"
        #r11 = "(" + r42 + r31 + "|" + r42 + "+" + r31 + r31 + ")"
        # can't do recursive, set a limit of 5
        # num(r42) must be equal to num(r31)
        r11 = "(" + r42 + r31
        for n in range(2, 5):
            r11 += ")|("
            for _ in range(n):
                r11 += r42
            for _ in range(n):
                r11 += r31
        cache[11] = "(" + r11 + "))"
    rule0 = _get_from_cache(cache, rule_defs, 0)
    return "^" + rule0 + "$"


text_data = """
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
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
#print(regex)
#print(len([msg for msg in messages if re.match(regex, msg)]))

regex = build_regex(rule_definitions, modify=True)
#print(regex)
print(len([msg for msg in messages if re.match(regex, msg)]))
exit(0)

for msg in messages:
    if re.match(regex, msg):
        print(msg)

