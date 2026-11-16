"""Q6 - Recursion and Its Limits: Counting Ways to Climb Temple Steps."""
import subprocess
import sys
import time
from functools import lru_cache

calls = 0


def ways_naive(n):
    global calls
    calls += 1
    if n <= 1:
        return 1                                  # base case: 0 or 1 step left -> exactly 1 way
    return ways_naive(n - 1) + ways_naive(n - 2)  # recursive case: last move was 1 step or 2 steps


@lru_cache(maxsize=None)
def ways_memo(n):
    global calls
    calls += 1
    if n <= 1:
        return 1
    return ways_memo(n - 1) + ways_memo(n - 2)


def ways_loop(n):
    """Keeps only the last two values: O(n) time, O(1) extra space (not counting the big result)."""
    a, b = 1, 1                                   # ways(0), ways(1)
    for _ in range(n - 1):
        a, b = b, a + b
    return b if n >= 1 else 1


print("=== PART A: design ===")
print("Base case     : n <= 1 -> 1 way (standing at the bottom, or one step left).")
print("Recursive case: ways(n) = ways(n-1) + ways(n-2)   (the devotee's last move was 1 step or 2 steps)")

print("\n=== PART B: correctness check - hand values for n = 1..6 ===")
by_hand = {1: 1, 2: 2, 3: 3, 4: 5, 5: 8, 6: 13}
print("PREDICTED by hand: ways(1)=1, ways(2)=2 (1+1, 2), ways(3)=3 (111,12,21), ways(4)=5, ways(5)=8, ways(6)=13 (each = sum of the two before)")
print(f"{'n':>2} {'by hand':>8} {'naive':>6} {'memo':>6} {'loop':>6}  match")
for n, h in by_hand.items():
    ways_memo.cache_clear()
    print(f"{n:>2} {h:>8} {ways_naive(n):>6} {ways_memo(n):>6} {ways_loop(n):>6}  {'YES' if ways_naive(n) == ways_memo(n) == ways_loop(n) == h else 'NO'}")

print("\n=== PART C: call tree for ways(5) (plain recursion) ===")
tree_calls = 0


def show_tree(n, depth=0):
    global tree_calls
    tree_calls += 1
    print("   " * depth + f"ways({n})")
    if n <= 1:
        return 1
    return show_tree(n - 1, depth + 1) + show_tree(n - 2, depth + 1)


show_tree(5)
print("total calls in this tree:", tree_calls)
print("Repeated work: ways(3) is computed 2 times, ways(2) 3 times, ways(1) 5 times, ways(0) 3 times in this tree.")
counts = {}


def count_each(n):
    counts[n] = counts.get(n, 0) + 1
    if n > 1:
        count_each(n - 1); count_each(n - 2)


count_each(5)
print("counted by the program:", dict(sorted(counts.items(), reverse=True)))
print("Plain recursion repeats work because ways(n-1) itself calls ways(n-2), and ways(n) calls ways(n-2) again - the same sub-question is asked many times.")

print("\n=== PART D: growth investigation - function calls ===")
print("PREDICTION: naive calls = 2*ways(n) - 1  (the leaves of the call tree are ways(n) calls that return 1; a tree whose nodes have 0 or 2 children")
print("            has leaves - 1 inner nodes). Memoised calls = n + 1  (each value 0..n is computed once; repeats are cache hits that skip the body).")
print(f"{'n':>4} {'ways(n)':>10} {'predicted naive':>16} {'naive calls':>12} {'predicted memo':>15} {'memo calls':>11}  ok")
for n in (10, 20, 25, 30):
    calls = 0; w = ways_naive(n); cn = calls
    ways_memo.cache_clear(); calls = 0; w2 = ways_memo(n); cm = calls
    print(f"{n:>4} {w:>10} {2 * w - 1:>16} {cn:>12} {n + 1:>15} {cm:>11}  {'YES' if (cn, cm) == (2 * w - 1, n + 1) and w == w2 else 'NO'}")
print("Ratio naive(n+1)/naive(n) is about 1.618 (the golden ratio): calls grow like phi^n, i.e. exponentially.")
for n in (20, 25, 30):
    calls = 0; ways_naive(n); a = calls
    calls = 0; ways_naive(n + 1); b = calls
    print(f"   calls({n + 1}) / calls({n}) = {b / a:.4f}")

print("\n=== PART E: deployment - ways_memo(1000) and the recursion limit ===")
print("sys.getrecursionlimit() =", sys.getrecursionlimit())
ways_memo.cache_clear()
try:
    ways_memo(1000)
except RecursionError as e:
    print("ways_memo(1000) ->", type(e).__name__ + ":", e)
print("Why: the first call ways_memo(1000) calls ways_memo(999), which calls ways_memo(998) ... down to ways_memo(1) BEFORE any value is cached.")
print("That is about 1,000 nested calls (plus the starting frame), and Python allows only 1,000 frames by default.")
ways_memo.cache_clear()
sys.setrecursionlimit(5000)
ways_memo.cache_clear()
t = time.perf_counter(); r = ways_memo(1000); t_memo = time.perf_counter() - t
print("after sys.setrecursionlimit(5000): ways_memo(1000) works. digits in the answer:", len(str(r)), "| cache entries:", ways_memo.cache_info().currsize, "| time:", f"{t_memo * 1000:.3f} ms")
sys.setrecursionlimit(1000)
print("limit restored to", sys.getrecursionlimit())

