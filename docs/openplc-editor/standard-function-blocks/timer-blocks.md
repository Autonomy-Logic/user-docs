# Timer Function Blocks

Timers are among the most frequently used function blocks in PLC programming. They let you introduce time-based behavior — delaying an action, holding an output for a set duration, or generating a fixed-length pulse. The IEC 61131-3 standard defines three timer function blocks, and all three are available in the Autonomy Edge web IDE as part of the **System Libraries**.

Every timer shares the same basic interface: a boolean input `IN` that triggers the timer, a time preset `PT` that defines the duration, a boolean output `Q` that reflects the timer state, and an elapsed time output `ET` that shows how much time has passed. Where they differ is in *when* `Q` becomes TRUE and how the timer responds to changes on `IN`.

## Declaring a Timer Variable

To use a timer in your program, declare a variable of the appropriate type in the **Variables Table**:

1. Open the Variables Table for your POU (Program, Function Block, or Function).
2. Add a new variable (e.g., `MyTimer`).
3. In the **Type** column, click the dropdown and select **System Libraries**.
4. Choose `TON`, `TOF`, or `TP` from the list.

The timer is now available as a local variable. You call it in your code by passing its inputs and reading its outputs.

---

## TON — On-Delay Timer

The TON block delays the activation of an output. When `IN` goes HIGH, the timer begins counting. The output `Q` goes HIGH only after the elapsed time reaches the preset `PT`. If `IN` goes LOW before `PT` is reached, the timer resets and `Q` never activates.

This is the most common timer in industrial automation. Use it whenever you need to ensure a condition has been TRUE for a minimum duration before acting on it.

### Inputs

| Name | Type | Description |
|------|------|-------------|
| `IN` | `BOOL` | Starts the timer when TRUE |
| `PT` | `TIME` | Preset time (duration before Q activates) |

### Outputs

| Name | Type | Description |
|------|------|-------------|
| `Q` | `BOOL` | TRUE when elapsed time reaches PT |
| `ET` | `TIME` | Elapsed time since IN went HIGH |

### Timing Behavior

```
IN:  _____|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|_____
           <----PT---->
Q:   _____________________|‾‾‾‾‾‾‾‾|_____
ET:  0...0 /‾‾‾‾‾‾‾‾‾‾‾PT...PT...PT 0...0
```

- When `IN` rises to TRUE, `ET` begins counting up from `T#0s`.
- When `ET` reaches `PT`, `Q` goes TRUE and `ET` holds at `PT`.
- When `IN` falls to FALSE, both `Q` and `ET` reset immediately to FALSE and `T#0s`.

### Structured Text Example

```iecst
PROGRAM ConveyorDelay
  VAR
    StartButton : BOOL;        (* Physical start button *)
    ConveyorRun : BOOL;        (* Output to motor contactor *)
    StartDelay  : TON;         (* 3-second startup delay *)
  END_VAR

  (* Only start the conveyor if the button is held for 3 seconds *)
  StartDelay(IN := StartButton, PT := T#3s);
  ConveyorRun := StartDelay.Q;
END_PROGRAM
```

In this example, the conveyor motor only starts if the operator holds the start button for a full 3 seconds. Releasing the button early resets the timer, preventing accidental activation.

---

## TOF — Off-Delay Timer

The TOF block keeps an output active for a set duration after its input goes LOW. When `IN` is HIGH, `Q` is immediately HIGH. When `IN` falls to FALSE, the timer begins counting, and `Q` stays HIGH until `ET` reaches `PT`. If `IN` goes HIGH again during the countdown, the timer resets and `Q` remains HIGH.

Use TOF when you need an output to remain active for a period after a condition is no longer met — for example, keeping a cooling fan running after a motor shuts off.

### Inputs

| Name | Type | Description |
|------|------|-------------|
| `IN` | `BOOL` | Holds output HIGH while TRUE; starts countdown when FALSE |
| `PT` | `TIME` | Duration Q stays HIGH after IN goes LOW |

### Outputs

| Name | Type | Description |
|------|------|-------------|
| `Q` | `BOOL` | TRUE while IN is HIGH or countdown is active |
| `ET` | `TIME` | Elapsed time since IN went LOW |

### Timing Behavior

```
IN:  _____|‾‾‾‾‾‾‾‾|____________________
                     <----PT---->
Q:   _____|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|________
ET:  0...0  0...0...0 /‾‾‾‾‾‾PT  0...0...0
```

