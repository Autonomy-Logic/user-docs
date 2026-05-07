# Pin Mapping

> **Desktop Editor Only:** Pin mapping is available exclusively in the desktop version of OpenPLC Editor for Arduino-compatible targets. If you're using the Autonomy Edge web IDE at [edge.autonomylogic.com](https://edge.autonomylogic.com), your programs deploy to runtime instances where I/O is managed by the runtime's hardware abstraction layer. See [Connecting to Runtimes](../connecting-to-runtimes) instead.

Pin mapping connects IEC 61131-3 I/O addresses in your PLC program to physical hardware pins on your target microcontroller. When you declare a variable like `StartButton AT %IX0.0 : BOOL`, the pin mapping configuration tells the firmware which GPIO pin to read for that address.

## How Pin Mapping Works

In your PLC program, you reference hardware I/O through standard IEC addresses:

```iecst
VAR
    StartButton AT %IX0.0 : BOOL;    (* Digital input *)
    MotorRunning AT %QX0.0 : BOOL;   (* Digital output *)
    Temperature AT %IW0 : INT;        (* Analog input *)
    SpeedSetpoint AT %QW0 : INT;      (* Analog output *)
END_VAR
```

The pin mapping table in the Device Configuration panel defines which physical pin on your microcontroller corresponds to each address. During the build, a `defines.h` file is generated that the firmware's Hardware Abstraction Layer (HAL) uses to initialize I/O.

## Accessing the Pin Mapping Interface

1. Open your project in the desktop editor.
2. Navigate to **Device** in the Project Explorer.
3. Select an Arduino-compatible board (pin mapping is disabled for OpenPLC Runtime targets).
4. The pin mapping table appears in the configuration panel, organized into four sections.

## Pin Types

| Pin Type | IEC Prefix | Purpose | Example Hardware |
|----------|------------|---------|------------------|
| **Digital Input** | `%IX` | Read digital signals | Switches, proximity sensors, limit switches |
| **Digital Output** | `%QX` | Control digital signals | Relays, solenoids, indicator LEDs |
| **Analog Input** | `%IW` | Read analog signals | Temperature sensors, potentiometers, pressure transducers |
| **Analog Output** | `%QW` | PWM or DAC output | Motor speed control, valve positioning |

## IEC Address Format

### Digital Addresses

Digital I/O uses a bit-addressed format organized into banks of 8 bits:

| Address Range | Description |
|---------------|-------------|
| `%IX0.0` through `%IX0.7` | First 8 digital inputs (bank 0) |
| `%IX1.0` through `%IX1.7` | Next 8 digital inputs (bank 1) |
| `%IX2.0` through `%IX2.7` | Next 8 digital inputs (bank 2) |
| `%QX0.0` through `%QX0.7` | First 8 digital outputs (bank 0) |
| `%QX1.0` through `%QX1.7` | Next 8 digital outputs (bank 1) |

The format is `%IX[byte].[bit]` for inputs and `%QX[byte].[bit]` for outputs, where `byte` is the bank number (starting at 0) and `bit` is the position within the bank (0 through 7).

### Analog Addresses

Analog I/O uses a sequential word-addressed format:

| Address | Description |
|---------|-------------|
| `%IW0`, `%IW1`, `%IW2`, ... | Analog inputs (sequential) |
| `%QW0`, `%QW1`, `%QW2`, ... | Analog outputs (sequential) |

Each analog address represents a 16-bit integer value.

## Adding Pin Mappings

The editor uses an on-demand approach. You add only the pins your application needs rather than configuring the entire board.

To add a new pin:

1. In the pin mapping section, click the add button for the desired pin type (Digital Input, Digital Output, Analog Input, or Analog Output).
2. A new row appears in the table.
3. Select the physical pin from the dropdown.
4. The editor automatically assigns the next available IEC address.

### Smart Defaults

When you open the pin dropdown, the editor presents a filtered list of board-specific default pins:

- **Board-aware suggestions**: Only pins valid for the selected pin type on your specific board are shown. For example, analog input pins are limited to ADC-capable GPIO pins.
- **Already-used filtering**: Pins already assigned to another mapping are excluded from the dropdown, preventing accidental double-assignment.
- **Auto-address assignment**: The editor assigns the next available IEC address in sequence. If `%IX0.0` and `%IX0.1` are taken, the next digital input gets `%IX0.2`.

### Custom Pin Names

You can type a custom pin name into the dropdown's text field instead of selecting from the suggestion list. This is useful for:

- Boards with non-standard pin naming conventions
- Using alternate pin functions not listed in the defaults
- Custom hardware configurations with external I/O expanders

## Removing Pin Mappings

To remove a pin mapping, click the delete button on the corresponding row. The IEC address is freed and becomes available for future assignments. Removing a pin does not automatically renumber the remaining addresses.

