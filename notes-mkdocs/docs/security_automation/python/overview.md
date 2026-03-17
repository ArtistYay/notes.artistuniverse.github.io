---
tags:
  - Python
  - Computer Programming
---

## What is Python?

Python is the go-to language for IT automation because of:

- Readable syntax — easy to learn and maintain

- Extensive libraries — Netmiko, NAPALM, Paramiko, Requests, etc.

- Cross-platform — runs on Windows, Linux, macOS

- Dynamic typing — no need to declare variable types

- Large community — tons of resources and pre-built solutions

## Subcategories

1. [Variables](variables.md)
2. [Data Types](data_types.md)
3. [Operators](operators.md)
4. [If / Else Statements](if_else_statements.md)
5. [Loops](loops.md)
6. [Functions](functions.md)
7. [Lists & Tuples](lists_and_tuples.md)
8. [Dictionaries & Sets](dictionaries_sets.md)
9. [Modules, Libraries & Packages](modules_libraries_and_packages.md)
10. [Error Handling & Debugging](error_handling_and_debugging.md)
11. [File Management](file_management.md)
12. [Applying Python (APIs & Automation)](applying_python.md)

## Quick Reference — Key Rules to Remember

| Concept | The Rule |
|---------|----------|
| Variables | Created on assignment — no declaration needed |
| `=` vs `==` | `=` assigns a value; `==` compares two values — mixing these up is a common bug |
| `is` vs `==` | `is` checks if two variables are the same object in memory; `==` checks if values are equal |
| Indentation | 4 spaces = one code block level. Missing or wrong indentation is a SyntaxError |
| List `[]` | Ordered, mutable — you can add, change, and remove items |
| Tuple `()` | Ordered, immutable — contents are fixed after creation |
| Dict `{}` with `:` | Key-value pairs — look up values by key, not by position |
| Set `{}` no `:` | Unordered, unique items only — great for deduplication |
| `for x in y` | Loops over every item in y, one at a time |
| `while condition` | Loops as long as condition is `True` — always update something to avoid infinite loops |
| `break` | Exit the loop immediately |
| `continue` | Skip to the next loop iteration |
| `def` | Defines a reusable function |
| `return` | Sends a value back from a function — without it, function returns `None` |
| `try / except` | Wraps risky code — if an error occurs, `except` runs instead of crashing |
| `with open()` | Best way to work with files — automatically closes the file when done |
| `"r"` / `"w"` / `"a"` | Read / Write (overwrites everything) / Append (adds to end) |
| `.strip()` | Removes leading/trailing whitespace and `\n` newline characters from a string |
| `.readlines()` | Reads all lines from a file into a list of strings |
| `csv.reader()` | Creates a reader object to loop through rows of a CSV file |
| `next(reader)` | Reads one row from a CSV reader — use this for the header row |
| `os.path.exists()` | Check if a file/folder exists before trying to open, delete, or modify it |
| `os.remove()` | Delete a file |
| `filecmp.cmp()` | Compare two files — returns `True` if identical |
| `import` | Load a module or library so you can use its functions |
| `help()` | View built-in documentation for any function, method, or module |
| `pip install` | Install a third-party library from the command line |   