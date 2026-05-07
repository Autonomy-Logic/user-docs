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

Python function blocks run inside the Python interpreter on the target device — the same one used by the OpenPLC runtime. So whatever is installed in that interpreter is available to your block.

This includes:

- **The full Python 3 standard library** — `math`, `json`, `datetime`, `re`, `statistics`, `collections`, `itertools`, `hashlib`, and so on. These are always available.
- **Any third-party packages installed on the device** — if you `pip install` a package on the device running the OpenPLC runtime (NumPy, Requests, paho-mqtt, pyserial, anything you need), your Python blocks can import and use it.

The device controls which packages are installed, not the editor. Two devices can have different sets of packages, and a project that works on one may fail to import on the other if a dependency is missing. Plan ahead: document any non-stdlib packages your project needs and make sure they're installed on every target device before deploying.

```python
import math          # Always available — standard library
import statistics    # Always available — standard library

import numpy as np   # Available only if `pip install numpy` was run on the target device
import requests      # Same — depends on the target device's Python environment
```

If an `import` fails because a package isn't installed, the Python process for that block will exit with an error visible in the runtime logs.

> **Keep the four imports at the top of the template** (`shared_memory`, `struct`, `time`, `os`). They're required even if you don't reference them in your own code.

### What You Cannot Do

- **Install packages from inside a block** — `pip install` happens on the device, not from your block code. A block cannot install its own dependencies at runtime.
- **Import your own `.py` files from the project** — each Python function block is a self-contained script. There's no way to share Python helper modules across blocks within an Autonomy Edge project. (You can still import any module installed on the device.)

## The One Real Rule: `block_loop()` Must Return

Each Python block runs in its own process, isolated from the PLC. The PLC scan keeps going regardless of what your Python code does — slow Python doesn't stall the PLC. So most of what you might assume is forbidden in a "real-time" context is actually fine here. The one hard rule is:

**`block_loop()` must return on every call.** Inputs are refreshed before each call and outputs are sent to the PLC after each call. If `block_loop()` never returns, your block stops exchanging data with the PLC.

```python
# Don't do this — block_loop() never returns, so the next refresh never happens
def block_loop():
    while True:
        do_something()
        time.sleep(0.1)
```

If you genuinely need a long-running background activity (a server socket, a continuous polling loop, etc.), spawn a thread for it from `block_init()` and let `block_loop()` return immediately:

```python
import threading

worker_lock = threading.Lock()

def background_worker():
    global some_output
    while True:
        result = do_long_running_work()
        with worker_lock:
            some_output = result  # protected access to a variable shared with block_loop()

def block_init():
    t = threading.Thread(target=background_worker, daemon=True)
    t.start()

def block_loop():
    # block_loop() can stay short — the worker is doing its own thing in the background
    pass
```

When a thread reads or writes a variable from your Variables Table, hold a lock around the access. Those variables are refreshed between cycles, so without coordination a thread can read a half-updated value or have its own write overwritten by the next refresh. A simple `threading.Lock` is enough for most cases.

## Things That Are Fine (But Worth Knowing)

### Blocking Operations

Network requests, file I/O, `time.sleep()`, large reads — all fine. They block your Python script, but the PLC keeps scanning normally. The visible effect is that your block's outputs update less often: if `block_loop()` takes 500 ms, the next sync happens about 600 ms later (500 ms work + 100 ms sleep) instead of every 100 ms. Sometimes that's exactly what you want; sometimes you'd rather move the slow work to a background thread (see above) so the main loop stays responsive.

### Threads

`threading.Thread` works. The caveat is the same one above: any variable from the Variables Table that's touched by both `block_loop()` and a worker thread should be guarded by a lock, because those variables are refreshed every cycle.

### Subprocesses

`subprocess.run`, `os.system`, `os.popen` should all work — your Python process is already a normal OS process. As with any subprocess use, mind the runtime cost (spawning a process is much slower than calling a Python function, so don't do it on every loop) and clean up your child processes if you launch any long-running ones.

## Variable Constraints

- The set of variables your block exchanges with the PLC is fixed by the Variables Table — you can't add or remove inputs/outputs at runtime.
- Assigning to an input from inside `block_loop()` has no effect — the next cycle overwrites whatever you wrote with the fresh value from the PLC.
- Strings are limited to 126 characters; longer values are truncated when written to a STRING output.
- Array variables keep the length declared in the Variables Table. Don't `append`/`pop` on them.

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

3. **Validate inputs before processing** — Input values come from outside the block and can take any value the PLC writes. Check for division by zero, out-of-range values, and invalid states:

    ```python
    def block_loop():
        global result
        if divisor != 0.0:
            result = 100.0 / divisor
        else:
            result = 0.0
    ```

4. **Use `try/except` for robustness** — Wrap your logic in exception handling to prevent the process from crashing:

    ```python
    def block_loop():
        global result
        try:
            result = complex_calculation(value)
        except Exception as e:
            print(f'Error in block_loop: {e}')
            result = 0  # Safe default
    ```

5. **Minimize print() in block_loop()** — Use print statements for debugging during development, but remove or comment them out for production.

6. **Keep computations deterministic** — Avoid relying on external state (files, time-of-day) for critical outputs. If the same inputs should always produce the same outputs, your logic will be easier to test and debug.

7. **Pre-compute constants in block_init()** — If your calculation uses constant values (lookup tables, conversion factors), compute them once in `block_init()` and store them as global variables:

    ```python
    import math

    def block_init():
        global lookup_table
        lookup_table = [math.sin(i * math.pi / 180) for i in range(360)]

    def block_loop():
        global result
        # angle is a UINT input declared in the Variables Table
        result = lookup_table[angle % 360]
    ```

## What's Next?

Continue to [Python Editor Features](/docs/openplc-editor/custom-languages/python-blocks/python-language-server) to learn about syntax highlighting, type checking, autocompletion, and other editing tools available in the Python code editor.
