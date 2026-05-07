# Modbus Client Configuration

When configured as a Modbus client (master), Autonomy Edge initiates connections to external Modbus servers and polls data on a configurable schedule. This lets your PLC program read sensor values, monitor remote I/O modules, control variable frequency drives, and exchange data with other PLCs — all from a centralized project.

## Adding a Remote Device

To add a Modbus client connection in the Autonomy Edge web editor:

1. In the project explorer, click the **+** button.
2. Select **Remote Device** from the dropdown menu.
3. Choose the transport protocol:
   - **Modbus/TCP** for Ethernet-based communication
   - **Modbus/RTU** for serial (RS-232 / RS-485) communication
4. Enter a descriptive name for the device (e.g., `TempSensors_Rack1`).
5. Click **Create**.
6. The new device entry appears under the **Devices** folder in the project tree.
7. Click the device entry to open its configuration panel.

You can add multiple remote devices to a single project. Each device maintains its own independent connection and polling schedule.

## Connection Settings

### Modbus TCP

| Setting | Description | Default |
|---------|-------------|---------|
| **Name** | Descriptive name for this remote device | `Remote Device` |
| **Host** | IP address or hostname of the Modbus server | -- (required) |
| **Port** | TCP port of the Modbus server | `502` |
| **Timeout** | Maximum time (in milliseconds) to wait for a response before declaring a communication error | `1000` |

### Modbus RTU

For serial connections, additional settings apply:

| Setting | Description | Default |
|---------|-------------|---------|
| **Name** | Descriptive name for this remote device | `Remote Device` |
| **Serial Port** | The serial port device (e.g., `/dev/ttyUSB0`) | -- (required) |
| **Baud Rate** | Communication speed in bits per second | `9600` |
| **Slave ID** | The Modbus slave address (1--247) of the target device | `1` |
| **Timeout** | Maximum time (in milliseconds) to wait for a response | `1000` |

Modbus RTU supports **multi-drop** configurations where multiple slave devices share a single RS-485 serial bus. Each device is identified by a unique slave ID. Add a separate remote device entry for each slave on the bus.

## Error Handling

When the client cannot communicate with a remote device (timeout, disconnection, or protocol error), you can choose how the mapped IEC variables behave:

| Option | Behavior |
|--------|----------|
| **Keep Last Value** | Retain the last successfully read value in the IEC variables. The PLC program continues operating with stale data until communication recovers. |
| **Set to Zero** | Reset all mapped IEC variables to zero. This provides a clear indication that data is no longer valid. |

Choose the option that best fits your application's safety requirements. For critical processes, **Set to Zero** combined with a watchdog timer in your PLC logic is generally safer.

## Connection Retry Behavior

When a connection to a remote device fails, the Modbus client uses an **exponential backoff** strategy to avoid flooding the network with reconnection attempts:

| Parameter | Value |
|-----------|-------|
| Initial retry delay | 2 seconds |
| Maximum retry delay | 30 seconds |
| Backoff multiplier | 1.5x |

The client starts with a 2-second delay between retries, increasing by a factor of 1.5 after each failure, up to a maximum of 30 seconds. Once communication is re-established, the retry timer resets.

## IO Groups

IO Groups are the core of the Modbus client configuration. Each IO Group defines a block of Modbus data to read from or write to the remote device. You can create multiple IO Groups per device to poll different data areas at different rates.

### IO Group Settings

| Field | Description |
|-------|-------------|
| **Name** | Descriptive name for this group (e.g., `TemperatureInputs`) |
| **Function Code** | The Modbus function code that determines the operation type |
| **Modbus Offset** | Starting address on the remote device (decimal or hexadecimal, e.g., `0` or `0x0000`) |
| **Length** | Number of registers or coils to read/write |
| **IEC Location** | The IEC 61131-3 address assigned to the first data point in this group (auto-assigned by the editor) |
| **Cycle Time (ms)** | How frequently this group is polled, in milliseconds |
| **Error Handling** | What to do on communication error (Keep Last Value or Set to Zero) |

### Supported Function Codes

| FC | Name | Operation | IEC Mapping |
|----|------|-----------|-------------|
| 1 | Read Coils | Read digital outputs from remote device | `%IX` (inputs) |
| 2 | Read Discrete Inputs | Read digital inputs from remote device | `%IX` (inputs) |
| 3 | Read Holding Registers | Read analog/word data from remote device | `%IW` (inputs) |
| 4 | Read Input Registers | Read analog input data from remote device | `%IW` (inputs) |
| 5 | Write Single Coil | Write one digital output to remote device | `%QX` (outputs) |
| 6 | Write Single Register | Write one analog value to remote device | `%QW` (outputs) |
| 15 | Write Multiple Coils | Write multiple digital outputs to remote device | `%QX` (outputs) |
| 16 | Write Multiple Registers | Write multiple analog values to remote device | `%QW` (outputs) |

**Key rule**: Read function codes (FC 1--4) map data to **input** addresses (`%I`), because from the PLC's perspective the data is coming *in* from the remote device. Write function codes (FC 5, 6, 15, 16) map to **output** addresses (`%Q`), because the PLC is sending data *out* to the remote device.

### Automatic IEC Location Assignment

When you create an IO Group, the editor automatically assigns the next available IEC location based on the function code. For example:

