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

If your `block_loop()` takes longer than 100 ms to execute, the next iteration starts immediately after the current one finishes. There's no backlog of missed cycles.

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

Python function blocks run inside the Python interpreter on the target device. The same one used by the OpenPLC runtime. So whatever is installed in that interpreter is available to your block.

This includes:

- **The full Python 3 standard library**: `math`, `json`, `datetime`, `re`, `statistics`, `collections`, `itertools`, `hashlib`, and so on. These are always available.
- **Any third-party packages installed on the device**: if you `pip install` a package on the device running the OpenPLC runtime (NumPy, Requests, paho-mqtt, pyserial, anything you need), your Python blocks can import and use it.

The device controls which packages are installed, not the editor. Two devices can have different sets of packages, and a project that works on one may fail to import on the other if a dependency is missing. Plan ahead: document any non-stdlib packages your project needs and make sure they're installed on every target device before deploying.

```python
import math          # Always available. Standard library
import statistics    # Always available. Standard library

import numpy as np   # Available only if `pip install numpy` was run on the target device
import requests      # Same. Depends on the target device's Python environment
```

If an `import` fails because a package isn't installed, the Python process for that block will exit with an error visible in the runtime logs.

> **Keep the four imports at the top of the template** (`shared_memory`, `struct`, `time`, `os`). They're required even if you don't reference them in your own code.

The generated wrapper that surrounds your script uses all four and does not import them itself. Dropping one is easy to do — they look unused — and the symptom is misleading: the block starts, exits about a second later, and the log says

```
[Python] PLC runtime has stopped.
[Python] Stopping Python block: MyBlock
```

The runtime has not stopped. The wrapper's liveness check calls `os.kill(plc_pid, 0)`, that raises `NameError` because `os` was never imported, and the handler reports it as a stopped runtime. If you see that message while the PLC is plainly still running, check your imports first.

### What You Cannot Do

- **Install packages from inside a block**: `pip install` happens on the device, not from your block code. A block cannot install its own dependencies at runtime.
- **Import your own `.py` files from the project**: each Python function block is a self-contained script. There's no way to share Python helper modules across blocks within an Autonomy Edge project. (You can still import any module installed on the device.)

## The One Real Rule: `block_loop()` Must Return

Each Python block runs in its own process, isolated from the PLC. The PLC scan keeps going regardless of what your Python code does. Slow Python doesn't stall the PLC. So most of what you might assume is forbidden in a "real-time" context is actually fine here. The one hard rule is:

**`block_loop()` must return on every call.** Inputs are refreshed before each call and outputs are sent to the PLC after each call. If `block_loop()` never returns, your block stops exchanging data with the PLC.

```python
# Don't do this: block_loop() never returns, so the next refresh never happens
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
    # block_loop() can stay short. The worker is doing its own thing in the background
    pass
```

When a thread reads or writes a variable from your Variables Table, hold a lock around the access. Those variables are refreshed between cycles, so without coordination a thread can read a half-updated value or have its own write overwritten by the next refresh. A simple `threading.Lock` is enough for most cases.

## Things That Are Fine (But Worth Knowing)

### Blocking Operations

Network requests, file I/O, `time.sleep()`, large reads. All fine. They block your Python script, but the PLC keeps scanning normally. The visible effect is that your block's outputs update less often: if `block_loop()` takes 500 ms, the next sync happens about 600 ms later (500 ms work + 100 ms sleep) instead of every 100 ms. Sometimes that's exactly what you want; sometimes you'd rather move the slow work to a background thread (see above) so the main loop stays responsive.

### Threads

`threading.Thread` works. The caveat is the same one above: any variable from the Variables Table that's touched by both `block_loop()` and a worker thread should be guarded by a lock, because those variables are refreshed every cycle.

### Subprocesses

