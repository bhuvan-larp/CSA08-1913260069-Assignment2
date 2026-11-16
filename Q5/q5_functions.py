"""Q5 - Functions, Parameters and Scope: College Canteen Order System."""
import time
import tracemalloc

GST_RATE = 0.05                      # assumption: 5 % GST on the canteen bill
PRICES = {"Tea": 12, "Vada": 10, "Dosa": 40, "Coffee": 15, "Samosa": 12}


def add_item_buggy(item, order=[]):
    order.append(item)
    return order


def add_item(item, order=None):
    if order is None:
        order = []
    order.append(item)
    return order


def bill(order, gst_rate=GST_RATE, *, round_to=2):
    """Positional: order. Default: gst_rate. Keyword-only: round_to. Returns TWO values (total, gst) as a tuple."""
    subtotal = sum(PRICES[i] for i in order)
    gst = round(subtotal * gst_rate, round_to)
    return round(subtotal + gst, round_to), gst


print("=== PART A: the bug - a default value is created ONCE, when the function is defined ===")
print("Before any call: add_item_buggy.__defaults__ =", add_item_buggy.__defaults__)
c1 = add_item_buggy("Tea")
print("customer 1 orders Tea   ->", c1, "| __defaults__ =", add_item_buggy.__defaults__)
c2 = add_item_buggy("Vada")
print("customer 2 orders Vada  ->", c2, "| __defaults__ =", add_item_buggy.__defaults__)
print("c1 is c2 (same list object)?", c1 is c2, "| id(c1) =", id(c1), "id(c2) =", id(c2))
print("The default list [] was created once at 'def' time and stored in __defaults__; every call without an order reuses that SAME list,")
print("so customer 2 sees customer 1's items. Mutable defaults (list, dict, set) are shared; immutable defaults (None, numbers, strings) are safe.")

print("\n=== PART B: the corrected design, tested with three customers in sequence ===")
orders = []
for customer, items in [("Anil", ["Tea", "Vada"]), ("Banu", ["Dosa"]), ("Chitra", ["Coffee", "Samosa", "Tea"])]:
    order = None                                 # each customer starts with NO order object
    for it in items:
        order = add_item(it, order)              # the first call creates a fresh list, later calls extend it
    orders.append((customer, order))
for customer, order in orders:
    total, gst = bill(order)
    print(f"{customer:7} order = {order}  subtotal+GST total = {total}, GST = {gst}")
print("three different list objects:", len({id(o) for _, o in orders}) == 3)
print("PREDICTED lists: ['Tea', 'Vada'], ['Dosa'], ['Coffee', 'Samosa', 'Tea'] ->", [o for _, o in orders] == [["Tea", "Vada"], ["Dosa"], ["Coffee", "Samosa", "Tea"]])
print("hand check Anil: Tea 12 + Vada 10 = 22; GST 5% = 1.1; total = 23.1 ->", bill(["Tea", "Vada"]))
print("independent after the buggy-free calls: add_item('Tea') =", add_item("Tea"), "| add_item('Vada') =", add_item("Vada"))

print("\n=== PART C: positional, keyword and default parameters ===")
print("positional : bill(['Tea','Vada'])               ->", bill(["Tea", "Vada"]))
print("default    : the gst_rate=0.05 above is used when it is not given")
print("keyword    : bill(['Tea','Vada'], gst_rate=0.18)  ->", bill(["Tea", "Vada"], gst_rate=0.18))
print("keyword-only: bill(['Tea','Vada'], round_to=0)   ->", bill(["Tea", "Vada"], round_to=0))
try:
    bill(["Tea"], 0.05, 3)
except TypeError as e:
    print("round_to given by position fails            ->", type(e).__name__ + ":", e)
print("Use positional for the 1-2 obvious arguments, keyword when the meaning is not obvious or many options exist, defaults for optional settings.")

