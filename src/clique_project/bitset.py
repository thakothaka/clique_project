def max_clique_bitset(A):
    n = A.shape[0]

    # adjacency bitset for each node
    adj = [0] * n
    for i in range(n):
        bits = 0
        row = A[i]
        for j in range(n):
            if row[j] == 1:
                bits |= (1 << j)
        adj[i] = bits

    best = 0  # bitset

    def expand(R, P):
        nonlocal best

        # bound: even if we take all from P, can’t beat best
        if (R.bit_count() + P.bit_count()) <= best.bit_count():
            return

        if P == 0:
            if R.bit_count() > best.bit_count():
                best = R
            return

        # pivot: choose u in (P) that maximizes |P & N(u)|
        # iterate candidates by bits
        # pick pivot quickly
        u = (P & -P).bit_length() - 1
        max_deg = (P & adj[u]).bit_count()
        tmp = P
        while tmp:
            vbit = tmp & -tmp
            v = vbit.bit_length() - 1
            deg = (P & adj[v]).bit_count()
            if deg > max_deg:
                max_deg = deg
                u = v
            tmp -= vbit

        # branch on vertices in P \ N(u)
        candidates = P & ~adj[u]
        while candidates:
            vbit = candidates & -candidates
            v = vbit.bit_length() - 1

            expand(R | vbit, P & adj[v])

            P -= vbit
            candidates -= vbit

            # another bound after removing v
            if (R.bit_count() + P.bit_count()) <= best.bit_count():
                return

    all_nodes = (1 << n) - 1
    expand(0, all_nodes)

    # decode best bitset -> list of nodes
    clique = []
    b = best
    while b:
        vbit = b & -b
        v = vbit.bit_length() - 1
        clique.append(v)
        b -= vbit
    return clique
