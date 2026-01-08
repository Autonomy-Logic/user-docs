# Overview

OpenPLC Editor is available in two versions that share the same core functionality but are designed for different use cases and workflows. This page explains the differences between the desktop and web versions to help you choose the right one for your needs.

## Desktop Editor

The desktop version of OpenPLC Editor is a standalone application that you download and install on your computer. It runs locally on Windows, macOS, or Linux and provides direct access to all features without requiring an internet connection.

### When to Use the Desktop Editor

The desktop editor is ideal when you need to:

- **Program microcontrollers**: The desktop editor supports programming Arduino boards, ESP32, and other microcontrollers directly. This feature is not available in the web version.
- **Work offline**: Since the editor runs locally, you can develop PLC programs without an internet connection.
- **Connect to local runtimes**: The desktop editor can connect directly to OpenPLC Runtime instances on your local network without requiring any cloud infrastructure.
- **Use Runtime v3**: If you have existing OpenPLC Runtime v3 installations, the desktop editor maintains compatibility with them.

### Desktop Editor Features

The desktop editor includes all the core programming features plus:

- Direct LAN connection to OpenPLC Runtime instances
- Arduino and microcontroller programming and upload
- Support for both Runtime v3 and v4
- Local file storage and project management
- No account or subscription required

## Web Editor (Autonomy Edge)

The web version of OpenPLC Editor is integrated into the Autonomy Edge platform and runs entirely in your browser. It provides the same programming capabilities as the desktop editor with additional cloud-based features for team collaboration and remote device management.

### When to Use the Web Editor

The web editor is ideal when you need to:

- **Access from anywhere**: Program PLCs from any device with a web browser, without installing software.
- **Collaborate with teams**: Share projects with colleagues and work together in real-time.
- **Manage remote devices**: Deploy programs to vPLC instances running on orchestrator agents anywhere in the world.
- **Automatic backups**: All projects are automatically saved and versioned in the cloud.
- **Centralized management**: Manage multiple PLCs and edge devices from a single dashboard.

### Web Editor Features

The web editor includes all the core programming features plus:

- Browser-based access from any device
- Cloud project storage with automatic versioning
- Team collaboration and project sharing
- Integration with orchestrator agents for remote deployment
- vPLC (virtual PLC) management and monitoring
- No software installation required

## Feature Comparison

| Feature | Desktop Editor | Web Editor |
|---------|---------------|------------|
| **Installation** | Download and install | No installation |
| **Internet Required** | No | Yes |
| **Runtime Connection** | Direct LAN | Via orchestrator |
| **Arduino/Microcontrollers** | Yes | No |
| **Runtime v3 Support** | Yes | No |
| **Runtime v4 Support** | Yes | Yes |
| **Project Storage** | Local files | Cloud |
| **Collaboration** | Manual sharing | Built-in |
| **vPLC Management** | No | Yes |
| **Account Required** | No | Yes |

## Shared Features

Both versions of OpenPLC Editor share the same core functionality:

### Programming Languages
- Structured Text (ST)
- Ladder Diagram (LD)
- Function Block Diagram (FBD)
- Instruction List (IL)
- Sequential Function Chart (SFC)
- Python (custom function blocks)
- C++ (custom function blocks)

### Development Tools
- Intelligent code editor with syntax highlighting
- Graphical editors for LD, FBD, and SFC
- Project explorer with hierarchical view
- Variable editor and management
- Real-time console for debugging
- Standard function block library

### Project Organization
- Program Organization Units (POUs)
- Custom data types (arrays, structures, enumerations)
- Task configuration
- Hardware configuration
- Communication protocol setup (Modbus, etc.)

## Choosing the Right Version

**Choose the Desktop Editor if:**
- You need to program Arduino or other microcontrollers
- You work primarily with local PLCs on your network
- You need offline access
- You have existing Runtime v3 installations

**Choose the Web Editor if:**
- You need to access projects from multiple devices
- You work with a team and need collaboration features
- You manage remote PLCs through orchestrator agents
- You want automatic cloud backups and versioning

## Using Both Versions

Many users find value in using both versions depending on their current task. Projects created in either version use the same project file format, making it possible to work on the same project in both environments (though manual file transfer is required between them).

For example, you might use the desktop editor for developing and testing programs locally with Arduino boards, then use the web editor to deploy and manage production systems remotely through the Autonomy Edge platform.
