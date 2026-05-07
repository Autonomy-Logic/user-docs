# Understanding vPLC Devices

A virtual PLC (vPLC) is a software-based programmable logic controller that runs on your orchestrator's machine. This page explains what vPLCs are, what they can do, and when to use them.

---

## What Is a vPLC?

A vPLC is a software PLC that runs on your orchestrator's host machine. It uses the [OpenPLC Runtime](https://github.com/Autonomy-Logic/openplc-runtime) to execute IEC 61131-3 programs. Just like a physical PLC, but created and managed entirely through the Autonomy Edge web interface.

Each vPLC:

- Runs a dedicated instance of the OpenPLC Runtime.
- Has its own IP address on your local network.
- Can optionally use serial port passthrough for communicating with physical devices.
- Is fully managed from the platform. Create, start, stop, restart, rename, and delete without SSH access.

---

## How vPLCs Relate to Orchestrators

Orchestrators and vPLCs have a parent-child relationship:

- An **orchestrator** is the agent software installed on a Linux machine. It manages vPLCs and communicates with the Autonomy Edge cloud.
- A **vPLC** (also called a "device" in the platform) is created and managed by an orchestrator.

One orchestrator can manage multiple vPLCs. Each vPLC belongs to exactly one orchestrator. When you delete an orchestrator, all its vPLCs are removed too.

---

## What Can a vPLC Do?

### Execute PLC Programs

The OpenPLC Runtime supports Structured Text (ST), Ladder Diagram (LD), Function Block Diagram (FBD), and Instruction List (IL). Programs are compiled and executed in a real-time scan cycle.

### Communicate via Modbus

Every vPLC includes built-in Modbus TCP/IP server and client capabilities. This lets your vPLC communicate with remote I/O modules, sensors, actuators, and other PLCs on the network.

### Use Serial Devices

You can map USB-to-serial adapters and other serial devices from the host machine to your vPLC. This is useful for connecting RS-485 converters, serial sensors, and other physical devices.

### Runtime Versions

When creating a vPLC, you select which version of the OpenPLC Runtime to use. The platform lists available versions from the [openplc-runtime GitHub releases](https://github.com/Autonomy-Logic/openplc-runtime/releases) (v4.0.6 and later). The latest stable release is pre-selected by default.

---

## vPLCs vs Physical PLCs

vPLCs and physical PLCs serve the same purpose. Executing automation programs. But differ in how they interface with the physical world:

| Aspect | vPLC | Physical PLC |
|--------|------|-------------|
| **Deployment** | Created in seconds from the platform | Requires physical hardware installation |
| **I/O Access** | Network protocols (Modbus TCP/IP, etc.) and serial passthrough | Direct hardware I/O modules |
| **Network** | Virtual network interfaces bridged to host network | Physical Ethernet ports |
| **Scalability** | Multiple instances on one machine | One PLC per hardware unit |
| **Program Compatibility** | IEC 61131-3 via OpenPLC Runtime | IEC 61131-3 via OpenPLC Runtime |
| **Remote Management** | Full lifecycle control from the cloud | Requires physical or network access |

---

## When to Use a vPLC

vPLCs are ideal for:

- **Rapid prototyping**: Spin up a new PLC in seconds to test automation logic.
- **Network-based I/O**: Control Modbus TCP/IP devices, communicate with other PLCs, or integrate with SCADA systems.
- **Education and training**: Create multiple independent PLCs on a single machine for lab exercises.
- **Consolidation**: Run multiple automation workloads on a single edge device.

For applications that require direct hardware I/O (sensors and actuators wired to digital/analog inputs and outputs), you can connect a vPLC to remote I/O modules via Modbus TCP/IP, or use serial port passthrough for USB-connected devices.

---

## Compatibility with OpenPLC Editor Desktop

vPLCs run the same OpenPLC Runtime as standalone installations. You can connect to a vPLC using the [OpenPLC Editor](https://openplcproject.com/) desktop application from any computer on the same local network. Just point the editor to the vPLC's IP address and port.

This is useful for:

- Offline development when internet connectivity is unavailable.
- Local debugging and variable monitoring.
- Integration with existing OpenPLC workflows.

The desktop editor sees no difference between a vPLC and a standalone OpenPLC installation.

---

## What's Next?

Ready to create your first device?

➡️ [Creating a vPLC Device](creating-vplc): Step-by-step guide to naming, configuring, and launching a vPLC.
