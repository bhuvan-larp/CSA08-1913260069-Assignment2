# Q7 – Diagnose, Redesign and Validate (13 marks, K5)
Run: `python3 q7_redesign.py` (output in `output.txt`); flowchart `q7_flowchart.png` (`python3 q7_flowchart.py`, needs matplotlib).
Chosen program: the plain recursive `ways_naive` from Q6.
* **A Diagnose (2):** for n = 25 there are 242,785 calls for only 26 different sub-questions (each asked 9,338 times on average); 50% of all calls are the base cases ways(1)/ways(0) (ways(1) alone 75,025 times); calls grow 1.618× per step (11.09× per 5 steps).
* **B Objective (2):** for n = 30 cut calls from 2,692,537 to ≤ 31 (85,000× fewer) and time from 0.1 s to < 0.01 ms; also work for n = 1,000 and 100,000 with no RecursionError and O(1) extra memory.
* **C Design (4):** bottom-up loop that keeps the last two values (own design; no lru_cache or library shortcut). Uses overlapping sub-problems and "depends only on the previous two". Trade-off: no sharing between queries → many queries use a table (O(n) memory). Pseudocode and flowchart included.
* **D Prediction (1):** additions = n − 1; ≥ 10⁴ speed-up at n = 30; printing ways(1..1000): 499,500 additions separately vs 999 with one table.
* **E Validate (2):** n = 10/20/25/30 counts 177 → 9, 21,891 → 19, 242,785 → 24, 2,692,537 → 29 (equal to the prediction); times 0.122835 s → 0.00000076 s at n = 30 (about 161,600×); all answers equal the original for n = 0..30; n = 100,000 in 66 ms.
* **F Defend (2):** objective achieved. New costs: no shared cache; big-number additions are not constant time. The original is still preferable as the clearest copy of the definition and for n ≤ ~20, and it is kept as the test oracle.
