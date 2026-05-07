# Python Function Blocks

Python function blocks let you write automation logic in Python while integrating seamlessly with your IEC 61131-3 program. You get access to Python's rich standard library for tasks like math, string processing, data conversion, and more — all within the Autonomy Edge platform.

## Why Python Function Blocks?

Standard IEC 61131-3 languages are built for deterministic, cyclic control logic. They're great at reading sensors, driving outputs, and executing tightly timed sequences. But some tasks are easier in a general-purpose language:

- **Complex calculations** — Statistical analysis, advanced math, or data transformations
- **String processing** — Parsing messages, formatting data, or building protocol payloads
- **Data conversion** — Converting between units, encoding/decoding values, or mapping ranges
- **Algorithm prototyping** — Quickly testing ideas with Python's expressive syntax before deciding whether to reimplement in ST

Python function blocks handle these tasks without leaving the Autonomy Edge platform.

## How Python FBs Fit In

Python function blocks run differently from standard IEC function blocks. Here's how they compare:

| Aspect | Standard IEC Function Block | Python Function Block |
|--------|---------------------------|----------------------|
| **Execution** | Runs inside the PLC scan cycle | Runs as a separate process |
| **Timing** | Synchronized with the scan cycle | Asynchronous, ~100 ms loop |
| **State** | Managed by the runtime | Managed by the Python process |
| **Language** | ST, LD, FBD, IL | Python 3 |
| **Libraries** | IEC standard functions only | Python standard library |

The key point: Python function blocks are **not synchronized** with the PLC scan cycle. The runtime launches a Python process, creates shared memory regions for input and output variables, and your Python code reads/writes those regions on its own ~100 ms loop. The PLC scan cycle and the Python loop run independently.

```
┌─────────────────────┐        Shared Memory        ┌──────────────────────┐
│    PLC Runtime      │ ◄──── Input Variables ────►  │  Python Process      │
│  (scan cycle)       │ ◄──── Output Variables ───►  │  (~100 ms loop)      │
│                     │                              │                      │
│  Reads/writes       │                              │  Reads/writes        │
│  shared memory      │                              │  shared memory       │
│  each scan cycle    │                              │  each ~100 ms        │
└─────────────────────┘                              └──────────────────────┘
```

## When to Use Python vs. IEC Languages

**Use Python function blocks when:**

- You need complex math that would be verbose in Structured Text (e.g., moving averages, statistical calculations)
- You want to process or format strings beyond what IEC string functions offer
- You need to work with data structures like lists or dictionaries
- You're prototyping logic quickly and Python's syntax helps you iterate faster

**Use standard IEC languages when:**

- You need deterministic, scan-cycle-synchronized execution
- You're implementing time-critical control logic (motor control, safety interlocks)
- You want guaranteed execution timing for real-time responsiveness
- Your logic is naturally expressed as relay logic (LD) or block connections (FBD)

> **Tip:** Python function blocks are only available as **Function Blocks**, not as Programs or Functions. When creating a new POU and choosing Python as the language, the POU type is always Function Block.

## Creating a Python Function Block

To create a Python function block in the Autonomy Edge IDE:

1. Open your project in the IDE at [edge.autonomylogic.com](https://edge.autonomylogic.com)
2. In the **Project Explorer**, right-click and select **Add POU** (or use the add button)
3. Enter a name for your function block (e.g., `ScaleInput`)
4. Select **Function Block** as the POU type
5. Select **Python** as the programming language
6. Click **Create**

The IDE opens a code editor pre-populated with the Python function block template.

## The Template Code

Every new Python function block starts with this template:

```python
from multiprocessing import shared_memory
import struct
import time
import os

def block_init():
    print('Block was initialized')

def block_loop():
    print('Block has run the loop function')
```

This template defines the two required functions:

- **`block_init()`** — Called exactly once when the Python process starts. Use it for one-time setup, such as initializing persistent variables or preparing data structures.
- **`block_loop()`** — Called repeatedly, approximately every 100 milliseconds. This is where your main logic goes — reading inputs, performing calculations, and writing outputs.

The import statements at the top (`shared_memory`, `struct`, `time`, `os`) are used for communication between your code and the PLC. You can use them in your own code as well, and you can add additional standard library imports as needed.

## A Basic Example

Here's a simple Python function block that scales an analog input value from a raw integer range to engineering units. Suppose you declare the following variables in the Variables Table:

| Name | Type | Class |
|------|------|-------|
| `raw_value` | INT | Input |
| `scale_min` | REAL | Input |
| `scale_max` | REAL | Input |
| `scaled_output` | REAL | Output |

The Python code:

```python
from multiprocessing import shared_memory
import struct
import time
import os

def block_init():
    # No special initialization needed for this example
    pass

def block_loop():
    # Read the raw INT input (16-bit signed)
    raw = struct.unpack('h', shm_in.buf[0:2])[0]

    # Read the two REAL inputs (32-bit floats)
    min_val = struct.unpack('f', shm_in.buf[2:6])[0]
    max_val = struct.unpack('f', shm_in.buf[6:10])[0]

    # Scale the raw value (assuming raw range 0-32767)
    if max_val != min_val:
        scaled = min_val + (raw / 32767.0) * (max_val - min_val)
    else:
        scaled = min_val

    # Write the REAL output (32-bit float)
    struct.pack_into('f', shm_out.buf, 0, scaled)
```

In this example:

- `shm_in` and `shm_out` are shared memory objects provided automatically — you don't create them yourself
- `struct.unpack()` reads binary data from the input shared memory region
- `struct.pack_into()` writes binary data to the output shared memory region
- The byte offsets (0, 2, 6, 10) correspond to the packed sizes of each variable in declaration order

Don't worry if the shared memory details seem complex at this point. The next page covers the full structure of Python function blocks, including how variables map to shared memory offsets and all the supported data types.

## Summary

Python function blocks provide a powerful way to extend your PLC programs with general-purpose Python code. They run as isolated processes, communicate through shared memory, and give you access to Python's standard library. The trade-off is that they're not synchronized with the PLC scan cycle, so they're best suited for non-time-critical computations rather than real-time control.

## What's Next?

Continue to [Python Function Block Structure](python-structure) to learn how `block_init()` and `block_loop()` work, how variables map to shared memory, and the complete type encoding reference.
