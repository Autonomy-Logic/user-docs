# Code Reusability

Writing logic once and reusing it across projects saves time and reduces bugs. Function Blocks are the primary vehicle for reusable code in PLC programming. This guide covers how to design them for maximum reuse, common patterns for modular control logic, and strategies for building your own library of components.

## Why Reusability Matters

You'll encounter the same control patterns over and over: motor start/stop, analog scaling, PID regulation, alarm management, state sequencing. Writing these from scratch every time wastes effort and introduces inconsistency. A well-designed reusable Function Block:

- **Reduces development time**: Instantiate a tested block instead of rewriting logic
- **Improves reliability**: A block tested in one project carries that confidence to the next
- **Simplifies maintenance**: Fix a bug once and all instances benefit
- **Standardizes behavior**: Every motor starter works the same way across all projects

## Function Blocks as the Unit of Reuse

### Functions vs. Function Blocks

| Feature | Function (FC) | Function Block (FB) |
|---------|---------------|---------------------|
| Internal state | None. Stateless | Yes. Retains values between calls |
| Multiple outputs | No. Single return value | Yes. Multiple output variables |
| Instances | Not needed | Each use requires a named instance |
| Typical use | Pure calculations | Stateful control logic |

**Use Functions** for stateless computations: scaling, clamping, unit conversion, math.

**Use Function Blocks** for anything that needs to remember state between scan cycles: timers, counters, motor controllers, state machines, PID loops.

### Anatomy of a Reusable Function Block

A well-designed Function Block follows a consistent pattern:

```iecst
FUNCTION_BLOCK FB_MotorStarter
  VAR_INPUT
    Enable      : BOOL;     (* Permission to run *)
    Start       : BOOL;     (* Start command *)
    Stop        : BOOL;     (* Stop command *)
    FaultReset  : BOOL;     (* Reset after fault *)
    MaxRunTime  : TIME;     (* Auto-stop after duration; T#0s = disabled *)
  END_VAR

  VAR_OUTPUT
    Running     : BOOL;     (* Motor is running *)
    Fault       : BOOL;     (* Fault condition active *)
    RunTime     : TIME;     (* Accumulated run time *)
  END_VAR

  VAR
    lRunTimer   : TON;      (* Internal run timer *)
    lLatched    : BOOL;     (* Start latch *)
  END_VAR
```

**Key design principles:**

1. **Inputs are parameters**: Everything the block needs comes through `VAR_INPUT`
2. **Outputs are status**: The block exposes its state through `VAR_OUTPUT`
3. **Internal state is hidden**: `VAR` holds implementation details the caller doesn't need
4. **No globals**: The block never reads or writes global variables directly

### Designing the Interface

The interface (inputs and outputs) is the contract between your block and its callers. Get this right and the block becomes easy to use everywhere.

**Input design guidelines:**

| Guideline | Example | Reason |
|-----------|---------|--------|
| Use meaningful names | `Enable`, not `IN1` | Self-documenting |
| Provide defaults via docs | `MaxRunTime: T#0s = disabled` | Caller knows safe defaults |
| Separate concerns | `Start` and `Stop` as separate inputs | Matches real-world wiring |
| Use BOOL for commands | `Start : BOOL` | Standard PLC pattern |
| Use appropriate types | `Setpoint : REAL`, not `Setpoint : INT` | Avoids precision loss |

**Output design guidelines:**

| Guideline | Example | Reason |
|-----------|---------|--------|
| Expose status, not internals | `Running : BOOL` | Caller doesn't need latch details |
| Include fault/error status | `Fault : BOOL` | Caller can react to problems |
| Provide diagnostic values | `RunTime : TIME` | Useful for monitoring and logging |

## Common Reusable Patterns

### Pattern 1: Motor Starter with Interlock

A motor starter that respects an enable condition and detects faults:

