# Global Variables Editor

The Global Variables Editor is where you declare and manage variables that are shared across your entire project. Unlike the Variables Editor inside each POU (which handles local, input, output, and other POU-scoped variables), this editor works exclusively with Global-class variables defined at the Resource level.

This page explains where to find the editor, how to use its features, and common workflows for hardware I/O mapping and data sharing.

## Where to Find It

The Global Variables Editor lives inside the **Resource Editor**. To open it:

1. In the **Project Explorer** (the tree panel on the left), find the **Resource** node under the project's configuration section.
2. Click on **Resource** to open the Resource Editor.

The Resource Editor is divided into three sections, stacked vertically:

| Section | Purpose |
|---------|---------|
| **Global Variables** | Declare variables shared across all POUs (this page) |
| **Tasks** | Configure execution tasks with priorities and intervals |
| **Instances** | Assign Program POUs to Tasks for execution |

The Global Variables section is the first (topmost) section.

## Table Columns

The Global Variables Editor uses a table layout similar to the Variables Editor inside POUs, with one key difference: the **Class** column is always set to `Global` and cannot be changed.

| Column | Description |
|--------|-------------|
| **#** | Row number (auto-assigned) |
| **Name** | The variable's identifier. Must be unique across all Global variables |
| **Class** | Always `Global` — not editable |
| **Type** | The data type (BOOL, INT, REAL, custom types, arrays, etc.) |
| **Location** | Hardware address for physical I/O mapping, with predefined pin options |
| **Initial Value** | The starting value for the variable |
| **Documentation** | Free-text description of the variable's purpose |
| **Debug** | Checkbox to enable monitoring during online debugging |

## The Location Combobox

The **Location** column offers a **combobox** with predefined hardware pin categories. When you click the Location cell, you see organized groups of available addresses:

| Category | Address Pattern | Description |
|----------|----------------|-------------|
| **Digital Inputs** | `%IX...` | Physical digital input pins (buttons, switches, proximity sensors) |
| **Digital Outputs** | `%QX...` | Physical digital output pins (relays, solenoids, LEDs) |
| **Analog Inputs** | `%IW...` | Physical analog input channels (temperature, pressure, level sensors) |
| **Analog Outputs** | `%QW...` | Physical analog output channels (variable drives, proportional valves) |

The predefined options list the specific pins available on your target hardware. This prevents addressing errors by letting you pick from valid pins rather than typing addresses manually.

### Custom Location Values

If the predefined pin options don't cover your needs — for example, if you need a memory-mapped address (`%MW...`) or an address not in the predefined list — you can type a custom value directly into the Location field. The combobox accepts free-form text in addition to the predefined selections.

### Leaving Location Empty

Not every Global variable needs a hardware location. Variables used purely for data sharing between POUs (setpoints, status flags, counters) should have the Location field left empty. Only assign a location when the variable represents a physical I/O point.

## Dual View: Table and Code

Like the Variables Editor inside POUs, the Global Variables Editor supports **dual-view** mode:

### Table View

The default spreadsheet-like interface. Best for:

- Browsing and editing individual variable properties
- Using the Location combobox to pick hardware pins
- Quick visual overview of all Globals

### Code View

A text-based editor showing the IEC 61131-3 declaration syntax. The declarations appear inside a `VAR_GLOBAL` block:

```
VAR_GLOBAL
    start_button AT %IX0.0 : BOOL := FALSE;
    stop_button AT %IX0.1 : BOOL := FALSE;
    motor_relay AT %QX0.0 : BOOL := FALSE;
    pressure AT %IW0 : INT := 0;
    valve_cmd AT %QW0 : INT := 0;
    system_mode : INT := 0;
    alarm_active : BOOL := FALSE;
END_VAR
```

Code View is useful for:

- Adding many variables quickly by typing
- Copying variable declarations from other projects or documentation
- Reviewing the exact IEC text that the table generates

> **Tip:** When you switch from Code View back to Table View, the editor validates the text. Syntax errors must be corrected before the switch completes.

## Adding Global Variables

Click the **+** (plus) button in the toolbar to add a new Global variable:

- If a row is selected, the new variable is inserted **below** the selected row and copies its configuration as a starting template.
- If no row is selected, the new variable is appended at the end of the list.

After adding, immediately rename the variable and configure its type, location (if applicable), and initial value.

## Removing Global Variables

Select one or more rows and click the **−** (minus) button.

> **Tip:** If any POU in your project references the removed Global variable via an External declaration, that POU will produce an error until you either recreate the Global or remove the External reference. Before deleting a Global, check which POUs use it.

