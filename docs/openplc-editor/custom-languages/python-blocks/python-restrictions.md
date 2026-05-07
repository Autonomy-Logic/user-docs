# Python Restrictions and Sandbox

Python function blocks offer significant flexibility, but they operate within a specific execution environment with constraints you need to understand. This page covers the execution model, available resources, things to avoid, and best practices for writing reliable Python FBs.

## Execution Model

### Process Isolation

Each Python function block runs in its own **separate process**, launched by the PLC runtime when the program starts. This means:

- Your Python code runs in a completely separate process from the PLC runtime
- It has its own memory space, independent of the PLC scan cycle
- Multiple Python function blocks each get their own process
- A crash in your Python code does not crash the PLC runtime

### The ~100 ms Loop

Your `block_loop()` function is called approximately every **100 milliseconds**. This timing is not configurable. The actual interval may vary slightly depending on:

- How long your `block_loop()` code takes to execute
- System load on the host machine
- Operating system scheduling

If your `block_loop()` takes longer than 100 ms to execute, the next iteration starts immediately after the current one finishes — there's no backlog of missed cycles.

### Not Scan-Cycle Synchronized

> **Tip:** Python function blocks are **not synchronized** with the PLC scan cycle. The PLC scan cycle and the Python ~100 ms loop run independently, at different rates, with no coordination between them.

This has practical consequences:

| Scenario | What Happens |
|----------|-------------|
| PLC scan cycle is 10 ms | Python sees ~10 scan cycles worth of change per loop iteration |
| PLC scan cycle is 50 ms | Python sees ~2 scan cycles worth of change per loop iteration |
| PLC scan cycle is 200 ms | Python may run multiple times between PLC scans |
| Python reads an input | The value may change between the read and the next PLC scan |
| Python writes an output | The PLC picks it up on its next scan, not immediately |

For time-critical control logic where every scan cycle matters (e.g., safety interlocks, fast motor control), use standard IEC languages instead.

## Available Libraries

Python function blocks have access to the **Python 3 standard library**. The following modules are already imported and available in your code:

- `struct` — Binary data packing and unpacking (essential for shared memory I/O)
- `time` — Time-related functions
- `os` — Operating system interface
- `multiprocessing.shared_memory` — Shared memory access

You can import any additional standard library module:

```python
import math
import json
import datetime
import collections
import statistics
import re
import decimal
import itertools
import functools
import hashlib
```

### What Is NOT Available

- **Third-party packages** — There's no mechanism to install packages via pip. You cannot use NumPy, Pandas, Requests, or any other package outside the Python standard library.
- **Custom modules** — You cannot import your own `.py` files. Each Python function block is a self-contained script.

## What to Avoid

### Blocking Operations

Since `block_loop()` runs on a ~100 ms cycle, any operation that blocks for a significant amount of time will delay subsequent iterations and disrupt the expected timing:

```python
# DO NOT do this — blocks the loop
def block_loop():
    import urllib.request
    response = urllib.request.urlopen('http://example.com')  # Network call, may take seconds
    data = response.read()
```

Specific operations to avoid:

| Operation | Why It's a Problem |
|-----------|-------------------|
| Network requests (HTTP, sockets) | Unpredictable latency, can block for seconds |
| File I/O on slow storage | Disk access can stall the loop |
| `time.sleep()` | Directly delays the loop by the sleep duration |
| Waiting for external processes | Blocks until the process completes |
| Large file reads/writes | Can take significant time depending on file size |

If you absolutely need to perform a slow operation, keep it in `block_init()` where a one-time delay is acceptable, rather than in `block_loop()` where it would cause recurring delays.

### Threading and Multiprocessing

The Python process is designed as a **single-threaded** execution model. Avoid:

```python
# DO NOT do this
import threading
def block_loop():
    t = threading.Thread(target=some_function)
    t.start()  # Creates threads that may conflict with shared memory access
```

Creating threads can lead to race conditions with the shared memory access and the loop management. Similarly, spawning child processes from within the Python process is not supported.

### Spawning Subprocesses

Do not use `subprocess`, `os.system()`, or `os.popen()` to launch other programs:

