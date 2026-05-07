# Modbus Addressing

This page provides complete address mapping tables and calculation formulas for integrating Autonomy Edge with Modbus clients and servers. Understanding these mappings is essential for correctly configuring SCADA systems, HMIs, and other Modbus devices to communicate with your PLC program.

## IEC 61131-3 Address Format

All located variables in Autonomy Edge follow the IEC 61131-3 addressing format:

```
%[I|Q|M][X|B|W|D|L]<address>
```

### Location Prefixes

| Prefix | Meaning | Modbus Equivalent |
|--------|---------|-------------------|
| `%I` | Input | Data read from external sources |
| `%Q` | Output | Data written to external destinations |
| `%M` | Memory | Internal storage (not accessible via Modbus in v4) |

### Size Specifiers

| Specifier | Name | Size | Example |
|-----------|------|------|---------|
| `X` | Bit | 1 bit | `%IX0.3` (input byte 0, bit 3) |
| `B` | Byte | 8 bits | `%IB5` (input byte 5) |
| `W` | Word | 16 bits | `%IW10` (input word 10) |
| `D` | Double Word | 32 bits | `%QD4` (output double word 4) |
| `L` | Long Word | 64 bits | `%QL0` (output long word 0) |

For bit addresses, the notation uses two numbers separated by a dot: `%IX<byte>.<bit>`, where byte is the byte offset and bit is the bit position within that byte (0--7).

## Modbus Server Address Mapping

When Autonomy Edge acts as a Modbus server (slave), external clients access PLC data using the following address maps.

### Discrete Inputs (FC 2 — Read Discrete Inputs)

Discrete inputs are read-only single-bit values that map to `%IX` addresses.

| Modbus Address | IEC Address | Description |
|----------------|-------------|-------------|
| 0 | `%IX0.0` | Input byte 0, bit 0 |
| 1 | `%IX0.1` | Input byte 0, bit 1 |
| 2 | `%IX0.2` | Input byte 0, bit 2 |
| ... | ... | ... |
| 7 | `%IX0.7` | Input byte 0, bit 7 |
| 8 | `%IX1.0` | Input byte 1, bit 0 |
| 9 | `%IX1.1` | Input byte 1, bit 1 |
| ... | ... | ... |
| 63 | `%IX7.7` | Input byte 7, bit 7 |
| ... | ... | ... |
| 7999 | `%IX999.7` | Input byte 999, bit 7 |

**Total**: Up to 8000 discrete inputs (1000 bytes x 8 bits).

### Coils (FC 1, FC 5, FC 15 — Read/Write Coils)

Coils are read/write single-bit values that map to `%QX` addresses.

| Modbus Address | IEC Address | Description |
|----------------|-------------|-------------|
| 0 | `%QX0.0` | Output byte 0, bit 0 |
| 1 | `%QX0.1` | Output byte 0, bit 1 |
| ... | ... | ... |
| 7 | `%QX0.7` | Output byte 0, bit 7 |
| 8 | `%QX1.0` | Output byte 1, bit 0 |
| ... | ... | ... |
| 63 | `%QX7.7` | Output byte 7, bit 7 |
| ... | ... | ... |
| 7999 | `%QX999.7` | Output byte 999, bit 7 |

**Total**: Up to 8000 coils (1000 bytes x 8 bits).

### Input Registers (FC 4 — Read Input Registers)

Input registers are read-only 16-bit values that map to `%IW` addresses.

| Modbus Address | IEC Address | Description |
|----------------|-------------|-------------|
| 0 | `%IW0` | Input word 0 |
| 1 | `%IW1` | Input word 1 |
| 2 | `%IW2` | Input word 2 |
| ... | ... | ... |
| 999 | `%IW999` | Input word 999 |

**Total**: Up to 1000 input registers.

### Holding Registers (FC 3, FC 6, FC 16 — Read/Write Holding Registers)

Holding registers are read/write 16-bit values that map to `%QW` addresses.

