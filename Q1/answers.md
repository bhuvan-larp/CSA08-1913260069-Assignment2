# Q1 – Decisions with Many Boundaries (6 marks, K4)
Run: `python3 q1_subsidy.py` (output in `output.txt`).
* Assumptions: ≤100 units = FULL subsidy; 101–200 with ration card = PARTIAL; above 200 with a member above 80 = PARTIAL (the portal does not say how much); "above 80" means age > 80.
* Predictions for 8 households (100, 101, 200, 201 units, age 80/81, 60 units with ration card) were written in the program before running; all 5 correct versions matched all 8.
* Separate `if`s are all tested independently, so more than one can be True: the buggy rule `units <= 200 and ration_card` has no lower bound, so ration-card houses with 0–100 units got FULL **and** PARTIAL (303 of 1,806 tested cases). `if-elif-else` runs only the first True branch.
* Design decision: if-elif-else with chained comparison (`101 <= units <= 200`): one line per slab, one number to edit per limit. Nested if hides the tests; combined Boolean repeats `units`.
* Alternative: match-case (guards) behaves like if-elif, O(k) per decision for k slabs; a slab table searched in a loop is O(k) time, O(k) data (measured 0.207 µs at k = 3 → 109.0 µs at k = 3000); bisect on a sorted table is O(log k) (about 0.11 µs).
Viva: Why can separate ifs give two results? What does `101 <= x <= 200` mean? When would you use a table instead of if-elif?
