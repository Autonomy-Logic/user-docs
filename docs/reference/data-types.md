# Data Types Reference

Every variable in your PLC program has a data type that determines its range, precision, memory usage, and allowed operations. This page covers all IEC 61131-3 data types supported by Autonomy Edge.

## Elementary Data Types

### Boolean

| Type | Size | Range | Default | Description |
|------|------|-------|---------|-------------|
| `BOOL` | 1 bit | `TRUE` / `FALSE` | `FALSE` | Binary value; used for digital I/O, flags, and conditions |

**Literals:** `TRUE`, `FALSE`, `0`, `1`

### Integer Types

| Type | Size | Range | Default | Description |
|------|------|-------|---------|-------------|
| `SINT` | 8 bits | -128 to 127 | 0 | Short integer |
| `INT` | 16 bits | -32,768 to 32,767 | 0 | Standard integer |
| `DINT` | 32 bits | -2,147,483,648 to 2,147,483,647 | 0 | Double integer |
| `LINT` | 64 bits | -9.2 × 10¹⁸ to 9.2 × 10¹⁸ | 0 | Long integer |

**Literals:** Decimal (`42`), hexadecimal (`16#2A`), octal (`8#52`), binary (`2#101010`)

### Unsigned Integer Types

| Type | Size | Range | Default | Description |
|------|------|-------|---------|-------------|
| `USINT` | 8 bits | 0 to 255 | 0 | Unsigned short integer |
| `UINT` | 16 bits | 0 to 65,535 | 0 | Unsigned integer |
| `UDINT` | 32 bits | 0 to 4,294,967,295 | 0 | Unsigned double integer |
| `ULINT` | 64 bits | 0 to 1.8 × 10¹⁹ | 0 | Unsigned long integer |

### Floating-Point Types

| Type | Size | Range | Precision | Default | Description |
|------|------|-------|-----------|---------|-------------|
| `REAL` | 32 bits | ±3.4 × 10³⁸ | ~7 decimal digits | 0.0 | Single-precision float |
| `LREAL` | 64 bits | ±1.8 × 10³⁰⁸ | ~15 decimal digits | 0.0 | Double-precision float |

**Literals:** `3.14`, `-0.001`, `1.0E3` (scientific notation)

> **Tip:** Use `REAL` for most analog values (temperature, pressure, level). Use `LREAL` when precision matters — accumulated totals, precise calculations, or high-resolution measurements.

### Time Types

| Type | Size | Range | Default | Description |
|------|------|-------|---------|-------------|
| `TIME` | 32 bits | T#0ms to T#49d17h2m47s295ms | `T#0s` | Duration / time span |
| `DATE` | 32 bits | D#1970-01-01 to D#2106-02-07 | `D#1970-01-01` | Calendar date |
| `TIME_OF_DAY` / `TOD` | 32 bits | TOD#00:00:00 to TOD#23:59:59.999 | `TOD#00:00:00` | Time of day |
| `DATE_AND_TIME` / `DT` | 64 bits | DT#1970-01-01-00:00:00 to DT#2106-... | `DT#1970-01-01-00:00:00` | Date and time combined |

**TIME literals:**

| Literal | Value |
|---------|-------|
| `T#500ms` | 500 milliseconds |
| `T#5s` | 5 seconds |
| `T#1m30s` | 1 minute 30 seconds |
| `T#2h15m` | 2 hours 15 minutes |
| `T#1d12h` | 1 day 12 hours |
| `T#100ms` | 100 milliseconds |

**DATE literals:** `D#2025-03-14`, `D#2025-12-31`

**TOD literals:** `TOD#08:30:00`, `TOD#23:59:59`

**DT literals:** `DT#2025-03-14-08:30:00`

### String Types

| Type | Size | Max Length | Default | Description |
|------|------|-----------|---------|-------------|
| `STRING` | Variable | 253 characters | `''` (empty) | Single-byte character string |
| `WSTRING` | Variable | 253 characters | `""` (empty) | Wide (Unicode) character string |

**Literals:** `'Hello World'` (STRING), `"Hello World"` (WSTRING)

### Byte String Types

| Type | Size | Range | Default | Description |
|------|------|-------|---------|-------------|
| `BYTE` | 8 bits | 16#00 to 16#FF | 16#00 | 8-bit bit string |
| `WORD` | 16 bits | 16#0000 to 16#FFFF | 16#0000 | 16-bit bit string |
| `DWORD` | 32 bits | 16#00000000 to 16#FFFFFFFF | 16#00000000 | 32-bit bit string |
| `LWORD` | 64 bits | 16#0...0 to 16#F...F | 16#0...0 | 64-bit bit string |

Byte string types are used for bitwise operations, packed flags, and raw data manipulation. They support bitwise AND, OR, XOR, NOT, SHL, SHR, ROL, and ROR operators.

## Type Conversion Functions

IEC 61131-3 requires explicit type conversion between incompatible types. The naming convention is `<FROM>_TO_<TO>()`.

### Numeric Conversions

