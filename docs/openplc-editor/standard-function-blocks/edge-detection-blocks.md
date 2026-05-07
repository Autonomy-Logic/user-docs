# Edge Detection Blocks

In PLC programming, many operations need to happen **once** when a signal changes, not continuously while a signal is in a particular state. For example, you might want to increment a counter the moment a button is pressed, not on every scan cycle the button is held down. This is where edge detection comes in.

An **edge** is the transition of a boolean signal from one state to another. A **rising edge** is the transition from FALSE to TRUE. A **falling edge** is the transition from TRUE to FALSE. The IEC 61131-3 standard provides two function blocks for detecting these transitions: **R_TRIG** and **F_TRIG**. Both are available in the Autonomy Edge web IDE under **System Libraries**.

Edge detection blocks produce an output pulse that lasts for exactly **one scan cycle**. On the scan where the transition occurs, the output is TRUE. On all subsequent scans — even if the input remains in its new state — the output returns to FALSE. This one-shot behavior is what makes edge detection so useful for triggering single actions.

## Why Edge Detection Matters

Consider a button connected to a PLC input. When the operator presses the button, the input goes TRUE and stays TRUE for as long as the button is held. At a typical scan time of 10ms, holding the button for half a second means the input is TRUE for approximately 50 consecutive scans. Without edge detection, any logic that checks `IF Button THEN DoSomething` will execute 50 times. With a rising edge trigger, the action executes exactly once — on the first scan where the button is detected as TRUE.

Edge detection is also used internally by other standard function blocks. The counter blocks (CTU, CTD, CTUD) all contain built-in rising edge triggers to ensure they count transitions rather than continuous states.

## Declaring an Edge Detection Variable

To use an edge trigger in your program:

1. Open the Variables Table for your POU.
2. Add a new variable (e.g., `ButtonEdge`).
3. In the **Type** column, click the dropdown and select **System Libraries**.
4. Choose `R_TRIG` or `F_TRIG` from the list.

---

## R_TRIG — Rising Edge Trigger

The R_TRIG block detects the transition of its input from FALSE to TRUE. The output `Q` is TRUE for exactly one scan cycle on each rising edge. On all other scans, `Q` is FALSE.

### Inputs

| Name | Type | Description |
|------|------|-------------|
| `CLK` | `BOOL` | Signal to monitor for rising edges |

### Outputs

| Name | Type | Description |
|------|------|-------------|
| `Q` | `BOOL` | TRUE for one scan on each rising edge of CLK |

### Logic

The block internally remembers the previous value of `CLK`. On each scan:
1. `Q` is TRUE only if `CLK` is currently TRUE **and** it was FALSE on the previous scan — meaning this is the first scan where `CLK` is TRUE.
2. The previous value is then updated for use in the next scan.

### Timing Behavior

```
CLK:  _____|‾‾‾‾‾‾‾‾‾‾|_____|‾‾‾‾‾|_____
Q:    _____|‾|_______________|‾|__________
            ^                 ^
        rising edge       rising edge
```

Each time `CLK` transitions from FALSE to TRUE, `Q` produces a single-scan pulse. The width of the pulse in real time equals one scan cycle.

### Structured Text Example

```iecst
PROGRAM EventLogger
  VAR
    DoorSensor    : BOOL;     (* TRUE when door opens *)
    DoorOpened    : BOOL;     (* One-shot pulse on door opening *)
    OpenCount     : INT;      (* How many times the door has opened *)
    DoorEdge      : R_TRIG;   (* Detect the moment the door opens *)
  END_VAR

  DoorEdge(CLK := DoorSensor);
  DoorOpened := DoorEdge.Q;

  IF DoorOpened THEN
    OpenCount := OpenCount + 1;
  END_IF;
END_PROGRAM
```

Each time the door opens, `OpenCount` increments by exactly 1, regardless of how long the door stays open.

---

## F_TRIG — Falling Edge Trigger

The F_TRIG block detects the transition of its input from TRUE to FALSE. The output `Q` is TRUE for exactly one scan cycle on each falling edge. On all other scans, `Q` is FALSE.

### Inputs

| Name | Type | Description |
|------|------|-------------|
| `CLK` | `BOOL` | Signal to monitor for falling edges |

### Outputs

