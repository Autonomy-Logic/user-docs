# Communication Settings

> **Desktop Editor Only:** The communication settings described on this page apply to Arduino-compatible microcontroller targets in the desktop version of OpenPLC Editor. If you're using the Autonomy Edge web IDE at [edge.autonomylogic.com](https://edge.autonomylogic.com) or deploying to an OpenPLC Runtime target, Modbus and other protocols are configured through the [Communication Protocols](../communication/README) section instead.

Communication settings configure Modbus RTU and Modbus TCP directly in the microcontroller firmware. When enabled, the firmware includes a Modbus slave that exposes your PLC program's I/O registers to external Modbus masters over serial or network interfaces.

## Availability by Target Type

Not all targets support embedded communication settings:

| Target Type | Modbus RTU | Modbus TCP | Configuration Location |
|-------------|------------|------------|------------------------|
| Arduino / Microcontroller (`arduino-cli`) | Yes | Yes (boards with Ethernet or WiFi) | Device Configuration in desktop editor |
| OpenPLC Runtime v3/v4 (`openplc_runtime`) | Disabled | Disabled | Runtime web interface |
| Web Editor targets | N/A | N/A | [Communication Protocols](../communication/README) in project |

When the selected board uses the `openplc_runtime` compiler type, both Modbus RTU and Modbus TCP settings are hidden in the Device Configuration panel.

## Modbus RTU Configuration

Modbus RTU enables serial communication between your microcontroller and industrial equipment, sensors, HMIs, or other PLCs. The microcontroller acts as a Modbus slave (server).

### Parameters

| Parameter | Options | Description |
|-----------|---------|-------------|
| **Interface** | Serial, Serial1, Serial2, Serial3 | The hardware UART port to use for Modbus communication |
| **Baud Rate** | 9600, 14400, 19200, 38400, 57600, 115200 | Communication speed; must match all devices on the bus |
| **Slave ID** | 0–255 | The Modbus address of this device on the serial bus |
| **RS-485 Enable Pin** | GPIO pin number (or empty) | The pin connected to the DE/RE pins of an RS-485 transceiver |

### Enabling Modbus RTU

1. In the Device Configuration panel, locate the Communication Settings section.
2. Enable **Modbus RTU**.
3. Select the **Interface**: choose the UART port connected to your RS-485 or RS-232 converter.
4. Set the **Baud Rate** to match the other devices on your Modbus network.
5. Assign a unique **Slave ID** for this device (each device on the bus must have a different ID).

### RS-485 Direction Control

RS-485 is a half-duplex bus, meaning the transceiver must switch between transmit and receive modes. The RS-485 Enable Pin controls this switching:

- Set this to the GPIO pin wired to the DE (Driver Enable) and RE (Receiver Enable) pins of your RS-485 transceiver module.
- The firmware drives this pin HIGH during transmission and LOW during reception.
- Leave this field empty if you're using RS-232 (full duplex) or if your RS-485 transceiver has automatic direction control.

### Interface Selection Guide

| Interface | Typical Usage |
|-----------|---------------|
| **Serial** | The primary UART (pins 0/1 on most Arduino boards). Note: this is also the USB serial port on many boards, so using it for Modbus may prevent serial monitor debugging. |
| **Serial1** | Second UART, available on Mega, Due, Leonardo, and many ESP32/STM32 boards. Preferred for Modbus when you want to keep Serial free for debugging. |
| **Serial2 / Serial3** | Additional UARTs on boards that support them (Mega, Due, ESP32). |

## Modbus TCP Configuration

Modbus TCP enables communication over Ethernet or WiFi networks. The microcontroller acts as a Modbus TCP server, listening for connections from Modbus TCP clients on port 502.

### Parameters

| Parameter | Applies To | Description |
|-----------|------------|-------------|
| **Interface** | All | `Ethernet` or `WiFi`. The network hardware to use |
| **MAC Address** | Ethernet | Hardware MAC address for the Ethernet interface |
| **SSID** | WiFi only | The name of the WiFi network to join |
| **Password** | WiFi only | The WiFi network password |
| **IP Mode** | All | `DHCP` (automatic) or `Static` (manual) |
| **IP Address** | Static only | The static IP address for this device |
| **Subnet Mask** | Static only | The network subnet mask |
| **Gateway** | Static only | The default gateway address |
| **DNS** | Static only | The DNS server address |

### Enabling Modbus TCP

1. In the Device Configuration panel, locate the Communication Settings section.
2. Enable **Modbus TCP**.
3. Select the **Interface**:
   - Choose **Ethernet** for boards with wired network hardware (W5500 shield, built-in Ethernet).
   - Choose **WiFi** for boards with wireless capability (ESP32, ESP8266, WiFi-enabled Arduino boards).
