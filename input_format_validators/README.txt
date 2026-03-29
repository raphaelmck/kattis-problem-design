# Sample Input Validators #

This directory contains two a sample input validators for a fake problem,
written in both Python 3 and in the checktestdata validation language (see:
https://github.com/DOMjudge/checktestdata/blob/master/doc/format-spec.md).

You can validate syntax using checktestdata, Python, or another supported
programming language.  You can separate the validation of syntax and other
properties (e.g. graph connectedness) across different validators if you wish.
For example, it may be easiest to use checktestdata to validate syntax, and
Python to check more complicated properties. The important thing is that
everything that needs validation is validated.

Please use these validators as you like. Modify them as needed for your
problem's input syntax.

Some important general things to remember are:
- Verify the syntax of all input, strictly, using something like
  carefully-written regular expressions. Checktestdata makes this easier.
- When verifying strings, verify length and character sets (e.g. lowercase a-z).
- When verifying integers and real numbers, ensure no leading zeros on
  non-zero numbers (to prevent arbitrarily long tokens).
- When verifying real numbers, ensure a maximum number of digits given after
  the decimal point (again, to prevent arbitrarily long tokens).
- Ensure there is no extra input (e.g. extra spaces, or extra blank lines).
- Make sure that every input constraint is checked, beyond just syntax when
  necessary. For example, if an input promises $k$ unique points, verify that
  they are unique; if a graph is promised to be connected, verify that it is.
- In some circumstances, you may need to actually solve the problem to verify
  some guarantee of the problem. The best way to do this is usually to copy a
  judge's solution here, and modify it so that it is an input validator.
- If you are using a general-purpose programming language, exit with code 42 to
  indicate success.
- Indicate failure by exiting with a non-42 exit code, asserting, etc.

This sample input validator is just for instructional purposes. It assumes
that the (fake) problem has an input syntax as follows:
1. The first line of input contains an integer $n$ indicating the number of
   cases that follow, where 1 <= n <= 100.
2. Each of the following $n$ lines has one case.
3. Each case has a string of 1-20 characters (using only a-z), a single
   space, an integer in the range [-100, 100], then a real number in the
   range [-10.0, 10.0] with an optional fractional portion of at most 3
   digits after the decimal point. All strings are required to be unique.

Here's a sample input which should pass these sample validators:
```
3
foo -31 3.141
bar 41 2.171
baz 59 0.3
```

