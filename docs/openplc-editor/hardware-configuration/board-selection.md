# Board Selection

> **Desktop Editor Only:** Board selection is available exclusively in the desktop version of OpenPLC Editor. If you're using the Autonomy Edge web IDE at [edge.autonomylogic.com](https://edge.autonomylogic.com), your programs deploy to runtime instances and you don't need to select a board. See [Connecting to Runtimes](../connecting-to-runtimes) instead.

The Board Selection interface lets you choose the target hardware for your PLC program. The desktop editor supports over 60 boards, ranging from basic Arduino microcontrollers to industrial PLCs and OpenPLC Runtime targets.

## Selecting a Board

To select a target board:

1. Open your project in the desktop editor.
2. Navigate to the **Device** section in the Project Explorer.
3. Click on **Configuration**.
4. In the Board dropdown, browse or search for your target board.
5. Click on the board to select it.

When you select a board, the editor displays its specifications:

| Specification | Description |
|---------------|-------------|
| **CPU** | Processor model and clock speed |
| **RAM** | Available memory |
| **Flash** | Program storage capacity |
| **Digital Pins** | Number of digital I/O pins |
| **Analog Pins** | Number of analog input/output pins |
| **Connectivity** | WiFi, Bluetooth, Ethernet availability |

## Compiler Types

Every board is assigned one of two compiler types. This determines how the editor builds and deploys your program.

### `arduino-cli` Compiler

Most boards use the `arduino-cli` compiler type. When this compiler is active:

- Your IEC 61131-3 program is compiled into firmware for the target board.
- The firmware is uploaded directly to the board via USB.
- **Pin Mapping** is enabled — you configure which physical pins map to IEC addresses.
- **Communication Settings** are enabled — you can configure Modbus RTU and Modbus TCP in the firmware.
- A serial port selection is available for choosing the USB upload port.

### `openplc_runtime` Compiler

OpenPLC Runtime targets (v3 and v4) use the `openplc_runtime` compiler type. When this compiler is active:

- The editor packages your program's source code and sends it to the runtime over the network.
- **Pin Mapping** is disabled — the runtime manages I/O through its own hardware abstraction.
- **Communication Settings** are disabled — Modbus and other protocols are configured through the runtime's web interface.
- **Port selection** is disabled — there's no USB connection.

## Board Categories

### Arduino Official Boards

Standard Arduino boards with native support:

| Board | CPU | Key Features |
|-------|-----|--------------|
| Arduino Uno | ATmega 328P @ 16 MHz | 14 digital, 6 analog pins |
| Arduino Uno R4 | Renesas RA4M1 @ 48 MHz | 14 digital, 6 analog pins |
| Arduino Uno R4 WiFi | Renesas RA4M1 @ 48 MHz | WiFi, Bluetooth |
| Arduino Mega | ATmega 2560 @ 16 MHz | 70 digital, 16 analog pins |
| Arduino Due | ARM Cortex-M3 @ 84 MHz | 54 digital, 12 analog pins |
| Arduino Leonardo | ATmega 32u4 @ 16 MHz | USB HID support |
| Arduino Nano | ATmega 328P @ 16 MHz | Compact form factor |
| Arduino Zero | ARM Cortex-M0+ @ 48 MHz | 32-bit architecture |
| Arduino Giga | STM32H747 @ 480 MHz | WiFi, Bluetooth, high performance |

### Arduino Industrial Boards

Professional-grade boards designed for industrial applications:

| Board | Description |
|-------|-------------|
| Arduino Opta | Industrial micro PLC with Ethernet |
| Portenta Machine Control | Industrial control with multiple I/O channels |
| Arduino Edge Control | Agricultural and environmental monitoring |
| Arduino MKR WiFi | Compact IoT board with WiFi |
| Arduino MKR Zero | Compact board with SD card support |

### ESP32 Family

WiFi and Bluetooth enabled microcontrollers from Espressif:

| Board | Key Features |
|-------|--------------|
| ESP32 Generic | Dual-core, WiFi, Bluetooth |
| ESP32 WROOM | Standard development board |
| ESP32 WROVER | Extended PSRAM |
| ESP32-S2 | Single-core, USB OTG |
| ESP32-S3 | Dual-core, AI acceleration |
| ESP32-C3 | RISC-V core, WiFi |
| ESP32-C6 | WiFi 6, Thread/Zigbee |
| ESP8266 NodeMCU | WiFi, compact |
| ESP8266 D1-mini | WiFi, minimal form factor |

### STM32 Boards

ARM Cortex-M based development boards:

