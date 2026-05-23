# Worked example: Python function block, data transform

Write a Python function block that converts a raw ADC integer (0–1023) into a temperature reading in degrees Celsius, then call it from an ST program. This is the pattern for any non-trivial maths or string processing that's easier to write in Python than in IEC.

**Surfaces exercised:** Python POU authoring, the Python LSP, the variables marshalling boundary, calling a function block instance from ST, the Simulator.

**Expected time:** about 10 minutes.

## Why Python instead of IEC?

The IEC scalar function library is comprehensive but not deep. For things like:

- Multi-step unit conversions with calibration constants,
- Lookup tables with interpolation,
- String parsing of an upstream sensor packet,
- Anything you'd reach for `numpy`-style math for,

Python wins on readability. The editor compiles Python FBs to a small C extension that the runtime invokes once per scan.

## The transform

A simple linear scaling, plus a calibration offset:

```
celsius = raw_adc * scale + offset
```

With `scale = 0.1` and `offset = -20.0`, a raw value of `0` reads as `−20°C` and a raw value of `1023` reads as `+82.3°C`. The sensor's data sheet would normally give you these constants.

## Step 1: Create the Python function block

1. In the project tree, click **`+`** at the top.
2. Pick **function-block**, name it `AdcToCelsius`, language **Python**.
3. Click **Create**. The new FB opens in the Python editor.

## Step 2: Declare the variables

Switch to the variables editor at the top. Add three rows:

| Name | Class | Type |
|---|---|---|
| `raw` | Input | INT |
| `out_c` | Output | REAL |
| `scale` | Input | REAL |

(Python function blocks only support `Input` and `Output` classes, no internal `Local` or `InOut`.)

Set the **Initial Value** of `scale` to `0.1`. The caller can override it, but the default makes the FB usable as-is.

## Step 3: Write the Python body

In the body editor:

```python
def execute(self):
    self.out_c = self.raw * self.scale + (-20.0)
```

That's it. Save.

The `self` object has one attribute per variable you declared. Reads come from inputs, writes go to outputs. The runtime calls `execute(self)` once per scan, marshalling values across the C↔Python boundary.

## Step 4: Use it from a program

Open `main` (or create a new ST program). Add variables:

| Name | Class | Type |
|---|---|---|
| `xform` | Local | AdcToCelsius |
| `raw_value` | Local | INT |
| `temperature_c` | Local | REAL |

`xform` is an **instance** of the function block you just authored, `AdcToCelsius` appears in the type picker under **User types** after you've created it.

In the ST body:

```iec
(* Simulate a raw ADC reading, replace with an actual %IW location in real use *)
raw_value := 512;

(* Call the FB instance *)
xform(raw := raw_value, scale := 0.1);
temperature_c := xform.out_c;
```

The first call sets the inputs and runs `execute`. `xform.out_c` is then the latest output value.

Save.

## Step 5: Run it

Click **Start Simulator**. After a few seconds the Debugger panel appears.

Tick the **Debug** column on `raw_value` and `temperature_c`. They appear in the Debugger:

- `raw_value` = `512`
- `temperature_c` = `31.2` (i.e. `512 * 0.1 - 20 = 31.2`)

## Step 6: Iterate

Open the Python FB body again. Change the formula:

```python
def execute(self):
    self.out_c = self.raw * self.scale + (-25.0)  # was -20.0
```

Save. Stop the Simulator, start it again. `temperature_c` is now `26.2`.

This is the inner loop: edit Python, hot-swap, observe.

## How values cross the boundary

The runtime translates `INT` and `REAL` to native Python `int` and `float`. `BOOL` becomes `bool`. Strings get more careful handling, they're packed via `struct.pack` per the FB's declared variable interface. See **[Python Variable Restrictions](../custom-languages/python-blocks/python-restrictions)** for the full list of supported types and the marshalling rules.

## Performance

Python FBs have a small per-call overhead, typically tens of microseconds for the marshal step. For most control loops (10–100 ms cycle), this is fine. For sub-millisecond loops, use C++ blocks instead, or inline the maths in ST.

## Troubleshooting

**The FB compiles but `out_c` is always 0.** Double-check `self.out_c` is being assigned. Python doesn't error on a typo, it just creates a new attribute that the runtime never sees. The output variable name in the table must match exactly.

**`AttributeError: 'AdcToCelsius' object has no attribute 'raw'` at runtime.** The variable's class is wrong. Inputs and outputs both need to be declared with the right class in the variables table.

**The Python block is unavailable in the new-element popover.** The Simulator and Runtime v4 support Python. If you're on Runtime v3 (or an Arduino-class target on the desktop), Python is disabled. Switch targets via the Orchestrators screen.

## Where to next

- **[Python Block Structure](../custom-languages/python-blocks/python-structure)**: the conceptual model of `execute(self)` and the `self` namespace.
- **[Python Programming Basics](../custom-languages/python-blocks/python-basics)**: full language reference, what's allowed inside an `execute`.
- **[C++ Function Blocks](../custom-languages/cpp-blocks/cpp-basics)**: the lower-latency cousin, with pointer-based variable access.
