# Understanding Tasks

Tasks are the heartbeat of PLC execution. Without a task, your program code sits idle. No matter how well-written it is. A task defines the schedule that drives program execution: how often the code runs, at what priority, and under what conditions.

This page explains what tasks are and how they work conceptually. The next pages cover how to configure them in the IDE.

## What Is a Task?

In IEC 61131-3, a **task** is a scheduling mechanism that belongs to a **resource** within a **configuration**. The task doesn't contain logic itself. It controls *when* logic executes by triggering the programs assigned to it.

Think of a task as a metronome. It ticks at a defined rate, and every time it ticks, it runs its assigned programs in order. Without a task, the runtime has no schedule to follow and nothing executes.

## Cyclic Tasks

A **Cyclic** task executes at a fixed, repeating time interval. This is the standard mode for most PLC applications.

When you set a task to Cyclic with an interval of `T#20ms`:

1. The runtime starts a timer.
2. Every 20 milliseconds, the timer fires.
3. The runtime executes all programs assigned to this task, in the order their instances are defined.
4. When execution completes, the runtime waits for the next timer event.

### Choosing an Interval

The cycle time is one of the most important decisions in PLC programming. It directly affects:

- **Response time**: A shorter interval means the PLC reacts faster to input changes.
- **CPU load**: A shorter interval means more cycles per second, consuming more processing power.
- **Determinism**: If the programs take longer to execute than the cycle time, cycles get skipped (overrun), which can cause unpredictable behavior.

Common intervals by application type:

| Application | Typical Interval | Reason |
|------------|-----------------|--------|
| High-speed motion control | 1–5 ms | Needs sub-millisecond response |
| Motor control, safety | 5–20 ms | Standard for discrete control |
| Process control (temperature, pressure) | 20–100 ms | Physical processes change slowly |
| Data logging, HMI updates | 100 ms–1 s | Doesn't need fast response |
| Housekeeping, diagnostics | 1–10 s | Background tasks |

> **Tip:** Start with `T#20ms` for general-purpose control. Adjust faster if you need quicker response, or slower if you need to save CPU.

### Interval Format

Intervals use the IEC 61131-3 **TIME literal** format, prefixed with `T#`:

| Literal | Duration |
|---------|----------|
| `T#1ms` | 1 millisecond |
| `T#20ms` | 20 milliseconds |
| `T#100ms` | 100 milliseconds |
| `T#1s` | 1 second |
| `T#5s` | 5 seconds |
| `T#1m` | 1 minute |
| `T#1h` | 1 hour |
| `T#1h30m` | 1 hour and 30 minutes |

You can combine units: `T#2s500ms` means 2.5 seconds.

## Interrupt Tasks

An **Interrupt** task executes in response to an event rather than a fixed timer. The `interval` field for an interrupt task specifies the event source or condition name.

Interrupt tasks are less common than cyclic tasks but are useful for:

- Responding to hardware events (e.g., a specific input changing state).
- Processing communication events.
- Handling alarms or exceptions.

For most applications, cyclic tasks are the standard approach.

## Priority

Each task has a **priority** value from 0 to 100:

- **0** = highest priority (runs first)
- **100** = lowest priority (runs last)

Priority matters when multiple tasks are scheduled to execute at the same instant. The runtime executes higher-priority tasks first. For a single-task project, priority has no practical effect. Just use `0`.

When using multiple tasks:
- Assign the **lowest number** (highest priority) to time-critical tasks (safety, fast control loops).
- Assign **higher numbers** (lower priority) to less time-sensitive tasks (logging, HMI updates).

## The Execution Cycle

Here's what happens during each cycle of a cyclic task:

1. **Timer fires** at the defined interval.
2. **Input scan**: The runtime reads all physical inputs and updates input variables.
3. **Program execution**: Each program instance assigned to the task runs in order. Within each program, the logic executes from top to bottom (or left to right for graphical languages).
4. **Output update**: The runtime writes all output variables to physical outputs.

This "read inputs → execute logic → write outputs" pattern is called the **scan cycle**. It's the fundamental execution model for all PLCs.

## Multiple Tasks

You can define multiple tasks in a single resource. Common patterns:

**Two-rate pattern:**
- A fast task (e.g., 10ms) for time-critical control.
- A slow task (e.g., 500ms) for monitoring and logging.

**Safety separation:**
- A high-priority task for safety logic.
- A normal-priority task for production logic.

Each task runs independently on its own schedule. The runtime interleaves execution based on timing and priority.

## Default Task Configuration

When you create a new task in the IDE, it defaults to:

- **Name**: `Task0` (auto-generated, editable)
- **Triggering**: `Cyclic`
- **Interval**: `T#20ms`
- **Priority**: `0`

This is a sensible starting point for most applications.

---

## What's Next?

Learn how to create and manage tasks in the IDE: [Task Editor](task-editor).
