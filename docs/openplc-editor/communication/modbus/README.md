# Modbus Communication

Modbus is a serial communication protocol originally published by Modicon in 1979 for use with programmable logic controllers. Over the decades it has become the de facto standard for industrial device communication thanks to its simplicity, openness, and broad vendor support. Autonomy Edge provides full Modbus TCP and RTU support for both server (slave) and client (master) roles, enabling your PLC programs to exchange data with virtually any Modbus-compatible device.

## How Modbus Works

Modbus follows a request/response model. A **client** (historically called the "master") sends a request to a **server** (historically called the "slave"), which processes the request and returns a response. Each request specifies a **function code** that tells the server what operation to perform and an **address range** that identifies the data to read or write.

A typical Modbus transaction looks like this:

1. The client opens a connection to the server (TCP) or selects it by slave ID (RTU).
2. The client sends a request containing a function code, starting address, and quantity.
3. The server validates the request, reads or writes the requested data, and returns a response.
4. The client processes the response and uses the data in its control logic.

If the server cannot process the request (invalid address, unsupported function code, device busy), it returns an **exception response** with an error code. The client can then retry, log the error, or take corrective action.

## Transport Layers

Communication happens over one of two transport layers:

| Transport | Medium | Addressing | Max Devices | Typical Speed | Use Case |
|-----------|--------|------------|-------------|---------------|----------|
| **Modbus TCP** | Ethernet (TCP/IP) | IP address + port | Unlimited (network capacity) | 10/100/1000 Mbps | Plant-floor Ethernet networks, remote I/O over IP |
| **Modbus RTU** | Serial (RS-232 / RS-485) | Slave ID (1--247) | 247 per bus (RS-485) | 9600--115200 baud | Legacy serial devices, multi-drop RS-485 buses |

### Modbus TCP

Modbus TCP wraps the standard Modbus protocol data unit (PDU) inside a TCP/IP packet. Each device is identified by its IP address, and multiple simultaneous connections are supported. The default port is **502**.

Advantages of Modbus TCP:
- Standard Ethernet infrastructure (switches, routers, firewalls)
- No distance limitations beyond normal Ethernet constraints
- Multiple simultaneous client connections to a single server
- Higher throughput than serial RTU

### Modbus RTU

Modbus RTU transmits data as a binary stream over serial lines (RS-232 for point-to-point, RS-485 for multi-drop). Each device on the bus has a unique **slave ID** (1--247). The bus operates in a half-duplex mode where only one device transmits at a time.

Modbus RTU supports **multi-drop** configurations where multiple slave devices share a single RS-485 serial bus. The client addresses each device by its slave ID, and only the addressed device responds. This makes RTU ideal for connecting multiple field instruments on a single cable run.

## Server vs. Client

| Role | Also Called | Description | When to Use |
|------|------------|-------------|-------------|
| **Server** | Slave | Listens for requests and exposes PLC data. External SCADA systems and HMIs connect to this. | When external systems need to read your PLC data or write setpoints |
| **Client** | Master | Initiates requests to poll data from remote devices such as sensors, VFDs, or other PLCs. | When your PLC needs to gather data from field devices |

A single Autonomy Edge project can run both roles simultaneously — for example, acting as a Modbus server for a SCADA system while also polling remote I/O modules and sensors as a Modbus client.

## Modbus Data Types

The Modbus specification defines four data types, each mapped to a specific area of device memory:

| Data Type | Access | Size | Modbus Term | Typical Use |
|-----------|--------|------|-------------|-------------|
| **Coils** | Read/Write | 1 bit | 0xxxx | Digital outputs (relays, solenoids, indicator lights) |
| **Discrete Inputs** | Read Only | 1 bit | 1xxxx | Digital inputs (switches, proximity sensors, limit switches) |
| **Holding Registers** | Read/Write | 16 bits | 4xxxx | Analog outputs, setpoints, configuration values, status words |
| **Input Registers** | Read Only | 16 bits | 3xxxx | Analog inputs (temperature, pressure, flow, level) |

> **Note on 5-digit notation**: Many Modbus tools and device manuals display addresses with a leading digit that indicates the data type (e.g., 40001 for the first holding register, 30001 for the first input register). Autonomy Edge uses **0-based** addressing internally, so holding register 40001 corresponds to address 0 in the editor. See the [Addressing](addressing) page for detailed conversion tables.

## Function Codes

Every Modbus transaction uses a function code (FC) to specify the operation. The most commonly used function codes are:

### Read Function Codes

| FC | Name | Data Type | Description |
|----|------|-----------|-------------|
| 1 | Read Coils | Coils (bits) | Read one or more coil (digital output) values |
| 2 | Read Discrete Inputs | Discrete Inputs (bits) | Read one or more discrete input values |
| 3 | Read Holding Registers | Holding Registers (16-bit) | Read one or more holding register values |
| 4 | Read Input Registers | Input Registers (16-bit) | Read one or more input register values |

