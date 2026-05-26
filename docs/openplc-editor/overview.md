# OpenPLC Editor: Overview

The OpenPLC Editor is the browser-based development environment for IEC 61131-3 PLC programs that ships with Autonomy Edge. You write code, manage variables, configure communication protocols, and deploy to vPLCs without leaving the browser.

The editor opens whenever you click **Open in editor** from a project page. It loads in the same browser tab.

![The OpenPLC Editor open on the EDF Demo project, showing the project tree on the left, the LD body editor for `main` in the centre, the library catalogue at the bottom of the side panel, and the console at the bottom](images/workspace-overview.png)

## What you can do

- Write PLC code in **Structured Text (ST)**, **Ladder Diagram (LD)**, **Function Block Diagram (FBD)**, and **Instruction List (IL)**.
- Author **Python** and **C/C++** function blocks for logic that doesn't fit cleanly in IEC 61131-3.
- Edit **variables** in a table or as raw `VAR ... END_VAR` text. Bind them to physical addresses (`%IX0.0`, `%QW3`, `%MD5`, …) or expose them through communication protocols.
- Define **custom data types** (arrays, enumerations, structures) and use them in your variable declarations.
- Configure **tasks** (cyclic, with priority and interval) and the program **instances** they run.
- Expose your variables over **Modbus TCP**, **OPC-UA**, or **S7Comm** as a server, or read remote I/O as a **Modbus master**.
- Run programs in the browser with the **built-in Simulator**, or connect to a real vPLC on an **orchestrator**, deploy your build, and watch live variable values in the **debugger**.
- Use the **AI Engineer** for chat-based help and inline code completion across ST, IL, Python, and C++.
- Track changes with the built-in **source control panel** (commits, history, branches, inline diffs).

## What's not here

A handful of features in the desktop OpenPLC Editor are **not part of the web editor**. The most relevant ones:

- The **board selector** and **VPP vendor screens**: the web editor is bound to the runtime image that built the vPLC, so the board is fixed.
- **USB upload** for Arduino-class targets.
- **Local file paths**: projects in the web editor live in the platform's git store, not on your disk.

If you need any of these, install the standalone OpenPLC Editor and use it alongside Autonomy Edge.

**The browser-based Simulator is fully supported in the web editor.** It's the same `avr8js` AVR emulator the desktop editor uses, running in your browser tab. See **[Running with the Simulator](building-deploying/simulator)**.

## How to read this section

- **[Workspace Layout](workspace-overview/workspace-layout)** is the orientation tour: title bar, activity bar, project tree, console.
- **[Programming Languages](programming-languages/structured-text/st-basics)** walks each IEC language with examples.
- **[Variables and Data Types](working-with-variables/variables-editor)** covers the variable table, classes, locations, and aliases.
- **[Standard Block Library](standard-function-blocks/timer-blocks)** is the per-block reference.
- **[Communication](communication/modbus/server)** is the per-protocol reference, with worked examples.
- **[Connecting to a vPLC](connecting-to-runtimes)** is how you get from "I wrote a program" to "it's running on a device".

## What's next

Start with the **[Workspace Layout](workspace-overview/workspace-layout)** to learn the editor's geography.
