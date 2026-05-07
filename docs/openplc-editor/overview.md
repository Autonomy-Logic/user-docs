# Autonomy Edge IDE: Overview

The Autonomy Edge IDE is a modern, browser-based development environment for IEC 61131-3 PLC programming. It runs directly within the Autonomy Edge platform. No desktop software to install.

## What You Can Do

The IDE gives you everything you need to develop PLC control logic:

- **Write PLC programs** in IEC 61131-3 languages: Ladder Diagram (LD), Structured Text (ST), Function Block Diagram (FBD), and Instruction List (IL).
- **Use Python and C/C++** for custom function blocks when you need capabilities beyond the standard languages.
- **Manage variables** with a visual table editor supporting all IEC variable classes (input, output, local, global, etc.) and standard data types.
- **Define custom data types** including arrays, enumerations, and structures.
- **Configure tasks and instances** that control when and how your programs execute on the device.
- **Compile and deploy** your project to devices through the Autonomy Edge platform.
- **Test instantly with the Simulator**: Run and debug your program directly in the browser using the [built-in Simulator](building-deploying/simulator), no hardware required.
- **Monitor runtime output** through the Console Panel, which shows compilation progress, runtime logs, and PLC execution output.
- **Configure communication protocols** including Modbus TCP/RTU (master and slave), S7Comm server, and OPC-UA server.

## Web IDE vs. Desktop Editor

The OpenPLC project also offers a desktop editor that runs as a standalone application on Windows, macOS, and Linux. Both share the same IEC 61131-3 project format, so projects created in one can generally be opened in the other.

Key differences:

- **Installation**: The web IDE runs in your browser with no install. The desktop editor requires a local installation.
- **Platform integration**: The web IDE is built into Autonomy Edge with direct device management and deployment. The desktop editor is a standalone application.
- **Deployment**: The web IDE deploys directly to your connected devices. The desktop editor requires manual transfer.
- **Runtime management**: In the web IDE, the runtime is managed automatically by the Orchestrator. In the desktop editor, you install and manage the runtime yourself.
- **Communication config**: The web IDE has visual editors for Modbus, S7Comm, and OPC-UA. The desktop editor has limited support.

If you're using the Autonomy Edge platform, the web IDE is the recommended development environment.

---

## Tablet and Mobile Use

Autonomy Edge works in modern mobile browsers (Safari on iPad, Chrome on Android). However, the IDE is designed for desktop use. Graphical editors (Ladder, FBD) work best with a mouse or trackpad. For monitoring and simple edits, a tablet with a Bluetooth keyboard works well.

---

## What's Next?

Learn the [Workspace Layout](workspace-overview/workspace-layout) to understand the IDE's interface and start working with your first project.
