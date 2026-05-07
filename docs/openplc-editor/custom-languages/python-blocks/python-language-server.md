# Python Editor Features

The Autonomy Edge IDE provides a rich editing experience for Python function blocks. You get syntax highlighting, type checking, autocompletion, hover documentation, and code snippets — all running directly in your browser.

## Editor Overview

When you open a Python function block in the IDE, the code editor provides:

- Python-specific syntax highlighting
- Pyright-based type checking and intelligent features
- A curated set of code snippets for common Python patterns
- Automatic indentation and bracket matching

The result is a modern editing experience where you can write, validate, and refine your Python code without leaving the browser.

## Syntax Highlighting

The Python syntax highlighter provides color-coded highlighting for:

- **Keywords**: `def`, `class`, `if`, `elif`, `else`, `for`, `while`, `try`, `except`, `import`, `from`, `return`, `global`, `with`, `as`, `yield`, `lambda`, etc.
- **Built-in functions**: `print()`, `len()`, `range()`, `int()`, `float()`, `str()`, `list()`, `dict()`, `tuple()`, `set()`, `type()`, `isinstance()`, etc.
- **Operators**: Arithmetic (`+`, `-`, `*`, `/`, `//`, `%`, `**`), comparison (`==`, `!=`, `<`, `>`, `<=`, `>=`), logical (`and`, `or`, `not`), bitwise (`&`, `|`, `^`, `~`, `<<`, `>>`)
- **Strings**: Single-quoted, double-quoted, triple-quoted, and raw strings (r-strings)
- **Numbers**: Integers, floats, hex (`0x`), octal (`0o`), binary (`0b`), and scientific notation
- **Comments**: Lines starting with `#`
- **Decorators**: Lines starting with `@`

Syntax highlighting activates immediately as you type — no delay or configuration required.

## Type Checking and Diagnostics

The IDE integrates **Pyright**, a fast static type checker for Python, running directly in your browser. Pyright analyzes your code for type errors, undefined variables, incorrect function signatures, and other issues. Diagnostics appear as underlined warnings or errors in the editor, with details shown when you hover over the underlined code.

Examples of issues Pyright can detect:

- Using an undefined variable name
- Passing the wrong number of arguments to a function
- Type mismatches (e.g., adding a string to an integer)
- Missing return statements in functions with declared return types
- Unreachable code after `return` or `raise`

Diagnostics are refreshed approximately every **1 second** after you stop typing, so feedback is near-instantaneous without being disruptive.

## Hover Documentation

When you hover your mouse over a variable, function, or module name, the editor displays a tooltip with:

- The inferred type of the symbol
- The function signature (for functions and methods)
- The docstring (for standard library functions and classes)

This is especially handy for standard library modules — hover over a function like `math.sin` or `json.loads` and you'll see its signature and docstring without leaving the editor.

## Autocompletion

As you type, the editor suggests completions based on:

- Python keywords and built-in functions
- Variables and functions defined in your code
- Module members after an import (e.g., typing `math.` shows `sin`, `cos`, `sqrt`, `pi`, etc.)
- Method names on objects (e.g., typing `my_list.` shows `append`, `extend`, `sort`, etc.)

Press **Tab** or **Enter** to accept a suggestion, or **Escape** to dismiss the completion list.

## Feature Summary

| Feature | Status | Description |
|---------|--------|-------------|
| Syntax highlighting | Enabled | Color-coded tokens as you type |
| Hover documentation | Enabled | Type info and docstrings on mouse hover |
| Autocompletion | Enabled | Context-aware suggestions as you type |
| Diagnostics | Enabled | Type errors and warnings, refreshed every ~1 second |
| Signature help | Disabled | No inline parameter hints during function calls |
| Rename symbol | Disabled | No cross-file rename refactoring |
| Go to definition | Disabled | No jump-to-definition navigation |

The disabled features are not applicable in the single-file context of Python function blocks, where each FB is a standalone script.

## Code Snippets

The editor includes **code snippets** for common Python patterns. Type a snippet prefix and select it from the completion list to insert a pre-formatted code template with placeholder fields you can tab through.

| Prefix | Expands To |
|--------|-----------|
| `if` | `if` statement with condition and body |
| `elif` | `elif` clause |
| `else` | `else` clause |
| `if/else` | Complete `if`/`else` block |
| `if/elif/else` | Complete `if`/`elif`/`else` block |
| `for` | `for` loop with iterable |
| `while` | `while` loop with condition |
| `try/except` | `try`/`except` block |
| `try/except/finally` | `try`/`except`/`finally` block |
| `try/except/else/finally` | Full `try` block with all clauses |
| `def` | Function definition with parameters and body |
| `class` | Class definition with `__init__` method |
| `with` | `with` statement (context manager) |
| `list` | List comprehension |
| `dict` | Dictionary comprehension |
| `lambda` | Lambda expression |

To use a snippet:

1. Start typing the snippet prefix (e.g., `for`)
2. Select the snippet from the autocompletion dropdown
3. The template is inserted with the first placeholder selected
4. Press **Tab** to move to the next placeholder
5. Press **Escape** when done editing placeholders

### Example: Using the `for` Snippet

Type `for` and select the snippet. The editor inserts:

```python
for item in iterable:
    pass
```

With `item` selected as the first placeholder. Type your variable name, press **Tab** to jump to `iterable`, type your collection name, then **Tab** again to move into the loop body.

## Tips for Effective Editing

### Use Type Hints for Better Diagnostics

While not required, adding type hints to your own helpers and locals helps Pyright provide more accurate diagnostics:

```python
def clamp(value: float, lo: float, hi: float) -> float:
    if value < lo: return lo
    if value > hi: return hi
    return value

def block_init() -> None:
    global sample_count
    sample_count = 0

def block_loop() -> None:
    global sample_count, average
    sample_count += 1
    average = clamp(reading / sample_count, 0.0, 100.0)
```

### Check Diagnostics Before Building

The diagnostics panel catches many errors that would otherwise surface only at build time or at runtime. Before building your project, check that there are no red (error) underlines in your Python code. Yellow (warning) underlines are worth reviewing but don't necessarily indicate problems.

### Use Print Statements for Debugging

The `print()` function is available and its output is captured by the runtime's logging system. During development, use print statements to confirm that input values look right and to inspect what your code is producing for outputs:

```python
def block_loop():
    global result
    print(f'Raw input value: {raw}')  # Visible in runtime logs

    result = raw * 2
    print(f'Output value: {result}')
```

> **Tip:** Remove or comment out verbose print statements before deploying to production to reduce logging overhead.

### Leverage Autocompletion for Imports

When you need a standard library module, type `import ` and the autocompletion list shows available modules:

```python
import math       # Mathematical functions
import json       # JSON encoding/decoding
import datetime   # Date and time handling
import re         # Regular expressions
import statistics # Statistical functions
```

## What's Next?

Continue to [C++ Function Blocks](../../custom-languages/cpp-blocks/cpp-basics) to learn about the other custom programming language available for extending PLC functionality with C++ code, including direct hardware access via Arduino-compatible APIs.
