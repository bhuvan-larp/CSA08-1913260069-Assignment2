"""Q2 - Loops that Count Attempts: OTP Verification at a Bank Kiosk.

Rules: 3 attempts; after 3 wrong attempts the account is locked for 30 minutes; a BLANK entry does not count as an attempt.
To make the output repeatable the customer's typing is a scripted list instead of input().
"""
import sys
import time

OTP = "482915"


def make_reader(typed):
    """Returns a function that behaves like input(): gives the next scripted entry."""
    it = iter(typed)
    return lambda prompt="": next(it)


# ---------- Design 1: while loop ----------
def verify_while(read):
    attempts = 0
    log = []
    while attempts < 3:
        entry = read("Enter OTP: ").strip()
        if entry == "":                       # blank entry: does not count
            log.append("blank (ignored)")
            continue                          # continue -> back to the while test WITHOUT counting
        attempts += 1                         # counted only for a real entry
        if entry == OTP:
            log.append(f"attempt {attempts}: correct")
            break                             # break -> leaves the loop; the loop-else is skipped
        log.append(f"attempt {attempts}: wrong ({entry})")
    else:
        # runs only when the loop ended WITHOUT break: 3 wrong attempts
        log.append("LOCKED for 30 minutes")
        return "LOCKED", attempts, log
    return "VERIFIED", attempts, log


# ---------- Design 2: for loop with range(3) and loop-else ----------
def verify_for(read):
    log = []
    counted = 0
    # a for-range loop cannot repeat one iteration for a blank entry, so an inner while loop
    # waits for a non-blank entry before the attempt is counted
    for attempt in range(3):
        entry = ""
        while entry == "":                    # inner loop: keep asking until the entry is not blank
            entry = read("Enter OTP: ").strip()
            if entry == "":
                log.append("blank (ignored)")
            else:
                pass                          # pass: nothing to do for a real entry here (placeholder for a future check)
        counted += 1
        if entry == OTP:
            log.append(f"attempt {attempt + 1}: correct")
            break
        log.append(f"attempt {attempt + 1}: wrong ({entry})")
    else:
        log.append("LOCKED for 30 minutes")
        return "LOCKED", counted, log
    return "VERIFIED", counted, log


# ---------- The bug: counter updated in the wrong place ----------
def verify_wrong_counter(read):
    attempts = 0
    while attempts < 3:
        attempts += 1                         # BUG: counted before the blank test
        entry = read("Enter OTP: ").strip()
        if entry == "":
            continue
        if entry == OTP:
            return "VERIFIED", attempts
    return "LOCKED", attempts


# ---------- Changed condition: 2 extra attempts after a correct security answer ----------
def verify_with_security(read, security_correct):
    allowed = 3
    attempts = 0
    asked_security = False
    log = []
    while attempts < allowed:                 # the limit CAN change inside the loop -> while is the natural choice
        entry = read("Enter OTP: ").strip()
        if entry == "":
            log.append("blank (ignored)")
            continue
        attempts += 1
        if entry == OTP:
            log.append(f"attempt {attempts}: correct")
            return "VERIFIED", attempts, log
        log.append(f"attempt {attempts}: wrong ({entry})")
        if attempts == 3 and not asked_security:
            asked_security = True
            if security_correct:
                allowed += 2
                log.append("security question correct -> 2 extra attempts (limit is now 5)")
            else:
                log.append("security question wrong -> no extra attempts")
    log.append("LOCKED for 30 minutes")
    return "LOCKED", attempts, log


# ---------- Alternative: recursion ----------
def verify_recursive(read, attempts=0, depth=1, max_depth=[0]):
    max_depth[0] = max(max_depth[0], depth)
    if attempts == 3:
        return "LOCKED", attempts
    entry = read("Enter OTP: ").strip()
    if entry == "":
        return verify_recursive(read, attempts, depth + 1)          # blank: same attempt count, one more stack frame
    if entry == OTP:
        return "VERIFIED", attempts + 1
    return verify_recursive(read, attempts + 1, depth + 1)


scenarios = {
    "S1 correct on 1st try": (["482915"], "VERIFIED", 1),
    "S2 wrong, wrong, correct": (["111111", "222222", "482915"], "VERIFIED", 3),
    "S3 three wrong -> lock": (["111111", "222222", "333333"], "LOCKED", 3),
    "S4 blanks do not count": (["", "111111", "", "", "222222", "333333"], "LOCKED", 3),
    "S5 blank then correct": (["", "482915"], "VERIFIED", 1),
}

print("=== PART A: predictions (before running) and results for while and for+range(3) designs ===")
print(f"{'scenario':26} {'predicted':16} | {'while loop':18} {'for loop':18} | match")
for name, (typed, pred_state, pred_attempts) in scenarios.items():
    s1, a1, l1 = verify_while(make_reader(typed))
    s2, a2, l2 = verify_for(make_reader(typed))
    ok = (s1, a1) == (pred_state, pred_attempts) == (s2, a2)
    print(f"{name:26} {pred_state + ' / ' + str(pred_attempts):16} | {s1 + ' / ' + str(a1):18} {s2 + ' / ' + str(a2):18} | {'YES' if ok else 'NO'}")

