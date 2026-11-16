# Q3 – Vehicle Registration Number Validator (6 marks, K4)
Run: `python3 q3_complete_code.py` (portal template, TODO 1 and 2 filled; output equals the portal's expected output) and `python3 q3_plates.py`.
* TODO 1: `text.replace(" ", "").replace("-", "").upper()`. TODO 2: length 9 or 10, then `reg[:2].isalpha()`, `reg[2:4].isdigit()`, `reg[4:-4].isalpha()`, `reg[-4:].isdigit()`. Extra function `format_reg` gives `TN 09 AB 1234`.
* Six predictions (two rejected: three series letters, one-digit district) all matched.
* Immutability: `s[0] = 'T'` raises TypeError; `s.upper()` returns a NEW string, `s` is unchanged unless reassigned. `s[-4:]` is always the 4-digit number; `s[4:-4]` is the series (`'M'` for a 9-character, `'AB'` for a 10-character number).
* Trap found: `isdigit()` accepts full-width, Arabic and superscript digits, so the template accepts them; adding `reg.isascii()` fixes it. Tabs/newlines are not removed by `replace(" ", "")`.
* Alternative: `re.fullmatch(r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}", reg)` gave the same result on 50,000 random plates; both are O(L); slicing 0.185 µs vs regex 0.358 µs per plate. The regex is shorter and easier to change ({1,3}); slicing needs a new length test.
Viva: Why are strings immutable? What do `s[-4:]` and `s[4:-4]` return? Why is isdigit() risky?
