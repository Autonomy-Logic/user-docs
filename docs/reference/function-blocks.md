# Standard Function Blocks Reference

A quick reference for all standard IEC 61131-3 function blocks available in the Autonomy Edge IDE through the **System Libraries**. Each block is listed with its interface, behavior summary, and a minimal usage example.

To use any of these blocks, declare a variable of the block's type in the **Variables Table** by selecting **System Libraries** from the type dropdown.

## Timers

Timers introduce time-based behavior into your PLC programs. All timers share the same interface pattern: a boolean input `IN`, a time preset `PT`, a boolean output `Q`, and an elapsed time output `ET`.

### TON — On-Delay Timer

Delays activation: `Q` goes TRUE only after `IN` has been TRUE for the duration `PT`.

| Direction | Name | Type | Description |
|-----------|------|------|-------------|
| Input | `IN` | `BOOL` | Starts the timer when TRUE |
| Input | `PT` | `TIME` | Preset delay duration |
| Output | `Q` | `BOOL` | TRUE after `ET` reaches `PT` (while `IN` is TRUE) |
| Output | `ET` | `TIME` | Elapsed time since `IN` went TRUE |

**Behavior:** When `IN` rises, `ET` counts from `T#0s` toward `PT`. When `ET >= PT`, `Q` goes TRUE. If `IN` falls before `PT`, `Q` stays FALSE and `ET` resets.

```iecst
StartDelay(IN := iStartBtn, PT := T#3s);
oMotor := StartDelay.Q;
```

### TOF — Off-Delay Timer

Extends deactivation: `Q` stays TRUE for duration `PT` after `IN` goes FALSE.

| Direction | Name | Type | Description |
|-----------|------|------|-------------|
| Input | `IN` | `BOOL` | `Q` is TRUE while `IN` is TRUE; starts countdown when FALSE |
| Input | `PT` | `TIME` | Duration `Q` stays TRUE after `IN` goes FALSE |
| Output | `Q` | `BOOL` | TRUE while `IN` is TRUE or countdown is active |
| Output | `ET` | `TIME` | Elapsed time since `IN` went FALSE |

**Behavior:** `Q` is immediately TRUE when `IN` goes TRUE. When `IN` falls, `ET` counts toward `PT`. When `ET >= PT`, `Q` goes FALSE.

```iecst
FanDelay(IN := iMotorRunning, PT := T#30s);
oFan := FanDelay.Q;
```

### TP — Pulse Timer

Generates a fixed-duration pulse: `Q` is TRUE for exactly `PT` starting on the rising edge of `IN`.

| Direction | Name | Type | Description |
|-----------|------|------|-------------|
| Input | `IN` | `BOOL` | Rising edge starts the pulse |
| Input | `PT` | `TIME` | Pulse duration |
| Output | `Q` | `BOOL` | TRUE for exactly `PT` duration |
| Output | `ET` | `TIME` | Elapsed time since pulse started |

**Behavior:** On rising edge of `IN`, `Q` goes TRUE for exactly `PT`. Not retriggerable — a new pulse only starts after the current one ends.

```iecst
AlarmPulse(IN := iFaultDetected, PT := T#5s);
oAlarmHorn := AlarmPulse.Q;
```

---

## Counters

Counters track discrete events. They count pulses on their input and compare the count to a preset value.

### CTU — Count Up

Counts rising edges on `CU`. Output `Q` goes TRUE when count value `CV` reaches preset `PV`.

| Direction | Name | Type | Description |
|-----------|------|------|-------------|
| Input | `CU` | `BOOL` | Count input (counts on rising edge) |
| Input | `R` | `BOOL` | Reset (sets `CV` to 0) |
| Input | `PV` | `INT` | Preset value (target count) |
| Output | `Q` | `BOOL` | TRUE when `CV >= PV` |
| Output | `CV` | `INT` | Current count value |

```iecst
PartCounter(CU := iPartSensor, R := iResetBtn, PV := 100);
oBatchComplete := PartCounter.Q;
lPartsCount := PartCounter.CV;
```

### CTD — Count Down

Counts down from a loaded value. Output `Q` goes TRUE when `CV` reaches zero.

| Direction | Name | Type | Description |
|-----------|------|------|-------------|
| Input | `CD` | `BOOL` | Count down input (counts on rising edge) |
| Input | `LD` | `BOOL` | Load (sets `CV` to `PV`) |
| Input | `PV` | `INT` | Preset value (loaded on `LD`) |
| Output | `Q` | `BOOL` | TRUE when `CV <= 0` |
| Output | `CV` | `INT` | Current count value |

```iecst
Remaining(CD := iDispenseSensor, LD := iRefillDone, PV := 50);
oRefillNeeded := Remaining.Q;
lItemsLeft := Remaining.CV;
```

### CTUD — Count Up/Down

Bidirectional counter that counts both up and down.

| Direction | Name | Type | Description |
|-----------|------|------|-------------|
| Input | `CU` | `BOOL` | Count up (rising edge) |
| Input | `CD` | `BOOL` | Count down (rising edge) |
| Input | `R` | `BOOL` | Reset (sets `CV` to 0) |
| Input | `LD` | `BOOL` | Load (sets `CV` to `PV`) |
| Input | `PV` | `INT` | Preset value |
| Output | `QU` | `BOOL` | TRUE when `CV >= PV` |
| Output | `QD` | `BOOL` | TRUE when `CV <= 0` |
| Output | `CV` | `INT` | Current count value |

