# Variables editor

The variables editor is the table at the top of every POU body. It lists each variable declared for that POU and lets you edit, add, remove, and reorder them. A toggle in the top-right corner switches between **table mode** (the default) and **code mode** (raw `VAR ... END_VAR` text).

![Variables editor for the EDF Demo main program: toolbar with Description field, Class Filter dropdown, +/-/up/down buttons, and a table/code mode toggle; three rows below showing blink (Local BOOL), TON0 (Local TON), TOF0 (Local TOF)](images/variables-table.png)

## Class, the column users get wrong the most

> **Heads up.** **The `Input` class is not how you read a physical input pin.** If you want a variable that's wired to a digital input (`%IX0.0`), or any other physical I/O, leave the class as `Local` (or `Output` if the variable ends with `:=` writes) and fill in the **`Location`** column instead. The `Input` class is for something else entirely. Read on.

In IEC 61131-3 the word "class" doesn't mean what most engineers expect. It refers to the **role a variable plays inside its POU's interface**, not how it's connected to the outside world. A variable's class answers the question: "who is allowed to read or write this from outside the POU?"

The six classes in this build:

| Class | What it actually means | Practical use |
|---|---|---|
| **Local** | Private to the POU. No outside caller can pass a value in or read one out. Survives across PLC scans inside Programs and Function Blocks (re-initialised every call inside Functions). | The default. Use this for **anything internal** to your program, counters, intermediate calculations, state flags. Also use this when you want to **read or write a physical I/O point** via the `Location` column. |
| **Input** | Declared as `VAR_INPUT`. Becomes an **input pin** on the function block when drawn in LD / FBD. The caller writes the value; your POU code reads it. **Has nothing to do with `%IX` physical inputs.** | Function block parameters: `enable`, `setpoint`, `target_temp`. Defines the calling interface of a custom FB or Function. |
| **Output** | Declared as `VAR_OUTPUT`. Becomes an **output pin** on the function block. Your POU code writes the value; the caller reads it. Again, **not** related to `%QX` physical outputs. | Return values from a function block: `motor_running`, `error_code`, `current_temp`. |
| **In Out** | Declared as `VAR_IN_OUT`. The pin is bidirectional, the caller passes a reference, your POU can both read and write it, and the change is visible to the caller after the call. | A buffer or accumulator that the caller wants the FB to mutate in place. Less common than Input + Output. |
| **External** | Declared as `VAR_EXTERNAL`. References a `Global` variable declared in the **Resource** editor. The `Location` is inherited from the global, you don't set it on the row. | Reading or writing a global from inside a POU. See **[Global variables](global-variables)**. |
| **Temp** | Declared as `VAR_TEMP`. Like `Local`, but the value is **reset to zero / FALSE at every scan**. | Loop counters and scratch values you genuinely don't need to persist. Programs and Function Blocks; not Functions (every function variable is already temp by nature). |

Choose **Input** / **Output** / **In Out** when you're building a **function block or function** that other parts of your project will call. Choose **Local** for everything else, including variables wired to physical I/O.

For Python and C++ function blocks, only `Input` and `Output` classes are offered. Internal state has to be modelled as struct members or static variables in the Python / C++ body.

## Reading and writing physical I/O, `Location`

Physical I/O mapping lives in the **`Location`** column, not in the `Class` column. The address you type tells the runtime which bit, byte, word, or register of the PLC's I/O image this variable is bound to.

### IEC address format

```
%I X 0.0
 │ │ │
 │ │ └── address (byte and bit for X, byte for B, word for W/D/L)
 │ └──── size: X bit, B byte, W word, D double word, L long word
 └────── area: I input, Q output, M memory
```

| Prefix | Area | Direction | Example variable | Physical meaning |
|---|---|---|---|---|
| `%I` | Input image | Read by your program | `start_btn : BOOL` at `%IX0.0` | Reads digital input pin 0.0 every scan |
| `%Q` | Output image | Written by your program | `motor : BOOL` at `%QX0.0` | Writes digital output pin 0.0 every scan |
| `%M` | Memory area | Read+write, no physical pin | `running_total : INT` at `%MW3` | Working memory the program owns. Retentive across PLC restarts (where the runtime supports retain). Also: this is what Modbus / OPC-UA / S7Comm servers expose to external clients. |

The size letter sets how many bits the variable consumes:

| Letter | Width | Use with types |
|---|---|---|
| `X` | 1 bit | `BOOL` |
| `B` | 8 bits | `BYTE`, `SINT`, `USINT` |
| `W` | 16 bits | `WORD`, `INT`, `UINT` |
| `D` | 32 bits | `DWORD`, `DINT`, `UDINT`, `REAL` |
| `L` | 64 bits | `LWORD`, `LINT`, `ULINT`, `LREAL` |

