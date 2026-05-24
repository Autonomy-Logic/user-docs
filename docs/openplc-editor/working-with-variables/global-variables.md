# Global variables

Most non-trivial projects have data that more than one POU needs to see: an emergency-stop flag, a machine mode, a setpoint everyone reads, a counter several routines update. IEC 61131-3 handles this with **global variables**. A global is declared once at the **Resource** level and any POU in the project can read or write it through an `External` declaration.

## Where globals live

Globals live in the **Resource** editor, not inside any POU's variable table. To open it, click **Resource** in the project tree:

![Resource editor showing three sections stacked vertically: Global Variables (with one global `system_mode` declared as DINT), Tasks (with `task0` Cyclic T#20ms priority 1), and Instances (with `instance0` binding the `main` program to `task0`)](images/resource-editor.png)

The Resource is divided into three sections, each its own table:

| Section | Purpose |
|---|---|
| **Global Variables** | Variables shared project-wide (this page). |
| **Tasks** | Execution schedules (cyclic with an interval, or interrupt-driven). |
| **Instances** | Bind a Program POU to a Task so it actually runs. |

A `Global` variable is just a row in the Global Variables table. The **Class** column is fixed to `Global` and can't be changed.

In IEC text form, globals are inside a `VAR_GLOBAL` block:

```iec
VAR_GLOBAL
    system_mode : INT := 0;
    emergency_stop : BOOL := FALSE;
    target_temperature : REAL := 22.5;
    production_count : DINT := 0;
END_VAR
```

## Declaring a global

In the **Global Variables** table at the top of the Resource editor:

1. Click the **`+`** in the top-right of that section.
2. A new row is added. The Class is `Global` (locked); fill in Name, Type, and optionally Initial Value.
3. Click the **Name** cell to rename, the **Type** cell to pick a type. Standard editing as in the per-POU variables table.

The columns are identical to the per-POU variables editor (`#`, Name, Class, Type, Location, Initial Value, Documentation, Debug). See **[Variables editor](variables-editor)** for the full reference.

A global can optionally have a `Location` (`%IX0.0`, `%MW3`, etc.). The most common reason to set one is to make the variable visible to a communication server: Modbus / OPC-UA / S7Comm all expose the IEC memory image to external clients, and the location tells the server which slot of that image the variable occupies. Globals without a location are pure in-memory data, fine for sharing project-wide state.

## Reading a global from a POU, `External`

A global is not automatically visible inside POUs. Each POU that needs to access it declares an `External` variable with the **same name and the same type**:

```iec
VAR_EXTERNAL
    system_mode : INT;
END_VAR
```

The External declaration doesn't create a new variable. It's a reference. Inside the POU, you read and write `system_mode` like any local variable; changes are immediately reflected in the global, and any other POU with a matching External sees the new value on the next scan.

A worked example. In the Resource:

| Name | Class | Type | Initial Value |
|---|---|---|---|
| `system_mode` | Global | INT | 0 |
| `emergency_stop` | Global | BOOL | FALSE |

In a program POU:

| Name | Class | Type |
|---|---|---|
| `system_mode` | External | INT |
| `emergency_stop` | External | BOOL |
| `local_counter` | Local | INT |

The program can then use all three together:

```iec
IF NOT emergency_stop AND system_mode = 1 THEN
    local_counter := local_counter + 1;
END_IF;
```

`local_counter` is private to this POU. `system_mode` and `emergency_stop` are project-wide; any other POU that declares matching Externals reads the same values.

### Name / type rules

- The External's **name must match the Global exactly** (case-insensitive in IEC).
- The **types must match exactly**. An External declared as `REAL` against a Global of `INT` is a type mismatch and fails on the next compile.
- The External itself doesn't carry an Initial Value: initial values live on the Global, since there is only one underlying value.

## When (and when not) to use globals

Globals are the right answer when something is **shared state** that needs to be visible across multiple POUs:

- Machine-wide modes (`system_mode` = AUTO / MANUAL / IDLE).
- Safety / fault flags (`emergency_stop`, `over_temperature`).
- Setpoints an operator changes from one POU but several other POUs read.
- Counters and totals that aggregate across the project.

Globals are not the right answer for:

- **Physical I/O that only one POU touches.** A variable bound to `%IX0.0` lives in the POU that reads it as a `Local` with a `Location`, no global needed. Globals are for in-program data sharing, not for input/output pin mapping.
- **Function-block interfaces.** Don't expose an FB's inputs and outputs as globals, declare them with `Input` and `Output` classes on the FB itself. Globals are noisier and harder to reason about than explicit interface pins.
- **Anything one POU could keep to itself.** Every global is one more thing every reader has to know about. Reach for `External` deliberately, not as a convenience.

## Globals and the Tasks / Instances sections

The Resource has two more sections below Global Variables: **Tasks** and **Instances**. These describe the *execution schedule* of your project, not its data.

- **Tasks** define when programs run (cyclic every `T#20ms`, etc.) and with what priority.
- **Instances** bind a specific Program POU to a Task: so e.g. `instance0` runs the `main` program inside `task0`.

You won't ever bind a global to a Task or Instance, globals are project-wide and exist independently of the schedule. The reason these three sections share the Resource editor is that they're all the "outside of any POU" parts of the IEC project: globals, schedules, and the binding between programs and schedules.

See **[Tasks and instances](../iec-concepts/tasks-instances)** for the conceptual model.

## What's next

- **[Variables editor](variables-editor)**: the full reference for the per-POU table that also applies to the Globals section.
- **[Tasks and instances](../iec-concepts/tasks-instances)**: the other two Resource sections.
- **[Modbus server](../communication/modbus/server)**: how the Globals' `Location` addresses get exposed to external Modbus clients.
