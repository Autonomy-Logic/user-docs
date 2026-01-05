# Modbus Client Configuration

This page explains how to configure OpenPLC as a Modbus TCP client (master), allowing your PLC program to read and write data to external Modbus devices.

## Overview

When configured as a Modbus client, OpenPLC can poll data from external Modbus servers such as:

- Remote I/O modules
- Variable frequency drives (VFDs)
- Power meters and sensors
- Other PLCs with Modbus server capability

## Adding a Remote Device

To add a Modbus client configuration to your project:

1. In the project explorer, click the blue **+** button
2. Select **Remote IO** > **Modbus**
3. A new remote device entry will appear under the Devices folder
4. Click on the device entry to configure its settings

## Device Configuration

### Connection Settings

| Setting | Description | Default |
|---------|-------------|---------|
| Name | A descriptive name for the device | Remote Device |
| Host | IP address or hostname of the Modbus server | - |
| Port | TCP port of the Modbus server | 502 |
| Timeout | Connection timeout in milliseconds | 1000 |

### Error Handling

| Option | Description |
|--------|-------------|
| Keep Last Value | On communication error, retain the last successfully read value |
| Set to Zero | On communication error, set all values to zero |

## IO Groups

IO Groups define what data to read or write from the remote device. Each IO group specifies:

- **Function Code**: The Modbus function to use
- **Offset**: The starting address on the remote device
- **Length**: Number of registers or coils to read/write
- **IEC Location**: The starting IEC address to map the data to
- **Cycle Time**: How often to poll this data (in milliseconds)

### Supported Function Codes

| Code | Name | Operation |
|------|------|-----------|
| FC 1 | Read Coils | Read digital outputs from remote device |
| FC 2 | Read Discrete Inputs | Read digital inputs from remote device |
| FC 3 | Read Holding Registers | Read analog outputs/data from remote device |
| FC 4 | Read Input Registers | Read analog inputs from remote device |
| FC 5 | Write Single Coil | Write a single digital output |
| FC 6 | Write Single Register | Write a single analog value |
| FC 15 | Write Multiple Coils | Write multiple digital outputs |
| FC 16 | Write Multiple Registers | Write multiple analog values |

## Adding an IO Group

1. In the remote device configuration, click **Add IO Group**
2. Configure the IO group settings:
   - Select the appropriate function code
   - Enter the starting offset (Modbus address)
   - Enter the number of registers/coils to read
   - Specify the IEC location to map the data
   - Set the polling cycle time
3. The IO group will appear in the device's IO group list

## Example Configuration

### Reading Temperature Sensors

To read 4 temperature values from a remote sensor module:

| Setting | Value |
|---------|-------|
| Host | 192.168.1.50 |
| Port | 502 |
| Function Code | FC 4 (Read Input Registers) |
| Offset | 0x0000 |
| Length | 4 |
| IEC Location | %IW100 |
| Cycle Time | 500 ms |

This configuration reads 4 input registers from the remote device every 500ms and maps them to %IW100 through %IW103 in your PLC program.

### Writing to a VFD

To control a variable frequency drive:

| Setting | Value |
|---------|-------|
| Host | 192.168.1.60 |
| Port | 502 |
| Function Code | FC 16 (Write Multiple Registers) |
| Offset | 0x0000 |
| Length | 2 |
| IEC Location | %QW200 |
| Cycle Time | 100 ms |

This configuration writes 2 holding registers to the VFD every 100ms, taking values from %QW200 and %QW201.

## Multiple Devices

You can add multiple remote devices to a single project. Each device operates independently with its own connection and polling schedule.

## Troubleshooting

### Communication Errors

1. Verify the remote device is powered and connected to the network
2. Check the IP address and port settings
3. Ensure the Modbus addresses are correct for your device
4. Increase the timeout value for slow networks

### Incorrect Data Values

1. Verify the function code matches what the remote device expects
2. Check the byte order (big-endian vs little-endian)
3. Ensure the data type interpretation is correct (signed vs unsigned)
4. Verify the offset addresses match the device documentation

### Polling Too Slow

1. Reduce the cycle time for critical data
2. Combine multiple reads into fewer IO groups where possible
3. Check network latency to the remote device
