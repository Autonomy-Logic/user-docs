# Board Selection

> **Desktop Editor Only**: Board selection for Arduino-compatible targets is only available in the desktop version of OpenPLC Editor. The web editor (Autonomy Edge) can only deploy to vPLC instances.

The Board Selection interface allows you to choose the target microcontroller board for your PLC program. The desktop editor supports over 60 different boards, ranging from simple Arduino microcontrollers to industrial PLCs.

![Board Selection Interface](images/board-selection.png)

## Selecting a Board

To select a target board:

1. Open your project in the desktop editor
2. Navigate to the **Device** section in the Project Explorer
3. Click on **Configuration**
4. In the Board dropdown, browse or search for your target board
5. Click on the board to select it

When you select a board, the editor displays:
- Board specifications (CPU, RAM, Flash memory)
- Available I/O capabilities (digital pins, analog pins, PWM)
- Connectivity options (WiFi, Bluetooth, Ethernet)
- A preview image of the board

![Board Specifications Panel](images/board-specs.png)

## Board Categories

### Arduino Official Boards

These are official Arduino boards with native support:

| Board | CPU | Key Features |
|-------|-----|--------------|
| Arduino Uno | ATmega 328P @ 16MHz | 14 digital, 6 analog pins |
| Arduino Uno R4 | Renesas RA4M1 @ 48MHz | 14 digital, 6 analog pins |
| Arduino Uno R4 WiFi | Renesas RA4M1 @ 48MHz | WiFi, Bluetooth |
| Arduino Mega | ATmega 2560 @ 16MHz | 70 digital, 16 analog pins |
| Arduino Due | ARM Cortex-M3 @ 84MHz | 54 digital, 12 analog pins |
| Arduino Leonardo | ATmega 32u4 @ 16MHz | USB HID support |
| Arduino Nano | ATmega 328P @ 16MHz | Compact form factor |
| Arduino Zero | ARM Cortex-M0+ @ 48MHz | 32-bit architecture |
| Arduino Giga | STM32H747 @ 480MHz | WiFi, Bluetooth, high performance |

### Arduino Industrial Boards

Professional-grade boards designed for industrial applications:

| Board | Description |
|-------|-------------|
| Arduino Opta | Industrial micro PLC with Ethernet |
| Portenta Machine Control | Industrial control with 8 digital I/O |
| Arduino Edge Control | Agricultural and environmental monitoring |
| Arduino MKR WiFi | Compact IoT board with WiFi |
| Arduino MKR Zero | Compact board with SD card support |

### ESP32 Family

WiFi and Bluetooth enabled microcontrollers:

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
| Bluepill STM32-F103CB | Cortex-M3 @ 72MHz | Multiple bootloader options |
| Blackpill STM32-F411CE | Cortex-M4 @ 100MHz | Higher performance |
| STM32-F446ZET (NUCLEO) | Cortex-M4 @ 180MHz | Full-featured development |

STM32 boards support multiple upload methods:
- **DFU Bootloader**: Built-in USB bootloader
- **HID Bootloader**: USB HID-based programming
- **SWD Programmer**: Debug probe (ST-Link)
- **Serial Programmer**: UART-based upload

### Raspberry Pi Pico Family

RP2040 and RP2350 based boards:

| Board | CPU | Features |
|-------|-----|----------|
| Raspberry Pico | RP2040 @ 133MHz | Dual Cortex-M0+ |
| Raspberry Pico 2 | RP2350 @ 150MHz | Cortex-M33 or RISC-V |
| Raspberry Pico W | RP2040 @ 133MHz | WiFi enabled |
| Nano RP2040 Connect | RP2040 @ 133MHz | WiFi, Bluetooth |

### Industrial PLC Boards

Purpose-built industrial automation hardware:

| Board | Features |
|-------|----------|
| CONTROLLINO MINI | ATmega328P, compact industrial PLC |
| CONTROLLINO MICRO | RP2040, Ethernet |
| CONTROLLINO MAXI | ATmega2560, Ethernet, expanded I/O |
| CONTROLLINO MAXI Automation | ATmega2560, industrial I/O |
| CONTROLLINO MEGA | ATmega2560, maximum I/O capacity |
| P1AM-100 | SAMD21, Productivity Open expansion |
| P1AM-200 | SAMD51, higher performance |
| FX3U-14M / LE3U-14M | STM32F103, Mitsubishi-style |
| FX3U-24MR / DollaTek | STM32F103, expanded I/O |

### OpenPLC Runtime Targets

For deployment to systems running the OpenPLC Runtime:

| Target | Use Case |
|--------|----------|
| OpenPLC Runtime v3 | Legacy runtime installations |
| OpenPLC Runtime v4 | Current runtime with Modbus support |

## First-Time Board Setup

When you select a board for the first time, the editor may need to download additional components:

1. **Arduino Core**: Platform-specific compilation tools
2. **Board Definitions**: Hardware configurations from board managers
3. **Libraries**: Required Arduino libraries for the board

![Core Installation](images/core-installation.png)

This download happens automatically during the first compilation. The editor displays progress and any errors that occur during installation.

## Changing Target Boards

You can change your target board at any time:

1. Select a new board from the board selection interface
2. Review and update the pin mapping (pins will be reset to defaults)
3. Verify communication settings are appropriate for the new board
4. Rebuild your project

When changing between Arduino targets, your PLC program code remains unchanged—only the hardware configuration needs updating.

When changing between Arduino targets and OpenPLC Runtime targets:
- Pin mapping is not applicable for Runtime targets
- Communication settings differ between target types
- Some features may only be available on specific target types

## Choosing the Right Board

Consider these factors when selecting a board:

| Requirement | Recommended Board |
|-------------|-------------------|
| Many I/O points | Arduino Mega, CONTROLLINO MEGA |
| WiFi connectivity | ESP32, ESP8266, Arduino Giga |
| Industrial environment | CONTROLLINO series, P1AM |
| Low cost | Arduino Uno, ESP32 |
| High performance | Arduino Due, STM32, Arduino Giga |
| Compact size | Arduino Nano, ESP8266 D1-mini |

> **Important**: For industrial production environments, always deploy to robust industrial-grade devices running OpenPLC Runtime v4 rather than Arduino development boards.

## Related Topics

- [Pin Mapping](pin-mapping.md) - Configure I/O pin assignments
- [Communication Settings](communication-settings.md) - Set up Modbus and networking
- [Supported Hardware Boards](../../reference/hardware-boards.md) - Complete board reference
