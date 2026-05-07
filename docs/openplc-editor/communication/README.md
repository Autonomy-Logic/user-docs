# Communication Protocols

Autonomy Edge supports a range of industrial communication protocols that allow your PLC programs to exchange data with SCADA systems, HMIs, remote I/O modules, sensors, and other automation devices. You configure all communication settings directly in the Autonomy Edge web editor at [edge.autonomylogic.com](https://edge.autonomylogic.com), with no desktop software required.

This section covers every supported protocol, how to add and configure communication interfaces, and the address mapping rules that tie your IEC 61131-3 program variables to protocol-level data points.

## Available Protocols

### Modbus

Modbus is the most widely deployed fieldbus protocol in industrial automation. Originally published by Modicon in 1979, it remains the go-to choice for connecting PLCs, sensors, drives, and SCADA systems thanks to its simplicity and near-universal vendor support. Autonomy Edge supports Modbus TCP for both server (slave) and client (master) roles, as well as Modbus RTU for serial communications over RS-232 and RS-485.

Key capabilities:

- **Modbus Server (Slave)**: Expose your PLC's I/O buffers so external SCADA systems and HMIs can read sensor values and write setpoints.
- **Modbus Client (Master)**: Poll data from remote devices (temperature sensors, flow meters, VFDs, other PLCs) on a configurable schedule.
- **Modbus RTU**: Communicate over serial buses with multi-drop support for multiple slave devices on a single RS-485 line.

Documentation pages:

- **[Modbus Overview](modbus/README)**: Concepts, data types, function codes, and terminology
- **[Modbus Server](modbus/server)**: Configure Autonomy Edge as a Modbus slave
- **[Modbus Client](modbus/client)**: Configure Autonomy Edge to poll external Modbus devices
- **[Modbus Addressing](modbus/addressing)**: IEC 61131-3 to Modbus address mapping tables and formulas

### EtherCAT

EtherCAT (Ethernet for Control Automation Technology) is a real-time industrial fieldbus that uses standard Ethernet cabling but replaces TCP/IP with a deterministic on-the-fly processing protocol. A single Ethernet frame travels around a daisy-chained line of slaves, and each slave reads and writes its slice of the process data as the frame passes through. Sub-millisecond cycle times across thousands of I/O points are routine. Autonomy Edge ships an EtherCAT master plugin for Runtime v4 that drives a segment of EtherCAT slaves directly from your IEC 61131-3 program.

Key capabilities:

- **Master role**: Autonomy Edge drives the segment. The runtime cycles process data on a dedicated NIC, polls slaves, and writes output values from your PLC variables.
- **ESI repository**: Upload Beckhoff, drives, and any other vendor's `.xml` ESI (EtherCAT Slave Information) files; the editor uses them to identify slaves and pre-map their I/O.
- **Live scan**: Discover slaves on a connected segment with one click, and add the matched ones to the project tree.
- **Per-slave configuration**: Verify vendor / product on startup, set state-machine timeouts, configure SM and PDI watchdogs, and enable distributed clocks for synchronised motion.
- **SDO startup parameters**: Write CoE configuration to slaves once at boot. Operating modes, ranges, filter times, anything declared in the ESI dictionary.
- **PDO channel mapping**: TxPDO inputs and RxPDO outputs are mapped to IEC 61131-3 located variables (`%IX`, `%QX`, `%IW`, `%QW`, …) automatically with collision detection across the project.
- **Runtime diagnostics**: Master state (Init / Pre-Op / Safe-Op / Op), per-slave state, AL status codes, and error counters reported live while the bus runs.

Documentation pages:

- **[EtherCAT Overview](ethercat/README)**: When to use EtherCAT, platform support, two-editor architecture
- **[Prerequisites](ethercat/prerequisites)**: NIC, OS permissions, cabling, topology, cycle-time floors
- **[Adding an EtherCAT segment](ethercat/adding-ethercat)**: Step-by-step bus creation
- **[Bus tab](ethercat/bus-scan)**: Network interface, scan, matching scanned devices to the repository
- **[Repository tab](ethercat/bus-repository)**: Upload and manage ESI files
- **[Advanced tab](ethercat/bus-advanced)**: Master cycle time, watchdog, task priority
- **[Channel Mappings](ethercat/slave-channel-mappings)**: PDO entries and IEC variable mapping
- **[Device Info](ethercat/slave-info)**: Read-only slave identification
- **[Configuration](ethercat/slave-configuration)**: Startup checks, timeouts, watchdog, distributed clocks
- **[Startup Parameters](ethercat/slave-startup-params)**: SDO writes performed before SAFE-OP → OP
- **[Diagnostics](ethercat/diagnostics)**: Runtime status panel reference
- **[Worked example](ethercat/example)**: End-to-end EK1100 + EL1809 + EL2809 segment
- **[Troubleshooting](ethercat/troubleshooting)**: Common UI and runtime failures with fixes

### OPC-UA

OPC-UA (Open Platform Communications Unified Architecture) is a modern, secure, platform-independent protocol designed for industrial data exchange. Unlike Modbus, OPC-UA includes built-in support for encryption, certificate-based authentication, role-based access control, and rich data modeling.

Autonomy Edge ships a full OPC-UA server for Runtime v4 that lets you expose project variables to external clients. Capabilities include:

- **Security profiles**: Choose from `None`, `Basic128Rsa15`, `Basic256`, and `Basic256Sha256` policies, paired with `Sign Only` or `Sign and Encrypt` message security modes.
- **User management**: Define users with password or certificate authentication.
- **Role-based access control**: Assign Viewer, Operator, or Engineer roles with per-variable read/write permissions.
- **Certificate management**: Auto-generate a self-signed certificate, or upload a custom certificate and private key in PEM format.
- **Full type mapping**: IEC 61131-3 data types (BOOL, INT, REAL, LREAL, TIME, STRING, structures, arrays, function block instances) are exposed automatically as OPC-UA nodes.
- **Bidirectional sync**: External clients can both read and write PLC variables, subject to the per-role permission matrix.

Documentation:

- **[OPC-UA Server Overview](opc-ua/README)**: when to use OPC-UA, how to add a server, default configuration, platform support.
- **[General Settings](opc-ua/general-settings)**: server identity, network binding, cycle time, namespace.
- **[Security Profiles](opc-ua/security-profiles)**: security policies, message security modes, authentication methods.
- **[Users](opc-ua/users)**: password and certificate-based accounts with role assignment.
- **[Certificates](opc-ua/certificates)**: server certificate strategy and trusted client certificates.
- **[Address Space](opc-ua/address-space)**: variable selection, namespace, IEC to OPC-UA type mapping, per-role permissions.
- **[Worked Example](opc-ua/example)**: end-to-end walkthrough exposing a variable with username / password authentication.
- **[Troubleshooting](opc-ua/troubleshooting)**: editor validation messages and client-side connection errors.

### S7Comm

S7Comm is the proprietary protocol used by Siemens SIMATIC S7-300, S7-400, S7-1200, and S7-1500 controllers. The Autonomy Edge S7Comm plugin makes the OpenPLC runtime act as a **Siemens-style server**: HMIs, SCADAs, and Siemens engineering tools (WinCC, TIA Portal monitor windows, Snap7-based clients, libnodave, NodeS7, python-snap7) connect over TCP/102 and read or write OpenPLC variables wrapped in S7-style **Data Blocks** (DB1, DB2, …). The plugin lives under **Server > S7Comm** in the project explorer alongside Modbus Server and OPC-UA Server.

Key capabilities:

- **Server role**: The runtime is the target. There is no Target IP, Rack, or Slot to configure on this side. Those are S7 client-side conventions.
- **Up to 64 Data Blocks**: Each DB is a window onto a PLC buffer. Choose from 14 buffer types covering boolean / byte / word / double-word / long-word inputs, outputs, and memory.
- **Customisable SZL identity**: Defaults to a Siemens S7-300 (`CPU 315-2 PN/DP`) for maximum HMI compatibility, but every identity field is editable.
- **Negotiated PDU**: Configurable 240 -- 960 byte PDU; the client and server agree on the smaller of the two at connection setup.
- **Per-category logging**: Independent toggles for connection events, data access (verbose), and errors.

Documentation pages:

- **[S7Comm Overview](s7comm/README)**: Concepts, when to choose S7Comm, platform support
- **[Server Configuration](s7comm/server-configuration)**: Bind address, port, max clients, PDU size
- **[Data Blocks](s7comm/data-blocks)**: DB modal, the 14-entry mapping catalog, sizing
- **[PLC Identity](s7comm/plc-identity)**: SZL fields and their defaults
- **[Logging](s7comm/logging)**: Connection, data access, and error toggles
- **[Example](s7comm/example)**: Walk-through using the blink project
- **[Troubleshooting](s7comm/troubleshooting)**: Port conflicts, PDU mismatches, validation errors

S7Comm has no built-in authentication or encryption. Use it on trusted networks, behind a firewall, or over a VPN. If you need security, use OPC-UA instead.

## Hardware Setup for Serial Protocols

### RS-485 for Modbus RTU

For Modbus RTU over RS-485, you need a serial port available on the machine where the Orchestrator is installed (this could be a Raspberry Pi, an industrial PC, an edge computer, or any Linux device). This can be either:

- A **native serial port** built into your machine (common on industrial PCs and edge computers).
- A **USB-to-RS-485 adapter** plugged into a USB port. Common adapters based on the FTDI FT232 or CH340 chipset work out of the box on Linux.

When creating a vPLC Device, the platform shows all available serial ports detected on the host. You select which port to assign to the vPLC and give it a **container path**: a virtual path that your PLC program will use (e.g., `/dev/ttyRS485` or any name you choose). This container path then appears in the Modbus RTU configuration dropdown inside the editor.

> **Important:** A serial port can only be assigned to **one vPLC at a time**. This is a hardware limitation. Unlike network interfaces, a serial line cannot be shared between multiple devices. If a port is already assigned to another vPLC, it will appear grayed out.

See [Creating vPLC Devices](../../platform-features/vplc-management/creating-vplc) for the full Device creation walkthrough, including serial port configuration.

## Adding Communication Interfaces

All communication protocols are configured through the project explorer in the Autonomy Edge web editor:

1. Open your project in the Autonomy Edge editor.
2. In the project explorer panel on the left, click the **+** button to add a new element.
3. Choose the type of communication you need:

| Menu Path | What It Creates |
|-----------|-----------------|
| **Server > Modbus/TCP** | A Modbus server (slave) that exposes PLC data to external clients |
| **Server > Siemens S7comm** | An S7Comm server that exposes PLC data to Siemens-style clients (HMIs, SCADAs, Snap7 tools) |
| **Server > OPC-UA** | An OPC-UA server for secure, modern industrial communication |
| **Remote Device > Modbus/TCP** | A Modbus client (master) connection to poll an external device over Ethernet |
| **Remote Device > Modbus/RTU** | A Modbus client over serial (RS-232/RS-485) for legacy devices |
| **Remote Device > EtherCAT** | An EtherCAT master segment with its own slave configuration, ESI repository, and channel mappings |

4. Enter a name for the new element and click **Create**.
5. The new entry appears in the project explorer tree under the appropriate folder (Servers or Devices).
6. Click the entry to open its configuration panel, where you set network parameters, data mappings, and protocol-specific options.

You can add multiple servers and remote devices to a single project. Each operates independently at runtime with its own connection and polling schedule.

## Protocol Support by Runtime

Not every protocol is available on every runtime target. The table below summarizes current support levels across the three runtime environments.

| Protocol | Runtime v4 | Runtime v3 | Arduino |
|----------|------------|------------|---------|
| Modbus Server (Slave) | Yes | Yes | Yes |
| Modbus Client (Master) | Yes | Yes | No |
| Modbus RTU Master | Yes | Yes | No |
| Siemens S7Comm | Yes | Yes | No |
| OPC-UA Server | Yes | No | No |
| EtherCAT | Yes | No | No |
| DNP3 | No | Beta | No |
| EtherNet/IP | In Development | Beta | No |

> **Note:** Documentation for DNP3 and EtherNet/IP will be added as their implementations are completed.

### Runtime v4

Runtime v4 is the current, actively developed runtime. It supports Modbus TCP (server and client), Modbus RTU (master), Siemens S7Comm, OPC-UA, and EtherCAT. EtherNet/IP is under active development and will be available in a future release.

### Runtime v3

Runtime v3 is the legacy runtime. It supports Modbus with extended address ranges (including `%M` memory locations) and has beta-level drivers for DNP3, EtherNet/IP, and S7Comm. These beta drivers provide basic functionality but lack the robustness and configurability of the v4 implementations.

### Arduino

Due to hardware and memory constraints, Arduino targets only support Modbus server mode. This allows an Arduino-based PLC to expose its I/O data to a Modbus client (e.g., a SCADA system) but cannot initiate outbound connections to remote devices.

## Key Concepts

### Server vs. Client

Understanding the difference between server and client roles is fundamental to configuring communication correctly:

- **Server (Slave)**: Your PLC listens for incoming connections and responds to read/write requests. Use this when an external system (SCADA, HMI, historian, cloud gateway) needs to access PLC data. The server is passive. It never initiates communication.
- **Client (Master)**: Your PLC initiates connections to remote devices and polls data on a configurable schedule. Use this when your PLC needs to read sensors, control drives, or communicate with other PLCs. The client is active. It controls when and how often data is exchanged.

A single project can use both roles simultaneously. For example, your PLC can act as a Modbus server for a SCADA system while also polling temperature sensors as a Modbus client and exposing process data through an OPC-UA server.

### IEC 61131-3 Address Binding

Every communication data point is bound to an IEC 61131-3 located variable in your PLC program. This means you can use variables like `%IW0`, `%QX0.0`, or `%QW100` in your Ladder Diagram, Structured Text, or Function Block Diagram, and the communication layer automatically synchronizes those values with the connected devices.

For Modbus, addresses are determined by the data type and function code:

- Input data (`%I`) comes from read operations (the PLC receives data from an external source)
- Output data (`%Q`) goes to write operations (the PLC sends data to an external destination)

For OPC-UA, any project variable can be exposed regardless of its IEC address type, including internal variables and structured types.

### Configuration Export

When you transfer a project to the runtime, the editor exports protocol configurations as JSON files inside the program package:

| Protocol | Configuration File | Contents |
|----------|--------------------|---------|
| Modbus Server | `modbus_slave.json` | Network settings, buffer sizes, enable flag |
| Modbus Client | `modbus_master.json` | Device connections, IO groups, polling schedules |
| OPC-UA Server | `opcua.json` | Server settings, security profiles, users, certificates, address space |

These files are generated automatically by the editor. You do not need to edit them by hand. The runtime reads them on startup to initialize the communication plugins.

### Choosing the Right Protocol

If you are unsure which protocol to use, consider the following guidelines:

| Scenario | Recommended Protocol |
|----------|---------------------|
| Connecting to legacy industrial devices (sensors, VFDs, meters) | Modbus TCP or RTU |
| Exposing data to a traditional SCADA system | Modbus Server |
| Communicating with Siemens PLCs (S7-1200, S7-1500) | Siemens S7Comm |
| High-speed, real-time fieldbus communication | EtherCAT |
| Secure communication with encryption and authentication | OPC-UA Server |
| Fine-grained access control (different permissions for operators vs. engineers) | OPC-UA Server |
| Exposing structured data types or arrays | OPC-UA Server |
| Communicating with Arduino-based PLCs | Modbus Server |
| Maximum simplicity with minimal configuration | Modbus Server |

In many industrial deployments, both Modbus and OPC-UA run simultaneously. Modbus for device-level communication with field instruments and OPC-UA for secure, higher-level data exchange with enterprise systems.

## Troubleshooting Communication Issues

If you experience communication problems, these general steps apply to all protocols:

1. **Verify runtime status**: Ensure the runtime is running and the PLC program is loaded. Communication plugins only start when the program is active.
2. **Check network connectivity**: Use standard network tools (`ping`, `telnet`) to verify the PLC and remote devices can reach each other on the expected ports.
3. **Review configuration**: Double-check IP addresses, port numbers, and protocol-specific settings in the configuration panel.
4. **Check firewall rules**: Industrial firewalls or host-based firewalls may block communication ports (502 for Modbus, 4840 for OPC-UA).
5. **Inspect runtime logs**: The runtime logs connection attempts, errors, and protocol-level diagnostics that can help identify the root cause.
6. **Test with diagnostic tools**: Use protocol-specific tools (e.g., QModMaster for Modbus, UaExpert for OPC-UA) to test connectivity independently of your PLC program.

For protocol-specific troubleshooting, see the individual documentation pages linked below.

## What's Next?

- **[Modbus Overview](modbus/README)**: Start here if you are working with Modbus devices
- **[OPC-UA Server](opc-ua/README)**: Start here for secure, modern industrial communication
- **[Modbus Addressing](modbus/addressing)**: Deep dive into IEC-to-Modbus address mapping rules
