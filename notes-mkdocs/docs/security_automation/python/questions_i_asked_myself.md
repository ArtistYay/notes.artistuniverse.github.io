### What is the difference between functions, methods, and modules?

Functions are blocks of code which is designed to do one job or have one responsibility. The can be created with the `def` keyword. For example:

```python
def square(number):
    if number not in range (1,65):
        raise ValueError ("square must be between 1 and 64")
    grainsOnSquare = 2 ** (number - 1)
    return grainsOnSquare

print(square(64))
```
Functions can use arguments inside their parentheses (inputs/parameters). In Python, functions are objects; they can be assigned to variables, passed as arguments to other functions, and returned from functions

A method is essentially a function that belongs to a class or is tied to a value of a certain data type, It represents the "behavior" of an object. Unlike functions, methods are "called on" a value or object using dot notation (e.g., `object.method()`)

A key difference between a method and a standalone function is that a method defined inside a class typically includes self as its first parameter. This allows the method to access the specific instance of the object it is acting upon. Data types like strings and lists have built-in methods. For example, `append()` is a method for lists, and `upper()` is a method for strings.

A module is a file containing Python code, such as functions, classes, and variables. Modules are used to organize code into manageable files and reuse code across different programs, To use the code within a module, you must import it using the `import` statement. Once imported, you access the functions or variables inside a module using the dot operator (e.g., `module_name.function_name()`).

### What is a Python function signature?

Function signature is the part of a function definition that specifies its name, its parameters (input arguments), and its expected return value.

### How do I read the Python documentation or know what it's telling me?

Function Signatures (e.g., def name(param1, param2):) acts as a usage contract. It tells you the name of the function, the arguments it requires, and any optional parameters that have default values

### Is there a built in tool that lists out built in methods and functions?

This question insipred me because I have an exam coming up and I can't really Google to get the answers I want. For this question it lead me to `dir(__builtins__)`. 

```python
pprint.pprint(dir(__builtins__), compact=True)
 ['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException',
  'BlockingIOError', 'BrokenPipeError', 'BufferError', 'BytesWarning',
  'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError',
  'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning',
  'EOFError', 'Ellipsis', 'EnvironmentError', 'Exception', 'False',
  'FileExistsError', 'FileNotFoundError', 'FloatingPointError', 'FutureWarning',
  'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError',
  'IndexError', 'InterruptedError', 'IsADirectoryError', 'KeyError',
  'KeyboardInterrupt', 'LookupError', 'MemoryError', 'ModuleNotFoundError',
  'NameError', 'None', 'NotADirectoryError', 'NotImplemented',
  'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning',
  'PermissionError', 'ProcessLookupError', 'RecursionError', 'ReferenceError',
  'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 'StopAsyncIteration',
  'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit',
  'TabError', 'TimeoutError', 'True', 'TypeError', 'UnboundLocalError',
  'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError',
  'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError',
  'Warning', 'ZeroDivisionError', '__IPYTHON__', '__build_class__', '__debug__',
  '__doc__', '__import__', '__loader__', '__name__', '__package__', '__spec__',
  'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray',
  'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'copyright',
  'credits', 'delattr', 'dict', 'dir', 'display', 'divmod', 'enumerate', 'eval',
  'exec', 'filter', 'float', 'format', 'frozenset', 'get_ipython', 'getattr',
  'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int',
  'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'map',
  'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow',
  'print', 'property', 'range', 'repr', 'reversed', 'round', 'set', 'setattr',
  'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type',
  'vars', 'zip']
```

### What is the difference between Python's OOP and the Software Development Principles?

If I'm understanding this properly, OOP is a programming paradigm (a way to organize code and data). While the Software Development Principles is a global set of rules devs all around the world follow.

### What is 'return' and how can I use it properly?

`return` is a keyword used inside a function to send a result back to the part of the program that called it. It is not like the `print()` function, `return` gives any output back to the program itself so it can be stored in a variable or used in an expression.

If you define a function but forget to include a `return` statement, Python will automatically return the value `None`, which represents the absence of a value.

While a function technically returns one thing, you can package multiple pieces of data into a single tuple (e.g., return x, y) to send back more than one result.

You can use `return` to "bail out" of a function early if an error is detected or a certain condition is met.

Since `return` exits the function immediately, any code written directly after a `return` statement in the same block will never run. This is known as *dead code* and should be avoided to prevent confusion.