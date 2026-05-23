# Function blocks and functions in Ladder Diagram

Contacts and coils only deal with `BOOL` signals. The moment you need a timer, a counter, an integer comparison, or any maths, you reach for a **function** or **function block** placed inline on the rung. This page covers how those fit into the LD model and the one detail that trips up almost every new LD user: **execution control**.

## What a block looks like in LD

A function or function block appears as a rectangular box on the rung:

- **Name** at the top (e.g. `TON`, `CTU`, `GT`, `ADD`).
- **Input pins** on the left, with their pin names (`IN`, `PT`, `IN1`, `IN2`, …).
- **Output pins** on the right (`Q`, `ET`, `OUT`, …).
- A small variable label above each pin where you bind a project variable.

For a function block (stateful), you also bind an **instance name** above the block, that's the variable you declared as type `TON` / `CTU` / `PID` / etc.

## Placing a block

Two ways:

- Click **Block** in the activity-bar toolbox while an LD body is active, then drop it on a rung position.
- Drag a block from the **Library** panel directly onto a rung.

In either case a picker opens letting you choose the specific block (system library, project user libraries, or your own POUs).

## The one rule that makes LD click

> **Contacts and coils can be placed on any BOOL input or output pin of a block.**

That's the whole game. The left and right power rails are just the most obvious BOOL connection points; every `BOOL` pin on a block is equally valid as somewhere to attach a contact, a coil, or a rung wire.

Concrete examples:

- A `TON` block has BOOL pins `IN` (input) and `Q` (output). You can wire the rung's left rail to `IN` and `Q` straight out to a coil on the right rail, the rung flows *through* the timer.
- A `CTU` counter has BOOL pins `CU` (count up) and `R` (reset) on the input side, plus `Q` (output). Drive `R` from a normally-closed reset contact, `CU` from a rising-edge source, and `Q` straight to a coil.
- An `R_TRIG` edge detector exposes a BOOL `Q` output: take it straight to a coil.

This is why function blocks like `TON` feel "naturally inline" in a rung: they have BOOL pins on both sides, so the rung wire has somewhere to land.

## The gotcha: blocks with no BOOL inputs

Comparison and arithmetic blocks (`GT`, `EQ`, `LT`, `ADD`, `MUL`, `SEL`, `MAX`, …) have **no BOOL input pins**. Their inputs are numbers; their output is either a number (`ADD`, `MUL`) or a single BOOL (`GT`, `EQ`).

When you drop one of these onto a rung, the rung wire has nowhere to land on the input side, so the editor attaches the block to **the top power rail**, dangling above your rung. Lots of new users get stuck here, certain they're doing something wrong because the block won't sit inline. **It's not a bug. The default placement just doesn't have a BOOL pin to enter on.**

You have two ways out:

1. **Leave the block where it is and ignore the rail attachment.** The block computes every scan regardless. Use its output (e.g. `GT.OUT`) like any other BOOL signal, drive a coil from it, gate a downstream block, etc.
2. **Turn on execution control.** This adds `EN` and `ENO` pins to the block, giving you an explicit BOOL way in and out. The block can then be wired into a rung's power flow like a regular FB.

## Execution control (EN / ENO)

Every block has an **Execution Control** flag (defaults to **off**). To toggle it:

