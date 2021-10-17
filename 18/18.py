

OPS = ['+', '*']
PARENS = ['(', ')']
NOT_A_NUMBER = OPS + PARENS

def transform(term):
    if term in NOT_A_NUMBER:
        return term
    else:
        return int(term)

def tokenizer(e):
    return [ transform(c) for c in list(e) if c != " " ]

def to_rpn(exp, start=0):
    res = []
    i = start 
    while i < len(exp):
        term = exp[i]
        if term == ")":
            return res, i+1
        elif term == "(":
            right, i = to_rpn(exp, i+1)
            res.extend(right)
        elif term in OPS:
            if exp[i+1] == "(":
                right, i = to_rpn(exp, i+2)
                res.extend(right)
            else:
                res.append(exp[i+1])
                i += 2
            res.append(term)
        else:
            res.append(term)
            i += 1
    return res

def operate(op_left, op, op_right):
    if op == "+":
        return op_left + op_right
    elif op == "*":
        return op_left * op_right
    else:
        raise Exception("bad operation", op_left, op, op_right)

def rpn_evaluator(rpn_exp):
    stack = []
    for e in rpn_exp: 
        if e in OPS:
            op2 = stack.pop()
            op1 = stack.pop()
            res = operate(op1, e, op2)
            stack.append(res)
        else:
            stack.append(e)
    if len(stack) != 1:
        raise Exception("bad expresion", stack)
    return stack[0]

def evaluate(exp):
    rpne = to_rpn(exp)
    return rpn_evaluator(rpne)


data = """2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2""".split("\n")


from pathlib import Path
raw_text = Path("input18.txt").read_text().split("\n")
data = [line for line in raw_text if line != ""]

expressions = [tokenizer(e) for e in data]

results = [(e, evaluate(e)) for e in expressions]

print(sum((r[1] for r in results)))
