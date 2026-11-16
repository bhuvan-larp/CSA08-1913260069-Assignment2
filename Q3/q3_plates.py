"""Q3 - Engineer a Vehicle Registration Number Validator (string operations only, no regular expressions in the main solution)."""
import random
import re
import string
import time

import pathlib

# reuse the three functions from the "Complete the Code" file without running its demo loop
src = pathlib.Path(__file__).with_name("q3_complete_code.py").read_text()
ns = {}
exec(src.split("for raw in")[0], ns)
normalise, is_valid, format_reg = ns["normalise"], ns["is_valid"], ns["format_reg"]


def is_valid_strict(reg):
    """Hardened version: also requires plain ASCII, because isalpha()/isdigit() accept other scripts and symbols."""
    return reg.isascii() and is_valid(reg)


def is_valid_regex(reg):
    """Alternative concept: one regular expression."""
    return re.fullmatch(r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}", reg) is not None


print("=== PART A: predictions (written before running) for six inputs, two should be rejected ===")
tests = [
    # (typed text, predicted normalised, predicted valid?)
    ("tn 09 ab 1234", "TN09AB1234", True),
    ("TN-09-AB-1234", "TN09AB1234", True),
    ("Tn09Ab1234", "TN09AB1234", True),
    ("ka 01 m 0007", "KA01M0007", True),
    ("TN 09 ABC 1234", "TN09ABC1234", False),       # three series letters -> length 11
    ("TN 9 AB 1234", "TN9AB1234", False),           # district has one digit
]
print(f"{'typed':18} | {'predicted':13} {'valid':6} | {'actual':13} {'valid':6} | match | receipt format")
ok_all = True
for raw, pred_norm, pred_valid in tests:
    reg = normalise(raw)
    v = is_valid(reg)
    ok = (reg, v) == (pred_norm, pred_valid)
    ok_all &= ok
    print(f"{raw!r:18} | {pred_norm:13} {str(pred_valid):6} | {reg:13} {str(v):6} | {'YES' if ok else 'NO ':3}   | {format_reg(reg) if v else '-'}")
print("all predictions correct:", ok_all)

print("\n=== PART B: Inquiry - immutability and slicing ===")
s = "tn09ab1234"
try:
    s[0] = "T"
except TypeError as e:
    print("s[0] = 'T' ->", type(e).__name__ + ":", e)
before = id(s)
t = s.upper()
print("s.upper() returns a NEW string:", repr(t), "| s is still", repr(s), "| same object?", id(t) == before)
s = s.upper()
print("only s = s.upper() makes the name s point to the new string:", repr(s))
print("Why strings are immutable: they are hashable dictionary keys, safe to share between variables, and their hash never changes.")
nine, ten = "KA01M0007", "TN09AB1234"
print(f"9-character number {nine!r}:  s[-4:] = {nine[-4:]!r}   s[4:-4] = {nine[4:-4]!r}   (series letters: 1)")
print(f"10-character number {ten!r}: s[-4:] = {ten[-4:]!r}   s[4:-4] = {ten[4:-4]!r}   (series letters: 2)")
print("s[-4:] is always the 4-digit number; s[4:-4] is whatever lies between the district and the number = the series (1 or 2 letters).")

print("\n=== PART C: edge cases and the isalpha()/isdigit() trap ===")
cases = ["", "   ", "TN09AB123", "TN09AB12345", "TN09ABC1234", "tn 09 ab 1234 ", "TN\t09AB1234", "TN09AB1234\n", "TN０９AB1234", "TN09AB١٢٣٤", "TN09AB²²²²"]
print(f"{'input':20} {'normalised':16} {'template is_valid':18} {'strict (ascii)':15}")
for raw in cases:
    reg = normalise(raw)
    print(f"{raw!r:20} {reg!r:16} {str(is_valid(reg)):18} {str(is_valid_strict(reg)):15}")
print("Observation: strings with full-width digits, Arabic digits or superscripts PASS the template's isdigit() check; the strict version rejects them.")
print("Tabs and new lines are not removed by replace(' ', '') - the strict check or a .split()/''.join() normaliser would be needed.")
print("normalise with split/join (removes ALL whitespace):", ''.join('TN\t09 AB-1234'.replace('-', '').split()).upper())

print("\n=== PART D: alternative concept - regular expression vs slicing ===")
rng = random.Random(1)
letters, digits = string.ascii_uppercase, string.digits


def random_plate():
    kind = rng.random()
    if kind < 0.5:
        return (rng.choice(letters) + rng.choice(letters) + "".join(rng.choice(digits) for _ in range(2))
                + "".join(rng.choice(letters) for _ in range(rng.choice([1, 2]))) + "".join(rng.choice(digits) for _ in range(4)))
    chars = list(random_plate_valid())
    i = rng.randrange(len(chars))
    chars[i] = rng.choice(letters + digits)
    return "".join(chars)[: rng.choice([8, 9, 10, 10, 11])]


def random_plate_valid():
    return (rng.choice(letters) + rng.choice(letters) + "".join(rng.choice(digits) for _ in range(2))
            + "".join(rng.choice(letters) for _ in range(rng.choice([1, 2]))) + "".join(rng.choice(digits) for _ in range(4)))


sample = [random_plate() for _ in range(50000)]
same = all(is_valid(p) == is_valid_regex(p) for p in sample)
print("50,000 random plates, slicing result == regex result for every plate:", same, "| valid plates in sample:", sum(is_valid(p) for p in sample))
print(f"{'method':22} {'time for 50,000 plates (s)':>28} {'per plate (us)':>15}")
for name, fn in [("slicing + isalpha", is_valid), ("re.fullmatch (cached pattern)", is_valid_regex)]:
    best = float("inf")
    for _ in range(5):
        t = time.perf_counter()
        for p in sample:
            fn(p)
        best = min(best, time.perf_counter() - t)
    print(f"{name:22} {best:>28.4f} {best / len(sample) * 1e6:>15.3f}")
print("Time: both examine each character at most once -> O(L) for a number of length L (L is at most 10 here).")
print("Readability: the regex states the pattern in one line, [A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}; the slicing version needs the length check")
print("and three slices. Ease of change: allowing 3 series letters is a one-character regex edit ({1,3}) but needs a new length test and slice rule in the slicing version.")
print("Note: the regex pattern does not accept the non-ASCII digit trap above because [0-9] means only ASCII digits.")
