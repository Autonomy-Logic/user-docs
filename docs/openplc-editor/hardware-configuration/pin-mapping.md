# Pin Mapping

> **Desktop Editor Only**: Pin mapping for Arduino-compatible targets is only available in the desktop version of OpenPLC Editor. The web editor (Autonomy Edge) deploys only to vPLC instances where I/O is handled by the runtime.

Pin mapping connects IEC 61131-3 I/O addresses in your PLC program to physical hardware pins on your target microcontroller. This configuration determines how your program interacts with the real world.

![Pin Mapping Interface](images/pin-mapping-overview.png)

## Understanding Pin Mapping

When you declare a variable with a hardware address in your PLC program, such as:

```iecst
VAR
    StartButton AT %IX0.0 : BOOL;    (* Digital input *)
    MotorRunning AT %QX0.0 : BOOL;   (* Digital output *)
    Temperature AT %IW0 : INT;        (* Analog input *)
    SpeedSetpoint AT %QW0 : INT;      (* Analog output *)
END_VAR
```

The pin mapping configuration tells the runtime which physical pins on your microcontroller correspond to these addresses.

## Accessing the Pin Mapping Interface

1. Open your project in the desktop editor
2. Navigate to **Device** in the Project Explorer
3. Select your target board (Arduino-compatible boards only)
4. The pin mapping table appears in the configuration panel

The interface displays four categories of pins:
- **Digital Inputs** - For reading digital signals (switches, sensors)
- **Digital Outputs** - For controlling digital signals (relays, LEDs)
- **Analog Inputs** - For reading analog signals (temperature sensors, potentiometers)
- **Analog Outputs** - For PWM or DAC outputs

![Pin Mapping Table](images/pin-mapping-table.png)

## Adding Pin Mappings

Unlike older versions of OpenPLC, you add only the pins your application needs:

1. In the pin mapping section, click to add a new pin
2. Select the pin type (Digital Input, Digital Output, Analog Input, or Analog Output)
3. Choose the physical pin from the dropdown (suggestions based on your board)
4. The editor automatically assigns the next available IEC address
5. Optionally, add a descriptive name for the pin

![Adding a Pin](images/pin-add.png)

### Custom Pin Names

You can enter custom pin names that aren't in the suggestion list. This is useful for:
- Boards with non-standard pin naming
- Using alternate pin functions
- Custom hardware configurations

## IEC Address Format

### Digital Addresses

Digital I/O uses bit-addressed format with 8 bits per bank:

| Address | Description |
|---------|-------------|
| `%IX0.0` - `%IX0.7` | First 8 digital inputs (bank 0) |
| `%IX1.0` - `%IX1.7` | Next 8 digital inputs (bank 1) |
| `%QX0.0` - `%QX0.7` | First 8 digital outputs (bank 0) |
| `%QX1.0` - `%QX1.7` | Next 8 digital outputs (bank 1) |

### Analog Addresses

Analog I/O uses word-addressed format:

| Address | Description |
|---------|-------------|
| `%IW0`, `%IW1`, `%IW2`... | Analog inputs |
| `%QW0`, `%QW1`, `%QW2`... | Analog outputs |

## Connecting Variables to Pins

After configuring your pin mapping, connect your program variables to pins:

1. In your POU's variable table, click on the **Location** field
2. Select one of the pins you defined in the pin mapping
3. The variable is now linked to that physical pin

![Variable Location Selection](images/variable-location.png)

This approach separates the hardware configuration from your program logic, making it easy to:
- Port programs to different hardware
- Change pin assignments without modifying code
- Reuse programs across projects

## Board-Specific Considerations

### Standard Arduino Boards (Uno, Nano, Leonardo)

- Limited number of pins available
- Analog outputs use PWM (8-bit resolution)
- Some pins have dual functions (SPI, I2C)
- Pins 0 and 1 typically used for serial communication

### Arduino Mega / Due

- Extended I/O capacity (54+ digital pins)
- More analog inputs (12-16 channels)
- Due has true DAC outputs on pins DAC0/DAC1

### ESP32 Boards

- More flexible pin assignments
- Most GPIO pins can be configured as input or output
- Analog outputs use LEDC PWM peripheral
- Some pins have restrictions (GPIO 6-11 typically unavailable)

### STM32 Boards

- Pin names use port notation (PA0, PB3, PC13)
- Wide range of configurable alternate functions
- Higher resolution ADC/DAC available on some models

### Industrial Boards (CONTROLLINO, P1AM)

- Fixed I/O assignments based on terminal blocks
- Pin names match physical terminal labels
- Pre-configured for industrial voltage levels

## How Pin Mapping Works Internally

When you compile your project for an Arduino target, the editor generates a `defines.h` file containing C preprocessor macros:

```c
// Generated pin masks
#define PINMASK_DIN 2, 3, 4, 5
#define PINMASK_DOUT 7, 8, 12, 13
#define PINMASK_AIN A0, A1, A2
#define PINMASK_AOUT 9, 10, 11

// I/O counts
#define NUM_DISCRETE_INPUT 4
#define NUM_DISCRETE_OUTPUT 4
#define NUM_ANALOG_INPUT 3
#define NUM_ANALOG_OUTPUT 3
```

The board's Hardware Abstraction Layer (HAL) uses these definitions to configure the I/O during initialization.

## Best Practices

### Start with a Simple Test

Before building your full application:
1. Add one digital output (like pin 13 with built-in LED)
2. Create a simple blink program
3. Verify the upload and execution works
4. Then expand to your full pin configuration

### Document Your Mappings

Use meaningful pin names that indicate the physical connection:
- `StartButton` instead of just `Pin2`
- `MotorRelay` instead of `Output1`

### Consider Electrical Characteristics

- Use PWM-capable pins for analog outputs
- Consider current limits when driving loads directly
- Use appropriate pull-up/pull-down for inputs

### Plan for Expansion

- Leave room for additional I/O if your application might grow
- Document which addresses are available for future use

## Troubleshooting

### Pin Not Responding

1. Verify the pin is correctly mapped in the configuration
2. Check that your variable has the correct location assigned
3. Ensure no conflicts with other pin functions (SPI, I2C, Serial)

### Analog Values Incorrect

1. Verify the pin supports analog input (ADC-capable)
2. Check voltage levels are within the board's range
3. Consider adding filtering for noisy signals

### Upload Succeeds but I/O Doesn't Work

1. Double-check physical wiring matches pin configuration
2. Verify the correct board is selected
3. Test with a simple program to isolate the issue

## Related Topics

- [Device Configuration Overview](device-config-overview.md) - Understanding target types
- [Board Selection](board-selection.md) - Choosing your target hardware
- [Communication Settings](communication-settings.md) - Configuring Modbus
- [Global Variables](../working-with-variables/global-variables.md) - Declaring I/O variables
