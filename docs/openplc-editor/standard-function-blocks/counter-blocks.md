# Counter Function Blocks

Counters track how many times an event occurs. Every time a boolean input transitions from FALSE to TRUE (a **rising edge**), the counter increments or decrements an internal count value. The IEC 61131-3 standard defines three counter types: **CTU** (count up), **CTD** (count down), and **CTUD** (count up and down). All three are available in the Autonomy Edge web IDE under **System Libraries**.

Counters are essential in industrial automation for tasks like counting parts on a conveyor, tracking batches, monitoring machine cycles, or measuring position in stepper-motor applications.

## How Counters Detect Edges

An important detail about counters: they count **transitions**, not continuous states. If an input stays HIGH for multiple scan cycles, the counter increments only once. On the first scan where the input transitions from FALSE to TRUE.

You don't need to add your own edge detection when using counters. The edge detection is built in.

## Declaring a Counter Variable

To use a counter in your program:

1. Open the Variables Table for your POU.
2. Add a new variable (e.g., `PartCounter`).
3. In the **Type** column, click the dropdown and select **System Libraries**.
4. Choose `CTU`, `CTD`, or `CTUD` from the list.

The counter is now available as a local variable in your code.

---

## CTU: Up Counter

The CTU block counts upward from zero. Each rising edge on the `CU` input increments the current value `CV` by one. The output `Q` becomes TRUE when `CV` reaches or exceeds the preset value `PV`. The reset input `R` sets `CV` back to zero at any time.

### Inputs

| Name | Type | Description |
|------|------|-------------|
| `CU` | `BOOL` | Count Up. Increments CV on each rising edge |
| `R` | `BOOL` | Reset. Sets CV to 0 when TRUE |
| `PV` | `INT` | Preset Value. Target count |

### Outputs

| Name | Type | Description |
|------|------|-------------|
| `Q` | `BOOL` | TRUE when CV >= PV |
| `CV` | `INT` | Current Value. The running count |

### FBD Diagram

<fbd-diagram src="/docs/diagrams/fbd/sfb-ctu-basic.json"></fbd-diagram>

### Behavior

1. On each scan, the block checks for a rising edge on `CU`.
2. If a rising edge is detected, `CV` increments by 1.
3. If `R` is TRUE, `CV` is reset to 0 (reset takes priority over counting).
4. `Q` is evaluated as `CV >= PV`.

### Structured Text Example

```iecst
PROGRAM BatchCounter
  VAR
    PartSensor   : BOOL;      (* Sensor detects each part *)
    ResetButton  : BOOL;      (* Operator reset *)
    BatchComplete: BOOL;      (* TRUE when batch is done *)
    PartsCount   : INT;       (* Current count for display *)
    Counter      : CTU;       (* Count up to 50 parts *)
  END_VAR

  Counter(CU := PartSensor, R := ResetButton, PV := 50);
  BatchComplete := Counter.Q;
  PartsCount    := Counter.CV;
END_PROGRAM
```

Each time the part sensor transitions to TRUE, the counter increments. When 50 parts have been counted, `BatchComplete` goes TRUE. The operator can press `ResetButton` to start a new batch.

---

## CTD: Down Counter

The CTD block counts downward from a loaded value. When the load input `LD` is TRUE, `CV` is loaded with the preset value `PV`. Each rising edge on the `CD` input decrements `CV` by one. The output `Q` becomes TRUE when `CV` reaches zero or goes below it.

### Inputs

| Name | Type | Description |
|------|------|-------------|
| `CD` | `BOOL` | Count Down. Decrements CV on each rising edge |
| `LD` | `BOOL` | Load. Loads PV into CV when TRUE |
| `PV` | `INT` | Preset Value. The starting count |

### Outputs

| Name | Type | Description |
|------|------|-------------|
| `Q` | `BOOL` | TRUE when CV <= 0 |
| `CV` | `INT` | Current Value. The remaining count |

### FBD Diagram

<fbd-diagram src="/docs/diagrams/fbd/sfb-ctd-basic.json"></fbd-diagram>

### Behavior

1. If `LD` is TRUE, `CV` is set to `PV` (load takes priority over counting).
2. On each rising edge of `CD`, `CV` decrements by 1.
3. `Q` is evaluated as `CV <= 0`.

### Structured Text Example

```iecst
PROGRAM Dispenser
  VAR
    ItemDispensed : BOOL;      (* Sensor confirms an item left *)
    LoadCommand   : BOOL;      (* Operator loads new batch *)
    HopperEmpty   : BOOL;      (* TRUE when all items dispensed *)
    Remaining     : INT;       (* Items left *)
    DownCounter   : CTD;       (* Count down from 100 *)
  END_VAR

  DownCounter(CD := ItemDispensed, LD := LoadCommand, PV := 100);
  HopperEmpty := DownCounter.Q;
  Remaining   := DownCounter.CV;
END_PROGRAM
```

The operator presses `LoadCommand` to initialize the counter to 100. Each dispensed item decrements the count. When the count reaches zero, `HopperEmpty` signals that the hopper needs refilling.

