# IEC 61131-3 Keywords

All reserved keywords in the IEC 61131-3 standard are listed here. These words have special meaning in PLC programming languages and you can't use them as variable names, POU names, or identifiers.

> **Tip:** Keywords are case-insensitive in IEC 61131-3 — `IF`, `If`, and `if` are all treated the same.

## Data Type Keywords

These keywords declare or reference data types.

| Keyword | Description |
|---------|-------------|
| `BOOL` | Boolean data type (TRUE/FALSE) |
| `SINT` | Short integer (8-bit signed) |
| `INT` | Integer (16-bit signed) |
| `DINT` | Double integer (32-bit signed) |
| `LINT` | Long integer (64-bit signed) |
| `USINT` | Unsigned short integer (8-bit) |
| `UINT` | Unsigned integer (16-bit) |
| `UDINT` | Unsigned double integer (32-bit) |
| `ULINT` | Unsigned long integer (64-bit) |
| `REAL` | Single-precision floating point (32-bit) |
| `LREAL` | Double-precision floating point (64-bit) |
| `TIME` | Time duration |
| `DATE` | Calendar date |
| `TIME_OF_DAY` | Time of day |
| `TOD` | Alias for TIME_OF_DAY |
| `DATE_AND_TIME` | Combined date and time |
| `DT` | Alias for DATE_AND_TIME |
| `STRING` | Single-byte character string |
| `WSTRING` | Wide (Unicode) character string |
| `BYTE` | 8-bit bit string |
| `WORD` | 16-bit bit string |
| `DWORD` | 32-bit bit string |
| `LWORD` | 64-bit bit string |

## Constant Keywords

| Keyword | Description |
|---------|-------------|
| `TRUE` | Boolean literal for logical true (1) |
| `FALSE` | Boolean literal for logical false (0) |

## Variable Declaration Keywords

These keywords define variable blocks within POUs.

| Keyword | Closing | Description |
|---------|---------|-------------|
| `VAR` | `END_VAR` | Local variables (internal to the POU) |
| `VAR_INPUT` | `END_VAR` | Input parameters (read-only inside the POU) |
| `VAR_OUTPUT` | `END_VAR` | Output parameters (writable, visible to callers) |
| `VAR_IN_OUT` | `END_VAR` | In-out parameters (read/write, passed by reference) |
| `VAR_EXTERNAL` | `END_VAR` | References to global variables |
| `VAR_GLOBAL` | `END_VAR` | Global variable declarations |
| `VAR_TEMP` | `END_VAR` | Temporary variables (not retained between calls) |
| `VAR_ACCESS` | `END_VAR` | Access path declarations for communication |
| `CONSTANT` | — | Modifier: variable value cannot change after initialization |
| `RETAIN` | — | Modifier: variable value survives power cycles |
| `NON_RETAIN` | — | Modifier: variable resets on power cycle |
| `AT` | — | Binds a variable to a located address (e.g., `AT %IX0.0`) |

## POU Declaration Keywords

These keywords define Program Organization Units.

| Keyword | Closing | Description |
|---------|---------|-------------|
| `PROGRAM` | `END_PROGRAM` | Declares a Program POU |
| `FUNCTION` | `END_FUNCTION` | Declares a Function POU (stateless, single return value) |
| `FUNCTION_BLOCK` | `END_FUNCTION_BLOCK` | Declares a Function Block POU (stateful, multiple outputs) |

## Configuration Keywords

These keywords define the runtime configuration structure.

| Keyword | Closing | Description |
|---------|---------|-------------|
| `CONFIGURATION` | `END_CONFIGURATION` | Top-level configuration declaration |
| `RESOURCE` | `END_RESOURCE` | Processing resource within a configuration |
| `TASK` | — | Task definition (specifies execution interval) |
| `WITH` | — | Associates a Program with a Task |
| `ON` | — | Specifies the resource for a task definition |

## Structured Text Control Flow Keywords

### Conditional Statements

| Keyword | Description |
|---------|-------------|
| `IF` | Begins a conditional statement |
| `THEN` | Marks the start of the conditional body |
| `ELSIF` | Additional condition in an IF chain |
| `ELSE` | Default branch when no conditions are TRUE |
| `END_IF` | Closes an IF statement |

### Selection Statement

