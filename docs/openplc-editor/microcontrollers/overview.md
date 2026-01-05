# Microcontroller Overview

This page provides an introduction to programming microcontrollers with OpenPLC Editor.

> **Note**: This feature is only available in the desktop version of OpenPLC Editor.

## What is Microcontroller Programming?

OpenPLC Editor can compile your IEC 61131-3 programs into native code that runs directly on microcontroller boards. This transforms affordable development boards into standalone PLC devices.

## How It Works

1. **Write Your Program**: Create your PLC program using any supported IEC 61131-3 language
2. **Configure Hardware**: Select your target board and configure pin mappings
3. **Compile**: The editor compiles your program into native microcontroller code
4. **Upload**: Transfer the compiled program to your board via USB
5. **Run**: Your board now operates as a standalone PLC

## Advantages

- **Low Cost**: Use affordable Arduino and ESP32 boards
- **Standalone Operation**: No computer required after programming
- **Real-time Control**: Direct hardware access for fast response times
- **Flexible I/O**: Configure any GPIO pin as input or output

## Pin Mapping

In OpenPLC Editor v4, you configure pin mappings directly in the editor:

1. Navigate to the Hardware Configuration section
2. Add the pins you want to use
3. Map each pin to an IEC address (%IX, %QX, %IW, %QW)
4. The editor provides pin name suggestions based on your selected board

Unlike v3, there is no fixed list of pins - you add only the pins your application needs.

## Limitations

- No network connectivity in basic configurations (some boards support WiFi)
- Limited memory compared to full runtime installations
- Program updates require physical USB connection

## Next Steps

- [Supported Boards](supported-boards.md): See which boards are compatible
- [Uploading to Boards](uploading-to-board.md): Learn how to upload programs
