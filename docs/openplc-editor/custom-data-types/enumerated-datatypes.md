# Enumerated Data Types

An enumeration defines a data type whose variable can hold exactly one value from a fixed set of named options. Instead of using raw integers to represent states (where `0` means idle, `1` means running, and `2` means faulted — and you have to remember which is which), you define an enumerated type with descriptive names like `IDLE`, `RUNNING`, and `FAULTED`. The result is code that reads like plain language and catches mistakes at design time rather than at runtime.

Enumerations are one of the most effective tools for writing clear, maintainable PLC programs.

## When to Use Enumerations

Enumerations are the right choice whenever a variable represents a **mode**, **state**, **category**, or **option** — anything that should be one of a limited, known set of possibilities.

Common industrial examples:

| Example Type | Values |
|-------------|--------|
| Machine state | IDLE, STARTING, RUNNING, STOPPING, FAULTED |
| Operating mode | MANUAL, AUTOMATIC, MAINTENANCE |
| Alarm level | NONE, INFO, WARNING, CRITICAL |
| Command code | START, STOP, PAUSE, RESUME, RESET |
| Product type | TYPE_A, TYPE_B, TYPE_C |
| Direction | FORWARD, REVERSE, STOPPED |

## The Enumeration Editor

When you open an enumeration data type in the IDE, the editor presents two main areas:

### Values Table

The values table is where you define the named values that make up the enumeration. Each row has a **Description** cell containing the value's name.

| Control | Action |
|---------|--------|
| **Add** (+) | Adds a new value row at the bottom of the table |
| **Remove** (−) | Removes the selected value row |
| **Up arrow** | Moves the selected value up in the list |
| **Down arrow** | Moves the selected value down in the list |

To edit a value's name, click directly on its Description cell and type the new name.

**Automatic cleanup:** If you leave a value's name empty and click away, that value row is automatically removed from the table.

### Initial Value Selector

A dropdown below the values table lets you choose which value should be the default when a variable of this type is created. The dropdown is populated with all the values you've defined.

If you don't select an initial value, the first value in the list is used as the default.

## Naming Rules for Values

Enumeration value names must follow these conventions:

- **Valid formats:** CamelCase, PascalCase, or snake_case (e.g., `Running`, `RUNNING`, `machine_running`).
- **No duplicates:** Each value name must be unique within the enumeration.
- **Non-empty:** A value cannot have a blank name (blank names are automatically removed).
- **Valid characters:** Letters, digits, and underscores. Cannot start with a digit.

**Recommended convention:** Use UPPER_CASE for enumeration values. This is the most common convention in IEC 61131-3 and makes enumeration values visually distinct from variable names and type names.

```
(* Recommended *)
IDLE, RUNNING, FAULTED

(* Also valid *)
Idle, Running, Faulted
idle, running, faulted
```

## Examples

### Machine State

A classic state-machine enumeration for controlling equipment.

**Configuration:**

| Property | Value |
|----------|-------|
| Name | `MachineState` |
| Values | IDLE, STARTING, RUNNING, STOPPING, FAULTED |
| Initial Value | IDLE |

**IEC 61131-3 representation:**

```
TYPE MachineState : (IDLE, STARTING, RUNNING, STOPPING, FAULTED) := IDLE; END_TYPE
```

### Alarm Level

Categorizing alarms by severity.

**Configuration:**

| Property | Value |
|----------|-------|
| Name | `AlarmLevel` |
| Values | NONE, INFO, WARNING, CRITICAL |
| Initial Value | NONE |

**IEC 61131-3 representation:**

```
TYPE AlarmLevel : (NONE, INFO, WARNING, CRITICAL) := NONE; END_TYPE
```

### Operating Mode

Switching between manual, automatic, and maintenance modes.

**Configuration:**

| Property | Value |
|----------|-------|
| Name | `OperatingMode` |
| Values | MANUAL, AUTOMATIC, MAINTENANCE |
| Initial Value | MANUAL |

**IEC 61131-3 representation:**

```
TYPE OperatingMode : (MANUAL, AUTOMATIC, MAINTENANCE) := MANUAL; END_TYPE
```

## Using Enumerations in Code

### Assignment

Assign an enumeration value to a variable by using the value name directly:

```
(* In the variables table: currentState : MachineState *)

currentState := IDLE;
currentState := RUNNING;
```

### Comparison

Compare a variable against enumeration values using standard comparison operators:

```
IF currentState = RUNNING THEN
    motor_on := TRUE;
END_IF;

IF currentState <> FAULTED THEN
    enable_outputs := TRUE;
END_IF;
```

### CASE Statements

Enumerations work naturally with CASE statements, which is the most common pattern for state machines:

```
CASE currentState OF
    IDLE:
        motor_on := FALSE;
        ready_light := TRUE;

    STARTING:
        motor_on := TRUE;
        ready_light := FALSE;
        IF motor_at_speed THEN
            currentState := RUNNING;
        END_IF;

    RUNNING:
        motor_on := TRUE;
        ready_light := TRUE;
        IF stop_requested THEN
            currentState := STOPPING;
        END_IF;

    STOPPING:
        motor_on := FALSE;
        IF motor_stopped THEN
            currentState := IDLE;
        END_IF;

    FAULTED:
        motor_on := FALSE;
        ready_light := FALSE;
        alarm := TRUE;
        IF reset_button THEN
            alarm := FALSE;
            currentState := IDLE;
        END_IF;
END_CASE;
```

This pattern is far more readable than using integer constants (0, 1, 2, 3, 4) for the same logic.

### Passing to Functions and Function Blocks

Enumeration variables can be passed as inputs to functions and function blocks. Define the function's input parameter with the enumeration type, and the caller provides a value of that type:

```
(* Function block with an enumeration input *)
(* FB input: commandIn : OperatingMode *)

controller(commandIn := currentMode);
```

## Reordering Values

The order of values in an enumeration can matter when the runtime maps them to underlying integer representations. The first value typically corresponds to 0, the second to 1, and so on. If your program logic depends on comparing enumerations with `<` or `>` operators (which compare the underlying ordinal positions), the order in the values table is significant.

Use the **up/down arrow** buttons in the editor to arrange values in the order that makes logical sense for your application — typically from the "least active" or "default" state to the "most active" or "exceptional" state.

## Tips for Working with Enumerations

> **Tip:** Always set a meaningful initial value. Choose the safest default state. For a machine, that's usually IDLE or STOPPED. For an alarm level, it's NONE.

> **Tip:** Prefer enumerations over integers. Replacing `IF state = 3` with `IF state = FAULTED` eliminates an entire category of bugs — the "magic number" problem.

- **Use enumerations for state machines.** The CASE statement combined with an enumeration variable is the standard PLC pattern for implementing state machines in Structured Text.
- **Keep value sets small and stable.** An enumeration with 30+ values may indicate that a different data modeling approach (perhaps a structure or a lookup table) would be more appropriate.
- **Document the meaning of each value** in code comments or in the variable documentation field if the name alone isn't self-explanatory.

---

## What's Next?

Learn how to group related fields into composite types with [Structure Data Types](structure-datatypes).
