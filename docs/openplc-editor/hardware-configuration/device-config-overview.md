# Device Configuration Overview

The Device Configuration section is where you configure how your PLC program connects to and controls hardware. The available options differ significantly between the desktop editor and the web editor (Autonomy Edge).

![Device Configuration Screen](images/device-config-overview.png)

## Accessing Device Configuration

To access the Device Configuration:

1. Open your project in the editor
2. In the Project Explorer, expand your project
3. Click on **Device** under the Configuration section

## Web Editor vs Desktop Editor

The hardware configuration options available depend on which version of OpenPLC Editor you're using.

### Web Editor (Autonomy Edge)

The web editor can **only** deploy programs to vPLC instances running on orchestrator agents. When you open Device Configuration in the web editor, you'll see options to:

- Connect to orchestrators linked to your account
- Select vPLC devices to deploy your program
- Configure communication protocols (Modbus)

The web editor does **not** support:
- Arduino or microcontroller programming
- Direct connection to local OpenPLC Runtime instances
- Pin mapping for hardware I/O
- Board selection

For web editor deployment, see [Connecting to Runtimes](../connecting-to-runtimes.md).

![Device Orchestrators View in Web Editor](images/device-orchestrators-expanded.png)

### Desktop Editor

The desktop editor provides full hardware configuration capabilities, including:

- **Board Selection**: Choose from 60+ supported Arduino-compatible boards
- **Pin Mapping**: Configure which physical pins map to IEC I/O addresses
- **Communication Settings**: Set up Modbus RTU/TCP for microcontroller targets
- **Direct Runtime Connection**: Connect to OpenPLC Runtime v3 or v4 instances

The desktop editor supports two fundamentally different deployment targets:

## Target Types (Desktop Editor)

### Arduino-Compatible Targets

When you select an Arduino-compatible board (such as Arduino Uno, ESP32, STM32), the editor performs **local compilation**:

1. Your PLC program is transpiled from IEC 61131-3 languages to C/C++ code
2. The editor uses the bundled OpenPLC runtime code optimized for microcontrollers
3. The **arduino-cli** toolchain compiles the code into binary firmware
4. The firmware is uploaded directly to the board via USB

This approach is ideal for:
- Standalone PLC devices running on dedicated microcontrollers
- Edge devices that operate independently
- Applications requiring direct hardware I/O control
- Prototyping and educational projects

> **Note**: Arduino boards aren't suitable for industrial environments. Use microcontroller targets for prototyping only. For production, deploy to industrial-grade devices running OpenPLC Runtime v4.

### OpenPLC Runtime Targets

When you select an OpenPLC Runtime target, the editor prepares source files for **remote compilation**:

1. Your PLC program source code (Structured Text) is packaged
2. The source is sent over the network to the OpenPLC Runtime
3. The runtime compiles and executes the program internally

This approach is ideal for:
- Linux-based systems (Raspberry Pi, industrial PCs, servers)
- vPLC instances (virtual PLCs running in containers)
- Applications requiring runtime debugging and monitoring
- Production systems with remote management needs

## Configuration Workflow

### Desktop Editor with Microcontroller

1. **Select Target Board**: Choose your Arduino-compatible board
2. **Configure Pin Mapping**: Assign physical pins to IEC addresses
3. **Set Communication Options**: Configure Modbus RTU/TCP if needed
4. **Build and Upload**: Compile and upload via USB

### Desktop Editor with OpenPLC Runtime

1. **Select Runtime Target**: Choose OpenPLC Runtime v3 or v4
2. **Enter Runtime Address**: Specify the IP address of the runtime
3. **Connect**: Establish connection to the runtime
4. **Build and Deploy**: Compile and upload over the network

### Web Editor with vPLC

1. **Open Orchestrators**: View available orchestrator agents
2. **Select vPLC**: Choose the vPLC device to deploy to
3. **Connect**: Establish connection through the orchestrator
4. **Build and Deploy**: Compile and upload through secure channel

## IEC Addressing

Regardless of the target type, all I/O points in your PLC program use IEC 61131-3 standard addressing:

| Address Type | Format | Example | Description |
|--------------|--------|---------|-------------|
| Digital Input | `%IX[bank].[bit]` | `%IX0.0` | First digital input |
| Digital Output | `%QX[bank].[bit]` | `%QX0.0` | First digital output |
| Analog Input | `%IW[index]` | `%IW0` | First analog input |
| Analog Output | `%QW[index]` | `%QW0` | First analog output |

For microcontroller targets, the pin mapping configuration connects these IEC addresses to physical hardware pins. For runtime targets, I/O addressing is handled by the runtime's hardware configuration.

## Next Steps

**Desktop Editor Users:**
- [Board Selection](board-selection.md) - Choose and configure your target board
- [Pin Mapping](pin-mapping.md) - Map IEC addresses to physical pins
- [Communication Settings](communication-settings.md) - Configure Modbus for microcontrollers

**Web Editor Users:**
- [Connecting to Runtimes](../connecting-to-runtimes.md) - Connect to vPLC devices via orchestrator
- [Communication Protocols](../communication/README.md) - Configure Modbus for vPLC devices