- First group using FC 3 (Read Holding Registers) might receive `%IW0`
- A second group using FC 3 with length 4 (after the first group of length 10) would receive `%IW10`
- A group using FC 16 (Write Multiple Registers) might receive `%QW0`

You can view and verify these assignments in the IO Tag Mapping table.

### Viewing Individual IO Points

Click the expand arrow next to any IO Group to see the individual data points. Each point shows:

| Column | Description |
|--------|-------------|
| **Name** | Auto-generated name (e.g., `TemperatureInputs_0`, `TemperatureInputs_1`) |
| **Type** | Data type (`Analog Input` for registers, `Digital Input`/`Digital Output` for coils) |
| **Address** | The assigned IEC address (`%IW0`, `%IW1`, etc.) |
| **Alias** | Optional custom name you can set for use in your PLC program |

## Cycle Time Optimization

When multiple IO Groups are configured with different cycle times, the runtime calculates the **greatest common divisor (GCD)** of all cycle times to determine the base polling interval. This optimizes communication by batching requests that fall on the same polling tick.

For example, if you have three IO Groups with cycle times of 100 ms, 200 ms, and 500 ms:

- GCD = 100 ms (the base polling interval)
- The 100 ms group is polled every tick
- The 200 ms group is polled every other tick
- The 500 ms group is polled every fifth tick

**Best practice**: Choose cycle times that are multiples of each other to get the most efficient polling schedule. Avoid prime-number cycle times that would result in a GCD of 1 ms.

## Example Configurations

### Reading Temperature Sensors

Poll four temperature values from a remote sensor module every 500 ms:

| Setting | Value |
|---------|-------|
| **Host** | `192.168.1.50` |
| **Port** | `502` |
| **Function Code** | FC 4 (Read Input Registers) |
| **Offset** | `0x0000` |
| **Length** | `4` |
| **IEC Location** | `%IW100` (auto-assigned) |
| **Cycle Time** | `500` ms |

This reads Modbus input registers 0--3 from the remote device and maps them to `%IW100` through `%IW103` in your PLC program. Your Structured Text or Ladder logic can then use these variables directly.

### Controlling a Variable Frequency Drive

Write speed and control commands to a VFD every 100 ms:

| Setting | Value |
|---------|-------|
| **Host** | `192.168.1.60` |
| **Port** | `502` |
| **Function Code** | FC 16 (Write Multiple Registers) |
| **Offset** | `0x0000` |
| **Length** | `2` |
| **IEC Location** | `%QW200` (auto-assigned) |
| **Cycle Time** | `100` ms |

This writes the values of `%QW200` (speed setpoint) and `%QW201` (control word) to Modbus holding registers 0--1 on the VFD every 100 ms.

### Multi-Drop RTU Configuration

Reading from three devices on a single RS-485 bus:

Add three separate remote device entries, all pointing to the same serial port but with different slave IDs:

| Device Name | Serial Port | Slave ID | IO Groups |
|-------------|-------------|----------|-----------|
| `FlowMeter_1` | `/dev/ttyUSB0` | `1` | FC 4, offset 0, length 2 |
| `FlowMeter_2` | `/dev/ttyUSB0` | `2` | FC 4, offset 0, length 2 |
| `PressureSensor` | `/dev/ttyUSB0` | `3` | FC 3, offset 10, length 4 |

Each device is polled independently according to its own cycle time.

## Configuration Export

When you transfer a project to the runtime, the Modbus client configuration is exported as `modbus_master.json` inside the program package. This file contains all remote device definitions, IO Group mappings, and polling parameters. It is generated automatically by the editor — you do not need to edit it manually.

## Troubleshooting

### Communication Errors

1. Verify the remote device is powered on and connected to the network (or serial bus).
2. Confirm the IP address (or serial port), port, and slave ID settings match the remote device.
3. Increase the timeout value if you are on a slow or congested network.
4. Use a Modbus diagnostic tool (e.g., QModMaster, `mbpoll`, or ModRSsim2) to verify the remote device responds correctly.

### Incorrect or Zero Data Values

1. Verify the function code matches what the remote device expects. Consult the device's Modbus register map documentation.
2. Check the Modbus offset — some devices use 0-based addressing while others use 1-based. You may need to subtract 1 from the address in the device documentation.
3. For 32-bit values spanning two registers, confirm the byte order. Autonomy Edge uses big-endian (high word first), which is the Modbus standard, but some devices use little-endian or mid-endian (word-swapped) byte order.
4. Verify the error handling setting. If set to **Set to Zero**, values will read as zero whenever communication is interrupted.

### Slow or Inconsistent Polling

1. Check the cycle time settings. Very short cycle times (under 50 ms) may not be achievable depending on network latency and the number of IO Groups.
2. Reduce the number of IO Groups or combine small reads into larger blocks where the remote device supports it.
3. Review the cycle time optimization section above — ensure your cycle times share a reasonable GCD.
4. On serial (RTU) connections, polling is inherently slower than TCP. Account for serial transmission time and turnaround delays.

## What's Next?

- **[Modbus Server Configuration](server)** — Expose your PLC data to external SCADA and HMI systems
- **[Modbus Addressing](addressing)** — Detailed address mapping tables, formulas, and runtime version differences
- **[Communication Protocols Overview](../README)** — Return to the protocols overview
