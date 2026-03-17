---
tags:
  - Python
  - Computer Programming
---

## Key Terms
Understanding the vocabulary helps you know what you're importing and why:

- **Script** — A `.py` file you run to automate a task
- **Module** — A `.py` file containing reusable functions, classes, or variables that other scripts can import
- **Package** — A folder (directory) containing multiple related modules, installed via `pip`
- **Library** — A broad term for a collection of modules that extend what Python can do

## Importing a Module
```python
# Import the entire module — access functions with module.function()
import math
result = math.sqrt(16)       # 4.0

# Import only a specific function — use it directly without the prefix
from math import sqrt
result = sqrt(16)

# Import with an alias — useful for long module names
import math as m
result = m.sqrt(16)
```

## Listing What's Available in a Module
If you want to see all the functions available in a module, use `dir()`:
```python
import math
print(dir(math))    # prints a list of everything in the math module
```

## Getting Help on Any Function or Module
The `help()` function displays the built-in documentation for anything in Python:
```python
help(print)         # Shows docs for the print() function
help(str.split)     # Shows docs for the string split() method

import os
help(os)            # Shows full documentation for the os module
```

## Useful Built-in Modules (No Install Needed)
These come with Python and are always available:
```python
import os           # File system operations: paths, directories, running commands
import re           # Regular expressions for pattern matching in strings
import json         # Read and write JSON data
import csv          # Read and write CSV files
import ipaddress    # Work with IP addresses and subnets
import datetime     # Work with dates and times
import math         # Mathematical functions (sqrt, floor, ceil, etc.)
import filecmp      # Compare files and directories
```

## The `ipaddress` Module — Network Automation Example
```python
import ipaddress

# Create a network object and iterate over all hosts in the subnet
network = ipaddress.ip_network("192.0.2.0/24")
for host in network.hosts():
    print(host)
# Automatically skips network address and broadcast address
```

## Installing Third-Party Packages with `pip`
`pip` is Python's package manager. Use it in your terminal/command line to install packages from the internet:
```bash
pip install netmiko      # SSH connections to network devices
pip install requests     # HTTP/API calls
pip install pandas       # Data analysis
pip install paramiko     # SSH protocol
pip install boto3        # AWS automation
```

## Common Network Automation Libraries

| Library | Purpose |
|---------|---------|
| `Netmiko` | SSH connections to routers, switches, firewalls |
| `NAPALM` | Interact with multiple network device OS types |
| `Paramiko` | Low-level SSHv2 implementation |
| `Requests` | Make HTTP requests to REST APIs |
| `Scapy` | Craft, send, and receive network packets |
| `Boto3` | Amazon Web Services (AWS) automation |
| `Pandas` | Data analysis, CSV/Excel file processing |