```iecst
FUNCTION_BLOCK FB_MotorStarter
  VAR_INPUT
    Enable     : BOOL;
    Start      : BOOL;
    Stop       : BOOL;
    Feedback   : BOOL;     (* Motor contactor feedback *)
    FaultReset : BOOL;
  END_VAR

  VAR_OUTPUT
    CmdRun     : BOOL;     (* Command to contactor *)
    Running    : BOOL;     (* Confirmed running *)
    Fault      : BOOL;     (* Feedback mismatch *)
  END_VAR

  VAR
    lLatched   : BOOL;
    lFbkTimer  : TON;      (* Feedback timeout *)
  END_VAR

  (* Start/Stop latch *)
  IF Start AND Enable AND NOT Fault THEN
    lLatched := TRUE;
  END_IF;
  IF Stop OR NOT Enable THEN
    lLatched := FALSE;
  END_IF;

  CmdRun := lLatched;

  (* Feedback monitoring *)
  lFbkTimer(IN := CmdRun AND NOT Feedback, PT := T#3s);
  IF lFbkTimer.Q THEN
    Fault := TRUE;
    lLatched := FALSE;
  END_IF;

  Running := CmdRun AND Feedback;

  (* Fault reset *)
  IF FaultReset AND NOT CmdRun THEN
    Fault := FALSE;
  END_IF;
END_FUNCTION_BLOCK
```

**Usage in a Program:**

```iecst
Pump1(Enable := gSystemReady, Start := iStartBtn, Stop := iStopBtn,
      Feedback := iPump1Fbk, FaultReset := iResetBtn);
oPump1Run := Pump1.CmdRun;

Pump2(Enable := gSystemReady, Start := iAutoStart, Stop := iAutoStop,
      Feedback := iPump2Fbk, FaultReset := iResetBtn);
oPump2Run := Pump2.CmdRun;
```

Two pumps, same logic, no duplication.

### Pattern 2: Analog Scaling Function

A stateless Function for converting raw analog values to engineering units:

```iecst
FUNCTION FC_ScaleAnalog : REAL
  VAR_INPUT
    RawValue   : INT;      (* Raw ADC value *)
    RawMin     : INT;      (* e.g., 0 for 4mA *)
    RawMax     : INT;      (* e.g., 32767 for 20mA *)
    EngMin     : REAL;     (* e.g., 0.0 for 0 PSI *)
    EngMax     : REAL;     (* e.g., 100.0 for 100 PSI *)
  END_VAR

  IF RawMax <> RawMin THEN
    FC_ScaleAnalog := EngMin +
      (INT_TO_REAL(RawValue - RawMin) / INT_TO_REAL(RawMax - RawMin))
      * (EngMax - EngMin);
  ELSE
    FC_ScaleAnalog := EngMin;
  END_IF;
END_FUNCTION
```

**Usage:**
```iecst
rPressure := FC_ScaleAnalog(iPress_Raw, 0, 32767, 0.0, 150.0);
rTemperature := FC_ScaleAnalog(iTemp_Raw, 0, 32767, -20.0, 120.0);
rLevel := FC_ScaleAnalog(iLevel_Raw, 0, 32767, 0.0, 5.0);
```

### Pattern 3: Edge Detection Wrapper

A block that detects both rising and falling edges of a signal:

```iecst
FUNCTION_BLOCK FB_EdgeDetect
  VAR_INPUT
    Signal     : BOOL;
  END_VAR

  VAR_OUTPUT
    Rising     : BOOL;     (* TRUE for one scan on 0->1 *)
    Falling    : BOOL;     (* TRUE for one scan on 1->0 *)
  END_VAR

  VAR
    lPrev      : BOOL;
  END_VAR

  Rising := Signal AND NOT lPrev;
  Falling := NOT Signal AND lPrev;
  lPrev := Signal;
END_FUNCTION_BLOCK
```

### Pattern 4: State Machine Template

A reusable pattern for sequencing operations:

```iecst
FUNCTION_BLOCK FB_Sequence
  VAR_INPUT
    Start      : BOOL;
    Abort      : BOOL;
    Reset      : BOOL;
  END_VAR

  VAR_OUTPUT
    Step       : INT;      (* Current step number *)
    Busy       : BOOL;     (* Sequence in progress *)
    Done       : BOOL;     (* Sequence complete *)
    Error      : BOOL;     (* Sequence aborted *)
  END_VAR

  VAR
    lStepTimer : TON;
  END_VAR

  IF Reset THEN
    Step := 0;
    Done := FALSE;
    Error := FALSE;
  END_IF;

  IF Abort AND Busy THEN
    Step := 0;
    Error := TRUE;
  END_IF;

  Busy := (Step > 0) AND NOT Done AND NOT Error;
END_FUNCTION_BLOCK
```

Callers extend this by adding step logic in a CASE statement that references `Step`.