```python
# DO NOT do this
import subprocess
def block_loop():
    result = subprocess.run(['ls', '-la'], capture_output=True)  # Spawns a child process
```

The Python process is already a child of the PLC runtime. Spawning further children creates an unmanaged process tree that the runtime cannot clean up properly.

### Infinite Loops in block_loop()

The loop timing is already managed for you. Do not create your own infinite loop inside `block_loop()`:

```python
# DO NOT do this — block_loop is already called repeatedly
def block_loop():
    while True:
        do_something()
        time.sleep(0.1)
```

This would prevent the next call to `block_loop()`, effectively freezing your function block.

## Shared Memory Constraints

- Shared memory regions have a **fixed size** determined by the declared variables
- You must not write beyond the allocated size of the output region
- You must not write to the input region (it's read-only from the Python perspective)
- Reading past the end of the input region or writing past the end of the output region leads to undefined behavior and may crash the process

## Performance Considerations

### Keep block_loop() Fast

Aim to keep each `block_loop()` execution well under 100 ms. If your computation takes close to or longer than 100 ms, the effective update rate drops:

| block_loop() Duration | Effective Update Rate |
|----------------------|----------------------|
| < 1 ms | ~100 ms (limited by the loop sleep) |
| 50 ms | ~150 ms (50 ms execution + 100 ms sleep) |
| 100 ms | ~200 ms (100 ms execution + 100 ms sleep) |
| 500 ms | ~600 ms (severely degraded) |

### Memory Usage

Each Python process consumes memory independently. The base Python interpreter uses approximately 10–20 MB. If you create large data structures (lists, buffers), account for this additional memory usage, especially if you have multiple Python function block instances running simultaneously.

### Stdout and Stderr

Anything you `print()` from your Python code is captured and forwarded to the PLC's logging system. Use `print()` for debugging, but avoid excessive output in production as it generates logging overhead.

```python
def block_init():
    print('MyBlock: initialized')  # Good — one-time message

def block_loop():
    # print(f'value: {value}')  # Avoid in production — prints every 100 ms
    pass
```

## Best Practices

1. **Initialize in `block_init()`, compute in `block_loop()`** — Keep the separation clean. All one-time setup goes in `block_init()`, all cyclic logic goes in `block_loop()`.

2. **Use `global` for persistent state** — Variables that need to survive between `block_loop()` calls must be declared `global` at the top of the function.

3. **Validate inputs before processing** — Shared memory values can change unexpectedly. Check for division by zero, out-of-range values, and invalid states:

    ```python
    def block_loop():
        divisor = struct.unpack_from('f', shm_in.buf, 0)[0]
        if divisor != 0.0:
            result = 100.0 / divisor
        else:
            result = 0.0
        struct.pack_into('f', shm_out.buf, 0, result)
    ```

4. **Use `try/except` for robustness** — Wrap your logic in exception handling to prevent the process from crashing:

    ```python
    def block_loop():
        try:
            # Your logic here
            value = struct.unpack_from('h', shm_in.buf, 0)[0]
            result = complex_calculation(value)
            struct.pack_into('h', shm_out.buf, 0, result)
        except Exception as e:
            print(f'Error in block_loop: {e}')
            # Write a safe default output
            struct.pack_into('h', shm_out.buf, 0, 0)
    ```

5. **Minimize print() in block_loop()** — Use print statements for debugging during development, but remove or comment them out for production.

6. **Keep computations deterministic** — Avoid relying on external state (files, time-of-day) for critical outputs. If the same inputs should always produce the same outputs, your logic will be easier to test and debug.

7. **Pre-compute constants in block_init()** — If your calculation uses constant values (lookup tables, conversion factors), compute them once in `block_init()` and store them as global variables:

    ```python
    def block_init():
        global lookup_table
        lookup_table = [math.sin(i * math.pi / 180) for i in range(360)]

    def block_loop():
        global lookup_table
        angle = struct.unpack_from('H', shm_in.buf, 0)[0] % 360
        result = lookup_table[angle]
        struct.pack_into('f', shm_out.buf, 0, result)
    ```

## What's Next?

Continue to [Python Editor Features](python-language-server) to learn about syntax highlighting, type checking, autocompletion, and other editing tools available in the Python code editor.
