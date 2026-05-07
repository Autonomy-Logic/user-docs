# Device Configuration Overview

The Device Configuration section defines how your PLC program connects to and controls hardware. In the Autonomy Edge web IDE at [edge.autonomylogic.com](https://edge.autonomylogic.com), you configure connections to target runtimes. The desktop editor adds support for Arduino-compatible microcontrollers and direct connections to OpenPLC Runtime installations.

## Accessing Device Configuration

To open the Device Configuration panel:

1. Open your project in the editor.
2. In the Project Explorer, expand your project tree.
3. Click **Device** under the Configuration section.

The options displayed depend on whether you're using the web editor or the desktop editor.

## Web Editor

When you open Device Configuration in the Autonomy Edge web IDE, you can browse available runtime targets linked to your account and connect to them.

### Communication Protocols in the Web Editor

The web editor supports configuring communication protocols for your targets:

- **Modbus Server**: Expose PLC registers to external Modbus masters.
- **Modbus Client**: Poll data from external Modbus slave devices.
- **OPC-UA Server**: Publish data using the OPC-UA standard (when available).

These protocols are added through the Project Explorer, not the Device Configuration panel itself. See [Communication Protocols](../communication/README) for setup instructions.

### What the Web Editor Does Not Support

The web editor deploys to the built-in Simulator or to runtime instances via Orchestrators. The following features are **not available** in the web editor:

- Pin mapping for physical hardware I/O
- Modbus RTU/TCP settings embedded in firmware
- Direct USB upload to microcontrollers
- Direct connection to local OpenPLC Runtime instances

For these capabilities, use the desktop editor.

> **Note:** The web editor does include a [built-in Simulator](../building-deploying/simulator) that emulates an AVR microcontroller directly in the browser. This lets you run and debug programs without any hardware or Orchestrator setup.

## Desktop Editor: Full Hardware Configuration

The desktop editor provides the complete set of hardware configuration options, organized into three areas:

| Configuration Area | Purpose |
|--------------------|---------|
| **Board Selection** | Choose from 100+ supported boards, view specs, download platform tools |
| **Pin Mapping** | Assign physical microcontroller pins to IEC 61131-3 I/O addresses |
| **Communication Settings** | Configure Modbus RTU and TCP for microcontroller firmware |

These areas are only active when an Arduino-compatible board is selected. When an OpenPLC Runtime target is selected, pin mapping and embedded communication settings are disabled because the runtime handles I/O and networking independently.

## Target Types

The editor supports three categories of deployment target, each with a different build and deployment workflow.

### Arduino-Compatible Targets (Desktop Editor)

When you select an Arduino-compatible board (e.g., Arduino Uno, ESP32, STM32), the editor performs **local compilation**:

1. Your IEC 61131-3 program is compiled into firmware.
2. The **arduino-cli** toolchain builds the binary for your target board.
3. A `defines.h` file is generated from your pin mapping configuration.
4. The firmware is uploaded directly to the board via USB.

This approach is suitable for:

- Standalone PLC devices running on dedicated microcontrollers
- Edge devices that operate independently without network connectivity
- Prototyping and educational projects

> **Tip:** Arduino development boards are not rated for industrial environments. For production deployments, use industrial-grade devices running OpenPLC Runtime v4 or deploy through Autonomy Edge.

### OpenPLC Runtime Targets (Desktop Editor)

When you select an OpenPLC Runtime target (v3 or v4), the editor prepares your program for **remote deployment**:

1. Your PLC program source code is packaged.
2. The source is sent over the network to the OpenPLC Runtime.
3. The runtime compiles and executes the program internally.

Pin mapping and embedded communication settings are disabled for runtime targets because:

- I/O addressing is handled by the runtime's own hardware configuration.
- Modbus and other protocols are configured through the runtime's web interface.

This approach is suitable for:

- Linux-based systems (Raspberry Pi, industrial PCs, edge servers)
- Applications requiring runtime debugging and monitoring
- Production systems with remote management needs

### Web Editor Targets

When you deploy from the Autonomy Edge web IDE, the program goes through a **cloud build pipeline**:

1. The IDE generates your project data.
2. The project is compiled and packaged.
3. The package is uploaded to the target runtime.
4. The runtime begins execution.

This approach is suitable for:

- Cloud-managed PLC deployments
- Teams that need centralized project management and secure remote access

## IEC 61131-3 Addressing

Regardless of the target type, all I/O points in your PLC program use standard IEC 61131-3 addressing:

| Address Type | Format | Example | Description |
|--------------|--------|---------|-------------|
| Digital Input | `%IX[byte].[bit]` | `%IX0.0` | First digital input |
| Digital Output | `%QX[byte].[bit]` | `%QX0.0` | First digital output |
| Analog Input | `%IW[index]` | `%IW0` | First analog input |
| Analog Output | `%QW[index]` | `%QW0` | First analog output |

For microcontroller targets, the pin mapping configuration connects these addresses to physical hardware pins. For runtime targets, I/O addressing is handled by the runtime's hardware abstraction layer.

## Configuration Workflows

### Web Editor

1. Open the Device section and select a target runtime.
2. Connect and authenticate with the runtime credentials.
3. Compile and deploy your program.

### Desktop Editor with Microcontroller

1. Select your target board from the [Board Selection](board-selection) interface.
2. Configure [Pin Mapping](pin-mapping) to assign physical pins to IEC addresses.
3. Set up [Communication Settings](communication-settings) for Modbus if needed.
4. Build and upload via USB.

### Desktop Editor with OpenPLC Runtime

1. Select **OpenPLC Runtime v3** or **OpenPLC Runtime v4** as the target.
2. Enter the runtime's IP address and port.
3. Connect to the runtime.
4. Build and deploy over the network.

## What's Next?

**Web Editor Users:**

- [Connecting to Runtimes](../connecting-to-runtimes): Full guide to connecting, authenticating, and deploying
- [Communication Protocols](../communication/README): Configure Modbus and OPC-UA

**Desktop Editor Users:**

- [Board Selection](board-selection): Choose and configure your target microcontroller board
- [Pin Mapping](pin-mapping): Map IEC addresses to physical hardware pins
- [Communication Settings](communication-settings): Configure Modbus RTU and TCP for microcontroller firmware
