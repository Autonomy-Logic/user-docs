# Workspace Layout

The editor has four main areas: the **menu bar** at the very top, the **activity bar** on the left edge, the **side panel** (project tree + library), and the **central editor area** with a **console** docked to its bottom.

![The editor open on a project, showing the menu bar at the top, the activity bar on the left, the side panel with the project tree and library, the central editor with a Ladder Diagram body and the variables table above it, and the console at the bottom](../images/workspace-overview.png)

## Menu bar

Across the top: **File**, **Edit**, **Display**, **Help**, **Recent**.

| Menu | What's in it |
|---|---|
| File | Save File, Save Project, Close Tab, Close Project, Page Setup, Preview, Print, Check for Updates |
| Edit | Refresh, Clear Errors, Zoom In/Out, Switch Perspective, Reset Perspective, Full Screen, Sort Alpha, Change Theme |
| Display | (currently a single entry — kept for future view options) |
| Help | Community support |
| Recent | Last few projects you've opened (empty until you've opened more than one) |

Most actions are also reachable from the activity bar or with keyboard shortcuts — see the inline `Ctrl + …` hints in the menus.

## Activity bar

The narrow vertical strip on the left edge. From top to bottom:

| Icon | What it does |
|---|---|
| Files (Explorer) | Show/hide the side panel with the project tree and library |
| Git branch (Source Control) | Open the source control panel (changes, history, branches). A small badge shows how many files have pending edits |
| Magnifier (Search) | Open the project-wide search panel |
| Zoom | Toggle the toolbox (only meaningful when a graphical editor is open) |
| Download (Build options) | Build / build + deploy / clean build menu |
| Play | Start the PLC on the connected runtime (requires a connected vPLC) |
| Bug (Debugger) | Open the live-variable debugger |
| AI | Open the AI Engineer chat panel |
| **(divider)** | |
| Block, Coil, Contact, Delete | LD-only toolbox (shown when a Ladder Diagram body is open) |
| Block, Input/Output Variable, Connector, Continuation, Comment | FBD-only toolbox (shown when a Function Block Diagram body is open) |
| **(divider)** | |
| X | Close the project |
| ← (bottom) | Exit the editor and return to the Autonomy Edge project page |

The activity bar is always visible. The middle of the bar changes based on what kind of editor you have open — only LD and FBD bodies trigger context toolboxes.

## Side panel

To the right of the activity bar. Shown when **Explorer** is enabled.

### Project tree (top)

![Project tree showing the EDF Demo project expanded: PLC root with Functions, Function Blocks, Programs/main, Data Types, Resource, Device/Orchestrators, and Servers branches](../images/project-tree.png)

The branches:

- **Functions** — `function` POUs.
- **Function Blocks** — `function-block` POUs (including Python and C++ blocks).
- **Programs** — `program` POUs. The one bound to a task as an instance is what actually runs.
- **Data Types** — user-defined arrays, enumerations, and structures.
- **Resource** — the project's global variables, tasks, and instances. Open it to edit any of the three.
- **Device** — connected orchestrators and remote devices (Modbus master, EtherCAT).
- **Servers** — communication servers (Modbus TCP slave, OPC-UA, S7Comm).

Click any leaf to open it as a tab in the central editor. The **`+`** button at the top of the tree opens the **Create Element** popover (function, function-block, program, data-type, server, remote-device).

For more, see **[Project Tree](project-explorer)**.

### Library catalogue (bottom)

Below the project tree, the **Library** section lists every library that's enabled in this project. The bundled libraries are `iec-std-functions`, `iec-standard-fb`, `additional-function-blocks`, and `oscat-basic`. Click **+ Manage libraries…** to add or remove libraries from the system pool, or to enable a library for this project.

Expanding a library reveals each function and function block it contains — drag them into a graphical body to use them.

For more, see the **[Library Manager](../standard-function-blocks/library-manager)** page.

## Central editor area

Where you write, draw, and configure things. The tabs at the top show what's open.

The editor's contents change with what you've selected in the tree:

- **POU bodies** open the appropriate language editor: Structured Text, Ladder, Function Block Diagram, Instruction List, Python, or C++.
- **Data Types** opens a form editor (array dimensions, enum values, or structure fields).
- **Resource** opens a combined view with three sub-editors: Globals, Tasks, Instances.
- **Servers** open per-protocol configuration editors.
- **Device entries** open per-device configuration editors (e.g., Modbus master groups, EtherCAT slave channels).

When a POU body is open, the **variables table** appears between the breadcrumb and the body. It lists every variable declared for that POU. Toggle between table mode and raw `VAR ... END_VAR` code mode with the icons on the table's right edge.

### Tabs

Multiple files can be open simultaneously. Click a tab to switch, or click its `×` to close it. The breadcrumb above the active tab traces the path from the project root to whatever you're editing.

## Console

The strip at the bottom of the editor. It has tabs:

- **Console** — build, compile, runtime connection, debugger, and library messages. Filter by level (info / warning / error) and free-text search.
- **PLC Logs** — appears once you're connected to a Runtime v4 vPLC. Streams the live log feed from the runtime.
- **Search results** — populated by the activity-bar **Search** action.

The console has a **Filters** button for level toggles + search, a **Download** button to export logs, and a **Clear console** button to wipe the current view.

## Resizing

Most boundaries are draggable:

- The split between the side panel and the central editor.
- The split between the editor and the console.
- The split inside a POU between the variables table and the body.
- The split between the project tree and the library catalogue.

The side panel and console can both be collapsed entirely to maximise the editing space — click the **Explorer** icon to toggle the side panel; resize the console divider down to zero to hide the console.

## What's next

- Inspect the project structure in detail: **[Project Tree](project-explorer)**.
- Learn the console and live-debugging surface: **[Console & PLC Logs](console-debugging)**.
- Jump to a programming language: **[Structured Text](../programming-languages/structured-text/st-basics)** · **[Ladder Diagram](../programming-languages/ladder-diagram/ld-basics)** · **[Function Block Diagram](../programming-languages/function-block-diagram/fbd-basics)** · **[Instruction List](../programming-languages/instruction-list/il-basics)**.
