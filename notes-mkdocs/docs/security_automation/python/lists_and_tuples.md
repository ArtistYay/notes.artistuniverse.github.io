---
tags:
  - Python
  - Computer Programming
---

## Lists — Ordered and Changeable

A list is an ordered collection of items enclosed in square brackets `[]`. Lists can hold items of different data types, and their contents can be changed after creation (this is called **mutable**).

```python
my_list = [1, 2, 3, "four", 5.0]
devices  = ["Switch1", "Router2", "Firewall3"]
```

## Accessing Items — Indexing
Every item in a list has a position number called an **index**. Indexing starts at `0` (not 1):
```python
devices = ["Switch1", "Router2", "Firewall3"]

print(devices[0])    # Switch1   — first item
print(devices[1])    # Router2   — second item
print(devices[-1])   # Firewall3 — last item (negative counts from end)
print(devices[-2])   # Router2   — second to last
```

## Slicing — Accessing a Range of Items
Slicing extracts a portion of a list. The syntax is `list[start:stop]`. The `stop` index is **not** included:
```python
devices = ["A", "B", "C", "D", "E"]

print(devices[1:3])   # ['B', 'C']       — index 1 up to (not including) 3
print(devices[:2])    # ['A', 'B']       — from start to index 2
print(devices[2:])    # ['C', 'D', 'E']  — from index 2 to the end
print(devices[:])     # ['A', 'B', 'C', 'D', 'E'] — full copy of the list
```

## Modifying a List
Because lists are mutable, you can change, add, or remove items after creation:
```python
devices = ["Switch1", "Router2", "Firewall3"]

# Change a single item by index
devices[1] = "Router_A"
# devices is now ['Switch1', 'Router_A', 'Firewall3']

# Change a range of items using slicing
statuses = ["up", "down", "up", "up", "down"]
statuses[1:3] = ["up", "up"]
# statuses is now ['up', 'up', 'up', 'up', 'down']
```

## Common List Methods
These are built-in actions you can perform on a list:
```python
devices = ["Switch1", "Router2"]

devices.append("Firewall3")         # Add one item to the end
devices.insert(1, "Switch2")        # Insert at a specific index (shifts others right)
devices.remove("Router2")           # Remove the first occurrence of this value
devices.pop()                       # Remove and return the last item
devices.pop(0)                      # Remove and return item at index 0
devices.sort()                      # Sort alphabetically/numerically in place
devices.reverse()                   # Reverse the order in place
print(len(devices))                 # Number of items in the list
print("Switch1" in devices)         # True or False — membership check
```

## List Constructor
You can create a list explicitly using `list()`:
```python
ip_list = list(("192.168.1.1", "192.168.1.2", "192.168.1.3"))
```

---

## Tuples — Ordered but Unchangeable

A tuple looks like a list but uses parentheses `()`. The key difference: tuples are **immutable** — once created, their contents cannot be modified. This makes them useful for storing data that should stay fixed (like device credentials or fixed configuration values).

```python
# Create a tuple
device_info = ("Router1", "192.168.1.1", "Cisco")

# Access by index — same as lists
print(device_info[0])    # Router1
print(device_info[-1])   # Cisco

# Trying to change a tuple will cause a TypeError
# device_info[0] = "Switch1"  ← This will crash
```

**When to use a Tuple vs. a List:**
- Use a **list** when data needs to be updated — adding devices, changing statuses, tracking errors
- Use a **tuple** when data should stay constant — IP/credential pairs, fixed config templates