# Python Function Block Structure

Every Python function block follows a specific structure: two required functions, a set of variables declared in the IDE's Variables Table, and a shared memory interface that bridges your Python code with the PLC runtime. This page explains each part so you can write Python function blocks with confidence.

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

> **Tip:** Use the `global` keyword to declare variables that need to persist between `block_init()` and `block_loop()`, and across multiple calls to `block_loop()`.

### `block_loop()`

Called **repeatedly**, approximately every **100 milliseconds**, for the entire lifetime of the process. This is where your main logic goes:

- Read input variables from shared memory
- Perform calculations or data processing
- Write output variables to shared memory

```python
def block_loop():
    global sample_buffer, sample_index, total_count

    # Read a REAL input (32-bit float)
    sensor_value = struct.unpack('f', shm_in.buf[0:4])[0]

    # Update the moving average buffer
    sample_buffer[sample_index] = sensor_value
    sample_index = (sample_index + 1) % len(sample_buffer)
    total_count += 1

    # Calculate average (only over filled portion if not yet full)
    count = min(total_count, len(sample_buffer))
    average = sum(sample_buffer[:count]) / count

    # Write the REAL output (32-bit float)
    struct.pack_into('f', shm_out.buf, 0, average)
```

## How Variables Are Declared

Variables for a Python function block are **not declared in the Python code**. Instead, you define them in the **Variables Table** in the IDE, just like any other IEC function block.

In the Variables Table, you specify:

| Column | Description |
|--------|-------------|
| **Name** | The variable name (e.g., `sensor_input`) |
| **Type** | An IEC 61131-3 data type (e.g., INT, REAL, BOOL) |
| **Class** | Input, Output, or Local |

The variable class determines how the variable is used:

| Class | Direction | Shared Memory Region |
|-------|-----------|---------------------|
| **Input** | PLC writes, Python reads | Input region (`shm_in`) |
| **Output** | Python writes, PLC reads | Output region (`shm_out`) |
| **Local** | Internal to the function block | Not in shared memory |

### Example Variable Declaration

Suppose you're building a temperature alarm function block. In the Variables Table, you'd declare:

| Name | Type | Class |
|------|------|-------|
| `temperature` | REAL | Input |
| `threshold` | REAL | Input |
| `hysteresis` | REAL | Input |
| `alarm` | BOOL | Output |
| `alarm_count` | INT | Output |

These five variables define the interface of your function block. When another POU instantiates your Python FB, it connects signals to the inputs and reads the outputs — exactly like a standard IEC function block.

## Variable Type Mapping

When you read from `shm_in` or write to `shm_out`, you must use the correct `struct` format string for each IEC data type. Here's the complete mapping:

| IEC Type | `struct` Format | Size (bytes) | Python Type | Description |
|----------|----------------|--------------|-------------|-------------|
| BOOL | `B` | 1 | int (0 or 1) | Unsigned char |
| SINT | `b` | 1 | int | Signed 8-bit integer |
| INT | `h` | 2 | int | Signed 16-bit integer |
| DINT | `i` | 4 | int | Signed 32-bit integer |
| LINT | `q` | 8 | int | Signed 64-bit integer |
| USINT | `B` | 1 | int | Unsigned 8-bit integer |
| UINT | `H` | 2 | int | Unsigned 16-bit integer |
| UDINT | `I` | 4 | int | Unsigned 32-bit integer |
| ULINT | `Q` | 8 | int | Unsigned 64-bit integer |
| REAL | `f` | 4 | float | 32-bit floating point |
| LREAL | `d` | 8 | float | 64-bit floating point |
| BYTE | `B` | 1 | int | 8-bit bit string |
| WORD | `H` | 2 | int | 16-bit bit string |
| DWORD | `I` | 4 | int | 32-bit bit string |
| LWORD | `Q` | 8 | int | 64-bit bit string |
| STRING | `b126s` | 127 | (int, bytes) | Length byte + 126-byte buffer |

### Calculating Byte Offsets

Variables are packed in the shared memory region **in the order they are declared** in the Variables Table. To calculate the byte offset for each variable, sum the sizes of all preceding variables.

For the temperature alarm example above (all inputs):

| Variable | Type | Format | Size | Offset |
|----------|------|--------|------|--------|
| `temperature` | REAL | `f` | 4 | 0 |
| `threshold` | REAL | `f` | 4 | 4 |
| `hysteresis` | REAL | `f` | 4 | 8 |

And for the outputs:

| Variable | Type | Format | Size | Offset |
|----------|------|--------|------|--------|
| `alarm` | BOOL | `B` | 1 | 0 |
| `alarm_count` | INT | `h` | 2 | 1 |

> **Tip:** Input and output variables occupy **separate** shared memory regions. Offsets start at 0 for each region independently.

## String Handling

Strings require special attention. A STRING variable is transmitted as **two values** in shared memory:

1. **Length byte** (`b` format, 1 byte): the number of valid characters in the string
2. **Body buffer** (`126s` format, 126 bytes): the raw character data, padded with null bytes

To read a string input:

```python
# Read a STRING input starting at the given offset
offset = 0
length = struct.unpack_from('b', shm_in.buf, offset)[0]
body = struct.unpack_from('126s', shm_in.buf, offset + 1)[0]
text = body[:length].decode('ascii')
```

To write a string output:

```python
# Write a STRING output starting at the given offset
offset = 0
text = "Hello PLC"
encoded = text.encode('ascii')[:126]  # Truncate to max 126 chars
length = len(encoded)
body = encoded.ljust(126, b'\x00')    # Pad to 126 bytes
struct.pack_into('b', shm_out.buf, offset, length)
struct.pack_into('126s', shm_out.buf, offset + 1, body)
```

Each STRING variable occupies **127 bytes** total (1 byte length + 126 bytes body) in the shared memory region.

## Complete Example

Here's a full example combining variable declarations and Python code. This function block implements a temperature alarm with hysteresis and a counter.

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
    global count, alarm_active
    count = 0
    alarm_active = False
    print('Temperature alarm block initialized')

def block_loop():
    global count, alarm_active

    # Read inputs (offsets: temperature=0, threshold=4, hysteresis=8)
    temp = struct.unpack_from('f', shm_in.buf, 0)[0]
    thresh = struct.unpack_from('f', shm_in.buf, 4)[0]
    hyst = struct.unpack_from('f', shm_in.buf, 8)[0]

    # Hysteresis logic: activate above threshold, deactivate below (threshold - hysteresis)
    if not alarm_active and temp > thresh:
        alarm_active = True
        count += 1
    elif alarm_active and temp < (thresh - hyst):
        alarm_active = False

    # Write outputs (offsets: alarm=0, alarm_count=1)
    struct.pack_into('B', shm_out.buf, 0, 1 if alarm_active else 0)
    struct.pack_into('h', shm_out.buf, 1, count)
```

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