4. If using WiFi, enter the **SSID** and **Password** for your network.
5. If using Ethernet, set the **MAC Address** (some boards have a factory-assigned MAC; others require manual entry).
6. Choose the **IP Mode**:
   - **DHCP**: The device obtains its IP address automatically from the network.
   - **Static**: Enter the IP Address, Subnet Mask, Gateway, and DNS manually.

### Board Requirements for Modbus TCP

| Interface | Required Hardware |
|-----------|-------------------|
| Ethernet | Board with built-in Ethernet (Arduino Opta, CONTROLLINO) or an Ethernet shield (W5500) |
| WiFi | ESP32, ESP8266, Arduino MKR WiFi, Arduino Uno R4 WiFi, Arduino Giga, or other WiFi-enabled board |

Boards without network hardware cannot use Modbus TCP. The editor disables the TCP option if the selected board doesn't include network capabilities.

## Modbus Address Mapping

When external Modbus masters communicate with your microcontroller, the Modbus registers map directly to IEC 61131-3 I/O addresses:

| Modbus Function Codes | Register Type | IEC Address | Access |
|-----------------------|---------------|-------------|--------|
| 01, 05, 15 | Coils (0x) | `%QX` | Read/Write |
| 02 | Discrete Inputs (1x) | `%IX` | Read Only |
| 04 | Input Registers (3x) | `%IW` | Read Only |
| 03, 06, 16 | Holding Registers (4x) | `%QW` | Read/Write |

For example, a Modbus master reading coil address 0 reads the value of `%QX0.0`. Writing holding register 0 writes to `%QW0`.

## Board-Specific Notes

### ESP32 / ESP8266

- WiFi is the primary network interface; these boards excel at Modbus TCP over WiFi.
- Multiple hardware UARTs are available, making it possible to run Modbus RTU and TCP simultaneously.
- ESP8266 has only one usable hardware UART for Modbus RTU (Serial1 is TX-only on most variants).

### Arduino with Ethernet Shield

- Requires a W5500-based Ethernet shield connected via SPI.
- The MAC address must be configured manually in most cases.
- SPI pins are shared with the shield; avoid mapping those pins for I/O.

### Arduino Opta / Portenta Machine Control

- Built-in industrial Ethernet with pre-assigned MAC addresses.
- Designed for industrial Modbus TCP networks.
- Robust connectors and industrial-grade components.

### CONTROLLINO

- Select models include built-in Ethernet and RS-485 interfaces.
- Suitable for both Modbus RTU and TCP deployments.
- Terminal block labels match the pin names in the editor.

## Testing Communication

After configuring and uploading your program:

1. **Verify network connectivity.** For TCP, confirm the device has obtained an IP address (check serial monitor output if available). For RTU, confirm the serial connection is wired correctly.
2. **Use a Modbus client tool** to test register access:
   - **TCP tools:** ModbusPoll, QModMaster, pymodbus, or any SCADA system with Modbus TCP support.
   - **RTU tools:** Serial-based Modbus tools with the correct COM port, baud rate, and slave ID.
3. **Read and write test values.** Write a value to a holding register (`%QW`) and verify your PLC program receives it. Read a coil (`%QX`) and verify it matches the output state.
4. **Check the IDE console** for any communication error messages during upload or runtime.

## Troubleshooting

### Modbus RTU not responding

- Verify the baud rate matches on both the microcontroller and the Modbus master.
- Check wiring: TX/RX for RS-232, or A/B lines for RS-485.
- Ensure the Slave ID doesn't conflict with another device on the bus.
- If using RS-485, verify the Enable Pin is correctly configured and wired.
- Confirm you selected the correct Serial interface (Serial vs Serial1, etc.).

### Modbus TCP connection refused

- Confirm the device has a valid IP address (check DHCP assignment or static configuration).
- Verify the Modbus client is connecting to port 502.
- Check firewall settings on your network.
- For WiFi, verify SSID and password are correct and the device has joined the network.
- Ensure the client and device are on the same subnet.

### Communication enabled but no data exchange

- Verify that communication is actually enabled in the Device Configuration (not just configured).
- Confirm the board supports the selected interface by checking the board's hardware specs.
- Review the console output during upload for any warnings about unsupported features.

## What's Next?

- [Device Configuration Overview](device-config-overview): Understand all target types and their communication options
- [Board Selection](board-selection): Choose a board with the network capabilities you need
- [Pin Mapping](pin-mapping): Configure I/O pin assignments alongside communication settings
- [Modbus Server](../communication/modbus/server): Configure Modbus server for runtime targets
- [Modbus Client](../communication/modbus/client): Configure Modbus client for polling external devices
- [Modbus Addressing](../communication/modbus/addressing): Detailed register-to-address mapping reference
