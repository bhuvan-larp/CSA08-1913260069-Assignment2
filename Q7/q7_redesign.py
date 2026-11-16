"""Q7 - Day-4 Design Challenge: Diagnose, Redesign and Validate.

Chosen program: the plain recursive ways_naive(n) of Q6 (temple steps).
Original  : ways(n) = ways(n-1) + ways(n-2), no memory of earlier answers.
Redesign  : bottom-up loop that keeps only the last two values (own design, no lru_cache and no built-in shortcut).
"""
import sys
import time

calls = 0


def ways_naive(n):                                # ORIGINAL (from Q6)
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_naive(n - 1) + ways_naive(n - 2)


def ways_redesign(n):                             # REDESIGN: returns (answer, additions performed)
    a, b = 1, 1                                   # ways(0), ways(1)
    additions = 0
    for _ in range(2, n + 1):
        a, b = b, a + b
        additions += 1
    return b, additions


def table_up_to(n_max):                           # REDESIGN, many queries: one pass fills ways(0..n_max)
    table = [1, 1]
    for i in range(2, n_max + 1):
        table.append(table[i - 1] + table[i - 2])
    return table


print("=== PART A: Diagnose the bottleneck (evidence from the original program) ===")
n = 25
per_n = {}


def count_calls(k):
    per_n[k] = per_n.get(k, 0) + 1
    if k > 1:
        count_calls(k - 1)
        count_calls(k - 2)


count_calls(n)
total = sum(per_n.values())
print(f"ways_naive({n}): total function calls = {total:,}  | distinct sub-questions (values 0..{n}) = {n + 1}")
print(f"average number of times the SAME sub-question is asked = {total / (n + 1):,.0f}")
print("How many times each sub-question ways(k) is called when we start from ways(25):")
print(f"{'k':>4} {'times called':>14} {'share of all calls':>20}")
for k in (25, 24, 23, 20, 15, 10, 5, 2, 1, 0):
    print(f"{k:>4} {per_n[k]:>14,} {per_n[k] / total * 100:>19.2f}%")
base = per_n[1] + per_n[0]
print(f"calls to the base cases ways(1) and ways(0): {base:,} = {base / total * 100:.1f}% of ALL calls -> most work is done at the very bottom of the tree")
print("Count growth with n (original):")
print(f"{'n':>4} {'calls':>12} {'ratio per 5 more steps':>28}")
prev = None
for k in (10, 15, 20, 25, 30):
    calls = 0; ways_naive(k)
    r = "" if prev is None else f"{calls / prev:.2f} (5 steps -> x{1.618 ** 5:.2f} expected)"
    print(f"{k:>4} {calls:>12,} {r:>28}")
    prev = calls
print("Diagnosis: (1) the count of calls grows exponentially, about 1.618 times per extra step (phi^n);")
print("           (2) most of the work is repeated: ways(1) alone is answered 75,025 times for n = 25 while its answer never changes;")
print("           (3) ways(n) depends only on the TWO previous answers, so nothing older than ways(n-2) ever needs to be remembered.")

print("\n=== PART B: Design objective (measurable) ===")
print("Objective: for n = 30, cut the function calls from 2,692,537 to at most 31 (one step per value) - at least 85,000 times fewer -")
print("           and the time from about 0.1 s to under 0.01 ms; and the same program must work for n = 1,000 and n = 100,000")
print("           with NO RecursionError and constant extra memory (two variables).")

print("\n=== PART C: Revised design ===")
print("What changed : recursion (top-down, asks the same question again and again) -> bottom-up loop that answers ways(2), ways(3), ... ways(n) once, in order.")
print("Property used: overlapping sub-problems (the same ways(k) is needed many times) and that each answer depends only on the previous two.")
print("Extra memory : none - two variables a and b. A table of all values (O(n)) is only needed when many different n are asked.")
print("New trade-off: no cache is shared between queries, so every query costs O(n) again; many queries -> build the table once (table_up_to).")
print("Pseudocode:")
print("   a <- 1 ; b <- 1                      # ways(0), ways(1)")
print("   repeat for i from 2 to n:")
print("       a, b <- b, a + b                 # slide the window of two values")
print("   return b                             # ways(n)   (n <= 1 returns 1)")
print("Flowchart: q7_flowchart.png (saved in this folder).")

