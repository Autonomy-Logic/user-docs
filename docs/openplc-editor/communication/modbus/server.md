# Modbus server

The Modbus server (slave) exposes parts of the PLC's memory image as **Modbus addresses** that any Modbus TCP client (SCADA, HMI, historian) can read or write. The server runs as a plugin inside the OpenPLC runtime on your vPLC. There's nothing to install; you only configure it.

## Add a Modbus server to your project

1. In the project tree, click the **`+`** button at the top.
2. Pick **server** in the popover, then **Modbus / TCP**.
3. Give it a name and click **Create**.
4. A new entry appears under **Servers** in the tree. Click it to open the configuration editor.

## Server configuration

The top section of the editor:

| Field | Default | Notes |
|---|---|---|
| **Enabled** | on | Disable to stop the server from accepting connections on the next runtime start. |
| **Network Interface** | `0.0.0.0` | The IP to bind to. Use `0.0.0.0` for all interfaces, or pin to a specific NIC. |
| **Port** | `502` | The standard Modbus TCP port. Ports below 1024 may need extra privileges on Linux — if the runtime can't bind, try `1502`. |

## Buffer mapping

The bulk of the editor is the **Buffer Mapping** accordion. There are four sections, one per Modbus block type. Each lets you set how many IEC items of each segment to expose, and the editor recomputes the address-mapping table live.

### Holding Registers (FC 3 / 6 / 16)
Lay out four IEC segments in order. Each entry below is "how many items of this kind to expose":

| IEC segment | Size per item | Max |
|---|---|---|
| `%QW` | 1 register | 1024 |
| `%MW` | 1 register | 1024 |
| `%MD` | **2 registers** | 1024 |
| `%ML` | **4 registers** | 1024 |

### Coils (FC 1 / 5 / 15)
Two IEC segments:

| IEC segment | Size per item | Max |
|---|---|---|
| `%QX` | 1 bit | 8192 |
| `%MX` | 1 bit | 8192 |

### Discrete Inputs (FC 2)
One segment:

| IEC segment | Size | Max |
|---|---|---|
| `%IX` | 1 bit | 8192 |

### Input Registers (FC 4)
One segment:

| IEC segment | Size | Max |
|---|---|---|
| `%IW` | 1 register | 1024 |

## Address Mapping Reference

The last accordion section is the **Address Mapping Reference** — a computed table showing exactly which Modbus address corresponds to which IEC address given your current segment sizes. This is the **single source of truth** for what an external Modbus client will see. If you've changed the defaults, consult this table, not the page on this site.

For the mapping rule itself (and why `%QX0.0` is coil 0 but `%QX1.0` is coil 8), see **[Modbus addressing](addressing)**.

## How clients connect

Once the server is enabled and the runtime is started, any standard Modbus TCP client can connect to the vPLC's IP on the configured port. There's no authentication — Modbus TCP has none. If you need access control, place the vPLC behind a firewall or VLAN.

For testing, [`mbpoll`](https://github.com/epsilonrt/mbpoll) is a quick CLI client:

```bash
# Read coil 0 from vPLC at 192.168.1.50, port 502
mbpoll -t 0 -r 0 192.168.1.50

# Write 1 to coil 8 (the first bit of %QX1.x)
mbpoll -t 0 -r 8 192.168.1.50 1
```

## Troubleshooting

**The server doesn't appear in the editor.** Make sure your target supports Modbus TCP server. The capability is exposed on Runtime v4 and the Simulator only.

**Connection refused.** Verify the runtime is running (the **Play** button is green in the activity bar) and that nothing else on the host is bound to the same port.

**Permission denied on bind.** Ports below 1024 need elevated privileges on Linux. Use 1502 or higher unless the runtime is launched as root.

**Writes don't land in the PLC.** Check that the variable's IEC address actually falls inside an exposed segment range. Open the **Address Mapping Reference** in the server editor to verify the variable's address has a Modbus address assigned.

## What's next

- **[Modbus addressing](addressing)** — the canonical mapping rule + tables.
- **[Modbus remote device](client)** — configure your vPLC as a master that reads remote slaves.
- **Worked example: [Modbus slave: expose digital outputs](../../examples/modbus-slave-outputs)**.
