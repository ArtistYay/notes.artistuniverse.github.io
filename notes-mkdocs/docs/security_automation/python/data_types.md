---
tags:
  - Python
  - Computer Programming
---

A data type tells Python what kind of value a variable holds and what operations can be performed on it. Python determines the type automatically based on the value you assign — this is called **dynamic typing**.

### Overview of Core Data Types

| Type | Example | Description |
|------|---------|-------------|
| `int` | `x = 5` | Whole numbers, positive or negative |
| `float` | `y = 3.14` | Decimal/floating-point numbers |
| `str` | `s = "hello"` | Text — any characters in quotes |
| `bool` | `b = True` | Only two values: `True` or `False` |
| `list` | `l = [1, 2, 3]` | Ordered collection, can be changed |
| `tuple` | `t = (1, 2, 3)` | Ordered collection, cannot be changed |
| `dict` | `d = {"key": "val"}` | Key-value pairs for fast lookups |
| `set` | `s = {1, 2, 3}` | Unordered, only stores unique values |
| `NoneType` | `x = None` | Represents the absence of a value |

### Numeric Types
```python
x = 5       # int — whole number
y = 3.14    # float — decimal number
```

### String Type
Strings store text. You can use single or double quotes — both work the same way:
```python
message = "Hello, Network Engineer!"
device = 'Cisco2960_south'
# Both are valid str types
```

### Boolean Type
Booleans can only be `True` or `False` (capital first letter required). They are the result of comparisons and are used in conditions:
```python
is_online = True
is_configured = False
```

### Sequence Types
```python
my_list  = [1, 2, 3]    # list — ordered and changeable
my_tuple = (1, 2, 3)    # tuple — ordered but cannot be changed
my_range = range(5)     # range — represents a sequence of numbers (0,1,2,3,4)
```

### NoneType
`None` is used to represent "nothing" or "no value". It is commonly used as a default or placeholder:
```python
result = None   # No value yet — will be assigned later
```

### Checking a Variable's Type
```python
x = 42
print(type(x))       # <class 'int'>

name = "Router1"
print(type(name))    # <class 'str'>
```

### Explicitly Setting a Type (Type Casting)
Sometimes you need to force a value into a specific type. This is called type casting:
```python
variableName = str("This is a string")
variableName = int(42)
variableName = list(("192.168.1.100", "192.168.1.101", "192.168.1.102"))
variableName = tuple(("192.168.1.100", "192.168.1.101", "192.168.1.102"))
variableName = dict(routerName="Cisco5501", ip="10.200.30.254")
variableName = set(("192.168.1.100", "192.168.1.101", "192.168.1.102"))
```
A common use case is converting a number to a string so you can concatenate it with text:
```python
port_number = 8080
message = "Connecting on port " + str(port_number)
```