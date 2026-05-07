# Console & Debugging

The Console Panel is the bottom section of the IDE workspace. It shows real-time output from the build process, runtime interactions, and search operations. This is your go-to place for understanding what's happening when you compile, deploy, and run your PLC programs.

## Console Tab

The **Console** tab is the primary output area. It shows timestamped log messages generated during:

- **Compilation** — When you click Compile, every step of the build process is logged here with progress updates.
- **Runtime control** — Start/stop messages, connection status changes, and runtime errors.
- **Validation** — Warnings about server IP mismatches, validation errors for Python or C/C++ POUs, and other pre-compilation checks.

Each log entry includes:

- A **timestamp** (configurable format)
- A **severity level** with color coding:
  - **Info** (blue) — Normal progress messages
  - **Warning** (yellow) — Non-fatal issues that may need attention
  - **Error** (red) — Failures that stop the build or indicate a problem
  - **Debug** (gray) — Detailed diagnostic output

### Filtering Logs

Click the **Filters** button (top-right corner of the Console tab) to access filtering options:

- **Search** — Type to filter logs in real-time. Only matching entries are shown.
- **Log Levels** — Toggle switches for Debug, Info, Warning, and Error. Turn off a level to hide those messages.
- **Timestamp Format** — Choose between full date/time (DD-MM-YY HH:MM:SS), time only (HH:MM:SS), or no timestamp.

An indicator appears on the Filters button when any non-default filter is active.

### Exporting Logs

Click the **Export** button (download icon) to save the currently displayed logs. Supported formats:

- **.txt** — Plain text with timestamps and severity levels.
- **.csv** — Comma-separated values for spreadsheet analysis.
- **.json** — Structured JSON array with timestamp, level, and message fields.

The file downloads automatically with a timestamped name.

### Clearing Logs

Click the **Clear** button (trash icon) to remove all log entries. This is useful before starting a new build to get a clean view.

### Auto-Scroll

The Console automatically scrolls to the latest entry as new messages arrive. If you scroll up to review earlier messages, auto-scroll pauses so you can read without the view jumping. Scroll back to the bottom to resume.

## Search Tab

The **Search** tab appears when you perform a search using the Activity Bar's Search button. It shows matching results from across your project with links to jump directly to the matching element.

## PLC Logs Tab

The **PLC Logs** tab appears when you're connected to a device. It shows live logs from the running PLC program. This is separate from the Console tab — the Console shows IDE-side messages (compilation, upload), while PLC Logs show output from the PLC process itself.

The PLC Logs tab has its own filtering controls and Clear button.

## Using the Console During Development

Here's a typical workflow:

1. **Clear the console** before compiling for a fresh view.
2. **Click Compile** and watch the progress in the Console tab.
3. **If errors occur**, read the error messages. Common issues include:
   - Syntax errors in Structured Text or Instruction List code
   - Undeclared variables or type mismatches
   - Python or C/C++ validation failures
4. **After successful compilation**, wait for the "Compilation completed successfully" message.
5. **Start the PLC** and switch to the PLC Logs tab to monitor runtime behavior.

> **Tip:** You can resize or collapse the Console Panel to maximize editor space. Drag the border between the Editor Area and Console Panel to adjust the height.

## Troubleshooting

### I don't see the PLC Logs tab

The PLC Logs tab only appears when you're connected to a device. Check your connection status in the Orchestrators panel.

### Console output is too noisy

Use the Filters panel to hide log levels you don't need. For example, turn off Debug to see only Info, Warning, and Error messages.

### I need to share logs with someone

Use the Export button to save logs as TXT, CSV, or JSON. The export includes only the currently filtered view, so you can narrow it down before exporting.

---

## What's Next?

Now that you know the workspace, learn about the core building blocks of IEC 61131-3 programs: [Program Organization Units (POUs)](../iec-concepts/pous).