| Keyword | Description |
|---------|-------------|
| `CASE` | Begins a multi-way selection statement |
| `OF` | Follows the selector expression in a CASE |
| `END_CASE` | Closes a CASE statement |

### Loop Statements

| Keyword | Description |
|---------|-------------|
| `FOR` | Begins a counted loop |
| `TO` | Specifies the end value in a FOR loop |
| `BY` | Specifies the step value in a FOR loop (optional, default 1) |
| `DO` | Marks the start of the loop body |
| `END_FOR` | Closes a FOR loop |
| `WHILE` | Begins a condition-checked loop (check before) |
| `END_WHILE` | Closes a WHILE loop |
| `REPEAT` | Begins a condition-checked loop (check after) |
| `UNTIL` | Specifies the exit condition in a REPEAT loop |
| `END_REPEAT` | Closes a REPEAT loop |
| `EXIT` | Immediately exits the innermost loop |
| `RETURN` | Immediately exits the current POU |
| `CONTINUE` | Skips to the next iteration of the innermost loop |

## Operator Keywords

### Arithmetic

| Keyword | Description |
|---------|-------------|
| `MOD` | Modulo (remainder after division) |

### Logical

| Keyword | Description |
|---------|-------------|
| `AND` | Logical/bitwise AND |
| `OR` | Logical/bitwise OR |
| `XOR` | Logical/bitwise exclusive OR |
| `NOT` | Logical/bitwise negation |

### Bitwise Shift

| Keyword | Description |
|---------|-------------|
| `SHL` | Shift left |
| `SHR` | Shift right |
| `ROL` | Rotate left |
| `ROR` | Rotate right |

## User-Defined Type Keywords

| Keyword | Closing | Description |
|---------|---------|-------------|
| `TYPE` | `END_TYPE` | Begins a user-defined type declaration |
| `STRUCT` | `END_STRUCT` | Declares a structured (record) type |
| `ARRAY` | — | Declares an array type |
| `OF` | — | Specifies the element type of an array |

## Standard Function Keywords

These are built-in functions available in all IEC 61131-3 implementations.

### Numeric Functions

| Keyword | Description |
|---------|-------------|
| `ABS` | Absolute value |
| `SQRT` | Square root |
| `EXP` | Exponential (e^x) |
| `LN` | Natural logarithm |
| `LOG` | Base-10 logarithm |
| `SIN` | Sine (radians) |
| `COS` | Cosine (radians) |
| `TAN` | Tangent (radians) |
| `ASIN` | Arc sine |
| `ACOS` | Arc cosine |
| `ATAN` | Arc tangent |
| `EXPT` | Exponentiation (base^exponent) |

### Selection Functions

| Keyword | Description |
|---------|-------------|
| `SEL` | Binary selection: SEL(G, IN0, IN1) — returns IN0 if G=FALSE, IN1 if G=TRUE |
| `MAX` | Maximum of inputs |
| `MIN` | Minimum of inputs |
| `LIMIT` | Clamp value: LIMIT(MN, IN, MX) — returns IN clamped to [MN, MX] |
| `MUX` | Multiplexer: selects one of N inputs based on index |

### Comparison Functions

| Keyword | Description |
|---------|-------------|
| `GT` | Greater than |
| `GE` | Greater than or equal |
| `EQ` | Equal |
| `LE` | Less than or equal |
| `LT` | Less than |
| `NE` | Not equal |

### String Functions

| Keyword | Description |
|---------|-------------|
| `LEN` | String length |
| `LEFT` | Left substring |
| `RIGHT` | Right substring |
| `MID` | Middle substring |
| `CONCAT` | String concatenation |
| `INSERT` | Insert substring |
| `DELETE` | Delete characters from string |
| `REPLACE` | Replace substring |
| `FIND` | Find position of substring |

## Reserved Address Prefixes

These prefixes are used in located variable addresses and are reserved:

| Prefix | Description |
|--------|-------------|
| `%I` | Input address space |
| `%Q` | Output address space |
| `%M` | Memory (marker) address space |
| `X` | Bit size (1 bit) |
| `B` | Byte size (8 bits) |
| `W` | Word size (16 bits) |
| `D` | Double word size (32 bits) |
| `L` | Long word size (64 bits) |

## What's Next?

- [Data Types Reference](data-types) — Detailed data type specifications
- [Standard Function Blocks Reference](function-blocks) — Quick reference for all standard FBs
- [Glossary](glossary) — Definitions of key terms
