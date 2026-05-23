# Variables Editor

The variables editor is the table at the top of every POU body. It lists each variable declared for that POU and lets you edit, add, remove, and reorder them. A toggle in the top-right corner switches between **table mode** (default) and **code mode** (raw `VAR ... END_VAR` text).

## Columns

| Column | Notes |
|---|---|
| **#** | Row index. Not editable. |
| **Name** | Identifier. Must be unique within the POU and follow IEC naming rules (`a-z`, `A-Z`, `0-9`, `_`; can't start with a digit). |
| **Class** | One of `Local`, `Input`, `Output`, `InOut`, `External`, `Temp`. For Python and C++ function blocks only `Input` and `Output` are offered. For globals (in the Resource editor), the class is always `Global`. |
| **Type** | The data type. Base types, custom types you defined in the Data Types section, arrays, or `derived` (an instance of a function block). |
| **Location** | IEC address (`%IX0.0`, `%QW3`, `%MD5`, `%MX0.7`, etc.). Shown for **Programs** and for **Function Blocks**; hidden for **Functions** and for `External` variables (those resolve their address from the global they reference). |
| **Initial Value** | Optional. The value the variable takes on cold start. |
| **Documentation** | Free-text. Visible to anyone reading the variable table or hovering the variable in the editor. |
| **Debug** | Per-row toggle. Variables with debug on are streamed to the **Debugger** when you run the project. |

A **class filter** above the table (`All` / `Local` / `Input` / `Output` / `InOut` / `External` / `Temp`) hides rows of other classes. It's a display filter; the filtered-out rows still exist.

## Table mode

### Adding a row
Click the **`+`** button in the top-right toolbar. If a row is selected, the new row is inserted below it and inherits the selected row's class+type as a starting point. Without a selection, the new row is appended at the end with a default name (rename it immediately).

### Removing rows
Select one or more rows and click **`−`**. If the variable is referenced anywhere in the POU body, the references are flagged in the next compile (or, in graphical bodies, immediately).

### Reordering
The **↑** and **↓** buttons move the selected row up or down. Order matters: positional call sites pass arguments by index when the named-argument form is not used.

### Renaming
Double-click the name cell, type the new name, hit Enter. If the variable is used in graphical bodies (LD, FBD), the editor opens a **Rename Impact** dialog listing every reference. Confirm to apply the rename everywhere at once.

### Changing class
Click the class cell to switch. Two consequences worth knowing:

- Switching to `External` clears `Location` — externals resolve their address from the matching global variable in the Resource editor.
- Switching away from `Local` clears `Location` likewise (only `Local` and Program-scope variables can hold an address directly).

### Type picker
Click the type cell. The dropdown groups:

- **Base types** — IEC scalars: `BOOL`, `BYTE`, `WORD`, `DWORD`, `LWORD`, `SINT`, `INT`, `DINT`, `LINT`, `USINT`, `UINT`, `UDINT`, `ULINT`, `REAL`, `LREAL`, `TIME`, `DATE`, `TIME_OF_DAY`, `DATE_AND_TIME`, `STRING`, `WSTRING`.
- **User data types** — your project's custom types.
- **Library types** — types contributed by enabled libraries (typically function-block instance types).
- **Array** — opens a sub-dialog: pick the element type and dimensions (`[0..9, 0..3]`, etc.).

### Location

The location is a directly-mapped IEC address. The prefix tells you what:

| Prefix | Meaning |
|---|---|
| `%I` | Input (read from physical I/O) |
| `%Q` | Output (write to physical I/O) |
| `%M` | Memory (no physical mapping; useful for retentive or working memory) |

Then a size:

| Letter | Size |
|---|---|
| `X` | Bit |
| `B` | Byte |
| `W` | Word (16 bits) |
| `D` | Double word (32 bits) |
| `L` | Long word (64 bits) |

Then the index. Bit addresses use `byte.bit` notation: `%QX0.0`, `%QX0.7`, `%QX1.0`. See **[Address mapping fundamentals](../communication/modbus/addressing)** for how these map to wire-protocol addresses.

## Code mode

Click the **`< >`** icon in the table's toolbar to switch to code mode. The table is replaced by a Monaco editor showing the raw IEC declarations:

```iec
VAR
    counter : INT := 0;
    running : BOOL := FALSE;
END_VAR

VAR_INPUT
    enable : BOOL;
    setpoint : REAL := 50.0;
END_VAR

VAR_OUTPUT
    motor_on : BOOL;
    error_code : INT;
END_VAR
```

Edit freely. When you switch back to table mode, the editor parses the text. Syntax errors prevent the switch and surface as red squiggles with hover messages.

Code mode is faster for bulk paste-in operations, copying declarations between projects, or quickly auditing exactly what's declared.

## Aliases (producer-managed addresses)

Some variables don't get their address typed by hand — they get it from an external producer. Examples:

- A pin assigned to a board's I/O via the device's pin-mapping (desktop only).
- A channel mapped from an EtherCAT slave.
- A point on a Modbus master remote device.

For these, the editor stores an **alias** alongside the variable's name. The variable's `Location` is then computed from the alias registry: whenever the producer reassigns the underlying address, your variable's location is rewritten on the next save (via `syncVariableAliases`).

If the producer goes away (you delete the EtherCAT channel, for example), the alias becomes **orphaned**. The variables editor marks the row with an amber warning icon and a hover message explaining what to do (re-bind the alias, or remove the orphan).

## Function-specific fields

A `function` POU has two extra fields above the variable table:

- **Return type** — the type of the value the function returns. Required (every IEC function returns something).
- **POU description** — free text describing what the function does.

Function blocks and programs don't have these fields.

## Globals

For project-wide variables, use the **Resource** editor (the **Resource** entry in the project tree). It contains a Globals section that looks and behaves identically to the per-POU table, but the class is always `Global`. POU-level variables can then declare class `External` and reference a global by name.

See **[Global Variables](global-variables)** for the full Resource walkthrough.

## What's next

- **[Custom Data Types](../custom-data-types/creating-datatypes)** — define arrays, enumerations, and structures.
- **[Address mapping](../communication/modbus/addressing)** — `%IX/%QX/%MW` and how they reach a wire protocol.
- **[Debugger](../building-deploying/debugger)** — what the **Debug** checkbox actually does.