| Modbus Address | IEC Address | Description |
|----------------|-------------|-------------|
| 0 | `%QW0` | Output word 0 |
| 1 | `%QW1` | Output word 1 |
| 2 | `%QW2` | Output word 2 |
| ... | ... | ... |
| 999 | `%QW999` | Output word 999 |

**Total**: Up to 1000 holding registers.

## Address Calculation Formulas

### Bit Addresses (Coils and Discrete Inputs)

To convert between IEC bit addresses and Modbus addresses:

```
Modbus Address = (Byte * 8) + Bit
```

To convert from Modbus address back to IEC format:

```
Byte = Modbus Address / 8    (integer division)
Bit  = Modbus Address % 8    (remainder)
```

**Examples**:

| IEC Address | Calculation | Modbus Address |
|-------------|-------------|----------------|
| `%IX0.0` | (0 * 8) + 0 | 0 |
| `%IX0.7` | (0 * 8) + 7 | 7 |
| `%IX1.0` | (1 * 8) + 0 | 8 |
| `%IX5.3` | (5 * 8) + 3 | 43 |
| `%QX10.5` | (10 * 8) + 5 | 85 |
| `%QX999.7` | (999 * 8) + 7 | 7999 |

### Word Addresses (Registers)

Register addresses have a one-to-one mapping:

```
Modbus Address = Word Number
```

**Examples**:

| IEC Address | Modbus Address |
|-------------|----------------|
| `%IW0` | 0 |
| `%IW25` | 25 |
| `%QW100` | 100 |
| `%QW999` | 999 |

## Multi-Register Data Types

Larger data types occupy consecutive Modbus registers. Autonomy Edge uses **big-endian** byte order (high word first), which is the Modbus standard.

### 32-bit Values (DINT, UDINT, REAL)

Each 32-bit value occupies 2 consecutive registers:

| IEC Address | Modbus Registers | Description |
|-------------|------------------|-------------|
| `%QD0` | Registers 0 and 1 | Register 0 = high word, Register 1 = low word |
| `%QD1` | Registers 2 and 3 | Register 2 = high word, Register 3 = low word |
| `%ID0` | Registers 0 and 1 | (Input side) |

Formula:

```
First Modbus Register = Double_Word_Number * 2
```

### 64-bit Values (LINT, ULINT, LREAL)

Each 64-bit value occupies 4 consecutive registers:

| IEC Address | Modbus Registers | Description |
|-------------|------------------|-------------|
| `%QL0` | Registers 0, 1, 2, 3 | Register 0 = most significant word |
| `%QL1` | Registers 4, 5, 6, 7 | Register 4 = most significant word |
| `%IL0` | Registers 0, 1, 2, 3 | (Input side) |

Formula:

```
First Modbus Register = Long_Word_Number * 4
```

## Memory Addresses and Runtime Versions

### Runtime v4 (Current) — No %M via Modbus

**Runtime v4 does not expose memory addresses (`%M`) through the Modbus server.** Only direct I/O addresses (`%I` and `%Q`) are accessible to Modbus clients.

The effective address ranges in v4 are limited to the basic I/O buffers:

| Data Type | Effective Range | Modbus Addresses |
|-----------|-----------------|------------------|
| Discrete Inputs | `%IX0.0` -- `%IX7.7` | 0 -- 63 |
| Coils | `%QX0.0` -- `%QX7.7` | 0 -- 63 |
| Input Registers | `%IW0` -- `%IW31` | 0 -- 31 |
| Holding Registers | `%QW0` -- `%QW31` | 0 -- 31 |

If you need to share internal variables with external systems and the v4 I/O buffer limits are too restrictive, consider using the [OPC-UA server](../opc-ua/README), which can expose any project variable regardless of its address type.

### Runtime v3 (Legacy) — Extended %M Ranges

Runtime v3 extended the Modbus holding register space to include memory addresses:

| Modbus Holding Register Range | IEC Addresses | Data Type |
|-------------------------------|---------------|-----------|
| 0 -- 999 | `%QW0` -- `%QW999` | 16-bit outputs |
| 1000 -- 2023 | `%MW0` -- `%MW1023` | 16-bit memory words |
| 2024 -- 4047 | `%MD0` -- `%MD1023` | 32-bit memory (2 registers each) |
| 4048 -- 8143 | `%ML0` -- `%ML1023` | 64-bit memory (4 registers each) |

