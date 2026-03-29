#!/usr/bin/env python3

# This is a sample input validator, written in Python 3.

# Please refer to the comments in README.md for a description of the syntax it
# is validating. Then, change it as you need.

import sys
import re

n_line = sys.stdin.readline()
print(repr(n_line)) # useful for debugging to see where we have read
assert re.match('^[1-9][0-9]*\n$', n_line) # note: no leading zeros
n = int(n_line)
assert 1 <= n <= 100

unique_strings = set()
for _ in range(n):
    case_line = sys.stdin.readline()
    print(repr(case_line)) # useful for debugging to see where we have read
    # check the line syntax (string, integer, real)
    assert re.match('^[a-z]{1,20} (0|-?[1-9][0-9]{0,2}) (0|-?[1-9][0-9]?)(\.[0-9]{1,3})?\n$', case_line)

    # parse the line
    s, i, f = case_line.split()
    assert -100 <= int(i) <= 100
    assert -10.0 <= float(f) <= 10.0

    # verify string uniqueness
    assert s not in unique_strings
    unique_strings.add(s)

# ensure no extra input
assert sys.stdin.readline() == ''

# if we get here, all is well; use exit code 42.
sys.exit(42)

