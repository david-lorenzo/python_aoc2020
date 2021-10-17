from numba import jit, int32

@jit(int32(int32,int32), nopython=True, cache=True)
def decr(n, x):
    if x == 1: return n
    return x-1

@jit(int32(int32,int32,int32,int32,int32), nopython=True, cache=True)
def find_dest(n, c, c1, c2, c3):
    a = decr(n, c)
    if a != c1 and a != c2 and a != c3: return a
    a = decr(n, a)
    if a != c1 and a != c2 and a != c3: return a
    a = decr(n, a)
    if a != c1 and a != c2 and a != c3: return a
    return decr(n, a)

@jit(cache=True)
def run(n, xs):
    lxs = len(xs)
    nxs = [None]*(lxs+1)
    for (i, v) in zip(xs, xs[1:]):
        nxs[i] = v
    nxs[xs[-1]] = xs[0]
    nxs[0] = xs[0]

    for _ in range(n):
        c  = nxs[0]
        c1 = nxs[c]
        c2 = nxs[c1]
        c3 = nxs[c2]
        c4 = nxs[c3]
        #d  = find_dest(lxs, c, c1, c2, c3)
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
    cups = [5, 9, 8, 1, 6, 2, 7, 3, 4]

    res1 = run(100, cups)
    print_sol(res1)

    in2 = list(range(1, 1_000_001))
    in2[0:9] = cups
    res2 = run(10_000_000, in2)
    m1 = res2[1]
    m2 = res2[m1]
    print(m1*m2)

main()
