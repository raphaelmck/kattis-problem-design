#!/usr/bin/env python3

import sys

def read_line():
    line = sys.stdin.readline()
    assert line != ''
    return line

def parse_int_token(tok):
    # Strict integer format: no leading zeros except for "0"
    if tok == "0":
        return 0
    if tok.startswith("-"):
        digits = tok[1:]
        assert digits != ""
        assert digits[0] != "0"
        assert digits.isdigit()
        return int(tok)
    else:
        assert tok[0] != "0"
        assert tok.isdigit()
        return int(tok)

def parse_fixed_k_ints_line(k):
    line = read_line()
    assert line.endswith("\n")
    parts = line[:-1].split(" ")
    assert len(parts) == k
    assert all(p != "" for p in parts)
    return [parse_int_token(p) for p in parts]

# First line: N K S
n, K, S = parse_fixed_k_ints_line(3)
assert 1 <= n <= 200000
assert 0 <= K <= 18
assert 1 <= S <= n

parent = list(range(n + 1))
size = [1] * (n + 1)

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def union(a, b):
    ra = find(a)
    rb = find(b)
    if ra == rb:
        return False
    if size[ra] < size[rb]:
        ra, rb = rb, ra
    parent[rb] = ra
    size[ra] += size[rb]
    return True

# Next N - 1 lines: edges
for _ in range(n - 1):
    u, v, w = parse_fixed_k_ints_line(3)
    assert 1 <= u <= n
    assert 1 <= v <= n
    assert u != v
    assert 1 <= w <= 10**9
    assert union(u, v)

# Check connectivity
root = find(1)
for x in range(2, n + 1):
    assert find(x) == root

# Next K lines: alarms
seen_rooms = set()
for _ in range(K):
    r, a, d = parse_fixed_k_ints_line(3)
    assert 1 <= r <= n
    assert 1 <= a <= 10**9
    assert 1 <= d <= 10**15
    assert r not in seen_rooms
    seen_rooms.add(r)

# No extra input
assert sys.stdin.readline() == ''

# Valid input
sys.exit(42)