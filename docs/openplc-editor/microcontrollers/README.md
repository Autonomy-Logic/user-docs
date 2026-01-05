# Microcontrollers

OpenPLC Editor (desktop version) supports programming microcontroller boards directly, allowing you to create standalone PLC devices using affordable hardware like Arduino, ESP32, and other compatible boards.

> **Note 1**: Arduino boards aren't suitable for industrial environments. Support for Arduino boards on OpenPLC should be used for prototyping purposes only. For deploying on industrial production environments, please upload your project to a robust industrial-grade device running OpenPLC Runtime v4.
> **Note 2**: Microcontroller programming is only available in the desktop version of OpenPLC Editor. The web editor (Autonomy Edge) can only program devices running OpenPLC Runtime v4 through the Autonomy Orchestrator Agent.

## Overview

With microcontroller support, you can:

- Write PLC programs using IEC 61131-3 languages
- Compile programs directly for microcontroller targets
- Upload programs via USB to the target board
- Create standalone automation controllers

## In This Section

- **[Overview](overview.md)**: Introduction to microcontroller programming with OpenPLC
- **[Supported Boards](supported-boards.md)**: List of compatible microcontroller boards
- **[Uploading to Boards](uploading-to-board.md)**: How to compile and upload programs

## Supported Board Families

OpenPLC Editor supports a wide variety of microcontroller boards:

- **Arduino**: Uno, Mega, Due, Nano, Leonardo, and more
- **ESP32/ESP8266**: WiFi-enabled boards for IoT applications
- **STM32**: High-performance ARM Cortex-M boards
- **Controllino**: Industrial Arduino-compatible PLCs
- **Raspberry Pi Pico**: RP2040-based boards
- **P1AM**: Industrial Arduino-compatible PLCs with modular I/O
