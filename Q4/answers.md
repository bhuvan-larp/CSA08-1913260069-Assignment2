# Q4 – Building Long Text: + or join()? (6 marks, K4)
Run: `python3 q4_complete_code.py` (TODO 1 filled: `";".join(parts) + ";"`; output `same text: True | length: 3048890`) and `python3 q4_statement.py`.
* Prediction: join and f-string+join are O(n); `+=` looks O(n²) because strings are immutable (each `+=` should copy the text built so far).
* Measured (best of 3): 1,000 / 10,000 / 200,000 lines: `+=` 0.00005 / 0.00044 / 0.00855 s; join 0.00003 / 0.00032 / 0.01172 s. In CPython 3.12 a `+=` on a local string with ONE reference is resized in place, so it was as fast as join (the prediction "might only be a constant factor" was right).
* When the optimisation cannot apply (a second reference to the string) the quadratic cost appears: 5,000 → 40,000 lines took 0.0034 → 0.2658 s; doubling the lines makes it about 4× slower.
* Three runs of the complete-code program: average `+=` time 0.0101 s, join 0.0041 s.
* Why join stays the recommended practice: it is O(n) in every Python implementation (PyPy, Jython) and in every situation; the `+=` speed depends on an implementation detail that disappears with a second reference, an attribute or a list element.
* Alternative: `io.StringIO` (O(n), one growing buffer, 6.9 MB peak) and writing line by line to a file (O(n) time, O(1) memory, 0.03 MB peak but slower per line); join needed the most memory (15.9 MB peak: list of parts plus final text).
Viva: Why is `+=` O(n²) in theory? Why was it fast in your test? Which method for a 1 GB statement?
