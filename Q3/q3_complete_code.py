def normalise(text):
    """'tn 09 ab 1234' -> 'TN09AB1234' (spaces and hyphens removed, upper case)."""
    # TODO 1: Remove spaces and hyphens and convert to upper case using string methods
    return text.replace(" ", "").replace("-", "").upper()


def is_valid(reg):
    """Valid form: 2 letters, 2 digits, 1 or 2 letters, 4 digits (e.g. TN09AB1234)."""
    # TODO 2: Check the length is 9 or 10, then check each part using slicing with
    # isalpha() and isdigit()
    if len(reg) not in (9, 10):
        return False
    return reg[:2].isalpha() and reg[2:4].isdigit() and reg[4:-4].isalpha() and reg[-4:].isdigit()


def format_reg(reg):
    """Format a VALID normalised number as 'TN 09 AB 1234' (the extra function asked by the portal)."""
    return f"{reg[:2]} {reg[2:4]} {reg[4:-4]} {reg[-4:]}"


for raw in ["tn 09 ab 1234", "KA-01-M-0007", "TN9AB1234", "TN 22 1234 AB"]:
    reg = normalise(raw)
    print(f"{raw:15} -> {reg:11} {'valid' if is_valid(reg) else 'INVALID'}")

print()
for raw in ["tn 09 ab 1234", "KA-01-M-0007"]:
    reg = normalise(raw)
    if is_valid(reg):
        print(f"receipt format: {format_reg(reg)}")
