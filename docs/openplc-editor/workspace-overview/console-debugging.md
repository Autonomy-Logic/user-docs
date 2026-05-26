# Console & PLC Logs

The strip at the bottom of the editor has two distinct streams: **Console** (messages from the editor itself: build progress, validation, connection state, debugger transport) and **PLC Logs** (messages streamed back from a connected vPLC).

The console always exists. The PLC Logs tab only appears once you're connected to a Runtime v4 vPLC.

## Console

The Console tab shows every message the editor generates during a session:

- **Compilation** progress (one entry per build step), with the final success or error summary.
- **Library** and **package manager** notices (when you add or remove a library).
- **Runtime connection** lifecycle (login, MD5 check, transport selection).
- **Debugger** state changes.
- **EtherCAT** scan and slave configuration notices.
- **Validation** errors (e.g., a Python block whose variables don't match its struct format).

Each entry carries a level: `info`, `warning`, `error`. The console auto-scrolls to the latest entry as messages arrive; scroll up to pause auto-scroll and read older entries.

### Filtering

Click **Filters** in the console's top-right corner.

- **Search**: free-text match across the message column. Updates as you type.
- **Levels**: toggle `info` / `warning` / `error` independently.
- **Timestamp format**: full date+time, time only, or none.

A small dot on the **Filters** button indicates an active non-default filter.

### Exporting

Click the download icon to save the currently filtered view as `.txt`, `.csv`, or `.json`. The file name carries an ISO timestamp.

### Clearing

The **Clear console** button at the right end empties the view. Past entries are gone (export first if you need to keep them).

### Clicking through compile errors

Compile errors in the console are clickable. Clicking one jumps to the offending source line in the appropriate POU body. This is the fastest way to fix a build failure.

## PLC Logs

Visible only when the editor is connected to a Runtime v4 vPLC (the runtime exposes a WebSocket log stream).

The PLC Logs tab is the runtime's own log feed, separate from anything the editor generates. Use it to see what your PLC program is actually doing at runtime, `printf` output from C++ blocks, exceptions from Python blocks, periodic status messages, etc.

It has the same Filters / Download / Clear controls as the Console.

## A typical build / run / debug session

1. Clear the console for a fresh view.
2. Click the **Build options** icon in the activity bar, then choose **Build & Upload** (or **Build** then **Start PLC** separately).
3. Watch the console: each compilation step logs a line. On error, click the message to jump to the source.
4. After upload completes, click **Play** to start the PLC.
5. Switch to **PLC Logs** to monitor runtime output.
6. Open the **Debugger** to watch live variable values on a time-series chart.

## What's next

- Author code: **[Programming Languages](../programming-languages/structured-text/st-basics)**.
- Watch live variables: **[Debugger](../building-deploying/debugger)**.
- Get connected: **[Connecting to a vPLC](../connecting-to-runtimes)**.
