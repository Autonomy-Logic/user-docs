# Python Function Block Structure

Every Python function block has the same shape: two required functions, plus a set of variables you declare in the IDE's Variables Table that become Python identifiers inside your code.

## The Two Required Functions

Your Python code must define exactly two functions. They're called automatically — you never call them yourself.

### `block_init()`

Called **once** when the Python process starts, before the first call to `block_loop()`. Use it for:

- Initializing persistent variables (counters, accumulators, buffers)
- Setting up data structures (lists, dictionaries)
- Printing startup messages for debugging

```python
def block_init():
    global sample_buffer, sample_index, total_count
    sample_buffer = [0.0] * 20
    sample_index = 0
    total_count = 0
    print('Moving average filter initialized with 20 samples')
```

> **Tip:** Use the `global` keyword to declare variables that need to persist between `block_init()` and `block_loop()`, and across multiple calls to `block_loop()` — including the output variables you assign to.

### `block_loop()`

Called **repeatedly**, approximately every **100 milliseconds**, for the entire lifetime of the process. This is where your main logic goes — read inputs, run your logic, assign outputs:

```python
def block_loop():
    global sample_buffer, sample_index, total_count, average

    # Update the moving average buffer with the current sensor reading
    sample_buffer[sample_index] = sensor_value
    sample_index = (sample_index + 1) % len(sample_buffer)
    total_count += 1

    # Calculate average (only over filled portion if not yet full)
    count = min(total_count, len(sample_buffer))
    average = sum(sample_buffer[:count]) / count
```

In this example, `sensor_value` is an Input declared in the Variables Table and `average` is an Output. The editor's runtime refreshes `sensor_value` before each call to `block_loop()` and sends `average` back to the PLC after `block_loop()` returns.

## How Variables Work

Variables for a Python function block are **not declared in the Python code**. Instead, you define them in the **Variables Table** in the IDE, just like any other IEC function block.

In the Variables Table, you specify:

| Column | Description |
|--------|-------------|
| **Name** | The variable name (e.g., `sensor_input`) |
| **Type** | An IEC 61131-3 data type (e.g., INT, REAL, BOOL) |
| **Class** | Input, Output, or Local |

The variable class determines the data flow:

| Class | Direction |
|-------|-----------|
| **Input** | PLC → Python (refreshed before every `block_loop()` call) |
| **Output** | Python → PLC (sent after every `block_loop()` call) |
| **Local** | Internal to the Python process; not visible to the PLC |

Inside `block_init()` and `block_loop()`, every variable from the table is available as a normal Python variable using the same name you typed. You don't need to read from any buffer, unpack any bytes, or compute any offsets — the editor wires that up for you.

A few Python-specific points worth knowing:

- **Reading is automatic** — just reference the input by name: `if temperature > 75.0:`
- **Writing requires `global`** — to assign to an output (or to any variable that must survive across `block_loop()` calls), declare it `global` at the top of the function. Otherwise Python treats your assignment as a function-local and the value never leaves the function.
- **Local variables in the table are independent of Python locals** — a Local declared in the table is a module-level Python variable that persists between cycles. A regular Python local declared with `temp = ...` inside `block_loop()` exists only for that one call.

## Supported Variable Types

You can use any of the following IEC types as inputs, outputs, or locals:

| IEC type | Python value |
|----------|--------------|
| BOOL | `bool` (`True` / `False`) |
| SINT, INT, DINT, LINT | `int` |
| USINT, UINT, UDINT, ULINT | `int` |
| BYTE, WORD, DWORD, LWORD | `int` |
| REAL, LREAL | `float` |
| STRING | `str` |
| ARRAY of any of the above | `list` |

When you read a variable, you get a plain Python value of the corresponding type. When you assign to an output, the value is converted back to its IEC type and sent to the PLC.

### Strings

STRING variables behave as ordinary Python `str` values. The maximum length is **126 characters** — anything longer will be truncated when written to an output.

```python
def block_loop():
    global message
    if temperature > threshold:
        message = "Over setpoint"
    else:
        message = "OK"
```

### Arrays

Array inputs and outputs appear as Python lists with the size declared in the Variables Table. Read and write individual elements like a normal list, but don't change the length — `append`/`pop` won't survive the round trip.

```python
# samples : ARRAY[0..9] OF INT (Input)
# average : REAL (Output)

def block_loop():
    global average
    average = sum(samples) / len(samples)
```

## Complete Example

A function block that implements a temperature alarm with hysteresis and a counter.

**Variables Table:**

| Name | Type | Class |
|------|------|-------|
| `temperature` | REAL | Input |
| `threshold` | REAL | Input |
| `hysteresis` | REAL | Input |
| `alarm` | BOOL | Output |
| `alarm_count` | INT | Output |

**Python Code:**

```python
from multiprocessing import shared_memory
import struct
import time
import os

def block_init():
    global alarm_active
    alarm_active = False
    print('Temperature alarm block initialized')

def block_loop():
    global alarm, alarm_count, alarm_active

    # Hysteresis: activate above threshold, deactivate below (threshold - hysteresis)
    if not alarm_active and temperature > threshold:
        alarm_active = True
        alarm_count += 1
    elif alarm_active and temperature < (threshold - hysteresis):
        alarm_active = False

    alarm = alarm_active
```

`alarm_active` is a Python-only flag (not in the Variables Table) that holds state between cycles. `alarm` and `alarm_count` are outputs, so they need `global` to be assigned. `temperature`, `threshold`, and `hysteresis` are inputs and can be read directly.

In the IEC program that uses this function block, you instantiate it just like any other FB:

```
VAR
    tempAlarm : TempAlarmFB;
END_VAR

tempAlarm(temperature := sensorReading, threshold := 75.0, hysteresis := 2.0);
IF tempAlarm.alarm THEN
    // Handle alarm condition
END_IF;
```

## What's Next?

Continue to [Python Restrictions and Sandbox](python-restrictions) to understand the execution constraints, available libraries, performance considerations, and best practices for writing reliable Python function blocks.
