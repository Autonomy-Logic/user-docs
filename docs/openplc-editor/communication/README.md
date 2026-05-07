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

- **[Modbus Overview](modbus/README)** — Concepts, data types, function codes, and terminology
- **[Modbus Server](modbus/server)** — Configure Autonomy Edge as a Modbus slave
- **[Modbus Client](modbus/client)** — Configure Autonomy Edge to poll external Modbus devices
- **[Modbus Addressing](modbus/addressing)** — IEC 61131-3 to Modbus address mapping tables and formulas

### OPC-UA

OPC-UA (Open Platform Communications Unified Architecture) is a modern, secure, platform-independent protocol designed for industrial data exchange. Unlike Modbus, OPC-UA includes built-in support for encryption, certificate-based authentication, role-based access control, and rich data modeling.

Autonomy Edge is developing a full OPC-UA server implementation for Runtime v4 that will let you expose any project variable to external clients. Planned features include:

- **Security profiles**: Choose from multiple encryption and signing algorithms (Basic256Sha256, AES-128, AES-256).
- **User management**: Define users with username/password or certificate authentication.
- **Role-based access control**: Assign viewer, operator, or engineer roles with per-variable read/write permissions.
- **Certificate management**: Auto-generated self-signed certificates or custom CA-signed certificates.
- **Full type mapping**: IEC 61131-3 data types (BOOL, INT, REAL, LREAL, TIME, STRING, structures, arrays) are automatically mapped to OPC-UA types.
- **Bidirectional sync**: External clients can both read and write PLC variables in real time.

Documentation:

- **[OPC-UA Server](opc-ua/README)** — Complete configuration guide covering all five configuration tabs

## Adding Communication Interfaces

All communication protocols are configured through the project explorer in the Autonomy Edge web editor:

1. Open your project in the Autonomy Edge editor.
2. In the project explorer panel on the left, click the **+** button to add a new element.
3. Choose the type of communication you need:

| Menu Path | What It Creates |
|-----------|-----------------|
| **Server > Modbus/TCP** | A Modbus server (slave) that exposes PLC data to external clients |
| **Server > OPC-UA** | An OPC-UA server for secure, modern industrial communication |
| **Remote Device > Modbus/TCP** | A Modbus client (master) connection to poll an external device over Ethernet |
| **Remote Device > Modbus/RTU** | A Modbus client over serial (RS-232/RS-485) for legacy devices |

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
| OPC-UA Server | In Development | No | No |
| DNP3 | No | Beta | No |
| EtherNet/IP | In Development | Beta | No |
| S7Comm | In Development | Yes | No |
| EtherCAT | In Development | No | No |

> **Note:** Documentation for S7Comm, DNP3, EtherNet/IP, and EtherCAT will be added as their implementations are completed.

### Runtime v4

Runtime v4 is the current, actively developed runtime. It supports Modbus (server and client). OPC-UA is currently in development and its documentation is a preview of the upcoming feature. Additional protocols (EtherNet/IP, S7Comm, EtherCAT) are also under active development and will be available in future releases.

### Runtime v3

Runtime v3 is the legacy runtime. It supports Modbus with extended address ranges (including `%M` memory locations) and has beta-level drivers for DNP3, EtherNet/IP, and S7Comm. These beta drivers provide basic functionality but lack the robustness and configurability of the v4 implementations.

### Arduino

Due to hardware and memory constraints, Arduino targets only support Modbus server mode. This allows an Arduino-based PLC to expose its I/O data to a Modbus client (e.g., a SCADA system) but cannot initiate outbound connections to remote devices.

## Key Concepts

### Server vs. Client

Understanding the difference between server and client roles is fundamental to configuring communication correctly:

- **Server (Slave)**: Your PLC listens for incoming connections and responds to read/write requests. Use this when an external system (SCADA, HMI, historian, cloud gateway) needs to access PLC data. The server is passive — it never initiates communication.
- **Client (Master)**: Your PLC initiates connections to remote devices and polls data on a configurable schedule. Use this when your PLC needs to read sensors, control drives, or communicate with other PLCs. The client is active — it controls when and how often data is exchanged.

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

These files are generated automatically by the editor — you do not need to edit them by hand. The runtime reads them on startup to initialize the communication plugins.

### Choosing the Right Protocol

If you are unsure which protocol to use, consider the following guidelines:

| Scenario | Recommended Protocol |
|----------|---------------------|
| Connecting to legacy industrial devices (sensors, VFDs, meters) | Modbus TCP or RTU |
| Exposing data to a traditional SCADA system | Modbus Server |
| Secure communication with encryption and authentication | OPC-UA Server |
| Fine-grained access control (different permissions for operators vs. engineers) | OPC-UA Server |
| Exposing structured data types or arrays | OPC-UA Server |
| Communicating with Arduino-based PLCs | Modbus Server |
| Maximum simplicity with minimal configuration | Modbus Server |

In many industrial deployments, both Modbus and OPC-UA run simultaneously — Modbus for device-level communication with field instruments and OPC-UA for secure, higher-level data exchange with enterprise systems.

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

- **[Modbus Overview](modbus/README)** — Start here if you are working with Modbus devices
- **[OPC-UA Server](opc-ua/README)** — Start here for secure, modern industrial communication
- **[Modbus Addressing](modbus/addressing)** — Deep dive into IEC-to-Modbus address mapping rules