1. **Double-click the block** in the rung. The **Block Properties** dialog opens.

   ![Block Properties dialog for a TON: Type picker on the left (iec-std-functions, iec-standard-fb, additional-function-blocks, oscat-basic, User Libraries), Name field, Execution Order, Execution Control toggle (off), Preview showing the block's pins. The TON preview shows IN/Q/PT/ET only](../images/block-properties-ton.png)

2. Flip **Execution Control** to **on**. The preview updates to show the block with `EN` (above the inputs) and `ENO` (above the outputs).

   ![Same dialog with Execution Control toggled on; the preview now shows the TON with EN and ENO pins added above the IN/Q/PT/ET pins](../images/block-properties-ton-eneno.png)

3. Click **OK**. The block in your rung redraws with the new pins.

### What EN and ENO do

- **`EN`** (input): when `TRUE`, the block executes this scan. When `FALSE`, the block is skipped, outputs retain their previous values.
- **`ENO`** (output): mirrors `EN`. `TRUE` while the block is executing, `FALSE` when skipped.

The combination gives you an explicit BOOL chain you can wire into a rung:

```
left rail → contact → EN | block | ENO → coil → right rail
```

### When to use each mode

| Mode | Best for |
|---|---|
| **Execution Control off** (default) | Stateless data-flow blocks: a `GT` that computes every scan and feeds its OUT into other logic, an `ADD` whose result is consumed downstream, an `MUX` selecting one of N values. |
| **Execution Control on** | Blocks you want to skip under some condition (saves cycles, prevents side effects), or any block you want visually inline between a contact and a coil. |

For stateful function blocks (`TON`, `CTU`, etc.) that already have BOOL pins like `IN` / `Q`, you usually don't *need* execution control, wiring the rung through `IN`/`Q` works the same way `EN`/`ENO` would. Execution control is the universal solution; using the block's own BOOL pins is the lighter-touch idiomatic LD way.

## Connecting variables to non-BOOL pins

For non-BOOL pins (`INT`, `REAL`, `TIME`, etc.) you don't wire physically, you **type the variable name** into the small text field next to the pin. The editor autocompletes from your variable table, filtered to types compatible with the pin.

- Inputs accept any variable, constant literal (`5`, `T#500ms`, `2.5`), or output of an upstream block.
- Outputs write into the named variable each scan they execute.

If the variable doesn't exist yet, just type the new name, the editor offers to add it to the variable table.

## User-authored function blocks

Any `function-block` POU you create in your project appears in the block picker's **User Libraries** section. You drop it and wire it exactly like a standard block; the editor reads your block's variable interface (inputs / outputs) to determine the pins.

You declare an instance variable to hold the block's state (`my_filter : MyFilter;`) and bind that instance to the block when you place it.

## A practical example: motor start with timer

```
Variables:
  start_cmd     : BOOL          (start command)
  e_stop        : BOOL          (emergency stop, NC contact)
  delay_timer   : TON           (3 s startup delay)
  motor_run     : BOOL          (motor output)
```

**Rung 1, start the timer when the operator presses start, gated by E-stop:**

<LadderDiagramViewer src="/docs/diagrams/ladder/fb-ton-timer.json" />

**Rung 2, drive the motor output from the timer's `Q`:**

<LadderDiagramViewer src="/docs/diagrams/ladder/fb-ton-output.json" />

The contact on `start_cmd` and the NC contact on `e_stop` both feed into the TON's `IN` BOOL pin (no execution control needed, the rung wire lands on `IN` directly). After 3 seconds, `delay_timer.Q` goes `TRUE` and rung 2's coil energises `motor_run`.

## Block reference

The detailed per-block pages cover pin types, behaviour, timing diagrams, and common patterns:

- **[Timer blocks](../../standard-function-blocks/timer-blocks)**: `TON`, `TOF`, `TP`
- **[Counter blocks](../../standard-function-blocks/counter-blocks)**: `CTU`, `CTD`, `CTUD` (and type-suffixed variants)
- **[Edge detection blocks](../../standard-function-blocks/edge-detection-blocks)**: `R_TRIG`, `F_TRIG`
- **[Bistable blocks](../../standard-function-blocks/bistable-blocks)**: `SR`, `RS`, `SEMA`
- **[Other standard blocks](../../standard-function-blocks/other-blocks)**: `RTC`, `INTEGRAL`, `DERIVATIVE`, `PID`, `RAMP`, `HYSTERESIS`

The IEC standard **functions** (comparison, arithmetic, bit-shift, type conversion, etc.) live in the `iec-std-functions` library, see the **[Library Manager](../../standard-function-blocks/library-manager)** page for how to enable them and where to find them in the picker.

## What's next

- **[LD Editor Features](ld-editor)**: toolbox, selection, multi-select, rung management.
- **[Worked example: Motor start / stop with seal-in](../../examples/start-stop-seal-in)**: applies everything on this page in a single rung.
- **[FBD Basics](../function-block-diagram/fbd-basics)**: the fully-graphical cousin of LD.
