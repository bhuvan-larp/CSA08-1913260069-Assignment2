# Q2 – Loops that Count Attempts (4 marks, K3)
Run: `python3 q2_otp.py` (output in `output.txt`). The customer's typing is a scripted list so the output is repeatable.
* while version: `continue` skips counting a blank entry, `break` leaves on the correct OTP, the loop-`else` locks the account after 3 wrong attempts (it runs only when the loop ends without `break`).
* for/range(3) version: needs an inner `while` to wait for a non-blank entry; a `pass` marks the do-nothing branch; loop-`else` locks.
* All 5 scenarios matched the predictions in both designs.
* Bug when the counter is updated before the blank test: two blanks + one wrong use up 3 "attempts", so a customer who then types the CORRECT OTP is locked out (shown in PART D).
* while is more natural when the limit can change or the number of tries is not known in advance. Changed condition (2 extra attempts after a correct security answer): the limit becomes a variable `allowed` (3 → 5), the question is asked once.
* Alternative: recursion is O(a) time like the loop but O(a) stack (depth a + 1 measured) versus O(1); it fails with RecursionError near 1,000 attempts.
Viva: What does loop-else do? Why does a blank not count? What is the bug with the counter?
