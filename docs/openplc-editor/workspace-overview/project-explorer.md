# Project Explorer

The Project Explorer is the sidebar on the left side of the IDE. It organizes your entire PLC project into a tree, giving you a clear view of everything in your project and quick access to open items in the Editor Area.

## Project Name

At the top of the Project Explorer, you'll see your project name with a folder icon. Click the name to edit it inline. Type a new name and click away (or press Tab) to save.

Next to the project name is a **+** button. Click it to create new project elements: Programs, Functions, Function Blocks, or Data Types. For POUs, you choose a name and programming language. For Data Types, you choose a name and type (array, enumeration, or structure).

## Tree Structure

Below the project name, your project is organized into these branches. Click any branch to expand or collapse it.

### Functions

All POUs of type **Function**. Functions take inputs, perform a computation, and return a single value. They don't maintain internal state between calls.

Each function shows an icon indicating its language (ST, LD, FBD, or IL). Click to open it in the Editor Area.

### Function Blocks

All POUs of type **Function Block**. Function blocks are reusable units that can maintain internal state. Their local variables persist between calls. You can create multiple instances of the same function block, each with its own data.

Function blocks support all five IEC 61131-3 languages plus Python and C/C++.

### Programs

All POUs of type **Program**. Programs are the top-level units that get assigned to tasks for execution. They're the entry point of your PLC logic. You bind them to tasks through instances in the Resource configuration.

### Data Types

Your user-defined data types, organized into sub-categories:

- **Arrays**: Array types with a base type and dimensions.
- **Enumerations**: Types that define a set of named values.
- **Structures**: Types that group multiple named fields of different types.

Click any data type to open its editor.

### Resources

Opens the Resource editor, which has three sections:

1. **Global Variables**: Variables shared across all POUs in the project.
2. **Tasks**: Execution tasks with triggering mode (Cyclic or Interrupt), interval, and priority.
3. **Instances**: Binds programs to tasks, defining which program runs under which task.

This is where you configure how your PLC project executes. See [Tasks & Instances](../iec-concepts/tasks-instances) for details.

### Devices

- **Orchestrators**: Lists all orchestrators registered in your Autonomy Edge account and their devices. From here, you select which device to connect to, and manage runtime login and user creation.
- **Remote Devices**: Any configured remote device connections (e.g., Modbus TCP/RTU clients).

### Servers

Communication server configurations:

- **Modbus TCP Slave**: Expose PLC memory to external SCADA systems or HMIs over Modbus TCP.
- **S7Comm Server**: Siemens S7 protocol compatibility for S7-compatible clients.
- **OPC-UA Server**: Publish PLC variables as an OPC-UA address space for standardized industrial communication.

Click any server to open its configuration editor.

## Opening Elements

Click any item in the tree to open it as a tab in the Editor Area. If it's already open, clicking switches to that tab. The IDE keeps track of all open tabs in the Navigation bar at the top of the Editor Area.

> **Tip:** Use the Search button in the Activity Bar to find specific elements in large projects. Matching items in the Project Explorer are highlighted with the search query.

---

## What's Next?

Learn how the [Console & Debugging](console-debugging) panel helps you track compilation and diagnose issues.
