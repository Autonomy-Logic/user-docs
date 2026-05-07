# Performance Optimization

In PLC programming, performance means completing all your logic within the configured scan cycle time. If your program takes longer than the task period allows, you get scan overruns — the runtime can't maintain deterministic timing, and your control system becomes unreliable. This guide covers how the scan cycle works, what causes performance problems, and practical techniques for writing efficient PLC code.

## Understanding the Scan Cycle

Every PLC scan cycle follows the same three-phase pattern:

1. **Read Inputs** — The runtime reads all physical and mapped inputs into the input image table
2. **Execute Program** — Your PLC program runs from top to bottom (or in task-assigned order)
3. **Write Outputs** — The runtime writes the output image table to physical and mapped outputs

The total time for all three phases is the **scan time**. Your task configuration sets the **scan period** (e.g., 50 ms). If the scan time exceeds the scan period, the runtime logs a warning and the next cycle starts late.

### Scan Time vs. Task Period

| Scenario | Effect |
|----------|--------|
| Scan time < Task period | Normal — runtime idles until next period |
| Scan time ≈ Task period | Borderline — any spike causes overrun |
| Scan time > Task period | Scan overrun — missed deadline, non-deterministic behavior |

> **Tip:** Keep your average scan time below 50% of the task period. This leaves headroom for worst-case spikes.

## Common Performance Problems

### 1. Unnecessary Computation Every Scan

Every line of code runs every scan cycle. If something only needs to run occasionally, gate it:

```iecst
(* Bad: recalculates every scan even when inputs haven't changed *)
result := SQRT(ABS(sensor1 * factor + offset)) / scale;

(* Good: only recalculate when input changes *)
IF sensor1 <> lPrevSensor1 THEN
    result := SQRT(ABS(sensor1 * factor + offset)) / scale;
    lPrevSensor1 := sensor1;
END_IF;
```

### 2. Large Loops

FOR loops that iterate over large arrays execute within a single scan. A loop over 10,000 elements blocks the entire cycle:

```iecst
(* Bad: processes entire buffer every scan *)
FOR i := 0 TO 9999 DO
    buffer[i] := buffer[i] * scale;
END_FOR;

(* Good: process a chunk per scan *)
FOR i := lChunkStart TO lChunkStart + 99 DO
    IF i <= 9999 THEN
        buffer[i] := buffer[i] * scale;
    END_IF;
END_FOR;
lChunkStart := lChunkStart + 100;
IF lChunkStart > 9999 THEN
    lChunkStart := 0;
END_IF;
```

### 3. Excessive Function Block Instances

Each Function Block instance uses memory and CPU time. Declaring 100 TON timers when you only use 10 wastes resources:

- Only declare instances you actually use
- If a timer is conditional, consider sharing a single instance with multiplexed inputs
- Remove unused variable declarations from the Variables Table

### 4. String Operations

String manipulation (concatenation, comparison, searching) is significantly slower than numeric operations. Minimize string processing in fast-scan tasks:

| Operation | Relative Cost |
|-----------|---------------|
| BOOL assignment | Baseline (1x) |
| INT arithmetic | ~1x |
| REAL arithmetic | ~2–5x |
| String comparison | ~10–50x |
| String concatenation | ~20–100x |

Move string operations to slower tasks (500 ms+) where possible.

### 5. Deep Nesting

Deeply nested IF statements and CASE structures increase complexity and can slow execution. Flatten where you can:

```iecst
(* Deep nesting — harder to read and optimize *)
IF cond1 THEN
    IF cond2 THEN
        IF cond3 THEN
            action := TRUE;
        END_IF;
    END_IF;
END_IF;

(* Flat — same logic, single evaluation *)
IF cond1 AND cond2 AND cond3 THEN
    action := TRUE;
END_IF;
```

## Task Configuration for Performance

### Assign POUs to Appropriate Tasks

Not all logic needs the fastest scan rate. Separating fast and slow logic into different tasks is the single most effective performance optimization:

| Task Period | Logic Type | Examples |
|-------------|-----------|---------|
| 10–20 ms | Safety, fast I/O | Emergency stop, high-speed counting, motion |
| 50–100 ms | Core control | PID loops, motor starters, sequences |
| 200–500 ms | Slow processes | Temperature control, level control |
| 1000+ ms | Non-critical | Diagnostics, data logging, HMI refresh |

### Avoid Running Everything in One Task

A single task running all POUs forces the fastest required rate on the slowest logic. If your emergency stop needs 10 ms but your temperature PID only needs 200 ms, running both at 10 ms wastes 95% of the PID's CPU time.

Split them:

