# Instance Management

Instances are the bridge between tasks and programs. While a task defines *when* code should execute, an instance defines *which* program to execute and *which task* drives it. Without at least one instance, your task runs on schedule but has nothing to execute.

## What Is an Instance?

An instance is a named reference that binds a **Program** POU to a **Task**. Each instance has three properties:

| Property | Description |
|----------|-------------|
| **Name** | A unique identifier for this instance (e.g., `instance0`). |
| **Program** | The Program POU to execute (selected from the project's program list). |
| **Task** | The task that drives this instance's execution schedule. |

When the runtime starts, it reads the instance definitions and wires each program to its assigned task. Every time the task fires, the runtime calls the programs assigned to it, in instance order.

## Accessing the Instances Editor

The Instances Editor is the third section of the Resource Editor, below the Tasks section. Open the **Resource** node in the Project Explorer to access it.

Like the Task Editor, it provides two views:

- **Table View** — A three-column interactive table.
- **Code View** — A text editor showing the full resource configuration.

## Table View

The instances table has three columns:

| Column | Description | Example |
|--------|-------------|---------|
| **Name** | The instance identifier. Must be unique. | `instance0` |
| **Program** | A dropdown listing all Program POUs in the project. | `MainProgram` |
| **Task** | A dropdown listing all tasks defined in the Tasks table. | `Task0` |

### Editing Cells

- **Name**: Click and type a new name. Names must be valid identifiers (letters, digits, underscores; starting with a letter or underscore).
- **Program**: Click to open a dropdown of all available Program POUs. Select the program you want this instance to execute.
- **Task**: Click to open a dropdown of all tasks. Select the task that should drive this instance.

## Creating Instances

### Using the Add Button

1. Click the **+** (plus) button in the Instances header.
2. A new row is inserted:
   - If a row is selected, the new instance is inserted below it with the same configuration.
   - If no row is selected, a new instance with default values is appended.
3. Defaults for a new instance:
   - **Name**: `instance0`
   - **Program**: empty (must be selected)
   - **Task**: empty (must be selected)
4. Select the desired Program and Task from the dropdowns.

### Using Code View

Switch to code view and add an instance line:

```
PROGRAM instance0 WITH Task0 : MainProgram;
```

The syntax is:

```
PROGRAM <instance_name> WITH <task_name> : <program_name>;
```

Switch back to table view to see the instance in the table.

## Managing Multiple Instances

You can create multiple instances to run different programs on different schedules.

### One Task, Multiple Programs

Assign several programs to the same task. They execute sequentially in instance order every time the task fires:

| Name | Program | Task |
|------|---------|------|
| `instance0` | `SafetyCheck` | `Task0` |
| `instance1` | `MotorControl` | `Task0` |
| `instance2` | `DataLogging` | `Task0` |

Execution order per cycle: `SafetyCheck` → `MotorControl` → `DataLogging`.

### Multiple Tasks, Multiple Programs

Distribute programs across different tasks for independent scheduling:

| Name | Program | Task |
|------|---------|------|
| `instance0` | `MotorControl` | `FastTask` |
| `instance1` | `TempRegulator` | `FastTask` |
| `instance2` | `HMIUpdate` | `SlowTask` |
| `instance3` | `Diagnostics` | `SlowTask` |

Here, `MotorControl` and `TempRegulator` run at `FastTask`'s interval (e.g., 10ms), while `HMIUpdate` and `Diagnostics` run at `SlowTask`'s interval (e.g., 500ms).

### Reordering Instances

Use the **up** and **down** arrow buttons to change instance order. This directly affects execution order when multiple instances share the same task.

To reorder:

1. Click an instance row to select it.
2. Click the up or down arrow button.
3. The instance moves one position.

### Deleting Instances

1. Click an instance row to select it.
2. Click the **−** (minus) button.
3. The instance is removed.

## Global Variables in the Resource

Above both the Tasks and Instances sections, the Resource Editor includes a **Global Variables** editor. Global variables are accessible from any POU in the project via the `External` variable class.

Global variables are commonly used for:

- Shared data between programs (e.g., a setpoint value used by both a control program and an HMI program).
- System-wide configuration parameters.
- Status flags visible to all POUs.

For full details, see [Global Variables](../working-with-variables/global-variables) and [Global Variables Editor](../working-with-variables/global-variables-editor).

## Code View Details

When you switch either the Tasks or Instances section to code view, the text editor shows the complete resource configuration:

```
TASK Task0(INTERVAL := T#20ms, PRIORITY := 0);
TASK Task1(INTERVAL := T#500ms, PRIORITY := 5);
PROGRAM instance0 WITH Task0 : MotorControl;
PROGRAM instance1 WITH Task0 : SafetyCheck;
PROGRAM instance2 WITH Task1 : DataLogger;
```

Key rules for the text format:

- `TASK` lines define tasks with `INTERVAL` and `PRIORITY` parameters.
- `PROGRAM` lines define instances with the `WITH` keyword linking to a task and `:` specifying the program.
- Each line ends with a semicolon.
- Order matters — instances assigned to the same task execute in the order they appear.

> **Tip:** When either the Task Editor or the Instances Editor is in code view, the other section is hidden to avoid conflicting edits. Switching back to table view parses the text and updates both tables.

## Complete Configuration Example

Here's a full resource configuration for an industrial conveyor system:

**Tasks:**

| Name | Triggering | Interval | Priority |
|------|-----------|----------|----------|
| `ControlTask` | Cyclic | `T#10ms` | 0 |
| `MonitorTask` | Cyclic | `T#200ms` | 5 |

**Instances:**

| Name | Program | Task |
|------|---------|------|
| `inst_safety` | `SafetyLogic` | `ControlTask` |
| `inst_conveyor` | `ConveyorControl` | `ControlTask` |
| `inst_monitor` | `SystemMonitor` | `MonitorTask` |

**Code view equivalent:**

```
TASK ControlTask(INTERVAL := T#10ms, PRIORITY := 0);
TASK MonitorTask(INTERVAL := T#200ms, PRIORITY := 5);
PROGRAM inst_safety WITH ControlTask : SafetyLogic;
PROGRAM inst_conveyor WITH ControlTask : ConveyorControl;
PROGRAM inst_monitor WITH MonitorTask : SystemMonitor;
```

Every 10 milliseconds, the runtime executes `SafetyLogic` then `ConveyorControl`. Every 200 milliseconds, it executes `SystemMonitor`.

## Troubleshooting

### Program dropdown is empty

You haven't created any Program POUs yet. Only POUs of type **Program** appear in the dropdown — Functions and Function Blocks are called from within programs, not assigned directly to tasks.

### Task dropdown is empty

You haven't created any tasks yet. Add at least one task in the Tasks section above before creating instances.

### Instance not executing

- Check that both the Program and Task fields are set (not empty).
- Verify the assigned task has a valid interval.
- Ensure the project has no errors that would prevent execution.

### Execution order seems wrong

Instance order determines execution sequence. Use the reorder arrows to adjust which program runs first within a shared task.

---

## What's Next?

With tasks and instances configured, your project is ready to be built and deployed. Continue to the [Programming Languages](../programming-languages/structured-text/st-basics) section to learn about writing program logic, or jump to [Building and Deploying](../building-deploying/project-compilation) if your programs are already written.
