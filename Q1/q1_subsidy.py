"""Q1 - Decisions with Many Boundaries: State Electricity Subsidy Eligibility.

Rule (portal):  <=100 units          -> subsidy
                101-200 units        -> partial subsidy ONLY if the household holds a ration card
                > 200 units          -> no subsidy, UNLESS a member is above 80 years of age
My assumptions: "subsidy" for <=100 is called FULL; the senior-citizen case above 200 units gets PARTIAL;
                "above 80" means age > 80 (80 itself is NOT above 80).
"""
import time
import bisect

FULL, PARTIAL, NONE = "FULL", "PARTIAL", "NONE"


def buggy_separate_ifs(units, ration_card, oldest_age):
    """The developer's version: separate if statements. Returns a LIST of subsidies given."""
    given = []
    if units <= 100:
        given.append(FULL)
    if units <= 200 and ration_card:          # forgot the lower bound 101 -> overlaps the first rule
        given.append(PARTIAL)
    if units > 200 and oldest_age > 80:
        given.append(PARTIAL)
    if not given:
        given.append(NONE)
    return given


def decide_elif(units, ration_card, oldest_age):
    """if-elif-else with chained comparisons: exactly ONE branch runs."""
    if units <= 100:
        return FULL
    elif 101 <= units <= 200:
        return PARTIAL if ration_card else NONE
    else:                                    # units > 200
        return PARTIAL if oldest_age > 80 else NONE


def decide_nested(units, ration_card, oldest_age):
    """Nested if version (for the design comparison)."""
    if units <= 100:
        return FULL
    else:
        if units <= 200:
            if ration_card:
                return PARTIAL
            else:
                return NONE
        else:
            if oldest_age > 80:
                return PARTIAL
            else:
                return NONE


def decide_boolean(units, ration_card, oldest_age):
    """Combined Boolean conditions version (for the design comparison)."""
    if units <= 100:
        return FULL
    if (101 <= units <= 200 and ration_card) or (units > 200 and oldest_age > 80):
        return PARTIAL
    return NONE


def decide_match(units, ration_card, oldest_age):
    """Alternative concept 1: match-case (Python 3.10+) with guards."""
    match units:
        case u if u <= 100:
            return FULL
        case u if u <= 200:
            return PARTIAL if ration_card else NONE
        case _:
            return PARTIAL if oldest_age > 80 else NONE


SLABS = [(100, "A"), (200, "B"), (float("inf"), "C")]       # (upper limit, slab code) - lookup table


def slab_of(units, slabs):
    """Alternative concept 2: list of (upper limit, decision) pairs searched in a loop. Returns (index, comparisons)."""
    comparisons = 0
    for i, (upper, _) in enumerate(slabs):
        comparisons += 1
        if units <= upper:
            return i, comparisons
    return len(slabs) - 1, comparisons


def decide_table(units, ration_card, oldest_age):
    idx, _ = slab_of(units, SLABS)
    if idx == 0:
        return FULL
    if idx == 1:
        return PARTIAL if ration_card else NONE
    return PARTIAL if oldest_age > 80 else NONE


households = [
    # (name, units, ration card, oldest age, PREDICTION written before running)
    ("H1", 100, False, 40, FULL),
    ("H2", 101, True, 45, PARTIAL),
    ("H3", 101, False, 45, NONE),
    ("H4", 200, True, 30, PARTIAL),
    ("H5", 200, False, 30, NONE),
    ("H6", 201, False, 81, PARTIAL),
    ("H7", 201, True, 80, NONE),
    ("H8", 60, True, 35, FULL),
]

print("=== PART A: predictions (made BEFORE running) vs observed, at every boundary ===")
print("Boundary units tested: 100, 101, 200, 201 (plus age boundary 80/81 and one low-use house with a ration card)")
print(f"{'house':5} {'units':>5} {'ration':>6} {'oldest':>6} | {'predicted':9} | {'if-elif':9} {'nested':9} {'boolean':9} {'match':9} {'table':9} | {'separate ifs (buggy)':22} {'ok?'}")
all_ok = True
for name, u, r, a, pred in households:
    e, n, b, m, t = decide_elif(u, r, a), decide_nested(u, r, a), decide_boolean(u, r, a), decide_match(u, r, a), decide_table(u, r, a)
    bug = buggy_separate_ifs(u, r, a)
    ok = e == n == b == m == t == pred
    all_ok &= ok
    print(f"{name:5} {u:>5} {str(r):>6} {a:>6} | {pred:9} | {e:9} {n:9} {b:9} {m:9} {t:9} | {str(bug):22} {'YES' if ok else 'NO'}")
