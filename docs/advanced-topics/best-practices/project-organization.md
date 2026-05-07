# Project Organization

A well-organized project is easier to maintain, debug, and extend. As your Autonomy Edge projects grow. More POUs, more variables, more communication protocols. A consistent structure prevents confusion and saves you time. This guide covers naming conventions, POU organization, and structural patterns that scale.

## Naming Conventions

Clear, consistent naming is the single most impactful thing you can do for maintainability. When you (or a colleague) come back to a project months later, good names eliminate guesswork.

### Variable Naming

| Convention | Example | When to Use |
|------------|---------|-------------|
| Prefix by scope | `gEmergencyStop` (global), `iSensorTemp` (input), `oValveOpen` (output) | Distinguishes variable class at a glance |
| Prefix by data type | `bMotorRunning` (BOOL), `rSetpoint` (REAL), `nCounter` (INT) | Useful when type matters for logic clarity |
| CamelCase | `ConveyorSpeed`, `TankLevel` | Readable for multi-word names |
| Snake_case | `conveyor_speed`, `tank_level` | Alternative style. Pick one and stay consistent |

**Recommended prefixes by variable class:**

| Prefix | Class | Example |
|--------|-------|---------|
| `i` or `in_` | Input | `iStartButton`, `in_pressure` |
| `o` or `out_` | Output | `oMotorRelay`, `out_valve` |
| `g` or `gl_` | Global | `gSystemMode`, `gl_alarm_active` |
| `l` or (none) | Local | `lStepIndex`, `counter` |
| `c` or `k` | Constant | `cMaxTemp`, `kDefaultSpeed` |

### POU Naming

Name your Programs, Function Blocks, and Functions to clearly convey their purpose:

| POU Type | Convention | Examples |
|----------|------------|---------|
| Program | Describes the process or machine area | `MainControl`, `ConveyorLine1`, `TankFilling` |
| Function Block | Describes the reusable behavior | `FB_MotorStarter`, `FB_PIDController`, `FB_Debounce` |
| Function | Describes the computation | `FC_ScaleAnalog`, `FC_Clamp`, `FC_TempConvert` |

> **Tip:** Use a `FB_` prefix for Function Blocks and `FC_` for Functions to distinguish them from Programs. Avoid generic names like `Control1` or `Test`. They become meaningless fast.

### Task and Instance Naming

| Element | Convention | Example |
|---------|------------|---------|
| Task | Describes timing or purpose | `FastScan_10ms`, `SlowScan_100ms`, `CommTask` |
| FB Instance | Describes the specific use | `PumpMotor_Starter`, `Tank1_LevelPID` |

## POU Organization Strategies

### Separation by Function

Organize POUs by what they do, not when they were created:

| Category | Purpose | Example POUs |
|----------|---------|--------------|
| **Control Logic** | Core process control | `MainSequence`, `FB_MotorStarter`, `FB_ValveControl` |
| **I/O Processing** | Signal conditioning and scaling | `FC_ScaleAnalog`, `FB_Debounce`, `FB_FilterInput` |
| **Communication** | Protocol handling | `FB_ModbusClient`, `FB_DataExchange` |
| **Alarms & Safety** | Fault detection and response | `FB_AlarmHandler`, `FB_SafetyMonitor` |
| **Utilities** | Reusable helpers | `FC_Clamp`, `FC_RampGenerator`, `FC_BitPack` |
| **HMI Interface** | Data for display and operator input | `FB_HMI_DataManager`, `FC_FormatDisplay` |

### Single Responsibility Principle

Each POU should do one thing well. If a Function Block handles motor control, alarm monitoring, and data logging all at once. Split it up:

```
(* Bad: one monolithic block *)
FB_DoEverything
  - controls motor
  - monitors temperature
  - logs data
  - manages alarms

(* Good: focused blocks composed together *)
FB_MotorControl      (* handles start/stop/speed *)
FB_TempMonitor       (* monitors temperature thresholds *)
FB_DataLogger        (* logs process values *)
FB_AlarmHandler      (* manages alarm states *)
```

A Program then composes these blocks:

```iecst
MotorCtrl(Enable := gSystemReady, Speed := gSpeedSetpoint);
TempMon(SensorValue := iTemp1, HighLimit := 85.0);
AlarmMgr(TempAlarm := TempMon.HighAlarm, MotorFault := MotorCtrl.Fault);
```

### Layered Architecture

For complex projects, consider a layered approach where each layer only calls the one below it:

| Layer | Responsibility | Example |
|-------|----------------|---------|
| **Coordination** | Sequences, modes, state machines | `MainSequence`, `ModeSelector` |
| **Control** | PID loops, motor starters, valve logic | `FB_PIDLoop`, `FB_MotorStarter` |
| **I/O Abstraction** | Scaling, filtering, debouncing | `FB_AnalogInput`, `FB_DigitalDebounce` |
| **Hardware** | Located variables, HAL mapping | Direct `%I` and `%Q` references |

This separation means you can test control logic with simulated I/O, or swap hardware platforms without touching the control layer.

## Variable Management

### Group Related Variables

When declaring variables in the Variables Table, group them logically rather than alphabetically or by creation order:

```iecst
(* Inputs - Sensors *)
iTemp_Zone1      : REAL;
iTemp_Zone2      : REAL;
iPress_Main      : REAL;

(* Inputs - Operator *)
iStartButton     : BOOL;
iStopButton      : BOOL;
iModeSelect      : INT;

(* Outputs - Actuators *)
oHeater_Zone1    : BOOL;
oHeater_Zone2    : BOOL;
oPump_Main       : BOOL;

(* Internal - State *)
lCurrentStep     : INT;
lCycleCount      : DINT;
```

### Minimize Global Variables

Global variables are shared across all POUs. Convenient, but risky in larger projects:

- **Use globals for**: System-wide state (emergency stop, system mode), shared process values that multiple POUs need
- **Avoid globals for**: Internal counters, temporary calculations, POU-specific state
- **Rule of thumb**: If a variable is only used in one POU, make it local

### Initialize Everything

Always set initial values for your variables. Uninitialized variables default to zero, but relying on implicit defaults makes code harder to understand and can hide bugs:

| Data Type | Good Default | Why |
|-----------|-------------|-----|
| `BOOL` | `FALSE` | Outputs off at startup |
| `INT` / `DINT` | `0` | Clear numeric state |
| `REAL` | `0.0` | Explicit floating-point |
| `TIME` | `T#0s` | No residual timing |

## Task Configuration Tips

### Match Scan Rate to Requirements

Not all logic needs the fastest possible rate. Assign POUs to tasks based on their actual timing needs:

| Task Period | Typical Use | Examples |
|-------------|-------------|---------|
| 10–20 ms | Fast I/O, motion, safety | Emergency stop, high-speed counting |
| 50–100 ms | Standard control loops | PID loops, motor control, sequencing |
| 200–500 ms | Slow processes, communication | Temperature control, data logging |
| 1000+ ms | HMI updates, diagnostics | Display refresh, alarm history |

Running everything at 10 ms wastes CPU and can cause scan overruns. See [Performance Optimization](performance-optimization) for more on scan cycle management.

### One Program Per Task (Usually)

Each task should typically execute one main Program. If you need multiple Programs in one task, make sure they have no order-dependent interactions. Execution order within a task isn't always guaranteed.

## Documentation Within Projects

### Commenting Strategy

```iecst
(* ============================================
   Program: TankFilling
   Purpose: Manages the fill sequence for Tank 1
   Author:  J. Smith
   Date:    2025-03-01
   ============================================ *)

(* State machine for fill sequence *)
CASE lFillStep OF
    0:  (* IDLE - waiting for start command *)
        oInletValve := FALSE;
        IF iStartFill AND NOT iHighLevel THEN
            lFillStep := 1;
        END_IF;

    1:  (* FILLING - inlet valve open *)
        oInletValve := TRUE;
        IF iHighLevel THEN
            lFillStep := 2;  (* Tank full *)
        END_IF;

    2:  (* COMPLETE - close valve, signal done *)
        oInletValve := FALSE;
        oFillComplete := TRUE;
END_CASE;
```

**When to comment:**
- At the top of each POU: purpose, author, date
- At each state in a state machine
- For non-obvious calculations or magic numbers
- When a workaround is needed for hardware quirks

**When NOT to comment:**
- Obvious assignments (`counter := counter + 1;` doesn't need one)
- Every single line. Over-commenting adds noise

## Project Templates

When starting new projects, set up a standard template with:

1. **A main coordination Program** that manages system modes (Manual, Auto, Fault)
2. **Standard FB instances** for common patterns (motor starters, valve controllers)
3. **Consistent variable naming** following your team's convention
4. **Pre-configured tasks** with appropriate scan rates
5. **A global variables section** for system-wide state (emergency stop, mode, heartbeat)

Reusing a template keeps things consistent across projects and cuts setup time.

## What's Next?

- [Code Reusability](code-reusability): Design Function Blocks for maximum reuse
- [Performance Optimization](performance-optimization): Optimize scan cycles and variable usage
- [Task Configuration](../../openplc-editor/task-configuration/understanding-tasks): Configure tasks and assign Programs