print("\n=== PART D: Prediction (before implementing) ===")
print("PREDICTED: additions = n - 1 for n >= 2 (n = 10 -> 9, 20 -> 19, 25 -> 24, 30 -> 29); no recursive calls; answers equal the original.")
print("PREDICTED: speed-up of at least 10^4 at n = 30 (2,692,537 calls vs 29 steps); calls go from exponential O(phi^n) to linear O(n).")
print("PREDICTED: for printing ways(1..1000), running the loop separately for every n costs 1+2+...+999 = 499,500 additions; one table pass costs 999.")

print("\n=== PART E: Implement and validate - same inputs, counts and times ===")
print(f"{'n':>4} {'answer equal':>13} {'original calls':>15} {'redesign additions':>19} {'predicted additions':>20} {'original time (s)':>18} {'redesign time (s)':>18} {'speed-up':>10}")
for n in (10, 20, 25, 30):
    calls = 0
    t = time.perf_counter(); a = ways_naive(n); to = time.perf_counter() - t
    c_orig = calls
    best = float("inf")
    for _ in range(5):
        t = time.perf_counter(); b, adds = ways_redesign(n); best = min(best, time.perf_counter() - t)
    print(f"{n:>4} {str(a == b):>13} {c_orig:>15,} {adds:>19} {n - 1:>20} {to:>18.6f} {best:>18.8f} {to / best:>10,.0f}x")
print("Answers also checked for every n from 0 to 30 against the original:", all(ways_redesign(k)[0] == (calls := 0, ways_naive(k))[1] for k in range(0, 31)))

print("\nLarge inputs (the original cannot run these):")
sys.set_int_max_str_digits(0)
for n in (1_000, 100_000):
    t = time.perf_counter(); ans, adds = ways_redesign(n); el = time.perf_counter() - t
    print(f"n = {n:>7,}: {adds:,} additions, {el * 1000:.3f} ms, answer has {len(str(ans)):,} digits, recursion depth used = 0")
try:
    ways_naive(1000)
except RecursionError as e:
    print("original ways_naive(1000) ->", type(e).__name__)

print("\nPrinting ways(1..1000): one query per n versus one table pass")
total_adds = sum(ways_redesign(k)[1] for k in range(1, 1001))
t = time.perf_counter(); [ways_redesign(k)[0] for k in range(1, 1001)]; t_sep = time.perf_counter() - t
t = time.perf_counter(); table = table_up_to(1000); t_tab = time.perf_counter() - t
print(f"loop for every n separately : {total_adds:,} additions, {t_sep * 1000:.2f} ms")
print(f"one table pass (table_up_to): {len(table) - 2:,} additions, {t_tab * 1000:.2f} ms, memory = list of 1,001 numbers")
print("table equals separate answers:", table[1:] == [ways_redesign(k)[0] for k in range(1, 1001)])

print("\n=== PART F: Defend the final design ===")
print("Objective achieved? Calls for n = 30: 2,692,537 -> 29 additions (about 93,000 times fewer); time at n = 30 reduced by the factor shown in PART E;")
print("   n = 1,000 and n = 100,000 run without any RecursionError. Every answer matched the original for n = 0..30.")
print("New costs: (1) no shared cache between queries - every query is O(n) again (the table pass fixes this for repeated queries at O(n) memory);")
print("   (2) the numbers themselves get large (about 0.69 bits per step), so each addition costs time proportional to the number's size - the")
print("   'O(n) additions' is not O(n) bit operations; the loop for n = 100,000 is still fast but not instant (see times above).")
print("Where the original is still preferable: it is a direct copy of the definition ways(n) = ways(n-1) + ways(n-2), the easiest to read and verify;")
print("   for n up to about 20 (21,891 calls, a few milliseconds) it is perfectly acceptable. I keep it only as the test oracle for the redesign.")