`subprocess.run`, `os.system`, `os.popen` should all work. Your Python process is already a normal OS process. As with any subprocess use, mind the runtime cost (spawning a process is much slower than calling a Python function, so don't do it on every loop) and clean up your child processes if you launch any long-running ones.

## Variable Constraints

- The set of variables your block exchanges with the PLC is fixed by the Variables Table. You can't add or remove inputs/outputs at runtime.
- Assigning to an input from inside `block_loop()` has no effect. The next cycle overwrites whatever you wrote with the fresh value from the PLC.
- Strings are limited to 126 characters; longer values are truncated when written to a STRING output.
- Array variables keep the length declared in the Variables Table. Don't `append`/`pop` on them.

## Shared Globals (VAR_EXTERNAL): One Writer Only

A Python block can declare a `VAR_EXTERNAL` to reach a global from the project's configuration, and read and write it like any other variable. But because your block runs in a separate process, updating a global is **not** the atomic operation it is in ST, LD or C++. This is the one place where the process boundary changes the meaning of your code rather than just its timing, so it's worth understanding before you rely on it.

### What actually happens

Your block never touches the global directly. Each cycle:

1. The PLC reads the global's current value and sends it in with your inputs.
2. Your `block_loop()` runs, in a different process, and may change its copy.
3. The PLC takes your copy back and stores it into the global.

Steps 1 and 3 each take the global's lock, so you never see or write a half-updated value. What isn't protected is the gap between them — and your block's whole cycle sits in that gap.

### The consequence: lost updates

If anything else writes the same global while your block is mid-cycle, step 3 overwrites it. Your block sends back a value computed from what it read at step 1, which is now stale.

So this line does **not** reliably increment a shared counter:

```python
def block_loop():
    global shared_count
    shared_count = shared_count + 1   # unsafe if anything else also writes shared_count
```

> **Warning:** In ST, LD or C++, `shared_count := shared_count + 1;` completes inside a single scan while holding the global's lock, so no update is lost. The same line in a Python block does not, because the read and the write happen a cycle apart in another process.

Measured on real hardware: a Python block and a C++ block each adding 2 to the same global, every cycle. The global held consistently **two thirds** of the total the two blocks had added between them. The missing third is updates that were read, added to, and then overwritten.

| Where the code runs | `g := g + 1` with another writer |
|---|---|
| ST / LD / FBD / IL | Safe. Read-modify-write completes in one scan under the global's lock |
| C++ function block | Safe. Same. The block runs inside the scan |
| **Python function block** | **Unsafe. Updates from other tasks in the same window are lost** |

### How to use globals safely from Python

- **Give each global a single writer.** If your Python block writes a global, nothing else should. That case is exact, with no lost updates at all.
- **Read freely.** Reading a global from Python is always safe. You may read a value that is a cycle old, but never a corrupt one.
- **Don't accumulate into a shared global.** If several tasks must contribute to one total, have each write its own contribution to its own variable and let an ST block add them up. The addition then happens inside the scan, where it is atomic.
- **Don't use a global as a lock or a semaphore** between a Python block and the rest of the program. Test-and-set cannot work across the boundary; two blocks can both see it free.

This is a deliberate trade. Holding the global's lock from step 1 to step 3 would make Python's read-modify-write atomic, but it would also block every other task that touches that global for a whole Python cycle (~100 ms), which is far worse for the rest of your program.

## Function Block Instances: The PLC Calls Them For You

You can declare a function block instance in a Python block's Variables Table — a `TON`, a counter, one of your own function blocks — and use its pins exactly as you would in ST.

What you cannot do is *call* it. `ton0()` has no meaning in Python: your block runs in a separate process, and the instance lives in the PLC's. You don't need to. **The PLC calls every instance your block declares, once per scan cycle**, and your Python code just reads and writes the pins.

```python
def block_loop():
    global elapsed, finished
    ton0.IN = start_signal      # drive the timer's inputs
    ton0.PT = 5_000_000_000     # T#5s, in nanoseconds

    finished = ton0.Q           # read what the instance produced
    elapsed = ton0.ET
```

Declare it the way you always would:

```
VAR
  ton0 : TON;
END_VAR
```

### Pin names are upper-cased

The compiler upper-cases members, so the pins are `ton0.IN`, `ton0.PT`, `ton0.Q`, `ton0.ET` — even if your own function block declares them in lower case. `ton0.in` would be a Python keyword anyway.

### What you can write, and what you can only read

| Pin kind | From Python |
|---|---|
| The block's inputs (`IN`, `PT`, …) | read and write |
| The block's in-outs | read and write |
| The block's outputs (`Q`, `ET`, …) | **read only** |
| The block's internal state | not available |

Assigning to an output has no effect, for the same reason assigning to one of your own inputs has none: the next cycle overwrites it. Internal state is deliberately not exposed — it belongs to the instance, and writing it from outside would corrupt the block.

### Outputs are one cycle behind

> **Tip:** Setting an input and reading an output in the same `block_loop()` does **not** give you the result of this cycle's call.

The sequence per scan is: the PLC applies what your block wrote, calls the instance, then publishes what it produced. Your block sees that on its *next* cycle. So:

```python
def block_loop():
    global result
    ton0.IN = True
    result = ton0.Q     # still the PREVIOUS cycle's value, not this one's
```

This is the same one-cycle lag every Python input already has (see [The ~100 ms Loop](#the-100-ms-loop) above) — it is just easier to overlook here, because setting a pin and reading a pin on adjacent lines *looks* synchronous. For logic where that matters, put the function block in an ST block instead.

### The instance runs every scan, not every Python cycle

The PLC calls the instance on its own scan cycle, which is typically much faster than your block's ~100 ms loop. A `TON` therefore keeps accurate time regardless of how often your Python code looks at it — the timer is not being driven by Python's cadence, only observed by it.

If your block declares several instances, they are called in the order they appear in the Variables Table.

### Controlling whether your block runs at all

Use the `EN` / `ENO` pins that every function block instance has:

```
myPyBlock(EN := systemReady);
running := myPyBlock.ENO;
```

When `EN` is false the block does not execute — and neither do the instances it declares.

### What is still not supported

- **An array of function block instances** (`ARRAY [0..3] OF TON`) is refused.
- **A generic pin** (`ANY_NUM` and friends) has no concrete type until it is wired, so a block with one cannot cross. The compiler names the pin it could not describe.

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
    print('MyBlock: initialized')  # Good. One-time message

def block_loop():
    # print(f'value: {value}')  # Avoid in production. Prints every 100 ms
    pass
```

## Best Practices

1. **Initialize in `block_init()`, compute in `block_loop()`**: Keep the separation clean. All one-time setup goes in `block_init()`, all cyclic logic goes in `block_loop()`.

2. **Use `global` for persistent state**: Variables that need to survive between `block_loop()` calls must be declared `global` at the top of the function.

3. **Validate inputs before processing**: Input values come from outside the block and can take any value the PLC writes. Check for division by zero, out-of-range values, and invalid states:

    ```python
    def block_loop():
        global result
        if divisor != 0.0:
            result = 100.0 / divisor
        else:
            result = 0.0
    ```

4. **Use `try/except` for robustness**: Wrap your logic in exception handling to prevent the process from crashing:

    ```python
    def block_loop():
        global result
        try:
            result = complex_calculation(value)
        except Exception as e:
            print(f'Error in block_loop: {e}')
            result = 0  # Safe default
    ```

5. **Minimize print() in block_loop()**: Use print statements for debugging during development, but remove or comment them out for production.

6. **Keep computations deterministic**: Avoid relying on external state (files, time-of-day) for critical outputs. If the same inputs should always produce the same outputs, your logic will be easier to test and debug.

7. **Pre-compute constants in block_init()**: If your calculation uses constant values (lookup tables, conversion factors), compute them once in `block_init()` and store them as global variables:

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