Memory coils in v3:

| Modbus Coil Range | IEC Addresses |
|-------------------|---------------|
| 8000+ | `%MX0.0`, `%MX0.1`, ... |

### Memory Address Formulas (v3 Only)

```
Modbus Coil    = 8000 + (Byte * 8) + Bit       (for %MX addresses)
Modbus Register = 1000 + Word_Number             (for %MW addresses)
Modbus Register = 2024 + (DWord_Number * 2)      (for %MD addresses)
Modbus Register = 4048 + (LWord_Number * 4)      (for %ML addresses)
```

## Modbus Client Address Mapping

When Autonomy Edge acts as a Modbus client (master), the IO Group configuration determines how remote device addresses map to local IEC addresses:

- **Read function codes (FC 1--4)**: Data from the remote device is mapped to **input** addresses (`%I`), because it is incoming data from the PLC's perspective.
- **Write function codes (FC 5, 6, 15, 16)**: Data is sourced from **output** addresses (`%Q`), because the PLC is sending it out.

The IEC location is automatically assigned by the editor when you create an IO Group. For example, an FC 3 group reading 4 registers starting at remote offset 0 might be assigned `%IW0` through `%IW3`.

## Common Addressing Pitfalls

### 1-Based vs. 0-Based Addressing

Some Modbus clients and device documentation use **1-based** addressing (the first register is 1, not 0). Autonomy Edge uses **0-based** addressing internally.

Common translations:

| Client Display | Protocol Address | Autonomy Edge Address |
|---------------|------------------|----------------------|
| 40001 | 0 | `%QW0` |
| 40002 | 1 | `%QW1` |
| 30001 | 0 | `%IW0` |
| 00001 | 0 | `%QX0.0` |
| 10001 | 0 | `%IX0.0` |

If values appear offset by one, check whether your client software uses 1-based addressing and adjust accordingly.

### Overlapping Address Ranges

When configuring multiple IO Groups in the Modbus client, ensure that no two groups map to the same IEC address range. Overlapping ranges can cause unpredictable behavior as one group's data overwrites another's.

### Byte Order Mismatches

Autonomy Edge uses **big-endian** byte order for 32-bit and 64-bit values (high word first). If a remote device uses little-endian or word-swapped byte order, the data will appear garbled. Consult the device documentation and configure your data interpretation accordingly.

### Exceeding Buffer Limits

On Runtime v4, attempting to read or write Modbus addresses beyond the effective buffer size (63 for coils/discrete inputs, 31 for registers) will return zero values or be silently ignored. Always verify your address ranges against the active runtime version.

## Quick Reference

| Data Type | IEC Format | Modbus FC | Address Range (v4) | Address Range (v3) |
|-----------|------------|-----------|--------------------|--------------------|
| Digital Input | `%IX<b>.<n>` | FC 2 | 0--63 | 0--7999 |
| Digital Output | `%QX<b>.<n>` | FC 1, 5, 15 | 0--63 | 0--7999 |
| Analog Input | `%IW<n>` | FC 4 | 0--31 | 0--1023 |
| Analog Output | `%QW<n>` | FC 3, 6, 16 | 0--31 | 0--999 |
| Memory Bit | `%MX<b>.<n>` | Coil 8000+ | Not supported | 8000+ |
| Memory Word | `%MW<n>` | Reg 1000+ | Not supported | 1000--2023 |
| Memory DWord | `%MD<n>` | Reg 2024+ | Not supported | 2024--4047 |
| Memory LWord | `%ML<n>` | Reg 4048+ | Not supported | 4048--8143 |

## What's Next?

- **[Modbus Server Configuration](server)** — Configure the Modbus server settings and buffer sizes
- **[Modbus Client Configuration](client)** — Set up polling of external Modbus devices
- **[OPC-UA Server](../opc-ua/README)** — Alternative protocol with no address range limitations
- **[Communication Protocols Overview](../README)** — Return to the protocols overview
