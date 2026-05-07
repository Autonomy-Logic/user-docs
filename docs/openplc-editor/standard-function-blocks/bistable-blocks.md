# Bistable Function Blocks

Bistable function blocks are memory elements. They remember whether they've been "set" or "reset" and hold that state until the opposite action occurs. In electrical terms, they behave like latching relays. Once energized, they stay on until explicitly turned off.

The IEC 61131-3 standard defines two bistable blocks, **SR** and **RS**, plus a **SEMA** (semaphore) block. All three are available in the Autonomy Edge web IDE under **System Libraries**.

The critical distinction between SR and RS is which input takes priority when both the set and reset inputs are TRUE at the same time. Understanding this difference is essential for writing safe, predictable control logic.

## Declaring a Bistable Variable

To use a bistable block in your program:

1. Open the Variables Table for your POU.
2. Add a new variable (e.g., `MotorLatch`).
3. In the **Type** column, click the dropdown and select **System Libraries**.
4. Choose `SR`, `RS`, or `SEMA` from the list.

---

## SR: Set-Reset (Set Dominant)

In the SR block, the **set input dominates**. If both `S1` and `R` are TRUE simultaneously, the output `Q1` will be TRUE. This makes SR the appropriate choice when it's more important to activate than to deactivate. For example, triggering a safety alarm that must remain active even if a reset condition happens to be true at the same time.

### Inputs

| Name | Type | Description |
|------|------|-------------|
| `S1` | `BOOL` | Set input (dominant) |
| `R` | `BOOL` | Reset input |

### Outputs

| Name | Type | Description |
|------|------|-------------|
| `Q1` | `BOOL` | Latched output |

### FBD Diagram

<fbd-diagram src="/docs/diagrams/fbd/sfb-sr-basic.json"></fbd-diagram>

### Logic Equation

```
Q1 := S1 OR ((NOT R) AND Q1)
```

This means:
- If `S1` is TRUE, `Q1` is TRUE regardless of `R`.
- If `S1` is FALSE and `R` is TRUE, `Q1` is FALSE.
- If both are FALSE, `Q1` retains its previous state.

### Truth Table

| S1 | R | Q1 (previous) | Q1 (result) | Explanation |
|----|---|---------------|-------------|-------------|
| FALSE | FALSE | FALSE | FALSE | No change. Stays off |
| FALSE | FALSE | TRUE | TRUE | No change. Stays on |
| TRUE | FALSE | any | TRUE | Set wins |
| FALSE | TRUE | any | FALSE | Reset wins |
| TRUE | TRUE | any | **TRUE** | **Set dominates** |

### Structured Text Example

```iecst
PROGRAM AlarmLatch
  VAR
    FaultDetected  : BOOL;    (* Sensor or logic fault condition *)
    AcknowledgeBtn : BOOL;    (* Operator acknowledges and clears *)
    AlarmActive    : BOOL;    (* Alarm output to HMI and horn *)
    AlarmLatch     : SR;      (* Set-dominant: alarm cannot be silenced while fault exists *)
  END_VAR

  AlarmLatch(S1 := FaultDetected, R := AcknowledgeBtn);
  AlarmActive := AlarmLatch.Q1;
END_PROGRAM
```

The alarm activates when a fault is detected. The operator can only clear the alarm by pressing acknowledge **after** the fault condition has been resolved. If the fault is still active when the operator presses acknowledge, the set input dominates and the alarm stays on.

---

## RS: Reset-Set (Reset Dominant)

In the RS block, the **reset input dominates**. If both `S` and `R1` are TRUE simultaneously, the output `Q1` will be FALSE. This makes RS the appropriate choice when safety requires that the off-state takes priority. For example, a motor control where the stop command must always override the start command.

### Inputs

| Name | Type | Description |
|------|------|-------------|
| `S` | `BOOL` | Set input |
| `R1` | `BOOL` | Reset input (dominant) |

### Outputs

| Name | Type | Description |
|------|------|-------------|
| `Q1` | `BOOL` | Latched output |

### FBD Diagram

<fbd-diagram src="/docs/diagrams/fbd/sfb-rs-basic.json"></fbd-diagram>

### Logic Equation

```
Q1 := (NOT R1) AND (S OR Q1)
```

This means:
- If `R1` is TRUE, `Q1` is FALSE regardless of `S`.
- If `R1` is FALSE and `S` is TRUE, `Q1` is TRUE.
- If both are FALSE, `Q1` retains its previous state.

### Truth Table