```
Task: FastScan (10 ms)
  → Program: SafetyLogic
  → Program: HighSpeedIO

Task: NormalScan (100 ms)
  → Program: MotorControl
  → Program: SequenceLogic

Task: SlowScan (500 ms)
  → Program: TemperatureControl
  → Program: DataLogging
```

## Variable Usage Optimization

### Choose the Right Data Type

| Need | Use | Don't Use |
|------|-----|-----------|
| ON/OFF state | `BOOL` | `INT` with 0/1 |
| Small counter (0–255) | `SINT` or `USINT` | `DINT` |
| Normal counter | `INT` | `LINT` |
| Large counter | `DINT` | `REAL` |
| Fractional values | `REAL` | `LREAL` (unless precision needed) |
| Precise calculation | `LREAL` | `REAL` (if precision matters) |

Smaller data types use less memory and can reduce CPU cycles.

### Minimize Variable Scope

| Scope | Memory | Access Speed | Use For |
|-------|--------|-------------|---------|
| Local (`VAR`) | Stack/local | Fastest | Temporaries, counters, internal state |
| Global (`VAR_GLOBAL`) | Shared | Slower | Values shared between POUs |
| Located (`%I`, `%Q`, `%M`) | I/O image | Varies | Physical I/O mapping |

**Rule**: If a variable doesn't need to be global, make it local.

### Avoid Redundant Copies

```iecst
(* Bad: copies value through intermediaries *)
temp1 := iSensorValue;
temp2 := temp1;
scaledValue := temp2 * 0.1;

(* Good: use the value directly *)
scaledValue := iSensorValue * 0.1;
```

## Efficient Code Patterns

### Use CASE Instead of Chained IF/ELSIF for State Machines

CASE statements are typically faster than long IF/ELSIF chains because the runtime can use a jump table:

```iecst
(* Efficient: CASE with integer selector *)
CASE lStep OF
    0: (* Idle *)
        oOutput := FALSE;
    1: (* Running *)
        oOutput := TRUE;
    2: (* Complete *)
        oOutput := FALSE;
        lDone := TRUE;
END_CASE;
```

### Pre-compute Constants

If a value doesn't change at runtime, calculate it once or use a constant:

```iecst
(* Bad: recalculates every scan *)
circumference := diameter * 3.14159265;

(* Good: compute once *)
IF NOT lInitDone THEN
    lCircumference := diameter * 3.14159265;
    lInitDone := TRUE;
END_IF;
```

### Boolean Short-Circuit Evaluation

Structure conditions so the cheapest or most likely check comes first:

```iecst
(* If gEmergencyStop is usually FALSE, check it first *)
IF NOT gEmergencyStop AND (complexCalculation() > threshold) THEN
    (* Complex calculation only runs when not in E-stop *)
END_IF;
```

## Monitoring Performance

### Using the Console

The Autonomy Edge IDE console displays runtime messages including scan overrun warnings. Keep an eye on these during development:

- Filter the console to show **Warning** and **Error** level messages
- Watch for repeated overrun messages — they indicate sustained performance problems
- A single overrun during startup is normal; recurring ones need investigation

### Variable Monitoring

Use the IDE's variable monitoring panel to observe:

- **Timer `ET` values** — If timers show elapsed times jumping (not counting smoothly), scans may be overrunning
- **Counter increments** — Counters should increment by 1 per event, not skip values
- **Boolean toggles** — Rapid toggling of outputs can indicate logic issues

### Debugging Performance

To figure out which POU is causing slow scans:

1. **Temporarily disable** suspect POUs by commenting out their calls
2. **Observe** if scan overruns stop
3. **Re-enable** POUs one at a time to isolate the bottleneck
4. **Optimize** the identified POU using the techniques in this guide

## Performance Checklist

Use this checklist when reviewing your project:

| Check | Question |
|-------|----------|
| Task assignment | Is each POU in an appropriate-speed task? |
| Loop bounds | Are all FOR loops bounded to reasonable sizes? |
| String operations | Are strings processed in slow tasks only? |
| Unused variables | Are all declared variables actually used? |
| Data types | Is each variable the appropriate size? |
| Global scope | Are globals minimized? |
| Conditional execution | Is expensive logic gated by conditions? |
| FB instances | Are unused Function Block instances removed? |
| Constants | Are fixed values pre-computed? |
| Nesting depth | Are IF/CASE structures reasonably flat? |

## What's Next?

- [Project Organization](project-organization) — Structure your project for maintainability
- [Runtime Debugging](../troubleshooting/runtime-debugging) — Monitor your program in real-time
- [Task Configuration](../../openplc-editor/task-configuration/understanding-tasks) — Set up tasks with appropriate scan periods
