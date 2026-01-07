# Communication Settings

Communication settings configure how your PLC program communicates with external systems using industrial protocols. The available options depend on whether you're using the desktop editor with microcontroller targets or deploying to OpenPLC Runtime/vPLC instances.

## Communication Options by Target Type

| Target | Modbus RTU | Modbus TCP | Configuration Location |
|--------|------------|------------|------------------------|
| Arduino/Microcontroller | Yes | Yes (WiFi/Ethernet boards) | Hardware Configuration |
| OpenPLC Runtime v4 | Via Runtime | Via Runtime | Runtime Web Interface |
| vPLC (Web Editor) | N/A | Via Runtime | Runtime Web Interface |

## Microcontroller Communication Settings

> **Desktop Editor Only**: These settings apply when targeting Arduino-compatible boards in the desktop editor.

For microcontroller targets, communication settings are configured in the Hardware Configuration section alongside board selection and pin mapping.

![Communication Settings for Microcontrollers](images/communication-settings-micro.png)

### Modbus RTU Configuration

Modbus RTU uses serial communication for connecting to industrial equipment, sensors, and other PLCs.

| Parameter | Options | Description |
|-----------|---------|-------------|
| **Interface** | Serial, Serial1, Serial2, Serial3 | Hardware serial port to use |
| **Baud Rate** | 9600, 14400, 19200, 38400, 57600, 115200 | Communication speed |
| **Slave ID** | 0-255 | Modbus address of this device |
| **RS-485 Enable Pin** | Pin number or empty | GPIO pin for RS-485 direction control |

#### Enabling Modbus RTU

1. In Hardware Configuration, locate the Communication Settings section
2. Check **Enable Modbus RTU**
3. Select the serial interface connected to your RS-485/RS-232 converter
4. Set the baud rate to match your network
5. Assign a unique Slave ID for this device

#### RS-485 Configuration

When using RS-485 half-duplex communication:

- The enable pin controls the direction of the RS-485 transceiver
- Set this to the GPIO pin connected to your RS-485 module's DE/RE pins
- Leave empty if using RS-232 or automatic direction control

### Modbus TCP Configuration

Modbus TCP enables communication over Ethernet or WiFi networks.

| Parameter | Description |
|-----------|-------------|
| **Interface** | Ethernet or WiFi |
| **SSID** | WiFi network name (WiFi only) |
| **Password** | WiFi password (WiFi only) |
| **MAC Address** | Network hardware address |
| **IP Mode** | DHCP or Static |
| **IP Address** | Static IP configuration |
| **Subnet** | Network subnet mask |
| **Gateway** | Network gateway address |
| **DNS** | DNS server address |

![Modbus TCP Settings](images/modbus-tcp-settings.png)

#### Board Requirements

| Interface | Required Hardware |
|-----------|-------------------|
| Ethernet | Board with Ethernet hardware (W5500, built-in MAC) |
| WiFi | ESP32, ESP8266, or WiFi-enabled Arduino |

## Runtime Communication Settings

For OpenPLC Runtime v4 and vPLC targets, Modbus communication is configured through the runtime's web interface or the Communication Protocols section in the editor.

See [Communication Protocols](../communication/README.md) for detailed information on:
- [Modbus Server Configuration](../communication/modbus/server.md)
- [Modbus Client Configuration](../communication/modbus/client.md)
- [Modbus Addressing](../communication/modbus/addressing.md)

## Modbus Address Mapping

Regardless of target type, Modbus registers map to your PLC's I/O addresses:

| Modbus Function | Register Type | IEC Address | Description |
|-----------------|---------------|-------------|-------------|
| 01, 05, 15 | Coils (0x) | `%QX` | Digital outputs (read/write) |
| 02 | Discrete Inputs (1x) | `%IX` | Digital inputs (read only) |
| 04 | Input Registers (3x) | `%IW` | Analog inputs (read only) |
| 03, 06, 16 | Holding Registers (4x) | `%QW` | Analog outputs (read/write) |

When a Modbus master reads or writes registers, the values are exchanged with your PLC program's variables at the corresponding addresses.

## Testing Communication

After configuring communication settings:

1. **Build and upload** your program to the target
2. Use a **Modbus client tool** to test connectivity:
   - For TCP: ModbusPoll, QModMaster, or pymodbus
   - For RTU: Serial Modbus tools with appropriate COM port settings
3. **Verify register access** by reading/writing test values
4. Check the **IDE console** for any communication errors

## Board-Specific Notes

### ESP32 / ESP8266

- WiFi is the primary network interface
- Can run both Modbus RTU and TCP simultaneously
- Multiple serial ports available for RTU

### Arduino with Ethernet Shield

- Requires W5500 or similar Ethernet shield
- Uses hardware SPI for communication
- MAC address typically needs manual configuration

### Arduino Opta / Machine Control

- Built-in Ethernet with industrial-grade connectivity
- Designed for industrial Modbus networks
- Pre-configured MAC addresses

### CONTROLLINO

- Industrial Ethernet built-in on some models
- RS-485 interface available
- Suitable for both RTU and TCP networks

## Troubleshooting

### RTU Connection Issues

- Verify baud rate matches on both ends
- Check wiring (TX/RX, A/B for RS-485)
- Ensure Slave ID doesn't conflict with other devices
- Verify RS-485 enable pin is correctly configured

### TCP Connection Issues

- Confirm IP address and port (default: 502)
- Check firewall settings on your network
- Verify WiFi credentials are correct
- Ensure device is on the same subnet as the master

### General Issues

- Check that communication is enabled in settings
- Verify the board supports the selected interface
- Review console output for error messages

## Related Topics

- [Device Configuration Overview](device-config-overview.md) - Understanding target types
- [Board Selection](board-selection.md) - Choosing your target hardware
- [Pin Mapping](pin-mapping.md) - Configuring I/O addresses
- [Modbus Communication](../communication/modbus/README.md) - Detailed Modbus configuration
