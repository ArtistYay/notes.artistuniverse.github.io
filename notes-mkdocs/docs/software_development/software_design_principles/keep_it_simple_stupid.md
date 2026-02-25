# KISS (Keep It Simple, Stupid)

## Overview

Don't write a thousand lines of code when it can be done in a hundred, be fr, no one is gonna read that complex crap when you do a PR.

## Best Practices

- Avoid "clever" code. If I can't read your code and know what's going on, I'm rejecting your PR.
- Divide and conquer. By breaking a program into small parts, a programmer can safely focus on one specific area at a time.
- Scalability. Simple systems are much more cost-effective to scale and maintain over the long term.

!!! youtube "KISS (Keep It Simple, Stupid)"
	<iframe width="560" height="315" src="https://www.youtube-nocookie.com/embed/P4_2T4561B4?si=pZkFDIdXM6NxKNgz" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Real-world scenario

Which one is readable? This:

```python
def simple_math(a, b):
 if a > 10:
 result = (a ** 2) * (b + 5) - (a + b) / 2
 else:
 result = (a * b) - (b / 2) + a ** b
 return result
```

or that:

```python
def complex_math(a, b):
 return ((a ** 2) * (b + 5)) - ((a + b) / 2) if a > 10 else ((a * b) - (b / 2) + a ** b)
```