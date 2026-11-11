# Debugger

The debugger lets you watch live variable values from a running vPLC, charted over time. It uses a custom Modbus PDU (function codes `0x41`–`0x45`) over WebSocket (Runtime v4) or Modbus TCP (Runtime v3) to read variable values out of the runtime on a tight polling loop.

There's no breakpoint / step support, this debugger is **live inspection only**.

## Prerequisites

- The editor is **connected** to a vPLC. See **[Connecting to a vPLC](../connecting-to-runtimes)**.
- You've **opted in** the variables you want to watch (Debug column checkbox in the variables table, see **[Variables editor](../working-with-variables/variables-editor)**). The **Tags** tab described below needs no opt-in: it lists the whole project.

## Opening the debugger

Click the **bug** icon in the activity bar (between Play and AI).

What happens behind the scenes:

1. The editor saves the project (if dirty).
2. The compiler runs a **debug build**, same as a release build, plus a `.dbg` symbol map and an MD5 hash of the compiled program.
3. The editor compares the local MD5 against the one currently running on the vPLC (`runtime.readProgramMd5`).
   - **Match** → the debug session starts.
   - **Mismatch** → a dialog prompts you to upload. Confirm to ship the build and start.

The console reports each step.

## What you see

The debugger panel replaces the console at the bottom of the editor.

It contains a **line chart**:

- **X axis**: elapsed time. The default window is 10 seconds; the buffer keeps 10 minutes of history.
- **Y axis**: variable values. Multiple variables share the chart; the legend on top lets you toggle each line.
- **Boolean** variables render at the top or bottom of the chart with sharp transitions.
- **Numeric** variables (REAL, INT, etc.) get normalised to the same Y range so they share the chart cleanly.

Controls along the top:

- **Pause / Play**: freeze the chart (the polling keeps running in the background; resume to see what happened).
- **Range selector**: pick the visible time window (1 s, 5 s, 10 s, 30 s, 1 min, 5 min, 10 min).
- **Elapsed clock**: total session time.

## The tag table

The **Tags** tab, next to **Debugger** at the bottom of the editor, lists **every variable of the project** in one table, with no need to tick anything first. Each row shows:

| Column | What it holds |
|---|---|
| **Name** | The variable name, with the program or `Global` it belongs to. A structure or function-block instance has a `+` that expands it into its members. |
| **Value** | The live value read from the running vPLC. |
| **Area** | The monitor view this tag belongs to, or `-` for none. Pick another view to move the tag to it. |
| **Address** | The variable's IEC address or alias, when it has one. |
| **Force** | `1` and `0` for a BOOL, a value box for any other type (press Enter to apply), and **release** on a tag that is currently forced. Forced rows are highlighted. |
| **Type** | The variable's IEC type. |
| **Comment** | The variable's documentation. |

The **Filter** box matches any part of a name, scope, view, address, type or comment, ignoring case, and the counter next to it reads `shown of total`.

Only the tags the table currently shows are polled, so a filter or a view also narrows what is read from the vPLC.

### Monitor views

A **view** is a named subset of the tags, the same idea as a Monitor Table in ISPSoft or a Tag table in TIA Portal.

- **New view** creates one and selects it.
- Choosing a view in **Area** on a tag's row moves that tag into it; choosing `-` takes it out of every view.
- The selector on the left switches between **All tags** and a single view.
- **Delete view** removes the selected view. The tags themselves are untouched.

Views are saved inside the project, so they come back the next time the project is opened, and they travel with it to anyone else who opens it.

## Opting variables in

In the variables table for any POU, tick the **Debug** column. Only ticked variables are polled. Tick fewer for more responsive polling; tick more for broader coverage.

You can change the selection mid-session. Newly ticked variables join the chart on the next poll cycle (typically `< 200 ms`).

## Limitations

- **No breakpoints.** The IEC runtime doesn't support pause/step semantics. This debugger is a watcher, not a control surface.
- **No history before connection.** The debugger only starts buffering once the session begins. Variables that change in the milliseconds before you open the debugger aren't recoverable.
- **Numeric scaling is global.** All numeric variables share one Y axis. Mix a `REAL` in the range `0…1` with an `INT` in `0…1000` and the small one will look flat, toggle the big one off in the legend to zoom in on the small one.

## Troubleshooting

**MD5 mismatch prompt.** The build on disk is newer than what's running on the vPLC. Accept the upload to sync them.

**Variables flat at zero.** Confirm the variable is actually ticked in the **Debug** column, and that the PLC is **Running** (Play button in the activity bar should be coloured-in / pressable).

**Polling stalls.** The runtime connection dropped. The console shows a transport error. Reconnect from the Edge Devices panel.

**The bug icon is grey.** You're not connected to a runtime. Open the Edge Devices screen and connect first.

## What's next

- **[Variables editor](../working-with-variables/variables-editor)**: turn the Debug column on for the variables you want to watch.
- **[Console & PLC Logs](../workspace-overview/console-debugging)**: read the runtime's own logs alongside the chart.
- **[Connecting to a vPLC](../connecting-to-runtimes)**: get the connection going.