| Name | Type | Description |
|------|------|-------------|
| `Q` | `BOOL` | TRUE for one scan on each falling edge of CLK |

### Logic

The block internally remembers the previous state of `CLK`. On each scan:
1. `Q` is TRUE only if `CLK` is currently FALSE **and** it was TRUE on the previous scan — meaning `CLK` has just transitioned to FALSE.
2. The previous value is then updated for use in the next scan.

### Timing Behavior

```
CLK:  _____|‾‾‾‾‾‾‾‾‾‾|_____|‾‾‾‾‾|_____
Q:    __________________|‾|_________|‾|___
                         ^           ^
                   falling edge  falling edge
```

Each time `CLK` transitions from TRUE to FALSE, `Q` produces a single-scan pulse.

### Structured Text Example

```iecst
PROGRAM PowerMonitor
  VAR
    PowerSupplyOK : BOOL;     (* TRUE when power supply is healthy *)
    PowerLost     : BOOL;     (* One-shot pulse on power failure *)
    FailureCount  : INT;      (* Total power loss events *)
    PowerEdge     : F_TRIG;   (* Detect the moment power is lost *)
  END_VAR

  PowerEdge(CLK := PowerSupplyOK);
  PowerLost := PowerEdge.Q;

  IF PowerLost THEN
    FailureCount := FailureCount + 1;
  END_IF;
END_PROGRAM
```

Each time the power supply fails (transitions from OK to not-OK), the program registers one failure event.

---

## Comparing R_TRIG and F_TRIG

| Property | R_TRIG | F_TRIG |
|----------|--------|--------|
| Detects | FALSE → TRUE transition | TRUE → FALSE transition |
| Output duration | One scan cycle | One scan cycle |
| Common use | Button press, sensor activation | Button release, signal loss |

Both blocks are stateful — they maintain internal memory across scan cycles. This is why they must be declared as function block instances (variables), not called as simple functions.

---

## Common Edge Detection Patterns

### Button Press Detection

Detect the press (rising edge) and release (falling edge) of a button independently:

```iecst
VAR
  Button      : BOOL;
  OnPress     : BOOL;
  OnRelease   : BOOL;
  PressEdge   : R_TRIG;
  ReleaseEdge : F_TRIG;
END_VAR

PressEdge(CLK := Button);
ReleaseEdge(CLK := Button);
OnPress   := PressEdge.Q;
OnRelease := ReleaseEdge.Q;

(* OnPress is TRUE for one scan when button is pressed *)
(* OnRelease is TRUE for one scan when button is released *)
```

### Toggle Output on Button Press

Use a rising edge to flip an output each time a button is pressed:

```iecst
VAR
  ToggleButton : BOOL;
  LightOutput  : BOOL;
  BtnEdge      : R_TRIG;
END_VAR

BtnEdge(CLK := ToggleButton);

IF BtnEdge.Q THEN
  LightOutput := NOT LightOutput;
END_IF;
```

Each button press toggles the light between on and off.

### Counting Transitions

While the CTU counter block has built-in edge detection, you can also build custom counting logic using R_TRIG:

```iecst
VAR
  ProxSensor   : BOOL;
  SensorEdge   : R_TRIG;
  CustomCount  : DINT := 0;
END_VAR

SensorEdge(CLK := ProxSensor);

IF SensorEdge.Q THEN
  CustomCount := CustomCount + 1;
END_IF;
```

This approach is useful when you need custom counting behavior that the standard counter blocks don't provide, such as counting by a value other than 1 or applying conditional logic before incrementing.

### Edge Detection in Safety Logic

Detect when a safety guard opens (falling edge) to trigger an immediate shutdown:

```iecst
VAR
  GuardClosed   : BOOL;       (* TRUE = guard is closed *)
  GuardOpened   : BOOL;       (* One-scan pulse when guard opens *)
  GuardEdge     : F_TRIG;
  EmergencyStop : BOOL;
END_VAR

GuardEdge(CLK := GuardClosed);
GuardOpened := GuardEdge.Q;

IF GuardOpened THEN
  EmergencyStop := TRUE;     (* Latch the emergency stop *)
END_IF;
```

---

## What's Next?

Explore the remaining standard function blocks — including PID control, integration, differentiation, and communication blocks — in [Additional Function Blocks](other-blocks).
