# Local Variables

Every PLC program needs to store data. Sensor readings, calculation results, control flags, and more. In IEC 61131-3, variables declared inside a Program Organization Unit (POU) are called **local variables**. They define the data that a Program, Function, or Function Block works with during execution.

This page covers the different variable classes available within POUs, how they behave during the scan cycle, and when to use each one.

## Variable Classes Overview

When you create a variable inside a POU, you assign it a **class** that determines its scope, visibility, and behavior:

| Class | Description | Available In |
|-------|-------------|--------------|
| **Local** | Internal variable, private to the POU | Programs, Functions, Function Blocks |
| **Input** | Receives a value from the caller | Functions, Function Blocks |
| **Output** | Sends a value back to the caller | Functions, Function Blocks |
| **InOut** | Passed by reference; shared between caller and POU | Functions, Function Blocks |
| **External** | References a Global variable declared in the Resource | Programs, Function Blocks |
| **Temp** | Temporary variable that exists only for one execution cycle | Programs, Function Blocks |

## Local Class

Local variables are the most common class. They hold internal data that only the POU itself can read and write. No other POU can access them directly.

```
VAR
    counter : INT;
    running : BOOL;
    setpoint : REAL := 75.0;
END_VAR
```

**Key behavior**: In Programs and Function Blocks, local variables **retain their values** between scan cycles. If `counter` is 5 at the end of one cycle, it's still 5 at the beginning of the next. This makes them suitable for accumulators, state machines, and any logic that depends on previous values.

In Functions, local variables do **not** retain their values. They're re-initialized each time the function executes.

### When to Use Local

- Internal counters, flags, and intermediate calculations
- State machine variables
- Timers and timer-related values
- Any data that shouldn't be visible outside the POU

## Input Class

Input variables define parameters that a Function or Function Block receives from its caller. Inside the POU, input variables are **read-only**: the POU can read their values but cannot modify them.

```
VAR_INPUT
    enable : BOOL;
    target_temp : REAL;
    max_speed : INT := 1000;
END_VAR
```

When another POU calls your function block, it provides values for these inputs:

```
my_controller(enable := TRUE, target_temp := 72.5, max_speed := 500);
```

### Hardware-Mapped Inputs

Input variables can also be mapped to physical hardware addresses. This is how you read data from real-world sensors and switches:

```
VAR_INPUT
    start_button AT %IX0.0 : BOOL;    (* Digital input, byte 0, bit 0 *)
    pressure AT %IW2 : INT;            (* Analog input, word 2 *)
END_VAR
```

### When to Use Input

- Parameters that a Function or Function Block needs from its caller
- Physical sensor readings mapped to hardware addresses
- Configuration values passed to reusable logic blocks

## Output Class

Output variables define values that a Function or Function Block sends back to its caller. Inside the POU, output variables are **read-write**: the POU computes a result and assigns it to the output.

```
VAR_OUTPUT
    motor_on : BOOL;
    current_speed : INT;
    error_code : INT;
END_VAR
```

The caller reads outputs using dot notation after invoking the function block:

```
my_controller(enable := TRUE, target_temp := 72.5);
IF my_controller.error_code <> 0 THEN
    alarm := TRUE;
END_IF;
```

### Hardware-Mapped Outputs

Output variables can be mapped to physical hardware addresses to drive actuators, relays, and other output devices:

```
VAR_OUTPUT
    motor_relay AT %QX0.0 : BOOL;     (* Digital output, byte 0, bit 0 *)
    valve_position AT %QW0 : INT;      (* Analog output, word 0 *)
END_VAR
```

### When to Use Output

- Computed results that the caller needs to read
- Status indicators and error codes
- Physical actuator and relay control via hardware addresses

## InOut Class

InOut variables are passed **by reference**. The caller and the POU share the same variable. Changes made inside the POU are immediately visible to the caller, and vice versa.

```
VAR_IN_OUT
    shared_buffer : ARRAY[0..99] OF INT;
    accumulator : REAL;
END_VAR
```

When calling a POU with InOut parameters, you must pass an existing variable (not a literal value):

```
VAR
    my_buffer : ARRAY[0..99] OF INT;
    my_total : REAL;
END_VAR

process_data(shared_buffer := my_buffer, accumulator := my_total);
(* my_buffer and my_total may have been modified by the function block *)
```