| Board | CPU | Notes |
|-------|-----|-------|
| Bluepill STM32-F103CB | Cortex-M3 @ 72 MHz | Multiple bootloader options |
| Blackpill STM32-F411CE | Cortex-M4 @ 100 MHz | Higher performance |
| STM32-F446ZET (NUCLEO) | Cortex-M4 @ 180 MHz | Full-featured development board |

STM32 boards support multiple upload methods:

| Upload Method | Description |
|---------------|-------------|
| DFU Bootloader | Built-in USB bootloader |
| HID Bootloader | USB HID-based programming |
| SWD Programmer | Debug probe (ST-Link) |
| Serial Programmer | UART-based upload |

### Raspberry Pi Pico Family

RP2040 and RP2350 based boards:

| Board | CPU | Features |
|-------|-----|----------|
| Raspberry Pico | RP2040 @ 133 MHz | Dual Cortex-M0+ |
| Raspberry Pico 2 | RP2350 @ 150 MHz | Cortex-M33 or RISC-V |
| Raspberry Pico W | RP2040 @ 133 MHz | WiFi enabled |
| Nano RP2040 Connect | RP2040 @ 133 MHz | WiFi, Bluetooth |

### Industrial PLC Boards

Purpose-built industrial automation hardware:

| Board | Features |
|-------|----------|
| CONTROLLINO MINI | ATmega328P, compact industrial PLC |
| CONTROLLINO MICRO | RP2040, Ethernet |
| CONTROLLINO MAXI | ATmega2560, Ethernet, expanded I/O |
| CONTROLLINO MAXI Automation | ATmega2560, industrial I/O |
| CONTROLLINO MEGA | ATmega2560, maximum I/O capacity |
| P1AM-100 | SAMD21, Productivity Open expansion modules |
| P1AM-200 | SAMD51, higher performance |
| FX3U-14M / LE3U-14M | STM32F103, Mitsubishi-style form factor |
| FX3U-24MR / DollaTek | STM32F103, expanded I/O |

### OpenPLC Runtime Targets

For deployment to systems running the OpenPLC Runtime software:

| Target | Compiler Type | Use Case |
|--------|---------------|----------|
| OpenPLC Runtime v3 | `openplc_runtime` | Legacy runtime installations |
| OpenPLC Runtime v4 | `openplc_runtime` | Current runtime with full Modbus and protocol support |

These targets don't use arduino-cli. Pin mapping and embedded communication settings are not applicable.

## First-Time Board Setup

When you select an Arduino-compatible board for the first time, the editor may need to download additional components before building can succeed:

| Component | Purpose |
|-----------|---------|
| **Arduino Core** | Platform-specific tools and board definitions |
| **Board Definitions** | Hardware configurations from Arduino board manager URLs |
| **Libraries** | Required Arduino libraries for the board's HAL |

This download happens automatically during the first build. The editor displays progress in the console and reports any errors.

## Changing Target Boards

You can change your target board at any time:

1. Select a new board from the Board dropdown.
2. Review the pin mapping — pins are reset to the new board's defaults.
3. Verify that communication settings are appropriate for the new board's capabilities.
4. Rebuild your project.

When switching between Arduino-compatible boards, your PLC program code remains unchanged. Only the hardware configuration (pin mapping and communication settings) needs updating.

When switching between an Arduino target and an OpenPLC Runtime target:

- Pin mapping becomes disabled (or re-enabled, depending on direction).
- Communication settings switch between embedded firmware configuration and runtime-managed configuration.
- Your PLC program logic is preserved.

## Choosing the Right Board

| Requirement | Recommended Board |
|-------------|-------------------|
| Many I/O points | Arduino Mega, CONTROLLINO MEGA |
| WiFi connectivity | ESP32, ESP8266, Arduino Giga |
| Industrial environment | CONTROLLINO series, P1AM, Arduino Opta |
| Low cost / prototyping | Arduino Uno, ESP32 |
| High performance | Arduino Due, STM32, Arduino Giga |
| Compact size | Arduino Nano, ESP8266 D1-mini |

> **Tip:** For industrial production environments, deploy to robust industrial-grade devices running OpenPLC Runtime v4 rather than Arduino development boards. Development boards are excellent for prototyping but are not rated for continuous industrial operation.

## What's Next?

- [Pin Mapping](pin-mapping) — Configure I/O pin assignments for your selected board
- [Communication Settings](communication-settings) — Set up Modbus RTU and TCP for microcontroller firmware
- [Device Configuration Overview](device-config-overview) — Understand the full range of target types
