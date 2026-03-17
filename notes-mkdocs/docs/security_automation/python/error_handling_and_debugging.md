---
tags:
  - Python
  - Computer Programming
---

## The Three Types of Python Errors

**Syntax Errors** — The code is grammatically wrong. Python can't even parse it, so it won't run at all. The error message tells you exactly which line:
```python
# ❌ Missing colon
if x > 5
    print("yes")

# ❌ Wrong bracket type
my_set = {1, 2, 3]    # opened with { but closed with ]

# ❌ Misspelled keyword
whille i < 5:         # 'while' is spelled wrong
```

**Runtime Errors** — The syntax is valid, but something goes wrong while the code is running. Common examples: dividing by zero, trying to access a file that doesn't exist, using a key that isn't in a dictionary:
```python
x = 10 / 0                      # ZeroDivisionError
file = open("missing_file.txt") # FileNotFoundError
value = my_dict["bad_key"]      # KeyError
```

**Logic Errors (Semantic Errors)** — The most frustrating type. The code runs without crashing, but it gives the wrong result. Python can't catch these — you have to find them yourself through testing and careful review:
```python
# ❌ Off-by-one error — runs 11 times (0-10) instead of 10
for i in range(11):
    print(i)

# ❌ Wrong comparison operator
if bandwidth > 100:      # "low bandwidth" check should use < not >
    print("Low bandwidth")

# ❌ Assignment instead of comparison inside a condition
if x = 2:                # Should be == not =
    print("x is 2")
```

## Debugging Techniques

**1. Print Statements** — The simplest debugging tool. Add `print()` calls to check variable values at different points in your code:
```python
def calculate_average(values):
    print(f"Input received: {values}")    # check what came in
    total = sum(values)
    print(f"Total: {total}")              # check intermediate result
    return total / len(values)
```

**2. Read the Error Message** — Python's error messages tell you the file, line number, and type of error. Read them carefully before guessing.

**3. Comment Out Code** — Temporarily disable sections to isolate which part is causing the problem.

**4. Use Python's Built-in Debugger (`pdb`)** — Lets you step through code line by line and inspect variables:
```python
import pdb
pdb.set_trace()   # execution pauses here so you can inspect
```

## `try` / `except` — Handling Errors Gracefully
Instead of letting your script crash when something goes wrong, wrap risky code in a `try` block. If an error occurs, the `except` block runs instead:

```python
# Basic structure
try:
    x = 1 / 0               # Code that might cause an error
except ZeroDivisionError:
    x = 0                   # What to do when that specific error occurs
    print("Cannot divide by zero — setting x to 0")
```

You can catch multiple exception types separately:
```python
try:
    result = 10 / num_devices
except ZeroDivisionError:
    print("Error: num_devices is zero")
except TypeError:
    print("Error: num_devices is not a number")
```

Catch any exception (use sparingly — being specific is better practice):
```python
try:
    result = 10 / 0
except Exception as e:
    print(f"An error occurred: {e}")
```

Network automation example — prevent one bad device from stopping the whole script:
```python
def connect_to_device(device):
    try:
        if device == "bad_device":
            raise ConnectionError("Cannot connect")
        print(f"Connected to {device}")
    except ConnectionError as e:
        print(f"Skipping {device} — connection failed: {e}")

devices = ["Router1", "bad_device", "Switch1"]
for device in devices:
    connect_to_device(device)
# Router1 connects, bad_device is skipped, Switch1 connects
```

## Input Validation
Always validate data before using it — bad input early causes confusing errors later:
```python
# Check that the input is the right type
def connect(ip, username, password):
    if not isinstance(ip, str) or not isinstance(username, str):
        raise TypeError("IP and username must be strings")

# Check that a value is in a valid range (valid IP octet: 0-255)
def validate_ip(ip_address):
    parts = ip_address.split(".")
    if len(parts) != 4 or not all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
        raise ValueError(f"Invalid IP address: {ip_address}")

# Check that required parameters are not missing
def connect(ip=None, username=None, password=None):
    if ip is None or username is None or password is None:
        raise ValueError("IP address, username, and password are all required")

# Check minimum length
def validate_password(password):
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
```