| Function | From | To | Notes |
|----------|------|----|-------|
| `INT_TO_REAL()` | `INT` | `REAL` | No precision loss |
| `REAL_TO_INT()` | `REAL` | `INT` | Truncates decimal portion |
| `DINT_TO_INT()` | `DINT` | `INT` | May overflow if value exceeds INT range |
| `INT_TO_DINT()` | `INT` | `DINT` | No precision loss |
| `SINT_TO_INT()` | `SINT` | `INT` | No precision loss |
| `INT_TO_SINT()` | `INT` | `SINT` | May overflow if value exceeds SINT range |
| `REAL_TO_LREAL()` | `REAL` | `LREAL` | No precision loss |
| `LREAL_TO_REAL()` | `LREAL` | `REAL` | May lose precision |
| `UINT_TO_INT()` | `UINT` | `INT` | May overflow if value > 32767 |
| `INT_TO_UINT()` | `INT` | `UINT` | Negative values become large positive |

### Boolean Conversions

| Function | From | To | Notes |
|----------|------|----|-------|
| `BOOL_TO_INT()` | `BOOL` | `INT` | FALSE → 0, TRUE → 1 |
| `INT_TO_BOOL()` | `INT` | `BOOL` | 0 → FALSE, non-zero → TRUE |
| `BOOL_TO_REAL()` | `BOOL` | `REAL` | FALSE → 0.0, TRUE → 1.0 |
| `BOOL_TO_BYTE()` | `BOOL` | `BYTE` | FALSE → 16#00, TRUE → 16#01 |

### String Conversions

| Function | From | To | Notes |
|----------|------|----|-------|
| `INT_TO_STRING()` | `INT` | `STRING` | e.g., 42 → `'42'` |
| `STRING_TO_INT()` | `STRING` | `INT` | e.g., `'42'` → 42 |
| `REAL_TO_STRING()` | `REAL` | `STRING` | Formatted decimal |
| `STRING_TO_REAL()` | `STRING` | `REAL` | Parses decimal string |
| `BOOL_TO_STRING()` | `BOOL` | `STRING` | `'TRUE'` or `'FALSE'` |

### Time Conversions

| Function | From | To | Notes |
|----------|------|----|-------|
| `TIME_TO_DINT()` | `TIME` | `DINT` | Value in milliseconds |
| `DINT_TO_TIME()` | `DINT` | `TIME` | Milliseconds to TIME |
| `TIME_TO_REAL()` | `TIME` | `REAL` | Value in milliseconds as float |

## Choosing the Right Data Type

| Use Case | Recommended Type | Why |
|----------|-----------------|-----|
| Digital I/O, flags | `BOOL` | Smallest, most efficient for ON/OFF |
| Small counter or index | `INT` | Sufficient for most counting tasks |
| Large counter or accumulator | `DINT` | Handles values up to ~2 billion |
| Analog sensor value | `REAL` | Fractional values with adequate precision |
| Timer preset or elapsed | `TIME` | Native time type with duration literals |
| Bit manipulation, masks | `BYTE`, `WORD` | Direct bitwise access |
| Text display or logging | `STRING` | Variable-length character data |
| Very large counts | `LINT` or `ULINT` | 64-bit range for extreme values |

## I/O Address Mapping

Data types determine how located variables map to the I/O image table:

| Address Prefix | Size | Data Type Equivalent | Example |
|----------------|------|---------------------|---------|
| `%IX` / `%QX` | 1 bit | `BOOL` | `%IX0.0` — Digital input, byte 0, bit 0 |
| `%IB` / `%QB` | 8 bits | `BYTE` / `SINT` | `%IB0` — Input byte 0 |
| `%IW` / `%QW` | 16 bits | `WORD` / `INT` | `%IW0` — Input word 0 (analog) |
| `%ID` / `%QD` | 32 bits | `DWORD` / `DINT` / `REAL` | `%ID0` — Input double word 0 |
| `%IL` / `%QL` | 64 bits | `LWORD` / `LINT` / `LREAL` | `%IL0` — Input long word 0 |
| `%MW` | 16 bits | `WORD` / `INT` | `%MW0` — Memory word 0 |
| `%MD` | 32 bits | `DWORD` / `DINT` | `%MD0` — Memory double word 0 |

## Type Compatibility Rules

### Implicit Compatibility

Some types are implicitly compatible in expressions:

- Integer types in arithmetic: `SINT`, `INT`, `DINT`, `LINT` can be mixed (smaller promotes to larger)
- Float types: `REAL` and `LREAL` can be mixed (`REAL` promotes to `LREAL`)

### Explicit Conversion Required

These combinations require explicit conversion functions:

- Integer ↔ Float: `INT_TO_REAL()`, `REAL_TO_INT()`
- Numeric ↔ String: `INT_TO_STRING()`, `STRING_TO_INT()`
- Boolean ↔ Numeric: `BOOL_TO_INT()`, `INT_TO_BOOL()`
- Time ↔ Numeric: `TIME_TO_DINT()`, `DINT_TO_TIME()`

## What's Next?

- [IEC 61131-3 Keywords](iec-keywords) — Reserved keywords reference
- [Glossary](glossary) — Definitions of key terms
- [Variables and Data Types](../openplc-editor/iec-concepts/variables-datatypes) — Working with variables in the IDE
