# Autonomy Edge IDE — Overview

The Autonomy Edge IDE is a modern, browser-based development environment for IEC 61131-3 PLC programming. It runs directly within the Autonomy Edge platform — no desktop software to install.

## What You Can Do

The IDE gives you everything you need to develop PLC control logic:

- **Write PLC programs** in IEC 61131-3 languages: Ladder Diagram (LD), Structured Text (ST), Function Block Diagram (FBD), and Instruction List (IL).
- **Use Python and C/C++** for custom function blocks when you need capabilities beyond the standard languages.
- **Manage variables** with a visual table editor supporting all IEC variable classes (input, output, local, global, etc.) and standard data types.
- **Define custom data types** including arrays, enumerations, and structures.
- **Configure tasks and instances** that control when and how your programs execute on the device.
- **Compile and deploy** your project to devices through the Autonomy Edge platform.
- **Monitor runtime output** through the Console Panel, which shows compilation progress, runtime logs, and PLC execution output.
- **Configure communication protocols** including Modbus TCP/RTU (master and slave), S7Comm server, and OPC-UA server.

## Web IDE vs. Desktop Editor

The OpenPLC project also offers a desktop editor that runs as a standalone application on Windows, macOS, and Linux. Both share the same IEC 61131-3 project format, so projects created in one can generally be opened in the other.

Key differences:

- **Installation** — The web IDE runs in your browser with no install. The desktop editor requires a local installation.
- **Platform integration** — The web IDE is built into Autonomy Edge with direct device management and deployment. The desktop editor is a standalone application.
- **Deployment** — The web IDE deploys directly to your connected devices. The desktop editor requires manual transfer.
- **Communication config** — The web IDE has visual editors for Modbus, S7Comm, and OPC-UA. The desktop editor has limited support.

If you're using the Autonomy Edge platform, the web IDE is the recommended development environment.

---

## What's Next?

Learn the [Workspace Layout](workspace-overview/workspace-layout) to understand the IDE's interface and start working with your first project.
