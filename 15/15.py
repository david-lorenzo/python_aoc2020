
def find_matches(xs, x):
    first = None
    second = None
    for i in range(len(xs)-1, -1, -1):
        if x == xs[i]:
            if not first:
                first = i + 1
                continue
            if not second:
                second = i + 1
                break
    return first, second

def run(data, n):
    for i in range(len(data), n):
        fst, snd = find_matches(data, data[-1])
        if not snd:
            last = 0
        else:
            last = fst - snd
        data.append(last)
#    print(data)
    return data[-1]

n = 2020
print([
436  == run([0,3,6], n),
1    == run([1,3,2], n),
10   == run([2,1,3], n),
27   == run([1,2,3], n),
78   == run([2,3,1], n),
438  == run([3,2,1], n),
1836 == run([3,1,2], n),
])

data = [15,12,0,14,3,1]
print("Result Part 1:", run(data, 2020))

## part 2

def run2(data, n):
    mem = {v: i for i, v in enumerate(data[:-1])}
    last = data[-1]
    for i in range(len(data), n):
        if last in mem:
            nxt = (i-1) - mem[last]
        else:
            nxt = 0
        mem[last] = i-1
        last = nxt
    return last

n = 30_000_000
data = [15,12,0,14,3,1]
print(run2(data, n))

print([
175594    == run2([0,3,6], n),
2578      == run2([1,3,2], n),
3544142   == run2([2,1,3], n),
261214    == run2([1,2,3], n),
6895259   == run2([2,3,1], n),
18        == run2([3,2,1], n),
362       == run2([3,1,2], n),
])