- When `IN` goes HIGH, `Q` goes HIGH immediately. `ET` stays at `T#0s`.
- When `IN` falls to FALSE, `ET` begins counting up from `T#0s`.
- When `ET` reaches `PT`, `Q` goes FALSE and `ET` holds at `PT`.
- If `IN` goes HIGH again before `PT` is reached, `ET` resets to `T#0s` and `Q` stays HIGH.

### Structured Text Example

```iecst
PROGRAM CoolingFan
  VAR
    MotorRunning : BOOL;       (* TRUE while motor is active *)
    FanOutput    : BOOL;       (* Cooling fan relay *)
    FanDelay     : TOF;        (* Keep fan on 30s after motor stops *)
  END_VAR

  FanDelay(IN := MotorRunning, PT := T#30s);
  FanOutput := FanDelay.Q;
END_PROGRAM
```

The cooling fan activates whenever the motor runs. When the motor shuts off, the fan continues for 30 more seconds to let the motor cool down.

---

## TP — Pulse Timer

The TP block generates a single pulse of fixed duration. On the rising edge of `IN`, `Q` goes HIGH and stays HIGH for exactly the duration `PT`, regardless of what happens to `IN` during that time. The timer is **not retriggerable** — if `IN` goes LOW and HIGH again while the pulse is active, it's ignored. A new pulse can only begin after the current one has completed.

Use TP when you need a consistent, fixed-duration output regardless of how long the input signal lasts.

### Inputs

| Name | Type | Description |
|------|------|-------------|
| `IN` | `BOOL` | Rising edge starts the pulse |
| `PT` | `TIME` | Duration of the output pulse |

### Outputs

| Name | Type | Description |
|------|------|-------------|
| `Q` | `BOOL` | TRUE for exactly the duration PT |
| `ET` | `TIME` | Elapsed time since pulse started |

### Timing Behavior

```
IN:  _____|‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|___________
          <----PT---->
Q:   _____|‾‾‾‾‾‾‾‾‾‾|__________________
ET:  0...0 /‾‾‾‾‾‾‾PT  0...0...0...0...0
```

- On the rising edge of `IN`, `Q` goes HIGH and `ET` begins counting.
- When `ET` reaches `PT`, `Q` goes FALSE and `ET` resets to `T#0s`.
- Changes to `IN` during the pulse have no effect.
- A new pulse starts only on the next rising edge of `IN` after the previous pulse has ended.

### Structured Text Example

```iecst
PROGRAM IndicatorFlash
  VAR
    SensorTriggered : BOOL;    (* Proximity sensor input *)
    IndicatorLight  : BOOL;    (* Output to indicator lamp *)
    FlashPulse      : TP;      (* 500ms flash on each trigger *)
  END_VAR

  FlashPulse(IN := SensorTriggered, PT := T#500ms);
  IndicatorLight := FlashPulse.Q;
END_PROGRAM
```

Each time the sensor detects an object, the indicator light flashes for exactly 500 milliseconds, regardless of how long the sensor stays active.

---

## Common Timer Patterns

### Input Debouncing with TON

Mechanical switches and sensors often produce noisy signals with rapid on/off transitions. A short TON delay filters out this noise:

```iecst
(* Only accept button press if stable for 50ms *)
Debounce(IN := RawButtonInput, PT := T#50ms);
CleanButtonSignal := Debounce.Q;
```

### Delayed Shutdown with TOF

Prevent systems from shutting down too quickly by keeping outputs active after the command is removed:

```iecst
(* Keep lubrication pump running 60s after machine stops *)
LubeDelay(IN := MachineRunning, PT := T#60s);
LubePumpOutput := LubeDelay.Q;
```

### Fixed-Duration Alarm with TP

Generate a consistent alarm pulse regardless of trigger duration:

```iecst
(* Sound alarm for exactly 5 seconds on any fault *)
AlarmPulse(IN := FaultDetected, PT := T#5s);
AlarmHorn := AlarmPulse.Q;
```

### Cascaded Timers

You can chain timers together for multi-step sequences:

```iecst
(* Step 1: Wait 2s, then start pump *)
Step1_Delay(IN := StartCommand, PT := T#2s);
PumpOutput := Step1_Delay.Q;

(* Step 2: Wait 5s after pump starts, then open valve *)
Step2_Delay(IN := PumpOutput, PT := T#5s);
ValveOutput := Step2_Delay.Q;
```

---

## What's Next?

Now that you understand timers, learn about counting events and tracking quantities with [Counter Function Blocks](counter-blocks).
