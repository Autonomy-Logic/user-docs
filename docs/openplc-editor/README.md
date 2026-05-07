# Autonomy Edge IDE

The Autonomy Edge IDE is your browser-based environment for creating, compiling, and deploying PLC programs on the Autonomy Edge platform. No installation required. Just open your browser and start building.

The IDE supports IEC 61131-3 programming languages. Ladder Diagram (LD), Structured Text (ST), Function Block Diagram (FBD), and Instruction List (IL). Plus Python and C/C++ function blocks. You can manage your entire PLC project from one interface: write programs, configure variables, set up tasks, and deploy to your devices.

## In This Section

### Workspace Overview

Get familiar with the IDE interface and learn where everything is.

- [**Workspace Layout**](workspace-overview/workspace-layout): The overall IDE layout: Activity Bar, Project Explorer, Editor Area, and Console Panel.
- [**Project Explorer**](workspace-overview/project-explorer): Navigate your project tree: Functions, Function Blocks, Programs, Data Types, Resources, Devices, and Servers.
- [**Console & Debugging**](workspace-overview/console-debugging): Read compilation output, runtime logs, and troubleshoot errors.

### IEC 61131-3 Concepts

Understand the building blocks of IEC 61131-3 PLC programming.

- [**Program Organization Units (POUs)**](iec-concepts/pous): Programs, Functions, and Function Blocks. What each is and when to use them.
- [**Variables & Data Types**](iec-concepts/variables-datatypes): Variable classes, base data types, and user-defined types.
- [**Tasks & Instances**](iec-concepts/tasks-instances): How tasks control execution timing and how instances bind programs to tasks.

### Task Configuration

Configure how and when your PLC programs execute.

- [**Understanding Tasks**](task-configuration/understanding-tasks): Cyclic vs. interrupt triggering, intervals, and priorities.
- [**Task Editor**](task-configuration/task-editor): Create, edit, and manage tasks in the Resource editor.
- [**Instance Management**](task-configuration/instance-management): Bind programs to tasks through instances.

### Building & Deploying

- [**Project Compilation**](building-deploying/project-compilation): How to compile your project and read the Console output.
- [**Deployment**](building-deploying/deployment-vplc): Deploy your compiled program to a device.
- [**XML Export**](building-deploying/xml-export): Export your project as a standard XML file for backup or sharing.

### Connecting to Runtimes

- [**Connecting to Runtimes**](connecting-to-runtimes): Connect the IDE to your devices, authenticate, and control program execution.

---

## Prerequisites

Before using the IDE, you need:

1. An Autonomy Edge account at `https://edge.autonomylogic.com`.
2. At least one orchestrator registered with an active device. See [Managing Device Status](../platform-features/vplc-management/managing-status) for setup instructions.

---

## What's Next?

Start with the [Workspace Layout](workspace-overview/workspace-layout) to get oriented in the IDE.
