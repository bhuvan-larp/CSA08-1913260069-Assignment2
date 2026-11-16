# CSA08 – Python Programming – Assignment 2 (CO2)
**Control Flow, Strings and Functions (50 marks)**

| | |
|---|---|
| Name | **<YOUR NAME HERE>** |
| Register number | **<YOUR REGISTER NUMBER HERE>** |
| Python version | Python 3.12 (written and run with Python 3.12.3; `match-case` in Q1 needs 3.10 or later) |
| Libraries | Standard library only; `matplotlib==3.11.2` only for the optional Q7 flowchart picture (`requirements.txt`) |

## How to run (from inside the repository folder)
```
python3 Q1/q1_subsidy.py
python3 Q2/q2_otp.py
python3 Q3/q3_complete_code.py   &&  python3 Q3/q3_plates.py
python3 Q4/q4_complete_code.py   &&  python3 Q4/q4_statement.py
python3 Q5/q5_complete_code.py   &&  python3 Q5/q5_functions.py
python3 Q6/q6_complete_code.py   &&  python3 Q6/q6_recursion.py
python3 Q7/q7_redesign.py        &&  python3 Q7/q7_flowchart.py     # flowchart optional
```
On Windows use `python` or `py`. Each question folder has `output.txt` (real output), `answers.md` (explanations and viva questions) and `screenshots/`.

## Result notes
| Q | Result |
|---|---|
| Q1 | 8 predicted households agree with 5 correct implementations; the separate-if version gave two subsidies in 303 of 1,806 cases. |
| Q2 | while and for/range(3) agree with 5 predicted scenarios; blanks do not count; the wrong counter locks out a correct OTP; recursion depth a+1 vs 1 frame. |
| Q3 | Complete-the-code output equals the portal's; 6 predictions correct; isdigit() accepts non-ASCII digits; regex equals slicing on 50,000 plates. |
| Q4 | Output `same text: True | length: 3048890`; `+=` equals join in CPython 3.12 for one reference, 4× slower per doubling with a second reference. |
| Q5 | Output equals the portal's; `__defaults__` shows the shared list; three customers independent. |
| Q6 | Output equals the portal's (242785 and 26 calls); ways_memo(1000) raises RecursionError; loop 0.03 ms for n = 1,000. |
| Q7 | Recursion redesigned as a loop: 2,692,537 calls → 29 additions at n = 30; n = 100,000 in 66 ms. |

## Assumptions
Q1: FULL / PARTIAL decisions, senior case above 200 units = PARTIAL, "above 80" = age > 80. Q5: GST 5%. Q4: (c) is a list of f-string lines joined once. Q2: typing is scripted instead of input() for repeatable output. Timings differ from computer to computer; counts do not. The Q6 time for plain recursion at n = 1,000 is an ESTIMATE (it cannot be run), not a measurement.
