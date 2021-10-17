import numpy as np
#import cProfile

def initialize(xs):
    lxs = len(xs)
    nxs = np.empty(lxs+1, dtype="int32")
    for (i, v) in zip(xs, xs[1:]):
        nxs[i] = v
    lasti = xs[-1]
    nxs[lasti] = xs[0]
    nxs[0] = xs[0]
    return nxs

def run(n, nxs):
    lxs = len(nxs)-1
    for _ in range(n):
        c  = nxs[0]
        c1 = nxs[c]
        c2 = nxs[c1]
        c3 = nxs[c2]
        c4 = nxs[c3]
        d = lxs if c == 1 else c-1
        if d == c1 or d == c2 or d == c3:
            d = lxs if d == 1 else d-1
            if d == c1 or d == c2 or d == c3:
                d = lxs if d == 1 else d-1
                if d == c1 or d == c2 or d == c3:
                    d = lxs if d == 1 else d-1
        d1 = nxs[d] 
        nxs[c3] = d1
        nxs[d] = c1
        nxs[c] = c4
        nxs[0] = c4
    return nxs

def print_sol(xs):
    n = xs[1]
    while n != 1:
        print(n, end="")
        n = xs[n]
    print("")

def main():
    data = [5, 9, 8, 1, 6, 2, 7, 3, 4]
    cups = initialize(data)

    res1 = run(100, cups)
    print_sol(res1)

    ind2 = list(range(1, 1_000_001))
    ind2[0:9] = data
    ina2 = initialize(ind2)
    res2 = run(10_000_000, ina2)
    m1 = res2[1]
    m2 = res2[m1]
    print(m1*m2)

main()
#cProfile.run("main()")
