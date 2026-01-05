# Hardware Configuration

This section covers hardware configuration for OpenPLC Runtime, including pin mapping for various platforms.

## Overview

OpenPLC Runtime can run on various hardware platforms, from standard PCs to embedded systems and microcontrollers. Each platform has different I/O capabilities that need to be configured.

## Hardware Platforms

### Linux PCs and Servers

When running on standard Linux systems, OpenPLC typically uses:

- **Modbus I/O**: Connect to remote I/O modules via Modbus TCP
- **GPIO**: On systems with GPIO (like Raspberry Pi)
- **Industrial I/O cards**: PCIe or USB-based I/O cards

### Raspberry Pi

The Raspberry Pi's GPIO pins can be mapped to IEC addresses:

- Digital inputs and outputs via GPIO pins
- Analog I/O requires additional hardware (ADC/DAC)

### Industrial Edge Devices

Many industrial edge devices running Linux can host OpenPLC Runtime:

- Siemens IOT2050
- Opto 22 groov EPIC/RIO
- WAGO PFC200
- Phoenix Contact PLCnext
- And many others

### Microcontrollers

For microcontroller targets (programmed via desktop editor), see the [Microcontrollers](../openplc-editor/microcontrollers/) section.

## Pin Mapping in v4

In OpenPLC Editor v4, pin mapping is configured directly in the editor:

1. Navigate to Hardware Configuration in your project
2. Add pins that your application needs
3. Map each pin to an IEC address
4. The editor provides suggestions based on your target platform

Unlike v3, there is no fixed pin list - you configure only the pins you need.

## In This Section

- **[Overview](overview.md)**: General hardware configuration concepts
- **[Raspberry Pi](raspberry-pi.md)**: GPIO configuration for Raspberry Pi
- **[Industrial Devices](industrial-devices.md)**: Configuration for industrial hardware

## Hardware Abstraction

OpenPLC uses a Hardware Abstraction Layer (HAL) to support different platforms. The HAL:

- Maps IEC addresses to physical pins
- Handles platform-specific I/O operations
- Provides a consistent interface for the PLC program

This allows the same PLC program to run on different hardware with only configuration changes.
