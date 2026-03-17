---
tags:
  - Python
  - Computer Programming
---

Loops let you repeat a block of code multiple times without rewriting it. Python has two types: `for` and `while`.

## `for` Loop — Iterate Over a Collection
A `for` loop goes through each item in a sequence one at a time. Think of it as "for each item in this collection, do something":
```python
devices = ["router", "switch", "firewall"]

for device in devices:
    print(device)
# Output: router, switch, firewall (each on its own line)
```

## `for` Loop with `range()`
`range()` generates a sequence of numbers. It is commonly used when you need to loop a specific number of times:
```python
for i in range(5):        # 0, 1, 2, 3, 4  (starts at 0 by default)
    print(i)

for i in range(1, 6):     # 1, 2, 3, 4, 5  (start, stop — stop is excluded)
    print(i)

for i in range(0, 10, 2): # 0, 2, 4, 6, 8  (start, stop, step)
    print(i)
```

## `for` Loop — Network Example
```python
# Generate all IP addresses in the 192.168.1.0/24 subnet
subnet = "192.168.1."
ip_addresses = [subnet + str(i) for i in range(1, 256)]

for ip in ip_addresses:
    print(ip)
```

## `while` Loop — Repeat While a Condition is True
A `while` loop keeps running as long as its condition evaluates to `True`. It is useful when you don't know in advance how many times you need to loop:
```python
i = 0
while i < 5:
    print(i)
    i += 1    # Always increment the counter, or the loop runs forever!
```
> ⚠️ Always make sure something inside the loop will eventually make the condition `False`. If the condition never becomes `False`, you get an **infinite loop** that hangs your program.

## `while` Loop — Network Example
```python
subnet = "192.168.1."
ip_addresses = []
i = 1

while i < 256:
    ip_addresses.append(subnet + str(i))
    i += 1   # increment keeps the loop from running forever
```

## `break` — Exit the Loop Early
`break` immediately stops the loop and jumps past it, even if the condition is still `True`:
```python
i = 1
while True:             # infinite loop — runs forever on its own
    if i > 255:
        break           # but break exits when i exceeds 255
    ip_addresses.append("192.168.1." + str(i))
    i += 1
```

## `continue` — Skip the Current Iteration
`continue` skips the rest of the current iteration and jumps directly to the next one:
```python
for i in range(1, 256):
    if i == 100:
        continue        # skip 192.168.1.100 — go straight to 101
    print("192.168.1." + str(i))
```