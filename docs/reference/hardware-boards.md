# Supported Hardware Boards

> **Desktop Editor Only**: Direct programming of Arduino-compatible boards is only available in the desktop version of OpenPLC Editor.

This reference documents all hardware boards supported by OpenPLC Editor for direct microcontroller programming. The editor supports over 60 different boards across multiple microcontroller families and architectures.

## Board Types

The editor supports two categories of deployment targets:

- **Arduino-Compatible Targets**: Microcontroller boards that receive compiled firmware via USB
- **OpenPLC Runtime Targets**: Linux-based systems or vPLCs running OpenPLC Runtime

## Arduino Official Boards

### Arduino AVR Family

| Board | CPU | RAM | Flash | Digital | Analog |
|-------|-----|-----|-------|---------|--------|
| Arduino Uno | ATmega 328P @ 16MHz | 2 KB | 32 KB | 14 | 6 |
| Arduino Leonardo | ATmega 32u4 @ 16MHz | 2.5 KB | 32 KB | 20 | 12 |
| Arduino Mega | ATmega 2560 @ 16MHz | 8 KB | 256 KB | 70 | 16 |
| Arduino Nano | ATmega 328P @ 16MHz | 2 KB | 32 KB | 22 | 8 |
| Arduino Micro | ATmega 32u4 @ 16MHz | 2.5 KB | 32 KB | 20 | 12 |

### Arduino Renesas Family

| Board | CPU | RAM | Flash | Connectivity |
|-------|-----|-----|-------|--------------|
| Arduino Uno R4 | Renesas RA4M1 @ 48MHz | 32 KB | 256 KB | - |
| Arduino Uno R4 WiFi | Renesas RA4M1 @ 48MHz | 32 KB | 256 KB | WiFi, BT |

### Arduino ARM Family

| Board | CPU | RAM | Flash |
|-------|-----|-----|-------|
| Arduino Due (native USB) | SAM3X8E @ 84MHz | 96 KB | 512 KB |
| Arduino Due (programming) | SAM3X8E @ 84MHz | 96 KB | 512 KB |
| Arduino Zero (native USB) | SAMD21G18 @ 48MHz | 32 KB | 256 KB |
| Arduino Zero (programming) | SAMD21G18 @ 48MHz | 32 KB | 256 KB |

### Arduino MegaAVR Family

| Board | CPU | RAM | Flash |
|-------|-----|-----|-------|
| Nano Every | ATmega4809 @ 20MHz | 6 KB | 48 KB |

### Arduino SAMD Family

| Board | CPU | RAM | Flash | Connectivity |
|-------|-----|-----|-------|--------------|
| MKR Zero | SAMD21 @ 48MHz | 32 KB | 256 KB | - |
| MKR WiFi | SAMD21 @ 48MHz | 32 KB | 256 KB | WiFi |
| Nano 33 IoT | SAMD21 @ 48MHz | 32 KB | 256 KB | WiFi |

### Arduino Mbed Family

| Board | CPU | RAM | Flash | Connectivity |
|-------|-----|-----|-------|--------------|
| Nano 33 BLE | nRF52840 @ 64MHz | 256 KB | 1 MB | BT |
| Nano RP2040 Connect | RP2040 @ 133MHz | 264 KB | 16 MB | WiFi, BT |

### Arduino High-Performance

| Board | CPU | RAM | Flash | Connectivity |
|-------|-----|-----|-------|--------------|
| Arduino Giga | STM32H747 @ 480MHz | 1 MB | 2 MB | WiFi, BT |

## Arduino Industrial Boards

| Board | CPU | Features |
|-------|-----|----------|
| Arduino Opta | STM32H747 @ 480MHz | Ethernet, industrial I/O |
| Portenta Machine Control H7 | STM32H747 @ 480MHz | 8 digital I/O, 3 analog |
| Arduino Edge Control | nRF52840 @ 64MHz | Agricultural monitoring |

## ESP32 Family

| Board | RAM | Flash | Connectivity |
|-------|-----|-------|--------------|
| ESP32 Generic | 520 KB | 4 MB | WiFi, BT |
| ESP32 WROOM | 520 KB | 4 MB | WiFi, BT |
| ESP32 WROVER | 520 KB | 4 MB | WiFi, BT |
| ESP32-DOIT DEVKIT V1 | 520 KB | 4 MB | WiFi, BT |
| ESP32-S2 | 320 KB | 4 MB | WiFi |
| ESP32-S3 | 512 KB | 4 MB | WiFi, BT |
| ESP32-C3 | 400 KB | 4 MB | WiFi |
| ESP32-C6 DevKitC-1 V1.2 | 400 KB | 4 MB | WiFi |
| Arduino Nano ESP32 | 520 KB | 4 MB | WiFi, BT |

## ESP8266 Family

| Board | RAM | Flash | Connectivity |
|-------|-----|-------|--------------|
| ESP8266 NodeMCU | 80 KB | 4 MB | WiFi |
| ESP8266 D1-mini | 80 KB | 4 MB | WiFi |

## STM32 Boards

