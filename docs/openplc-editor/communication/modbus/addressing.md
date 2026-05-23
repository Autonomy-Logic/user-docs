# Modbus addressing

When a Modbus client talks to your vPLC, it reads and writes **Modbus addresses** (coil 7, holding register 12, etc.). Your PLC program reads and writes **IEC addresses** (`%QX0.0`, `%MW3`, etc.). This page explains how the two map.

## The rule, in one paragraph

Within each Modbus block (coils, discrete inputs, holding registers, input registers), the IEC segments you've configured for that block are laid out **sequentially**, starting at Modbus address 0 of that block. Sizes count in the addressable unit of that block: bits for coils and discrete inputs, 16-bit registers for holding and input registers. **Bit addresses are formatted as `[byte].[bit]`**, so the 0th coil bit is `%QX0.0`, the 7th is `%QX0.7`, the 8th rolls over to `%QX1.0`.

That's it. The rest of this page is concrete examples.

## Holding registers (FC 3 / 6 / 16)

Holding registers are 16-bit, read/write. The default segment layout exposes four IEC segments back-to-back:

| Modbus address | IEC | Size per IEC item |
|---|---|---|
| `0 … qwCount−1` | `%QW0 … %QW(qwCount−1)` | 1 register |
| next `mwCount` | `%MW0 … %MW(mwCount−1)` | 1 register |
| next `mdCount × 2` | `%MD0 … %MD(mdCount−1)` | **2 registers each** |
| next `mlCount × 4` | `%ML0 … %ML(mlCount−1)` | **4 registers each** |

So if you have `qwCount = 4`, `mwCount = 8`, `mdCount = 2`, `mlCount = 0`:

| Modbus addr | IEC |
|---|---|
| 0 | `%QW0` |
| 1 | `%QW1` |
| 2 | `%QW2` |
| 3 | `%QW3` |
| 4 | `%MW0` |
| 5 | `%MW1` |
| … | … |
| 11 | `%MW7` |
| 12, 13 | `%MD0` (lo word, hi word) |
| 14, 15 | `%MD1` |

The exact counts are set in the **Modbus Server** editor under **Buffer Mapping → Holding Registers**. Maximum 1024 registers per IEC segment.

## Coils (FC 1 / 5 / 15)

Coils are single bits, read/write. The default segment layout exposes two IEC segments:

| Modbus address | IEC | Notes |
|---|---|---|
| `0 … qxBits−1` | `%QX0.0 … %QX⌊(qxBits−1)/8⌋.((qxBits−1) mod 8)` | `byte.bit` |
| next `mxBits` | `%MX0.0 …` | same `byte.bit` rule |

Worked examples (default `qxBits = 800`):

| Modbus coil | IEC |
|---|---|
| 0 | `%QX0.0` |
| 7 | `%QX0.7` |
| 8 | `%QX1.0` |
| 16 | `%QX2.0` |
| 799 | `%QX99.7` |
| 800 | `%MX0.0` (first bit of the `%MX` segment) |

Maximum 8192 bits per IEC segment.

## Discrete inputs (FC 2)

Read-only bits. One segment by default:

| Modbus address | IEC |
|---|---|
| 0 | `%IX0.0` |
| 7 | `%IX0.7` |
| 8 | `%IX1.0` |
| `ixBits−1` | last bit of the segment |

Maximum 8192 bits.

## Input registers (FC 4)

Read-only 16-bit registers. One segment by default:

| Modbus address | IEC |
|---|---|
| 0 | `%IW0` |
| 1 | `%IW1` |
| `iwCount−1` | last register |

Maximum 1024 registers.

## The live address-mapping reference

The **Modbus Server** editor has an **Address Mapping Reference** accordion at the bottom that computes the full table at render time from your current buffer sizes. **This is the source of truth**, if you've changed the default segment sizes, look at that table, not at the defaults on this page.

## Why `%QX1.0` is coil 8, not coil 10

The bit numbering follows the byte/bit convention from IEC 61131-3 itself: `%QX<byte>.<bit>` where `bit` is 0…7. So `%QX0.7` is the 8th bit of the segment (bit index 7), and `%QX1.0` is the 9th bit (start of the next byte). Many off-the-shelf Modbus tools number coils 1-based (so coil 1 in the tool is coil 0 on the wire). Be careful which numbering your client uses.

## What about `%IB`, `%QB`, `%ID`, `%QD`, `%IL`, `%QL`?

Modbus doesn't index byte / double / long input or output segments separately. If you have a `%QD0` variable and you want it on Modbus, declare a `%MD` and copy the value across in your program, or use the **S7Comm** server (which does map all 14 PLC-memory variants directly). See **[S7Comm data blocks](../s7comm/data-blocks)**.

## What's next

- **[Modbus server](server)**: configure the slave end (what's running on your vPLC).
- **[Modbus remote device](../../device-config-overview)**: configure your vPLC as a master reading remote slaves.
- **Worked example: [Modbus slave: expose digital outputs](../../examples/modbus-slave-outputs)**.
