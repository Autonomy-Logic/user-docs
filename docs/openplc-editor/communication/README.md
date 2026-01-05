# Communication Protocols

OpenPLC Editor supports configuring various industrial communication protocols to enable your PLC programs to communicate with other devices, sensors, and systems. This section covers how to set up and use these protocols.

## Available Protocols

### Modbus

Modbus is one of the most widely used industrial communication protocols. OpenPLC supports both Modbus server (slave) and Modbus client (master) configurations:

- **[Modbus Server](modbus/server.md)**: Configure your PLC to act as a Modbus slave device, exposing its internal registers to other systems
- **[Modbus Client](modbus/client.md)**: Configure your PLC to poll data from external Modbus devices
- **[Modbus Addressing](modbus/addressing.md)**: Understanding how IEC 61131-3 addresses map to Modbus registers

### OPC-UA (Coming Soon)

OPC-UA (Open Platform Communications Unified Architecture) is a modern, secure protocol for industrial communication. Support for OPC-UA is currently in development.

- **[OPC-UA Overview](opc-ua/overview.md)**: Introduction to OPC-UA in OpenPLC

## Adding Communication Configurations

Communication protocols are configured through the project explorer in OpenPLC Editor:

1. In the project explorer, locate the project tree
2. Click the blue **+** button to add a new element
3. Select the type of communication you want to add:
   - **Server > Modbus**: Add a Modbus server (slave) configuration
   - **Remote IO > Modbus**: Add a Modbus client (master) to poll external devices

## Protocol Support by Version

| Protocol | Desktop Editor | Web Editor | Runtime v4 | Runtime v3 |
|----------|---------------|------------|------------|------------|
| Modbus Server (Slave) | Yes | Yes | Yes | Yes |
| Modbus Client (Master) | Yes | Yes | Yes | Yes |
| OPC-UA | Development | Development | Development | No |
| DNP3 | No | No | No | Yes |
| EtherNet/IP | No | No | No | Yes |

Note: DNP3 and EtherNet/IP are only available in Runtime v3 and are not supported in the v4 architecture.
