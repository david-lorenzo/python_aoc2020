

PROD = "*"
SUM = "+"
LPAREN = "("
RPAREN = ")"
OPS = [SUM, PROD]
PARENS = [LPAREN, RPAREN]
SYMBOLS = OPS + PARENS

def transform(term):
    if term in SYMBOLS:
        return term
    else:
        return int(term)

def tokenizer(e):
    return [ transform(c) for c in list(e) if c != " " ]

def evaluate(ex, start=0):
    stack = []
    i = start
    while i < len(ex):
        e = ex[i]
        if e not in SYMBOLS:
            stack.append(e)
            i += 1
        elif e == PROD:
            stack.append(e)
            i += 1
        elif e == SUM:
            op1 = stack.pop()
            other = ex[i+1]
            if other not in SYMBOLS:
                op2 = other
                i += 2
            elif other == LPAREN:
                op2, i = evaluate(ex, i+2)
            else:
                raise Exception("bad expression")
            res = op1 + op2
            stack.append(res)
        elif e == LPAREN:
            res, i = evaluate(ex, i+1)
            stack.append(res)
        elif e == RPAREN:
            i += 1
            break
        else:
            raise Exception("bad token", e)
    res = 1
    for e in stack:
        if e not in SYMBOLS:
            res *= e
        elif e in PARENS or e == SUM:
            raise Exception("bad expression")
    return res, i
            
# data = """1 + (2 * 3) + (4 * (5 + 6))
# 2 * 3 + (4 * 5)
# 5 + (8 * 3 + 9 + 3 * 4 * 3)
# 5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
# ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2""".split("\n")
# expressions = [tokenizer(e) for e in data]
# expected = [51, 46, 1445, 669060, 23340]
# print(expected == [evaluate(e)[0] for e in expressions])
# exit(0)

# expression = tokenizer("8 * 3 + 9 + 3 * 4 * 3")
# print(expression, evaluate(expression))

from pathlib import Path
raw_text = Path("input18.txt").read_text().split("\n")
data = [line for line in raw_text if line != ""]
expressions = [tokenizer(e) for e in data]
results = [(e, evaluate(e)) for e in expressions]
print(sum((r[1][0] for r in results)))


