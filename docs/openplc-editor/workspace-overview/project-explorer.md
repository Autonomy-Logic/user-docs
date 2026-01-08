# Project Explorer

The Project Explorer is your central navigation hub in the Autonomy Edge IDE. It provides a hierarchical tree view of all components in your PLC project, making it easy to organize, locate, and access different parts of your program.

## Overview

The Project Explorer panel is located on the left side of the IDE workspace. It displays your project structure in a collapsible tree format, allowing you to quickly navigate between different elements of your program.

![Project Explorer](images/project-explorer-clean.png)
*The Project Explorer showing the complete project hierarchy*

## Project Structure

Every project in the IDE follows a standard IEC 61131-3 structure with the following main sections:

### 1. Project Root

At the top of the tree is your project name. Clicking on the project name allows you to edit the project's metadata and settings.

### 2. Functions

This section contains all Function POUs (Program Organization Units) in your project. Functions are reusable code blocks that:
- Accept input parameters
- Return a single value
- Have no internal state (no memory between calls)
- Are ideal for mathematical calculations and data transformations

Functions are displayed with a special icon and can be expanded to show their properties. You can create functions in any of the five IEC 61131-3 languages (ST, LD, IL, FBD, SFC).

### 3. Function Blocks

Function Blocks are more complex POUs that:
- Accept input and output parameters
- Maintain internal state between calls
- Can have local variables that persist
- Are ideal for control algorithms and state machines

Function Blocks can be written in the standard IEC 61131-3 languages, as well as Python and C++ for advanced functionality.

### 4. Programs

Programs are the top-level POUs that:
- Are executed by tasks
- Can call functions and function blocks
- Contain the main logic of your application
- Are assigned to tasks for cyclic or interrupt-driven execution

Each project must have at least one program. Programs are displayed in the tree and can be opened by clicking on them.

### 5. Data Types

The Data Types section contains custom data type definitions that you create for your project:

- **Array**: Multi-dimensional arrays of base types or custom types
- **Enumerated**: Named constants for improved code readability
- **Structure**: Complex data types with multiple fields (similar to structs in C)

Custom data types help you organize complex data and make your code more maintainable.

### 6. Resource

The Resource section contains the runtime configuration for your program:

- **Global Variables**: Variables accessible from all POUs in the project
- **Tasks**: Cyclic or interrupt-driven execution tasks
- **Instances**: Assignments of programs to tasks

This is where you configure how your program will execute on the target device.

### 7. Device

The Device section contains hardware-specific configuration:

- **Configuration**: I/O mapping, communication settings, and board selection
- **Hardware Setup**: Pin assignments and device-specific parameters

This section allows you to map your program variables to physical inputs and outputs.

## Working with the Project Explorer

### Opening Files

To open any element in the Project Explorer:
1. Click on the element name (e.g., a program, function, or data type)
2. The file will open in a new tab in the editor area
3. Multiple files can be open simultaneously in tabs

### Creating New Elements

To create a new POU, data type, or other element:
1. Click the **+** button at the top of the Project Explorer
2. Select the type of element you want to create
3. Choose the programming language (for POUs)
4. Enter a name for the new element
5. The new element will be created and opened in the editor

### Context Menus

Right-clicking on elements in the Project Explorer (indicated by the three-dot menu icon) provides additional options:
- **Rename**: Change the name of the element
- **Delete**: Remove the element from the project
- **Duplicate**: Create a copy of the element
- **Properties**: View and edit element properties

### Expanding and Collapsing

- Click the arrow icon next to a section to expand or collapse it
- This helps you focus on the parts of the project you're currently working on
- The IDE remembers which sections you have expanded

## Library Panel

Below the Project Explorer is the Library panel, which provides access to:

### Standard Function Blocks
Pre-built function blocks for common operations:
- **Timers**: TON, TOF, TP for time-based control
- **Counters**: CTU, CTD, CTUD for counting operations
- **Bistable**: RS, SR for set/reset logic
- **Edge Detection**: R_TRIG, F_TRIG for detecting signal changes

### Additional Libraries
Extended function blocks for specific applications:
- **Arduino Function Blocks**: Arduino-specific I/O and peripherals
- **Communication Blocks**: MQTT, Modbus, and other protocols
- **Hardware-Specific Blocks**: Modules for specific PLC hardware

### Using Library Blocks

To use a library block in your code:
1. Expand the library category in the Library panel
2. Drag the function block into your code (for graphical languages)
3. Or type the function block name in your code (for text languages)
4. The function block will be automatically included in your program

## Navigation Tips

1. **Use Search**: Press Ctrl+F to search for elements across your entire project
2. **Breadcrumbs**: Use the breadcrumb trail above the editor to navigate back through your path
3. **Recent Files**: Use the Recent menu to quickly access files you've worked on recently
4. **Keyboard Navigation**: Use arrow keys to navigate the tree, Enter to open files
5. **Filter View**: Collapse sections you're not using to reduce clutter

## Project Organization Best Practices

1. **Group Related Functions**: Keep related functions together by using consistent naming
2. **Use Descriptive Names**: Choose clear, descriptive names for POUs and data types
3. **Organize by Purpose**: Group function blocks by their purpose (e.g., all motor control blocks together)
4. **Document Your Structure**: Use comments and documentation fields to explain the purpose of each element
5. **Keep It Simple**: Don't create too many nested structures; keep the hierarchy flat when possible

## Next Steps

Now that you understand how to navigate the Project Explorer, you can learn about the Console and Debugging features to monitor and troubleshoot your programs during development and runtime.
