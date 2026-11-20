# Worked example: Python function block, data transform

Write a Python function block that converts a raw ADC integer (0 to 1023) into a temperature reading in degrees Celsius, then call it from an ST program. This is the pattern for maths or string processing that is easier to write in Python than in IEC.

**Surfaces exercised:** Python POU authoring, the Python template, the exchange of inputs and outputs between the PLC and Python, calling a function block instance from ST, the Simulator.

**Expected time:** about 10 minutes.

## Why Python instead of IEC?

The IEC scalar function library is comprehensive but not deep. For things like:

- Multi-step unit conversions with calibration constants,
- Lookup tables with interpolation,
- String parsing of an upstream sensor packet,
- Anything you'd reach for numpy for,

Python wins on readability. Each instance of a Python block runs in its own Python interpreter, next to the PLC. About every 100 ms, the PLC sends the block its inputs, the block runs once, and it sends its outputs back. This exchange does not follow the PLC scan cycle, so use Python for work that is not time-critical.

## The transform

A simple linear scaling, plus a calibration offset:

```
celsius = raw_adc * scale + offset
```

With `scale = 0.1` and `offset = -20.0`, a raw value of `0` reads as `-20°C` and a raw value of `1023` reads as `+82.3°C`. The sensor's data sheet would normally give you these constants.

## Step 1: Create the Python function block

1. In the project tree, click **`+`** at the top.
2. Pick **Function Block**, name it `AdcToCelsius`, language **Python**.
3. Click **Create**. The new block opens in the Python editor, filled with this template:

```python
# ================================================================
# DISCLAIMER: Python Function Block Execution
#
# This block runs asynchronously from the main PLC runtime.
# ---------------------------------------------------------------
# - All variables are shared with the runtime through shared memory.
# - The block_init() function is called once when the block starts.
# - The block_loop() function is called periodically (~100ms).
# - IMPORTANT: This periodic call DOES NOT follow the PLC scan cycle.
#   It is NOT guaranteed that block_loop() will execute once per scan.
#
# Use this block for non-time-critical tasks. For logic that must
# match the PLC scan cycle, use standard IEC 61131-3 function blocks.
# ================================================================

from multiprocessing import shared_memory
import struct
import time
import os

def block_init():
    print('Block was initialized')

def block_loop():
    print('Block has run the loop function')
```

Keep the four `import` lines and both functions: the block needs them to run. `block_init()` runs once when the block starts. `block_loop()` runs about every 100 ms.

## Step 2: Declare the variables

Switch to the variables editor at the top. Add three rows:

| Name | Class | Type |
|---|---|---|
| `raw` | Input | INT |
| `scale` | Input | REAL |
| `out_c` | Output | REAL |

Each row becomes a Python variable with the same name. Before each `block_loop()` call, `raw` and `scale` hold the latest values from the PLC. After each call, the value of `out_c` goes back to the PLC.

## Step 3: Write the Python body

Change only `block_loop()`, at the bottom of the template. Leave the comment header, the imports and `block_init()` as they are. The end of the block now reads:

```python
def block_init():
    print('Block was initialized')

def block_loop():
    global out_c
    out_c = raw * scale + (-20.0)
```

Save.

Two things to notice:

- `global out_c` is required. In Python, assigning to a module-level variable from inside a function needs `global`. Without it, `out_c` is a new local variable, and the PLC never sees the value.
- Inputs need no `global`, because the code only reads them.

The template's `print` in `block_loop()` is gone on purpose: it would print a line every 100 ms. The `print` in `block_init()` shows one line on the Console when the block starts.

## Step 4: Use it from a program

Open `main` (or create a new ST program). Add variables:

| Name | Class | Type |
|---|---|---|
| `xform` | Local | AdcToCelsius |
| `raw_value` | Local | INT |
| `temperature_c` | Local | REAL |

`xform` is an **instance** of the function block you just wrote. `AdcToCelsius` appears in the type picker under **User types** after you've created it.

In the ST body:

```iec
(* Simulate a raw ADC reading, replace with an actual %IW location in real use *)
raw_value := 512;

(* Call the FB instance *)
xform(raw := raw_value, scale := 0.1);
temperature_c := xform.out_c;
```

The call hands the inputs to the block. `xform.out_c` holds the latest output the block sent back. Because the exchange runs about every 100 ms and not once per scan, the first scans read `0.0` until the block has run once.

Save.

## Step 5: Run it

Click **Start Simulator**. The editor builds the project, prepares a Python interpreter for `xform`, and starts the program. After a few seconds the Debugger panel appears.

Open the **Console** tab: it shows `[AdcToCelsius] Block was initialized`. The name in brackets tells you which block printed the line.

Tick the **Debug** column on `raw_value` and `temperature_c`. They appear in the Debugger:

- `raw_value` = `512`
- `temperature_c` = `31.2` (that is, `512 * 0.1 - 20 = 31.2`)

## Step 6: Iterate

Click **Stop Simulator**. Open the Python block again and change the offset:

```python
def block_loop():
    global out_c
    out_c = raw * scale + (-25.0)  # was -20.0
```

Save, then click **Start Simulator** again. `temperature_c` is now `26.2`.

This is the inner loop: edit the Python code, restart the Simulator, observe.

## How values cross the boundary

`INT` and the other integer types arrive in Python as `int`, `REAL` and `LREAL` as `float`, and `BOOL` as `bool`. Strings have a maximum length. See **[Python Variable Restrictions](../custom-languages/python-blocks/python-restrictions)** for the full list of supported types.

## Timing

The block and the PLC exchange values about every 100 ms, whatever the PLC's cycle time. A value the PLC writes can take up to one exchange to reach Python, and the result takes up to one more exchange to come back. For logic that must follow the scan cycle, use an IEC function block instead.

## Troubleshooting

**The block runs but `out_c` is always 0.** Check that `block_loop()` starts with `global out_c`. Without it, the assignment creates a local variable and the PLC never sees it. Also check that the name in the code matches the name in the variables table exactly.

**The Console shows a `NameError` for the block.** The code reads a name that is not in the variables table, often a typo. The block stops, its outputs keep their last values, and the PLC keeps running. Fix the name and start the Simulator again.

**The Python block is unavailable in the new-element popover.** The Simulator and Runtime v4 support Python. If you're on Runtime v3 (or an Arduino-class target on the desktop), Python is disabled. Switch targets via the Edge Devices screen.

## Where to next

- **[Python Block Structure](../custom-languages/python-blocks/python-structure)**: `block_init()`, `block_loop()`, and how the variables table maps to Python variables.
- **[Python Programming Basics](../custom-languages/python-blocks/python-basics)**: the template and a first example.
- **[C++ Function Blocks](../custom-languages/cpp-blocks/cpp-basics)**: the other way to write a block in a general-purpose language.
- **[Running with the Simulator](../building-deploying/simulator)**: how Python blocks run on the Simulator.