print("\nHow far does raising the limit help? Each test runs in a SEPARATE Python process, so a failure cannot stop this program:")
print(f"{'n':>7} {'limit set':>10}  {'lru_cache version':44} {'dictionary-memo version':44}")
for n in (1000, 5000, 20000, 100000):
    res = []
    for kind in ("lru", "dict"):
        if kind == "lru":
            body = "from functools import lru_cache\n@lru_cache(maxsize=None)\ndef w(n):\n    return 1 if n<=1 else w(n-1)+w(n-2)\n"
        else:
            body = "m={}\ndef w(n):\n    if n<=1: return 1\n    if n in m: return m[n]\n    m[n]=w(n-1)+w(n-2)\n    return m[n]\n"
        code = f"import sys; sys.setrecursionlimit({n + 100}); sys.set_int_max_str_digits(0)\n" + body + f"print(len(str(w({n}))))"
        p = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=300)
        if p.returncode == 0:
            res.append(f"works, {p.stdout.strip()} digits")
        else:
            last = p.stderr.strip().splitlines()[-1] if p.stderr.strip() else f"exit code {p.returncode}"
            res.append(("FAILS: " + last)[:44] if p.returncode == 1 else f"CRASH exit code {p.returncode}")
    print(f"{n:>7} {n + 100:>10}  {res[0]:44} {res[1]:44}")
print("So raising the limit is not a reliable fix: on this computer (Python 3.12.3) the lru_cache version already fails at n = 5,000 although the limit was raised,")
print("while a plain dictionary memo keeps working; the result depends on the Python version and the machine.")

print("\n=== PART F: all three methods for n = 1,000 ===")
ways_memo.cache_clear(); sys.setrecursionlimit(5000)
t = time.perf_counter(); rm = ways_memo(1000); tm = time.perf_counter() - t
sys.setrecursionlimit(1000)
t = time.perf_counter(); rl = ways_loop(1000); tl = time.perf_counter() - t
print(f"memoised (limit raised) : {len(str(rm))} digits, {tm * 1000:.4f} ms, 1,001 function-body calls")
print(f"loop (last two values)  : {len(str(rl))} digits, {tl * 1000:.4f} ms, 999 loop steps, no recursion")
print("same answer:", rm == rl)
print("first 20 digits:", str(rl)[:20], "... last 20 digits:", str(rl)[-20:])
print("plain recursion for n = 1,000: NOT RUN. It would need 2*ways(1000) - 1 calls, a number with", len(str(2 * rl - 1)), "digits.")
t30 = None
tm_list = []
for n in (25, 28, 30, 32):
    calls = 0; t = time.perf_counter(); ways_naive(n); tt = time.perf_counter() - t
    tm_list.append((n, calls, tt))
    print(f"   measured plain recursion: n = {n}: calls = {calls:>9}, time = {tt:.4f} s")
rate = tm_list[-1][2] / tm_list[-1][1]
est_seconds = (2 * rl - 1) * rate
print(f"ESTIMATE (not measured): at {rate * 1e6:.3f} microseconds per call, 2*ways(1000)-1 calls would take about {est_seconds:.2e} seconds,")
print("   far longer than the age of the universe (about 4.4e17 seconds).")

print("\n=== PART G: alternative - the loop - time and space ===")
print("Time : plain recursion O(phi^n) (about 1.618^n); memoised recursion O(n); loop O(n).")
print("Space: memoised recursion O(n) for the cache AND O(n) stack depth; loop O(1) extra (two variables).")
def ways_dict_depth(n, memo, depth, stats):
    stats[0] = max(stats[0], depth)
    if n <= 1:
        return 1
    if n in memo:
        return memo[n]
    memo[n] = ways_dict_depth(n - 1, memo, depth + 1, stats) + ways_dict_depth(n - 2, memo, depth + 1, stats)
    return memo[n]


print(f"{'n':>6} {'memo time (ms)':>15} {'loop time (ms)':>15} {'memo cache entries':>19} {'memo max stack depth (measured)':>32} {'loop stack depth':>17}")
for n in (100, 500, 1000, 2000):
    sys.setrecursionlimit(max(5000, n + 100))
    ways_memo.cache_clear()
    t = time.perf_counter(); a = ways_memo(n); tmm = (time.perf_counter() - t) * 1000
    t = time.perf_counter(); b = ways_loop(n); tll = (time.perf_counter() - t) * 1000
    stats = [0]
    c = ways_dict_depth(n, {}, 1, stats)
    assert a == b == c
    print(f"{n:>6} {tmm:>15.4f} {tll:>15.4f} {ways_memo.cache_info().currsize:>19} {stats[0]:>32} {1:>17}")
sys.setrecursionlimit(1000)
print("(stack depth measured with a dictionary-memo twin of the function that records its deepest call; the loop uses one frame.)")

print("\n=== PART H: decision ===")
print("Decision: use the LOOP in the program that prints answers for staircases up to 1,000 steps, and keep the memoised recursion only as the")
print("readable specification and for tests.  Raising the recursion limit works for 1,000 (shown above) but its effect depends on the")
print("Python version and machine, it still needs O(n) stack frames, and the lru_cache version fails at n = 5,000 even with a raised limit (table above). The loop needs no limit, no cache")
print("and finished n = 1,000 in a fraction of a millisecond. Both together: loop for production, memo version cross-checks the loop in tests.")