| S | R1 | Q1 (previous) | Q1 (result) | Explanation |
|---|-----|---------------|-------------|-------------|
| FALSE | FALSE | FALSE | FALSE | No change. Stays off |
| FALSE | FALSE | TRUE | TRUE | No change. Stays on |
| TRUE | FALSE | any | TRUE | Set wins |
| FALSE | TRUE | any | FALSE | Reset wins |
| TRUE | TRUE | any | **FALSE** | **Reset dominates** |

### Structured Text Example

```iecst
PROGRAM MotorControl
  VAR
    StartButton : BOOL;       (* Momentary start pushbutton *)
    StopButton  : BOOL;       (* Momentary stop pushbutton *)
    MotorOutput : BOOL;       (* Output to motor contactor *)
    MotorLatch  : RS;         (* Reset-dominant: stop always wins *)
  END_VAR

  MotorLatch(S := StartButton, R1 := StopButton);
  MotorOutput := MotorLatch.Q1;
END_PROGRAM
```

The motor starts when the operator presses Start and stays running after the button is released (latched). Pressing Stop turns it off. If both buttons are pressed simultaneously, the stop command wins. A standard safety requirement in motor control.

---

## Choosing Between SR and RS

The choice depends on your safety requirements:

| Scenario | Recommended Block | Reason |
|----------|-------------------|--------|
| Motor start/stop | **RS** (Reset Dominant) | Stop must always override start |
| Alarm activation | **SR** (Set Dominant) | Alarm must not be silenced while the fault persists |
| Safety interlock | **RS** (Reset Dominant) | Safety shutdown must always take priority |
| Latching a request | **SR** (Set Dominant) | Request should persist until explicitly cleared |

> **Tip:** If the output being ON represents a potentially dangerous state (like a motor running), use RS so that the off-command always wins. If the output being ON represents a protective state (like an alarm or interlock), use SR so that the protection can't be bypassed.

---

## SEMA: Semaphore

The SEMA block implements a simple resource-locking mechanism. It has a `CLAIM` input and a `RELEASE` input, with a `BUSY` output that indicates whether the resource is currently claimed. Once claimed, subsequent claim attempts are ignored until the resource is released.

### Inputs

| Name | Type | Description |
|------|------|-------------|
| `CLAIM` | `BOOL` | Request to claim the resource |
| `RELEASE` | `BOOL` | Request to release the resource |

### Outputs

| Name | Type | Description |
|------|------|-------------|
| `BUSY` | `BOOL` | TRUE when the resource is currently claimed |

### FBD Diagram

<fbd-diagram src="/docs/diagrams/fbd/sfb-sema-basic.json"></fbd-diagram>

### Behavior

- When `CLAIM` transitions to TRUE and the resource is not busy, `BUSY` goes TRUE.
- When `RELEASE` is TRUE, `BUSY` goes FALSE.
- If the resource is already busy, additional `CLAIM` signals are ignored.

### Structured Text Example

```iecst
PROGRAM SharedPrinter
  VAR
    Station1Request : BOOL;   (* Station 1 wants the printer *)
    Station1Done    : BOOL;   (* Station 1 finished printing *)
    PrinterBusy     : BOOL;   (* Printer is currently in use *)
    PrinterLock     : SEMA;   (* Semaphore for exclusive access *)
  END_VAR

  PrinterLock(CLAIM := Station1Request, RELEASE := Station1Done);
  PrinterBusy := PrinterLock.BUSY;
END_PROGRAM
```

---

## Common Bistable Patterns

### Motor Start/Stop with Safety Interlock

Combine RS with an external safety condition:

```iecst
(* Motor can only start if guard is closed, stop always wins *)
MotorLatch(S := StartBtn AND GuardClosed, R1 := StopBtn OR NOT GuardClosed);
MotorRun := MotorLatch.Q1;
```

If the safety guard opens, the reset input goes TRUE and the motor stops immediately. The motor can't restart until the guard is closed again.

### Alarm Latching with Acknowledgment

Use SR to create an alarm that must be acknowledged after the fault clears:

```iecst
(* Alarm stays active until BOTH: fault clears AND operator acknowledges *)
AlarmLatch(S1 := FaultCondition, R := AckButton AND NOT FaultCondition);
AlarmOutput := AlarmLatch.Q1;
```

The reset condition requires that the acknowledge button is pressed AND the fault is no longer present. This prevents operators from dismissing active faults.

---

## What's Next?

Understand how to detect signal transitions. A fundamental building block used inside counters and many control patterns. With [Edge Detection Blocks](edge-detection-blocks).
