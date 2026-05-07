# FAQ

Frequently asked questions about Autonomy Edge and IEC 61131-3 programming.

---

## General

### What is Autonomy Edge?

Autonomy Edge is a cloud-based platform for industrial automation built on OpenPLC v4. It provides a web-based IDE for writing PLC programs in IEC 61131-3 languages, cloud infrastructure for managing projects and devices, and an orchestrator system for deploying virtual PLCs (vPLCs) to edge hardware. Access the platform at [edge.autonomylogic.com](https://edge.autonomylogic.com).

### What is OpenPLC?

OpenPLC is an open-source Programmable Logic Controller platform. It includes an editor for writing PLC programs and a runtime that executes them. Autonomy Edge builds on OpenPLC v4, adding cloud project management, a web-based IDE, AI-assisted programming, orchestrator-managed vPLCs, and team collaboration features.

### What programming languages are supported?

Autonomy Edge supports three of the five IEC 61131-3 programming languages:

| Language | Type | Best For |
|----------|------|----------|
| **Structured Text (ST)** | Text-based | Complex algorithms, math, data processing |
| **Ladder Diagram (LD)** | Graphical | Discrete control, relay logic replacement |
| **Function Block Diagram (FBD)** | Graphical | Signal processing, data flow |

Instruction List (IL) is available but deprecated in the standard. SFC is not currently supported.

### Is Autonomy Edge free?

Visit [edge.autonomylogic.com](https://edge.autonomylogic.com) for current pricing and plan details. The platform offers different tiers based on the number of projects, devices, and features you need.

### What browsers are supported?

Autonomy Edge works in modern web browsers including Chrome, Firefox, Edge, and Safari. For the best experience, use the latest version of Chrome or Firefox.

---

## IEC 61131-3 Programming

### What is a POU?

A POU (Program Organization Unit) is the building block of IEC 61131-3 programs. There are three types:

- **Program**: The top-level executable unit, assigned to a task for cyclic execution
- **Function Block**: A reusable component with internal state (retains values between calls)
- **Function**: A stateless computation that returns a single value

See [POUs](../openplc-editor/iec-concepts/pous) for details.

### What is the difference between a Function and a Function Block?

| Feature | Function | Function Block |
|---------|----------|----------------|
| State | Stateless (no memory between calls) | Stateful (retains values between scans) |
| Return value | Single return value | Multiple outputs |
| Instances | Called directly by name | Requires a named instance |
| Use case | Math, conversions, pure computations | Timers, counters, controllers, state machines |

### What is a scan cycle?

The scan cycle is the fundamental execution loop of a PLC:

1. **Read inputs**: Copy physical input states into the input image table
2. **Execute program**: Run all assigned PLC logic
3. **Write outputs**: Copy the output image table to physical outputs

This cycle repeats at the interval defined by the task period (e.g., every 50 ms). The time to complete one cycle is the scan time.

### What are located variables?

Located variables are bound to specific addresses in the I/O image table, mapping them to physical inputs, outputs, or memory locations:

| Address | Meaning | Example |
|---------|---------|---------|
| `%IX0.0` | Digital input, byte 0, bit 0 | Start button |
| `%QX0.0` | Digital output, byte 0, bit 0 | Motor relay |
| `%IW0` | Analog input, word 0 | Temperature sensor |
| `%QW0` | Analog output, word 0 | Speed setpoint |
| `%MW0` | Memory word 0 | Internal storage |

### How do I choose between ST, LD, and FBD?

| If you need... | Use |
|----------------|-----|
| Complex math or algorithms | **ST**: full expression support, control flow |
| Relay logic or discrete control | **LD**: intuitive for electricians, mirrors wiring diagrams |
| Signal flow or data processing | **FBD**: visual data flow, good for connecting blocks |
| Mixed requirements | Use different languages for different POUs in the same project |

You can freely mix languages within a project. Each POU can be written in a different language, and they all interoperate seamlessly.

### What standard function blocks are available?

| Block | Category | Purpose |
|-------|----------|---------|
| `TON` | Timer | On-delay timer |
| `TOF` | Timer | Off-delay timer |
| `TP` | Timer | Pulse timer |
| `CTU` | Counter | Count up |
| `CTD` | Counter | Count down |
| `CTUD` | Counter | Count up/down |
| `SR` | Bistable | Set-dominant latch |
| `RS` | Bistable | Reset-dominant latch |
| `R_TRIG` | Edge | Rising edge detector |
| `F_TRIG` | Edge | Falling edge detector |

See [Standard Function Blocks Reference](function-blocks) for complete details.

---

## Devices and Deployment

### What is a vPLC?

A vPLC (virtual PLC) is a software-based PLC running the OpenPLC Runtime. Instead of dedicated hardware, vPLCs run on edge devices managed by an orchestrator. They execute the same IEC 61131-3 programs as physical PLCs and connect to physical I/O through Modbus, OPC-UA, or GPIO passthrough.

### What is an orchestrator?

An orchestrator is a software agent that runs on your edge hardware (Raspberry Pi, industrial gateway, or any Linux machine). It:

- Connects securely to the Autonomy Edge cloud
- Creates and manages vPLCs on the device
- Handles networking so vPLCs appear as native devices on your LAN
- Reports system health (CPU, memory, disk, uptime)

Install an orchestrator with:
```bash
curl https://getedge.me | bash
```

### What hardware can I run an orchestrator on?

The orchestrator runs on any supported Linux machine. Tested platforms include:

| Platform | Architecture |
|----------|-------------|
| Raspberry Pi 4/5 | ARM64 |
| Raspberry Pi 3 | ARM32 (armv7) |
| Intel/AMD PCs and servers | x86_64 |
| Industrial edge gateways (Siemens, WAGO, etc.) | Varies |

### How does a vPLC communicate with field devices?

vPLCs connect to field devices through:

| Method | Protocol | Use Case |
|--------|----------|----------|
| **Modbus TCP** | Modbus client/server | Most common; remote I/O modules, sensors, actuators |
| **OPC-UA** | OPC-UA client | Industrial systems with OPC-UA servers |
| **S7Comm** | S7 protocol | Siemens equipment |
| **GPIO passthrough** | Direct GPIO | When the orchestrator runs on hardware with GPIO (e.g., Raspberry Pi) |

### Can I run multiple vPLCs on one orchestrator?

Yes. Each vPLC runs as an independent process. The orchestrator manages all vPLCs on the host, and each one can have its own network configuration, program, and I/O connections. Resource limits depend on the host hardware (CPU, memory, disk).

### How do I deploy a program to a vPLC?

1. Write and compile your program in the Autonomy Edge IDE
2. Navigate to the **Devices** section in the dashboard
3. Select your target device (vPLC)
4. Upload the compiled program
5. Start the device

The program is packaged and deployed through the orchestrator automatically.

---

## Troubleshooting

### My program won't compile. What should I check?

Common compilation issues:

1. **Missing semicolons**: Every ST statement must end with `;`
2. **Unmatched control structures**: Every `IF` needs `END_IF`, every `FOR` needs `END_FOR`
3. **Undeclared variables**: All variables must be in the Variables Table
4. **Type mismatches**: Use explicit conversion functions (`INT_TO_REAL()`, etc.)
5. **Wrong assignment operator**: Use `:=`, not `=`

See [Common Compilation Errors](../advanced-topics/troubleshooting/compilation-errors) for a comprehensive guide.

### My orchestrator shows offline. What should I do?

1. Verify internet connectivity from the edge device
2. Check the orchestrator service is running on the device
3. Restart the orchestrator service if needed
4. Check the Autonomy Edge dashboard for status details

See [Network Issues](../advanced-topics/troubleshooting/network-issues) for detailed diagnostics.

### My timer doesn't seem to work correctly.

Common timer issues:

- **`IN` not staying TRUE**: TON requires `IN` to be TRUE continuously for the full duration `PT`
- **Timer never resets**: TON resets when `IN` goes FALSE; TOF resets when `IN` goes TRUE
- **Timer too fast/slow**: Check your task period; timers depend on the scan cycle for timing resolution
- **Using the type instead of an instance**: You must declare a variable of type TON/TOF/TP and call the instance

See [Timer Function Blocks](../openplc-editor/standard-function-blocks/timer-blocks) for detailed timing diagrams.

### How do I check my scan cycle time?

Monitor the console panel in the IDE for scan overrun warnings. If scan time exceeds the configured task period, the runtime logs a warning message. You can also observe timer `ET` values. If they count unevenly, scans may be overrunning.

See [Performance Optimization](../advanced-topics/best-practices/performance-optimization) for techniques to reduce scan time.

### Why are my Modbus values wrong?

Common Modbus data issues:

- **Byte order mismatch**: Device uses different endianness than expected
- **Register offset by 1**: Some devices are 0-based, others 1-based
- **Wrong function code**: Coils vs. holding registers vs. input registers
- **32-bit values spanning two registers**: Ensure your mapping accounts for multi-register values

See [Network Issues](../advanced-topics/troubleshooting/network-issues) for Modbus troubleshooting.

---

## Platform and Features

### Does the IDE support AI assistance?

Yes. The Autonomy Edge IDE includes an AI assistant that can help with:

- **Code completion**: Context-aware suggestions as you type
- **Chat**: Ask questions about IEC 61131-3, get help with code, debug issues

AI features are credit-based. Check your remaining credits via the AI panel in the IDE.

### Can I use the platform offline?

The Autonomy Edge web IDE requires an internet connection to access the platform at edge.autonomylogic.com. Your projects are stored in the cloud. For offline development, you can use the OpenPLC Desktop Editor, which supports the same IEC 61131-3 languages and can export programs compatible with the OpenPLC Runtime.

### Can I import/export projects?

Yes. The IDE supports:

- **Import**: Upload a project ZIP file through the IDE's import dialog
- **Export/Download**: Download a project as a ZIP file from the project details page
- **Clone**: Clone public projects shared by other users

### Does Autonomy Edge support team collaboration?

Projects are managed per user account. Team collaboration features are available depending on your plan. Contact Autonomy Logic for details on team plans and shared workspaces.

### What communication protocols does the runtime support?

| Protocol | Direction | Description |
|----------|-----------|-------------|
| Modbus TCP (client/master) | PLC reads/writes remote devices | Connect to Modbus-compatible I/O |
| Modbus TCP (server/slave) | External systems read/write PLC data | Expose data to SCADA or HMI systems |
| OPC-UA (client) | PLC reads from OPC-UA servers | Industrial OPC-UA integration |
| S7Comm | PLC communicates with Siemens PLCs | Siemens equipment interoperability |

Additional protocols can be added through the runtime's plugin system. See [Custom Libraries](../advanced-topics/integration-apis/custom-libraries) for information on extending functionality.

---

## Runtime

### Do I need to install the OpenPLC Runtime for Autonomy Edge?

No. When you create a Device on an Orchestrator, the platform installs and manages the runtime automatically. The standalone Runtime (available on GitHub) is designed for use with the Desktop Editor only.

### I see a Runtime web interface mentioned online. Where is it?

The runtime web interface is a feature of the standalone Desktop Editor workflow. In Autonomy Edge, all device management and monitoring is done through the cloud platform. There is no separate runtime web interface to access.

## What's Next?

- [Glossary](glossary): Key terms and definitions
- [Keyboard Shortcuts](keyboard-shortcuts): IDE shortcut reference
- [Getting Started](../getting-started/introduction): New to Autonomy Edge? Start here
