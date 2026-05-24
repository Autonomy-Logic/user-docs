# Variable classes inside a POU

Every variable you declare inside a Program Organization Unit (POU), a Program, Function, or Function Block, has a **class**. In IEC 61131-3 the class describes the variable's role in the POU: whether it's private to the POU, part of its calling interface, a reference to a global, or scratch space that doesn't persist between scans.

This page covers each class conceptually. For how to edit the variable table in the editor, adding rows, typing addresses, switching modes, see **[Variables editor](variables-editor)**.

![Variables table for the EDF Demo `main` program showing three Local variables: `blink` (BOOL), `TON0` (TON instance), `TOF0` (TOF instance)](images/variables-table.png)

## Local, `VAR`

The default. A local variable is private to the POU: no caller passes it in and no caller reads it back. In Programs and Function Blocks, local variables **retain their value across scans**, which is what makes counters, latches, state machines, and any logic with memory work.

```iec
VAR
    counter : INT := 0;
    running : BOOL;
    setpoint : REAL := 75.0;
END_VAR
```

In Functions, local variables behave differently: a function's frame is fresh on every call, so locals are re-initialised every time.

When to choose Local: anything internal to the POU. Counters, accumulators, intermediate calculation results, state flags, timer instances. Also anything you want bound to a specific I/O address via the `Location` column, that mapping is done with the address, not by changing the class.

## Input, `VAR_INPUT`

A parameter the caller passes in when invoking the POU. Inside the POU, an input is **read-only**: your code reads it; only the caller can write it.

```iec
VAR_INPUT
    enable : BOOL;
    target_temp : REAL;
    max_speed : INT := 1000;
END_VAR
```

When another POU calls this function block, it supplies the inputs:

```iec
my_controller(enable := TRUE, target_temp := 72.5, max_speed := 500);
```

In a graphical body, an `Input`-class variable becomes a pin on the **left** side of the function block. When you drop a TON timer onto a Ladder rung, its `IN` and `PT` pins are exactly this: `VAR_INPUT IN : BOOL; PT : TIME; END_VAR` inside the TON definition.

When to choose Input: only on Functions and Function Blocks, and only for values another POU is meant to feed in. A Program is the top of the call chain, its variables are inputs to "the world" via the Location column, not to a caller.

## Output, `VAR_OUTPUT`

The mirror of Input. An output is **read-write inside the POU and read-only outside**: your POU code writes the value; the caller reads it after the call returns.

```iec
VAR_OUTPUT
    motor_on : BOOL;
    current_speed : INT;
    error_code : INT;
END_VAR
```

The caller reads outputs through dot notation on the function-block instance:

```iec
my_controller(enable := TRUE, target_temp := 72.5);
IF my_controller.error_code <> 0 THEN
    alarm := TRUE;
END_IF;
```

In LD or FBD, an `Output`-class variable becomes a pin on the **right** side of the block, like TON's `Q` and `ET` pins.

When to choose Output: only on Functions and Function Blocks, and only for values another POU is meant to consume.

## In Out, `VAR_IN_OUT`

Bidirectional. The caller passes a variable **by reference**; the POU can read and write it; changes are visible to the caller after the call.

```iec
VAR_IN_OUT
    shared_buffer : ARRAY[0..99] OF INT;
    accumulator : REAL;
END_VAR
```

The caller has to pass an actual variable (not a literal):

```iec
VAR
    my_buffer : ARRAY[0..99] OF INT;
    my_total : REAL;
END_VAR

process_data(shared_buffer := my_buffer, accumulator := my_total);
(* my_buffer and my_total may have been modified in place *)
```

When to choose In Out: large data structures you don't want to copy in and back out (arrays, structures), or accumulators a function block needs to update for the caller.

## External, `VAR_EXTERNAL`

A reference to a Global variable declared in the **Resource**. The External declaration doesn't create a new variable, it links to an existing global by name and type.

```iec
VAR_EXTERNAL
    system_mode : INT;
    emergency_stop : BOOL;
END_VAR
```

For the External to work, a `VAR_GLOBAL` with the same name and same type must exist in the Resource editor. Reading or writing the External inside the POU reads or writes the underlying global; any other POU with a matching External sees the change on the next scan.

When to choose External: when the same value needs to be visible to several POUs across the project. Setpoints, machine-wide modes, emergency-stop flags. Anything that's project-wide rather than per-POU.

Per-POU values that just happen to be bound to physical I/O (a digital input or a digital output your program owns) are not Externals, they're `Local` with a `Location`. Externals exist to share **state between POUs**, not to map to **pins**.

See **[Global variables](global-variables)** for the Resource side.

## Temp, `VAR_TEMP`

Like `Local`, but **reset to the initial value (or zero / FALSE) at the start of every scan**. Programs and Function Blocks only; functions are already temp by nature.

```iec
VAR_TEMP
    intermediate_result : REAL;
    loop_index : INT;
END_VAR
```

When to choose Temp: scratch values that genuinely don't need to persist between scans. Loop counters, intermediate results in a per-scan computation, working values you'd otherwise have to remember to zero at the top of every scan.

## Retention summary

How each class behaves across scan cycles:

| Class | Retained across scans? | Notes |
|---|---|---|
| Local (Program / FB) | Yes | The IEC default for stateful logic. |
| Local (Function) | No | Fresh frame on every call. |
| Input | Set by caller | The caller writes it on every invocation. |
| Output | Yes (FBs) | FB outputs persist until the next call rewrites them. |
| In Out | References caller | The caller's variable retains based on its own class. |
| External | Yes | The underlying global is retained for the lifetime of the project. |
| Temp | No | Reset to initial value at the start of every scan. |

`RETAIN` is a separate IEC concept that means "survive a PLC restart" (power cycle), implemented as `VAR RETAIN ... END_VAR`. The table editor doesn't expose a retain flag in this build; declare it directly in code mode if you need it.

## Picking a class in practice

A short flowchart for the most common cases:

| You want… | Class | Notes |
|---|---|---|
| To count, latch, or otherwise remember a value within one POU | **Local** | The default. |
| To read or write a physical I/O pin from a Program | **Local** | Set the `Location` to `%IX...` / `%QX...`. The class stays Local. |
| To define an input pin on a custom Function Block | **Input** | Only useful for FBs and Functions. |
| To define an output pin on a custom Function Block | **Output** | Same constraint. |
| To share a value across multiple POUs | **External** (in each POU) + **Global** (in the Resource) | The same name and type on both ends. |
| Scratch variables that you don't want to persist | **Temp** | Reset every scan. |

## Naming rules

- ASCII letters, digits, and underscores. Can't start with a digit.
- Names are **case-insensitive** in IEC matching. `motor` and `Motor` are the same identifier and will collide.
- Reserved keywords (`VAR`, `END_VAR`, `IF`, `TRUE`, `BOOL`, etc.) are not allowed as names.

## What's next

- **[Variables editor](variables-editor)**: the editor UI: columns, dropdowns, code mode, locations.
- **[Global variables](global-variables)**: the Resource side of the External relationship.
- **[Modbus addressing](../communication/modbus/addressing)**: how IEC addresses map to wire-protocol addresses.