```iecst
Inventory(CU := iItemIn, CD := iItemOut, R := iInventoryReset,
          LD := FALSE, PV := 200);
oOverstock := Inventory.QU;
oEmpty := Inventory.QD;
lStockLevel := Inventory.CV;
```

---

## Bistable (Latch) Blocks

Bistable blocks implement set/reset (latch) behavior. They maintain their output state until explicitly changed.

### SR — Set-Dominant Bistable

Set input takes priority. If both `S1` and `R` are TRUE simultaneously, output `Q1` is TRUE.

| Direction | Name | Type | Description |
|-----------|------|------|-------------|
| Input | `S1` | `BOOL` | Set input (dominant) |
| Input | `R` | `BOOL` | Reset input |
| Output | `Q1` | `BOOL` | Latched output |

**Logic:** `Q1 := S1 OR (Q1 AND NOT R)`

```iecst
AlarmLatch(S1 := iFaultDetected, R := iAcknowledgeBtn);
oAlarmLight := AlarmLatch.Q1;
```

### RS — Reset-Dominant Bistable

Reset input takes priority. If both `S` and `R1` are TRUE simultaneously, output `Q1` is FALSE.

| Direction | Name | Type | Description |
|-----------|------|------|-------------|
| Input | `S` | `BOOL` | Set input |
| Input | `R1` | `BOOL` | Reset input (dominant) |
| Output | `Q1` | `BOOL` | Latched output |

**Logic:** `Q1 := NOT R1 AND (S OR Q1)`

```iecst
MotorLatch(S := iStartBtn, R1 := iStopBtn OR iEStop);
oMotorCmd := MotorLatch.Q1;
```

**SR vs. RS — When to Use Which:**

| Scenario | Use | Reason |
|----------|-----|--------|
| Safety-critical alarm | SR (set-dominant) | Alarm stays active even if reset is accidentally pressed |
| Motor start/stop | RS (reset-dominant) | Stop always wins for safety |
| General latching | Either | Choose based on which input should win on conflict |

---

## Edge Detection Blocks

Edge detectors produce a single-scan TRUE pulse when they detect a signal transition.

### R_TRIG — Rising Edge Detector

Outputs a one-scan pulse when the input transitions from FALSE to TRUE.

| Direction | Name | Type | Description |
|-----------|------|------|-------------|
| Input | `CLK` | `BOOL` | Signal to monitor |
| Output | `Q` | `BOOL` | TRUE for one scan on rising edge |

```iecst
ButtonEdge(CLK := iButton);
IF ButtonEdge.Q THEN
    lCounter := lCounter + 1;  (* Count press events, not held state *)
END_IF;
```

### F_TRIG — Falling Edge Detector

Outputs a one-scan pulse when the input transitions from TRUE to FALSE.

| Direction | Name | Type | Description |
|-----------|------|------|-------------|
| Input | `CLK` | `BOOL` | Signal to monitor |
| Output | `Q` | `BOOL` | TRUE for one scan on falling edge |

```iecst
ReleaseDetect(CLK := iProxSensor);
IF ReleaseDetect.Q THEN
    oEjectCylinder := TRUE;  (* Trigger on sensor release *)
END_IF;
```

---

## Quick Reference Summary

| Block | Category | Inputs | Outputs | One-Line Description |
|-------|----------|--------|---------|---------------------|
| `TON` | Timer | `IN`, `PT` | `Q`, `ET` | Delays output activation by `PT` |
| `TOF` | Timer | `IN`, `PT` | `Q`, `ET` | Extends output for `PT` after input drops |
| `TP` | Timer | `IN`, `PT` | `Q`, `ET` | Fixed-duration pulse of `PT` |
| `CTU` | Counter | `CU`, `R`, `PV` | `Q`, `CV` | Counts up to `PV` |
| `CTD` | Counter | `CD`, `LD`, `PV` | `Q`, `CV` | Counts down from `PV` |
| `CTUD` | Counter | `CU`, `CD`, `R`, `LD`, `PV` | `QU`, `QD`, `CV` | Bidirectional counter |
| `SR` | Bistable | `S1`, `R` | `Q1` | Set-dominant latch |
| `RS` | Bistable | `S`, `R1` | `Q1` | Reset-dominant latch |
| `R_TRIG` | Edge | `CLK` | `Q` | Rising edge detector |
| `F_TRIG` | Edge | `CLK` | `Q` | Falling edge detector |

## Declaring Standard Function Blocks

To use any standard function block in your program:

1. Open the **Variables Table** for your POU
2. Add a new variable with a descriptive name (e.g., `StartDelay`, `PartCounter`)
3. In the **Type** column, click the dropdown and select **System Libraries**
4. Choose the desired block type (TON, CTU, SR, etc.)
5. The instance is now available in your code

You can declare multiple instances of the same type. Each instance maintains its own independent state:

```iecst
Timer1(IN := condition1, PT := T#5s);
Timer2(IN := condition2, PT := T#10s);
(* Timer1 and Timer2 are independent — different inputs, different timing *)
```

## What's Next?

- [Timer Function Blocks](../openplc-editor/standard-function-blocks/timer-blocks) — Detailed timer documentation with timing diagrams
- [Counter Function Blocks](../openplc-editor/standard-function-blocks/counter-blocks) — Detailed counter documentation
- [Data Types Reference](data-types) — Data types used by function block parameters
