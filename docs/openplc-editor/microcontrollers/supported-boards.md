# Supported Boards

OpenPLC Editor supports a wide variety of microcontroller boards. This page lists the compatible boards and their capabilities.

> **Note**: This feature is only available in the desktop version of OpenPLC Editor.

## Arduino Family

### Arduino Uno
- **Processor**: ATmega328P
- **Digital I/O**: 14 pins (6 PWM)
- **Analog Inputs**: 6 pins
- **Best For**: Learning, simple projects

### Arduino Mega
- **Processor**: ATmega2560
- **Digital I/O**: 54 pins (15 PWM)
- **Analog Inputs**: 16 pins
- **Best For**: Projects requiring many I/O points

### Arduino Due
- **Processor**: ARM Cortex-M3
- **Digital I/O**: 54 pins (12 PWM)
- **Analog Inputs**: 12 pins
- **Best For**: High-performance applications

### Arduino Nano
- **Processor**: ATmega328P
- **Digital I/O**: 14 pins (6 PWM)
- **Analog Inputs**: 8 pins
- **Best For**: Compact projects

### Arduino Leonardo
- **Processor**: ATmega32U4
- **Digital I/O**: 20 pins (7 PWM)
- **Analog Inputs**: 12 pins
- **Best For**: USB HID applications

### Arduino MKR Family
- Various MKR boards with WiFi, GSM, and other connectivity options

## ESP Family

### ESP32
- **Processor**: Dual-core Xtensa LX6
- **Digital I/O**: Up to 34 GPIO
- **Analog Inputs**: Up to 18 channels
- **WiFi**: Built-in
- **Best For**: IoT and connected applications

### ESP8266
- **Processor**: Single-core Xtensa L106
- **Digital I/O**: Up to 17 GPIO
- **Analog Inputs**: 1 channel
- **WiFi**: Built-in
- **Best For**: Simple IoT projects

## STM32 Family

### STM32 Blue Pill
- **Processor**: ARM Cortex-M3
- **Digital I/O**: 37 GPIO
- **Analog Inputs**: 10 channels
- **Best For**: Cost-effective ARM development

### STM32 Black Pill
- **Processor**: ARM Cortex-M4
- **Digital I/O**: Various
- **Analog Inputs**: Multiple channels
- **Best For**: Higher performance applications

### STM32 Nucleo Boards
- Various Nucleo development boards with different STM32 processors

## Industrial Boards

### Controllino Maxi
- **Based On**: ATmega2560
- **Digital Inputs**: 12
- **Digital Outputs**: 12 (relay)
- **Analog Inputs**: 10
- **Best For**: Industrial applications

### Controllino Mega
- **Based On**: ATmega2560
- **Digital Inputs**: 21
- **Digital Outputs**: 24 (relay + MOSFET)
- **Analog Inputs**: 18
- **Best For**: Large industrial projects

### Controllino Mini
- **Based On**: ATmega328P
- **Digital Inputs**: 8
- **Digital Outputs**: 8
- **Analog Inputs**: 6
- **Best For**: Small industrial applications

## Other Boards

### Raspberry Pi Pico
- **Processor**: RP2040 (Dual-core ARM Cortex-M0+)
- **Digital I/O**: 26 GPIO
- **Analog Inputs**: 3 channels
- **Best For**: Affordable ARM development

## Pin Mapping

In OpenPLC Editor v4, pin mappings are configured in the editor rather than using a fixed list. The editor provides pin name suggestions based on your selected board through the `hals.json` configuration file.

To configure pins:
1. Select your target board in Hardware Configuration
2. Add pins using the pin mapping interface
3. The editor suggests valid pin names for your board
4. Map each pin to an IEC address

## Choosing a Board

Consider these factors when selecting a board:

| Factor | Recommendation |
|--------|----------------|
| Many I/O points | Arduino Mega, Controllino Mega |
| WiFi connectivity | ESP32, ESP8266 |
| Industrial environment | Controllino series |
| Low cost | Arduino Uno, ESP32 |
| High performance | Arduino Due, STM32 |
| Compact size | Arduino Nano, ESP8266 |