## Reordering Global Variables

Use the **Up Arrow** and **Down Arrow** buttons to reorder variables in the list. While ordering doesn't affect program behavior, keeping them organized improves maintainability — for example, grouping all inputs together, then all outputs, then shared data variables.

## Common Configurations

### Mapping Physical I/O

The most common use of Global variables is centralizing all hardware I/O mapping in one place. Here's a typical setup for a small machine:

| Name | Class | Type | Location | Initial Value | Documentation |
|------|-------|------|----------|---------------|---------------|
| `start_btn` | Global | BOOL | %IX0.0 | FALSE | Start pushbutton, NO contact |
| `stop_btn` | Global | BOOL | %IX0.1 | FALSE | Stop pushbutton, NC contact |
| `e_stop` | Global | BOOL | %IX0.2 | FALSE | Emergency stop, NC contact |
| `motor_fwd` | Global | BOOL | %QX0.0 | FALSE | Motor forward contactor |
| `motor_rev` | Global | BOOL | %QX0.1 | FALSE | Motor reverse contactor |
| `speed_ref` | Global | INT | %QW0 | 0 | VFD speed reference, 0-10000 |
| `temp_sensor` | Global | INT | %IW0 | 0 | PT100 temperature, raw ADC |

This approach means you only need to update the Resource if wiring changes — the Programs themselves reference these variables through External declarations and never deal with hardware addresses directly.

### Sharing Data Between Programs

For variables that coordinate logic between Programs but have no hardware connection, leave the Location empty:

| Name | Class | Type | Location | Initial Value | Documentation |
|------|-------|------|----------|---------------|---------------|
| `system_mode` | Global | INT | | 0 | 0=Off, 1=Manual, 2=Auto |
| `batch_count` | Global | DINT | | 0 | Total parts produced |
| `alarm_code` | Global | INT | | 0 | Active alarm number, 0=none |
| `recipe_id` | Global | INT | | 1 | Currently loaded recipe |

### Mixed Configuration

In practice, most projects combine both patterns — hardware-mapped Globals and data-sharing Globals in the same table:

```
VAR_GLOBAL
    (* Physical Inputs *)
    start_btn AT %IX0.0 : BOOL := FALSE;
    stop_btn AT %IX0.1 : BOOL := FALSE;
    temp_sensor AT %IW0 : INT := 0;

    (* Physical Outputs *)
    motor_run AT %QX0.0 : BOOL := FALSE;
    heater AT %QX0.1 : BOOL := FALSE;
    speed_ref AT %QW0 : INT := 0;

    (* Shared Data *)
    system_mode : INT := 0;
    target_temp : REAL := 25.0;
    alarm_active : BOOL := FALSE;
END_VAR
```

Using comments in Code View (as shown above) helps visually separate the categories.

## Differences from the POU Variables Editor

| Feature | POU Variables Editor | Global Variables Editor |
|---------|---------------------|------------------------|
| Class selection | Multiple classes (Local, Input, Output, InOut, External, Temp) | Always `Global` (not editable) |
| Class filter | Dropdown to filter by class | Not present (only one class) |
| Location combobox | Text field for manual address entry | Combobox with predefined hardware pin categories |
| Return type selector | Present for Functions | Not present |
| POU description | Present for Functions | Not present |
| Scope | Local to one POU | Project-wide |

## Tips for Managing Globals

> **Tip:** Group related variables together. Keep inputs, outputs, and shared data in separate clusters. Use Code View comments or consistent naming prefixes (`io_`, `cfg_`, `sts_`) to reinforce the grouping.

> **Tip:** Document the Location mapping. For hardware-mapped Globals, use the Documentation column to note the physical wiring (e.g., "Terminal X3-Pin 4, 24VDC proximity sensor"). This is invaluable during commissioning and troubleshooting.

1. **Set safe initial values**: Outputs should default to their safe state (typically `FALSE` or `0`). If the PLC restarts unexpectedly, the initial values determine the state before any logic executes.

2. **Review before deleting**: Since Globals are referenced project-wide via External variables, deleting a Global can break multiple POUs at once. Check all External references first.

3. **Keep the list manageable**: If you find yourself with dozens of Globals, consider whether some should be reorganized. Use User Data Types (structures) to group related variables into a single Global of a custom type.

---

## What's Next?

Now that you know how to declare and manage variables at every level of your project, explore how to create custom data types to organize complex data:

- [Creating Data Types](../custom-data-types/creating-datatypes) — Define structures, enumerations, and other custom types for your variables