## Connecting Variables to Pins

After configuring your pin mappings, link program variables to the mapped addresses:

1. In your POU's variable table, click on the **Location** field for a variable.
2. Select one of the addresses you defined in the pin mapping (e.g., `%IX0.0`).
3. The variable is now bound to that physical pin at runtime.

This separation of hardware configuration from program logic means you can:

- Port programs to different hardware by changing only the pin mapping.
- Reassign pins without modifying any PLC code.
- Reuse the same program across multiple projects with different boards.

## Generated Output: `defines.h`

When you build your project for an Arduino-compatible target, the editor generates a `defines.h` file from your pin mapping. This file contains C preprocessor macros that the board's HAL reads during initialization:

```c
// Pin masks. List of physical pins for each I/O type
#define PINMASK_DIN  2, 3, 4, 5
#define PINMASK_DOUT 7, 8, 12, 13
#define PINMASK_AIN  A0, A1, A2
#define PINMASK_AOUT 9, 10, 11

// I/O counts
#define NUM_DISCRETE_INPUT  4
#define NUM_DISCRETE_OUTPUT 4
#define NUM_ANALOG_INPUT    3
#define NUM_ANALOG_OUTPUT   3
```

The order of pins in each `PINMASK_*` macro corresponds directly to the IEC address order. For example, `PINMASK_DIN 2, 3, 4, 5` means:

| IEC Address | Physical Pin |
|-------------|--------------|
| `%IX0.0` | Pin 2 |
| `%IX0.1` | Pin 3 |
| `%IX0.2` | Pin 4 |
| `%IX0.3` | Pin 5 |

## Board-Specific Considerations

### Standard Arduino Boards (Uno, Nano, Leonardo)

- Limited pin count; plan your I/O allocation carefully.
- Analog outputs use PWM (8-bit resolution) on specific PWM-capable pins.
- Pins 0 and 1 are typically reserved for serial communication. Avoid mapping them unless you don't need Serial.
- Some pins are shared with SPI or I2C; check for conflicts if using those peripherals.

### Arduino Mega / Due

- Extended I/O capacity with 54+ digital pins and 12–16 analog inputs.
- Arduino Due has true DAC outputs on pins DAC0 and DAC1 (12-bit resolution).
- Larger pin count means more flexibility but also more potential for wiring errors.

### ESP32 Boards

- Most GPIO pins can be configured as either input or output.
- Analog outputs use the LEDC PWM peripheral.
- GPIO 6 through 11 are typically unavailable (connected to internal flash).
- WiFi operation may interfere with certain ADC channels on some variants.

### STM32 Boards

- Pin names use port notation (e.g., PA0, PB3, PC13).
- Wide range of alternate functions per pin.
- Higher-resolution ADC and DAC available on some models (12-bit or 16-bit).

### Industrial Boards (CONTROLLINO, P1AM)

- Fixed I/O assignments that match physical terminal block labels.
- Pin names in the editor correspond directly to the labels printed on the device.
- Pre-configured for industrial voltage levels (24V digital I/O on some models).

## Best Practices

**Start simple.** Before building your full application, add one digital output (such as pin 13, which has a built-in LED on most Arduino boards), create a simple blink program, and verify that upload and execution work correctly.

**Use meaningful names.** When you assign variables to pin locations, use descriptive names like `StartButton` or `MotorRelay` rather than generic labels like `Pin2` or `Output1`.

**Match pin capabilities to usage.** Use PWM-capable pins for analog outputs. Use ADC-capable pins for analog inputs. Check the board's datasheet if the dropdown suggestions seem limited.

**Plan for expansion.** Leave room for additional I/O points if your application may grow. Document which addresses and pins are still available.

## Troubleshooting

### Pin not responding

1. Verify the pin is correctly mapped in the Device Configuration.
2. Check that your program variable has the correct `AT %` location assigned.
3. Ensure the pin is not conflicting with another peripheral (SPI, I2C, Serial).

### Analog values incorrect

1. Confirm the pin is ADC-capable (listed in the analog input defaults for your board).
2. Check that voltage levels are within the board's ADC input range.
3. Consider adding filtering in your PLC logic for noisy analog signals.

### Upload succeeds but I/O does not work

1. Double-check that physical wiring matches the pin mapping configuration.
2. Verify the correct board is selected in Board Selection.
3. Test with a minimal program to isolate whether the issue is in wiring or logic.

## What's Next?

- [Board Selection](board-selection): Choose your target microcontroller board
- [Communication Settings](communication-settings): Configure Modbus RTU and TCP for microcontroller firmware
- [Device Configuration Overview](device-config-overview): Understand all target types and deployment workflows
- [Global Variables](../working-with-variables/global-variables): Declare I/O variables in your PLC program
