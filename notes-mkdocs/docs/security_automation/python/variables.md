---
tags:
  - Python
  - Computer Programming
---

A variable is a named container that holds a value. In Python, you don't declare a variable in advance — it is created the moment you assign a value to it using `=`.

## Creating Variables
```python
x = 42
switchName = "Cisco2960_south"

print(x)           # 42
print(switchName)  # Cisco2960_south
```

## Variables Have No Fixed Type
Unlike languages like Java or C, Python variables don't have a locked-in type. The same variable can hold an integer one moment and a string the next:
```python
x = 42              # x is an int
x = "Cisco2960"     # x is now a str — this is valid in Python
```

## Case Sensitivity
Variable names are case-sensitive, meaning `switchName`, `SWITCHNAME`, and `switchname` are three completely different variables. Best practice is to never rely on case differences to distinguish variables — use descriptive names instead:
```python
# Bad practice — confusing
switchname = "Cisco2960_east"
SWITCHNAME = "Cisco2960_west"

# Good practice — clear and distinct names
switchname_east = "Cisco2960_east"
switchname_west = "Cisco2960_west"
```

## Variable Naming Rules
- Can contain letters, numbers, and underscores (`_`)
- Cannot start with a number (`2device` is invalid, `device2` is fine)
- Cannot use Python reserved keywords (like `if`, `for`, `while`, `def`)
- Convention: use `snake_case` for variable names (e.g., `device_name`, `ip_address`)

## Multiple Assignment
Python lets you assign multiple variables in a single line:
```python
# Assign different values to multiple variables at once
x, y, z = "router", "switch", "firewall"
print(x)  # router
print(y)  # switch
print(z)  # firewall

# Assign the same value to multiple variables
switch1 = switch2 = switch3 = "Juniper"
```
> ⚠️ When assigning multiple values, the number of variables must match the number of values exactly, or Python will raise a ValueError.

## Unpacking a Collection
If you have a list or tuple, you can unpack its values directly into individual variables in one line:
```python
ip_addresses = ["172.20.200.10", "172.20.200.11", "172.20.200.12"]
ip1, ip2, ip3 = ip_addresses

print(ip1)  # 172.20.200.10
print(ip2)  # 172.20.200.11
print(ip3)  # 172.20.200.12
```

## Printing Variables
The `print()` function is the most common way to display output:
```python
ip1 = "10.100.200.30"
ip2 = "10.100.200.40"

# Comma-separated — print() adds a space between items automatically
print(ip1, ip2)

# Using + to concatenate strings (all items must be strings)
print("Primary IP: " + ip1)

# f-string (most flexible — can mix variables and text cleanly)
print(f"Primary: {ip1}, Secondary: {ip2}")
```