# Using custom types in code

Once you've defined a custom data type, it joins the base types in every type picker across the project. Declaring a variable of a custom type is just like declaring an `INT`, the editor handles the rest.

## In the variables editor

Open any POU's variable table (or the Resource's Global Variables section) and click the **Type** cell. The dropdown shows three categories you'll care about for custom types:

- **Base types**: `BOOL`, `INT`, `REAL`, `TIME`, …
- **User data types**: everything you've defined in this project's Data Types section.
- **Array**: opens a sub-dialog to define an *inline* array. For arrays you only need once; reusable arrays should be defined in Data Types.

Pick a User Data Type. The variable now has that type, and you can use it in the body code or in a graphical block.

In code mode, the variable looks just like a base-type one:

```iec
VAR
    mode : MachineMode := IDLE;
    sensor : SensorReading;
    history : TempReadings;
END_VAR
```

## Accessing fields and elements

The syntax depends on the type's derivation.

### Enumerations, comparison and assignment

Enum values are usable directly by name:

```iec
mode := RUNNING;

IF mode = IDLE THEN
    (* … *)
END_IF;
```

You can pass enum-typed variables to function blocks, store them in structures, and put them in arrays.

### Arrays, indexed access

Use `[index]` to get or set an element. Indices can be literals, integer variables, or expressions:

```iec
history[0] := 25.0;
last := history[9];

FOR i := 0 TO 9 DO
    history[i] := 0.0;
END_FOR;

(* multi-dimensional access *)
recipe[1, 2] := 100;
```

Whole-array assignment works too, when both sides are the same type:

```iec
backup := history;        (* element-by-element copy *)
```

### Structures, dot-notation field access

Read or write a field with `instance.field_name`:

```iec
sensor.value := raw * 0.01;
sensor.valid := TRUE;
sensor.timestamp := DT#2026-05-23-14:30:00;

IF sensor.valid AND sensor.value > sensor.range_high THEN
    over_temperature := TRUE;
END_IF;
```

Whole-structure assignment works the same as arrays, copies every field:

```iec
backup := sensor;
```

### Nested combinations

The patterns chain naturally:

```iec
(* array of struct: dot after the index *)
sensors[3].value := 22.5;
sensors[3].valid := TRUE;

(* struct of array: index after the field *)
recipe.steps[0].duration := T#5s;

(* deeper nesting works too *)
plant.lines[2].sensors[5].value := 100.0;
```

## In graphical bodies (LD, FBD)

Custom-typed variables work just like base-typed ones in graphical bodies. The constraints:

- A pin typed `BOOL` accepts any BOOL-typed variable, including a field that resolves to a BOOL (`sensor.valid`, `mode = IDLE` as a comparison).
- A pin typed `INT` / `REAL` / etc. accepts any variable or expression of that type, including array elements (`history[3]`) and structure fields (`sensor.value`).
- Type-matching is checked at compile time. Mis-typed wires fail the build with the offending line surfaced in the console.

For typing variables on a block's pin in LD, type the path directly:

| Pin type | Valid value example |
|---|---|
| BOOL input | `sensor.valid` |
| INT input | `history[3]` |
| REAL input | `sensor.value` |
| Enum input | `current_mode` or `IDLE` (the literal) |

## Function block instances are also typed

Function block types (`TON`, `CTU`, a user-authored `MyController`) follow the same model, they're types you declare instances of:

```iec
VAR
    my_timer : TON;          (* TON is a function-block type *)
    my_controller : MyController;
END_VAR
```

Then you call the instance and read its outputs by dot notation, the same as structure fields:

```iec
my_timer(IN := start_btn, PT := T#5s);
IF my_timer.Q THEN
    motor := TRUE;
END_IF;
```

The dot notation is identical to a structure's field access because under the hood a function-block instance is, essentially, a structure that knows how to execute itself.

## Custom types as function-block parameters

You can declare function-block input/output classes with custom types. This is the cleanest way to pass a whole structure into a block:

```iec
FUNCTION_BLOCK ProcessReading
VAR_INPUT
    reading : SensorReading;       (* whole struct in *)
END_VAR
VAR_OUTPUT
    alarm : BOOL;
END_VAR

(* body *)
alarm := reading.valid AND (reading.value > reading.range_high);

END_FUNCTION_BLOCK
```

Calling it:

```iec
my_proc(reading := temp_sensor);
IF my_proc.alarm THEN
    (* … *)
END_IF;
```

For large structures or arrays, use class `In Out` so the data is passed by reference rather than copied.

## Common patterns

Three small examples that combine multiple custom types:

### State machine using an enum

```iec
VAR
    mode : MachineMode := IDLE;
END_VAR

CASE mode OF
    IDLE:
        IF start_btn THEN mode := RUNNING; END_IF;
    RUNNING:
        IF error THEN mode := FAULTED;
        ELSIF stop_btn THEN mode := IDLE;
        END_IF;
    FAULTED:
        IF reset_btn THEN mode := IDLE; END_IF;
END_CASE;
```

### Ring buffer using an array

```iec
VAR
    history : ARRAY[0..99] OF REAL;
    write_index : INT := 0;
END_VAR

history[write_index] := current_temp;
write_index := write_index + 1;
IF write_index > 99 THEN
    write_index := 0;
END_IF;
```

### Per-sensor records using a structure

```iec
VAR
    sensors : ARRAY[0..3] OF SensorReading;
END_VAR

(* read sensor 2 *)
IF sensors[2].valid AND sensors[2].value > sensors[2].range_high THEN
    alarms[2] := TRUE;
END_IF;
```

## What's next

- **[Variables editor](../working-with-variables/variables-editor)**: full reference for the variable table where you declare instances of your custom types.
- **[Array data types](array-datatypes)** · **[Enumerated data types](enumerated-datatypes)** · **[Structure data types](structure-datatypes)**, the three per-derivation pages.
