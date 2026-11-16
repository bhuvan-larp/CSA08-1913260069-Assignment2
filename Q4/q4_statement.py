"""Q4 - Building Long Text: + or join()?  (Monthly SMS Bill Statement)"""
import io
import os
import subprocess
import sys
import tempfile
import time
import tracemalloc


def lines_for(n):
    return [f"Item{i}:Rs{i % 50}" for i in range(n)]


def build_plus(parts):                       # (a) repeated += in a loop
    text = ""
    for p in parts:
        text += p + ";"
    return text


def build_join(parts):                       # (b) list of parts followed by one "".join()
    out = []
    for p in parts:
        out.append(p + ";")
    return "".join(out)


def build_fstring(parts):                    # (c) an f-string for each line, then joined
    return "".join([f"{p};" for p in parts])


def build_plus_aliased(parts):               # += with a second reference to the string: CPython cannot resize in place
    text = ""
    for p in parts:
        keep = text                           # extra reference -> reference count 2 -> every += must copy the whole text
        text += p + ";"
    return text


def build_stringio(parts):                   # alternative: io.StringIO
    buf = io.StringIO()
    for p in parts:
        buf.write(p)
        buf.write(";")
    return buf.getvalue()


def best_time(fn, parts, repeat=3):
    best = float("inf")
    for _ in range(repeat):
        t = time.perf_counter()
        fn(parts)
        best = min(best, time.perf_counter() - t)
    return best


print("=== PART A: prediction (before running) ===")
print("PREDICTED: (b) join and (c) f-string+join are fastest and grow in step with the number of lines, O(n).")
print("           (a) += looks O(n^2) because a string is immutable: every += should copy the whole text built so far.")
print("           BUT CPython sometimes resizes the string in place, so (a) may only be a constant factor slower.")
print("           With a second reference to the string (build_plus_aliased) the in-place trick is impossible -> clear O(n^2).")

print("\n=== PART B: correctness - all versions give the same text ===")
for n in (0, 1, 5, 1000):
    p = lines_for(n)
    texts = [build_plus(p), build_join(p), build_fstring(p), build_plus_aliased(p), build_stringio(p)]
    print(f"n = {n:>5}: all 5 versions equal: {all(t == texts[0] for t in texts)} | length {len(texts[0])}")
print("hand check for n = 3: expected 'Item0:Rs0;Item1:Rs1;Item2:Rs2;' ->", repr(build_join(lines_for(3))))

print("\n=== PART C: timing (best of 3, seconds) for 1,000 / 10,000 / 200,000 lines ===")
print(f"{'lines':>8} {'length':>9} {'(a) += loop':>12} {'(b) join':>10} {'(c) f-string+join':>18} {'(a)/(b)':>8}")
for n in (1_000, 10_000, 200_000):
    p = lines_for(n)
    ta, tb, tc = best_time(build_plus, p), best_time(build_join, p), best_time(build_fstring, p)
    print(f"{n:>8} {len(build_join(p)):>9} {ta:>12.5f} {tb:>10.5f} {tc:>18.5f} {ta / tb:>8.2f}")

print("\n=== PART D: when the in-place optimisation is NOT possible (second reference) ===")
print("Derived: characters copied = sum over lines of the current length = about n^2/2 x average line length")
print(f"{'lines':>8} {'+= with alias (s)':>18} {'join (s)':>10} {'ratio':>8} {'chars copied (derived)':>24}")
prev = None
for n in (5_000, 10_000, 20_000, 40_000):
    p = lines_for(n)
    t_alias = best_time(build_plus_aliased, p, repeat=1)
    tb = best_time(build_join, p)
    avg_len = len(build_join(p)) / n
    copied = int(avg_len * n * n / 2)
    print(f"{n:>8} {t_alias:>18.4f} {tb:>10.5f} {t_alias / tb:>8.0f} {copied:>24,}")
    prev = t_alias
print("Doubling the lines makes the aliased += about 4 times slower (quadratic), while join only doubles.")

print("\n=== PART E: three runs of the 'Complete the Code' program (200,000 lines), average ===")
here = os.path.dirname(os.path.abspath(__file__))
tp, tj = [], []
for run in range(3):
    out = subprocess.run([sys.executable, "q4_complete_code.py"], cwd=here, capture_output=True, text=True).stdout
    line = [l for l in out.splitlines() if l.startswith("+=")][0]
    a = float(line.split("+= time:")[1].split("s")[0])
    b = float(line.split("join time:")[1].split("s")[0])
    tp.append(a); tj.append(b)
    print(f"run {run + 1}: {out.splitlines()[0]} | {line}")
print(f"average += time = {sum(tp) / 3:.4f} s | average join time = {sum(tj) / 3:.4f} s | ratio = {sum(tp) / sum(tj):.2f}")

print("\n=== PART F: alternative - StringIO and writing line by line to a file ===")
n = 200_000
p = lines_for(n)


def write_file(parts):
    with tempfile.NamedTemporaryFile("w", delete=True, suffix=".txt") as f:
        for x in parts:
            f.write(x)
            f.write(";")
        f.flush()
        return os.path.getsize(f.name)


print(f"{'method':22} {'time (s)':>9} {'peak extra memory (MB)':>24}")
for name, fn in [("join (list + join)", build_join), ("io.StringIO", build_stringio), ("+= loop (a)", build_plus), ("write to file", write_file)]:
    t = best_time(fn, p)
    tracemalloc.start()
    fn(p)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"{name:22} {t:>9.4f} {peak / 1e6:>24.2f}")
print("(memory measured with tracemalloc; the shared input list of 200,000 lines is created before measuring and not counted)")
print("join: O(n) time, memory = the list of 200,000 small strings + the final text (the largest of the four here). StringIO: O(n) time, one growing buffer.")
print("file: O(n) time, O(1) memory (only the current line), the statement never exists as one big string.")
print("+= loop: up to O(n^2) characters copied in the worst case (shown in PART D); CPython's in-place resize hides this only for a single-reference local string.")