## Composition Over Complexity

### Building Complex Behavior from Simple Blocks

Instead of one big block that does everything, compose simple ones:

```iecst
(* Compose a "Smart Valve" from simple building blocks *)
ValveEdge(Signal := iValveCmd);          (* Edge detection *)
ValveDebounce(IN := iValveFbk, PT := T#100ms);  (* Debounce feedback *)
ValveCtrl(Enable := gReady,
          Open := ValveEdge.Rising,
          Close := ValveEdge.Falling,
          Feedback := ValveDebounce.Q,
          FaultReset := iReset);
oValveOut := ValveCtrl.CmdOpen;
```

Each block is simple and testable on its own. Together, they give you sophisticated valve control with edge detection, debounce, and fault monitoring.

### When to Create a New Block

Create a new Function Block when:

- You're copying and pasting code between POUs
- The same pattern appears in three or more places
- A piece of logic has a clear, well-defined responsibility
- You need multiple instances with different parameters

**Don't** create a block for:
- One-off logic specific to a single application
- Trivial operations (a single assignment or comparison)
- Logic that's still changing frequently. Stabilize it first, then extract

## Designing for Different Contexts

A truly reusable block works across different applications without modification. Design for flexibility:

### Parameterize, Don't Hardcode

```iecst
(* Bad: hardcoded threshold *)
IF temperature > 85.0 THEN alarm := TRUE; END_IF;

(* Good: parameterized threshold *)
FUNCTION_BLOCK FB_ThresholdAlarm
  VAR_INPUT
    Value     : REAL;
    Threshold : REAL;     (* Caller sets the limit *)
    Hysteresis: REAL;     (* Prevents rapid toggling *)
  END_VAR
  VAR_OUTPUT
    Alarm     : BOOL;
  END_VAR

  IF Value > Threshold THEN
    Alarm := TRUE;
  ELSIF Value < (Threshold - Hysteresis) THEN
    Alarm := FALSE;
  END_IF;
END_FUNCTION_BLOCK
```

### Keep Blocks Language-Neutral

If a block's logic is written in Structured Text, it can be used from any POU regardless of the calling language. ST-based Function Blocks can be instantiated in Ladder Diagram or Function Block Diagram programs just like the standard library blocks (TON, CTU, etc.).

## Building a Personal Library

Over time, you'll build up a collection of reusable blocks. Organize them into categories:

| Category | Example Blocks |
|----------|---------------|
| **I/O Processing** | `FB_Debounce`, `FC_ScaleAnalog`, `FB_AnalogFilter` |
| **Motor Control** | `FB_MotorStarter`, `FB_VFD_Control`, `FB_SoftStart` |
| **Process Control** | `FB_PID_Basic`, `FB_RampGenerator`, `FB_Setpoint` |
| **Alarms** | `FB_ThresholdAlarm`, `FB_DeviationAlarm`, `FB_AlarmLatch` |
| **Sequencing** | `FB_Sequence`, `FB_StepTimer`, `FB_BatchControl` |
| **Utilities** | `FB_EdgeDetect`, `FC_Clamp`, `FC_Map`, `FB_Pulse` |
| **Communication** | `FB_ModbusRegMap`, `FB_DataPacket` |

See [Custom Libraries](../integration-apis/custom-libraries) for details on packaging your blocks as importable libraries.

## Testing Reusable Blocks

Before relying on a block in production:

1. **Test with boundary values**: What happens with zero, negative, or maximum inputs?
2. **Test edge cases**: What if `Enable` is toggled rapidly? What if `Start` and `Stop` are both TRUE?
3. **Test in isolation**: Use a simple test Program that exercises all inputs and monitors all outputs
4. **Verify timing**: For blocks with timers, confirm behavior across different scan rates
5. **Use the debugger**: Monitor internal variables during execution to verify state transitions

> **Tip:** The Autonomy Edge IDE's variable monitoring and console output make it easy to test blocks before deployment. See [Runtime Debugging](../troubleshooting/runtime-debugging) for details.

## What's Next?

- [Performance Optimization](performance-optimization): Write efficient code that doesn't overload the scan cycle
- [Custom Libraries](../integration-apis/custom-libraries): Package your reusable blocks into importable libraries
- [Standard Function Blocks](../../openplc-editor/standard-function-blocks/timer-blocks): Reference for the built-in blocks you can compose with
