---
tags:
  - Python
---

## Stages

### *Print a prompt*

Bumped into an error when I scripted out this:

```python
import sys
def main():
    command = input(sys.stdout.write("$ "))
    print(f"{command}: command not found")
    pass
if __name__ == "__main__":
    main()
```

Apparently, I was getting an output of `$ 2` python reads the doesn't read the input() function first instead it looks at the `sys.stdout.write()` function first and recognizing that there is two objects.
