# Variables Editor

The Variables Editor is the visual interface where you create, modify, and organize the variables for each POU (Program, Function, or Function Block) in your project. It appears at the top of every POU editor, above the programming area where you write your logic.

This page covers every feature of the Variables Editor — its table columns, dual-view modes, filtering, and the special behaviors that differ depending on your POU type.

## Opening the Variables Editor

The Variables Editor is always visible when you open a POU. Click on any Program, Function, or Function Block in the Project Explorer to open it. The editor area splits into two sections:

1. **Variables Editor** (top) — the table or code view described on this page
2. **Programming Editor** (bottom) — where you write logic in your chosen language (LD, FBD, ST, or IL)

You can resize the boundary between these two sections by dragging the divider.

## Table View

The default view presents variables in a spreadsheet-like table. Each row represents one variable, and the columns let you configure every aspect of it.

### Table Columns

The columns displayed depend on the POU type:

**For Function Blocks and Functions:**

| Column | Description |
|--------|-------------|
| **#** | Row number (auto-assigned, not editable) |
| **Name** | The variable's identifier. Must be unique within the POU and follow IEC naming rules |
| **Class** | The variable class: Local, Input, Output, InOut, External, or Temp |
| **Type** | The data type (BOOL, INT, REAL, custom types, arrays, etc.) |
| **Location** | Optional hardware address (e.g., `%IX0.0`, `%QW0`) for mapping to physical I/O |
| **Initial Value** | The value the variable starts with (e.g., `0`, `TRUE`, `3.14`) |
| **Documentation** | A free-text description of the variable's purpose |
| **Debug** | Checkbox that enables monitoring this variable during online debugging |

**For Programs:**

| Column | Description |
|--------|-------------|
| **#** | Row number |
| **Name** | The variable's identifier |
| **Class** | The variable class |
| **Type** | The data type |
| **Initial Value** | Starting value |
| **Documentation** | Description |
| **Debug** | Debug monitoring toggle |

Notice that Programs **do not show the Location column**. In Programs, hardware I/O mapping is typically handled through Global variables in the Resource configuration rather than directly in the Program's variable table.

### Functions: Special Fields

When editing a **Function**, two additional fields appear above the variable table:

- **Return Type**: A dropdown selector for the Function's return data type. Every Function must return a value, and this field defines its type (e.g., BOOL, INT, REAL).
- **POU Description**: A text field for documenting what the Function does.

These fields don't appear for Programs or Function Blocks.

## Adding Variables

Click the **+** (plus) button in the Variables Editor toolbar to add a new variable:

- If a row is currently selected, the new variable is inserted **below** the selected row and copies the selected row's configuration as a starting point.
- If no row is selected, the new variable is appended at the end of the table.

The new variable receives a default name — rename it immediately to something meaningful. Click on any cell in the new row to edit its properties.

## Removing Variables

Select one or more rows and click the **−** (minus) button to remove them.

> **Tip:** If a variable is referenced in the POU's graphical logic (for example, used in a Ladder Diagram contact or a Function Block Diagram connection), removing it will also remove those references. Review the POU's logic before deleting variables.

## Reordering Variables

Use the **Up Arrow** and **Down Arrow** buttons to move the selected variable up or down in the list. Variable order matters in IEC 61131-3 because it determines the positional mapping of Input and Output parameters when calling Functions and Function Blocks.

For example, if a Function Block has Input variables declared in this order:

| # | Name | Class |
|---|------|-------|
| 1 | enable | Input |
| 2 | setpoint | Input |
| 3 | timeout | Input |

Then callers can pass values either by name or by position. Reordering these variables changes the positional mapping.

## Class Filter

The Variables Editor includes a **class filter dropdown** above the table that lets you show only variables of a specific class:

| Filter | Shows |
|--------|-------|
| All | Every variable in the POU |
| Local | Only Local variables |
| Input | Only Input variables |
| Output | Only Output variables |
| InOut | Only InOut variables |
| External | Only External variables |
| Temp | Only Temp variables |