print("all five correct implementations agree with every prediction:", all_ok)

print("\n=== PART B: why separate ifs can give two results ===")
print("Each separate 'if' is tested on its own, so more than one condition can be True for the same household.")
print("In the buggy code the 2nd rule is 'units <= 200 and ration_card' (no lower bound), so a ration-card house with 60 units")
print("satisfies BOTH rule 1 (units <= 100) and rule 2.  Result:", buggy_separate_ifs(60, True, 35), "-> two subsidies")
print("if-elif-else tests top to bottom and runs only the FIRST branch that is True, then jumps past the rest. Result:", decide_elif(60, True, 35))

print("\n=== PART C: exhaustive check 0..300 units x ration card x age {30, 80, 81} ===")
doubles = 0
disagree = 0
total = 0
for u in range(0, 301):
    for r in (False, True):
        for a in (30, 80, 81):
            total += 1
            if len(buggy_separate_ifs(u, r, a)) > 1:
                doubles += 1
            if not (decide_elif(u, r, a) == decide_nested(u, r, a) == decide_boolean(u, r, a) == decide_match(u, r, a) == decide_table(u, r, a)):
                disagree += 1
print(f"cases checked: {total} | cases where the buggy separate-if version gave TWO results: {doubles} | cases where correct versions disagree: {disagree}")
print("units range where the bug shows (ration card holders): 0 to 100 ->", sum(1 for u in range(301) if len(buggy_separate_ifs(u, True, 30)) > 1), "values of units")

print("\n=== PART D: design decision (nested if vs combined Boolean) ===")
import inspect


def code_lines(fn):
    """Lines of real code: not counting the def line, the docstring and blank lines."""
    lines = inspect.getsource(fn).splitlines()[1:]
    out, in_doc = [], False
    for ln in lines:
        t = ln.strip()
        if t.startswith('"""'):
            if not (t.endswith('"""') and len(t) > 3):
                in_doc = not in_doc
            continue
        if in_doc or not t:
            continue
        out.append(t)
    return len(out)


print("Lines of code in each function (counted by the program, without def line, docstring and blank lines):",
      "nested =", code_lines(decide_nested), "| combined Boolean =", code_lines(decide_boolean), "| if-elif with chained comparison =", code_lines(decide_elif))
print("Decision: if-elif-else with chained comparisons, and one small conditional expression inside each slab.")
print("  - slabs are mutually exclusive, so the elif chain reads exactly like the portal rule (one line per slab)")
print("  - a change of a limit (e.g. 200 -> 250) edits ONE number; the Boolean version repeats units in two places")
print("  - nested if hides the ration-card and age tests three levels deep and is the hardest to change")

print("\n=== PART E: alternative concepts - time per decision for k slabs ===")
print("Derived: if-elif and slab table with a loop test up to k limits -> O(k) per decision (worst case k comparisons); table space O(k);")
print("match-case with guards behaves like if-elif: O(k). A sorted table with bisect: O(log k).")
print(f"{'k slabs':>8} {'worst-case comparisons (loop)':>30} {'loop time per decision (us)':>28} {'bisect time per decision (us)':>30}")
for k in (3, 30, 300, 3000):
    slabs = [(10 * (i + 1), i) for i in range(k - 1)] + [(float("inf"), k - 1)]
    limits = [s[0] for s in slabs]
    worst_units = 10 * k + 5                                  # falls in the last slab
    _, comps = slab_of(worst_units, slabs)
    reps = 20000 if k <= 300 else 2000
    t = time.perf_counter()
    for _ in range(reps):
        slab_of(worst_units, slabs)
    t_loop = (time.perf_counter() - t) / reps
    t = time.perf_counter()
    for _ in range(reps):
        bisect.bisect_left(limits, worst_units)
    t_bis = (time.perf_counter() - t) / reps
    assert slab_of(worst_units, slabs)[0] == bisect.bisect_left(limits, worst_units)
    print(f"{k:>8} {comps:>30} {t_loop * 1e6:>28.3f} {t_bis * 1e6:>30.3f}")
print("The loop's comparisons equal k (worst case) and its time grows about 10x for every 10x more slabs -> O(k).")
print("For the real rule k = 3, so every version takes well under a microsecond; readability decides.")
print("Space: if-elif / match = O(1) data (the code itself has k branches); table = O(k) data that can be edited without changing code.")