print("\n=== PART B: log of scenario S4 (blanks must not count) - while version ===")
for line in verify_while(make_reader(scenarios["S4 blanks do not count"][0]))[2]:
    print("  ", line)
print("=== for version, same input ===")
for line in verify_for(make_reader(scenarios["S4 blanks do not count"][0]))[2]:
    print("  ", line)

print("\n=== PART C: where break, continue, pass and loop-else are needed ===")
print("  break    : leaves the loop as soon as the OTP is correct (so the lock code in 'else' does not run)")
print("  continue : (while version) a blank entry skips the counting and goes back to the loop test")
print("  pass     : (for version) the empty 'else' branch of the blank test - a placeholder that does nothing")
print("  loop-else: the else clause of while/for runs only if the loop finished WITHOUT break = three wrong attempts -> lock")
print("  proof of loop-else: S2 (correct on 3rd try) never prints LOCKED:", "LOCKED" not in " ".join(verify_while(make_reader(scenarios["S2 wrong, wrong, correct"][0]))[2]))

print("\n=== PART D: bug when the counter is updated in the wrong place ===")
typed = ["", "111111", "482915"]
print("typed entries:", typed, "(a blank, one wrong, then the correct OTP)")
print("PREDICTED: correct counter -> VERIFIED on attempt 2; wrong counter counts the blank -> attempts 1,2,3 used up; still VERIFIED here")
print("correct version (while) :", verify_while(make_reader(typed))[:2])
print("wrong-counter version   :", verify_wrong_counter(make_reader(typed)))
typed2 = ["", "111111", "", "482915"]
print("typed entries:", typed2, "(two blanks, one wrong, then the correct OTP)")
print("PREDICTED: correct -> VERIFIED (2 counted attempts); wrong counter -> LOCKED after 3 'attempts' (2 blanks + 1 wrong)")
print("correct version (while) :", verify_while(make_reader(typed2))[:2])
try:
    print("wrong-counter version   :", verify_wrong_counter(make_reader(typed2)))
except StopIteration:
    print("wrong-counter version   : ran out of typed entries")
print("A customer with the CORRECT OTP is locked out because blank entries used up the attempts.")

print("\n=== PART E: when is while more natural than for? ===")
print("  for range(3): the number of tries is fixed in advance and blank entries need an extra inner loop.")
print("  while attempts < allowed: the loop runs 'until a condition changes', and the limit itself can change.")
print("  The changed condition below shows this: the limit becomes 5 inside the loop - impossible to change in range(3).")

print("\n=== PART F: changed condition - 2 extra attempts after a correct security answer ===")
changed = {
    "3 wrong, security OK, then correct on 5th": (["1", "2", "3", "4", "482915"], True),
    "3 wrong, security OK, 5 wrong -> lock": (["1", "2", "3", "4", "5"], True),
    "3 wrong, security WRONG -> lock": (["1", "2", "3"], False),
}
for name, (typed, sec) in changed.items():
    state, attempts, log = verify_with_security(make_reader(typed), sec)
    print(f"  {name:44} -> {state} after {attempts} attempts")
    for line in log:
        print("       ", line)
print("Design change: replace the fixed 3 by a variable 'allowed' (while loop). Asking the security question happens ONCE (flag).")

print("\n=== PART G: alternative - recursion: time O(a), stack space O(a) vs O(1) ===")
print(f"sys.getrecursionlimit() = {sys.getrecursionlimit()}")
print(f"{'attempts a':>10} {'loop time (ms)':>15} {'recursion time (ms)':>20} {'max stack depth (recursion)':>28} {'loop stack frames':>18}")
for a in (3, 100, 500, 900):
    wrong = [f"{i:06d}" for i in range(a)]

    def loop_version(read, limit):
        n = 0
        while n < limit:
            entry = read("").strip()
            n += 1
            if entry == OTP:
                return "VERIFIED", n
        return "LOCKED", n

    def rec_version(read, limit, n=0, depth=1, md=[0]):
        md[0] = max(md[0], depth)
        if n == limit:
            return "LOCKED", n, md[0]
        entry = read("").strip()
        if entry == OTP:
            return "VERIFIED", n + 1, md[0]
        return rec_version(read, limit, n + 1, depth + 1, md)

    t = time.perf_counter(); r1 = loop_version(make_reader(wrong), a); tl = (time.perf_counter() - t) * 1000
    t = time.perf_counter(); r2 = rec_version(make_reader(wrong), a, md=[0]); tr = (time.perf_counter() - t) * 1000
    assert r1[:2] == r2[:2] == ("LOCKED", a)
    print(f"{a:>10} {tl:>15.4f} {tr:>20.4f} {r2[2] - 0:>28} {1:>18}")
try:
    r = None
    wrong = [f"{i:06d}" for i in range(2000)]

    def rec_big(read, limit, n=0):
        if n == limit:
            return n
        read("")
        return rec_big(read, limit, n + 1)

    rec_big(make_reader(wrong), 2000)
except RecursionError as e:
    print("recursion with 2000 attempts ->", type(e).__name__ + ":", e)
print("Both do one step per attempt, so time is O(a). The loop keeps 1 frame (O(1) stack); recursion keeps a frames (O(a)) and fails near the limit.")
