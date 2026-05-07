# Creating Data Types

In any PLC project of meaningful size, the built-in data types (BOOL, INT, REAL, etc.) quickly become insufficient for organizing your data clearly. Imagine a program that tracks 20 temperature sensors, each with a value, an alarm status, and a timestamp. Without user-defined types, you'd need dozens of individual variables with carefully coordinated names — a recipe for confusion and bugs.

IEC 61131-3 solves this with **user-defined data types**. These let you define your own types that group, structure, and constrain data in ways that match your application's real-world domain. Once defined, a custom type works just like a built-in type: you can declare variables, pass them to functions and function blocks, and use them across your entire project.

## The Three Kinds of User-Defined Types

The Autonomy Edge IDE supports three derivations of user-defined data types:

| Derivation | Purpose | Example Use Case |
|------------|---------|------------------|
| **Array** | An ordered collection of elements, all of the same type | A bank of 10 temperature sensors, all stored as REAL values |
| **Enumeration** | A set of named values — the variable can hold exactly one | Machine states like IDLE, RUNNING, PAUSED, FAULTED |
| **Structure** | A composite type grouping multiple named fields of different types | A sensor reading bundling a REAL value, a BOOL validity flag, and a DT timestamp |

### When to Use Each Type

**Choose an Array when** you have multiple values of the same type that logically belong together. Arrays are ideal for sensor banks, recipe tables, data buffers, and lookup tables. If you find yourself creating variables like `temp_1`, `temp_2`, `temp_3`, an array is the better approach.

**Choose an Enumeration when** a variable should only hold one value from a fixed set of named options. Enumerations make your code self-documenting — `state := RUNNING` is far clearer than `state := 2`. They're perfect for machine states, operating modes, alarm levels, and command codes.

**Choose a Structure when** you have several related values of different types that logically belong together. Structures let you treat a group of fields as a single unit — you can declare one variable instead of five, pass it to a function block as one parameter, and keep your variable tables clean.

## Creating a Data Type in the IDE

### Step 1: Open the Creation Dialog

Click the **+** (plus) button next to your project name at the top of the Project Explorer sidebar. This opens the element creation dialog.

### Step 2: Select Data Type

In the creation dialog, choose to create a **Data Type**. You'll see three icons representing the available derivations:

| Icon | Derivation | Description |
|------|------------|-------------|
| Array icon | **Array** | Creates an array data type |
| Enum icon | **Enumeration** | Creates an enumerated data type |
| Structure icon | **Structure** | Creates a structure data type |

### Step 3: Name Your Data Type

Enter a name for your data type. The name must follow these rules:

- Must be a valid IEC 61131-3 identifier (letters, digits, and underscores; cannot start with a digit).
- **Cannot conflict** with any existing POU (Program, Function, or Function Block) name.
- **Cannot conflict** with any other existing data type name.
- Should be descriptive — names like `SensorData`, `MachineState`, or `TemperatureBuffer` clearly communicate the type's purpose.

### Step 4: Choose the Derivation

Select whether your data type will be an Array, Enumeration, or Structure by clicking the corresponding icon.

### Step 5: Create

Click **Create**. The new data type appears in the **Data Types** branch of the Project Explorer, categorized under its derivation.

### Step 6: Configure

Click the newly created data type in the Project Explorer to open its editor. Each derivation has a specialized editor:

- **Array editor** — Set the base type, define dimensions, and optionally provide an initial value.
- **Enumeration editor** — Add named values and select a default initial value.
- **Structure editor** — Add fields with names, types, and optional initial values.

## The Data Types Branch

In the Project Explorer, all user-defined data types appear under the **Data Types** branch, subdivided by derivation:

```
Project Name
  +-- Functions
  +-- Function Blocks
  +-- Programs
  +-- Data Types
  |     +-- Arrays
  |     |     +-- TemperatureBuffer
  |     |     +-- LookupTable
  |     +-- Enumerations
  |     |     +-- MachineState
  |     |     +-- AlarmLevel
  |     +-- Structures
  |           +-- SensorData
  |           +-- MotorConfig
  +-- Resources
  +-- Devices
  +-- Servers
```

Each data type displays a label indicating its derivation ("arr" for arrays, "enum" for enumerations, "str" for structures). Click any data type to open its editor.

## Overview of the Type Editors

### Array Editor

The array editor presents a compact form with:

- A **Base Type** dropdown to choose the element type (any base type or user-defined type).
- An **Initial Value** text field for an optional default value.
- A **Dimensions** table where you add one or more dimension ranges (e.g., `0..9`).

### Enumeration Editor

The enumeration editor shows:

- A **Values** table where you add, remove, and reorder the named values.
- An **Initial Value** dropdown to select which value should be the default.

### Structure Editor

The structure editor displays:

- A **Variables** table with columns for row number (#), Name, Type, and Initial Value.
- Each row represents a field of the structure.
- The Type column provides a dropdown with base types, user-defined types, and the option to create an inline array type.

## IEC 61131-3 Text Representation

Here's a quick preview of how each derivation looks in IEC 61131-3 text form:

**Array:**
```
TYPE SensorBank : ARRAY [0..9] OF REAL; END_TYPE
```

**Enumeration:**
```
TYPE MachineState : (IDLE, RUNNING, PAUSED, FAULTED) := IDLE; END_TYPE
```

**Structure:**
```
TYPE SensorData :
  STRUCT
    Value : REAL;
    Valid : BOOL;
    Timestamp : DT;
  END_STRUCT
END_TYPE
```

Each is covered in full detail in its respective documentation page.

## Practical Guidelines

> **Tip:** Start simple. If you only need a few related variables, local variables may be enough. Introduce a structure when you find yourself repeating the same group of variables in multiple POUs or when the group exceeds three or four related items.

> **Tip:** Combine types for complex data models. You can create a structure whose fields include arrays and other user-defined types, or create an array whose base type is a structure. This composability is one of the most powerful aspects of the type system.

- **Name types by their domain meaning**, not their technical structure. `SensorReading` is better than `RealBoolDtStruct`. `MachineState` is better than `FourValueEnum`.

- **Plan your types before coding.** Sketch out the data model for your application before writing POU logic. Defining the right types upfront saves significant refactoring later.

- **Keep names consistent across the project.** If you name a structure `SensorData`, name the variable `sensorData` or `sensor` — not `sd` or `data1`.

---

## What's Next?

Learn how to define ordered collections of elements with [Array Data Types](array-datatypes).