Bit addresses use `byte.bit` notation: `%IX0.0`, `%IX0.7`, `%IX1.0` (rolls over to the next byte). See **[Modbus addressing](../communication/modbus/addressing)** for how these IEC addresses end up on the wire when an external client reads them.

### Common patterns

**Reading a physical button / switch:**

```
Name        Class  Type  Location
start_btn   Local  BOOL  %IX0.0
e_stop      Local  BOOL  %IX0.1
```

Both are `Local`. The `Location` does the I/O mapping; the `Class` is just "internal to this POU."

**Driving a physical output:**

```
Name        Class  Type  Location
motor       Local  BOOL  %QX0.0
alarm_lamp  Local  BOOL  %QX0.1
```

Same idea: `Local` class, `Location` does the work.

**Exposing a value to an external Modbus client:**

```
Name           Class  Type  Location
process_temp   Local  REAL  %MD2
```

`%MD2` (32-bit double in memory) is where the Modbus server would map a holding register the SCADA system reads. See the **[Modbus server](../communication/modbus/server)** page for the buffer mapping.

### Aliases, when the `Location` is set for you

For variables that come from a producer (a Modbus master remote device, an EtherCAT slave channel, a board pin map on the desktop editor), you don't type the location yourself. The producer **owns** it and writes it into the row through the alias registry. You see the resolved `Location` in the table and use the variable like any other. If the producer moves the underlying address, the row updates automatically on the next save.

If the producer goes away (you delete the remote device or the EtherCAT channel), the variable becomes **orphaned**. The editor marks the row with an amber warning glyph and a hover tooltip explaining how to fix it (re-bind or remove).

## All columns

| Column | Notes |
|---|---|
| **#** | Row index. Not editable; visual only. |
| **Name** | Identifier. Must be unique within the POU and follow IEC naming rules: `a-z`, `A-Z`, `0-9`, `_`; can't start with a digit; case-insensitive in IEC matching. |
| **Class** | One of the six classes above. For Python / C++ FBs only `Input` and `Output` are offered. For globals (in the Resource editor) the class is always `Global`. |
| **Type** | The data type. Base IEC scalar types, custom types from the Data Types section, arrays, or derived types (a function block instance). See the type picker below. |
| **Location** | Optional IEC address. Shown for Programs and Function Blocks. Cleared automatically if you switch the class to `External` (externals inherit from their global). |
| **Initial Value** | Optional. Cold-start value. Defaults: `FALSE` for BOOL, `0` for numerics, empty for strings. |
| **Documentation** | Free-text. Shows in hover tooltips inside the body editor and in the variable picker autocomplete. |
| **Debug** | Per-row checkbox. When on, the variable is streamed to the **[Debugger](../building-deploying/debugger)** chart during a debug run. |

A **class filter** dropdown above the table (`All` / `Local` / `Input` / `Output` / `InOut` / `External` / `Temp`) hides rows of the other classes. It's a view-only filter; the hidden variables are still declared.

## Toolbar, adding, removing, reordering

The four small icons in the top-right of the table:

| Icon | Action |
|---|---|
| **`+`** | Add a new row. If a row is selected, the new row is inserted below it and inherits the selected row's class + type. Otherwise it's appended at the end. |
| **`−`** | Remove the selected row(s). If the variable is used in the body, the references are flagged in the next compile (or, in graphical bodies, immediately as red text). |
| **`↑` / `↓`** | Move the selected row up or down. Order matters, positional call sites (e.g. `my_fb(true, 5, 100)` without named arguments) pass values in declared order. |

To **rename**, double-click the Name cell, type, hit Enter. The editor walks the bodies to find every reference and updates them in one pass. If the variable is referenced in graphical bodies (LD, FBD), a **Rename Impact** dialog lists every reference before applying.

To **change class**, click the Class cell and pick from the dropdown. Two side effects:

- Switching to `External` clears the `Location` (externals resolve their address from the matching global).
- Switching away from `Local` to `Input` / `Output` / `In Out` / `Temp` clears the `Location` too (only `Local` and Program-scope variables hold direct addresses).

## Type picker

Click the Type cell. The dropdown groups available types:

- **Base types**: IEC scalars: `BOOL`, `BYTE`, `WORD`, `DWORD`, `LWORD`, `SINT`, `INT`, `DINT`, `LINT`, `USINT`, `UINT`, `UDINT`, `ULINT`, `REAL`, `LREAL`, `TIME`, `DATE`, `TIME_OF_DAY`, `DATE_AND_TIME`, `STRING`, `WSTRING`.
- **User data types**: types you defined in the project's **Data Types** section: arrays, enumerations, structures.
- **Library types**: types exposed by enabled libraries. Most commonly **function block instance types** (`TON`, `CTU`, `RS`, etc.), declaring a variable as `TON` gives you a `TON` instance you can call from the body.
- **Array**: opens a sub-dialog to define an inline array (`ARRAY[0..9, 0..3] OF INT`). For arrays you reuse, define them in Data Types instead.

## Table mode vs code mode

The toggle in the top-right switches the view. Both modes show the **same** variables, they're two ways of editing the same data.

**Table mode** is the default. Spreadsheet-like, faster for small edits, every column is a typed input.

**Code mode** is the raw IEC declaration text. Same content rendered as `VAR_INPUT / VAR / VAR_OUTPUT / VAR_EXTERNAL` blocks, edited in the Monaco editor.

![Variables editor in code mode showing raw IEC syntax: VAR_INPUT block with `blink : BOOL;` and END_VAR. The toggle in the top-right is highlighted](images/variables-code-mode.png)

Code mode is fastest for:

- Pasting a chunk of declarations from another project.
- Bulk-renaming with multi-cursor edits.
- Auditing exactly what was declared without scrolling a long table.

When you switch back to table mode, the editor parses the text. Syntax errors prevent the switch and surface as red squiggles with hover messages.

Compare these two views, they describe the same declaration:

| Table mode | Code mode |
|---|---|
| `Name: setpoint, Class: Input, Type: REAL, Initial Value: 50.0` | `VAR_INPUT setpoint : REAL := 50.0; END_VAR` |
| `Name: counter, Class: Local, Type: INT, Initial Value: 0` | `VAR counter : INT := 0; END_VAR` |
| `Name: motor, Class: Local, Type: BOOL, Location: %QX0.0` | `VAR motor AT %QX0.0 : BOOL; END_VAR` |

## Function-specific fields

A `function` POU has two extra fields above the variable table:

- **Return type**: the type of the value the function returns. Required (every IEC function returns something).
- **POU description**: free text describing what the function does. Surfaces in the function picker and IntelliSense tooltips.

Function blocks and programs don't have these fields.

## Common mistakes

### "I want to read a button so I set the class to `Input`"

Wrong. The button is a physical input pin (`%IX0.0`), wired into the PLC. Mapping a variable to it goes in the **`Location`** column, not the **`Class`** column. Set class to `Local`, set Location to `%IX0.0`, leave the rest at defaults.

If you set the class to `Input` and don't put anything in `Location`, you get a function-block parameter that no caller is feeding, it'll always read as `FALSE`. The button on the panel will press and nothing happens.

### "My output won't turn on, its class is `Output`"

Same mistake, mirror image. `Output` class makes the variable an **FB output pin**, a value your POU writes for a caller to read. It doesn't write to a physical output unless something else (a parent POU or, traditionally, a wiring assignment in the resource configuration) takes that output pin and forwards it to `%QX0.0`. The simple path: `Local` class, `Location: %QX0.0`, and your program writes the variable directly.

### "I changed a variable's class and the location disappeared"

Expected behaviour. `Location` only makes sense for class `Local` (in Programs) and class `Local` inside Function Blocks. Switching away clears the field so you don't end up with an FB input that thinks it owns a physical pin.

### "I want a variable to keep its value between scans, do I use Retain?"

In Programs and Function Blocks, **`Local` class variables already retain their values between scans**, that's the normal IEC behaviour. `Temp` is the opposite: it explicitly **resets to zero / FALSE every scan**. `RETAIN` (a separate IEC keyword) means "survive a PLC restart"; this build doesn't expose a retain flag in the table editor, it's available in code mode by typing `VAR RETAIN ... END_VAR` directly.

### "I see two variables that look like duplicates after a copy/paste"

IEC names are case-insensitive. `motor` and `Motor` count as the same name. The editor flags the conflict on the next save.

## Globals

For project-wide variables, use the **Resource** editor (the **Resource** entry in the project tree). It contains a Globals section that looks and behaves identically to the per-POU table, but the class is always `Global`. POU-level variables can then declare class `External` and reference a global by name.

See **[Global variables](global-variables)** for the full Resource walkthrough.

## What's next

- **[Custom Data Types](../custom-data-types/creating-datatypes)**: define arrays, enumerations, and structures.
- **[Modbus addressing](../communication/modbus/addressing)**: how `%IX/%QX/%MW` map to wire-protocol addresses.
- **[Debugger](../building-deploying/debugger)**: what the **Debug** checkbox actually does.