### Write Function Codes

| FC | Name | Data Type | Description |
|----|------|-----------|-------------|
| 5 | Write Single Coil | Single Coil (1 bit) | Write a single coil to ON (0xFF00) or OFF (0x0000) |
| 6 | Write Single Register | Single Holding Register | Write a single 16-bit value to a holding register |
| 15 | Write Multiple Coils | Multiple Coils | Write a block of coil values in a single request |
| 16 | Write Multiple Registers | Multiple Holding Registers | Write a block of register values in a single request |

When Autonomy Edge acts as a Modbus **client**, read function codes (FC 1--4) map incoming data to `%I` (input) addresses, while write function codes (FC 5, 6, 15, 16) source outgoing data from `%Q` (output) addresses.

## Multi-Register Data Types

While native Modbus registers are 16 bits wide, larger data types are supported by reading or writing consecutive registers:

| IEC Data Type | Size | Registers Required | Byte Order |
|---------------|------|--------------------|------------|
| INT / UINT | 16 bits | 1 | N/A (single register) |
| DINT / UDINT / REAL | 32 bits | 2 | Big-endian (high word first) |
| LINT / ULINT / LREAL | 64 bits | 4 | Big-endian (high word first) |

Autonomy Edge uses **big-endian** (network byte order) for all multi-register values, which is the Modbus standard. The first register in a group contains the most significant word. Some third-party devices may use little-endian or word-swapped byte order — consult the device documentation if values appear garbled.

## IEC 61131-3 Address Mapping

Autonomy Edge maps Modbus data types directly to IEC 61131-3 located variables:

| Modbus Data Type | IEC Prefix | Address Range | Example |
|------------------|------------|---------------|---------|
| Discrete Inputs | `%IX` | `%IX0.0` through `%IX999.7` | `%IX5.3` = Modbus discrete input 43 |
| Coils | `%QX` | `%QX0.0` through `%QX999.7` | `%QX0.0` = Modbus coil 0 |
| Input Registers | `%IW` | `%IW0` through `%IW999` | `%IW25` = Modbus input register 25 |
| Holding Registers | `%QW` | `%QW0` through `%QW999` | `%QW100` = Modbus holding register 100 |

> **Runtime v4 limitation**: The v4 runtime maps Modbus to a smaller subset of the I/O buffer (64 coils/discrete inputs, 32 registers). Memory addresses (`%M`) are not accessible via Modbus in v4. See the [Addressing](addressing) page for version-specific details.

For complete address mapping tables, calculation formulas, and runtime version differences, see the [Addressing](addressing) page.

## Configuration in Autonomy Edge

All Modbus configuration is done in the project explorer of the Autonomy Edge web editor:

- **To add a Modbus server**: Click the **+** button, select **Server**, choose **Modbus/TCP**, and enter a name.
- **To add a Modbus client (TCP)**: Click the **+** button, select **Remote Device**, choose **Modbus/TCP**, and enter a name.
- **To add a Modbus client (RTU)**: Click the **+** button, select **Remote Device**, choose **Modbus/RTU**, and enter a name.

The new element appears in the project tree. Click it to open its configuration panel where you set connection parameters, data mappings, and polling options.

When you transfer the project to the runtime, the editor automatically exports the configuration:
- Modbus server settings are saved as `modbus_slave.json`
- Modbus client settings are saved as `modbus_master.json`

## Common Modbus Use Cases

Here are some typical scenarios where Modbus is used in Autonomy Edge projects:

| Use Case | Role | Transport | Description |
|----------|------|-----------|-------------|
| SCADA monitoring | Server | TCP | A SCADA system reads sensor values and process data from the PLC |
| HMI control | Server | TCP | An HMI panel reads and writes setpoints, alarm acknowledgments, and mode selections |
| Remote I/O expansion | Client | TCP | The PLC polls digital and analog I/O from remote Modbus I/O modules |
| VFD speed control | Client | TCP or RTU | The PLC writes speed setpoints and reads status from variable frequency drives |
| Energy metering | Client | RTU | The PLC reads power, voltage, and current from energy meters on an RS-485 bus |
| Multi-PLC coordination | Server + Client | TCP | Multiple PLCs exchange data by acting as both servers and clients |
| Sensor array | Client | RTU (multi-drop) | The PLC polls multiple temperature or pressure sensors on a single RS-485 bus |

## What's Next?

- **[Server Configuration](server)** — Start here if SCADA or HMI systems need to connect to your PLC
- **[Client Configuration](client)** — Start here if your PLC needs to read sensors or control drives
- **[Communication Protocols Overview](../README)** — Return to the protocols overview for OPC-UA and other options
