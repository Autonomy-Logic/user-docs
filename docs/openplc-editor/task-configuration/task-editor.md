# Task Editor

The Task Editor is the primary interface for creating, configuring, and managing tasks in the Autonomy Edge IDE. It lives inside the Resource Editor and provides both a table-based view for quick edits and a text-based view for direct code entry.

## Opening the Resource Editor

To access the Task Editor, open the **Resource** node in the Project Explorer tree. The Resource Editor opens as a tab and is divided into three sections, top to bottom:

1. **Global Variables** — Variables accessible across all POUs.
2. **Tasks** — The Task Editor, covered on this page.
3. **Instances** — The Instances Editor, where you assign programs to tasks.

## Task Editor Layout

The Task Editor section has a header bar with:

- A label showing "Tasks" (in table view) or "Text editor" (in code view).
- **Action buttons** for manipulating rows (visible only in table view).
- **View toggle** icons on the right to switch between table and code views.

### Table View

The table view is the default and most intuitive way to manage tasks. It displays a four-column table:

| Column | Description | Example |
|--------|-------------|---------|
| **Name** | The task identifier. Must be unique within the resource. | `Task0` |
| **Triggering** | How the task is activated. Select `Cyclic` or `Interrupt` from a dropdown. | `Cyclic` |
| **Interval** | The execution period (for Cyclic tasks) or event source (for Interrupt tasks). | `T#20ms` |
| **Priority** | Numeric priority from 0 (highest) to 100 (lowest). | `0` |

Each cell is editable — click on any cell to modify its value directly. The Name and Priority columns accept free text input, while Triggering provides a dropdown selector.

### Code View

Click the code icon (to the right of the table icon) to switch to a text-based editor. The code view uses a Monaco editor and displays the complete resource configuration — both tasks and instances — in a textual format:

```
TASK Task0(INTERVAL := T#20ms, PRIORITY := 0);
TASK Task1(INTERVAL := T#100ms, PRIORITY := 5);
PROGRAM instance0 WITH Task0 : MainProgram;
PROGRAM instance1 WITH Task1 : MonitorProgram;
```

When you switch from code view back to table view, the IDE parses the text and applies changes. If there's a syntax error, you'll see an error message and the switch is prevented until the code is corrected.

> **Tip:** The code view shows both tasks and instances in a single text block. Editing in code view modifies both the Tasks table and the Instances table simultaneously.

## Creating Tasks

### Using the Add Button

1. In table view, click the **+** (plus) button in the header.
2. A new task row is inserted:
   - If a row is selected, the new task is inserted below it and copies the selected task's configuration.
   - If no row is selected, a new task with default values is appended at the end.
3. Defaults for a new task:
   - **Name**: `Task0`
   - **Triggering**: `Cyclic`
   - **Interval**: `T#20ms`
   - **Priority**: `0`
4. Edit the name and other fields as needed.

### Using Code View

Switch to code view and type a new `TASK` line:

```
TASK MyFastTask(INTERVAL := T#5ms, PRIORITY := 0);
```

Switch back to table view to see the task appear in the table.

## Editing Tasks

### Changing the Name

Click the Name cell and type a new name. Task names must be valid IEC 61131-3 identifiers: start with a letter or underscore, followed by letters, digits, or underscores. Names must be unique within the resource.

### Changing the Triggering Mode

Click the Triggering cell to open a dropdown with two options:

- **Cyclic** — The task runs repeatedly at the interval specified.
- **Interrupt** — The task runs in response to an external event.

For most applications, use Cyclic. See [Understanding Tasks](understanding-tasks) for a detailed explanation of both modes.

### Setting the Interval

Click the Interval cell and type a time literal:

```
T#20ms     (* 20 milliseconds — standard for discrete control *)
T#100ms    (* 100 milliseconds — process control *)
T#1s       (* 1 second — slow monitoring *)
```

The interval field accepts any valid IEC 61131-3 TIME literal. See the [interval format table](understanding-tasks#interval-format) for the full syntax.

### Setting the Priority

Click the Priority cell and enter a number between 0 and 100:

- **0** = highest priority
- **100** = lowest priority

For single-task projects, priority doesn't matter — just use `0`.

## Reordering Tasks

Use the **up arrow** and **down arrow** buttons in the header to move the selected task row up or down. Task order can matter when multiple tasks share the same interval — the runtime processes them in the order defined.

To reorder:

1. Click a task row to select it (it becomes highlighted).
2. Click the up or down arrow button.
3. The row moves one position in the corresponding direction.

## Deleting Tasks

1. Click a task row to select it.
2. Click the **−** (minus) button in the header.
3. The task is immediately removed.

> **Tip:** Deleting a task does not automatically remove instances that reference it. Clean up the Instances table after deleting a task to avoid orphan references.

## Undo and Redo

Every action in the Task Editor — creating, editing, deleting, reordering — is tracked in the project's undo history:

| Action | Shortcut |
|--------|----------|
| Undo | `Ctrl+Z` (Windows/Linux) or `Cmd+Z` (macOS) |
| Redo | `Ctrl+Y` (Windows/Linux) or `Cmd+Shift+Z` (macOS) |

This works in both table view and code view.

## Common Task Configurations

### Single-Task Project (Most Common)

For straightforward applications, one task is enough:

| Name | Triggering | Interval | Priority |
|------|-----------|----------|----------|
| `Task0` | Cyclic | `T#20ms` | 0 |

Then create a single instance that assigns your main program to `Task0`. This is the default setup.

### Dual-Rate Configuration

For projects that need both fast control and slower monitoring:

| Name | Triggering | Interval | Priority |
|------|-----------|----------|----------|
| `FastControl` | Cyclic | `T#10ms` | 0 |
| `SlowMonitor` | Cyclic | `T#500ms` | 10 |

Assign time-critical programs to `FastControl` and monitoring programs to `SlowMonitor`.

### Safety-Critical Configuration

Separate safety logic from normal operations:

| Name | Triggering | Interval | Priority |
|------|-----------|----------|----------|
| `SafetyTask` | Cyclic | `T#5ms` | 0 |
| `ProductionTask` | Cyclic | `T#20ms` | 5 |
| `DiagnosticsTask` | Cyclic | `T#1s` | 20 |

Higher priority (lower number) ensures safety logic always runs first.

## Troubleshooting

### "Syntax error" when switching from code view to table view

The text in the code editor doesn't parse correctly. Common causes:

- Missing semicolons at the end of lines.
- Invalid time literal format (use `T#` prefix, e.g., `T#20ms` not `20ms`).
- Missing the `INTERVAL :=` or `PRIORITY :=` syntax.

Fix the code and try switching again.

### Tasks not executing at the expected rate

- Check that the Interval value is correct. `T#20ms` is 20 milliseconds, not 20 seconds.
- Ensure the program logic fits within the cycle time. If your program takes 30ms to execute but the interval is 20ms, cycles will overrun.

### Duplicate task names

Each task must have a unique name. The IDE will reject duplicate names with an error message.

---

## What's Next?

Now that you can create and configure tasks, learn how to assign programs to them: [Instance Management](instance-management).