---

## CTUD: Up-Down Counter

The CTUD block combines both counting directions. It can count up on one input and count down on another, simultaneously. It has two output flags: `QU` indicates the count has reached or exceeded the preset, and `QD` indicates the count has reached zero or below.

### Inputs

| Name | Type | Description |
|------|------|-------------|
| `CU` | `BOOL` | Count Up. Increments CV on each rising edge |
| `CD` | `BOOL` | Count Down. Decrements CV on each rising edge |
| `R` | `BOOL` | Reset. Sets CV to 0 when TRUE |
| `LD` | `BOOL` | Load. Loads PV into CV when TRUE |
| `PV` | `INT` | Preset Value. Upper threshold for QU |

### Outputs

| Name | Type | Description |
|------|------|-------------|
| `QU` | `BOOL` | TRUE when CV >= PV |
| `QD` | `BOOL` | TRUE when CV <= 0 |
| `CV` | `INT` | Current Value |

### FBD Diagram

<fbd-diagram src="/docs/diagrams/fbd/sfb-ctud-basic.json"></fbd-diagram>

### Behavior

1. If `R` is TRUE, `CV` is set to 0.
2. If `LD` is TRUE, `CV` is loaded with `PV`.
3. On a rising edge of `CU`, `CV` increments by 1.
4. On a rising edge of `CD`, `CV` decrements by 1.
5. `QU` is evaluated as `CV >= PV`.
6. `QD` is evaluated as `CV <= 0`.

If both `CU` and `CD` have rising edges on the same scan, both operations execute and the net count does not change.

### Structured Text Example

```iecst
PROGRAM ParkingGarage
  VAR
    EntrySensor  : BOOL;      (* Car entering the garage *)
    ExitSensor   : BOOL;      (* Car leaving the garage *)
    ResetCount   : BOOL;      (* Midnight reset *)
    GarageFull   : BOOL;      (* TRUE when capacity reached *)
    GarageEmpty  : BOOL;      (* TRUE when no cars inside *)
    OccupiedSpots: INT;       (* Number of cars currently parked *)
    Tracker      : CTUD;      (* Track occupancy, max 200 *)
  END_VAR

  Tracker(CU := EntrySensor, CD := ExitSensor,
          R := ResetCount, LD := FALSE, PV := 200);
  GarageFull    := Tracker.QU;
  GarageEmpty   := Tracker.QD;
  OccupiedSpots := Tracker.CV;
END_PROGRAM
```

Cars entering the garage increment the count; cars leaving decrement it. When the garage reaches its 200-space capacity, `GarageFull` activates, which could trigger a "FULL" sign at the entrance.

---

## Data Type Variants

Each counter is available in multiple variants to accommodate different integer sizes. The standard `CTU`, `CTD`, and `CTUD` use `INT` (16-bit signed). Wider variants are available for applications that need larger ranges:

| Variant | CV / PV Type | Range |
|---------|-------------|-------|
| `CTU` / `CTD` / `CTUD` | `INT` | -32,768 to 32,767 |
| `CTU_DINT` / `CTD_DINT` / `CTUD_DINT` | `DINT` | -2,147,483,648 to 2,147,483,647 |
| `CTU_LINT` / `CTD_LINT` / `CTUD_LINT` | `LINT` | 64-bit signed integer |
| `CTU_UDINT` / `CTD_UDINT` / `CTUD_UDINT` | `UDINT` | 0 to 4,294,967,295 |
| `CTU_ULINT` / `CTD_ULINT` / `CTUD_ULINT` | `ULINT` | 64-bit unsigned integer |

For most applications, the standard `INT` variant is sufficient. Use `DINT` or wider variants when counting large numbers of events (e.g., total machine cycles over a long production run) where the standard `INT` range of 32,767 may overflow.

To use a variant, select it from System Libraries just as you would the standard version. For example, declare a variable of type `CTU_DINT` instead of `CTU`.

---

## Common Counter Patterns

### Batch Counting with Auto-Reset

Automatically reset the counter and trigger an action every N events:

```iecst
(* Count 12 items per box, then signal box-full and reset *)
BoxCounter(CU := ItemSensor, R := BoxFull, PV := 12);
BoxFull := BoxCounter.Q;
```

When `BoxFull` goes TRUE, it immediately feeds back to the reset input `R`, which sets `CV` back to 0 on the next scan. This creates a repeating cycle.

### Position Tracking with CTUD

Track a position that moves in both directions:

```iecst
(* Track stepper motor position with forward/reverse pulses *)
PositionTracker(CU := ForwardPulse, CD := ReversePulse,
                R := HomeSwitch, LD := FALSE, PV := 1000);
AtEndOfTravel := PositionTracker.QU;
AtHome        := PositionTracker.QD;
CurrentPos    := PositionTracker.CV;
```

---

## What's Next?

Learn how to latch outputs and create memory elements with [Bistable Function Blocks](bistable-blocks).
