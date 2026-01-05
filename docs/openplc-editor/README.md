# OpenPLC Editor

OpenPLC Editor is a powerful IEC 61131-3 programming environment for creating PLC programs. It is available in two forms: as a standalone desktop application for Windows, macOS, and Linux, and as a browser-based editor integrated into the Autonomy Edge platform.

Both versions share the same core functionality, allowing you to create, edit, and deploy PLC programs using the five standard IEC 61131-3 programming languages, as well as custom languages like Python and C++.

## What is IEC 61131-3?

IEC 61131-3 is the international standard for programmable logic controller (PLC) programming languages. It defines five programming languages that are widely used in industrial automation:

- **Structured Text (ST)**: A high-level, text-based language similar to Pascal
- **Ladder Diagram (LD)**: A graphical language that resembles electrical relay logic
- **Function Block Diagram (FBD)**: A graphical language using interconnected function blocks
- **Instruction List (IL)**: A low-level, assembly-like text language
- **Sequential Function Chart (SFC)**: A graphical language for sequential control

## Key Features

OpenPLC Editor provides a comprehensive development environment with the following features:

### Professional Development Tools
- **Multi-language Support**: Write code in any of the five IEC 61131-3 languages, plus Python and C++ for custom function blocks
- **Intelligent Code Editor**: Syntax highlighting, code completion, and error detection
- **Graphical Editors**: Visual programming tools for Ladder Diagram, Function Block Diagram, and Sequential Function Chart
- **Project Explorer**: Hierarchical view of all project components including POUs, data types, and configuration

### Debugging and Testing
- **Real-time Console**: Monitor runtime logs and system messages
- **Variable Debugging**: Watch and modify variable values during execution

### Project Organization
- **Program Organization Units (POUs)**: Organize your code into reusable Programs, Function Blocks, and Functions
- **Custom Data Types**: Define structures, arrays, and enumerations for complex data handling
- **Task Configuration**: Configure cyclic and interrupt-driven tasks for real-time control
- **Hardware Configuration**: Map your program to physical I/O and communication interfaces

## Desktop vs Web Editor

OpenPLC Editor is available in two versions to suit different workflows:

| Feature | Desktop Editor | Web Editor (Autonomy Edge) |
|---------|---------------|---------------------------|
| Installation | Download and install locally | No installation required |
| Runtime Connection | Direct connection over LAN | Connection via orchestrator agent |
| Arduino/Microcontrollers | Full support | Not available |
| Runtime v3 Support | Yes | No |
| Cloud Storage | Local files only | Automatic cloud backup |
| Collaboration | Manual file sharing | Built-in team collaboration |

For detailed information about each version, see the [Overview](overview.md) page.

## Getting Started

**Desktop Editor**: Download and install the editor from [autonomylogic.com/download](https://autonomylogic.com/download), then connect directly to OpenPLC Runtime instances on your local network.

**Web Editor (Autonomy Edge)**: Sign up at [edge.autonomylogic.com](https://edge.autonomylogic.com) and open any project from your dashboard. The IDE will load in your browser, providing you with a complete development environment.

## What You'll Learn

In this section of the documentation, you will learn:

1. **Overview**: Understanding the differences between desktop and web versions
2. **Installation**: How to install the desktop editor on your system
3. **Connecting to Runtimes**: How to connect to OpenPLC Runtime instances
4. **Workspace Overview**: Understanding the layout, project explorer, and console
5. **IEC 61131-3 Concepts**: Core concepts like POUs, variables, data types, tasks, and instances
6. **Programming Languages**: Detailed guides for each supported programming language
7. **Custom Languages**: Using Python and C++ for advanced function blocks
8. **Working with Variables**: Managing local and global variables
9. **Custom Data Types**: Creating and using arrays, structures, and enumerations
10. **Standard Function Blocks**: Using the built-in library of standard functions
11. **Task Configuration**: Setting up cyclic and interrupt-driven execution
12. **Hardware Configuration**: Configuring I/O and communication settings
13. **Communication Protocols**: Setting up Modbus and other industrial protocols
14. **Microcontrollers**: Programming Arduino and other microcontroller boards (desktop only)
15. **Building and Deploying**: Compiling and deploying your programs to devices

Whether you're new to PLC programming or an experienced automation engineer, this documentation will help you make the most of OpenPLC Editor.
