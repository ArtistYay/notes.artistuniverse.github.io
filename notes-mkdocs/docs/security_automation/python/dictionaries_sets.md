---
tags:
  - Python
  - Computer Programming
---

## Dictionaries — Key-Value Pairs

A dictionary stores data as **key-value pairs** using curly braces `{}` with colons `:` separating keys from values. Dictionaries are ideal when you need to quickly look up a value by a label rather than by position.

- Keys must be unique
- Values can be any data type, including other dictionaries or lists
- Dictionaries are mutable. you can add, update, or remove pairs

```python
network_devices = {
    "Router1":   "192.168.1.1",
    "Switch1":   "10.0.0.1",
    "Firewall1": "172.16.0.1",
}
```

## Accessing Values
Use the key in square brackets to get the corresponding value:
```python
router_ip = network_devices["Router1"]   # "192.168.1.1"
```

If you try to access a key that doesn't exist, Python raises a `KeyError`. To avoid this, use `.get()`, which returns `None` (or a default you specify) instead of crashing:
```python
ip = network_devices.get("Router1")               # "192.168.1.1"
ip = network_devices.get("NonExistent")            # None — no error
ip = network_devices.get("NonExistent", "unknown") # "unknown" as fallback
```

## Adding and Updating Items
```python
# Add a new key-value pair
network_devices["Switch2"] = "10.0.0.2"

# Update an existing value
network_devices["Router1"] = "192.168.1.10"

# Update multiple items at once using .update()
updates = {"model": "Cisco 3850", "os_version": "15.2"}
device_info.update(updates)
# If a key already exists, its value is overwritten. New keys are added.
```

## Removing Items
```python
del network_devices["Switch1"]              # Delete a key-value pair
value = network_devices.pop("Router1")      # Remove and return the value
```

## Looping Through a Dictionary
```python
device_info = {"hostname": "switch1", "ip": "192.168.1.1", "model": "Cisco 3750"}

for key in device_info:                      # loops through keys only
    print(key)

for key, value in device_info.items():       # loops through both key and value
    print(f"{key}: {value}")

for value in device_info.values():           # loops through values only
    print(value)
```

## Dictionary Constructor
You can build a dictionary from a list of tuples using `dict()`:
```python
device_list = [("Router1", "192.168.1.1"), ("Switch1", "10.0.0.1")]
network_devices = dict(device_list)
# Result: {'Router1': '192.168.1.1', 'Switch1': '10.0.0.1'}
```

## Nested Dictionary
Dictionaries can hold any data type as a value, including other dictionaries:
```python
mixed = {
    "integer_key":     42,
    "string_key":      "hello",
    "list_key":        [1, 2, 3],
    "nested_dict_key": {"nested_key": "value"},
}
```

---

## Sets — Unordered and Unique

A set also uses curly braces `{}`, but has **no key-value pairs** — it's just a collection of individual values. The defining feature of a set is that it **automatically removes duplicates** and has **no guaranteed order**.

Sets are perfect when you need to store unique items or quickly check membership.

```python
vlans = {10, 20, 30, 40}
network_devices = {"Switch", "Router", "Firewall"}
```

### Creating a Set from a List (Removing Duplicates)
This is one of the most common uses of sets — instantly deduplicate a list:
```python
access_log = ["alice", "bob", "alice", "charlie", "bob", "alice"]
unique_users = set(access_log)
# Result: {'alice', 'bob', 'charlie'} — duplicates are gone automatically
```

## Modifying Sets
```python
devices = {"Switch", "Router"}

devices.add("Firewall")                           # Add one item
devices.update(["Load Balancer", "Proxy Server"]) # Add multiple items

devices.remove("Router")    # Remove item — raises KeyError if not found
devices.discard("Router")   # Remove item — no error if not found (safer)
```

## Set Operations
Sets support mathematical set operations, which are very useful for comparing data:
```python
set_a = {"Router", "Switch", "Firewall"}
set_b = {"Switch", "Firewall", "Load Balancer"}

print(set_a | set_b)   # Union:        all items from both sets
                       # {'Router', 'Switch', 'Firewall', 'Load Balancer'}

print(set_a & set_b)   # Intersection: only items that are in BOTH sets
                       # {'Switch', 'Firewall'}

print(set_a - set_b)   # Difference:   items in A but NOT in B
                       # {'Router'}
```