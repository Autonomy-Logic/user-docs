# Structure Data Types

A structure (often called a "struct") is a composite data type that groups multiple named fields of potentially different types into a single unit. Where an array holds many values of the same type, a structure holds a fixed set of values that can each be a different type. This mirrors how real-world data is naturally organized — a sensor reading isn't just a number; it's a number paired with a validity flag, a timestamp, and an identifier.

Structures are one of the most powerful tools for keeping PLC programs organized, readable, and maintainable.

## When to Use Structures

Structures are the right choice whenever you have a group of related values that logically belong together and are always used as a unit. Common industrial examples:

| Structure | Fields | Purpose |
|-----------|--------|---------|
| `SensorData` | Value (REAL), Valid (BOOL), Timestamp (DT) | Bundle a measurement with its metadata |
| `MotorConfig` | Speed (REAL), Direction (INT), Enabled (BOOL), MaxCurrent (REAL) | Group all motor parameters |
| `PIDParams` | Kp (REAL), Ki (REAL), Kd (REAL), Setpoint (REAL) | Keep PID tuning values together |
| `RecipeStep` | StepNumber (INT), Duration (TIME), Temperature (REAL), Pressure (REAL) | Define one step of a production recipe |
| `AlarmRecord` | Active (BOOL), Level (INT), Message (STRING), Time (DT) | Store alarm information |

**Rule of thumb:** If you find yourself declaring three or more variables that share a common prefix (e.g., `motor_speed`, `motor_direction`, `motor_enabled`, `motor_maxCurrent`), that group is a strong candidate for a structure.

## The Structure Editor

When you open a structure data type in the IDE, the editor presents a **Variables Table** with the following columns:

| Column | Description |
|--------|-------------|
| **#** | Row number (auto-assigned, not editable) |
| **Name** | The field name — click to edit |
| **Type** | The field's data type — click to open a dropdown selector |
| **Initial Value** | An optional default value for the field — click to edit |

### Adding Fields

Click the **+** (Add) button above the table to insert a new field row. The IDE generates a default name following the pattern `structureVar_1`, `structureVar_2`, and so on. Rename these to meaningful names immediately.

### Removing Fields

Select a row and click the **−** (Remove) button to delete that field from the structure.

### Reordering Fields

Use the **up arrow** and **down arrow** buttons to change the order of fields. While field order doesn't usually affect runtime behavior, keeping fields in a logical order (e.g., identification fields first, then measurement fields, then status flags) makes the structure easier to understand.

### Naming Fields

Field names must be:

- Valid IEC 61131-3 identifiers (letters, digits, underscores; cannot start with a digit).
- Unique within the structure — no two fields can share the same name.
- Descriptive — `Temperature` is better than `var1`.

### Choosing Field Types

Click the **Type** cell for a field to open a dropdown selector. The available types are organized into categories:

| Category | Description |
|----------|-------------|
| **Base Types** | BOOL, SINT, INT, DINT, LINT, USINT, UINT, UDINT, ULINT, REAL, LREAL, TIME, DATE, TOD, DT, STRING, BYTE, WORD, DWORD, LWORD |
| **User Data Types** | Any structure, enumeration, or array type you've created in the project |
| **System Libraries** | Types provided by included system libraries |
| **User Libraries** | Types provided by user-imported libraries |
| **Array** | Opens an Array modal dialog where you define an inline array type |

This flexibility means a structure's fields can be simple base types, other structures (nesting), enumerations, or arrays.

### Array Fields via the Modal Dialog

When you select **Array** from the type dropdown, a modal dialog opens where you configure an inline array type for that specific field. The modal works exactly like the standalone [Array editor](array-datatypes): you choose a base type, add dimension rows, and define the ranges.

This is useful when a structure needs to contain a fixed-size collection — for example, a `SensorBank` structure with a field `Readings : ARRAY [0..9] OF REAL`.

### Setting Initial Values

