# Custom Libraries

As your projects grow and you build up reusable Function Blocks and Functions, you can organize them into custom libraries. Libraries let you package, share, and reuse your tested automation logic across multiple projects without copying code. This guide covers how to create, organize, and use custom function block libraries in Autonomy Edge.

## What is a Custom Library?

A custom library is a collection of related Function Blocks and Functions that you've written and want to reuse across projects. Think of it as a toolbox of pre-built components:

| Standard Libraries | Custom Libraries |
|-------------------|------------------|
| TON, TOF, TP (timers) | FB_MotorStarter, FB_ValveControl |
| CTU, CTD, CTUD (counters) | FB_PIDBasic, FB_RampGen |
| SR, RS (latches) | FC_ScaleAnalog, FC_Clamp |
| R_TRIG, F_TRIG (edges) | FB_AlarmHandler, FB_Sequence |

Standard libraries come built into the runtime. Custom libraries are the ones you build yourself.

## Creating a Custom Library

### Step 1: Design the Library Structure

Start by deciding what the library contains and how it's organized. Group related functionality together:

**Example: Motor Control Library**

| POU | Type | Purpose |
|-----|------|---------|
| `FB_MotorDOL` | Function Block | Direct-on-line motor starter |
| `FB_MotorReversing` | Function Block | Reversing motor starter with interlock |
| `FB_MotorSoftStart` | Function Block | Soft start with ramp-up time |
| `FC_MotorRunTime` | Function | Calculate total accumulated run time |
| `FB_MotorProtection` | Function Block | Overload and fault detection |

**Example: Process Control Library**

| POU | Type | Purpose |
|-----|------|---------|
| `FB_PID_Basic` | Function Block | Basic PID controller |
| `FB_RampGenerator` | Function Block | Linear ramp up/down |
| `FB_ThresholdAlarm` | Function Block | High/low alarm with hysteresis |
| `FB_DeviationAlarm` | Function Block | Alarm when value deviates from setpoint |
| `FC_ScaleAnalog` | Function | Scale raw analog to engineering units |
| `FC_Clamp` | Function | Clamp value to min/max range |

### Step 2: Write and Test Each POU

Create each Function Block and Function in a dedicated test project. Follow the design guidelines from [Code Reusability](../best-practices/code-reusability):

1. **Define clear interfaces** — Use `VAR_INPUT` for parameters, `VAR_OUTPUT` for status, `VAR` for internal state
2. **Avoid global variables** — The POU should be self-contained
3. **Use appropriate data types** — Match parameter types to their purpose
4. **Document the interface** — Add comments describing each input and output

```iecst
(* ============================================
   FB_ThresholdAlarm
   Library: ProcessControl
   Purpose: Generates alarm when value exceeds
            threshold with configurable hysteresis
   ============================================ *)
FUNCTION_BLOCK FB_ThresholdAlarm
  VAR_INPUT
    Value      : REAL;     (* Process value to monitor *)
    HighLimit  : REAL;     (* Upper alarm threshold *)
    LowLimit   : REAL;     (* Lower alarm threshold *)
    Hysteresis : REAL;     (* Dead band to prevent toggling *)
    Enable     : BOOL;     (* Enable alarm monitoring *)
  END_VAR

  VAR_OUTPUT
    HighAlarm  : BOOL;     (* TRUE when Value > HighLimit *)
    LowAlarm   : BOOL;     (* TRUE when Value < LowLimit *)
    Alarm      : BOOL;     (* TRUE when any alarm active *)
  END_VAR

  IF NOT Enable THEN
    HighAlarm := FALSE;
    LowAlarm := FALSE;
  ELSE
    (* High alarm with hysteresis *)
    IF Value > HighLimit THEN
      HighAlarm := TRUE;
    ELSIF Value < (HighLimit - Hysteresis) THEN
      HighAlarm := FALSE;
    END_IF;

    (* Low alarm with hysteresis *)
    IF Value < LowLimit THEN
      LowAlarm := TRUE;
    ELSIF Value > (LowLimit + Hysteresis) THEN
      LowAlarm := FALSE;
    END_IF;
  END_IF;

  Alarm := HighAlarm OR LowAlarm;
END_FUNCTION_BLOCK
```

### Step 3: Test Thoroughly

Before packaging a POU into a library, test it with:

| Test | What to Verify |
|------|----------------|
| Normal operation | Outputs match expected behavior for typical inputs |
| Boundary values | Behavior at minimum, maximum, and zero values |
| Edge cases | Rapid input changes, simultaneous conflicting inputs |
| Type limits | What happens with INT overflow, REAL precision limits |
| Multiple instances | Two instances with different parameters don't interfere |
| Different scan rates | Timing-dependent blocks work at various task periods |

> **Tip:** Use the Autonomy Edge debugger to monitor all inputs, outputs, and internal variables during testing. See [Runtime Debugging](../troubleshooting/runtime-debugging) for details.

### Step 4: Organize into a Library Project

Create a dedicated Autonomy Edge project for each library:

