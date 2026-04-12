#!/usr/bin/env python3
"""
Test case generator for "Museum Guard Shift".

Usage:
    python3 gen.py <type> [seed]

Types:
    chain   N K S  -- chain tree of length N, K alarms, start at S
    star    N K     -- star tree (hub=1), K alarms on leaves
    binary  depth K -- complete binary tree of given depth, K alarms
    random  N K     -- random Prufer-sequence tree, K alarms

Examples:
    python3 gen.py chain 10000 18 1
    python3 gen.py star 200000 18
    python3 gen.py binary 17 18
    python3 gen.py random 5000 18 42

The generator writes a valid test case to stdout, then runs the accepted
solution (cppsol2.cpp compiled to /tmp/sol_gen) to produce an .ans file.
Both are written as <name>.in / <name>.ans to the current working directory
when the --write flag is given (otherwise just prints to stdout).

Design
------
For feasible test cases:
  - Pick a random visiting order of the K alarms.
  - Compute travel + handling times along that order.
  - Set deadlines slightly above those finish times (with a configurable
    slack parameter).

For impossible/tight test cases:
  - Use slack=0 to make exactly one deadline impossible by subtracting 1.
"""

import random

# ---------------------------------------------------------------------------
# Tree generators -- each returns (n, edge_list)
# where edge_list is a list of (u, v, w) 1-indexed
# ---------------------------------------------------------------------------

def gen_chain(n, w_lo=1, w_hi=10**9, rng=None):
    rng = rng or random
    edges = []
    for i in range(1, n):
        w = rng.randint(w_lo, w_hi)
        edges.append((i, i + 1, w))
    return n, edges


def gen_star(n, w_lo=1, w_hi=10**9, rng=None):
    rng = rng or random
    edges = []
    for i in range(2, n + 1):
        w = rng.randint(w_lo, w_hi)
        edges.append((1, i, w))
    return n, edges


def gen_binary(depth, w_lo=1, w_hi=10**9, rng=None):
    rng = rng or random
    n = (1 << (depth + 1)) - 1
    edges = []
    for v in range(1, n + 1):
        left = 2 * v
        right = 2 * v + 1
        if left <= n:
            edges.append((v, left, rng.randint(w_lo, w_hi)))
        if right <= n:
            edges.append((v, right, rng.randint(w_lo, w_hi)))
    return n, edges


def gen_random(n, w_lo=1, w_hi=10**9, rng=None):
    """Random tree via Prufer sequence."""
    rng = rng or random
    if n == 1:
        return 1, []
    prufer = [rng.randint(1, n) for _ in range(n - 2)]
    degree = [1] * (n + 1)
    for v in prufer:
        degree[v] += 1
    edges = []
    leaf_heap = sorted(v for v in range(1, n + 1) if degree[v] == 1)
    import heapq
    heapq.heapify(leaf_heap)
    for u in prufer:
        v = heapq.heappop(leaf_heap)
        edges.append((v, u, rng.randint(w_lo, w_hi)))
        degree[u] -= 1
        if degree[u] == 1:
            heapq.heappush(leaf_heap, u)
    u = heapq.heappop(leaf_heap)
    v = heapq.heappop(leaf_heap)
    edges.append((u, v, rng.randint(w_lo, w_hi)))
    return n, edges


# ---------------------------------------------------------------------------
# Distance computation (BFS on the generated tree)
# ---------------------------------------------------------------------------

def build_adj(n, edges):
    adj = [[] for _ in range(n + 1)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj


def bfs_dist(adj, src, n):
    dist = [-1] * (n + 1)
    dist[src] = 0
    q = [src]
    head = 0
    while head < len(q):
        u = q[head]; head += 1
        for v, w in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + w
                q.append(v)
    return dist


# ---------------------------------------------------------------------------
# Main generator
# ---------------------------------------------------------------------------

def generate(tree_type, n, k, s, seed, slack=5, tight_fraction=0.3):
    rng = random.Random(seed)

    if tree_type == "chain":
        n, edges = gen_chain(n, rng=rng)
    elif tree_type == "star":
        n, edges = gen_star(n, rng=rng)
    elif tree_type == "binary":
        # n is actually depth here
        n, edges = gen_binary(n, rng=rng)
    elif tree_type == "random":
        n, edges = gen_random(n, rng=rng)
    else:
        raise ValueError(f"Unknown tree type: {tree_type}")

    adj = build_adj(n, edges)

    # Pick K distinct alarm rooms (not necessarily distinct from s)
    if k > n:
        k = n
    alarm_rooms = rng.sample(range(1, n + 1), k)

    # Compute distances
    dist_s = bfs_dist(adj, s, n)
    dist_alarm = [bfs_dist(adj, r, n) for r in alarm_rooms]

    # Build a feasible schedule: random visiting order
    order = list(range(k))
    rng.shuffle(order)

    finish_times = []
    t = 0
    for idx in order:
        r = alarm_rooms[idx]
        step = len(finish_times)
        if step == 0:
            t += dist_s[r]
        else:
            prev_alarm_idx = order[step - 1]
            t += dist_alarm[prev_alarm_idx][r]
        a_i = rng.randint(1, 10**6)
        t += a_i
        finish_times.append((idx, a_i, t))

    # Assign deadlines: d_i = finish_time + slack (or -1 to force impossible)
    alarm_data = [None] * k
    for (idx, a_i, ft) in finish_times:
        if rng.random() < tight_fraction:
            d_i = ft  # exactly tight
        else:
            d_i = ft + rng.randint(1, slack * 10**6)
        alarm_data[idx] = (alarm_rooms[idx], a_i, d_i)

    lines = []
    lines.append(f"{n} {k} {s}")
    for u, v, w in edges:
        lines.append(f"{u} {v} {w}")
    for r, a, d in alarm_data:
        lines.append(f"{r} {a} {d}")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Museum Guard Shift test case generator")
    parser.add_argument("type", choices=["chain", "star", "binary", "random"],
                        help="Tree shape")
    parser.add_argument("n", type=int, help="N (number of nodes, or depth for binary)")
    parser.add_argument("k", type=int, help="K (number of alarms, 0..18)")
    parser.add_argument("s", type=int, nargs="?", default=1, help="Starting room (default: 1)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--slack", type=int, default=5,
                        help="Deadline slack multiplier (default 5)")
    parser.add_argument("--tight", type=float, default=0.3,
                        help="Fraction of deadlines that are exactly tight (default 0.3)")
    args = parser.parse_args()

    tc = generate(args.type, args.n, args.k, args.s, args.seed,
                  slack=args.slack, tight_fraction=args.tight)
    print(tc, end="")