The **Initial Value** column lets you specify a default value for individual fields. When a variable of this structure type is created, each field starts with its initial value (or the type's default zero value if none is set).

- For numeric fields: enter a number (e.g., `0`, `100.0`).
- For BOOL fields: enter `TRUE` or `FALSE`.
- For TIME fields: enter a time literal (e.g., `T#5s`).
- For STRING fields: enter the string value.

## Examples

### SensorData

A structure for bundling a sensor reading with its metadata.

**Configuration:**

| # | Name | Type | Initial Value |
|---|------|------|---------------|
| 1 | Value | REAL | 0.0 |
| 2 | Valid | BOOL | FALSE |
| 3 | Timestamp | DT | |
| 4 | SensorId | INT | 0 |

**IEC 61131-3 representation:**

```
TYPE SensorData :
  STRUCT
    Value : REAL := 0.0;
    Valid : BOOL := FALSE;
    Timestamp : DT;
    SensorId : INT := 0;
  END_STRUCT
END_TYPE
```

### MotorConfig

A structure grouping all parameters for a motor drive.

**Configuration:**

| # | Name | Type | Initial Value |
|---|------|------|---------------|
| 1 | Speed | REAL | 0.0 |
| 2 | Direction | BOOL | FALSE |
| 3 | Enabled | BOOL | FALSE |
| 4 | MaxCurrent | REAL | 10.0 |
| 5 | RampTime | TIME | T#2s |

**IEC 61131-3 representation:**

```
TYPE MotorConfig :
  STRUCT
    Speed : REAL := 0.0;
    Direction : BOOL := FALSE;
    Enabled : BOOL := FALSE;
    MaxCurrent : REAL := 10.0;
    RampTime : TIME := T#2s;
  END_STRUCT
END_TYPE
```

### PIDParams

A structure for PID controller tuning parameters.

**Configuration:**

| # | Name | Type | Initial Value |
|---|------|------|---------------|
| 1 | Kp | REAL | 1.0 |
| 2 | Ki | REAL | 0.0 |
| 3 | Kd | REAL | 0.0 |
| 4 | Setpoint | REAL | 0.0 |
| 5 | MinOutput | REAL | 0.0 |
| 6 | MaxOutput | REAL | 100.0 |

**IEC 61131-3 representation:**

```
TYPE PIDParams :
  STRUCT
    Kp : REAL := 1.0;
    Ki : REAL := 0.0;
    Kd : REAL := 0.0;
    Setpoint : REAL := 0.0;
    MinOutput : REAL := 0.0;
    MaxOutput : REAL := 100.0;
  END_STRUCT
END_TYPE
```

## Structures Containing Other User-Defined Types

One of the most powerful aspects of structures is that their fields can be other user-defined types. This lets you build layered, domain-specific data models.

**Example: A structure with an enumeration field:**

Assuming you have the `AlarmLevel` enumeration (NONE, INFO, WARNING, CRITICAL):

| # | Name | Type | Initial Value |
|---|------|------|---------------|
| 1 | Active | BOOL | FALSE |
| 2 | Level | AlarmLevel | NONE |
| 3 | Message | STRING | |
| 4 | Time | DT | |

**Example: A structure with an array field:**

| # | Name | Type | Initial Value |
|---|------|------|---------------|
| 1 | ChannelId | INT | 0 |
| 2 | Readings | ARRAY [0..9] OF REAL | |
| 3 | Average | REAL | 0.0 |
| 4 | Valid | BOOL | FALSE |

The `Readings` field is configured using the Array modal dialog accessible from the Type dropdown.

## Accessing Structure Fields in Code

In Structured Text, you access individual fields using **dot notation**:

```
(* Declare in the variables table: sensor : SensorData *)

(* Write to fields *)
sensor.Value := 23.7;
sensor.Valid := TRUE;
sensor.SensorId := 5;

(* Read from fields *)
currentTemp := sensor.Value;
IF sensor.Valid THEN
    process_reading(sensor.Value);
END_IF;
```

For nested structures (a structure containing another structure):

```
(* If MotorUnit has a field Config of type MotorConfig *)
myMotor.Config.Speed := 1500.0;
myMotor.Config.Enabled := TRUE;
```

For structure fields that are arrays:

```
(* If ChannelData has a field Readings of type ARRAY [0..9] OF REAL *)
channel.Readings[3] := 42.5;
avgValue := channel.Average;
```

## Tips for Working with Structures

> **Tip:** Keep structures focused. A structure should represent one coherent concept. If it grows beyond 10–12 fields, consider splitting it into smaller, nested structures.

> **Tip:** Use initial values for safe defaults. Setting `Enabled := FALSE` and `MaxCurrent := 10.0` in the type definition means every new variable of that type starts in a known, safe state.

- **Combine structures with arrays** for powerful data tables. An array of `SensorData` (declared as `ARRAY [0..19] OF SensorData`) gives you a table of 20 sensor readings, each with its own value, validity, timestamp, and ID.
- **Reuse structures across POUs.** Once defined, a structure type is available project-wide. Define it once, use it everywhere.

---

## What's Next?

Learn how to put your custom types to work in real programs with [Using Custom Data Types](using-custom-types).
