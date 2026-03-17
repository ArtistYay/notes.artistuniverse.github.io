---
tags:
  - Python
  - Computer Programming
---

Operators are symbols that perform actions on values and variables. Python groups them into several categories.

## Arithmetic Operators
Used for math calculations:

| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `+` | Addition | `3 + 5` | `8` |
| `-` | Subtraction | `7 - 2` | `5` |
| `*` | Multiplication | `4 * 6` | `24` |
| `/` | Division | `8 / 2` | `4.0` (always float) |
| `%` | Modulus | `10 % 3` | `1` (remainder only) |
| `//` | Floor Division | `15 // 4` | `3` (rounds down, drops decimal) |
| `**` | Exponentiation | `2 ** 3` | `8` (2 to the power of 3) |

**Modulus (`%`)** — Returns only the remainder after division. Useful for checking if a number is even or odd:
```python
print(10 % 2)   # 0  → even (no remainder)
print(10 % 3)   # 1  → 3 goes into 10 three times with 1 left over
```

**Floor Division (`//`)** — Divides and drops everything after the decimal point:
```python
print(15 // 4)  # 3  → would be 3.75, but floor division drops the .75
```

## Assignment Operators
Used to assign or update a variable's value. The shorthand versions (`+=`, `-=`, etc.) are very common in loops:

| Operator | Example | Same As |
|----------|---------|---------|
| `=` | `a = 12` | Set a to 12 |
| `+=` | `a += 7` | `a = a + 7` |
| `-=` | `a -= 7` | `a = a - 7` |
| `*=` | `a *= 7` | `a = a * 7` |
| `/=` | `a /= 7` | `a = a / 7` |
| `%=` | `a %= 7` | `a = a % 7` |
| `//=` | `a //= 7` | `a = a // 7` |
| `**=` | `a **= 7` | `a = a ** 7` |

```python
# Common use: incrementing a counter inside a loop
count = 0
count += 1   # same as count = count + 1
```

## Comparison Operators
Used to compare two values. The result is always a `bool` — either `True` or `False`:

| Operator | Meaning | Example |
|----------|---------|---------|
| `==` | Equal to | `x == 5` |
| `!=` | Not equal to | `x != 5` |
| `>` | Greater than | `x > 5` |
| `<` | Less than | `x < 5` |
| `>=` | Greater than or equal | `x >= 5` |
| `<=` | Less than or equal | `x <= 5` |

> ⚠️ A common mistake: using `=` (assignment) instead of `==` (comparison) inside an `if` statement will cause a SyntaxError or unexpected behavior.

## Logical Operators
Used to combine multiple conditions together:
```python
# and — BOTH conditions must be True for the whole thing to be True
if x > 0 and x < 10:
    print("x is between 0 and 10")

# or — AT LEAST ONE condition must be True
if x < 0 or x > 100:
    print("x is out of normal range")

# not — reverses/flips the condition
if not device_status == "online":
    print("Device is not online")
```

## Membership Operators
Used to check whether a value exists inside a collection (list, string, dictionary, set, etc.):
```python
devices = ["router", "switch", "firewall"]

if "router" in devices:
    print("Router found in list")       # This runs

if "printer" not in devices:
    print("Printer is not in the list") # This also runs
```

## Identity Operators
Used to check whether two variables point to the exact same object in memory — not just the same value:
```python
x = [1, 2, 3]
y = x           # y points to the SAME object as x

print(x is y)       # True  — same object in memory
print(x is not y)   # False

a = [1, 2, 3]
b = [1, 2, 3]       # a and b are separate objects with equal values

print(a is b)   # False — different objects, even though values match
print(a == b)   # True  — values are the same
```
> **Key rule:** Use `==` to compare values. Use `is` only when you specifically need to check if two variables reference the same object. `is not` is common for checking `if x is not None`.