# Modbus remote device (master)

When you want your vPLC to **read** from or **write** to a remote Modbus slave (a field-level sensor, a meter, an external PLC), configure a **Modbus remote device**. The vPLC becomes the master; the remote is the slave.

This lives under **Device** in the project tree, not under **Servers** (which is the *slave*-side configuration covered on the **[Modbus server](server)** page).

## Add a remote device

1. Click the **`+`** button at the top of the project tree.
2. Pick **remote-device**, then **Modbus**.
3. Give it a name; click **Create**.
4. The new entry appears under **Device** in the tree. Click it to open its editor.

The capability is gated to Runtime v4 and the Simulator targets. Other targets won't offer Modbus in the remote-device picker.

## Transport configuration

At the top of the editor, pick **Modbus TCP** or **Modbus RTU (serial)**.

### TCP transport

| Field | Default | Notes |
|---|---|---|
| **Host** | (empty) | IP or hostname of the remote slave. |
| **Port** | `502` | TCP port. |
| **Slave ID** | `1` | Unit identifier (range `0…255` for TCP). |
| **Timeout (ms)** | `1000` | How long to wait for a response before flagging a read/write as failed. |

### RTU transport (serial)

| Field | Default | Notes |
|---|---|---|
| **Serial port** | first available | Combobox populated from `runtime.getSerialPorts`. |
| **Baud rate** | `9600` | One of `9600 / 19200 / 38400 / 57600 / 115200`. |
| **Parity** | `N` | `N`one / `E`ven / `O`dd. |
| **Stop bits** | `1` | `1` or `2`. |
| **Data bits** | `8` | `7` or `8`. |
| **Slave ID** | `1` | Unit identifier (range `1…247` for RTU). |
| **Timeout (ms)** | `1000` | Same meaning as TCP. |

## I/O groups

Below the transport, the editor lists **I/O Groups**. Each group corresponds to one polled Modbus operation against the remote (one function code, one address range, one polling cycle).

Per group:

| Field | Notes |
|---|---|
| **Function code** | `FC 1` Read Coils, `FC 2` Read Discrete Inputs, `FC 3` Read Holding Registers, `FC 4` Read Input Registers, `FC 5` Write Single Coil, `FC 6` Write Single Register, `FC 15` Write Multiple Coils, `FC 16` Write Multiple Registers. |
| **Cycle time** | How often (ms) to issue this operation. The master pipelines all groups round-robin under their cycles. |
| **Offset** | Modbus address (on the remote) where the read/write starts. |
| **Length** | How many addresses to read/write per cycle. |
| **Error handling** | What to do if a cycle fails: `keep-last-value` (leave the local mirror untouched) or `set-to-zero` (clear the local mirror on failure). |

### I/O points (per group)

Within a group, you declare the **I/O points** — individual values pulled from (or written into) the polled address range. Each point has:

- **Name** — your local identifier (used in the variables editor as the `Type`).
- **Type** — `BOOL` for FC 1/2/5/15, `INT` for FC 3/4/6/16. Larger types take consecutive addresses.
- **IEC location** — the local IEC address into which the remote value is mirrored on read (or from which the local value is written on write). E.g. `%IX0.0` for a remote discrete-input mirrored into the input image.
- **Alias** (optional) — a stable name for the point. If you reorganise the group later, the alias keeps the variables editor happy without manual rewires.

## How it shows up in code

Once a remote device is configured, its I/O points appear as auto-declared variables in the project. You reference them by their **alias** (preferred) or by their **IEC location** directly. The runtime reads / writes the remote on the cycle time you configured, and the local IEC mirror is kept in sync.

For pulled points, your program reads the local address as if it were a normal input. For pushed points, you write to the local address and the runtime ships the value to the remote at the next cycle.

## Diagnostics

The console reports each I/O Group's first failure and recovery. Persistent failures appear at every cycle in the runtime logs (the **PLC Logs** tab, visible when connected).

## Troubleshooting

**No remote-device option in the popover.** The active target doesn't support Modbus master (capability `modbusTcpRemote` or `modbusRtuRemote`). Use Runtime v4 or the Simulator.

**TCP timeouts.** The host or port is unreachable. From a shell on the orchestrator host: `telnet <ip> 502` should connect.

**RTU never responds.** Match the serial parameters exactly: a single mismatched parity or stop bit silently drops every frame. Cross-check with the slave's data sheet.

**Reading wrong values.** Modbus tools differ in coil/register numbering (some 1-based, some 0-based). The IEC address in the I/O point is **the wire address**, not the 1-based "PLC address" some HMIs display.

## What's next

- **[Modbus addressing](addressing)** — coil 8 vs. `%QX1.0`, holding-register layout.
- **[Modbus server](server)** — the slave side.
