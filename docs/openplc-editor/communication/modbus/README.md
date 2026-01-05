# Modbus Communication

Modbus is a serial communication protocol originally published by Modicon in 1979 for use with its programmable logic controllers. It has become a de facto standard communication protocol in industrial environments and is now one of the most commonly available means of connecting industrial electronic devices.

OpenPLC supports Modbus TCP for both server (slave) and client (master) operations, allowing your PLC programs to communicate with a wide variety of industrial equipment.

## Modbus Concepts

### Server vs Client (Slave vs Master)

In Modbus terminology:

- **Server (Slave)**: A device that responds to requests from a client. When OpenPLC acts as a Modbus server, other systems can read and write to its internal registers.
- **Client (Master)**: A device that initiates requests to servers. When OpenPLC acts as a Modbus client, it can poll data from external Modbus devices.

### Modbus Data Types

Modbus defines four types of data:

| Type | Access | Size | Description |
|------|--------|------|-------------|
| Coils | Read/Write | 1 bit | Digital outputs |
| Discrete Inputs | Read Only | 1 bit | Digital inputs |
| Holding Registers | Read/Write | 16 bits | Analog outputs / general storage |
| Input Registers | Read Only | 16 bits | Analog inputs |

## In This Section

- **[Server Configuration](server.md)**: Set up OpenPLC as a Modbus slave device
- **[Client Configuration](client.md)**: Configure OpenPLC to poll external Modbus devices
- **[Addressing](addressing.md)**: Understand how IEC 61131-3 addresses map to Modbus registers
