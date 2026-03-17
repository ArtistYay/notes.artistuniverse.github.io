---
tags:
  - Python
  - Computer Programming
---

Python has powerful built-in tools for working with files. In network automation, you constantly deal with files: configuration files, log files, CSV reports, firmware images, and more.

## The `open()` Function
`open()` is the starting point for any file operation. It takes two arguments: the filename and the mode. It returns a **file object** that you then use to read from or write to:
```python
file = open("config.txt", "r")   # open for reading
```

## File Modes

| Mode | Meaning | What happens |
|------|---------|-------------|
| `"r"` | Read | Opens existing file for reading. Error if file doesn't exist. |
| `"w"` | Write | Creates file if needed. **Overwrites all existing content.** |
| `"a"` | Append | Creates file if needed. Adds to the **end** — does not erase existing content. |
| `"x"` | Create | Creates a new file. Error if the file already exists. |
| `"rb"` | Read binary | Opens file in binary mode for reading (images, firmware, etc.) |
| `"wb"` | Write binary | Opens file in binary mode for writing |

> ⚠️ The difference between `"w"` and `"a"` is critical — `"w"` **destroys** all existing content. Use `"a"` when you want to add to a file (like a log) without losing what's already there.

## The `with` Statement Is The Right Way to Open Files
Always use the `with` statement when working with files. It **automatically closes the file** when the indented block ends, even if an error occurs inside. Without it, forgetting `.close()` wastes system resources and can cause data not to be saved:

```python
# ❌ Old way — you must remember to close manually
file = open("config.txt", "r")
content = file.read()
file.close()   # easy to forget — and if an error happens above, this never runs

# ✅ Better way — with handles closing automatically
with open("config.txt", "r") as file:
    content = file.read()
# file is automatically closed here, no matter what happened above
```

Why closing matters:
- Frees up system resources tied to the file
- Ensures that data you wrote is actually flushed and saved to disk
- Prevents other parts of your code from interacting with a half-finished file

## Reading Files
There are three methods to read content from a file:

**`.read()`** — Reads the entire file as a single string:
```python
with open("config.txt", "r") as file:
    content = file.read()
    print(content)    # one big string with all the content
```

**`.readline()`** — Reads one line at a time. Each call reads the next line. Useful when you only need the first line, or want to process a file line by line without loading it all at once:
```python
with open("config.txt", "r") as file:
    first_line  = file.readline()   # reads line 1
    second_line = file.readline()   # reads line 2 on the next call
```

**`.readlines()`** — Reads all lines and returns them as a **list**, one string per line. Each string includes the `\n` newline character at the end:
```python
with open("config.txt", "r") as file:
    lines = file.readlines()
# ['show version\n', 'show ip route\n', 'show interfaces\n']
```

**Cleaning up newlines with `.strip()`:**
When you read lines from a file, each line ends with `\n`. Use `.strip()` to remove trailing whitespace and newlines before using the value:
```python
with open("config.txt", "r") as file:
    commands = file.readlines()

commands = [line.strip() for line in commands]
# Before: ['show version\n', 'show ip route\n']
# After:  ['show version',   'show ip route']
```

**Reading only part of a file:**
```python
with open("log.txt", "r") as file:
    first_100_chars = file.read(100)   # reads only the first 100 bytes/characters
```

## Writing to Files
```python
# "w" mode — creates the file if needed, overwrites if it exists
with open("output.txt", "w") as file:
    file.write("interface GigabitEthernet0/1\n")
    file.write("ip address 192.168.1.1 255.255.255.0\n")

# "a" mode — adds to the end, preserving existing content
with open("log.txt", "a") as file:
    file.write("Device connected at 10:30\n")
```

## Text Files vs. Binary Files
**Text files** are human-readable. Examples: `.txt`, `.cfg`, `.log`, `.py`. When Python reads a text file, it automatically handles character encoding (converting bytes to readable characters like UTF-8).

**Binary files** are not human-readable — they contain raw bytes that represent images, audio, executables, firmware, etc. Python does NOT perform encoding/decoding on binary files — it reads and writes the exact bytes. You must open them with `"rb"` or `"wb"`:
```python
# Reading a firmware image (binary file)
def read_firmware_image(firmware_file):
    with open(firmware_file, "rb") as file:
        firmware_data = file.read()   # returns bytes object, not a string
    return firmware_data
```

In network automation: use text mode for config files and logs; use binary mode for firmware images and packet captures.

## CSV Files — Comma Separated Values
CSV (Comma Separated Values) files store tabular data — like a spreadsheet where each row is a line and values are separated by commas. Python's built-in `csv` module handles them properly, including edge cases like commas inside quoted fields.

**Reading a CSV file:**
```python
import csv

def read_device_info(device_file):
    with open(device_file, "r") as file:
        reader = csv.reader(file)           # create a reader object from the file
        headers = next(reader)              # next() reads ONE row — use for the header row
        devices = [row for row in reader]   # read all remaining rows into a list
    return headers, devices

# Each row comes back as a list of strings:
# headers → ['hostname', 'ip_address', 'type']
# devices → [['router1', '192.168.1.1', 'router'], ['switch1', '10.0.0.1', 'switch'], ...]
```

**Writing a CSV file:**
```python
import csv

devices = [
    ["Router1", "192.168.1.1", "router"],
    ["Switch1", "10.0.0.1",    "switch"],
]

with open("devices.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["hostname", "ip_address", "type"])   # write the header row first
    for device in devices:
        writer.writerow(device)                            # write each data row
```

## The `os` Module — File System Operations
The `os` module lets you interact with the operating system to work with files and directories:

```python
import os

# Check if a file or folder exists
if os.path.exists("config.txt"):
    print("File found!")
else:
    print("File not found.")

# Delete a file (always check existence first to avoid an error)
if os.path.exists("old_log.txt"):
    os.remove("old_log.txt")

# Delete an empty folder
if os.path.exists("logs"):
    os.rmdir("logs")    # only works if the folder is empty

# Rename a file or folder
os.rename("old_name.txt", "new_name.txt")

# Create a new directory
os.mkdir("new_folder")

# Get the current working directory (where your script is running from)
print(os.getcwd())

# List all files and folders in a directory
print(os.listdir("."))    # "." means the current directory
```

Always check if a file exists before operating on it. This prevents `FileNotFoundError` crashes:
```python
import os

config_file = "router_config.txt"

if os.path.exists(config_file):
    with open(config_file, "r") as file:
        commands = file.readlines()
    print(f"Loaded {len(commands)} configuration commands")
else:
    print(f"Config file '{config_file}' not found — cannot proceed.")
```

## Comparing Files with `filecmp`
The `filecmp` module checks whether two files are identical. In network automation, this is useful for detecting configuration drift — checking whether a device's running config has changed from the known-good backup:
```python
import filecmp

if filecmp.cmp("config_backup.txt", "config_current.txt"):
    print("Configurations match — no drift detected.")
else:
    print("Configurations differ — review changes!")
```

## SSH + File Automation with Paramiko
A complete example combining file reading with SSH to push config commands to a device:
```python
import paramiko

def automate_config(device_ip, username, password, config_file):
    # Set up the SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the device
    ssh.connect(device_ip, username=username, password=password)

    # Read commands from the config file
    with open(config_file, "r") as file:
        commands = file.read().splitlines()   # reads lines and strips \n

    # Send each command to the device
    for command in commands:
        ssh.exec_command(command)

    ssh.close()
```