print("\n=== PART D: returning more than one value ===")
total, gst = bill(["Dosa", "Coffee"])
print("total, gst = bill(['Dosa','Coffee']) ->", total, gst, "| the function returns ONE tuple:", type(bill(["Dosa"])).__name__, bill(["Dosa"]))
print("hand check: 40 + 15 = 55; GST = 2.75; total = 57.75 ->", (total, gst) == (57.75, 2.75))

print("\n=== PART E: local, global and nonlocal ===")
x = "global x"


def local_demo():
    x = "local x"                                   # a NEW local name; the global x is untouched
    return x


def read_global_demo():
    return x                                         # reading a global needs no keyword


def global_demo():
    global x
    x = "changed by global_demo"                     # without 'global' this would create a local x instead


def unbound_demo():
    try:
        print(x)                                     # x is assigned below, so x is LOCAL in the whole function
        x = "later"
    except UnboundLocalError as e:
        return type(e).__name__ + ": " + str(e)


print("local_demo() ->", local_demo(), "| global x after it:", x)
print("read_global_demo() ->", read_global_demo())
global_demo()
print("after global_demo(): x =", x)
print("unbound_demo() ->", unbound_demo())


def outer():
    count = 0
    def inner_wrong():
        count = 99                                   # new local name, outer count unchanged
        return count
    def inner_right():
        nonlocal count                               # rebinds the variable of the ENCLOSING function
        count += 1
        return count
    inner_wrong()
    a = inner_right()
    b = inner_right()
    return count, a, b


print("outer(): (count, first call, second call) =", outer(), " -> nonlocal changed the enclosing count; inner_wrong did not")
print("Why 'global' is needed: assigning to a name inside a function makes it local by default; 'global' says use the module-level name.")
print("Why it is usually avoided: any function can change it, so bugs are hard to trace, functions cannot be tested alone, and the")
print("order of calls changes results. Pass values in as arguments and return results instead.")
counter = 0


def bad_total(price):
    global counter
    counter += price
    return counter


print("global-counter style: bad_total(10) =", bad_total(10), ", bad_total(10) =", bad_total(10), "(same call, different answers)")
print("pure style: bill(['Tea']) =", bill(["Tea"]), ", bill(['Tea']) =", bill(["Tea"]), "(same call, same answer)")

print("\n=== PART F: alternatives - order passed explicitly, or kept in a closure ===")


def add_explicit(item, order):                       # design 2: the caller must always supply the list
    order.append(item)
    return order


def make_order():                                    # design 3: closure - the list lives in the enclosing function
    order = []

    def add(item):
        order.append(item)

    def get():
        return list(order)
    return add, get


add1, get1 = make_order()
add2, get2 = make_order()
add1("Tea"); add1("Vada"); add1("Coffee"); add2("Dosa"); add2("Samosa")
print("closure customer 1 ->", get1(), "| closure customer 2 ->", get2(), "(independent: each call of make_order() makes a new list)")
print("the list is hidden inside the closure cell:", [c.cell_contents for c in add1.__closure__])


def run_default(n):
    o = None
    for i in range(n):
        o = add_item(i, o)


def run_explicit(n):
    o = []
    for i in range(n):
        add_explicit(i, o)


def run_closure(n):
    add, get = make_order()
    for i in range(n):
        add(i)


N = 200_000
print(f"{'design':22} {'time per item (us)':>20} {'peak memory (MB) for 200,000 items':>36}")
for name, fn in [("default None", run_default), ("explicit list", run_explicit), ("closure", run_closure)]:
    best = float("inf")
    for _ in range(3):
        t = time.perf_counter()
        fn(N)
        best = min(best, time.perf_counter() - t)
    tracemalloc.start()
    fn(N)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"{name:22} {best / N * 1e6:>20.3f} {peak / 1e6:>36.3f}")
print("Time: adding one item is one list.append in every design -> O(1) per item (the three rows are within a small constant of each other).")
print("Space per customer: the n items are stored once = O(n) in every design (same peak memory). Extra: default-None and explicit add O(1);")
print("the closure adds one function object and one cell (O(1)) per customer and hides the list, so callers cannot change it by accident.")
