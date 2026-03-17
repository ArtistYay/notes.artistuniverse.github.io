---
tags:
  - Python
  - Computer Programming
---

`if/else` statements let your code make decisions. Python evaluates a condition — if it is `True`, one block of code runs; if it is `False`, a different block runs.

## Basic `if` / `else`
```python
device_status = "online"

if device_status == "online":
    print("Device is online. Proceed with configuration.")
else:
    print("Device is offline. Unable to perform configuration.")
```

## Adding `elif` for Multiple Conditions
`elif` stands for "else if." It lets you chain multiple conditions. Python checks each one from top to bottom and executes only the first one that is `True`:
```python
x = 20

if x < 10:
    print("x is less than 10")
elif x < 30:
    print("x is less than 30 but not less than 10")
else:
    print("x is 30 or more")
```
- You can have as many `elif` blocks as you need.
- The `else` at the end is a "catch-all" — it runs only if none of the conditions above were `True`.
- Both `elif` and `else` are optional. A lone `if` is valid on its own.

## Real-World Example — Classify an IP Address
```python
ip_address = "192.168.1.1"

if ip_address.startswith("192.168"):
    print(f"{ip_address} is private — 192.168.0.0/16 range")
elif ip_address.startswith("10"):
    print(f"{ip_address} is private — 10.0.0.0/8 range")
elif ip_address.startswith("172.16"):
    print(f"{ip_address} is private — 172.16.0.0/12 range")
else:
    print(f"{ip_address} is not a private IP address")
```

## Indentation — How Python Defines Code Blocks
Python does not use curly braces `{}` like many other languages. Instead, it uses **indentation** (4 spaces per level) to define which lines belong to which block. This is strict — incorrect indentation is a syntax error:
```python
x = 10

if x > 5:
    print("Inside the if block")      # indented → belongs to the if
    print("Still inside the block")   # indented → also belongs to the if

print("Outside the if block")         # NOT indented → always runs
```

**Example of what breaks:**
```python
# ❌ This causes an IndentationError
if x > 5:
print("x is greater than 5")   # must be indented!
```