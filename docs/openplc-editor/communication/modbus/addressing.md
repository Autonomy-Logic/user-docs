# Modbus Addressing

This page explains how IEC 61131-3 addresses in OpenPLC map to Modbus addresses, enabling communication between your PLC program and Modbus clients or servers.

## Address Mapping Overview

OpenPLC uses a direct mapping between IEC 61131-3 located variables and Modbus addresses. Understanding this mapping is essential for integrating OpenPLC with SCADA systems, HMIs, and other Modbus devices.

## IEC 61131-3 Address Format

IEC 61131-3 addresses follow this format: `%[I|Q|M][X|B|W|D|L]<address>`

| Prefix | Meaning |
|--------|---------|
| %I | Input |
| %Q | Output |
| %M | Memory |

| Size | Meaning | Bits |
|------|---------|------|
| X | Bit | 1 |
| B | Byte | 8 |
| W | Word | 16 |
| D | Double Word | 32 |
| L | Long Word | 64 |

## Modbus Server Address Mapping

When OpenPLC acts as a Modbus server (slave), the following mappings apply:

### Discrete Inputs (FC 2)

| Modbus Address | IEC Address | Description |
|----------------|-------------|-------------|
| 0 | %IX0.0 | Digital input bit 0 |
| 1 | %IX0.1 | Digital input bit 1 |
| ... | ... | ... |
| 7 | %IX0.7 | Digital input bit 7 |
| 8 | %IX1.0 | Digital input bit 8 |
| ... | ... | ... |
| 7999 | %IX999.7 | Digital input bit 7999 |

### Coils (FC 1, 5, 15)

| Modbus Address | IEC Address | Description |
|----------------|-------------|-------------|
| 0 | %QX0.0 | Digital output bit 0 |
| 1 | %QX0.1 | Digital output bit 1 |
| ... | ... | ... |
| 7 | %QX0.7 | Digital output bit 7 |
| 8 | %QX1.0 | Digital output bit 8 |
| ... | ... | ... |
| 7999 | %QX999.7 | Digital output bit 7999 |

### Input Registers (FC 4)

| Modbus Address | IEC Address | Description |
|----------------|-------------|-------------|
| 0 | %IW0 | Analog input word 0 |
| 1 | %IW1 | Analog input word 1 |
| ... | ... | ... |
| 999 | %IW999 | Analog input word 999 |

### Holding Registers (FC 3, 6, 16)

| Modbus Address | IEC Address | Description |
|----------------|-------------|-------------|
| 0 | %QW0 | Analog output word 0 |
| 1 | %QW1 | Analog output word 1 |
| ... | ... | ... |
| 999 | %QW999 | Analog output word 999 |

## Memory Addresses

Memory addresses (%M) can also be accessed via Modbus:

### Memory Bits (via Coils)

| Modbus Address | IEC Address |
|----------------|-------------|
| 8000 | %MX0.0 |
| 8001 | %MX0.1 |
| ... | ... |

### Memory Words (via Holding Registers)

| Modbus Address | IEC Address |
|----------------|-------------|
| 1000 | %MW0 |
| 1001 | %MW1 |
| ... | ... |

## 32-bit and 64-bit Values

For 32-bit (DINT, REAL) and 64-bit (LINT, LREAL) values, multiple consecutive Modbus registers are used:

### 32-bit Values (2 registers)

| IEC Address | Modbus Registers |
|-------------|------------------|
| %QD0 | Registers 0-1 |
| %QD1 | Registers 2-3 |
| %MD0 | Registers 1000-1001 |

### 64-bit Values (4 registers)

| IEC Address | Modbus Registers |
|-------------|------------------|
| %QL0 | Registers 0-3 |
| %QL1 | Registers 4-7 |
| %ML0 | Registers 1000-1003 |

## Byte Order

OpenPLC uses big-endian byte order for multi-byte values, which is the standard for Modbus. When reading 32-bit values:

- Register N contains the high word
- Register N+1 contains the low word

## Practical Examples

### Reading a Digital Input from SCADA

To read digital input %IX0.0 from a SCADA system:
- Use Function Code 2 (Read Discrete Inputs)
- Read from Modbus address 0

### Writing an Analog Output from HMI

To write to analog output %QW10 from an HMI:
- Use Function Code 6 (Write Single Register) or FC 16 (Write Multiple Registers)
- Write to Modbus address 10

### Reading a 32-bit Float

To read a REAL value stored at %MD100:
- Use Function Code 3 (Read Holding Registers)
- Read 2 registers starting at Modbus address 1100
- Combine the two 16-bit values into a 32-bit float

## Address Calculation Formulas

### Bit Addresses

```
Modbus_Address = (Byte_Number * 8) + Bit_Number
```

Example: %IX5.3 = (5 * 8) + 3 = 43

### Word Addresses

```
Modbus_Address = Word_Number
```

Example: %IW25 = 25

### Memory Addresses

```
Modbus_Coil = 8000 + (Byte_Number * 8) + Bit_Number
Modbus_Register = 1000 + Word_Number
```

## Common Issues

### Address Offset Confusion

Some Modbus clients use 1-based addressing (addresses start at 1 instead of 0). If your client shows address 40001 for the first holding register, subtract 40001 to get the OpenPLC address (0).

### Data Type Mismatch

Ensure your SCADA/HMI is configured to interpret the data correctly:
- Coils and discrete inputs are single bits
- Registers are 16-bit unsigned integers by default
- 32-bit values span two consecutive registers
