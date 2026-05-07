# Global Variables

In most PLC projects, multiple Programs need to share data. A common setpoint, a system-wide emergency stop flag, or a status register that several routines read and update. IEC 61131-3 provides **Global variables** for exactly this purpose. They're declared once in the Resource configuration and can be accessed from any POU in the project.

This page explains how Global variables work, how to connect them to POUs using the External class, and common patterns for sharing data across your project.

## What Are Global Variables?

A Global variable is declared at the **Resource** level rather than inside a specific POU. Because it lives outside any individual Program, Function, or Function Block, it's accessible project-wide.

Key characteristics:

- **Declared in the Resource**: You create Global variables in the Resource Editor, not inside a POU's variable table.
- **Always retained**: Global variable values persist across scan cycles for the entire lifetime of the program.
- **Shared by design**: Any POU that needs to read or write a Global variable can do so by declaring a matching External variable.
- **Class is always "Global"**: In the Resource Editor, the class column is fixed to `Global` and cannot be changed.

In IEC 61131-3 text format, Global variables are declared within a `VAR_GLOBAL` block:

```
VAR_GLOBAL
    system_mode : INT := 0;
    emergency_stop : BOOL := FALSE;
    target_temperature : REAL := 22.5;
    production_count : DINT := 0;
END_VAR
```

## The Global-External Relationship

Global variables aren't automatically visible inside POUs. To access a Global variable from a Program, Function, or Function Block, you must declare an **External** variable with the **same name and same data type** inside that POU.

Think of it as a two-step process:

1. **Declare the Global** in the Resource (one time, project-wide)
2. **Declare an External** in each POU that needs access (links to the Global)

### Step 1: Declare the Global

In the Resource Editor's Global Variables section, add a variable:

| Name | Class | Type | Initial Value |
|------|-------|------|---------------|
| `system_mode` | Global | INT | 0 |

### Step 2: Reference with External

In the POU's variable table, add a variable with the External class:

| Name | Class | Type |
|------|-------|------|
| `system_mode` | External | INT |

The name and type **must match exactly**. Once declared, you can read and write `system_mode` inside the POU just like any other variable. Changes are immediately reflected in the Global variable, and all other POUs with matching External declarations see the updated value.

### What Happens If They Don't Match?

- **Name mismatch**: The External variable won't find a corresponding Global, resulting in an error.
- **Type mismatch**: If the External declares `INT` but the Global is `REAL`, you'll get a type conflict error.

Always keep Global and External declarations synchronized.

## Physical I/O Mapping

Global variables can be mapped to physical hardware addresses, just like Input and Output variables in POUs. This is a common pattern for centralizing all I/O mapping in one place.

```
VAR_GLOBAL
    start_button AT %IX0.0 : BOOL;
    stop_button AT %IX0.1 : BOOL;
    motor_relay AT %QX0.0 : BOOL;
    pressure_sensor AT %IW0 : INT;
    valve_output AT %QW0 : INT;
END_VAR
```

In the IDE, the Global Variables Editor provides a **Location** column with a combobox offering predefined hardware pin categories:

| Category | Address Prefix | Typical Use |
|----------|---------------|-------------|
| Digital Inputs | `%IX...` | Buttons, switches, proximity sensors |
| Digital Outputs | `%QX...` | Relays, solenoids, indicator lights |
| Analog Inputs | `%IW...` | Temperature sensors, pressure transducers |
| Analog Outputs | `%QW...` | Variable-speed drives, proportional valves |

You can also type a custom location value if the predefined options don't cover your specific addressing needs.

### Centralized vs. Distributed I/O Mapping

There are two approaches to mapping hardware I/O:

**Centralized (recommended)**: Map all physical addresses in Global variables, then reference them with External variables in POUs. This keeps all hardware configuration in one place, making it easy to update when wiring changes.

```
(* In Resource - Global Variables *)
VAR_GLOBAL
    start_btn AT %IX0.0 : BOOL;
    motor_out AT %QX0.0 : BOOL;
END_VAR

(* In Program - External references *)
VAR_EXTERNAL
    start_btn : BOOL;
    motor_out : BOOL;
END_VAR
```

**Distributed**: Map hardware addresses directly in each POU's local variables. This is simpler for small projects but becomes harder to maintain as the project grows.

> **Tip:** Even if a physical input is only used by one Program, declaring it as a Global in the Resource keeps all hardware mapping centralized. This pays off when the project grows.

## Use Cases for Global Variables

### Setpoints and Configuration

Store operating parameters that multiple Programs reference:

```
VAR_GLOBAL
    target_speed : INT := 1500;        (* RPM *)
    max_temperature : REAL := 85.0;    (* Degrees C *)
    operation_mode : INT := 1;         (* 0=Manual, 1=Auto *)
END_VAR
```

Any Program that controls a motor, monitors temperature, or checks the operation mode declares an External reference to these Globals. When an operator changes `operation_mode`, every Program sees the new value immediately.

### Status Flags and Alarms

Share status information across the project:

```
VAR_GLOBAL
    system_running : BOOL := FALSE;
    alarm_active : BOOL := FALSE;
    fault_code : INT := 0;
END_VAR
```

One Program sets `alarm_active := TRUE` when it detects a problem. Other Programs check `alarm_active` to enter their safe-state logic.

### Data Sharing Between Programs

When two Programs running in different Tasks need to exchange data, Global variables are the standard mechanism.

**Example: A conveyor system with two Programs**

The `SensorProgram` reads sensor data and updates Globals:

```
(* SensorProgram - VAR_EXTERNAL *)
VAR_EXTERNAL
    part_detected : BOOL;
    part_count : DINT;
END_VAR

(* SensorProgram - Logic *)
IF proximity_sensor AND NOT prev_sensor THEN
    part_detected := TRUE;
    part_count := part_count + 1;
END_IF;
prev_sensor := proximity_sensor;
```

The `ConveyorProgram` reads those Globals to control the conveyor:

```
(* ConveyorProgram - VAR_EXTERNAL *)
VAR_EXTERNAL
    part_detected : BOOL;
    part_count : DINT;
END_VAR

(* ConveyorProgram - Logic *)
IF part_detected THEN
    conveyor_speed := fast_speed;
    part_detected := FALSE;  (* Acknowledge *)
ELSE
    conveyor_speed := slow_speed;
END_IF;
```

Both Programs reference the same `part_detected` and `part_count` Globals. The Resource configuration declares:

```
VAR_GLOBAL
    part_detected : BOOL := FALSE;
    part_count : DINT := 0;
END_VAR
```

## Best Practices

1. **Use meaningful, unique names**: Global variables are project-wide, so name them clearly. Prefixing with a category can help: `cfg_target_speed`, `sts_alarm_active`, `io_start_button`.

2. **Centralize I/O mapping**: Declare all physical I/O addresses as Global variables in the Resource. This creates a single source of truth for hardware mapping.

3. **Set initial values**: Always provide sensible defaults. A system that starts in a known, safe state is easier to commission and debug.

4. **Limit the number of Globals**: Overusing Global variables creates hidden dependencies between POUs. If a variable is only needed by one POU, keep it Local.

5. **Document each Global**: Use the Documentation field in the Global Variables Editor to describe the variable's purpose, valid range, and which POUs use it.

6. **Be mindful of concurrent access**: If two Programs running in separate Tasks both write to the same Global, the final value depends on execution order. Design your logic so that only one Program writes to a given Global, or use explicit handshaking.

---

## What's Next?

Learn how to work with the editor tools for managing variables:

- [Variables Editor](variables-editor): The visual table for creating and editing variables inside POUs
