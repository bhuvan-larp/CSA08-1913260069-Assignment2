# Q6 – Recursion and Its Limits (8 marks, K5)
Run: `python3 q6_complete_code.py` (TODO 1 filled; output equals the portal's expected `naive: 121393 calls = 242785` and `memo : 121393 calls = 26`, then the RecursionError for 1000) and `python3 q6_recursion.py`.
* Base case `n <= 1 → 1`; recursive case `ways(n) = ways(n-1) + ways(n-2)` (the last move was 1 or 2 steps). Hand values n = 1..6: 1, 2, 3, 5, 8, 13 – all matched.
* Call tree for n = 5 has 15 calls; ways(3) is computed 2 times, ways(2) 3 times, ways(1) 5 times: the same sub-question is repeated.
* Calls: naive = 2·ways(n) − 1 (177, 21,891, 242,785, 2,692,537 for n = 10, 20, 25, 30 – prediction matched) growing 1.618× per step; memoised = n + 1 (11, 21, 26, 31).
* `ways_memo(1000)` → RecursionError: the first call recurses 1,000 deep before anything is cached and the default limit is 1,000. Raising the limit to 5,000 made it work (209 digits), but the lru_cache version failed again at n = 5,000 even with a raised limit, while a plain dictionary memo kept working.
* Plain recursion for n = 1,000 was NOT run: about 6.43e201 seconds (an ESTIMATE from measured speed). Memo (limit raised) 0.32 ms, loop 0.04 ms for n = 1,000.
* Decision: loop for production (O(n) time, O(1) space, no limit); memoised recursion kept as the readable specification and for tests.
Viva: Why does plain recursion repeat work? What does lru_cache do? Why is the loop O(1) space?
