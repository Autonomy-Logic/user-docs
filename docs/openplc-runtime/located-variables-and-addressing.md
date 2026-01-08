# Located Variables and Addressing

This page explains the IEC 61131-3 addressing system used in OpenPLC for mapping variables to physical I/O and memory locations.

## Understanding Located Variables

In IEC 61131-3, located variables are variables that are bound to specific memory addresses. These addresses represent physical inputs, outputs, or internal memory locations in the PLC.

## Address Format

IEC 61131-3 addresses follow this format:

```
%[Location][Size][Address]
```

### Location Prefixes

| Prefix | Meaning | Description |
|--------|---------|-------------|
| %I | Input | Physical inputs from sensors, switches, etc. |
| %Q | Output | Physical outputs to actuators, relays, etc. |
| %M | Memory | Internal memory for intermediate values |

### Size Specifiers

| Specifier | Size | Data Type | Range |
|-----------|------|-----------|-------|
| X | 1 bit | BOOL | 0 or 1 |
| B | 8 bits | BYTE | 0 to 255 |
| W | 16 bits | WORD | 0 to 65535 |
| D | 32 bits | DWORD | 0 to 4294967295 |
| L | 64 bits | LWORD | 0 to 2^64-1 |

## Address Examples

### Bit Addresses (X)

Bit addresses use the format `%[I|Q|M]X<byte>.<bit>`:

| Address | Description |
|---------|-------------|
| %IX0.0 | Input byte 0, bit 0 |
| %IX0.7 | Input byte 0, bit 7 |
| %IX1.0 | Input byte 1, bit 0 |
| %QX0.0 | Output byte 0, bit 0 |
| %MX0.0 | Memory byte 0, bit 0 |

### Byte Addresses (B)

| Address | Description |
|---------|-------------|
| %IB0 | Input byte 0 (bits 0-7) |
| %IB1 | Input byte 1 (bits 8-15) |
| %QB0 | Output byte 0 |
| %MB0 | Memory byte 0 |

### Word Addresses (W)

| Address | Description |
|---------|-------------|
| %IW0 | Input word 0 (bytes 0-1) |
| %IW1 | Input word 1 (bytes 2-3) |
| %QW0 | Output word 0 |
| %MW0 | Memory word 0 |

### Double Word Addresses (D)

| Address | Description |
|---------|-------------|
| %ID0 | Input double word 0 (bytes 0-3) |
| %QD0 | Output double word 0 |
| %MD0 | Memory double word 0 |

### Long Word Addresses (L)

| Address | Description |
|---------|-------------|
| %IL0 | Input long word 0 (bytes 0-7) |
| %QL0 | Output long word 0 |
| %ML0 | Memory long word 0 |

## Address Overlap

Different size specifiers can access the same physical memory. For example:

- %IW0 contains %IB0 and %IB1
- %IB0 contains %IX0.0 through %IX0.7
- %ID0 contains %IW0 and %IW1

Be careful when using overlapping addresses to avoid unintended side effects.

## Memory Map

### Input Memory (%I)

Used for reading values from physical inputs or communication protocols.

| Address Range | Size | Typical Use |
|---------------|------|-------------|
| %IX0.0 - %IX999.7 | 8000 bits | Digital inputs |
| %IW0 - %IW999 | 1000 words | Analog inputs |

### Output Memory (%Q)

Used for writing values to physical outputs or communication protocols.

| Address Range | Size | Typical Use |
|---------------|------|-------------|
| %QX0.0 - %QX999.7 | 8000 bits | Digital outputs |
| %QW0 - %QW999 | 1000 words | Analog outputs |

### Internal Memory (%M)

Used for internal calculations and data storage.

| Address Range | Size | Typical Use |
|---------------|------|-------------|
| %MX0.0 - ... | Variable | Internal flags |
| %MW0 - ... | Variable | Internal registers |
| %MD0 - ... | Variable | 32-bit values |

## Using Located Variables in Programs

### Declaration

In Structured Text, declare located variables like this:

```
VAR
    StartButton AT %IX0.0 : BOOL;
    MotorSpeed AT %IW0 : INT;
    MotorRun AT %QX0.0 : BOOL;
    SetPoint AT %MW0 : INT;
END_VAR
```

### Direct Access

You can also access addresses directly without declaration:

```
IF %IX0.0 THEN
    %QX0.0 := TRUE;
END_IF;
```

However, using declared variables with meaningful names is recommended for readability.

## Best Practices

### Use Meaningful Names

Always declare located variables with descriptive names:

```
(* Good *)
StartButton AT %IX0.0 : BOOL;

(* Avoid *)
Input1 AT %IX0.0 : BOOL;
```

### Document Your Address Map

Maintain a document listing all used addresses and their purposes.

### Avoid Address Conflicts

Plan your address usage to prevent overlapping assignments that could cause unexpected behavior.

### Group Related Addresses

Organize addresses logically:
- %IX0.x - %IX3.x: Machine 1 inputs
- %IX4.x - %IX7.x: Machine 2 inputs
- etc.
