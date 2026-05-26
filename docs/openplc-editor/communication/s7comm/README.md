# S7Comm Server

S7Comm is the proprietary communication protocol used by Siemens SIMATIC S7-300, S7-400, S7-1200, and S7-1500 PLCs. It runs over TCP/IP on port **102** (ISO-on-TCP / RFC 1006) and is widely supported by HMIs, SCADA systems, and engineering tools. WinCC, TIA Portal monitor windows, Snap7-based clients, libnodave, NodeS7, python-snap7, and many third-party drivers.

The Autonomy Edge S7Comm plugin makes the OpenPLC runtime act as a **Siemens-style server**. External clients connect to the runtime, browse Data Blocks (DB1, DB2, …), and read or write PLC variables exactly as if they were talking to a real S7-300. There is no Target IP, Rack, or Slot to configure on this side. Those are S7 client-side details. Your job is only to expose the buffers you want clients to see.

## When to Choose S7Comm

| Scenario | Recommended |
|----------|-------------|
| Existing HMI or SCADA already speaks S7 (WinCC, Movicon, Ignition Siemens driver) | S7Comm Server |
| Drop-in replacement for a Siemens S7-300/S7-1200 controller | S7Comm Server |
| Tooling based on Snap7, libnodave, NodeS7, python-snap7 | S7Comm Server |
| Generic SCADA without a Siemens driver | [Modbus Server](../modbus/server) |
| Encryption, certificates, role-based access | [OPC-UA Server](../opc-ua/README) |
| Exposing structures or arbitrary project variables | [OPC-UA Server](../opc-ua/README) |

S7Comm has no built-in authentication or encryption. Use it only on trusted networks, behind a firewall, or over a VPN. If you need security, pick OPC-UA.

## Platform Support

| Runtime | S7Comm Server Support |
|---------|----------------------|
| Runtime v4 | Yes |
| Runtime v3 | Beta |
| Arduino | No |

The full configuration surface described in this guide targets **Runtime v4**. The v3 implementation is a beta driver with limited configurability and is not the focus of this documentation.

## Adding an S7Comm Server

To add an S7Comm server to your project in the Autonomy Edge web editor:

1. In the project explorer, click the **+** button.
2. Select **Server** from the dropdown menu.
3. Choose **Siemens S7comm** as the protocol and enter a descriptive name (at least 3 characters).
4. Click **Create**.
5. The new entry appears under the **Servers** folder in the project tree.
6. Click the entry to open its configuration panel.

The configuration panel is organised into four collapsible sections, listed below. The first two (**Server Configuration** and **Data Blocks**) are open by default; **PLC Identity** and **Logging** are collapsed.

| Section | Purpose |
|---------|---------|
| **Server Configuration** | Network bind address, port, client/PDU limits, enable toggle |
| **Data Blocks** | The list of Siemens-style DBs (DB1, DB2, …) that clients see |
| **PLC Identity** | The values returned in S7 SZL queries (CPU model, serial, etc.) |
| **Logging** | Per-category logging toggles |

## Documentation Pages

- **[Server Configuration](server-configuration)**: Network bind address, port, max clients, PDU size
- **[Data Blocks](data-blocks)**: Define DBs, choose buffer mappings, the 14-entry mapping catalog
- **[PLC Identity](plc-identity)**: Customise the SZL identification reported to clients
- **[Logging](logging)**: Connection, data-access, and error logging toggles
- **[Example](example)**: Worked walkthrough exposing the blink project's `led` variable as DB1
- **[Troubleshooting](troubleshooting)**: UI-visible failures, port conflicts, PDU mismatches

## Key Concepts

### Server, Not Client

The plugin is a **server**. It listens for incoming connections and responds. It never reaches out to a Siemens PLC. If you need the OpenPLC runtime to read from or write to an existing Siemens controller (S7-1200, S7-1500), that is a client/master role and is not covered by this plugin.

### Data Blocks Map to PLC Buffers

Every Data Block you create in the editor is a slice of the PLC's I/O or memory buffer that becomes visible as DB&lt;n&gt; to S7 clients. The DB number, size in bytes, and the buffer area it points to (Boolean Output `%QX`, Word Input `%IW`, Long Word Memory `%ML`, …) are all configured per-DB. See [Data Blocks](data-blocks) for the full mapping catalog.

### PDU Size Is Negotiated

The PDU (Protocol Data Unit) size sets the maximum payload of a single S7 telegram. The server advertises the value you configure (default 480 bytes); the client may request a smaller value at connection setup. Both sides agree on the **lower** of the two. There is no error if a client asks for less.

### Configuration Export

When you transfer the project to the runtime, the editor exports the S7Comm configuration as a JSON file inside the program package. The runtime reads it on startup to start the listener. You do not need to edit this file by hand.

## What's Next?

- **[Server Configuration](server-configuration)**: Start here to set up the listener
- **[Data Blocks](data-blocks)**: Define what clients can see
- **[Example](example)**: Walk through a full configuration with the blink project
- **[Communication Protocols Overview](../README)**: Compare S7Comm to Modbus and OPC-UA
