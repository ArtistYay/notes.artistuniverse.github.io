---
tags:
  - Python
  - Computer Programming
---

A function is a named, reusable block of code. Instead of copying the same logic in multiple places, you define it once and call it whenever you need it.

## Defining and Calling a Function
Use the `def` keyword, followed by a name, parentheses, and a colon. The function body is indented below:
```python
# Define the function
def greet():
    print("Hello, Network Engineer!")

# Call the function
greet()   # → Hello, Network Engineer!
```

## Functions with Parameters
Parameters are the variables listed in the function definition. They act as placeholders — when you call the function, you pass in the actual values (called arguments):
```python
def add_device(network_devices, device):
    network_devices.add(device)
    return network_devices

# Call with arguments
my_devices = {"Switch", "Router", "Firewall"}
my_devices = add_device(my_devices, "Load Balancer")
# my_devices now contains "Load Balancer" too
```

The key insight: parameters are flexible. The function doesn't care which specific variable you pass — it just works on whatever is given to it. This is what makes functions reusable:
```python
def configure_devices(device_list):
    for device in device_list:
        print(f"Configuring {device}")

routers = ["Router1", "Router2"]
switches = ["Switch1", "Switch2"]

configure_devices(routers)    # works on routers
configure_devices(switches)   # same function, different data
```

## Returning a Value
The `return` statement sends a result back to wherever the function was called. Without `return`, the function returns `None` by default:
```python
def count_devices(network_devices):
    return len(network_devices)

devices = ["Switch", "Router", "Firewall"]
count = count_devices(devices)
print(count)  # 3
```

## Default Parameter Values
You can set a default value for a parameter. If the caller doesn't provide that argument, the default is used:
```python
def connect(ip, port=22):
    print(f"Connecting to {ip} on port {port}")

connect("192.168.1.1")          # Uses default: port 22
connect("192.168.1.1", 8080)    # Overrides default: port 8080
```

## `pass` — Placeholder for Empty Functions
If you need to define a function but aren't ready to write the body yet, use `pass` to avoid a SyntaxError:
```python
def my_function():
    pass    # valid empty function — does nothing
```

## Why Functions Matter
- **Reusability** — Write the logic once, use it anywhere
- **Readability** — A meaningful function name explains what the code does without reading every line
- **Modularity** — Break large problems into small, focused pieces
- **Less repetition** — Change the logic in one place instead of hunting it down everywhere