### Bluepill (STM32F103)

| Board | CPU | Upload Method |
|-------|-----|---------------|
| Bluepill STM32-F103CB (DFU) | Cortex-M3 @ 72MHz | DFU Bootloader |
| Bluepill STM32-F103CB (HID) | Cortex-M3 @ 72MHz | HID Bootloader |
| Bluepill STM32-F103CB (SWD) | Cortex-M3 @ 72MHz | SWD Programmer |
| Bluepill STM32-F103CB (Serial) | Cortex-M3 @ 72MHz | Serial Programmer |

### Blackpill (STM32F411)

| Board | CPU | Upload Method |
|-------|-----|---------------|
| Blackpill STM32-F411CE (DFU) | Cortex-M4 @ 100MHz | DFU Bootloader |
| Blackpill STM32-F411CE (HID) | Cortex-M4 @ 100MHz | HID Bootloader |
| Blackpill STM32-F411CE (SWD) | Cortex-M4 @ 100MHz | SWD Programmer |
| Blackpill STM32-F411CE (Serial) | Cortex-M4 @ 100MHz | Serial Programmer |

### STM32 NUCLEO

| Board | CPU | Features |
|-------|-----|----------|
| STM32-F446ZET (NUCLEO) | Cortex-M4 @ 180MHz | Full-featured devboard |

## Raspberry Pi Pico Family

| Board | CPU | RAM | Connectivity |
|-------|-----|-----|--------------|
| Raspberry Pico | RP2040 @ 133MHz | 264 KB | - |
| Raspberry Pico 2 | RP2350 @ 150MHz | 520 KB | - |
| Raspberry Pico 2 (RISCV) | RP2350 @ 150MHz | 520 KB | - |
| Raspberry Pico W | RP2040 @ 133MHz | 264 KB | WiFi |

## CONTROLLINO Industrial PLCs

| Board | CPU | Features |
|-------|-----|----------|
| CONTROLLINO MINI | ATmega 328P @ 16MHz | Compact industrial PLC |
| CONTROLLINO MICRO | RP2040 @ 133MHz | Ethernet |
| CONTROLLINO MAXI | ATmega 2560 @ 16MHz | Ethernet, expanded I/O |
| CONTROLLINO MAXI Automation | ATmega 2560 @ 16MHz | Industrial I/O, Ethernet |
| CONTROLLINO MEGA | ATmega 2560 @ 16MHz | Maximum I/O, Ethernet |

## Productivity Open (P1AM)

| Board | CPU | Features |
|-------|-----|----------|
| P1AM-100 | SAMD21 @ 48MHz | Expansion modules |
| P1AM-200 | SAMD51P20 @ 120MHz | Higher performance |

## Industrial Clone PLCs

| Board | CPU | Style |
|-------|-----|-------|
| FX3U-14M / LE3U-14M | STM32F103VCT6 @ 72MHz | Mitsubishi-style |
| WS3U-14Mx | STM32F103VCT6 @ 72MHz | Mitsubishi-style |
| FX3U-24MR / DollaTek | STM32F103VCT6 @ 72MHz | Mitsubishi-style |

## Other Industrial Boards

| Board | CPU | Features |
|-------|-----|----------|
| Iruino VEA | ESP32 | Industrial ESP32-based |
| SEQUENT-ESP32-PI | ESP32 | Raspberry Pi form factor |

## OpenPLC Runtime Targets

| Target | Description |
|--------|-------------|
| OpenPLC Runtime v3 | Legacy runtime installations |
| OpenPLC Runtime v4 | Current runtime with Modbus support |

## Board Manager URLs

For boards requiring external board manager definitions, the editor automatically configures:

| Platform | Board Manager URL |
|----------|-------------------|
| ESP32 | `https://espressif.github.io/arduino-esp32/package_esp32_index.json` |
| ESP8266 | `https://arduino.esp8266.com/stable/package_esp8266com_index.json` |
| STM32 | `https://github.com/stm32duino/BoardManagerFiles/raw/main/package_stmicroelectronics_index.json` |
| CONTROLLINO (AVR) | `https://raw.githubusercontent.com/CONTROLLINO-PLC/CONTROLLINO_Library/master/Boards/package_ControllinoHardware_index.json` |
| CONTROLLINO (RP2040) | `https://github.com/CONTROLLINO-PLC/controllino_rp2/releases/download/global/package_controllino_rp2_index.json` |
| RP2040/Pico | `https://github.com/earlephilhower/arduino-pico/releases/download/global/package_rp2040_index.json` |
| P1AM (FACTS) | `https://raw.githubusercontent.com/facts-engineering/facts-engineering.github.io/master/package_productivity-P1AM-boardmanagermodule_index.json` |

## Related Topics

- [Board Selection](../openplc-editor/hardware-configuration/board-selection.md) - Choosing and configuring boards
- [Pin Mapping](../openplc-editor/hardware-configuration/pin-mapping.md) - I/O configuration
- [Device Configuration Overview](../openplc-editor/hardware-configuration/device-config-overview.md) - Understanding target types
