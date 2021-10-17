from pathlib import Path
from collections import Counter

data = Path("input10.txt").read_text().split("\n")
nums = list(map(int, data[:-1]))

mx = max(nums) + 3
onums = sorted(nums + [0, mx])
onums1 = onums[:-1]
onums2 = onums[1:]

def sub(pair):
    x, y = pair
    return x - y

counter = Counter(map(sub, zip(onums2, onums1)))

ones = counter[1]
threes = counter[3]

res = ones * threes

# don't use, not optimal
def choices(adaptors):
    index = set(adaptors)
    target = adaptors[-1]
    def _choices(acc):
        start = acc[-1]
        for i in [1, 2, 3]:
            next_adaptor = start + i
            if next_adaptor not in index:
                continue
            if next_adaptor == target:
                acc.append(next_adaptor)
                yield acc
            elif next_adaptor < target:
                next_acc = acc[:]
                next_acc.append(next_adaptor)
                yield from _choices(next_acc)
    yield from _choices([adaptors[0]])


# don't use, not optimal
def choices2(adaptors):
    index = set(adaptors)
    target = adaptors[-1]
    def _choices(n):
        for i in [1, 2, 3]:
            m = n + i
            if m not in index:
                continue
            if m == target:
                yield 1
            elif m < target:
                yield from _choices(m)
    yield from _choices(adaptors[0])

def choices3(data):
    mem = {}
    def _run(p):
        if p in mem: return mem[p]
        total = 0
        for i in [p+1, p+2, p+3]:
            if i == len(data):
                return 1
            vp = data[p]
            vi = data[i]
            vd = vi - vp
            if vd in [1, 2, 3]:
                total += _run(i)
        mem[p] = total
        return total
    return _run(0)

print(choices3(onums))
