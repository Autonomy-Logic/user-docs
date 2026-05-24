# Global variables editor

The Global Variables editor is the top section of the **Resource** editor. It declares variables that are visible project-wide, in contrast to the per-POU variables editor which is scoped to a single Program, Function, or Function Block.

![Resource editor with all three sections visible: Global Variables (with `system_mode` declared as a DINT Global), Tasks (one cyclic task), Instances (binding the `main` program to that task)](images/resource-editor.png)

The table looks and behaves like the per-POU variables editor, with one structural difference: the **Class** column is fixed to `Global` and cannot be changed. Every other column. Name, Type, Location, Initial Value, Documentation, Debug, works the same way. See **[Variables editor](variables-editor)** for the column-by-column reference and the table/code-mode toggle.

## Opening it

In the project tree, click **Resource**. The Resource editor opens as a tab in the central editor area. The Global Variables table is the first section at the top; Tasks and Instances are below it.

## What's different from per-POU variables

| | Per-POU variables editor | Global Variables editor |
|---|---|---|
| Scope | Local to one POU | Project-wide |
| Class column | Six options (Local / Input / Output / In Out / External / Temp) | Fixed to `Global` |
| Class filter dropdown | Yes | Not present (only one class) |
| Return type field | Yes (for Functions) | Not present |
| POU description field | Yes (for Functions) | Not present |

Everything else, adding, removing, reordering, the Type picker, code mode, renaming, the alias mechanism, is identical.

## Typical patterns

A clean way to organise globals is to group them by purpose. The two main categories you'll see in practice are **physical I/O** (variables with a `Location`) and **shared data** (variables without one).

### Physical I/O

Globals with a `Location` like `%IX0.0` or `%QX0.0` map directly to physical input or output pins on the runtime. Centralising them in the Resource means each POU references them through `External` declarations and never has to think about wiring; if the wiring changes you only update one place.

| Name | Class | Type | Location | Initial Value | Documentation |
|---|---|---|---|---|---|
| `start_btn` | Global | BOOL | `%IX0.0` | FALSE | Start pushbutton, NO contact |
| `stop_btn` | Global | BOOL | `%IX0.1` | FALSE | Stop pushbutton, NC contact |
| `e_stop` | Global | BOOL | `%IX0.2` | FALSE | Emergency stop, NC contact |
| `motor_fwd` | Global | BOOL | `%QX0.0` | FALSE | Motor forward contactor |
| `motor_rev` | Global | BOOL | `%QX0.1` | FALSE | Motor reverse contactor |
| `speed_ref` | Global | INT | `%QW0` | 0 | VFD speed reference, 0–10000 |
| `temp_sensor` | Global | INT | `%IW0` | 0 | PT100 temperature, raw ADC |

This isn't required, a Program can just as easily declare its own `Local`-class variables with `Location` set, and most small projects do. The case for centralising in the Resource is shared visibility: every POU that imports a Global through `External` reads or writes the same physical pin without each POU needing its own Location declaration.

### Shared data

Globals without a `Location` are pure in-memory shared state. The runtime allocates storage for them; no physical pin involved.

| Name | Class | Type | Location | Initial Value | Documentation |
|---|---|---|---|---|---|
| `system_mode` | Global | INT | | 0 | 0 = Off, 1 = Manual, 2 = Auto |
| `batch_count` | Global | DINT | | 0 | Total parts produced |
| `alarm_code` | Global | INT | | 0 | Active alarm number; 0 = none |
| `recipe_id` | Global | INT | | 1 | Currently loaded recipe |

### Mixed

Most real projects combine both. The code-mode view groups them inside a single `VAR_GLOBAL` block; comments help separate the groups visually:

```iec
VAR_GLOBAL
    (* Physical Inputs *)
    start_btn AT %IX0.0 : BOOL := FALSE;
    stop_btn  AT %IX0.1 : BOOL := FALSE;
    temp_sensor AT %IW0 : INT  := 0;

    (* Physical Outputs *)
    motor_run AT %QX0.0 : BOOL := FALSE;
    heater    AT %QX0.1 : BOOL := FALSE;
    speed_ref AT %QW0   : INT  := 0;

    (* Shared Data *)
    system_mode    : INT  := 0;
    target_temp    : REAL := 25.0;
    alarm_active   : BOOL := FALSE;
END_VAR
```

Note the `AT %IX...` / `AT %QX...` notation in code mode, this is the IEC syntax for declaring a variable with a Location, and it's legal in `VAR` (Local) and `VAR_GLOBAL` blocks. It's **not** legal in `VAR_INPUT` / `VAR_OUTPUT` blocks, which is why physical I/O lives in Local or Global declarations, never in an FB's interface.

## Communication servers and globals

Modbus / OPC-UA / S7Comm servers expose the IEC memory image to external clients. For a global to be reachable through one of those servers, give it a `Location` in the appropriate memory area:

- `%QX` / `%QW` / `%MD` etc. for variables the server should make writable (e.g. Modbus holding registers, OPC-UA writable nodes).
- `%IX` / `%IW` for read-only inputs the server publishes.
- `%MX` / `%MW` / `%MD` / `%ML` for variables that aren't tied to physical I/O but live in shared memory the server can map.

The mapping rules are protocol-specific; see **[Modbus server](../communication/modbus/server)** and **[OPC-UA address space](../communication/opc-ua/address-space)** for the details.

## Caution before deleting

A Global referenced by an `External` in any POU will produce a compile error on the next build if you remove it. Before deleting, check whether any POU references it, either by searching the project (the activity-bar **Search** action) or by looking for `External` rows with the matching name in your POU variable tables.

## What's next

- **[Global variables](global-variables)**: the conceptual side: how Globals and Externals work together.
- **[Variables editor](variables-editor)**: the editing UI that this section reuses.
- **[Modbus server](../communication/modbus/server)**: how globals with `%QW` / `%MX` Locations end up on the wire.