### When to Use InOut

- Large data structures (arrays, structs) to avoid copying
- Variables that the POU needs to both read and modify
- Shared accumulators or buffers between caller and callee

## External Class

External variables create a reference to a **Global variable** declared in the Resource configuration. This is the mechanism that lets POUs share data across the entire project.

```
VAR_EXTERNAL
    system_mode : INT;
    emergency_stop : BOOL;
END_VAR
```

For an external variable to work, a global variable with the **same name and type** must exist in the Resource. The external declaration doesn't create a new variable. It links to the existing global one.

### When to Use External

- Accessing shared configuration values (setpoints, modes)
- Reading or writing status flags shared across multiple POUs
- Coordinating behavior between Programs running in different Tasks

For a complete explanation of Global variables and the Global-External relationship, see [Global Variables](global-variables).

## Temp Class

Temp variables are **temporary**: they exist only for the duration of a single execution cycle. Unlike local variables, temp variables are **not retained** between cycles. Each time the POU executes, temp variables start from their initial value (or an undefined state if no initial value is set).

```
VAR_TEMP
    intermediate_result : REAL;
    loop_index : INT;
END_VAR
```

### When to Use Temp

- Intermediate calculations that don't need to persist
- Loop counters
- Scratch space for data processing within a single cycle

## I/O Addressing for Hardware-Mapped Variables

When a variable needs to represent a physical input or output on the PLC hardware, you assign it a **location** using the IEC 61131-3 addressing format:

```
%<Prefix><Size><Address>
```

### Address Components

| Component | Options | Meaning |
|-----------|---------|---------|
| **Prefix** | `I` | Input. Reading from sensors, switches |
| | `Q` | Output. Writing to actuators, relays |
| | `M` | Memory. Internal storage |
| **Size** | `X` | Bit (BOOL) |
| | `B` | Byte (8 bits) |
| | `W` | Word (16 bits) |
| | `D` | Double word (32 bits) |
| | `L` | Long word (64 bits) |

### Address Examples

| Address | Meaning |
|---------|---------|
| `%IX0.0` | Digital input, byte 0, bit 0 |
| `%IX1.3` | Digital input, byte 1, bit 3 |
| `%IW2` | Analog input, word 2 (16-bit) |
| `%QX0.0` | Digital output, byte 0, bit 0 |
| `%QX1.3` | Digital output, byte 1, bit 3 |
| `%QW0` | Analog output, word 0 (16-bit) |
| `%MD10` | Memory double word 10 (32-bit) |

Bit addresses use a two-part number (`byte.bit`), while byte, word, and larger addresses use a single number.

For a complete reference on the addressing system, see [Modbus Addressing](../communication/modbus/addressing).

## Retention Behavior Summary

Understanding when variable values persist between cycles is critical for correct PLC logic:

| Class | Retained Between Cycles? | Notes |
|-------|--------------------------|-------|
| Local (Program/FB) | Yes | Value carries over from cycle to cycle |
| Local (Function) | No | Re-initialized on every call |
| Input | N/A | Set by caller each time the POU executes |
| Output | Yes (in FBs) | Function Block outputs persist |
| InOut | N/A | References the caller's variable |
| External | Yes | Points to a Global, which is always retained |
| Temp | No | Reset every cycle |

## Best Practices

> **Tip:** Default to the Local class unless you have a specific reason to choose another. Most variables in a typical POU are Local.

> **Tip:** Always provide initial values for variables that depend on a known starting state, especially counters, flags, and setpoints.

1. **Minimize External references**: Each External variable creates a coupling between the POU and the Resource configuration. Use them deliberately for genuinely shared data, not as a convenience shortcut.

2. **Use Temp for scratch data**: If a variable is only needed within one scan cycle and doesn't need to remember its value, declare it as Temp. This communicates intent and helps with debugging.

3. **Name variables descriptively**: A variable named `motor_running` is far more maintainable than `flag1`. Use the Documentation field in the variables table to add context when the name alone isn't sufficient.

4. **Match Input/Output types to function block interfaces**: When designing reusable Function Blocks, choose Input and Output variable types carefully. They form the block's public interface.

---

## What's Next?

Now that you understand the variable classes available inside POUs, learn how shared data works across the entire project:

- [Global Variables](global-variables): Declaring project-wide variables in the Resource and accessing them with the External class
