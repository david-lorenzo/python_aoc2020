def run(int n, xs):
    cdef int idx, i, v, c, c1, c2, c3, c4, d, d1
    cdef int lxs = len(xs)
    cdef int nxs[1_000_001]
    #cdef int lxs = 1_000_000
    #for idx in range(999_999):
    for idx in range(lxs-1):
        i = xs[idx]
        v = xs[idx+1]
        nxs[i] = v
    nxs[xs[-1]] = xs[0]
    nxs[0] = xs[0]

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
