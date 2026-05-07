# Array Data Types

An array is an ordered collection of elements that all share the same data type. Instead of declaring ten separate variables for ten temperature sensors, you define a single array type and declare one variable that holds all ten values. Arrays bring order to repetitive data, simplify loops, and reduce the chance of mismatched variable names and types.

In IEC 61131-3, array types are defined with a base type (the type of each element) and one or more dimensions (the index ranges that determine the array's size). The IDE supports both single-dimensional and multi-dimensional arrays.

## Understanding Array Dimensions

Every array dimension is defined by a range in the format:

```
LEFT..RIGHT
```

Where `LEFT` is the lower bound and `RIGHT` is the upper bound, both non-negative integers. The number of elements in that dimension is `RIGHT - LEFT + 1`.

| Dimension | Elements | Indices |
|-----------|----------|---------|
| `0..9` | 10 | 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 |
| `1..5` | 5 | 1, 2, 3, 4, 5 |
| `0..99` | 100 | 0 through 99 |
| `1..1` | 1 | 1 |

**Validation rules:**

- Both bounds must be non-negative integers.
- The format must be exactly `LEFT..RIGHT` (two dots separating two numbers).
- The right bound must be strictly greater than the left bound.

### Multi-Dimensional Arrays

An array can have more than one dimension. Each additional dimension adds another index level. For example, a 2D array with dimensions `0..4` and `0..9` creates a 5-by-10 grid of elements (50 total).

To access an element in a multi-dimensional array, you provide one index per dimension:

```
myMatrix[2, 7]    (* Row 2, Column 7 of a 2D array *)
```

Multi-dimensional arrays are useful for lookup tables, coordinate grids, recipe matrices, and any data that naturally fits a tabular structure.

## The Array Editor

When you open an array data type in the IDE, the editor presents three main controls:

### Base Type Selector

A dropdown where you choose the element type for the array. You can select from:

- **Base types** — BOOL, SINT, INT, DINT, LINT, USINT, UINT, UDINT, ULINT, REAL, LREAL, TIME, DATE, TOD, DT, STRING, BYTE, WORD, DWORD, LWORD
- **User-defined types** — Any structure, enumeration, or other array type you've already created in the project

This means you can create arrays of structures (e.g., an array of `SensorData` records) or arrays of enumerations.

### Initial Value Field

An optional text field where you specify a default value for the array. If left blank, elements default to the zero/empty value of the base type (0 for integers, 0.0 for reals, FALSE for booleans, etc.).

### Dimensions Table

A table where each row represents one dimension of the array:

| Control | Action |
|---------|--------|
| **+** (Add) | Adds a new dimension row |
| **−** (Remove) | Removes the selected dimension row |
| **Up arrow** | Moves the selected dimension up (reorders dimensions) |
| **Down arrow** | Moves the selected dimension down |

Each row contains an editable text field where you enter the dimension range in `LEFT..RIGHT` format.

**To create a single-dimensional array:** Add one dimension row and enter the range (e.g., `0..9`).

**To create a multi-dimensional array:** Add multiple dimension rows. The first row is the first index, the second row is the second index, and so on.

## Examples

### Sensor Bank

A common industrial pattern: monitoring multiple sensors of the same type.

**Configuration:**

| Property | Value |
|----------|-------|
| Name | `SensorBank` |
| Base Type | `REAL` |
| Dimensions | `0..9` |

**IEC 61131-3 representation:**

```
TYPE SensorBank : ARRAY [0..9] OF REAL; END_TYPE
```

This creates a type that holds 10 real-valued sensor readings. Declare a variable `temperatures : SensorBank` and access individual readings as `temperatures[0]` through `temperatures[9]`.

### Data Buffer

A circular buffer for storing recent measurements.

**Configuration:**

| Property | Value |
|----------|-------|
| Name | `DataBuffer` |
| Base Type | `INT` |
| Dimensions | `0..255` |

**IEC 61131-3 representation:**

```
TYPE DataBuffer : ARRAY [0..255] OF INT; END_TYPE
```

### Lookup Table (2D)

A two-dimensional table for mapping inputs to outputs — for example, a speed lookup indexed by gear and throttle position.

**Configuration:**

| Property | Value |
|----------|-------|
| Name | `SpeedTable` |
| Base Type | `REAL` |
| Dimension 1 | `1..6` |
| Dimension 2 | `0..10` |

**IEC 61131-3 representation:**

```
TYPE SpeedTable : ARRAY [1..6, 0..10] OF REAL; END_TYPE
```

Access: `targetSpeed := speedLookup[gear, throttlePos];`

### Boolean Flag Array

Tracking the on/off state of multiple outputs.

**Configuration:**

| Property | Value |
|----------|-------|
| Name | `OutputFlags` |
| Base Type | `BOOL` |
| Dimensions | `0..15` |

**IEC 61131-3 representation:**

```
TYPE OutputFlags : ARRAY [0..15] OF BOOL; END_TYPE
```

## Accessing Array Elements in Code

Once you declare a variable of an array type, you access elements using bracket notation with the index.

### In Structured Text

```
(* Declare a variable of the SensorBank type *)
(* In the variables table: temps : SensorBank *)

(* Read a single element *)
currentTemp := temps[3];

(* Write to a single element *)
temps[0] := 25.5;

(* Loop through all elements *)
FOR i := 0 TO 9 DO
    IF temps[i] > highLimit THEN
        alarms[i] := TRUE;
    END_IF;
END_FOR;

(* Multi-dimensional access *)
value := speedLookup[gear, throttle];
```

### In Ladder Diagram and Function Block Diagram

In graphical languages, you typically use array elements as inputs or outputs of function blocks by referencing them with their index. For example, wire `temps[0]` as an input to a comparison block, or assign the output of a math block to `buffer[writeIndex]`.

## Working with Array Initial Values

The Initial Value field in the array editor accepts a value that's applied when the PLC starts. For simple cases, you can set a single default value. For arrays of numeric types, leaving the initial value empty means all elements start at zero (or FALSE for BOOL arrays).

If you need specific initial values for individual elements, set them in the initialization section of your program code rather than in the type definition.

## Tips for Working with Arrays

> **Tip:** Choose meaningful index ranges. Starting at 0 is conventional, but IEC 61131-3 allows any starting index. Use 1-based indexing if it matches your domain (e.g., `1..8` for 8 physical channels numbered 1 through 8).

> **Tip:** Combine with structures for rich data. An array of a structure type (e.g., `ARRAY [0..9] OF SensorData`) gives you a table of structured records — far more powerful than parallel arrays.

- **Watch your bounds.** Accessing an index outside the declared range is undefined behavior. Always validate indices before using them, especially when the index comes from a calculated value or an external input.
- **Use FOR loops** to iterate over array elements in Structured Text. The loop counter naturally maps to the array index.

---

## What's Next?

Learn how to define named value sets with [Enumerated Data Types](enumerated-datatypes).