1. **Name the project** clearly: `Lib_MotorControl`, `Lib_ProcessControl`, `Lib_Utilities`
2. **Add all library POUs** to the project
3. **Create a test Program** that exercises all the library's POUs — this serves as both a test and a usage example
4. **Document each POU** with header comments including purpose, inputs, outputs, and example usage

### Step 5: Share and Reuse

To use library POUs in another project:

1. **Open the library project** and copy the desired POUs (Function Blocks and Functions)
2. **Paste them into the target project** as new POUs
3. **Declare instances** in the Variables Table of the Programs that will use them
4. **Call the instances** in your code just like standard library blocks

## Library Design Best Practices

### Consistent Naming Convention

Use a prefix that identifies the library:

| Library | Prefix | Example |
|---------|--------|---------|
| Motor Control | `MC_` or `FB_Motor` | `MC_DOLStarter`, `FB_MotorDOL` |
| Process Control | `PC_` or `FB_PID` | `PC_BasicPID`, `FB_PID_Basic` |
| Utilities | `UT_` or `FC_` | `UT_ScaleAnalog`, `FC_Clamp` |
| Alarm Management | `AL_` or `FB_Alarm` | `AL_Threshold`, `FB_AlarmLatch` |

### Version Your Libraries

Keep track of library versions to manage updates:

- Add a version comment at the top of each POU
- Maintain a changelog in the library project's description
- When updating a library POU, test thoroughly before deploying to production projects

### Design for Composition

Library blocks should work well together. Design them to be composed:

```iecst
(* Using Motor Control + Process Control + Alarm libraries together *)

(* Scale the analog input *)
rPressure := FC_ScaleAnalog(iPressRaw, 0, 32767, 0.0, 150.0);

(* Monitor for alarm conditions *)
PressAlarm(Value := rPressure, HighLimit := 120.0,
           LowLimit := 10.0, Hysteresis := 5.0, Enable := TRUE);

(* Control the pump based on pressure *)
PumpCtrl(Enable := NOT PressAlarm.HighAlarm,
         Start := iStartCmd, Stop := iStopCmd OR PressAlarm.HighAlarm,
         Feedback := iPumpFbk, FaultReset := iReset);
oPumpRun := PumpCtrl.CmdRun;
```

### Keep Dependencies Minimal

A library POU should not depend on:
- Global variables from a specific project
- Other custom library POUs (unless they're in the same library)
- Platform-specific features

If a block needs data from the environment, accept it through inputs rather than reading globals.

## Common Library Categories

Here are typical libraries that automation engineers build over time:

### I/O Processing Library

| POU | Purpose |
|-----|---------|
| `FB_AnalogInput` | Scale, filter, and validate an analog input |
| `FB_AnalogOutput` | Scale and clamp an analog output |
| `FB_DigitalDebounce` | Debounce a noisy digital input |
| `FC_ScaleLinear` | Linear scaling between two ranges |
| `FC_Clamp` | Clamp a value to min/max bounds |
| `FB_MovingAverage` | Smooth a noisy signal over N samples |

### Motor Control Library

| POU | Purpose |
|-----|---------|
| `FB_MotorDOL` | Direct-on-line start with feedback monitoring |
| `FB_MotorReversing` | Forward/reverse with interlock and changeover delay |
| `FB_MotorSoftStart` | Gradual ramp-up with configurable ramp time |
| `FB_MotorRunHours` | Track accumulated run time for maintenance |

### Alarm Management Library

| POU | Purpose |
|-----|---------|
| `FB_ThresholdAlarm` | High/low alarm with hysteresis |
| `FB_DeviationAlarm` | Alarm when value deviates from setpoint |
| `FB_RateAlarm` | Alarm when value changes too quickly |
| `FB_AlarmLatch` | Latching alarm that requires acknowledge |
| `FB_AlarmDelay` | Delayed alarm (ignore brief spikes) |

### Sequencing Library

| POU | Purpose |
|-----|---------|
| `FB_StepSequence` | Step-by-step sequencer with timeout |
| `FB_BatchPhase` | Batch process phase controller |
| `FB_Handshake` | Request/acknowledge handshake pattern |
| `FB_Interlock` | Multi-condition interlock check |

## Troubleshooting Library Issues

### Compilation Errors After Adding Library POUs

- **Duplicate names** — Make sure no library POU has the same name as an existing POU in the target project
- **Missing dependencies** — If a library FB uses another library FB internally, both must be present in the target project
- **Type conflicts** — Verify that custom data types used by the library are also defined in the target project

### Instance Behavior Differences

If a library block works in the test project but not in the target:

- **Check the task period** — Timing-dependent blocks (with timers) behave differently at different scan rates
- **Check input wiring** — Verify all required inputs are connected
- **Check initial values** — Some blocks require specific initialization

## What's Next?

- [Code Reusability](../best-practices/code-reusability) — Design principles for reusable Function Blocks
- [Standard Function Blocks Reference](../../reference/function-blocks) — Quick reference for built-in blocks
- [Project Organization](../best-practices/project-organization) — Structure projects for maintainability
