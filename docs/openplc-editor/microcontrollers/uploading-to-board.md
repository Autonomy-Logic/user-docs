# Uploading to Boards

This page explains how to compile and upload PLC programs to microcontroller boards using OpenPLC Editor.

> **Note**: This feature is only available in the desktop version of OpenPLC Editor.

## Prerequisites

Before uploading to a board, ensure you have:

1. OpenPLC Editor desktop application installed
2. A compatible microcontroller board
3. USB cable to connect the board to your computer
4. Appropriate USB drivers installed (if required by your board)

## Step-by-Step Upload Process

### 1. Create or Open Your Project

Open an existing project or create a new one with your PLC program.

### 2. Configure Hardware

1. Navigate to the **Device** section in the project explorer
2. Click on **Configuration**
3. Select your target board from the available options
4. Configure the pin mappings for your application

### 3. Add Pin Mappings

1. In the Hardware Configuration, click to add a new pin
2. Select the pin name from the suggestions (based on your board)
3. Assign an IEC address to the pin:
   - Digital inputs: %IX0.0, %IX0.1, etc.
   - Digital outputs: %QX0.0, %QX0.1, etc.
   - Analog inputs: %IW0, %IW1, etc.
   - Analog outputs: %QW0, %QW1, etc.
4. Repeat for all pins your program uses

### 4. Connect Your Board

1. Connect your microcontroller board to your computer via USB
2. Wait for the operating system to recognize the device
3. Note the serial port assigned to your board (if needed)

### 5. Compile and Upload

1. Click the **Compile and Upload** button in the toolbar
2. Select the serial port for your board (if prompted)
3. Wait for the compilation to complete
4. The program will automatically upload to your board
5. Monitor the console for progress and any errors

### 6. Verify Operation

Once uploaded:
- The board will automatically start running your program
- LEDs or outputs should respond according to your program logic
- The board operates independently - you can disconnect USB

## Troubleshooting

### Board Not Detected

1. **Check USB connection**: Try a different USB cable or port
2. **Install drivers**: Some boards require specific USB drivers
3. **Check Device Manager** (Windows) or `ls /dev/tty*` (Linux/macOS)

### Compilation Errors

1. **Check your program**: Ensure there are no syntax errors
2. **Verify pin mappings**: Make sure all used addresses are mapped
3. **Check board selection**: Ensure the correct board is selected

### Upload Fails

1. **Close other applications**: Ensure no other program is using the serial port
2. **Reset the board**: Press the reset button before uploading
3. **Check permissions** (Linux): Add your user to the `dialout` group
   ```bash
   sudo usermod -a -G dialout $USER
   ```

### Program Doesn't Run Correctly

1. **Verify pin mappings**: Check that pins are mapped to correct addresses
2. **Check wiring**: Ensure physical connections match your configuration
3. **Review program logic**: Test with simple programs first

## Tips for Success

### Start Simple

Begin with a simple program (like blinking an LED) to verify your setup works before moving to complex applications.

### Document Pin Mappings

Keep a record of which physical pins are mapped to which IEC addresses for future reference.

### Use Meaningful Names

In your PLC program, use descriptive variable names that indicate the physical connection (e.g., `StartButton`, `MotorRelay`).

### Test Incrementally

Add functionality gradually and test after each addition to isolate problems quickly.

## Updating Programs

To update a program on your board:

1. Make changes to your project in OpenPLC Editor
2. Connect the board via USB
3. Click Compile and Upload again
4. The new program replaces the old one

Note: There is no way to read the program back from the board. Always keep your project files saved.
