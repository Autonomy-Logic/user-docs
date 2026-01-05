# Hardware Overview

This page provides an overview of hardware configuration concepts in OpenPLC Runtime.

## Hardware Abstraction Layer (HAL)

OpenPLC uses a Hardware Abstraction Layer to interface with physical I/O. The HAL:

- Translates IEC addresses to physical hardware operations
- Supports multiple hardware platforms
- Allows the same PLC program to run on different hardware

## I/O Types

### Digital Inputs

Digital inputs read binary (on/off) signals from:

- Push buttons and switches
- Proximity sensors
- Limit switches
- Digital sensors

Mapped to: `%IX` addresses (e.g., %IX0.0, %IX0.1)

### Digital Outputs

Digital outputs control binary devices:

- Relays and contactors
- Indicator lights
- Solenoid valves
- Motor starters

Mapped to: `%QX` addresses (e.g., %QX0.0, %QX0.1)

### Analog Inputs

Analog inputs read continuous values from:

- Temperature sensors
- Pressure transducers
- Flow meters
- Level sensors

Mapped to: `%IW` addresses (e.g., %IW0, %IW1)

### Analog Outputs

Analog outputs control variable devices:

- Variable frequency drives
- Proportional valves
- Analog meters
- Dimmer controls

Mapped to: `%QW` addresses (e.g., %QW0, %QW1)

## Configuration Methods

### Direct GPIO

On platforms with GPIO (like Raspberry Pi), pins can be directly mapped to IEC addresses.

### Modbus I/O

Remote I/O modules connected via Modbus TCP provide:

- Distributed I/O across a network
- Industrial-grade isolation
- Easy expansion

### Plugin-Based I/O

Custom plugins can interface with:

- Specialized hardware
- Industrial protocols
- Custom I/O cards

## Pin Mapping in OpenPLC Editor v4

In v4, pin mapping is done in the editor:

1. Open your project in OpenPLC Editor
2. Navigate to Hardware Configuration
3. Add pins for your target hardware
4. Assign IEC addresses to each pin

The editor provides pin name suggestions based on your selected platform through the `hals.json` configuration.

## Best Practices

### Plan Your I/O Layout

Before configuring hardware:

1. List all required inputs and outputs
2. Group related I/O logically
3. Reserve addresses for future expansion
4. Document your address assignments

### Use Meaningful Names

Always use descriptive variable names:

```
StartButton AT %IX0.0 : BOOL;  (* Good *)
I0_0 AT %IX0.0 : BOOL;         (* Avoid *)
```

### Consider Electrical Requirements

When selecting hardware:

- Match voltage levels (24V DC is common in industrial)
- Consider isolation requirements
- Plan for surge protection
- Account for cable lengths