This is particularly useful in POUs with many variables. For example, if you want to review just the Input parameters of a Function Block, select "Input" from the filter to hide all other variables temporarily.

The filter only affects the display — it doesn't delete or modify any variables.

## Type Selector

When you click on the **Type** cell for a variable, a dropdown selector appears with categories of available types:

| Category | Contents |
|----------|----------|
| **Base Types** | Standard IEC types: BOOL, BYTE, WORD, DWORD, LWORD, SINT, INT, DINT, LINT, USINT, UINT, UDINT, ULINT, REAL, LREAL, TIME, DATE, STRING, WSTRING, etc. |
| **User Data Types** | Custom structures, enumerations, and other types you've created in your project |
| **System Libraries** | Types provided by system-level libraries included in the project |
| **User Libraries** | Types from libraries you've added to the project |
| **Array** | Opens a configuration dialog to define an array type with element type and dimensions |

Select the appropriate category, then choose the specific type. For arrays, you'll specify the element type and the array bounds (e.g., `ARRAY[0..9] OF INT`).

## Code View

The Variables Editor supports a **dual-view** mode. You can switch between the visual table and a text-based **Code View** by clicking the toggle in the editor toolbar.

### What Code View Shows

Code view displays the variable declarations in standard IEC 61131-3 text format, inside a Monaco editor. For example:

```
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

### Editing in Code View

You can edit variable declarations directly in the text editor. This is useful for:

- Quickly adding multiple variables by typing
- Copying and pasting variable declarations from documentation or other projects
- Reviewing the exact IEC 61131-3 syntax

### Validation on Switch

When you switch **from Code View back to Table View**, the editor validates the text you entered. If there are syntax errors (missing semicolons, invalid types, malformed declarations), the editor reports them and prevents the switch until the errors are corrected.

This ensures that the table always contains valid variable declarations.

## Renaming Variables

To rename a variable, double-click the **Name** cell and type the new name. If the variable is used in graphical editors (Ladder Diagram or Function Block Diagram), renaming it triggers a **Rename Impact Modal**.

The Rename Impact Modal shows you every location where the old variable name appears in the POU's graphical logic. You can review the references before confirming the rename, which automatically updates all occurrences.

## Undo and Redo

The Variables Editor supports undo and redo for all operations — adding, removing, editing, and reordering variables:

| Action | Shortcut |
|--------|----------|
| Undo | `Ctrl+Z` (Windows/Linux) or `Cmd+Z` (macOS) |
| Redo | `Ctrl+Y` (Windows/Linux) or `Cmd+Shift+Z` (macOS) |

This works in both Table View and Code View.

## POU-Specific Differences

| Feature | Program | Function | Function Block |
|---------|---------|----------|----------------|
| Location column | No | Yes | Yes |
| Return type selector | No | Yes | No |
| POU description field | No | Yes | No |
| Available classes | Local, External, Temp | Local, Input, Output, InOut, Temp | Local, Input, Output, InOut, External, Temp |

## Tips for Effective Use

> **Tip:** Name variables before configuring them. When you add a new variable, change its name first — this helps you track what each row represents as you configure the rest.

> **Tip:** Use the class filter for large POUs. If your POU has more than 10–15 variables, filtering by class makes it much easier to find specific variables.

> **Tip:** Review Code View periodically. Switching to Code View gives you a quick overview of all declarations in standard IEC syntax — a good way to verify the table produced what you intended.

1. **Set initial values for state-dependent variables**: Counters, accumulators, and flags should always have explicit initial values to ensure predictable behavior on first run.

2. **Use the Documentation column**: A brief note like "Motor speed in RPM, range 0-3000" saves significant time when revisiting the project later.

---

## What's Next?

Learn how to manage Global variables that are shared across the entire project:

- [Global Variables Editor](global-variables-editor) — The specialized editor for creating and managing Global variables in the Resource configuration
