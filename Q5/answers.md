# Q5 – Functions, Parameters and Scope (7 marks, K4)
Run: `python3 q5_complete_code.py` (TODO 1 filled; output equals the portal's expected output, then prints `(['Tea', 'Vada'],)`) and `python3 q5_functions.py`.
* The bug: the default `[]` is created once when `def` runs and is stored in `add_item_buggy.__defaults__`; every call without `order` appends to that same list (`__defaults__` grows to `(['Tea', 'Vada'],)`; `c1 is c2` is True).
* Fix: `order=None`, create `[]` inside the function. Tested with three customers: each order is a different list object.
* Parameters: positional for the obvious ones, keyword for meaning/options, defaults for optional settings, keyword-only (`*`) to force a name. Return several values with a tuple: `total, gst = bill(order)` (GST 5% is my assumption).
* Scope: assignment makes a name local; `global` is needed to rebind a module-level name; `nonlocal` rebinds the enclosing function's variable; reading a global needs nothing; assigning after reading raises UnboundLocalError. Globals are avoided because any function can change them (same call, different answers).
* Alternatives: explicit list passed by the caller, or a closure `make_order()` that hides the list. All three: O(1) per item (0.04 µs), same peak memory (8.0 MB for 200,000 items); closure adds one function and one cell per customer.
Viva: When is a default value created? Why is None used? What does nonlocal do?
